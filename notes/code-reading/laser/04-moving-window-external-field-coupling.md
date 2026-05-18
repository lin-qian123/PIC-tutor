# Laser、moving window 与 external fields 的运行时耦合

绑定源码：

- `../warpx/Source/Utils/WarpXMovingWindow.cpp`
- `../warpx/Source/Particles/LaserParticleContainer.cpp`
- `../warpx/Source/Particles/ParticleCreation/AddParticles.cpp`
- `../warpx/Source/Initialization/ExternalField.cpp`
- `../warpx/Source/Initialization/WarpXInitData.cpp`

这一篇不再重复 laser profile 公式，而是回答一个更容易在源码阅读里断开的运行时问题：

1. moving window 开始移动后，普通 species 的连续注入平面和 laser antenna 分别怎样更新。
2. 为什么 parser/constant 网格外场能跟着 moving window 走，而 `read_from_file` 外场被直接禁止。
3. AMR / finest-spacing / boosted-frame 在这条链里怎样分别作用到 species 和 laser。

## 1. `MoveWindow()` 同时维护三类“随窗口前进的对象”

`WarpX::MoveWindow()` 在真正平移网格前，先更新三类连续变量：

```cpp
moving_window_x += (moving_window_v - WarpX::beta_boost * PhysConst::c)/(1 - moving_window_v * WarpX::beta_boost / PhysConst::c) * dt[0];
::UpdateInjectionPosition(*mypc, gamma_boost, beta_boost, boost_direction, moving_window_dir, dt[0]);
mypc->UpdateAntennaPosition(dt[0]);
```

这里的三项含义不同：

1. `moving_window_x` 是窗口几何本身的连续位置。
2. `UpdateInjectionPosition(...)` 更新普通 species 的 `m_current_injection_position`。
3. `UpdateAntennaPosition(dt)` 更新 laser antenna 的 `m_updated_position`。

也就是说，在 WarpX 里，“moving window 在动”并不等于“所有需要注入的对象都只看一个统一的前沿坐标”。species 和 laser 各自维护自己的运行态注入位置。

## 2. 普通 species 的连续注入位置来自 `PlasmaInjector` 的 bulk momentum

`WarpXMovingWindow.cpp` 里的 `UpdateInjectionPosition(...)` 会遍历所有 container，但真正能从中提取“注入速度”的只有有 `PlasmaInjector` 的物理粒子 species：

```cpp
PlasmaInjector* plasma_injector = pc.GetPlasmaInjector(0);
...
const amrex::XDim3 u_bulk = plasma_injector->getInjectorMomentumHost()->getBulkMomentum(
    current_injection_position[0],
    current_injection_position[1],
    current_injection_position[2]);
...
v_shift = PhysConst::c * u_bulk_vec[dir] / std::sqrt(1._rt + u_bulk_vec[dir]*u_bulk_vec[dir]);
```

因此这里更新的不是“窗口速度”，而是：

1. 先在当前注入面上查询 injector 的 bulk momentum；
2. 再转成该方向上的 bulk velocity；
3. 最后把这个速度积分成新的 `m_current_injection_position`。

如果启用了 boosted frame，这个速度还会继续做一次洛伦兹速度变换：

```cpp
v_shift = (v_shift - PhysConst::c*beta_boost)
        / (1._rt - v_shift*beta_boost/PhysConst::c);
```

所以普通 species 的连续注入位置是“流体/束流本身在 boosted frame 中应当处于哪里”的结果，而不是简单地跟着 `moving_window_v` 机械平移。

## 3. laser antenna 的更新规则不同：只看 boost，不看 `PlasmaInjector`

laser 容器没有 `PlasmaInjector`。它在 moving-window 期间的运行态更新入口是：

```cpp
void
LaserParticleContainer::UpdateAntennaPosition (const amrex::Real dt)
{
    if (do_continuous_injection and (WarpX::gamma_boost > 1)){
        ...
        m_updated_position[...] -= WarpX::beta_boost *
            WarpX::boost_direction[...] * PhysConst::c * dt;
    }
}
```

