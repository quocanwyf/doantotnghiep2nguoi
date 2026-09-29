"""One-shot S4→S8 replay of frozen T-017 raw using frozen development S8 threshold.

No detector, encoder, selection, labels, or threshold are fitted here. Private
per-trial output stays outside Git.
"""

from __future__ import annotations

import argparse
import json
import math
import platform
import time
from collections import Counter
from pathlib import Path

from t011_xqlfw_baseline import EXPECTED, digest
from t020_s8_dev_threshold import SPLIT_SHA256


T017_RAW_SHA256 = "dceea1abe0d09e78479473bc28a068f2b32d601c840cff0fceac09e1419811c8"
T017_LABEL_SHA256 = "130408bd8f7a02ce502f31cb8f386a01d7adfeab9d5be00bc8fe9a195adc7d11"
T015_S4_FROZEN_SHA256 = "a63f64d7fa6cfe4d3d98f2d52c10a30d7bb8445b20de8b0e6b4780ff1ff7980d"


def write_once(path: Path, data: object) -> None:
    if path.exists():
        raise FileExistsError(f"Will not overwrite replay result: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False) + "\n", encoding="utf-8")


def classify(row: dict, method: str, threshold: float) -> dict:
    kind = row["reference_type"]
    selected = row[method + "_selection"]
    target = row["ground_truth_box_index"]
    scores = row["scene_scores_by_detection"]
    if kind not in ("present", "absent") or len(scores) != row["scene_detection_count"] or len(scores) < 2:
        raise ValueError("Unexpected T-017 row")
    if selected is None:
        expected = "UNRESOLVED" if kind == "present" else "NO_FACE_SELECTED"
        if row[method + "_outcome"] != expected:
            raise ValueError("S4 outcome differs from frozen output")
        return {"selection": None, "s4_outcome": expected, "s8_verdict": "NOT_RUN", "s8_ground_truth": None,
                "selected_cosine": None, "pipeline_outcome": expected}
    if not isinstance(selected, int) or selected < 0 or selected >= len(scores):
        raise ValueError("Invalid S4 selection")
    score = float(scores[selected])
    if not math.isfinite(score):
        raise ValueError("Non-finite cosine")
    correct = kind == "present" and selected == target
    expected_s4 = "CORRECT_TARGET" if correct else ("WRONG_TARGET" if kind == "present" else "FALSE_SELECTION")
    if row[method + "_outcome"] != expected_s4:
        raise ValueError("S4 selected box differs from frozen outcome")
    verdict = "ACCEPT" if score >= threshold else "REJECT"
    if kind == "absent":
        pipeline = "FALSE_SELECTION_ACCEPTED" if verdict == "ACCEPT" else "FALSE_SELECTION_REJECTED"
    elif correct:
        pipeline = "CORRECT_ACCEPT" if verdict == "ACCEPT" else "CORRECT_REJECT"
    else:
        pipeline = "WRONG_ACCEPT" if verdict == "ACCEPT" else "WRONG_REJECT"
    return {"selection": selected, "s4_outcome": expected_s4, "s8_verdict": verdict,
            "s8_ground_truth": "GENUINE" if correct else "IMPOSTOR", "selected_cosine": score,
            "pipeline_outcome": pipeline}


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    for name in ("t017-raw", "s8-frozen", "output"):
        p.add_argument("--" + name, type=Path, required=True)
    p.add_argument("--expected-s8-frozen-sha256", required=True)
    args = p.parse_args()
    if args.output.exists():
        p.error("Output exists; a holdout replay must not be rerun to change results")
    if digest(args.t017_raw) != T017_RAW_SHA256:
        raise ValueError("T-017 raw hash differs")
    if digest(args.s8_frozen) != args.expected_s8_frozen_sha256:
        raise ValueError("S8 development config hash differs")
    holdout = json.loads(args.t017_raw.read_text(encoding="utf-8"))
    frozen = json.loads(args.s8_frozen.read_text(encoding="utf-8"))
    if (holdout["phase"] != "holdout" or holdout["label_manifest_sha256"] != T017_LABEL_SHA256
            or holdout["frozen_config_sha256"] != T015_S4_FROZEN_SHA256
            or holdout["source_sha256"] != EXPECTED
            or frozen["source_sha256"] != EXPECTED or frozen["split_sha256"] != SPLIT_SHA256
            or frozen["selection_rule"] != "t011_select_threshold_min_abs_fmr_minus_fnmr_tie_lower_fmr_higher_threshold"):
        raise ValueError("Locked source/label/split/rule mismatch")
    threshold = float(frozen["threshold"])
    if not math.isfinite(threshold) or not -1 <= threshold <= 1:
        raise ValueError("Invalid frozen S8 threshold")
    rows = holdout["raw_trials"]
    if len(rows) != 90 or Counter(row["reference_type"] for row in rows) != {"present": 49, "absent": 41}:
        raise ValueError("T-017 locked holdout denominator differs")
    if len({(row["sample"], row["reference_type"]) for row in rows}) != len(rows):
        raise ValueError("Duplicate trial")
    start = time.perf_counter_ns()
    trials = []
    for row in rows:
        trials.append({"sample": row["sample"], "reference_type": row["reference_type"],
                       "scene_detection_count": row["scene_detection_count"],
                       "ground_truth_box_index": row["ground_truth_box_index"],
                       "methods": {method: classify(row, method, threshold) for method in ("b0", "p1", "p2")}})
    replay_ms = (time.perf_counter_ns() - start) / 1e6
    summary = {}
    for method in ("b0", "p1", "p2"):
        groups = {}
        s8 = Counter()
        for kind in ("present", "absent"):
            group = [trial for trial in trials if trial["reference_type"] == kind]
            counts = Counter(trial["methods"][method]["pipeline_outcome"] for trial in group)
            groups[kind] = {"denominator": len(group), "pipeline_outcomes": dict(counts),
                            "two_faces": sum(trial["scene_detection_count"] == 2 for trial in group),
                            "three_or_more_faces": sum(trial["scene_detection_count"] >= 3 for trial in group)}
            for trial in group:
                info = trial["methods"][method]
                if info["s8_verdict"] != "NOT_RUN":
                    s8[info["s8_ground_truth"] + "_" + info["s8_verdict"]] += 1
        summary[method] = {"groups": groups, "s8_conditional_counts": dict(s8),
                           "s8_called": sum(s8.values()),
                           "end_to_end_present_correct_accept": groups["present"]["pipeline_outcomes"].get("CORRECT_ACCEPT", 0),
                           "end_to_end_absent_no_accept": groups["absent"]["pipeline_outcomes"].get("NO_FACE_SELECTED", 0) + groups["absent"]["pipeline_outcomes"].get("FALSE_SELECTION_REJECTED", 0)}
    result = {"scope": "T-020 frozen S4→S8 XQLFW proxy replay; not deployment evaluation",
              "t017_raw_sha256": T017_RAW_SHA256, "s8_frozen_sha256": digest(args.s8_frozen),
              "script_sha256": digest(Path(__file__)), "s8_threshold": threshold,
              "s8_same_embedding_as_s4": True,
              "summary": summary, "raw_trials": trials,
              "replay_runtime_ms": replay_ms, "environment": {"python": platform.python_version()}}
    write_once(args.output, result)
    print(json.dumps({"raw_sha256": digest(args.output), **{k: v for k, v in result.items() if k != "raw_trials"}}, ensure_ascii=True, indent=2))


if __name__ == "__main__":
    main()
