# `AllocLevelMFs()` 特例分支：external particle fields、`rho/F/G`、HybridPIC、fluids、macroscopic、EB

绑定源码：

- `../warpx/Source/WarpX.cpp`
- `../warpx/Source/Initialization/WarpXInitData.cpp`

上一篇 `11-readparameters-combination-constraints.md` 解释了 `ReadParameters()` 怎样先裁掉不合法的组合。这一篇只做下一步：这些组合一旦成立，`AllocLevelMFs()` 和 `InitData()` 会具体分配哪些字段、创建哪些物理支线对象、以及这些对象在 fresh-run 初始化主链里何时真正被消费。

## 1. `rho_fp` 不是总存在的，它的分量数由 solver 和 cleaning 共同决定

源码位置：`../warpx/Source/WarpX.cpp:2670-2690`。

```cpp
int rho_ncomps = 0;
if( (electrostatic_solver_id == ElectrostaticSolverAlgo::LabFrame) ||
    (electrostatic_solver_id == ElectrostaticSolverAlgo::LabFrameElectroMagnetostatic) ||
    (electrostatic_solver_id == ElectrostaticSolverAlgo::LabFrameEffectivePotential) ||
    (electromagnetic_solver_id == ElectromagneticSolverAlgo::HybridPIC) ) {
    rho_ncomps = ncomps;
}
if (do_dive_cleaning) {
    rho_ncomps = 2*ncomps;
}
if (WarpX::electromagnetic_solver_id == ElectromagneticSolverAlgo::PSATD) {
    if (do_dive_cleaning || update_with_rho || current_correction) {
        rho_ncomps = (WarpX::m_JRhom) ? ncomps : 2*ncomps;
    }
}
if (rho_ncomps > 0)
{
    m_fields.alloc_init(FieldType::rho_fp, ... rho_ncomps, ngRho, 0.0_rt);
}
```

这里最重要的是：`rho_fp` 并不是“电荷密度字段当然总要有”。WarpX 只在以下几类路径下显式分配它：

- electrostatic 系列
- `HybridPIC`
- `do_dive_cleaning`
- PSATD 且需要 `update_with_rho` 或 `current_correction`

分量数也不是固定的：

- 普通 electrostatic / `HybridPIC`：`rho_ncomps = ncomps`
- `do_dive_cleaning`：升到 `2*ncomps`
- PSATD：
  - 一般 `update_with_rho/current_correction` 需要 `2*ncomps`
  - `JRhom` 特例又收回到 `ncomps`

所以这里的本质不是“存不存一份 rho”，而是“这个 solver 在初始化和推进中是否真的把 rho 当作演化态变量来持有，以及要不要区分 old/new”。

## 2. `phi_fp`、`F_fp`、`G_fp` 是三条不同的约束字段，不要混读

源码位置：`../warpx/Source/WarpX.cpp:2692-2719`。

```cpp
if (electrostatic_solver_id == ElectrostaticSolverAlgo::LabFrame ||
    electrostatic_solver_id == ElectrostaticSolverAlgo::LabFrameElectroMagnetostatic ||
    electrostatic_solver_id == ElectrostaticSolverAlgo::LabFrameEffectivePotential )
{
    m_fields.alloc_init(FieldType::phi_fp, ... ncomps, ngPhi, 0.0_rt );
}

if (do_dive_cleaning)
{
    m_fields.alloc_init(FieldType::F_fp, ... ncomps, ngF, 0.0_rt);
}

if (do_divb_cleaning)
{
    m_fields.alloc_init(FieldType::G_fp, ... ncomps, ngG, 0.0_rt);
}
```

这三条线分别对应三种完全不同的物理/算法角色：

- `phi_fp`
  - 只属于 electrostatic / electromagnetostatic / effective-potential 解法
  - 是 Poisson 或相关势求解器的主状态
- `F_fp`
  - 只在 `do_dive_cleaning` 时存在
  - 属于演化阶段的 `div(E)` 清理辅助场
- `G_fp`
  - 只在 `do_divb_cleaning` 时存在
  - 属于演化阶段的 `div(B)` 清理辅助场

因此初始化阶段里“分配了一个标量场”这件事不能笼统解释。这里至少有三种来源：

- electrostatic 势
- electric divergence cleaner
- magnetic divergence cleaner

## 3. `G_fp` / `G_cp` 的 index type 还会跟 `grid_type` 继续耦合

源码位置：`../warpx/Source/WarpX.cpp:2935-2948`。

```cpp
if (do_divb_cleaning)
{
    if (grid_type == GridType::Collocated)
    {
        m_fields.alloc_init(FieldType::G_cp,
            lev, amrex::convert(cba, IntVect::TheUnitVector()), dm,
            ncomps, ngG, 0.0_rt);
    }
    else
    {
        m_fields.alloc_init(FieldType::G_cp,
            lev, amrex::convert(cba, IntVect::TheZeroVector()), dm,
            ncomps, ngG, 0.0_rt);
    }
}
```

