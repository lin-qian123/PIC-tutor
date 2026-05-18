# `particle_boundary_scrape`、`particle_data_python` 与 `particle_fields_diags` single-precision 的验证边界

绑定对象：

- `../warpx/Examples/Tests/particle_boundary_scrape`
- `../warpx/Examples/Tests/particle_data_python`
- `../warpx/Examples/Tests/particle_fields_diags`
- `../warpx/Python/pywarpx/particle_containers.py`
- `../warpx/Source/Python/Particles/WarpXParticleContainer.cpp`
- `../warpx/Source/Particles/PhysicalParticleContainer.cpp`

这一组条目都落在 `Particles` 的“diagnostics / Python interface validation”边界上，但它们验证的对象并不相同：

- `particle_boundary_scrape` 验证 scraped-particle removal 与 Python boundary-buffer wrapper
- `particle_data_python` 验证 Python 粒子属性访问、runtime attributes、手动沉积接口
- `particle_fields_diags` single-precision 变体验证的是 particle-field reductions 在单精度下的容差边界，但当前仍未在 CMake 中启用

---

## 1. `particle_boundary_scrape`：先验证 EB scraping 删除，再验证 Python buffer 包装器

### 1.1 native 输入与 analysis 的最小合同

`inputs_test_3d_particle_scrape` 构造的是一个很窄的电子束，朝着一个立方体 embedded boundary 前进：

```text
warpx.eb_implicit_function = "-max(max(max(x-12.5e-6,-12.5e-6-x), max(y-12.5e-6,-12.5e-6-y)), max(z-(-6.15e-5),-8.65e-5-z))"
electrons.uz = 2000.
electrons.save_particles_at_xhi = 1
electrons.save_particles_at_eb = 1
```

`analysis_scrape.py` 的断言非常克制，但很硬：

1. 第 40 步时，所有电子都还存在
2. 第 60 步时，所有电子都已被 EB 吸收并从主 species 中删除

对应断言就是：

```python
np40 = ds40.index.particle_headers["electrons"].num_particles
assert np40 == 612

np60 = ds60.index.particle_headers["electrons"].num_particles
assert np60 == 0
```

这条 regression 的第一层意义是：

- `ScrapeParticlesAtEB()` 的删除语义确实发生了
- 删除发生在粒子真正走到 EB 之后，而不是过早/过晚

但 native 入口并不直接检查 scraped buffer 内容。

### 1.2 PICMI 变体更强：它直接检查 `ParticleBoundaryBufferWrapper`

`inputs_test_3d_particle_scrape_picmi.py` 在 `sim.step(max_steps)` 之后，直接构造：

```python
particle_buffer = particle_containers.ParticleBoundaryBufferWrapper()
```

然后逐层检查：

1. EB buffer 中累计粒子数必须是 612
2. `stepScraped` 必须都大于 40
3. 汇总所有 rank 的 `w` 数组后，总粒子数仍是 612
4. `clear_buffer()` 之后，buffer size 必须回到 0

所以 PICMI 变体验证的是一条更长的链：

- `ParticleBoundaryBuffer.cpp` 把 scraped particles 连同 `stepScraped` 等属性写进 buffer
- `Source/Python/WarpX.cpp` 暴露 `get_particle_boundary_buffer()`
- `pywarpx/particle_containers.py::ParticleBoundaryBufferWrapper` 把底层 buffer 包装成 Python 可访问对象
- `get_particle_boundary_buffer_size(...)`
- `get_particle_boundary_buffer(...)`
- `clear_buffer()`

也就是说，`particle_boundary_scrape` 不是单纯“边界吸收后粒子没了”，而是两层合同一起测：

1. 主 species 内粒子确实被 EB scrape 并删除
2. 被删掉的粒子确实进入了 Python 可读/可清空的 boundary buffer

### 1.3 当前边界

这组 test 仍然不是 `BoundaryScrapingDiagnostics` 文件 writer 的最强入口。它没有直接验证：

- openPMD `particles_at_eb`
- flush 后自动清空 buffer

这些内容更接近 `Diagnostics` 目录里已经整理过的 `BoundaryScraping` 笔记。

这里验证的是粒子模块一侧的“scrape + Python wrapper”合同。

---

## 2. `particle_data_python`：真正验证的是 Python runtime attributes 和手动沉积接口

### 2.1 这组 test 没有独立 analysis 脚本

