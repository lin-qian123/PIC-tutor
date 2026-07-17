# PIC-tutor v0.110

这是面向读者的 PIC 教程版本说明，不是开发日志。书稿从连续的 Vlasov-Maxwell 模型出发，逐步建立宏粒子、网格、时间推进、粒子推进器、沉积、场求解器、边界、AMR 与诊断之间的关系，最后用 WarpX 的源码和可运行案例把这些概念落到程序行为上。

## 读者在本版可以学到什么

- 用 Vlasov-Maxwell 方程解释 PIC 中粒子与场为什么必须相互交换源项。
- 从 leapfrog 时间层读懂一个显式 PIC step，而不是把 `Evolve()` 看成黑盒。
- 区分 Boris、Vay 与 Higuera-Cary 等粒子推进器的物理假设、离散结构和适用边界。
- 解释 shape factor、charge/current deposition、current correction、guard cell 与 AMR 同步如何共同影响守恒和噪声。
- 根据 CFL、Debye 长度、plasma frequency、边界和诊断量选择一个可解释的输入案例。
- 用源码路径、输入参数、输出量和回归分析共同判断“程序运行了”是否等于“物理结果可信”。

## 证据范围

本版绑定同级只读 WarpX checkout 的源码、官方文档、示例、regression 和已取得的论文资产。正文把结论分成三层：数学/文献解释、当前源码映射、实际运行或分析结果。局部 runtime 通过不自动代表完整几何、阶数、AMR 或收敛阶覆盖；`BOUNDARY`、`OPEN`、`UNPROVEN` 等词表示证据边界，不是措辞上的保留。

v0.110 重新执行了 RZ/RSPHERE 正式收敛 study 的第二组 12 个 2-rank producer。correction-on 的 14 项 repeat-slope comparison 全部通过，最大绝对 slope 差为 `2.0135e-11`；这只证明重复 family 的 slope 一致性，仍不等于 formal numerical order 或 axis-charge closure 已完成。完整证据见 [当前缺口登记](../docs/current-book-gap-register.md) 和 v0.110 的发布审计文件。

## 源码快照与复现

- WarpX 分支：`pkuHEDPbranch`
- WarpX commit：`063f8b586f04321e13150ae3e730e0794ca75cb1`
- 源码入口：`$WARPX_ROOT/Source/`
- 官方文档：`$WARPX_ROOT/Docs/source/`
- 示例和回归：`$WARPX_ROOT/Examples/`、`$WARPX_ROOT/Regression/`

在仓库根目录执行 `python scripts/build_v110.py` 可重建合订 Markdown、HTML 和 PDF；执行 `python scripts/verify_v110_build.py --build-log <log>` 可检查产物的章节、链接、图表、页数和证据合同。历史版本记录保存在 `docs/version-history-v0.110.md`，不再作为正文前言拼入读者版。
