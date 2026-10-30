import os
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "runtime"))
import vlm_gate as G  # noqa: E402

WH = (1080, 2340)


def _d(cls, box, label=None):
    return {"bbox": list(box), "type": "icon", "label": label, "cls": cls, "confidence": 0.9}


DETS = [_d("Toolbar", (0, 80, 1080, 240)), _d("Text", (40, 120, 400, 200), "Settings"),
        _d("Switch", (900, 400, 1040, 470)), _d("Text", (40, 400, 500, 470), 'Wi-Fi "home"'),
        _d("Icon", (960, 120, 1040, 200)), _d("Image", (0, 600, 1080, 1400))]


def test_dhash_ignores_status_bar_and_detects_change():
    rng = np.random.default_rng(0)
    a = rng.integers(0, 255, (2340, 1080, 3), dtype=np.uint8)
    b = a.copy()
    b[:60] = 0  # clock tick in the status bar
    assert G.hamming(G.dhash(a), G.dhash(b)) == 0 and G.is_stable(a, b)
    c = a.copy()
    c[800:2000] = 255 - c[800:2000]
    assert not G.is_stable(a, c)


def test_digest_is_compact_ordered_and_quoted():
    text, marks = G.digest(DETS, WH)
    lines = text.splitlines()
    assert lines[1].startswith("1 Toolbar 0,3,100,6")
    assert '"Wi-Fi \'home\'"' in text and len(marks) == 6
    assert [marks[i]["cls"] for i in sorted(marks)][:3] == ["Toolbar", "Text", "Icon"]
    text2, marks2 = G.digest(DETS, WH, max_items=3)
    assert "omitted" in text2 and {marks2[i]["cls"] for i in marks2} >= {"Toolbar"}


def test_marks_and_crop():
    img = np.full((2340, 1080, 3), 255, np.uint8)
    _, marks = G.digest(DETS, WH)
    som = G.set_of_marks(img, marks)
    assert (som != 255).any() and (img == 255).all()
    crop, (x0, y0, s) = G.crop_for(img, [DETS[2], DETS[3]], pad=10, max_side=256)
    assert (x0, y0) == (30, 390) and max(crop.shape[:2]) == 256 and s < 1


def test_route_tiers():
    assert G.route("count", DETS, WH) == G.LOCAL
    assert G.route("find_text", DETS, WH) == G.LOCAL
    assert G.route("semantic", DETS, WH, stable=False) == G.RECAPTURE
    assert G.route("semantic", DETS, WH, sensitive=True) == G.BLOCK
    assert G.route("count", DETS, WH, sensitive=True) == G.LOCAL  # local never leaks
    assert G.route("visual", DETS, WH) == G.VLM_CROP
    assert G.route("semantic", DETS[:2], WH) == G.VLM_FULL
    assert G.route("semantic", DETS, WH) == G.VLM_CROP  # 2/5 leaves labelled
    lab = DETS + [_d("TextButton", (40, 2000, 500, 2100), "OK")]
    assert G.route("semantic", lab, WH) == G.TEXT_LLM


def test_router_learns_and_roundtrips(tmp_path):
    rng = np.random.default_rng(0)
    X, y = [], []
    for _ in range(400):
        n_lab = int(rng.integers(0, 6))
        dets = [_d("Text", (0, 100 * i, 500, 100 * i + 50), "t" if i < n_lab else None) for i in range(6)]
        X.append(G.features(dets, WH, "semantic"))
        y.append(float(n_lab >= 3))
    r = G.Router().fit(X, y)
    acc = ((r.predict_proba(X) > 0.5) == np.array(y)).mean()
    assert acc > 0.9
    r.save(str(tmp_path / "r.json"))
    r2 = G.Router.load(str(tmp_path / "r.json"))
    assert np.allclose(r.predict_proba(X), r2.predict_proba(X))
    full = [_d("Text", (0, 100 * i, 500, 100 * i + 50), "t") for i in range(6)]
    assert G.route("semantic", full, WH, router=r, p_text=0.5) == G.TEXT_LLM


def test_cache_hits_unchanged_screen_only():
    c = G.AnswerCache(max_dist=4, ttl=10)
    c.put("com.app", "q", 0b1011, "yes", now=0)
    assert c.get("com.app", "q", 0b1001, now=1) == "yes"     # 1 bit off
    assert c.get("com.app", "q", 0b1011 ^ 0xFF, now=1) is None
    assert c.get("com.other", "q", 0b1011, now=1) is None
    assert c.get("com.app", "q", 0b1011, now=11) is None     # expired


def test_incumbent_class_names_route():
    inc = [_d("Modal", (100, 600, 980, 1600)), _d("TextButton", (600, 1400, 900, 1500), "OK"),
           _d("Text", (150, 700, 900, 800), "Allow?"), _d("Checkbox", (150, 900, 200, 950))]
    assert G.route("semantic", inc, WH) == G.TEXT_LLM
    assert G.features(inc, WH, "semantic").shape == G.features(DETS, WH, "semantic").shape
