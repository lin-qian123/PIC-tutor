# Python 02: field registry, particle containers, boundary buffers, and PICMI access

绑定源码：

- `../warpx/Source/Python/WarpX.cpp`
- `../warpx/Source/Python/MultiFabRegister.cpp`
- `../warpx/Source/Python/Particles/MultiParticleContainer.cpp`
- `../warpx/Source/Python/Particles/WarpXParticleContainer.cpp`
- `../warpx/Source/Python/Particles/ParticleBoundaryBuffer.cpp`
- `../warpx/Python/pywarpx/fields.py`
- `../warpx/Python/pywarpx/extensions/MultiFabRegister.py`
- `../warpx/Python/pywarpx/picmi.py`

这篇聚焦 Python 如何真正访问 C++ runtime 数据：

1. fields
2. particle containers
3. boundary buffer
4. PICMI 高层 convenience property

## 1. fields 的真实入口已经不是旧 `MultiFabWrapper`

`pywarpx/fields.py` 开头就明确把 `MultiFabWrapper` 标成 obsolete：

- 推荐路径是：
  - `sim.fields.get(...)`
  - 或 `warpx.multifab_register()`

这和项目里已有的：

- [03-field-wrapper-validation-map.md](/Volumes/PHILIPS/programs/PIC/PIC-tutor/notes/code-reading/python/03-field-wrapper-validation-map.md)

是一致的。

因此当前 field access 的真实主链不是旧 wrapper，而是：

```text
WarpX::GetMultiFabRegister()
-> pybind MultiFabRegister
-> Python extension helpers
-> sim.fields.get(...)
```

## 2. `WarpX.cpp` 只把 registry/containers 借给 Python

在 `Source/Python/WarpX.cpp` 里，和数据访问最直接相关的绑定是：

- `multifab_register`
- `multi_particle_container`
- `get_particle_boundary_buffer`

这三条都用：

- `reference_internal`

返回内部对象。

所以 Python 并没有拿到数据副本，而是直接拿到 WarpX 当前 runtime 的活动对象视图。

## 3. `MultiParticleContainer` binding 的角色是全局 species 路由

`Source/Python/Particles/MultiParticleContainer.cpp` 当前只暴露了少量高价值入口：

- `get(name)`
- `set_plasma_lens_strength(...)`
- `get_charge_density(lev, local)`

这说明 `MultiParticleContainer` 在 Python 侧的真实职责是：

- 按 species 名字取容器
- 做少量全局多 species runtime 控制
- 提供整体电荷密度入口

它不是每个粒子操作都在这里完成的“大接口类”。

## 4. `WarpXParticleContainer` 才是粒子数据操作主接口

`Source/Python/Particles/WarpXParticleContainer.cpp` 暴露的功能可以分 4 类。

### 4.1 直接加粒子

- `add_n_particles(...)`

这里 pybind 会把 numpy arrays 先拷成 `amrex::Vector`，再调用：

- `AddNParticles(...)`

因此当前 Python 注粒子路径不是零拷贝，而是：

- Python array
- 转 `amrex::Vector`
- 再进 C++

### 4.2 统计量

- `sum_particle_weight(local)`
- `sum_particle_charge(local)`
- `sum_particle_energy(local)`

### 4.3 沉积和场派生

- `deposit_charge(rho, lev)`
- `deposit_current(mf_name, lev, dt, relative_time)`
- `get_charge_density(lev, local)`
- `get_number_density(lev)`

这条链说明 Python 不只是读粒子散点，还能直接驱动：

- 充电沉积
- 电流沉积
- 粒子数密度重建

### 4.4 species runtime switches

- `set_do_not_push`
- `set_do_not_gather`
- `set_do_not_deposit`

所以 Python 侧已经可以直接改 species runtime policy，而不只是后处理读取。

## 5. `particle_data_python` 这组 validation 正好验证上面这条链

项目里已有的：

- `particles/28-particle-diagnostics-python-interface-validation-map.md`

已经说明：

- `particle_data_python`
- `restart/inputs_test_2d_id_cpu_read_picmi.py`
- `restart/inputs_test_2d_runtime_components_picmi.py`

真正验证的是：

- runtime attributes
- `add_particles(...)`
- `get_real_comp_index(...)`
- 手动沉积接口
- `idcpu` 解包读取

也就是说，`WarpXParticleContainer.cpp` 这层不是“潜在能力”，而是已有强 regression 覆盖的 active contract。

## 6. boundary buffer 在 Python 侧是独立访问面

`Source/Python/Particles/ParticleBoundaryBuffer.cpp` 暴露两层对象：

1. `BoundaryBufferParIter`
2. `ParticleBoundaryBuffer`

`ParticleBoundaryBuffer` 的核心接口是：

- `clear_particles()`
- `get_particle_container(species_name, boundary)`
- `get_num_particles_in_container(species_name, boundary, local)`

这和 diagnostics 笔记里已经压实的语义一致：

- scraped particles 从主 species 删除后
- 会进入 boundary buffer
- Python 能独立读取、统计、再清空它

因此 boundary buffer 不是普通 `WarpXParticleContainer` 的附属字段，而是一条单独的数据访问面。

## 7. `sim.fields` 与 `sim.particles` 在 PICMI 里只是 convenience property

`pywarpx/picmi.py` 里：

- `fields`
  - 返回 `self.extension.warpx.multifab_register()`
- `particles`
  - 返回 `self.extension.warpx.multi_particle_container()`

因此 PICMI `Simulation` 的：

- `sim.fields`
- `sim.particles`

不是新对象层，而只是把底层 pybind runtime accessor 换成更方便的用户入口。

这点很关键，因为它说明：

- PICMI convenience API
- pybind registry/container API

底层其实是同一份运行态对象。

## 8. field wrapper validation 的真实对象是 register，而不是旧 wrapper

`python_wrappers` regression 当前的硬断言在：

- `inputs_test_2d_python_wrappers_picmi.py`

而它实际验证的是：

- `sim.fields.get(...)`
- valid-domain `E/B/F/G`
- `pml_E/B/F/G`

这说明 field access 主线真正需要记住的是：

- `MultiFabRegister.cpp`
- Python extension `MultiFabRegister.py`
- `sim.fields.get(...)`

而不是旧 `fields.py` 的 `MultiFabWrapper` 封装。

## 9. 当前 Python 访问层的最准确分层

把 Python data access 压成一张图，就是：

```text
WarpX singleton
-> multifab_register / multi_particle_container / particle_boundary_buffer
-> pybind class wrappers
-> Python extension helpers and PICMI convenience properties
-> user-side access: sim.fields, sim.particles, buffer readers
```

其中三条最重要的 active contract 分别是：

1. field access
   - `python_wrappers`
2. particle runtime attributes / deposition
   - `particle_data_python`
3. scraped-particle buffer access
   - `particle_boundary_scrape`

这三条已经足以把 `Python/` 从“只是个 binding 目录”提升成当前项目里有明确验证边界的 runtime interface layer。
