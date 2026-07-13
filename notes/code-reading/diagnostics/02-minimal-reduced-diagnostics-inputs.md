# 第 8 章 reduced diagnostics 最小输入合同

本笔记把 `FieldProbe`、`ParticleHistogram2D` 和 `LoadBalanceCosts` 三类 reduced diagnostics 的最小输入入口绑定到当前 WarpX 示例。它验证的是参数骨架、官方 analysis consumer 和章节边界，不把“文件写出”升级成物理收敛性证明。

## 1. 三类最小骨架

### FieldProbe

当前官方 `Examples/Tests/reduced_diags/inputs_test_3d_reduced_diags` 同时给出 point、integrated point、line 和 plane：

```ini
warpx.reduced_diags_names = FP FP_integrate FP_line FP_plane
FP.type = FieldProbe
FP.probe_geometry = Point
FP_integrate.integrate = 1
FP_line.probe_geometry = Line
FP_plane.probe_geometry = Plane
```

读者应进一步指定 `intervals`、坐标和 line/plane 的 `resolution`，再用对应的 `FP_*.txt` 或项目 reader-side 脚本检查输出。`FieldProbe` 的解析 diffraction gate 仍必须单独看 `field_probe` case，不能由 schema 检查代替。

### ParticleHistogram2D

`Examples/Physics_applications/laser_ion/inputs_test_2d_laser_ion_acc` 给出 `z`--`uz` 相空间的完整参数骨架：

```ini
PhaseSpaceIons.type = ParticleHistogram2D
PhaseSpaceIons.histogram_function_abs(t,x,y,z,ux,uy,uz,w) = "z"
PhaseSpaceIons.histogram_function_ord(t,x,y,z,ux,uy,uz,w) = "uz"
PhaseSpaceIons.value_function(t,x,y,z,ux,uy,uz,w) = "w"
```

实际输入还要给出 bin 数、范围、axis labels 和 species。该 writer 落盘为 openPMD mesh，不能因为 companion `.txt` 为空就判断输出缺失；物理收敛性仍需独立的粒子数或分辨率对照。

### LoadBalanceCosts

最小的 text reduced diagnostic 入口是：

```ini
warpx.reduced_diags_names = LBC
LBC.type = LoadBalanceCosts
algo.load_balance_costs_update = Heuristic
```

官方 `analysis_reduced_diags_load_balance_costs.py` 不读取 plotfile，而是从 `LBC.txt` 重建 rank-level efficiency，并比较 load balance 前后的效率。`Timers` 是另一种 cost source；不能从输入文件名或 test 名称推断某个 solver 已切到 PSATD，必须回读实际 input。

## 2. 可重复检查

```bash
python scripts/audit_diagnostics_minimal_inputs.py \
  --project-root . \
  --warpx-root ../warpx \
  --output-json runs/stage-c-validation/diagnostics-minimal-inputs/contract.json \
  --output-md runs/stage-c-validation/diagnostics-minimal-inputs/contract.md
```

当前合同共 12 项。它确认示例、章节和 official consumer 仍相互对应，但不替代 `FieldProbe` 的解析 gate、`ParticleHistogram2D` 的收敛研究或 `LoadBalanceCosts` 的真实运行结果。
