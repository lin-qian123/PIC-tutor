# GaussianBeam 与 openPMD 粒子文件注入精读

绑定源码：`../warpx`，分支 `pkuHEDPbranch`，commit `063f8b586f04321e13150ae3e730e0794ca75cb1`。

本笔记补齐 `04-particle-creation-kernels.md` 中没有展开的两条初始化边缘路径：

- `injection_style = gaussian_beam`：在 IO rank 上按高斯空间分布生成束流宏粒子，再通过 `AddNParticles()` 注入粒子容器。
- `injection_style = external_file`：从 openPMD 文件读取粒子 position/momentum/weighting/mass/charge，再通过 `AddNParticles()` 注入粒子容器。

这两条路径和 `AddPlasma()` 的核心差别是：它们不在每个 cell 内按 `InjectorDensity` 生成候选粒子，而是先得到显式粒子列表，再调用 `AddNParticles()`。

## 1. 官方参数边界

官方文档位置：`../warpx/Docs/source/usage/parameters.rst:1418-1494`。

```rst
* ``gaussian_beam``: Inject particle beam with gaussian distribution in
  space in all directions. This requires additional parameters:

  * ``<species_name>.q_tot`` (beam charge),

  * ``<species_name>.npart_real`` (total number of real particles in the beam)

  The user must define one and only only between ``q_tot`` and ``npart_real``.
  The latter must be used for neutral species.

  * ``<species_name>.npart`` (number of macroparticles in the beam),

  * ``<species_name>.x/y/z_m`` (average position in ``x/y/z``),

  * ``<species_name>.x/y/z_rms`` (standard deviation in ``x/y/z``),
```

Gaussian beam 是直接采样束流相空间，而不是通过 cell density profile 体注入。文档还定义了 cut、symmetrization、focal distance 和 rotation。

外部文件注入：

```rst
* ``external_file``: Inject macroparticles with properties (mass, charge, position, and momentum - :math:`\gamma \beta m c`) read from an external openPMD file.
  With it users can specify the additional arguments:

  * ``<species_name>.injection_file`` (``string``) openPMD file name and

  * :pp:param:`<species_name>.charge` (``double``) optional (default is read from openPMD file) when set this will be the charge of the physical particle represented by the injected macroparticles.

  * :pp:param:`<species_name>.mass` (``double``) optional (default is read from openPMD file) when set this will be the charge of the physical particle represented by the injected macroparticles.

  * ``<species_name>.z_shift`` (``double``) optional (default is no shift) when set this value will be added to the longitudinal, ``z``, position of the particles.

  * ``<species_name>.impose_t_lab_from_file`` (``bool``) optional (default is false) only read if warpx.gamma_boost > 1., it allows to set t_lab for the Lorentz Transform as being the time stored in the openPMD file.
```

文档明确 warning：`external_file` 下 `q_tot` 不支持重标定，文件中的 `weighting` 才是权重来源。

## 2. `PlasmaInjector` 构造期分派

源码位置：`../warpx/Source/Initialization/PlasmaInjector.cpp:126-153`。

```cpp
    std::string injection_style = "none";
    utils::parser::query(pp_species, source_name, "injection_style", injection_style);
    std::transform(injection_style.begin(),
                   injection_style.end(),
                   injection_style.begin(),
                   ::tolower);

    num_particles_per_cell_each_dim.assign(3, 0);

    if (injection_style == "singleparticle") {
        setupSingleParticle(pp_species);
        return;
    } else if (injection_style == "multipleparticles") {
        setupMultipleParticles(pp_species);
        return;
    } else if (injection_style == "gaussian_beam") {
        setupGaussianBeam(pp_species);
    } else if (injection_style == "nrandompercell") {
        setupNRandomPerCell(pp_species);
    } else if (injection_style == "nfluxpercell") {
        setupNFluxPerCell(pp_species);
    } else if (injection_style == "nuniformpercell") {
        setupNuniformPerCell(pp_species);
    } else if (injection_style == "external_file") {
        setupExternalFile(pp_species);
    } else if (injection_style != "none") {
        SpeciesUtils::StringParseAbortMessage("Injection style", injection_style);
    }
```