`particle_data_python/CMakeLists.txt` 里的三个条目都是：

- `analysis = OFF`
- 只保留 `analysis_default_regression.py --path diags/diag1000010`

所以它们的强断言不在外部 analysis，而是直接写在 PICMI 输入脚本里。

这点很重要：这是“输入脚本自检 + checksum 基线”的结构，不是传统的“跑完再交给 analysis.py”。

### 2.2 `inputs_test_2d_particle_attr_access_picmi.py` 在测什么

这份输入脚本显式走了 Python 粒子接口：

1. `sim.initialize_inputs()`
2. `sim.initialize_warpx()`
3. `electrons = sim.particles.get("electrons")`
4. `electrons.add_real_comp("newPid")`
5. 安装 `beforestep` callback，反复 `add_particles(...)`

后面又直接断言：

- `electrons.size` 是否等于各 rank 每步注入粒子数之和
- `get_real_comp_index("w") == 2`
- `get_real_comp_index("newPid") == 6`
- 遍历 tile 时每个 `pti["newPid"]` 都等于 5

并且还继续测了 Python 暴露出来的手动沉积接口：

```python
electrons.deposit_current(
    "current_fp", 0, sim.extension.warpx.getdt(0), -0.5 * sim.extension.warpx.getdt(0)
)
assert np.max(np.abs(sim.fields.get("current_fp", "x", 0)[...])) > 0
assert np.max(np.abs(sim.fields.get("current_fp", "z", 0)[...])) > 0
```

所以这条 regression 真正验证的是：

- Python 侧 `add_real_comp(...)` 能把新 runtime attribute 正确加到 species 上
- Python 侧 `add_particles(...)` 能把 builtin attrs 和新增 attrs 一起写入 WarpX SoA
- Python 侧 tile iterator 能正确读回这些 attrs
- `deposit_current(...)` 这个 Python wrapper 能触发 C++ 侧 `DepositCurrent(...)`

源码落点是：

- `pywarpx/particle_containers.py`
- `Source/Python/Particles/WarpXParticleContainer.cpp`

### 2.3 一个当前真实缺口：`--unique` 变体没有真正切换行为

`CMakeLists.txt` 里有一个名字看起来不同的条目：

```text
test_2d_particle_attr_access_unique_picmi
```

它通过命令行把 `--unique` 传给同一个输入脚本。

但当前脚本里真正调用 `add_particles(...)` 的地方仍然写死了：

```python
electrons.add_particles(
    ...,
    unique_particles=True,
)
```

也就是说，`args.unique` 当前并没有进入这个调用位点。

所以这条 “unique” 变体在当前 checkout 下更像是：

- 名义上存在的行为分叉
- 实际上尚未生效的 regression scaffold

这不该被误记成“已经覆盖 unique vs non-unique 两种注入语义”。

### 2.4 `inputs_test_2d_prev_positions_picmi.py` 在测什么

这份输入打开了：

```text
warpx_save_previous_position=True
```

随后直接在 Python 里验证：

- `prev_x` / `prev_z` 运行时属性索引是否存在
- 每个 tile 的 `prev_z` 值都落在合理范围内
- 返回粒子数是否和本地粒子数一致

对应源码链是：

- `pywarpx/picmi.py` 把 `warpx_save_previous_position` 传进 species
- `PhysicalParticleContainer.cpp` 构造期按维度添加 `prev_x/prev_y/prev_z`
- `PushPX()` 在推进前先把当前位置抄到这些旧位置数组里

所以 `prev_positions_picmi` 验证的是：

- Python 参数到 C++ runtime attributes 的接线
- 旧位置缓存是否真的在推进前被保存

它不是“粒子轨道正确性分析”，而是 `save_previous_position` 这条 Python-to-runtime-attribute 合同的验证。

### 2.5 `inputs_test_2d_id_cpu_read_picmi.py`：`idcpu` 解包读取合同

`restart/inputs_test_2d_id_cpu_read_picmi.py` 虽然挂在 `restart/` 目录里，但它当前真正验证的不是 restart 保真，而是 Python 侧能否正确读出 WarpX 粒子的 `idcpu` 打包字段。

脚本结构很克制：

1. 用 PICMI 建一个 2D electrostatic 最小骨架；
2. 在 `beforestep` callback 里稳定加入 10 个电子；
3. 跑完后遍历
   - `pti["idcpu"]`
   - `libwarpx.amr.unpack_ids(...)`
   - `libwarpx.amr.unpack_cpus(...)`
