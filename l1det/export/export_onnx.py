"""Export a NanoDet-Plus checkpoint to the L1 ONNX contract (off-box only).

Graph: BGR 0..255 -> normalize -> backbone/FPN/head -> DFL decode ->
single-label (argmax) -> class-aware NMS -> dets [1, K, 6].

conf_floor / iou_thr / max_det are required graph inputs: every caller states
the floor explicitly (the incumbent's 0.25 floor was baked in and invisible).

    python export_onnx.py --nanodet-root ext/nanodet \
        --config config/l1det.yml --ckpt model_best.ckpt --out ui_detect_l1.onnx
Without --ckpt the weights are random (latency benchmarking only).
"""
import argparse
import json
import os
import sys

import onnx
import torch
import torch.nn as nn
import torch.nn.functional as F

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "runtime"))
from ui_detect_l1 import NAMES, STRIDES, REG_MAX, STRIDE  # noqa: E402

# NanoDet's training normalization (BGR order)
MEAN = (103.53, 116.28, 123.675)
STD = (57.375, 57.12, 58.395)
DEFAULTS = {"conf_floor": 0.25, "iou_thr": 0.6, "max_det": 300}  # trace-time values only
OPSET = 17


class _NMS(torch.autograd.Function):
    """ONNX NonMaxSuppression. Eager forward is a placeholder; only the
    exported graph is used (and tested against the numpy reference)."""

    @staticmethod
    def forward(ctx, boxes, scores, max_det, iou_thr, conf_floor):
        n = min(int(max_det), boxes.shape[1])
        idx = torch.zeros((n, 3), dtype=torch.int64)
        idx[:, 2] = torch.arange(n)
        return idx

    @staticmethod
    def symbolic(g, boxes, scores, max_det, iou_thr, conf_floor):
        return g.op("NonMaxSuppression", boxes, scores, max_det, iou_thr,
                    conf_floor, center_point_box_i=0)