这说明清理场 `G` 的存在性虽然由 `do_divb_cleaning` 决定，但它的离散放置仍然继续受 `grid_type` 控制：

- collocated grid：`G` 走 node-centered
- staggered / hybrid：`G` 走 cell-centered

所以 `ReadParameters()` 里 grid 选择的影响，到这里仍然在继续传导。

## 4. external grid fields 和 external particle fields 是两套不同的分配合同

源码位置：`../warpx/Source/WarpX.cpp:2820-2891`。

```cpp
if (m_p_ext_field_params->B_ext_grid_type != ExternalFieldType::default_zero && m_p_ext_field_params->B_ext_grid_type != ExternalFieldType::constant) {
    m_fields.alloc_init(FieldType::Bfield_fp_external, ... m_fields.get(FieldType::Bfield_fp,...)->ixType());
}
...
if (mypc->m_B_ext_particle_s == "read_from_file") {
    auto *Bfield_aux_levl_0 = m_fields.get(FieldType::Bfield_aux, Direction{0}, lev);
    const int ncomp_ext_B = mypc->m_external_particle_fields_metadata.m_nBfields;
    m_fields.alloc_init(FieldType::B_external_particle_field, ... Bfield_aux_levl_0->ixType(), dm, ncomp_ext_B, ngEB, 0.0_rt);
}
```

这里必须区分两类“外场来自文件”：

1. `*_fp_external`
   - 目标是“加到网格主场上”
   - index type 必须匹配 `Efield_fp/Bfield_fp`
   - 后续由 `AddExternalFields()` 叠加到 fine-patch 主场
2. `*_external_particle_field`
   - 目标是“只给粒子看”
   - index type 必须匹配 `Efield_aux/Bfield_aux`
   - 分量数来自 `m_external_particle_fields_metadata`
   - 它不是主网格场的简单副本

所以 external particle field 不是“另一份 `fp_external`”。它跟 `aux` 的契约更紧，因为粒子 gather 看的就是 `aux` 路径，而不是 `fp` 本身。

## 5. `aux` 是否 alias 到 `fp`，会决定 external particle field 的 index type

源码位置：`../warpx/Source/WarpX.cpp:2720-2818`。

```cpp
if (aux_is_nodal and grid_type != GridType::Collocated)
{
    ... alloc nodal Efield_aux/Bfield_aux ...
} else if (lev == 0) {
    if (WarpX::fft_do_time_averaging) {
        ... alias aux -> avg_fp ...
    } else {
        if (mypc->m_B_ext_particle_s == "read_from_file") {
            ... alloc Bfield_aux ...
        } else {
            m_fields.alias_init(FieldType::Bfield_aux, FieldType::Bfield_fp, ...);
        }
        if (mypc->m_E_ext_particle_s == "read_from_file") {
            ... alloc Efield_aux ...
        } else {
            m_fields.alias_init(FieldType::Efield_aux, FieldType::Efield_fp, ...);
        }
    }
}
```

这里的关键点是：只要 external particle field 来自文件，`aux` 往往就不能再简单 alias 到 `fp`，而要单独分配。

原因很直接：

- 粒子看到的场必须允许再叠加一套粒子专属外场
- 这套场的 index type 必须和粒子 gather 使用的 `aux` 对齐

所以 external particle field 不只是“多分几块 `MultiFab`”，它还会把最常见的 `aux -> fp` alias 优化打断。

## 6. `HybridPICModel`、fluids、macroscopic medium 都是在 `AllocLevelMFs()` 里向对象图继续长出分支

源码位置：`../warpx/Source/WarpX.cpp:2530-2555`。

```cpp
if (WarpX::electromagnetic_solver_id == ElectromagneticSolverAlgo::HybridPIC)
{
    m_hybrid_pic_model->AllocateLevelMFs(...);
}

if (do_fluid_species) {
    myfl->AllocateLevelMFs(m_fields, ba, dm, lev);
    ...
    myfl->InitData(m_fields, geom[lev].Domain(), cur_time, lev, geom[lev], gamma_boost, beta_boost);
}

if (m_em_solver_medium == MediumForEM::Macroscopic) {
    WARPX_ALWAYS_ASSERT_WITH_MESSAGE( lev==0,
        "Macroscopic properties are not supported with mesh refinement.");
    m_macroscopic_properties->AllocateLevelMFs(ba, dm, ngEB);
}
```

这三条支线都不是构造函数里“一次性 new 出对象”就结束了。真正的场级状态扩张发生在 `AllocLevelMFs()`：

