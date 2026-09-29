"""Freeze a descriptive S8 threshold on T-014 development identities only.

Writes private pair scores and a small frozen config outside Git. Never reads
T-017 holdout scores or identities.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
import time
from collections import Counter
from pathlib import Path

import cv2
import numpy as np
from insightface.app import FaceAnalysis

from t011_xqlfw_baseline import EXPECTED, checked_zip, counts, digest, load_pairs, prepare_pack, select_threshold


SPLIT_SHA256 = "23542240bcc7b5d852ed469a35180dd7e68ae18942390bba25dc9106946692e2"


def write_once(path: Path, data: object) -> None:
    if path.exists():
        raise FileExistsError(f"Will not overwrite frozen artifact: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False) + "\n", encoding="utf-8")


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    for key in ("images", "pairs", "model", "split", "cache", "raw-output", "frozen-output"):
        p.add_argument("--" + key, type=Path, required=True)
    args = p.parse_args()
    if args.raw_output.exists() or args.frozen_output.exists():
        p.error("Outputs must not exist before threshold selection")
    source_hashes = {key: digest(getattr(args, key)) for key in ("images", "pairs", "model")}
    if source_hashes != EXPECTED or digest(args.split) != SPLIT_SHA256:
        raise ValueError("Source or T-014 split SHA differs from locked protocol")
    split = json.loads(args.split.read_text(encoding="utf-8"))
    if split["source_sha256"] != {key: source_hashes[key] for key in ("images", "pairs")}:
        raise ValueError("T-014 split source differs")
    dev_ids = set(split["splits"]["development"]["identities"])
    eval_ids = set(split["splits"]["evaluation"]["identities"])
    pilot_ids = set(split["pilot_excluded_identities"])
    if not dev_ids or dev_ids & eval_ids or dev_ids & pilot_ids:
        raise ValueError("Development identities overlap evaluation or pilot")

    with checked_zip(args.images) as image_zip, checked_zip(args.model) as model_zip:
        lookup = {}
        for name in image_zip.namelist():
            if name.lower().endswith(".jpg"):
                parts = name.split("/")
                key = (parts[-2], parts[-1])
                if key in lookup:
                    raise ValueError("Duplicate image key")
                lookup[key] = name
        all_pairs = load_pairs(args.pairs, lookup)
        dev_pairs = [(index, left, right, same) for index, (left, right, same, _) in enumerate(all_pairs)
                     if left.split("/")[-2] in dev_ids and right.split("/")[-2] in dev_ids]
        if not any(row[3] for row in dev_pairs) or all(row[3] for row in dev_pairs):
            raise ValueError("Development pair sample lacks one class")
        requested = sorted({name for _, left, right, _ in dev_pairs for name in (left, right)})
        model_root, onnx_hashes = prepare_pack(model_zip, args.cache)
        app = FaceAnalysis(name="buffalo_sc", root=str(model_root), allowed_modules=["detection", "recognition"], providers=["CPUExecutionProvider"])
        app.prepare(ctx_id=-1, det_size=(640, 640), det_thresh=0.5)
        features: dict[str, np.ndarray] = {}
        outcomes: Counter[str] = Counter()
        start = time.monotonic()
        for number, name in enumerate(requested, 1):
            image = cv2.imdecode(np.frombuffer(image_zip.read(name), dtype=np.uint8), cv2.IMREAD_COLOR)
            if image is None:
                outcomes["decode_error"] += 1
                continue
            faces = app.get(image)
            if len(faces) == 0:
                outcomes["zero_faces"] += 1
            elif len(faces) > 1:
                outcomes["multiple_faces"] += 1
            else:
                vector = np.asarray(faces[0].embedding, dtype=np.float64).ravel()
                norm = np.linalg.norm(vector)
                if vector.size != 512 or not np.isfinite(vector).all() or norm == 0:
                    raise ValueError("Unexpected embedding")
                features[name] = vector / norm
                outcomes["one_face"] += 1
            if number % 500 == 0:
                print(f"Development images: {number}/{len(requested)}", flush=True)
        rows = []
        excluded: Counter[str] = Counter()
        for index, left, right, same in dev_pairs:
            if left not in features or right not in features:
                excluded["genuine" if same else "impostor"] += 1
                continue
            rows.append({"pair_index": index, "genuine": bool(same), "score": float(np.dot(features[left], features[right]))})
    scores = np.asarray([row["score"] for row in rows], dtype=np.float64)
    labels = np.asarray([row["genuine"] for row in rows], dtype=bool)
    threshold = select_threshold(scores, labels)
    result = counts(scores, labels, threshold)
    raw = {"scope": "T-020 S8 development pair scores; no T-017 data", "source_sha256": source_hashes,
           "split_sha256": SPLIT_SHA256, "rows": rows}
    write_once(args.raw_output, raw)
    frozen = {"scope": "T-020 S8 development descriptive threshold; not deployment policy",
              "threshold": threshold, "selection_rule": "t011_select_threshold_min_abs_fmr_minus_fnmr_tie_lower_fmr_higher_threshold",
              "source_sha256": source_hashes, "split_sha256": SPLIT_SHA256,
              "script_sha256": digest(Path(__file__)), "raw_sha256": digest(args.raw_output),
              "model_onnx_sha256": onnx_hashes, "requested_images": len(requested),
              "image_outcomes": dict(outcomes), "eligible_pairs": {"genuine": sum(x[3] for x in dev_pairs), "impostor": sum(not x[3] for x in dev_pairs)},
              "excluded_pairs": dict(excluded), "usable_pair_counts_at_threshold": result,
              "fmr_on_development": result["false_accept"] / result["impostor"],
              "fnmr_on_development": result["false_reject"] / result["genuine"],
              "runtime_seconds": time.monotonic() - start,
              "environment": {"python": platform.python_version(), "opencv": cv2.__version__, "numpy": np.__version__, "provider": "CPUExecutionProvider"}}
    write_once(args.frozen_output, frozen)
    print(json.dumps({"frozen_sha256": digest(args.frozen_output), **frozen}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
