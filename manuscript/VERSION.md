# PIC-tutor v0.4

版本日期：2026-06-29

## 定位

`v0.4` 是 `PIC-tutor` 的沉积与形函数校准版。它继承 `v0.3` 的第一卷范围，并把第 5 章 `沉积与形函数` 从旧源码长草稿推进到当前源码可复查状态。

本版的重点不是扩写新章节，而是把第 5 章的源码证据从旧的 `WarpXParticleContainer.cpp` 局部行号，重新校准为当前的三层结构：`ShapeFactors.H` 定义 0-4 阶形函数，`WarpXParticleContainer::DepositCurrent()` / `DepositCharge()` 做 tile 级分派，`Particles/Deposition/CurrentDeposition.H` 承载 Direct、Esirkepov、Villasenor 和 Vay 的实际 current deposition kernel。v0.4 也把 Langmuir 与 `vay_deposition` 的 `divE-rho/epsilon_0` 检查写成第 5 章的本地验证入口。

本版仍不是出版终稿。它的目标是把第 2、3、3A、4、5 章先变成能按当前源码逐段复查的骨架；第 6 章场求解器仍是下一批需要同步的核心章节。

## 源码基线

- 本书项目仓库：`/Volumes/PHILIPS/programs/PIC/PIC-tutor`
- WarpX 只读源码：`../warpx`
- 当前 WarpX 分支：`pkuHEDPbranch`
- 当前 WarpX commit：`8c488b1a9`

v0.4 只修改 `PIC-tutor` 书稿项目，不修改 `../warpx` 原仓库。章节里的源码行号按上述 checkout 复核；后续若 WarpX 更新，必须重新校准行号后再发布新版。

## v0.4 章节范围

| 章节 | 文件 | v0.4 状态 | 下一步缺口 |
|---|---|---|---|
| 写作说明 | `chapters/00-preface.md` | 沿用 v0.1 | 需同步最终出版路线 |
| 动理学模型 | `chapters/01-kinetic-models.md` | 沿用 v0.1 | Hockney-Eastwood、Yee 等一手文献闭环未完成 |
| PIC 总循环 | `chapters/02-pic-loop.md` | 已做 v0.2 源码校准 | 仍需把基础文献和公式变量定义做出版级补齐 |
| WarpX 主演化路径 | `chapters/03-warpx-evolve.md` | 已做 v0.2 源码校准 | `OneStep_sub1()`、JRhom、implicit 分支还需专章级精读 |
| WarpX 初始化链 | `chapters/03a-warpx-initialization.md` | 已做 v0.2 长草稿收束 | 需要拆短小节、补流程图、压缩过长审计段落 |
| 粒子推进器 | `chapters/04-particle-pushers.md` | 已做 v0.3 源码校准 | 仍需压缩多物理长段，并把更多 validation 表格图形化 |
| 沉积与形函数 | `chapters/05-deposition-shapes.md` | 已做 v0.4 源码校准 | Esirkepov、Villasenor-Buneman 论文仍需 MinerU 闭环，`ChargeDeposition` 的 ABLASTR 模板还需继续逐行展开 |
| 场求解器 | `chapters/06-field-solvers.md` | 沿用 v0.1 长草稿 | PSATD、PML、implicit/hybrid 验证小节需回填 |
| 边界、PML 与 AMR | `chapters/07-boundaries-amr.md` | 沿用 v0.1 | 需要把 boundary/EB/parallelization 笔记进一步合并 |
| 诊断、验证与案例 | `chapters/08-diagnostics-cases.md` | 沿用 v0.1 | 需要更多本地运行图表和 reader-side analysis |
| 文献路线 | `chapters/09-literature-roadmap.md` | 沿用 v0.1 提纲 | 需要和 `docs/literature-map.md` 去重并完成优先级 |
| 符号表 | `appendices/A-symbols.md` | 沿用 v0.1 最小草稿 | 需要单位、参数、常用缩写和索引 |

## v0.4 已完成的增量

- 冻结 `manuscript/VERSION-v0.3.md`，避免重建 v0.3 时误用 v0.4 版本说明。
- 新增 v0.4 当前版本说明，并把构建输出切到 `dist/pic-tutor-v0.4.md` 与 `dist/pic-tutor-v0.4.html`。
- 把第 5 章绑定到当前 WarpX commit `8c488b1a9`。
- 更新 `PhysicalParticleContainer::Evolve()` 中 push 前/后 charge deposition、current deposition 和 AMR buffer 路径的当前行号。
- 更新 `WarpXParticleContainer::DepositCurrent()` 的分派地图，明确 shared-memory 只支持 direct，Esirkepov/Villasenor/Vay 各自的显式/隐式边界。
- 更新 `WarpXParticleContainer::DepositCharge()` 的入口说明，区分 shared-memory `doChargeDepositionSharedShapeN<1..4>()` 与普通 `ablastr::particles::deposit_charge(...)` 路径。
- 把 `Examples/Tests/langmuir/analysis_utils.py` 与 `Examples/Tests/vay_deposition/analysis.py` 的 `divE-rho/epsilon_0` 检查写入第 5 章验证边界。

## 成书前必须补齐

- 每章记录最终采用的 WarpX commit，并避免同章混用未说明的历史行号。
- 每章补齐公式变量定义、参数入口、源码路径、行号和真实源码块。
- 至少为核心章节绑定一个 Example 或 Regression。
- 把 `docs/parameter-map.md` 和 `docs/example-regression-map.md` 中的资料条目回填为正文叙述。
- 按 `docs/paper-reading-workflow.md` 完成核心论文 MinerU 转换和中文讲解笔记。
- 建立稳定的 Markdown/HTML/PDF 构建流程；v0.4 仍只保证 Markdown/HTML。
- 对 public GitHub 仓库中的 PDF 和运行产物做版权与体积审计。

## v0.4 构建方式

生成合订 Markdown 和 HTML 预览：

```bash
python scripts/build_v04.py
```

生成的文件：

- `dist/pic-tutor-v0.4.md`
- `dist/pic-tutor-v0.4.html`（若本机存在 `pandoc`）
