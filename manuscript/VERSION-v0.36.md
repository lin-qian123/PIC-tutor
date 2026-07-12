# PIC-tutor v0.36

版本日期：2026-07-02

## 定位

`v0.36` 是 `PIC-tutor` 的 RZ JRhom LL2 first-stage target-checkout workflow 版。它继承 `v0.35` 已经完成的 repeated/MPI helper 与 handoff bundle，但这次不再停在“资产已经生成”，而是把这条线继续推进到可以对目标 WarpX checkout 做 preview、audit、report 和 staging 的工程链路。也就是说，当前模块的闭合点已经从“helper 原型成立”推进成“helper 如何以最小写入面落进目标 worktree”。

本版仍不修改 `../warpx`。新增的核心事实是：当前 `rz_jrhom_first_stage_bundle/` 已经不只是一组 helper/diff/provenance 文本，而是具备了对应的 `scripts/preview_rz_jrhom_first_stage_patch.py`、`scripts/audit_rz_jrhom_first_stage_patch.py`、`scripts/report_rz_jrhom_first_stage_patch.py` 和 `scripts/stage_rz_jrhom_first_stage_patch.py`。因此，`v0.36` 完成的是“把 RZ JRhom LL2 从 handoff bundle 推进到 target-checkout workflow”，而不是提前声称 WarpX upstream regression 已经正式上提。

本版仍不是出版终稿。它继续保留 LeeCPC2015 PDF/MinerU 缺口，也保留 comoving patch 与 RZ helper 都尚未真正上提到 WarpX upstream 的现实边界；后续仍应在目标 checkout 上做更贴近实际提交流程的 dry-run/stage 复核，再决定是否正式上提。

## 源码基线

- 本书项目仓库：`/Volumes/PHILIPS/programs/PIC/PIC-tutor`
- WarpX 只读源码：`../warpx`
- 当前 WarpX 分支：`pkuHEDPbranch`
- 当前 WarpX commit：`8c488b1a9`

v0.36 只修改 `PIC-tutor` 书稿项目，不修改 `../warpx` 原仓库。本版继续按当前 checkout 核对 `Examples/Tests/nci_psatd_stability/inputs_test_rz_psatd_JRhom_LL2`、`analysis_psatd_CC1.py`、`analysis_galilean.py`、`PsatdAlgorithmRZ.cpp`、`WarpXEvolve.cpp`、`CMakeLists.txt` 和 `rz-jrhom-reference-scan-mpi2.json` ledger 的对应关系，并把 helper 阈值来源、运行样本路径、bundle 内容和 target-checkout workflow 写回 provenance。后续若 WarpX 更新，必须重新校准源码行号、测试入口和 ledger 样本后再发布新版。

## v0.36 章节范围

| 章节 | 文件 | v0.36 状态 | 下一步缺口 |
|---|---|---|---|
| 写作说明 | `chapters/00-preface.md` | 沿用 v0.1 | 需同步最终出版路线 |
| 动理学模型 | `chapters/01-kinetic-models.md` | 沿用 v0.1 | Hockney-Eastwood、Yee 等一手文献闭环未完成 |
| PIC 总循环 | `chapters/02-pic-loop.md` | 已做 v0.2 源码校准 | 仍需把基础文献和公式变量定义做出版级补齐 |
| WarpX 主演化路径 | `chapters/03-warpx-evolve.md` | 已做 v0.2 源码校准 | `OneStep_sub1()`、JRhom、implicit 分支还需专章级精读 |
| WarpX 初始化链 | `chapters/03a-warpx-initialization.md` | 已做 v0.2 长草稿收束 | 需要拆短小节、补流程图、压缩过长审计段落 |
| 粒子推进器 | `chapters/04-particle-pushers.md` | 已做 v0.3 源码校准 | 仍需压缩多物理长段，并把更多 validation 表格图形化 |
| 沉积与形函数 | `chapters/05-deposition-shapes.md` | 已做 v0.4 源码校准 | Esirkepov、Villasenor-Buneman 论文仍需 MinerU 闭环，`ChargeDeposition` 的 ABLASTR 模板还需继续逐行展开 |
| 场求解器 | `chapters/06-field-solvers.md` | 已补 Lehe/Kirchen/Godfrey 文献闭环、PSATD/NCI 源码机制对照表，并在 v0.26-v0.36 连续收口 comoving 与 RZ validation：当前已具备 comoving handoff/staging 工具链，以及 RZ JRhom LL2 的 repeated/MPI helper、handoff bundle 与 target-checkout workflow | 仍需决定是否真正在目标 WarpX checkout 上 staging 并上提；若不继续上提，就切到下一个成书模块 |
| 边界、PML 与 AMR | `chapters/07-boundaries-amr.md` | 已在 v0.25 增补 LeeCPC2015 论文-源码公式核对清单，把 PML profile、FD PML、PSATD PML、`C1-C25`、Galilean、cleaning 和 RZ 分支的待证项拆开 | 仍需取得 Lee/Vay 授权 PDF、完成 MinerU 逐段讲解，并实现 dedicated transition-zone regression |
| 诊断、验证与案例 | `chapters/08-diagnostics-cases.md` | 沿用 v0.1 | 需要更多本地运行图表和 reader-side analysis |
| 文献路线 | `chapters/09-literature-roadmap.md` | 沿用 v0.1 提纲 | 需要和 `docs/literature-map.md` 去重并完成优先级 |
| 符号表 | `appendices/A-symbols.md` | 沿用 v0.1 最小草稿 | 需要单位、参数、常用缩写和索引 |

