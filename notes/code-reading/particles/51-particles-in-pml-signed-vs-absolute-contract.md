# 51 particles in PML：官方有符号 gate 与强化绝对值 gate 的边界

绑定源码：

- `../warpx/Examples/Tests/particles_in_pml/analysis_particles_in_pml.py`
- `scripts/analyze_particles_in_pml_contract.py`
- `scripts/audit_particles_in_pml_analysis_contract.py`

## 1. 两个 analysis 实际计算的不是同一个量

当前 WarpX 官方 analysis 使用：

```python
max_Efield = max(Ex_array.max(), Ey_array.max(), Ez_array.max())
assert max_Efield < tolerance_abs
```

这不是全场绝对值范数。若负向电场峰值的绝对值大于阈值，而正向峰值没有超过阈值，官方 gate 仍可能通过。

项目独立 contract 则对每个分量先取绝对值最大值，再在三个分量之间取最大值：

```python
field_max = {
    name: float(np.max(np.abs(grid["boxlib", name].to_ndarray())))
    for name in ("Ex", "Ey", "Ez")
}
max_abs = max(field_max.values())
```

两者都可以作为可执行证据，但证据含义不同：前者复现上游现有 regression consumer，后者是对残余场强更严格的 reader-side audit。

## 2. 3D AMR sibling 的具体分歧

官方 `test_3d_particles_in_pml_mr` 2-rank 运行在 `diag1000200` 上给出：

- signed official value：`106.43539539129057 < 110`，官方 gate 通过；
- independent `Ex_min`：`-110.3993781372607`；
- independent `Ex_max`：`106.43539539129057`；
- absolute maximum：`110.3993781372607 > 110`，强化 gate 失败。

因此，本书把该 sibling 归类为：

> producer 完成、官方 consumer 通过、绝对值强化审计失败的 AMR 判据边界。

它不能被写成“3D AMR particles-in-PML 强验证已通过”，也不能仅凭这一次结果断言 PML 实现错误。当前能确定的是官方 analysis 对负向峰值不敏感，而独立 contract 暴露了一个超出官方阈值 `0.399378...` 的负向峰值。

## 3. 后续上游修正建议

若要把这条 active regression 升级为严格的残余场合同，最小 analysis 修正是把官方 consumer 改为逐分量绝对值最大值：

```python
max_Efield = max(
    abs(Ex_array).max(), abs(Ey_array).max(), abs(Ez_array).max()
)
```

这不是本项目对 `../warpx` 的修改；它只是基于当前 checkout 的可审计修正建议。修正后还需要重新运行 3D AMR case，并决定是保留 `110` 阈值、提高实现容差，还是调整输入/网格分辨率。当前 v0.42 只收录判据审计和建议，不伪造 upstream 已修复。

源码审计命令：

```bash
python scripts/audit_particles_in_pml_analysis_contract.py \
  --warpx-root ../warpx \
  --output-dir runs/stage-c-validation/particles-in-pml-analysis-source-contract
```