class Deploy(nn.Module):
    def __init__(self, model, num_classes, raw=False):
        super().__init__()
        self.backbone, self.fpn, self.head = model.backbone, model.fpn, model.head
        self.nc, self.raw = num_classes, raw
        self.register_buffer("mean", torch.tensor(MEAN).view(1, 3, 1, 1))
        self.register_buffer("std", torch.tensor(STD).view(1, 3, 1, 1))
        self.register_buffer("proj", torch.arange(REG_MAX + 1, dtype=torch.float32))

    def forward(self, images, conf_floor=None, iou_thr=None, max_det=None):
        x = (images - self.mean) / self.std
        out = self.head._forward_onnx(self.fpn(self.backbone(x)))  # [1,N,C+4(R+1)]
        if self.raw:
            return out
        cls, reg = out[0].split([self.nc, 4 * (REG_MAX + 1)], dim=-1)
        h, w = images.shape[2], images.shape[3]
        pri = []
        for s in STRIDES:
            ys = torch.arange(h // s, dtype=torch.float32) * s
            xs = torch.arange(w // s, dtype=torch.float32) * s
            yy, xx = torch.meshgrid(ys, xs, indexing="ij")
            pri.append(torch.stack([xx.flatten(), yy.flatten(),
                                    torch.full_like(xx.flatten(), s)], -1))
        pri = torch.cat(pri, 0)
        dist = F.softmax(reg.reshape(-1, 4, REG_MAX + 1), -1) @ self.proj
        dist = dist * pri[:, 2:3]
        wh = torch._shape_as_tensor(images)[2:].flip(0).repeat(2).to(torch.float32)
        boxes = torch.stack([pri[:, 0] - dist[:, 0], pri[:, 1] - dist[:, 1],
                             pri[:, 0] + dist[:, 2], pri[:, 1] + dist[:, 3]], -1)
        boxes = torch.minimum(boxes.clamp(min=0), wh)
        score, label = cls.max(-1)
        shifted = boxes + label.unsqueeze(-1).to(torch.float32) * 4096.0
        keep = _NMS.apply(shifted.unsqueeze(0), score.view(1, 1, -1),
                          max_det, iou_thr, conf_floor)[:, 2]
        dets = torch.cat([boxes[keep], score[keep].unsqueeze(-1),
                          label[keep].unsqueeze(-1).to(torch.float32)], -1)
        return dets.unsqueeze(0)


def _channel_shuffle(x, groups):
    # upstream uses x.data.size(), which bakes the trace-time H,W into the
    # graph and breaks every other input shape; x.shape stays symbolic
    b, c, h, w = x.shape
    x = x.view(b, groups, c // groups, h, w).transpose(1, 2).contiguous()
    return x.view(b, -1, h, w)


def build(nanodet_root, config, ckpt, num_classes=None):
    sys.path.insert(0, nanodet_root)
    from nanodet.model.arch import build_model
    from nanodet.model.backbone import shufflenetv2
    from nanodet.util import cfg, load_config

    shufflenetv2.channel_shuffle = _channel_shuffle

    load_config(cfg, config)
    cfg.defrost()
    cfg.model.arch.backbone.pretrain = False  # never pull ImageNet weights here
    if num_classes:
        cfg.model.arch.head.num_classes = cfg.model.arch.aux_head.num_classes = num_classes
    model = build_model(cfg.model)
    if ckpt:
        sd = torch.load(ckpt, map_location="cpu", weights_only=False)
        sd = sd.get("state_dict", sd)
        # prefer EMA weights, strip the lightning "model." prefix
        ema = {k[len("avg_model."):]: v for k, v in sd.items() if k.startswith("avg_model.")}
        sd = ema or {k[len("model."):] if k.startswith("model.") else k: v for k, v in sd.items()}
        missing, _ = model.load_state_dict(sd, strict=False)
        missing = [k for k in missing if not k.startswith("aux")]
        if missing:
            raise RuntimeError("checkpoint missing keys: %s" % missing[:5])
    return model.eval(), cfg.model.arch.head.num_classes


def export(model, nc, out, shape=(640, 320), raw=False, meta=None):
    dep = Deploy(model, nc, raw).eval()
    x = torch.randn(1, 3, *shape) * 50 + 114
    if raw:
        args, names = (x,), ["images"]
    else:
        args = (x, torch.tensor([DEFAULTS["conf_floor"]]), torch.tensor([DEFAULTS["iou_thr"]]),
                torch.tensor([DEFAULTS["max_det"]], dtype=torch.int64))
        names = ["images", "conf_floor", "iou_thr", "max_det"]
    out_name = "raw" if raw else "dets"
    torch.onnx.export(
        dep, args, out, opset_version=OPSET, dynamo=False, do_constant_folding=True,
        input_names=names, output_names=[out_name],
        dynamic_axes={"images": {2: "H", 3: "W"}, out_name: {1: "K"}},
    )
    m = onnx.load(out)
    md = {
        "names": json.dumps(NAMES if nc == len(NAMES) else list(range(nc))),
        "input": "BGR float32 0..255 NCHW; letterbox longest side 640, top-left, "
                 "pad bottom/right to /%d with 114" % STRIDE,
        "output": "raw head [1,N,C+32], sigmoid applied" if raw else
                  "dets [1,K,6] x1,y1,x2,y2,conf,cls in input px, conf desc",
        "control_inputs": "conf_floor f32[1], iou_thr f32[1], max_det i64[1] (required)",
        "arch": "NanoDet-Plus (Apache-2.0)",
    }
    md.update(meta or {})
    for k, v in md.items():
        m.metadata_props.append(onnx.StringStringEntryProto(key=k, value=v))
    onnx.checker.check_model(m)
    onnx.save(m, out)
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--nanodet-root", required=True)
    ap.add_argument("--config", required=True)
    ap.add_argument("--ckpt", default=None)
    ap.add_argument("--out", default="ui_detect_l1.onnx")
    ap.add_argument("--num-classes", type=int, default=None, help="override config")
    ap.add_argument("--raw", action="store_true", help="no embedded decode/NMS")
    ap.add_argument("--meta", default="{}", help="extra metadata JSON (license, data)")
    a = ap.parse_args()
    mdl, ncls = build(a.nanodet_root, a.config, a.ckpt, a.num_classes)
    print(export(mdl, ncls, a.out, raw=a.raw, meta=json.loads(a.meta)))
