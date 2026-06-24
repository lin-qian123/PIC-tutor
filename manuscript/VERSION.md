# PIC-tutor v0.2

版本日期：2026-06-25

## 定位

`v0.2` 是 `PIC-tutor` 的可审校草稿版。它继承 `v0.1` 的第一卷范围，但不再只做合订，而是先把最核心的主循环与初始化章节推进到可复查状态：

1. 第 2 章 `PIC 总循环`：同步当前 WarpX 源码基线，重核显式电磁无 subcycling 路径、PSATD/FDTD 分支和最小 Langmuir 运行闭环。
2. 第 3 章 `WarpX 主演化路径`：同步 `main.cpp -> WarpX::GetInstance() -> InitData() -> Evolve() -> OneStep()` 的调用图和关键行号。
3. 第 3A 章 `WarpX 初始化链`：把长材料稿收束为可审校长草稿，明确构造期、`InitData()` 分叉、fresh run/restart、外场、粒子初始化和初始 diagnostics 的边界。

本版仍不是出版终稿。它的目标是给后续 v0.3/v0.4 打好“源码证据可信、章节能读、构建可复现”的基础。

## 源码基线

- 本书项目仓库：`/Volumes/PHILIPS/programs/PIC/PIC-tutor`
- WarpX 只读源码：`../warpx`
- 当前 WarpX 分支：`pkuHEDPbranch`
- 当前 WarpX commit：`8c488b1a9`

v0.2 只修改 `PIC-tutor` 书稿项目，不修改 `../warpx` 原仓库。章节里的源码行号按上述 checkout 复核；后续若 WarpX 更新，必须重新校准行号后再发布新版。

## v0.2 章节范围

| 章节 | 文件 | v0.2 状态 | 下一步缺口 |
|---|---|---|---|
| 写作说明 | `chapters/00-preface.md` | 沿用 v0.1 | 需同步最终出版路线 |
| 动理学模型 | `chapters/01-kinetic-models.md` | 沿用 v0.1 | Hockney-Eastwood、Yee 等一手文献闭环未完成 |
| PIC 总循环 | `chapters/02-pic-loop.md` | 已做 v0.2 源码校准 | 仍需把基础文献和公式变量定义做出版级补齐 |
| WarpX 主演化路径 | `chapters/03-warpx-evolve.md` | 已做 v0.2 源码校准 | `OneStep_sub1()`、JRhom、implicit 分支还需专章级精读 |
| WarpX 初始化链 | `chapters/03a-warpx-initialization.md` | 已做 v0.2 长草稿收束 | 需要拆短小节、补流程图、压缩过长审计段落 |
| 粒子推进器 | `chapters/04-particle-pushers.md` | 沿用 v0.1 长草稿 | 多物理粒子过程需拆分 |
| 沉积与形函数 | `chapters/05-deposition-shapes.md` | 沿用 v0.1 长草稿 | Esirkepov、Villasenor-Buneman 论文仍需 MinerU 闭环 |
| 场求解器 | `chapters/06-field-solvers.md` | 沿用 v0.1 长草稿 | PSATD、PML、implicit/hybrid 验证小节需回填 |
| 边界、PML 与 AMR | `chapters/07-boundaries-amr.md` | 沿用 v0.1 | 需要把 boundary/EB/parallelization 笔记进一步合并 |
| 诊断、验证与案例 | `chapters/08-diagnostics-cases.md` | 沿用 v0.1 | 需要更多本地运行图表和 reader-side analysis |
| 文献路线 | `chapters/09-literature-roadmap.md` | 沿用 v0.1 提纲 | 需要和 `docs/literature-map.md` 去重并完成优先级 |
| 符号表 | `appendices/A-symbols.md` | 沿用 v0.1 最小草稿 | 需要单位、参数、常用缩写和索引 |

## v0.2 已完成的增量

- 冻结 `manuscript/VERSION-v0.1.md`，避免重建 v0.1 时误用 v0.2 版本说明。
- 新增 v0.2 当前版本说明，并把构建输出切到 `dist/pic-tutor-v0.2.md` 与 `dist/pic-tutor-v0.2.html`。
- 把第 2、3、3A 章的旧源码基线 `063f8b586f...` 更新到 `8c488b1a9`。
- 复核并更新 `Source/Evolve/WarpXEvolve.cpp`、`Source/Initialization/WarpXInitData.cpp` 相关关键行号。
- 给第 2、3、3A 章补上 v0.2 校准说明，明确哪些分支已核，哪些分支仍是后续工作。

## 成书前必须补齐

- 每章记录最终采用的 WarpX commit，并避免同章混用未说明的历史行号。
- 每章补齐公式变量定义、参数入口、源码路径、行号和真实源码块。
- 至少为核心章节绑定一个 Example 或 Regression。
- 把 `docs/parameter-map.md` 和 `docs/example-regression-map.md` 中的资料条目回填为正文叙述。
- 按 `docs/paper-reading-workflow.md` 完成核心论文 MinerU 转换和中文讲解笔记。
- 建立稳定的 Markdown/HTML/PDF 构建流程；v0.2 仍只保证 Markdown/HTML。
- 对 public GitHub 仓库中的 PDF 和运行产物做版权与体积审计。

## v0.2 构建方式

生成合订 Markdown 和 HTML 预览：

```bash
python scripts/build_v02.py
```

生成的文件：

- `dist/pic-tutor-v0.2.md`
- `dist/pic-tutor-v0.2.html`（若本机存在 `pandoc`）
