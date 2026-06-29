# PIC 程序详解：从物理模型到 WarpX 源码

这是 `PIC-tutor` 的 Markdown-first 书稿。当前收束版本是 `v0.6` 场求解器读者侧图表草稿，目标是先形成一条可复查的主线，再逐章加深公式推导、源码逐行讲解、图表和可复现实验。

## 版本边界

- WarpX 路径：`../warpx`
- WarpX 分支：`pkuHEDPbranch`
- 当前 WarpX commit：`8c488b1a9`
- 第 2、3、3A、4、5、6 章已按当前 checkout 重新核对核心源码行号；其他章节中出现的旧 commit 表示当时阅读基线，后续仍需逐章校准。
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

## v0.6 构建

详见 [VERSION.md](VERSION.md)。生成合订 Markdown 和 HTML 预览：

```bash
python ../scripts/build_v06.py
```

历史 v0.1 版本说明冻结在 [VERSION-v0.1.md](VERSION-v0.1.md)，可用 `python ../scripts/build_v01.py` 重建 v0.1 合订稿。
历史 v0.2 版本说明冻结在 [VERSION-v0.2.md](VERSION-v0.2.md)，可用 `python ../scripts/build_v02.py` 重建 v0.2 合订稿。
历史 v0.3 版本说明冻结在 [VERSION-v0.3.md](VERSION-v0.3.md)，可用 `python ../scripts/build_v03.py` 重建 v0.3 合订稿。
历史 v0.4 版本说明冻结在 [VERSION-v0.4.md](VERSION-v0.4.md)，可用 `python ../scripts/build_v04.py` 重建 v0.4 合订稿。
历史 v0.5 版本说明冻结在 [VERSION-v0.5.md](VERSION-v0.5.md)，可用 `python ../scripts/build_v05.py` 重建 v0.5 合订稿。
