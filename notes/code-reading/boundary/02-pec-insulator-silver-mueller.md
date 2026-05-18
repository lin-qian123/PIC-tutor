# Boundary 02: PEC / PMC / PECInsulator 与 Silver-Mueller

绑定源码：

- `../warpx/Source/BoundaryConditions/WarpX_PEC.cpp`
- `../warpx/Source/BoundaryConditions/PEC_Insulator.cpp`
- `../warpx/Source/BoundaryConditions/WarpXFieldBoundaries.cpp`
- `../warpx/Source/Particles/WarpXParticleContainer.cpp`
- `../warpx/Docs/source/theory/boundary_conditions.rst`
- `../warpx/Docs/source/usage/parameters.rst`

## 1. 这一层最容易被误解的地方

WarpX 里的 PEC、PMC、PECInsulator、Silver-Mueller 不是同一类边界：

- PEC / PMC：带有明确场奇偶对称和 rho/J 镜像规则的“反射型”边界
- PECInsulator：空间上混合 PEC 与 insulator 的边界，边界值可由 parser 表达式指定
- Silver-Mueller：只作用于 FDTD/Yee 时间推进中的吸收型场边界

如果只从输入参数表看，很容易把它们都理解成“改改 E/B 的边界值”。源码显示这不够，至少还要区分：

1. 场边界上的零值或指定值；
2. guard cell 的镜像延拓规则；
3. rho / J 沉积后的镜像回填；
4. 粒子穿越边界时是否裁剪轨迹。

## 2. PEC 对 E、B 的奇偶规则

`SetEfieldOnPEC()` 的规则是：

- 边界上的切向 `E` 置零；
- guard 区中的切向 `E` 取 mirror 值再乘 `-1`；
- 法向 `E` 在 guard 区直接镜像，不翻号。

核心逻辑：

```cpp
if (ig == 0) {
    if (is_tangent_to_PEC && is_nodal[idim] == 1) {
        OnPECBoundary = true;
    }
} else if (ig > 0) {
    ...
    if (is_tangent_to_PEC) { sign *= -1._rt; }
}
...
if (OnPECBoundary) {
    Efield(ijk_vec,n) = 0._rt;
} else if (GuardCell) {
    Efield(ijk_vec,n) = sign * Efield(ijk_mirror,n);
}
```

源码位置：`../warpx/Source/BoundaryConditions/WarpX_PEC.cpp:171-195`。

`SetBfieldOnPEC()` 则正好相反：

- 边界上的法向 `B` 置零；
- guard 区中的法向 `B` 镜像后翻号；
- 切向 `B` 在 guard 区镜像，不翻号。

核心逻辑：

```cpp
if (ig == 0) {
    if (is_normal_to_PEC && is_nodal[idim]==1) {
        OnPECBoundary = true;
    }
} else if ( ig > 0) {
    ...
    if (is_normal_to_PEC) { sign *= -1._rt; }
}
...
if (OnPECBoundary) {
    Bfield(ijk_vec,n) = 0._rt;
} else if (GuardCell) {
    Bfield(ijk_vec,n) = sign * Bfield(ijk_mirror,n);
}
```

源码位置：`../warpx/Source/BoundaryConditions/WarpX_PEC.cpp:315-340`。

这和理论文档一致：PEC 边界上切向 `E` 与法向 `B` 为零。见 `../warpx/Docs/source/theory/boundary_conditions.rst:275-282`。

## 3. PMC 在源码里并没有单独实现一套 kernel

`WarpXFieldBoundaries.cpp` 对 PMC 的处理方式很直接：

- `ApplyEfieldBoundary()` 里，PMC 调的是 `PEC::ApplyPECtoBfield(...)`
- `ApplyBfieldBoundary()` 里，PMC 调的是 `PEC::ApplyPECtoEfield(...)`

源码位置：`../warpx/Source/BoundaryConditions/WarpXFieldBoundaries.cpp:91-123` 和 `196-209`。

这意味着 PMC 不是独立再写一套场镜像逻辑，而是通过“交换 E/B 在 PEC 语义中的角色”来实现：

- PMC 边界上为零的是切向 `B` 与法向 `E`
- 其 guard-cell 奇偶规则也由同一套 PEC helper 复用

因此，理解 PMC 最直接的方式不是去找另一套公式，而是把 PEC 的 E/B 角色互换。

## 4. rho 与 J 的镜像不是附带效果，而是边界定义的一部分

