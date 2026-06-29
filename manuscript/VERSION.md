# PIC-tutor v0.20

版本日期：2026-06-29

## 定位

`v0.20` 是 `PIC-tutor` 的 WarpX PSATD/NCI 源码对照版。它不新增论文目录，而是在 `v0.17`、`v0.18`、`v0.19` 已完成的 Lehe 2016、Kirchen 2016、Godfrey 2014 文献闭环基础上，回到当前 `../warpx` checkout，逐项核对 `warpx.use_filter`、RZ PSATD k-space filter、FDTD Godfrey gather filter、`psatd.current_correction`、finite-order PSATD 参数，以及 `nci_psatd_stability` 的 analysis 判据。

本版仍不修改 `../warpx`。第 6 章新增 `6.6.4 v0.20 源码闭环：WarpX PSATD/NCI 机制对照表`，把 “filter / current correction / current scaling / finite-order PSATD / Galilean representation / JRhom” 分成不同机制，避免把它们压成一个泛化的“稳定化开关”。

本版仍不是出版终稿。它完成了 PSATD/NCI 章节中最容易混淆的一轮源码校准；后续仍需继续补 PML PSATD 文献闭环、推导 `X1-X4` 系数、建立 PDF 出版流程，并对 public GitHub 仓库中的 PDF 与运行产物做版权和体积审计。

## 源码基线

- 本书项目仓库：`/Volumes/PHILIPS/programs/PIC/PIC-tutor`
- WarpX 只读源码：`../warpx`
- 当前 WarpX 分支：`pkuHEDPbranch`
- 当前 WarpX commit：`8c488b1a9`

v0.20 只修改 `PIC-tutor` 书稿项目，不修改 `../warpx` 原仓库。本版按当前 checkout 重新核对了 `WarpX.cpp`、`WarpXInitData.cpp`、`BilinearFilter.cpp`、`Filter.cpp`、`WarpXComm.cpp`、`WarpXPushFieldsEM.cpp`、`SpectralBinomialFilter.cpp`、`SpectralFieldDataRZ.cpp`、`NCIGodfreyFilter.cpp`、`PhysicalParticleContainer.cpp`、`SpectralSolver.cpp`、`PsatdAlgorithmGalilean.cpp`、`PsatdAlgorithmComoving.cpp`、`PsatdAlgorithmJRhomSecondOrder.cpp`，以及 `Examples/Tests/nci_psatd_stability` 的输入卡、CMake wiring 和 analysis 脚本。后续若 WarpX 更新，必须重新校准源码行号和测试入口后再发布新版。

## v0.20 章节范围

| 章节 | 文件 | v0.20 状态 | 下一步缺口 |
|---|---|---|---|
| 写作说明 | `chapters/00-preface.md` | 沿用 v0.1 | 需同步最终出版路线 |
| 动理学模型 | `chapters/01-kinetic-models.md` | 沿用 v0.1 | Hockney-Eastwood、Yee 等一手文献闭环未完成 |
| PIC 总循环 | `chapters/02-pic-loop.md` | 已做 v0.2 源码校准 | 仍需把基础文献和公式变量定义做出版级补齐 |
| WarpX 主演化路径 | `chapters/03-warpx-evolve.md` | 已做 v0.2 源码校准 | `OneStep_sub1()`、JRhom、implicit 分支还需专章级精读 |
| WarpX 初始化链 | `chapters/03a-warpx-initialization.md` | 已做 v0.2 长草稿收束 | 需要拆短小节、补流程图、压缩过长审计段落 |
| 粒子推进器 | `chapters/04-particle-pushers.md` | 已做 v0.3 源码校准 | 仍需压缩多物理长段，并把更多 validation 表格图形化 |
| 沉积与形函数 | `chapters/05-deposition-shapes.md` | 已做 v0.4 源码校准 | Esirkepov、Villasenor-Buneman 论文仍需 MinerU 闭环，`ChargeDeposition` 的 ABLASTR 模板还需继续逐行展开 |
| 场求解器 | `chapters/06-field-solvers.md` | 已补 Lehe/Kirchen/Godfrey 文献闭环，并在 v0.20 增补 PSATD/NCI 源码机制对照表 | 仍需 PML PSATD 论文闭环和 `X1-X4` 系数逐项推导 |
| 边界、PML 与 AMR | `chapters/07-boundaries-amr.md` | 已做 v0.16 transition-zone regression patch 计划 | 需要真正实现 dedicated route-count reduced diagnostic 与 regression |
| 诊断、验证与案例 | `chapters/08-diagnostics-cases.md` | 沿用 v0.1 | 需要更多本地运行图表和 reader-side analysis |
| 文献路线 | `chapters/09-literature-roadmap.md` | 沿用 v0.1 提纲 | 需要和 `docs/literature-map.md` 去重并完成优先级 |
| 符号表 | `appendices/A-symbols.md` | 沿用 v0.1 最小草稿 | 需要单位、参数、常用缩写和索引 |

