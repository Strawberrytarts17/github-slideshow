"""Runtime tests. Run under device-equivalent versions (py3.10, numpy 1.26).

    L1DET_MODEL=ui_detect_l1.onnx L1DET_MODEL_RAW=ui_detect_l1_raw.onnx pytest -q
Model tests skip when the env vars are unset. Build the fixture pair with
make_test_models.py (same weights, embedded vs --raw; raw is the reference).
"""
import os
import sys

import numpy as np
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "runtime"))
import ui_detect_l1 as L  # noqa: E402

MODEL = os.environ.get("L1DET_MODEL")
MODEL_RAW = os.environ.get("L1DET_MODEL_RAW")
needs_models = pytest.mark.skipif(not (MODEL and MODEL_RAW), reason="set L1DET_MODEL(_RAW)")


def _screen(h=2340, w=1080, seed=0):
    rng = np.random.default_rng(seed)
    img = np.full((h, w, 3), 245, np.uint8)
    for _ in range(40):  # UI-ish rectangles so the net sees structure
        x, y = rng.integers(0, w - 200), rng.integers(0, h - 120)
        img[y:y + rng.integers(20, 120), x:x + rng.integers(20, 200)] = rng.integers(0, 255, 3)
    return img


def test_classes_txt_matches_names():
    p = os.path.join(os.path.dirname(__file__), "..", "classes.txt")
    assert open(p).read().split() == L.NAMES
    assert len(set(L.NAMES)) == len(L.NAMES)
    assert L.TEXT_CLASSES <= set(L.NAMES) and L.CONTAINER_CLASSES <= set(L.NAMES)


@pytest.mark.parametrize("hw", [(2340, 1080), (1080, 2340), (2400, 1080), (640, 640), (100, 37)])
def test_letterbox_shape_and_inverse(hw):
    img = _screen(*hw) if min(hw) > 200 else np.zeros(hw + (3,), np.uint8)
    lb, s = L.letterbox(img)
    assert max(lb.shape[:2]) == L.YOLO_SIZE
    assert lb.shape[0] % L.STRIDE == 0 and lb.shape[1] % L.STRIDE == 0
    # a full-image box in letterbox space maps back to the full screen
    nh, nw = round(hw[0] * s), round(hw[1] * s)
    back = np.array([0, 0, nw, nh]) / s
    assert np.allclose(back, [0, 0, hw[1], hw[0]], atol=1 / s)
    assert (lb[nh:] == L.PAD_FILL).all() and (lb[:, nw:] == L.PAD_FILL).all()


def test_nms_basic():
    b = np.array([[0, 0, 10, 10], [1, 1, 10, 10], [20, 20, 30, 30]], np.float32)
    assert L.nms(b, np.array([0.9, 0.8, 0.7], np.float32), 0.5).tolist() == [0, 2]
    assert L.nms(b, np.array([0.9, 0.8, 0.7], np.float32), 0.95).tolist() == [0, 1, 2]


@needs_models
def test_embedded_contract():
    import onnxruntime as ort
    s = ort.InferenceSession(MODEL, providers=["CPUExecutionProvider"])
    assert [i.name for i in s.get_inputs()] == ["images", "conf_floor", "iou_thr", "max_det"]
    lb, _ = L.letterbox(_screen())
    out = s.run(None, {"images": lb.transpose(2, 0, 1)[None].astype(np.float32),
                       "conf_floor": np.array([0.3], np.float32),
                       "iou_thr": np.array([0.6], np.float32),
                       "max_det": np.array([50], np.int64)})[0]
    assert out.ndim == 3 and out.shape[0] == 1 and out.shape[2] == 6
    assert 0 < out.shape[1] <= 50
    assert (out[0, :, 4] > 0.3).all() and (np.diff(out[0, :, 4]) <= 0).all()


@needs_models
@pytest.mark.parametrize("hw", [(2340, 1080), (1080, 2340), (1920, 1080)])
@pytest.mark.parametrize("conf,iou", [(0.3, 0.6), (0.4, 0.3), (0.45, 0.9)])
def test_embedded_matches_reference(hw, conf, iou):
    emb, raw = L.L1Detector(MODEL), L.L1Detector(MODEL_RAW)
    assert emb.embedded_nms and not raw.embedded_nms
    img = _screen(*hw, seed=hw[0])
    a, b = emb.raw(img, conf, iou), raw.raw(img, conf, iou)
    assert len(a) == len(b) > 0
    assert np.allclose(a, b, atol=1e-2), np.abs(a - b).max()


@needs_models
def test_floor_is_really_exposed():
    det = L.L1Detector(MODEL)
    img = _screen()
    n = [len(det.raw(img, conf=c, max_det=5000)) for c in (0.5, 0.45, 0.4, 0.3)]
    assert n == sorted(n) and n[-1] > n[0]


@needs_models
def test_schema():
    out = L.L1Detector(MODEL)(_screen(), conf=0.3)
    assert out
    for d in out:
        assert set(d) == {"bbox", "type", "label", "cls", "confidence"}
        x1, y1, x2, y2 = d["bbox"]
        assert all(isinstance(v, int) for v in d["bbox"])
        assert 0 <= x1 <= x2 <= 1080 and 0 <= y1 <= y2 <= 2340
        assert d["type"] == ("text" if d["cls"] in L.TEXT_CLASSES else "icon")
        assert d["label"] is None and d["cls"] in L.NAMES
