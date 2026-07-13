# RZ axis divergence fitted coefficient

v0.100 在跨分辨率 RMSE 对照之外，对同一组 6 个 correction-on/off axis 输出执行无偏最小二乘拟合。reader 先用一阶纵向差分去除 `Dz(Ez)`，再拟合

$$
D_r^{\mathrm{obs}} \approx a\,E_r/\Delta r.
$$

得到的系数与 naive 2 和源码系数 4 的距离如下：

| correction | grid | fitted `a` | `|a-2|` | `|a-4|` |
|---|---:|---:|---:|---:|
| on | `64x128` | `4.308992` | `2.308992` | `0.308992` |
| off | `64x128` | `3.246228` | `1.246228` | `0.753772` |
| on | `128x256` | `3.550571` | `1.550571` | `0.449429` |
| off | `128x256` | `3.773158` | `1.773158` | `0.226842` |
| on | `256x512` | `3.886482` | `1.886482` | `0.113518` |
| off | `256x512` | `3.346320` | `1.346320` | `0.653680` |

6/6 个拟合系数都更接近 4 而不是 2，分类为 `RZ_AXIS_STENCIL_FIT_COEFFICIENT_CROSS_RESOLUTION_OBSERVED_CHARGE_BOUNDARY_OPEN`。这进一步支持 solver-native axis stencil 的 operator alignment，但不能单独证明 rho scaling、deposition kernel 或完整 charge closure。报告见 `runs/stage-c-validation/rz-axis-divergence-fit-v0.100/contract.{json,md}`。
