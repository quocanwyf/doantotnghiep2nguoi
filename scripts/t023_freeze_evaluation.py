"""Freeze T-023 holdout inputs and a development-only research rule before scoring."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from t017_s4_run import DELTA, TAU
from t023_build_bfw import INNER_MD5, OUTER_SHA256, digest, encoded
from t023_development import LOCK_SHA256, MODEL_SHA256, REFERENCE_THETAS


DEV_RAW_SHA256 = "21596e6565fbd6aa3b6d41e7c25b38a49012fba53e3b5c16bd3b7c8b0425c908"
DEV_SUMMARY_SHA256 = "e78f193235a6fd8d91e1cdf2a256afc82104487ec163b241ca234d8a74a2a69b"
RESEARCH_THETA = 0.23
SELECTION_RULE = (
    "On development predeclared 0.01 grid, retain thresholds with >=95% accept "
    "among correctly S4-selected genuine scenes; minimize S4-derived hard-negative "
    "accept count, tie-break by smaller genuine-pair FNMR then ordinary-impostor FMR "
    "then smaller threshold. This is a research screen, not business acceptance."
)
CODE_FILES = (
    "scripts/t023_build_bfw.py", "scripts/t023_detector_audit.py",
    "scripts/t023_lock_bfw.py", "scripts/t023_development.py",
    "scripts/t023_evaluation.py", "scripts/t017_s4_run.py",
    "scripts/t022_s8_development.py", "scripts/t011_xqlfw_baseline.py",
)


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    for name in ("locked", "dev-raw", "dev-summary", "images", "model", "output"):
        p.add_argument("--" + name, type=Path, required=True)
    args = p.parse_args()
    if args.output.exists():
        p.error("Refusing to overwrite freeze")
    if (digest(args.locked), digest(args.dev_raw), digest(args.dev_summary)) != (
            LOCK_SHA256, DEV_RAW_SHA256, DEV_SUMMARY_SHA256):
        raise ValueError("Locked benchmark or development results changed")
    if digest(args.images, "md5") != INNER_MD5 or digest(args.model) != MODEL_SHA256:
        raise ValueError("Source archive/model changed")
    summary = json.loads(args.dev_summary.read_text(encoding="utf-8"))
    if summary["raw_sha256"] != DEV_RAW_SHA256 or summary["lock_sha256"] != LOCK_SHA256:
        raise ValueError("Development provenance mismatch")
    grid = summary["threshold_grid"]
    selected = [r for r in grid if r["s4_selected_genuine"]["n"] >= 50 and
                r["s4_selected_genuine"]["accept"] / r["s4_selected_genuine"]["n"] >= .95]
    selected.sort(key=lambda r: (r["s4_derived_hard_negative"]["accept"],
                                 r["genuine_pair"]["reject"] / r["genuine_pair"]["n"],
                                 r["ordinary_impostor_pair"]["accept"] / r["ordinary_impostor_pair"]["n"],
                                 r["theta"]))
    if not selected or selected[0]["theta"] != RESEARCH_THETA:
        raise ValueError("Development-only selection rule does not yield frozen theta")
    if set(REFERENCE_THETAS) - {r["theta"] for r in grid}:
        raise ValueError("Reference thresholds missing from development grid")
    repo = Path(__file__).resolve().parent.parent
    code_hashes = {name: digest(repo / name) for name in CODE_FILES}
    freeze = {
        "scope": "T-023 BFW holdout pre-score freeze; no evaluation score opened",
        "lock_sha256": LOCK_SHA256,
        "bfw_release_sha256": OUTER_SHA256,
        "bfw_inner_md5": INNER_MD5,
        "mobilefacenet_pack_sha256": MODEL_SHA256,
        "development_raw_sha256": DEV_RAW_SHA256,
        "development_summary_sha256": DEV_SUMMARY_SHA256,
        "p2": {"tau": TAU, "delta": DELTA},
        "s8_rule": "accept if same cosine score >= theta; else reject",
        "primary_research_theta": RESEARCH_THETA,
        "historical_theta": .15,
        "stress_theta": .25,
        "research_selection_rule": SELECTION_RULE,
        "evaluation_guard": "one run, no retune/exclusion/model/GT change after scores",
        "code_sha256": code_hashes,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(encoded(freeze))
    print(json.dumps({"freeze_sha256": digest(args.output),
                      "theta": RESEARCH_THETA, "rule": SELECTION_RULE,
                      "code_sha256": code_hashes}, indent=2))


if __name__ == "__main__":
    main()
