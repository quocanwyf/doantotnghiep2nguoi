"""Score only the pre-locked T-023 BFW development split with frozen MobileFaceNet.

Raw scores remain outside Git. Evaluation records are never loaded into a
scoring loop, and this script cannot select a model or deployment threshold.
"""

from __future__ import annotations

import argparse
import json
import os
import platform
import time
import zipfile
from collections import Counter
from pathlib import Path

import cv2
import numpy as np
import onnxruntime as ort
from insightface import __version__ as insightface_version
from insightface.app import FaceAnalysis

from t011_xqlfw_baseline import prepare_pack
from t017_s4_run import DELTA, TAU, get_faces, select_p2
from t022_s8_development import describe, threshold_row
from t023_build_bfw import INNER_MD5, digest, encoded, get_image, letterbox
from t023_detector_audit import MODEL_SHA256


LOCK_SHA256 = "d586d97f1656a7f83b5ae37410b87ff0a0a95997e687d0ed47673205a38aec3b"
EXPECTED_ONNX = {
    "det_500m.onnx": "5e4447f50245bbd7966bd6c0fa52938c61474a04ec7def48753668a9d8b4ea3a",
    "w600k_mbf.onnx": "9cc6e4a75f0e2bf0b1aed94578f144d15175f357bdc05e815e5c4a02b319eb4f",
}
REFERENCE_THETAS = (0.122254, 0.15, 0.25, TAU)


