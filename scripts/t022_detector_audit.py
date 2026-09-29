"""Audit T-022 source/pair/scene eligibility with SCRFD only, before cosine.

Ground-truth identities come from the score-blind construction manifest, never
from detector boxes. Boxes are only matched to the known left/right image tiles.
The output remains private because it contains source image member names.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import zipfile
from collections import Counter
from pathlib import Path

import cv2
import numpy as np
from insightface.app import FaceAnalysis

from t011_xqlfw_baseline import prepare_pack


MODEL_SHA256 = "57d31b56b6ffa911c8a73cfc1707c73cab76efe7f13b675a05223bf42de47c72"


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def decode(encoded: bytes) -> np.ndarray:
    result = cv2.imdecode(np.frombuffer(encoded, dtype=np.uint8), cv2.IMREAD_COLOR)
    if result is None:
        raise ValueError("Image could not be decoded")
    return result


def source_status(app: FaceAnalysis, archive: zipfile.ZipFile, member: str) -> str:
    image = decode(archive.read(member))
    faces = app.get(image)
    if len(faces) == 0:
        return "ZERO_DETECTION"
    if len(faces) > 1:
        return "MULTIPLE_DETECTIONS"
    return "ONE_DETECTION"


def scene_status(app: FaceAnalysis, path: Path) -> tuple[str, list[dict]]:
    image = decode(path.read_bytes())
    if image.shape != (250, 516, 3):
        raise ValueError(f"Controlled scene shape differs: {path}")
    faces = app.get(image)
    boxes = []
    for face in faces:
        box = [float(value) for value in face.bbox]
        center = (box[0] + box[2]) / 2
        panel = 0 if center < 250 else (1 if center >= 266 else None)
        boxes.append({"xyxy": box, "panel": panel})
    if len(boxes) != 2:
        return "NOT_TWO_DETECTIONS", boxes
    if sorted(box["panel"] for box in boxes if box["panel"] is not None) != [0, 1]:
        return "BOX_PANEL_AMBIGUOUS", boxes
    return "TWO_PANELS_MAPPED", boxes


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("images", "model", "manifest", "output"):
        parser.add_argument("--" + name, required=True, type=Path)
    parser.add_argument("--expected-manifest-sha256", required=True)
    args = parser.parse_args()
    if args.output.exists():
        parser.error("Audit output already exists")
    if digest(args.manifest) != args.expected_manifest_sha256.lower():
        raise ValueError("Score-blind candidate manifest changed")
    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    if digest(args.images) != manifest["source_sha256"]["images"] or digest(args.model) != MODEL_SHA256:
        raise ValueError("Source/model hash differs")
    if manifest["seed"] != "T-022-controlled-two-face-v1":
        raise ValueError("Unexpected construction seed")
    with zipfile.ZipFile(args.model) as model_zip:
        model_root, onnx_hashes = prepare_pack(model_zip, args.output.parent / "cache")
    app = FaceAnalysis(name="buffalo_sc", root=str(model_root), allowed_modules=["detection"],
                       providers=["CPUExecutionProvider"])
    app.prepare(ctx_id=-1, det_size=(640, 640), det_thresh=0.5)
    if set(app.models) != {"detection"}:
        raise ValueError("Recognition module was unexpectedly loaded")
    all_members = {name for group in manifest["pairs"].values() for row in group
                   for name in (row["left"], row["right"])}
    all_members.update(name for row in manifest["scenes"] for name in
                       [row["reference_member"], *row["panel_members"]])
    sources = {}
    with zipfile.ZipFile(args.images) as image_zip:
        for index, member in enumerate(sorted(all_members), 1):
            sources[member] = source_status(app, image_zip, member)
            if index % 500 == 0:
                print(f"Detection-only source audit: {index}/{len(all_members)}", flush=True)
    pairs = {}
    for group, rows in manifest["pairs"].items():
        pairs[group] = [{"pair_index": row["index"], "genuine": row["genuine"],
                         "status": "USABLE" if all(sources[name] == "ONE_DETECTION"
                                                   for name in (row["left"], row["right"])) else "SOURCE_DETECTION_EXCLUDED"}
                        for row in rows]
    scenes = []
    for index, row in enumerate(manifest["scenes"], 1):
        relevant = [row["reference_member"], *row["panel_members"]]
        if not all(sources[name] == "ONE_DETECTION" for name in relevant):
            status, boxes = "SOURCE_DETECTION_EXCLUDED", []
        else:
            path = args.manifest.parent / row["scene_file"]
            if digest(path) != row["scene_sha256"]:
                raise ValueError(f"Scene bytes changed: {row['trial']}")
            status, boxes = scene_status(app, path)
        scenes.append({"trial": row["trial"], "group": row["group"], "kind": row["kind"],
                       "status": status, "boxes": boxes})
        if index % 80 == 0:
            print(f"Detection-only scene audit: {index}/{len(manifest['scenes'])}", flush=True)
    result = {"scope": "T-022 detection-only eligibility audit; NOT locked identity GT or recognition evaluation",
              "manifest_sha256": digest(args.manifest), "model_sha256": MODEL_SHA256,
              "detector_onnx_sha256": onnx_hashes["det_500m.onnx"],
              "source_status": sources, "pairs": pairs, "scenes": scenes}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes((json.dumps(result, ensure_ascii=False, sort_keys=True,
                                        separators=(",", ":")) + "\n").encode("utf-8"))
    summary = {"source_images": len(sources), "source_outcomes": dict(Counter(sources.values())),
               "groups": {}}
    for group in ("development", "evaluation"):
        summary["groups"][group] = {
            "pairs": {"genuine_usable": sum(row["genuine"] and row["status"] == "USABLE" for row in pairs[group]),
                      "ordinary_impostor_usable": sum(not row["genuine"] and row["status"] == "USABLE" for row in pairs[group]),
                      "source_detection_excluded": sum(row["status"] != "USABLE" for row in pairs[group])},
            "scenes": {kind: dict(Counter(row["status"] for row in scenes if row["group"] == group and row["kind"] == kind))
                       for kind in ("present", "absent")}}
    print(json.dumps({"audit_sha256": digest(args.output), **summary,
                      "visual_identity_review": "PENDING", "recognition_scores_read": False}, indent=2))


if __name__ == "__main__":
    main()
