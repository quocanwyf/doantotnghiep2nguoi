"""Run T-022 development only on the pre-score locked controlled proxy.

Evaluation images and pair scores are never opened. This script describes the
full S8 score/decision trade-off; it does not choose an operating threshold.
Raw scores stay outside Git.
"""

from __future__ import annotations

import argparse
import hashlib
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


LOCK_SHA256 = "d752c99fae5071c2aedb7fe0e40842b8b25c05decf539b61df8e988fee8ec131"
MODEL_SHA256 = "57d31b56b6ffa911c8a73cfc1707c73cab76efe7f13b675a05223bf42de47c72"
EXPECTED_ONNX = {
    "det_500m.onnx": "5e4447f50245bbd7966bd6c0fa52938c61474a04ec7def48753668a9d8b4ea3a",
    "w600k_mbf.onnx": "9cc6e4a75f0e2bf0b1aed94578f144d15175f357bdc05e815e5c4a02b319eb4f",
}


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def write_once(path: Path, value: object) -> None:
    if path.exists():
        raise FileExistsError(f"Refusing to overwrite {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    data = json.dumps(value, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":"), allow_nan=False) + "\n"
    path.write_text(data, encoding="utf-8")


def image_features(app: FaceAnalysis, encoded: bytes) -> tuple[np.ndarray, np.ndarray]:
    faces, vectors, _, _ = get_faces(app, encoded)
    boxes = np.asarray([face.bbox for face in faces], dtype=float).reshape(-1, 4)
    return boxes, vectors


def describe(scores: list[float]) -> dict:
    if not scores:
        return {"n": 0, "min": None, "p05": None, "p25": None,
                "median": None, "p75": None, "p95": None, "max": None}
    values = np.asarray(scores, dtype=float)
    return {"n": len(scores), "min": float(values.min()),
            "p05": float(np.percentile(values, 5)),
            "p25": float(np.percentile(values, 25)),
            "median": float(np.median(values)),
            "p75": float(np.percentile(values, 75)),
            "p95": float(np.percentile(values, 95)),
            "max": float(values.max())}


def threshold_row(theta: float, pairs: list[dict], scenes: list[dict]) -> dict:
    genuine = [r for r in pairs if r["genuine"]]
    ordinary = [r for r in pairs if not r["genuine"]]
    selected_genuine = [r for r in scenes if r["kind"] == "present" and r["s4_outcome"] == "CORRECT_TARGET"]
    hard = [r for r in scenes if r["s4_outcome"] in ("WRONG_TARGET", "FALSE_SELECTION")]
    absent = [r for r in scenes if r["kind"] == "absent"]
    false_selected_absent = [r for r in absent if r["s4_outcome"] == "FALSE_SELECTION"]
    result = {
        "theta": theta,
        "genuine_pair": {"n": len(genuine), "accept": sum(r["score"] >= theta for r in genuine),
                         "reject": sum(r["score"] < theta for r in genuine)},
        "ordinary_impostor_pair": {"n": len(ordinary), "accept": sum(r["score"] >= theta for r in ordinary),
                                   "reject": sum(r["score"] < theta for r in ordinary)},
        "s4_selected_genuine": {"n": len(selected_genuine),
                                "accept": sum(r["selected_score"] >= theta for r in selected_genuine),
                                "reject": sum(r["selected_score"] < theta for r in selected_genuine)},
        "s4_derived_hard_negative": {"n": len(hard),
                                     "accept": sum(r["selected_score"] >= theta for r in hard),
                                     "reject": sum(r["selected_score"] < theta for r in hard)},
        "absent_pipeline": {"all_absent": len(absent),
                            "s4_no_select": sum(r["s4_outcome"] == "NO_FACE_SELECTED" for r in absent),
                            "s4_false_select": len(false_selected_absent),
                            "s8_accept_after_false_select": sum(r["selected_score"] >= theta for r in false_selected_absent),
                            "s8_reject_after_false_select": sum(r["selected_score"] < theta for r in false_selected_absent)},
    }
    return result


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    for name in ("locked", "images", "model", "cache", "raw-output", "summary-output"):
        p.add_argument("--" + name, required=True, type=Path)
    args = p.parse_args()
    if args.raw_output.exists() or args.summary_output.exists():
        p.error("Outputs must not exist; this is one development run")
    if digest(args.locked) != LOCK_SHA256:
        raise ValueError("Locked benchmark changed after label audit")
    locked = json.loads(args.locked.read_text(encoding="utf-8"))
    if locked["recognition_scores_read"] is not False or locked["seed"] != "T-022-controlled-two-face-v1":
        raise ValueError("Locked benchmark provenance differs")
    if digest(args.images) != locked["source_sha256"]["images"] or digest(args.model) != MODEL_SHA256:
        raise ValueError("XQLFW or frozen model pack changed")
    pairs = [row for row in locked["pairs"]["development"] if row["lock_status"] == "USABLE_SOURCE_LABEL"]
    scenes = [row for row in locked["scenes"] if row["group"] == "development" and row["lock_status"] == "USABLE_SELF_CONFIRMED"]
    if Counter(row["kind"] for row in scenes) != {"present": 32, "absent": 32}:
        raise ValueError("Development scene denominator differs from review")
    if Counter("genuine" if row["genuine"] else "ordinary" for row in pairs) != {"genuine": 1318, "ordinary": 992}:
        raise ValueError("Development pair denominator differs from review")
    started = time.monotonic()
    with zipfile.ZipFile(args.images) as images, zipfile.ZipFile(args.model) as model:
        root, onnx_hashes = prepare_pack(model, args.cache)
        if onnx_hashes != EXPECTED_ONNX:
            raise ValueError("ONNX weights differ from T-017")
        app = FaceAnalysis(name="buffalo_sc", root=str(root),
                           allowed_modules=["detection", "recognition"],
                           providers=["CPUExecutionProvider"])
        app.prepare(ctx_id=-1, det_size=(640, 640), det_thresh=0.5)
        if set(app.models) != {"detection", "recognition"}:
            raise ValueError("Unexpected model modules")
        required_members = {name for row in pairs for name in (row["left"], row["right"])}
        required_members.update(name for row in scenes for name in (row["reference_member"], *row["panel_members"]))
        features = {}
        for index, member in enumerate(sorted(required_members), 1):
            boxes, vectors = image_features(app, images.read(member))
            if len(boxes) != 1:
                raise ValueError(f"Locked source image no longer has one face: {member}")
            features[member] = vectors[0]
            if index % 500 == 0:
                print(f"Development source embeddings {index}/{len(required_members)}", flush=True)
        pair_rows = [{"pair_index": row["index"], "genuine": row["genuine"],
                      "score": float(features[row["left"]] @ features[row["right"]])}
                     for row in pairs]
        scene_rows = []
        for index, row in enumerate(scenes, 1):
            scene_file = args.locked.parent / row["scene_file"]
            if digest(scene_file) != row["scene_sha256"]:
                raise ValueError(f"Controlled scene changed: {row['trial']}")
            boxes, vectors = image_features(app, scene_file.read_bytes())
            expected = sorted(row["boxes"], key=lambda item: item["panel"])
            if len(boxes) != 2 or sorted(item["panel"] for item in expected) != [0, 1]:
                raise ValueError(f"Locked scene mapping differs: {row['trial']}")
            indexed = sorted(enumerate(boxes), key=lambda item: (item[1][0] + item[1][2]) / 2)
            if any(np.max(np.abs(box - np.asarray(expected[panel]["xyxy"]))) > 1.0
                   for panel, (_, box) in enumerate(indexed)):
                raise ValueError(f"Scene detector box changed: {row['trial']}")
            scores = [float(vec @ features[row["reference_member"]]) for vec in vectors]
            selected = select_p2(scores, TAU, DELTA)
            selected_panel = None
            if selected is not None:
                center = (boxes[selected][0] + boxes[selected][2]) / 2
                selected_panel = 0 if center < 250 else (1 if center >= 266 else None)
                if selected_panel is None:
                    raise ValueError(f"Selected box in panel gutter: {row['trial']}")
            if selected is None:
                outcome = "UNRESOLVED" if row["kind"] == "present" else "NO_FACE_SELECTED"
            elif row["kind"] == "absent":
                outcome = "FALSE_SELECTION"
            else:
                outcome = "CORRECT_TARGET" if selected_panel == row["target_panel"] else "WRONG_TARGET"
            scene_rows.append({"trial": row["trial"], "kind": row["kind"],
                               "target_panel": row["target_panel"], "scores_by_detection": scores,
                               "selected_detection": selected, "selected_panel": selected_panel,
                               "selected_score": scores[selected] if selected is not None else None,
                               "top_score": max(scores), "margin": abs(scores[0] - scores[1]),
                               "s4_outcome": outcome})
            if index % 16 == 0:
                print(f"Development controlled scenes {index}/{len(scenes)}", flush=True)
    s4 = {kind: dict(Counter(row["s4_outcome"] for row in scene_rows if row["kind"] == kind))
          for kind in ("present", "absent")}
    selected_genuine = [row["selected_score"] for row in scene_rows if row["s4_outcome"] == "CORRECT_TARGET"]
    hard_absent = [row["selected_score"] for row in scene_rows if row["s4_outcome"] == "FALSE_SELECTION"]
    hard_present = [row["selected_score"] for row in scene_rows if row["s4_outcome"] == "WRONG_TARGET"]
    grid = [round(-1 + index * 0.05, 8) for index in range(41)]
    grid += [0.122254, TAU]  # historical references, not proposed operating points
    grid = sorted(set(grid))
    raw = {"scope": "T-022 development only; locked synthetic XQLFW proxy; no evaluation; no threshold selection",
           "lock_sha256": LOCK_SHA256, "source_sha256": locked["source_sha256"],
           "model_pack_sha256": MODEL_SHA256,
           "model_onnx_sha256": onnx_hashes, "code_sha256": digest(Path(__file__)),
           "p2_parameters": {"tau": TAU, "delta": DELTA},
           "pairs": pair_rows, "scenes": scene_rows}
    write_once(args.raw_output, raw)
    summary = {"scope": raw["scope"], "lock_sha256": LOCK_SHA256,
               "raw_sha256": digest(args.raw_output), "code_sha256": raw["code_sha256"],
               "source_sha256": raw["source_sha256"], "model_pack_sha256": MODEL_SHA256,
               "model_onnx_sha256": onnx_hashes,
               "p2_parameters": raw["p2_parameters"],
               "denominators": {"genuine_pair": 1318, "ordinary_impostor_pair": 992,
                                "present_scene": 32, "absent_scene": 32,
                                "s4_selected_genuine": len(selected_genuine),
                                "s4_hard_negative_absent": len(hard_absent),
                                "s4_hard_negative_present": len(hard_present)},
               "s4_outcomes": s4,
               "score_distribution": {
                   "genuine_pair": describe([r["score"] for r in pair_rows if r["genuine"]]),
                   "ordinary_impostor_pair": describe([r["score"] for r in pair_rows if not r["genuine"]]),
                   "s4_selected_genuine": describe(selected_genuine),
                   "s4_hard_negative_absent": describe(hard_absent),
                   "s4_hard_negative_present": describe(hard_present)},
               "threshold_grid": [threshold_row(theta, pair_rows, scene_rows) for theta in grid],
               "threshold_grid_note": "Predeclared descriptive [-1,1] step 0.05 plus historical T-020 theta and T-017 tau; no selected research/deployment threshold",
               "environment": {"python": platform.python_version(), "platform": platform.platform(),
                               "logical_cpus": os.cpu_count(), "opencv": cv2.__version__,
                               "onnxruntime": ort.__version__, "insightface": insightface_version,
                               "numpy": np.__version__, "provider": "CPUExecutionProvider",
                               "detector_input": [640, 640], "detector_threshold": 0.5},
               "runtime_seconds": time.monotonic() - started}
    write_once(args.summary_output, summary)
    print(json.dumps({"raw_sha256": digest(args.raw_output),
                      "summary_sha256": digest(args.summary_output),
                      "denominators": summary["denominators"], "s4_outcomes": s4,
                      "score_distribution": summary["score_distribution"],
                      "runtime_seconds": summary["runtime_seconds"]}, indent=2))


if __name__ == "__main__":
    main()
