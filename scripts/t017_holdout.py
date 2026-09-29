"""Select unseen T-017 XQLFW scenes without using any recognition scores.

Private manifest and face images must stay outside Git.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path

import cv2
import numpy as np
from insightface.app import FaceAnalysis

from t011_xqlfw_baseline import EXPECTED, checked_zip, digest, load_pairs, prepare_pack
from t014_identity_split import order


SPLIT_SHA = "23542240bcc7b5d852ed469a35180dd7e68ae18942390bba25dc9106946692e2"
OLD_SCENE_SHA = "ae80423e479d616052a2bf2cc5a24d2dd45519bb12957525e33f8ab45b769c74"


def identity(member: str) -> str:
    return member.split("/")[-2]


def encode(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("images", "pairs", "model", "split-manifest", "old-scene-manifest", "output-dir"):
        parser.add_argument("--" + name, type=Path, required=True)
    args = parser.parse_args()
    if args.output_dir.exists() and any(args.output_dir.iterdir()):
        parser.error("Private output directory must be new or empty")
    source = {"images": digest(args.images), "pairs": digest(args.pairs), "model": digest(args.model)}
    if source != EXPECTED or digest(args.split_manifest) != SPLIT_SHA or digest(args.old_scene_manifest) != OLD_SCENE_SHA:
        raise ValueError("Pinned source/split/T-015 manifest differs")
    split = json.loads(args.split_manifest.read_text(encoding="utf-8"))
    old = json.loads(args.old_scene_manifest.read_text(encoding="utf-8"))
    if split["source_sha256"] != {key: source[key] for key in ("images", "pairs")}:
        raise ValueError("Split source mismatch")
    if old["split_manifest_sha256"] != SPLIT_SHA:
        raise ValueError("T-015 split mismatch")
    used_ids = set(split["pilot_excluded_identities"])
    for row in old["selected"]:
        for key in ("scene_zip_member", "present_ref_zip_member", "absent_ref_zip_member"):
            used_ids.add(identity(row[key]))
    evaluation_ids = set(split["splits"]["evaluation"]["identities"])
    development_ids = set(split["splits"]["development"]["identities"])
    if evaluation_ids & development_ids:
        raise ValueError("T-014 identity overlap")
    allowed_ids = evaluation_ids - used_ids
    if len(allowed_ids) < 64:
        raise ValueError("Too few unseen evaluation identities")
    args.output_dir.mkdir(parents=True)
    with checked_zip(args.images) as archive, checked_zip(args.model) as model_zip:
        lookup = {}
        for member in archive.namelist():
            if member.lower().endswith(".jpg"):
                key = (identity(member), member.split("/")[-1])
                if key in lookup:
                    raise ValueError("Duplicate image key")
                lookup[key] = member
        pairs = load_pairs(args.pairs, lookup)
        requested = sorted({member for left, right, _, _ in pairs for member in (left, right)})
        genuine = defaultdict(set)
        for left, right, same, _ in pairs:
            if same and left != right:
                genuine[left].add(right)
                genuine[right].add(left)
        allowed_members = [member for member in requested if identity(member) in allowed_ids]
        if not allowed_members:
            raise ValueError("No unseen evaluation images")
        ordered = sorted((member for member in allowed_members if genuine[member]), key=lambda value: order("T-017-clean-scenes-v1", value))
        root, onnx_hashes = prepare_pack(model_zip, args.output_dir / "cache")
        detector = FaceAnalysis(name="buffalo_sc", root=str(root), allowed_modules=["detection"], providers=["CPUExecutionProvider"])
        detector.prepare(ctx_id=-1, det_size=(640, 640), det_thresh=0.5)
        records = []
        counts = Counter()
        scene_ids = set()
        for member in ordered:
            if len(records) == 64:
                break
            if identity(member) in scene_ids:
                continue
            counts["scanned"] += 1
            image = cv2.imdecode(np.frombuffer(archive.read(member), dtype=np.uint8), cv2.IMREAD_COLOR)
            if image is None:
                counts["decode_error"] += 1
                continue
            faces = detector.get(image)
            if len(faces) < 2:
                counts["zero_or_one_detection"] += 1
                continue
            neighbors = [ref for ref in genuine[member] if identity(ref) == identity(member)]
            if not neighbors:
                counts["no_valid_genuine_ref"] += 1
                continue
            present = min(neighbors, key=lambda value: order("T-017-present-v1", value))
            absent = min((ref for ref in allowed_members if identity(ref) != identity(member)), key=lambda value: order("T-017-absent-v1\0" + member, value))
            sample = f"holdout-{len(records) + 1:03d}"
            files = {role: f"{sample}-{role}.jpg" for role in ("scene", "present_ref", "absent_ref")}
            for role, selected in (("scene", member), ("present_ref", present), ("absent_ref", absent)):
                (args.output_dir / files[role]).write_bytes(archive.read(selected))
            records.append({
                "sample": sample, "split": "holdout", "scene_zip_member": member,
                "present_ref_zip_member": present, "absent_ref_zip_member": absent,
                "files": files, "scene_shape_hw": list(image.shape[:2]),
                "detected_boxes_xyxy": [face.bbox.astype(float).tolist() for face in faces],
                "detected_scores": [float(face.det_score) for face in faces],
            })
            scene_ids.add(identity(member))
            counts["selected"] += 1
            if len(records) % 16 == 0:
                print(f"selected {len(records)}/64; scanned {counts['scanned']}", flush=True)
        manifest = {
            "scope": "T-017 clean holdout; private identifiers/images/boxes; no recognition scores",
            "source_sha256": source, "split_manifest_sha256": SPLIT_SHA,
            "old_scene_manifest_sha256": OLD_SCENE_SHA,
            "used_prior_known_identities": len(used_ids),
            "eligible_unseen_evaluation_identities": len(allowed_ids),
            "detector_model_sha256": onnx_hashes["det_500m.onnx"],
            "selection_seed": "T-017-clean-scenes-v1",
            "scans": dict(counts), "selected": records,
        }
        output = args.output_dir / "scene-manifest.json"
        output.write_bytes(encode(manifest))
        print(json.dumps({"selected": len(records), "scans": dict(counts), "used_prior_known_identities": len(used_ids), "eligible_unseen_evaluation_identities": len(allowed_ids), "manifest_sha256": digest(output)}, indent=2))


if __name__ == "__main__":
    main()
