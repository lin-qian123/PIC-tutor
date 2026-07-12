# PIC-tutor v0.39

版本日期：2026-07-02

## 定位

`v0.39` 是 `PIC-tutor` 的 deposition paper-backed assets 版。它继承 `v0.38` 已经完成的 current-deposition source-closure 基线，但这次不再把第 5 章停在“源码主文已冻结、关键文献仍主要是缺口目录”的状态，而是继续把 `Esirkepov 2001` 与 `Villasenor-Buneman 1992` 两条 charge-conserving 主线都推进到项目内可审读的论文资产层。当前模块的闭合点已经从“源码主线成形”推进成“源码主线之外，最关键的两篇沉积主文献也都已有本地 PDF、MinerU 和第一轮中文讲解，剩余工作转成公式级精读与正文回写”。

本版仍不修改 `../warpx`。新增的核心事实是：`references/04_particle_pushers_deposition_shapes/` 下两篇最关键的 charge-conserving deposition 主文献现在都已经落成项目内可读资产。`Esirkepov 2001` 已补入作者 arXiv 预印本、MinerU Markdown、`images/`、`reading-log.md` 和第一轮中文讲解；`Villasenor-Buneman 1992` 也已从本机现成 PDF/MinerU 资产 materialize 到项目目录，并补齐相同结构的论文专属材料。也就是说，`v0.39` 完成的是“把第 5 章两条主文献从 audit/gap 状态推进到第一轮 paper-backed 资产状态”，而不是提前声称已经完成公式级精读或出版级正文回写。

本版仍不是出版终稿。它继续保留 `Esirkepov 2001` 的 CPC 定稿 PDF 对照，也继续保留 `Villasenor-Buneman 1992` 与 `Esirkepov 2001` 两篇论文都还只是第一轮结构精读、尚未做公式级逐项展开的现实边界；第 5 章 `ChargeDeposition` ABLASTR 模板与部分 implicit 路径也仍可进一步精修。第 6 章 upstream handoff 和第 7 章 Lee/Vay 论文闭环同样未结束。后续应优先补齐 `Esirkepov 2001` 的发表版对照，并把 `Esirkepov/Villasenor` 两篇论文系统回写到第 5 章，再把这一章从“源码主文闭环”推进到更完整的“论文-源码双闭环”。

## 源码基线

- 本书项目仓库：`/Volumes/PHILIPS/programs/PIC/PIC-tutor`
- WarpX 只读源码：`../warpx`
- 当前 WarpX 分支：`pkuHEDPbranch`
- 当前 WarpX commit：`8c488b1a9`

v0.39 只修改 `PIC-tutor` 书稿项目，不修改 `../warpx` 原仓库。本版继续以 v0.38 已核定的第 5 章源码主文为基础，同步更新 `references/04_particle_pushers_deposition_shapes/` 下两篇主文献的项目内资产、`README.md` / `TODO.md` / `manuscript/README.md` / 第 9 章路线图中的状态说明，并重建当前合订稿。后续若 WarpX 更新，必须重新校准源码行号、沉积入口和 regression 锚点后再发布新版。

## v0.39 章节范围

