# PIC-tutor v0.33

版本日期：2026-06-30

## 定位

`v0.33` 是 `PIC-tutor` 的 comoving PSATD first-stage patch asset reproducibility 版。它继承 `v0.32` 的 local calibration audit，不再把第一阶段 patch helper 和 unified diff 停留在手工草案层，而是把它们收敛成由 ledger 驱动重建的可复生成资产。

本版仍不修改 `../warpx`。第 6 章继续围绕 `6.8.3` / `6.8.4` 收口 comoving PSATD，新增的关键事实是：第一阶段 `finite + spike` patch 草案现在已经有了明确的单一真源，即 `runs/fieldsolver-validation/comoving-reference-ledgers/comoving-stable-vs-no-comoving.json`。`analysis_comoving_first_stage_draft.py` 和 `comoving_first_stage_patch.diff` 可由 `scripts/build_comoving_first_stage_patch.py` 自动回填，其中候选 `SPIKE_RATIO_MAX` 默认来自 `spike_ratio_ref_stable * 1.001`。因此，`v0.33` 完成的是“把 patch 草案变成可重建资产”，而不是提前声称 WarpX 侧最终 energy gate 已经定稿。

本版仍不是出版终稿。它继续保留 LeeCPC2015 PDF/MinerU 缺口，也保留 comoving WarpX patch 尚未提交这一现实边界；后续仍应补齐 Lee/Vay PML 论文全文，并在更接近 upstream regression 的 MPI/并行设置下重复 comoving contrast，或转向 RZ validation 强判据表。

## 源码基线

- 本书项目仓库：`/Volumes/PHILIPS/programs/PIC/PIC-tutor`
- WarpX 只读源码：`../warpx`
- 当前 WarpX 分支：`pkuHEDPbranch`
- 当前 WarpX commit：`8c488b1a9`

v0.33 只修改 `PIC-tutor` 书稿项目，不修改 `../warpx` 原仓库。本版继续按当前 checkout 核对 `Examples/Tests/nci_psatd_stability/CMakeLists.txt:28-38`、`inputs_test_2d_comoving_psatd_hybrid:1-138`、`analysis_galilean.py:1-111`、`analysis_psatd_CC1.py`、`SpectralSolver.cpp`、`WarpX.cpp` 和参数文档里的 `psatd.v_comoving` 语义，并把对应本地运行、ledger 路径和生成脚本路径写入 provenance。后续若 WarpX 更新，必须重新校准源码行号、文档段落、测试入口和 ledger 样本后再发布新版。

## v0.33 章节范围

