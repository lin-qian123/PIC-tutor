# `BoundaryScrapingDiagnostics`、`ParticleBoundaryBuffer` 与 Python scraped-particle 接口

绑定源码：

- `../warpx/Source/Diagnostics/BoundaryScrapingDiagnostics.H`
- `../warpx/Source/Diagnostics/BoundaryScrapingDiagnostics.cpp`
- `../warpx/Source/Diagnostics/Diagnostics.cpp`
- `../warpx/Source/Diagnostics/MultiDiagnostics.cpp`
- `../warpx/Source/Python/WarpX.cpp`
- `../warpx/Source/Python/Particles/ParticleBoundaryBuffer.cpp`
- `../warpx/Python/pywarpx/particle_containers.py`
- `../warpx/Python/pywarpx/picmi.py`
- `../warpx/Docs/source/usage/parameters.rst`
- `../warpx/Docs/source/usage/workflows/python_warpx.rst`
- `../warpx/Docs/source/usage/workflows/python_particle_boundary_data.rst`

前面几篇已经把 scraped particle buffer 的生产侧讲清了：domain boundary 在 `ApplyBoundaryConditions()` 之后、`deleteInvalidParticles()` 之前收集；EB 路径会回溯到 `phi=0` 真实交点，并记录 `step/time/normal` 元数据。这一篇只回答消费侧：

1. `BoundaryScrapingDiagnostics` 怎样把 buffer 写成 diagnostics；
2. Python 怎样直接读同一个 buffer；
3. diagnostics 和 Python 混用时，谁负责清空 buffer。

## 1. `BoundaryScraping` 是单独的 diagnostics 类型，不是 full diagnostics 的变体

`MultiDiagnostics` 读到：

```cpp
diag_type_str == "BoundaryScraping"
```

时，会直接创建：

```cpp
alldiags[i] = std::make_unique<BoundaryScrapingDiagnostics>(i, diags_names[i], diags_types[i]);
```

这说明 boundary scraping 在 WarpX 里是单独的 diagnostics 分支，而不是普通 plotfile/openPMD 输出再加一个过滤器。

## 2. 它明确声明自己“不处理 fields，只处理 particles”

`BoundaryScrapingDiagnostics::ReadParameters()` 先把基类默认字段输出关掉：

```cpp
m_varnames_fields = {};
m_varnames = {};
```

然后把 buffer 数量设成：

```cpp
m_num_buffers = AMREX_SPACEDIM*2;
if (eb_enabled) { m_num_buffers += 1; }
```

因此它的输出对象不是 level field data，而是：

- 每个维度的 `lo/hi` domain boundary；
- 若启用 EB，再加一个 `eb` boundary。

这也解释了为什么它的：

- `InitializeFieldFunctors()`
- `InitializeBufferData()`
- `DoComputeAndPack()`

都几乎是空实现。它根本不走普通 field diagnostics 的打包路径。

## 3. 它真正做的初始化动作，是把 diagnostics species 句柄指向 `ParticleBoundaryBuffer`

关键函数是：

```cpp
void BoundaryScrapingDiagnostics::InitializeParticleBuffer (const MultiParticleContainer& mpc)
```

这里先处理 species 选择：

```cpp
if (m_output_species_names.empty()) {
    m_output_species_names = mpc.GetSpeciesNames();
}
```

也就是用户不指定 species 时，默认输出所有 species。

然后对每个 boundary、每个 species，直接取出 boundary buffer 容器：

```cpp
WarpXParticleContainer::Base* bnd_buffer =
    particle_buffer.getParticleBufferPointer(species_name, i_buffer);
m_output_species[i_buffer].push_back(ParticleDiag(m_diag_name, species_name, pc, bnd_buffer));
```

这里最重要的事实是：`ParticleDiag` 绑定的不是主粒子容器，而是 `ParticleBoundaryBuffer` 里那个 boundary-specific 的 species 容器。`BoundaryScrapingDiagnostics` 不重新扫描主粒子数组，而是直接消费先前已经收集好的 scraped event。

## 4. 它当前只支持 openPMD

`ReadParameters()` 里有两个硬约束。

第一，WarpX 必须编译 openPMD：

