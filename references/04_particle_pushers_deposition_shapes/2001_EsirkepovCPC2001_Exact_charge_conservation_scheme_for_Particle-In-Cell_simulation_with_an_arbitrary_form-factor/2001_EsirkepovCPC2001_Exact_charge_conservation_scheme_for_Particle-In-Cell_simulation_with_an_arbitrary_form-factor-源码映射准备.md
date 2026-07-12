# EsirkepovCPC2001 源码映射准备

## 状态

本文件不是论文逐段讲解，但已经不再处于“只有 metadata”的早期状态。当前项目内已经具备：

- arXiv 合法全文 PDF；
- MinerU Markdown；
- `images/`；
- 第一轮中文讲解与 reading log。

2026-07-11 的出版信息复核进一步确认了 CPC 题名、卷期、页码和 DOI；ScienceDirect 直接 PDF 地址虽可发现，但当前环境仍返回下载错误/HTTP 403。因此这里把“发表版身份已核实”和“发表版正文尚未取得”明确拆开。

因此这里记录的不是“拿到全文后再说”的空框架，而是当前 Chapter 5 已经可用、并且还应继续深化的 paper-to-source 映射骨架。

## 映射框架

| 论文中应查找的内容 | WarpX / PIC-tutor 对应层 | 当前可核源码 |
|---|---|---|
| arbitrary form-factor 下的精确离散连续性方程 | `ShapeFactors.H`、old/new shape difference、current prefix accumulation | `../warpx/Source/Particles/ShapeFactors.H`、`CurrentDeposition.H` |
| `density decomposition` 与 `W^1+W^2+W^3=S_{new}-S_{old}` | `sx_old-sx_new` / `sy_old-sy_new` / `sz_old-sz_new` 三组方向差分源 | `../warpx/Source/Particles/Deposition/CurrentDeposition.H:955-989` 一带的 3D loop |
| 新旧粒子位置如何进入守恒电流构造 | `compute_shape_factor` 与 `compute_shifted_shape_factor` 的配合 | `../warpx/Source/Particles/ShapeFactors.H:93-156` |
| `Eq.(23)` 的 `1/3,1/6` 系数怎样落到代码 | `one_third/one_sixth` 双横向 old/new mixed average | `CurrentDeposition.H:955-989` |
| 守恒电流的实际离散写法 | `doEsirkepovDepositionShapeN<N>()` kernel | `../warpx/Source/Particles/Deposition/CurrentDeposition.H:675-1215` |
| form-factor order 如何改变 stencil | `nox/noy/noz` 对 shape order 与 kernel 分派的控制 | `../warpx/Source/Particles/WarpXParticleContainer.cpp:654-695` |
| 与 direct deposition 的对比边界 | `q v S` 风格的 direct current assignment 与 charge-conserving current 之间的合同差异 | `CurrentDeposition.H:47-274` 与 Chapter 5 对照段 |
| 几何/网格条件的当前实现边界 | collocated grid 与 shared-memory deposition 的限制 | `WarpXParticleContainer.cpp:546-650` |
| 论文声称的 “only possible linear procedure” | `sdxi/sdyj/sdzk` 三组 prefix loop 不应被误读成经验配方 | Chapter 5 `5.11` 与中文讲解 `4.4-4.5` |

## 当前继续深化的必做项

1. 继续把论文里的 `only possible linear procedure` 论证压实到正文，而不只停留在中文讲解笔记里。
2. 对照论文中的符号，给 `sx_old/sx_new`、`W^1/W^2/W^3` 及 related mixed averages 补更统一的正文记号，避免主文只剩源码变量名。
3. 明确论文中是如何处理 arbitrary form-factor 与不同维度路径的，并与 WarpX 当前的 1D/2D/3D/RZ 宏分支比较。
4. 判断 WarpX 当前 implicit Esirkepov 路径哪些仍属于论文原始结构，哪些已是后续工程扩展。
5. 一旦取得 CPC 出版版 PDF，按 title / abstract / section numbering / `Eq.(23)` / second-order spline algorithm 五项做预印本-发表版对照；目前 title、书目信息和公开摘要已完成 metadata-level 核对，正文级四项仍待 PDF。

## 当前正文边界

当前 Chapter 5 对 Esirkepov 的叙述可以明确到：

- 代码和 regression 已经证明 WarpX 当前如何实现这条 charge-conserving deposition 路径；
- arXiv 合法全文、MinerU 和第一轮中文讲解已经足以支撑第一轮 paper-backed 主叙述；
- 但更细的逐式讲解与 CPC 发表版差异核对仍未完成。
