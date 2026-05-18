# `free_electron_laser` 背后的真正主链：rigid injection、外加粒子场与 BTD

绑定源码：

- `../warpx/Source/Particles/RigidInjectedParticleContainer.H`
- `../warpx/Source/Particles/RigidInjectedParticleContainer.cpp`
- `../warpx/Source/Particles/MultiParticleContainer.cpp`
- `../warpx/Source/Diagnostics/BTDiagnostics.cpp`
- `../warpx/Source/Diagnostics/ParticleDiag/ParticleDiag.cpp`

代表性 examples / regressions：

- `../warpx/Examples/Physics_applications/free_electron_laser/inputs_test_1d_fel`
- `../warpx/Examples/Physics_applications/free_electron_laser/analysis_fel.py`
- `../warpx/Examples/Tests/rigid_injection/inputs_test_2d_rigid_injection_lab`
- `../warpx/Examples/Tests/rigid_injection/inputs_test_2d_rigid_injection_btd`
- `../warpx/Examples/Tests/rigid_injection/analysis_rigid_injection_lab.py`
- `../warpx/Examples/Tests/rigid_injection/analysis_rigid_injection_btd.py`
- `../warpx/Examples/Tests/boosted_diags/inputs_test_3d_laser_acceleration_btd`
- `../warpx/Examples/Tests/boosted_diags/analysis.py`

## 1. 这条链为什么不属于 `lasers.names`

`free_electron_laser` 没有走 `LaserProfiles` 和 `LaserParticleContainer`。它的输入主线是：

1. `particles.rigid_injected_species = electrons positrons`
2. `electrons/positrons.injection_style = gaussian_beam`
3. `electrons/positrons.zinject_plane = 0.0`
4. `electrons/positrons.rigid_advance = 0`
5. `particles.B_ext_particle_init_style = parse_B_ext_particle_function`
6. `particles.By_external_particle_function(x,y,z,t) = if( z>0, Bu*cos(k_u*z), 0 )`
7. diagnostics 里同时启用 boosted-frame 和 `BackTransformed`

因此这里的“辐射”不是人工天线输入，而是刚性束流进入 undulator 外磁场后，在 boosted frame 与 moving window 下自发增长的结果量。

## 2. `MultiParticleContainer` 如何切到 rigid-injected species

`MultiParticleContainer.cpp` 里，species 若出现在 `particles.rigid_injected_species`，就不会实例化普通 `PhysicalParticleContainer`，而是改成：

```cpp
particle_container = std::make_unique<RigidInjectedParticleContainer>(
    amr_core, i_s, species_names[i_s]);
```

同一个容器层还会读取：

```cpp
pp_particles.query("B_ext_particle_init_style", m_B_ext_particle_s);
```

因此，`free_electron_laser` 这条应用链的入口其实同时跨了两条基础设施：

- 粒子容器从普通 species 切到 `RigidInjectedParticleContainer`
- 粒子看到的背景场从主场 `E/Bfield_fp` 扩展到 external particle field

## 3. `RigidInjectedParticleContainer` 的真实合同

`RigidInjectedParticleContainer` 不是“延后生成粒子”的特殊 injector，而是“粒子已经存在，但在 `zinject_plane` 之前按刚体规则推进”的容器。

构造期直接读：

```cpp
utils::parser::getWithParser(pp_species_name, "zinject_plane", zinject_plane);
pp_species_name.query_enum_sloppy("rigid_advance", rigid_advance_mode, "-_");
```

其中 `rigid_advance` 有两类主要语义：

- `vzbar`：未注入区域按平均束流速度推进
- `vz`：未注入区域按各自粒子速度推进

WarpX 的布尔输入只是它们的简写：

- `true` -> `vzbar`
- `false` -> `vz`

`inputs_test_2d_rigid_injection_lab` 和 `inputs_test_2d_rigid_injection_btd` 都用：

```text
beam.rigid_advance = true
```

而 `free_electron_laser` 用的是：

```text
electrons.rigid_advance = 0
positrons.rigid_advance = 0
```

也就是更接近 `RigidAdvanceMode::vz`。

### 3.1 `test_1d_fel` 这条 regression 的真正硬断言

