# 40 RZ mode writeback and inverse-volume scaling：RZ 电流沉积不是 kernel 写完就结束

绑定源码：

- `../warpx/Source/Particles/Deposition/CurrentDeposition.H`
- `../warpx/Source/Particles/MultiParticleContainer.cpp`
- `../warpx/Source/Particles/WarpXParticleContainer.cpp`
- `../warpx/Source/FieldSolver/WarpXPushFieldsEM.cpp`

前置阅读：

- `../notes/code-reading/particles/32-current-deposition-continuity-and-geometry-boundaries.md`
- `../notes/code-reading/particles/39-current-deposition-writeback-rules-in-1dz-rcylinder-rsphere.md`

第 5 章如果只写到 `CurrentDeposition.H` 里的 kernel，会让读者误以为 “current deposition = kernel 原子加结束”。对 RZ/RCYLINDER/RSPHERE 来说，这还差最后一层网格体积语义；而对 RZ 来说，`m>0` 模态的写回也不是把 mode-0 公式直接复制一份。

## 1. implicit Esirkepov 的 RZ 写回：`Jr/Jz` 和 `Jtheta` 不是同一公式

`doChargeConservingDepositionShapeNImplicit(...)` 在 `XZ/RZ` 分支里的 mode-0 主干是：

```cpp
sdxi += wq*invdtd.x*(sx_old[i] - sx_new[i])*0.5_rt*(sz_new[k] + sz_old[k]);
... Jx_arr(..., 0, 0)

Real const sdyj = wq*vy*invvol*(
    one_third*(sx_new[i]*sz_new[k] + sx_old[i]*sz_old[k])
   +one_sixth*(sx_new[i]*sz_old[k] + sx_old[i]*sz_new[k]));
... Jy_arr(..., 0, 0)

sdzk += wq*invdtd.z*(sz_old[k] - sz_new[k])*0.5_rt*(sx_new[i] + sx_old[i]);
... Jz_arr(..., 0, 0)
```

源码位置：`../warpx/Source/Particles/Deposition/CurrentDeposition.H:992-1038`。

也就是说，RZ 的 mode 0 仍沿用 “径向/轴向守恒差分 + 角向平均写回” 这一层物理分工。

但 `m>0` 模态不是简单把这三条 mode-0 标量值乘上一个相同相位。源码紧跟着写成：

```cpp
const Complex djr_cmplx = 2._rt * sdxi * xy_mid;
const Complex djt_cmplx = -2._rt * I*(...)*wq*invdtd.x/(amrex::Real)imode
                          *(Complex(sx_new[i]*sz_new[k], 0._rt)*(xy_new - xy_mid)
                          + Complex(sx_old[i]*sz_old[k], 0._rt)*(xy_mid - xy_old));
const Complex djz_cmplx = 2._rt * sdzk * xy_mid;
```

源码位置：`../warpx/Source/Particles/Deposition/CurrentDeposition.H:1000-1038`。

这里要记三件事：

1. `Jr` 与 `Jz`
   - `m>0` 仍由已经累计好的 `sdxi/sdzk` 乘 `xy_mid = e^{im\theta_mid}` 得到复模态；
   - 所以它们和 mode 0 的关系比较直接。

2. `Jtheta`
   - 不走 “先算一个 mode-0 `sdyj` 再乘相位”；
   - 而是单独用 `xy_new / xy_mid / xy_old`、`1/imode` 和新旧 shape 组合重建 `djt_cmplx`。

3. 符号约定
   - 源码注释明确写着这个式子前面的 minus sign 来自 “different convention with respect to Davidson et al.”；
   - 因此书里不能把 RZ 模态公式轻率写成“照 Davidson 抄一遍”。

所以，第 5 章里讲 RZ current deposition 时，最稳妥的表述不是 “RZ 是 XZ 加上 Fourier modes”，而是：

- mode 0 的径向/轴向守恒结构确实与 `XZ` 主干同构；
- 但 `m>0` 尤其是 `Jtheta`，有自己单独的复模态重建公式。

## 2. deposition kernel 写完后，RZ/RCYLINDER/RSPHERE 还要做 inverse-volume scaling

多物种入口 `MultiParticleContainer::DepositCurrent()` 在所有 species 沉积完成后，会对

- `WARPX_DIM_RZ`
- `WARPX_DIM_RCYLINDER`
- `WARPX_DIM_RSPHERE`

统一调用：

```cpp
WarpX::GetInstance().ApplyInverseVolumeScalingToCurrentDensity(
    J[lev][0], J[lev][1], J[lev][2], lev);
```

源码位置：`../warpx/Source/Particles/MultiParticleContainer.cpp:605-610`。
单 species 路径里也有同样调用，见 `../warpx/Source/Particles/WarpXParticleContainer.cpp:960-964`。

这说明 `CurrentDeposition.H` kernel 写回的量还不是最终物理电流密度；至少在柱/球对称几何下，它还缺一层按实际网格体积的缩放。

## 3. `ApplyInverseVolumeScalingToCurrentDensity(...)`：先处理轴附近 wraparound，再除以几何体积因子

真正的缩放实现在 `WarpX::ApplyInverseVolumeScalingToCurrentDensity(...)`：

```cpp
// Rescale current in r-z mode since the inverse volume factor was not
// included in the current deposition.
```

源码位置：`../warpx/Source/FieldSolver/WarpXPushFieldsEM.cpp:1455-1456`。

这段实现的关键信息是：

1. 轴附近 guard-cell wraparound
   - `Jr`、`Jt`、`Jz` 都先把负半径 guard cell 的沉积折回到轴上方；
   - 各分量、各模态的正负号并不完全相同。

2. RZ / RCYLINDER 的主缩放
   - 非轴点统一除以 `2*pi*r`；
   - 即把 kernel 中未包含的环向体积因子补回来。

3. RSPHERE 的主缩放
   - 非轴点统一除以 `4*pi*r*r`；
   - 源码注释说明它来自球壳体积因子的近似，刻意略掉最高阶项。

4. 轴点特殊处理
   - `Jr`、`Jt` 在轴上被强制置零；
   - `Jz` 在 `RZ/RCYLINDER` 下不是简单置零，而是除以 `pi*dr*axis_volume_factor`；
   - `axis_volume_factor` 来自 Verboncoeur 2001，可在 runtime 通过 `m_verboncoeur_axis_correction` 在 `1/3` 与 `1/4` 之间切换。

源码位置：`../warpx/Source/FieldSolver/WarpXPushFieldsEM.cpp:1400-1586`。

因此，第 5 章如果只写 “RZ current deposition 在 kernel 里完成 old/new difference 累加”，仍然少了一层关键事实：

- kernel 负责把粒子轨迹写成守恒的离散 source；
- `ApplyInverseVolumeScalingToCurrentDensity(...)` 再把它变成与柱/球坐标真实控制体积相容的 current density。

## 4. 对第 5 章最值得带走的结论

1. RZ mode 不是纯粹的 `XZ + Fourier copy`
   - `Jr/Jz` 的 `m>0` 模态确实从 `sdxi/sdzk` 乘 `xy_mid` 而来；
   - 但 `Jtheta` 有自己独立的 `djt_cmplx` 重建式。

2. RZ/RCYLINDER/RSPHERE 的 deposition 不是 kernel 原子加就结束
   - 后续还必须做 inverse-volume scaling；
   - 否则书里讲到的 `J` 仍不是最终供场求解器消费的物理密度量。

3. 轴附近也不是普通内点公式
   - 既有 wraparound 符号规则；
   - 也有 `Jr/Jt=0`、`Jz` 走 Verboncoeur 修正体积因子的特殊处理。
