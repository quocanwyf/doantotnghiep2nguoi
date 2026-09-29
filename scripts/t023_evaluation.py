"""Run one frozen T-023 BFW evaluation; refuse any altered input or code."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from t023_build_bfw import INNER_MD5, digest
from t023_development import LOCK_SHA256, MODEL_SHA256, score_split, summarize, write_once
from t023_freeze_evaluation import CODE_FILES, RESEARCH_THETA


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    for name in ("freeze", "locked", "images", "model", "cache", "raw-output", "summary-output"):
        p.add_argument("--" + name, type=Path, required=True)
    args = p.parse_args()
    if args.raw_output.exists() or args.summary_output.exists():
        p.error("Evaluation outputs already exist; refusing a rerun")
    freeze_sha256 = digest(args.freeze)
    freeze = json.loads(args.freeze.read_text(encoding="utf-8"))
    if freeze["lock_sha256"] != LOCK_SHA256 or freeze["primary_research_theta"] != RESEARCH_THETA:
        raise ValueError("Ground truth or research rule differs")
    if digest(args.locked) != LOCK_SHA256 or digest(args.images, "md5") != INNER_MD5:
        raise ValueError("Holdout source/ground truth differs")
    if digest(args.model) != MODEL_SHA256:
        raise ValueError("Frozen model pack differs")
    repo = Path(__file__).resolve().parent.parent
    for name in CODE_FILES:
        if digest(repo / name) != freeze["code_sha256"][name]:
            raise ValueError(f"Frozen code changed: {name}")
    locked = json.loads(args.locked.read_text(encoding="utf-8"))
    if locked["recognition_scores_read"] is not False:
        raise ValueError("GT was not locked before score")
    pairs, scenes, run = score_split(locked, args.images, args.model, args.cache,
                                     args.locked.parent, "evaluation")
    raw = {"scope": "T-023 one frozen BFW evaluation run; no retune",
           "freeze_sha256": freeze_sha256, "lock_sha256": LOCK_SHA256,
           "model_pack_sha256": MODEL_SHA256, "pairs": pairs, "scenes": scenes}
    write_once(args.raw_output, raw)
    full = summarize(pairs, scenes)
    primary = next(row for row in full["threshold_grid"] if row["theta"] == RESEARCH_THETA)
    historical = next(row for row in full["threshold_grid"] if row["theta"] == .15)
    stress = next(row for row in full["threshold_grid"] if row["theta"] == .25)
    summary = {"scope": raw["scope"], "freeze_sha256": freeze_sha256,
               "raw_sha256": digest(args.raw_output), "model_pack_sha256": MODEL_SHA256,
               **run, **{key: full[key] for key in ("denominators", "s4_outcomes",
                                                  "s4_absent_strata", "score_distribution")},
               "primary_theta": RESEARCH_THETA, "primary_result": primary,
               "historical_theta_0_15": historical, "stress_theta_0_25": stress,
               "note": "No threshold/model selection based on evaluation; raw per-sample scores private"}
    write_once(args.summary_output, summary)
    print(json.dumps({"raw_sha256": digest(args.raw_output),
                      "summary_sha256": digest(args.summary_output),
                      "denominators": full["denominators"], "s4_outcomes": full["s4_outcomes"],
                      "primary_result": primary, "score_distribution": full["score_distribution"],
                      "runtime_seconds": run["runtime_seconds"]}, indent=2))


if __name__ == "__main__":
    main()
