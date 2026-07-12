# PIC-tutor v0.38

版本日期：2026-07-02

## 定位

`v0.38` 是 `PIC-tutor` 的 current-deposition source-closure 版。它继承 `v0.37` 已经完成的 deposition primary-literature access-audit 基线，但这次不再停留在“第 5 章知道缺哪两篇关键文献、目录也已经建好”的状态，而是继续把 `CurrentDeposition.H`、`WarpXParticleContainer.cpp`、`ShapeFactors.H`、`ChargeDeposition.H` 与 `SyncCurrentAndRho()` 这一整条 current deposition 主线压成可连续审读的正文。当前模块的闭合点已经从“文献缺口与正文边界已经固定”推进成“源码主文已经成形并可冻结，剩余主要缺口收缩为 primary literature PDF/MinerU 和少量后续精修”。

本版仍不修改 `../warpx`。新增的核心事实是：第 5 章 current deposition 现在已经不仅有 paper-specific gap directories 和 access audit，也已经把 Direct、Esirkepov、Villasenor、Vay 四条路径的入口分派、shape-factor indexing/alignment、几何分支写回、RZ/球柱几何缩放、shared-memory 限制、fine/coarse source synchronization 与 `PEC` source-boundary 收口回填为稳定正文。也就是说，`v0.38` 完成的是“把沉积主线从源码摘记推进成可冻结的书稿模块”，而不是继续把关键叙述留在零散 notes 或 TODO 里。

本版仍不是出版终稿。它继续保留 `Esirkepov 2001` 的 CPC 定稿 PDF 对照，以及第 5 章 `ChargeDeposition` ABLASTR 模板与部分 implicit 路径尚可进一步精修的空间；同时虽然 `Villasenor-Buneman 1992` 已从本机现成 PDF/MinerU 资产推进成 paper-backed 目录，但这条线也还需要更细的公式级中文讲解和正文回写。第 6 章 upstream handoff 和第 7 章 Lee/Vay 论文闭环也都还未结束。后续应优先补齐 `Esirkepov 2001` 的发表版对照，并把 `Esirkepov/Villasenor` 两篇论文系统回写到第 5 章，再把这一章从“源码主文闭环”推进到更完整的“论文-源码双闭环”。

## 源码基线

- 本书项目仓库：`/Volumes/PHILIPS/programs/PIC/PIC-tutor`
- WarpX 只读源码：`../warpx`
- 当前 WarpX 分支：`pkuHEDPbranch`
- 当前 WarpX commit：`8c488b1a9`

v0.38 只修改 `PIC-tutor` 书稿项目，不修改 `../warpx` 原仓库。本版继续按当前 checkout 核对 `ShapeFactors.H`、`WarpXParticleContainer.cpp`、`CurrentDeposition.H`、`ChargeDeposition.H`、`MultiParticleContainer.cpp`、`WarpXEvolve.cpp`、`WarpXPushFieldsEM.cpp`、`Examples/Tests/langmuir/analysis_utils.py` 和 `Examples/Tests/vay_deposition/analysis.py` 与第 5 章正文的对应关系，同时把 current deposition 主线扩写所依赖的 code-reading notes、版本说明和待办边界同步回项目文档。后续若 WarpX 更新，必须重新校准源码行号、沉积入口和 regression 锚点后再发布新版。

## v0.38 章节范围

