# `WarpXFluidContainer` 与 PIC / fields / HybridPIC 的耦合：它沉积到普通 `rho/J`，不是 `HybridPICModel` 电子闭合本身

绑定源码：

- `../warpx/Source/Fluids/WarpXFluidContainer.cpp`
- `../warpx/Source/FieldSolver/FiniteDifferenceSolver/HybridPICModel/HybridPICModel.cpp`
- `../warpx/Source/Evolve/WarpXEvolve.cpp`
- `../warpx/Source/WarpX.cpp`
- `../warpx/Source/Utils/WarpXMovingWindow.cpp`
- `../warpx/Examples/Tests/langmuir_fluids/`

这一篇只回答一个容易混淆的问题：

> WarpX 里的 `Fluids/` 和 `HybridPICModel` 到底是不是同一件事？

当前 worktree 的答案是否定的。

- `HybridPICModel` 是 field solver 内部的 electron-fluid closure；
- `Fluids/` 是额外 cold-fluid species 的 runtime layer。

## 1. Lorentz source：fluid 直接 gather `Efield_aux/Bfield_aux`

`GatherAndPush()` 的入口已经说明，fluid species 不是自己解场，而是像粒子一样从现有主场里 gather：

```cpp
GatherAndPush(fields,
    *fields.get(FieldType::Efield_aux, Direction{0}, lev),
    *fields.get(FieldType::Efield_aux, Direction{1}, lev),
    *fields.get(FieldType::Efield_aux, Direction{2}, lev),
    *fields.get(FieldType::Bfield_aux, Direction{0}, lev),
    *fields.get(FieldType::Bfield_aux, Direction{1}, lev),
    *fields.get(FieldType::Bfield_aux, Direction{2}, lev),
    cur_time, lev);
```

而 gather 时，源码会先把各分量从自身 staggering 插值回 fluid 的 nodal `N` 点。

这说明 fluid species 的 Lorentz source 语义是：

- 使用和主 PIC 场同一份 `aux` fields；
- 只是在使用前先插值到 nodal fluid state 位置。

## 2. 外场 parser：fluid species 也能挂自己的 `E/B_external_function`

`WarpXFluidContainer::ReadParameters()` 里，fluid species 还能读自己独立的 parser 外场：

```cpp
pp_species_name.query("B_ext_init_style", m_B_ext_s);
pp_species_name.query("E_ext_init_style", m_E_ext_s);
```

当样式是 `parse_*_ext_function` 时，会编译：

```cpp
utils::parser::Store_parserString(
    pp_species_name, "Bx_external_function(x,y,z,t)", str_Bx_ext_function);
...
```

随后在 `GatherAndPush()` 里：

- 非 boosted 时，直接按当前 `(x,y,z,t)` 评估并加到 `E/B`；
- boosted 时，先变回 lab frame 坐标评估，再做 Lorentz transform 带回 boosted frame。

所以 fluid 外场合同和粒子外场 / grid external field 又不一样：它是 per-fluid-species 的 parser-defined source。

## 3. fluid momentum source 用的还是粒子侧 Higuera-Cary pusher

流体 Lorentz source 并没有自写一套 ODE integrator，而是直接复用粒子侧 Higuera-Cary momentum update：

```cpp
UpdateMomentumHigueraCary(tmp_Ux, tmp_Uy, tmp_Uz,
    Ex_Nodal, Ey_Nodal, Ez_Nodal,
    Bx_Nodal, By_Nodal, Bz_Nodal, q, m, dt );
```

因此当前 worktree 的 fluid source-step 不是“Euler source update”，而是：

- 先把连续介质状态局部还原成 `U = NU/N`
- 再把它当成相对论 momentum variable
- 用 Higuera-Cary 做一小步 Lorentz source 积分

## 4. `rho` 沉积：每步前后各沉积一次，直接进入普通 `rho_fp`

`Evolve()` 在 source + advection 之前后各沉积一次电荷：

```cpp
DepositCharge(fields, *fields.get(FieldType::rho_fp,lev), lev, 0);
...
DepositCharge(fields, *fields.get(FieldType::rho_fp,lev), lev, 1);
```

`DepositCharge()` 本身很简单：

```cpp
if ( owner_mask_rho_arr(i,j,k) ) { rho_arr(i,j,k,icomp) += q*N_arr(i,j,k); }
```

