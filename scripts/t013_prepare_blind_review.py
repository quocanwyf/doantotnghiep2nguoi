#!/usr/bin/env python3
"""Create a blind, local-only review packet from the T-013 private pilot manifest."""

import argparse
import csv
import json
import random
import shutil
from pathlib import Path


FIELDS = [
    "case_id",
    "reference",
    "scene_people",
    "reference_usable",
    "relation",
    "target_x_normalized",
    "target_y_normalized",
    "reason",
    "reviewer",
    "review_date",
]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--packet-dir", type=Path, required=True)
    parser.add_argument("--key-file", type=Path, required=True)
    args = parser.parse_args()

    source = args.manifest.resolve()
    packet = args.packet_dir.resolve()
    key_file = args.key_file.resolve()
    if packet == source.parent or source.is_relative_to(packet):
        parser.error("packet-dir must not contain the source manifest")
    if key_file.is_relative_to(packet):
        parser.error("key-file must be outside packet-dir")
    if packet.exists() and any(packet.iterdir()):
        parser.error("packet-dir must be empty")
    if key_file.exists():
        parser.error("key-file already exists")

    rows = json.loads(source.read_text(encoding="utf-8"))["selected"]
    if len(rows) != 24 or len({row["sample"] for row in rows}) != 24:
        parser.error("expected 24 distinct pilot samples")

    rng = random.Random("T-013-blind-review-v1")
    rng.shuffle(rows)
    packet.mkdir(parents=True, exist_ok=True)
    key_file.parent.mkdir(parents=True, exist_ok=True)
    answer_key = []
    blank_rows = []

    for index, row in enumerate(rows, 1):
        case_id = f"case-{index:02d}"
        scene_source = source.parent / row["files"]["scene"]
        shutil.copyfile(scene_source, packet / f"{case_id}-scene.jpg")
        ref_roles = ["present_ref", "absent_ref"]
        rng.shuffle(ref_roles)
        mapping = {"case_id": case_id, "sample": row["sample"], "references": {}}
        for label, role in zip(("A", "B"), ref_roles):
            ref_source = source.parent / row["files"][role]
            shutil.copyfile(ref_source, packet / f"{case_id}-ref-{label}.jpg")
            mapping["references"][label] = role
            blank_rows.append({"case_id": case_id, "reference": label})
        answer_key.append(mapping)

    with (packet / "review-blank.csv").open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(blank_rows)
    key_file.write_text(
        json.dumps({"seed": "T-013-blind-review-v1", "cases": answer_key}, indent=2),
        encoding="utf-8",
    )
    print(f"Prepared {len(rows)} blind cases and {len(blank_rows)} review rows.")
    print("Keep the key separate from the reviewer packet; do not commit either.")


if __name__ == "__main__":
    main()
