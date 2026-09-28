"""Select a reproducible private XQLFW sample for manual S4 feasibility audit.

The script does not assign target labels or score an S4 method. It writes face
images and per-image identifiers only to the requested private output folder.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path

from t011_xqlfw_baseline import EXPECTED, checked_zip, digest, load_pairs, prepare_pack


def rank(seed: str, value: str) -> str:
    return hashlib.sha256(f"{seed}\0{value}".encode("utf-8")).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--images", required=True, type=Path)
    parser.add_argument("--pairs", required=True, type=Path)
    parser.add_argument("--model", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--sample-count", type=int, default=24)
    parser.add_argument("--max-scan", type=int, default=600)
    parser.add_argument("--seed", default="T-013-v1")
    args = parser.parse_args()
    if args.sample_count <= 0 or args.max_scan <= 0:
        raise ValueError("sample-count and max-scan must be positive")
    if args.output_dir.exists() and any(args.output_dir.iterdir()):
        raise ValueError("Output directory must be new or empty")

    actual = {"images": digest(args.images), "pairs": digest(args.pairs), "model": digest(args.model)}
    if actual != EXPECTED:
        raise ValueError("Input hash differs from B0 E2")

    import cv2
    import numpy as np
    import onnxruntime as ort
    from insightface import __version__ as insightface_version
    from insightface.app import FaceAnalysis

    with checked_zip(args.images) as archive, checked_zip(args.model) as model_zip:
        lookup = {}
        for name in archive.namelist():
            if name.lower().endswith(".jpg"):
                parts = name.split("/")
                key = (parts[-2], parts[-1])
                if key in lookup:
                    raise ValueError("Duplicate XQLFW image key")
                lookup[key] = name
        pairs = load_pairs(args.pairs, lookup)
        requested = sorted({name for left, right, _, _ in pairs for name in (left, right)})
        if len(requested) != 7263 or len(pairs) != 6000:
            raise ValueError("Image/pair manifest differs from B0")

        genuine_neighbors: dict[str, set[str]] = defaultdict(set)
        for left, right, same, _ in pairs:
            if same and left != right:
                genuine_neighbors[left].add(right)
                genuine_neighbors[right].add(left)

        args.output_dir.mkdir(parents=True, exist_ok=True)
        model_root, onnx_hashes = prepare_pack(model_zip, args.output_dir / "cache")
        app = FaceAnalysis(
            name="buffalo_sc",
            root=str(model_root),
            allowed_modules=["detection"],
            providers=["CPUExecutionProvider"],
        )
        app.prepare(ctx_id=-1, det_size=(640, 640), det_thresh=0.5)

        ordered = sorted(requested, key=lambda name: (rank(args.seed, name), name))
        selected = []
        selected_identities = set()
        scan_counts = Counter()
        for name in ordered[: args.max_scan]:
            image = cv2.imdecode(np.frombuffer(archive.read(name), dtype=np.uint8), cv2.IMREAD_COLOR)
            if image is None:
                scan_counts["decode_error"] += 1
                continue
            faces = app.get(image)
            category = "zero" if not faces else "one" if len(faces) == 1 else "multiple"
            scan_counts[category] += 1
            if len(faces) <= 1 or name not in genuine_neighbors:
                continue
            identity = name.split("/")[-2]
            if identity in selected_identities:
                continue
            references = sorted(genuine_neighbors[name], key=lambda item: (rank(args.seed, item), item))
            present_ref = references[0]
            absent_refs = sorted(
                (item for item in requested if item.split("/")[-2] != identity),
                key=lambda item: (rank(args.seed + "-absent-" + name, item), item),
            )
            absent_ref = absent_refs[0]

            number = len(selected) + 1
            scene_file = f"sample-{number:02d}-scene.jpg"
            present_file = f"sample-{number:02d}-present-ref.jpg"
            absent_file = f"sample-{number:02d}-absent-ref.jpg"
            for filename, member in (
                (scene_file, name), (present_file, present_ref), (absent_file, absent_ref)
            ):
                (args.output_dir / filename).write_bytes(archive.read(member))
            selected.append({
                "sample": number,
                "scene_zip_member": name,
                "present_ref_zip_member": present_ref,
                "absent_ref_zip_member": absent_ref,
                "files": {"scene": scene_file, "present_ref": present_file, "absent_ref": absent_file},
                "scene_shape_wh": [int(image.shape[1]), int(image.shape[0])],
                "detected_boxes_xyxy": [[float(x) for x in face.bbox] for face in faces],
                "detected_scores": [float(face.det_score) for face in faces],
                "manual_label": "PENDING",
            })
            selected_identities.add(identity)
            if len(selected) == args.sample_count:
                break

    private_manifest = {
        "scope": "private manual feasibility audit; not an S4 experiment or benchmark result",
        "seed": args.seed,
        "source_sha256": actual,
        "onnx_sha256": onnx_hashes,
        "runtime": {"cv2": cv2.__version__, "onnxruntime": ort.__version__, "insightface": insightface_version},
        "scan_counts": dict(scan_counts),
        "selected": selected,
    }
    (args.output_dir / "private-manifest.json").write_text(
        json.dumps(private_manifest, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    summary = {
        "scope": "detector-only pilot sampling; manual labels not yet assigned",
        "seed": args.seed,
        "source_sha256": actual,
        "requested_images": len(requested),
        "max_scan": args.max_scan,
        "sample_goal": args.sample_count,
        "scanned_images": sum(scan_counts.values()),
        "scan_counts": dict(scan_counts),
        "selected_multi_detection_scenes": len(selected),
        "selected_distinct_identities": len(selected_identities),
        "manual_review_status": "PENDING",
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