`Examples/Physics_applications/free_electron_laser/CMakeLists.txt` 不是只给这条应用留一个 checksum 名，而是同时绑定：

```cmake
add_warpx_test(
    test_1d_fel
    ...
    "analysis_fel.py diags/diag_labframe"
    "analysis_default_regression.py --path diags/diag_labframe"
)
```

`analysis_fel.py` 明确做两层强断言：

1. 在 `diag_labframe` 里对 `log(E_x^2)` 的线性增长区做拟合，要求 gain length 接近 `0.22 m`，相对误差小于 `15%`。
2. 分别在 lab-frame 与 boosted-frame diagnostics 上做 FFT，要求还原出的 radiation wavelength 满足 undulator 理论值，误差小于 `1%`。

因此 `test_1d_fel` 的意义不是“这个 example 能跑”，而是直接验证：

- rigid injected electron/positron 共流束抵消 space-charge 的建模合同；
- `particles.By_external_particle_function(...)` 给出的 undulator 外加粒子磁场；
- `BackTransformed` diagnostics 与 boosted-frame full diagnostics 对同一 FEL 标度的重建一致性。

## 4. 初始化阶段：先 boost `zinject_plane`，再加粒子

`InitData()` 的主线是：

```cpp
const Real zinject_plane_boost =
    zinject_plane/WarpX::gamma_boost - WarpX::beta_boost*c*t_boost;
zinject_plane_levels.resize(finestLevel()+1, zinject_plane_boost);

AddParticles(0);
RemapParticles();
Redistribute();
```

这里有两个关键点。

第一，`zinject_plane` 在容器内部保存的不是实验室位置，而是 boost 后、逐 level 保存的 `zinject_plane_levels`。

第二，粒子不是在 `zinject_plane` 到来时才创建。它们会先完整生成，再由 `RemapParticles()` 和后续 `Evolve()` 保证“注入面前方”和“注入面后方”服从不同推进规则。

## 5. `RemapParticles()` 和 `PushPX()` 真正在做什么

`RemapParticles()` 只在 `rigid_advance_mode == vzbar` 时做额外位置改写。它会：

1. 先估计 boost frame 下束流平均速度 `vzbeam_ave_boosted`
2. 回推出每个粒子在实验室系 `t=0` 时对应的 `z_lab`
3. 去掉各自真实速度带来的展宽
4. 改用平均束流速度重写 `z`

这一步的目标不是物理推进，而是把“尚未进入等离子体的束团”准备成刚体传播的参考态。

之后 `PushPX()` 会先调用基类 `PhysicalParticleContainer::PushPX(...)` 完整执行一次正常 gather/push：

```cpp
PhysicalParticleContainer::PushPX(... ScaleFields(do_scale, dt,
    zinject_plane_lev_previous, vzbeam_ave_boosted, v_boost), ...);
```

然后，对仍在 `zinject_plane` 前方的粒子撤销这次普通推进：

- 把 `x/y/z` 恢复成保存值
- 再按 `vzbar` 或 `vz` 规则只沿束流方向前移

因此 rigid injection 的真实实现不是“另外写一套 pusher”，而是：

1. 先正常 gather/push
2. 再对未注入粒子做条件性回滚和刚体式重写

## 6. boost 和 moving window 怎样共同移动注入面

在 `Evolve()` 里，每个 level 的注入面都会更新：

```cpp
zinject_plane_lev_previous = zinject_plane_levels[lev];
zinject_plane_levels[lev] -= dt*WarpX::beta_boost*PhysConst::c;
zinject_plane_lev = zinject_plane_levels[lev];
```

这说明至少在 boosted frame 下，`zinject_plane` 不是静止面，而是随 boost 速度在计算系里持续平移。

随后源码会根据：

```cpp
WarpX::moving_window_v + WarpX::beta_boost*PhysConst::c
```

判断某个 level 是否已经 `done_injecting_lev`。所以 rigid injection 的终止条件本来就是 boost 和 moving window 的联立结果，而不是单独看 `zinject_plane`。

## 7. `free_electron_laser` 中的 undulator 其实是 particle external field

