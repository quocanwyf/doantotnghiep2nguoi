"""Freeze T-023 BFW source labels after detector and score-blind visual audit.

The private output contains source identity paths and must stay outside Git.
No recognition encoder, P2 score, or T-022 evaluation output is read here.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

from t023_build_bfw import SEED, digest, encoded, identity


CANDIDATE_SHA256 = "3ac495fefaf440687f379965f44fac772b585dd5e66b09fcde25d0115af1a492"
DETECTOR_AUDIT_SHA256 = "280964a73be58d7995d2fe2c8809ef57463ce6c24336c2d3e86f805a1ae95cb0"

# One-person review of all 26 contact sheets, before opening MobileFaceNet scores.
# These are uncertain source-identity relationships; no label is forced.
VISUAL_AMBIGUOUS = {
    "f4-007-3": "Reference/right-panel identity visually uncertain at source quality",
    "f5-029-4": "Reference/right-panel identity visually uncertain at source quality",
}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("candidate", "detector-audit", "output"):
        parser.add_argument("--" + name, required=True, type=Path)
    args = parser.parse_args()
    if args.output.exists():
        parser.error("Refusing to overwrite a locked benchmark")
    if digest(args.candidate) != CANDIDATE_SHA256:
        raise ValueError("Candidate manifest differs from reviewed version")
    if digest(args.detector_audit) != DETECTOR_AUDIT_SHA256:
        raise ValueError("Detector audit differs from reviewed version")
    candidate = json.loads(args.candidate.read_text(encoding="utf-8"))
    audit = json.loads(args.detector_audit.read_text(encoding="utf-8"))
    if candidate["seed"] != SEED or candidate["recognition_scores_read"] is not False:
        raise ValueError("Candidate provenance differs")
    if audit["manifest_sha256"] != CANDIDATE_SHA256:
        raise ValueError("Detector audit was run on a different candidate")
    scene_audit = {row["trial"]: row for row in audit["scenes"]}
    pair_audit = {row["pair"]: row for row in audit["pairs"]}
    if (set(scene_audit) != {row["trial"] for row in candidate["scenes"]}
            or set(pair_audit) != {row["pair"] for row in candidate["pairs"]}):
        raise ValueError("Detector audit is incomplete")
    if not set(VISUAL_AMBIGUOUS) <= set(scene_audit):
        raise ValueError("Visual review refers to an unknown trial")

    locked_scenes = []
    group_identities = {"development": set(), "evaluation": set()}
    group_anchors = {"development": set(), "evaluation": set()}
    for row in candidate["scenes"]:
        if row["group"] not in group_identities:
            raise ValueError("Unknown split")
        identities = [identity(row["reference_member"]),
                      *(identity(member) for member in row["panel_members"])]
        if row["reference_identity"] != identities[0] or identities[1:] != row["panel_identities"]:
            raise ValueError("Source identity path mismatch")
        matches = [i for i, value in enumerate(identities[1:]) if value == identities[0]]
        if row["kind"] == "present" and matches != [row["target_panel"]]:
            raise ValueError("Present scene source label inconsistent")
        if row["kind"] == "absent" and (matches or row["target_panel"] is not None):
            raise ValueError("Absent scene source label inconsistent")
        if identities[1] == identities[2]:
            raise ValueError("Scene panels share source identity")
        group_identities[row["group"]].update(identities)
        group_anchors[row["group"]].add((row["fold"], identities[0]))
        audited = scene_audit[row["trial"]]
        if (audited["group"], audited["kind"], audited["stratum"]) != (
                row["group"], row["kind"], row["stratum"]):
            raise ValueError("Scene detector audit mismatch")
        if row["trial"] in VISUAL_AMBIGUOUS:
            status, reason = "AMBIGUOUS", VISUAL_AMBIGUOUS[row["trial"]]
        elif audited["status"] != "TWO_PANELS_MAPPED":
            status, reason = "EXCLUDED_DETECTOR", audited["status"]
        else:
            status = "USABLE_SOURCE_AND_SELF_REVIEW"
            reason = "BFW source identity, detector panel map and visual review agree"
        locked_scenes.append({**row, "lock_status": status, "lock_reason": reason,
                              "detector_boxes": audited["boxes"]})

    locked_pairs = []
    for row in candidate["pairs"]:
        if row["group"] not in group_identities:
            raise ValueError("Unknown split")
        same = identity(row["left"]) == identity(row["right"])
        if same != row["genuine"] or row["left"] == row["right"]:
            raise ValueError("Pair source identity or distinct-image rule mismatch")
        group_identities[row["group"]].update((identity(row["left"]), identity(row["right"])))
        audited = pair_audit[row["pair"]]
        if (audited["group"], audited["genuine"]) != (row["group"], row["genuine"]):
            raise ValueError("Pair detector audit mismatch")
        status = "USABLE_SOURCE_LABEL" if audited["status"] == "USABLE" else "EXCLUDED_DETECTOR"
        locked_pairs.append({**row, "lock_status": status})
    if group_identities["development"] & group_identities["evaluation"]:
        raise ValueError("Identity overlap between development and evaluation")
    if any(len(group_anchors[group]) != 60 for group in group_anchors):
        raise ValueError("Anchor count differs from protocol")

    locked = {
        "scope": "T-023 BFW controlled two-panel proxy; score-blind identity lock",
        "review": "One-person review of all 26 scene sheets; no independent image-label reviewer; pairs checked by source label and detector only",
        "candidate_sha256": CANDIDATE_SHA256,
        "detector_audit_sha256": DETECTOR_AUDIT_SHA256,
        "seed": SEED,
        "release_sha256": candidate["release_sha256"],
        "inner_md5": candidate["inner_md5"],
        "recognition_scores_read": False,
        "hard_negative_definition": "A P2-selected non-target box in a source-labeled target-absent scene; source identity, not P2, supplies ground truth",
        "scenes": locked_scenes,
        "pairs": locked_pairs,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(encoded(locked))
    print(json.dumps({
        "lock_sha256": digest(args.output),
        "anchor_count": {group: len(values) for group, values in group_anchors.items()},
        "identity_count": {group: len(values) for group, values in group_identities.items()},
        "scenes": {group: dict(Counter("/".join((row["kind"], row["stratum"], row["lock_status"]))
                                        for row in locked_scenes if row["group"] == group))
                   for group in group_identities},
        "pairs": {group: dict(Counter("/".join((str(row["genuine"]), row["lock_status"]))
                                       for row in locked_pairs if row["group"] == group))
                  for group in group_identities},
    }, ensure_ascii=False, default=str, indent=2))


if __name__ == "__main__":
    main()
