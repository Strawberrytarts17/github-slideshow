"""L1 UI element detector — on-device runtime.

Runs on the device: Python 3.10, numpy 1.26, cv2 4.5, onnxruntime CPU EP.
No torch / PIL / tflite. Drop-in for the incumbent ``NAMES`` / ``_yolo``.

Output schema (unchanged from ui_detect_lite.detect()):
    [{'bbox': [x1, y1, x2, y2], 'type': 'icon'|'text', 'label': None,
      'cls': str, 'confidence': float}]
bbox is full-screen physical pixels (letterbox already reversed).
``label`` is always None here; the OCR stage fills it.

Model contract (see export/export_onnx.py):
    inputs   images     float32 [1, 3, H, W]  BGR, 0..255, H and W multiples of 64
             conf_floor float32 [1]  required — the confidence floor
             iou_thr    float32 [1]  required
             max_det    int64   [1]  required
    output   dets       float32 [1, K, 6]  x1, y1, x2, y2, conf, cls
                        (letterboxed-input pixels, sorted by conf desc)
The confidence floor is a runtime input, not a baked constant: ``conf=0.05``
really does recall boxes down to 0.05.

A model exported *without* embedded NMS (raw head output
[1, N, C + 4*(REG_MAX+1)]) is also accepted; ``postprocess_raw`` is then the
exact post-processing, and doubles as the reference the embedded graph is
tested against.
"""
import json
import os

import cv2
import numpy as np
import onnxruntime as ort

_HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_MODEL = os.path.join(_HERE, "ui_detect_l1.onnx")

YOLO_SIZE = 640      # longest side after resize
STRIDE = 64          # largest head stride; pad H and W to a multiple of it
PAD_FILL = 114
STRIDES = (8, 16, 32, 64)
REG_MAX = 7

NAMES = [
    "Text", "TextButton", "Button", "Icon", "Image", "EditText", "SearchBar",
    "CheckBox", "RadioButton", "Switch", "Slider", "ProgressBar", "Spinner",
    "Chip", "Tab", "TabBar", "Toolbar", "ListItem", "Dialog",
]

# Classes that carry readable text: 'type' == 'text', OCR reads them.
# Confirm against how ui_detect_lite uses 'type' today.
TEXT_CLASSES = frozenset(["Text", "TextButton", "EditText", "SearchBar", "Chip", "Tab", "Spinner"])
# Containers: never take an OCR label themselves (replaces the old
# ">50% of screen" size heuristic with a class rule).
CONTAINER_CLASSES = frozenset(["Dialog", "ListItem", "TabBar", "Toolbar"])