4. 直接断言：
   - `ids_sum == 5050`
   - `cpu_sum == 0`

所以这条 test 的真正合同是：

- Python tile iterator 能读到 `idcpu`
- `unpack_ids/unpack_cpus` 这条 wrapper 能正确解包底层粒子标识
- 单 rank 下 callback 注入粒子的 `id` 分配与 `cpu` 归属保持可预期

它不该被误写成“普通 restart checksum”。

### 2.6 `inputs_test_2d_runtime_components_picmi.py`：动态 runtime attrs 与 checkpoint scaffold

`restart/inputs_test_2d_runtime_components_picmi.py` 则更接近 `particle_data_python` 的延长线。它在 PICMI 输入脚本里直接做：

1. `electrons.add_real_comp("newPid")`
2. `beforestep` callback 里持续 `add_particles(..., newPid=5.0)`
3. 跑完后断言：
   - `electrons.size == 90`
   - `get_real_comp_index("w") == 2`
   - `get_real_comp_index("newPid") == 6`
   - 每个 tile 的 `pti["newPid"]` 都等于 `5`

它的核心验证对象是：

- Python runtime attribute 动态注册
- callback 粒子注入时新增组件随粒子一同写入
- Python tile iterator 能在运行后正确读回这些组件

这条输入同时还显式挂了：

- `picmi.Checkpoint(name="chk", period=5)`
- `amr.restart=...` 参数解析

并且 `CMakeLists.txt` 里保留了：

- `test_2d_runtime_components_picmi`
- `test_2d_runtime_components_picmi_restart`

其中 restart 变体当前仍是 `FIXME` 状态，`analysis` 和 `checksum` 都没有启用。所以当前最准确的写法是：

- 主 test：强脚本内自检 + checksum 基线
- restart 变体：存在 checkpoint/restart scaffold，但尚未成为活跃 regression

---

## 3. `particle_fields_diags` single-precision：脚本已存在，但 regression 仍未启用

### 3.1 当前 CMake 状态

`particle_fields_diags/CMakeLists.txt` 里，双精度条目是活跃的：

```text
test_3d_particle_fields_diags
```

但单精度条目仍然被整段注释掉：

```text
# FIXME
#add_warpx_test(
#    test_3d_particle_fields_diags_single_precision
#    ...
#    "analysis_particle_diags_single.py diags/diag1000200"
#    "analysis_default_regression.py --path diags/diag1000200 --rtol 1e-3"
#)
```

所以当前真实状态不是“单精度已经被稳定覆盖”，而是：

- analysis 脚本存在
- 容差策略存在
- CMake regression 仍未恢复

### 3.2 single-precision analysis 实际做了什么

`analysis_particle_diags_single.py` 本身只是：

```python
an.do_analysis(single_precision=True)
```

真正逻辑都复用 `analysis_particle_diags_impl.py`，只是把容差从双精度的

```python
tolerance = 1e-12
```

放宽到：

```python
tolerance = 5e-3
```

因此单精度版本要验证的对象并没有变化，仍然是：

- `particle_fields_to_plot`
- parser reduction
- `.filter(...)`
- `.do_average`
- plotfile/openPMD 一致性

只是承认：

- 单精度下这条 reduction/writer 链需要显著更宽的误差带

### 3.3 当前能得出的保守结论

在当前本地 checkout 里，`particle_fields_diags` single-precision 最准确的表述应当是：

- 这是一个“已经准备好 analysis 入口，但尚未恢复到活跃 CMake regression”的保留验证项
- 不能把它写成“已有稳定单精度回归”
- 也不能把它误读成“完全没有单精度考虑”

---

## 4. 这组 regression 对 `Particles` 章节的真实补充

把这三组条目并到一起看，补上的不是新的粒子物理，而是三类接口合同：

1. `particle_boundary_scrape`
   - scraped particles 怎样从主 species 删除，并进入 Python 可访问的 boundary buffer
2. `particle_data_python`
   - Python wrapper 怎样新增 runtime attributes、注入粒子、读回 tile arrays、手动触发沉积
3. `particle_fields_diags` single-precision
   - 粒子 diagnostics reduction 在单精度下已有 analysis 预案，但尚未恢复为活跃回归

所以它们更适合被记成：

- `Particles` 的 diagnostics / Python-interface validation 层

而不是再混回单粒子 pusher 或普通边界条件测试。
