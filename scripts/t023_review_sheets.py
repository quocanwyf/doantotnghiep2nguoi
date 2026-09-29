"""Generate private, score-blind scene contact sheets for T-023 self-review."""

from __future__ import annotations

import argparse
import json
import math
import zipfile
from pathlib import Path, PurePosixPath

import cv2
import numpy as np

from t023_build_bfw import get_image
from t023_detector_audit import CANDIDATE_SHA256
from t023_build_bfw import digest


def tile(image: np.ndarray) -> np.ndarray:
    canvas = np.full((150, 150, 3), 127, dtype=np.uint8)
    h, w = image.shape[:2]
    scale = min(140 / h, 140 / w)
    resized = cv2.resize(image, (round(w * scale), round(h * scale)),
                         interpolation=cv2.INTER_AREA if scale < 1 else cv2.INTER_LINEAR)
    y, x = (150 - resized.shape[0]) // 2, (150 - resized.shape[1]) // 2
    canvas[y:y + resized.shape[0], x:x + resized.shape[1]] = resized
    return canvas


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("manifest", "images", "output-dir"):
        parser.add_argument("--" + name, type=Path, required=True)
    args = parser.parse_args()
    if digest(args.manifest) != CANDIDATE_SHA256:
        raise ValueError("Candidate manifest differs")
    if args.output_dir.exists() and any(args.output_dir.iterdir()):
        parser.error("Review folder must be new/empty")
    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    args.output_dir.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(args.images) as archive:
        lookup = {"/".join(PurePosixPath(name).parts[-3:]): name for name in archive.namelist()
                  if name.lower().endswith(".jpg")}
        for group in ("development", "evaluation"):
            rows = [row for row in manifest["scenes"] if row["group"] == group]
            for page in range(math.ceil(len(rows) / 24)):
                sheet = np.full((6 * 185, 4 * 460, 3), 235, dtype=np.uint8)
                for offset, row in enumerate(rows[page * 24:(page + 1) * 24]):
                    y, x = divmod(offset, 4)
                    top, left = y * 185, x * 460
                    label = f"{row['trial']} {row['kind']} {row['stratum']}"
                    cv2.putText(sheet, label, (left + 2, top + 18), cv2.FONT_HERSHEY_SIMPLEX,
                                0.42, (0, 0, 0), 1, cv2.LINE_AA)
                    names = [row["reference_member"], *row["panel_members"]]
                    for column, member in enumerate(names):
                        face = tile(get_image(archive, lookup, member))
                        sheet[top + 25:top + 175, left + 2 + column * 151:left + 152 + column * 151] = face
                    for column, caption in enumerate(("REF", "LEFT", "RIGHT")):
                        cv2.putText(sheet, caption, (left + 3 + column * 151, top + 174),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.36, (0, 255, 0), 1, cv2.LINE_AA)
                output = args.output_dir / f"{group}-{page + 1:02d}.png"
                if not cv2.imwrite(str(output), sheet):
                    raise OSError("Unable to write contact sheet")
    print(json.dumps({"candidate_sha256": CANDIDATE_SHA256,
                      "sheets_per_group": math.ceil(300 / 24),
                      "status": "PENDING_VISUAL_REVIEW; no recognition score"}))


if __name__ == "__main__":
    main()