构造期只设置 flag 和读取参数：

- `gaussian_beam` 走 `setupGaussianBeam()`；
- `external_file` 走 `setupExternalFile()`；
- 真正创建粒子仍发生在 `PhysicalParticleContainer::AddParticles()`。

## 3. Gaussian beam 参数解析

源码位置：`../warpx/Source/Initialization/PlasmaInjector.cpp:229-299`。

```cpp
void PlasmaInjector::setupGaussianBeam (amrex::ParmParse const& pp_species)
{
    utils::parser::getWithParser(pp_species, source_name, "x_m", x_m);
    utils::parser::getWithParser(pp_species, source_name, "y_m", y_m);
    utils::parser::getWithParser(pp_species, source_name, "z_m", z_m);
    utils::parser::getWithParser(pp_species, source_name, "x_rms", x_rms);
    utils::parser::getWithParser(pp_species, source_name, "y_rms", y_rms);
    utils::parser::getWithParser(pp_species, source_name, "z_rms", z_rms);
    utils::parser::queryWithParser(pp_species, source_name, "x_cut", x_cut);
    utils::parser::queryWithParser(pp_species, source_name, "y_cut", y_cut);
    utils::parser::queryWithParser(pp_species, source_name, "z_cut", z_cut);

    const bool q_tot_is_specified = pp_species.contains("q_tot");
    const bool N_tot_is_specified = pp_species.contains("npart_real");
    WARPX_ALWAYS_ASSERT_WITH_MESSAGE( q_tot_is_specified != N_tot_is_specified,
        "Error: Exactly one between q_tot and npart_real have to be specified.");
```

`q_tot` 和 `npart_real` 二选一：

- charged species 常用 `q_tot`，权重通过 `q_tot/(npart*charge)` 得到；
- neutral species 必须用 `npart_real`，因为 `charge=0` 时无法通过总电荷反推真实粒子数。

后续读取宏粒子数、对称化、聚焦和旋转：

```cpp
    utils::parser::getWithParser(pp_species, source_name, "npart", npart);
    utils::parser::queryWithParser(pp_species, source_name, "do_symmetrize", do_symmetrize);
    utils::parser::queryWithParser(pp_species, source_name, "symmetrization_order", symmetrization_order);
    const bool focusing_is_specified = pp_species.contains("focal_distance");
    utils::parser::queryWithParser(pp_species, source_name, "do_gaussian_beam_rotation", do_rotation);
    utils::parser::queryWithParser(pp_species, source_name, "do_gaussian_beam_rotation_momenta", do_rotation_momenta);

    if(do_rotation){
        utils::parser::queryWithParser(pp_species, source_name, "gaussian_beam_rotation_angle", rotation_angle);
        utils::parser::getArrWithParser(pp_species, source_name, "gaussian_beam_rotation_axis", rotation_axis, 0, 3);
    }

    if(focusing_is_specified){
        do_focusing = true;
        utils::parser::queryWithParser(pp_species, source_name, "focal_distance", focal_distance);
    }
```

最后把动量分布交给 `SpeciesUtils::parseMomentum()`：

```cpp
    gaussian_beam = true;
    SpeciesUtils::parseMomentum(species_name, source_name, "gaussian_beam", h_inj_mom,
                                ux_parser, uy_parser, uz_parser,
                                ux_th_parser, uy_th_parser, uz_th_parser,
                                h_mom_temp, h_mom_vel);
```

这说明 Gaussian beam 的空间分布由 `AddGaussianBeam()` 自己采样，动量分布仍复用 `InjectorMomentum` 体系。

## 4. Gaussian beam 权重和截断

源码位置：`../warpx/Source/Particles/ParticleCreation/AddParticles.cpp:366-434`。

