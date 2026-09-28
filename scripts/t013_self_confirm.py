"""Controlled T-013 metadata/visual/embedding cross-check on the fixed private pilot.

This script never assigns visual labels. It only checks the earlier visual
screening against source metadata and B0 embedding ranks. Per-case output is
private and must not be committed.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

import cv2
import numpy as np
from insightface.app import FaceAnalysis

from t011_xqlfw_baseline import EXPECTED, checked_zip, digest, load_pairs, prepare_pack


def identity(member: str) -> str:
    return member.split("/")[-2]


def face_data(app: FaceAnalysis, path: Path) -> tuple[np.ndarray, np.ndarray]:
    image = cv2.imread(str(path))
    if image is None:
        raise ValueError("Pilot image could not be decoded")
    faces = app.get(image)
    boxes = np.asarray([face.bbox for face in faces], dtype=np.float64).reshape(-1, 4)
    vectors = []
    for face in faces:
        vector = np.asarray(face.embedding, dtype=np.float64).ravel()
        norm = np.linalg.norm(vector)
        if vector.size != 512 or not np.isfinite(vector).all() or not np.isfinite(norm) or norm == 0:
            raise ValueError("Invalid B0 embedding")
        vectors.append(vector / norm)
    return boxes, np.asarray(vectors, dtype=np.float64).reshape(-1, 512)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--images", type=Path, required=True)
    parser.add_argument("--pairs", type=Path, required=True)
    parser.add_argument("--model", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--cache", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        parser.error("private output already exists")

    actual = {"images": digest(args.images), "pairs": digest(args.pairs), "model": digest(args.model)}
    if actual != EXPECTED:
        raise ValueError("Source hash differs from the B0 reference")
    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    if manifest["source_sha256"] != actual or len(manifest["selected"]) != 24:
        raise ValueError("Pilot manifest differs from the pinned source or 24-scene selection")

    with checked_zip(args.images) as archive, checked_zip(args.model) as model_zip:
        lookup = {}
        for member in archive.namelist():
            if member.lower().endswith(".jpg"):
                parts = member.split("/")
                lookup[(parts[-2], parts[-1])] = member
        pairs = load_pairs(args.pairs, lookup)
        genuine = {
            frozenset((left, right))
            for left, right, same, _ in pairs
            if same and left != right
        }
        model_root, _ = prepare_pack(model_zip, args.cache)
        app = FaceAnalysis(
            name="buffalo_sc",
            root=str(model_root),
            allowed_modules=["detection", "recognition"],
            providers=["CPUExecutionProvider"],
        )
        app.prepare(ctx_id=-1, det_size=(640, 640), det_thresh=0.5)

        records = []
        for number, row in enumerate(manifest["selected"], 1):
            sample = row["sample"]
            scene_member = row["scene_zip_member"]
            present_member = row["present_ref_zip_member"]
            absent_member = row["absent_ref_zip_member"]
            members = {
                "scene": scene_member,
                "present_ref": present_member,
                "absent_ref": absent_member,
            }
            metadata_reasons = []
            if identity(scene_member) != identity(present_member):
                metadata_reasons.append("PRESENT_IDENTITY_MISMATCH")
            if identity(scene_member) == identity(absent_member):
                metadata_reasons.append("ABSENT_IDENTITY_MISMATCH")
            if frozenset((scene_member, present_member)) not in genuine:
                metadata_reasons.append("NO_GENUINE_SOURCE_PAIR")
            for role, member in members.items():
                local = args.manifest.parent / row["files"][role]
                if member not in archive.namelist() or local.read_bytes() != archive.read(member):
                    metadata_reasons.append(f"{role.upper()}_BYTES_MISMATCH")

            scene_boxes, scene_vecs = face_data(app, args.manifest.parent / row["files"]["scene"])
            present_boxes, present_vecs = face_data(app, args.manifest.parent / row["files"]["present_ref"])
            absent_boxes, absent_vecs = face_data(app, args.manifest.parent / row["files"]["absent_ref"])
            original_boxes = np.asarray(row["detected_boxes_xyxy"], dtype=np.float64).reshape(-1, 4)
            box_consistent = (
                scene_boxes.shape == original_boxes.shape
                and np.max(np.abs(scene_boxes - original_boxes), initial=0.0) <= 1.0
            )

            visual = row.get("visual_screening_codex", {})
            scene_category = visual.get("scene_category", "VISUAL_MISSING")
            target_index = visual.get("target_detection_index")
            present_status = "AMBIGUOUS"
            present_reason = None
            absent_status = "AMBIGUOUS"
            absent_reason = None
            present_scores = None
            absent_scores = None
            target_score = None

            if scene_category == "false_extra_detection":
                present_reason = absent_reason = "NOT_MULTIPERSON"
            elif scene_category != "true_multi_person_clear_target":
                present_reason = absent_reason = "VISUAL_AMBIGUOUS"
            elif metadata_reasons:
                present_reason = absent_reason = "SOURCE_MISMATCH"
            elif not box_consistent or len(scene_vecs) < 2 or not isinstance(target_index, int) or target_index >= len(scene_vecs):
                present_reason = absent_reason = "SCENE_RERUN_MISMATCH"
            elif len(present_vecs) != 1:
                present_reason = absent_reason = "PRESENT_REFERENCE_NOT_ONE_FACE"
            else:
                present_scores = scene_vecs @ present_vecs[0]
                target_score = float(present_scores[target_index])
                competing = np.delete(present_scores, target_index)
                if len(competing) == 0 or not np.all(target_score > competing):
                    present_reason = absent_reason = "PRESENT_RANK_CONFLICT"
                else:
                    present_status = "SELF_CONFIRMED"
                    present_reason = "METADATA_VISUAL_RANK_CONSISTENT"
                    if len(absent_vecs) != 1:
                        absent_reason = "ABSENT_REFERENCE_NOT_ONE_FACE"
                    elif visual.get("absent_reference") != "appears_absent_unverified":
                        absent_reason = "ABSENT_VISUAL_UNCERTAIN"
                    else:
                        absent_scores = scene_vecs @ absent_vecs[0]
                        if float(np.max(absent_scores)) >= target_score:
                            absent_reason = "ABSENT_RELATIVE_SCORE_CONFLICT"
                        else:
                            absent_status = "SELF_CONFIRMED"
                            absent_reason = "METADATA_VISUAL_RELATIVE_SCORE_CONSISTENT"

            records.append({
                "sample": sample,
                "scene_category": scene_category,
                "metadata_reasons": metadata_reasons,
                "scene_detection_count": len(scene_vecs),
                "rerun_boxes_consistent": bool(box_consistent),
                "present_reference_detection_count": len(present_vecs),
                "absent_reference_detection_count": len(absent_vecs),
                "visual_target_detection_index": target_index,
                "present_status": present_status,
                "present_reason": present_reason,
                "present_scores_by_detection": present_scores.tolist() if present_scores is not None else None,
                "present_target_score": target_score,
                "absent_status": absent_status,
                "absent_reason": absent_reason,
                "absent_scores_by_detection": absent_scores.tolist() if absent_scores is not None else None,
            })
            if number % 4 == 0:
                print(f"checked {number}/24 scenes", flush=True)

    summary = {
        "scope": "T-013 self-confirm pilot, not independent ground truth or S4 performance",
        "source_sha256": actual,
        "scene_categories": dict(Counter(record["scene_category"] for record in records)),
        "present_status": dict(Counter(record["present_status"] for record in records)),
        "present_reasons": dict(Counter(record["present_reason"] for record in records)),
        "absent_status": dict(Counter(record["absent_status"] for record in records)),
        "absent_reasons": dict(Counter(record["absent_reason"] for record in records)),
        "records": records,
    }
    args.output.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    public_summary = {key: value for key, value in summary.items() if key != "records"}
    print(json.dumps(public_summary, indent=2))


if __name__ == "__main__":
    main()
