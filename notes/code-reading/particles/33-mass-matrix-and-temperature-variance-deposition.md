# 33 mass matrix and temperature variance deposition：线性响应矩阵与统计矩沉积不是 `rho/J` 的附属项

绑定源码：

- `../warpx/Source/Particles/WarpXParticleContainer.cpp`
- `../warpx/Source/Particles/PhysicalParticleContainer.cpp`
- `../warpx/Source/Particles/MultiParticleContainer.cpp`
- `../warpx/Source/Particles/Deposition/MassMatricesDeposition.H`
- `../warpx/Source/Particles/Deposition/TemperatureDeposition.H`
- `../warpx/Source/Particles/Deposition/VarianceAccumulationBuffer.cpp`

前置阅读：

- `../notes/code-reading/particles/10-implicit-suborbit-mass-matrices-jfnk.md`
- `../notes/code-reading/particles/32-current-deposition-continuity-and-geometry-boundaries.md`

上一轮已经把常规 `rho/J` 沉积压成了：

- 离散连续性合同；
- `Direct / Esirkepov / Villasenor / Vay` 的算法分叉；
- `implicit / RZ / 1D_Z / RCYLINDER / RSPHERE` 的时间层和几何边界。

这里继续收另一层：WarpX 里“粒子回网格”不只包括 `rho/J`。至少还有两条沉积支线：

1. implicit/JFNK 用的 **mass matrices**，它们沉的是线性化电流响应；
2. per-species diagnostics 用的 **temperature / variance deposition**，它们沉的是统计矩而不是 Maxwell 源项。

## 1. mass matrices 不是另一个 `current_fp`，而是 implicit 线性化的粒子响应块

`MultiParticleContainer::DepositMassMatrices()` 一开始就把

- `MassMatrices_X`
- `MassMatrices_Y`
- `MassMatrices_Z`

三组方向块清零，然后逐 species 调 `pc->DepositMassMatrices(fields, lev, dt)`：

```cpp
for (int n = 0; n < 3; ++n) {
    fields.get(FieldType::MassMatrices_X, Direction{n}, lev)->setVal(0.0);
    fields.get(FieldType::MassMatrices_Y, Direction{n}, lev)->setVal(0.0);
    fields.get(FieldType::MassMatrices_Z, Direction{n}, lev)->setVal(0.0);
}

for (auto& pc : allcontainers) {
    pc->DepositMassMatrices(fields, lev, dt);
}
```

源码位置：`../warpx/Source/Particles/MultiParticleContainer.cpp:617-629`。

这说明它的对象级语义一开始就和常规 `current_fp` 不同：

- `current_fp` 是这一时间步的真正 Maxwell 源项；
- `MassMatrices_*` 是 implicit/JFNK 线性阶段要消费的粒子响应矩阵。

## 2. `PhysicalParticleContainer::DepositMassMatrices()` 仍然复用粒子-to-grid 几何，但消费的是 `Bfield_aux`

species 级入口位于 `../warpx/Source/Particles/PhysicalParticleContainer.cpp:828-883`。

这条路径：

- 先取 `Bfield_aux`
- 再取九个矩阵块：
  - `Sxx/Sxy/Sxz`
  - `Syx/Syy/Syz`
  - `Szx/Szy/Szz`
- 然后调 `WarpXParticleContainer::DepositMassMatrices(...)`

```cpp
const amrex::MultiFab & Bx = *fields.get(FieldType::Bfield_aux, Direction{0}, lev);
...
amrex::MultiFab * Sxx = fields.get(FieldType::MassMatrices_X, Direction{0}, lev);
...
WarpXParticleContainer::DepositMassMatrices(pti, wp, uxp, uyp, uzp,
                  Sxx, Sxy, Sxz, Syx, Syy, Syz, Szx, Szy, Szz,
                  bxfab, byfab, bzfab, 0, np_to_deposit, thread_num, lev, lev, dt);
```

因此它不是把普通 `J` 再存一份，而是在同样的粒子-网格支撑域上，沉积 “给定 `B` 与速度后，`J(E)` 对 `E` 的局部线性响应”。

## 3. mass matrices 的第一层限制写死在 `WarpXParticleContainer.cpp`

`WarpXParticleContainer::DepositMassMatrices()` 的入口一开始就明确拒绝：

- `Esirkepov`
- `Vay`
- collocated grid

```cpp
if (WarpX::current_deposition_algo == CurrentDepositionAlgo::Esirkepov ||
    WarpX::current_deposition_algo == CurrentDepositionAlgo::Vay) {
    WARPX_ABORT_WITH_MESSAGE("mass matrices cannot be used with Esirkepov or Vay depositions.");
}
if (WarpX::grid_type == GridType::Collocated) {
    WARPX_ABORT_WITH_MESSAGE("mass matrices cannot be used with a collocated grid.");
}
```

源码位置：`../warpx/Source/Particles/WarpXParticleContainer.cpp:1131-1136`。

后面真正允许的只剩两条：

- `Villasenor`
- `Direct`

分别走：

- `doVillasenorSigmaDeposition<...>()`
- `doDirectSigmaDeposition<...>()`

