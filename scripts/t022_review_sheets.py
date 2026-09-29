"""Create private contact sheets for score-blind T-022 visual identity review."""

from __future__ import annotations

import argparse
import hashlib
import json
import zipfile
from collections import defaultdict
from pathlib import Path

import cv2
import numpy as np


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def decode(encoded: bytes) -> np.ndarray:
    image = cv2.imdecode(np.frombuffer(encoded, dtype=np.uint8), cv2.IMREAD_COLOR)
    if image is None:
        raise ValueError("Image decode failed")
    return image


def mark_scene(image: np.ndarray, row: dict, labels: list[str]) -> np.ndarray:
    marked = image.copy()
    for item in row["boxes"]:
        panel = item["panel"]
        color = (0, 170, 0) if panel is not None and labels[panel] == "TARGET" else (0, 0, 220)
        x1, y1, x2, y2 = (int(round(value)) for value in item["xyxy"])
        cv2.rectangle(marked, (x1, y1), (x2, y2), color, 2)
    return marked


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    for name in ("images", "manifest", "detector-audit", "output-dir"):
        p.add_argument("--" + name, required=True, type=Path)
    p.add_argument("--manifest-sha256", required=True)
    p.add_argument("--detector-audit-sha256", required=True)
    args = p.parse_args()
    if args.output_dir.exists() and any(args.output_dir.iterdir()):
        p.error("Output directory must be new or empty")
    if digest(args.manifest) != args.manifest_sha256.lower() or digest(args.detector_audit) != args.detector_audit_sha256.lower():
        raise ValueError("Frozen candidate/audit hash mismatch")
    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    audit = json.loads(args.detector_audit.read_text(encoding="utf-8"))
    if audit["manifest_sha256"] != digest(args.manifest):
        raise ValueError("Audit references another manifest")
    trials = {row["trial"]: row for row in manifest["scenes"]}
    checks = {row["trial"]: row for row in audit["scenes"]}
    anchors = defaultdict(dict)
    for trial, row in trials.items():
        anchors[trial.rsplit("-", 1)[0]][row["kind"]] = row
    if any(set(rows) != {"present", "absent"} for rows in anchors.values()):
        raise ValueError("Every anchor needs both scene kinds")
    args.output_dir.mkdir(parents=True)
    saved = []
    with zipfile.ZipFile(args.images) as archive:
        for group in ("development", "evaluation"):
            names = sorted(name for name in anchors if name.startswith(group + "-"))
            for offset in range(0, len(names), 8):
                sheet = np.full((8 * 295, 1340, 3), 245, dtype=np.uint8)
                for local_index, name in enumerate(names[offset:offset + 8]):
                    base = local_index * 295
                    present, absent = anchors[name]["present"], anchors[name]["absent"]
                    ref = decode(archive.read(present["reference_member"]))
                    if ref.shape != (250, 250, 3):
                        raise ValueError("Reference size differs")
                    left = decode((args.manifest.parent / present["scene_file"]).read_bytes())
                    right = decode((args.manifest.parent / absent["scene_file"]).read_bytes())
                    pcheck, acheck = checks[present["trial"]], checks[absent["trial"]]
                    plabels = ["TARGET" if index == present["target_panel"] else "OTHER" for index in (0, 1)]
                    left = mark_scene(left, pcheck, plabels)
                    right = mark_scene(right, acheck, ["OTHER", "OTHER"])
                    cv2.putText(sheet, f"{name}  P:{pcheck['status']}  A:{acheck['status']}",
                                (8, base + 17), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (25, 25, 25), 1)
                    for label, x in (("REF", 8), ("PRESENT", 266), ("ABSENT", 790)):
                        cv2.putText(sheet, label, (x, base + 34), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (25, 25, 25), 1)
                    sheet[base + 40:base + 290, 8:258] = ref
                    sheet[base + 40:base + 290, 266:782] = left
                    sheet[base + 40:base + 290, 790:1306] = right
                filename = f"{group}-{offset // 8 + 1:02d}.png"
                path = args.output_dir / filename
                if not cv2.imwrite(str(path), sheet):
                    raise OSError(f"Unable to write {path}")
                saved.append({"file": filename, "sha256": digest(path), "anchors": names[offset:offset + 8]})
    index = args.output_dir / "index.json"
    index.write_text(json.dumps({"scope": "private score-blind identity/box visual audit; no cosine",
                                 "manifest_sha256": digest(args.manifest),
                                 "detector_audit_sha256": digest(args.detector_audit),
                                 "sheets": saved}, sort_keys=True, separators=(",", ":")) + "\n", encoding="utf-8")
    print(json.dumps({"sheet_count": len(saved), "anchors": len(anchors), "index_sha256": digest(index)}, indent=2))


if __name__ == "__main__":
    main()