| 章节 | 文件 | v0.29 状态 | 下一步缺口 |
|---|---|---|---|
| 写作说明 | `chapters/00-preface.md` | 沿用 v0.1 | 需同步最终出版路线 |
| 动理学模型 | `chapters/01-kinetic-models.md` | 沿用 v0.1 | Hockney-Eastwood、Yee 等一手文献闭环未完成 |
| PIC 总循环 | `chapters/02-pic-loop.md` | 已做 v0.2 源码校准 | 仍需把基础文献和公式变量定义做出版级补齐 |
| WarpX 主演化路径 | `chapters/03-warpx-evolve.md` | 已做 v0.2 源码校准 | `OneStep_sub1()`、JRhom、implicit 分支还需专章级精读 |
| WarpX 初始化链 | `chapters/03a-warpx-initialization.md` | 已做 v0.2 长草稿收束 | 需要拆短小节、补流程图、压缩过长审计段落 |
| 粒子推进器 | `chapters/04-particle-pushers.md` | 已做 v0.3 源码校准 | 仍需压缩多物理长段，并把更多 validation 表格图形化 |
| 沉积与形函数 | `chapters/05-deposition-shapes.md` | 已做 v0.4 源码校准 | Esirkepov、Villasenor-Buneman 论文仍需 MinerU 闭环，`ChargeDeposition` 的 ABLASTR 模板还需继续逐行展开 |
| 场求解器 | `chapters/06-field-solvers.md` | 已补 Lehe/Kirchen/Godfrey 文献闭环、PSATD/NCI 源码机制对照表，并在 v0.26 增补 Cartesian `X1-X4`、v0.27 增补 time-averaging `Psi/Y`、v0.28 增补 JRhom `Y1-Y8`、v0.29 增补 RZ/Galilean RZ 系数边界、v0.30 增补 comoving PSATD 系数与验证边界、v0.31 增补 comoving regression analysis 升级方案、v0.32 增补本地 stable/contrast ledger audit、v0.33 增补 first-stage patch 资产重建链 | 仍需真正提交 WarpX 侧 `analysis_comoving.py`，并在更贴近 upstream regression 的设置下收敛最终 energy gate |
| 边界、PML 与 AMR | `chapters/07-boundaries-amr.md` | 已在 v0.25 增补 LeeCPC2015 论文-源码公式核对清单，把 PML profile、FD PML、PSATD PML、`C1-C25`、Galilean、cleaning 和 RZ 分支的待证项拆开 | 仍需取得 Lee/Vay 授权 PDF、完成 MinerU 逐段讲解，并实现 dedicated transition-zone regression |
| 诊断、验证与案例 | `chapters/08-diagnostics-cases.md` | 沿用 v0.1 | 需要更多本地运行图表和 reader-side analysis |
| 文献路线 | `chapters/09-literature-roadmap.md` | 沿用 v0.1 提纲 | 需要和 `docs/literature-map.md` 去重并完成优先级 |
| 符号表 | `appendices/A-symbols.md` | 沿用 v0.1 最小草稿 | 需要单位、参数、常用缩写和索引 |

## v0.33 已完成的增量

- 冻结 `manuscript/VERSION-v0.32.md`，避免重建 v0.32 时误用 v0.33 版本说明。
- 新增 `scripts/build_v33.py`，生成 `dist/pic-tutor-v0.33.md` 与 `dist/pic-tutor-v0.33.html`。
- 把 `scripts/build_v32.py` 保持为读取冻结前的 v0.32 构建逻辑，确保 v0.32 版本说明可复现。
- 新增 `scripts/build_comoving_first_stage_patch.py`，从 `runs/fieldsolver-validation/comoving-reference-ledgers/comoving-stable-vs-no-comoving.json` 自动生成 `analysis_comoving_first_stage_draft.py` 和 `comoving_first_stage_patch.diff`。
- 用当前 ledger 的 `spike_ratio_ref_stable = 1.1103719982074416` 与默认 `safety_factor = 1.001` 自动回填候选 `SPIKE_RATIO_MAX = 1.1114823702056489`，把阈值来源、helper 内容和 patch wiring 绑定回同一份 reference。
- 更新 `24-psatd-comoving-first-stage-patch-draft.md`、`notes/code-reading/fieldsolver/README.md` 和第 6 章 `6.8.4`，把“最小 patch 草案”升级为“可重建 patch 草案资产”。

## 成书前必须补齐

- 每章记录最终采用的 WarpX commit，并避免同章混用未说明的历史行号。
- 每章补齐公式变量定义、参数入口、源码路径、行号和真实源码块。
- 至少为核心章节绑定一个 Example 或 Regression。
- 把 `docs/parameter-map.md` 和 `docs/example-regression-map.md` 中的资料条目回填为正文叙述。
- 按 `docs/paper-reading-workflow.md` 完成核心论文 MinerU 转换和中文讲解笔记。
- 建立稳定的 Markdown/HTML/PDF 构建流程；v0.29 仍只保证 Markdown/HTML。
- 对 public GitHub 仓库中的 PDF 和运行产物做版权与体积审计。

## v0.33 构建方式

生成合订 Markdown 和 HTML 预览：

```bash
python scripts/build_v33.py
```

生成的文件：

- `dist/pic-tutor-v0.33.md`
- `dist/pic-tutor-v0.33.html`（若本机存在 `pandoc`）