源码位置：`../warpx/Source/Particles/WarpXParticleContainer.cpp:1161-1365`。

这再次说明：mass matrices 不是“所有 current deposition 再顺手导个矩阵”。它只和一部分沉积算法兼容。

## 4. mass matrices 沉积和普通 `J` 沉积共享 guard-cell / tilebox / shape 安全条件

`WarpXParticleContainer::DepositMassMatrices()` 和普通 `DepositCurrent()` 一样：

- 检查 `depos_lev == lev` 或 `lev-1`
- 用 `shape_extent` 检查粒子支撑域是否放得进当前 tile 或 guard cells
- 用 `tilebox`/`coarsen(tilebox)` 区分本 level 与 coarse buffer

这说明它虽然语义上不是 Maxwell 源项，但在几何上仍是一条标准 particle-to-grid deposition 路。

## 5. `MassMatricesDeposition.H` 还暴露了实现成熟度边界

`MassMatricesDeposition.H` 内部直接保留了一个很硬的注释：

```cpp
// Should not be here. Full mass matrices not yet implemented in 3D
```

源码位置：`../warpx/Source/Particles/Deposition/MassMatricesDeposition.H:448`。

因此这条线当前更准确的理解是：

- WarpX 已经有可工作的 mass-matrix deposition 主链；
- 但它并不是“一套在所有维度和所有耦合块上都完全成熟的全矩阵实现”。

## 6. 温度沉积不是 `current_fp` 的后处理，而是 species 自己分配的一套统计矩场

`PhysicalParticleContainer::AllocData()` 在 species 打开 `do_temperature_deposition` 时，会按 `current_fp` 的 box/stagger/guard 规格额外分配：

- `T_<species>` 三个方向场

随后再创建 `VarianceAccumulationBuffer`：

```cpp
if (m_do_temperature_deposition) {
    ...
    ablastr::fields::MultiLevelVectorField J_vf =
        warpx.m_fields.get_mr_levels_alldirs(warpx::fields::FieldType::current_fp, warpx.finestLevel());
    ...
    warpx.m_fields.alloc_init(T_field_name, Direction{idir},
        lev, ba, dm, WarpX::ncomps, ng, 0.0_rt);
    ...
    local_temperature_arrays = std::make_unique<warpx::particles::deposition::VarianceAccumulationBuffer>(
        T_vf, species_name);
}
```

源码位置：`../warpx/Source/Particles/PhysicalParticleContainer.cpp:363-387`。

这里最关键的边界是：

- `T_<species>` 的网格布局是按 `current_fp` 的方向和 guard-cell 规则来分配的；
- 但它的物理语义不是 current，而是 per-species velocity variance / temperature。

## 7. 多物种入口是 `DepositTemperatures()`，不是主 `Evolve()` 里的 `rho/J` 分派

`MultiParticleContainer::DepositTemperatures()` 对每个打开 `do_temperature_deposition` 的 species：

1. 找出 `T_<species>` 三个方向场；
2. 清零；
3. 调 `pc->AccumulateVelocitiesAndComputeTemperature(T_vf, relative_time)`。

源码位置：`../warpx/Source/Particles/MultiParticleContainer.cpp:645-670`。

因此 temperature deposition 是一条单独的 “per-species statistical deposition” 主线，不是 `DepositCurrent()` 里的附属分支。

## 8. `DepositTemperature()` 的工作前提比普通 `J` 沉积更窄

`PhysicalParticleContainer::DepositTemperature()` 一开始就要求：

- 当前 species 确实打开 `m_do_temperature_deposition`
- `current_deposition_algo == Direct`
- `push_type == Explicit`
- `!WarpX::do_shared_mem_current_deposition`

否则直接 abort：

```cpp
if (WarpX::current_deposition_algo != CurrentDepositionAlgo::Direct
    || push_type != PushType::Explicit
    || WarpX::do_shared_mem_current_deposition
    )
{
    WARPX_ABORT_WITH_MESSAGE(
        "Temperature Deposition only works with explicit solvers, direct current deposition, "
        "and non-shared memory deposition."
    );
}
```

源码位置：`../warpx/Source/Particles/PhysicalParticleContainer.cpp:1844-1858`。

这说明温度沉积不是“所有 deposition 算法都能顺带算的 diagnostics”，而是当前只和 explicit + direct 这条主链配套。

## 9. temperature deposition 的内部对象是 `n / w / w2 / vbar` 四类统计量

`DepositTemperature()` 不直接把温度写出来。它先抓出一整组中间统计数组：

- `n`
- `w`
- `w2`
- `vbar`

分别按 `x/y/z` 三个方向存：

```cpp
auto & nx_iab =    local_temperature_arrays->get_n(Direction{0}, lev)->get(pti);
...
auto & wx_fab =    local_temperature_arrays->get("w", Direction{0}, lev)->get(pti);
...
auto & w2x_fab =   local_temperature_arrays->get("w2", Direction{0}, lev)->get(pti);
...
auto & vxbar_fab = local_temperature_arrays->get("vbar", Direction{0}, lev)->get(pti);
```

