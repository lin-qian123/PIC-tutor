# PIC-tutor v0.19

版本日期：2026-06-29

## 定位

`v0.19` 是 `PIC-tutor` 的 PSATD NCI 策略谱系版。它继承 `v0.18` 的 Kirchen et al. 2016 boosted-frame Galilean 应用证据，并继续补入 Godfrey, Vay, Haber 2014 的本地 PDF、MinerU Markdown、图片、中文讲解笔记和 reading log，把第 6 章中的 NCI 讨论从 “Galilean 能稳定” 扩展成更完整的策略分类：fixed-grid PSATD 的数字滤波、插值阶数、current scaling、时间步选择，与 Galilean PSATD 的表示层面消除机制并列说明。

本版仍不修改 `../warpx`。v0.19 新增 `references/06_stability_filtering_nci/2014_GodfreyJCP2014_Numerical_stability_analysis_of_the_PSATD_PIC_algorithm/`，其中包含原 PDF、MinerU 转换 Markdown、图片、中文讲解笔记和 reading log；第 6 章新增 `6.6.3 v0.19 文献闭环：Godfrey et al. 2014 的 PSATD NCI 策略谱系`。本版的写作重点是把 `warpx.use_filter = 1`、`psatd.current_correction`、`psatd.do_time_averaging`、`psatd.JRhom` 和 Galilean PSATD 分成不同机制，避免把它们统称为同一个“稳定化开关”。

本版仍不是出版终稿。它完成了 PSATD/Galilean/NCI 文献闭环的第三个核心节点；后续仍需继续核 WarpX 当前 filter profile、current correction 源码实现、finite-order PSATD 参数，以及 PML PSATD 相关论文和出版级 PDF 流程。

## 源码基线

- 本书项目仓库：`/Volumes/PHILIPS/programs/PIC/PIC-tutor`
- WarpX 只读源码：`../warpx`
- 当前 WarpX 分支：`pkuHEDPbranch`
- 当前 WarpX commit：`8c488b1a9`

v0.19 只修改 `PIC-tutor` 书稿项目，不修改 `../warpx` 原仓库。本版按当前 checkout 连接了 Godfrey et al. 2014、Lehe et al. 2016、Kirchen et al. 2016、WarpX `nci_psatd_stability` regression、`analysis_galilean.py`、`analysis_psatd_CC1.py` 和第 6 章已有的 PSATD/JRhom 源码精读。后续若 WarpX 更新，必须重新校准源码行号和测试入口后再发布新版。

## v0.19 章节范围

| 章节 | 文件 | v0.19 状态 | 下一步缺口 |
|---|---|---|---|
| 写作说明 | `chapters/00-preface.md` | 沿用 v0.1 | 需同步最终出版路线 |
| 动理学模型 | `chapters/01-kinetic-models.md` | 沿用 v0.1 | Hockney-Eastwood、Yee 等一手文献闭环未完成 |
| PIC 总循环 | `chapters/02-pic-loop.md` | 已做 v0.2 源码校准 | 仍需把基础文献和公式变量定义做出版级补齐 |
| WarpX 主演化路径 | `chapters/03-warpx-evolve.md` | 已做 v0.2 源码校准 | `OneStep_sub1()`、JRhom、implicit 分支还需专章级精读 |
| WarpX 初始化链 | `chapters/03a-warpx-initialization.md` | 已做 v0.2 长草稿收束 | 需要拆短小节、补流程图、压缩过长审计段落 |
| 粒子推进器 | `chapters/04-particle-pushers.md` | 已做 v0.3 源码校准 | 仍需压缩多物理长段，并把更多 validation 表格图形化 |
| 沉积与形函数 | `chapters/05-deposition-shapes.md` | 已做 v0.4 源码校准 | Esirkepov、Villasenor-Buneman 论文仍需 MinerU 闭环，`ChargeDeposition` 的 ABLASTR 模板还需继续逐行展开 |
| 场求解器 | `chapters/06-field-solvers.md` | 已补 Lehe 2016、Kirchen 2016、Godfrey 2014 的 PSATD/Galilean/NCI 文献闭环 | 仍需核 WarpX filter/current correction 源码公式、PML PSATD 论文和 `X1-X4` 系数逐项推导 |
| 边界、PML 与 AMR | `chapters/07-boundaries-amr.md` | 已做 v0.16 transition-zone regression patch 计划 | 需要真正实现 dedicated route-count reduced diagnostic 与 regression |
| 诊断、验证与案例 | `chapters/08-diagnostics-cases.md` | 沿用 v0.1 | 需要更多本地运行图表和 reader-side analysis |
| 文献路线 | `chapters/09-literature-roadmap.md` | 沿用 v0.1 提纲 | 需要和 `docs/literature-map.md` 去重并完成优先级 |
| 符号表 | `appendices/A-symbols.md` | 沿用 v0.1 最小草稿 | 需要单位、参数、常用缩写和索引 |

## v0.19 已完成的增量

- 冻结 `manuscript/VERSION-v0.18.md`，避免重建 v0.18 时误用 v0.19 版本说明。
- 新增 `scripts/build_v19.py`，生成 `dist/pic-tutor-v0.19.md` 与 `dist/pic-tutor-v0.19.html`。
- 把 `scripts/build_v18.py` 改为读取冻结的 `manuscript/VERSION-v0.18.md`，保持 v0.18 版本说明可复现。
- 新增 Godfrey et al. 2014 论文专属目录，保存 PDF、MinerU Markdown、图片、中文讲解笔记和 reading log。
- 在第 6 章新增 `6.6.3 v0.19 文献闭环：Godfrey et al. 2014 的 PSATD NCI 策略谱系`。
- 把 fixed-grid PSATD 的数字滤波、三次插值、current scaling、时间步选择，与 Galilean PSATD 的表示层面策略分开说明。
- 明确 `warpx.use_filter = 1` 属于 filter/smoothing 家族，`psatd.current_correction` 属于连续性方程/Gauss law 约束路径，`psatd.JRhom` 属于源项时间积分家族，三者不应混写成同一个机制。

## 成书前必须补齐

- 每章记录最终采用的 WarpX commit，并避免同章混用未说明的历史行号。
- 每章补齐公式变量定义、参数入口、源码路径、行号和真实源码块。
- 至少为核心章节绑定一个 Example 或 Regression。
- 把 `docs/parameter-map.md` 和 `docs/example-regression-map.md` 中的资料条目回填为正文叙述。
- 按 `docs/paper-reading-workflow.md` 完成核心论文 MinerU 转换和中文讲解笔记。
- 建立稳定的 Markdown/HTML/PDF 构建流程；v0.19 仍只保证 Markdown/HTML。
- 对 public GitHub 仓库中的 PDF 和运行产物做版权与体积审计。

## v0.19 构建方式

生成合订 Markdown 和 HTML 预览：

```bash
python scripts/build_v19.py
```

生成的文件：

- `dist/pic-tutor-v0.19.md`
- `dist/pic-tutor-v0.19.html`（若本机存在 `pandoc`）