def letterbox(img, size=YOLO_SIZE, stride=STRIDE, fill=PAD_FILL):
    """Resize longest side to ``size``, pad bottom/right to a multiple of
    ``stride``. Top-left anchored, so the inverse is a single divide.

    Returns (padded HxWx3 uint8, scale).
    """
    h, w = img.shape[:2]
    scale = size / max(h, w)
    nh, nw = max(1, round(h * scale)), max(1, round(w * scale))
    if (nh, nw) != (h, w):
        img = cv2.resize(img, (nw, nh), interpolation=cv2.INTER_LINEAR)
    ph = -(-nh // stride) * stride
    pw = -(-nw // stride) * stride
    out = np.full((ph, pw, 3), fill, dtype=np.uint8)
    out[:nh, :nw] = img
    return out, scale


def _center_priors(h, w):
    """(N, 3) array of [cx, cy, stride] in head output order (NanoDet-Plus:
    level by level, row-major, centers at integer multiples of the stride)."""
    out = []
    for s in STRIDES:
        fh, fw = h // s, w // s
        ys, xs = np.mgrid[0:fh, 0:fw]
        out.append(np.stack([xs.ravel() * s, ys.ravel() * s,
                             np.full(fh * fw, s)], axis=1))
    return np.concatenate(out, 0).astype(np.float32)


def nms(boxes, scores, iou_thr):
    """Greedy NMS. boxes (N,4) xyxy, scores (N,) -> kept indices, score desc."""
    order = np.argsort(-scores, kind="stable")
    x1, y1, x2, y2 = boxes.T
    area = np.clip(x2 - x1, 0, None) * np.clip(y2 - y1, 0, None)
    keep = []
    while order.size:
        i = order[0]
        keep.append(i)
        rest = order[1:]
        iw = np.clip(np.minimum(x2[i], x2[rest]) - np.maximum(x1[i], x1[rest]), 0, None)
        ih = np.clip(np.minimum(y2[i], y2[rest]) - np.maximum(y1[i], y1[rest]), 0, None)
        inter = iw * ih
        iou = inter / np.maximum(area[i] + area[rest] - inter, 1e-9)
        order = rest[iou <= iou_thr]
    return np.asarray(keep, dtype=np.int64)


def postprocess_raw(raw, in_h, in_w, conf=0.25, iou=0.6, max_det=300):
    """Exact post-processing for a raw NanoDet-Plus head output.

    raw: (N, C + 4*(REG_MAX+1)), class scores already sigmoid-ed.
    Single label per anchor (argmax), class-aware NMS.
    Returns (K, 6) [x1, y1, x2, y2, conf, cls] in letterboxed-input pixels.
    """
    nc = raw.shape[1] - 4 * (REG_MAX + 1)
    cls_scores, reg = raw[:, :nc], raw[:, nc:]
    pri = _center_priors(in_h, in_w)
    reg = reg.reshape(-1, 4, REG_MAX + 1)
    reg = np.exp(reg - reg.max(-1, keepdims=True))
    reg /= reg.sum(-1, keepdims=True)
    dist = (reg @ np.arange(REG_MAX + 1, dtype=np.float32)) * pri[:, 2:3]
    boxes = np.stack([pri[:, 0] - dist[:, 0], pri[:, 1] - dist[:, 1],
                      pri[:, 0] + dist[:, 2], pri[:, 1] + dist[:, 3]], 1)
    boxes = np.clip(boxes, 0, [in_w, in_h, in_w, in_h])
    cls = cls_scores.argmax(1)
    score = cls_scores[np.arange(len(cls)), cls]
    m = score > conf
    boxes, score, cls = boxes[m], score[m], cls[m]
    # class-aware NMS via per-class coordinate offset
    off = cls[:, None].astype(np.float32) * 4096.0
    keep = nms(boxes + off, score, iou)[:max_det]
    return np.concatenate([boxes[keep], score[keep, None],
                           cls[keep, None].astype(np.float32)], 1)


class L1Detector:
    def __init__(self, model_path=DEFAULT_MODEL, threads=4):
        so = ort.SessionOptions()
        # S918 is 1+4+3 big.LITTLE; letting ORT spread onto the A510 little
        # cores makes stragglers. 4 is a starting point — measure 2/4/6.
        so.intra_op_num_threads = threads
        so.inter_op_num_threads = 1
        so.execution_mode = ort.ExecutionMode.ORT_SEQUENTIAL
        so.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_ALL
        self.sess = ort.InferenceSession(model_path, so,
                                         providers=["CPUExecutionProvider"])
        self.inputs = {i.name for i in self.sess.get_inputs()}
        self.output = self.sess.get_outputs()[0].name
        self.embedded_nms = "conf_floor" in self.inputs
        meta = self.sess.get_modelmeta().custom_metadata_map
        self.names = json.loads(meta["names"]) if "names" in meta else NAMES
        if self.names != NAMES:
            raise ValueError("model class list != runtime NAMES: %r" % self.names)

    def raw(self, img_bgr, conf=0.25, iou=0.6, max_det=300, size=YOLO_SIZE):
        """(K, 6) float32 [x1, y1, x2, y2, conf, cls] in screen pixels."""
        h0, w0 = img_bgr.shape[:2]
        lb, scale = letterbox(img_bgr, size)
        x = np.ascontiguousarray(lb.transpose(2, 0, 1)[None], dtype=np.float32)
        feeds = {"images": x}
        if self.embedded_nms:
            feeds["conf_floor"] = np.array([conf], np.float32)
            feeds["iou_thr"] = np.array([iou], np.float32)
            feeds["max_det"] = np.array([max_det], np.int64)
        out = self.sess.run([self.output], feeds)[0]
        if self.embedded_nms:
            dets = out.reshape(-1, 6)
        else:
            dets = postprocess_raw(out[0], lb.shape[0], lb.shape[1], conf, iou, max_det)
        dets = dets.astype(np.float32)  # copy; float32 on both paths
        dets[:, :4] /= scale
        dets[:, [0, 2]] = dets[:, [0, 2]].clip(0, w0)
        dets[:, [1, 3]] = dets[:, [1, 3]].clip(0, h0)
        return dets

    def __call__(self, img_bgr, conf=0.25, iou=0.6, max_det=300, size=YOLO_SIZE):
        out = []
        for x1, y1, x2, y2, c, k in self.raw(img_bgr, conf, iou, max_det, size):
            name = self.names[int(k)]
            out.append({
                "bbox": [int(round(x1)), int(round(y1)), int(round(x2)), int(round(y2))],
                "type": "text" if name in TEXT_CLASSES else "icon",
                "label": None,
                "cls": name,
                "confidence": float(c),
            })
        return out


_DET = None


def _yolo(img_bgr, conf=0.25, size=YOLO_SIZE):
    """Drop-in for the incumbent ``_yolo``: lazy singleton, §2 schema."""
    global _DET
    if _DET is None:
        _DET = L1Detector()
    return _DET(img_bgr, conf=conf, size=size)


if __name__ == "__main__":
    # device smoke test: python ui_detect_l1.py model.onnx screenshot.png [conf]
    import sys
    import time

    det = L1Detector(sys.argv[1])
    img = cv2.imread(sys.argv[2])
    conf = float(sys.argv[3]) if len(sys.argv) > 3 else 0.25
    det(img, conf=conf)  # warm-up
    t0 = time.perf_counter()
    out = det(img, conf=conf)
    print("%d boxes, %.1f ms incl. letterbox + post" % (len(out), (time.perf_counter() - t0) * 1e3))
    for d in out[:20]:
        print(d)
