# PIC-tutor v0.35

版本日期：2026-07-02

## 定位

`v0.35` 是 `PIC-tutor` 的 RZ JRhom LL2 first-stage helper 版。它继承 `v0.34` 的 comoving PSATD upstream handoff bundle，但这次不再继续扩充 comoving 提交资产，而是把第 6 章另一条已经明确暴露出的缺口真正往前推了一步：`test_rz_psatd_JRhom_LL2` 不再只有“方向判断”和“reference sibling 排序”，而是已经落成一个可直接运行的第一阶段 `finite + energy` helper 原型。

本版仍不修改 `../warpx`。新增的核心事实是：当前本地 sibling 扫描已经给出 baseline `baseline-jrhom-ll2-timeavg-cleaning` 与 unstable reference `ll2-no-timeavg-cleaning` 的可用 energy ordering；`PIC-tutor` 现在把这条 ordering 收成 `scripts/analysis_rz_jrhom.py`，默认执行 finite-field sanity 与 energy gate，并把 spike 保留为可选增强项。因此，`v0.35` 完成的是“把 RZ JRhom LL2 从 checksum-only 缺口推进到 helper 原型”，而不是提前声称 WarpX upstream regression 已经完成。

本版仍不是出版终稿。它继续保留 LeeCPC2015 PDF/MinerU 缺口，也保留 comoving patch 尚未真正上提、RZ helper 仍未真正进入 WarpX `CMakeLists.txt` 的现实边界；后续仍应在 repeated/MPI 或更贴近 upstream regression 的设置下复核当前 energy gate，再决定是否正式上提。

## 源码基线

- 本书项目仓库：`/Volumes/PHILIPS/programs/PIC/PIC-tutor`
- WarpX 只读源码：`../warpx`
- 当前 WarpX 分支：`pkuHEDPbranch`
- 当前 WarpX commit：`8c488b1a9`

v0.35 只修改 `PIC-tutor` 书稿项目，不修改 `../warpx` 原仓库。本版继续按当前 checkout 核对 `Examples/Tests/nci_psatd_stability/inputs_test_rz_psatd_JRhom_LL2`、`analysis_psatd_CC1.py`、`analysis_galilean.py`、`PsatdAlgorithmRZ.cpp`、`WarpXEvolve.cpp`、`CMakeLists.txt` 和本地 `rz-jrhom-reference-scan.json` ledger 的对应关系，并把 helper 阈值来源、运行样本路径和验证结果写回 provenance。后续若 WarpX 更新，必须重新校准源码行号、测试入口和 ledger 样本后再发布新版。

## v0.35 章节范围

| 章节 | 文件 | v0.35 状态 | 下一步缺口 |
|---|---|---|---|
| 写作说明 | `chapters/00-preface.md` | 沿用 v0.1 | 需同步最终出版路线 |
| 动理学模型 | `chapters/01-kinetic-models.md` | 沿用 v0.1 | Hockney-Eastwood、Yee 等一手文献闭环未完成 |
| PIC 总循环 | `chapters/02-pic-loop.md` | 已做 v0.2 源码校准 | 仍需把基础文献和公式变量定义做出版级补齐 |
| WarpX 主演化路径 | `chapters/03-warpx-evolve.md` | 已做 v0.2 源码校准 | `OneStep_sub1()`、JRhom、implicit 分支还需专章级精读 |
| WarpX 初始化链 | `chapters/03a-warpx-initialization.md` | 已做 v0.2 长草稿收束 | 需要拆短小节、补流程图、压缩过长审计段落 |
| 粒子推进器 | `chapters/04-particle-pushers.md` | 已做 v0.3 源码校准 | 仍需压缩多物理长段，并把更多 validation 表格图形化 |
| 沉积与形函数 | `chapters/05-deposition-shapes.md` | 已做 v0.4 源码校准 | Esirkepov、Villasenor-Buneman 论文仍需 MinerU 闭环，`ChargeDeposition` 的 ABLASTR 模板还需继续逐行展开 |
| 场求解器 | `chapters/06-field-solvers.md` | 已补 Lehe/Kirchen/Godfrey 文献闭环、PSATD/NCI 源码机制对照表，并在 v0.26-v0.35 连续收口 comoving 与 RZ validation：当前已具备 comoving handoff bundle，以及 RZ JRhom LL2 的第一阶段 `finite + energy` helper 原型 | 仍需把 comoving patch 与 RZ helper 分别在更贴近 upstream regression 的 repeated/MPI 设置下复核，并决定是否真正上提 WarpX wiring |
| 边界、PML 与 AMR | `chapters/07-boundaries-amr.md` | 已在 v0.25 增补 LeeCPC2015 论文-源码公式核对清单，把 PML profile、FD PML、PSATD PML、`C1-C25`、Galilean、cleaning 和 RZ 分支的待证项拆开 | 仍需取得 Lee/Vay 授权 PDF、完成 MinerU 逐段讲解，并实现 dedicated transition-zone regression |
| 诊断、验证与案例 | `chapters/08-diagnostics-cases.md` | 沿用 v0.1 | 需要更多本地运行图表和 reader-side analysis |
| 文献路线 | `chapters/09-literature-roadmap.md` | 沿用 v0.1 提纲 | 需要和 `docs/literature-map.md` 去重并完成优先级 |
| 符号表 | `appendices/A-symbols.md` | 沿用 v0.1 最小草稿 | 需要单位、参数、常用缩写和索引 |

## v0.35 已完成的增量

- 冻结 `manuscript/VERSION-v0.34.md`，避免重建 v0.34 时误用 v0.35 版本说明。
- 新增 `scripts/build_v35.py`，生成 `dist/pic-tutor-v0.35.md` 与 `dist/pic-tutor-v0.35.html`。
- 新增 `scripts/analysis_rz_jrhom.py`，把 `test_rz_psatd_JRhom_LL2` 的第一阶段 helper 原型收成可直接运行的 `finite + energy` 脚本接口，并保留 `spike` 作为可选增强项。
- 新增 `notes/code-reading/fieldsolver/29-rz-jrhom-first-stage-helper.md`，把 baseline/reference 选择、`tol_energy` 导出方式、可选 `spike` gate 和当前 provenance 边界写清楚。
- 更新 `notes/code-reading/fieldsolver/README.md`、`README.md`、`TODO.md` 和第 6 章，把 `test_rz_psatd_JRhom_LL2` 的状态从“已找到 reference sibling”推进成“已落成 helper 原型”。
- 用当前本地 plotfile 验证 helper 分辨力：baseline `diag1000025` 能通过默认 energy gate，而 `ll2-no-timeavg-cleaning` 在同一阈值下失败。

## 成书前必须补齐

- 每章记录最终采用的 WarpX commit，并避免同章混用未说明的历史行号。
- 每章补齐公式变量定义、参数入口、源码路径、行号和真实源码块。
- 至少为核心章节绑定一个 Example 或 Regression。
- 把 `docs/parameter-map.md` 和 `docs/example-regression-map.md` 中的资料条目回填为正文叙述。
- 按 `docs/paper-reading-workflow.md` 完成核心论文 MinerU 转换和中文讲解笔记。
- 建立稳定的 Markdown/HTML/PDF 构建流程；v0.35 仍只保证 Markdown/HTML。
- 对 public GitHub 仓库中的 PDF 和运行产物做版权与体积审计。

## v0.35 构建方式

生成合订 Markdown 和 HTML 预览：

```bash
python scripts/build_v35.py
```

生成的文件：

- `dist/pic-tutor-v0.35.md`
- `dist/pic-tutor-v0.35.html`（若本机存在 `pandoc`）