```cpp
void
PhysicalParticleContainer::AddGaussianBeam (PlasmaInjector const& plasma_injector){

    const amrex::Real x_m = plasma_injector.x_m;
    const amrex::Real y_m = plasma_injector.y_m;
    const amrex::Real z_m = plasma_injector.z_m;
    const amrex::Real x_rms = plasma_injector.x_rms;
    const amrex::Real y_rms = plasma_injector.y_rms;
    const amrex::Real z_rms = plasma_injector.z_rms;
    const amrex::Real x_cut = plasma_injector.x_cut;
    const amrex::Real y_cut = plasma_injector.y_cut;
    const amrex::Real z_cut = plasma_injector.z_cut;
    const amrex::Real q_tot = plasma_injector.q_tot;
    const amrex::Real N_tot = plasma_injector.N_tot;
    long npart = plasma_injector.npart;
```

这条路径先把参数复制到局部变量，然后在 host vector 中累积粒子数据。当前实现只在 IO processor 生成束流：

```cpp
    if (ParallelDescriptor::IOProcessor()) {
        // If do_symmetrize, create either 4x or 8x fewer particles, and
        // Replicate each particle either 4 times (x,y) (-x,y) (x,-y) (-x,-y)
        // or 8 times, additionally (y,x), (-y,x), (y,-x), (-y,-x)
        if (do_symmetrize){
            npart /= symmetrization_order;
        }
        // compute the weight from N_tot if the user specified npart_real = N_tot
        // compute the weight from q_tot if the user specified q_tot
        // note that npart is the number of macroparticles
        const amrex::Real weight_3d = (N_tot > 0._rt) ? (N_tot / npart) : (q_tot / (npart*charge));
```

权重公式是：

$$
w_{3d} =
\begin{cases}
N_{\mathrm{tot}}/N_p, & \text{if } N_{\mathrm{tot}}>0,\\
Q_{\mathrm{tot}}/(N_p q), & \text{otherwise}.
\end{cases}
$$

这里 `N_p` 是宏粒子数。随后按维度把 3D 权重折算到低维模型。例如 XZ 中除以 `y_rms`，1D 中除以 `x_rms*y_rms`：

```cpp
#if defined(WARPX_DIM_3D) || defined(WARPX_DIM_RZ)
            const amrex::Real weight = weight_3d;
            amrex::Real x = amrex::RandomNormal(x_m, x_rms);
            amrex::Real y = amrex::RandomNormal(y_m, y_rms);
            amrex::Real z = amrex::RandomNormal(z_m, z_rms);
#elif defined(WARPX_DIM_XZ)
            const amrex::Real weight = weight_3d/y_rms;
            amrex::Real x = amrex::RandomNormal(x_m, x_rms);
            constexpr amrex::Real y = 0._prt;
            amrex::Real z = amrex::RandomNormal(z_m, z_rms);
```

这不是从真实 3D 束流严格积分得到的全部信息，而是 WarpX 对低维模型中“每单位缺失维度长度/面积”的权重约定。

cut 和 bounds 检查：

```cpp
            if (plasma_injector.insideBounds(x, y, z)  &&
                std::abs( x - x_m ) <= x_cut * x_rms     &&
                std::abs( y - y_m ) <= y_cut * y_rms     &&
                std::abs( z - z_m ) <= z_cut * z_rms   ) {
                XDim3 u = plasma_injector.getMomentum(x, y, z);
```

重要细节：`q_tot` 是未 cut 束流的总电荷；如果 cut 去掉尾部粒子，实际注入总电荷会小于输入 `q_tot`。官方文档也明确提示了这一点。

## 5. 聚焦：从焦平面束斑反推初始横向位置

源码位置：`../warpx/Source/Particles/ParticleCreation/AddParticles.cpp:435-471`。

```cpp
            if (plasma_injector.do_focusing){
                const XDim3 u_bulk = plasma_injector.getInjectorMomentumHost()->getBulkMomentum(x,y,z);
                const amrex::Real u_bulk_norm = std::sqrt( u_bulk.x*u_bulk.x+u_bulk.y*u_bulk.y+u_bulk.z*u_bulk.z );

                // Compute the position of the focal plane
                // (it is located at a distance `focal_distance` from the beam centroid, in the direction of the bulk velocity)
                const amrex::Real n_x = u_bulk.x/u_bulk_norm;
                const amrex::Real n_y = u_bulk.y/u_bulk_norm;
                const amrex::Real n_z = u_bulk.z/u_bulk_norm;
                const amrex::Real x_f = x_m + focal_distance * n_x;
                const amrex::Real y_f = y_m + focal_distance * n_y;
                const amrex::Real z_f = z_m + focal_distance * n_z;
                const amrex::Real gamma = std::sqrt( 1._rt + (u.x*u.x+u.y*u.y+u.z*u.z) );
```

