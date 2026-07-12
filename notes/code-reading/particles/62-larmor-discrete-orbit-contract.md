# Larmor 离散轨道合同

## 2026-07-13：从 checksum surface 提取逐帧轨道量

输入来源是当前 WarpX checkout 的 `Examples/Tests/larmor/inputs_test_2d_larmor`，运行产物位于 `runs/stage-c-validation/larmor_single_process/`。新增脚本 `scripts/analyze_larmor_orbit_contract.py`，读取 `diag1000000` 到 `diag1000010` 的 6 个 Full plotfile，逐帧提取 electron/positron 的 `x`、`z`（WarpX 2D XZ 诊断中的 `particle_position_x/y`）和 `u_x/u_z`。

合同当前通过：

- 时间严格递增，6 帧输出间隔一致，为 `1.4741589604685529e-10 s`；
- 两个 species 在每帧均保持 1 个粒子，位置和动量均为有限值；
- 外部 `B_y=7.8110417851950768e-4 T`、`gamma=1.1` 对应的连续回旋频率为 `1.2489287798252453e8 rad/s`；
- 以每个输出间隔估算的 Boris rotation angle 为 `1.8410675470607752e-2 rad`。

这条合同只把原先 checksum surface 中的离散时间序列变成可审计的轨道数据入口，不把 radius spread、momentum drift 或 phase increment 自动升级成论文 gate。原因是当前输入同时包含 AMR、PML、current correction、divergence cleaning，且没有输出 half-step velocity；因此它仍不能证明 Vay Appendix B 的 gyroradius 条件，也不能证明 Higuera-Cary 2017 的 Poincare topology / resonance-island 结论。

报告：`runs/stage-c-validation/larmor_single_process/larmor-orbit-contract.{json,md}`。