## v0.36 已完成的增量

- 冻结 `manuscript/VERSION-v0.35.md`，避免重建 v0.35 时误用 v0.36 版本说明。
- 新增 `scripts/build_v36.py`，生成 `dist/pic-tutor-v0.36.md` 与 `dist/pic-tutor-v0.36.html`。
- 新增 `scripts/stage_rz_jrhom_first_stage_patch.py`，支持对任意 WarpX checkout 先做 `--dry-run`，再自动复制 `analysis_rz_jrhom.py` 并只改写 `test_rz_psatd_JRhom_LL2` 的 analysis 行。
- 新增 `scripts/audit_rz_jrhom_first_stage_patch.py`，对任意 WarpX checkout 只读判断 helper 是否存在且与 bundle 一致、analysis 行是否仍是 `OFF`，并把整体状态归类为 `unstaged / partial / staged`。
- 新增 `scripts/report_rz_jrhom_first_stage_patch.py`，基于只读审计生成 markdown 预检报告，直接给出当前状态和下一条建议命令。
- 新增 `scripts/preview_rz_jrhom_first_stage_patch.py`，对任意 WarpX checkout 只读打印 helper 文件和 `CMakeLists.txt` 的 unified diff。
- 新增 `notes/code-reading/fieldsolver/32-rz-jrhom-target-checkout-workflow.md`，把这一轮为什么收口在 target-checkout workflow、四个脚本各自的职责和推荐调用顺序固定成接续文档。
- 更新 `notes/code-reading/fieldsolver/README.md`、`README.md`、`TODO.md`、`manuscript/README.md` 和第 6 章，把 `test_rz_psatd_JRhom_LL2` 的状态从“已有 handoff bundle”推进成“已有可执行 target-checkout workflow”。

## 成书前必须补齐

- 每章记录最终采用的 WarpX commit，并避免同章混用未说明的历史行号。
- 每章补齐公式变量定义、参数入口、源码路径、行号和真实源码块。
- 至少为核心章节绑定一个 Example 或 Regression。
- 把 `docs/parameter-map.md` 和 `docs/example-regression-map.md` 中的资料条目回填为正文叙述。
- 按 `docs/paper-reading-workflow.md` 完成核心论文 MinerU 转换和中文讲解笔记。
- 建立稳定的 Markdown/HTML/PDF 构建流程；v0.36 仍只保证 Markdown/HTML。
- 对 public GitHub 仓库中的 PDF 和运行产物做版权与体积审计。

## v0.36 构建方式

生成合订 Markdown 和 HTML 预览：

```bash
python scripts/build_v36.py
```

生成的文件：

- `dist/pic-tutor-v0.36.md`
- `dist/pic-tutor-v0.36.html`（若本机存在 `pandoc`）
