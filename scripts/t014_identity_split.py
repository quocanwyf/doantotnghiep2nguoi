"""Create a deterministic identity-disjoint XQLFW split for T-014.

Writes filenames and identities only to a private output outside Git. The
printed summary contains counts and a manifest hash, never face identifiers.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path

from t011_xqlfw_baseline import EXPECTED, checked_zip, digest, load_pairs


SEED = "T-014-identity-v1"
SCENE_SEED = "T-014-scenes-v1"


def order(seed: str, value: str) -> tuple[str, str]:
    return hashlib.sha256((seed + "\0" + value).encode("utf-8")).hexdigest(), value


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--images", required=True, type=Path)
    parser.add_argument("--pairs", required=True, type=Path)
    parser.add_argument("--pilot-manifest", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    if args.output.exists():
        parser.error("private output already exists")

    hashes = {"images": digest(args.images), "pairs": digest(args.pairs)}
    if hashes != {key: EXPECTED[key] for key in hashes}:
        raise ValueError("Input differs from pinned B0 XQLFW")
    pilot = json.loads(args.pilot_manifest.read_text(encoding="utf-8"))
    if any(pilot["source_sha256"][key] != hashes[key] for key in hashes):
        raise ValueError("Pilot does not use the same XQLFW source")

    with checked_zip(args.images) as archive:
        lookup = {}
        for member in archive.namelist():
            if member.lower().endswith(".jpg"):
                parts = member.split("/")
                key = (parts[-2], parts[-1])
                if key in lookup:
                    raise ValueError("Duplicate source image key")
                lookup[key] = member
        pairs = load_pairs(args.pairs, lookup)
        requested = sorted({member for left, right, _, _ in pairs for member in (left, right)})
    if len(pairs) != 6000 or len(requested) != 7263:
        raise ValueError("Pair/image count differs from B0")

    identity_of = lambda member: member.split("/")[-2]
    pilot_ids = {identity_of(row["scene_zip_member"]) for row in pilot["selected"]}
    if len(pilot_ids) != 24:
        raise ValueError("Expected 24 distinct pilot identities")
    image_counts = Counter(identity_of(member) for member in requested)
    identities = sorted(set(image_counts) - pilot_ids, key=lambda value: order(SEED, value))
    cut = len(identities) * 7 // 10
    split_ids = {"development": identities[:cut], "evaluation": identities[cut:]}
    if not split_ids["development"] or not split_ids["evaluation"]:
        raise ValueError("Empty identity split")

    genuine_neighbors = defaultdict(set)
    for left, right, same, _ in pairs:
        if same and left != right:
            genuine_neighbors[left].add(right)
            genuine_neighbors[right].add(left)
    private = {
        "scope": "T-014 identity split; target/source identities only; background people unknown",
        "seed": SEED,
        "scene_seed": SCENE_SEED,
        "source_sha256": hashes,
        "pilot_excluded_identities": sorted(pilot_ids),
        "splits": {},
    }
    summary = {
        "seed": SEED,
        "source_sha256": hashes,
        "pilot_excluded_identities": len(pilot_ids),
        "pilot_excluded_images": sum(image_counts[value] for value in pilot_ids),
        "splits": {},
    }
    for split_name, ids in split_ids.items():
        id_set = set(ids)
        scene_order = sorted(
            (member for member in requested if identity_of(member) in id_set and member in genuine_neighbors),
            key=lambda value: order(SCENE_SEED, value),
        )
        private["splits"][split_name] = {"identities": ids, "scene_order": scene_order}
        summary["splits"][split_name] = {
            "identities": len(ids),
            "images": sum(image_counts[value] for value in ids),
            "eligible_target_identities": len({identity_of(member) for member in scene_order}),
            "eligible_scene_images_before_detection": len(scene_order),
        }

    encoded = (json.dumps(private, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")
    args.output.write_bytes(encoded)
    summary["private_manifest_sha256"] = hashlib.sha256(encoded).hexdigest()
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
