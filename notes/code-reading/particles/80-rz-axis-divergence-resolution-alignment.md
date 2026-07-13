# RZ axis divergence resolution-family alignment

v0.99 将 v0.98 的 axis stencil 对照从单一 `256x512` 末态扩展到已有的三档 resolution family。每个 case 都读取 axis `Er/Ez/divE`，先按同一 reader-side 一阶纵向差分去掉 `Dz(Ez)`，再比较源码定义的 `4*Er/dr` 与 naive `2*Er/dr`。

| correction | grid | naive `2*Er/dr` RMSE | source `4*Er/dr` RMSE |
|---|---:|---:|---:|
| on | `64x128` | `2.7752e14` | `3.7296e13` |
| off | `64x128` | `2.7615e14` | `1.6705e14` |
| on | `128x256` | `2.2645e14` | `6.6455e13` |
| off | `128x256` | `2.2721e14` | `2.9943e13` |
| on | `256x512` | `2.5968e14` | `1.7287e13` |
| off | `256x512` | `2.5999e14` | `1.2638e14` |

6/6 个 case 都支持 source coefficient 更接近输出的判断，合同分类为 `RZ_AXIS_STENCIL_ALIGNMENT_CROSS_RESOLUTION_OBSERVED_CHARGE_BOUNDARY_OPEN`。这提高了 solver-native axis stencil 解释的跨分辨率稳定性，但仍不证明 rho-side inverse-volume scaling、deposition kernel、位置/诊断转换或完整 charge closure 已正确。报告见 `runs/stage-c-validation/rz-axis-divergence-resolution-v0.99/contract.{json,md}`。
