"""CPU latency of ONNX detectors. Device-safe: numpy + onnxruntime only.

    python bench_onnx.py model.onnx [more.onnx ...] --shapes 640x320,640x640 --threads 1,2,4,6
Shapes are HxW of the letterboxed input (portrait 1080x2340 at 640 -> 640x320).
Reports median / p90 of session.run only (no pre/post-processing) — the
number the <= 50 ms budget is about.
"""
import argparse
import time

import numpy as np
import onnxruntime as ort


def feeds_for(sess, h, w):
    f = {}
    for i in sess.get_inputs():
        if i.name == "images":
            f[i.name] = (np.random.rand(1, 3, h, w) * 255).astype(np.float32)
        elif i.name == "orig_target_sizes":  # D-FINE deploy graph
            f[i.name] = np.array([[w, h]], np.int64)
        elif i.name == "max_det":
            f[i.name] = np.array([300], np.int64)
        elif i.name == "conf_floor":
            f[i.name] = np.array([0.25], np.float32)
        elif i.name == "iou_thr":
            f[i.name] = np.array([0.6], np.float32)
        else:
            raise ValueError("unknown input %s" % i.name)
    return f


def bench(path, h, w, threads, warmup=10, runs=50):
    so = ort.SessionOptions()
    so.intra_op_num_threads = threads
    so.inter_op_num_threads = 1
    so.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_ALL
    s = ort.InferenceSession(path, so, providers=["CPUExecutionProvider"])
    f = feeds_for(s, h, w)
    for _ in range(warmup):
        s.run(None, f)
    t = []
    for _ in range(runs):
        t0 = time.perf_counter()
        s.run(None, f)
        t.append((time.perf_counter() - t0) * 1e3)
    return float(np.median(t)), float(np.percentile(t, 90))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("models", nargs="+")
    ap.add_argument("--shapes", default="640x320")
    ap.add_argument("--threads", default="1,4")
    ap.add_argument("--runs", type=int, default=50)
    a = ap.parse_args()
    print("ort", ort.__version__)
    print("%-28s %-8s %3s %8s %8s" % ("model", "HxW", "thr", "med_ms", "p90_ms"))
    for p in a.models:
        for shp in a.shapes.split(","):
            h, w = map(int, shp.split("x"))
            for th in map(int, a.threads.split(",")):
                try:
                    med, p90 = bench(p, h, w, th, runs=a.runs)
                    print("%-28s %-8s %3d %8.1f %8.1f" % (p.split("/")[-1][:28], shp, th, med, p90))
                except Exception as e:  # fixed-shape model at a foreign shape
                    print("%-28s %-8s %3d   n/a (%s)" % (p.split("/")[-1][:28], shp, th, type(e).__name__))