- `HybridPICModel`
  - 在每个 level 上再追加自己的场寄存器
  - 因此它不仅是 solver 选择，也是字段版图选择
- fluids
  - 先 `AllocateLevelMFs`
  - 再立刻 `InitData`
  - 说明 fluid 不是单纯占位容器，而是在 level 分配阶段就进入初始化主链
- macroscopic medium
  - 只能 `lev==0`
  - 直接把 mesh refinement 排除掉

因此这一层的本质不是“后面还有几个功能模块”，而是：

- `HybridPIC` 会扩展 field registry
- fluids 会在 level 分配阶段就写入初值
- macroscopic medium 会直接收紧 AMR 合法空间

## 7. `EB::enabled()` 会把普通 level 分配变成“level set + cut-cell metadata”分配

源码位置：`../warpx/Source/WarpX.cpp:2567-2641`。

```cpp
if (EB::enabled()) {
    m_fields.alloc_init(FieldType::distance_to_eb, lev, amrex::convert(ba, IntVect::TheNodeVector()), dm, nc_ls, ng_ls, 0.0_rt);
    AllocInitMultiFab(m_eb_reduce_particle_shape[lev], ...);

    if (lev == maxLevel()) {
        if (WarpX::electromagnetic_solver_id != ElectromagneticSolverAlgo::PSATD) {
            AllocInitMultiFab(m_eb_update_E[lev][0], ...);
            AllocInitMultiFab(m_eb_update_B[lev][0], ...);
            ...
        }
        if (WarpX::electromagnetic_solver_id == ElectromagneticSolverAlgo::ECT) {
            m_fields.alloc_init(FieldType::edge_lengths, ...);
            m_fields.alloc_init(FieldType::face_areas, ...);
            ...
            m_borrowing[lev][0] = std::make_unique<amrex::LayoutData<FaceInfoBox>>(...);
            ...
        }
    }
}
```

这里至少有三层递进：

1. 只要 EB 开启，所有 level 都会有：
   - `distance_to_eb`
   - `m_eb_reduce_particle_shape`
2. 只有 finest level 才额外持有：
   - `m_eb_update_E/B`
3. 只有 ECT solver 才进一步持有：
   - `edge_lengths`
   - `face_areas`
   - `area_mod`
   - `Venl`
   - `ECTRhofield`
   - `FaceInfoBox` 借用关系

所以 EB 不是一个单一分支，而是：

- runtime EB 开关
- finest-level 特例
- ECT solver 特例

三层条件叠加后的字段分配树。

## 8. 这些对象在 `InitData()` 里什么时候真正被消费

分配之后，fresh-run 初始化主链并不会等到 `Evolve()` 才第一次使用这些对象。

源码位置：`../warpx/Source/Initialization/WarpXInitData.cpp:848-890`。

```cpp
BuildBufferMasks();

if (m_em_solver_medium == MediumForEM::Macroscopic) {
    m_macroscopic_properties->InitData(...);
}

m_electrostatic_solver->InitData();

if (WarpX::electromagnetic_solver_id == ElectromagneticSolverAlgo::HybridPIC) {
    m_hybrid_pic_model->InitData(m_fields);
}

CheckGuardCells();

if (m_do_initial_div_cleaning) {
    WarpX::ProjectionCleanDivB();
}
```

这说明 `AllocLevelMFs()` 里长出来的很多支线，马上就会在 `InitData()` 后半段被消费：

- buffer masks 立即构建
- macroscopic medium 立即写入材料数据
- electrostatic solver 立即初始化自己的状态
- `HybridPICModel` 立即根据已分配字段做 `InitData`
- `ProjectionCleanDivB()` 立即消费外部 `B` 场与相关字段

因此 initialization 的真实结构不是：

1. 分配字段
2. 以后再说

而是：

1. `ReadParameters()` 选出对象图
2. `AllocLevelMFs()` 把特例字段全部摊开
3. `InitData()` 后半段立刻消费这些字段，把它们变成真实初态

## 9. 小结：`AllocLevelMFs()` 是“参数约束”到“可执行初态”的最后一跳

把这一层补上之后，可以更准确地理解初始化链：

- `ReadParameters()` 决定哪些物理-算法组合允许存在
- `AllocLevelMFs()` 决定这些组合具体长成哪组字段和辅助对象
- `InitData()` 后半段再立刻消费它们，构成：
  - electrostatic / hybrid / fluid / macroscopic / EB / external-field / divergence-cleaning
    各自的初始化分支

因此阅读顺序上，`ReadParameters()` 后面最该接的不是抽象说明，而正是 `AllocLevelMFs()` 这些看似琐碎的分配特例。因为它们才是“输入参数最后怎样变成一张可跑的状态图”的直接证据。
