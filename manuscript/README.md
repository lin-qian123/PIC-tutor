# PIC 程序详解：从物理模型到 WarpX 源码

这是 `PIC-tutor` 的 Markdown-first 书稿。当前收束版本是 `v0.1` 第一卷草稿，目标是先形成一条可审阅的主线，再逐章加深公式推导、源码逐行讲解、图表和可复现实验。

## 版本边界

- WarpX 路径：`../warpx`
- WarpX 分支：`pkuHEDPbranch`
- 当前 WarpX commit：`8c488b1a9`
- 历史章节中出现的旧 commit 表示当时阅读基线；终稿前需要逐章按当前 checkout 重新核对源码行号。
- 本书稿不修改 WarpX 原仓库。
- 本版优先覆盖显式电磁 PIC 主线：Vlasov-Maxwell、宏粒子、gather-push-deposit-field solve、WarpX 主循环、粒子推进、沉积、场求解、边界/AMR、诊断和案例。

## 目录

1. [写作说明](chapters/00-preface.md)
2. [动理学模型与 PIC 的基本思想](chapters/01-kinetic-models.md)
3. [PIC 总循环](chapters/02-pic-loop.md)
4. [WarpX 主演化路径](chapters/03-warpx-evolve.md)
5. [WarpX 初始化链](chapters/03a-warpx-initialization.md)
6. [粒子推进器](chapters/04-particle-pushers.md)
7. [电荷、电流沉积与形函数](chapters/05-deposition-shapes.md)
8. [电磁场求解器](chapters/06-field-solvers.md)
9. [边界条件、PML 与 AMR](chapters/07-boundaries-amr.md)
10. [诊断、验证与案例](chapters/08-diagnostics-cases.md)
11. [文献路线与后续扩写计划](chapters/09-literature-roadmap.md)

## 证据文件

- 源码映射：`../docs/source-map.md`
- 章节模板：`../docs/chapter-template.md`
- 文献库：`../bibliography/warpx-refs.bib`
- PDF 文献索引：`../references/00_index/current_inventory.md`

## v0.1 构建

详见 [VERSION.md](VERSION.md)。生成合订 Markdown 和 HTML 预览：

```bash
python ../scripts/build_v01.py
```
