"""Decide what, if anything, goes to the cloud VLM, and make it small.

Device-safe: numpy + cv2. Works on L1Detector output (the §2 schema, with
'label' filled by OCR where available).

Cheapest first:
    RECAPTURE  screen mid-transition: re-grab, don't spend a call
    LOCAL      answer from detections (counts, presence, label lookup)
    TEXT_LLM   send digest() — text only, no image
    VLM_CROP   send crop_for() of the relevant boxes, downscaled, with marks
    VLM_FULL   send the whole screen, downscaled, with marks
    BLOCK      sensitive screen: nothing leaves the device
Set-of-marks: the VLM answers with a mark id, coordinates come from the
detector, so the "no coords from the VLM" rule holds by construction.
"""
import json
import time

import cv2
import numpy as np

from ui_detect_l1 import NAMES

RECAPTURE, LOCAL, TEXT_LLM, VLM_CROP, VLM_FULL, BLOCK = (
    "recapture", "local", "text_llm", "vlm_crop", "vlm_full", "block")
KINDS = ("count", "presence", "find_text", "semantic", "visual")
# L1 containers + the incumbent's, so route() also works in front of ui_detect_v1
CONTAINERS = frozenset(["Dialog", "ListItem", "TabBar", "Toolbar", "Modal", "Drawer",
                        "BackgroundImage", "Card", "Bottom_Navigation", "Multi_Tab", "UpperTaskBar"])
_IDX = {n: i for i, n in enumerate(NAMES)}
STATUS_BAR_FRAC = 0.035  # top band excluded from hashing: the clock ticks


def dhash(img, size=8):
    """64-bit difference hash, status bar excluded."""
    top = int(img.shape[0] * STATUS_BAR_FRAC)
    g = cv2.cvtColor(img[top:], cv2.COLOR_BGR2GRAY)
    s = cv2.resize(g, (size + 1, size), interpolation=cv2.INTER_AREA)
    bits = (s[:, 1:] > s[:, :-1]).ravel()
    return int(np.packbits(bits).view(">u8")[0])


def hamming(a, b):
    return bin(a ^ b).count("1")


def is_stable(img_a, img_b, max_dist=2):
    """Two grabs ~150 ms apart; differing hashes = animation/transition."""
    return hamming(dhash(img_a), dhash(img_b)) <= max_dist


