# PIC-tutor v0.21

版本日期：2026-06-29

## 定位

`v0.21` 是 `PIC-tutor` 的 PSATD PML 源码闭环版。它继承 `v0.20` 对 PSATD/NCI 机制边界的拆分，继续推进第 6/7 章交界处的 PML PSATD 短板：从 `WarpX::PushPSATD()` 的主域/普通 PML/RZ PML 调用顺序、`PML::PushPSATD()` 的 split-component spectral push、`PML_RZ::PushPSATD()` 的 RZ spectral push、`PsatdAlgorithmPml` 和 `PsatdAlgorithmPmlRZ` 的公式结构，以及 `analysis_pml_psatd.py` / `analysis_pml_psatd_rz.py` / checksum-only 3D cleaning test 的证据等级开始，补成一条可复查的源码-公式-regression 对照。

本版仍不修改 `../warpx`。第 7 章新增 `7.5.3 v0.21 PSATD PML 源码闭环：普通 PML、RZ PML 与 regression 边界`。本版的核心写作边界是：PSATD PML 不是普通 FDTD PML damping 的同义词；普通 Cartesian PML 在主域 PSATD 反变换后单独推进 split fields，RZ PML 则在主域 spectral field push 前进入 `PML_RZ::PushPSATD()`；2D PSATD/Galilean PML 有反射率强 analysis，RZ PSATD PML 有残余场强 analysis，而 3D PSATD+PML+div-cleaning 目前只是 checksum/output baseline。

本版仍不是出版终稿。它完成了 PSATD PML 的源码层闭环，但尚未补一手 PSATD-PML 理论文献的 MinerU 中文讲解，也没有推导普通 Cartesian `PsatdAlgorithmPml` 中全部 `C1-C25` 系数。后续应继续做 PML 论文闭环、PDF 出版流程和版权/体积审计。

## 源码基线

- 本书项目仓库：`/Volumes/PHILIPS/programs/PIC/PIC-tutor`
- WarpX 只读源码：`../warpx`
- 当前 WarpX 分支：`pkuHEDPbranch`
- 当前 WarpX commit：`8c488b1a9`

v0.21 只修改 `PIC-tutor` 书稿项目，不修改 `../warpx` 原仓库。本版按当前 checkout 重新核对了 `WarpXPushFieldsEM.cpp`、`PML.cpp`、`PML_RZ.cpp`、`SpectralSolver.cpp`、`PsatdAlgorithmPml.cpp`、`PsatdAlgorithmPmlRZ.cpp`，以及 `Examples/Tests/pml` 的 CMake wiring、2D PSATD/Galilean 输入卡、RZ PSATD 输入卡、3D cleaning checksum 输入卡和 analysis 脚本。后续若 WarpX 更新，必须重新校准源码行号和测试入口后再发布新版。

## v0.21 章节范围

| 章节 | 文件 | v0.21 状态 | 下一步缺口 |
|---|---|---|---|
| 写作说明 | `chapters/00-preface.md` | 沿用 v0.1 | 需同步最终出版路线 |
| 动理学模型 | `chapters/01-kinetic-models.md` | 沿用 v0.1 | Hockney-Eastwood、Yee 等一手文献闭环未完成 |
| PIC 总循环 | `chapters/02-pic-loop.md` | 已做 v0.2 源码校准 | 仍需把基础文献和公式变量定义做出版级补齐 |
| WarpX 主演化路径 | `chapters/03-warpx-evolve.md` | 已做 v0.2 源码校准 | `OneStep_sub1()`、JRhom、implicit 分支还需专章级精读 |
| WarpX 初始化链 | `chapters/03a-warpx-initialization.md` | 已做 v0.2 长草稿收束 | 需要拆短小节、补流程图、压缩过长审计段落 |
| 粒子推进器 | `chapters/04-particle-pushers.md` | 已做 v0.3 源码校准 | 仍需压缩多物理长段，并把更多 validation 表格图形化 |
| 沉积与形函数 | `chapters/05-deposition-shapes.md` | 已做 v0.4 源码校准 | Esirkepov、Villasenor-Buneman 论文仍需 MinerU 闭环，`ChargeDeposition` 的 ABLASTR 模板还需继续逐行展开 |
| 场求解器 | `chapters/06-field-solvers.md` | 已补 Lehe/Kirchen/Godfrey 文献闭环，并在 v0.20 增补 PSATD/NCI 源码机制对照表 | 仍需 `X1-X4` 系数逐项推导 |
| 边界、PML 与 AMR | `chapters/07-boundaries-amr.md` | 已在 v0.21 增补 PSATD PML 源码/公式/regression 边界 | 仍需 PML 理论文献 MinerU 闭环和 dedicated transition-zone regression 实现 |
| 诊断、验证与案例 | `chapters/08-diagnostics-cases.md` | 沿用 v0.1 | 需要更多本地运行图表和 reader-side analysis |
| 文献路线 | `chapters/09-literature-roadmap.md` | 沿用 v0.1 提纲 | 需要和 `docs/literature-map.md` 去重并完成优先级 |
| 符号表 | `appendices/A-symbols.md` | 沿用 v0.1 最小草稿 | 需要单位、参数、常用缩写和索引 |