## v0.20 已完成的增量

- 冻结 `manuscript/VERSION-v0.19.md`，避免重建 v0.19 时误用 v0.20 版本说明。
- 新增 `scripts/build_v20.py`，生成 `dist/pic-tutor-v0.20.md` 与 `dist/pic-tutor-v0.20.html`。
- 把 `scripts/build_v19.py` 改为读取冻结的 `manuscript/VERSION-v0.19.md`，保持 v0.19 版本说明可复现。
- 在第 6 章新增 `6.6.4 v0.20 源码闭环：WarpX PSATD/NCI 机制对照表`。
- 明确 `warpx.use_filter = 1` 在普通 Cartesian 路径上是实空间 bilinear/binomial-like stencil，在 RZ PSATD 路径上会转成 spectral k-space binomial filter；它们属于 filter/smoothing 家族。
- 明确 WarpX 源码中的 `NCIGodfreyFilter` 是 `use_fdtd_nci_corr` 触发的 FDTD gather-side z 向 5 点 Godfrey filter，不是 `nci_psatd_stability` 输入卡里 `warpx.use_filter = 1` 的 PSATD filter。
- 明确 `psatd.current_correction` 是投影式连续性方程/Gauss-law 修正；Galilean 分支会引入移动坐标相位项，但它仍不是 Godfrey 2014 的 NCI current scaling 因子 $\zeta$。
- 明确 `psatd.nox/noy/noz = inf` 只允许在 `periodic_single_box_fft = 1` 下作为无限阶谱求解器使用；普通 multi-box PSATD 必须使用有限阶正整数。
- 明确 `analysis_galilean.py` 是电场能量比 gate，并且只在 current-correction 分支额外检查 `divE-rho/\epsilon_0`；`analysis_psatd_CC1.py` 是 JRhom CC1 的能量 gate；`test_rz_psatd_JRhom_LL2` 仍是 checksum-only。

## 成书前必须补齐

- 每章记录最终采用的 WarpX commit，并避免同章混用未说明的历史行号。
- 每章补齐公式变量定义、参数入口、源码路径、行号和真实源码块。
- 至少为核心章节绑定一个 Example 或 Regression。
- 把 `docs/parameter-map.md` 和 `docs/example-regression-map.md` 中的资料条目回填为正文叙述。
- 按 `docs/paper-reading-workflow.md` 完成核心论文 MinerU 转换和中文讲解笔记。
- 建立稳定的 Markdown/HTML/PDF 构建流程；v0.20 仍只保证 Markdown/HTML。
- 对 public GitHub 仓库中的 PDF 和运行产物做版权与体积审计。

## v0.20 构建方式

生成合订 Markdown 和 HTML 预览：

```bash
python scripts/build_v20.py
```

生成的文件：

- `dist/pic-tutor-v0.20.md`
- `dist/pic-tutor-v0.20.html`（若本机存在 `pandoc`）
