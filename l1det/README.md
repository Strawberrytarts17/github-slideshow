# L1 UI detector — clean-license replacement

The only doc for this package. Status 2026-10-29: everything that doesn't need
training data or a GPU is built and tested: the ONNX contract, on-device glue,
exporter, benchmark, eval and dataset tools. Training is blocked on two things:
a GPU box and the legal sign-off in [Provenance](#provenance).

## Answers to the handover's §7 questions

**1. Taxonomy: train 19 classes, not 21** (`classes.txt`, model index order).
- **Drop `List`.** It's a container: huge boxes, the same failure as defect 5,
  and the >85% filter keeps small lists and drops full-screen ones, so its
  supervision is inconsistent. Glue derives it as the union of `ListItem`s.
- **Merge `Card` into `ListItem`** ("tappable content block": row, grid cell,
  feed card). a11y rarely declares a card: plain `CardView` reports its
  `FrameLayout` superclass, and Compose cards have no role. `RecyclerView`
  children, on the other hand, are exposed reliably. Training a class the label
  source can't produce would recreate defect 4.
- **Define `Button` / `TextButton` / `Icon` by appearance, not widget class.**
  Rule: `ImageButton` or clickable `ImageView` up to ~56 dp → `Icon`. Without it,
  toolbar glyph buttons get labelled `Button` while identical glyphs elsewhere
  get `Icon`, and both classes degrade.
- **Don't split by state.** Record `checked`/`selected` in `meta.jsonl` now
  (see device-side asks) so a state head can be added later without re-collecting.
- **Merge gate after the first run:** a class with AP50 < 0.3 whose misses go
  more than 50% to one sibling (eval_ap prints confusions) gets merged. Likely
  candidates: Chip→TextButton, Button→Icon, SearchBar→EditText.
- The mapping lives in one dict (`tools/prepare_dataset.py: SOURCE_MAPS`).
  Already-collected 21-class data converts by name, so nothing needs re-collecting.

**2. One model, one head; `Text` is just a class.** Text *recognition* stays a
separate stage, but it should be fed the detector's text-class boxes instead
of running PP-OCR's own detector. That drops PP-OCR det from the 2840 ms path.
Caveat: a11y text boxes are view bounds (padding, often multi-line), and PP-OCR
rec wants single lines. So split multi-line crops with a row-projection profile
(numpy), or run PP-OCR det only inside the crop. How much this saves depends
on the det/rec split, which needs measuring (ask A5).

**3. Device data: count instances per class across apps, not frames.** Assume
CLAY (human-verified, ~59.5k Rico screens) is cleared for pretraining. Then a
first run is worth it at roughly 1,000–1,500 device frames, once
`prepare_dataset.py` reports every class `ok`:

| | instances | distinct apps |
|---|---|---|
| SearchBar, Chip, Tab, Dialog (no public source has them) | ≥ 300 | ≥ 15 |
| all other classes (CLAY covers them; device data is domain adaptation) | ≥ 100 | ≥ 10 |

The held-out set is separate: 200–300 frames from apps that are not in
training (split by package, never by frame), human-verified. It should include
~100 hand-labelled image-only super-app frames, since that's where the
incumbent is weakest and no a11y labels exist. If CLAY isn't cleared, plan on
several thousand frames, and Switch/Slider/RadioButton/ProgressBar will be thin.

CLAY instance counts (computed from its `clay_labels.csv`): Text 357k ·
Pictogram 217k · ListItem 124k · Button 97k · Image 59k · Toolbar 34k ·
TextInput 11k · CheckBox 5.7k · NavigationBar 5.5k · Card 4.7k · Spinner 3.4k ·
Switch 3.0k · RadioButton 1.7k · Slider 1.4k (only 345 screens) · ProgressBar 1.2k.

## Decisions

### Architecture: NanoDet-Plus-m-1.5x (measured, not estimated)

All candidates were exported to ONNX opset 17 with random weights and timed
with `tools/bench_onnx.py`. Setup: Xeon 2.1 GHz shared VM, 4 vCPU,
onnxruntime 1.17.3 CPU, fp32, `session.run` only, median of 100 runs over two
repetitions. Single-thread numbers are noisy (±25%).

| model | input (H×W) | params | fp32 file | 1 thread | 4 threads | × YOLOv8n @4t |
|---|---|---|---|---|---|---|
| YOLOv8n (incumbent architecture) | 640×320 | 3.0 M | — | 36–48 ms | 21–23 ms | 1.0 |
| **NanoDet-Plus-m-1.5x** (+ embedded NMS) | 640×320 | 2.43 M | 9.9 MB | 35–49 ms | 21–24 ms | **~1.0** |
| NanoDet-Plus-m-1.0x (+ embedded NMS) | 640×320 | 1.15 M | 4.8 MB | 25–32 ms | 18 ms | ~0.8 |
| NanoDet-Plus-m-1.5x | 640×640 | | | 93 ms | 38 ms | 1.7 |
| D-FINE-N | 640×640 only | 3.73 M | 12.9 MB | 115 ms | 45 ms | ~2.0 |
| D-FINE-S | 640×640 only | 10.2 M | **32.3 MB** | 316 ms | 116 ms | **~5.1** |

**Why D-FINE-S is rejected:**
- About 5× the incumbent's cost.
- At 32 MB fp32 it breaks the ~15 MB cap.
- Its deploy graph is fixed to a 640×640 square, so on a portrait screen half
  the input is padding.

**Why NanoDet-Plus-1.5x:**
- About the same cost as the incumbent at rect-640.
- Dynamic input shapes.
- Apache-2.0 code.

**Device projection** (cost ≈ ratio × incumbent's device time):
- If the incumbent infers in **46 ms**, 1.5x lands at ~40–50 ms: within the
  50 ms budget, with no headroom. 1.0x lands at ~35–40 ms.
- If the incumbent's 640 number is really **165 ms** (the §3 tradeoff line),
  no fp32 candidate fits at 640. Then the options are int8, 1.0x, or 512 input.
- Ask A1 settles which case applies.

Exporter fix worth knowing: NanoDet's ShuffleNetV2 `channel_shuffle` calls
`x.data.size()`, which bakes the trace-time H×W into the graph. Any other
aspect ratio then fails at runtime. `export/export_onnx.py` patches it.

### ONNX contract (`runtime/ui_detect_l1.py` docstring is authoritative)

- **Inputs:**
  - `images` f32 [1,3,H,W]: BGR, 0..255, normalization is inside the graph.
  - `conf_floor` f32[1], `iou_thr` f32[1], `max_det` i64[1]: **required**. The
    confidence floor is a runtime input, so `conf=0.05` really does recall
    boxes down to 0.05.
- **Output:** `dets` [1,K,6] = x1,y1,x2,y2,conf,cls, in input pixels, sorted
  by conf. One label per box (argmax), class-aware NMS.
- **Letterbox:** longest side 640, **top-left** anchored, padded bottom/right
  to **/64** with fill 114. This is not ultralytics' centred /32. The training
  pipeline must import the same `letterbox()` rather than reimplement it.
- **Class names** are embedded in the model metadata. The glue refuses a model
  whose names differ from `NAMES`.
- **`_yolo(img, conf, size)` / `L1Detector()(img)`** return the §2 schema with
  `label=None`. OCR fills `label`.
- `CONTAINER_CLASSES` (Dialog, ListItem, TabBar, Toolbar) never take an OCR
  label. This class rule replaces the ">50% of screen" size heuristic.
- `TEXT_CLASSES` sets `type`. Check it against how `ui_detect_lite` uses `type`.
- `postprocess_raw()` is the exact numpy post-processing for a `--raw` export.
  Tests check the embedded graph against it on three screen shapes and three
  threshold settings.

## Provenance

| item | used? | license | status |
|---|---|---|---|
| NanoDet code (RangiLyu/nanodet) | yes: architecture, training | Apache-2.0 | verified (repo LICENSE) |
| NanoDet COCO checkpoints | **no** | weights trained on COCO (Flickr images, mixed licenses) | avoid |
| torchvision ShuffleNetV2 ImageNet weights | **no**: exporter forces `pretrain=False` | code BSD-3; weights follow ImageNet's non-commercial terms | avoid unless legal approves |
| D-FINE (Peterande/D-FINE) | no, rejected on latency | Apache-2.0 | — |
| CLAY labels (google-research-datasets/clay) | planned primary public source | **no license stated in repo** | **confirm before training** |
| Rico screens + view hierarchies (images behind CLAY) | planned | not confirmed (official site unreachable from here) | **confirm before training** |
| VINS (sbunian/VINS) | maybe, Android subset only | repo Apache-2.0; images include Rico, iPhone and design-site screens the authors don't own | legal check |
| RICO Semantics (google-research-datasets/rico_semantics) | **not recommended** | **CC BY-SA 4.0** (ShareAlike); icon annotations only | verified |
| Device set (collect.py) | train + held-out | own collection; screenshots of third-party apps | internal policy |
| Incumbent YOLOv8 | **nothing**: no weights, distillation or pseudo-labels from it | AGPL-3.0 / Apache-2.0 conflict | excluded |
| YOLOv8n timing row above | local benchmark only | ultralytics (AGPL) run locally, random weights | nothing from it is in this repo |

**Init weights:** start from random init (pretraining happens on CLAY, in the
UI domain). That way no weight provenance is inherited at all. ImageNet init is
an A/B worth running only if legal clears it.

## Device-side asks (one session covers all of A)

**A. Measurements.** Copy `l1det/` to the device. The `bench/RANDOM_*.onnx`
files are random-weight models for timing only and must never ship.
1. Benchmark the candidates against the incumbent:
   `python tools/bench_onnx.py bench/RANDOM_nanodet-plus-1.5x.onnx bench/RANDOM_nanodet-plus-1.0x.onnx models/ui_detect_v1/models/ui_detect_yolo.onnx --shapes 640x320,512x256 --threads 1,2,4,6,8`.
   This puts all three on the same device, threads and ORT, and picks the thread count.
2. Smoke-test the glue on the real ORT/numpy/cv2:
   `python runtime/ui_detect_l1.py bench/RANDOM_nanodet-plus-1.5x.onnx screen.png`.
   The boxes are meaningless; this only checks that the glue runs.
3. Report `onnxruntime.__version__`.
4. Is 46 ms (peek_fast) the same model and input size as the 165 ms "640" figure?
5. Split the 2840 ms into PP-OCR det vs rec. Split the 0.22 s fast path into
   screencap (`-p` PNG encode/decode is often most of it; raw `screencap` is
   worth timing) vs inference.

**B. `collect.py` changes.** Cheap now, impossible to backfill later.
- Per box in `meta.jsonl`, record:
  - raw a11y fields: `className`, `viewIdResourceName`, `clickable`,
    `checkable`, `checked`, `selected`, `enabled`, has-text, has-contentDescription,
    window type;
  - the dropped nodes, with the reason each was dropped.

  With this, any taxonomy change is a re-map, not a re-collection.
- Per frame: `package`, activity, width, height, density, orientation. The
  split-by-app and the dp size rule need them. `prepare_dataset.py` reads
  `--group-key package` and `width`/`height` by default.
- Status bar, nav bar and IME: dump those windows or record their bounds.
  Otherwise their icons are trained as background.
- Flag large leaf nodes (WebView, SurfaceView, childless `View` over a set
  share of the screen) as unlabelled regions. Training will ignore them instead
  of learning "this is background".
- Keep saving sensitive-app frames image-only (the red line stays). ~100 of them,
  hand-labelled, become the super-app slice of the held-out set.
- Targeted pages:
  - Switch: Settings → Connections and toggle sub-pages. This also confirms the
    Switch mapping.
  - Slider: brightness, volume, media seek bars.
  - SearchBar, Chip, Tab: search and filter screens in shopping and food apps.

## Plan and gates

1. **Done:** contract, glue, exporter, benchmark, eval, dataset prep; 26 tests
   pass under py3.10 / numpy 1.26.2 / ORT 1.17.3.
2. **Gate — legal:** CLAY and Rico terms; random init vs ImageNet init.
3. **Needs a GPU box** (this container has 4 vCPU and no GPU):
   - CLAY converter: Rico `unique_uis.tar.gz`, ~6 GB, is reachable.
   - NanoDet loss changes:
     - per-source class masks, so a class a source doesn't annotate gets no
       negative loss;
     - ignore regions.
   - Shared letterbox.
   - Pretrain on CLAY, then fine-tune on the device train split. Optionally add
     high-confidence pseudo-labels on image-only frames; they never go in the eval.
4. **Eval:** `tools/eval_ap.py` on the human-verified held-out set. Report
   per-class AP honestly (Switch, Slider, SearchBar, Chip), then apply the
   merge gate.
5. **int8:** static QDQ with device frames as calibration. Keep it only if AP50
   drops ≤ 1 pt and device latency improves.
6. **Ship:** ONNX + `classes.txt` + `runtime/ui_detect_l1.py` + this provenance table.

## Layout and commands

```
classes.txt                 19 classes, model index order
runtime/ui_detect_l1.py     ships to device: NAMES, _yolo, L1Detector, letterbox, postprocess_raw
export/export_onnx.py       NanoDet checkpoint -> ONNX contract (off-box, torch)
tools/bench_onnx.py         latency (device-safe)
tools/eval_ap.py            per-class AP50 / AP50:95 / recall + confusions (device-safe)
tools/prepare_dataset.py    remap, validate, split-by-app, coverage report (device-safe)
tests/                      pytest; make_test_models.py builds the random-weight fixture pair
bench/RANDOM_*.onnx         random-weight timing models — never ship
```

```sh
# tests (device-equivalent env: py3.10, numpy 1.26.2, onnxruntime, opencv)
python tests/make_test_models.py --nanodet-root ext/nanodet --out-dir /tmp/l1   # off-box, torch
L1DET_MODEL=/tmp/l1/fixture.onnx L1DET_MODEL_RAW=/tmp/l1/fixture_raw.onnx pytest -q tests/
# export a trained checkpoint
python export/export_onnx.py --nanodet-root ext/nanodet --config l1det.yml --ckpt best.ckpt \
    --out ui_detect_l1.onnx --meta '{"weights": "<run id>", "data": "<dataset versions>"}'
# data
python tools/prepare_dataset.py collected/ prepared/
python tools/eval_ap.py --gt held_out/labels --images held_out/images --model ui_detect_l1.onnx
```
