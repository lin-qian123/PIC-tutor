# Hybrid PIC 模型深拆：Ohm 定律、时间层与外部场

绑定源码与文档：

- `../warpx/Source/FieldSolver/WarpXPushFieldsHybridPIC.cpp`
- `../warpx/Source/FieldSolver/FiniteDifferenceSolver/HybridPICModel/HybridPICModel.H`
- `../warpx/Source/FieldSolver/FiniteDifferenceSolver/HybridPICModel/HybridPICModel.cpp`
- `../warpx/Source/FieldSolver/FiniteDifferenceSolver/HybridPICModel/ExternalVectorPotential.H`
- `../warpx/Source/FieldSolver/FiniteDifferenceSolver/HybridPICModel/ExternalVectorPotential.cpp`
- `../warpx/Source/FieldSolver/FiniteDifferenceSolver/HybridPICSolveE.cpp`
- `../warpx/Docs/source/theory/models_algorithms/kinetic_fluid_hybrid_model.rst`
- `../warpx/Docs/source/usage/parameters.rst:3578-3716`

`10-implicit-and-hybrid.md` 已经把 hybrid PIC 放进隐式/混合求解器总览里。这一篇单独拆 `HybridPICModel`，重点讲清楚它和普通电磁 PIC 的根本差别：WarpX 不再用 Maxwell-Ampere 方程推进 `E`，而是用电子流体的广义 Ohm 定律求 `E`，再用 Faraday 定律推进 `B`。

## 1. 物理模型：动能离子 + 流体电子

官方理论文档给出的 hybrid PIC 基本方程是：

$$
\frac{\partial\mathbf B}{\partial t}=-\nabla\times\mathbf E,
$$

以及

$$
\mathbf E
=-\frac{1}{e n_e}\left(\mathbf J_e\times\mathbf B+\nabla P_e\right)
+\eta\mathbf J-\eta_h\nabla^2\mathbf J.
$$

电子电流由总电流减去 kinetic species 电流和外部电流：

$$
\mathbf J_e=\mathbf J-\sum_{s\ne e}\mathbf J_s-\mathbf J_{\rm ext},
$$

总电流来自忽略位移电流的 Ampere 定律：

$$
\mu_0\mathbf J=\nabla\times\mathbf B.
$$

这几个式子对应到源码时要注意符号。`HybridPICSolveE.cpp` 里先计算的是

$$
e n_e \mathbf E \leftarrow (\mathbf J-\mathbf J_i)\times\mathbf B,
$$

而文档里有

$$
-\mathbf J_e\times\mathbf B=-(\mathbf J-\mathbf J_i-\mathbf J_{\rm ext})\times\mathbf B.
$$

源码中的 `Jfield` 已经是 `CalculatePlasmaCurrent()` 得到的 plasma current，即 `curl B / mu0` 减去外部电流；`Jifield` 是离子/流体物种沉积电流。因此 `(J - Ji) x B` 正是 Ohm 定律中需要的电子项符号。

## 2. 参数对象：`HybridPICModel`

`HybridPICModel` 保存的不是一个 field solver，而是一组模型参数、临时场类型和帮助函数。头文件说明了它的定位：

```cpp
/**
 * \brief This class contains the parameters needed to evaluate hybrid field
 * solutions (kinetic ions with fluid electrons).
 */
class HybridPICModel
{
public:
    HybridPICModel ();

    /** Read user-defined model parameters. Called in constructor. */
    void ReadParameters ();
```

关键参数包括：

```cpp
/** Number of substeps to take when evolving B */
int m_substeps = 10;

bool m_holmstrom_vacuum_region = false;

/** Electron temperature in eV */
amrex::Real m_elec_temp;
/** Reference electron density */
amrex::Real m_n0_ref = 1.0;
/** Electron pressure scaling exponent */
amrex::Real m_gamma = 5.0/3.0;

/** Plasma density floor - if n < n_floor it will be set to n_floor */
amrex::Real m_n_floor = 1.0;
```

电阻和超电阻是 parser 表达式：

