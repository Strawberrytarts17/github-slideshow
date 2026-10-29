"""Remap a collected YOLO dataset to the L1 taxonomy, validate it, split by app,
and report per-class coverage against the first-run targets. numpy only.

    python prepare_dataset.py SRC OUT [--source device21] [--group-key package]

SRC is collect.py output: images/, labels/, classes.txt, meta.jsonl.
Class names (not ids) are mapped, so SRC may use any index order.
OUT gets labels/ (remapped), train.txt / holdout.txt (image paths) and
report.json. Images are referenced, not copied.

The split is by group (app package), never by frame: frames of one app are
near-duplicates even after dHash, and a frame-level split inflates AP.
"""
import argparse
import collections
import hashlib
import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
TARGET = open(os.path.join(HERE, "..", "classes.txt")).read().split()

# source class name -> L1 class name (None = drop the box). Single source of
# truth for the taxonomy; edit here, not in collect.py, and re-run.
SOURCE_MAPS = {
    # collect.py's proposed 21-class taxonomy
    "device21": {**{n: n for n in TARGET}, "Card": "ListItem", "List": None},
    # CLAY (google-research-datasets/clay label_map.txt). BUTTON splits into
    # TextButton/Button by whether the Rico node has text — done in the CLAY
    # converter, which emits BUTTON_TEXT / BUTTON_NOTEXT.
    "clay": {
        "TEXT": "Text", "LABEL": "Text", "PICTOGRAM": "Icon", "IMAGE": "Image",
        "BUTTON_TEXT": "TextButton", "BUTTON_NOTEXT": "Button",
        "TEXT_INPUT": "EditText", "CHECK_BOX": "CheckBox", "RADIO_BUTTON": "RadioButton",
        "SWITCH": "Switch", "SLIDER": "Slider", "PROGRESS_BAR": "ProgressBar",
        "SPINNER": "Spinner", "NAVIGATION_BAR": "TabBar", "TOOLBAR": "Toolbar",
        "LIST_ITEM": "ListItem", "CARD_VIEW": "ListItem",
        "ROOT": None, "BACKGROUND": None, "CONTAINER": None, "DRAWER": None,
        "PAGER_INDICATOR": None, "ADVERTISEMENT": None, "MAP": None,
        "DATE_PICKER": None, "NUMBER_STEPPER": None,
    },
}

# First-run targets: (instances, distinct apps). Classes with no public source
# (CLAY has none of these) need the most device data.
NO_PUBLIC = {"SearchBar", "Chip", "Tab", "Dialog"}
TARGETS = {n: (300, 15) if n in NO_PUBLIC else (100, 10) for n in TARGET}


def load_meta(path, image_key):
    meta = {}
    if os.path.exists(path):
        for line in open(path, encoding="utf-8"):
            if line.strip():
                r = json.loads(line)
                stem = os.path.splitext(os.path.basename(str(r.get(image_key, ""))))[0]
                meta[stem] = r
    return meta


