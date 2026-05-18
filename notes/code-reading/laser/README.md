# Laser 源码精读入口

绑定源码：`../warpx/Source/Laser`。

## 模块边界

- 构建入口：`Laser/CMakeLists.txt`、`Laser/Make.package`。
- 主要文件：`LaserProfiles.H`、`LaserProfilesImpl/LaserProfileGaussian.cpp`、`LaserProfileFromFile.cpp`、`LaserProfileFieldFunction.cpp`。
- 关联模块：`Particles/LaserParticleContainer.*`、field boundary/injection。

## 核心问题

- laser profile 如何从参数、文件或函数定义。
- Gaussian laser、field function laser、from-file laser 如何映射到边界注入或粒子容器。
- laser 与 moving window、boosted frame、diagnostics 的关系。

## 精读顺序

1. `LaserProfiles.H` 类型和公共接口。
2. `LaserProfileGaussian.cpp`。
3. `LaserProfileFromFile.cpp`。
4. `LaserProfileFieldFunction.cpp`。
5. `Particles/LaserParticleContainer.*`。

## 输出目标

- `00-laser-profile-dispatch.md`
- `01-gaussian-from-file-and-runtime.md`
- `02-field-function-and-particle-update-kernel.md`
- `03-laser-validation-map.md`
- `04-moving-window-external-field-coupling.md`
- `05-application-and-diagnostic-cases.md`
- `06-rigid-injection-btd-and-undulator-coupling.md`
- `07-laser-ion-multiphysics-switches.md`

## 当前进度

- 已完成 `00-laser-profile-dispatch.md`：梳理 `ILaserProfile` 合同、`laser_profiles_dictionary` 的 `gaussian / parse_field_function / from_file` 分派、`CommonLaserParameters` 与 `LaserParticleContainer` 构造期的公共参数归一化、`e_max` / `a0` 二选一约束、boosted-frame 与 moving-window continuous-injection 几何前提，以及人工天线粒子和普通物理粒子容器的职责差异。
- 已完成 `01-gaussian-from-file-and-runtime.md`：梳理 `GaussianLaserProfile` 的 diffraction / chirp / STC 复包络、`FromFileLaserProfile` 的 `lasy/binary` 独占后端、`time_chunk_size` / `delay` / 时间块流式读取，以及 `LaserParticleContainer::InitData()` / `Evolve()` / `ContinuousInjection()` 如何把 profile 振幅变成人工天线粒子并通过 `J/rho` 沉积写入 Maxwell 求解器。
- 已完成 `02-field-function-and-particle-update-kernel.md`：梳理 `FieldFunctionLaserProfile` 如何把 `field_function(X,Y,t)` 直接编译成 parser、`calculate_laser_plane_coordinates()` 如何把真实粒子位置投回激光平面、`ComputeWeightMobility()` 如何先约束天线粒子峰值速度再反推权重、`update_laser_particle()` 如何把目标场值变成显式/隐式一致的动量与位置更新，以及当前 `parse_field_function` 的 regression 主要嵌在 `particle_absorbing_boundary` 场景中的事实边界。
- 已完成 `03-laser-validation-map.md`：梳理 `laser_injection`、implicit laser injection、`laser_injection_from_file`、`laser_acceleration`、RZ openPMD、BTD 与 Python callback 相关条目各自在验证什么，明确哪些有 envelope/frequency 或理论/格式断言，哪些主要仍依赖 checksum。
- 已完成 `04-moving-window-external-field-coupling.md`：梳理 `WarpX::MoveWindow()` 如何分别更新普通 species 的 `m_current_injection_position` 和 laser antenna 的 `m_updated_position`，为什么 species 与 laser 的 `ContinuousInjection()` 语义不同、AMR 下两者分别按 level-0 cell 与 finest spacing 起作用，以及为什么 constant/parser 外场能随 moving window 重建而 `read_from_file` 外场被源码显式禁止。
- 已完成 `05-application-and-diagnostic-cases.md`：梳理 `laser_ion` 如何把 Gaussian laser 主链接到 full/time-averaged/reduced diagnostics 组合、`free_electron_laser` 如何通过 rigid bunch + external particle field + BTD 生成辐射，以及 `laser_on_fine` 为什么更像 AMR placement checksum test 而不是应用 physics regression。
- 已完成 `06-rigid-injection-btd-and-undulator-coupling.md`：梳理 `free_electron_laser` 背后真正起作用的不是 `lasers.names`，而是 `RigidInjectedParticleContainer`、`particles.B_ext_particle_init_style = parse_B_ext_particle_function` 和 `BackTransformed` diagnostics 的组合；并用 `rigid_injection` 与 `boosted_diags` tests 把 rigid propagation、BTD plotfile/openPMD 一致性、`random_fraction` 子采样和 FEL gain-length / wavelength 断言分层拆开。
- 已完成 `07-laser-ion-multiphysics-switches.md`：梳理 `laser_ion` 当前真正激活的是 laser + 预电离 target + diagnostics，而 field ionization、collisions 与 QED 只是输入层的可选分叉；并把 `do_field_ionization -> InitIonizationModule -> mapSpeciesProduct -> doFieldIonization -> ionizationLevel 沉积`、`collision_names -> CollisionHandler -> split_momentum_push` 和 `QED runtime attributes -> InitQED` 三条接入链，以及对应的独立 regression 证据分开写清。
- 2026-05-17 审计结论：`Source/Laser/` 当前源码树只包含 `LaserProfiles.H` 与三类 `LaserProfilesImpl/*`，它们连同 `Particles/LaserParticleContainer.*`、`Utils/WarpXMovingWindow.cpp`、`Initialization/ExternalField.*` 的 laser 侧耦合，已经分别被 `00-07` 八篇笔记覆盖；因此项目级 `TODO.md` 中把 `Laser/` 和 `ExternalField.* / WarpXMovingWindow.cpp` 列为未完成主线已不再符合当前工作树状态。

## 验证线索

- `Examples/Tests/laser_injection/`
- `Examples/Tests/laser_injection_from_file/`
- `Examples/Tests/particle_absorbing_boundary/`
- `Examples/Physics_applications/laser_acceleration/`
- `Examples/Physics_applications/laser_ion/`
