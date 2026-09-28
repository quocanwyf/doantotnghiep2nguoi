"""T-016 descriptive replay of frozen T-015 S4 outputs; never runs a model."""

from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
from statistics import median

EXPECTED_SHA256 = {
    "development-raw-v1.json": "ff1f98c177ddd70f79ca24365ba16a5b7045234a68c98bd090016452dc269fbd",
    "evaluation-raw-v1.json": "bfb452355ba038ea935b54e4daf1df76c01d28d1b437839dc3f4daaa579d1209",
    "frozen-p2-v1.json": "a63f64d7fa6cfe4d3d98f2d52c10a30d7bb8445b20de8b0e6b4780ff1ff7980d",
    "locked-label-audit-v1.json": "747f9f0877b92c9f87fbceec944e4de5132c393cfa766f44fd6c9ea9ce333785",
    "scene-manifest.json": "ae80423e479d616052a2bf2cc5a24d2dd45519bb12957525e33f8ab45b769c74",
}


def load_locked(root: Path, name: str) -> dict:
    data = (root / name).read_bytes()
    got = hashlib.sha256(data).hexdigest()
    if got != EXPECTED_SHA256[name]:
        raise ValueError(f"{name}: SHA-256 mismatch; stop descriptive analysis")
    return json.loads(data)


def summarize(rows: list[dict], tau: float, delta: float) -> dict:
    result = {}
    for reference_type in ("present", "absent"):
        group = [r for r in rows if r["reference_type"] == reference_type]
        result[reference_type] = {
            "n": len(group),
            "b0": dict(Counter(r["b0_outcome"] for r in group)),
            "p1": dict(Counter(r["p1_outcome"] for r in group)),
            "p2": dict(Counter(r["p2_outcome"] for r in group)),
            "score_gate_pass": sum(r["top_score"] >= tau for r in group),
            "margin_gate_pass": sum(r["top_two_gap"] >= delta for r in group),
            "both_gates_pass": sum(r["top_score"] >= tau and r["top_two_gap"] >= delta for r in group),
            "top_score_range_median": [min(r["top_score"] for r in group), median(r["top_score"] for r in group), max(r["top_score"] for r in group)],
            "top_two_gap_range_median": [min(r["top_two_gap"] for r in group), median(r["top_two_gap"] for r in group), max(r["top_two_gap"] for r in group)],
        }
    return result


def critical(rows: list[dict], tau: float, delta: float) -> list[dict]:
    selected = [r for r in rows if
        (r["reference_type"] == "present" and (r["p1_outcome"] == "WRONG_TARGET" or r["p2_outcome"] == "UNRESOLVED"))
        or (r["reference_type"] == "absent" and r["p2_outcome"] == "FALSE_SELECTION")]
    return [{
        "sample": r["sample"], "reference_type": r["reference_type"],
        "n_faces": r["scene_detection_count"], "gt_box": r["ground_truth_box_index"],
        "p1_selection": r["p1_selection"], "p1_outcome": r["p1_outcome"],
        "p2_selection": r["p2_selection"], "p2_outcome": r["p2_outcome"],
        "top_score": r["top_score"], "top_two_gap": r["top_two_gap"],
        "score_gate_pass": r["top_score"] >= tau,
        "margin_gate_pass": r["top_two_gap"] >= delta,
    } for r in selected]


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--private-dir", type=Path, required=True)
    args = p.parse_args()
    data = {name: load_locked(args.private_dir, name) for name in EXPECTED_SHA256}
    frozen = data["frozen-p2-v1.json"]
    dev = data["development-raw-v1.json"]
    evaluation = data["evaluation-raw-v1.json"]
    if dev["phase"] != "development" or evaluation["phase"] != "evaluation":
        raise ValueError("T-015 phase provenance differs")
    if frozen["development_raw_sha256"] != EXPECTED_SHA256["development-raw-v1.json"]:
        raise ValueError("Frozen development provenance differs")
    for raw in (dev, evaluation):
        if raw["code_sha256"] != frozen["code_sha256"] or raw["source_sha256"] != frozen["source_sha256"]:
            raise ValueError("Code/source provenance differs from frozen P2")
        if raw["p2_parameters"] != {"tau": float(frozen["tau"]), "delta": float(frozen["delta"])}:
            raise ValueError("P2 parameters differ from frozen values")
        if raw["label_manifest_sha256"] != frozen["label_manifest_sha256"] or raw["label_manifest_sha256"] != EXPECTED_SHA256["locked-label-audit-v1.json"]:
            raise ValueError("Label provenance differs")
        if raw["scene_manifest_sha256"] != frozen["scene_manifest_sha256"] or raw["scene_manifest_sha256"] != EXPECTED_SHA256["scene-manifest.json"]:
            raise ValueError("Scene provenance differs")
    if evaluation["frozen_config_sha256"] != EXPECTED_SHA256["frozen-p2-v1.json"]:
        raise ValueError("Evaluation frozen config provenance differs")
    tau, delta = float(frozen["tau"]), float(frozen["delta"])
    result = {
        "scope": "T-016 descriptive analysis only; no model run, relabeling, or retuning",
        "input_sha256": EXPECTED_SHA256,
        "tau": tau, "delta": delta,
        "development": summarize(dev["raw_trials"], tau, delta),
        "evaluation": summarize(evaluation["raw_trials"], tau, delta),
        "critical_evaluation_trials": critical(evaluation["raw_trials"], tau, delta),
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