`focal_distance` 的含义不是“把粒子直接放到焦平面”，而是用户给的 `x_rms/y_rms/z_rms` 被解释为焦平面束斑。代码先按这个分布采样，然后根据粒子速度反推到初始化面。

```cpp
                const amrex::Real v_x = u.x / gamma * PhysConst::c;
                const amrex::Real v_y = u.y / gamma * PhysConst::c;
                const amrex::Real v_z = u.z / gamma * PhysConst::c;

                // Compute the time at which the particle will cross the focal plane
                const amrex::Real v_dot_n = v_x * n_x + v_y * n_y + v_z * n_z;
                const amrex::Real t = ((x_f-x)*n_x + (y_f-y)*n_y + (z_f-z)*n_z) / v_dot_n;

                // Displace particles in the direction orthogonal to the beam bulk momentum
                // i.e. orthogonal to (n_x, n_y, n_z)
#if defined(WARPX_DIM_3D) || defined(WARPX_DIM_RZ)
                x = x - (v_x - v_dot_n*n_x) * t;
                y = y - (v_y - v_dot_n*n_y) * t;
                z = z - (v_z - v_dot_n*n_z) * t;
```

数学上，令束流平均方向为单位向量 `n`，速度分解为

$$
\mathbf{v} = v_\parallel \mathbf{n} + \mathbf{v}_\perp.
$$

粒子到达焦平面的时间为

$$
t = \frac{(\mathbf{x}_f-\mathbf{x})\cdot\mathbf{n}}{\mathbf{v}\cdot\mathbf{n}}.
$$

代码用 `x <- x - v_perp t` 把焦平面横向位置反推到初始化面。这里忽略 space charge 和外场作用，是弹道近似。

## 6. 旋转：位置和动量使用 Rodrigues 公式

源码位置：`../warpx/Source/Particles/ParticleCreation/AddParticles.cpp:472-517`。

```cpp
#if defined(WARPX_DIM_3D) || defined(WARPX_DIM_XZ)
            if (plasma_injector.do_rotation){

                    // normalize the rotation axis
                    const Real k_norm = std::sqrt(rotation_axis[0]*rotation_axis[0] + rotation_axis[1]*rotation_axis[1] + rotation_axis[2]*rotation_axis[2]);
                    const Real kx = rotation_axis[0]/k_norm;
                    const Real ky = rotation_axis[1]/k_norm;
                    const Real kz = rotation_axis[2]/k_norm;

                    // compute rotated vector:
                    // v_rot = v * cos + (k x v) sin + k (k * v) (1 - cos)
```

位置旋转围绕束流 centroid：

```cpp
#if defined(WARPX_DIM_3D)
                    x = x_m + (x-x_m)*std::cos(rotation_angle) + k_cross_x*std::sin(rotation_angle) + kx*k_dot_x*(1._rt - std::cos(rotation_angle));
                    y = y_m + (y-y_m)*std::cos(rotation_angle) + k_cross_y*std::sin(rotation_angle) + ky*k_dot_x*(1._rt - std::cos(rotation_angle));
                    z = z_m + (z-z_m)*std::cos(rotation_angle) + k_cross_z*std::sin(rotation_angle) + kz*k_dot_x*(1._rt - std::cos(rotation_angle));
#elif defined(WARPX_DIM_XZ)
                    x = x_m + (x-x_m)*std::cos(rotation_angle) + k_cross_x*std::sin(rotation_angle) + kx*k_dot_x*(1._rt - std::cos(rotation_angle));
                    z = z_m + (z-z_m)*std::cos(rotation_angle) + k_cross_z*std::sin(rotation_angle) + kz*k_dot_x*(1._rt - std::cos(rotation_angle));
                    ignore_unused(k_cross_y);
#endif
```

如果 `do_gaussian_beam_rotation_momenta` 打开，动量也用同一个旋转：

