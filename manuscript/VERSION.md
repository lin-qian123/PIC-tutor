# PIC-tutor v0.12

版本日期：2026-06-29

## 定位

`v0.12` 是 `PIC-tutor` 的 AMR coarse-fine 图形化证据版。它继承 `v0.11` 的 guard-cell/regrid 闭环，并继续把第 7 章里的 coarse-fine substitution、transition zone、`WarpXComm_K.H` 点值 kernel 和 regression 证据组织成一张读者侧流程图与一张证据等级表。

本版的重点是把“公式、源码和测试”三条线对齐：`F(a)=F(r)+I[F(s)-F(c)]` 对应 `UpdateAuxilaryData*()` 和 `warpx_interp()`；transition zone 对应 `gather/current buffer masks` 与 `PartitionParticlesInBuffers()`；MR regression 则必须区分强 analysis、组合路径残余场检查和 checksum-only workflow。

本版仍不是出版终稿。它把第 7 章 AMR 粗细界面解释推进到可审校图表，但 PSATD/Galilean/NCI/PML 文献闭环、HTML 宽表格人工审读、更多边界索引条目正文和 PDF 出版流程仍需继续推进。

## 源码基线

- 本书项目仓库：`/Volumes/PHILIPS/programs/PIC/PIC-tutor`
- WarpX 只读源码：`../warpx`
- 当前 WarpX 分支：`pkuHEDPbranch`
- 当前 WarpX commit：`8c488b1a9`

v0.12 只修改 `PIC-tutor` 书稿项目，不修改 `../warpx` 原仓库。章节里的源码路径和 regression 入口按上述 checkout 复核；后续若 WarpX 更新，必须重新校准源码行号和测试入口后再发布新版。

## v0.12 章节范围

| 章节 | 文件 | v0.12 状态 | 下一步缺口 |
|---|---|---|---|
| 写作说明 | `chapters/00-preface.md` | 沿用 v0.1 | 需同步最终出版路线 |
| 动理学模型 | `chapters/01-kinetic-models.md` | 沿用 v0.1 | Hockney-Eastwood、Yee 等一手文献闭环未完成 |
| PIC 总循环 | `chapters/02-pic-loop.md` | 已做 v0.2 源码校准 | 仍需把基础文献和公式变量定义做出版级补齐 |
| WarpX 主演化路径 | `chapters/03-warpx-evolve.md` | 已做 v0.2 源码校准 | `OneStep_sub1()`、JRhom、implicit 分支还需专章级精读 |
| WarpX 初始化链 | `chapters/03a-warpx-initialization.md` | 已做 v0.2 长草稿收束 | 需要拆短小节、补流程图、压缩过长审计段落 |
| 粒子推进器 | `chapters/04-particle-pushers.md` | 已做 v0.3 源码校准 | 仍需压缩多物理长段，并把更多 validation 表格图形化 |
| 沉积与形函数 | `chapters/05-deposition-shapes.md` | 已做 v0.4 源码校准 | Esirkepov、Villasenor-Buneman 论文仍需 MinerU 闭环，`ChargeDeposition` 的 ABLASTR 模板还需继续逐行展开 |
| 场求解器 | `chapters/06-field-solvers.md` | 已做 v0.7 验证入口表 | PSATD/Galilean/NCI/PML 论文仍需 MinerU 闭环，HTML 宽表格还需人工审读 |
| 边界、PML 与 AMR | `chapters/07-boundaries-amr.md` | 已做 v0.12 AMR coarse-fine 图形化证据 | 需要人工审读 HTML 图表，并继续补更专门的 transition-zone validation |
| 诊断、验证与案例 | `chapters/08-diagnostics-cases.md` | 沿用 v0.1 | 需要更多本地运行图表和 reader-side analysis |
| 文献路线 | `chapters/09-literature-roadmap.md` | 沿用 v0.1 提纲 | 需要和 `docs/literature-map.md` 去重并完成优先级 |
| 符号表 | `appendices/A-symbols.md` | 沿用 v0.1 最小草稿 | 需要单位、参数、常用缩写和索引 |

## v0.12 已完成的增量

- 冻结 `manuscript/VERSION-v0.11.md`，避免重建 v0.11 时误用 v0.12 版本说明。
- 新增 `scripts/build_v12.py`，生成 `dist/pic-tutor-v0.12.md` 与 `dist/pic-tutor-v0.12.html`。
- 把 `scripts/build_v11.py` 改为读取冻结的 `manuscript/VERSION-v0.11.md`，保持 v0.11 版本说明可复现。
- 在第 7 章新增 `7.7.2 v0.12 coarse-fine substitution 与 transition zone 的证据图`。
- 用 Mermaid 图把 `F(s) -> F(s)-F(c) -> F(a)`、`E/Bfield_aux`、`E/Bfield_cax`、`current/rho_buf` 和 `PartitionParticlesInBuffers()` 串成读者侧流程。
- 把 transition zone 明确写成 `nfine_gather` 与 `nfine_deposit` 两个不同分界，而不是单个“是否在 fine patch 内”的布尔条件。
- 新增 AMR regression 证据等级表，区分 `langmuir` MR 强 analysis、`particles_in_pml_mr` 组合路径残余场强检查、`subcycling_mr` checksum-only workflow。

## 成书前必须补齐

- 每章记录最终采用的 WarpX commit，并避免同章混用未说明的历史行号。
- 每章补齐公式变量定义、参数入口、源码路径、行号和真实源码块。
- 至少为核心章节绑定一个 Example 或 Regression。
- 把 `docs/parameter-map.md` 和 `docs/example-regression-map.md` 中的资料条目回填为正文叙述。
- 按 `docs/paper-reading-workflow.md` 完成核心论文 MinerU 转换和中文讲解笔记。
- 建立稳定的 Markdown/HTML/PDF 构建流程；v0.12 仍只保证 Markdown/HTML。
- 对 public GitHub 仓库中的 PDF 和运行产物做版权与体积审计。

## v0.12 构建方式

生成合订 Markdown 和 HTML 预览：

```bash
python scripts/build_v12.py
```

生成的文件：

- `dist/pic-tutor-v0.12.md`
- `dist/pic-tutor-v0.12.html`（若本机存在 `pandoc`）
