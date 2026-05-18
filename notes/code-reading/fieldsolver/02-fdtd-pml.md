# FDTD PML 更新精读

绑定源码：`../warpx`，分支 `pkuHEDPbranch`，commit `063f8b586f04321e13150ae3e730e0794ca75cb1`。

本笔记覆盖 Cartesian FDTD PML 的第一轮源码阅读：

- `../warpx/Source/FieldSolver/FiniteDifferenceSolver/EvolveBPML.cpp`
- `../warpx/Source/FieldSolver/FiniteDifferenceSolver/EvolveEPML.cpp`
- `../warpx/Source/FieldSolver/FiniteDifferenceSolver/EvolveFPML.cpp`
- `../warpx/Source/BoundaryConditions/PMLComponent.H`
- 官方理论文档 `../warpx/Docs/source/theory/boundary_conditions.rst`
- 官方参数文档 `../warpx/Docs/source/usage/parameters.rst`

## 1. PML 的物理目标：无反射吸收电磁波

官方理论文档位置：`../warpx/Docs/source/theory/boundary_conditions.rst:8-60`。Berenger PML 对 TE 情形把场分量拆开，例如：

```rst
\varepsilon _{0}\frac{\partial E_{x}}{\partial t}+\sigma _{y}E_{x} = \frac{\partial H_{z}}{\partial y}

\varepsilon _{0}\frac{\partial E_{y}}{\partial t}+\sigma _{x}E_{y} = -\frac{\partial H_{z}}{\partial x}

\mu _{0}\frac{\partial H_{zx}}{\partial t}+\sigma ^{*}_{x}H_{zx} = -\frac{\partial E_{y}}{\partial x}

\mu _{0}\frac{\partial H_{zy}}{\partial t}+\sigma ^{*}_{y}H_{zy} = \frac{\partial E_{x}}{\partial y}

H_{z}  = H_{zx}+H_{zy}
```

核心思想是：

- 在吸收层中引入空间相关的阻尼系数 $\sigma$。
- 把某些场分量拆成沿不同方向阻尼的 split components。
- 在理想参数匹配下，入射波进入 PML 不产生阻抗突变，因此尽量少反射。

官方文档进一步给出离散更新，位置 `boundary_conditions.rst:174-210`。其中典型形式是

$$
E_x^{n+1}
=\frac{1-\sigma_y\Delta t/2}{1+\sigma_y\Delta t/2}E_x^n
+\frac{\Delta t/\Delta y}{1+\sigma_y\Delta t/2}
(H_z^{n+1/2}(k+1/2)-H_z^{n+1/2}(k-1/2)).
$$

当前笔记只读 field update 源码；阻尼系数 $\sigma$ 的生成和 damping 操作在 `BoundaryConditions/PML.*` 中，后续边界章节继续展开。

## 2. PML 参数入口

官方参数文档位置：`../warpx/Docs/source/usage/parameters.rst:888-952`。

```rst
.. pp:param:: warpx.pml_ncell
    :type: ``int``
    :default: 10

    The depth of the PML, in number of cells.

.. pp:param:: warpx.pml_delta
    :type: ``int``
    :default: 10

    The characteristic depth, in number of cells, over which
    the absorption coefficients of the PML increases.

.. pp:param:: warpx.do_pml_in_domain
    :type: ``int``
    :default: 0

    Whether to create the PML inside the simulation area or outside. If inside,
    it allows the user to propagate particles in PML and to use extended PML

.. pp:param:: warpx.pml_has_particles
    :type: ``int``
    :default: 0

    Whether to propagate particles in PML or not. Can only be done if PML are in simulation domain,
    i.e. if ``warpx.do_pml_in_domain = 1``.
```

与本节源码直接相关的还有：

```rst
.. pp:param:: warpx.do_pml_j_damping
    :type: ``int``
    :default: 0

    Whether to damp current in PML. Can only be used if particles are propagated in PML,
    i.e. if ``warpx.pml_has_particles = 1``.

.. pp:param:: warpx.do_pml_dive_cleaning
    :type: ``bool``

    Whether to use divergence cleaning for E in the PML region.

.. pp:param:: warpx.do_pml_divb_cleaning
    :type: ``bool``

    Whether to use divergence cleaning for B in the PML region.
```

`EvolveEPML.cpp` 中的 `pml_has_particles` 控制 PML 电流项是否进入 E 更新；`EvolveBPML.cpp` 中的 `dive_cleaning` 控制是否把 PML split E 的 diagonal components 也加入 B 更新。