```cpp
                    if (plasma_injector.do_rotation_momenta){
                        const Real k_dot_u = kx*u.x + ky*u.y + kz*u.z;
                        const Real k_cross_u_x = ky*u.z - kz*u.y;
                        const Real k_cross_u_y = kz*u.x - kx*u.z;
                        const Real k_cross_u_z = kx*u.y - ky*u.x;

                        // rotate momenta
                        u.x = u.x * std::cos(rotation_angle) + k_cross_u_x * std::sin(rotation_angle) + kx * k_dot_u * (1._rt - std::cos(rotation_angle));
                        u.y = u.y * std::cos(rotation_angle) + k_cross_u_y * std::sin(rotation_angle) + ky * k_dot_u * (1._rt - std::cos(rotation_angle));
                        u.z = u.z * std::cos(rotation_angle) + k_cross_u_z * std::sin(rotation_angle) + kz * k_dot_u * (1._rt - std::cos(rotation_angle));
                    }
```

源码和文档一致：动量旋转不能独立于位置旋转，必须先打开位置旋转。

## 7. 对称化：用镜像粒子降低横向统计噪声

源码位置：`../warpx/Source/Particles/ParticleCreation/AddParticles.cpp:522-604`。

```cpp
                u.x *= PhysConst::c;
                u.y *= PhysConst::c;
                u.z *= PhysConst::c;

                if (do_symmetrize && symmetrization_order == 8){
                    // Add eight particles to the beam:
                    CheckAndAddParticle(x, y, z, u.x, u.y, u.z, weight/8._rt,
                                        particle_x,  particle_y,  particle_z,
                                        particle_ux, particle_uy, particle_uz,
                                        particle_w);
                    CheckAndAddParticle(x, -y, z, u.x, -u.y, u.z, weight/8._rt,
                                        particle_x,  particle_y,  particle_z,
                                        particle_ux, particle_uy, particle_uz,
                                        particle_w);
```

对称化不是改变物理束流均值，而是为每个随机样本生成镜像粒子，使横向偶极矩等低阶噪声更小：

- order 4：`(x,y), (x,-y), (-x,y), (-x,-y)`；
- order 8：再加入 `x/y` 交换后的四个点。

每个镜像粒子的权重除以对称化阶数，保持同一个样本代表的总真实粒子数不变。

最终落点仍然是 `AddNParticles()`：

```cpp
    AddNParticles(0, np, xp,  yp,  zp, uxp, uyp, uzp,
                  1, attr, 0, attr_int, 1);
}
```

## 8. `CheckAndAddParticle()`：Gaussian/openPMD 共同使用 boosted-frame 变换

源码位置：`../warpx/Source/Particles/ParticleCreation/AddParticles.cpp:340-364`。

```cpp
void
PhysicalParticleContainer::CheckAndAddParticle (
    amrex::ParticleReal x, amrex::ParticleReal y, amrex::ParticleReal z,
    amrex::ParticleReal ux, amrex::ParticleReal uy, amrex::ParticleReal uz,
    amrex::ParticleReal weight,
    amrex::Gpu::HostVector<ParticleReal>& particle_x,
    amrex::Gpu::HostVector<ParticleReal>& particle_y,
    amrex::Gpu::HostVector<ParticleReal>& particle_z,
    amrex::Gpu::HostVector<ParticleReal>& particle_ux,
    amrex::Gpu::HostVector<ParticleReal>& particle_uy,
    amrex::Gpu::HostVector<ParticleReal>& particle_uz,
    amrex::Gpu::HostVector<ParticleReal>& particle_w,
    amrex::Real t_lab) const
{
    if (WarpX::gamma_boost > 1.) {
        MapParticletoBoostedFrame(x, y, z, ux, uy, uz, t_lab);
    }
    particle_x.push_back(x);
    particle_y.push_back(y);
    particle_z.push_back(z);
    particle_ux.push_back(ux);
    particle_uy.push_back(uy);
    particle_uz.push_back(uz);
    particle_w.push_back(weight);
}
```