`WarpX_PEC.cpp` 最重要的部分不是 E/B 置零，而是 `ReflectJorRho()` 与 `SetJorRho()` 两个 helper。

`ReflectJorRho()` 先把 guard cell 中已经沉积进去的 rho 或 J 反射回域内 mirror 位置：

```cpp
field(ijk_vec,n) += rscale * psign[iside] * field(ijk_mirror,n);
```

源码位置：`../warpx/Source/BoundaryConditions/WarpX_PEC.cpp:427-430`。

`SetJorRho()` 再把 guard 区本身设成与边界对称性一致的值：

```cpp
field(ijk_mirror,n) = inv_rscale * psign[iside] * field(ijk_vec,n);
```

源码位置：`../warpx/Source/BoundaryConditions/WarpX_PEC.cpp:484-501`。

源码注释已经把物理含义写得很清楚：

- PMC：对 rho / `J_parallel` 是对称反射，对 `J_perp` 是反对称反射
- PEC：对 rho / `J_parallel` 是反对称反射，对 `J_perp` 是对称反射

见 `../warpx/Source/BoundaryConditions/WarpX_PEC.cpp:344-357` 与 `435-452`。

这正对应 image charge / image current 的符号选择，所以 PEC/PMC 在 WarpX 里本质上是“场 + 沉积 + 粒子”的联合边界，不是单独的 Maxwell 边界。

## 5. rho 与 J 的反射入口

`WarpXFieldBoundaries.cpp` 中，rho 与 J 的反射并不是总是执行，而是只有满足“存在反射型粒子边界或 PEC/PMC/PECInsulator”时才进入：

```cpp
if (::isAnyBoundary<FieldBoundaryType::PECInsulator>(field_boundary_lo, field_boundary_hi) ||
    ... ) {
    PEC::ApplyReflectiveBoundarytoRhofield(...);
}
```

以及：

```cpp
if (::isAnyBoundary<FieldBoundaryType::PECInsulator>(field_boundary_lo, field_boundary_hi) ||
    ... ) {
    PEC::ApplyReflectiveBoundarytoJfield(...);
}
```

源码位置：`../warpx/Source/BoundaryConditions/WarpXFieldBoundaries.cpp:263-296`。

这一步说明 rho / J 边界不是由沉积 kernel 自动完成，而是在沉积之后、边界后处理阶段显式执行。

## 6. PECInsulator 不是“部分 PEC + 部分 open”，而是“部分 PEC + 部分带表达式的边界值”

`PEC_Insulator.cpp` 的核心 helper 是 `SetFieldOnPEC_Insulator()`。它先判断当前位置属于：

- 真 PEC 区
- insulator 区
- 边界点还是 guard 点
- 法向分量还是切向分量

然后分别施加不同规则。

对 `E_like` 场：

- 法向分量：guard 区镜像
- 切向分量在 PEC 上置零
- 切向分量在 insulator 上可由 parser 给定边界值
- guard 区 insulator 切向分量按 `2*boundary - mirror` 外推

关键逻辑：

```cpp
if (on_nodal_boundary) {
    if (is_insulator_boundary) {
        if (set_field) {
            field(ijk_vec, n) = field_value;
        }
    } else {
        field(ijk_vec, n) = 0._rt;
    }
} else if (guard_cell) {
    if (is_insulator_boundary) {
        amrex::Real const field_boundary = (set_field ? field_value : field(ijk_boundary, n));
        field(ijk_vec, n) = 2._rt*field_boundary - field(ijk_mirror, n);
    } else {
        field(ijk_vec, n) = -field(ijk_mirror, n);
    }
}
```

源码位置：`../warpx/Source/BoundaryConditions/PEC_Insulator.cpp:194-212`。

对 `B_like` 场：

- 法向 `B` 在 PEC 上置零，在 insulator 上允许沿边界外推
- 切向 `B` 若在 insulator 且显式给定，则边界 cell 直接设为 parser 值

源码位置：`../warpx/Source/BoundaryConditions/PEC_Insulator.cpp:215-249`。

因此 PECInsulator 的重点不是“这个边界到底是 PEC 还是绝缘体”，而是“边界上的哪一段由 area parser 判定为 insulator，以及该段切向场是否显式给定”。

## 7. PECInsulator 的空间区域和边界值都来自 parser

`PEC_Insulator` 初始化时先读取 area parser，再读取切向场 parser，随后统一整理到 `m_set_*` 标志和 parser executor 中：