FEL 输入里最关键的一行不是 laser profile，而是：

```text
particles.B_ext_particle_init_style = parse_B_ext_particle_function
particles.By_external_particle_function(x,y,z,t) = if( z>0, Bu*cos(k_u*z), 0 )
```

这意味着 undulator 场不是加到主场 `Bfield_fp` 上，而是通过粒子 gather 侧的 external particle field 接口直接提供给束流。

因此 `free_electron_laser` 的物理主链是：

1. 刚性束团在 boost frame 下推进
2. 粒子在 gather 时看到 `B_y(z)` 外磁场
3. 束团被 undulator 摆动并产生辐射
4. 辐射场再通过 boosted-frame diagnostics 和 BTD 被读出

## 8. BTD 在这里验证的不是“有没有输出文件”，而是 lab-frame 物理是否恢复正确

`analysis_fel.py` 的断言强度比 checksum 高得多。它在两套 diagnostics 上都做物理拟合：

1. lab-frame diagnostics：
   - 提取峰值辐射场随 `z` 的指数增长
   - 拟合 gain length
   - FFT 提取 radiation wavelength
2. boosted-frame diagnostics：
   - 先把 `Ex` 和 `By` Lorentz 变回实验室场
   - 再重复 gain length 和 wavelength 拟合

因此它在同时验证：

- rigid bunch + undulator 场的整体 FEL 标度
- boosted-frame 诊断恢复到 lab frame 后的物理一致性
- `BackTransformed` diagnostics 的时间空间重建合同

## 9. `rigid_injection` tests 在给哪一层做更基础的硬断言

`free_electron_laser` 太复杂，不适合单独定位 rigid injection 是否工作正常。更基础的硬断言来自 `Examples/Tests/rigid_injection/`。

### 9.1 `analysis_rigid_injection_lab.py`

它验证：

- 刚性传播到 `z0 = 20 um` 之前束宽不应按自由展宽演化
- 过了注入面之后，束宽应按理论
  $$
  w(z)=\sqrt{w_0^2 + (z-z_0)^2\theta_0^2}
  $$
  演化
- `gaussian_beam` runtime attributes 是否被正确初始化

因此这个 test 主要覆盖：

- `RigidInjectedParticleContainer`
- `gaussian_beam` 注入
- runtime attributes 保真

### 9.2 `analysis_rigid_injection_btd.py`

它在 boosted frame 下进一步验证两件事：

1. plotfile BTD 和 openPMD BTD 的粒子位置/动量必须逐项一致
2. back-transformed 到 lab frame 后的束宽仍应满足 rigid injection 理论

因此它比 `analysis_rigid_injection_lab.py` 多覆盖了一层：

- `BackTransformed` diagnostics 对粒子数据的格式一致性与物理一致性

## 10. `boosted_diags` 在这条链上扮演什么 supporting role

`Examples/Tests/boosted_diags/analysis.py` 本身不是 rigid injection 测试。它主要验证：

- plotfile BTD 与 openPMD BTD 的场数据一致
- `diag2.beam.random_fraction = 0.5` 的粒子子采样是否真的生效

也就是说，它为 `free_electron_laser` 和 `rigid_injection_btd` 提供的是一层更通用的 supporting evidence：

- BTD 两种 writer 的一致性
- `ParticleDiag` / writer 侧 `random_fraction` 过滤合同

它不能替代 `analysis_fel.py` 或 `analysis_rigid_injection_btd.py`，但能证明 BTD 基础设施本身不是黑箱。

## 11. 这条链在书稿里的更合理归位

从实现上看，`free_electron_laser` 不应继续被写成“laser 注入例子”。更合理的归位是：

1. `Laser/` 章节只负责说明为什么它不走 `lasers.names`
2. 粒子章节负责：
   - `RigidInjectedParticleContainer`
   - runtime attributes
   - external particle field gather
3. diagnostics / boosted-frame 章节负责：
   - BTD particle/field consistency
   - plotfile vs openPMD consistency
   - random particle subsampling

因此，FEL 这条链真正串起来的是：

- 注入策略
- 粒子看到的背景场
- boosted diagnostics

而不是 Laser antenna 本体。
