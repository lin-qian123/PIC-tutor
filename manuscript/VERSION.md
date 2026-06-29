# PIC-tutor v0.14

版本日期：2026-06-29

## 定位

`v0.14` 是 `PIC-tutor` 的 transition-zone validation 线索版。它继承 `v0.13` 的 HTML 可读性收口，并回到第 7 章，把 `n_field_gather_buffer/n_current_deposition_buffer`、`E/Bfield_cax`、`current_buf/rho_buf` 和 `PartitionParticlesInBuffers()` 的验证边界写成可执行的检查清单。

本版的重点不是新增一个泛泛 AMR 案例，而是明确当前已有 regression 到底覆盖什么、没覆盖什么。`langmuir` MR 系列仍是强 AMR 场解证据，`particles_in_pml_mr` 是组合路径残余场强检查，`subcycling_mr` 只是 checksum-only workflow baseline；它们都不能直接证明 transition-zone 分区、coarse gather 和 buffer deposition 的每条 branch 已被逐项验证。

本版仍不是出版终稿。它把第 7 章从源码审计推进到 validation 设计层；后续仍需真正新增或找到 dedicated transition-zone test、继续补 PSATD/Galilean/NCI/PML 文献闭环、扩写更多边界索引条目，并建立 PDF 出版流程。

## 源码基线

- 本书项目仓库：`/Volumes/PHILIPS/programs/PIC/PIC-tutor`
- WarpX 只读源码：`../warpx`
- 当前 WarpX 分支：`pkuHEDPbranch`
- 当前 WarpX commit：`8c488b1a9`

v0.14 只修改 `PIC-tutor` 书稿项目，不修改 `../warpx` 原仓库。本版按当前 checkout 重新复核了 transition-zone 相关源码入口和现有 regression wiring；后续若 WarpX 更新，必须重新校准源码行号和测试入口后再发布新版。

## v0.14 章节范围

| 章节 | 文件 | v0.14 状态 | 下一步缺口 |
|---|---|---|---|
| 写作说明 | `chapters/00-preface.md` | 沿用 v0.1 | 需同步最终出版路线 |
| 动理学模型 | `chapters/01-kinetic-models.md` | 沿用 v0.1 | Hockney-Eastwood、Yee 等一手文献闭环未完成 |
| PIC 总循环 | `chapters/02-pic-loop.md` | 已做 v0.2 源码校准 | 仍需把基础文献和公式变量定义做出版级补齐 |
| WarpX 主演化路径 | `chapters/03-warpx-evolve.md` | 已做 v0.2 源码校准 | `OneStep_sub1()`、JRhom、implicit 分支还需专章级精读 |
| WarpX 初始化链 | `chapters/03a-warpx-initialization.md` | 已做 v0.2 长草稿收束 | 需要拆短小节、补流程图、压缩过长审计段落 |
| 粒子推进器 | `chapters/04-particle-pushers.md` | 已做 v0.3 源码校准 | 仍需压缩多物理长段，并把更多 validation 表格图形化 |
| 沉积与形函数 | `chapters/05-deposition-shapes.md` | 已做 v0.4 源码校准 | Esirkepov、Villasenor-Buneman 论文仍需 MinerU 闭环，`ChargeDeposition` 的 ABLASTR 模板还需继续逐行展开 |
| 场求解器 | `chapters/06-field-solvers.md` | 已做 v0.7 验证入口表 | PSATD/Galilean/NCI/PML 论文仍需 MinerU 闭环，HTML 宽表格还需继续审读 |
| 边界、PML 与 AMR | `chapters/07-boundaries-amr.md` | 已做 v0.14 transition-zone validation 线索 | 需要真正新增或找到 dedicated transition-zone analysis |
| 诊断、验证与案例 | `chapters/08-diagnostics-cases.md` | 沿用 v0.1 | 需要更多本地运行图表和 reader-side analysis |
| 文献路线 | `chapters/09-literature-roadmap.md` | 沿用 v0.1 提纲 | 需要和 `docs/literature-map.md` 去重并完成优先级 |
| 符号表 | `appendices/A-symbols.md` | 沿用 v0.1 最小草稿 | 需要单位、参数、常用缩写和索引 |

## v0.14 已完成的增量

- 冻结 `manuscript/VERSION-v0.13.md`，避免重建 v0.13 时误用 v0.14 版本说明。
- 新增 `scripts/build_v14.py`，生成 `dist/pic-tutor-v0.14.md` 与 `dist/pic-tutor-v0.14.html`。
- 把 `scripts/build_v13.py` 改为读取冻结的 `manuscript/VERSION-v0.13.md`，保持 v0.13 版本说明可复现。
- 在第 7 章新增 `7.7.3 v0.14 transition-zone validation 应该直接检查什么`。
- 把 transition-zone 拆成 startup buffer allocation、mask topology、particle partition、gather/deposition routing、coarse-level sync 五段可验证合同。
- 明确现有 `langmuir` MR、`particles_in_pml_mr`、`subcycling_mr` 的证据边界，避免把组合测试或 checksum-only workflow 写成 dedicated transition-zone branch validation。
- 写出后续 dedicated validation 的最小设计：固定 MR patch 与单粒子位置，分别覆盖 buffer-width 对比、`deposit_on_main_grid`、`gather_from_main_grid`，并直接观测或反推出 gather/deposit 目标层。

## 成书前必须补齐

- 每章记录最终采用的 WarpX commit，并避免同章混用未说明的历史行号。
- 每章补齐公式变量定义、参数入口、源码路径、行号和真实源码块。
- 至少为核心章节绑定一个 Example 或 Regression。
- 把 `docs/parameter-map.md` 和 `docs/example-regression-map.md` 中的资料条目回填为正文叙述。
- 按 `docs/paper-reading-workflow.md` 完成核心论文 MinerU 转换和中文讲解笔记。
- 建立稳定的 Markdown/HTML/PDF 构建流程；v0.14 仍只保证 Markdown/HTML。
- 对 public GitHub 仓库中的 PDF 和运行产物做版权与体积审计。

## v0.14 构建方式

生成合订 Markdown 和 HTML 预览：

```bash
python scripts/build_v14.py
```

生成的文件：

- `dist/pic-tutor-v0.14.md`
- `dist/pic-tutor-v0.14.html`（若本机存在 `pandoc`）