```cpp
/** Plasma resistivity */
std::string m_eta_expression = "0.0";
std::unique_ptr<amrex::Parser> m_resistivity_parser;
amrex::ParserExecutor<2> m_eta;
bool m_resistivity_has_J_dependence = false;

/** Plasma hyper-resisitivity */
std::string m_eta_h_expression = "0.0";
std::unique_ptr<amrex::Parser> m_hyper_resistivity_parser;
amrex::ParserExecutor<2> m_eta_h;
bool m_include_hyper_resistivity_term = false;
bool m_hyper_resistivity_has_B_dependence = false;
```

这意味着输入参数可以是常数，也可以是 `rho,J` 或 `rho,B` 的函数。源码通过 parser 的 symbol set 判断是否需要额外插值 `|J|` 或 `|B|`。

## 3. 参数读取：必要参数与稳定性约束

构造函数只做一件事：

```cpp
HybridPICModel::HybridPICModel ()
{
    ReadParameters();
}
```

`ReadParameters()` 先读子步数，并强制它为偶数：

```cpp
utils::parser::queryWithParser(pp_hybrid, "substeps", m_substeps);
if (m_substeps % 2 != 0) {
    ablastr::warn_manager::WMRecordWarning(
        "HybridPIC",
        "hybrid_pic_model.substeps must be divisible by 2. "
        "The value " + std::to_string(m_substeps) + " is not valid. "
        "Automatically adjusting to " + std::to_string(m_substeps + 1) + ".",
        ablastr::warn_manager::WarnPriority::medium);
    m_substeps += 1;
}
```

它必须为偶数，因为 `HybridPICEvolveFields()` 把整个 field step 分成两个半步，每半步执行 `substeps/2` 次 RK 推进。

电子压力参数的约束在源码中是硬 abort：

```cpp
utils::parser::queryWithParser(pp_hybrid, "gamma", m_gamma);
if (!utils::parser::queryWithParser(pp_hybrid, "elec_temp", m_elec_temp)) {
    Abort("hybrid_pic_model.elec_temp must be specified when using the hybrid solver");
}
const bool n0_ref_given = utils::parser::queryWithParser(pp_hybrid, "n0_ref", m_n0_ref);
if (m_gamma != 1.0 && !n0_ref_given) {
    Abort("hybrid_pic_model.n0_ref should be specified if hybrid_pic_model.gamma != 1");
}
```

随后把 eV 转成 J：

```cpp
// convert electron temperature from eV to J
m_elec_temp *= PhysConst::q_e;
```

因此文档里 `hybrid_pic_model.elec_temp` 的单位是 eV，但内部压力公式使用 SI 能量单位。

## 4. Hybrid 专用 MultiFab

`AllocateLevelMFs()` 分配 hybrid solver 独有的临时场：

```cpp
fields.alloc_init(FieldType::hybrid_electron_pressure_fp,
    lev, amrex::convert(ba, rho_nodal_flag),
    dm, ncomps, ngRho, 0.0_rt);

fields.alloc_init(FieldType::hybrid_rho_fp_temp,
    lev, amrex::convert(ba, rho_nodal_flag),
    dm, ncomps, ngRho, 0.0_rt);
```

`hybrid_electron_pressure_fp` 存 `P_e`，`hybrid_rho_fp_temp` 存上一时间层或中间时间层的 ion charge density。电流临时量分三类：

```cpp
fields.alloc_init(FieldType::hybrid_current_fp_temp, Direction{0},
    lev, amrex::convert(ba, jx_nodal_flag),
    dm, ncomps, ngJ, 0.0_rt);
...
fields.alloc_init(FieldType::hybrid_current_fp_plasma, Direction{0},
    lev, amrex::convert(ba, jx_nodal_flag),
    dm, ncomps, ngJ, 0.0_rt);
```

- `hybrid_current_fp_temp`：保存 `J_i^{n-1/2}`、`J_i^n` 或外推后的 `J_i^{n+1}`。
- `hybrid_current_fp_plasma`：保存由 `curl B / mu0` 得到的总 plasma current，之后减去外部电流。
- `hybrid_current_fp_external`：如果用户指定外部电流，则按同样 staggering 分配。

外部矢势场由 `ExternalVectorPotential` 额外分配：

```cpp
if (m_add_external_fields) {
    m_external_vector_potential->AllocateLevelMFs(
        fields,
        lev, ba, dm,
        ncomps, ngEB,
        Ex_nodal_flag, Ey_nodal_flag, Ez_nodal_flag,
        Bx_nodal_flag, By_nodal_flag, Bz_nodal_flag
    );
}
```