```cpp
for(const auto & area_parser : m_insulator_area_lo) {
    m_area_parsers_lo.push_back(area_parser->compile<2>());
}
...
::SetupFieldParsers(...)
```

源码位置：`../warpx/Source/BoundaryConditions/PEC_Insulator.cpp:437-456`。

真正应用时，对每个边界点先把索引转成坐标：

```cpp
amrex::XDim3 const coords = ::ConvertIndexToCoordinate(iv, xyzmin, dx, lo, Fx_nodal);
::XDimTransverse const tcoords = ::GetTransverseCoordinates(idim, coords);
bool const is_insulator = (area_parser(tcoords.t1, tcoords.t2) > 0._rt);
amrex::Real const field_value = (set_Fx ? Fx_parser(tcoords.t1, tcoords.t2, time) : 0._rt);
```

源码位置：`../warpx/Source/BoundaryConditions/PEC_Insulator.cpp:714-722`。

这与参数文档完全一致：`insulator.area_*` 决定哪一块是绝缘体，`insulator.Ex_*` / `Ey_*` / `B*_*` 这些 parser 决定切向边界值。见 `../warpx/Docs/source/usage/parameters.rst:788-818`。

## 8. `crop_on_PEC_boundary` 不改场，它改粒子轨迹

文档提到 `particles.crop_on_PEC_boundary`，容易误以为它只是可视化或诊断开关。源码显示它真正影响粒子轨迹处理。

参数读取位置：

```cpp
pp_particles.query("crop_on_PEC_boundary", m_crop_on_PEC_boundary);
```

源码位置：`../warpx/Source/Particles/WarpXParticleContainer.cpp:157`。

之后在粒子跨边界处理时，只有当该开关打开且 field boundary 为 PEC 或 PECInsulator 时，才启用裁剪：

```cpp
do_cropping[idim][0] = m_crop_on_PEC_boundary &&
    (... field_boundary_lo[idim] == FieldBoundaryType::PEC
     || field_boundary_lo[idim] == FieldBoundaryType::PECInsulator));
```

源码位置：`../warpx/Source/Particles/WarpXParticleContainer.cpp:533-540`。

所以 `crop_on_PEC_boundary` 是粒子几何处理选项，不是场边界算法的一部分，但它决定粒子是否会在 PEC/PECInsulator 处留下“跨过边界再被纠正”的轨迹。

## 9. Silver-Mueller 的实现边界

这一轮没有继续深入 `ApplySilverMuellerBoundary()` 内部 stencil，但从调用位置已经可以确定三条边界：

1. 只在 `ApplyBfieldBoundary()` 里触发；
2. 只在 `lev == 0`；
3. 只在 `subcycling_half == FirstHalf`。

对应代码：

```cpp
if (lev == 0) {
    if (subcycling_half == SubcyclingHalf::FirstHalf) {
        if(::isAnyBoundary<FieldBoundaryType::Absorbing_SilverMueller>(...)){
            m_fdtd_solver_fp[0]->ApplySilverMuellerBoundary(...);
        }
    }
}
```

源码位置：`../warpx/Source/BoundaryConditions/WarpXFieldBoundaries.cpp:231-239`。

这和参数文档中的说明一致：Silver-Mueller 只适用于 Yee Maxwell solver。见 `../warpx/Docs/source/usage/parameters.rst:779-781`。

## 10. 当前阶段的稳定结论

1. PEC / PMC 的核心不是“边界上哪一项为零”，而是 E/B 奇偶延拓与 rho/J 镜像的整体配套。
2. PMC 在实现上主要通过复用 PEC helper 并交换 E/B 角色得到。
3. `ApplyReflectiveBoundarytoRhofield()` 和 `ApplyReflectiveBoundarytoJfield()` 是 PEC/PMC 物理语义落到沉积场上的关键入口。
4. PECInsulator 允许边界在横向位置上切换 PEC 与 insulator，并对 insulator 区的切向边界值使用 parser 表达式。
5. `crop_on_PEC_boundary` 作用于粒子轨迹裁剪，不属于场边界更新本身。
6. Silver-Mueller 当前至少已知是 FDTD/Yee half-push 专用边界，不是通用开放边界。

当前本地 regression 里，PMC 还有一条很直接的场级验证入口：`Examples/Tests/pec/inputs_test_3d_pmc_field`。它在 `z` 方向设 `pmc`，在局部区域初始化正弦 `Ey/Bx` 波包，再由 `analysis_pec.py` 检查 standing-wave 的 `Ey_max`/`Ey_min` 是否接近理论的 `±2E_in`，相对误差低于 `1%`。因此这条测试验证的不是抽象“PMC 被支持”，而是 PMC 通过交换 PEC 的 E/B 角色后，反射相位与构成的 standing-wave 振幅仍满足理论合同。

