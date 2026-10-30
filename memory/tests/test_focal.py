"""PC-side tests for focal.py. On-device modules (droid, screen_peek, vision_api, ui_detect_lite)
are replaced by recording fakes; on the phone run focal.selfcheck() instead.
Run: cd memory && python -m pytest tests -q"""
import os
import sys
from types import SimpleNamespace

import numpy as np
import pytest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [os.path.dirname(HERE), HERE]
import focal  # noqa: E402
import synth  # noqa: E402

W, H = 720, 1544


@pytest.fixture(autouse=True)
def fresh(monkeypatch):
    focal.reset()
    focal.S.wh = focal.S.rot = focal.S.err = None
    focal.S.hooks.clear()
    focal.use('auto')
    focal._MODS.clear()
    for name in ('droid', 'screen_peek', 'vision_api', 'ui_detect_lite'):
        monkeypatch.setitem(sys.modules, name, None)  # absent unless a test installs a fake
    monkeypatch.delenv('FOCAL_MODEL', raising=False)
    yield
    focal._MODS.clear()


def install(monkeypatch, name, **attrs):
    mod = SimpleNamespace(calls=[], **attrs)
    monkeypatch.setitem(sys.modules, name, mod)
    focal._MODS.clear()
    return mod


def white(w=W, h=H):
    return np.full((h, w, 3), 255, np.uint8)


# ---------------------------------------------------------------- geometry

