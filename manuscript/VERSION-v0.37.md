# PIC-tutor v0.37

版本日期：2026-07-02

## 定位

`v0.37` 是 `PIC-tutor` 的 deposition primary-literature access-audit 版。它继承 `v0.36` 已经完成的 target-checkout workflow 书稿基线，但这次不继续扩写第 6 章工具链，而是回到第 5 章沉积主线，把两篇最关键的一手文献 `Esirkepov 2001` 与 `Villasenor-Buneman 1992` 从“路线图里提到但没有落地资产”的状态，推进到已经具备 paper-specific 目录、访问审计、源码映射准备笔记和正文边界声明的可接续状态。也就是说，当前模块的闭合点已经从“知道缺哪两篇论文”推进成“缺口目录、访问证据、正文边界与后续采集动作都已经固定下来”。

本版仍不修改 `../warpx`。新增的核心事实是：当前 `references/04_particle_pushers_deposition_shapes/` 下已经新增 `Esirkepov 2001` 与 `Villasenor-Buneman 1992` 的 paper-specific 缺口目录，每篇都包含 `README.md`、`access-audit.md` 和源码映射准备笔记。Crossref 与 OpenAlex 已经把书目信息、DOI 和闭源访问状态核定清楚，ScienceDirect 直接 PDF 端点在本机环境中返回 HTTP 403 也已写入审计。因此，`v0.37` 完成的是“把第 5 章主文献缺口目录化并审计清楚”，而不是提前声称已经取得 PDF、完成 MinerU 或完成逐段中文讲解。

本版仍不是出版终稿。它继续保留 `Esirkepov 2001` 与 `Villasenor-Buneman 1992` 的授权 PDF/MinerU 缺口，也继续保留 LeeCPC2015 PDF/MinerU 缺口和第 6 章尚未真正上提到 WarpX upstream 的现实边界；后续仍应优先补全文获取，再决定是否把第 5 章推进到论文-源码双闭环。

## 源码基线

- 本书项目仓库：`/Volumes/PHILIPS/programs/PIC/PIC-tutor`
- WarpX 只读源码：`../warpx`
- 当前 WarpX 分支：`pkuHEDPbranch`
- 当前 WarpX commit：`8c488b1a9`

v0.37 只修改 `PIC-tutor` 书稿项目，不修改 `../warpx` 原仓库。本版继续按当前 checkout 核对 `ShapeFactors.H`、`WarpXParticleContainer.cpp`、`CurrentDeposition.H`、`ChargeDeposition.H`、`Examples/Tests/langmuir/analysis_utils.py` 和 `Examples/Tests/vay_deposition/analysis.py` 与第 5 章正文的对应关系，同时把 `Esirkepov 2001`、`Villasenor-Buneman 1992` 的 DOI、访问状态、缺口原因和后续源码映射任务写回 paper-specific 目录与第 9 章路线图。后续若 WarpX 更新，必须重新校准源码行号、沉积入口和 regression 锚点后再发布新版。

## v0.37 章节范围

