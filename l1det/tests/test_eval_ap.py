import os
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))
import eval_ap as E  # noqa: E402

NAMES = ["A", "B", "C"]


def _gt(rng, n=8):
    xy = rng.uniform(0.2, 0.8, (n, 2))
    wh = rng.uniform(0.05, 0.15, (n, 2))
    return np.concatenate([rng.integers(0, 2, (n, 1)), xy, wh], 1).astype(np.float32)


def test_perfect_predictions_score_one():
    rng = np.random.default_rng(0)
    gts = [_gt(rng) for _ in range(5)]
    pairs = [(g, np.concatenate([g, np.full((len(g), 1), 0.9)], 1)) for g in gts]
    rows, conf = E.evaluate(pairs, NAMES)
    for r in rows[:2]:
        assert abs(r["AP50"] - 1) < 1e-6 and abs(r["AP50_95"] - 1) < 1e-6 and r["R@conf"] == 1
    assert rows[2]["n_gt"] == 0 and np.isnan(rows[2]["AP50"])
    assert not conf


def test_swapped_class_is_a_confusion_not_a_hit():
    g = np.array([[0, 0.5, 0.5, 0.2, 0.2]], np.float32)
    p = np.array([[1, 0.5, 0.5, 0.2, 0.2, 0.9]], np.float32)
    rows, conf = E.evaluate([(g, p)], NAMES)
    assert rows[0]["AP50"] == 0 and conf[("A", "B")] == 1


def test_shifted_box_passes_50_fails_95_and_dupes_are_fps():
    g = np.array([[0, 0.5, 0.5, 0.2, 0.2]], np.float32)
    p = np.array([[0, 0.52, 0.5, 0.2, 0.2, 0.9], [0, 0.52, 0.5, 0.2, 0.2, 0.8]], np.float32)
    r = E.evaluate([(g, p)], NAMES)[0][0]
    assert r["AP50"] == 1 and r["AP50_95"] < 1


def test_low_confidence_fp_ranked_first_lowers_ap():
    g = np.array([[0, 0.3, 0.3, 0.1, 0.1]], np.float32)
    p = np.array([[0, 0.8, 0.8, 0.1, 0.1, 0.9], [0, 0.3, 0.3, 0.1, 0.1, 0.5]], np.float32)
    r = E.evaluate([(g, p)], NAMES)[0][0]
    assert 0.4 < r["AP50"] < 0.6
