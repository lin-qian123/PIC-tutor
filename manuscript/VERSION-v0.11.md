# PIC-tutor v0.11

版本日期：2026-06-29

## 定位

`v0.11` 是 `PIC-tutor` 的 AMR guard-cell/regrid 闭环版。它继承 `v0.10` 的边界强 analysis 正文，并继续把第 7 章里原先只作为入口地图出现的 `GuardCellManager`、`WarpXComm` 和 `WarpXRegrid` 串成一段可审校正文。

本版的重点是说明 WarpX 的 AMR 运行时不是单纯的 coarse-fine 插值公式。guard-cell 预算同时约束数组分配、阶段通信和 load-balance 后重建；field 的 `FillBoundary`、PML exchange、source 项的 `SyncCurrent/SyncRho` 和 `RemakeLevel()` 必须共同保持布局、通信和诊断指针一致。

本版仍不是出版终稿。它补齐第 7 章 AMR 并行层的一条核心主线，但 PSATD/Galilean/NCI/PML 文献闭环、HTML 宽表格人工审读、更多边界索引条目正文和 PDF 出版流程仍需继续推进。

## 源码基线

- 本书项目仓库：`/Volumes/PHILIPS/programs/PIC/PIC-tutor`
- WarpX 只读源码：`../warpx`
- 当前 WarpX 分支：`pkuHEDPbranch`
- 当前 WarpX commit：`8c488b1a9`

v0.11 只修改 `PIC-tutor` 书稿项目，不修改 `../warpx` 原仓库。章节里的源码路径和 regression 入口按上述 checkout 复核；后续若 WarpX 更新，必须重新校准源码行号和测试入口后再发布新版。

## v0.11 章节范围

| 章节 | 文件 | v0.11 状态 | 下一步缺口 |
|---|---|---|---|
| 写作说明 | `chapters/00-preface.md` | 沿用 v0.1 | 需同步最终出版路线 |
| 动理学模型 | `chapters/01-kinetic-models.md` | 沿用 v0.1 | Hockney-Eastwood、Yee 等一手文献闭环未完成 |
| PIC 总循环 | `chapters/02-pic-loop.md` | 已做 v0.2 源码校准 | 仍需把基础文献和公式变量定义做出版级补齐 |
| WarpX 主演化路径 | `chapters/03-warpx-evolve.md` | 已做 v0.2 源码校准 | `OneStep_sub1()`、JRhom、implicit 分支还需专章级精读 |
| WarpX 初始化链 | `chapters/03a-warpx-initialization.md` | 已做 v0.2 长草稿收束 | 需要拆短小节、补流程图、压缩过长审计段落 |
| 粒子推进器 | `chapters/04-particle-pushers.md` | 已做 v0.3 源码校准 | 仍需压缩多物理长段，并把更多 validation 表格图形化 |
| 沉积与形函数 | `chapters/05-deposition-shapes.md` | 已做 v0.4 源码校准 | Esirkepov、Villasenor-Buneman 论文仍需 MinerU 闭环，`ChargeDeposition` 的 ABLASTR 模板还需继续逐行展开 |
| 场求解器 | `chapters/06-field-solvers.md` | 已做 v0.7 验证入口表 | PSATD/Galilean/NCI/PML 论文仍需 MinerU 闭环，HTML 宽表格还需人工审读 |
| 边界、PML 与 AMR | `chapters/07-boundaries-amr.md` | 已做 v0.11 AMR guard-cell/regrid 闭环正文 | 需要继续把 coarse-fine substitution、transition zone 和更多 regression 条目图形化 |
| 诊断、验证与案例 | `chapters/08-diagnostics-cases.md` | 沿用 v0.1 | 需要更多本地运行图表和 reader-side analysis |
| 文献路线 | `chapters/09-literature-roadmap.md` | 沿用 v0.1 提纲 | 需要和 `docs/literature-map.md` 去重并完成优先级 |
| 符号表 | `appendices/A-symbols.md` | 沿用 v0.1 最小草稿 | 需要单位、参数、常用缩写和索引 |

## v0.11 已完成的增量

- 冻结 `manuscript/VERSION-v0.10.md`，避免重建 v0.10 时误用 v0.11 版本说明。
- 新增 `scripts/build_v11.py`，生成 `dist/pic-tutor-v0.11.md` 与 `dist/pic-tutor-v0.11.html`。
- 把 `scripts/build_v10.py` 改为读取冻结的 `manuscript/VERSION-v0.10.md`，保持 v0.10 版本说明可复现。
- 在第 7 章新增 `7.7.1 v0.11 guard-cell、通信和 regrid 的闭环`。
- 把 `GuardCellManager` 的 `ng_alloc_*` 与 `ng_FieldSolver/ng_FieldGather/ng_UpdateAux` 等阶段交换量区分开。
- 说明 subcycling、Galilean/comoving、moving window、JRhom/time-averaging、filter、PSATD FFT stencil 和 safe mode 如何共同影响 guard-cell 预算。
- 把 `WarpXComm.cpp` 中 E/B 的 PML exchange、valid-domain `FillBoundary`、single-precision wrapper、`nodal_sync` 和 safe-mode full exchange 串成一条通信语义。
- 把 `SyncCurrent()` / `SyncRho()` 的 coarse-fine source 同步写成 `coarsen -> optional buffer merge -> temporary receive -> OwnerMask de-dup -> SumBoundary` 的流程。
- 把 `WarpXRegrid.cpp::RemakeLevel()` 写成 load-balance 后的重建端，说明 field registry、EB factory、spectral solver、buffer mask、particle boundary buffer 和 diagnostics 的一致提交关系。

## 成书前必须补齐

- 每章记录最终采用的 WarpX commit，并避免同章混用未说明的历史行号。
- 每章补齐公式变量定义、参数入口、源码路径、行号和真实源码块。
- 至少为核心章节绑定一个 Example 或 Regression。
- 把 `docs/parameter-map.md` 和 `docs/example-regression-map.md` 中的资料条目回填为正文叙述。
- 按 `docs/paper-reading-workflow.md` 完成核心论文 MinerU 转换和中文讲解笔记。
- 建立稳定的 Markdown/HTML/PDF 构建流程；v0.11 仍只保证 Markdown/HTML。
- 对 public GitHub 仓库中的 PDF 和运行产物做版权与体积审计。

## v0.11 构建方式

生成合订 Markdown 和 HTML 预览：

```bash
python scripts/build_v11.py
```

生成的文件：

- `dist/pic-tutor-v0.11.md`
- `dist/pic-tutor-v0.11.html`（若本机存在 `pandoc`）
