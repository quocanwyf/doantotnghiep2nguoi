"""Freeze T-022 evaluation inputs, ground truth, code and rule before scoring.

Reads metadata and hashes only. No face embedding, cosine score or evaluation
outcome is computed. Writes a private, immutable-once JSON freeze file.
"""

from __future__ import annotations

import argparse
import json
import platform
from collections import Counter
from pathlib import Path

import cv2
import numpy as np
import onnxruntime as ort
from insightface import __version__ as insightface_version

from t017_s4_run import DELTA, TAU
from t022_s8_development import EXPECTED_ONNX, LOCK_SHA256, MODEL_SHA256, digest, write_once
from t022_s8_evaluation import (
    DEVELOPMENT_SUMMARY_SHA256,
    THETA_OLD,
    THETA_RESEARCH,
    THETA_STRESS,
    VERSION,
    canonical_sha256,
    code_hashes,
    evaluation_rows,
    ground_truth_hash,
)


def source_identity(member: str) -> str:
    return Path(member.replace("\\", "/")).parent.name


def identities(locked: dict, split: str) -> set[str]:
    result = set()
    for row in locked["pairs"][split]:
        result.update((source_identity(row["left"]), source_identity(row["right"])))
    for row in locked["scenes"]:
        if row["group"] == split:
            result.add(row["reference_identity"])
            result.update(row["panel_identities"])
    return result


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    for name in ("locked", "images", "model", "development-summary", "output"):
        p.add_argument("--" + name, required=True, type=Path)
    args = p.parse_args()
    if args.output.exists():
        p.error("Freeze file already exists")
    if digest(args.locked) != LOCK_SHA256:
        raise ValueError("Pre-score benchmark manifest changed")
    locked = json.loads(args.locked.read_text(encoding="utf-8"))
    if locked["recognition_scores_read"] is not False or locked["seed"] != "T-022-controlled-two-face-v1":
        raise ValueError("Benchmark provenance differs")
    if digest(args.images) != locked["source_sha256"]["images"]:
        raise ValueError("XQLFW archive changed")
    if digest(args.model) != MODEL_SHA256:
        raise ValueError("Model pack changed")
    if digest(args.development_summary) != DEVELOPMENT_SUMMARY_SHA256:
        raise ValueError("Development summary used to approve rule changed")
    development = json.loads(args.development_summary.read_text(encoding="utf-8"))
    if (development["lock_sha256"] != LOCK_SHA256
            or development["p2_parameters"] != {"tau": TAU, "delta": DELTA}
            or development["denominators"]["s4_selected_genuine"] != 29
            or development["denominators"]["s4_hard_negative_absent"] != 4):
        raise ValueError("Development evidence differs from approved rule")
    research_row = next(row for row in development["threshold_grid"]
                        if row["theta"] == THETA_RESEARCH)
    if (research_row["s4_selected_genuine"] != {"n": 29, "accept": 29, "reject": 0}
            or research_row["s4_derived_hard_negative"] != {"n": 4, "accept": 3, "reject": 1}
            or research_row["ordinary_impostor_pair"]["accept"] != 31
            or research_row["genuine_pair"]["reject"] != 126):
        raise ValueError("Research point differs from reviewed development evidence")
    pairs, scenes = evaluation_rows(locked)
    overlap = identities(locked, "development") & identities(locked, "evaluation")
    if overlap:
        raise ValueError(f"Development/evaluation source identity overlap: {len(overlap)}")
    for row in (row for row in locked["scenes"] if row["group"] == "evaluation"):
        scene_file = args.locked.parent / row["scene_file"]
        if digest(scene_file) != row["scene_sha256"]:
            raise ValueError(f"Evaluation scene byte hash changed: {row['trial']}")
    freeze = {
        "version": VERSION,
        "scope": "T-022 one frozen evaluation; synthetic XQLFW proxy, no deployment claim",
        "approved_by": "Quốc An",
        "approval_date": "2026-09-29",
        "locked_benchmark_sha256": LOCK_SHA256,
        "ground_truth_sha256": ground_truth_hash(locked),
        "evaluation_status_counts": {
            "scenes": dict(Counter(row["lock_status"] for row in locked["scenes"]
                                   if row["group"] == "evaluation")),
            "pairs": dict(Counter(row["lock_status"] for row in locked["pairs"]["evaluation"])),
        },
        "evaluation_scene_hash_list_sha256": canonical_sha256(
            [{"trial": row["trial"], "sha256": row["scene_sha256"]}
             for row in locked["scenes"] if row["group"] == "evaluation"]),
        "identity_disjoint": True,
        "source_sha256": locked["source_sha256"],
        "model_pack_sha256": MODEL_SHA256,
        "model_onnx_sha256": EXPECTED_ONNX,
        "development_summary_sha256": DEVELOPMENT_SUMMARY_SHA256,
        "p2_parameters": {"tau": TAU, "delta": DELTA},
        "detector_config": {
            "pack": "buffalo_sc",
            "modules": ["detection", "recognition"],
            "provider": "CPUExecutionProvider",
            "det_size": [640, 640],
            "det_thresh": 0.5,
            "encoder_input": [112, 112],
        },
        "s8_rule": {
            "comparison": "cosine >= theta",
            "historical_theta": THETA_OLD,
            "research_theta": THETA_RESEARCH,
            "stress_theta": THETA_STRESS,
            "primary": "research_theta",
            "reference_selection": "On development predeclared grid theta>=historical; require 0/29 S4-selected genuine rejects; minimize 4 S4-derived hard-negative accepts; ties ordinary FMR, genuine FNMR, then smaller theta",
        },
        "usable_counts": {
            "genuine_pair": 355, "ordinary_impostor_pair": 131,
            "present_scene": 30, "absent_scene": 30,
        },
        "code_sha256": code_hashes(Path(__file__).resolve().parent.parent),
        "runtime_packages": {
            "python": platform.python_version(), "opencv": cv2.__version__,
            "onnxruntime": ort.__version__, "insightface": insightface_version,
            "numpy": np.__version__, "provider": "CPUExecutionProvider",
        },
    }
    write_once(args.output, freeze)
    print(json.dumps({
        "freeze_sha256": digest(args.output),
        "ground_truth_sha256": freeze["ground_truth_sha256"],
        "evaluation_scene_hash_list_sha256": freeze["evaluation_scene_hash_list_sha256"],
        "identity_disjoint": True,
        "evaluation_status_counts": freeze["evaluation_status_counts"],
        "usable_counts": freeze["usable_counts"],
        "code_sha256": freeze["code_sha256"],
        "s8_rule": freeze["s8_rule"],
    }, indent=2))


if __name__ == "__main__":
    main()