## 5. 初始化：parser、staggering 和外部电流

`InitData()` 编译电阻/超电阻 parser，并记录表达式是否依赖 `J` 或 `B`：

```cpp
m_resistivity_parser = std::make_unique<amrex::Parser>(
    utils::parser::makeParser(m_eta_expression, {"rho","J"}));
m_eta = m_resistivity_parser->compile<2>();
const std::set<std::string> resistivity_symbols = m_resistivity_parser->symbols();
m_resistivity_has_J_dependence += resistivity_symbols.count("J");

m_include_hyper_resistivity_term = (m_eta_h_expression != "0.0");
m_hyper_resistivity_parser = std::make_unique<amrex::Parser>(
    utils::parser::makeParser(m_eta_h_expression, {"rho","B"}));
m_eta_h = m_hyper_resistivity_parser->compile<2>();
```

随后它把 `J/B/E` 的 staggering 保存到 GPU array：

```cpp
amrex::IntVect Jx_stag = fields.get(FieldType::current_fp, Direction{0}, 0)->ixType().toIntVect();
amrex::IntVect Bx_stag = fields.get(FieldType::Bfield_fp, Direction{0}, 0)->ixType().toIntVect();
amrex::IntVect Ex_stag = fields.get(FieldType::Efield_fp, Direction{0}, 0)->ixType().toIntVect();
...
Jx_IndexType[idim]    = Jx_stag[idim];
Bx_IndexType[idim]    = Bx_stag[idim];
Ex_IndexType[idim]    = Ex_stag[idim];
```

这些 index type 直接被 `HybridPICSolveE.cpp` 的 `Interp()` 使用。它们决定了 `J`、`B`、`rho`、`P_e` 如何插值到 nodal grid 或 E-field staggering。

低维编译时，源码把未使用维度设为 nodal：

```cpp
#if defined(WARPX_DIM_XZ) || defined(WARPX_DIM_RZ) || defined(WARPX_DIM_1D_Z)
    Jx_IndexType[2]    = 1;
    Jy_IndexType[2]    = 1;
    Jz_IndexType[2]    = 1;
    Bx_IndexType[2]    = 1;
    By_IndexType[2]    = 1;
    Bz_IndexType[2]    = 1;
    Ex_IndexType[2]    = 1;
    Ey_IndexType[2]    = 1;
    Ez_IndexType[2]    = 1;
#endif
```

这是一个容易漏掉的实现细节：如果未使用维度不强制设成 nodal，通用插值函数会读到不合物理含义的 index type。

## 6. 主推进：`HybridPICEvolveFields()`

hybrid field push 的入口在 `WarpXPushFieldsHybridPIC.cpp`：

```cpp
void WarpX::HybridPICEvolveFields ()
{
    ...
    WARPX_ALWAYS_ASSERT_WITH_MESSAGE(
        finest_level == 0,
        "Ohm's law E-solve only works with a single level.");

    const int sub_steps = m_hybrid_pic_model->m_substeps;
    const bool add_external_fields = m_hybrid_pic_model->m_add_external_fields;
```

第一条硬限制是无 AMR。源码和参数文档都说明 hybrid solver 只支持 single level。

如果使用外部矢势分裂场，进入 field push 前先从 total `B` 中减去旧时刻外部 `B_ext`：

```cpp
if (add_external_fields) {
    m_hybrid_pic_model->m_external_vector_potential->UpdateHybridExternalFields(
        gett_old(0),
        0.5_rt*dt[0]);

    for (int lev = 0; lev <= finest_level; ++lev) {
        for (int idim = 0; idim < 3; ++idim) {
            MultiFab::Subtract(
                *m_fields.get(FieldType::Bfield_fp, Direction{idim}, lev),
                *m_fields.get(FieldType::hybrid_B_fp_external, Direction{idim}, lev),
                0, 0, 1,
                m_fields.get(FieldType::Bfield_fp, Direction{idim}, lev)->nGrowVect());
        }
    }
}
```

这说明内部 hybrid push 操作的是“自洽演化场”，外部场只在需要的地方作为 split contribution 加入。

## 7. 时间层组织：rho 和 ion current

