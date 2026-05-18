# Boundary 01: PML 数据结构、阻尼系数与更新路径

绑定源码：

- `../warpx/Source/BoundaryConditions/PML.H`
- `../warpx/Source/BoundaryConditions/PML.cpp`
- `../warpx/Source/BoundaryConditions/WarpXEvolvePML.cpp`
- `../warpx/Source/BoundaryConditions/PML_current.H`
- `../warpx/Source/BoundaryConditions/WarpX_PML_kernels.H`
- `../warpx/Docs/source/usage/parameters.rst`

## 1. PML 类的职责边界

`PML` 类不是单个 kernel，而是一个“PML 子域 + 系数缓存 + 数据交换”的管理器：

```cpp
class PML
{
public:
    PML (...,
         int ncell, int delta, ...,
         int do_moving_window, int pml_has_particles, int do_pml_in_domain,
         ...
         bool do_pml_dive_cleaning, bool do_pml_divb_cleaning,
         ...,
         amrex::Real v_sigma_sb,
         ablastr::fields::MultiFabRegister& fields,
         amrex::IntVect do_pml_Lo = amrex::IntVect::TheUnitVector(),
         amrex::IntVect do_pml_Hi = amrex::IntVect::TheUnitVector());
```

源码位置：`../warpx/Source/BoundaryConditions/PML.H:137-156`。

## 2. SigmaBox：PML 阻尼系数的缓存层

`PML.H` 里真正关键的数据结构是 `SigmaBox`：

```cpp
struct SigmaBox
{
    SigmaVect sigma;
    SigmaVect sigma_cumsum;
    SigmaVect sigma_star;
    SigmaVect sigma_star_cumsum;
    SigmaVect sigma_fac;
    SigmaVect sigma_cumsum_fac;
    SigmaVect sigma_star_fac;
    SigmaVect sigma_star_cumsum_fac;
    amrex::Real v_sigma;
};
```

源码位置：`../warpx/Source/BoundaryConditions/PML.H:46-76`。

它同时缓存：

- 原始阻尼剖面；
- 半格点阻尼剖面；
- 剖面积分；
- 时间推进直接使用的乘法因子；
- PML 电流阻尼使用的累计因子。

## 3. PML BoxArray 的生成方式

`PML.cpp` 先根据 regular domain 是否是单个矩形，分成两条路径：

```cpp
if (is_single_box_domain) {
    return MakeBoxArray_single(...);
} else {
    return MakeBoxArray_multiple(...);
}
```

源码位置：`../warpx/Source/BoundaryConditions/PML.cpp:271-281`。

单一矩形域时，`MakeBoxArray_single()` 用 `adjCell` 在外侧长出厚度为 `ncell[idim]` 的 PML box。多 patch 场景则由 `MakeBoxArray_multiple()` 先 grow patch，再取补集与交集构造 PML 包围层。

这里还有一个约束：

```cpp
WARPX_ALWAYS_ASSERT_WITH_MESSAGE(
    grid_bx.length(idim) > ncell[idim],
    "Consider using larger amr.blocking_factor with PMLs");
```

源码位置：`../warpx/Source/BoundaryConditions/PML.cpp:215-224`。

这说明多 patch 情况下，PML 厚度不能超过 patch 在该方向的长度，否则不同 patch 周围的 PML 会重叠。

## 4. sigma 剖面如何离散

`SigmaBox` 构造时先设置一个方向依赖的系数：

```cpp
fac[idim] = 4.0_rt*PhysConst::c/(dx[idim]*static_cast<Real>(delta[idim]*delta[idim]));
```

源码位置：`../warpx/Source/BoundaryConditions/PML.cpp:327-330`。

然后 `FillLo()` / `FillHi()` 用离边界距离平方构造阻尼：

```cpp
Real offset = static_cast<Real>(glo-i);
p_sigma[i-slo] = fac*(offset*offset);
...
offset = static_cast<Real>(glo-i) - 0.5_rt;
p_sigma_star[i-sslo] = fac*(offset*offset);
```

源码位置：`../warpx/Source/BoundaryConditions/PML.cpp:83-92`。

所以当前实现里：

- `sigma` 是二次增长 profile；
- `sigma_star` 对应半格点 profile；
- `delta` 控制阻尼增长深度，而不是总厚度。

## 5. PML 主阻尼入口

`WarpXEvolvePML.cpp` 的顶层入口是：

```cpp
void WarpX::DampPML ()
{
    for (int lev = 0; lev <= finest_level; ++lev) {
        DampPML(lev);
    }
}
```

源码位置：`../warpx/Source/BoundaryConditions/WarpXEvolvePML.cpp:45-50`。

Cartesian 实际工作函数是 `DampPML_Cartesian()`。它取出 `pml_E`、`pml_B`、`sigba` 和各场的 stagger 信息，然后调用 `warpx_damp_pml_*` kernels。

## 6. split field 的阻尼不是整矢量统一乘系数

以 `warpx_damp_pml_ex()` 为例：

```cpp
if (sy == 0) {
    Ex(i,j,k,PMLComp::xy) *= sigma_star_fac_y[j-ylo];
} else {
    Ex(i,j,k,PMLComp::xy) *= sigma_fac_y[j-ylo];
}

if (sz == 0) {
    Ex(i,j,k,PMLComp::xz) *= sigma_star_fac_z[k-zlo];
} else {
    Ex(i,j,k,PMLComp::xz) *= sigma_fac_z[k-zlo];
}
```

源码位置：`../warpx/Source/BoundaryConditions/WarpX_PML_kernels.H:77-89`。

这说明：

