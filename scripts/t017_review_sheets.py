"""Render private T-017 review sheets from original images, without boxes/scores."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import cv2
import numpy as np


def panel(path: Path, title: str) -> np.ndarray:
    original = cv2.imread(str(path))
    if original is None:
        raise ValueError(f"Cannot read {path}")
    resized = cv2.resize(original, (500, 500), interpolation=cv2.INTER_NEAREST)
    canvas = np.full((540, 500, 3), 255, dtype=np.uint8)
    canvas[:500] = resized
    cv2.putText(canvas, title, (8, 528), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
    return canvas


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--manifest", type=Path, required=True)
    p.add_argument("--output-dir", type=Path, required=True)
    args = p.parse_args()
    if args.output_dir.exists() and any(args.output_dir.iterdir()):
        p.error("Review directory must be new or empty")
    args.output_dir.mkdir(parents=True)
    rows = json.loads(args.manifest.read_text(encoding="utf-8"))["selected"]
    for offset in range(0, len(rows), 4):
        triplets = []
        for row in rows[offset:offset + 4]:
            files = row["files"]
            triplets.append(np.hstack([
                panel(args.manifest.parent / files["scene"], row["sample"] + " scene"),
                panel(args.manifest.parent / files["present_ref"], "present ref"),
                panel(args.manifest.parent / files["absent_ref"], "absent ref"),
            ]))
        output = args.output_dir / f"holdout-{offset + 1:03d}-through-{min(offset + 4, len(rows)):03d}.png"
        if not cv2.imwrite(str(output), np.vstack(triplets)):
            raise OSError(f"Cannot write {output}")
    print(f"Rendered {(len(rows) + 3) // 4} private no-box sheets")


if __name__ == "__main__":
    main()