def is_holdout(group, frac):
    h = int(hashlib.sha1(group.encode("utf-8")).hexdigest()[:8], 16)
    return h / 0xFFFFFFFF < frac


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src")
    ap.add_argument("out")
    ap.add_argument("--source", default="device21", choices=sorted(SOURCE_MAPS))
    ap.add_argument("--group-key", default="package", help="meta.jsonl field to split on")
    ap.add_argument("--image-key", default="image", help="meta.jsonl field naming the image")
    ap.add_argument("--holdout", type=float, default=0.15, help="fraction of groups held out")
    ap.add_argument("--min-px", type=float, default=8, help="drop boxes thinner than this")
    a = ap.parse_args()

    src_names = open(os.path.join(a.src, "classes.txt")).read().split()
    cmap = SOURCE_MAPS[a.source]
    unknown = [n for n in src_names if n not in cmap]
    if unknown:
        sys.exit("unmapped source classes %s: add them to SOURCE_MAPS[%r]" % (unknown, a.source))
    lut = {i: (TARGET.index(cmap[n]) if cmap[n] else -1) for i, n in enumerate(src_names)}
    meta = load_meta(os.path.join(a.src, "meta.jsonl"), a.image_key)

    img_dir, lab_dir = os.path.join(a.src, "images"), os.path.join(a.src, "labels")
    out_lab = os.path.join(a.out, "labels")
    os.makedirs(out_lab, exist_ok=True)
    stats = {"frames": 0, "boxes_in": 0, "boxes_out": 0, "dropped_by_map": 0,
             "dropped_geometry": 0, "frames_no_meta": 0, "frames_empty": 0}
    inst = collections.Counter()
    apps = collections.defaultdict(set)
    split = {"train": [], "holdout": []}
    groups = {"train": set(), "holdout": set()}
    for fn in sorted(os.listdir(img_dir)):
        stem = os.path.splitext(fn)[0]
        lp = os.path.join(lab_dir, stem + ".txt")
        if not os.path.exists(lp):
            continue
        stats["frames"] += 1
        m = meta.get(stem)
        if m is None:
            stats["frames_no_meta"] += 1
        group = str(m.get(a.group_key, "unknown")) if m else "unknown"
        w = float(m.get("width", 0)) if m else 0
        h = float(m.get("height", 0)) if m else 0
        lab = np.loadtxt(lp, ndmin=2, dtype=np.float64).reshape(-1, 5)
        stats["boxes_in"] += len(lab)
        keep = []
        for c, xc, yc, bw, bh in lab:
            t = lut.get(int(c), -1)
            if t < 0:
                stats["dropped_by_map"] += 1
                continue
            x1, y1, x2, y2 = xc - bw / 2, yc - bh / 2, xc + bw / 2, yc + bh / 2
            thin = w and h and (bw * w < a.min_px or bh * h < a.min_px)
            if bw <= 0 or bh <= 0 or x1 < -1e-3 or y1 < -1e-3 or x2 > 1 + 1e-3 or y2 > 1 + 1e-3 or thin:
                stats["dropped_geometry"] += 1
                continue
            keep.append((t, xc, yc, bw, bh))
        if not keep:
            stats["frames_empty"] += 1  # kept: pure negatives are still signal
        part = "holdout" if is_holdout(group, a.holdout) else "train"
        split[part].append(os.path.abspath(os.path.join(img_dir, fn)))
        groups[part].add(group)
        with open(os.path.join(out_lab, stem + ".txt"), "w") as f:
            for t, xc, yc, bw, bh in keep:
                f.write("%d %.6f %.6f %.6f %.6f\n" % (t, xc, yc, bw, bh))
                inst[TARGET[t]] += 1
                apps[TARGET[t]].add(group)
        stats["boxes_out"] += len(keep)

    for part, paths in split.items():
        with open(os.path.join(a.out, part + ".txt"), "w") as f:
            f.write("\n".join(paths) + ("\n" if paths else ""))
    with open(os.path.join(a.out, "classes.txt"), "w") as f:
        f.write("\n".join(TARGET) + "\n")
    cover = []
    for n in TARGET:
        need_i, need_a = TARGETS[n]
        cover.append({"cls": n, "instances": inst[n], "apps": len(apps[n]),
                      "target": [need_i, need_a],
                      "ok": inst[n] >= need_i and len(apps[n]) >= need_a})
    report = {"stats": stats, "groups": {k: len(v) for k, v in groups.items()},
              "frames": {k: len(v) for k, v in split.items()}, "coverage": cover}
    json.dump(report, open(os.path.join(a.out, "report.json"), "w"), indent=1)

    print(json.dumps(stats))
    print("groups train/holdout: %d/%d  frames: %d/%d" % (
        len(groups["train"]), len(groups["holdout"]), len(split["train"]), len(split["holdout"])))
    if "unknown" in groups["train"] | groups["holdout"]:
        print("WARNING: frames without meta/%s are grouped as 'unknown' (one app)" % a.group_key)
    print("%-12s %7s %5s  %s" % ("class", "inst", "apps", "first-run target"))
    for r in cover:
        print("%-12s %7d %5d  %s %d inst / %d apps" % (
            r["cls"], r["instances"], r["apps"], "ok  " if r["ok"] else "NEED", *r["target"]))


if __name__ == "__main__":
    main()