粒子已经被推进到 `t_{n+1}` 后，hybrid solver 先沉积：

```cpp
// The particles have now been pushed to their t_{n+1} positions.
// Perform charge deposition at t_{n+1} and current deposition at t_{n+1/2}.
HybridPICDepositRhoAndJ();
```

此时已知：

- `rho_fp_temp = rho^n`
- `rho_fp = rho^{n+1}`
- `current_fp_temp = J_i^{n-1/2}`
- `current_fp = J_i^{n+1/2}`

源码注释直接写明这个状态：

```cpp
// During the above deposition the charge and current density were updated
// so that, at this time, we have rho^{n} in rho_fp_temp, rho{n+1} in the
// 0'th index of `rho_fp`, J_i^{n-1/2} in `current_fp_temp` and J_i^{n+1/2}
// in `current_fp`.
```

第一半步需要 `J_i^n`：

```cpp
MultiFab::LinComb(
    *current_fp_temp[lev][idim],
    0.5_rt, *current_fp_temp[lev][idim], 0,
    0.5_rt, *m_fields.get(FieldType::current_fp, Direction{idim}, lev), 0,
    0, 1, current_fp_temp[lev][idim]->nGrowVect()
);
```

也就是

$$
\mathbf J_i^n=\frac12\left(\mathbf J_i^{n-1/2}+\mathbf J_i^{n+1/2}\right).
$$

第二半步需要

$$
\rho^{n+1/2}=\frac12(\rho^n+\rho^{n+1}),
$$

对应源码：

```cpp
MultiFab::LinComb(
    *rho_fp_temp[lev], 0.5_rt, *rho_fp_temp[lev], 0,
    0.5_rt, *m_fields.get(FieldType::rho_fp, lev), 0, 0, 1, rho_fp_temp[lev]->nGrowVect()
);
```

最后为了得到 `E^{n+1}`，外推离子电流：

```cpp
MultiFab::LinComb(
    *current_fp_temp[lev][idim],
    -1._rt, *current_fp_temp[lev][idim], 0,
    2._rt, *m_fields.get(FieldType::current_fp, Direction{idim}, lev), 0,
    0, 1, current_fp_temp[lev][idim]->nGrowVect()
);
```

因为此时 `current_fp_temp` 已经是 `J_i^n`，这条语句给出

$$
\mathbf J_i^{n+1}=2\mathbf J_i^{n+1/2}-\mathbf J_i^n
=\frac32\mathbf J_i^{n+1/2}-\frac12\mathbf J_i^{n-1/2}.
$$

这和理论文档中的 extrapolation step 一致。

## 8. `BfieldEvolveRK()`：每个 half-step 的 RK4

hybrid solver 不用单个大步推进 `B`，而是在两个半步中各执行 `substeps/2` 次 RK：

```cpp
const int sub_steps_per_half = sub_steps / 2;
for (int sub_step = 0; sub_step < sub_steps_per_half; sub_step++)
{
    m_hybrid_pic_model->BfieldEvolveRK(
        m_fields.get_mr_levels_alldirs(FieldType::Bfield_fp, finest_level),
        m_fields.get_mr_levels_alldirs(FieldType::Efield_fp, finest_level),
        current_fp_temp, rho_fp_temp,
        m_eb_update_E,
        dt[0]/sub_steps,
        SubcyclingHalf::FirstHalf, guard_cells.ng_FieldSolver,
        WarpX::sync_nodal_points
    );
}
```

`BfieldEvolveRK()` 先保存旧 `B`，再分配两个 component 的 `K`：

```cpp
std::array< MultiFab, 3 > B_old;
std::array< MultiFab, 3 > K;
for (int ii = 0; ii < 3; ii++)
{
    B_old[ii] = MultiFab(
        Bfield[lev][ii]->boxArray(), Bfield[lev][ii]->DistributionMap(), 1,
        Bfield[lev][ii]->nGrowVect()
    );
    MultiFab::Copy(B_old[ii], *Bfield[lev][ii], 0, 0, 1, ng);

    K[ii] = MultiFab(
        Bfield[lev][ii]->boxArray(), Bfield[lev][ii]->DistributionMap(), 2,
        Bfield[lev][ii]->nGrowVect()
    );
}
```