| 章节 | 文件 | v0.38 状态 | 下一步缺口 |
|---|---|---|---|
| 写作说明 | `chapters/00-preface.md` | 沿用 v0.1 | 需同步最终出版路线 |
| 动理学模型 | `chapters/01-kinetic-models.md` | 沿用 v0.1 | Hockney-Eastwood、Yee 等一手文献闭环未完成 |
| PIC 总循环 | `chapters/02-pic-loop.md` | 已做 v0.2 源码校准 | 仍需把基础文献和公式变量定义做出版级补齐 |
| WarpX 主演化路径 | `chapters/03-warpx-evolve.md` | 已做 v0.2 源码校准 | `OneStep_sub1()`、JRhom、implicit 分支还需专章级精读 |
| WarpX 初始化链 | `chapters/03a-warpx-initialization.md` | 已做 v0.2 长草稿收束 | 需要拆短小节、补流程图、压缩过长审计段落 |
| 粒子推进器 | `chapters/04-particle-pushers.md` | 已做 v0.3 源码校准 | 仍需压缩多物理长段，并把更多 validation 表格图形化 |
| 沉积与形函数 | `chapters/05-deposition-shapes.md` | 已在 v0.38 把 current deposition 主线冻结为源码主文闭环；其后 `Esirkepov 2001` 与 `Villasenor-Buneman 1992` 都已具备本地 PDF、MinerU Markdown 和第一轮中文讲解 | 仍需为 `Esirkepov 2001` 补齐 CPC 定稿对照，并继续深化两篇论文的公式级讲解与正文回写，再继续精修 `ChargeDeposition` 的 ABLASTR 模板与部分 implicit 路径 |
| 场求解器 | `chapters/06-field-solvers.md` | 已补 Lehe/Kirchen/Godfrey 文献闭环、PSATD/NCI 源码机制对照表，并在 v0.26-v0.36 连续收口 comoving 与 RZ validation：当前已具备 comoving handoff/staging 工具链，以及 RZ JRhom LL2 的 repeated/MPI helper、handoff bundle 与 target-checkout workflow | 仍需决定是否真正在目标 WarpX checkout 上 staging 并上提；若不继续上提，就切到下一个成书模块 |
| 边界、PML 与 AMR | `chapters/07-boundaries-amr.md` | 已在 v0.25 增补 LeeCPC2015 论文-源码公式核对清单，把 PML profile、FD PML、PSATD PML、`C1-C25`、Galilean、cleaning 和 RZ 分支的待证项拆开 | 仍需取得 Lee/Vay 授权 PDF、完成 MinerU 逐段讲解，并实现 dedicated transition-zone regression |
| 诊断、验证与案例 | `chapters/08-diagnostics-cases.md` | 沿用 v0.1 | 需要更多本地运行图表和 reader-side analysis |
| 文献路线 | `chapters/09-literature-roadmap.md` | 已改写为 evidence-tier 路线图，并把第 5 章 deposition 文献缺口固定成可接续目录与审计状态 | 仍需继续消化 `docs/literature-map.md` 中可并入正文的旧条目，并推动下一批优先论文 materialize |
| 符号表 | `appendices/A-symbols.md` | 沿用 v0.1 最小草稿 | 需要单位、参数、常用缩写和索引 |

## v0.38 已完成的增量

- 冻结 `manuscript/VERSION-v0.37.md`，避免重建 v0.37 时误用 v0.38 版本说明。
- 新增 `scripts/build_v38.py`，生成 `dist/pic-tutor-v0.38.md` 与 `dist/pic-tutor-v0.38.html`。
- 为第 5 章新增并回填 `notes/code-reading/particles/37-43`，把 Direct 与 Villasenor 边界裁剪、shape-factor indexing/alignment、`1D_Z / RCYLINDER / RSPHERE` 写回、RZ inverse-volume scaling、`DepositCurrent()` 分派合同、Villasenor segment loop、显式/隐式共用 kernel 等源码事实压进稳定主线。
- 重写第 5 章 current deposition 主文，减少重复的开发记录口吻，把 `DepositCurrent()`、`CurrentDeposition.H`、`DepositCharge()` 与 `SyncCurrentAndRho()` 接成连续叙述。
- 把 `ApplyRhofieldBoundary(...)` / `ApplyJfieldBoundary(...)` 的 source-boundary 语义、`J_cp/fine_lev_cp/mf_comm` 的 fine/coarse synchronization 容器角色，以及 RZ/球柱几何的最终电流密度缩放明确收口到正文。
- 更新 `README.md`、`TODO.md` 和 `manuscript/README.md`，把第 5 章 current deposition 模块正式标记为“源码主文已冻结，剩余工作主要是 primary literature 与精修”。

## 成书前必须补齐

- 每章记录最终采用的 WarpX commit，并避免同章混用未说明的历史行号。
- 每章补齐公式变量定义、参数入口、源码路径、行号和真实源码块。
- 至少为核心章节绑定一个 Example 或 Regression。
- 把 `docs/parameter-map.md` 和 `docs/example-regression-map.md` 中的资料条目回填为正文叙述。
- 按 `docs/paper-reading-workflow.md` 完成核心论文 MinerU 转换和中文讲解笔记。
- 建立稳定的 Markdown/HTML/PDF 构建流程；v0.38 仍只保证 Markdown/HTML。
- 对 public GitHub 仓库中的 PDF 和运行产物做版权与体积审计。

## v0.38 构建方式

生成合订 Markdown 和 HTML 预览：

```bash
python scripts/build_v38.py
```

生成的文件：

- `dist/pic-tutor-v0.38.md`
- `dist/pic-tutor-v0.38.html`（若本机存在 `pandoc`）
