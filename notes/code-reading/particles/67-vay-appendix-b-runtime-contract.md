# Vay Appendix B: bounded uniform-B runtime contract

## Case

在当前 WarpX 2D binary 上，从官方 `larmor/inputs_test_2d_larmor` 输入出发，命令行覆盖 `max_level=0`、`maxwell_solver=none`、关闭 PML 和 divergence cleaning、固定外部 `B_y`、分别选择 `boris/vay/higuera`，并令 `max_step=80`、`diag1.intervals=1`。三条 case 各生成 `diag1000000` 到 `diag1000080` 共 81 个 Full plotfile。

## 结果

`scripts/analyze_vay_appendix_b_runtime_contract.py` 在既有比较 JSON 上执行更窄的 Appendix-B gate：离散动量旋转角、position-update velocity proxy、gyroradius proxy 和动量范数保持。

| quantity | maximum error/spread |
|---|---:|
| Boris/Vay discrete phase error | `< 1.0e-10 rad` |
| Higuera-Cary phase deviation from Boris/Vay reference | `4.1984e-05 rad` |
| position-update velocity proxy | `1.3363e-14` |
| gyroradius proxy | `4.7740e-15` |
| momentum norm spread | `1.0520e-14` |

这一步把原先 uniform-B sibling 提升为一个有明确 Appendix-B 判据的 bounded runtime contract，但仍不宣称论文图形逐点复现：公共 Full plotfile 没有直接 half-step velocity attribute，速度和回旋半径仍由相邻帧位置差重建。

## 退出边界

三条 case 都在写出最后的 `diag1000080` 后进入同一个 `ComputeDivE: Unknown algorithm` finalize tail。该尾部与 physics data contract 分开记录；报告以完整 81 帧数据为准，不把非零进程退出升级为 pusher 物理失败。

报告：`runs/stage-c-validation/vay-appendix-b-runtime-proxy/contract.{json,md}`；底层 81 帧轨道位于 `runs/stage-c-validation/vay_appendix_b_orbit/`。