源码位置：`../warpx/Source/Particles/PhysicalParticleContainer.cpp:1901-1912`。

这条线的第一性目标不是 “沉一个 `T`”，而是先沉：

- sample count
- 权重和
- 去均值前或去均值后的二次矩
- 平均速度所需的 `wv`

## 10. 当前实际走的是双遍统计法，不是单遍在线算法

`AccumulateVelocitiesAndComputeTemperature()` 里把沉积类型硬编码成：

```cpp
auto depos_type = TemperatureDepositionType::DOUBLE_PASS;
```

源码位置：`../warpx/Source/Particles/PhysicalParticleContainer.cpp:1992`。

后面的实际流程是：

1. **第一遍**
   - 沉 `n`
   - 沉 `w`
   - 沉 `wv`
2. 对这些累积量做 boundary sum
3. 清零 `w2`
4. **第二遍**
   - 用第一遍得到的 cell-mean velocity 再沉 demeaned `w(v-\bar v)^2`
5. 对 `w2` 做 boundary sum
6. 再在 cell 内归一化出 unbiased variance

这条双遍合同和 `TemperatureDeposition.H` 里的 `SINGLE_PASS / DOUBLE_PASS` 枚举是对齐的：

- `TemperatureDepositionType`
- `TemperatureDepositionPass`

源码位置：

- `../warpx/Source/Particles/Deposition/TemperatureDepositionTypes.H:13-20`
- `../warpx/Source/Particles/PhysicalParticleContainer.cpp:1992-2081`

## 11. `TemperatureDeposition.H` 的 kernel 不是沉 `J`，而是沉 weighted moments

`varianceDepositionSubKernel()` 的内部结构非常清楚：

- 第一遍或 single-pass：
  - `n += 1`
  - `w += w_p`
  - `wv += w_p v`
- 第二遍或 single-pass：
  - `w2 += w_p (v-\bar v)^2`

源码位置：`../warpx/Source/Particles/Deposition/TemperatureDeposition.H:25-115`。

其中双遍时的 `\bar v` 不是预先给定，而是先从第一遍的累积量现场归一：

```cpp
vxb = vxbar_arr(...)/wx_arr(...);
```

然后再用

```cpp
const amrex::Real vxd = vxr - vxb;
...
w2x_arr += wpx_var*vxd*vxd;
```

因此 temperature deposition 本质上是：

- particle-to-grid weighted-moment deposition
- 不是 Maxwell 源项 deposition

## 12. `T_x/T_y/T_z` 最后来自 unbiased variance，再乘 `m/k_B`

第二遍结束后，`AccumulateVelocitiesAndComputeTemperature()` 在 cell 内做：

```cpp
const amrex::Real norm = n/((n-1._rt)*sumw);
varx_arr(i,j,k) = norm*w2x_arr(i,j,k);
```

single-pass 时还额外减去 `sumwv^2/sumw` 项。

源码位置：`../warpx/Source/Particles/PhysicalParticleContainer.cpp:2132-2177`。

最后再乘

```cpp
const amrex::Real Tnorm = this->getMass()/ablastr::constant::SI::kb;
```

并通过 `ConvertVarianceToTemperatureAndFilter()`：

1. 把内部 variance 乘成 Kelvin；
2. `FillBoundary`；
3. 可选 `ApplyFilterMF(...)`；
4. 过滤后再同步 ghost cells。

源码位置：

- `../warpx/Source/Particles/PhysicalParticleContainer.cpp:2183-2188`
- `../warpx/Source/Particles/Deposition/VarianceAccumulationBuffer.cpp:79-118`

## 13. 几何边界：RZ 只支持 mode 0

`doVarianceDepositionShapeN()` 里直接要求：

```cpp
WARPX_ALWAYS_ASSERT_WITH_MESSAGE(
    n_rz_azimuthal_modes == 1,
    "Azimuthal Fourier decomposition for temperature deposition is not implemented."
    " Only mode=0 supported in RZ."
);
```

源码位置：`../warpx/Source/Particles/Deposition/TemperatureDeposition.H:454-460`。

这条边界和普通 `rho/J` 沉积不同，说明统计矩沉积当前的几何覆盖还更窄。

## 14. 这条线回到第 5 章后，沉积就不该再只写成 “rho/J 交回网格”

把这些源码放在一起，第 5 章里更稳定的结构应当是：

1. `rho/J` deposition
   - 服务 Maxwell 源项与离散连续性
2. mass-matrix deposition
   - 服务 implicit/JFNK 的线性化电流响应
3. temperature/variance deposition
   - 服务 per-species statistical diagnostics

三者都共享 particle-to-grid 的 shape、tilebox、guard-cell 和 boundary-sum 工程骨架，但物理语义完全不同。

## 15. 当前前沿

最自然的下一步有两条：

1. 把这条 “`rho/J`、mass matrices、temperature/variance” 的三分法回填到 `manuscript/chapters/05-deposition-shapes.md`。
2. 然后继续收 `SyncCurrentAndRho()` 与 guard/current/rho 同步路径，把源项从沉积走到场求解的最后一层闭环补齐。
