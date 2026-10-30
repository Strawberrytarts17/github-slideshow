"""focal_train: synthetic YOLO dataset -> tiles -> (torch) train -> ONNX -> focal.look(backend='onnx').
Run: cd memory && python -m pytest tests -q"""
import os
import sys

import numpy as np
import pytest
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [os.path.dirname(HERE), HERE]
import focal  # noqa: E402
import focal_train  # noqa: E402
import synth  # noqa: E402

NAMES = ['Text', 'Icon', 'Image']


def yolo_dataset(root, n):
    os.makedirs(os.path.join(root, 'images'))
    os.makedirs(os.path.join(root, 'labels'))
    with open(os.path.join(root, 'classes.txt'), 'w') as fh:
        fh.write('\n'.join(NAMES))
    for i in range(n):
        img, boxes = synth.screen(100 + i)
        h, w = img.shape[:2]
        Image.fromarray(img[..., ::-1]).save(os.path.join(root, 'images', f's{i}.png'))
        with open(os.path.join(root, 'labels', f's{i}.txt'), 'w') as fh:
            for c, (x1, y1, x2, y2) in boxes:
                fh.write(f'{NAMES.index(c)} {(x1 + x2) / 2 / w} {(y1 + y2) / 2 / h} {(x2 - x1) / w} {(y2 - y1) / h}\n')
    return root


@pytest.fixture(autouse=True)
def fresh():
    focal.reset()
    focal.S.wh = focal.S.rot = None
    focal._MODS.clear()
    yield
    focal.use('auto')


def test_tiles_labels_cells_with_the_detect_rule(tmp_path):
    src = yolo_dataset(str(tmp_path / 'ds'), 4)
    counts = focal_train.tiles(src, str(tmp_path / 'tiles'), per_image=6)
    assert set(counts) == {'Text', 'Icon', 'Image', 'blank'}
    assert sum(counts.values()) == sum(len(os.listdir(tmp_path / 'tiles' / c)) for c in counts)
    for name in os.listdir(tmp_path / 'tiles' / 'blank'):
        px = np.asarray(Image.open(tmp_path / 'tiles' / 'blank' / name))
        assert focal._pixel(px[..., ::-1].copy())[0] == 'blank'


def test_train_exports_a_model_focal_can_load(tmp_path):
    pytest.importorskip('torch')
    pytest.importorskip('torchvision')
    pytest.importorskip('onnxruntime')
    src = yolo_dataset(str(tmp_path / 'ds'), 40)
    focal_train.tiles(src, str(tmp_path / 'tiles'), per_image=8)
    out = str(tmp_path / 'm' / 'model.onnx')
    acc = focal_train.train(str(tmp_path / 'tiles'), out, epochs=6, size=48, workers=0)
    assert acc > 0.8

    focal.use('onnx', path=out)
    img, boxes = synth.screen(7)  # unseen screen
    x1, y1, x2, y2 = next(b for c, b in boxes if c == 'Image')
    fx = focal.look(at=((x1 + x2) // 2, (y1 + y2) // 2, 90), frame=img)
    assert fx.backend == 'onnx' and focal.S.onnx.size == 48
    assert fx.cell('c').label == 'Image', str(fx)
    fx = focal.look(at=(*synth.empty_spot(boxes, 40), 40), frame=img)
    assert fx.cell('c').label == 'blank', str(fx)