| 章节 | 文件 | v0.37 状态 | 下一步缺口 |
|---|---|---|---|
| 写作说明 | `chapters/00-preface.md` | 沿用 v0.1 | 需同步最终出版路线 |
| 动理学模型 | `chapters/01-kinetic-models.md` | 沿用 v0.1 | Hockney-Eastwood、Yee 等一手文献闭环未完成 |
| PIC 总循环 | `chapters/02-pic-loop.md` | 已做 v0.2 源码校准 | 仍需把基础文献和公式变量定义做出版级补齐 |
| WarpX 主演化路径 | `chapters/03-warpx-evolve.md` | 已做 v0.2 源码校准 | `OneStep_sub1()`、JRhom、implicit 分支还需专章级精读 |
| WarpX 初始化链 | `chapters/03a-warpx-initialization.md` | 已做 v0.2 长草稿收束 | 需要拆短小节、补流程图、压缩过长审计段落 |
| 粒子推进器 | `chapters/04-particle-pushers.md` | 已做 v0.3 源码校准 | 仍需压缩多物理长段，并把更多 validation 表格图形化 |
| 沉积与形函数 | `chapters/05-deposition-shapes.md` | 已做 v0.4 源码校准，并在 v0.37 为 `Esirkepov 2001` 与 `Villasenor-Buneman 1992` 建立 paper-specific 目录、access audit 和源码映射准备笔记 | 仍需拿到授权 PDF、完成 MinerU 逐段讲解，并继续展开 `ChargeDeposition` 的 ABLASTR 模板与 implicit 路径 |
| 场求解器 | `chapters/06-field-solvers.md` | 已补 Lehe/Kirchen/Godfrey 文献闭环、PSATD/NCI 源码机制对照表，并在 v0.26-v0.36 连续收口 comoving 与 RZ validation：当前已具备 comoving handoff/staging 工具链，以及 RZ JRhom LL2 的 repeated/MPI helper、handoff bundle 与 target-checkout workflow | 仍需决定是否真正在目标 WarpX checkout 上 staging 并上提；若不继续上提，就切到下一个成书模块 |
| 边界、PML 与 AMR | `chapters/07-boundaries-amr.md` | 已在 v0.25 增补 LeeCPC2015 论文-源码公式核对清单，把 PML profile、FD PML、PSATD PML、`C1-C25`、Galilean、cleaning 和 RZ 分支的待证项拆开 | 仍需取得 Lee/Vay 授权 PDF、完成 MinerU 逐段讲解，并实现 dedicated transition-zone regression |
| 诊断、验证与案例 | `chapters/08-diagnostics-cases.md` | 沿用 v0.1 | 需要更多本地运行图表和 reader-side analysis |
| 文献路线 | `chapters/09-literature-roadmap.md` | 已改写为 evidence-tier 路线图，并把第 5 章 deposition 文献缺口固定成可接续目录与审计状态 | 仍需继续消化 `docs/literature-map.md` 中可并入正文的旧条目，并推动下一批优先论文 materialize |
| 符号表 | `appendices/A-symbols.md` | 沿用 v0.1 最小草稿 | 需要单位、参数、常用缩写和索引 |

## v0.37 已完成的增量

- 冻结 `manuscript/VERSION-v0.36.md`，避免重建 v0.36 时误用 v0.37 版本说明。
- 新增 `scripts/build_v37.py`，生成 `dist/pic-tutor-v0.37.md` 与 `dist/pic-tutor-v0.37.html`。
- 为 `Esirkepov 2001` 新增 paper-specific 目录，包含 `README.md`、`access-audit.md` 和源码映射准备笔记，固定 DOI、访问状态、当前缺口和后续正文回填点。
- 为 `Villasenor-Buneman 1992` 新增 paper-specific 目录，包含 `README.md`、`access-audit.md` 和源码映射准备笔记，固定 DOI、访问状态、当前缺口和后续正文回填点。
- 更新第 5 章，把当前沉积主文献的状态明确改写为“源码已核、主文未闭环”，避免把源码校准误写成论文-源码双闭环。
- 更新第 9 章，把 deposition 线从笼统的“缺论文”改写成 evidence-tier 路线图中的已落地 gap directories + access audits，并重排 acquisition 优先级。
- 更新 `README.md`、`TODO.md` 和 `manuscript/README.md`，把这轮文献缺口目录化工作收口为当前版本资产。

## 成书前必须补齐

- 每章记录最终采用的 WarpX commit，并避免同章混用未说明的历史行号。
- 每章补齐公式变量定义、参数入口、源码路径、行号和真实源码块。
- 至少为核心章节绑定一个 Example 或 Regression。
- 把 `docs/parameter-map.md` 和 `docs/example-regression-map.md` 中的资料条目回填为正文叙述。
- 按 `docs/paper-reading-workflow.md` 完成核心论文 MinerU 转换和中文讲解笔记。
- 建立稳定的 Markdown/HTML/PDF 构建流程；v0.37 仍只保证 Markdown/HTML。
- 对 public GitHub 仓库中的 PDF 和运行产物做版权与体积审计。

## v0.37 构建方式

生成合订 Markdown 和 HTML 预览：

```bash
python scripts/build_v37.py
```

生成的文件：

- `dist/pic-tutor-v0.37.md`
- `dist/pic-tutor-v0.37.html`（若本机存在 `pandoc`）