- `Exy` 与 `Exz` 分开阻尼；
- 用 `sigma_fac` 还是 `sigma_star_fac`，由该分量在对应方向是 nodal 还是 staggered 决定。

## 7. PML 电流怎样进入 split E 更新

如果 `warpx.pml_has_particles = 1`，PML 区域允许粒子继续传播；这时粒子电流也要进入 split 电场。

`push_ex_pml_current()` 的形式是：

```cpp
alpha_xy = sigjy[k-ylo]/(sigjy[k-ylo]+sigjz[l-zlo]);
alpha_xz = sigjz[l-zlo]/(sigjy[k-ylo]+sigjz[l-zlo]);
Ex(j,k,l,PMLComp::xy) = Ex(j,k,l,PMLComp::xy) - mu_c2_dt  * alpha_xy * jx(j,k,l);
Ex(j,k,l,PMLComp::xz) = Ex(j,k,l,PMLComp::xz) - mu_c2_dt  * alpha_xz * jx(j,k,l);
```

源码位置：`../warpx/Source/BoundaryConditions/PML_current.H:27-36`。

这意味着 `J_x` 不是直接加到“整体 `E_x`”上，而是按 split 方向分摊给 `Exy` 和 `Exz`。

## 8. PML 电流阻尼

若开启 `warpx.do_pml_j_damping = 1`，`DampJPML()` 会进一步对 PML 电流做阻尼。它使用 `sigma_cumsum_fac` / `sigma_star_cumsum_fac`：

```cpp
const Real* sigma_cumsum_fac_j_x = sigba[mfi].sigma_cumsum_fac[0].data();
const Real* sigma_star_cumsum_fac_j_x = sigba[mfi].sigma_star_cumsum_fac[0].data();
```

源码位置：`../warpx/Source/BoundaryConditions/WarpXEvolvePML.cpp:274-285`。

对应 kernel 如 `damp_jx_pml()`：

```cpp
jx(j,k,l) = jx(j,k,l) * sigsjx[j-xlo] * sigjy[k-ylo] * sigjz[l-zlo];
```

源码位置：`../warpx/Source/BoundaryConditions/PML_current.H:98-112`。

## 9. 参数语义和实现的对应关系

PML 相关参数见 `../warpx/Docs/source/usage/parameters.rst:888-950`，其主要对应关系如下：

- `warpx.pml_ncell`：PML 总厚度
- `warpx.pml_delta`：sigma 增长深度
- `warpx.do_pml_in_domain`：PML 在域内还是域外
- `warpx.pml_has_particles`：是否在 PML 中推进粒子
- `warpx.do_pml_j_damping`：是否对 PML current 再阻尼
- `warpx.v_particle_pml`：PML 中粒子吸收速度假设
- `warpx.do_pml_dive_cleaning` / `warpx.do_pml_divb_cleaning`：是否对 PML 中的 `F/G` 清理场启用阻尼

## 10. 当前阶段的稳定结论

1. WarpX 的 PML 是独立 PML 网格、split fields 和 sigma 缓存的组合，不是单个边界公式。
2. `SigmaBox` 把阻尼剖面、积分剖面和离散推进系数全部预计算下来。
3. PML 阻尼按 split component 和 stagger 位置分别施加。
4. 若允许粒子进入 PML，则电流也要按 split 方式注入，并可继续做 PML current damping。

## 11. 当前最稳定的 regression 入口

`Examples/Tests/pml/` 这一组 tests 现在至少应拆成五条不同的验证合同，而不是再笼统写成 “PML”：

1. `analysis_pml_yee.py`
   - 对 `test_2d_pml_x_yee`
   - 从最终 `Ex/Ey/Ez/Bx/By/Bz` 重建总电磁能量
   - 计算反射率 `R = E_end / E_start`
   - 要求其相对理论 `5.683000058954201e-07` 的误差低于 `5%`
2. `analysis_pml_ckc.py`
   - 对 `test_2d_pml_x_ckc`
   - 同样检查最终反射率
   - 但理论值换成 `1.8015e-06`
3. `analysis_pml_psatd.py`
   - 同时覆盖 `test_2d_pml_x_psatd` 与 `test_2d_pml_x_galilean`
   - 先用 `diag1000050` 复算初始电磁能量并要求与硬编码参考值一致到 `1e-14`
   - 再要求最终反射率低于 `1e-6`
   - 因而它验证的是 `PSATD/Galilean PSATD + PML` 的低反射率合同，不是简单的 checksum
4. `analysis_pml_psatd_rz.py`
   - 对 `test_rz_pml_psatd`
   - 不是比较能量比，而是在脉冲离域后直接要求域内 `max(|Er|,|Ez|) < 2`
   - 因而它验证的是 RZ radial PML 的残余场衰减
5. checksum / restart / workflow 边界
   - `test_2d_pml_x_psatd_restart` 与 `test_2d_pml_x_yee_restart` 通过顶层 `Examples/analysis_default_restart.py` 做逐字段 restart 一致性比较
   - `test_3d_pml_psatd_dive_divb_cleaning` 当前 `analysis=OFF`
   - 它只应诚实记录为 `psatd + pml + do_dive/divb_cleaning` 的 workflow baseline

这组回归最重要的边界是：WarpX 的 PML tests 现在并不都在测同一种“吸收率”。2D Cartesian FDTD/PSATD 在测反射率，RZ PSATD 在测离域后的残余场，而 restart 变体在测逐字段可重复性。

## 12. 下一步

- 继续精读 `WarpX_PEC.cpp` 与 `PEC_Insulator.cpp`，整理 PEC/PMC/PECInsulator 的镜像与沉积规则。
- 回到第 7 章，把 periodic 约束、Silver-Mueller half-push 条件和 PML 数据流写进正文。
