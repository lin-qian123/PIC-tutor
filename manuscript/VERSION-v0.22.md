# PIC-tutor v0.22

版本日期：2026-06-29

## 定位

`v0.22` 是 `PIC-tutor` 的 PML 理论文献闭环版。它继承 `v0.21` 的 PSATD PML 源码闭环，继续把第 7 章的 PML 论证从“源码和 regression 对照”推进到“官方理论文档、WarpX 书目、PML/PSATD 论文线索和 `PsatdAlgorithmPml.cpp` 系数分层”的版本。

本版仍不修改 `../warpx`。第 7 章新增 `7.5.4 v0.22 PML 理论文献闭环：从 Berenger/APML 到 PSATD split-field 系数`。本版的核心写作边界是：Berenger/APML 解释的是连续匹配和 split-field 理论，`PML.cpp` / `SigmaBox` 解释的是实空间 sigma profile 和 damping，`PsatdAlgorithmPml.cpp` 的 `C1-C25` 解释的是 PML 子域 split components 的 pseudo-spectral Maxwell propagator；三者相关但不能混写成同一套“PML 系数”。

本版仍不是出版终稿。它新增 Lee/Vay PML 论文取证目录，并记录了 AIP 官方 PDF 在本机下载时返回 HTTP 403，因此尚未完成 PDF/MinerU/逐段中文讲解。后续应取得授权 PDF 后继续补完整论文笔记，并把 Lee/Vay 文中的 pseudo-spectral PML 反射率/效率公式逐项对应到 WarpX 当前 `PsatdAlgorithmPml.cpp`。

## 源码基线

- 本书项目仓库：`/Volumes/PHILIPS/programs/PIC/PIC-tutor`
- WarpX 只读源码：`../warpx`
- 当前 WarpX 分支：`pkuHEDPbranch`
- 当前 WarpX commit：`8c488b1a9`

v0.22 只修改 `PIC-tutor` 书稿项目，不修改 `../warpx` 原仓库。本版继续按当前 checkout 核对 `Docs/source/theory/boundary_conditions.rst`、`Docs/source/refs.bib`、`PML.cpp`、`PsatdAlgorithmPml.cpp` 和 `PsatdAlgorithmPmlRZ.cpp`。后续若 WarpX 更新，必须重新校准源码行号、文档段落和测试入口后再发布新版。

## v0.22 章节范围

| 章节 | 文件 | v0.22 状态 | 下一步缺口 |
|---|---|---|---|
| 写作说明 | `chapters/00-preface.md` | 沿用 v0.1 | 需同步最终出版路线 |
| 动理学模型 | `chapters/01-kinetic-models.md` | 沿用 v0.1 | Hockney-Eastwood、Yee 等一手文献闭环未完成 |
| PIC 总循环 | `chapters/02-pic-loop.md` | 已做 v0.2 源码校准 | 仍需把基础文献和公式变量定义做出版级补齐 |
| WarpX 主演化路径 | `chapters/03-warpx-evolve.md` | 已做 v0.2 源码校准 | `OneStep_sub1()`、JRhom、implicit 分支还需专章级精读 |
| WarpX 初始化链 | `chapters/03a-warpx-initialization.md` | 已做 v0.2 长草稿收束 | 需要拆短小节、补流程图、压缩过长审计段落 |
| 粒子推进器 | `chapters/04-particle-pushers.md` | 已做 v0.3 源码校准 | 仍需压缩多物理长段，并把更多 validation 表格图形化 |
| 沉积与形函数 | `chapters/05-deposition-shapes.md` | 已做 v0.4 源码校准 | Esirkepov、Villasenor-Buneman 论文仍需 MinerU 闭环，`ChargeDeposition` 的 ABLASTR 模板还需继续逐行展开 |
| 场求解器 | `chapters/06-field-solvers.md` | 已补 Lehe/Kirchen/Godfrey 文献闭环，并在 v0.20 增补 PSATD/NCI 源码机制对照表 | 仍需 `X1-X4` 系数逐项推导 |
| 边界、PML 与 AMR | `chapters/07-boundaries-amr.md` | 已在 v0.22 增补 Berenger/APML、WarpX `refs.bib`、Lee/Vay 文献线索和 `C1-C25` 分层说明 | 仍需取得 Lee/Vay 授权 PDF、完成 MinerU 逐段讲解，并实现 dedicated transition-zone regression |
| 诊断、验证与案例 | `chapters/08-diagnostics-cases.md` | 沿用 v0.1 | 需要更多本地运行图表和 reader-side analysis |
| 文献路线 | `chapters/09-literature-roadmap.md` | 沿用 v0.1 提纲 | 需要和 `docs/literature-map.md` 去重并完成优先级 |
| 符号表 | `appendices/A-symbols.md` | 沿用 v0.1 最小草稿 | 需要单位、参数、常用缩写和索引 |

## v0.22 已完成的增量

- 冻结 `manuscript/VERSION-v0.21.md`，避免重建 v0.21 时误用 v0.22 版本说明。
- 新增 `scripts/build_v22.py`，生成 `dist/pic-tutor-v0.22.md` 与 `dist/pic-tutor-v0.22.html`。
- 把 `scripts/build_v21.py` 改为读取冻结的 `manuscript/VERSION-v0.21.md`，保持 v0.21 版本说明可复现。
- 在第 7 章新增 `7.5.4 v0.22 PML 理论文献闭环：从 Berenger/APML 到 PSATD split-field 系数`。
- 从 WarpX 官方文档梳理 Berenger split-field、APML 阻抗匹配条件和离散指数阻尼更新的层级。
- 从 WarpX `Docs/source/refs.bib` 梳理 `Berengerjcp94`、`Vay2002`、`Vaycpc04`、`LeeCPC2015`、`Vay2000` 在本书中的角色。
- 新增 `references/08_boundaries_pml_geometry/2016_LeeVayACP2016_Efficiency_of_the_PML_with_high-order_FD_and_pseudo-spectral_Maxwell_solvers/`，记录 AIP 官方 DOI 页面、PDF 下载失败原因和中文讲解骨架。
- 明确 `PML.cpp` / `SigmaBox` 的实空间 sigma damping 与 `PsatdAlgorithmPml.cpp` 的 `C1-C25` 谱推进系数属于不同层。
- 把 `C1-C9`、`C10-C22`、`C23-C25` 分别解释成投影/交叉耦合/cleaning 三组谱空间系数，而不是 FDTD PML 的 damping profile。

## 成书前必须补齐

- 每章记录最终采用的 WarpX commit，并避免同章混用未说明的历史行号。
- 每章补齐公式变量定义、参数入口、源码路径、行号和真实源码块。
- 至少为核心章节绑定一个 Example 或 Regression。
- 把 `docs/parameter-map.md` 和 `docs/example-regression-map.md` 中的资料条目回填为正文叙述。
- 按 `docs/paper-reading-workflow.md` 完成核心论文 MinerU 转换和中文讲解笔记。
- 建立稳定的 Markdown/HTML/PDF 构建流程；v0.22 仍只保证 Markdown/HTML。
- 对 public GitHub 仓库中的 PDF 和运行产物做版权与体积审计。

## v0.22 构建方式

生成合订 Markdown 和 HTML 预览：

```bash
python scripts/build_v22.py
```

生成的文件：

- `dist/pic-tutor-v0.22.md`
- `dist/pic-tutor-v0.22.html`（若本机存在 `pandoc`）
