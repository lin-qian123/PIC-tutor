# PIC-tutor v0.16

版本日期：2026-06-29

## 定位

`v0.16` 是 `PIC-tutor` 的 transition-zone regression patch 计划版。它继承 `v0.15` 的测试草案，并继续把 dedicated transition-zone validation 拆成后续可以在 WarpX 侧实际实现的 patch 任务：新增 reduced diagnostic、在 `PhysicalParticleContainer::Evolve()` 记录 route counts、可选输出 buffer masks、补输入卡、补 analysis 和 CMake wiring。

本版的重点仍不是修改 `../warpx`，而是在书稿内把修改点、接口形状、文件清单和验证门槛写清楚。v0.16 复核了 `MultiReducedDiags` 的类型字典、`ReducedDiags` 的文本输出框架、`ParticleNumber` 的 species 循环模板，以及 `PhysicalParticleContainer::Evolve()` 中 `nfine_deposit/nfine_gather` 产生后的唯一可靠观测点。结论是：route-count 应优先做成 regression-only reduced diagnostic；mask 输出可以作为第二阶段 field functor 或 debug field surface，不应阻塞第一条强 validation。

本版仍不是出版终稿。它把第 7 章从测试草案层推进到 patch 计划层；后续仍需真正实现 dedicated transition-zone test、继续补 PSATD/Galilean/NCI/PML 文献闭环、扩写更多边界索引条目，并建立 PDF 出版流程。

## 源码基线

- 本书项目仓库：`/Volumes/PHILIPS/programs/PIC/PIC-tutor`
- WarpX 只读源码：`../warpx`
- 当前 WarpX 分支：`pkuHEDPbranch`
- 当前 WarpX commit：`8c488b1a9`

v0.16 只修改 `PIC-tutor` 书稿项目，不修改 `../warpx` 原仓库。本版按当前 checkout 重新复核了 transition-zone 相关源码入口、reduced diagnostics 扩展入口和 regression wiring；后续若 WarpX 更新，必须重新校准源码行号和测试入口后再发布新版。

## v0.16 章节范围

| 章节 | 文件 | v0.16 状态 | 下一步缺口 |
|---|---|---|---|
| 写作说明 | `chapters/00-preface.md` | 沿用 v0.1 | 需同步最终出版路线 |
| 动理学模型 | `chapters/01-kinetic-models.md` | 沿用 v0.1 | Hockney-Eastwood、Yee 等一手文献闭环未完成 |
| PIC 总循环 | `chapters/02-pic-loop.md` | 已做 v0.2 源码校准 | 仍需把基础文献和公式变量定义做出版级补齐 |
| WarpX 主演化路径 | `chapters/03-warpx-evolve.md` | 已做 v0.2 源码校准 | `OneStep_sub1()`、JRhom、implicit 分支还需专章级精读 |
| WarpX 初始化链 | `chapters/03a-warpx-initialization.md` | 已做 v0.2 长草稿收束 | 需要拆短小节、补流程图、压缩过长审计段落 |
| 粒子推进器 | `chapters/04-particle-pushers.md` | 已做 v0.3 源码校准 | 仍需压缩多物理长段，并把更多 validation 表格图形化 |
| 沉积与形函数 | `chapters/05-deposition-shapes.md` | 已做 v0.4 源码校准 | Esirkepov、Villasenor-Buneman 论文仍需 MinerU 闭环，`ChargeDeposition` 的 ABLASTR 模板还需继续逐行展开 |
| 场求解器 | `chapters/06-field-solvers.md` | 已做 v0.7 验证入口表 | PSATD/Galilean/NCI/PML 论文仍需 MinerU 闭环，HTML 宽表格还需继续审读 |
| 边界、PML 与 AMR | `chapters/07-boundaries-amr.md` | 已做 v0.16 transition-zone regression patch 计划 | 需要真正实现 dedicated route-count reduced diagnostic 与 regression |
| 诊断、验证与案例 | `chapters/08-diagnostics-cases.md` | 沿用 v0.1 | 需要更多本地运行图表和 reader-side analysis |
| 文献路线 | `chapters/09-literature-roadmap.md` | 沿用 v0.1 提纲 | 需要和 `docs/literature-map.md` 去重并完成优先级 |
| 符号表 | `appendices/A-symbols.md` | 沿用 v0.1 最小草稿 | 需要单位、参数、常用缩写和索引 |

## v0.16 已完成的增量

- 冻结 `manuscript/VERSION-v0.15.md`，避免重建 v0.15 时误用 v0.16 版本说明。
- 新增 `scripts/build_v16.py`，生成 `dist/pic-tutor-v0.16.md` 与 `dist/pic-tutor-v0.16.html`。
- 把 `scripts/build_v15.py` 改为读取冻结的 `manuscript/VERSION-v0.15.md`，保持 v0.15 版本说明可复现。
- 在第 7 章新增 `7.7.5 v0.16 transition-zone regression patch 计划`。
- 把后续 WarpX 修改拆成五个 patch：`TransitionZoneRoutes` reduced diagnostic、`PhysicalParticleContainer::Evolve()` route-count hook、可选 mask debug output、`Examples/Tests/amr_transition_zone` 输入卡与 analysis、CMake wiring。
- 明确 route-count reduced diagnostic 的输出列、触发时机、species/tile 聚合口径和 analysis 断言。
- 明确第一阶段不必输出整张 mask；只要 route-count 能证明 interior / gather-only / deposit-only / both-buffer / main-grid override 都被命中，就能形成强 branch validation。

## 成书前必须补齐

- 每章记录最终采用的 WarpX commit，并避免同章混用未说明的历史行号。
- 每章补齐公式变量定义、参数入口、源码路径、行号和真实源码块。
- 至少为核心章节绑定一个 Example 或 Regression。
- 把 `docs/parameter-map.md` 和 `docs/example-regression-map.md` 中的资料条目回填为正文叙述。
- 按 `docs/paper-reading-workflow.md` 完成核心论文 MinerU 转换和中文讲解笔记。
- 建立稳定的 Markdown/HTML/PDF 构建流程；v0.16 仍只保证 Markdown/HTML。
- 对 public GitHub 仓库中的 PDF 和运行产物做版权与体积审计。

## v0.16 构建方式

生成合订 Markdown 和 HTML 预览：

```bash
python scripts/build_v16.py
```

生成的文件：

- `dist/pic-tutor-v0.16.md`
- `dist/pic-tutor-v0.16.html`（若本机存在 `pandoc`）
