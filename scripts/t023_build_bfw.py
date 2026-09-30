"""Construct a T-023 score-blind BFW candidate manifest and controlled scenes.

This reads BFW source labels and author-supplied SENet50 scores only to sample
the declared challenge stratum. It never loads MobileFaceNet, P2 or T-022 raw
outputs. The manifest and images contain identities and must remain outside Git.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import math
import zipfile
from collections import Counter, defaultdict
from pathlib import Path, PurePosixPath

import cv2
import numpy as np


SEED = "T-023-BFW-scoreblind-v2"
OUTER_SHA256 = "5053c12a0d65424ae619ba7376746e6977c2fb23b2682741ecdff82ef52a6957"
INNER_MD5 = "c1c5869f31c6137b40f7755ce8e8f6db"
# Three image paths listed as incorrect identity/cartoon in the author's README.
EXCLUDED_PATH_SHA256 = {
    "075286f604cced55d78e6e49a86e232d2be0056972921faf3b1724e51ce",
    "7aa09c03f6d2f052a44b11a39afa191eec4a3a41165453de4a58ee1c50e2d86a",
    "9ce7bbb511d02d1f2fddb5a66b9e52f852b7ff21595cbb83e20a2103c78d2484",
}


def digest(path: Path, algorithm: str = "sha256") -> str:
    h = hashlib.new(algorithm)
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(8 * 1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def rank(tag: str, value: str) -> str:
    return hashlib.sha256((SEED + "\0" + tag + "\0" + value).encode()).hexdigest()


def identity(member: str) -> str:
    return "/".join(PurePosixPath(member).parts[-3:-1])


def canonical(member: str) -> str:
    return "/".join(PurePosixPath(member.replace("\\", "/")).parts[-3:])


def is_reported_bad(member: str) -> bool:
    return hashlib.sha256(canonical(member).encode()).hexdigest() in EXCLUDED_PATH_SHA256


def encoded(value: object) -> bytes:
    return (json.dumps(value, sort_keys=True, ensure_ascii=False,
                       separators=(",", ":"), allow_nan=False) + "\n").encode("utf-8")


def load_source(outer: zipfile.ZipFile, image_zip: zipfile.ZipFile):
    images = defaultdict(list)
    member_lookup = {}
    for member in image_zip.namelist():
        if not member.lower().endswith(".jpg"):
            continue
        path = PurePosixPath(member)
        if path.is_absolute() or ".." in path.parts:
            raise ValueError("Unsafe image member")
        key = canonical(member)
        if key in member_lookup:
            raise ValueError("Duplicate BFW image path")
        member_lookup[key] = member
        if not is_reported_bad(key):
            images[identity(key)].append(key)
    folds = defaultdict(set)
    source_rows = 0
    label_mismatch = 0
    missing = 0
    with outer.open("bfw-datatable.csv") as source:
        for row in csv.DictReader(io.TextIOWrapper(source, encoding="utf-8")):
            source_rows += 1
            a, b = canonical(row["p1"]), canonical(row["p2"])
            same = identity(a) == identity(b)
            label_mismatch += same != (row["label"] == "1")
            missing += a not in member_lookup or b not in member_lookup
            folds[int(row["fold"])].update((identity(a), identity(b)))
    if (source_rows, label_mismatch, missing, len(images)) != (923898, 0, 0, 800):
        raise ValueError("BFW source metadata differs from the pre-score audit")
    if any(len(folds[fold]) != 160 for fold in range(1, 6)):
        raise ValueError("BFW fold size differs")
    if any(folds[a] & folds[b] for a in folds for b in folds if a < b):
        raise ValueError("BFW fold identities overlap")
    return images, member_lookup, folds


def get_image(archive: zipfile.ZipFile, lookup: dict[str, str], member: str) -> np.ndarray:
    image = cv2.imdecode(np.frombuffer(archive.read(lookup[member]), dtype=np.uint8),
                         cv2.IMREAD_COLOR)
    if image is None:
        raise ValueError(f"Cannot decode BFW image: {member}")
    return image


def letterbox(image: np.ndarray) -> np.ndarray:
    height, width = image.shape[:2]
    if not height or not width:
        raise ValueError("Invalid image shape")
    # Detector-only pilot on unused fold-1 identities showed that a face filling
    # the whole panel is usually missed by frozen SCRFD. This 140px max side was
    # fixed before recognition scoring and is applied to all source/scene inputs.
    scale = min(140 / height, 140 / width)
    new_w, new_h = max(1, round(width * scale)), max(1, round(height * scale))
    resized = cv2.resize(image, (new_w, new_h), interpolation=cv2.INTER_AREA if scale < 1 else cv2.INTER_LINEAR)
    panel = np.full((250, 250, 3), 127, dtype=np.uint8)
    x, y = (250 - new_w) // 2, (250 - new_h) // 2
    panel[y:y + new_h, x:x + new_w] = resized
    return panel


def composite(left: np.ndarray, right: np.ndarray) -> np.ndarray:
    scene = np.full((250, 516, 3), 127, dtype=np.uint8)
    scene[:, :250] = left
    scene[:, 266:] = right
    return scene


def selected_anchors(images: dict, folds: dict) -> dict[int, list[str]]:
    result = {}
    for fold in range(1, 6):
        count = 20 if fold <= 3 else 30
        eligible = sorted((person for person in folds[fold] if len(images[person]) >= 6),
                          key=lambda person: rank(f"anchor:{fold}", person))
        if len(eligible) < count:
            raise ValueError("Insufficient source identities before model score")
        result[fold] = eligible[:count]
    return result


def challenge_candidates(outer: zipfile.ZipFile, references: dict[str, str]):
    by_ref = defaultdict(list)
    with outer.open("bfw-datatable.csv") as source:
        for row in csv.DictReader(io.TextIOWrapper(source, encoding="utf-8")):
            if row["label"] != "0":
                continue
            a, b = canonical(row["p1"]), canonical(row["p2"])
            for ref, other in ((a, b), (b, a)):
                if references.get(identity(ref)) != ref or is_reported_bad(other):
                    continue
                try:
                    independent_score = float(row["senet50"])
                except ValueError:
                    continue
                if math.isfinite(independent_score):
                    by_ref[ref].append((independent_score, other))
    return by_ref


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--release", type=Path, required=True)
    parser.add_argument("--images", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    if args.output_dir.exists() and any(args.output_dir.iterdir()):
        parser.error("Output directory must be new/empty; do not overwrite a benchmark")
    if digest(args.release) != OUTER_SHA256 or digest(args.images, "md5") != INNER_MD5:
        raise ValueError("BFW author release or inner image archive differs")
    with zipfile.ZipFile(args.release) as outer, zipfile.ZipFile(args.images) as image_zip:
        if outer.testzip() is not None or image_zip.testzip() is not None:
            raise ValueError("Corrupt BFW archive")
        images, lookup, folds = load_source(outer, image_zip)
        anchors = selected_anchors(images, folds)
        references = {person: sorted(images[person], key=lambda x: rank("reference", x))[0]
                      for people in anchors.values() for person in people}
        challenge = challenge_candidates(outer, references)
        args.output_dir.mkdir(parents=True, exist_ok=True)
        scenes, pairs = [], []
        for fold in range(1, 6):
            group = "development" if fold <= 3 else "evaluation"
            for ordinal, person in enumerate(anchors[fold], 1):
                anchor = f"f{fold}-{ordinal:03d}"
                ref = references[person]
                positives = sorted((x for x in images[person] if x != ref),
                                   key=lambda x: rank("genuine:" + anchor, x))[:4]
                others = sorted((x for x in folds[fold] if x != person),
                                key=lambda x: rank("other:" + anchor, x))
                ordinary_people = others[:4]
                used_people = {person, *ordinary_people}
                for number, positive in enumerate(positives, 1):
                    pairs.append({"pair": anchor + f"-g{number}", "group": group,
                                  "fold": fold, "left": ref, "right": positive,
                                  "genuine": True, "source_label": "BFW folder identity"})
                for number, other in enumerate(ordinary_people, 1):
                    b = min(images[other], key=lambda x: rank("ordinary:" + anchor, x))
                    pairs.append({"pair": anchor + f"-o{number}", "group": group,
                                  "fold": fold, "left": ref, "right": b,
                                  "genuine": False, "source_label": "BFW distinct folder identities"})
                present_other = next(x for x in others if x not in used_people)
                used_people.add(present_other)
                present_b = min(images[present_other], key=lambda x: rank("present-other:" + anchor, x))
                plans = [("present", "random", positives[0], present_b)]
                for number in range(2):
                    selected = [x for x in others if x not in used_people][:2]
                    b_id, c_id = selected
                    used_people.update(selected)
                    b = min(images[b_id], key=lambda x: rank(f"random-b:{anchor}:{number}", x))
                    c = min(images[c_id], key=lambda x: rank(f"random-c:{anchor}:{number}", x))
                    plans.append(("absent", "random", b, c))
                candidates = sorted(challenge[ref], key=lambda x: (-x[0], rank("challenge:" + anchor, x[1])))
                top = candidates[:math.ceil(len(candidates) * 0.20)]
                eligible_challenge = []
                for independent_score, image in top:
                    other_id = identity(image)
                    if other_id not in used_people and other_id not in [identity(x) for x in eligible_challenge]:
                        eligible_challenge.append(image)
                    if len(eligible_challenge) == 2:
                        break
                if len(eligible_challenge) != 2:
                    raise ValueError("Fewer than two independent-score challenge identities")
                for number, b in enumerate(eligible_challenge):
                    used_people.add(identity(b))
                    c_id = next(x for x in others if x not in used_people)
                    used_people.add(c_id)
                    c = min(images[c_id], key=lambda x: rank(f"challenge-c:{anchor}:{number}", x))
                    plans.append(("absent", "challenge", b, c))
                if len(plans) != 5:
                    raise AssertionError("One present plus four absent scenes required")
                for number, (kind, stratum, a, b) in enumerate(plans):
                    tiles = [a, b]
                    if rank("side:" + anchor, str(number))[-1] in "01234567":
                        tiles.reverse()
                    scene = composite(*(letterbox(get_image(image_zip, lookup, x)) for x in tiles))
                    scene_file = f"{anchor}-{number}.png"
                    path = args.output_dir / scene_file
                    if not cv2.imwrite(str(path), scene):
                        raise OSError(f"Cannot write {path}")
                    target_panel = tiles.index(positives[0]) if kind == "present" else None
                    scenes.append({"trial": f"{anchor}-{number}", "group": group, "fold": fold,
                                   "anchor": anchor, "kind": kind, "stratum": stratum,
                                   "reference_member": ref, "reference_identity": person,
                                   "panel_members": tiles, "panel_identities": [identity(x) for x in tiles],
                                   "target_panel": target_panel, "scene_file": scene_file,
                                   "scene_sha256": digest(path),
                                   "source_label": "BFW folder identity, validated against official pair table",
                                   "visual_review": "PENDING", "detector_audit": "PENDING"})
    seen = {row["reference_identity"] for row in scenes if row["group"] == "development"}
    unseen = {row["reference_identity"] for row in scenes if row["group"] == "evaluation"}
    if seen & unseen or len(seen) != 60 or len(unseen) != 60:
        raise ValueError("Anchor split differs")
    manifest = {"scope": "T-023 score-blind BFW candidate; not locked GT or model result",
                "seed": SEED, "release_sha256": OUTER_SHA256, "inner_md5": INNER_MD5,
                "construction": "one present/two hash-random absent/two top-20%-SENet-enriched absent per anchor",
                "letterbox": "aspect-preserving max-side 140 within 250x250 gray-127 panel; two panels, 16px gutter",
                "recognition_scores_read": False, "scenes": scenes, "pairs": pairs}
    path = args.output_dir / "candidate-manifest.json"
    path.write_bytes(encoded(manifest))
    print(json.dumps({"candidate_sha256": digest(path), "seed": SEED,
                      "identities": {"development": len(seen), "evaluation": len(unseen)},
                      "scenes": {"/".join(k): v for k, v in Counter(
                          (x["group"], x["kind"], x["stratum"]) for x in scenes).items()},
                      "pairs": {f"{group}/{kind}": v for (group, kind), v in Counter(
                          (x["group"], x["genuine"]) for x in pairs).items()},
                      "recognition_scores_read": False}, indent=2, default=str))


if __name__ == "__main__":
    main()
