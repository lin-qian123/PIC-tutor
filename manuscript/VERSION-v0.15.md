# PIC-tutor v0.15

版本日期：2026-06-29

## 定位

`v0.15` 是 `PIC-tutor` 的 transition-zone 测试草案版。它继承 `v0.14` 的 validation 检查清单，并继续把 dedicated transition-zone validation 推进到可落地测试设计：最小 MR 输入卡、粒子分区预期表、plotfile/openPMD 可观测面，以及需要 WarpX 测试专用 instrumentation 的位置。

本版的重点不是修改 `../warpx`，而是在书稿内给出一条后续可以提交到 WarpX regression 的测试草案。v0.15 明确了普通 Full diagnostics 能观察粒子位置、动量、rho/J 和 parser-derived particle fields，却不能直接暴露 `current_buffer_masks`、`gather_buffer_masks`、`nfine_gather`、`nfine_deposit`、`E/Bfield_cax` 与 `current_buf/rho_buf` 的内部路由。因此，草案把“可用现有诊断间接推断的检查”和“要强证明必须新增的测试专用 instrumentation”分开。

本版仍不是出版终稿。它把第 7 章从 validation 设计层推进到测试草案层；后续仍需真正实现 dedicated transition-zone test、继续补 PSATD/Galilean/NCI/PML 文献闭环、扩写更多边界索引条目，并建立 PDF 出版流程。

## 源码基线

- 本书项目仓库：`/Volumes/PHILIPS/programs/PIC/PIC-tutor`
- WarpX 只读源码：`../warpx`
- 当前 WarpX 分支：`pkuHEDPbranch`
- 当前 WarpX commit：`8c488b1a9`

v0.15 只修改 `PIC-tutor` 书稿项目，不修改 `../warpx` 原仓库。本版按当前 checkout 重新复核了 transition-zone 相关源码入口、现有 diagnostics 写法和 regression wiring；后续若 WarpX 更新，必须重新校准源码行号和测试入口后再发布新版。

## v0.14 章节范围

| 章节 | 文件 | v0.14 状态 | 下一步缺口 |
|---|---|---|---|
| 写作说明 | `chapters/00-preface.md` | 沿用 v0.1 | 需同步最终出版路线 |
| 动理学模型 | `chapters/01-kinetic-models.md` | 沿用 v0.1 | Hockney-Eastwood、Yee 等一手文献闭环未完成 |
| PIC 总循环 | `chapters/02-pic-loop.md` | 已做 v0.2 源码校准 | 仍需把基础文献和公式变量定义做出版级补齐 |
| WarpX 主演化路径 | `chapters/03-warpx-evolve.md` | 已做 v0.2 源码校准 | `OneStep_sub1()`、JRhom、implicit 分支还需专章级精读 |
| WarpX 初始化链 | `chapters/03a-warpx-initialization.md` | 已做 v0.2 长草稿收束 | 需要拆短小节、补流程图、压缩过长审计段落 |
| 粒子推进器 | `chapters/04-particle-pushers.md` | 已做 v0.3 源码校准 | 仍需压缩多物理长段，并把更多 validation 表格图形化 |
| 沉积与形函数 | `chapters/05-deposition-shapes.md` | 已做 v0.4 源码校准 | Esirkepov、Villasenor-Buneman 论文仍需 MinerU 闭环，`ChargeDeposition` 的 ABLASTR 模板还需继续逐行展开 |
| 场求解器 | `chapters/06-field-solvers.md` | 已做 v0.7 验证入口表 | PSATD/Galilean/NCI/PML 论文仍需 MinerU 闭环，HTML 宽表格还需继续审读 |
| 边界、PML 与 AMR | `chapters/07-boundaries-amr.md` | 已做 v0.15 transition-zone 测试草案 | 需要真正实现 dedicated transition-zone analysis 或 instrumentation |
| 诊断、验证与案例 | `chapters/08-diagnostics-cases.md` | 沿用 v0.1 | 需要更多本地运行图表和 reader-side analysis |
| 文献路线 | `chapters/09-literature-roadmap.md` | 沿用 v0.1 提纲 | 需要和 `docs/literature-map.md` 去重并完成优先级 |
| 符号表 | `appendices/A-symbols.md` | 沿用 v0.1 最小草稿 | 需要单位、参数、常用缩写和索引 |

## v0.15 已完成的增量

- 冻结 `manuscript/VERSION-v0.14.md`，避免重建 v0.14 时误用 v0.15 版本说明。
- 新增 `scripts/build_v15.py`，生成 `dist/pic-tutor-v0.15.md` 与 `dist/pic-tutor-v0.15.html`。
- 把 `scripts/build_v14.py` 改为读取冻结的 `manuscript/VERSION-v0.14.md`，保持 v0.14 版本说明可复现。
- 在第 7 章新增 `7.7.4 v0.15 dedicated transition-zone 测试草案`。
- 给出建议的 WarpX regression family：`Examples/Tests/amr_transition_zone/`，包含普通 buffer-width、`deposit_on_main_grid`、`gather_from_main_grid` 三类输入和统一 analysis。
- 设计最小 2D MR 输入卡骨架：固定 fine patch、单步或双步推进、deterministic multiple-particle 装填、Full diagnostics、rho/J/particle fields 输出。
- 写出粒子分区预期表，区分 interior、gather-only buffer、deposit-only buffer、both-buffer、强制 main-grid deposit 与强制 main-grid gather。
- 明确现有 diagnostics 的可观测上限：可以推断部分 gather/deposition 行为，但强证明需要额外输出 mask、`nfine_*`、route id 或 per-tile route counts。

## 成书前必须补齐

- 每章记录最终采用的 WarpX commit，并避免同章混用未说明的历史行号。
- 每章补齐公式变量定义、参数入口、源码路径、行号和真实源码块。
- 至少为核心章节绑定一个 Example 或 Regression。
- 把 `docs/parameter-map.md` 和 `docs/example-regression-map.md` 中的资料条目回填为正文叙述。
- 按 `docs/paper-reading-workflow.md` 完成核心论文 MinerU 转换和中文讲解笔记。
- 建立稳定的 Markdown/HTML/PDF 构建流程；v0.15 仍只保证 Markdown/HTML。
- 对 public GitHub 仓库中的 PDF 和运行产物做版权与体积审计。

## v0.15 构建方式

生成合订 Markdown 和 HTML 预览：

```bash
python scripts/build_v15.py
```

生成的文件：

- `dist/pic-tutor-v0.15.md`
- `dist/pic-tutor-v0.15.html`（若本机存在 `pandoc`）
