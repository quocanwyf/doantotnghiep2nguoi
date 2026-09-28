"""Create private contact sheets for visual T-015 label review (no model scores)."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import cv2
import numpy as np


def panel(path: Path, title: str, boxes: list[list[float]] | None = None) -> np.ndarray:
    image = cv2.imread(str(path))
    if image is None:
        raise ValueError(f"Cannot decode {path}")
    image = cv2.resize(image, (500, 500), interpolation=cv2.INTER_NEAREST)
    if boxes:
        sx, sy = 500 / cv2.imread(str(path)).shape[1], 500 / cv2.imread(str(path)).shape[0]
        for index, box in enumerate(boxes):
            x1, y1, x2, y2 = box
            x1, x2 = round(x1 * sx), round(x2 * sx)
            y1, y2 = round(y1 * sy), round(y2 * sy)
            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 255), 2)
            cv2.putText(image, str(index), (x1 + 2, max(y1 + 25, 25)), cv2.FONT_HERSHEY_SIMPLEX, 0.85, (0, 255, 255), 2)
    canvas = np.full((540, 500, 3), 255, dtype=np.uint8)
    canvas[:500] = image
    cv2.putText(canvas, title, (8, 528), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
    return canvas


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--manifest", type=Path, required=True)
    p.add_argument("--output-dir", type=Path, required=True)
    a = p.parse_args()
    if a.output_dir.exists() and any(a.output_dir.iterdir()):
        p.error("Output directory must be new or empty")
    a.output_dir.mkdir(parents=True)
    rows = json.loads(a.manifest.read_text(encoding="utf-8"))["selected"]
    for offset in range(0, len(rows), 4):
        blocks = []
        for row in rows[offset : offset + 4]:
            files = row["files"]
            sample = row["sample"]
            blocks.append(np.hstack([
                panel(a.manifest.parent / files["scene"], sample + " scene", row["detected_boxes_xyxy"]),
                panel(a.manifest.parent / files["present_ref"], sample + " present ref"),
                panel(a.manifest.parent / files["absent_ref"], sample + " absent ref"),
            ]))
        name = f"{rows[offset]['sample']}-through-{rows[min(offset + 3, len(rows)-1)]['sample']}.png"
        cv2.imwrite(str(a.output_dir / name), np.vstack(blocks))
    print(f"Wrote {(len(rows) + 3) // 4} private review sheets")


if __name__ == "__main__":
    main()
