# AddParticles 与 AddPlasma 精读：从注入器到粒子 SoA

绑定源码：`../warpx`，分支 `pkuHEDPbranch`，commit `063f8b586f04321e13150ae3e730e0794ca75cb1`。

本笔记覆盖：

- `../warpx/Source/Particles/PhysicalParticleContainer.cpp:429-449`
- `../warpx/Source/Particles/ParticleCreation/AddParticles.cpp`
- `../warpx/Source/Particles/ParticleCreation/AddPlasmaUtilities.H/.cpp`
- `../warpx/Source/Particles/ParticleCreation/SmartCreate.H`
- `../warpx/Source/Particles/ParticleCreation/DefaultInitialization.H`
- `../warpx/Source/Particles/WarpXParticleContainer.cpp:183-354`

目标是把初始化链最后一段讲清楚：`PlasmaInjector` 中的规则如何变成 AMReX particle tile 里的 SoA 数据。

## 1. 入口：`InitData()` 只做两件事

源码位置：`../warpx/Source/Particles/PhysicalParticleContainer.cpp:429-433`。

```cpp
void PhysicalParticleContainer::InitData ()
{
    AddParticles(0); // Note - add on level 0
    Redistribute();  // We then redistribute
}
```

粒子初始化入口非常短：

1. `AddParticles(0)` 在 level 0 生成初始粒子；
2. `Redistribute()` 把粒子从临时 tile 或初始 tile 移动到正确网格/tile，并移除无效粒子。

这解释了为什么 `AddPlasma()` 内部可以先“过量创建候选粒子，再把无效粒子 ID 标成 invalid”：最终清理由重分布阶段完成。

## 2. `AddParticles()` 按注入类型分发

源码位置：`../warpx/Source/Particles/ParticleCreation/AddParticles.cpp:194-260`。

```cpp
void
PhysicalParticleContainer::AddParticles (int lev)
{
    ABLASTR_PROFILE("PhysicalParticleContainer::AddParticles()");

    for (auto const& plasma_injector : plasma_injectors) {

        if (plasma_injector->add_single_particle) {
            if (WarpX::gamma_boost > 1.) {
                MapParticletoBoostedFrame(plasma_injector->single_particle_pos[0],
                                          plasma_injector->single_particle_pos[1],
                                          plasma_injector->single_particle_pos[2],
                                          plasma_injector->single_particle_u[0],
                                          plasma_injector->single_particle_u[1],
                                          plasma_injector->single_particle_u[2]);
            }
            const amrex::Vector<ParticleReal> xp = {plasma_injector->single_particle_pos[0]};
            const amrex::Vector<ParticleReal> yp = {plasma_injector->single_particle_pos[1]};
            const amrex::Vector<ParticleReal> zp = {plasma_injector->single_particle_pos[2]};
            const amrex::Vector<ParticleReal> uxp = {plasma_injector->single_particle_u[0]};
            const amrex::Vector<ParticleReal> uyp = {plasma_injector->single_particle_u[1]};
            const amrex::Vector<ParticleReal> uzp = {plasma_injector->single_particle_u[2]};
            const amrex::Vector<amrex::Vector<ParticleReal>> attr = {{plasma_injector->single_particle_weight}};
            const amrex::Vector<amrex::Vector<int>> attr_int;
            AddNParticles(lev, 1, xp, yp, zp, uxp, uyp, uzp,
                          1, attr, 0, attr_int, 0);
            return;
        }
```

`AddParticles()` 遍历该 species 持有的 `plasma_injectors`。它不是一个统一采样 kernel，而是先按注入类型选择路径：

- `add_single_particle`：手工指定一个粒子；
- `add_multiple_particles`：手工指定多个粒子；
- `gaussian_beam`：CPU 上生成高斯束，再走 `AddNParticles()`；
- `external_file`：从 openPMD 粒子文件读入；
- `doInjection()`：体注入，调用 `AddPlasma()`。

源码后半段：

```cpp
        if (plasma_injector->gaussian_beam) {
            AddGaussianBeam(*plasma_injector);
        }

        if (plasma_injector->external_file) {
            AddPlasmaFromFile(*plasma_injector,
                              plasma_injector->q_tot,
                              plasma_injector->z_shift);
        }

        if ( plasma_injector->doInjection() ) {
            AddPlasma(*plasma_injector, lev);
        }
    }
}
```

这说明 `PlasmaInjector` 只是参数总容器，真正生成粒子的实现分散在多个函数中。

## 3. 连续注入与 flux 注入

源码位置：`../warpx/Source/Particles/ParticleCreation/AddParticles.cpp:263-292`。

