"""Synthetic phone screens with ground-truth boxes, for tests and focal_train smoke runs."""
import numpy as np
from PIL import Image, ImageDraw, ImageFont

FONT = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
WORDS = 'search settings upgrade vision message contacts discover profile send photo album'.split()


def _font(size):
    try:
        return ImageFont.truetype(FONT, size)
    except OSError:
        return ImageFont.load_default(size=size)


def _photo(rng, w, h):
    lo = rng.random((max(2, h // 24), max(2, w // 24), 3))
    img = np.asarray(Image.fromarray((lo * 255).astype(np.uint8)).resize((w, h), Image.BICUBIC), np.float32)
    img += rng.normal(0, 18, img.shape)
    return np.clip(img, 0, 255).astype(np.uint8)


def screen(seed=0, w=720, h=1544):
    """-> (BGR ndarray, [(cls, (x1, y1, x2, y2)), ...])"""
    rng = np.random.default_rng(seed)
    im = Image.new('RGB', (w, h), (255, 255, 255))
    dr = ImageDraw.Draw(im)
    boxes = []
    y = 40
    while y < h - 260:
        kind = rng.choice(['text', 'icon', 'image', 'gap'], p=[0.4, 0.25, 0.2, 0.15])
        if kind == 'text':
            size = int(rng.integers(26, 44))
            x = int(rng.integers(20, 200))
            s = ' '.join(rng.choice(WORDS, int(rng.integers(1, 3))))
            x2 = min(w - 10, x + int(dr.textlength(s, font=_font(size))))
            dr.text((x, y), s, fill=(20, 20, 20), font=_font(size))
            boxes.append(('Text', (x, y, x2, y + size + 6)))
            y += size + 30
        elif kind == 'icon':
            n = int(rng.integers(2, 5))
            side = int(rng.integers(64, 110))
            for k in range(n):
                x = 30 + k * (side + 60)
                if x + side > w - 10:
                    break
                col = tuple(int(c) for c in rng.integers(30, 230, 3))
                dr.rounded_rectangle((x, y, x + side, y + side), radius=side // 5, fill=col)
                dr.ellipse((x + side // 4, y + side // 4, x + 3 * side // 4, y + 3 * side // 4), fill=(255, 255, 255))
                boxes.append(('Icon', (x, y, x + side, y + side)))
            y += side + 40
        elif kind == 'image':
            iw, ih = int(rng.integers(260, w - 40)), min(int(rng.integers(180, 320)), h - 10 - y)
            x = int(rng.integers(20, w - iw - 10))
            im.paste(Image.fromarray(_photo(rng, iw, ih)), (x, y))
            boxes.append(('Image', (x, y, x + iw, y + ih)))
            y += ih + 40
        else:
            y += int(rng.integers(120, 260))
    return np.asarray(im)[..., ::-1].copy(), boxes


def empty_spot(boxes, r, w=720, h=1544):
    """Centre of a 2r square that touches no box (for 'blank' assertions)."""
    for y in range(r, h - r, 8):
        for x in range(r, w - r, 8):
            if all(x + r <= b[0] or x - r >= b[2] or y + r <= b[1] or y - r >= b[3] for _, b in boxes):
                return x, y
    raise AssertionError('screen has no empty spot')
