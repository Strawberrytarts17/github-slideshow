# focal → SOP patch (paste the two blocks, then delete this file)

The originals live on the phone, so this file only carries what to insert and where.
After pasting, the single source of truth for focal details is the `focal.py` docstring
(`help(focal)`), the same "code is the source of truth" pattern as `droid.SENSITIVE_APPS`.
The SOPs only get routing and red lines, so nothing is documented twice.

## 1) `memory/vision_sop.md` — insert after the line that starts with `OCR 常吞空格`

```markdown
焦点视觉 memory/focal.py(注视圈 + 3×3 原分辨率格分类, 全端侧, 0 token; 细节=help(focal))
定位: 补在 peek_fast 与 ask_vision 之间。由便宜到贵, 同一帧可复用: 外周 peek_fast()/focal.periphery() 决定看哪 → focal.look() 圈内 3×3 分类 → focal.read() 只 OCR 圈内 → focal.ask() 只把圈内裁剪交 VLM。
原理: 注视圈=(x,y,r), 外接方形切 nw n ne / w c e / sw s se 九格, 每格按原分辨率裁出——只缩面积不缩分辨率(上文实测: 面积是唯一有效提速, 降分辨率 OCR 乱码)。
用法: fx=focal.look(at=el)(el=look()/peek 元素: 元素占满中格 c, 八邻格=上下文) / at=(x,y[,r]) / at='ne'(钻入该格, r/3; periphery() 之后=跳到该区) → print(fx) 共 4 行; focal.back()/reset()。
读: focal.read(frame=fx.frame) 圈内 droid.ocr_text; focal.read(want=[…]) 走 screen_peek.peek(roi=圈外接矩形, img=帧) 模糊匹配。
问: focal.ask('问题') 只送圈内裁剪, ≈w·h/750 tok(r=180 → 173 tok; 1080×2400 整屏缩放后 ≈1920 tok; 公式估算, 待实测); context=True 拼全屏缩略图+红圈, 仍 <300 tok。返回值同 ask_vision('Error: …' 不抛)。
点: focal.tap('ne') 点该格中心并自动带 fx 帧的 screen=; 屏幕尺寸/旋转一变, look() 重置注视并在表头标 gaze reset, 不缩放旧坐标(同 phone_use 当帧规则)。
标签读法: 大写=模型类(NAMES)+分数(detect 后端另带 OCR 字); ~小写=像素启发式 blank/glyph/graphic/photo/mixed, 无分数, 只说明"有东西/像什么", 不是检测结论; ·=空。表头 [pixel<-detect: TypeError] = 后端失败已回落, 别当检测到位(同"折表成功≠检测到位")。
分类器 focal.use('auto') 按序选可用者: onnx(专用格分类器 models/focal_cls_v1/model.onnx, 由 memory/focal_train.py 用 collect.py 数据训练, 类名/预处理写在 onnx 元数据里, 只拷一个文件) > detect(droid.ui_detect 跑在圈内裁剪上, YOLO 内部放大 = 小目标变大) > pixel(纯 numpy)。Python 里 import 不到 onnxruntime 时用 focal.use('onnx', runner=APK 总线函数)。
首次/升级后先跑 focal.selfcheck(): 打印 droid/screen_peek/vision_api 的实际签名 + 各级耗时; ui_detect 框格式、peek 的 roi 元组格式(focal 传 x1,y1,x2,y2)只在这里核对, 不猜。实测 ms 回填本段。
敏感 App 可用: 只走截图+OCR+YOLO+坐标 tap, 从不调 dump。
眼动仪画面: focal.render() → 截图上画圈+九格+注视轨迹, 回图给用户看。手机屏上实时画圈需 APK 悬浮层(已留 focal.on_move(fn) 钩子), 且该层必须不进截图, 否则污染圈内分类。
```

## 2) `memory/phone_use.md` — §1 工具选型 table, new row between row 2 (shot+ui_detect) and row 3 (vision)

```markdown
| 2.5 focal | 已知大致位置, 要看清小图标/密集区/判断某块是什么 | 注视圈内 3×3 原分辨率分类 + 圈内 OCR/VLM(省 token) | 先 focal.selfcheck(); ~小写标签=启发式, 非检测 |
```