```cpp
#ifndef WARPX_USE_OPENPMD
    WARPX_ABORT_WITH_MESSAGE(...)
#endif
```

第二，diagnostics 格式必须是 `openpmd`：

```cpp
WARPX_ALWAYS_ASSERT_WITH_MESSAGE(
    m_format == "openpmd",
    error_string);
```

因此 `BoundaryScrapingDiagnostics` 当前不是通用 diagnostics writer，而是一个 openPMD-only 的 scraped-particle 输出器。

它还支持：

```cpp
<diag_name>.intervals
```

用来控制多久 flush 一次；官方参数文档说明默认是在模拟末尾统一写出。

## 5. Flush 的真实语义是“按 boundary 写目录，然后清空这个 boundary 的 buffer”

`BoundaryScrapingDiagnostics::Flush(i_buffer, ...)` 先统计当前 boundary 上累计的粒子数：

```cpp
n_particles += particle_buffer.getNumParticlesInContainer(species_name, i_buffer, false);
```

若为 0 就直接返回。

若非 0，则写到：

```cpp
const std::string file_prefix =
    m_file_prefix + "/particles_at_" + particle_buffer.boundaryName(i_buffer);
```

因此输出天然分成：

- `particles_at_xlo`
- `particles_at_xhi`
- `particles_at_zlo`
- `particles_at_eb`

等子目录。

更关键的是写完后它立刻执行：

```cpp
particle_buffer.clearParticles(i_buffer);
```

也就是说，`BoundaryScrapingDiagnostics` 不是只读观察者，而是带消费语义的 sink。它会在 flush 后主动清空对应 boundary 的 in-memory buffer。

## 6. Python 侧暴露的是同一个底层 `ParticleBoundaryBuffer`

C++ pybind 层只是把 WarpX 单例内部的对象直接暴露出去：

```cpp
.def("get_particle_boundary_buffer",
    [](WarpX& wx){ return &wx.GetParticleBoundaryBuffer(); },
    py::return_value_policy::reference_internal
)
```

所以 `sim.extension.get_particle_boundary_buffer()` 得到的不是副本，而是 WarpX 内部那一份 `ParticleBoundaryBuffer` 本体。

`Source/Python/Particles/ParticleBoundaryBuffer.cpp` 暴露了三个原语：

- `clear_particles`
- `get_particle_container(species_name, boundary)`
- `get_num_particles_in_container(species_name, boundary, local)`

而 Python 高层 `ParticleBoundaryBufferWrapper` 只是把这些原语包装成更方便的接口。

## 7. Python 里的 boundary 字符串会按几何维度映射成整数槽位

用户传入的边界名是：

- `x_lo`
- `x_hi`
- `z_lo`
- `eb`

但 wrapper 会调用 `_get_boundary_number(boundary)` 做映射。

规则是：

- 3D: `x/y/z -> 0/1/2`，因此 `eb = 6`
- 2D 或 RZ: `x/z -> 0/1`，因此 `eb = 4`
- 1D: `z -> 0`，因此 `eb = 2`

所以 Python 侧的 `"eb"` 不是特殊容器，只是 `AMREX_SPACEDIM*2` 后面那个附加 boundary slot。

## 8. `get_particle_boundary_buffer()` 返回的是 zero-copy 视图，不是快照

`ParticleBoundaryBufferWrapper.get_particle_boundary_buffer(...)` 会拿到：

```python
part_container = self.particle_buffer.get_particle_container(
    species_name, self._get_boundary_number(boundary)
)
```

然后按 `comp_name` 去 `real_soa_names` 或 `int_soa_names` 里找列，并返回：

```python
xp.array(soa.get_real_data(comp_idx), copy=False)
xp.array(soa.get_int_data(comp_idx), copy=False)
```

因此几个边界必须记住：

- 返回的是 numpy/cupy 视图，不是复制；
- 写这些数组会直接改底层 boundary buffer；
- `comp_name` 不只可以取 `x/y/z/ux/uy/uz/w`，也可以取：
  - `stepScraped`
  - `deltaTimeScraped`
  - `timeScraped`
  - 对 `eb` 还可以取 `nx/ny/nz`

这和 openPMD diagnostics 的语义完全不同。diagnostics 是落盘并清空；Python 是直接暴露当前内存态。

