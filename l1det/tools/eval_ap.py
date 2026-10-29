"""Per-class AP on a held-out set. numpy only (+ cv2/onnxruntime with --model),
so it runs on the device as well as off-box.

    # score an ONNX model directly on held-out screenshots
    python eval_ap.py --gt held_out/labels --images held_out/images --model ui_detect_l1.onnx
    # or score prediction files: one .txt per image, "cls xc yc w h conf" normalized
    python eval_ap.py --gt held_out/labels --pred preds/

GT is YOLO "cls xc yc w h" normalized, class ids in classes.txt order.
IoU is invariant to per-axis scaling, so everything stays normalized.
Reports AP50, AP50:95 (COCO 101-point), recall at --conf, and the top
cross-class confusions (what each missed GT box was predicted as instead).
"""
import argparse
import collections
import glob
import json
import os

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
IOUS = np.linspace(0.5, 0.95, 10)


def read_txt(path, with_conf):
    if not os.path.exists(path):
        return np.zeros((0, 6 if with_conf else 5), np.float32)
    a = np.loadtxt(path, ndmin=2, dtype=np.float32)
    return a.reshape(-1, 6 if with_conf else 5)


def xywh2xyxy(b):
    return np.stack([b[:, 0] - b[:, 2] / 2, b[:, 1] - b[:, 3] / 2,
                     b[:, 0] + b[:, 2] / 2, b[:, 1] + b[:, 3] / 2], 1)


def iou_matrix(a, b):
    tl = np.maximum(a[:, None, :2], b[None, :, :2])
    br = np.minimum(a[:, None, 2:], b[None, :, 2:])
    inter = np.prod(np.clip(br - tl, 0, None), 2)
    area = lambda x: np.prod(np.clip(x[:, 2:] - x[:, :2], 0, None), 1)  # noqa: E731
    return inter / np.maximum(area(a)[:, None] + area(b)[None] - inter, 1e-12)


def ap101(tp, conf, n_gt):
    if n_gt == 0:
        return float("nan")
    if len(tp) == 0:
        return 0.0
    o = np.argsort(-conf, kind="stable")
    ctp = np.cumsum(tp[o])
    rec = ctp / n_gt
    prec = ctp / np.arange(1, len(ctp) + 1)
    prec = np.maximum.accumulate(prec[::-1])[::-1]  # monotone envelope
    idx = np.searchsorted(rec, np.linspace(0, 1, 101), side="left")
    return float(np.where(idx < len(prec), prec[np.minimum(idx, len(prec) - 1)], 0).mean())


def evaluate(pairs, names, conf_op=0.25):
    """pairs: iterable of (gt (N,5) cls,xc,yc,w,h ; pred (M,6) cls,xc,yc,w,h,conf)."""
    nc = len(names)
    tps = [[[] for _ in IOUS] for _ in range(nc)]
    confs = [[] for _ in range(nc)]
    n_gt = np.zeros(nc, int)
    hit_op = np.zeros(nc, int)
    confusion = collections.Counter()
    for gt, pr in pairs:
        gb, pb = xywh2xyxy(gt[:, 1:5]), xywh2xyxy(pr[:, 1:5])
        gc, pc, ps = gt[:, 0].astype(int), pr[:, 0].astype(int), pr[:, 5]
        iou_all = iou_matrix(gb, pb) if len(gb) and len(pb) else np.zeros((len(gb), len(pb)))
        for c in range(nc):
            gi, pi = np.where(gc == c)[0], np.where(pc == c)[0]
            n_gt[c] += len(gi)
            pi = pi[np.argsort(-ps[pi], kind="stable")]
            confs[c].extend(ps[pi].tolist())
            ious = iou_all[np.ix_(gi, pi)]
            for t, thr in enumerate(IOUS):
                used = np.zeros(len(gi), bool)
                tp = np.zeros(len(pi))
                for j in range(len(pi)):
                    if not len(gi):
                        break
                    cand = np.where(~used & (ious[:, j] >= thr))[0]
                    if len(cand):
                        k = cand[np.argmax(ious[cand, j])]
                        used[k], tp[j] = True, 1
                tps[c][t].extend(tp.tolist())
                if t == 0:
                    op = ps[pi] >= conf_op
                    hit_op[c] += int(tp[op].sum())
        # confusion at the operating point: GT with no same-class match at
        # IoU 0.5 -> class of the best-overlapping other prediction
        live = ps >= conf_op
        for g in range(len(gb)):
            if not live.any():
                break
            ov = np.where(live, iou_all[g], 0)
            if ((pc == gc[g]) & (ov >= 0.5)).any():
                continue
            j = int(np.argmax(ov))
            if ov[j] >= 0.5:
                confusion[(names[gc[g]], names[pc[j]])] += 1
    rows = []
    for c in range(nc):
        cf = np.asarray(confs[c])
        aps = [ap101(np.asarray(tps[c][t]), cf, n_gt[c]) for t in range(len(IOUS))]
        rows.append({"cls": names[c], "n_gt": int(n_gt[c]), "AP50": aps[0],
                     "AP50_95": float(np.mean(aps)) if n_gt[c] else float("nan"),
                     "R@conf": hit_op[c] / n_gt[c] if n_gt[c] else float("nan")})
    return rows, confusion