## 3. PML split components 的存储方式

源码位置：`../warpx/Source/BoundaryConditions/PMLComponent.H:8-18`。

```cpp
/* In WarpX, the split fields of the PML (e.g. Eyx, Eyz) are stored as
 * components of a MultiFab (e.g. component 0 and 1 of the MultiFab for Ey)
 * The correspondence between the component index (0,1) and its meaning
 * (yx, yz, etc.) is defined in the present file */

 struct PMLComp {
   enum { xy=0, xz=1, xx=2,
          yz=0, yx=1, yy=2,
          zx=0, zy=1, zz=2,
          x=0, y=1, z=2 }; // Used for the PML components of F
 };
```

例如：

- `Ex(..., PMLComp::xy)` 表示 `Ex` 中由 y 方向 derivative 驱动的 split component。
- `Ex(..., PMLComp::xz)` 表示 `Ex` 中由 z 方向 derivative 驱动的 split component。
- `Ex(..., PMLComp::xx)` 用于 `F` 的 `grad(F)` 修正。
- `F(..., PMLComp::x/y/z)` 是 PML 中 `F` 的三个 split components。

普通区域中 `Ex/Ey/Ez` 每个 `MultiFab` 通常只需要一个 component；PML 区域中每个场分量需要多个 split components。

## 4. `EvolveBPML()`：B 的 split-field curl(E)

PML B 更新入口在 `../warpx/Source/FieldSolver/FiniteDifferenceSolver/EvolveBPML.cpp:37-79`。

```cpp
void FiniteDifferenceSolver::EvolveBPML (
    ablastr::fields::MultiFabRegister& fields,
    PatchType patch_type,
    int level,
    amrex::Real const dt,
    const bool dive_cleaning
)
{
    using warpx::fields::FieldType;

    // Select algorithm (The choice of algorithm is a runtime option,
    // but we compile code for each algorithm, using templates)
#if defined(WARPX_DIM_RZ) || defined(WARPX_DIM_RCYLINDER) || defined(WARPX_DIM_RSPHERE)
    amrex::ignore_unused(fields, patch_type, level, dt, dive_cleaning);
    WARPX_ABORT_WITH_MESSAGE(
        "PML only implemented in Cartesian geometry.");
#else
    const ablastr::fields::VectorField Bfield = (patch_type == PatchType::fine) ?
        fields.get_alldirs(FieldType::pml_B_fp, level) : fields.get_alldirs(FieldType::pml_B_cp, level);
    const ablastr::fields::VectorField Efield = (patch_type == PatchType::fine) ?
        fields.get_alldirs(FieldType::pml_E_fp, level) : fields.get_alldirs(FieldType::pml_E_cp, level);
```

重要边界：FDTD PML 在这里显式只支持 Cartesian。RZ/RCYLINDER/RSPHERE 会 abort，而不是静默降级。

算法分派和普通 `EvolveB()` 一致：

```cpp
if (m_grid_type == ablastr::utils::enums::GridType::Collocated) {
    EvolveBPMLCartesian <CartesianNodalAlgorithm> (Bfield, Efield, dt, dive_cleaning);
} else if (m_fdtd_algo == ElectromagneticSolverAlgo::Yee || m_fdtd_algo == ElectromagneticSolverAlgo::ECT) {
    EvolveBPMLCartesian <CartesianYeeAlgorithm> (Bfield, Efield, dt, dive_cleaning);
} else if (m_fdtd_algo == ElectromagneticSolverAlgo::CKC) {
    EvolveBPMLCartesian <CartesianCKCAlgorithm> (Bfield, Efield, dt, dive_cleaning);
}
```

`Bx` 的 split 更新源码位置：`EvolveBPML.cpp:113-137`。

```cpp
Bx(i, j, k, PMLComp::xz) += dt * (
    T_Algo::UpwardDz(Ey, coefs_z, n_coefs_z, i, j, k, PMLComp::yx)
  + T_Algo::UpwardDz(Ey, coefs_z, n_coefs_z, i, j, k, PMLComp::yz)
  + UpwardDz_Ey_yy);

Bx(i, j, k, PMLComp::xy) -= dt * (
    T_Algo::UpwardDy(Ez, coefs_y, n_coefs_y, i, j, k, PMLComp::zx)
  + T_Algo::UpwardDy(Ez, coefs_y, n_coefs_y, i, j, k, PMLComp::zy)
  + UpwardDy_Ez_zz);
```

它对应普通区域中

