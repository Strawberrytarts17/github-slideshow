"""Smoke tests for prepare_dataset.py and eval_ap.py --model on a toy dataset."""
import json
import os
import subprocess
import sys

import cv2
import numpy as np
import pytest

HERE = os.path.dirname(os.path.abspath(__file__))
TOOLS = os.path.join(HERE, "..", "tools")
SRC21 = ["Button", "TextButton", "Icon", "Image", "Text", "EditText", "SearchBar", "Switch",
         "CheckBox", "RadioButton", "Slider", "ProgressBar", "Spinner", "Tab", "TabBar",
         "Toolbar", "ListItem", "List", "Card", "Chip", "Dialog"]


def _toy(root, n=12):
    for d in ("images", "labels"):
        os.makedirs(os.path.join(root, d))
    open(os.path.join(root, "classes.txt"), "w").write("\n".join(SRC21) + "\n")
    with open(os.path.join(root, "meta.jsonl"), "w") as meta:
        for i in range(n):
            stem = "f%03d" % i
            cv2.imwrite(os.path.join(root, "images", stem + ".png"), np.full((234, 108, 3), 240, np.uint8))
            rows = ["18 0.5 0.5 0.4 0.2",      # Card -> ListItem
                    "17 0.5 0.5 0.9 0.8",      # List -> dropped by map
                    "7 0.5 0.2 0.2 0.05",      # Switch
                    "4 0.5 0.9 0.0 0.1",       # degenerate -> dropped
                    "2 0.99 0.5 0.1 0.1"]      # out of bounds -> dropped
            open(os.path.join(root, "labels", stem + ".txt"), "w").write("\n".join(rows) + "\n")
            meta.write(json.dumps({"image": "images/%s.png" % stem, "package": "app%d" % (i % 6),
                                   "width": 1080, "height": 2340}) + "\n")


def test_prepare_remaps_validates_and_splits_by_app(tmp_path):
    src, out = str(tmp_path / "src"), str(tmp_path / "out")
    _toy(src)
    subprocess.run([sys.executable, os.path.join(TOOLS, "prepare_dataset.py"), src, out,
                    "--holdout", "0.4"], check=True, capture_output=True)
    rep = json.load(open(os.path.join(out, "report.json")))
    assert rep["stats"]["boxes_in"] == 60 and rep["stats"]["boxes_out"] == 24
    assert rep["stats"]["dropped_by_map"] == 12 and rep["stats"]["dropped_geometry"] == 24
    names = open(os.path.join(out, "classes.txt")).read().split()
    lab = np.loadtxt(os.path.join(out, "labels", "f000.txt"), ndmin=2)
    assert sorted(names[int(c)] for c in lab[:, 0]) == ["ListItem", "Switch"]
    tr = open(os.path.join(out, "train.txt")).read().split()
    ho = open(os.path.join(out, "holdout.txt")).read().split()
    assert len(tr) + len(ho) == 12
    app = lambda p: int(os.path.basename(p)[1:4]) % 6  # noqa: E731
    assert not {app(p) for p in tr} & {app(p) for p in ho}  # no app on both sides


def test_prepare_refuses_unmapped_class(tmp_path):
    src = str(tmp_path / "src")
    _toy(src, n=1)
    open(os.path.join(src, "classes.txt"), "a").write("Remember\n")
    r = subprocess.run([sys.executable, os.path.join(TOOLS, "prepare_dataset.py"), src,
                        str(tmp_path / "o")], capture_output=True, text=True)
    assert r.returncode != 0 and "Remember" in r.stderr


@pytest.mark.skipif(not os.environ.get("L1DET_MODEL"), reason="set L1DET_MODEL")
def test_eval_runs_model_end_to_end(tmp_path):
    src, out = str(tmp_path / "src"), str(tmp_path / "out")
    _toy(src)
    subprocess.run([sys.executable, os.path.join(TOOLS, "prepare_dataset.py"), src, out], check=True,
                   capture_output=True)
    r = subprocess.run([sys.executable, os.path.join(TOOLS, "eval_ap.py"), "--gt", os.path.join(out, "labels"),
                        "--images", os.path.join(src, "images"), "--model", os.environ["L1DET_MODEL"],
                        "--json", str(tmp_path / "r.json")], capture_output=True, text=True, check=True)
    assert "mAP50" in r.stdout
    rows = json.load(open(tmp_path / "r.json"))["rows"]
    assert {x["cls"] for x in rows if x["n_gt"]} == {"ListItem", "Switch"}