每个 RK stage 都调用 `FieldPush()`，而 `FieldPush()` 的含义是：

```cpp
// Calculate J = curl x B / mu0 - J_ext
CalculatePlasmaCurrent(Bfield, eb_update_E);
// Calculate the E-field from Ohm's law
HybridPICSolveE(Efield, Jfield, Bfield, rhofield, eb_update_E, true);
...
// Push forward the B-field using Faraday's law
warpx.EvolveB(dt, subcycling_half, t_old);
warpx.FillBoundaryB(ng, nodal_sync);
```

所以 RK 的每个 stage 都会用当前 stage 的 `B` 重新计算 plasma current 和 Ohm-law `E`，再用 Faraday 推进 `B`。这就是 hybrid solver 稳定性和成本的核心。

最终 RK4 组合写成：

```cpp
Kx(i, j, k, 0) += Bx(i, j, k) - Bx_old(i, j, k) + 2.0_rt * Kx(i, j, k, 1);
Bx(i, j, k) = Bx_old(i, j, k) + Kx(i, j, k, 0) / 3.0_rt;
```

因为 `K` 中存的是带 `dt` 因子的中间增量，这里的 `/3` 对应经典 RK4 权重

$$
\frac{1}{6}(K_0+2K_1+2K_2+K_3),
$$

只不过源码里的 `K0`、`K1` 已经以 `0.5 dt` 的形式存储。

## 9. `CalculatePlasmaCurrent()`：Ampere 电流减外部电流

Ohm 定律需要总 plasma current。WarpX 用 FDTD solver 的 Ampere curl 计算：

```cpp
ablastr::fields::VectorField current_fp_plasma =
    warpx.m_fields.get_alldirs(FieldType::hybrid_current_fp_plasma, lev);
warpx.get_pointer_fdtd_solver_fp(lev)->CalculateCurrentAmpere(
    current_fp_plasma, Bfield, eb_update_E, lev
);
```

随后填 guard cells：

```cpp
for (int i=0; i<3; i++) {
    current_fp_plasma[i]->FillBoundary(warpx.Geom(lev).periodicity());
}
```

如果有外部电流，还要减掉：

```cpp
if (m_has_external_current) {
    ablastr::fields::VectorField current_fp_external =
        warpx.m_fields.get_alldirs(FieldType::hybrid_current_fp_external, lev);
    for (int i=0; i<3; i++) {
        current_fp_plasma[i]->minus(*current_fp_external[i], 0, 1, 1);
    }
}
```

物理上这是把 `J_ext` 从 Ampere 总电流里剥离出来，保证 `J_e = J - J_i - J_ext`。

## 10. 电子压力

电子压力闭合在头文件里是一个静态函数：

```cpp
struct ElectronPressure {

    AMREX_GPU_HOST_DEVICE AMREX_FORCE_INLINE
    static amrex::Real get_pressure (amrex::Real const n0,
                                     amrex::Real const T0,
                                     amrex::Real const gamma,
                                     amrex::Real const rho) {
        return n0 * T0 * std::pow((rho/PhysConst::q_e)/n0, gamma);
    }
};
```

对应公式是：

$$
P_e=n_0T_{e0}\left(\frac{n_e}{n_0}\right)^\gamma,
\qquad n_e=\rho/e.
$$

`FillElectronPressureMF()` 对每个 cell 填写：

```cpp
ParallelFor(tilebox, [=] AMREX_GPU_DEVICE (int i, int j, int k) {
    Pe(i, j, k) = ElectronPressure::get_pressure(
        n0_ref, elec_temp, gamma, rho(i, j, k)
    );
});
```

然后 `CalculateElectronPressure()` 应用 electron pressure 边界并填 guard：

```cpp
warpx.ApplyElectronPressureBoundary(lev, PatchType::fine);
ablastr::utils::communication::FillBoundary(
    *electron_pressure_fp,
    WarpX::do_single_precision_comms,
    warpx.Geom(lev).periodicity(),
    true);
```

## 11. Ohm 定律 kernel：两步算 E

`FiniteDifferenceSolver::HybridPICSolveE()` 先根据几何和 grid type 选择模板：

