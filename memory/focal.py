"""focal — the agent's eye tracker: a gaze circle + 3×3 high-res cell classifier, fully on-device.

Where it sits (cheapest first; one frame can be shared by every tier, like peek(img=frame)):
  periphery  whole screen, low-res    "where to look"       screen_peek.peek_fast / focal.periphery()
  fovea      gaze circle, native res  "what is there"       focal.look()  -> 3×3 cells, local classifier
  read       OCR inside circle only   "what does it say"    focal.read()  -> droid.ocr_text / screen_peek.peek(roi=rect)
  ask        VLM on the circle crop   "what does it mean"   focal.ask()   -> ask_vision(crop)
The circle is (x, y, r) in physical screen px; its bounding square is cut into 3×3 cells
  nw n ne / w c e / sw s se
and each cell is classified at native resolution. Per vision_sop: shrinking AREA is the speed-up,
shrinking RESOLUTION breaks OCR — the fovea does the first and never the second.

Usage
  import focal
  fx = focal.look()                  # capture + classify at the gaze (default: screen centre, r = min(W,H)/6)
  print(fx)                          # header + 3 rows, ~60-100 tokens
  focal.look(at=el)                  # el = droid.look()/peek element: el fills the centre cell, ring = context
  focal.look(at=(x, y)) / at=(x, y, r) / at=(x1, y1, x2, y2)
  focal.look(at='ne')                # move onto a cell of the last grid (fovea: r/3 drill; periphery: saccade)
  focal.back(); focal.reset()        # previous fixation / screen centre
  focal.periphery()                  # 3×3 over the whole screen, low-res pixel stats: pick where to look
  focal.read(frame=fx.frame)         # OCR inside the circle (reuse the frame = no extra shot); with the
                                     #   detect backend the cells already carry ui_detect's OCR text: don't re-OCR
  focal.read(want=['搜索'])           # fuzzy match inside the circle via screen_peek.peek
  focal.ask('这个图标是什么?')          # VLM on the crop only; context=True adds a thumbnail with the circle
  focal.tap('ne')                    # tap a cell centre, bound to the fixation's frame (screen=); refuses
                                     #   fixations older than TAP_MAX_AGE s (e.g. from an earlier turn)
  focal.render()                     # PNG of circle + grid + scanpath -> temp/focal_view.png (eye-tracker view)
  focal.use('auto'|'onnx'|'detect'|'pixel'|fn)   # cell classifier; run focal.selfcheck() on device first

Reading a cell
  'ne Icon .82 "设置"'  model class (ui_detect_lite.NAMES) + score (+ OCR text from the detect backend)
  'ne ~glyph'           pixel heuristic, no score: blank / glyph (text or mono icon) / graphic / photo / mixed
  'ne ·'                blank
  Header '[pixel<-detect: TypeError]' = backend failed and fell back; never read that as a detection.

Backends ('auto' picks the first usable)
  onnx    dedicated tile classifier, models/focal_cls_v1/model.onnx (or $FOCAL_MODEL); classes and
          preprocessing live in the model metadata (built by focal_train.py). If onnxruntime is not
          importable in this Python, pass runner=fn(nchw_float32) -> logits (e.g. the APK bus).
  detect  droid.ui_detect on the circle crop; YOLO resizes the crop up, so small targets get bigger.
          A cell takes the box that best fits it (cover of cell + share of box inside cell).
  pixel   numpy only, ~1 ms; always computed for salience and as the fallback label.

Rules
  * Coordinates belong to the frame they came from. If the screen size/rotation changes, look() resets
    the gaze (header says 'gaze reset') instead of rescaling; tap() always passes the fixation's screen=.
  * Never calls dump(): safe for SENSITIVE_APPS (screenshots + OCR + YOLO + coordinate taps only).
  * A live on-phone ring needs an APK overlay: hook it with focal.on_move(fn(x, y, r)). That overlay
    must stay out of screenshots, or it pollutes every cell it crosses.
"""
import json
import math
import os
import re
import time
from dataclasses import dataclass, field
from types import SimpleNamespace

import numpy as np