$$
\partial_t B_x=\partial_zE_y-\partial_yE_z,
$$

但 PML 中 `E_y` 和 `E_z` 被拆成多个 components，因此源码对 `PMLComp::yx/yz/yy`、`PMLComp::zx/zy/zz` 求和。

`dive_cleaning` 为真时，才加入 diagonal components：

```cpp
amrex::Real UpwardDz_Ey_yy = 0._rt;
amrex::Real UpwardDy_Ez_zz = 0._rt;
if (dive_cleaning)
{
    UpwardDz_Ey_yy = T_Algo::UpwardDz(Ey, coefs_z, n_coefs_z, i, j, k, PMLComp::yy);
    UpwardDy_Ez_zz = T_Algo::UpwardDy(Ez, coefs_y, n_coefs_y, i, j, k, PMLComp::zz);
}
```

这说明 PML 中的 divergence-cleaning components 会参与 B 更新；不开启时它们不进入 curl(E)。

## 5. `EvolveEPML()`：E 的 split-field curl(B)、F 修正和 PML 粒子电流

PML E 更新入口在 `../warpx/Source/FieldSolver/FiniteDifferenceSolver/EvolveEPML.cpp:40-99`。

```cpp
void FiniteDifferenceSolver::EvolveEPML (
    ablastr::fields::MultiFabRegister& fields,
    PatchType patch_type,
    int level,
    MultiSigmaBox const& sigba,
    amrex::Real const dt, bool pml_has_particles ) {
```

和 B 一样，FDTD PML 只支持 Cartesian：

```cpp
#if defined(WARPX_DIM_RZ) || defined(WARPX_DIM_RCYLINDER) || defined(WARPX_DIM_RSPHERE)
    amrex::ignore_unused(fields, patch_type, level, sigba, dt, pml_has_particles);
    WARPX_ABORT_WITH_MESSAGE(
        "PML are only implemented in Cartesian geometry.");
```

它取出 PML E/B/J 和可选 `pml_F`：

```cpp
const ablastr::fields::VectorField Efield = (patch_type == PatchType::fine) ?
    fields.get_alldirs(FieldType::pml_E_fp, level) : fields.get_alldirs(FieldType::pml_E_cp, level);
const ablastr::fields::VectorField Bfield = (patch_type == PatchType::fine) ?
    fields.get_alldirs(FieldType::pml_B_fp, level) : fields.get_alldirs(FieldType::pml_B_cp, level);
const ablastr::fields::VectorField Jfield = (patch_type == PatchType::fine) ?
    fields.get_alldirs(FieldType::pml_j_fp, level) : fields.get_alldirs(FieldType::pml_j_cp, level);
```

`Ex` split 更新位置：`EvolveEPML.cpp:151-160`。

```cpp
Ex(i, j, k, PMLComp::xz) -= c2 * dt * (
    T_Algo::DownwardDz(By, coefs_z, n_coefs_z, i, j, k, PMLComp::yx)
  + T_Algo::DownwardDz(By, coefs_z, n_coefs_z, i, j, k, PMLComp::yz) );
Ex(i, j, k, PMLComp::xy) += c2 * dt * (
    T_Algo::DownwardDy(Bz, coefs_y, n_coefs_y, i, j, k, PMLComp::zx)
  + T_Algo::DownwardDy(Bz, coefs_y, n_coefs_y, i, j, k, PMLComp::zy) );
```

这对应普通区域中

$$
\partial_tE_x=c^2(\partial_yB_z-\partial_zB_y),
$$

但同样写成 split components。

若 `Ffield` 存在，PML E 加上 split `grad(F)`：

```cpp
Ex(i, j, k, PMLComp::xx) += c2 * dt * (
    T_Algo::UpwardDx(F, coefs_x, n_coefs_x, i, j, k, PMLComp::x)
  + T_Algo::UpwardDx(F, coefs_x, n_coefs_x, i, j, k, PMLComp::y)
  + T_Algo::UpwardDx(F, coefs_x, n_coefs_x, i, j, k, PMLComp::z) );
```

如果 PML 中允许粒子传播，则 PML E 还要响应 PML 电流。源码位置：`EvolveEPML.cpp:238-275`。

