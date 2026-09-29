"""Lock score-blind T-022 labels after source, detector and visual audit.

Only generic trial IDs and review reasons live in this script. The output manifest
contains face-source identities, so keep it outside Git. No recognition model,
cosine score, P1 or P2 output is loaded here.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path


EXPECTED_CANDIDATE_SHA256 = "9a200393e017f8e5a4be6fd13f16d8101f1c84b47e7fb166837c7e5f76f38c83"
EXPECTED_DETECTOR_AUDIT_SHA256 = "721782910733e37bfb93e042bc828ad6cf7b7dc3ca2b19574f1229f315745e33"

# One-person self-review of all 20 contact sheets before opening any cosine.
# Exclude both scene types for an anchor if either has uncertain identity,
# additional visible faces, or a questionable target-to-box association.
VISUAL_AMBIGUOUS = {
    "development-016": "Extra/background person or face cannot be ruled out",
    "development-023": "Additional visible person at source-panel edge",
    "development-024": "Extra/background person or face cannot be ruled out",
    "development-034": "Additional visible background face in target source panel",
    "development-035": "Additional visible background face in non-target source panel",
    "development-048": "Additional visible background face in target source panel",
    "development-050": "Extra/background person or face cannot be ruled out",
    "development-061": "Extra/background person or face cannot be ruled out",
    "development-064": "Additional visible person at target source-panel edge",
    "development-073": "Reference image contains additional visible face",
    "development-089": "Additional visible background people in non-target source panel",
    "development-092": "Additional visible person at target source-panel edge",
    "development-093": "Additional visible person at target source-panel edge",
    "development-094": "Reference-to-target identity is visually uncertain at this quality",
    "evaluation-001": "Additional visible person in non-target source panel",
    "evaluation-014": "Additional visible person in non-target source panel",
    "evaluation-016": "Additional visible persons in target source panel",
    "evaluation-017": "Additional visible person in non-target source panel",
    "evaluation-034": "Additional visible persons in source panels",
    "evaluation-058": "Reference image contains additional visible faces",
    "evaluation-060": "Additional visible person at non-target source-panel edge",
}


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def identity(member: str) -> str:
    return member.replace("\\", "/").split("/")[-2]


def encoded_json(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidate", required=True, type=Path)
    parser.add_argument("--detector-audit", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    if args.output.exists():
        parser.error("Lock output already exists")
    if digest(args.candidate) != EXPECTED_CANDIDATE_SHA256:
        raise ValueError("Candidate manifest differs from the visually reviewed version")
    if digest(args.detector_audit) != EXPECTED_DETECTOR_AUDIT_SHA256:
        raise ValueError("Detector audit differs from the visually reviewed version")
    candidate = json.loads(args.candidate.read_text(encoding="utf-8"))
    detector = json.loads(args.detector_audit.read_text(encoding="utf-8"))
    if detector["manifest_sha256"] != EXPECTED_CANDIDATE_SHA256:
        raise ValueError("Detector and candidate manifests do not match")
    audited = {row["trial"]: row for row in detector["scenes"]}
    candidate_trials = {row["trial"] for row in candidate["scenes"]}
    if set(audited) != candidate_trials:
        raise ValueError("Scene audit is incomplete")

    by_anchor = {}
    for row in candidate["scenes"]:
        anchor = row["trial"].rsplit("-", 1)[0]
        by_anchor.setdefault(anchor, {})[row["kind"]] = row
    if any(set(kinds) != {"present", "absent"} for kinds in by_anchor.values()):
        raise ValueError("Every anchor must have both scene types")
    if set(VISUAL_AMBIGUOUS) - set(by_anchor):
        raise ValueError("Visual review refers to a missing anchor")

    locked_scenes = []
    for anchor, kinds in sorted(by_anchor.items()):
        both_mapped = all(audited[row["trial"]]["status"] == "TWO_PANELS_MAPPED"
                          for row in kinds.values())
        for kind in ("present", "absent"):
            row = kinds[kind]
            if anchor in VISUAL_AMBIGUOUS:
                status = "AMBIGUOUS"
                reason = VISUAL_AMBIGUOUS[anchor]
            elif not both_mapped:
                status = "EXCLUDED_DETECTOR"
                reason = "At least one paired scene failed source/scene detector audit"
            else:
                status = "USABLE_SELF_CONFIRMED"
                reason = "Official source identity/pair label, panel map and visual contact sheet agree"
            locked_scenes.append({**row, "visual_review": status,
                                  "box_audit": audited[row["trial"]]["status"],
                                  "lock_status": status, "lock_reason": reason,
                                  "boxes": audited[row["trial"]]["boxes"]})

    source_identity_sets = {group: set() for group in ("development", "evaluation")}
    for row in locked_scenes:
        for member in [row["reference_member"], *row["panel_members"]]:
            source_identity_sets[row["group"]].add(identity(member))
    if source_identity_sets["development"] & source_identity_sets["evaluation"]:
        raise ValueError("Scene identity leakage")

    # Lock labels of the official XQLFW pairs, after detector eligibility.
    # Exclude exact source-image pairs also used in any controlled scene, so
    # ordinary impostor examples are not the same image pairs as S4 trials.
    scene_pairs = {frozenset((row["reference_member"], member))
                   for row in locked_scenes if row["lock_status"] == "USABLE_SELF_CONFIRMED"
                   for member in row["panel_members"]}
    locked_pairs = {}
    for group in ("development", "evaluation"):
        audit_pairs = {row["pair_index"]: row for row in detector["pairs"][group]}
        source_pairs = candidate["pairs"][group]
        if set(audit_pairs) != {row["index"] for row in source_pairs}:
            raise ValueError("Pair audit is incomplete")
        locked_pairs[group] = []
        for row in source_pairs:
            audit = audit_pairs[row["index"]]
            if (identity(row["left"]) == identity(row["right"])) != row["genuine"]:
                raise ValueError("Pair identity label differs")
            if audit["status"] != "USABLE":
                status = "EXCLUDED_DETECTOR"
            elif not row["genuine"] and frozenset((row["left"], row["right"])) in scene_pairs:
                status = "EXCLUDED_SCENE_PAIR_OVERLAP"
            else:
                status = "USABLE_SOURCE_LABEL"
            locked_pairs[group].append({**row, "lock_status": status})
    pair_id_sets = {group: {identity(value) for row in rows if row["lock_status"] == "USABLE_SOURCE_LABEL"
                            for value in (row["left"], row["right"])}
                    for group, rows in locked_pairs.items()}
    if (pair_id_sets["development"] | source_identity_sets["development"]) & (
            pair_id_sets["evaluation"] | source_identity_sets["evaluation"]):
        raise ValueError("Pair/scene identity leakage between development and evaluation")

    result = {
        "scope": "T-022 score-blind locked synthetic/controlled XQLFW S8 benchmark; NOT exam-room data",
        "review": "One-person self-confirmation of all 20 contact sheets; no independent reviewer",
        "candidate_sha256": EXPECTED_CANDIDATE_SHA256,
        "detector_audit_sha256": EXPECTED_DETECTOR_AUDIT_SHA256,
        "seed": candidate["seed"],
        "source_sha256": candidate["source_sha256"],
        "hard_negative_definition": "On an eligible target-absent scene only, a non-target face selected by frozen T-017 P2 is an S4-derived hard negative for the reference identity; source metadata, not P2 score, establishes non-target ground truth",
        "recognition_scores_read": False,
        "scenes": locked_scenes,
        "pairs": locked_pairs,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(encoded_json(result))
    summary = {"lock_sha256": digest(args.output), "groups": {}}
    for group in ("development", "evaluation"):
        summary["groups"][group] = {
            "scenes": {kind: dict(Counter(row["lock_status"] for row in locked_scenes
                                          if row["group"] == group and row["kind"] == kind))
                       for kind in ("present", "absent")},
            "pairs": {kind: dict(Counter(row["lock_status"] for row in locked_pairs[group]
                                         if row["genuine"] == genuine))
                      for kind, genuine in (("genuine", True), ("ordinary_impostor", False))},
            "locked_source_identities": len(source_identity_sets[group] | pair_id_sets[group]),
        }
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
