# `Particles` 验证入口：`particle_fields_diags`、`plasma_lens`、`pass_mpi_communicator`

绑定源码：

- `../warpx/Examples/Tests/particle_fields_diags`
- `../warpx/Examples/Tests/plasma_lens`
- `../warpx/Examples/Tests/pass_mpi_communicator`
- `../warpx/Source/Diagnostics/Diagnostics.cpp`
- `../warpx/Source/Diagnostics/FullDiagnostics.cpp`
- `../warpx/Source/Particles/Gather/GetExternalFields.H`
- `../warpx/Source/Particles/Gather/GetExternalFields.cpp`
- `../warpx/Source/Particles/MultiParticleContainer.cpp`
- `../warpx/Python/pywarpx/picmi.py`
- `../warpx/Python/pywarpx/_libwarpx.py`

这一组条目也不能统称为“普通粒子物理 regression”。

- `particle_fields_diags`：验证的是 diagnostics 从粒子生成 cell-centered fields 的合同。
- `plasma_lens`：验证的是 external particle fields 里的 plasma lens 路径，不是普通自洽场推进。
- `pass_mpi_communicator`：当前是一个待恢复的 Python/MPI 接口入口，CMake 中 analysis/checksum 都没有启用。

## 1. `particle_fields_diags`：`particle_fields_to_plot` 的 writer 合同

`inputs_test_3d_particle_fields_diags` 建的是一个最小多 species 场景：

- `electrons`
- `protons`
- `photons`
- periodic 3D
- `algo.current_deposition = esirkepov`
- `warpx.use_filter = 1`
- `warpx.synchronize_velocity_for_diagnostics = 1`

关键不在轨道，而在 diagnostics 配置：

```text
diag1.particle_fields_to_plot = z uz uz_filt zuz jz
diag1.particle_fields_species = electrons protons photons
diag1.particle_fields.z(x,y,z,ux,uy,uz) = z
diag1.particle_fields.uz(x,y,z,ux,uy,uz) = uz
diag1.particle_fields.uz_filt(x,y,z,ux,uy,uz) = uz
diag1.particle_fields.uz_filt.filter(x,y,z,ux,uy,uz) = (uz < 0)
diag1.particle_fields.zuz(x,y,z,ux,uy,uz) = z * uz
diag1.particle_fields.jz(x,y,z,ux,uy,uz) = uz*q_e
diag1.particle_fields.jz.do_average = 0
```

analysis 不是只读 plotfile，而是三向对照：

1. 用 `yt` 从粒子数据手工重建 cell-centered quantity。
2. 读 Full plotfile 中的 `boxlib` particle-fields meshes。
3. 再读 openPMD 中同名 meshes。

然后比较：

- `zavg`
- `uzavg`
- `zuzavg`
- `uzavg_filt`
- `jz`

对每个 species 都要求 plotfile 与 openPMD 同时贴合手工重建值。

因此它真正验证的是：

- `Diagnostics.cpp` 对 `particle_fields_to_plot`
- `<diag>.particle_fields_species`
- `<diag>.particle_fields.<name>.do_average`
- `<diag>.particle_fields.<name>.filter(...)`
  的参数解析
- `FullDiagnostics.cpp` / `ParticleReductionFunctor`
  把粒子聚合成 cell-centered field 的实现
- plotfile 与 openPMD writer 在这一层的输出一致性

这条 test 应归类为：

- particle diagnostics / particle-to-mesh reductions / plotfile-openPMD consistency

而不是泛泛的“particle pusher”或“single particle”。

## 2. `plasma_lens`：external particle field 的解析对照

`plasma_lens/analysis.py` 直接给出了这组 test 的本质：它不是检查自洽电磁波，而是把两颗测试电子穿过一串 plasma lenses，然后把最终横向位置和横向动量与解析薄透镜串联模型比较。

analysis 的逻辑是：

1. 从 diagnostics 里取两颗电子最终 `(x,y,z,ux,uy)`。
2. 从输入参数恢复 lens 序列。
3. 用 `applylens(...)` 逐段解析推进。
4. 最后比较：
   - `x`
   - `y`
   - `ux`
   - `uy`

标准容差大致是：

- 位置 `2e-2`
- 速度 `2e-3`

短透镜版本再稍微放宽。

### 2.1 `repeated_plasma_lens` 分支

普通输入、boosted 输入、short 输入和 Python 原生输入，核心都在走：

- `particles.E_ext_particle_init_style = repeated_plasma_lens`
- `particles.B_ext_particle_init_style = repeated_plasma_lens`

真实源码入口是：

- `MultiParticleContainer.cpp`
  负责读取
  - `repeated_plasma_lens_period`
  - `repeated_plasma_lens_starts`
  - `repeated_plasma_lens_lengths`
  - `repeated_plasma_lens_strengths_E/B`