```cpp
void
PhysicalParticleContainer::ContinuousInjection (const amrex::RealBox& injection_box)
{
    // Inject plasma on level 0. Particles will be redistributed.
    const int lev=0;
    for (auto const& plasma_injector : plasma_injectors) {
        AddPlasma(*plasma_injector, lev, injection_box);
    }
}

void
PhysicalParticleContainer::ContinuousFluxInjection (amrex::Real t, amrex::Real dt)
{
    for (auto const& plasma_injector : plasma_injectors) {
        if (plasma_injector->doFluxInjection()){
            // Check the optional parameters for start and stop of injection
            if ( ((plasma_injector->flux_tmin<0) || (t>=plasma_injector->flux_tmin)) &&
                 ((plasma_injector->flux_tmax<0) || (t< plasma_injector->flux_tmax)) ){

                AddPlasmaFlux(*plasma_injector, dt);
            }
        }
    }
}
```

体注入和 flux 注入的物理量不同：

- 体注入给的是数密度 `n(x)`，粒子权重近似为 `n * cell_volume / num_ppc`；
- flux 注入给的是通量 `\Gamma(x,t)`，粒子权重近似为 `\Gamma * area * dt / num_ppc`。

这一区别会在 `compute_scale_fac_volume()` 和 `compute_scale_fac_area_plane()` 中体现。

## 4. boosted frame 坐标变换

源码位置：`../warpx/Source/Particles/ParticleCreation/AddParticles.cpp:293-338`。

```cpp
void PhysicalParticleContainer::MapParticletoBoostedFrame (
    amrex::ParticleReal& x, amrex::ParticleReal& y, amrex::ParticleReal& z,
    amrex::ParticleReal& ux, amrex::ParticleReal& uy, amrex::ParticleReal& uz, amrex::Real t_lab) const
{
    // Map the particles from the lab frame to the boosted frame.
    const amrex::ParticleReal uz_boost = WarpX::gamma_boost*WarpX::beta_boost*PhysConst::c;

    // tpr is the particle's time in the boosted frame
    const amrex::ParticleReal tpr = WarpX::gamma_boost*t_lab - uz_boost*z/PhysConst::c2;

    // The particle's transformed location in the boosted frame
    const amrex::ParticleReal xpr = x;
    const amrex::ParticleReal ypr = y;
    const amrex::ParticleReal zpr = WarpX::gamma_boost*z - uz_boost*t_lab;

    // transform u and gamma to the boosted frame
    const amrex::ParticleReal gamma_lab = std::sqrt(1._rt + (ux*ux + uy*uy + uz*uz)/PhysConst::c2);
    uz = WarpX::gamma_boost*uz - uz_boost*gamma_lab;
```

这里对位置和纵向动量做 Lorentz boost。注意代码中 `ux/uy/uz` 在这个函数内带有速度量纲，`gamma_lab` 使用 `(u^2/c^2)` 还原无量纲关系。

后半段把粒子沿 boosted-frame 速度推进到当前 boosted-frame 时间：

```cpp
    const amrex::ParticleReal gammapr = std::sqrt(1._rt + (ux*ux + uy*uy + uz*uz)/PhysConst::c2);

    const amrex::ParticleReal vxpr = ux/gammapr;
    const amrex::ParticleReal vypr = uy/gammapr;
    const amrex::ParticleReal vzpr = uz/gammapr;

    if (do_backward_propagation){
        uz = -uz;
    }

    constexpr int lev = 0;
    const amrex::Real t0 = WarpX::GetInstance().gett_new(lev);
    if (boost_adjust_transverse_positions) {
        x = xpr - (tpr-t0)*vxpr;
        y = ypr - (tpr-t0)*vypr;
    }
    z = zpr - (tpr-t0)*vzpr;
}
```

这段实现的物理意义是：输入文件或单粒子参数通常在 lab frame 给出，boosted-frame 模拟需要把它们映射到同一个模拟时间切片上。

## 5. `AddNParticles()`：手工粒子、束流和 openPMD 的共同落点

源码位置：`../warpx/Source/Particles/WarpXParticleContainer.cpp:183-354`。

```cpp
void
WarpXParticleContainer::AddNParticles (int /*lev*/, long n,
                                       amrex::Vector<amrex::ParticleReal> const & x,
                                       amrex::Vector<amrex::ParticleReal> const & y,
                                       amrex::Vector<amrex::ParticleReal> const & z,
                                       amrex::Vector<amrex::ParticleReal> const & ux,
                                       amrex::Vector<amrex::ParticleReal> const & uy,
                                       amrex::Vector<amrex::ParticleReal> const & uz,
                                       const int nattr_real,
                                       amrex::Vector<amrex::Vector<amrex::ParticleReal>> const & attr_real,
                                       const int nattr_int,
                                       amrex::Vector<amrex::Vector<int>> const & attr_int,
                                       int uniqueparticles, amrex::Long id)
{
```

`AddNParticles()` 是“已有粒子列表写入粒子容器”的通用接口。它的输入已经是粒子坐标、动量和属性数组，不再调用 `InjectorDensity` 或 `InjectorMomentum`。

它先决定当前 MPI rank 应处理的粒子段：

