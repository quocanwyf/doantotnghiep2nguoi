"""Run one T-017 clean confirmation with T-015 frozen B0/P1/P2 and tau/delta.

Per-sample scores are private and must remain outside Git. No tuning path exists.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import time
from collections import Counter
from pathlib import Path

import cv2
import numpy as np
import onnxruntime as ort
from insightface import __version__ as insightface_version
from insightface.app import FaceAnalysis
from insightface.app.common import Face

from t011_xqlfw_baseline import EXPECTED, checked_zip, digest, prepare_pack, wilson
from t011_xqlfw_r50_comparison import unit


FROZEN_SHA256 = "a63f64d7fa6cfe4d3d98f2d52c10a30d7bb8445b20de8b0e6b4780ff1ff7980d"
SCENE_SHA256 = "5ca44481ce26abe62e2e699bdaae44c7b9227f2a5c54f6ac9d865330ad658290"
LABEL_SHA256 = "130408bd8f7a02ce502f31cb8f386a01d7adfeab9d5be00bc8fe9a195adc7d11"
TAU = 0.14789717107158995
DELTA = 0.07647264965285691


def encode(data: object) -> bytes:
    return (json.dumps(data, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False) + "\n").encode("utf-8")


def number(value: float) -> float | str:
    if np.isneginf(value):
        return "-inf"
    if np.isposinf(value):
        return "+inf"
    return float(value)


def parse_number(value: float | str) -> float:
    if value == "-inf":
        return -float("inf")
    if value == "+inf":
        return float("inf")
    return float(value)


def select_p1(scores: list[float]) -> int | None:
    if len(scores) < 2:
        return None
    maximum = max(scores)
    winners = [index for index, score in enumerate(scores) if score == maximum]
    return winners[0] if len(winners) == 1 else None


def select_p2(scores: list[float], tau: float, delta: float) -> int | None:
    winner = select_p1(scores)
    if winner is None:
        return None
    ordered = sorted(scores, reverse=True)
    return winner if ordered[0] >= tau and ordered[0] - ordered[1] >= delta else None


def outcome(reference_type: str, selected: int | None, target_index: int | None) -> str:
    if selected is None:
        return "UNRESOLVED" if reference_type == "present" else "NO_FACE_SELECTED"
    if reference_type == "absent":
        return "FALSE_SELECTION"
    return "CORRECT_TARGET" if selected == target_index else "WRONG_TARGET"


def get_faces(app: FaceAnalysis, encoded: bytes):
    started = time.perf_counter_ns()
    image = cv2.imdecode(np.frombuffer(encoded, dtype=np.uint8), cv2.IMREAD_COLOR)
    if image is None:
        raise ValueError("Source image decode failed")
    detected, landmarks = app.models["detection"].detect(image, max_num=0, metric="default")
    decode_detect_ms = (time.perf_counter_ns() - started) / 1e6
    faces = []
    vectors = []
    embedding_ms = []
    for index, box in enumerate(detected):
        face = Face(bbox=box[:4], kps=landmarks[index] if landmarks is not None else None, det_score=box[4])
        tick = time.perf_counter_ns()
        vector = unit(app.models["recognition"].get(image, face))
        embedding_ms.append((time.perf_counter_ns() - tick) / 1e6)
        faces.append(face)
        vectors.append(vector)
    return faces, np.asarray(vectors, dtype=float).reshape(-1, 512), decode_detect_ms, embedding_ms


def calculate(split_name: str, scene: dict, labels: dict, images: Path, model: Path, cache: Path, expected_hashes: dict):
    with checked_zip(images) as archive, checked_zip(model) as model_zip:
        root, onnx_hashes = prepare_pack(model_zip, cache)
        app = FaceAnalysis(name="buffalo_sc", root=str(root), allowed_modules=["detection", "recognition"], providers=["CPUExecutionProvider"])
        app.prepare(ctx_id=-1, det_size=(640, 640), det_thresh=0.5)
        if onnx_hashes != expected_hashes:
            raise ValueError("ONNX hash differs from frozen B0")
        rows = []
        for position, record in enumerate(scene["selected"], 1):
            if record["split"] != split_name:
                continue
            label = labels[record["sample"]]
            usable = [kind for kind in ("present", "absent") if label[kind + "_status"] == "SELF_CONFIRMED"]
            if not usable:
                continue
            scene_faces, scene_vectors, scene_ms, scene_embedding_ms = get_faces(app, archive.read(record["scene_zip_member"]))
            original = np.asarray(record["detected_boxes_xyxy"], dtype=float).reshape(-1, 4)
            rerun = np.asarray([face.bbox for face in scene_faces], dtype=float).reshape(-1, 4)
            if original.shape != rerun.shape or np.max(np.abs(original - rerun), initial=0.0) > 1.0:
                raise ValueError(f"Scene detector boxes changed for {record['sample']}")
            if len(scene_faces) < 2:
                raise ValueError("Selected scene no longer has >=2 detections")
            for kind in usable:
                ref_member = record[kind + "_ref_zip_member"]
                ref_faces, ref_vectors, ref_ms, ref_embedding_ms = get_faces(app, archive.read(ref_member))
                if len(ref_faces) != 1:
                    raise ValueError(f"Usable reference no longer has exactly one face: {record['sample']} {kind}")
                scores = (scene_vectors @ ref_vectors[0]).astype(float).tolist()
                tick = time.perf_counter_ns()
                p1 = select_p1(scores)
                p1_ms = (time.perf_counter_ns() - tick) / 1e6
                ordered = sorted(scores, reverse=True)
                rows.append({
                    "sample": record["sample"], "split": split_name, "reference_type": kind,
                    "ground_truth_box_index": label["ground_truth_box_index"] if kind == "present" else None,
                    "scene_detection_count": len(scene_faces), "scene_scores_by_detection": scores,
                    "top_score": ordered[0], "top_two_gap": ordered[0] - ordered[1],
                    "b0_selection": None, "b0_outcome": outcome(kind, None, label["ground_truth_box_index"]),
                    "p1_selection": p1, "p1_outcome": outcome(kind, p1, label["ground_truth_box_index"]),
                    "timing_ms": {
                        "scene_decode_detect": scene_ms, "scene_embedding_each_face": scene_embedding_ms,
                        "reference_decode_detect": ref_ms, "reference_embedding_each_face": ref_embedding_ms,
                        "p1_decision": p1_ms,
                    },
                })
            if position % 16 == 0:
                print(f"{split_name}: candidate scores through selected scene {position}/64", flush=True)
    return rows, onnx_hashes


def summarize(rows: list[dict]):
    result = {}
    for kind in ("present", "absent"):
        group = [row for row in rows if row["reference_type"] == kind]
        counts = {}
        for method in ("b0", "p1", "p2"):
            values = Counter(row[method + "_outcome"] for row in group)
            counts[method] = dict(values)
            if kind == "present":
                counts[method]["correct_wilson95"] = wilson(values["CORRECT_TARGET"], len(group))
                counts[method]["wrong_wilson95"] = wilson(values["WRONG_TARGET"], len(group))
                selected = values["CORRECT_TARGET"] + values["WRONG_TARGET"]
                counts[method]["wrong_among_selected"] = values["WRONG_TARGET"] / selected if selected else None
            else:
                counts[method]["false_selection_wilson95"] = wilson(values["FALSE_SELECTION"], len(group))
        result[kind] = {"denominator": len(group), "methods": counts}
    timing = {}
    fields = {
        "scene_decode_detect": [r["timing_ms"]["scene_decode_detect"] for r in rows],
        "scene_embedding_each_face": [x for r in rows for x in r["timing_ms"]["scene_embedding_each_face"]],
        "reference_decode_detect": [r["timing_ms"]["reference_decode_detect"] for r in rows],
        "reference_embedding_each_face": [x for r in rows for x in r["timing_ms"]["reference_embedding_each_face"]],
        "p1_decision": [r["timing_ms"]["p1_decision"] for r in rows],
        "p2_decision": [r["timing_ms"]["p2_decision"] for r in rows],
    }
    for field, values in fields.items():
        timing[field] = {"n": len(values), "median_ms": float(np.median(values)), "p95_ms": float(np.percentile(values, 95))}
    return {"groups": result, "timing": timing, "scene_face_counts": dict(Counter(r["scene_detection_count"] for r in rows if r["reference_type"] == "present"))}


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    for name in ("images", "pairs", "model", "scene-manifest", "label-manifest", "cache", "output", "frozen"):
        p.add_argument("--" + name, type=Path, required=True)
    args = p.parse_args()
    if args.output.exists():
        p.error("Private raw output already exists")
    hashes = {"images": digest(args.images), "pairs": digest(args.pairs), "model": digest(args.model)}
    if hashes != EXPECTED:
        raise ValueError("B0 source or model hash differs")
    scene_hash = digest(args.scene_manifest)
    label_hash = digest(args.label_manifest)
    if scene_hash != SCENE_SHA256 or label_hash != LABEL_SHA256 or digest(args.frozen) != FROZEN_SHA256:
        raise ValueError("T-017 scene/label or T-015 P2 frozen hash differs")
    scene = json.loads(args.scene_manifest.read_text(encoding="utf-8"))
    label = json.loads(args.label_manifest.read_text(encoding="utf-8"))
    if label["scene_manifest_sha256"] != scene_hash or label["source_sha256"]["model"] != hashes["model"]:
        raise ValueError("Locked label provenance differs")
    by_sample = {row["sample"]: row for row in label["records"]}
    if len(by_sample) != 64 or len(scene["selected"]) != 64:
        raise ValueError("Expected 64 locked clean holdout scenes")
    code_hash = digest(Path(__file__))
    expected_onnx = {
        "det_500m.onnx": scene["detector_model_sha256"],
        "w600k_mbf.onnx": "9cc6e4a75f0e2bf0b1aed94578f144d15175f357bdc05e815e5c4a02b319eb4f",
    }
    frozen = json.loads(args.frozen.read_text(encoding="utf-8"))
    if frozen["source_sha256"] != hashes or frozen["tau"] != TAU or frozen["delta"] != DELTA:
        raise ValueError("T-015 frozen model/source/tau/delta differs")
    rows, onnx_hashes = calculate("holdout", scene, by_sample, args.images, args.model, args.cache, expected_onnx)
    tau, delta = TAU, DELTA
    for row in rows:
        tick = time.perf_counter_ns()
        selected = select_p2(row["scene_scores_by_detection"], tau, delta)
        row["timing_ms"]["p2_decision"] = (time.perf_counter_ns() - tick) / 1e6
        row["p2_selection"] = selected
        row["p2_outcome"] = outcome(row["reference_type"], selected, row["ground_truth_box_index"])
    report = {
        "scope": "T-017 clean XQLFW holdout proxy S4; not exam check-in or final deployment decision",
        "phase": "holdout", "source_sha256": hashes, "onnx_sha256": onnx_hashes,
        "scene_manifest_sha256": scene_hash, "label_manifest_sha256": label_hash,
        "code_sha256": code_hash, "frozen_config_sha256": digest(args.frozen) if frozen else None,
        "environment": {"python": platform.python_version(), "platform": platform.platform(), "logical_cpus": os.cpu_count(), "opencv": cv2.__version__, "onnxruntime": ort.__version__, "insightface": insightface_version, "numpy": np.__version__, "provider": "CPUExecutionProvider", "detector_input": [640, 640], "detector_threshold": 0.5, "encoder_input": [112, 112], "cache": "ONNX files on local disk; process-local model warm"},
        "p2_parameters": {"tau": number(tau), "delta": number(delta)}, "dev_search": None,
        "summary": summarize(rows), "raw_trials": rows,
    }
    args.output.write_bytes(encode(report))
    public = {key: value for key, value in report.items() if key != "raw_trials"}
    print(json.dumps({"raw_sha256": digest(args.output), **public}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
