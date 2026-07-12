# 3D AMR particles-in-PML：signed/absolute 分量与层级合同

本 note 对当前 `../warpx` 的官方 `test_3d_particles_in_pml_mr` 末态做 reader-side 分解，避免把官方的

```python
max(Ex.max(), Ey.max(), Ez.max())
```

误读成全场绝对值范数。可执行脚本为 `scripts/analyze_particles_in_pml_signed_absolute_levels.py`，报告为
`runs/stage-c-validation/particles_in_pml_3d_mr_mpi2/signed-absolute-level-contract.{json,md}`。

## 观测结果

该运行有两个 field frame：`diag1000000` 初始帧和 `diag1000200` 末态帧。初始帧的 `Ex/Ey/Ez` 全部为零；末态 finest covering grid 为 `256x256x256`，阈值为 `110`：

| 分量 | 正向最大值 | 负向最小值 | 绝对值最大值 |
|---|---:|---:|---:|
| `Ex` | `106.4353954` | `-110.3993781` | `110.3993781` |
| `Ey` | `102.5970828` | `-102.5970828` | `102.5970828` |
| `Ez` | `102.5970828` | `-102.5970828` | `102.5970828` |

因此：

- 官方 signed consumer 看到的最大值是 `106.4353954 < 110`，会通过；
- absolute consumer 看到 `|Ex|=110.3993781 > 110`，会失败；
- 唯一越过阈值的分量是负向 `Ex`，不是 `Ey/Ez` 的对称峰；
- 负向 `Ex` 峰值位置约为 `(-25.875,-0.375,3.125) um`，位于靠近 `x` 低边界的 in-domain PML 区域。

level 0 与 level 1 covering-grid 读取给出相同的极值，说明该差异不是独立 reader 在 coarse/fine 选择上的偶然错位；它来自同一末态场上的符号敏感性。当前证据仍不能决定应该修改上游 analysis 的范数、AMR/PML 演化，还是该维度专用的 `110` 容差，因此不修改 `../warpx`，也不把该 sibling 标成强通过。

## 证据边界

这条 contract 只回答三个问题：哪个时间帧触发差异、哪个分量/符号触发差异、该峰值在 coarse/fine 读取下是否稳定。它不证明负向峰值一定是数值错误，也不提供阈值重标定依据。成书中最准确的分类仍是：

> 3D AMR + particles-in-PML producer 可运行；官方 signed gate 通过；严格 absolute residual-field gate 因负向 `Ex` 峰值失败。

源码判据审计继续由 `scripts/audit_particles_in_pml_analysis_contract.py` 负责；本 note 的运行级补充不修改上游脚本。