```cpp
    long ibegin = 0;
    long iend = n;
    if (!uniqueparticles) {
        const int myproc = amrex::ParallelDescriptor::MyProc();
        const int nprocs = amrex::ParallelDescriptor::NProcs();
        const auto navg = n/nprocs;
        const auto nleft = n - navg * nprocs;
        if (myproc < nleft) {
            ibegin = myproc*(navg+1);
            iend = ibegin + navg+1;
        } else {
            ibegin = myproc*navg + nleft;
            iend = ibegin + navg;
        }
    }
```

随后把数据先写到 pinned tile，再复制到真正的 particle tile：

```cpp
    auto& particle_tile = DefineAndReturnParticleTile(0, 0, 0);

    using PinnedTile = typename ContainerLike<amrex::PolymorphicArenaAllocator>::ParticleTileType;
    PinnedTile pinned_tile;
    auto soa_rdata_names = GetRealSoANames();
    auto soa_idata_names = GetIntSoANames();
    pinned_tile.define(NumRuntimeRealComps(), NumRuntimeIntComps(), &soa_rdata_names, &soa_idata_names, amrex::The_Pinned_Arena());
```

固定属性 `x,y,z,w,ux,uy,uz` 直接 push：

```cpp
        pinned_tile.push_back_real(PIdx::w, attr_real[0].data() + ibegin, attr_real[0].data() + iend);
        pinned_tile.push_back_real(PIdx::ux, ux.data() + ibegin, ux.data() + iend);
        pinned_tile.push_back_real(PIdx::uy, uy.data() + ibegin, uy.data() + iend);
        pinned_tile.push_back_real(PIdx::uz, uz.data() + ibegin, uz.data() + iend);
```

最后默认初始化其他 runtime 属性并重分布：

```cpp
        pinned_tile.resize(np);
        // Default initialize the other real and integer runtime attributes
        DefaultInitializeRuntimeAttributes(pinned_tile, nattr_real - 1, nattr_int);

        auto old_np = particle_tile.numParticles();
        auto new_np = old_np + pinned_tile.numParticles();
        particle_tile.resize(new_np);
        amrex::copyParticles(
            particle_tile, pinned_tile, 0, old_np, pinned_tile.numParticles()
        );
    }

    // Move particles to their appropriate tiles
    Redistribute();
```

所以 `AddNParticles()` 是一个 host-list 到 AMReX particle container 的桥梁。

## 6. `AddPlasma()`：体注入主 kernel 的总体结构

源码位置：`../warpx/Source/Particles/ParticleCreation/AddParticles.cpp:746-813`。

```cpp
void
PhysicalParticleContainer::AddPlasma (PlasmaInjector& plasma_injector, int lev, amrex::RealBox part_realbox)
{
    ABLASTR_PROFILE("PhysicalParticleContainer::AddPlasma()");

    // If no part_realbox is provided, initialize particles in the whole domain
    const Geometry& geom = Geom(lev);
    bool initial_injection;
    if (!part_realbox.ok()) {
        part_realbox = geom.ProbDomain();
        initial_injection = true;
    } else {
        initial_injection = false;
    }

    const int num_ppc = plasma_injector.num_particles_per_cell;
    const auto dx = geom.CellSizeArray();
    const auto problo = geom.ProbLoArray();

    defineAllParticleTiles();
```

`part_realbox` 决定注入区域：

- 初始注入没有传 box，使用整个物理域；
- moving window 连续注入传入窗口新增区域。

随后取出位置、密度和动量 functor：

```cpp
    InjectorPosition* inj_pos = plasma_injector.getInjectorPosition();
    InjectorMomentum* inj_mom = plasma_injector.getInjectorMomentumDevice();
    InjectorMomentum* h_inj_mom = plasma_injector.getInjectorMomentumHost();
    const amrex::Real gamma_boost = WarpX::gamma_boost;
    const amrex::Real beta_boost = WarpX::beta_boost;
    const amrex::Real t = WarpX::GetInstance().gett_new(lev);
    const amrex::Real density_min = plasma_injector.density_min;
    const amrex::Real density_max = plasma_injector.density_max;
```

`h_inj_mom` 是 host 侧动量对象，用于 `prepare()` 阶段的 ballistic correction；`inj_mom` 是 device 侧对象，用于 GPU kernel。

## 7. ballistic correction：为什么 density 要回到 lab-frame 初始面

源码位置：`../warpx/Source/Particles/ParticleCreation/AddParticles.cpp:98-122`。