## 9. `get_particle_scraped_this_step()` 只是用 `stepScraped` 做筛选

这个高层方法先取当前步号：

```python
current_step = libwarpx.libwarpx_so.get_instance().getistep(level)
```

再分别取：

- 请求的 `comp_name`
- `stepScraped`

最后做：

```python
data[step == current_step]
```

所以它不是另一个“本步专用 buffer”，只是对累计 buffer 用 `stepScraped` 过滤一次。

这正是官方 `secondary_ion_emission` 示例能在每步 callback 中只处理本步刚撞边界粒子的原因。

## 10. Python 路径要求用户手动清空；diagnostics 路径会自动清空

官方参数文档明确写了：若通过 Python 访问 scraped particle buffer，需要用户自己调用：

```python
buffer.clear_buffer()
```

否则 buffer 会持续增长，可能造成内存问题。

这和 `BoundaryScrapingDiagnostics::Flush()` 的行为正好相反：

- Python 路径：用户自己决定何时读、何时清；
- diagnostics 路径：按 `intervals` 或 last-timestep flush，写完就清。

因此这两条消费链虽然指向同一份 `ParticleBoundaryBuffer`，但生命周期管理责任完全不同。

## 11. `diag_lo/diag_hi` 这类 reduced-domain 粒子输出目前并不支持 particle buffer

`Diagnostics::InitData()` / `InitDataAfterRestart()` 里还有一条容易忽略的基类限制。

如果用户给 diagnostics 指定了 `diag_lo` 或 `diag_hi`，基类会直接：

```cpp
m_output_species.at(i_buffer).clear();
```

并给出警告，说明 reduced-domain diagnostics 目前不支持 particle I/O。源码注释更直接：

```cpp
// This is a temporary fix until particle_buffer is supported in diagnostics.
```

因此 `BoundaryScrapingDiagnostics` 虽然是粒子 diagnostics，但仍继承这条边界。它不能简单理解成“任意局部窗口下的 scraped-particle 裁剪器”。

## 12. PICMI 已经把它封装成单独的高层对象

`pywarpx.picmi` 里已经有：

```python
class ParticleBoundaryScrapingDiagnostic(...)
```

它暴露了：

- `warpx_format`
- `warpx_openpmd_backend`
- `warpx_openpmd_encoding`
- `warpx_file_prefix`
- `warpx_random_fraction`
- `warpx_uniform_stride`
- `warpx_plot_filter_function`
- `warpx_dump_last_timestep`

因此 PICMI 用户不需要手写底层 `diag_type=BoundaryScraping`，这条链已经被显式抬到了 Python 配置层。

## 13. 最容易踩坑的事实：Python 和 diagnostics 如果同时开，实际是在竞争同一份 buffer

把源码链拼起来，可得出一个很具体的结论：

1. 生产侧把 scraped event 放进 `WarpX::GetParticleBoundaryBuffer()`。
2. `BoundaryScrapingDiagnostics` flush 时从这里写 openPMD，并 `clearParticles(i_buffer)`。
3. Python `ParticleBoundaryBufferWrapper` 读的也是这同一份对象。

所以如果两者同时启用，用户必须清楚：

- diagnostics flush 之后，Python 再读只能看到后续新积累的数据；
- Python 若提前改写底层数组，也会影响 diagnostics 最终写出的内容；
- Python 不清 buffer 会积累内存，但 diagnostics 的定期 flush 会替它清掉部分 boundary buffer。

这不是“两个接口看同一份历史文件”，而是“两个消费者操作同一份内存状态”。

## 14. 对书稿的直接结论

这一层最重要的不是“又多了一个 diagnostics 类型”，而是三个实际边界：

- `BoundaryScrapingDiagnostics` 只写 particles，不写 fields，而且当前只支持 openPMD；
- Python wrapper 与 diagnostics 共用同一个 `ParticleBoundaryBuffer`，不是两份独立数据；
- 清空责任取决于消费路径，混用时必须显式考虑 flush 时机。

如果不把这几点写清，读者很容易误以为：

- `save_particles_at_*` 会自动生成独立文件；
- Python 读到的是 diagnostics 文件的镜像；
- `get_particle_scraped_this_step()` 背后存在“本步专用队列”。

源码表明这三种理解都不对。