```cpp
if (pml_has_particles) {
    Array4<Real> const& Jx = Jfield[0]->array(mfi);
    Array4<Real> const& Jy = Jfield[1]->array(mfi);
    Array4<Real> const& Jz = Jfield[2]->array(mfi);
    const Real* sigmaj_x = sigba[mfi].sigma[0].data();
    const Real* sigmaj_y = sigba[mfi].sigma[1].data();
    const Real* sigmaj_z = sigba[mfi].sigma[2].data();
    // ...
    const Real mu_c2_dt = (PhysConst::mu0*PhysConst::c2) * dt;

    amrex::ParallelFor( tex, tey, tez,
        [=] AMREX_GPU_DEVICE (int i, int j, int k) {
            push_ex_pml_current(i, j, k, Ex, Jx,
                sigmaj_y, sigmaj_z, y_lo, z_lo, mu_c2_dt);
        },
```

普通区域中电流项是

$$
-c^2\mu_0\mathbf J.
$$

PML 中通过 `push_ex_pml_current` 等 helper 结合 sigma damping 处理，helper 定义在 `BoundaryConditions/PML_current.H`，后续粒子-in-PML 和 current damping 会继续展开。

## 6. `EvolveFPML()`：PML 中的 div(E) cleaning

PML F 更新入口位置：`../warpx/Source/FieldSolver/FiniteDifferenceSolver/EvolveFPML.cpp:39-67`。

```cpp
void FiniteDifferenceSolver::EvolveFPML (
    amrex::MultiFab* Ffield,
    ablastr::fields::VectorField const Efield,
    amrex::Real const dt ) {

    // Select algorithm (The choice of algorithm is a runtime option,
    // but we compile code for each algorithm, using templates)
#if defined(WARPX_DIM_RZ) || defined(WARPX_DIM_RCYLINDER) || defined(WARPX_DIM_RSPHERE)
    amrex::ignore_unused(Ffield, Efield, dt);
    WARPX_ABORT_WITH_MESSAGE(
        "PML are only implemented in Cartesian geometry.");
```

主 kernel 位置：`EvolveFPML.cpp:92-125`。

```cpp
F(i, j, k, PMLComp::x) += dt * (
      T_Algo::DownwardDx(Ex, coefs_x, n_coefs_x, i, j, k, PMLComp::xx)
    + T_Algo::DownwardDx(Ex, coefs_x, n_coefs_x, i, j, k, PMLComp::xy)
    + T_Algo::DownwardDx(Ex, coefs_x, n_coefs_x, i, j, k, PMLComp::xz) );

F(i, j, k, PMLComp::y) += dt * (
      T_Algo::DownwardDy(Ey, coefs_y, n_coefs_y, i, j, k, PMLComp::yx)
    + T_Algo::DownwardDy(Ey, coefs_y, n_coefs_y, i, j, k, PMLComp::yy)
    + T_Algo::DownwardDy(Ey, coefs_y, n_coefs_y, i, j, k, PMLComp::yz) );

F(i, j, k, PMLComp::z) += dt * (
      T_Algo::DownwardDz(Ez, coefs_z, n_coefs_z, i, j, k, PMLComp::zx)
    + T_Algo::DownwardDz(Ez, coefs_z, n_coefs_z, i, j, k, PMLComp::zy)
    + T_Algo::DownwardDz(Ez, coefs_z, n_coefs_z, i, j, k, PMLComp::zz) );
```

普通区域 `F` 更新是

$$
\partial_tF=\nabla\cdot\mathbf E-\rho/\epsilon_0.
$$

PML 中这里没有 rho 项；它只累积 split E 的 divergence。PML 中粒子电流对 E 的影响在 `EvolveEPML()` 中处理。

## 7. 当前已确认的功能边界

- FDTD PML 源码明确只支持 Cartesian；RZ、RCYLINDER、RSPHERE 会 abort。
- `EvolveBPML()`、`EvolveEPML()`、`EvolveFPML()` 都复用 `CartesianYee/CKC/Nodal` 差分模板。
- PML 场不是普通 `E/B/F` 的单 component 副本，而是 split components 存储在多 component `MultiFab` 中。
- `EvolveG()` 中普通区域的 `G` 已实现，但 `WarpX::EvolveG()` 注释写明 PML 中 `G` evolution 仍是 TODO；PML 里当前只看到 `F` 的 split update。
- 如果 `pml_has_particles` 为真，PML E 更新还要处理 `pml_j`，并通过 sigma arrays 做 current damping/absorption。

后续需要继续进入：

- `BoundaryConditions/PML.cpp`：PML box、sigma profile、damping 因子的构造。
- `BoundaryConditions/PML_current.H`：`push_ex_pml_current` 等电流阻尼 helper。
- `EvolveBPML/EPML` 与 `DampPML()` 在主循环中的先后关系。