```cpp
AMREX_GPU_HOST_DEVICE AMREX_FORCE_INLINE
amrex::Real applyBallisticCorrection(const XDim3& pos, const InjectorMomentum* inj_mom,
                              amrex::Real gamma_boost, amrex::Real beta_boost, amrex::Real t) noexcept
{
    const XDim3 u_bulk = inj_mom->getBulkMomentum(pos.x, pos.y, pos.z);
    const amrex::Real gamma_bulk = std::sqrt(1._rt +
                         (u_bulk.x*u_bulk.x+u_bulk.y*u_bulk.y+u_bulk.z*u_bulk.z));
    const amrex::Real betaz_bulk = u_bulk.z/gamma_bulk;
    const amrex::Real z0 = gamma_boost * ( pos.z*(1.0_rt-beta_boost*betaz_bulk)
                         - PhysConst::c*t*(betaz_bulk-beta_boost) );
    return z0;
}
```

注释中给出的公式是：

$$
z_{0,lab} = \gamma_b \left[z_{boost}(1-\beta_b\beta_{z,lab}) - ct_{boost}(\beta_{z,lab}-\beta_b)\right].
$$

这不是场推进，而是 ballistic correction：假设粒子在注入前以 bulk velocity 匀速运动，反推它在 lab-frame `t=0` 的位置。原因是用户给的 density/profile 通常定义在 lab-frame 初始面上；boosted-frame 模拟在不同时间切片上注入时，需要回到这个定义面查询密度和边界。

## 8. 先数候选粒子数，再一次性 resize tile

源码位置：`../warpx/Source/Particles/ParticleCreation/AddParticles.cpp:823-927`。

```cpp
    for (MFIter mfi = MakeMFIter(lev, info); mfi.isValid(); ++mfi)
    {
        const amrex::Box& tile_box = mfi.tilebox();
        const amrex::RealBox tile_realbox = WarpX::getRealBox(tile_box, lev);

        amrex::RealBox overlap_realbox;
        amrex::Box overlap_box;
        amrex::IntVect shifted;
        const bool no_overlap = find_overlap(tile_realbox, part_realbox, dx, problo, overlap_realbox, overlap_box, shifted);
        if (no_overlap) {
            continue; // Go to the next tile
        }

        auto* inj_rho = plasma_injector.getInjectorDensity(mfi.LocalIndex());
```

`find_overlap()` 先求当前 tile 与注入 box 的交叠区域。随后用一个 device vector 记录每个 cell 要创建的候选粒子数：

```cpp
        amrex::Gpu::DeviceVector<amrex::Long> counts(overlap_box.numPts(), 0);
        amrex::Gpu::DeviceVector<amrex::Long> offset(overlap_box.numPts());
        auto *pcounts = counts.data();
        amrex::ParallelFor(overlap_box, [=] AMREX_GPU_DEVICE (int i, int j, int k) noexcept
        {
            const amrex::IntVect iv(AMREX_D_DECL(i, j, k));
            auto lo = getCellCoords(overlap_corner, dx, {0._rt, 0._rt, 0._rt}, iv);
            auto hi = getCellCoords(overlap_corner, dx, {1._rt, 1._rt, 1._rt}, iv);

            lo.z = applyBallisticCorrection(lo, inj_mom, gamma_boost, beta_boost, t);
            hi.z = applyBallisticCorrection(hi, inj_mom, gamma_boost, beta_boost, t);

            if (inj_pos->overlapsWith(lo, hi))
            {
                auto index = overlap_box.index(iv);
                pcounts[index] = num_ppc*r;
```

这里先用 cell bounds 和 injection position 判断是否可能有粒子。为了避免对完全零密度区域创建粒子，又检查 cell 角点/中心附近的密度：

```cpp
                const auto checker = [&](){
                    for (const auto& x : xlim) {
                        for (const auto& y : ylim) {
                            for (const auto& z : zlim) {
                                if (inj_pos->insideBounds(x,y,z) and (inj_rho->getDensity(x,y,z) > 0) ) {
                                    return 1;
                                }
                            }
                        }
                    }
                    return 0;
                };
                pcounts[index] = checker() ? num_ppc*r : 0;
            }
        });
```

然后 exclusive scan 得到总候选数和每个 cell 的写入 offset：

```cpp
        const amrex::Long max_new_particles = amrex::Scan::ExclusiveSum(counts.size(), counts.data(), offset.data());

        amrex::Long pid;
        {
            pid = ParticleType::NextID();
            ParticleType::NextID(pid+max_new_particles);
        }
```

这种“两遍”结构是 GPU 代码常见写法：先并行计数，再一次性扩容，再并行填充。

## 9. 无效粒子的处理：清零并设置 invalid ID

源码位置：`../warpx/Source/Particles/ParticleCreation/AddParticles.cpp:155-191`。