def test_default_fixation_is_screen_centre_and_compact():
    fx = focal.look(frame=white())
    assert (fx.x, fx.y, fx.r) == (W // 2, H // 2, W // 6)
    assert fx.rect == (W // 2 - W // 6, H // 2 - W // 6, W // 2 + W // 6, H // 2 + W // 6)
    lines = str(fx).splitlines()
    assert len(lines) == 4 and lines[0].startswith('focal (360,772) r=120 cell=80x80 [pixel')
    assert lines[1] == 'nw · | n · | ne ·'


def test_cells_tile_the_rect_exactly():
    fx = focal.look(at=(300, 500, 100), frame=white())
    area = np.zeros((H, W), int)
    for c in fx.cells:
        area[c.box[1]:c.box[3], c.box[0]:c.box[2]] += 1
    x1, y1, x2, y2 = fx.rect
    assert area[y1:y2, x1:x2].min() == 1 and area.sum() == (x2 - x1) * (y2 - y1)


def test_gaze_is_clamped_on_screen():
    fx = focal.look(at=(0, H + 50, 5), frame=white())
    assert fx.r == focal.R_MIN
    assert fx.rect[0] == 0 and fx.rect[3] == H


def test_element_fills_centre_cell():
    fx = focal.look(at={'cls': 'Icon', 'x': 300, 'y': 400, 'box': [270, 370, 330, 430]}, frame=white())
    assert fx.r == 90 and fx.cell('c').box == (270, 370, 330, 430)


def test_drill_into_cell_then_back():
    focal.look(at=(360, 700, 180), frame=white())
    ne = focal.S.last.cell('ne')
    fx = focal.look(at='ne', frame=white())
    assert (fx.x, fx.y) == ne.xy and fx.r == 60
    assert focal.back() == (360, 700, 180)


def test_periphery_then_saccade_to_cell():
    p = focal.periphery(frame=white())
    assert p.kind == 'periphery' and str(p).startswith('periphery 720x1544 cell=240x514')
    fx = focal.look(at='se', frame=white())
    assert (fx.x, fx.y) == p.cell('se').xy and fx.r == 120


def test_screen_change_resets_gaze_instead_of_rescaling():
    focal.look(at=(100, 100, 50), frame={'image': white(), 'screen': {'rotation': 0}})
    fx = focal.look(frame={'image': white(), 'screen': {'rotation': 2}})  # 180°: same size
    assert 'gaze reset' in fx.note and (fx.x, fx.y) == (W // 2, H // 2)
    fx = focal.look(frame=white(H, W))  # landscape
    assert 'gaze reset' in fx.note and fx.rect[2] <= H
    with pytest.raises(RuntimeError):
        focal.look(at='ne', frame=white())  # old grid is gone too
    with pytest.raises(RuntimeError, match='look'):
        focal.read(frame=white(H, W))  # read/ask refuse instead of reading a re-centred gaze


def test_on_move_hook_and_broken_hook():
    seen = []
    focal.on_move(lambda x, y, r: seen.append((x, y, r)))
    focal.on_move(lambda x, y, r: 1 / 0)
    focal.look(at=(200, 300, 60), frame=white())
    assert seen[-1] == (200, 300, 60) and isinstance(focal.S.err, ZeroDivisionError)


# ---------------------------------------------------------------- pixel backend

def unclamped(cls):
    """(screen, box) for the first synthetic cls box whose element-fit gaze (r = 1.5 * long side)
    needs no edge clamping, so the centre cell lands exactly on it."""
    for seed in range(40):
        img, boxes = synth.screen(seed)
        for c, (x1, y1, x2, y2) in boxes:
            r, cx, cy = 1.5 * max(x2 - x1, y2 - y1), (x1 + x2) / 2, (y1 + y2) / 2
            if c == cls and r <= min(cx, cy, W - cx, H - cy):
                return img, (x1, y1, x2, y2)
    raise AssertionError(f'no unclamped {cls} in 40 seeds')


def test_pixel_labels_on_synthetic_screen():
    img, boxes = synth.screen(3)
    x1, y1, x2, y2 = next(b for c, b in boxes if c == 'Image')  # wide: gaze inside it instead
    fx = focal.look(at=((x1 + x2) // 2, (y1 + y2) // 2, 80), frame=img)
    assert str(fx.cell('c')) == 'c ~photo', str(fx)
    for cls, want in (('Text', '~glyph'), ('Icon', '~graphic')):
        im, b = unclamped(cls)
        fx = focal.look(at=b, frame=im, backend='pixel')
        assert str(fx.cell('c')) == 'c ' + want, (cls, str(fx))
        assert fx.cell('c').score is None
    fx = focal.look(at=(*synth.empty_spot(boxes, 40), 40), frame=img)
    assert fx.cell('c').label == 'blank'


# ---------------------------------------------------------------- detect backend

def test_detect_backend_labels_cells_in_screen_coords(monkeypatch):
    def ui_detect(img):
        d.calls.append(img.shape)
        return [  # crop-local coordinates, as for any image handed to ui_detect
            {'cls': 'Modal', 'conf': 0.9, 'label': '', 'box': [0, 0, 360, 360]},
            {'cls': 'Icon', 'conf': 0.8, 'label': '设置', 'box': [250, 10, 350, 110]},
            {'cls': 'Text', 'conf': 0.7, 'label': 'Upgradevisioncapabilities', 'box': [10, 280, 110, 320]},
        ]
    d = install(monkeypatch, 'droid', ui_detect=ui_detect)
    install(monkeypatch, 'ui_detect_lite', NAMES=['Text', 'Icon', 'Dialog'], MODEL_TO_CANON={'Modal': 'Dialog'})
    fx = focal.look(at=(360, 700, 180), frame=white())
    assert fx.backend == 'detect' and d.calls == [(360, 360, 3)]
    assert str(fx.cell('ne')) == 'ne Icon .80 "设置"'
    assert str(fx.cell('sw')) == 'sw Text .70 "Upgradevi…"'
    assert fx.cell('c').label == 'Dialog' and fx.cell('c').box == (300, 640, 420, 760)
    assert [c.name for c in fx.find('dialog')] == ['nw', 'n', 'w', 'c', 'e', 's', 'se']


def test_assign_prefers_box_that_fits_the_cell():
    cells = focal._grid_boxes((0, 0, 300, 300))
    dets = [{'cls': 'ListItem', 'conf': 0.99, 'text': '', 'box': (0, 0, 300, 300)},
            {'cls': 'Icon', 'conf': 0.3, 'text': '', 'box': (110, 110, 190, 190)}]
    got = [r[0] for r in focal.assign(cells, dets)]
    assert got[4] == 'Icon' and got.count('ListItem') == 8
    point = [{'cls': 'Text', 'conf': .5, 'text': 'hi', 'box': (250, 250, 250, 250)}]  # centre-only detection
    assert [r and r[0] for r in focal.assign(cells, point)] == [None] * 8 + ['Text']


def test_detect_failure_falls_back_and_says_so(monkeypatch):
    def ui_detect(img, conf):
        raise AssertionError('unreachable')
    install(monkeypatch, 'droid', ui_detect=ui_detect)
    fx = focal.look(frame=white())
    assert fx.backend == 'pixel<-detect: TypeError' and isinstance(focal.S.err, TypeError)
    assert all(c.score is None for c in fx.cells)


# ---------------------------------------------------------------- onnx backend

def rgb_model(path, batch='N', classes=('red', 'green', 'blue')):
    """Tiny real ONNX: GlobalAveragePool -> Flatten -> Gemm(x10) -> Softmax; argmax = dominant channel."""
    onnx = pytest.importorskip('onnx')
    from onnx import TensorProto, helper
    g = helper.make_graph(
        [helper.make_node('GlobalAveragePool', ['x'], ['p']),
         helper.make_node('Flatten', ['p'], ['f']),
         helper.make_node('Gemm', ['f', 'w', 'b'], ['z']),
         helper.make_node('Softmax', ['z'], ['y'], axis=1)],
        'rgb', [helper.make_tensor_value_info('x', TensorProto.FLOAT, [batch, 3, 16, 16])],
        [helper.make_tensor_value_info('y', TensorProto.FLOAT, [batch, 3])],
        [helper.make_tensor('w', TensorProto.FLOAT, [3, 3], (np.eye(3) * 10).ravel().tolist()),
         helper.make_tensor('b', TensorProto.FLOAT, [3], [0, 0, 0])])
    m = helper.make_model(g, opset_imports=[helper.make_opsetid('', 13)])
    m.ir_version = 8
    for k, v in (('classes', list(classes)), ('mean', [0, 0, 0]), ('std', [1, 1, 1]), ('rgb', True)):
        m.metadata_props.add(key=k, value=__import__('json').dumps(v))
    onnx.save(m, path)
    return path


def colour_grid():
    img = white()
    fx = focal.look(at=(360, 700, 150), frame=img)
    bgr = {'nw': (0, 0, 255), 'c': (0, 255, 0), 'se': (255, 0, 0), 'e': (128, 128, 128)}
    for name, col in bgr.items():
        x1, y1, x2, y2 = fx.cell(name).box
        img[y1:y2, x1:x2] = col
    return img


@pytest.mark.parametrize('batch', ['N', 1])
def test_onnx_backend_reads_metadata_and_classifies(tmp_path, monkeypatch, batch):
    pytest.importorskip('onnxruntime')
    monkeypatch.setenv('FOCAL_MODEL', rgb_model(str(tmp_path / 'm.onnx'), batch))
    img = colour_grid()
    fx = focal.look(frame=img)  # 'auto' finds $FOCAL_MODEL
    assert fx.backend == 'onnx'
    assert [str(fx.cell(n)) for n in ('nw', 'c', 'se')] == ['nw red 1.00', 'c green 1.00', 'se blue 1.00']
    assert fx.cell('e').score is None  # grey: p=.33 < MIN_CONF -> pixel label kept
    assert focal.S.onnx.size == 16 and focal.S.onnx.batch == (batch == 'N')


def test_onnx_runner_injection_without_onnxruntime(monkeypatch):
    monkeypatch.setitem(sys.modules, 'onnxruntime', None)
    seen = []

    def bus(x):  # stands in for the APK-bus ONNX runner
        seen.append(x.shape)
        return x.mean(axis=(2, 3)) * 10
    img = colour_grid()
    focal.use('onnx', runner=bus, classes=['red', 'green', 'blue'], size=8, mean=[0, 0, 0], std=[1, 1, 1])
    fx = focal.look(frame=img)
    assert seen == [(9, 3, 8, 8)] and fx.cell('nw').label == 'red'
    focal.use('onnx')  # no model, no runtime -> visible fallback
    assert focal.look(frame=white()).backend.startswith('pixel<-onnx')


def test_auto_order_onnx_detect_pixel(tmp_path, monkeypatch):
    assert focal.look(frame=white()).backend == 'pixel'
    install(monkeypatch, 'droid', ui_detect=lambda img: [])
    focal.use('auto')
    assert focal.look(frame=white()).backend == 'detect'
    pytest.importorskip('onnxruntime')
    monkeypatch.setenv('FOCAL_MODEL', rgb_model(str(tmp_path / 'm.onnx')))
    focal.use('auto')
    assert focal.look(frame=white()).backend == 'onnx'


# ---------------------------------------------------------------- read / ask / tap / capture

def test_read_ocr_and_peek_use_the_gaze_rect(monkeypatch):
    d = install(monkeypatch, 'droid', ocr_text=lambda crop: d.calls.append(crop.shape) or 'Upgradevision')
    sp = install(monkeypatch, 'screen_peek', peek=lambda **kw: sp.calls.append(kw) or {'found': ['设置']})
    fx = focal.look(at=(360, 700, 100), frame=white())
    assert focal.read(frame=fx.frame) == 'Upgradevision' and d.calls == [(200, 200, 3)]
    assert focal.read(['设置'], frame=fx.frame) == {'found': ['设置']}
    kw = sp.calls[0]
    assert kw['want'] == ['设置'] and kw['roi'] == fx.rect and kw['img'] is fx.frame['image']


def test_ask_sends_crop_or_composite_and_passes_errors(monkeypatch):
    va = install(monkeypatch, 'vision_api', ask_vision=lambda img, q: va.calls.append((img.shape, q)) or 'Error: 429')
    focal.look(at=(360, 700, 180), frame=white())
    assert focal.ask('什么图标?', frame=white()) == 'Error: 429'
    assert va.calls[0] == ((360, 360, 3), '什么图标?')
    focal.ask('什么图标?', frame=white(), context=True)
    (h, w, _), q = va.calls[1]
    assert h == 360 and w == 360 + 8 + round(W * 360 / H) and q.endswith('红圈=焦点位置。什么图标?')
    focal.look(at=(360, 700, 30), frame=white())
    focal.ask('?', frame=white())
    assert va.calls[2][0] == (256, 256, 3)  # tiny crop upscaled
    install(monkeypatch, 'droid', ask_vision=lambda img, q: 'via droid')
    assert focal.ask('?', frame=white()) == 'via droid'  # droid.ask_vision is the unified entry


def test_tap_uses_cell_centre_and_frame_screen(monkeypatch):
    d = install(monkeypatch, 'droid', tap=lambda x, y, **kw: d.calls.append((x, y, kw)) or 'ok')
    with pytest.raises(RuntimeError):
        focal.tap()
    scr = {'w': W, 'h': H, 'rotation': 0}
    fx = focal.look(at=(360, 700, 90), frame={'image': white(), 'screen': scr})
    focal.tap('ne')
    assert d.calls == [(fx.cell('ne').xy + ({'screen': scr},))]
    focal.look(frame=white())
    focal.tap()
    assert d.calls[-1] == (360, 700, {})


def test_capture_retries_only_the_transient(monkeypatch):
    n = []

    def capture():
        n.append(1)
        if len(n) == 1:
            raise RuntimeError('java.lang.RuntimeException: takeScreenshot failed code=3')
        return {'image': white(), 'screen': {'rotation': 0}}
    install(monkeypatch, 'droid', capture=capture)
    monkeypatch.setattr(focal.time, 'sleep', lambda s: None)
    assert focal.look().frame['screen'] == {'rotation': 0} and len(n) == 2

    def black():
        raise RuntimeError('2 consecutive black frames (FLAG_SECURE?)')
    install(monkeypatch, 'droid', capture=black, shot=black)
    with pytest.raises(RuntimeError, match='black'):
        focal.look()


# ---------------------------------------------------------------- render / tokens / selfcheck

def test_render_draws_circle_grid_and_scanpath(tmp_path):
    from PIL import Image
    focal.look(at=(200, 300, 90), frame=white())
    fx = focal.look(at=(500, 1000, 120), frame=white())
    path = focal.render(str(tmp_path / 'v.png'))
    px = np.asarray(Image.open(path))
    assert tuple(px[1000, 500 + 120]) == (255, 0, 0)    # red ring at radius r (RGB on disk)
    assert tuple(px[fx.rect[1], 450]) == (255, 200, 0)  # grid line
    assert tuple(px[650, 350]) == (0, 128, 255)         # scanpath midpoint between fixations


def test_est_tokens_matches_vision_sop():
    assert abs(focal.est_tokens(720, 1544) - 1482) <= 1
    assert focal.est_tokens(1080, 2400) == 1920  # capped at 1.44 MP like ask_vision (-> ~804x1788)
    assert focal.est_tokens(360, 360) == 173


def test_selfcheck_runs_against_fakes(monkeypatch, capsys):
    img, _ = synth.screen(1)
    install(monkeypatch, 'droid', capture=lambda: {'image': img, 'screen': None},
            ui_detect=lambda im: [{'cls': 'Icon', 'conf': .9, 'box': [0, 0, 40, 40]}],
            ocr_text=lambda crop: 'abc', tap=lambda x, y: None)
    install(monkeypatch, 'screen_peek', peek=lambda **kw: {'found': []})
    focal.look(at=(100, 100, 50), frame=img)
    focal.selfcheck()
    out = capsys.readouterr().out
    assert 'look[detect]' in out and 'look[pixel]' in out and 'read(want)' in out
    assert 'look[onnx]' in out and 'FAIL' in out  # no model here: reported, not raised
    assert focal.gaze() == (100, 100, 50)            # state restored
