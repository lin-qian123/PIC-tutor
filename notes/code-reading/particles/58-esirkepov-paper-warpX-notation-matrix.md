# Esirkepov 论文记号与 WarpX 变量对照

本 note 把第 5 章中容易被混写的论文记号和当前 WarpX `CurrentDeposition.H` 变量固定成一张可复查的对照表。源码审计脚本为 `scripts/audit_esirkepov_notation_contract.py`，报告归档于 `runs/stage-c-validation/esirkepov-notation-source-contract/contract.{json,md}`。

## 对照表

| 论文层对象 | WarpX 当前实现 | 代码中的直接证据 | 不能外推的内容 |
|---|---|---|---|
| `W^1`：x 向 shape difference | `sx_old - sx_new` 沿 `i` 前缀累计到 `sdxi`，写入 `Jx` | `CurrentDeposition.H` 的 `sdxi` loop | 不是所有几何分支都共用 3D 数组下标 |
| `W^2`：y 向 shape difference | `sy_old - sy_new` 沿 `j` 前缀累计到 `sdyj`，写入 `Jy` | `sdyj` loop | RZ/XZ 中 `y` 是 out-of-plane 分量，数组布局不同 |
| `W^3`：z 向 shape difference | `sz_old - sz_new` 沿 `k` 前缀累计到 `sdzk`，写入 `Jz` | `sdzk` loop | 1D/2D/RZ 会减少实际循环维度 |
| old/new form factor | `sx_old/sx_new`、`sy_old/sy_new`、`sz_old/sz_new` | `Compute_shape_factor` + `Compute_shifted_shape_factor` | 同名数组不等于论文中的 publisher 排版符号逐字一致 |
| transverse tensor-product factor | `one_third` 与 `one_sixth` 的 `old-old / old-new / new-old / new-new` 混合平均 | `Jx/Jy/Jz` 三组内层表达式 | 该映射来自预印本与源码，不能写成 CPC 定稿已逐页核对 |
| current normalization | `invdtd.x/y/z = transverse inverse cell area / dt` | `invdtd` 初始化 | 不能把它简化为所有分量都只乘 `1/dt` |
| final source writeback | `Atomic::AddNoRet` 到 `Jx_arr/Jy_arr/Jz_arr` | 三个方向的 writeback | 不替代 `SyncCurrent()`、guard-cell 或 AMR coarse-fine contract |

## 证据边界

这张表关闭的是“论文方向分解如何落到源码变量”的记号歧义，不是 publisher-PDF compare。当前本地论文全文是作者 arXiv 预印本；CPC 发表版的 DOI、题名、卷期和页码已核实，但 ScienceDirect PDF 下载页仍无法提供可读取定稿。因此正文可以使用 `W^1/W^2/W^3 -> sdxi/sdyj/sdzk` 的结构对应，但不能声称 abstract、section numbering、`Eq.(23)` 排版和 second-order spline 段落已经逐页比较完成。

同样，这不是 runtime 全覆盖声明。已有 1D/2D/3D Langmuir 和 RZ/径向分支证据必须继续按 geometry、shape、AMR、boundary 和 implicit 分层引用；本表只为这些运行证据提供统一记号入口。