## v0.21 已完成的增量

- 冻结 `manuscript/VERSION-v0.20.md`，避免重建 v0.20 时误用 v0.21 版本说明。
- 新增 `scripts/build_v21.py`，生成 `dist/pic-tutor-v0.21.md` 与 `dist/pic-tutor-v0.21.html`。
- 把 `scripts/build_v20.py` 改为读取冻结的 `manuscript/VERSION-v0.20.md`，保持 v0.20 版本说明可复现。
- 在第 7 章新增 `7.5.3 v0.21 PSATD PML 源码闭环：普通 PML、RZ PML 与 regression 边界`。
- 明确 `WarpX::PushPSATD()` 中主域 PSATD、RZ PML spectral push、普通 PML spectral push 和物理边界条件的先后顺序。
- 明确普通 PML 构造时会为 PML 子域单独创建 `in_pml=true`、`periodic_single_box=false`、`update_with_rho=false`、`fft_do_time_averaging=false` 的 `SpectralSolver`，并在 `SpectralSolver.cpp` 中优先分派到 `PsatdAlgorithmPml`。
- 明确 `PML::PushPSATD()` 对 fine/coarse PML patch 的 split `E/B/F/G` components 做 forward transform、spectral update 和 backward transform；RZ `PML_RZ::PushPSATD()` 只推进 `Er/Et/Br/Bt` 的 PML spectral fields。
- 明确 `analysis_pml_psatd.py` 是 2D PSATD/Galilean PML 的强反射率 gate：第 50 步能量 oracle 相对误差 `< 1e-14`，末态反射率 `< 1e-6`。
- 明确 `analysis_pml_psatd_rz.py` 是 RZ radial PML 的末态残余场 gate：`max(|Er|, |Ez|) < 2.0`。
- 明确 `test_3d_pml_psatd_dive_divb_cleaning` 当前 `analysis=OFF`，只能写成 3D PSATD+PML+div-cleaning 的 checksum/workflow baseline。

## 成书前必须补齐

- 每章记录最终采用的 WarpX commit，并避免同章混用未说明的历史行号。
- 每章补齐公式变量定义、参数入口、源码路径、行号和真实源码块。
- 至少为核心章节绑定一个 Example 或 Regression。
- 把 `docs/parameter-map.md` 和 `docs/example-regression-map.md` 中的资料条目回填为正文叙述。
- 按 `docs/paper-reading-workflow.md` 完成核心论文 MinerU 转换和中文讲解笔记。
- 建立稳定的 Markdown/HTML/PDF 构建流程；v0.21 仍只保证 Markdown/HTML。
- 对 public GitHub 仓库中的 PDF 和运行产物做版权与体积审计。

## v0.21 构建方式

生成合订 Markdown 和 HTML 预览：

```bash
python scripts/build_v21.py
```

生成的文件：

- `dist/pic-tutor-v0.21.md`
- `dist/pic-tutor-v0.21.html`（若本机存在 `pandoc`）
