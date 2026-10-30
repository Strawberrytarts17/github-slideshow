"""focal_train — build the onnx backend's cell classifier from collect.py data (runs on a PC).

  python focal_train.py tiles ../data/ui_dataset ../data/focal_tiles     # YOLO boxes -> labelled 3×3 cells
  python focal_train.py train ../data/focal_tiles ../models/focal_cls_v1/model.onnx
  phone: copy model.onnx to models/focal_cls_v1/, then focal.use('auto') and focal.selfcheck()

tiles  For each screenshot, gaze the way focal.look(at=el) does (focal.fit, r jittered ×0.7-1.3) on a
       few boxes plus two random gazes, cut the 3×3 cells and label each with focal.assign (the same
       rule as the detect backend, so both backends mean the same thing by a label). A cell no box
       claims becomes 'blank' only if the pixel heuristic agrees; otherwise it is dropped, because
       a11y labels miss self-drawn widgets and unknown is not blank.
train  A 4-block CNN (~0.3 M params, ~1.2 MB) trained from scratch on the tiles: small enough for 9
       tiles per look on a phone CPU and free of third-party weights, so no licence question (never
       start from the ui_detect ONNX weights, see MODEL_NOTICE). Classes, size, mean, std and rgb go
       into the ONNX metadata, so model.onnx is the only file to copy.
       PC needs: pip install torch torchvision onnx onnxscript
"""
import argparse
import glob
import json
import os
from collections import Counter

import numpy as np
from PIL import Image

import focal

EXTS = ('.png', '.jpg', '.jpeg', '.webp')
MEAN, STD = [0.485, 0.456, 0.406], [0.229, 0.224, 0.225]


def _names(src, names=None):
    for p in (names, os.path.join(src, 'classes.txt'), os.path.join(os.path.dirname(src.rstrip('/')), 'classes.txt')):
        if p and os.path.isfile(p):
            with open(p, encoding='utf-8') as fh:
                return [ln.strip() for ln in fh if ln.strip()]
    ul = focal._mod('ui_detect_lite')
    if getattr(ul, 'NAMES', None):
        return list(ul.NAMES)
    raise SystemExit('no class list: pass --names temp/l1det/classes.txt')


def _yolo(path, names, w, h):
    dets = []
    with open(path, encoding='utf-8') as fh:
        for line in fh:
            p = line.split()
            if len(p) < 5:
                continue
            k, cx, cy, bw, bh = int(p[0]), *map(float, p[1:5])
            dets.append({'cls': focal._canon(names[k]) if k < len(names) else str(k), 'conf': 1.0, 'text': '',
                         'box': ((cx - bw / 2) * w, (cy - bh / 2) * h, (cx + bw / 2) * w, (cy + bh / 2) * h)})
    return dets


def tiles(src, dst, per_image=6, seed=0, names=None):
    """Write dst/<class>/<image>_<gaze>_<cell>.png; return Counter of tiles per class."""
    names, rng, counts = _names(src, names), np.random.default_rng(seed), Counter()
    for img_path in sorted(glob.glob(os.path.join(src, '**', '*'), recursive=True)):
        stem, ext = os.path.splitext(img_path)
        lab = stem.replace(os.sep + 'images' + os.sep, os.sep + 'labels' + os.sep) + '.txt'
        if ext.lower() not in EXTS or not os.path.isfile(lab):
            continue
        rgb = np.asarray(Image.open(img_path).convert('RGB'))
        bgr = np.ascontiguousarray(rgb[..., ::-1])
        h, w = bgr.shape[:2]
        dets = _yolo(lab, names, w, h)
        picks = rng.permutation(len(dets))[:max(0, per_image - 2)]
        gazes = [(x, y, r * rng.uniform(0.7, 1.3)) for x, y, r in (focal.fit(dets[i]['box']) for i in picks)]
        gazes += [(rng.uniform(0, w), rng.uniform(0, h), min(w, h) / 6 * rng.uniform(0.5, 1.5)) for _ in range(2)]
        for g, (x, y, r) in enumerate(gazes):
            x, y, r = focal._clamp(x, y, r or min(w, h) / 6, w, h)
            boxes = focal._grid_boxes((x - r, y - r, x + r, y + r))
            for name, b, hit in zip(focal.CELLS, boxes, focal.assign(boxes, dets)):
                if hit is None and focal._pixel(bgr[b[1]:b[3], b[0]:b[2]])[0] != 'blank':
                    continue
                cls = hit[0] if hit else 'blank'
                os.makedirs(os.path.join(dst, cls), exist_ok=True)
                tag = os.path.basename(stem)
                Image.fromarray(rgb[b[1]:b[3], b[0]:b[2]]).save(os.path.join(dst, cls, f'{tag}_{g}_{name}.png'))
                counts[cls] += 1
    return counts