```cpp
if (WarpX::grid_type == GridType::Staggered)
{
    HybridPICSolveECartesian <CartesianYeeAlgorithm> (
        Efield, Jfield, Jifield, Bfield, rhofield, Pefield,
        eb_update_E, lev, hybrid_model, solve_for_Faraday
    );
} else {
    HybridPICSolveECartesian <CartesianNodalAlgorithm> (
        Efield, Jfield, Jifield, Bfield, rhofield, Pefield,
        eb_update_E, lev, hybrid_model, solve_for_Faraday
    );
}
```

Cartesian kernel 明确写了 E-field calculation 的两步：

```cpp
// The E-field calculation is done in 2 steps:
// 1) The J x B term is calculated on a nodal mesh in order to ensure
//    energy conservation.
// 2) The nodal E-field values are averaged onto the Yee grid and the
//    electron pressure & resistivity terms are added (these terms are
//    naturally located on the Yee grid).
```

第一步在 nodal grid 上计算 `(J-Ji)xB`：

```cpp
// calculate enE = (J - Ji) x B
enE_nodal(i, j, k, 0) = (
    (jy_interp - jiy_interp) * Bz_interp
    - (jz_interp - jiz_interp) * By_interp
);
enE_nodal(i, j, k, 1) = (
    (jz_interp - jiz_interp) * Bx_interp
    - (jx_interp - jix_interp) * Bz_interp
);
enE_nodal(i, j, k, 2) = (
    (jx_interp - jix_interp) * By_interp
    - (jy_interp - jiy_interp) * Bx_interp
);
```

第二步把 nodal `enE` 插值到 E-field 所在位置，加压力梯度、电阻和超电阻。以 `Ex` 为例：

```cpp
const Real rho_val = Interp(rho, nodal, Ex_stag, coarsen, i, j, k, 0);

if (rho_val < rho_floor && holmstrom_vacuum_region) {
    Ex(i, j, k) = 0._rt;
} else {
    const Real grad_Pe = (!solve_for_Faraday) ?
        T_Algo::UpwardDx(Pe, coefs_x, n_coefs_x, i, j, k)
        : 0._rt;

    const auto enE_x = Interp(enE, nodal, Ex_stag, coarsen, i, j, k, 0);
    const auto rho_val_limited = std::max(rho_val, rho_floor);

    Ex(i, j, k) = (enE_x - grad_Pe) / rho_val_limited;
}
```

这里 `rho_val_limited` 是 `1/rho` 的数值保护；`holmstrom_vacuum_region` 打开时，低密度区域直接把 `E` 设为 0，用来抑制 vacuum fluctuation。

`solve_for_Faraday` 是一个非常关键的开关。源码只在要用这个 `E` 推进 `B` 时加入电阻/超电阻项：

```cpp
if (solve_for_Faraday) {
    Real jtot_val = 0._rt;
    if (resistivity_has_J_dependence) {
        const Real jx_val = Jx(i, j, k);
        const Real jy_val = Interp(Jy, Jy_stag, Ex_stag, coarsen, i, j, k, 0);
        const Real jz_val = Interp(Jz, Jz_stag, Ex_stag, coarsen, i, j, k, 0);
        jtot_val = std::sqrt(jx_val*jx_val + jy_val*jy_val + jz_val*jz_val);
    }

    Ex(i, j, k) += eta(rho_val, jtot_val) * Jx(i, j, k);
```

超电阻是 Laplacian of current：

```cpp
auto nabla2Jx = T_Algo::Dxx(Jx, coefs_x, n_coefs_x, i, j, k)
    + T_Algo::Dyy(Jx, coefs_y, n_coefs_y, i, j, k)
    + T_Algo::Dzz(Jx, coefs_z, n_coefs_z, i, j, k);

Ex(i, j, k) -= eta_h(rho_val, btot_val) * nabla2Jx;
```

因此实际离散形式可以读成：

$$
E_x
=\frac{[(J-J_i)\times B]_x-\partial_xP_e}{\rho_{\rm lim}}
+\eta J_x-\eta_h\nabla^2J_x,
$$

其中压力梯度项只在最终 `E^{n+1}` 计算时加入，Faraday push 的中间 `E` 跳过它，因为

$$
\nabla\times\nabla P_e=0
$$

对 `B` 推进没有贡献。

## 12. 外部矢势 split fields

