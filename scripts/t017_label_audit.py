"""Lock T-017 clean self-confirm labels after box-free visual points and R50.

R50 is audit-only. This module never imports or runs MobileFaceNet scores.
All per-sample names, images and audit scores remain in a private output.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path

import cv2
import numpy as np
from insightface import model_zoo
from insightface.app import FaceAnalysis

from t011_xqlfw_baseline import EXPECTED, checked_zip, digest, load_pairs, prepare_pack
from t011_xqlfw_r50_comparison import R50_ZIP_SHA256, prepare_r50, unit


SCENE_SHA256 = "5ca44481ce26abe62e2e699bdaae44c7b9227f2a5c54f6ac9d865330ad658290"
VISUAL_SHA256 = "c19136dbb743dcbd15ef177886bd064444c312a9ee44e7f5d6d0dbd9a2a0d728"


def identity(member: str) -> str:
    return member.split("/")[-2]


def encode(data: object) -> bytes:
    return (json.dumps(data, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def face_data(app: FaceAnalysis, r50, path: Path):
    image = cv2.imread(str(path))
    if image is None:
        return None, [], np.empty((0, 512))
    faces = app.get(image)
    vectors = np.asarray([unit(r50.get(image, face)) for face in faces], dtype=np.float64).reshape(-1, 512)
    return image, faces, vectors


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    for name in ("images", "pairs", "model", "r50-model", "scene-manifest", "visual-review", "output", "cache"):
        p.add_argument("--" + name, type=Path, required=True)
    a = p.parse_args()
    if a.output.exists():
        p.error("Private label output already exists")
    actual = {"images": digest(a.images), "pairs": digest(a.pairs), "model": digest(a.model), "r50_model": digest(a.r50_model)}
    if {key: actual[key] for key in EXPECTED} != EXPECTED or actual["r50_model"] != R50_ZIP_SHA256:
        raise ValueError("Pinned source or model hash differs")
    scene_bytes = a.scene_manifest.read_bytes()
    visual_bytes = a.visual_review.read_bytes()
    if hashlib.sha256(scene_bytes).hexdigest() != SCENE_SHA256 or hashlib.sha256(visual_bytes).hexdigest() != VISUAL_SHA256:
        raise ValueError("T-017 scene/visual lock differs")
    scene = json.loads(scene_bytes)
    visual = json.loads(visual_bytes)
    if scene["source_sha256"] != {key: actual[key] for key in EXPECTED}:
        raise ValueError("Scene manifest uses different source")
    if visual["scene_manifest_sha256"] != hashlib.sha256(scene_bytes).hexdigest():
        raise ValueError("Visual review does not match selected scene manifest")
    by_sample = {row["sample"]: row for row in visual["labels"]}
    if len(by_sample) != 64 or len(scene["selected"]) != 64:
        raise ValueError("Expected one visual label for every selected scene")
    with checked_zip(a.images) as images, checked_zip(a.model) as model_zip, checked_zip(a.r50_model) as r50_zip:
        lookup = {}
        for member in images.namelist():
            if member.lower().endswith(".jpg"):
                key = (identity(member), member.split("/")[-1])
                if key in lookup:
                    raise ValueError("Duplicate image key")
                lookup[key] = member
        pairs = load_pairs(a.pairs, lookup)
        genuine = {frozenset((left, right)) for left, right, same, _ in pairs if same and left != right}
        root, _ = prepare_pack(model_zip, a.cache)
        r50_path = prepare_r50(r50_zip, a.cache)
        app = FaceAnalysis(name="buffalo_sc", root=str(root), allowed_modules=["detection"], providers=["CPUExecutionProvider"])
        app.prepare(ctx_id=-1, det_size=(640, 640), det_thresh=0.5)
        r50 = model_zoo.get_model(str(r50_path), providers=["CPUExecutionProvider"])
        r50.prepare(ctx_id=-1)
        if tuple(r50.input_size) != (112, 112):
            raise ValueError("Unexpected R50 input")
        records = []
        for position, row in enumerate(scene["selected"], 1):
            sample = row["sample"]
            v = by_sample[sample]
            members = {"scene": row["scene_zip_member"], "present_ref": row["present_ref_zip_member"], "absent_ref": row["absent_ref_zip_member"]}
            reasons = []
            if identity(members["scene"]) != identity(members["present_ref"]):
                reasons.append("PRESENT_SOURCE_IDENTITY_MISMATCH")
            if identity(members["scene"]) == identity(members["absent_ref"]):
                reasons.append("ABSENT_SOURCE_IDENTITY_MISMATCH")
            if frozenset((members["scene"], members["present_ref"])) not in genuine:
                reasons.append("NO_GENUINE_SOURCE_PAIR")
            for role, member in members.items():
                if a.scene_manifest.parent.joinpath(row["files"][role]).read_bytes() != images.read(member):
                    reasons.append(role.upper() + "_BYTES_MISMATCH")
            image_s, faces_s, vec_s = face_data(app, r50, a.scene_manifest.parent / row["files"]["scene"])
            _, faces_p, vec_p = face_data(app, r50, a.scene_manifest.parent / row["files"]["present_ref"])
            _, faces_a, vec_a = face_data(app, r50, a.scene_manifest.parent / row["files"]["absent_ref"])
            boxes = np.asarray([face.bbox for face in faces_s], dtype=float).reshape(-1, 4)
            original = np.asarray(row["detected_boxes_xyxy"], dtype=float).reshape(-1, 4)
            stable = boxes.shape == original.shape and np.max(np.abs(boxes - original), initial=0.0) <= 1.0
            if not stable:
                reasons.append("SCENE_DETECTION_CHANGED")
            target_index = None
            point = v.get("target_center_normalized")
            if v["scene_category"] == "false_extra_detection":
                reasons.append("FALSE_EXTRA_DETECTION")
            elif v["scene_category"] != "true_multi_person_clear_target":
                reasons.append("VISUAL_AMBIGUOUS")
            elif point is None or image_s is None:
                reasons.append("VISUAL_POINT_MISSING")
            else:
                x, y = point[0] * image_s.shape[1], point[1] * image_s.shape[0]
                contained = [i for i, (x1, y1, x2, y2) in enumerate(boxes) if x1 <= x <= x2 and y1 <= y <= y2]
                if len(contained) == 0:
                    reasons.append("TARGET_MISSED_BY_DETECTOR")
                elif len(contained) > 1:
                    reasons.append("TARGET_BOX_AMBIGUOUS")
                else:
                    target_index = contained[0]
            if len(faces_s) < 2:
                reasons.append("SCENE_NOT_MULTIDETECTION_ON_RERUN")
            if len(faces_p) != 1:
                reasons.append("PRESENT_REFERENCE_NOT_ONE_FACE")
            if len(faces_a) != 1:
                reasons.append("ABSENT_REFERENCE_NOT_ONE_FACE")
            present_scores = absent_scores = None
            if target_index is not None and len(faces_p) == 1 and len(faces_s) >= 2:
                present_scores = (vec_s @ vec_p[0]).tolist()
                target_score = present_scores[target_index]
                if any(target_score <= score for i, score in enumerate(present_scores) if i != target_index):
                    reasons.append("R50_PRESENT_RANK_CONFLICT")
            if target_index is not None and len(faces_a) == 1 and len(faces_s) >= 2:
                absent_scores = (vec_s @ vec_a[0]).tolist()
                if present_scores is not None and max(absent_scores) >= present_scores[target_index]:
                    reasons.append("R50_ABSENT_RELATIVE_CONFLICT")
            common = [reason for reason in reasons if reason != "ABSENT_REFERENCE_NOT_ONE_FACE" and reason != "R50_ABSENT_RELATIVE_CONFLICT"]
            present_status = "SELF_CONFIRMED" if not common else "AMBIGUOUS"
            absent_status = "SELF_CONFIRMED" if not reasons and v["absent_visual"] == "appears_absent_unverified" else "AMBIGUOUS"
            records.append({
                "sample": sample, "split": row["split"], "scene_detection_count": len(faces_s),
                "present_reference_detection_count": len(faces_p), "absent_reference_detection_count": len(faces_a),
                "scene_category": v["scene_category"],
                "target_center_normalized": point, "ground_truth_box_index": target_index,
                "stable_detector_boxes": bool(stable), "reasons": reasons,
                "present_status": present_status, "absent_status": absent_status,
                "r50_present_scores": present_scores, "r50_absent_scores": absent_scores,
            })
            if position % 16 == 0:
                print(f"audited {position}/64", flush=True)
    result = {
        "scope": "T-017 private clean self-confirm labels; visual point before detector box; R50 audit-only; no independent reviewer; no MBF candidate scores",
        "source_sha256": actual,
        "scene_manifest_sha256": hashlib.sha256(scene_bytes).hexdigest(),
        "visual_review_sha256": hashlib.sha256(visual_bytes).hexdigest(),
        "records": records,
    }
    a.output.write_bytes(encode(result))
    public = {}
    for split_name in ("holdout",):
        group = [r for r in records if r["split"] == split_name]
        public[split_name] = {
            "scenes": len(group),
            "scene_categories": dict(Counter(r["scene_category"] for r in group)),
            "present_status": dict(Counter(r["present_status"] for r in group)),
            "absent_status": dict(Counter(r["absent_status"] for r in group)),
            "reasons": dict(Counter(reason for r in group for reason in r["reasons"])),
        }
    print(json.dumps({"label_manifest_sha256": digest(a.output), "audit": public}, indent=2))


if __name__ == "__main__":
    main()