```cpp
AMREX_GPU_HOST_DEVICE AMREX_FORCE_INLINE
void ZeroInitializeAndSetNegativeID (
    uint64_t * AMREX_RESTRICT idcpu,
    const amrex::GpuArray<ParticleReal*,PIdx::nattribs>& pa, long& ip,
    const bool& do_field_ionization, int* pi
#ifdef WARPX_QED
    ,const QEDHelper& qed_helper
#endif
    ) noexcept
{
    for (int idx=0 ; idx < PIdx::nattribs ; idx++) {
        pa[idx][ip] = 0._rt;
    }
    if (do_field_ionization) {pi[ip] = 0;}
#ifdef WARPX_QED
    if (qed_helper.has_quantum_sync) {qed_helper.p_optical_depth_QSR[ip] = 0._rt;}
    if (qed_helper.has_breit_wheeler) {qed_helper.p_optical_depth_BW[ip] = 0._rt;}
#endif

    idcpu[ip] = amrex::ParticleIdCpus::Invalid;
}
```

候选粒子可能因为越界、密度低于阈值、boosted-frame 反推后不在注入区等原因无效。WarpX 不在 kernel 内动态删除，而是：

1. 把所有固定属性清零；
2. 对 ionization/QED runtime 属性也清零；
3. 把 `idcpu` 设为 invalid；
4. 后续 `Redistribute()` 或 `deleteInvalidParticles()` 清理。

这避免了 GPU kernel 中复杂的并发压缩。

## 10. 体注入 kernel：坐标、密度、动量、权重

源码位置：`../warpx/Source/Particles/ParticleCreation/AddParticles.cpp:964-1203`。

```cpp
        amrex::ParallelForRNG(overlap_box,
        [=] AMREX_GPU_DEVICE (int i, int j, int k, amrex::RandomEngine const& engine) noexcept
        {
            const amrex::IntVect iv = amrex::IntVect(AMREX_D_DECL(i, j, k));
            const auto index = overlap_box.index(iv);

            const amrex::Real scale_fac = compute_scale_fac_volume(dx, pcounts[index]);
            for (int i_part = 0; i_part < pcounts[index]; ++i_part)
            {
                long ip = poffset[index] + i_part;
                pa_idcpu[ip] = amrex::SetParticleIDandCPU(pid+ip, cpuid);
                const XDim3 r = (fine_overlap_box.ok() && fine_overlap_box.contains(iv)) ?
                  inj_pos->getPositionUnitBox(i_part, rrfac, engine) :
                  inj_pos->getPositionUnitBox(i_part, amrex::IntVect::TheUnitVector(), engine);
                auto pos = getCellCoords(overlap_corner, dx, r, iv);
```

`r` 是 cell 内的单位坐标，来自 `InjectorPosition`。`getCellCoords()` 把单位坐标映射到真实空间坐标，并按 3D/XZ/RZ/1D/径向几何做编译期分支。

体注入的权重系数来自：

```cpp
AMREX_GPU_HOST_DEVICE AMREX_FORCE_INLINE
amrex::Real compute_scale_fac_volume (const amrex::GpuArray<amrex::Real, AMREX_SPACEDIM>& dx,
                                      const amrex::Long pcount) {
    using namespace amrex::literals;
    return (pcount != 0) ? AMREX_D_TERM(dx[0],*dx[1],*dx[2])/pcount : 0.0_rt;
}
```

也就是

$$
w_p = n(\mathbf{x}) \frac{\Delta V}{N_{ppc}},
$$

其中 `N_ppc` 在 refined injection region 会乘以 refinement ratio。

lab frame 分支：

```cpp
                if (gamma_boost == 1._rt) {
                    const amrex::Real z0 = applyBallisticCorrection(pos, inj_mom, gamma_boost,
                                                             beta_boost, t);
                    if (!inj_pos->insideBounds(xb, yb, z0)) {
                        ZeroInitializeAndSetNegativeID(pa_idcpu, pa, ip, loc_do_field_ionization, pi
#ifdef WARPX_QED
                                                   ,qed_helper
#endif
                                                   );
                        continue;
                    }

                    u = inj_mom->getMomentum(pos.x, pos.y, z0, engine);
                    dens = inj_rho->getDensity(pos.x, pos.y, z0);

                    if ( dens < density_min ){
                        ZeroInitializeAndSetNegativeID(pa_idcpu, pa, ip, loc_do_field_ionization, pi
#ifdef WARPX_QED
                                                   ,qed_helper
#endif
                                                   );
                        continue;
                    }
                    dens = amrex::min(dens, density_max);
                }
```

boosted frame 分支：

```cpp
                } else {
                    const amrex::Real z0_lab = applyBallisticCorrection(pos, inj_mom, gamma_boost,
                                                                        beta_boost, t);
                    if (!inj_pos->insideBounds(xb, yb, z0_lab)) {
                        ZeroInitializeAndSetNegativeID(pa_idcpu, pa, ip, loc_do_field_ionization, pi
#ifdef WARPX_QED
                                                   ,qed_helper
#endif
                                                   );
                        continue;
                    }
                    dens = inj_rho->getDensity(pos.x, pos.y, z0_lab);
                    if ( dens < density_min ){
                        ZeroInitializeAndSetNegativeID(pa_idcpu, pa, ip, loc_do_field_ionization, pi
#ifdef WARPX_QED
                                                   ,qed_helper
#endif
                                                   );
                        continue;
                    }
                    dens = amrex::min(dens, density_max);

                    u = inj_mom->getMomentum(pos.x, pos.y, 0._rt, engine);
                    const amrex::Real gamma_lab = std::sqrt( 1._rt+(u.x*u.x+u.y*u.y+u.z*u.z) );
                    const amrex::Real betaz_lab = u.z/(gamma_lab);

                    dens = gamma_boost * dens * ( 1.0_rt - beta_boost*betaz_lab );
                    u.z = gamma_boost * ( u.z -beta_boost*gamma_lab );
                }
```

