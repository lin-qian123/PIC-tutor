# PIC-tutor v0.10

版本日期：2026-06-29

## 定位

`v0.10` 是 `PIC-tutor` 的边界强 analysis 路径扩写版。它继承 `v0.9` 的第 7 章 regression 入口索引，并把其中四条最适合进入正文的验证路径先写成可审校段落：particle domain boundary、PEC/PMC 场反射、particles in PML 和 RZ embedded-boundary scraping。

本版的重点不是新增更宽的索引，而是把“表格里的判据”转成读者可以跟着源码和输入卡理解的叙述。每条路径都明确代表输入、analysis 脚本、主要数值断言和对应源码风险，避免把 checksum-only 或 smoke 测试误写成强物理验证。

本版仍不是出版终稿。它把第 7 章从索引推进到首批正文段落，但 AMR/regrid/guard-cell 的细节、PSATD/Galilean/NCI/PML 论文闭环、HTML 宽表格人工审读和 PDF 出版流程仍需继续补齐。

## 源码基线

- 本书项目仓库：`/Volumes/PHILIPS/programs/PIC/PIC-tutor`
- WarpX 只读源码：`../warpx`
- 当前 WarpX 分支：`pkuHEDPbranch`
- 当前 WarpX commit：`8c488b1a9`

v0.10 只修改 `PIC-tutor` 书稿项目，不修改 `../warpx` 原仓库。章节里的源码路径和 regression 入口按上述 checkout 复核；后续若 WarpX 更新，必须重新校准源码行号和测试入口后再发布新版。

## v0.10 章节范围

| 章节 | 文件 | v0.10 状态 | 下一步缺口 |
|---|---|---|---|
| 写作说明 | `chapters/00-preface.md` | 沿用 v0.1 | 需同步最终出版路线 |
| 动理学模型 | `chapters/01-kinetic-models.md` | 沿用 v0.1 | Hockney-Eastwood、Yee 等一手文献闭环未完成 |
| PIC 总循环 | `chapters/02-pic-loop.md` | 已做 v0.2 源码校准 | 仍需把基础文献和公式变量定义做出版级补齐 |
| WarpX 主演化路径 | `chapters/03-warpx-evolve.md` | 已做 v0.2 源码校准 | `OneStep_sub1()`、JRhom、implicit 分支还需专章级精读 |
| WarpX 初始化链 | `chapters/03a-warpx-initialization.md` | 已做 v0.2 长草稿收束 | 需要拆短小节、补流程图、压缩过长审计段落 |
| 粒子推进器 | `chapters/04-particle-pushers.md` | 已做 v0.3 源码校准 | 仍需压缩多物理长段，并把更多 validation 表格图形化 |
| 沉积与形函数 | `chapters/05-deposition-shapes.md` | 已做 v0.4 源码校准 | Esirkepov、Villasenor-Buneman 论文仍需 MinerU 闭环，`ChargeDeposition` 的 ABLASTR 模板还需继续逐行展开 |
| 场求解器 | `chapters/06-field-solvers.md` | 已做 v0.7 验证入口表 | PSATD/Galilean/NCI/PML 论文仍需 MinerU 闭环，HTML 宽表格还需人工审读 |
| 边界、PML 与 AMR | `chapters/07-boundaries-amr.md` | 已做 v0.10 强 analysis 路径正文 | 需要继续细核 AMR/regrid/guard-cell 路径，并把更多索引条目扩写成正文 |
| 诊断、验证与案例 | `chapters/08-diagnostics-cases.md` | 沿用 v0.1 | 需要更多本地运行图表和 reader-side analysis |
| 文献路线 | `chapters/09-literature-roadmap.md` | 沿用 v0.1 提纲 | 需要和 `docs/literature-map.md` 去重并完成优先级 |
| 符号表 | `appendices/A-symbols.md` | 沿用 v0.1 最小草稿 | 需要单位、参数、常用缩写和索引 |

## v0.10 已完成的增量

- 冻结 `manuscript/VERSION-v0.9.md`，避免重建 v0.9 时误用 v0.10 版本说明。
- 新增 `scripts/build_v10.py`，生成 `dist/pic-tutor-v0.10.md` 与 `dist/pic-tutor-v0.10.html`。
- 把 `scripts/build_v09.py` 改为读取冻结的 `manuscript/VERSION-v0.9.md`，保持 v0.9 版本说明可复现。
- 在第 7 章新增 `7.5.2 v0.10 四条强 analysis 路径的正文化`。
- 把 particle domain boundary 写成 absorbing、reflecting、periodic 三类粒子语义的最小解析轨道合同。
- 把 PEC/PMC 写成站波振幅合同，并区分单层 `1%` 容差与 MR `5%` 容差。
- 把 particles in PML 写成粒子穿出 in-domain PML 后的残余场合同，明确 `pml_has_particles`、`do_pml_in_domain` 和 `do_pml_j_damping` 的组合意义。
- 把 RZ EB scraping 写成主容器删除、scraped buffer 记录和 `plot_filter_function` 过滤输出之间的守恒合同。

## 成书前必须补齐

- 每章记录最终采用的 WarpX commit，并避免同章混用未说明的历史行号。
- 每章补齐公式变量定义、参数入口、源码路径、行号和真实源码块。
- 至少为核心章节绑定一个 Example 或 Regression。
- 把 `docs/parameter-map.md` 和 `docs/example-regression-map.md` 中的资料条目回填为正文叙述。
- 按 `docs/paper-reading-workflow.md` 完成核心论文 MinerU 转换和中文讲解笔记。
- 建立稳定的 Markdown/HTML/PDF 构建流程；v0.10 仍只保证 Markdown/HTML。
- 对 public GitHub 仓库中的 PDF 和运行产物做版权与体积审计。

## v0.10 构建方式

生成合订 Markdown 和 HTML 预览：

```bash
python scripts/build_v10.py
```

生成的文件：

- `dist/pic-tutor-v0.10.md`
- `dist/pic-tutor-v0.10.html`（若本机存在 `pandoc`）
