"""Select the frozen T-014 scene/reference sample before any candidate scores.

Private output contains face images, source identifiers and detector boxes. Keep
it outside Git. This stage imports no recognition model or candidate score.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import time
from collections import Counter, defaultdict
from pathlib import Path

import cv2
import numpy as np
from insightface.app import FaceAnalysis

from t011_xqlfw_baseline import EXPECTED, checked_zip, digest, load_pairs, prepare_pack
from t014_identity_split import order


def identity(member: str) -> str:
    return member.split("/")[-2]


def encode(data: object) -> bytes:
    return (json.dumps(data, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--images", required=True, type=Path)
    parser.add_argument("--pairs", required=True, type=Path)
    parser.add_argument("--model", required=True, type=Path)
    parser.add_argument("--split-manifest", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    args = parser.parse_args()
    if args.output_dir.exists() and any(args.output_dir.iterdir()):
        parser.error("Private output directory must be new or empty")
    hashes = {"images": digest(args.images), "pairs": digest(args.pairs), "model": digest(args.model)}
    if hashes != EXPECTED:
        raise ValueError("Pinned B0 asset hash mismatch")
    split_bytes = args.split_manifest.read_bytes()
    split = json.loads(split_bytes)
    if split["source_sha256"] != {key: hashes[key] for key in ("images", "pairs")}:
        raise ValueError("T-014 split source mismatch")
    if set(split["splits"]["development"]["identities"]) & set(split["splits"]["evaluation"]["identities"]):
        raise ValueError("Development/evaluation target identity overlap")

    args.output_dir.mkdir(parents=True)
    with checked_zip(args.images) as images, checked_zip(args.model) as model_zip:
        lookup = {}
        for member in images.namelist():
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
        root, model_hashes = prepare_pack(model_zip, args.output_dir / "cache")
        app = FaceAnalysis(name="buffalo_sc", root=str(root), allowed_modules=["detection"], providers=["CPUExecutionProvider"])
        app.prepare(ctx_id=-1, det_size=(640, 640), det_thresh=0.5)
        records = []
        scans = {}
        for split_name in ("development", "evaluation"):
            source = split["splits"][split_name]
            id_set = set(source["identities"])
            allowed = [member for member in requested if identity(member) in id_set]
            chosen_ids = set()
            counts = Counter()
            for member in source["scene_order"]:
                if len(chosen_ids) == 64:
                    break
                if identity(member) in chosen_ids or not genuine[member]:
                    continue
                counts["scanned"] += 1
                started = time.perf_counter()
                image = cv2.imdecode(np.frombuffer(images.read(member), dtype=np.uint8), cv2.IMREAD_COLOR)
                if image is None:
                    counts["decode_error"] += 1
                    continue
                faces = app.get(image)
                elapsed_ms = (time.perf_counter() - started) * 1000
                if len(faces) < 2:
                    counts["zero_or_one_detection"] += 1
                    continue
                present = sorted(genuine[member], key=lambda value: order("T-014-present-v1", value))[0]
                absent = sorted((value for value in allowed if identity(value) != identity(member)), key=lambda value: order("T-014-absent-v1\0" + member, value))[0]
                index = len(chosen_ids) + 1
                prefix = f"{split_name}-{index:03d}"
                files = {"scene": prefix + "-scene.jpg", "present_ref": prefix + "-present.jpg", "absent_ref": prefix + "-absent.jpg"}
                for role, selected in (("scene", member), ("present_ref", present), ("absent_ref", absent)):
                    (args.output_dir / files[role]).write_bytes(images.read(selected))
                records.append({
                    "sample": prefix,
                    "split": split_name,
                    "scene_zip_member": member,
                    "present_ref_zip_member": present,
                    "absent_ref_zip_member": absent,
                    "files": files,
                    "scene_shape_hw": list(image.shape[:2]),
                    "detected_boxes_xyxy": [face.bbox.astype(float).tolist() for face in faces],
                    "detected_scores": [float(face.det_score) for face in faces],
                    "decode_detect_ms": elapsed_ms,
                    "selection_index_in_scene_order": source["scene_order"].index(member),
                })
                chosen_ids.add(identity(member))
                counts["selected"] += 1
                if index % 16 == 0:
                    print(f"{split_name}: selected {index}/64; scanned {counts['scanned']}", flush=True)
            scans[split_name] = dict(counts)
        private = {
            "scope": "T-015 pre-label scene selection; no recognition scores; private identifiers/images",
            "source_sha256": hashes,
            "split_manifest_sha256": hashlib.sha256(split_bytes).hexdigest(),
            "detector_model_sha256": model_hashes["det_500m.onnx"],
            "detector_input": [640, 640],
            "detector_threshold": 0.5,
            "selection_rule": "first 64 >=2 detections, genuine neighbor, <=1 scene per source identity per split",
            "scans": scans,
            "selected": records,
        }
        output = args.output_dir / "scene-manifest.json"
        output.write_bytes(encode(private))
        print(json.dumps({"scans": scans, "manifest_sha256": digest(output), "records": len(records)}, indent=2))


if __name__ == "__main__":
    main()
