# PIC-tutor v0.34

版本日期：2026-06-30

## 定位

`v0.34` 是 `PIC-tutor` 的 comoving PSATD first-stage upstream handoff 版。它继承 `v0.33` 的 patch asset reproducibility，不再只把第一阶段 patch 停留在“可重建 helper + diff + provenance note”的层面，而是继续把 upstream 交付所需的提交文本资产也统一收进 ledger 驱动生成链。

本版仍不修改 `../warpx`。第 6 章继续围绕 `6.8.3` / `6.8.4` 收口 comoving PSATD，新增的关键事实是：当前第一阶段 `finite + spike` patch 已经不仅有稳定阈值来源和最小代码草案，还具备提交时可直接复用的 `submission packet` 与 `PR draft`。因此，`v0.34` 完成的是“把 patch 草案升级成可交付的 upstream handoff bundle”，而不是提前声称 WarpX 侧最终 energy gate 已经定稿。

本版仍不是出版终稿。它继续保留 LeeCPC2015 PDF/MinerU 缺口，也保留 comoving WarpX patch 尚未真正上提这一现实边界；后续仍应在 handoff bundle 基础上决定是否直接按 `finite + spike` 提第一阶段 patch，或先在更接近 upstream regression 的 repeated/MPI 设置下重做 comoving contrast。

## 源码基线

- 本书项目仓库：`/Volumes/PHILIPS/programs/PIC/PIC-tutor`
- WarpX 只读源码：`../warpx`
- 当前 WarpX 分支：`pkuHEDPbranch`
- 当前 WarpX commit：`8c488b1a9`

v0.34 只修改 `PIC-tutor` 书稿项目，不修改 `../warpx` 原仓库。本版继续按当前 checkout 核对 `Examples/Tests/nci_psatd_stability/CMakeLists.txt:28-38`、`inputs_test_2d_comoving_psatd_hybrid:1-138`、`analysis_galilean.py:1-111`、`analysis_psatd_CC1.py`、`SpectralSolver.cpp`、`WarpX.cpp` 和参数文档里的 `psatd.v_comoving` 语义，并把对应本地运行、ledger 路径和生成脚本路径写入 provenance。后续若 WarpX 更新，必须重新校准源码行号、文档段落、测试入口和 ledger 样本后再发布新版。

## v0.34 章节范围

| 章节 | 文件 | v0.34 状态 | 下一步缺口 |
|---|---|---|---|
| 写作说明 | `chapters/00-preface.md` | 沿用 v0.1 | 需同步最终出版路线 |
| 动理学模型 | `chapters/01-kinetic-models.md` | 沿用 v0.1 | Hockney-Eastwood、Yee 等一手文献闭环未完成 |
| PIC 总循环 | `chapters/02-pic-loop.md` | 已做 v0.2 源码校准 | 仍需把基础文献和公式变量定义做出版级补齐 |
| WarpX 主演化路径 | `chapters/03-warpx-evolve.md` | 已做 v0.2 源码校准 | `OneStep_sub1()`、JRhom、implicit 分支还需专章级精读 |
| WarpX 初始化链 | `chapters/03a-warpx-initialization.md` | 已做 v0.2 长草稿收束 | 需要拆短小节、补流程图、压缩过长审计段落 |
| 粒子推进器 | `chapters/04-particle-pushers.md` | 已做 v0.3 源码校准 | 仍需压缩多物理长段，并把更多 validation 表格图形化 |
| 沉积与形函数 | `chapters/05-deposition-shapes.md` | 已做 v0.4 源码校准 | Esirkepov、Villasenor-Buneman 论文仍需 MinerU 闭环，`ChargeDeposition` 的 ABLASTR 模板还需继续逐行展开 |
| 场求解器 | `chapters/06-field-solvers.md` | 已补 Lehe/Kirchen/Godfrey 文献闭环、PSATD/NCI 源码机制对照表，并在 v0.26-v0.34 连续收口 comoving 系数、analysis 方案、local calibration audit、可重建 patch 资产、velocity-only cross-check 与 upstream handoff bundle | 仍需真正决定是否按当前 `finite + spike` 口径上提 WarpX patch，并在更贴近 upstream regression 的设置下收敛最终 energy gate |
| 边界、PML 与 AMR | `chapters/07-boundaries-amr.md` | 已在 v0.25 增补 LeeCPC2015 论文-源码公式核对清单，把 PML profile、FD PML、PSATD PML、`C1-C25`、Galilean、cleaning 和 RZ 分支的待证项拆开 | 仍需取得 Lee/Vay 授权 PDF、完成 MinerU 逐段讲解，并实现 dedicated transition-zone regression |
| 诊断、验证与案例 | `chapters/08-diagnostics-cases.md` | 沿用 v0.1 | 需要更多本地运行图表和 reader-side analysis |
| 文献路线 | `chapters/09-literature-roadmap.md` | 沿用 v0.1 提纲 | 需要和 `docs/literature-map.md` 去重并完成优先级 |
| 符号表 | `appendices/A-symbols.md` | 沿用 v0.1 最小草稿 | 需要单位、参数、常用缩写和索引 |

## v0.34 已完成的增量

- 冻结 `manuscript/VERSION-v0.33.md`，避免重建 v0.33 时误用 v0.34 版本说明。
- 新增 `scripts/build_v34.py`，生成 `dist/pic-tutor-v0.34.md` 与 `dist/pic-tutor-v0.34.html`。
- 把 `scripts/build_v33.py` 保持为读取冻结前的 v0.33 构建逻辑，确保 v0.33 版本说明可复现。
- 扩展 `scripts/build_comoving_first_stage_patch.py`，除 `analysis_comoving_first_stage_draft.py`、`comoving_first_stage_patch.diff`、`comoving_first_stage_provenance_note.md` 与 `comoving_first_stage_submission_packet.md` 外，再自动生成 `notes/code-reading/fieldsolver/comoving_first_stage_pr_draft.md`。
- 把第一阶段 patch 的代码资产、review claim、out-of-scope 边界和 reviewer checklist 全部绑定回同一份 ledger，减少 helper、diff、packet、PR 文本之间的人工漂移。
- 更新 `24-psatd-comoving-first-stage-patch-draft.md`、`notes/code-reading/fieldsolver/README.md`、`README.md`、`TODO.md` 和第 6 章 `6.8.4`，把当前模块从“可重建 patch 草案资产”推进为“可直接交付的 upstream handoff bundle”。

## 成书前必须补齐

- 每章记录最终采用的 WarpX commit，并避免同章混用未说明的历史行号。
- 每章补齐公式变量定义、参数入口、源码路径、行号和真实源码块。
- 至少为核心章节绑定一个 Example 或 Regression。
- 把 `docs/parameter-map.md` 和 `docs/example-regression-map.md` 中的资料条目回填为正文叙述。
- 按 `docs/paper-reading-workflow.md` 完成核心论文 MinerU 转换和中文讲解笔记。
- 建立稳定的 Markdown/HTML/PDF 构建流程；v0.34 仍只保证 Markdown/HTML。
- 对 public GitHub 仓库中的 PDF 和运行产物做版权与体积审计。

## v0.34 构建方式

生成合订 Markdown 和 HTML 预览：

```bash
python scripts/build_v34.py
```

生成的文件：

- `dist/pic-tutor-v0.34.md`
- `dist/pic-tutor-v0.34.html`（若本机存在 `pandoc`）
