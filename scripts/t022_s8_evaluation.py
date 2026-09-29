"""Run T-022 frozen evaluation once, after an external pre-score freeze.

This reuses the exact T-022 development inference helpers. It refuses any
manifest, ground truth, model, P2 parameter, S8 rule, or code hash mismatch.
Raw per-sample results stay outside Git and outputs cannot be overwritten.
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
from t017_s4_run import DELTA, TAU, select_p2
from t022_s8_development import (
    EXPECTED_ONNX,
    LOCK_SHA256,
    MODEL_SHA256,
    describe,
    digest,
    image_features,
    threshold_row,
    write_once,
)


VERSION = "T-022-S8-evaluation-v1"
THETA_OLD = 0.122254
THETA_RESEARCH = 0.15
THETA_STRESS = 0.25
DEVELOPMENT_SUMMARY_SHA256 = "c279922825717fab6959d5f0ff3437f4087e917e0123ba623251136227b91485"
CODE_FILES = (
    "scripts/t011_xqlfw_baseline.py",
    "scripts/t017_s4_run.py",
    "scripts/t022_s8_development.py",
    "scripts/t022_s8_evaluation.py",
    "scripts/t022_freeze_s8_evaluation.py",
)


def canonical_sha256(value: object) -> str:
    encoded = json.dumps(value, ensure_ascii=False, sort_keys=True,
                         separators=(",", ":"), allow_nan=False).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def evaluation_rows(locked: dict) -> tuple[list[dict], list[dict]]:
    pairs = [row for row in locked["pairs"]["evaluation"]
             if row["lock_status"] == "USABLE_SOURCE_LABEL"]
    scenes = [row for row in locked["scenes"]
              if row["group"] == "evaluation" and row["lock_status"] == "USABLE_SELF_CONFIRMED"]
    if Counter("genuine" if row["genuine"] else "ordinary" for row in pairs) != {
            "genuine": 355, "ordinary": 131}:
        raise ValueError("Evaluation pair denominator differs from pre-score lock")
    if Counter(row["kind"] for row in scenes) != {"present": 30, "absent": 30}:
        raise ValueError("Evaluation scene denominator differs from pre-score lock")
    if len({row["trial"] for row in scenes}) != len(scenes):
        raise ValueError("Duplicate evaluation trial ID")
    return pairs, scenes


def ground_truth_hash(locked: dict) -> str:
    """Fingerprint ALL evaluation labels/statuses, including excluded rows."""
    return canonical_sha256({
        "pairs": locked["pairs"]["evaluation"],
        "scenes": [row for row in locked["scenes"] if row["group"] == "evaluation"],
    })


def code_hashes(repo_root: Path) -> dict[str, str]:
    return {name: digest(repo_root / name) for name in CODE_FILES}


def check_freeze(args: argparse.Namespace) -> tuple[dict, dict, list[dict], list[dict]]:
    if digest(args.frozen) != args.frozen_sha256.lower():
        raise ValueError("Freeze file SHA-256 differs from separately published pre-run hash")
    frozen = json.loads(args.frozen.read_text(encoding="utf-8"))
    if frozen["version"] != VERSION or frozen["locked_benchmark_sha256"] != LOCK_SHA256:
        raise ValueError("Frozen version or benchmark hash differs")
    if digest(args.locked) != LOCK_SHA256:
        raise ValueError("Locked benchmark changed")
    locked = json.loads(args.locked.read_text(encoding="utf-8"))
    if locked["recognition_scores_read"] is not False or locked["seed"] != "T-022-controlled-two-face-v1":
        raise ValueError("Locked benchmark provenance differs")
    if frozen["source_sha256"] != locked["source_sha256"]:
        raise ValueError("Frozen source hashes differ from benchmark")
    if digest(args.images) != locked["source_sha256"]["images"] or digest(args.model) != MODEL_SHA256:
        raise ValueError("XQLFW or model pack changed")
    if frozen["model_pack_sha256"] != MODEL_SHA256 or frozen["model_onnx_sha256"] != EXPECTED_ONNX:
        raise ValueError("Frozen model hashes differ")
    if frozen["ground_truth_sha256"] != ground_truth_hash(locked):
        raise ValueError("Evaluation ground truth or exclusion statuses changed")
    if frozen["evaluation_scene_hash_list_sha256"] != canonical_sha256(
            [{"trial": row["trial"], "sha256": row["scene_sha256"]}
             for row in locked["scenes"] if row["group"] == "evaluation"]):
        raise ValueError("Frozen evaluation scene hash list changed")
    if frozen["identity_disjoint"] is not True:
        raise ValueError("Identity-disjoint freeze assertion missing")
    if frozen["development_summary_sha256"] != DEVELOPMENT_SUMMARY_SHA256:
        raise ValueError("Development evidence provenance differs")
    if frozen["code_sha256"] != code_hashes(Path(__file__).resolve().parent.parent):
        raise ValueError("Evaluation code or an imported inference module changed after freeze")
    if frozen["p2_parameters"] != {"tau": TAU, "delta": DELTA}:
        raise ValueError("P2 parameters differ from T-017")
    if frozen["s8_rule"] != {
            "comparison": "cosine >= theta",
            "historical_theta": THETA_OLD,
            "research_theta": THETA_RESEARCH,
            "stress_theta": THETA_STRESS,
            "primary": "research_theta",
            "reference_selection": "On development predeclared grid theta>=historical; require 0/29 S4-selected genuine rejects; minimize 4 S4-derived hard-negative accepts; ties ordinary FMR, genuine FNMR, then smaller theta",
    }:
        raise ValueError("S8 rule or three report points differ from approved development rule")
    if frozen["detector_config"] != {
            "pack": "buffalo_sc",
            "modules": ["detection", "recognition"],
            "provider": "CPUExecutionProvider",
            "det_size": [640, 640],
            "det_thresh": 0.5,
            "encoder_input": [112, 112],
    }:
        raise ValueError("Detector/encoder config differs")
    if frozen["runtime_packages"] != {
            "python": platform.python_version(), "opencv": cv2.__version__,
            "onnxruntime": ort.__version__, "insightface": insightface_version,
            "numpy": np.__version__, "provider": "CPUExecutionProvider",
    }:
        raise ValueError("Runtime package versions differ from freeze")
    pairs, scenes = evaluation_rows(locked)
    if frozen["usable_counts"] != {
            "genuine_pair": 355, "ordinary_impostor_pair": 131,
            "present_scene": 30, "absent_scene": 30,
    }:
        raise ValueError("Frozen denominators differ")
    return frozen, locked, pairs, scenes


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    for name in ("locked", "frozen", "images", "model", "cache", "raw-output", "summary-output"):
        p.add_argument("--" + name, required=True, type=Path)
    p.add_argument("--frozen-sha256", required=True)
    p.add_argument("--preflight-only", action="store_true",
                   help="Check freeze/source/labels without opening score inference")
    args = p.parse_args()
    if not args.preflight_only and (args.raw_output.exists() or args.summary_output.exists()):
        p.error("Raw/summary output already exists; evaluation is one-run only")
    frozen, locked, pairs, scenes = check_freeze(args)
    if args.preflight_only:
        print(json.dumps({"preflight": "PASS", "frozen_sha256": args.frozen_sha256,
                          "ground_truth_sha256": frozen["ground_truth_sha256"],
                          "counts": frozen["usable_counts"]}, indent=2))
        return
    started = time.monotonic()
    with zipfile.ZipFile(args.images) as images, zipfile.ZipFile(args.model) as model:
        root, onnx_hashes = prepare_pack(model, args.cache)
        if onnx_hashes != EXPECTED_ONNX:
            raise ValueError("ONNX weights differ from freeze")
        app = FaceAnalysis(name="buffalo_sc", root=str(root),
                           allowed_modules=["detection", "recognition"],
                           providers=["CPUExecutionProvider"])
        app.prepare(ctx_id=-1, det_size=(640, 640), det_thresh=0.5)
        if set(app.models) != {"detection", "recognition"}:
            raise ValueError("Unexpected inference modules")
        required_members = {name for row in pairs for name in (row["left"], row["right"])}
        required_members.update(name for row in scenes for name in
                                (row["reference_member"], *row["panel_members"]))
        features = {}
        for index, member in enumerate(sorted(required_members), 1):
            boxes, vectors = image_features(app, images.read(member))
            if len(boxes) != 1:
                raise ValueError(f"Frozen source image no longer has one face: {member}")
            features[member] = vectors[0]
            if index % 200 == 0:
                print(f"Evaluation source embeddings {index}/{len(required_members)}", flush=True)
        pair_rows = [
            {"pair_index": row["index"], "genuine": row["genuine"],
             "score": float(features[row["left"]] @ features[row["right"]])}
            for row in pairs
        ]
        scene_rows = []
        for index, row in enumerate(scenes, 1):
            scene_file = args.locked.parent / row["scene_file"]
            if digest(scene_file) != row["scene_sha256"]:
                raise ValueError(f"Frozen scene changed: {row['trial']}")
            boxes, vectors = image_features(app, scene_file.read_bytes())
            expected = sorted(row["boxes"], key=lambda item: item["panel"])
            if len(boxes) != 2 or sorted(item["panel"] for item in expected) != [0, 1]:
                raise ValueError(f"Frozen scene box count/mapping differs: {row['trial']}")
            indexed = sorted(enumerate(boxes), key=lambda item: (item[1][0] + item[1][2]) / 2)
            if any(np.max(np.abs(box - np.asarray(expected[panel]["xyxy"]))) > 1.0
                   for panel, (_, box) in enumerate(indexed)):
                raise ValueError(f"Frozen scene detector box differs: {row['trial']}")
            scores = [float(vec @ features[row["reference_member"]]) for vec in vectors]
            selected = select_p2(scores, TAU, DELTA)
            selected_panel = None
            if selected is not None:
                center = (boxes[selected][0] + boxes[selected][2]) / 2
                selected_panel = 0 if center < 250 else (1 if center >= 266 else None)
                if selected_panel is None:
                    raise ValueError(f"Selected box in gutter: {row['trial']}")
            if selected is None:
                outcome = "UNRESOLVED" if row["kind"] == "present" else "NO_FACE_SELECTED"
            elif row["kind"] == "absent":
                outcome = "FALSE_SELECTION"
            else:
                outcome = "CORRECT_TARGET" if selected_panel == row["target_panel"] else "WRONG_TARGET"
            scene_rows.append({
                "trial": row["trial"], "kind": row["kind"],
                "target_panel": row["target_panel"], "scores_by_detection": scores,
                "selected_detection": selected, "selected_panel": selected_panel,
                "selected_score": scores[selected] if selected is not None else None,
                "top_score": max(scores), "margin": abs(scores[0] - scores[1]),
                "s4_outcome": outcome,
            })
            if index % 15 == 0:
                print(f"Evaluation controlled scenes {index}/{len(scenes)}", flush=True)
    s4 = {kind: dict(Counter(row["s4_outcome"] for row in scene_rows if row["kind"] == kind))
          for kind in ("present", "absent")}
    raw = {
        "scope": "T-022 one-run frozen evaluation; synthetic XQLFW proxy only",
        "phase": "evaluation",
        "frozen_sha256": args.frozen_sha256.lower(),
        "lock_sha256": LOCK_SHA256,
        "ground_truth_sha256": frozen["ground_truth_sha256"],
        "source_sha256": locked["source_sha256"],
        "model_pack_sha256": MODEL_SHA256,
        "model_onnx_sha256": onnx_hashes,
        "code_sha256": frozen["code_sha256"],
        "p2_parameters": frozen["p2_parameters"],
        "s8_rule": frozen["s8_rule"],
        "pairs": pair_rows,
        "scenes": scene_rows,
    }
    write_once(args.raw_output, raw)
    points = {
        "research_primary": THETA_RESEARCH,
        "historical_baseline": THETA_OLD,
        "stress_only": THETA_STRESS,
    }
    summary = {
        "scope": raw["scope"], "phase": "evaluation",
        "frozen_sha256": raw["frozen_sha256"],
        "lock_sha256": LOCK_SHA256,
        "ground_truth_sha256": raw["ground_truth_sha256"],
        "raw_sha256": digest(args.raw_output),
        "code_sha256": frozen["code_sha256"],
        "p2_parameters": frozen["p2_parameters"],
        "s4_outcomes": s4,
        "denominators": {
            **frozen["usable_counts"],
            "s4_selected_genuine": s4["present"].get("CORRECT_TARGET", 0),
            "s4_hard_negative_present": s4["present"].get("WRONG_TARGET", 0),
            "s4_hard_negative_absent": s4["absent"].get("FALSE_SELECTION", 0),
        },
        "score_distribution": {
            "genuine_pair": describe([row["score"] for row in pair_rows if row["genuine"]]),
            "ordinary_impostor_pair": describe([row["score"] for row in pair_rows if not row["genuine"]]),
            "s4_selected_genuine": describe([row["selected_score"] for row in scene_rows
                                             if row["s4_outcome"] == "CORRECT_TARGET"]),
            "s4_derived_hard_negative": describe([row["selected_score"] for row in scene_rows
                                                  if row["s4_outcome"] in ("WRONG_TARGET", "FALSE_SELECTION")]),
        },
        "operating_points": {
            label: threshold_row(theta, pair_rows, scene_rows)
            for label, theta in points.items()
        },
        "environment": {
            "python": platform.python_version(), "platform": platform.platform(),
            "logical_cpus": os.cpu_count(), "opencv": cv2.__version__,
            "onnxruntime": ort.__version__, "insightface": insightface_version,
            "numpy": np.__version__, "provider": "CPUExecutionProvider",
            "detector_input": [640, 640], "detector_threshold": 0.5,
            "encoder_input": [112, 112],
        },
        "runtime_seconds": time.monotonic() - started,
    }
    write_once(args.summary_output, summary)
    print(json.dumps({"raw_sha256": digest(args.raw_output),
                      "summary_sha256": digest(args.summary_output),
                      "frozen_sha256": raw["frozen_sha256"],
                      "denominators": summary["denominators"],
                      "s4_outcomes": s4,
                      "operating_points": summary["operating_points"],
                      "runtime_seconds": summary["runtime_seconds"]}, indent=2))


if __name__ == "__main__":
    main()