`ExternalVectorPotential` 用空间函数 `A(x,y,z)` 和时间函数 `s(t)` 生成外部场：

```cpp
pp_ext_A.queryarr("fields", m_field_names);

WARPX_ALWAYS_ASSERT_WITH_MESSAGE(!m_field_names.empty(),
    "No external field names defined in external_vector_potential.fields");
```

如果不是从文件读，就读取空间表达式：

```cpp
pp_ext_A.query(m_field_names[i]+".Ax_external_grid_function(x,y,z)",
    m_Ax_ext_grid_function[i]);
...
pp_ext_A.query(m_field_names[i]+".A_time_external_function(t)",
    m_A_ext_time_function[i]);
```

源码禁止把时间依赖直接塞进空间 `A`：

```cpp
const std::set<std::string> A_ext_symbols = m_A_external_parser[i][idim]->symbols();
WARPX_ALWAYS_ASSERT_WITH_MESSAGE(A_ext_symbols.count("t") == 0,
    "Externally Applied Vector potential time variation must be set with A_time_external_function(t)");
```

初始化后可选做 `div A` projection cleaning，再计算参考 curl：

```cpp
if (m_do_clean_divA) {
    warpx::initialization::ProjectionDivCleaner dc(Aext_field, true);
    dc.setSourceFromField();
    dc.solve();
    dc.correctField();
}

CalculateExternalCurlA(m_field_names[i]);
```

`UpdateHybridExternalFields(t, dt)` 里，外部 `B` 和 `E` 来自：

$$
\mathbf B_{\rm ext}=s(t)\nabla\times\mathbf A,
$$

$$
\mathbf E_{\rm ext}=-\frac{s(t+\Delta t/2)-s(t-\Delta t/2)}{\Delta t}\mathbf A.
$$

源码就是：

```cpp
const amrex::Real scale_factor_B = m_A_time_scale[i](t);

const amrex::Real sf_l = m_A_time_scale[i](t-0.5_rt*dt);
const amrex::Real sf_r = m_A_time_scale[i](t+0.5_rt*dt);
const amrex::Real scale_factor_E = -(sf_r - sf_l)/dt;
```

然后累加到 `hybrid_E_fp_external` 和 `hybrid_B_fp_external`：

```cpp
AddExternalFieldFromVectorPotential(E_ext[lev], scale_factor_E, A_ext[lev], warpx.GetEBUpdateEFlag()[lev]);
AddExternalFieldFromVectorPotential(B_ext[lev], scale_factor_B, curlA_ext[lev], warpx.GetEBUpdateBFlag()[lev]);
```

## 13. 边界和未实现分支

当前源码和文档给出的限制必须在书稿中明确：

- `HybridPICEvolveFields()` 要求 `finest_level == 0`，不支持 AMR。
- `HybridPICSolveE()` 如果 `lev > 0` 直接 abort。
- RZ 只支持 `m=0` azimuthal mode。
- RSPHERE 的 hybrid E solve 还没有完整实现。
- 外部矢势 split fields 要求 `external_vector_potential.fields` 非空。
- 外部矢势的时间变化只能通过 `A_time_external_function(t)`，不能写在 `A[x/y/z]_external_grid_function(x,y,z)` 里。

对应源码之一是：

```cpp
void FiniteDifferenceSolver::HybridPICSolveESpherical (
    ...
{
    WARPX_ABORT_WITH_MESSAGE("HybridPICSolveESphrical not fully implemented");
}
```

## 14. 这一轮需要带入正文的结论

- hybrid PIC 的 `E` 不是 Maxwell-Ampere 推进结果，而是 Ohm 定律闭合结果。
- `rho_fp_temp` / `current_fp_temp` 是时间层缓存，不是普通 scratch array。
- `BfieldEvolveRK()` 每个 RK stage 都重新计算 `J=curl B/mu0-J_ext` 和 Ohm-law `E`。
- `HybridPICSolveE.cpp` 的能量一致性关键在于先在 nodal grid 上算 `(J-J_i)xB`，再插值回 E staggering。
- `solve_for_Faraday` 控制是否加入会影响 `curl E` 的项；压力梯度在中间 Faraday solve 中可跳过。
- 外部矢势实现的是 split-field 外场，`B_ext=s(t)curl A`，`E_ext=-ds/dt A`。
