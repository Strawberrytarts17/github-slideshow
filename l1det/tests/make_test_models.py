"""Build the random-weight fixture pair for test_runtime.py (off-box, needs torch).

    python make_test_models.py --nanodet-root ext/nanodet --out-dir /tmp/l1
BN is calibrated and class logits re-initialized so scores spread over (0, 1);
with plain random init every score sits at the 0.01 prior.
"""
import argparse
import os
import sys

import torch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "export"))
from export_onnx import build, export  # noqa: E402
from ui_detect_l1 import NAMES  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("--nanodet-root", required=True)
ap.add_argument("--out-dir", required=True)
a = ap.parse_args()
torch.manual_seed(0)
cfg = os.path.join(a.nanodet_root, "config", "nanodet-plus-m-1.5x_416.yml")
model, nc = build(a.nanodet_root, cfg, None, len(NAMES))
with torch.no_grad():
    # random init + default BN stats makes head features vanish (~1e-9);
    # calibrate BN on noise so activations are unit-scale, then spread logits
    for mod in model.modules():
        if isinstance(mod, torch.nn.BatchNorm2d):
            mod.reset_running_stats()
            mod.momentum = None
    model.train()
    for _ in range(4):
        x = (torch.rand(2, 3, 640, 320) * 255 - 114) / 58
        model.head(model.fpn(model.backbone(x)))
    model.eval()
    for conv in model.head.gfl_cls:
        conv.bias[:nc] = -1.0
        conv.weight[:nc].normal_(0, 0.004)
os.makedirs(a.out_dir, exist_ok=True)
for raw in (False, True):
    path = os.path.join(a.out_dir, "fixture%s.onnx" % ("_raw" if raw else ""))
    print(export(model, nc, path, raw=raw, meta={"weights": "RANDOM - test/benchmark fixture, not a detector"}))