这里的 density 变换对应四流密度变换：

$$
n' = \gamma_b n (1-\beta_b\beta_z),
$$

纵向动量变换为

$$
u_z' = \gamma_b(u_z-\beta_b\gamma).
$$

最后写入 SoA：

```cpp
                u.x *= PhysConst::c;
                u.y *= PhysConst::c;
                u.z *= PhysConst::c;

                amrex::Real weight = dens;
                weight *= scale_fac;

                pa[PIdx::w ][ip] = weight;
                pa[PIdx::ux][ip] = u.x;
                pa[PIdx::uy][ip] = u.y;
                pa[PIdx::uz][ip] = u.z;
```

这再次确认：`InjectorMomentum` 返回的是无量纲 `gamma beta`，粒子数组中存的是 `gamma v = c gamma beta`。

## 11. RZ/RSPHERE 的半径重采样和权重修正

源码位置：`../warpx/Source/Particles/ParticleCreation/AddParticles.cpp:1009-1058, 1163-1175`。

RZ/径向几何不能简单在半径 `r` 上均匀采样后保持权重不变。代码先在逻辑半径上采样，再按 `radial_numpercell_power` 重映射：

```cpp
                amrex::Real const xu = (pos.x - rmin)/(rmax - rmin);
                amrex::Real const rc = std::pow(rmax, 1._rt + radial_numpercell_power)
                                     - std::pow(rmin, 1._rt + radial_numpercell_power);
                amrex::Real const rminp = std::pow(rmin, 1._rt + radial_numpercell_power);
                amrex::Real const xb = std::pow(xu*rc + rminp, 1._rt/(1._rt + radial_numpercell_power));
                amrex::Real const yb = theta;

                pos.x = xb*std::cos(theta);
                pos.y = xb*std::sin(theta);
```

然后对宏粒子权重乘以几何系数：

```cpp
                const amrex::Real coeff = 2._rt*MathConst::pi/(1._rt + radial_numpercell_power)
                        *(rmax - std::pow(rmax, -radial_numpercell_power)*std::pow(rmin, 1._rt + radial_numpercell_power))*
                        (rmax/(rmax - rmin));
                weight *= coeff*std::pow(xb/rmax, 1._rt - radial_numpercell_power);
```

物理上，这是在 cylindrical volume element

$$
dV = 2\pi r\,dr\,dz
$$

下保证宏粒子统计代表真实体积权重。`radial_numpercell_power` 控制粒子数在半径方向的分布，权重系数补偿采样分布与物理体积元之间的差异。

## 12. runtime 属性、ionization 和 QED optical depth

源码位置：`../warpx/Source/Particles/ParticleCreation/AddParticles.cpp:1134-1154`。

```cpp
                if (loc_do_field_ionization) {
                    pi[ip] = loc_ionization_initial_level;
                }

#ifdef WARPX_QED
                if(qed_helper.has_quantum_sync){
                    qed_helper.p_optical_depth_QSR[ip] = qed_helper.quantum_sync_get_opt(engine);
                }

                if(qed_helper.has_breit_wheeler){
                    qed_helper.p_optical_depth_BW[ip] = qed_helper.breit_wheeler_get_opt(engine);
                }
#endif
                // Initialize user-defined integers with user-defined parser
                for (int ia = 0; ia < n_user_int_attribs; ++ia) {
                    pa_user_int_data[ia][ip] = static_cast<int>(user_int_parserexec_data[ia](pos.x, pos.y, pos.z, u.x, u.y, u.z, t));
                }
                // Initialize user-defined real attributes with user-defined parser
                for (int ia = 0; ia < n_user_real_attribs; ++ia) {
                    pa_user_real_data[ia][ip] = user_real_parserexec_data[ia](pos.x, pos.y, pos.z, u.x, u.y, u.z, t);
                }
```

这段代码说明用户自定义属性不是事后统一补丁，而是在粒子创建 kernel 中用当前位置、动量和时间直接求值。QED optical depth 用随机数初始化，field ionization 则写入初始电离能级。

`DefaultInitialization.H` 给出默认策略：

