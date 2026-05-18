# `Fluids/` 总图：`MultiFluidContainer` 只是薄调度层，真实物理状态在 `WarpXFluidContainer`

绑定源码：

- `../warpx/Source/Fluids/MultiFluidContainer.H`
- `../warpx/Source/Fluids/MultiFluidContainer.cpp`
- `../warpx/Source/Fluids/WarpXFluidContainer.H`
- `../warpx/Source/Fluids/WarpXFluidContainer.cpp`
- `../warpx/Source/WarpX.cpp`
- `../warpx/Source/Evolve/WarpXEvolve.cpp`
- `../warpx/Source/Utils/WarpXMovingWindow.cpp`

这一组源码比 `Particles/`、`FieldSolver/` 窄很多。当前 worktree 里 `Source/Fluids` 真正承担的事情只有三类：

1. 读取 `fluids.species_names`，为每个流体 species 创建一个 `WarpXFluidContainer`；
2. 为每个流体 species 分配 nodal `N` 和 `NU`；
3. 在每个 PIC step 里，把初始化、Lorentz source、advective update、`rho/J` 沉积串成一条薄运行时链。

所以 `Fluids/` 不是一个独立 solver framework，更像是“cold-fluid species runtime layer”。

## 1. 对象边界：`MultiFluidContainer` 只做 species fan-out

`MultiFluidContainer` 的职责在头文件注释里已经写得很直白：

```cpp
/**
 * The class MultiFluidContainer holds multiple instances of the
 * class WarpXFluidContainer, stored in its member variable "allcontainers".
 * ...
 * - Functions that loop over all instances of WarpXFluidContainer in
 *   allcontainers and calls the corresponding function
 * - Functions that specifically handle multiple species
 */
class MultiFluidContainer
```

构造函数只做一件事：读取 `fluids.species_names`，逐个创建 `WarpXFluidContainer`：

```cpp
const ParmParse pp_fluids("fluids");
pp_fluids.queryarr("species_names", species_names);

const int nspecies = static_cast<int>(species_names.size());

allcontainers.resize(nspecies);
for (int i = 0; i < nspecies; ++i) {
    allcontainers[i] = std::make_unique<WarpXFluidContainer>(i, species_names[i]);
}
```

这说明 `Fluids/` 的 existence gate 不在 `MultiFluidContainer` 内部，而在更上层：

- `WarpX::ReadParameters()` 先检查 `fluids.species_names` 是否为空；
- 只有非空时，`do_fluid_species` 才会变成真；
- 后面构造函数才会真的 `myfl = std::make_unique<MultiFluidContainer>()`。

也就是说，`fluids.species_names` 控制的是整条流体子系统是否存在，而不是某个局部开关。

## 2. 启动期约束：流体 species 现在不能和任意全局配置自由组合

`WarpX.cpp` 在决定 `do_fluid_species` 时，立即加了几条硬约束：

```cpp
do_fluid_species = !fluid_species_names.empty();
if (do_fluid_species) {
    WARPX_ALWAYS_ASSERT_WITH_MESSAGE(max_level <= 1,
        "Fluid species cannot currently be used with mesh refinement.");
    WARPX_ALWAYS_ASSERT_WITH_MESSAGE(
        electrostatic_solver_id != ElectrostaticSolverAlgo::Relativistic,
        "Fluid species cannot currently be used with the relativistic electrostatic solver.");
#ifdef WARPX_DIM_RZ
    WARPX_ALWAYS_ASSERT_WITH_MESSAGE( n_rz_azimuthal_modes <= 1,
        "Fluid species cannot be used with more than 1 azimuthal mode.");
#endif
}
```

当前 worktree 的真实边界因此是：

- 不支持 AMR；
- 不支持 relativistic electrostatic solver；
- RZ 下不支持 `n_rz_azimuthal_modes > 1`。

## 3. level data：每个 fluid species 只新增两组 nodal 量

`WarpXFluidContainer::AllocateLevelMFs()` 给每个 species 分配的字段非常克制：

```cpp
fields.alloc_init(
        name_mf_N, lev, amrex::convert(ba, amrex::IntVect::TheNodeVector()), dm,
        ncomps, nguards, 0.0_rt);

fields.alloc_init(
        name_mf_NU, Direction{0}, lev, amrex::convert(ba, amrex::IntVect::TheNodeVector()), dm,
        ncomps, nguards, 0.0_rt);
...
```

其中：

- `fluid_density_<species>` 存 `N`
- `fluid_momentum_density_<species>` 存三分量 `NU`

这里的 `U` 不是无量纲四速度，而是 SI 单位的 bulk momentum-like velocity variable。初始化时源码会显式乘 `c`：

```cpp
u.x = u.x * clight;
u.y = u.y * clight;
u.z = u.z * clight;
...
NUx_arr(i, j, k) = n * u.x;
NUy_arr(i, j, k) = n * u.y;
NUz_arr(i, j, k) = n * u.z;
```