- `GetExternalEBField`
  在粒子 gather 之后、push 之前按粒子位置实时加 lens focusing field

所以这条 regression 真正验证的是：

- external particle fields 的 repeated-plasma-lens 元数据装配
- `GetExternalEBField` 中按粒子 `z` 位置选 lens、并在 lens 内做 residence-fraction 修正的实现
- boosted-frame 下分析端把 `z` 反变换回 lab frame 后，解析模型仍成立

### 2.2 `hard_edged` / lattice 分支

`inputs_test_3d_plasma_lens_hard_edged` 没走 `repeated_plasma_lens`，而是：

- `lattice.elements = ...`
- `plasmalens*.type = plasmalens`
- `plasmalens*.dEdx = ...`

这条路径把 test 切到了 accelerator lattice 分支：

- `AcceleratorLattice`
- `HardEdgedPlasmaLens`
- `LatticeElementFinder`

analysis 仍复用同一个解析对照脚本，因此它本质上是在验证：

- `repeated_plasma_lens`
- accelerator-lattice hard-edged lens

这两套外部粒子场入口在最终粒子动力学上是否一致。

### 2.3 这组 regression 的真实分类

因此 `plasma_lens` 这组最准确的口径应是：

- external particle fields / repeated plasma lens / accelerator lattice lens / boosted consistency

而不是笼统地塞进 `general / to classify`。

## 3. `pass_mpi_communicator`：当前是未启用的 Python/MPI 接口占位

这一组最容易被误记成“已有 regression，只是没细读”。实际上当前不是。

`inputs_test_2d_pass_mpi_comm_picmi.py` 做了三件事：

1. 用 `mpi4py` 把 `COMM_WORLD` 按 rank 拆成两个 communicator。
2. 给不同 communicator 配不同 plasma density。
3. 计划把 `new_comm` 传给
   `sim.step(max_steps, mpi_comm=new_comm)`，
   然后验证 WarpX 侧看到的 `NProcs` 和 rank 映射是否正确。

但关键代码现在全被注释掉了。原因源码里也能直接看到：

- `pywarpx/picmi.py`
  允许 `Simulation.initialize_warpx(mpi_comm=...)`
  和 `Simulation.step(..., mpi_comm=...)`
- 但 `_libwarpx.py`
  里 `amrex_init(self, argv, mpi_comm=None)` 对非空 `mpi_comm` 直接：
  `raise Exception("mpi_comm argument not yet supported")`

因此 CMake 里对应条目是：

- `analysis = OFF`
- `checksum = OFF`

这意味着当前它不应被归类成一个“已有 analysis/checksum 的 regression”，而应被归类成：

- Python API / MPI communicator handoff / currently disabled test scaffold

analysis.py 本身也不是对参考答案做比较，而是比较两个 plotfile 的 checksum 是否不同。它的预期语义是：

- 如果两个 communicator 真被正确分开运行
- 不同密度就应该产生不同结果
- 两个 plotfile 的 checksums 不应相同

但由于 `mpi_comm` 传递目前没有启用，这条 analysis 现在不会进入 CMake 主回归。

## 4. 哪些应回填第 4 章

这三组里，适合回填第 4 章 `Particles` 正文的只有前两类：

1. `particle_fields_diags`
   - 因为它直接消费粒子位置、动量和 species 数据
   - 能说明“粒子数据如何在 diagnostics 层再投影成 field-like meshes”
2. `plasma_lens`
   - 因为它直接连接 external particle fields 与 `PushPX()`
   - 能说明 repeated-plasma-lens / lattice lens 不是主网格场，而是粒子侧外场

`pass_mpi_communicator` 则更适合留在 regression 索引和工程状态说明里，不需要占第 4 章正文篇幅。它验证的是 Python/MPI 初始化接口，而不是粒子物理算法。

## 5. 当前验证边界

这轮阅读后，这三组 test 的边界可以压实成：

- `particle_fields_diags`
  - 有强 analysis
  - 验证粒子到 diagnostics mesh 的 reduction 合同，以及 plotfile/openPMD 一致性
- `plasma_lens`
  - 有强 analysis
  - 验证 repeated-plasma-lens 与 hard-edged lattice lens 两条 external particle field 路径
- `pass_mpi_communicator`
  - 当前不是活跃 regression
  - 是一个因 `mpi_comm` 尚未支持而被禁用的 Python/MPI 接口脚手架

因此后续书稿或索引里如果要写“这些测试在验证什么”，最保守且准确的说法就是：

- `particle_fields_diags`：粒子 diagnostics 约束
- `plasma_lens`：粒子侧外场 / lens 约束
- `pass_mpi_communicator`：当前禁用的 communicator handoff 工程入口