def predict_dir(model, images, conf):
    import cv2
    import sys
    sys.path.insert(0, os.path.join(HERE, "..", "runtime"))
    from ui_detect_l1 import L1Detector
    det = L1Detector(model)
    out = {}
    for p in sorted(glob.glob(os.path.join(images, "*"))):
        img = cv2.imread(p)
        if img is None:
            continue
        h, w = img.shape[:2]
        d = det.raw(img, conf=conf)
        xc, yc = (d[:, 0] + d[:, 2]) / 2 / w, (d[:, 1] + d[:, 3]) / 2 / h
        bw, bh = (d[:, 2] - d[:, 0]) / w, (d[:, 3] - d[:, 1]) / h
        out[os.path.splitext(os.path.basename(p))[0]] = np.stack([d[:, 5], xc, yc, bw, bh, d[:, 4]], 1)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--gt", required=True)
    ap.add_argument("--pred", help="dir of prediction .txt (cls xc yc w h conf)")
    ap.add_argument("--images", help="with --model: dir of held-out screenshots")
    ap.add_argument("--model")
    ap.add_argument("--classes", default=os.path.join(HERE, "..", "classes.txt"))
    ap.add_argument("--conf", type=float, default=0.25, help="operating point for R@conf")
    ap.add_argument("--json", help="write results here")
    a = ap.parse_args()
    names = open(a.classes).read().split()
    stems = sorted(os.path.splitext(os.path.basename(p))[0] for p in glob.glob(os.path.join(a.gt, "*.txt")))
    if a.model:
        preds = predict_dir(a.model, a.images, conf=0.001)  # full PR curve, floor near 0
    else:
        preds = {s: read_txt(os.path.join(a.pred, s + ".txt"), True) for s in stems}
    pairs = ((read_txt(os.path.join(a.gt, s + ".txt"), False),
              preds.get(s, np.zeros((0, 6), np.float32))) for s in stems)
    rows, conf = evaluate(pairs, names, a.conf)
    print("%d images" % len(stems))
    print("%-12s %6s %6s %8s %7s" % ("class", "n_gt", "AP50", "AP50:95", "R@%.2f" % a.conf))
    for r in sorted(rows, key=lambda r: (np.nan_to_num(r["AP50"], nan=9), r["cls"])):
        print("%-12s %6d %6.3f %8.3f %7.3f" % (r["cls"], r["n_gt"], r["AP50"], r["AP50_95"], r["R@conf"]))
    valid = [r for r in rows if r["n_gt"]]
    print("mAP50 %.3f  mAP50:95 %.3f  (over %d classes with GT)" % (
        np.mean([r["AP50"] for r in valid]), np.mean([r["AP50_95"] for r in valid]), len(valid)))
    if conf:
        print("top confusions (GT -> predicted, IoU>=0.5):")
        for (g, p), n in conf.most_common(10):
            print("  %-12s -> %-12s %d" % (g, p, n))
    if a.json:
        json.dump({"rows": rows, "confusion": [[g, p, n] for (g, p), n in conf.most_common()]},
                  open(a.json, "w"), indent=1)


if __name__ == "__main__":
    main()
