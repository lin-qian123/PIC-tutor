# PIC-tutor v0.28

版本日期：2026-06-29

## 定位

`v0.28` 是 `PIC-tutor` 的 PSATD-JRhom `Y1-Y8` 系数闭环版。它继承 `v0.27` 的 Cartesian average-field `Psi/Y` 图谱，并继续收束第 6 章中另一个容易混写的短板：JRhom second-order 中 `Y1-Y5` 与 `Y6-Y8` 的不同作用面。

本版仍不修改 `../warpx`。第 6 章新增 `6.7.1 v0.28 JRhom second-order Y1-Y8 系数的源码公式闭环`，并新增 `notes/code-reading/fieldsolver/19-psatd-jrhom-y-coefficients.md`。本版的核心写作边界是：这里的 `Y1-Y8` 只对应 Cartesian `PsatdAlgorithmJRhomSecondOrder.cpp` 的多项式源项积分，不直接覆盖 Galilean average-field `Y1-Y4`、RZ/Galilean RZ 或 PML PSATD。

本版仍不是出版终稿。它继续保留 LeeCPC2015 PDF/MinerU 缺口，但不再把项目推进完全卡在授权全文上。后续仍应补齐 Lee/Vay PML 论文全文，同时继续把第 6 章的 RZ/Galilean RZ 和 comoving 系数体系逐项拆清。

## 源码基线

- 本书项目仓库：`/Volumes/PHILIPS/programs/PIC/PIC-tutor`
- WarpX 只读源码：`../warpx`
- 当前 WarpX 分支：`pkuHEDPbranch`
- 当前 WarpX commit：`8c488b1a9`

v0.28 只修改 `PIC-tutor` 书稿项目，不修改 `../warpx` 原仓库。本版继续按当前 checkout 核对 `PsatdAlgorithmJRhomSecondOrder.cpp:32-542`、`WarpXEvolve.cpp:843-1008`、`SpectralSolver.cpp:60-107`、`Examples/Tests/nci_psatd_stability/analysis_psatd_CC1.py` 和 `inputs_test_3d_uniform_plasma_psatd_JRhom_CC1`。后续若 WarpX 更新，必须重新校准源码行号、文档段落和测试入口后再发布新版。

## v0.28 章节范围

| 章节 | 文件 | v0.28 状态 | 下一步缺口 |
|---|---|---|---|
| 写作说明 | `chapters/00-preface.md` | 沿用 v0.1 | 需同步最终出版路线 |
| 动理学模型 | `chapters/01-kinetic-models.md` | 沿用 v0.1 | Hockney-Eastwood、Yee 等一手文献闭环未完成 |
| PIC 总循环 | `chapters/02-pic-loop.md` | 已做 v0.2 源码校准 | 仍需把基础文献和公式变量定义做出版级补齐 |
| WarpX 主演化路径 | `chapters/03-warpx-evolve.md` | 已做 v0.2 源码校准 | `OneStep_sub1()`、JRhom、implicit 分支还需专章级精读 |
| WarpX 初始化链 | `chapters/03a-warpx-initialization.md` | 已做 v0.2 长草稿收束 | 需要拆短小节、补流程图、压缩过长审计段落 |
| 粒子推进器 | `chapters/04-particle-pushers.md` | 已做 v0.3 源码校准 | 仍需压缩多物理长段，并把更多 validation 表格图形化 |
| 沉积与形函数 | `chapters/05-deposition-shapes.md` | 已做 v0.4 源码校准 | Esirkepov、Villasenor-Buneman 论文仍需 MinerU 闭环，`ChargeDeposition` 的 ABLASTR 模板还需继续逐行展开 |
| 场求解器 | `chapters/06-field-solvers.md` | 已补 Lehe/Kirchen/Godfrey 文献闭环、PSATD/NCI 源码机制对照表，并在 v0.26 增补 Cartesian `X1-X4`、v0.27 增补 time-averaging `Psi/Y`、v0.28 增补 JRhom `Y1-Y8` 源码公式闭环 | 仍需 RZ/Galilean RZ 和 comoving 系数逐项拆表 |
| 边界、PML 与 AMR | `chapters/07-boundaries-amr.md` | 已在 v0.25 增补 LeeCPC2015 论文-源码公式核对清单，把 PML profile、FD PML、PSATD PML、`C1-C25`、Galilean、cleaning 和 RZ 分支的待证项拆开 | 仍需取得 Lee/Vay 授权 PDF、完成 MinerU 逐段讲解，并实现 dedicated transition-zone regression |
| 诊断、验证与案例 | `chapters/08-diagnostics-cases.md` | 沿用 v0.1 | 需要更多本地运行图表和 reader-side analysis |
| 文献路线 | `chapters/09-literature-roadmap.md` | 沿用 v0.1 提纲 | 需要和 `docs/literature-map.md` 去重并完成优先级 |
| 符号表 | `appendices/A-symbols.md` | 沿用 v0.1 最小草稿 | 需要单位、参数、常用缩写和索引 |

## v0.28 已完成的增量

- 冻结 `manuscript/VERSION-v0.27.md`，避免重建 v0.27 时误用 v0.28 版本说明。
- 新增 `scripts/build_v28.py`，生成 `dist/pic-tutor-v0.28.md` 与 `dist/pic-tutor-v0.28.html`。
- 把 `scripts/build_v27.py` 改为读取冻结的 `manuscript/VERSION-v0.27.md`，保持 v0.27 版本说明可复现。
- 新增 `notes/code-reading/fieldsolver/19-psatd-jrhom-y-coefficients.md`，覆盖 Cartesian `PsatdAlgorithmJRhomSecondOrder.cpp` 的 `Y1-Y8` 源码公式、零模处理、普通 `E/B/F` 更新式、time-averaged field 累计式和防混写边界。
- 更新 `notes/code-reading/fieldsolver/README.md`，把新图谱纳入 fieldsolver 精读顺序。
- 在第 6 章新增 `6.7.1 v0.28 JRhom second-order Y1-Y8 系数的源码公式闭环`，把 `Y1-Y5` 与普通 `E/B/F` 多项式源项积分、`Y6-Y8` 与 average-field 累计积分的关系写成正文。

## 成书前必须补齐

- 每章记录最终采用的 WarpX commit，并避免同章混用未说明的历史行号。
- 每章补齐公式变量定义、参数入口、源码路径、行号和真实源码块。
- 至少为核心章节绑定一个 Example 或 Regression。
- 把 `docs/parameter-map.md` 和 `docs/example-regression-map.md` 中的资料条目回填为正文叙述。
- 按 `docs/paper-reading-workflow.md` 完成核心论文 MinerU 转换和中文讲解笔记。
- 建立稳定的 Markdown/HTML/PDF 构建流程；v0.28 仍只保证 Markdown/HTML。
- 对 public GitHub 仓库中的 PDF 和运行产物做版权与体积审计。

## v0.28 构建方式

生成合订 Markdown 和 HTML 预览：

```bash
python scripts/build_v28.py
```

生成的文件：

- `dist/pic-tutor-v0.28.md`
- `dist/pic-tutor-v0.28.html`（若本机存在 `pandoc`）
