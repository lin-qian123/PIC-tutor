# PIC-tutor v0.13

版本日期：2026-06-29

## 定位

`v0.13` 是 `PIC-tutor` 的第 7 章 HTML 审读与排版收口版。它继承 `v0.12` 的 AMR coarse-fine 图形化证据，不新增物理结论，而是把成书预览中最容易影响审校的表格、长源码路径、代码块和 Mermaid 图容器先收成稳定样式。

本版的重点是把“内容已写出”推进到“可以在浏览器里审读”：第 7 章的 regression 索引表和 AMR 证据等级表要能横向滚动，长路径与 inline code 要能断行，Mermaid 源码块要保留横向滚动而不压坏正文宽度，正文栏宽要比 Pandoc 默认 `36em` 更适合技术书稿。

本版仍不是出版终稿。它解决 Markdown/HTML 预览层的第一轮排版问题；PSATD/Galilean/NCI/PML 文献闭环、更多边界索引条目正文、transition-zone 专门 validation、PDF 出版流程和版权/体积审计仍需继续推进。

## 源码基线

- 本书项目仓库：`/Volumes/PHILIPS/programs/PIC/PIC-tutor`
- WarpX 只读源码：`../warpx`
- 当前 WarpX 分支：`pkuHEDPbranch`
- 当前 WarpX commit：`8c488b1a9`

v0.13 只修改 `PIC-tutor` 书稿项目，不修改 `../warpx` 原仓库。本版没有重核新的 WarpX 源码行号；章节里的源码路径和 regression 入口沿用 v0.12 复核结果。后续若 WarpX 更新，必须重新校准源码行号和测试入口后再发布新版。

## v0.13 章节范围

| 章节 | 文件 | v0.13 状态 | 下一步缺口 |
|---|---|---|---|
| 写作说明 | `chapters/00-preface.md` | 沿用 v0.1 | 需同步最终出版路线 |
| 动理学模型 | `chapters/01-kinetic-models.md` | 沿用 v0.1 | Hockney-Eastwood、Yee 等一手文献闭环未完成 |
| PIC 总循环 | `chapters/02-pic-loop.md` | 已做 v0.2 源码校准 | 仍需把基础文献和公式变量定义做出版级补齐 |
| WarpX 主演化路径 | `chapters/03-warpx-evolve.md` | 已做 v0.2 源码校准 | `OneStep_sub1()`、JRhom、implicit 分支还需专章级精读 |
| WarpX 初始化链 | `chapters/03a-warpx-initialization.md` | 已做 v0.2 长草稿收束 | 需要拆短小节、补流程图、压缩过长审计段落 |
| 粒子推进器 | `chapters/04-particle-pushers.md` | 已做 v0.3 源码校准 | 仍需压缩多物理长段，并把更多 validation 表格图形化 |
| 沉积与形函数 | `chapters/05-deposition-shapes.md` | 已做 v0.4 源码校准 | Esirkepov、Villasenor-Buneman 论文仍需 MinerU 闭环，`ChargeDeposition` 的 ABLASTR 模板还需继续逐行展开 |
| 场求解器 | `chapters/06-field-solvers.md` | 已做 v0.7 验证入口表 | PSATD/Galilean/NCI/PML 论文仍需 MinerU 闭环，HTML 宽表格还需继续审读 |
| 边界、PML 与 AMR | `chapters/07-boundaries-amr.md` | 已做 v0.13 HTML 可读性收口 | 需要继续补更专门的 transition-zone validation |
| 诊断、验证与案例 | `chapters/08-diagnostics-cases.md` | 沿用 v0.1 | 需要更多本地运行图表和 reader-side analysis |
| 文献路线 | `chapters/09-literature-roadmap.md` | 沿用 v0.1 提纲 | 需要和 `docs/literature-map.md` 去重并完成优先级 |
| 符号表 | `appendices/A-symbols.md` | 沿用 v0.1 最小草稿 | 需要单位、参数、常用缩写和索引 |

## v0.13 已完成的增量

- 冻结 `manuscript/VERSION-v0.12.md`，避免重建 v0.12 时误用 v0.13 版本说明。
- 新增 `scripts/build_v13.py`，生成 `dist/pic-tutor-v0.13.md` 与 `dist/pic-tutor-v0.13.html`。
- 把 `scripts/build_v12.py` 改为读取冻结的 `manuscript/VERSION-v0.12.md`，保持 v0.12 版本说明可复现。
- 新增 `manuscript/assets/pic-tutor-html-style.html`，由 v0.13 构建脚本通过 Pandoc `--include-in-header` 注入 HTML。
- 扩大 HTML 正文最大宽度，并给 TOC、表格、代码块、inline code、Mermaid 源码块和打印视图提供项目级样式。
- 保持第 7 章 v0.12 的 AMR coarse-fine 物理内容不变，只把浏览器审读体验先稳定下来。

## 成书前必须补齐

- 每章记录最终采用的 WarpX commit，并避免同章混用未说明的历史行号。
- 每章补齐公式变量定义、参数入口、源码路径、行号和真实源码块。
- 至少为核心章节绑定一个 Example 或 Regression。
- 把 `docs/parameter-map.md` 和 `docs/example-regression-map.md` 中的资料条目回填为正文叙述。
- 按 `docs/paper-reading-workflow.md` 完成核心论文 MinerU 转换和中文讲解笔记。
- 建立稳定的 Markdown/HTML/PDF 构建流程；v0.13 仍只保证 Markdown/HTML。
- 对 public GitHub 仓库中的 PDF 和运行产物做版权与体积审计。

## v0.13 构建方式

生成合订 Markdown 和 HTML 预览：

```bash
python scripts/build_v13.py
```

生成的文件：

- `dist/pic-tutor-v0.13.md`
- `dist/pic-tutor-v0.13.html`（若本机存在 `pandoc`）
