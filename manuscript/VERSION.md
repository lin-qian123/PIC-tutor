# PIC-tutor v0.5

版本日期：2026-06-29

## 定位

`v0.5` 是 `PIC-tutor` 的场求解器校准版。它继承 `v0.4` 的第一卷范围，并把第 6 章 `电磁场求解器` 从旧源码长草稿推进到当前源码可复查状态。

本版的重点仍不是扩写新章节，而是把第 6 章的源码证据从早期行号校准到当前的场推进主线：`WarpX::OneStep_nosub()` 分出 FDTD 和 PSATD 两条路径，`WarpXPushFieldsEM.cpp` 承接 `EvolveB/E`、`PushPSATD` 和 PML 推进，`FiniteDifferenceSolver` 承载 Yee/Nodal/CKC 的模板 stencil，`SpectralSolver` 分派普通、Galilean、comoving、PML 与 JRhom PSATD 算法。v0.5 也把 `OneStep_JRhom()`、PML damping/copyJ 和 pml regression 入口补进第 6 章的证据地图。

本版仍不是出版终稿。它的目标是把第 2、3、3A、4、5、6 章先变成能按当前源码逐段复查的骨架；下一批需要继续收束第 6 章的文献闭环、图表表达，以及第 7 章边界、PML 与 AMR。

## 源码基线

- 本书项目仓库：`/Volumes/PHILIPS/programs/PIC/PIC-tutor`
- WarpX 只读源码：`../warpx`
- 当前 WarpX 分支：`pkuHEDPbranch`
- 当前 WarpX commit：`8c488b1a9`

v0.5 只修改 `PIC-tutor` 书稿项目，不修改 `../warpx` 原仓库。章节里的源码行号按上述 checkout 复核；后续若 WarpX 更新，必须重新校准行号后再发布新版。

## v0.5 章节范围

| 章节 | 文件 | v0.5 状态 | 下一步缺口 |
|---|---|---|---|
| 写作说明 | `chapters/00-preface.md` | 沿用 v0.1 | 需同步最终出版路线 |
| 动理学模型 | `chapters/01-kinetic-models.md` | 沿用 v0.1 | Hockney-Eastwood、Yee 等一手文献闭环未完成 |
| PIC 总循环 | `chapters/02-pic-loop.md` | 已做 v0.2 源码校准 | 仍需把基础文献和公式变量定义做出版级补齐 |
| WarpX 主演化路径 | `chapters/03-warpx-evolve.md` | 已做 v0.2 源码校准 | `OneStep_sub1()`、JRhom、implicit 分支还需专章级精读 |
| WarpX 初始化链 | `chapters/03a-warpx-initialization.md` | 已做 v0.2 长草稿收束 | 需要拆短小节、补流程图、压缩过长审计段落 |
| 粒子推进器 | `chapters/04-particle-pushers.md` | 已做 v0.3 源码校准 | 仍需压缩多物理长段，并把更多 validation 表格图形化 |
| 沉积与形函数 | `chapters/05-deposition-shapes.md` | 已做 v0.4 源码校准 | Esirkepov、Villasenor-Buneman 论文仍需 MinerU 闭环，`ChargeDeposition` 的 ABLASTR 模板还需继续逐行展开 |
| 场求解器 | `chapters/06-field-solvers.md` | 已做 v0.5 源码校准 | PSATD/Galilean/NCI/PML 论文仍需 MinerU 闭环，读者侧流程图和 validation 表格还需补齐 |
| 边界、PML 与 AMR | `chapters/07-boundaries-amr.md` | 沿用 v0.1 | 需要把 boundary/EB/parallelization 笔记进一步合并 |
| 诊断、验证与案例 | `chapters/08-diagnostics-cases.md` | 沿用 v0.1 | 需要更多本地运行图表和 reader-side analysis |
| 文献路线 | `chapters/09-literature-roadmap.md` | 沿用 v0.1 提纲 | 需要和 `docs/literature-map.md` 去重并完成优先级 |
| 符号表 | `appendices/A-symbols.md` | 沿用 v0.1 最小草稿 | 需要单位、参数、常用缩写和索引 |

## v0.5 已完成的增量

- 冻结 `manuscript/VERSION-v0.4.md`，避免重建 v0.4 时误用 v0.5 版本说明。
- 新增 v0.5 当前版本说明，并把构建输出切到 `dist/pic-tutor-v0.5.md` 与 `dist/pic-tutor-v0.5.html`。
- 把第 6 章绑定到当前 WarpX commit `8c488b1a9`。
- 更新 `WarpX::OneStep_nosub()` 的 FDTD 与 PSATD 分支行号，明确 `SyncCurrentAndRho()`、`CopyJPML()`、`DampJPML()`、`PushPSATD()`、`DampPML()` 和 guard-cell 回填的相对顺序。
- 更新 `WarpX::EvolveB()` / `WarpX::EvolveE()` 的当前分派路径，并重新标定 `FiniteDifferenceSolver::EvolveB/E()` 的 Yee/Nodal/CKC 模板 kernel 行号。
- 更新 `WarpX::PushPSATD()` 的 current correction、Vay deposition、spectral transform、PML push 和物理边界回填路径。
- 补入 `SpectralSolver` 的算法分派地图，区分 PML、comoving、Galilean、first-order JRhom 与 second-order JRhom。
- 补入 `WarpX::OneStep_JRhom()` 的多次沉积、rho/J 谱变换和平均场回填路径。
- 把 `Examples/Tests/pml` 的 Yee/CKC/PSATD/Galilean/RZ PML regression 入口写入第 6 章验证边界。

## 成书前必须补齐

- 每章记录最终采用的 WarpX commit，并避免同章混用未说明的历史行号。
- 每章补齐公式变量定义、参数入口、源码路径、行号和真实源码块。
- 至少为核心章节绑定一个 Example 或 Regression。
- 把 `docs/parameter-map.md` 和 `docs/example-regression-map.md` 中的资料条目回填为正文叙述。
- 按 `docs/paper-reading-workflow.md` 完成核心论文 MinerU 转换和中文讲解笔记。
- 建立稳定的 Markdown/HTML/PDF 构建流程；v0.5 仍只保证 Markdown/HTML。
- 对 public GitHub 仓库中的 PDF 和运行产物做版权与体积审计。

## v0.5 构建方式

生成合订 Markdown 和 HTML 预览：

```bash
python scripts/build_v05.py
```

生成的文件：

- `dist/pic-tutor-v0.5.md`
- `dist/pic-tutor-v0.5.html`（若本机存在 `pandoc`）