| 章节 | 文件 | v0.39 状态 | 下一步缺口 |
|---|---|---|---|
| 写作说明 | `chapters/00-preface.md` | 沿用 v0.1 | 需同步最终出版路线 |
| 动理学模型 | `chapters/01-kinetic-models.md` | 沿用 v0.1 | Hockney-Eastwood、Yee 等一手文献闭环未完成 |
| PIC 总循环 | `chapters/02-pic-loop.md` | 已做 v0.2 源码校准 | 仍需把基础文献和公式变量定义做出版级补齐 |
| WarpX 主演化路径 | `chapters/03-warpx-evolve.md` | 已做 v0.2 源码校准 | `OneStep_sub1()`、JRhom、implicit 分支还需专章级精读 |
| WarpX 初始化链 | `chapters/03a-warpx-initialization.md` | 已做 v0.2 长草稿收束 | 需要拆短小节、补流程图、压缩过长审计段落 |
| 粒子推进器 | `chapters/04-particle-pushers.md` | 已做 v0.3 源码校准 | 仍需压缩多物理长段，并把更多 validation 表格图形化 |
| 沉积与形函数 | `chapters/05-deposition-shapes.md` | 已保留 v0.38 的源码主文闭环，并在 v0.39 把 `Esirkepov 2001` 与 `Villasenor-Buneman 1992` 都推进到项目内 paper-backed 资产状态 | 仍需为 `Esirkepov 2001` 补齐 CPC 定稿对照，并继续深化两篇论文的公式级讲解与正文回写，再继续精修 `ChargeDeposition` 的 ABLASTR 模板与部分 implicit 路径 |
| 场求解器 | `chapters/06-field-solvers.md` | 已补 Lehe/Kirchen/Godfrey 文献闭环、PSATD/NCI 源码机制对照表，并在 v0.26-v0.36 连续收口 comoving 与 RZ validation：当前已具备 comoving handoff/staging 工具链，以及 RZ JRhom LL2 的 repeated/MPI helper、handoff bundle 与 target-checkout workflow | 仍需决定是否真正在目标 WarpX checkout 上 staging 并上提；若不继续上提，就切到下一个成书模块 |
| 边界、PML 与 AMR | `chapters/07-boundaries-amr.md` | 已在 v0.25 增补 LeeCPC2015 论文-源码公式核对清单，把 PML profile、FD PML、PSATD PML、`C1-C25`、Galilean、cleaning 和 RZ 分支的待证项拆开 | 仍需取得 Lee/Vay 授权 PDF、完成 MinerU 逐段讲解，并实现 dedicated transition-zone regression |
| 诊断、验证与案例 | `chapters/08-diagnostics-cases.md` | 沿用 v0.1 | 需要更多本地运行图表和 reader-side analysis |
| 文献路线 | `chapters/09-literature-roadmap.md` | 已改写为 evidence-tier 路线图，并把第 5 章最关键两篇 deposition 主文献更新到 paper-backed 状态 | 仍需继续消化 `docs/literature-map.md` 中可并入正文的旧条目，并推动下一批优先论文 materialize |
| 符号表 | `appendices/A-symbols.md` | 沿用 v0.1 最小草稿 | 需要单位、参数、常用缩写和索引 |

## v0.39 已完成的增量

- 冻结 `manuscript/VERSION-v0.38.md`，避免重建 v0.38 时误用 v0.39 版本说明。
- 新增 `scripts/build_v39.py`，生成 `dist/pic-tutor-v0.39.md` 与 `dist/pic-tutor-v0.39.html`。
- 将 `Esirkepov 2001` 作者 arXiv 预印本 materialize 到项目目录，补齐本地 PDF、MinerU Markdown、`images/`、`reading-log.md` 与第一轮中文讲解，并把 access audit 从“未 ingest”推进到“preprint-backed first pass”。
- 将 `Villasenor-Buneman 1992` 的本机现成 PDF/MinerU 资产 materialize 到项目目录，补齐本地 PDF、Markdown、`images/`、`reading-log.md` 与第一轮中文讲解，并把 access audit 从“source-only gap”推进到“paper-backed first pass”。
- 更新第 5 章、第 9 章、`README.md`、`TODO.md` 与 `manuscript/README.md`，把第 5 章最关键两条 charge-conserving 主线统一标记为“已有第一轮项目内论文资产，剩余工作转为公式级精读与正文回写”。

## 成书前必须补齐

- 每章记录最终采用的 WarpX commit，并避免同章混用未说明的历史行号。
- 每章补齐公式变量定义、参数入口、源码路径、行号和真实源码块。
- 至少为核心章节绑定一个 Example 或 Regression。
- 把 `docs/parameter-map.md` 和 `docs/example-regression-map.md` 中的资料条目回填为正文叙述。
- 按 `docs/paper-reading-workflow.md` 完成核心论文 MinerU 转换和中文讲解笔记。
- 建立稳定的 Markdown/HTML/PDF 构建流程；v0.39 仍只保证 Markdown/HTML。
- 对 public GitHub 仓库中的 PDF 和运行产物做版权与体积审计。

## v0.39 构建方式

生成合订 Markdown 和 HTML 预览：

```bash
python scripts/build_v39.py
```

生成的文件：

- `dist/pic-tutor-v0.39.md`
- `dist/pic-tutor-v0.39.html`（若本机存在 `pandoc`）
