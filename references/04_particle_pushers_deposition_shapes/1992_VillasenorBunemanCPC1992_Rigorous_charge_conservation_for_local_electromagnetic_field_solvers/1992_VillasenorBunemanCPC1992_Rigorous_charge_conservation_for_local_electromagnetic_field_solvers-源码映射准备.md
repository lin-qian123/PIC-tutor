# VillasenorBunemanCPC1992 源码映射准备

## 状态

本文件不是论文逐段讲解，但当前也已经不再是“只有 access audit”的占位文档。项目内现已具备：

- 本地 PDF；
- MinerU Markdown；
- `images/`；
- 第一轮中文讲解与 reading log。

因此这里记录的是当前 Chapter 5 已经可以依赖、并且还应继续往下压的 paper-to-source 映射骨架。

## 映射框架

| 论文中应查找的内容 | WarpX / PIC-tutor 对应层 | 当前可核源码 |
|---|---|---|
| local electromagnetic field solvers 下的严格电荷守恒条件 | Villasenor current deposition 对 cell-crossing segment 的局部组织 | `../warpx/Source/Particles/Deposition/CurrentDeposition.H:2347` 起的 Villasenor 路径 |
| 为什么作者强调不把一般位移拆成正交 move | `earliest-crossing` 驱动的真实轨迹分段，而不是先假设正交子移动 | Chapter 5 `5.11` 与中文讲解 `2.3` |
| 粒子轨迹如何按 cell crossings 分段 | crossing counting 与 segment-wise deposition | `CurrentDeposition.H` 中 Villasenor explicit/implicit 路径 |
| four-/seven-/ten-boundary 几何怎样落到现代代码 | `cell_crossings -> num_segments -> local this_J* writeback` | `CurrentDeposition.H` Villasenor kernel 主循环与 Chapter 5 对照段 |
| 为什么结果比 Esirkepov 更“tight stencil” | 按 segment 局部沉积，而不是一次性 old/new support | Chapter 5 当前代码笔记与 kernel 展开 |
| 二维 four-boundary 通量与当代 `XZ/RZ` kernel 的关系 | `directional transport * (old+new)/2 * dt_seg/dt` | `CurrentDeposition.H` 的 `XZ/RZ` Villasenor 分支 |
| 三维交叉项 `ΔxΔyΔz/12` 如何在代码中留下痕迹 | `one_third/one_sixth` 双横向 old/new mixed average | `CurrentDeposition.H` 的 3D Villasenor 分支 |
| 显式与隐式时间层恢复差异 | `relative_time` vs `x_n/u_n/u_{n+1/2}` | `manuscript/chapters/05-deposition-shapes.md` 当前对应段与源码位置 |
| 与 collocated / shared-memory 的当前实现边界 | WarpX 当前对 Villasenor 的工程限制 | `WarpXParticleContainer.cpp:546-650` 与 `752-835` |

## 当前继续深化的必做项

1. 继续把 `Eq.(6)-(9)` 四边界通量公式讲得更细，并更明确地对到 `XZ/RZ` kernel 的 `directional transport * transverse average` 结构。
2. 继续核对论文中的 segment-by-segment current construction，确认当前 Chapter 5 对 crossing 分段逻辑的文字是否与原文一致。
3. 明确论文是在什么几何和 staggering 假设下给出 local solver 的严格守恒，并与 WarpX 当前条件逐项比较。
4. 把论文中的局部守恒推导与当前 WarpX 显式 / 隐式 Villasenor 分支分开写清，避免把现代工程扩展误当成原文主结果。
5. 如果论文含有比源码更清楚的 stencil 图示或 crossing 图示，后续应优先把这些图插回 Chapter 5。

## 当前正文边界

当前 Chapter 5 对 Villasenor-Buneman 的叙述可以明确到：

- 代码和 regression 已经证明 WarpX 当前如何实现这条 charge-conserving deposition 路径；
- 本地 PDF、MinerU 和第一轮中文讲解已经足以支撑第一轮 paper-backed 主叙述；
- 但更细的逐式讲解、图示回填和论文-源码逐项并列仍未完成。