def net(k, widths=(32, 64, 128, 192)):
    """conv-bn-relu-pool ×4 -> global average -> linear. Any input size >= 16 px."""
    from torch import nn
    layers, c = [], 3
    for w in widths:
        layers += [nn.Conv2d(c, w, 3, padding=1, bias=False), nn.BatchNorm2d(w), nn.ReLU(inplace=True), nn.MaxPool2d(2)]
        c = w
    return nn.Sequential(*layers, nn.AdaptiveAvgPool2d(1), nn.Flatten(), nn.Dropout(0.2), nn.Linear(c, k))


def train(src, out, epochs=15, size=64, batch=64, lr=3e-3, seed=0, workers=2):
    """Train on dst/<class>/*.png from tiles(); export a self-describing ONNX; return val accuracy."""
    import onnx
    import torch
    import torchvision
    from torch import nn
    from torchvision import transforms as T

    torch.manual_seed(seed)
    base = [T.Resize((size, size)), T.ToTensor(), T.Normalize(MEAN, STD)]
    full = torchvision.datasets.ImageFolder(src)
    classes = full.classes
    # split by source screenshot (tile names are <screenshot>_<gaze>_<cell>.png): cells of one screen
    # in both halves would make val accuracy look better than it is
    shots = [os.path.basename(p).rsplit('_', 2)[0] for p, _ in full.samples]
    uniq = sorted(set(shots))
    held = {uniq[i] for i in torch.randperm(len(uniq))[:max(1, len(uniq) // 10)].tolist()}
    val_idx = [i for i, s in enumerate(shots) if s in held]
    tr_idx = [i for i, s in enumerate(shots) if s not in held]
    n_val = len(val_idx)
    tr = torchvision.datasets.ImageFolder(src, T.Compose([T.ColorJitter(0.2, 0.2, 0.2)] + base))
    va = torchvision.datasets.ImageFolder(src, T.Compose(base))
    tr_dl = torch.utils.data.DataLoader(torch.utils.data.Subset(tr, tr_idx), batch, shuffle=True,
                                        num_workers=workers)
    va_dl = torch.utils.data.DataLoader(torch.utils.data.Subset(va, val_idx), batch, num_workers=workers)

    model = net(len(classes))
    freq = torch.bincount(torch.tensor(full.targets), minlength=len(classes)).float().clamp(min=1)
    loss_fn = nn.CrossEntropyLoss(weight=(freq.sum() / freq).sqrt())  # damp blank/Text dominance
    opt = torch.optim.AdamW(model.parameters(), lr)
    sched = torch.optim.lr_scheduler.OneCycleLR(opt, lr, total_steps=max(1, epochs * len(tr_dl)))

    acc = 0.0
    for ep in range(epochs):
        model.train()
        for x, y in tr_dl:
            opt.zero_grad()
            loss_fn(model(x), y).backward()
            opt.step()
            sched.step()
        model.eval()
        hit, per = 0, Counter()
        with torch.no_grad():
            for x, y in va_dl:
                p = model(x).argmax(1)
                hit += int((p == y).sum())
                for t, q in zip(y.tolist(), p.tolist()):
                    per[(classes[t], t == q)] += 1
        acc = hit / n_val
        print(f'epoch {ep + 1}/{epochs} val acc {acc:.3f}')
    print('per class (right/total):', ', '.join(
        f'{c} {per[(c, True)]}/{per[(c, True)] + per[(c, False)]}' for c in classes))

    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    model.eval()
    torch.onnx.export(model, (torch.zeros(2, 3, size, size),), out, input_names=['x'], output_names=['logits'],
                      dynamic_shapes=({0: torch.export.Dim('n')},), external_data=False)  # dummy n=2: export pins size-1 dims
    m = onnx.load(out)
    meta = {'classes': classes, 'size': size, 'mean': MEAN, 'std': STD, 'rgb': True,
            'source': f'focal_train: 4-block CNN from scratch, {len(full)} tiles, val acc {acc:.3f}'}
    for k, v in meta.items():
        m.metadata_props.add(key=k, value=json.dumps(v, ensure_ascii=False))
    onnx.save(m, out)
    print(f'wrote {out} ({os.path.getsize(out) // 1024} KB, {len(classes)} classes)')
    return acc


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    sub = ap.add_subparsers(dest='cmd', required=True)
    a = sub.add_parser('tiles')
    a.add_argument('src')
    a.add_argument('dst')
    a.add_argument('--per-image', type=int, default=6)
    a.add_argument('--names')
    b = sub.add_parser('train')
    b.add_argument('src')
    b.add_argument('out')
    b.add_argument('--epochs', type=int, default=15)
    b.add_argument('--size', type=int, default=64)
    args = ap.parse_args()
    if args.cmd == 'tiles':
        print(dict(tiles(args.src, args.dst, args.per_image, names=args.names)))
    else:
        train(args.src, args.out, args.epochs, args.size)
