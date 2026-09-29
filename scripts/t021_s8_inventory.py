"""Count unused XQLFW source identities/pairs/scenes for T-021, without scores.

No face image, identity or per-sample record is written or printed.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from t011_xqlfw_baseline import EXPECTED, checked_zip, digest, load_pairs


PINNED = {
    "split": "23542240bcc7b5d852ed469a35180dd7e68ae18942390bba25dc9106946692e2",
    "t015_scene": "ae80423e479d616052a2bf2cc5a24d2dd45519bb12957525e33f8ab45b769c74",
    "t017_scene": "5ca44481ce26abe62e2e699bdaae44c7b9227f2a5c54f6ac9d865330ad658290",
}


def identity(member: str) -> str:
    return member.replace("\\", "/").split("/")[-2]


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    for name in ("images", "pairs", "model", "split", "t015-scene", "t017-scene"):
        p.add_argument("--" + name, type=Path, required=True)
    a = p.parse_args()
    if {key: digest(getattr(a, key)) for key in EXPECTED} != EXPECTED:
        raise ValueError("XQLFW/model sources differ from reviewed baseline")
    if {key: digest(getattr(a, key)) for key in PINNED} != PINNED:
        raise ValueError("A T-014/T-015/T-017 manifest changed")
    split = json.loads(a.split.read_text(encoding="utf-8"))
    manifests = [json.loads(path.read_text(encoding="utf-8")) for path in (a.t015_scene, a.t017_scene)]
    used_ids = {identity(value) for manifest in manifests for row in manifest["selected"]
                for key, value in row.items() if key.endswith("_zip_member")}
    with checked_zip(a.images) as archive:
        lookup = {(identity(name), name.split("/")[-1]): name for name in archive.namelist() if name.lower().endswith(".jpg")}
        pairs = load_pairs(a.pairs, lookup)
    result = {"scope": "metadata inventory only; not audited S8 dataset", "source_sha256": EXPECTED,
              "manifest_sha256": PINNED, "prior_used_identity_count": len(used_ids), "splits": {}}
    for group in ("development", "evaluation"):
        ids = set(split["splits"][group]["identities"]) - used_ids
        eligible = [(same, left, right) for left, right, same, _ in pairs
                    if identity(left) in ids and identity(right) in ids]
        scenes = [name for name in split["splits"][group]["scene_order"] if identity(name) in ids]
        result["splits"][group] = {"unused_source_identities": len(ids),
                                   "potential_pairs": len(eligible),
                                   "potential_genuine_pairs": sum(same for same, _, _ in eligible),
                                   "potential_impostor_pairs": sum(not same for same, _, _ in eligible),
                                   "scene_order_images": len(scenes)}
    print(json.dumps(result, ensure_ascii=True, indent=2))


if __name__ == "__main__":
    main()