CELLS = ('nw', 'n', 'ne', 'w', 'c', 'e', 'sw', 's', 'se')
R_MIN = 24          # smallest gaze radius: cells stay >= 16 px
TRAIL = 16          # fixations kept for back() and the rendered scanpath
FIT_MIN = 0.15      # detect: a box must cover >= 15% of a cell, or have its centre in it
MIN_CONF = 0.4      # onnx: below this the cell keeps the pixel label
ASK_MIN_SIDE = 256  # ask(): upscale tiny crops so the VLM can see them (~88 tok)
TAP_MAX_AGE = 10    # tap(): seconds a fixation stays tappable (turns take >15 s, screens move)
MODEL_REL = os.path.join('models', 'focal_cls_v1', 'model.onnx')
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')  # agent root: memory/ models/ temp/

S = SimpleNamespace(gaze=None, wh=None, rot=None, trail=[], last=None, hooks=[],
                    backend='auto', opts={}, onnx=None, onnx_err=None, err=None)
_MODS = {}


def _mod(name):
    if name not in _MODS:
        try:
            _MODS[name] = __import__(name)
        except Exception:
            _MODS[name] = None
    return _MODS[name]


def _need(name):
    m = _mod(name)
    if m is None:
        raise ImportError(f'focal needs {name} (on-device module) for this call')
    return m


# ---------------------------------------------------------------- frames

def _retry(fn, n=3, wait=0.3):
    # Only the documented transient (takeScreenshot failed code=3) is retried; a FLAG_SECURE
    # black-frame error must surface immediately.
    for i in range(n):
        try:
            return fn()
        except Exception as e:
            if 'takeScreenshot failed' not in str(e) or i == n - 1:
                raise
            time.sleep(wait * (i + 1))


def capture():
    """Fresh frame {'image': BGR ndarray, 'screen': ...} via droid.capture() (fallback droid.shot())."""
    d = _need('droid')
    if hasattr(d, 'capture'):
        f = _retry(d.capture)
        return f if isinstance(f, dict) else {'image': f, 'screen': None}
    return {'image': _retry(d.shot), 'screen': None}


def _frame(frame):
    if frame is None:
        return capture()
    if isinstance(frame, np.ndarray):
        return {'image': frame, 'screen': None}
    return frame


def _rotation(screen):
    if isinstance(screen, dict):
        for k in ('rotation', 'rot', 'orientation'):
            if k in screen:
                return screen[k]
    return None


def _bind(f):
    """Tie the gaze to this frame's geometry; a size/rotation change resets it (no rescaling)."""
    h, w = f['image'].shape[:2]
    rot = _rotation(f.get('screen'))
    changed = S.wh is not None and (S.wh != (w, h) or (rot is not None and S.rot is not None and rot != S.rot))
    if changed:
        S.gaze, S.last = None, None
        S.trail.clear()
    S.wh = (w, h)
    if rot is not None:
        S.rot = rot
    return ' · gaze reset: screen changed' if changed else ''


# ---------------------------------------------------------------- geometry

