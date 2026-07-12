# Uniform-B pusher runtime contract

## 2026-07-13：Boris/Vay/Higuera-Cary 窄化对照

为推进 Vay Appendix B 和 Higuera-Cary topology 的 runtime 缺口，使用当前 `../warpx/build_full/bin/warpx.2d...` 从 `Examples/Tests/larmor/inputs_test_2d_larmor` 启动三条 case-local sibling，并通过命令行覆盖：

- `amr.max_level=0`：移除 MR；
- `algo.maxwell_solver=none`、`warpx.const_dt=1e-9`：不推进自洽电磁场，只保留外部粒子 `B_y`；
- `boundary.field_lo/hi=none`、`warpx.do_dive_cleaning=0`：移除 PML 和 div-cleaning；
- `algo.particle_pusher=boris|vay|higuera`；
- `max_step=80`、`diag1.intervals=1`：逐步输出 81 个 Full plotfile。

`scripts/compare_uniform_b_pushers.py` 对三条产物统一读取 XZ 轨道：位置分量是 `particle_position_x/y`，面内动量分量是 `particle_momentum_x/z`。三条 case 的输入、输出 cadence、粒子数和有限状态检查全部通过：

| pusher | radius relative spread | momentum norm relative spread | momentum phase increment |
|---|---:|---:|---:|
| Boris | `3.88925585e-3` | `4.13289029e-15` | `1.24730914e-1` |
| Vay | `3.88925585e-3` | `1.05200844e-14` | `1.24730914e-1` |
| Higuera-Cary | `3.21781662e-3` | `9.01721517e-15` | `1.24772899e-1` |

这组结果是“窄化 external-B particle-pusher 对照”，不是论文图形复现。当前 diagnostics 仍没有 half-step velocity，因此不能关闭 Vay Appendix B 的 `v^{i+1/2}` gyroradius 条件；也没有 Poincare-section consumer，因此不能关闭 Higuera-Cary 论文的 resonance-island/topology 边界。运行时结束后 binary 在 AMReX finalize 后留下不退出的尾进程，但 81 个 plotfile 和 `warpx_used_inputs` 已完整落盘；该环境行为单独保留，不计入物理 PASS。

报告：`runs/stage-c-validation/pusher_uniform_b_comparison/contract.{json,md}`。