def reading_order(dets):
    """Ids in reading order (48 px rows, then left to right)."""
    row = lambda d: (d["bbox"][1] // 48, d["bbox"][0])  # noqa: E731
    return {i + 1: d for i, d in enumerate(sorted(dets, key=row))}


def digest(dets, wh, max_items=60, max_label=40):
    """Compact text layout. One line per element:
    'id cls x,y,w,h "label"' with x,y,w,h in integer percent of the screen.
    Returns (text, {id: det})."""
    w, h = wh
    marks = reading_order(dets)
    # keep containers and labelled/interactive items first if over budget
    pri = sorted(marks, key=lambda i: (marks[i]["cls"] not in CONTAINERS and not marks[i].get("label"), i))
    keep = sorted(pri[:max_items])
    lines = ["id cls x,y,w,h(%%) label | screen %dx%d" % (w, h)]
    for i in keep:
        d = marks[i]
        x1, y1, x2, y2 = d["bbox"]
        s = "%d %s %d,%d,%d,%d" % (i, d["cls"], 100 * x1 // w, 100 * y1 // h,
                                   max(1, 100 * (x2 - x1) // w), max(1, 100 * (y2 - y1) // h))
        if d.get("label"):
            s += ' "%s"' % d["label"].replace('"', "'")[:max_label]
        lines.append(s)
    if len(marks) > len(keep):
        lines.append("(+%d unlabelled items omitted)" % (len(marks) - len(keep)))
    return "\n".join(lines), {i: marks[i] for i in keep}


def downscale(img, max_side):
    s = max_side / max(img.shape[:2])
    if s >= 1:
        return img, 1.0
    return cv2.resize(img, (round(img.shape[1] * s), round(img.shape[0] * s)),
                      interpolation=cv2.INTER_AREA), s


def set_of_marks(img, marks):
    """Copy of img with each box outlined and numbered. Draw before downscaling."""
    out = img.copy()
    t = max(2, img.shape[1] // 400)
    fs = img.shape[1] / 1100
    for i, d in marks.items():
        x1, y1, x2, y2 = d["bbox"]
        cv2.rectangle(out, (x1, y1), (x2, y2), (0, 0, 255), t)
        txt = str(i)
        (tw, th), _ = cv2.getTextSize(txt, cv2.FONT_HERSHEY_SIMPLEX, fs, t)
        cv2.rectangle(out, (x1, y1), (x1 + tw + 4, y1 + th + 6), (0, 0, 255), -1)
        cv2.putText(out, txt, (x1 + 2, y1 + th + 2), cv2.FONT_HERSHEY_SIMPLEX, fs, (255, 255, 255), t)
    return out


def crop_for(img, dets, pad=24, max_side=768):
    """Crop to the union of dets (e.g. the Dialog, or the boxes a question is
    about), downscale. Returns (crop, (x0, y0, scale)) to map back if needed."""
    b = np.array([d["bbox"] for d in dets])
    x0, y0 = max(0, b[:, 0].min() - pad), max(0, b[:, 1].min() - pad)
    x1 = min(img.shape[1], b[:, 2].max() + pad)
    y1 = min(img.shape[0], b[:, 3].max() + pad)
    crop, s = downscale(img[y0:y1, x0:x1], max_side)
    return crop, (int(x0), int(y0), s)


def features(dets, wh, kind):
    """Router features: what the digest can and can't express."""
    w, h = wh
    area = float(w * h)
    leaves = [d for d in dets if d["cls"] not in CONTAINERS]
    hist = np.zeros(len(NAMES))
    for d in dets:
        if d["cls"] in _IDX:  # other detectors' classes: not in the histogram
            hist[_IDX[d["cls"]]] += 1
    a = lambda ds: sum((d["bbox"][2] - d["bbox"][0]) * (d["bbox"][3] - d["bbox"][1]) for d in ds) / area  # noqa: E731
    labelled = [d for d in leaves if d.get("label")]
    f = [len(leaves) / 50.0,
         len(labelled) / max(1, len(leaves)),                       # text coverage
         a([d for d in leaves if d["cls"] == "Image"]),             # visual content share
         a(leaves),                                                 # detector coverage
         float(any(d["cls"] == "Dialog" for d in dets))]
    return np.concatenate([np.log1p(hist), f, np.eye(len(KINDS))[KINDS.index(kind)]]).astype(np.float32)


class Router:
    """Logistic regression: P(the text-only tier gives the accepted answer).
    Train from shadow logs (run TEXT_LLM alongside each VLM call, label = they
    agreed). numpy fit, weights as JSON — trains and runs on the device."""

    def __init__(self, w=None, b=0.0):
        self.w, self.b = (None if w is None else np.asarray(w, np.float32)), float(b)

    def fit(self, X, y, l2=1e-2, lr=0.5, epochs=500):
        X, y = np.asarray(X, np.float32), np.asarray(y, np.float32)
        self.w, self.b = np.zeros(X.shape[1], np.float32), 0.0
        for _ in range(epochs):
            p = self.predict_proba(X)
            g = p - y
            self.w -= lr * (X.T @ g / len(y) + l2 * self.w)
            self.b -= lr * float(g.mean())
        return self

    def predict_proba(self, X):
        return 1 / (1 + np.exp(-(np.asarray(X, np.float32) @ self.w + self.b)))

    def save(self, path):
        json.dump({"w": self.w.tolist(), "b": self.b}, open(path, "w"))

    @classmethod
    def load(cls, path):
        d = json.load(open(path))
        return cls(d["w"], d["b"])


def route(kind, dets, wh, sensitive=False, stable=True, router=None, p_text=0.8):
    """Pick the cheapest tier likely to answer. kind is one of KINDS."""
    if not stable:
        return RECAPTURE
    if kind in ("count", "presence"):
        return LOCAL
    leaves = [d for d in dets if d["cls"] not in CONTAINERS]
    if kind == "find_text" and any(d.get("label") for d in leaves):
        return LOCAL
    if sensitive:
        return BLOCK  # local tiers already handled above; nothing goes out
    if len(leaves) < 3:
        return VLM_FULL  # self-drawn / unknown UI: the digest would be empty
    if kind == "visual":
        return VLM_CROP
    if router is not None and router.w is not None:
        p = float(router.predict_proba(features(dets, wh, kind)[None])[0])
        return TEXT_LLM if p >= p_text else VLM_CROP
    labelled = sum(1 for d in leaves if d.get("label")) / len(leaves)
    return TEXT_LLM if labelled >= 0.5 else VLM_CROP


class AnswerCache:
    """Reuse answers for an unchanged screen: (package, question) keyed,
    matched by dHash within max_dist bits, expiring after ttl seconds."""

    def __init__(self, max_dist=4, ttl=300.0, max_entries=256):
        self.max_dist, self.ttl, self.max_entries = max_dist, ttl, max_entries
        self.entries = []  # (t, package, question, hash, answer)

    def get(self, package, question, h, now=None):
        now = time.time() if now is None else now
        self.entries = [e for e in self.entries if now - e[0] < self.ttl]
        for t, p, q, eh, ans in reversed(self.entries):
            if p == package and q == question and hamming(eh, h) <= self.max_dist:
                return ans
        return None

    def put(self, package, question, h, answer, now=None):
        self.entries.append((time.time() if now is None else now, package, question, h, answer))
        del self.entries[:-self.max_entries]