这说明 laser antenna 的 `m_updated_position` 只在：

- `do_continuous_injection = 1`
- `gamma_boost > 1`

时才会被单独推进，并且推进量只来自 boost velocity，而不是来自某个 profile-dependent 传播速度。

原因是：

1. laser profile 的传播方向在构造期已经被约束成和 moving window 方向一致；
2. boosted-frame 下，天线平面本身相对仿真坐标系在漂移；
3. 这个漂移只需要由 boost kinematics 给出，不需要再查询 `PlasmaInjector` 那一套 bulk momentum 接口。

因此普通 species 和 laser 在 moving-window 阶段虽然都叫 continuous injection，但它们维护运行态位置的机制根本不同。

## 4. `ContinuousInjection()` 的语义也不一样

### 4.1 普通 species：每次给新 cells 生成新的物理粒子

物理粒子的 runtime 注入是：

```cpp
void
PhysicalParticleContainer::ContinuousInjection (const amrex::RealBox& injection_box)
{
    const int lev=0;
    for (auto const& plasma_injector : plasma_injectors) {
        AddPlasma(*plasma_injector, lev, injection_box);
    }
}
```

在 `MoveWindow()` 中，WarpX 会先把连续注入位置 snap 到整数个 cell：

```cpp
new_injection_position = pc.m_current_injection_position +
    std::floor( (geom[lev].ProbHi(dir) - pc.m_current_injection_position)/dx ) * dx;
```

然后用这段新出现的 `particleBox` 调用 `pc.ContinuousInjection(particleBox)`。

所以普通 species 的 continuous injection 合同是：

1. 只在 level 0 上发生；
2. 只给 moving window 新扫进来的整 cell 区间补粒子；
3. 每次都会重新调用 `AddPlasma(...)`。

### 4.2 laser：只在 antenna 首次进入当前注入盒时生成人工天线粒子

laser 的 runtime 注入则完全不同：

```cpp
if (is_contained)
{
    m_laser_injection_box = injection_box;
    InitData();
}
```

`LaserParticleContainer::ContinuousInjection()` 不会每步重建整束激光。它只做一件事：

- 当 `m_updated_position` 第一次进入当前 `injection_box` 时，调用一次 `InitData()`。

之后激光的演化靠的是已有人工天线粒子在 `Evolve()` 中反复：

1. 计算平面坐标；
2. 更新 profile；
3. 更新人工粒子；
4. `DepositCurrent()` / `DepositCharge()`。

因此：

- 普通 species 的 continuous injection 是“不断生成新的物理粒子流”；
- laser 的 continuous injection 是“决定天线何时进入域并开始发射”。

## 5. AMR 下，species 和 laser 使用不同的空间尺度

这一点在 moving-window 场景下尤其容易混淆。

普通 species 的 runtime 注入盒是：

- level 0 的 `particleBox`
- 按 level 0 的 `dx` 向下取整
- 后续再由 AMR、`refine_plasma`、buffer masks、coarse-fine deposition 路径去消费

laser 则不是按 level 0 spacing 建粒子。`LaserParticleContainer::InitData()` 会直接：

```cpp
InitData(maxLevel());
...
ComputeSpacing(lev, S_X, S_Y);
```

也就是说，天线粒子 spacing 总是按 finest level 计算，即使 continuous injection 的触发盒来自 moving window 的新进入区域。

这就是为什么：

1. `refine_plasma=1` 影响的是普通物理粒子注入与沉积均匀性；
2. laser antenna 一旦进入域内，直接按 finest-cell spacing 发射；
3. 两者虽然都和 moving window 有关，但 AMR 作用点不同。

## 6. moving window 如何处理外场：constant/parser 可平移，`read_from_file` 不可

`LoadExternalFields()` 在初始化阶段就明确禁止：

```cpp
WARPX_ALWAYS_ASSERT_WITH_MESSAGE(
    WarpX::do_moving_window == 0,
    "External fields from file are not compatible with the moving window." );
```