Gaussian beam 调用时通常不传 `t_lab`，使用默认值 0；openPMD 外部文件可以用 `impose_t_lab_from_file` 让 `t_lab` 等于文件 iteration time。

## 9. openPMD 外部文件：构造期读取质量和电荷

源码位置：`../warpx/Source/Initialization/PlasmaInjector.cpp:483-584`。

```cpp
void PlasmaInjector::setupExternalFile (amrex::ParmParse const& pp_species)
{
#ifndef WARPX_USE_OPENPMD
    WARPX_ABORT_WITH_MESSAGE(
        "WarpX has to be compiled with USE_OPENPMD=TRUE to be able"
        " to read the external openPMD file with species data");
#endif
    external_file = true;
    std::string str_injection_file;
    utils::parser::get(pp_species, source_name, "injection_file", str_injection_file);
    // optional parameters
    utils::parser::queryWithParser(pp_species, source_name, "q_tot", q_tot);
    utils::parser::queryWithParser(pp_species, source_name, "z_shift",z_shift);
```

没有 openPMD 支持会直接 abort。构造期只打开一次 file，检查结构，并读取可选的 `charge`/`mass` 常量 record。

```cpp
        auto series = openPMD::Series(
            str_injection_file, openPMD::Access::READ_ONLY);

        WARPX_ALWAYS_ASSERT_WITH_MESSAGE(
            series.iterations.size() == 1u,
            "External file should contain only 1 iteration\n");
        openPMD::Iteration it = series.iterations.begin()->second;
        WARPX_ALWAYS_ASSERT_WITH_MESSAGE(
            it.particles.size() == 1u,
            "External file should contain only 1 species\n");
```

实现假设文件只有一个 iteration 和一个 species。然后处理质量/电荷优先级：

```cpp
        charge_from_source = ps.contains("charge");
        mass_from_source = ps.contains("mass");

        if (charge_from_source) {
            if (charge_is_specified) {
                ablastr::warn_manager::WMRecordWarning("Species",
                    "Both '" + ps_name + ".charge' and '" +
                        ps_name + ".injection_file' specify a charge.\n'" +
                        ps_name + ".charge' will take precedence.\n");
            }
            else if (species_is_specified) {
                ablastr::warn_manager::WMRecordWarning("Species",
                    "Both '" + ps_name + ".species_type' and '" +
                        ps_name + ".injection_file' specify a charge.\n'" +
                        ps_name + ".species_type' will take precedence.\n");
            }
            else {
                auto p_q_ptr =
                    ps["charge"][openPMD::RecordComponent::SCALAR].loadChunk<amrex::ParticleReal>();
                series.flush();
                amrex::ParticleReal const p_q = p_q_ptr.get()[0];
                auto const charge_unit = static_cast<amrex::Real>(ps["charge"][openPMD::RecordComponent::SCALAR].unitSI());
                charge = p_q * charge_unit;
            }
        }
```

优先级是：

```text
input charge/mass > input species_type > openPMD charge/mass record
```

读取完成后广播到非 IO rank：

```cpp
    std::array<int,2> flags{charge_from_source, mass_from_source};
    amrex::ParallelDescriptor::Bcast(flags.data(), flags.size(), amrex::ParallelDescriptor::IOProcessorNumber());
    charge_from_source = flags[0];
    mass_from_source   = flags[1];
    if (charge_from_source) {
        amrex::ParallelDescriptor::Bcast(&charge, 1, amrex::ParallelDescriptor::IOProcessorNumber());
    }
    if (mass_from_source) {
        amrex::ParallelDescriptor::Bcast(&mass, 1, amrex::ParallelDescriptor::IOProcessorNumber());
    }
```

## 10. openPMD 外部文件：创建粒子列表

源码位置：`../warpx/Source/Particles/ParticleCreation/AddParticles.cpp:607-743`。

