# PIC-tutor v0.23

版本日期：2026-06-29

## 定位

`v0.23` 是 `PIC-tutor` 的 LeeCPC2015 获取审计与公式映射准备版。它继承 `v0.22` 的 PML 理论文献闭环，继续把第 7 章的 PML/PSATD 文献短板从“知道应该读哪篇论文”推进到“主引用目录、开放获取审计、metadata-only 状态和后续公式映射框架”。

本版仍不修改 `../warpx`。第 7 章新增 `7.5.5 v0.23 LeeCPC2015 获取审计与公式映射准备`。本版的核心写作边界是：WarpX 主引用是 CPC 2015 的 `LeeCPC2015`，AIP 2016 只是相关会议版；当前 OpenAlex/Crossref/OSTI 已证明存在 accepted-manuscript 线索，但本机仍未取得可转换 PDF，因此项目不能声称已经完成 MinerU 或论文逐段讲解。

本版仍不是出版终稿。它新增 LeeCPC2015 主引用目录和获取审计，但尚未取得授权 PDF。后续应通过机构访问、OSTI 可用全文或 AIP 可访问 PDF 补齐原文资产，再执行 MinerU 转换、逐段中文讲解和公式映射。

## 源码基线

- 本书项目仓库：`/Volumes/PHILIPS/programs/PIC/PIC-tutor`
- WarpX 只读源码：`../warpx`
- 当前 WarpX 分支：`pkuHEDPbranch`
- 当前 WarpX commit：`8c488b1a9`

v0.23 只修改 `PIC-tutor` 书稿项目，不修改 `../warpx` 原仓库。本版继续按当前 checkout 核对 `Docs/source/refs.bib`、`bibliography/warpx-refs.bib`、`PML::PushPSATD()`、`PsatdAlgorithmPml.cpp` 和 `Examples/Tests/pml` analysis 入口。后续若 WarpX 更新，必须重新校准源码行号、文档段落和测试入口后再发布新版。

## v0.23 章节范围

| 章节 | 文件 | v0.23 状态 | 下一步缺口 |
|---|---|---|---|
| 写作说明 | `chapters/00-preface.md` | 沿用 v0.1 | 需同步最终出版路线 |
| 动理学模型 | `chapters/01-kinetic-models.md` | 沿用 v0.1 | Hockney-Eastwood、Yee 等一手文献闭环未完成 |
| PIC 总循环 | `chapters/02-pic-loop.md` | 已做 v0.2 源码校准 | 仍需把基础文献和公式变量定义做出版级补齐 |
| WarpX 主演化路径 | `chapters/03-warpx-evolve.md` | 已做 v0.2 源码校准 | `OneStep_sub1()`、JRhom、implicit 分支还需专章级精读 |
| WarpX 初始化链 | `chapters/03a-warpx-initialization.md` | 已做 v0.2 长草稿收束 | 需要拆短小节、补流程图、压缩过长审计段落 |
| 粒子推进器 | `chapters/04-particle-pushers.md` | 已做 v0.3 源码校准 | 仍需压缩多物理长段，并把更多 validation 表格图形化 |
| 沉积与形函数 | `chapters/05-deposition-shapes.md` | 已做 v0.4 源码校准 | Esirkepov、Villasenor-Buneman 论文仍需 MinerU 闭环，`ChargeDeposition` 的 ABLASTR 模板还需继续逐行展开 |
| 场求解器 | `chapters/06-field-solvers.md` | 已补 Lehe/Kirchen/Godfrey 文献闭环，并在 v0.20 增补 PSATD/NCI 源码机制对照表 | 仍需 `X1-X4` 系数逐项推导 |
| 边界、PML 与 AMR | `chapters/07-boundaries-amr.md` | 已在 v0.23 增补 LeeCPC2015 主引用获取审计、metadata-only 状态和公式映射准备表 | 仍需取得 Lee/Vay 授权 PDF、完成 MinerU 逐段讲解，并实现 dedicated transition-zone regression |
| 诊断、验证与案例 | `chapters/08-diagnostics-cases.md` | 沿用 v0.1 | 需要更多本地运行图表和 reader-side analysis |
| 文献路线 | `chapters/09-literature-roadmap.md` | 沿用 v0.1 提纲 | 需要和 `docs/literature-map.md` 去重并完成优先级 |
| 符号表 | `appendices/A-symbols.md` | 沿用 v0.1 最小草稿 | 需要单位、参数、常用缩写和索引 |

## v0.23 已完成的增量

- 冻结 `manuscript/VERSION-v0.22.md`，避免重建 v0.22 时误用 v0.23 版本说明。
- 新增 `scripts/build_v23.py`，生成 `dist/pic-tutor-v0.23.md` 与 `dist/pic-tutor-v0.23.html`。
- 把 `scripts/build_v22.py` 改为读取冻结的 `manuscript/VERSION-v0.22.md`，保持 v0.22 版本说明可复现。
- 新增 `references/08_boundaries_pml_geometry/2015_LeeCPC2015_Efficiency_of_the_PML_with_high-order_FD_and_pseudo-spectral_Maxwell_solvers/`，作为 WarpX 主引用 `LeeCPC2015` 的专属目录。
- 新增 `access-audit.md`，记录 OpenAlex、Crossref、OSTI、ScienceDirect、Elsevier API 和 AIP 会议版的获取状态。
- 新增 `2015_LeeCPC2015_...-公式映射准备.md`，列出全文到位后要映射到 `PML.cpp`、`PML::PushPSATD()`、`PsatdAlgorithmPml.cpp` 和 PML regression 的主题。
- 更新 manifest，将 `LeeCPC2015` 标为 `metadata_only`，不把它误记为已下载 PDF。
- 在第 7 章新增 `7.5.5 v0.23 LeeCPC2015 获取审计与公式映射准备`，明确当前还不能声称完成 PDF/MinerU/逐段中文讲解。

## 成书前必须补齐

- 每章记录最终采用的 WarpX commit，并避免同章混用未说明的历史行号。
- 每章补齐公式变量定义、参数入口、源码路径、行号和真实源码块。
- 至少为核心章节绑定一个 Example 或 Regression。
- 把 `docs/parameter-map.md` 和 `docs/example-regression-map.md` 中的资料条目回填为正文叙述。
- 按 `docs/paper-reading-workflow.md` 完成核心论文 MinerU 转换和中文讲解笔记。
- 建立稳定的 Markdown/HTML/PDF 构建流程；v0.23 仍只保证 Markdown/HTML。
- 对 public GitHub 仓库中的 PDF 和运行产物做版权与体积审计。

## v0.23 构建方式

生成合订 Markdown 和 HTML 预览：

```bash
python scripts/build_v23.py
```

生成的文件：

- `dist/pic-tutor-v0.23.md`
- `dist/pic-tutor-v0.23.html`（若本机存在 `pandoc`）
