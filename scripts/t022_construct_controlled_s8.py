"""Build a score-blind controlled two-face XQLFW S8 benchmark candidate.

Private outputs contain face images and source identities. They must stay outside Git.
This script neither loads a model nor reads cosine/P2 output. A separate visual and
detector-only audit must lock usable labels before any recognition score is opened.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import zipfile
from collections import defaultdict
from pathlib import Path

import cv2
import numpy as np


SEED = "T-022-controlled-two-face-v1"
PINNED = {
    "images": "1af459679fba23a12f4d83c82a81523eb930a4aec759eebefcbdde69a678962c",
    "pairs": "636852f90b886f3f56c73b13c9775f7ffcd37662dbb189c694f6a0a605b63b84",
    "split": "23542240bcc7b5d852ed469a35180dd7e68ae18942390bba25dc9106946692e2",
    "t015_scene": "ae80423e479d616052a2bf2cc5a24d2dd45519bb12957525e33f8ab45b769c74",
    "t017_scene": "5ca44481ce26abe62e2e699bdaae44c7b9227f2a5c54f6ac9d865330ad658290",
}


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def identity(member: str) -> str:
    return member.replace("\\", "/").split("/")[-2]


def ordered(tag: str, value: str) -> tuple[str, str]:
    return hashlib.sha256((SEED + "\0" + tag + "\0" + value).encode()).hexdigest(), value


def encoded_json(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def load_pairs(path: Path, lookup: dict[tuple[str, str], str]) -> list[dict]:
    lines = path.read_text(encoding="utf-8").splitlines()
    if lines[0].split() != ["10", "300"] or len(lines) != 6001:
        raise ValueError("Unexpected XQLFW pair protocol")
    result = []
    for index, line in enumerate(lines[1:]):
        fields = line.split()
        if len(fields) == 3:
            names = ((fields[0], fields[1]), (fields[0], fields[2]))
            same = True
        elif len(fields) == 4:
            names = ((fields[0], fields[1]), (fields[2], fields[3]))
            same = False
        else:
            raise ValueError(f"Malformed pair {index}")
        members = []
        for person, number in names:
            key = person, f"{person}_{int(number):04d}.jpg"
            if key not in lookup:
                raise ValueError(f"Missing image in pair {index}")
            members.append(lookup[key])
        if (identity(members[0]) == identity(members[1])) != same:
            raise ValueError(f"Source identity disagrees with pair label {index}")
        result.append({"index": index, "left": members[0], "right": members[1], "genuine": same})
    return result


def decode(archive: zipfile.ZipFile, member: str) -> np.ndarray:
    image = cv2.imdecode(np.frombuffer(archive.read(member), dtype=np.uint8), cv2.IMREAD_COLOR)
    if image is None or image.shape != (250, 250, 3):
        raise ValueError(f"Source image decode/shape differs: {member}")
    return image


def composite(left: np.ndarray, right: np.ndarray) -> np.ndarray:
    canvas = np.full((250, 516, 3), 127, dtype=np.uint8)
    canvas[:, :250] = left
    canvas[:, 266:] = right
    return canvas


def build_group(group: str, ids: set[str], pairs: list[dict], requested: int,
                archive: zipfile.ZipFile, output_dir: Path) -> tuple[list[dict], list[dict], dict]:
    eligible = [row for row in pairs if identity(row["left"]) in ids and identity(row["right"]) in ids]
    genuine = defaultdict(list)
    negative = defaultdict(list)
    members = set()
    for row in eligible:
        members.update((row["left"], row["right"]))
        if row["genuine"]:
            genuine[identity(row["left"])].append(row)
        else:
            negative[identity(row["left"])].append((row, row["right"]))
            negative[identity(row["right"])].append((row, row["left"]))
    anchors = sorted(set(genuine) & set(negative), key=lambda x: ordered(group + ":anchor", x))
    if len(anchors) < requested:
        raise ValueError(f"Only {len(anchors)} anchors in {group}, requested {requested}")
    all_members = sorted(members)
    scenes = []
    chosen = anchors[:requested]
    for number, anchor in enumerate(chosen, 1):
        pos = min(genuine[anchor], key=lambda x: ordered(group + ":genuine", str(x["index"])))
        a_ref, a_scene = pos["left"], pos["right"]
        if ordered(group + ":orientation", anchor)[0][-1] in "01234567":
            a_ref, a_scene = a_scene, a_ref
        neg, b = min(negative[anchor], key=lambda x: ordered(group + ":negative", str(x[0]["index"])))
        c = min((m for m in all_members if identity(m) not in {anchor, identity(b)}),
                key=lambda m: ordered(group + ":other", anchor + "\0" + m))
        name = f"{group}-{number:03d}"
        for kind, faces in (("present", (a_scene, b)), ("absent", (b, c))):
            if ordered(group + ":side", name + kind)[0][-1] in "01234567":
                faces = faces[::-1]
            image = composite(decode(archive, faces[0]), decode(archive, faces[1]))
            filename = f"{name}-{kind}.png"
            path = output_dir / filename
            if not cv2.imwrite(str(path), image):
                raise OSError(f"Unable to write {path}")
            scenes.append({"trial": f"{name}-{kind}", "group": group, "kind": kind,
                           "reference_member": a_ref, "reference_identity": anchor,
                           "panel_members": list(faces), "panel_identities": [identity(x) for x in faces],
                           "target_panel": list(faces).index(a_scene) if kind == "present" else None,
                           "scene_file": filename, "scene_sha256": digest(path),
                           "genuine_pair_index": pos["index"], "negative_pair_index": neg["index"],
                           "source_label": "XQLFW folder identity + official pair protocol",
                           "visual_review": "PENDING", "box_audit": "PENDING"})
    return scenes, eligible, {"candidate_anchors": len(anchors), "selected_anchors": len(chosen),
                              "potential_genuine_pairs": sum(x["genuine"] for x in eligible),
                              "potential_impostor_pairs": sum(not x["genuine"] for x in eligible)}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("images", "pairs", "split", "t015-scene", "t017-scene", "output-dir"):
        parser.add_argument("--" + name, required=True, type=Path)
    parser.add_argument("--development-anchors", type=int, default=96)
    parser.add_argument("--evaluation-anchors", type=int, default=64)
    args = parser.parse_args()
    if args.development_anchors < 1 or args.evaluation_anchors < 1:
        parser.error("Anchor counts must be positive")
    if args.output_dir.exists() and any(args.output_dir.iterdir()):
        parser.error("Output directory must be new or empty")
    paths = {"images": args.images, "pairs": args.pairs, "split": args.split,
             "t015_scene": args.t015_scene, "t017_scene": args.t017_scene}
    if {key: digest(value) for key, value in paths.items()} != PINNED:
        raise ValueError("Pinned source/split/previous scene hash differs")
    split = json.loads(args.split.read_text(encoding="utf-8"))
    prior = [json.loads(path.read_text(encoding="utf-8")) for path in (args.t015_scene, args.t017_scene)]
    used_ids = {identity(value) for manifest in prior for row in manifest["selected"]
                for key, value in row.items() if key.endswith("_zip_member")}
    dev_ids = set(split["splits"]["development"]["identities"]) - used_ids
    eval_ids = set(split["splits"]["evaluation"]["identities"]) - used_ids
    if dev_ids & eval_ids or (dev_ids | eval_ids) & set(split["pilot_excluded_identities"]):
        raise ValueError("Known identity leakage across split/pilot")
    args.output_dir.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(args.images) as archive:
        lookup = {}
        for member in archive.namelist():
            if not member.lower().endswith(".jpg"):
                continue
            path = Path(member.replace("\\", "/"))
            if path.is_absolute() or ".." in path.parts:
                raise ValueError("Unsafe source member")
            key = identity(member), path.name
            if key in lookup:
                raise ValueError("Duplicate source image key")
            lookup[key] = member
        pairs = load_pairs(args.pairs, lookup)
        all_scenes, pair_rows, summary = [], {}, {}
        for group, ids, requested in (("development", dev_ids, args.development_anchors),
                                      ("evaluation", eval_ids, args.evaluation_anchors)):
            scenes, eligible, counts = build_group(group, ids, pairs, requested, archive, args.output_dir)
            all_scenes.extend(scenes)
            pair_rows[group] = eligible
            summary[group] = {"remaining_source_identities": len(ids), **counts,
                              "planned_present": requested, "planned_absent": requested}
    manifest = {"scope": "score-blind synthetic/controlled two-face candidate; NOT locked ground truth",
                "seed": SEED, "source_sha256": PINNED, "layout": "250x250 JPEG tiles, unscaled, 16px gray gutter, lossless PNG",
                "identity_disjoint_known_source": True, "excluded_prior_source_identity_count": len(used_ids),
                "scenes": all_scenes, "pairs": pair_rows}
    manifest_path = args.output_dir / "candidate-manifest.json"
    manifest_path.write_bytes(encoded_json(manifest))
    print(json.dumps({"manifest_sha256": digest(manifest_path), "scene_count": len(all_scenes),
                      "group_counts": summary, "visual_review": "PENDING", "recognition_scores_read": False}, indent=2))


if __name__ == "__main__":
    main()