```cpp
void
PhysicalParticleContainer::AddPlasmaFromFile(PlasmaInjector & plasma_injector,
                                             amrex::ParticleReal q_tot,
                                             amrex::ParticleReal z_shift)
{
    // Declare temporary vectors on the CPU
    amrex::Gpu::HostVector<ParticleReal> particle_x;
    amrex::Gpu::HostVector<ParticleReal> particle_z;
    amrex::Gpu::HostVector<ParticleReal> particle_ux;
    amrex::Gpu::HostVector<ParticleReal> particle_uz;
    amrex::Gpu::HostVector<ParticleReal> particle_w;
    amrex::Gpu::HostVector<ParticleReal> particle_y;
    amrex::Gpu::HostVector<ParticleReal> particle_uy;
```

外部文件注入和 Gaussian beam 一样，先建 host vector。openPMD 编译开关下，IO rank 取得 series 所有权：

```cpp
#ifdef WARPX_USE_OPENPMD
    //TODO: Make changes for read/write in multiple MPI ranks
    if (ParallelDescriptor::IOProcessor()) {
        // take ownership of the series and close it when done
        auto series = std::any_cast<openPMD::Series>(std::move(plasma_injector.m_openpmd_input_series));

        // assumption asserts: see PlasmaInjector
        openPMD::Iteration it = series.iterations.begin()->second;
        const ParmParse pp_species_name(species_name);
        pp_species_name.query("impose_t_lab_from_file", impose_t_lab_from_file);
        double t_lab = 0._prt;
        if (impose_t_lab_from_file) {
            // Impose t_lab as being the time stored in the openPMD file
            t_lab = it.time<double>() * it.timeUnitSI();
        }
```

当前 TODO 注释说明这条路径还没有多 MPI rank 并行读写优化：读文件主要在 IO processor 上完成，再通过 `AddNParticles()` 的 `uniqueparticles=1` 路径处理。

加载 position、positionOffset、momentum、weighting：

```cpp
        auto const npart = ps["position"]["x"].getExtent()[0];
#if !defined(WARPX_DIM_1D_Z)  // 2D, 3D, RZ, 1D_R
        const std::shared_ptr<ParticleReal> ptr_x = ps["position"]["x"].loadChunk<ParticleReal>();
        const std::shared_ptr<ParticleReal> ptr_offset_x = ps["positionOffset"]["x"].loadChunk<ParticleReal>();
        auto const position_unit_x = static_cast<ParticleReal>(ps["position"]["x"].unitSI());
        auto const position_offset_unit_x = static_cast<ParticleReal>(ps["positionOffset"]["x"].unitSI());
#endif
```

权重 record：

```cpp
        const std::shared_ptr<ParticleReal> ptr_w = ps["weighting"][openPMD::RecordComponent::SCALAR].loadChunk<ParticleReal>();
        auto const w_unit = static_cast<ParticleReal>(ps["weighting"][openPMD::RecordComponent::SCALAR].unitSI());
```

如果用户给了 `q_tot`，只 warning，不重标定：

```cpp
        if (q_tot != 0.0) {
            std::stringstream warnMsg;
            warnMsg << " Loading particle species from file. " << ps_name << ".q_tot is ignored.";
            ablastr::warn_manager::WMRecordWarning("AddPlasmaFromFile",
               warnMsg.str(), ablastr::warn_manager::WarnPriority::high);
        }
```

## 11. openPMD 单粒子的单位换算

源码位置：`../warpx/Source/Particles/ParticleCreation/AddParticles.cpp:680-715`。

```cpp
        for (auto i = decltype(npart){0}; i<npart; ++i){

            amrex::ParticleReal const weight = ptr_w.get()[i]*w_unit;

#if !defined(WARPX_DIM_1D_Z)
            amrex::ParticleReal const x = ptr_x.get()[i]*position_unit_x + ptr_offset_x.get()[i]*position_offset_unit_x;
#else
            amrex::ParticleReal const x = 0.0_prt;
#endif
#if defined(WARPX_DIM_3D) || defined(WARPX_DIM_RZ) || defined(WARPX_DIM_RCYLINDER) || defined(WARPX_DIM_RSPHERE)
            amrex::ParticleReal const y = ptr_y.get()[i]*position_unit_y + ptr_offset_y.get()[i]*position_offset_unit_y;
#else
            amrex::ParticleReal const y = 0.0_prt;
#endif
#if !defined(WARPX_DIM_RCYLINDER)
            amrex::ParticleReal const z = ptr_z.get()[i]*position_unit_z + ptr_offset_z.get()[i]*position_offset_unit_z + z_shift;
#else
            amrex::ParticleReal const z = 0.0_prt;
#endif
```