def _clamp(x, y, r, w, h):
    r = int(max(R_MIN, min(r, min(w, h) // 2)))
    return int(min(max(x, r), w - r)), int(min(max(y, r), h - r)), r


def _grid_boxes(rect):
    xs = np.linspace(rect[0], rect[2], 4).round().astype(int).tolist()
    ys = np.linspace(rect[1], rect[3], 4).round().astype(int).tolist()
    return [(xs[j], ys[i], xs[j + 1], ys[i + 1]) for i in range(3) for j in range(3)]


def _box(d):
    """(x1, y1, x2, y2) from a detection/element dict or tuple; zero-size box if only a centre is known."""
    if isinstance(d, (tuple, list)):
        return tuple(float(v) for v in d) if len(d) == 4 else (d[0], d[1], d[0], d[1])
    for k in ('box', 'bbox', 'b', 'rect', 'xyxy'):
        v = d.get(k)
        if isinstance(v, str):
            v = [float(n) for n in re.findall(r'-?\d+(?:\.\d+)?', v)]
        if v is not None and len(v) == 4:
            return tuple(float(n) for n in v)
    if all(k in d for k in ('x1', 'y1', 'x2', 'y2')):
        return tuple(float(d[k]) for k in ('x1', 'y1', 'x2', 'y2'))
    if 'x' in d and 'y' in d:
        w, h = float(d.get('w', 0)), float(d.get('h', 0))
        return (d['x'] - w / 2, d['y'] - h / 2, d['x'] + w / 2, d['y'] + h / 2)
    raise ValueError(f'no box/centre in {d!r}')


def _set_gaze(x, y, r, push=True):
    if push and S.gaze is not None:
        S.trail.append(S.gaze)
        del S.trail[:-TRAIL]
    S.gaze = (x, y, r)
    for fn in S.hooks:
        try:
            fn(x, y, r)
        except Exception as e:  # a broken overlay must not break vision
            S.err = e


def _move(at, r, w, h):
    gr = S.gaze[2] if S.gaze else min(w, h) // 6
    if isinstance(at, str):
        if S.last is None:
            raise RuntimeError('no grid to move into yet: call focal.look() or focal.periphery() first')
        b = S.last.cell(at).box
        x, y, gr = (b[0] + b[2]) // 2, (b[1] + b[3]) // 2, min(b[2] - b[0], b[3] - b[1]) // 2
    elif isinstance(at, (tuple, list)) and len(at) in (2, 3):
        x, y = at[0], at[1]
        gr = at[2] if len(at) == 3 else gr
    else:
        x, y, fr = fit(at)
        gr = fr or gr
    _set_gaze(*_clamp(x, y, r or gr, w, h))


def fit(el):
    """Gaze (x, y, r) that puts an element in the centre cell (side 2r/3) and its neighbours in the
    ring; r is None for a centre-only element. Also used by focal_train to cut training tiles."""
    b = _box(el)
    r = 1.5 * max(b[2] - b[0], b[3] - b[1])
    return (b[0] + b[2]) / 2, (b[1] + b[3]) / 2, r or None


def gaze():
    """Current (x, y, r) or None (next look() starts at screen centre)."""
    return S.gaze


def back():
    """Return to the previous fixation."""
    if S.trail:
        _set_gaze(*S.trail.pop(), push=False)
    return S.gaze


def reset():
    """Forget gaze and scanpath; next look() starts at screen centre."""
    S.gaze, S.last = None, None
    S.trail.clear()


def on_move(fn):
    """Register fn(x, y, r), called on every gaze change (e.g. an APK overlay drawing the ring)."""
    S.hooks.append(fn)
    return fn


# ---------------------------------------------------------------- cells

@dataclass
class Cell:
    name: str
    box: tuple
    label: str = 'blank'
    score: float = None     # None = pixel heuristic, not a model claim
    sal: float = 0.0        # 0..1 edge energy, for choosing where to look next
    text: str = ''

    @property
    def xy(self):
        return (self.box[0] + self.box[2]) // 2, (self.box[1] + self.box[3]) // 2

    def __str__(self):
        if self.label == 'blank':
            body = '·'
        elif self.score is None:
            body = '~' + self.label
        else:
            body = f'{self.label} {self.score:.2f}'.replace(' 0.', ' .')
        if self.text:
            body += ' "' + (self.text if len(self.text) <= 10 else self.text[:9] + '…') + '"'
        return f'{self.name} {body}'


@dataclass
class Fixation:
    kind: str               # 'focal' | 'periphery'
    x: int
    y: int
    r: int
    rect: tuple
    cells: list
    backend: str
    ms: int
    note: str = ''
    frame: dict = field(default=None, repr=False)
    t: float = 0.0          # time.time() of the fixation

    def cell(self, name):
        return self.cells[CELLS.index(name)]

    def find(self, label):
        """Cells whose label matches (case-insensitive), best first."""
        hits = [c for c in self.cells if c.label.lower() == label.lower()]
        return sorted(hits, key=lambda c: (c.score or 0, c.sal), reverse=True)

    def best(self):
        """Most salient non-blank cell, or None."""
        live = [c for c in self.cells if c.label != 'blank']
        return max(live, key=lambda c: c.sal) if live else None

    def __str__(self):
        c = self.cells[4].box
        size = f'cell={c[2] - c[0]}x{c[3] - c[1]}'
        if self.kind == 'periphery':
            head = f'periphery {self.rect[2]}x{self.rect[3]} {size}'
        else:
            head = f'focal ({self.x},{self.y}) r={self.r} {size}'
        rows = [' | '.join(str(c) for c in self.cells[i:i + 3]) for i in (0, 3, 6)]
        return '\n'.join([f'{head} [{self.backend} {self.ms}ms]{self.note}'] + rows)


# ---------------------------------------------------------------- classifiers

def _pixel(tile):
    """Coarse label + salience for one BGR tile from pixel statistics alone."""
    t = tile.astype(np.float32)
    b, g, r = t[..., 0], t[..., 1], t[..., 2]
    gray = 0.114 * b + 0.587 * g + 0.299 * r
    gx, gy = np.abs(np.diff(gray, axis=1)), np.abs(np.diff(gray, axis=0))
    sal = float(min(1.0, (gx.mean() + gy.mean()) / 20)) if gray.size > 1 else 0.0
    edge = (np.mean(gx > 24) + np.mean(gy > 24)) / 2 if gx.size and gy.size else 0.0
    if gray.std() < 3 or edge < 0.003:
        return 'blank', sal
    rg, yb = r - g, 0.5 * (r + g) - b
    chroma = math.hypot(rg.std(), yb.std()) + 0.3 * math.hypot(rg.mean(), yb.mean())
    q = (tile >> 5).astype(np.int32)
    ncol = len(np.unique(q[..., 0] * 64 + q[..., 1] * 8 + q[..., 2]))
    if ncol > 64:  # many colours: a photo has few flat pixels, a region of mixed UI has many
        flat = (np.mean(gx < 2) + np.mean(gy < 2)) / 2
        return ('photo' if flat < 0.6 else 'mixed'), sal
    return ('glyph' if chroma < 12 else 'graphic'), sal


def _canon(name):
    ul = _mod('ui_detect_lite')
    names = getattr(ul, 'NAMES', None)
    if isinstance(name, (int, np.integer)) and names:
        name = names[int(name)]
    return getattr(ul, 'MODEL_TO_CANON', {}).get(name, name)


def _dets(raw):
    """Normalise detector output to [{'cls', 'box', 'conf', 'text'}]; unparseable items are skipped."""
    if isinstance(raw, dict):
        raw = raw.get('items') or raw.get('dets') or raw.get('boxes') or []
    out = []
    for d in raw or []:
        if not isinstance(d, dict):
            continue
        try:
            box = _box(d)
        except ValueError:
            continue
        cls = next((d[k] for k in ('cls', 'class', 'name') if d.get(k) is not None), '?')
        conf = next((d[k] for k in ('conf', 'score', 'p') if d.get(k) is not None), 1.0)
        text = next((d[k] for k in ('label', 'text', 't') if d.get(k)), '')
        out.append({'cls': _canon(cls), 'box': box, 'conf': float(conf), 'text': str(text)})
    return out


def assign(boxes, dets, fit_min=FIT_MIN):
    """Per cell box, the detection that best fits it -> (cls, conf, text) or None.
    fit = share of the cell it covers + share of itself inside the cell, so a small icon
    inside a cell beats a page-sized container that merely covers it. Also used to label
    training tiles (focal_train.py), so the detect backend and the onnx model agree."""
    out = []
    for c in boxes:
        area = max(1, (c[2] - c[0]) * (c[3] - c[1]))
        best, key = None, None
        for d in dets:
            b = d['box']
            inter = max(0, min(c[2], b[2]) - max(c[0], b[0])) * max(0, min(c[3], b[3]) - max(c[1], b[1]))
            mx, my = (b[0] + b[2]) / 2, (b[1] + b[3]) / 2
            inside = c[0] <= mx < c[2] and c[1] <= my < c[3]
            cover = inter / area
            if cover < fit_min and not inside:
                continue
            own = inter / max(1, (b[2] - b[0]) * (b[3] - b[1])) if b[2] > b[0] and b[3] > b[1] else float(inside)
            k = (cover + own, d['conf'])
            if key is None or k > key:
                best, key = d, k
        out.append((best['cls'], best['conf'], best['text']) if best else None)
    return out


def _cls_pixel(crop, boxes, tiles):
    return [None] * len(tiles)


def _cls_detect(crop, boxes, tiles):
    raw = _need('droid').ui_detect(np.ascontiguousarray(crop))
    return assign(boxes, _dets(raw))


def _cls_onnx(crop, boxes, tiles):
    m = _onnx()
    return [(lab, p, '') if p >= m.min_conf else None for lab, p in m(tiles)]


def _resize(img, w, h):
    cv2 = _mod('cv2')
    if cv2 is not None:
        return cv2.resize(img, (w, h), interpolation=cv2.INTER_AREA if w < img.shape[1] else cv2.INTER_LINEAR)
    H, W = img.shape[:2]
    ys = np.clip((np.arange(h) + 0.5) * H / h - 0.5, 0, H - 1)
    xs = np.clip((np.arange(w) + 0.5) * W / w - 0.5, 0, W - 1)
    y0, x0 = ys.astype(int), xs.astype(int)
    y1, x1 = np.minimum(y0 + 1, H - 1), np.minimum(x0 + 1, W - 1)
    wy, wx = (ys - y0)[:, None, None], (xs - x0)[None, :, None]
    f = img.astype(np.float32)
    top = f[y0][:, x0] * (1 - wx) + f[y0][:, x1] * wx
    bot = f[y1][:, x0] * (1 - wx) + f[y1][:, x1] * wx
    return (top * (1 - wy) + bot * wy).round().astype(img.dtype)


class _Onnx:
    """Tile classifier. Metadata keys read from the model: classes, size, mean, std, rgb (JSON)."""

    def __init__(self, path=None, runner=None, classes=None, size=None, mean=None, std=None,
                 rgb=None, min_conf=MIN_CONF):
        self.path, meta, self.batch = path or _find_model(), {}, True
        if runner is None:
            if not self.path:
                raise FileNotFoundError(f'no focal model: set $FOCAL_MODEL or add {MODEL_REL}')
            ort = _mod('onnxruntime')
            if ort is None:
                raise ImportError('onnxruntime not importable here: use(\'onnx\', runner=fn) with the APK bus')
            sess = ort.InferenceSession(self.path, providers=['CPUExecutionProvider'])
            inp = sess.get_inputs()[0]
            meta = sess.get_modelmeta().custom_metadata_map or {}
            if size is None and isinstance(inp.shape[2], int):
                size = inp.shape[2]
            self.batch = not (isinstance(inp.shape[0], int) and inp.shape[0] == 1)
            runner = lambda x, s=sess, n=inp.name: s.run(None, {n: x})[0]  # noqa: E731

        def pick(v, key, default):
            return v if v is not None else (json.loads(meta[key]) if key in meta else default)
        self.run, self.min_conf = runner, min_conf
        self.size = int(pick(size, 'size', 96))
        self.mean = np.float32(pick(mean, 'mean', [0.485, 0.456, 0.406]))
        self.std = np.float32(pick(std, 'std', [0.229, 0.224, 0.225]))
        self.rgb = bool(pick(rgb, 'rgb', True))
        self.classes = pick(classes, 'classes', None) or _classes_txt(self.path) \
            or list(getattr(_mod('ui_detect_lite'), 'NAMES', []))
        if not self.classes:
            raise ValueError('focal model has no class list (metadata "classes" or classes.txt)')

    def _prep(self, t):
        t = _resize(t, self.size, self.size)
        if self.rgb:
            t = t[..., ::-1]
        return ((t.astype(np.float32) / 255 - self.mean) / self.std).transpose(2, 0, 1)

    def __call__(self, tiles):
        x = np.ascontiguousarray(np.stack([self._prep(t) for t in tiles]), dtype=np.float32)
        y = self.run(x) if self.batch else np.concatenate([self.run(x[i:i + 1]) for i in range(len(x))])
        y = np.asarray(y, np.float32).reshape(len(tiles), -1)
        if not (np.all(y >= 0) and np.allclose(y.sum(1), 1, atol=1e-3)):
            y = np.exp(y - y.max(1, keepdims=True))
            y /= y.sum(1, keepdims=True)
        k = y.argmax(1)
        return [(self.classes[i] if i < len(self.classes) else str(i), float(y[j, i])) for j, i in enumerate(k)]


def _find_model():
    for p in (os.environ.get('FOCAL_MODEL'), os.path.join(ROOT, MODEL_REL), MODEL_REL):
        if p and os.path.isfile(p):
            return os.path.normpath(p)
    return None


def _classes_txt(path):
    p = path and os.path.join(os.path.dirname(path), 'classes.txt')
    if p and os.path.isfile(p):
        with open(p, encoding='utf-8') as fh:
            return [ln.strip() for ln in fh if ln.strip()]
    return None


def _onnx():
    if S.onnx is None:
        S.onnx = _Onnx(**S.opts)
    return S.onnx


def use(backend='auto', **opts):
    """Choose the cell classifier: 'auto' | 'onnx' | 'detect' | 'pixel' | fn(crop, boxes, tiles).
    onnx opts: path, runner, classes, size, mean, std, rgb, min_conf."""
    S.backend, S.opts, S.onnx, S.onnx_err = backend, opts, None, None


def _resolve(name):
    if callable(name):
        return getattr(name, '__name__', 'custom'), name
    if name == 'auto':
        name = 'pixel'
        if S.onnx_err is None:
            try:
                _onnx()
                name = 'onnx'
            except Exception as e:
                S.onnx_err = e
        if name == 'pixel' and hasattr(_mod('droid'), 'ui_detect'):
            name = 'detect'
    return name, {'onnx': _cls_onnx, 'detect': _cls_detect, 'pixel': _cls_pixel}[name]


def _grid(img, rect, backend, stride=1):
    t0 = time.perf_counter()
    x1, y1, x2, y2 = rect
    crop = img[y1:y2, x1:x2]
    local = _grid_boxes((0, 0, x2 - x1, y2 - y1))
    tiles = [crop[b[1]:b[3]:stride, b[0]:b[2]:stride] for b in local]
    name, fn = _resolve(backend or S.backend)
    try:
        res = fn(crop, local, tiles)
    except Exception as e:
        S.err, res, name = e, [None] * 9, f'pixel<-{name}: {type(e).__name__}'
    cells = []
    for nm, b, t, r in zip(CELLS, local, tiles, res):
        lab, sal = _pixel(t)
        c = Cell(nm, (b[0] + x1, b[1] + y1, b[2] + x1, b[3] + y1), lab, None, round(sal, 2))
        if r is not None:
            c.label, c.score, c.text = r[0], round(float(r[1]), 2), r[2] or ''
        cells.append(c)
    return cells, name, int((time.perf_counter() - t0) * 1000)


# ---------------------------------------------------------------- tiers

def look(at=None, r=None, frame=None, backend=None):
    """Fixate and classify the 3×3 cells inside the gaze circle. Returns a Fixation (print it)."""
    f = _frame(frame)
    note = _bind(f)
    h, w = f['image'].shape[:2]
    if at is not None or r is not None:
        _move(at if at is not None else S.gaze or (w // 2, h // 2), r, w, h)
    elif S.gaze is None:
        _set_gaze(*_clamp(w // 2, h // 2, min(w, h) // 6, w, h), push=False)
    x, y, rr = _clamp(*S.gaze, w, h)
    rect = (x - rr, y - rr, x + rr, y + rr)
    cells, name, ms = _grid(f['image'], rect, backend)
    S.last = Fixation('focal', x, y, rr, rect, cells, name, ms, note, f, time.time())
    return S.last


def periphery(frame=None, backend='pixel', stride=4):
    """3×3 over the whole screen from subsampled pixels (cheap): choose a cell, then look(at='ne')."""
    f = _frame(frame)
    note = _bind(f)
    h, w = f['image'].shape[:2]
    cells, name, ms = _grid(f['image'], (0, 0, w, h), backend, stride)
    S.last = Fixation('periphery', w // 2, h // 2, max(w, h) // 2, (0, 0, w, h), cells, name, ms, note, f, time.time())
    return S.last


def _gaze_rect(f):
    if _bind(f):  # unlike look(), reading/asking must not silently move to a re-centred gaze
        raise RuntimeError('screen size/rotation changed since the gaze was set: call focal.look() again')
    h, w = f['image'].shape[:2]
    x, y, r = _clamp(*(S.gaze or (w // 2, h // 2, min(w, h) // 6)), w, h)
    return x - r, y - r, x + r, y + r


def read(want=None, frame=None, **kw):
    """OCR inside the gaze circle. want=[...] -> screen_peek.peek(roi=rect, img=frame) fuzzy match;
    otherwise droid.ocr_text(crop). frame=fx.frame reuses a fixation's frame (no new shot)."""
    f = _frame(frame)
    x1, y1, x2, y2 = rect = _gaze_rect(f)
    if want:
        return _need('screen_peek').peek(want=list(want), roi=rect, img=f['image'], **kw)
    return _need('droid').ocr_text(np.ascontiguousarray(f['image'][y1:y2, x1:x2]))


def _ring(img, x, y, r, color, t=3):
    h, w = img.shape[:2]
    ya, yb, xa, xb = max(0, y - r - t), min(h, y + r + t + 1), max(0, x - r - t), min(w, x + r + t + 1)
    yy, xx = np.ogrid[ya:yb, xa:xb]
    d = np.sqrt((xx - x) ** 2 + (yy - y) ** 2)
    img[ya:yb, xa:xb][np.abs(d - r) <= t / 2] = color


def _composite(img, rect):
    x1, y1, x2, y2 = rect
    crop = img[y1:y2, x1:x2]
    side = crop.shape[0]
    h, w = img.shape[:2]
    k = side / h
    thumb = _resize(img, max(1, round(w * k)), side).copy()
    _ring(thumb, round((x1 + x2) / 2 * k), round((y1 + y2) / 2 * k), max(3, round((x2 - x1) / 2 * k)),
          (0, 0, 255), 2)
    gap = np.full((side, 8, 3), 255, img.dtype)
    return np.concatenate([crop, gap, thumb], axis=1)


def ask(question, frame=None, context=False, **kw):
    """ask_vision on the gaze crop only (~w*h/750 tok). context=True appends a full-screen thumbnail
    with the circle marked. Returns ask_vision's str ('Error: ...' on failure, not raised)."""
    f = _frame(frame)
    rect = _gaze_rect(f)
    img = f['image']
    if context:
        img = _composite(img, rect)
        question = '左: 焦点区原分辨率; 右: 全屏缩略图, 红圈=焦点位置。' + question
    else:
        img = img[rect[1]:rect[3], rect[0]:rect[2]]
    if min(img.shape[:2]) < ASK_MIN_SIDE:
        k = ASK_MIN_SIDE / min(img.shape[:2])
        img = _resize(img, round(img.shape[1] * k), round(img.shape[0] * k))
    d = _mod('droid')
    fn = getattr(d, 'ask_vision', None) or _need('vision_api').ask_vision
    return fn(np.ascontiguousarray(img), question, **kw)


def est_tokens(w, h):
    """Image-token estimate after ask_vision's 1.44 MP cap (vision_sop: 720×1544 ≈ 1482 tok)."""
    s = min(1.0, math.sqrt(1.44e6 / (w * h)))
    return math.ceil(w * s * h * s / 750)


def tap(cell='c', fx=None):
    """Tap a cell centre of the last (or given) fixation, bound to that fixation's frame."""
    fx = fx or S.last
    if fx is None:
        raise RuntimeError('no fixation yet: call focal.look() first')
    age = time.time() - fx.t
    if age > TAP_MAX_AGE:
        raise RuntimeError(f'fixation is {age:.0f}s old: focal.look() again before tapping')
    x, y = fx.cell(cell).xy
    d = _need('droid')
    screen = (fx.frame or {}).get('screen')
    return d.tap(x, y, screen=screen) if screen is not None else d.tap(x, y)


def render(path=None, fx=None):
    """Draw circle + 3×3 grid + scanpath on the fixation's frame; save PNG; return its path."""
    fx = fx or S.last
    if fx is None:
        raise RuntimeError('nothing to render: call focal.look() first')
    img = fx.frame['image'].copy()
    for c in fx.cells:
        x1, y1, x2, y2 = c.box
        img[y1:y2, [x1, max(x1, x2 - 1)]] = (0, 200, 255)
        img[[y1, max(y1, y2 - 1)], x1:x2] = (0, 200, 255)
    pts = [g[:2] for g in S.trail] + [(fx.x, fx.y)]
    for (ax, ay), (bx, by) in zip(pts, pts[1:]):
        n = int(max(abs(bx - ax), abs(by - ay))) + 1
        xs = np.clip(np.linspace(ax, bx, n).round().astype(int), 0, img.shape[1] - 1)
        ys = np.clip(np.linspace(ay, by, n).round().astype(int), 0, img.shape[0] - 1)
        img[ys, xs] = (255, 128, 0)
    for gx, gy, gr in S.trail:
        _ring(img, gx, gy, max(6, gr // 8), (255, 128, 0), 2)
    if fx.kind == 'focal':
        _ring(img, fx.x, fx.y, fx.r, (0, 0, 255), max(3, fx.r // 40))
        _ring(img, fx.x, fx.y, 3, (0, 0, 255), 4)
    if path is None:  # vision rule: never the project root; agent temp/, fixed name, overwritten
        os.makedirs(os.path.join(ROOT, 'temp'), exist_ok=True)
        path = os.path.normpath(os.path.join(ROOT, 'temp', 'focal_view.png'))
    cv2 = _mod('cv2')
    if cv2 is not None:
        cv2.imwrite(path, img)
    else:
        from PIL import Image
        Image.fromarray(np.ascontiguousarray(img[..., ::-1])).save(path)
    return path


# ---------------------------------------------------------------- on-device check

def selfcheck(frame=None):
    """Run once per install/upgrade on the phone. Prints the real signatures of every external call
    focal makes, then times each tier on one live frame. Fix whichever line says FAIL; put the
    measured ms into vision_sop. Gaze state is restored afterwards."""
    import inspect
    out = []
    for mod, fns in (('droid', ('capture', 'shot', 'ui_detect', 'ocr_text', 'tap', 'ask_vision')),
                     ('screen_peek', ('peek', 'peek_fast')), ('vision_api', ('ask_vision',)),
                     ('ui_detect_lite', ()), ('onnxruntime', ()), ('cv2', ())):
        m = _mod(mod)
        out.append(f'{mod}: {"ok" if m else "MISSING"}')
        for fn in fns:
            if m is not None and hasattr(m, fn):
                try:
                    sig = str(inspect.signature(getattr(m, fn)))
                except (TypeError, ValueError):
                    sig = '(?)'
                out.append(f'  {fn}{sig}')
            elif m is not None:
                out.append(f'  {fn}: absent')
    saved = (S.gaze, S.wh, S.rot, list(S.trail), S.last)
    try:
        t0 = time.perf_counter()
        f = _frame(frame)
        out.append(f'capture {int((time.perf_counter() - t0) * 1000)}ms {f["image"].shape}')
        reset()
        for b in ('pixel', 'detect', 'onnx'):
            fx = look(frame=f, backend=b)
            ok = 'FAIL ' + repr(S.err) if fx.backend.startswith('pixel<-') else 'ok'
            out.append(f'look[{b}] {fx.ms}ms {ok}\n{fx}')
        if hasattr(_mod('droid'), 'ui_detect'):
            raw = _dets(_mod('droid').ui_detect(np.ascontiguousarray(f['image'])))
            out.append(f'ui_detect full frame: {len(raw)} boxes, first: {raw[:1]}')
        rect = _gaze_rect(f)
        for label, call in (('read()', lambda: read(frame=f)), ('read(want)', lambda: read(['设置'], frame=f)),
                            ('periphery', lambda: periphery(frame=f))):
            t0 = time.perf_counter()
            try:
                res = call()
                out.append(f'{label} {int((time.perf_counter() - t0) * 1000)}ms ok: {str(res)[:120]!r}')
            except Exception as e:
                out.append(f'{label} FAIL {type(e).__name__}: {e}')
        out.append(f'roi rect passed to peek = {rect} (x1,y1,x2,y2): check the matched x,y fall inside it')
        side = rect[2] - rect[0]
        out.append(f'ask tokens ≈ {est_tokens(side, side)} (crop) vs {est_tokens(*S.wh)} (full screen)')
    finally:
        S.gaze, S.wh, S.rot, S.trail, S.last = saved
    print('\n'.join(out))
