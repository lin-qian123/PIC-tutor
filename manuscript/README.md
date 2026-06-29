# PIC 程序详解：从物理模型到 WarpX 源码

这是 `PIC-tutor` 的 Markdown-first 书稿。当前收束版本是 `v0.22` PML 理论文献闭环版，目标是先形成一条可复查、可审读、可验证的主线，再逐章加深公式推导、源码逐行讲解、图表和可复现实验。

## 版本边界

- WarpX 路径：`../warpx`
- WarpX 分支：`pkuHEDPbranch`
- 当前 WarpX commit：`8c488b1a9`
- 第 2、3、3A、4、5、6 章已按当前 checkout 重新核对核心源码行号；第 6 章已在 v0.17/v0.18/v0.19 补入 Lehe et al. 2016、Kirchen et al. 2016 和 Godfrey et al. 2014 的 PSATD/Galilean/NCI 文献闭环，并在 v0.20 把 WarpX filter/current-correction/finite-order PSATD 和 NCI analysis 判据拆成源码对照表；第 7 章已完成 v0.12 AMR coarse-fine 图形化证据正文、v0.13 HTML 排版收口、v0.14 transition-zone validation 检查清单、v0.15 dedicated transition-zone 测试草案、v0.16 regression patch 计划、v0.21 PSATD PML 源码/公式/regression 边界，并在 v0.22 补入 Berenger/APML、Lee/Vay 文献线索和 `C1-C25` 系数分层；后续仍需真正实现 route-count reduced diagnostic 与 regression。
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

## v0.22 构建

详见 [VERSION.md](VERSION.md)。生成合订 Markdown 和 HTML 预览：

```bash
python ../scripts/build_v22.py
```

历史 v0.1 版本说明冻结在 [VERSION-v0.1.md](VERSION-v0.1.md)，可用 `python ../scripts/build_v01.py` 重建 v0.1 合订稿。
历史 v0.2 版本说明冻结在 [VERSION-v0.2.md](VERSION-v0.2.md)，可用 `python ../scripts/build_v02.py` 重建 v0.2 合订稿。
历史 v0.3 版本说明冻结在 [VERSION-v0.3.md](VERSION-v0.3.md)，可用 `python ../scripts/build_v03.py` 重建 v0.3 合订稿。
历史 v0.4 版本说明冻结在 [VERSION-v0.4.md](VERSION-v0.4.md)，可用 `python ../scripts/build_v04.py` 重建 v0.4 合订稿。
历史 v0.5 版本说明冻结在 [VERSION-v0.5.md](VERSION-v0.5.md)，可用 `python ../scripts/build_v05.py` 重建 v0.5 合订稿。
历史 v0.6 版本说明冻结在 [VERSION-v0.6.md](VERSION-v0.6.md)，可用 `python ../scripts/build_v06.py` 重建 v0.6 合订稿。
历史 v0.7 版本说明冻结在 [VERSION-v0.7.md](VERSION-v0.7.md)，可用 `python ../scripts/build_v07.py` 重建 v0.7 合订稿。
历史 v0.8 版本说明冻结在 [VERSION-v0.8.md](VERSION-v0.8.md)，可用 `python ../scripts/build_v08.py` 重建 v0.8 合订稿。
历史 v0.9 版本说明冻结在 [VERSION-v0.9.md](VERSION-v0.9.md)，可用 `python ../scripts/build_v09.py` 重建 v0.9 合订稿。
历史 v0.10 版本说明冻结在 [VERSION-v0.10.md](VERSION-v0.10.md)，可用 `python ../scripts/build_v10.py` 重建 v0.10 合订稿。
历史 v0.11 版本说明冻结在 [VERSION-v0.11.md](VERSION-v0.11.md)，可用 `python ../scripts/build_v11.py` 重建 v0.11 合订稿。
历史 v0.12 版本说明冻结在 [VERSION-v0.12.md](VERSION-v0.12.md)，可用 `python ../scripts/build_v12.py` 重建 v0.12 合订稿。
历史 v0.13 版本说明冻结在 [VERSION-v0.13.md](VERSION-v0.13.md)，可用 `python ../scripts/build_v13.py` 重建 v0.13 合订稿。
历史 v0.14 版本说明冻结在 [VERSION-v0.14.md](VERSION-v0.14.md)，可用 `python ../scripts/build_v14.py` 重建 v0.14 合订稿。
历史 v0.15 版本说明冻结在 [VERSION-v0.15.md](VERSION-v0.15.md)，可用 `python ../scripts/build_v15.py` 重建 v0.15 合订稿。
历史 v0.16 版本说明冻结在 [VERSION-v0.16.md](VERSION-v0.16.md)，可用 `python ../scripts/build_v16.py` 重建 v0.16 合订稿。
历史 v0.17 版本说明冻结在 [VERSION-v0.17.md](VERSION-v0.17.md)，可用 `python ../scripts/build_v17.py` 重建 v0.17 合订稿。
历史 v0.18 版本说明冻结在 [VERSION-v0.18.md](VERSION-v0.18.md)，可用 `python ../scripts/build_v18.py` 重建 v0.18 合订稿。
历史 v0.19 版本说明冻结在 [VERSION-v0.19.md](VERSION-v0.19.md)，可用 `python ../scripts/build_v19.py` 重建 v0.19 合订稿。
历史 v0.20 版本说明冻结在 [VERSION-v0.20.md](VERSION-v0.20.md)，可用 `python ../scripts/build_v20.py` 重建 v0.20 合订稿。
历史 v0.21 版本说明冻结在 [VERSION-v0.21.md](VERSION-v0.21.md)，可用 `python ../scripts/build_v21.py` 重建 v0.21 合订稿。