```cpp
static std::map<std::string, InitializationPolicy> initialization_policies = {
    {"w",     InitializationPolicy::Zero },
    {"ux",    InitializationPolicy::Zero },
    {"uy",    InitializationPolicy::Zero },
    {"uz",    InitializationPolicy::Zero },
#ifdef WARPX_DIM_RZ
    {"theta", InitializationPolicy::Zero},
#endif

#ifdef WARPX_QED
    {"opticalDepthBW",   InitializationPolicy::RandomExp},
    {"opticalDepthQSR",   InitializationPolicy::RandomExp}
#endif
};
```

`AddPlasma()` 对自身直接创建的属性手工写入；`AddNParticles()` 等路径则通过 `DefaultInitializeRuntimeAttributes()` 补齐未外部提供的 runtime 属性。

## 13. `AddPlasmaFlux()`：通量注入的权重公式

源码位置：`../warpx/Source/Particles/ParticleCreation/AddParticles.cpp:1231-1766`。

flux 注入的总体结构与体注入相似：tile 交叠、计数、scan、resize、kernel 写入。但它有三个关键不同。

第一，创建临时容器：

```cpp
    PhysicalParticleContainer tmp_pc(&WarpX::GetInstance());
    for (int ic = 0; ic < NumRuntimeRealComps(); ++ic) { tmp_pc.AddRealComp(GetRealSoANames()[ic + NArrayReal], false); }
    for (int ic = 0; ic < NumRuntimeIntComps(); ++ic) { tmp_pc.AddIntComp(GetIntSoANames()[ic + NArrayInt], false); }
    tmp_pc.defineAllParticleTiles();
```

flux 注入的粒子初始位置可能在边界面上，随后会随机推进 `t_fract`，所以先放到临时容器中，重分布后再合并回当前容器。

第二，候选粒子数允许非整数 `num_particles_per_cell_real`：

```cpp
            const int num_ppc_int = static_cast<int>(num_ppc_real_in_this_cell*r + amrex::Random(engine));
            pcounts[index] = num_ppc_int;
```

这是随机舍入：若 `num_ppc_real = 2.3`，每个 cell 平均生成 2.3 个宏粒子。

第三，权重按面积和时间计算：

```cpp
AMREX_GPU_HOST_DEVICE AMREX_FORCE_INLINE
amrex::Real compute_scale_fac_area_plane (const amrex::GpuArray<amrex::Real, AMREX_SPACEDIM>& dx,
                                    const amrex::Real num_ppc_real, const int flux_normal_axis) {
    using namespace amrex::literals;
    amrex::Real scale_fac = AMREX_D_TERM(dx[0],*dx[1],*dx[2])/num_ppc_real;
    // Scale particle weight by the area of the emitting surface, within one cell
#if defined(WARPX_DIM_3D)
    scale_fac /= dx[flux_normal_axis];
#elif defined(WARPX_DIM_RZ) || defined(WARPX_DIM_XZ)
    if (flux_normal_axis == 0) { scale_fac /= dx[0]; }
    if (flux_normal_axis == 2) { scale_fac /= dx[1]; }
#endif
    return scale_fac;
}
```

在 3D 中，`dx*dy*dz / dx_normal` 就是注入面的面积。最终：

```cpp
                const amrex::Real flux = inj_flux->getFlux(ppos.x, ppos.y, ppos.z, t);
                if (flux <= 0) {
                    pa_idcpu[ip] = amrex::ParticleIdCpus::Invalid;
                    continue;
                }
```

权重：

```cpp
                const amrex::Real weight = flux * scale_fac * dt;
                pa[PIdx::w ][ip] = weight;
                pa[PIdx::ux][ip] = pu.x;
                pa[PIdx::uy][ip] = pu.y;
                pa[PIdx::uz][ip] = pu.z;
```

也就是

$$
w_p = \Gamma(\mathbf{x},t)\frac{\Delta A\,\Delta t}{N_{ppc}}.
$$

为了让流入不是所有粒子都压在边界面上，代码随机推进一小段时间：

```cpp
                const amrex::Real t_fract = amrex::Random(engine)*dt;
                UpdatePosition(ppos.x, ppos.y, ppos.z, pu.x, pu.y, pu.z, t_fract, mass);
```

## 14. `AddPlasmaUtilities`：交叠区域和面积/体积缩放

源码位置：`../warpx/Source/Particles/ParticleCreation/AddPlasmaUtilities.cpp:12-43`。

```cpp
bool find_overlap (const amrex::RealBox& tile_realbox, const amrex::RealBox& part_realbox,
                   const amrex::GpuArray<amrex::Real, AMREX_SPACEDIM>& dx,
                   const amrex::GpuArray<amrex::Real, AMREX_SPACEDIM>& prob_lo,
                   amrex::RealBox& overlap_realbox, amrex::Box& overlap_box, amrex::IntVect& shifted)
{
    using namespace amrex::literals;

    bool no_overlap = false;
    for (int dir=0; dir<AMREX_SPACEDIM; dir++) {
        if ( tile_realbox.lo(dir) <= part_realbox.hi(dir) ) {
            const amrex::Real ncells_adjust = std::floor( (tile_realbox.lo(dir) - part_realbox.lo(dir))/dx[dir] );
            overlap_realbox.setLo( dir, part_realbox.lo(dir) + std::max(ncells_adjust, 0._rt) * dx[dir]);
        } else {
            no_overlap = true; break;
        }
```