关键是目标：

- 它沉积到普通 `rho_fp`
- 而不是某个 fluid 专属 `rho`

因此 fluid charge density 和粒子 charge density 在主循环语义里本来就被设计成同一个场求解器右端项的一部分。

## 5. `J` 沉积：先算 nodal 流体电流，再插值回求解器真实 staggering

`DepositCurrent()` 的真实结构分两段。

第一段先在 nodal 网格上构造流体电流：

```cpp
tmp_jx_fluid_arr(i, j, k) = q * (NUx_arr(i, j, k) / gamma);
tmp_jy_fluid_arr(i, j, k) = q * (NUy_arr(i, j, k) / gamma);
tmp_jz_fluid_arr(i, j, k) = q * (NUz_arr(i, j, k) / gamma);
```

也就是

$$
\mathbf J = q N \mathbf V = q \frac{\mathbf{NU}}{\gamma}.
$$

第二段再把 nodal `tmp_j*` 插值到求解器当前真正使用的 `jx/jy/jz` staggering：

```cpp
const amrex::Real jx_tmp = ablastr::coarsen::sample::Interp(tmp_jx_fluid_arr,
    j_nodal_type, jx_type, coarsening_ratio, i, j, k, 0);
if ( owner_mask_x_arr(i,j,k) ) { jx_arr(i, j, k) += jx_tmp; }
```

所以它的合同不是“fluid current 本来就在 Yee 网格上”，而是：

1. 流体内部状态统一存在 nodal 点；
2. 需要沉积时，再对齐到当前 solver / `grid_type` 使用的目标 `J` staggering。

## 6. 这也是它和 `HybridPICModel` 的关键区别

`HybridPICModel` 里描述的电子流体闭合不是这样工作的。field solver 那边走的是：

- 用 `curl B / mu0` 构造总 plasma current；
- 减去外部电流；
- 再减去 kinetic ion current；
- 剩下的是电子流体电流；
- 再用广义 Ohm 定律求 `E`。

也就是说：

- `HybridPICModel` 的“电子流体”不是通过 `WarpXFluidContainer::DepositCurrent()` 沉积来的；
- 它是场求解器内部从 `B` 和离子电流反推出来的闭合量。

而 `Fluids/` 这里的流体 species：

- 有自己的 `N/NU`
- 自己 gather `E/B`
- 自己推进
- 最后像普通物质一样沉积 `rho/J`

因此两者的关系只能说是“都和 fluid 有关”，不能说是同一条算法链。

## 7. moving window：fluid 和连续粒子注入并行，但粒子是 `RealBox`，fluid 是 nodal `Box`

`WarpXMovingWindow.cpp` 里对 fluid 的连续注入路径和粒子不同。

粒子是用 `RealBox particleBox` 做连续注入，而 fluid 用的是 nodal `Box injection_box`：

```cpp
amrex::Box injection_box = geom[lev].Domain();
injection_box.surroundingNodes();
...
fl.InitData( m_fields, injection_box, cur_time, lev, geom[lev], gamma_boost, beta_boost);
```

这说明 moving window 下的 fluid 注入不是宏粒子级“再采样”，而是连续场变量的 nodal 重新填充。

## 8. regression 入口：当前最直接的是 `langmuir_fluids`

当前 worktree 里，`Fluids/` 最直接的 validation 入口不是通用 field solver regression，而是 `langmuir_fluids` 这棵树。已有初始化验证笔记已经明确：

- 它不只看场；
- 会同时检查 `E/J/rho`
- 并与 cold-fluid 解析解对照

因此 `langmuir_fluids` 的定位很重要：

- 它验证的不是 `HybridPICModel`
- 而是 `WarpXFluidContainer` 这条 cold-fluid runtime layer。

## 9. 当前 worktree 下 `Fluids/` 的真实结论

把这条线压成一句话：

`Fluids/` 提供的是额外 cold-fluid species，它们复用粒子侧 initialization/parser 与 Higuera-Cary source-step，内部状态存在 nodal `N/NU` 上，最后再把 `rho/J` 沉积回普通场寄存器；这和 `HybridPICModel` 里用电子 Ohm 定律闭合 `E` 的 solver-internal fluid 不是同一件事。
