"""Audit BFW T-023 candidate with SCRFD detection only, before recognition.

The private output retains source paths and box coordinates. Identity labels
remain those of BFW, never inferred from a detection or encoder score.
"""

from __future__ import annotations

import argparse
import json
import zipfile
from collections import Counter
from pathlib import Path

import cv2
import numpy as np
from insightface.app import FaceAnalysis

from t011_xqlfw_baseline import prepare_pack
from t023_build_bfw import INNER_MD5, digest, get_image, letterbox


CANDIDATE_SHA256 = "3ac495fefaf440687f379965f44fac772b585dd5e66b09fcde25d0115af1a492"
MODEL_SHA256 = "57d31b56b6ffa911c8a73cfc1707c73cab76efe7f13b675a05223bf42de47c72"
DETECTOR_SHA256 = "5e4447f50245bbd7966bd6c0fa52938c61474a04ec7def48753668a9d8b4ea3a"


def source_status(app: FaceAnalysis, image: np.ndarray) -> str:
    count = len(app.get(letterbox(image)))
    return "ONE_DETECTION" if count == 1 else ("ZERO_DETECTION" if count == 0 else "MULTIPLE_DETECTIONS")


def scene_status(app: FaceAnalysis, encoded: bytes) -> tuple[str, list[dict]]:
    scene = cv2.imdecode(np.frombuffer(encoded, dtype=np.uint8), cv2.IMREAD_COLOR)
    if scene is None or scene.shape != (250, 516, 3):
        raise ValueError("Controlled scene shape/decode differs")
    boxes = []
    for face in app.get(scene):
        box = [float(value) for value in face.bbox]
        center = (box[0] + box[2]) / 2
        panel = 0 if center < 250 else (1 if center >= 266 else None)
        boxes.append({"xyxy": box, "panel": panel})
    if len(boxes) != 2:
        return "NOT_TWO_DETECTIONS", boxes
    if sorted(item["panel"] for item in boxes if item["panel"] is not None) != [0, 1]:
        return "BOX_PANEL_AMBIGUOUS", boxes
    return "TWO_PANELS_MAPPED", boxes


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("manifest", "images", "model", "output"):
        parser.add_argument("--" + name, type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        parser.error("Refusing to overwrite detector audit")
    if digest(args.manifest) != CANDIDATE_SHA256 or digest(args.images, "md5") != INNER_MD5:
        raise ValueError("Candidate/inner images differ from score-blind construction")
    if digest(args.model) != MODEL_SHA256:
        raise ValueError("Frozen model pack differs")
    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    if manifest["recognition_scores_read"] is not False:
        raise ValueError("Candidate was not score-blind")
    with zipfile.ZipFile(args.model) as pack:
        root, onnx_hashes = prepare_pack(pack, args.output.parent / "cache")
    if onnx_hashes["det_500m.onnx"] != DETECTOR_SHA256:
        raise ValueError("SCRFD weights differ")
    app = FaceAnalysis(name="buffalo_sc", root=str(root), allowed_modules=["detection"],
                       providers=["CPUExecutionProvider"])
    app.prepare(ctx_id=-1, det_size=(640, 640), det_thresh=0.5)
    if set(app.models) != {"detection"}:
        raise ValueError("Recognition module unexpectedly loaded")
    all_members = {name for row in manifest["pairs"] for name in (row["left"], row["right"])}
    all_members.update(name for row in manifest["scenes"] for name in
                       [row["reference_member"], *row["panel_members"]])
    source = {}
    with zipfile.ZipFile(args.images) as images:
        lookup = {"/".join(Path(name).parts[-3:]): name for name in images.namelist()
                  if name.lower().endswith(".jpg")}
        if not all_members <= set(lookup):
            raise ValueError("Source image missing in author archive")
        for number, member in enumerate(sorted(all_members), 1):
            source[member] = source_status(app, get_image(images, lookup, member))
            if number % 500 == 0:
                print(f"T-023 detection-only source audit {number}/{len(all_members)}", flush=True)
    pairs = [{"pair": row["pair"], "group": row["group"], "genuine": row["genuine"],
              "status": "USABLE" if source[row["left"]] == source[row["right"]] == "ONE_DETECTION"
              else "EXCLUDED_DETECTOR"} for row in manifest["pairs"]]
    scenes = []
    for number, row in enumerate(manifest["scenes"], 1):
        related = [row["reference_member"], *row["panel_members"]]
        if any(source[name] != "ONE_DETECTION" for name in related):
            status, boxes = "SOURCE_DETECTION_EXCLUDED", []
        else:
            path = args.manifest.parent / row["scene_file"]
            if digest(path) != row["scene_sha256"]:
                raise ValueError("Candidate scene bytes changed")
            status, boxes = scene_status(app, path.read_bytes())
        scenes.append({"trial": row["trial"], "group": row["group"], "kind": row["kind"],
                       "stratum": row["stratum"], "status": status, "boxes": boxes})
        if number % 100 == 0:
            print(f"T-023 detection-only scene audit {number}/{len(manifest['scenes'])}", flush=True)
    result = {"scope": "T-023 detector-only audit; not identity GT lock or recognition score",
              "manifest_sha256": CANDIDATE_SHA256, "detector_onnx_sha256": DETECTOR_SHA256,
              "model_pack_sha256": MODEL_SHA256, "source_status": source,
              "pairs": pairs, "scenes": scenes}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes((json.dumps(result, sort_keys=True, ensure_ascii=False,
                                        separators=(",", ":")) + "\n").encode("utf-8"))
    print(json.dumps({"audit_sha256": digest(args.output), "source_images": len(source),
                      "source": dict(Counter(source.values())),
                      "pairs": {group: {f"{kind}/{status}": count for (kind, status), count in
                                        Counter((r["genuine"], r["status"]) for r in pairs
                                                if r["group"] == group).items()}
                                for group in ("development", "evaluation")},
                      "scenes": {group: {"/".join(key): count for key, count in
                                         Counter((r["kind"], r["stratum"], r["status"])
                                                 for r in scenes if r["group"] == group).items()}
                                 for group in ("development", "evaluation")},
                      "recognition_scores_read": False}, default=str, indent=2))


if __name__ == "__main__":
    main()