def write_once(path: Path, value: object) -> None:
    if path.exists():
        raise FileExistsError(f"Refusing to overwrite {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(encoded(value))


def features(app: FaceAnalysis, image: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    ok, buffer = cv2.imencode(".png", image)
    if not ok:
        raise ValueError("Unable to encode image")
    faces, vectors, _, _ = get_faces(app, buffer.tobytes())
    boxes = np.asarray([face.bbox for face in faces], dtype=float).reshape(-1, 4)
    return boxes, vectors


def score_split(locked: dict, images: Path, model: Path, cache: Path,
                locked_root: Path, group: str) -> tuple[list[dict], list[dict], dict]:
    """Shared frozen scoring method; caller decides if a split may be opened."""
    if group not in ("development", "evaluation"):
        raise ValueError("Unknown split")
    pairs = [r for r in locked["pairs"] if r["group"] == group and r["lock_status"] == "USABLE_SOURCE_LABEL"]
    scenes = [r for r in locked["scenes"] if r["group"] == group and r["lock_status"] == "USABLE_SOURCE_AND_SELF_REVIEW"]
    required = {member for row in pairs for member in (row["left"], row["right"])}
    required.update(member for row in scenes for member in (row["reference_member"], *row["panel_members"]))
    started = time.monotonic()
    with zipfile.ZipFile(images) as image_archive, zipfile.ZipFile(model) as model_archive:
        root, onnx_hashes = prepare_pack(model_archive, cache)
        if onnx_hashes != EXPECTED_ONNX:
            raise ValueError("Frozen detector/encoder weights differ")
        app = FaceAnalysis(name="buffalo_sc", root=str(root),
                           allowed_modules=["detection", "recognition"],
                           providers=["CPUExecutionProvider"])
        app.prepare(ctx_id=-1, det_size=(640, 640), det_thresh=0.5)
        if set(app.models) != {"detection", "recognition"}:
            raise ValueError("Unexpected model modules")
        lookup = {"/".join(Path(name).parts[-3:]): name for name in image_archive.namelist()
                  if name.lower().endswith(".jpg")}
        if not required <= set(lookup):
            raise ValueError("Missing image from frozen BFW archive")
        vectors = {}
        for number, member in enumerate(sorted(required), 1):
            face = letterbox(get_image(image_archive, lookup, member))
            boxes, embeddings = features(app, face)
            if len(boxes) != 1:
                raise ValueError("Locked source detector count changed")
            vectors[member] = embeddings[0]
            if number % 500 == 0:
                print(f"T-023 {group} source embeddings {number}/{len(required)}", flush=True)
        pair_rows = [{"pair": row["pair"], "genuine": row["genuine"],
                      "score": float(vectors[row["left"]] @ vectors[row["right"]])}
                     for row in pairs]
        scene_rows = []
        for number, row in enumerate(scenes, 1):
            scene_file = locked_root / row["scene_file"]
            if digest(scene_file) != row["scene_sha256"]:
                raise ValueError("Frozen scene image changed")
            frame = cv2.imread(str(scene_file))
            if frame is None:
                raise ValueError("Frozen scene cannot be read")
            boxes, embeddings = features(app, frame)
            if len(boxes) != 2:
                raise ValueError("Frozen scene detector count changed")
            by_panel = sorted(range(2), key=lambda i: (boxes[i][0] + boxes[i][2]) / 2)
            audit_boxes = sorted(row["detector_boxes"], key=lambda x: x["panel"])
            if [b["panel"] for b in audit_boxes] != [0, 1]:
                raise ValueError("Frozen panel map differs")
            if any(np.max(np.abs(boxes[by_panel[panel]] - np.asarray(audit_boxes[panel]["xyxy"]))) > 1.0
                   for panel in (0, 1)):
                raise ValueError("Frozen detector boxes changed")
            scores = [float(embedding @ vectors[row["reference_member"]]) for embedding in embeddings]
            selected = select_p2(scores, TAU, DELTA)
            selected_panel = by_panel.index(selected) if selected is not None else None
            if selected is None:
                outcome = "UNRESOLVED" if row["kind"] == "present" else "NO_FACE_SELECTED"
            elif row["kind"] == "absent":
                outcome = "FALSE_SELECTION"
            else:
                outcome = "CORRECT_TARGET" if selected_panel == row["target_panel"] else "WRONG_TARGET"
            scene_rows.append({"trial": row["trial"], "anchor": row["anchor"],
                               "kind": row["kind"], "stratum": row["stratum"],
                               "target_panel": row["target_panel"], "scores_by_detection": scores,
                               "selected_detection": selected, "selected_panel": selected_panel,
                               "selected_score": scores[selected] if selected is not None else None,
                               "top_score": max(scores), "margin": abs(scores[0] - scores[1]),
                               "s4_outcome": outcome})
            if number % 50 == 0:
                print(f"T-023 {group} controlled scenes {number}/{len(scenes)}", flush=True)
    return pair_rows, scene_rows, {"runtime_seconds": time.monotonic() - started,
                                    "model_onnx_sha256": onnx_hashes}


def summarize(pairs: list[dict], scenes: list[dict]) -> dict:
    genuine = [r["score"] for r in pairs if r["genuine"]]
    ordinary = [r["score"] for r in pairs if not r["genuine"]]
    selected_genuine = [r["selected_score"] for r in scenes if r["s4_outcome"] == "CORRECT_TARGET"]
    hard = [r["selected_score"] for r in scenes if r["s4_outcome"] in ("FALSE_SELECTION", "WRONG_TARGET")]
    grid = sorted(set([round(-1 + i * 0.01, 8) for i in range(201)] + list(REFERENCE_THETAS)))
    return {
        "denominators": {"genuine_pair": len(genuine), "ordinary_pair": len(ordinary),
                         "present_scene": sum(r["kind"] == "present" for r in scenes),
                         "absent_scene": sum(r["kind"] == "absent" for r in scenes),
                         "selected_genuine": len(selected_genuine), "s4_hard_negative": len(hard),
                         "hard_anchor": len({r["anchor"] for r in scenes if r["s4_outcome"] in ("FALSE_SELECTION", "WRONG_TARGET")})},
        "s4_outcomes": {kind: dict(Counter(r["s4_outcome"] for r in scenes if r["kind"] == kind))
                        for kind in ("present", "absent")},
        "s4_absent_strata": {kind: dict(Counter(r["s4_outcome"] for r in scenes
                                               if r["kind"] == "absent" and r["stratum"] == kind))
                             for kind in ("random", "challenge")},
        "score_distribution": {"genuine_pair": describe(genuine),
                               "ordinary_impostor_pair": describe(ordinary),
                               "s4_selected_genuine": describe(selected_genuine),
                               "s4_derived_hard_negative": describe(hard)},
        "threshold_grid": [threshold_row(t, pairs, scenes) for t in grid],
        "threshold_grid_note": "Predeclared descriptive grid [-1,1] step 0.01 plus four reference scores; no selection from evaluation",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("locked", "images", "model", "cache", "raw-output", "summary-output"):
        parser.add_argument("--" + name, required=True, type=Path)
    args = parser.parse_args()
    if args.raw_output.exists() or args.summary_output.exists():
        parser.error("Refusing to overwrite development outputs")
    if digest(args.locked) != LOCK_SHA256 or digest(args.images, "md5") != INNER_MD5:
        raise ValueError("Benchmark source/lock differs")
    if digest(args.model) != MODEL_SHA256:
        raise ValueError("MobileFaceNet model pack differs")
    locked = json.loads(args.locked.read_text(encoding="utf-8"))
    if locked["recognition_scores_read"] is not False:
        raise ValueError("Ground truth was not locked before score")
    pairs, scenes, run = score_split(locked, args.images, args.model, args.cache,
                                     args.locked.parent, "development")
    raw = {"scope": "T-023 BFW development only; evaluation not opened",
           "lock_sha256": LOCK_SHA256, "code_sha256": digest(Path(__file__)),
           "model_pack_sha256": MODEL_SHA256, "p2_parameters": {"tau": TAU, "delta": DELTA},
           "pairs": pairs, "scenes": scenes}
    write_once(args.raw_output, raw)
    summary = {"scope": raw["scope"], "lock_sha256": LOCK_SHA256,
               "raw_sha256": digest(args.raw_output), "code_sha256": raw["code_sha256"],
               "model_pack_sha256": MODEL_SHA256, **run, **summarize(pairs, scenes),
               "environment": {"python": platform.python_version(), "platform": platform.platform(),
                               "logical_cpus": os.cpu_count(), "opencv": cv2.__version__,
                               "onnxruntime": ort.__version__, "insightface": insightface_version,
                               "numpy": np.__version__, "provider": "CPUExecutionProvider"}}
    write_once(args.summary_output, summary)
    print(json.dumps({"raw_sha256": digest(args.raw_output),
                      "summary_sha256": digest(args.summary_output),
                      "denominators": summary["denominators"],
                      "s4_outcomes": summary["s4_outcomes"],
                      "score_distribution": summary["score_distribution"],
                      "runtime_seconds": run["runtime_seconds"]}, indent=2))


if __name__ == "__main__":
    main()