因此这一层的 conserved state 更准确地写成

$$
(N,\;N U_x,\;N U_y,\;N U_z),
$$

而不是粒子那边的 `(x,u,w)` 宏粒子表述。

## 4. 初始化：沿用 species injector 体系，而不是另起一套 fluid parser

`WarpXFluidContainer` 构造函数里最关键的动作，是把粒子侧已有的 species parser 复用过来：

```cpp
SpeciesUtils::parseDensity(species_name, "", h_inj_rho, density_parser, geom);
SpeciesUtils::parseMomentum(species_name, "", "none", h_inj_mom,
    ux_parser, uy_parser, uz_parser, ux_th_parser, uy_th_parser, uz_th_parser, h_mom_temp, h_mom_vel);
```

这意味着：

- fluid species 的密度 profile 仍走 `SpeciesUtils::parseDensity(...)`；
- bulk momentum / thermal spread 的输入语义也复用粒子侧 parser；
- `Fluids/` 并没有定义一套与粒子完全不同的 profile language。

`InitData()` 只是把这些 parser / injector 落到 nodal `N` 和 `NU` 上，并在 boosted frame 下做一次 lab-to-boost transform：

```cpp
if (gamma_boost > 1._rt){
    z = gamma_boost*(z + beta_boost*clight*cur_time);
}
...
const amrex::Real n_boosted = gamma_boost*n*( 1.0_rt - beta_boost*u.z/(gamma*clight) );
const amrex::Real uz_boosted = gamma_boost*(u.z - beta_boost*clight*gamma);
```

## 5. 运行时位置：它插在粒子沉积和场推进之间

`WarpXEvolve.cpp` 中的调用位置很关键：

```cpp
if (do_fluid_species) {
    myfl->Evolve(m_fields,
                 lev,
                 current_fp_string,
                 cur_time,
                 skip_deposition
    );
}
```

它发生在粒子 `rho/J` 沉积和 inverse-volume scaling 之后、同一个主 step 内。这说明 fluid species 不是额外独立时间循环，而是和 PIC 主循环共用同一个 `dt`。

从 `WarpXFluidContainer::Evolve()` 看，每个 fluid step 的顺序固定为：

1. 需要时先沉积旧时间层 `rho` 到 `rho_fp(..., comp=0)`；
2. `GatherAndPush()` 用 `Efield_aux/Bfield_aux` 做 Lorentz source；
3. `centrifugal_source_rz()` 处理 RZ/RCYLINDER/RSPHERE 曲率源；
4. `ApplyBcFluidsAndComms()` 补非周期边界和 guard-cell 通信；
5. `AdvectivePush_Muscl()` 做 cold-fluid advection；
6. 再沉积新时间层 `rho` 到 `rho_fp(..., comp=1)`；
7. `DepositCurrent()` 把流体电流加进当前求解器所用 `current_fp_string`。

## 6. moving window：fluid cells 会和粒子一样被整体平移和连续再注入

`WarpXMovingWindow.cpp` 对 fluid 的处理也很直接。

先整体平移每个 species 的 `N/NU`：

```cpp
WarpXFluidContainer const& fl = myfl->GetFluidContainer(i);
::shiftMF( *m_fields.get(fl.name_mf_N, lev), geom[lev], num_shift, dir, ... );
::shiftMF( *m_fields.get(fl.name_mf_NU, Direction{0}, lev), geom[lev], num_shift, dir, ... );
...
```

再在新露出的 nodal 区域上重新调用 `InitData()`：

```cpp
WarpXFluidContainer& fl = myfl->GetFluidContainer(i);
fl.InitData( m_fields, injection_box, cur_time, lev, geom[lev], gamma_boost, beta_boost);
```

因此 moving window 下的 fluid 语义和连续粒子注入是一致的：

- 旧窗口内容整体平移；
- 新暴露区域不是插值外推，而是重新按初始 profile 生成。

## 7. 当前模块边界

基于当前 worktree，`Fluids/` 最重要的边界是：

1. 它描述的是 cold relativistic fluid species，不是 `HybridPICModel` 那个电子流体闭合本身。
2. 它复用粒子侧 species parser 与 initialization 体系。
3. 它通过普通 `rho/J` 沉积把源项并回 WarpX 主场，而不是直接改写场求解器的内部方程。
4. 它当前源码面很薄，核心真正需要精读的只剩三处：
   - `WarpXFluidContainer::Evolve`
   - `WarpXFluidContainer::AdvectivePush_Muscl`
   - `GatherAndPush` / `DepositCurrent` / `DepositCharge`

下一篇分别拆 `MUSCL-Hancock` advection 和 `fluid <-> PIC/hybrid` 耦合。
