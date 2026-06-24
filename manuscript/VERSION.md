# PIC-tutor v0.1

版本日期：2026-06-25

## 定位

`v0.1` 是 `PIC-tutor` 的第一卷草稿版。它不追求覆盖完整 38 章规划，而是先把现有材料收束成一条可阅读主线：

1. PIC 的动理学模型和宏粒子思想。
2. PIC 总循环和 WarpX 主演化路径。
3. WarpX 初始化链、粒子推进、沉积和场求解。
4. 边界、PML、AMR、诊断和第一批验证案例。
5. 文献路线和后续扩写计划。

本版适合用来审查全书写法、术语、证据链和章节节奏；它还不是可出版终稿。

## 源码基线

- 本书项目仓库：`/Volumes/PHILIPS/programs/PIC/PIC-tutor`
- WarpX 只读源码：`../warpx`
- 当前 WarpX 分支：`pkuHEDPbranch`
- 当前 WarpX commit：`8c488b1a9`

成书前仍需逐章重读源码并记录当天 commit。本版会保留旧章节中已经写入的历史 commit 作为“当时阅读基线”，但 `v0.1` 总说明以这里的当前 checkout 为准。

## v0.1 章节范围

| 章节 | 文件 | v0.1 状态 | 主要缺口 |
|---|---|---|---|
| 写作说明 | `chapters/00-preface.md` | 可读草稿 | 需同步最终出版路线 |
| 动理学模型 | `chapters/01-kinetic-models.md` | 可读草稿 | Hockney-Eastwood、Yee 等文献闭环未完成 |
| PIC 总循环 | `chapters/02-pic-loop.md` | 可审阅草稿 | 需要按当前 WarpX commit 重核行号 |
| WarpX 主演化路径 | `chapters/03-warpx-evolve.md` | 可审阅草稿 | `OneStep_*` 分支和 callbacks 还需终审 |
| WarpX 初始化链 | `chapters/03a-warpx-initialization.md` | 材料充分的长草稿 | 需要压缩、分节、同步验证表 |
| 粒子推进器 | `chapters/04-particle-pushers.md` | 材料充分的长草稿 | 多物理粒子过程需拆到后续卷或单章 |
| 沉积与形函数 | `chapters/05-deposition-shapes.md` | 材料充分的长草稿 | Esirkepov、Villasenor-Buneman 论文仍需 MinerU 闭环 |
| 场求解器 | `chapters/06-field-solvers.md` | 材料充分的长草稿 | PSATD、PML、implicit/hybrid 验证小节需再回填 |
| 边界、PML 与 AMR | `chapters/07-boundaries-amr.md` | 可读草稿 | 需要把 boundary/EB/parallelization 笔记进一步合并 |
| 诊断、验证与案例 | `chapters/08-diagnostics-cases.md` | 可读草稿 | 需要更多本地运行图表和 reader-side analysis |
| 文献路线 | `chapters/09-literature-roadmap.md` | 提纲草稿 | 需要和 `docs/literature-map.md` 去重并完成优先级 |
| 符号表 | `appendices/A-symbols.md` | 最小草稿 | 需要单位、参数、常用缩写和索引 |

## 成书前必须补齐

- 每章记录最终采用的 WarpX commit。
- 每章补齐公式变量定义、参数入口、源码路径、行号和真实源码块。
- 至少为核心章节绑定一个 Example 或 Regression。
- 把 `docs/parameter-map.md` 和 `docs/example-regression-map.md` 中的资料条目回填为正文叙述。
- 按 `docs/paper-reading-workflow.md` 完成核心论文 MinerU 转换和中文讲解笔记。
- 建立稳定的 Markdown/HTML/PDF 构建流程。
- 对 public GitHub 仓库中的 PDF 和运行产物做版权与体积审计。

## v0.1 构建方式

生成合订 Markdown：

```bash
python scripts/build_v01.py
```

生成的文件：

- `dist/pic-tutor-v0.1.md`
- `dist/pic-tutor-v0.1.html`（若本机存在 `pandoc`）