position 使用 openPMD 的 `position + positionOffset`，再乘对应 `unitSI`。`z_shift` 是 WarpX 额外加到纵向坐标上的偏移。

动量换算：

```cpp
            if (plasma_injector.insideBounds(x, y, z)) {

                // The normalized momentum is u = p / m = gamma beta c
                // with m = m_e for photons, m the particle mass otherwise.
                amrex::ParticleReal const mass_eff = (m_mass > 0.0_prt) ? m_mass : PhysConst::m_e;
                amrex::ParticleReal const ux = ptr_ux.get()[i]*momentum_unit_x/mass_eff;
                amrex::ParticleReal const uz = ptr_uz.get()[i]*momentum_unit_z/mass_eff;
                amrex::ParticleReal uy = 0.0_prt;
                if (ps["momentum"].contains("y")) {
                    uy = ptr_uy.get()[i]*momentum_unit_y/mass_eff;
                }
```

openPMD 文件中动量 record 表示物理动量 `p`。除以质量后得到 `p/m = gamma v`，也就是 WarpX 粒子数组中的 `ux/uy/uz` 量纲。对光子等 `m_mass <= 0` 的情况，代码用电子质量作为有效归一化质量，这和注释一致。

最后共同走 `CheckAndAddParticle()`：

```cpp
                CheckAndAddParticle(x, y, z, ux, uy, uz, weight,
                                    particle_x,  particle_y,  particle_z,
                                    particle_ux, particle_uy, particle_uz,
                                    particle_w, static_cast<amrex::Real>(t_lab));
            }
        }
```

如果 boosted-frame simulation 且 `impose_t_lab_from_file=1`，这里传入的 `t_lab` 会被 `MapParticletoBoostedFrame()` 用来计算 boosted-frame 坐标。

## 12. 两条路径和 `AddPlasma()` 的差异

| 路径 | 位置来源 | 权重来源 | 动量来源 | 并行生成方式 | 最终写入 |
|---|---|---|---|---|---|
| `AddPlasma()` | 每个 cell 内 `InjectorPosition` | `density * volume / ppc` | `InjectorMomentum` | 每个 tile GPU kernel | 直接写 particle tile |
| `AddPlasmaFlux()` | 注入面/EB 上 `InjectorPosition` | `flux * area * dt / ppc` | `InjectorMomentumGaussianFlux` 等 | 每个 tile GPU kernel + tmp container | tmp container 后合并 |
| `AddGaussianBeam()` | host 上随机高斯采样 | `N_tot/npart` 或 `q_tot/(npart*q)` | `InjectorMomentum` | IO rank host vector | `AddNParticles()` |
| `AddPlasmaFromFile()` | openPMD `position + offset` | openPMD `weighting` | openPMD `momentum / mass` | IO rank 读文件 | `AddNParticles()` |

因此，Gaussian beam/openPMD 更像“粒子列表注入”，而不是“网格密度采样注入”。

## 13. 初始化模块至此的完整边界

到本篇为止，阶段 2 Initialization 的 species 初始化路径已经覆盖：

```text
PlasmaInjector
  -> setupSingleParticle / setupMultipleParticles
  -> setupGaussianBeam
  -> setupExternalFile
  -> setupNRandomPerCell / setupNuniformPerCell
  -> setupNFluxPerCell

PhysicalParticleContainer::AddParticles
  -> AddNParticles for explicit lists
  -> AddGaussianBeam for random beam list
  -> AddPlasmaFromFile for openPMD list
  -> AddPlasma for density-based volume injection
  -> AddPlasmaFlux for flux injection during evolution
```

后续正式章节可以按三层写：

1. 输入参数层：`injection_style`、`profile`、`momentum_distribution_type`。
2. 物理模型层：空间分布、权重、动量分布、boosted-frame 变换。
3. 实现层：host list 注入、GPU tile kernel 注入、runtime 属性初始化、`Redistribute()` 清理和分配。