禁止条件包括四类：

1. `B_ext_grid_type == read_from_file`
2. `E_ext_grid_type == read_from_file`
3. `mypc->m_B_ext_particle_s == "read_from_file"`
4. `mypc->m_E_ext_particle_s == "read_from_file"`

原因不在于 openPMD 不能读，而在于 moving window 需要在每次平移后给“新进入的网格区域”重新赋值。

这个动作在 `shiftMF(...)` 里只支持两种重填方式：

```cpp
if (!useparser) {
    srcfab(i,j,k,n) = external_field;
} else {
    srcfab(i,j,k,n) = field_parser(x,y,z);
}
```

也就是说，新进入的 cells 只能用：

1. 常量 `external_field`
2. 解析函数 `field_parser(x,y,z)`

来重建。`read_from_file` 路径没有提供“窗口每推进一次，就把新的 physical coordinates 映射到文件并增量重读”的实现，所以只能直接禁用。

## 7. moving window 真正平移的是“主场”，不是 `*_fp_external`

在 `MoveWindow()` 中，WarpX 平移的是：

- `Bfield_fp / Efield_fp`
- `Bfield_cp / Efield_cp`
- `Bfield_aux / Efield_aux`
- `current_fp/current_cp`
- `rho_fp/rho_cp`
- `F/G`
- fluids
- PML / averaged fields

并且 `E/Bfield_fp` 新进入区域的默认值由外场常量或 parser 给出：

```cpp
::shiftMF(*m_fields.get(FieldType::Bfield_fp, Direction{dim}, lev), ..., 
    m_p_ext_field_params->B_external_grid[dim], use_Bparser, Bfield_parser);
::shiftMF(*m_fields.get(FieldType::Efield_fp, Direction{dim}, lev), ..., 
    m_p_ext_field_params->E_external_grid[dim], use_Eparser, Efield_parser);
```

这说明 moving-window 阶段真正被维护的是“已经加到主场合同里的外场背景”，而不是单独把 `Bfield_fp_external/Efield_fp_external` 作为一份独立、可随窗口更新的 registry 再平移一次。

因此 constant/parser 外场之所以兼容 moving window，本质上是因为它们能够在主场的新边界区被重新生成。

## 8. 这条链如何落到 examples / regressions

当前最贴近这条交界合同的本地例子是：

1. `Examples/Physics_applications/laser_acceleration/inputs_test_2d_laser_acceleration_boosted`
   - moving window
   - boosted frame
   - plasma species `do_continuous_injection = 1`
   - laser antenna
   - 当前主要依赖 checksum
2. `Examples/Physics_applications/laser_acceleration/inputs_test_2d_refined_injection`
   - `refine_plasma = 1`
   - `analysis_refined_injection.py`
   - 直接验证 moving-window 连续注入在 refinement edge 附近的粒子数与 `rho` 均匀性
3. `Examples/Tests/subcycling/inputs_test_2d_subcycling_mr`
   - moving window
   - MR + subcycling
   - 连续注入的 plasma species
   - 当前主要仍是 checksum 基线
4. `Examples/Tests/load_external_field/*`
   - 这些 tests 验证 grid/particle external field 的加载和消费
   - 但它们默认都是静态窗口场景，正好对应源码里 “`read_from_file` 与 moving window 不兼容” 的实现边界

## 9. 对当前书稿最重要的结论

这条运行态交界可以压成四条简洁结论：

1. 普通 species 和 laser 都支持 continuous injection，但两者维护运行态位置的逻辑不同。
2. species 的新粒子是在新 cells 中反复生成的；laser 只是等天线进入域内后生成一次人工发射粒子。
3. AMR 下普通 species 的移动窗口注入按 level 0 cell 对齐，而 laser antenna spacing 直接按 finest level 建立。
4. moving window 只能和 constant/parser 外场兼容，因为它要求能在新进入网格区即时重建背景场；`read_from_file` 缺少这条增量重建合同，所以被显式禁用。