`find_overlap()` 把真实坐标 box 转回 cell box，并返回 `shifted`，用于从注入区域局部 cell index 转到全局网格位置。

flux 版本会把法向方向压缩成一个面：

```cpp
            overlap_realbox.setLo( dir, plasma_injector.surface_flux_pos );
            overlap_realbox.setHi( dir, plasma_injector.surface_flux_pos );
            overlap_box.setSmall( dir, 0 );
            overlap_box.setBig( dir, 0 );
```

这正是面通量和体密度的几何差异。

## 15. `SmartCreate`：给二次粒子创建用的通用初始化器

源码位置：`../warpx/Source/Particles/ParticleCreation/SmartCreate.H:34-84`。

```cpp
struct SmartCreate
{
    const InitializationPolicy* m_policy_real;
    const InitializationPolicy* m_policy_int;
    int m_weight_index = 0;

    template <typename PartData>
    AMREX_GPU_HOST_DEVICE AMREX_FORCE_INLINE
    void operator() (
        PartData& prt, const int i_prt,
        amrex::RandomEngine const& engine,
        const amrex::Real x = 0.0,
        const amrex::Real y = 0.0,
        const amrex::Real z = 0.0,
        const int cpu = 0,
        const int id = 0) const noexcept
    {
```

`SmartCreate` 与 `AddPlasma()` 的关系是：它不是体注入主路径，而是给 ionization、collision、QED 等“运行中产生新粒子”的路径提供默认创建策略。它先写位置和 ID：

```cpp
#if defined(WARPX_DIM_3D)
        prt.m_rdata[PIdx::x][i_prt] = x;
        prt.m_rdata[PIdx::y][i_prt] = y;
        prt.m_rdata[PIdx::z][i_prt] = z;
#elif defined(WARPX_DIM_XZ) || defined(WARPX_DIM_RZ)
        prt.m_rdata[PIdx::x][i_prt] = x;
        prt.m_rdata[PIdx::z][i_prt] = z;
        amrex::ignore_unused(y);
#endif

        prt.m_idcpu[i_prt] = amrex::SetParticleIDandCPU(id, cpu);
```

再用策略表初始化其他固定和 runtime 属性：

```cpp
        for (int j = AMREX_SPACEDIM; j < PartData::NAR; ++j) {
            prt.m_rdata[j][i_prt] = initializeRealValue(m_policy_real[j], engine);
        }
        for (int j = 0; j < prt.m_num_runtime_real; ++j) {
            prt.m_runtime_rdata[j][i_prt] = initializeRealValue(m_policy_real[j+PartData::NAR], engine);
        }
```

因此，粒子创建系统有两条互补路径：

- 初始化/注入：`AddParticles -> AddPlasma/AddPlasmaFlux/AddNParticles`；
- 运行中二次产生：`SmartCreate`/`FilterCreateTransform`/碰撞与 QED 创建函数。

## 16. 本段初始化链的完整数据流

从本阶段阅读的源码看，species 初始化完整路径是：

```text
PhysicalParticleContainer::InitData()
  -> AddParticles(lev=0)
     -> single/multiple/gaussian/openPMD: AddNParticles()
     -> density-based injection: AddPlasma()
     -> flux-based injection during run: AddPlasmaFlux()

AddPlasma()
  -> find_overlap(tile, injection box)
  -> count candidate particles per cell
  -> scan counts to offsets
  -> reserve particle IDs and resize tile
  -> sample cell-local position with InjectorPosition
  -> query density with InjectorDensity
  -> sample momentum with InjectorMomentum
  -> transform boosted-frame density/momentum if needed
  -> compute macro weight
  -> initialize ionization/QED/user runtime attributes
  -> write PIdx::x/y/z/w/ux/uy/uz
  -> invalid candidates marked by invalid ID
  -> caller Redistribute cleans and places particles
```

这条链把物理模型和 HPC 数据结构连接起来：

- 物理层：数密度、通量、热分布、漂移、Lorentz boost、径向体积元；
- 数值层：cell 内采样、宏粒子权重、refined injection、density cut；
- 工程层：tile overlap、prefix scan、SoA 写入、invalid ID、runtime attributes、GPU/CPU 兼容。

后续如果要把初始化章节写入正式书稿，应把本笔记和 `02-plasma-injector.md`、`03-density-momentum-dispatch.md` 合并成“species 初始化”大章：先讲输入参数和物理模型，再讲 functor，再讲 kernel，再讲 openPMD、Gaussian beam、flux injection 的特殊路径。
