# PIC-tutor v0.9

版本日期：2026-06-29

## 定位

`v0.9` 是 `PIC-tutor` 的边界 regression 判据索引版。它继承 `v0.8` 的第 7 章源码入口地图，并继续把边界、PML、AMR 和 boundary scraping 的验证证据从“知道入口在哪里”推进到“知道哪些 regression 真正在验证什么”的状态。

本版的重点是给第 7 章补一个统一的 regression 入口索引表。表格按当前 `../warpx` checkout 中的 `Examples/Tests/*/CMakeLists.txt`、输入卡和 `analysis*.py` 整理，明确区分物理强 analysis、restart 一致性检查和 checksum-only 输出回归。这样后续扩写边界章节时，可以避免把 `analysis=OFF` 的 smoke/checksum 路径误写成完整物理 benchmark。

本版仍不是出版终稿。它的目标是把第 7 章先连接到可运行测试入口，下一步再继续把表格中的重点条目扩写成正文推导，并补齐 AMR/regrid/guard-cell 的细节段落。

## 源码基线

- 本书项目仓库：`/Volumes/PHILIPS/programs/PIC/PIC-tutor`
- WarpX 只读源码：`../warpx`
- 当前 WarpX 分支：`pkuHEDPbranch`
- 当前 WarpX commit：`8c488b1a9`

v0.9 只修改 `PIC-tutor` 书稿项目，不修改 `../warpx` 原仓库。章节里的源码行号和 regression 入口按上述 checkout 复核；后续若 WarpX 更新，必须重新校准行号和测试入口后再发布新版。

## v0.9 章节范围

| 章节 | 文件 | v0.9 状态 | 下一步缺口 |
|---|---|---|---|
| 写作说明 | `chapters/00-preface.md` | 沿用 v0.1 | 需同步最终出版路线 |
| 动理学模型 | `chapters/01-kinetic-models.md` | 沿用 v0.1 | Hockney-Eastwood、Yee 等一手文献闭环未完成 |
| PIC 总循环 | `chapters/02-pic-loop.md` | 已做 v0.2 源码校准 | 仍需把基础文献和公式变量定义做出版级补齐 |
| WarpX 主演化路径 | `chapters/03-warpx-evolve.md` | 已做 v0.2 源码校准 | `OneStep_sub1()`、JRhom、implicit 分支还需专章级精读 |
| WarpX 初始化链 | `chapters/03a-warpx-initialization.md` | 已做 v0.2 长草稿收束 | 需要拆短小节、补流程图、压缩过长审计段落 |
| 粒子推进器 | `chapters/04-particle-pushers.md` | 已做 v0.3 源码校准 | 仍需压缩多物理长段，并把更多 validation 表格图形化 |
| 沉积与形函数 | `chapters/05-deposition-shapes.md` | 已做 v0.4 源码校准 | Esirkepov、Villasenor-Buneman 论文仍需 MinerU 闭环，`ChargeDeposition` 的 ABLASTR 模板还需继续逐行展开 |
| 场求解器 | `chapters/06-field-solvers.md` | 已做 v0.7 验证入口表 | PSATD/Galilean/NCI/PML 论文仍需 MinerU 闭环，HTML 宽表格还需人工审读 |
| 边界、PML 与 AMR | `chapters/07-boundaries-amr.md` | 已做 v0.9 regression 判据索引 | 需要把索引表扩写成分节正文，并继续细核 AMR/regrid/guard-cell 路径 |
| 诊断、验证与案例 | `chapters/08-diagnostics-cases.md` | 沿用 v0.1 | 需要更多本地运行图表和 reader-side analysis |
| 文献路线 | `chapters/09-literature-roadmap.md` | 沿用 v0.1 提纲 | 需要和 `docs/literature-map.md` 去重并完成优先级 |
| 符号表 | `appendices/A-symbols.md` | 沿用 v0.1 最小草稿 | 需要单位、参数、常用缩写和索引 |

## v0.9 已完成的增量

- 冻结 `manuscript/VERSION-v0.8.md`，避免重建 v0.8 时误用 v0.9 版本说明。
- 新增 v0.9 当前版本说明，并把构建输出切到 `dist/pic-tutor-v0.9.md` 与 `dist/pic-tutor-v0.9.html`。
- 把 `scripts/build_v08.py` 改为读取冻结的 `manuscript/VERSION-v0.8.md`，保持 v0.8 版本说明可复现。
- 在第 7 章新增 `v0.9 边界 regression 入口索引`，按 family、代表输入、analysis 入口、主要判据和源码风险整理。
- 表格覆盖 domain particle boundary、PEC/PMC、PECInsulator、PML FDTD/PSATD/RZ/restart、particles in PML、3D EB scrape、RZ EB scraping/filter 和 Silver-Mueller。
- 明确 `test_3d_pec_particle`、`test_2d_pec_field_insulator` 和 `test_3d_pml_psatd_dive_divb_cleaning` 当前属于 checksum-only 或 smoke/checksum 证据，不能写成强物理验证。

## 成书前必须补齐

- 每章记录最终采用的 WarpX commit，并避免同章混用未说明的历史行号。
- 每章补齐公式变量定义、参数入口、源码路径、行号和真实源码块。
- 至少为核心章节绑定一个 Example 或 Regression。
- 把 `docs/parameter-map.md` 和 `docs/example-regression-map.md` 中的资料条目回填为正文叙述。
- 按 `docs/paper-reading-workflow.md` 完成核心论文 MinerU 转换和中文讲解笔记。
- 建立稳定的 Markdown/HTML/PDF 构建流程；v0.9 仍只保证 Markdown/HTML。
- 对 public GitHub 仓库中的 PDF 和运行产物做版权与体积审计。

## v0.9 构建方式

生成合订 Markdown 和 HTML 预览：

```bash
python scripts/build_v09.py
```

生成的文件：

- `dist/pic-tutor-v0.9.md`
- `dist/pic-tutor-v0.9.html`（若本机存在 `pandoc`）