Silver-Mueller 的 regression 口径则正好相反。`Examples/Tests/silver_mueller/analysis.py` 不去看 standing wave，也不去对照解析反射系数，而是直接检查脉冲离域后整个诊断网格上的场残余必须很小：

```python
max_reflection_amplitude = 0.01
assert np.all(abs(Ex) < max_reflection_amplitude)
assert np.all(abs(Ey) < max_reflection_amplitude)
assert np.all(abs(Ez) < max_reflection_amplitude)
```

RZ 版本则把同一判据作用到 `Er/Et/Ez`。由于这些输入里的入射激光峰值量级约为 `10 V/m`，这组测试真正验证的是

$$
|E_{\mathrm{reflected}}| \ll |E_{\mathrm{incident}}|,
$$

也就是 Silver-Mueller 作为开放边界时，离域后的残余反射场必须足够小，而不是像 PMC 那样有意构造反射并检查 standing-wave 振幅。

当前本地 family 一共四条：

- `inputs_test_1d_silver_mueller`
- `inputs_test_2d_silver_mueller_x`
- `inputs_test_2d_silver_mueller_z`
- `inputs_test_rz_silver_mueller_z`

PEC 这一组也有同样的 helper 边界。`Examples/Tests/pec/analysis_default_regression.py` 只是目录内 checksum helper 副本，代码与顶层 `Examples/analysis_default_regression.py` 同构。当前它的职责是：

- 给 `test_3d_pec_field`
- `test_3d_pec_field_mr`
- `test_2d_pec_field_insulator`
- `test_2d_pec_field_insulator_implicit`
- `test_2d_pec_field_insulator_implicit_restart`
- `test_3d_pec_particle`

这些条目提供历史输出基线，而不替代：

- `analysis_pec.py` 的 standing-wave 振幅断言
- `analysis_pec_mr.py` 的 MR standing-wave 容差断言
- `analysis_pec_insulator_implicit.py` 的能量账本断言

所以 `pec` family 的口径必须分成：

1. 有独立 analysis 的强边界条件回归；
2. 只靠 checksum 兜底的输出基线与粒子侧工作流条目。

其中 2D `x` 向版本把 Silver-Mueller 只放在 `x` 边界、另一方向保持 periodic，专门覆盖横向出射；2D `z` 向和 RZ `z` 向版本则覆盖轴向出射，并把 RZ 轴线 `r_lo = none` 的正则性约束同开放边界放到同一个最小基准里。

同一目录里的 `pec` family 还给了 PEC/PECInsulator 两组互补回归：

- `test_3d_pec_field`
- `test_3d_pec_field_mr`
- `test_2d_pec_field_insulator_implicit`
- `test_2d_pec_field_insulator_implicit_restart`

其中前两条复用 `analysis_pec.py` / `analysis_pec_mr.py`，直接检查 PEC standing wave 的 `Ey_max/Ey_min` 是否接近理论 `±2E_in`；单级版本容差 `1%`，MR 版本放宽到 `5%`。这说明 PEC 场边界的强回归对象不是抽象“切向 E 为零”，而是反射后构成的 standing-wave 振幅是否和理论一致。

后两条则走 `analysis_pec_insulator_implicit.py`，不再看 standing wave，而是把 `fieldenergy.txt` 与 `poyntingflux.txt` 合成能量账本，要求

$$
\frac{|E_{\mathrm{field}} + E_{\mathrm{loss}}|}{E_{\max}} < 10^{-13}.
$$

因此 `pec_insulator` 的 implicit regression 真正验证的是：

- `insulator.area_x_hi(...)`
- `insulator.By_x_hi(...,t)`
- implicit Yee 场推进
- 以及边界 Poynting flux reduced diagnostics

这四层一起组成的精确能量记账合同。`..._restart` 变体则进一步表明，从 checkpoint 恢复后同一合同仍成立，但当前并没有额外做逐字段 restart 对照。

## 11. 下一步

- 若继续推进边界模块，下一优先项应是把 `ApplySilverMuellerBoundary()` 内部公式与理论文档对齐。
- 然后转到 `Parallelization/` 与 `AMR`，补 coarse-fine、guard-cell、subcycling 的边界耦合。
