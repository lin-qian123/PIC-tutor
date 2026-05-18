# `Laser` 验证入口地图：哪些 tests 真在验证什么

绑定源码：

- `../warpx/Examples/Tests/laser_injection/`
- `../warpx/Examples/Tests/laser_injection_from_file/`
- `../warpx/Examples/Physics_applications/laser_acceleration/`
- `../warpx/Examples/Tests/boosted_diags/`

## 1. 这一篇解决什么问题

前面三篇已经把 laser 的源码链打通了，但如果不把 regression 证据层压实，就很容易把所有 laser tests 都笼统地归类成“能跑起来”。

当前本地 WarpX checkout 里，laser 相关 tests 实际上分成三类：

1. 真正对注入场包络或频率做物理断言的 tests
2. 对 downstream 物理量做断言，但 laser 只是驱动器的 tests
3. 几乎只靠 checksum 的工程/工作流变体

这一篇把这些边界分开。

## 2. `Examples/Tests/laser_injection/`：注入本体的主验证

### 2.1 1D / 2D 是真正的物理断言

`laser_injection/CMakeLists.txt` 注册：

- `test_1d_laser_injection`
- `test_2d_laser_injection`
- `test_3d_laser_injection`
- `test_1d_laser_injection_implicit`
- `test_2d_laser_injection_implicit`

其中 1D/2D 的 analysis 不是 checksum 占位，而是直接：

- 从最终场提取 laser field
- 用 Hilbert transform 求 envelope
- 与理论 Gaussian 包络逐点比较
- 再用 FFT 检查主频是否等于 `c / wavelength`

因此这组 tests 的硬断言对象是：

1. `GaussianLaserProfile::fill_amplitude()`
2. `LaserParticleContainer` 的人工天线粒子沉积链
3. Maxwell solver 接收该电流后生成的传播场

### 2.2 implicit 变体不是“只有 checksum”

`test_1d_laser_injection_implicit` 和 `test_2d_laser_injection_implicit` 在 CMake 里继续复用：

- `analysis_1d.py`
- `analysis_2d.py`

源码位置：`laser_injection/CMakeLists.txt:33-50`。

这意味着它们并不是“只验证 implicit 能跑完”。它们对 implicit 路径的要求更强：

- 在 `semi_implicit_em + newton + gmres` 组合下
- 人工天线粒子更新和沉积之后
- 仍然必须得到与显式路径同一口径的包络与主频

所以 implicit laser injection 的验证边界是：

- 有真实场断言
- 但只覆盖 1D/2D
- 3D implicit 这里没有对应条目

### 2.3 3D `laser_injection` 仍主要依赖 checksum

`test_3d_laser_injection` 虽然也有 `analysis_3d.py`，但脚本本身只是生成 `laser_analysis.png`，没有 assert 任何物理量。

因此 3D `laser_injection` 的真实验证结构是：

- 有 analysis 文件
- 但 analysis 不构成硬物理断言
- 实际仍主要依赖 checksum

这是一个必须明确写出来的弱点，不能把“analysis 文件存在”误说成“3D 注入场已被解析验证”。

这里还要单独记一条 helper 边界：目录里的 `analysis_default_regression.py` 只是本地 checksum helper 副本，代码与顶层 `Examples/analysis_default_regression.py` 同构。它的职责是：

- 自动识别 plotfile / openPMD
- 按当前测试目录名调用 `evaluate_checksum(...)`
- 给 1D/2D/3D 以及 implicit laser-injection 变体提供历史输出基线

它不增加新的 laser 物理断言，因此不能和 `analysis_1d.py` / `analysis_2d.py` 的 envelope/frequency analysis 混成同一层。

## 3. `Examples/Tests/laser_injection_from_file/`：文件驱动 profile 的主验证

这一组 tests 在前一篇已经做过一轮梳理。这里强调它在整个验证版图中的位置：

- 它是 `from_file` 后端最强的一组 regression
- 1D/2D/3D/RZ 都有 envelope + frequency 双断言
- binary、Cartesian lasy、RZ `thetaMode` lasy、boosted-frame 变体都覆盖到了

所以如果问题是：

- `lasy_file_name` 读对没
- `binary_file_name` 读对没
- `time_chunk_size/delay/update(t)` 是否破坏了注入场

当前最直接的证据仍然是 `laser_injection_from_file/`，不是 `laser_acceleration/`

这一组还必须分清两类脚本：

1. 真正的注入后 analysis
   - `analysis_1d.py`
   - `analysis_1d_boost.py`
   - `analysis_2d.py`
   - `analysis_2d_binary.py`
   - `analysis_3d.py`
   - `analysis_rz.py`
   - `analysis_from_RZ_file.py`
2. 只负责生成输入文件的 prepare 脚本
   - `inputs_test_*_prepare.py`

prepare 脚本在 `CMakeLists.txt` 里都注册成独立 dependency，且统一是：

- `analysis = OFF`
- `checksum = OFF`

它们的职责不是做物理断言，而是给主 test 预生成外部 laser 文件。

### 3.1 `analysis_default_regression.py` 只是 `from_file` 家族的 checksum helper

和 `laser_injection/` 一样，`laser_injection_from_file/analysis_default_regression.py` 只是本地 checksum helper 副本。它为：

- lasy 1D/2D/3D
- boosted lasy
- RZ lasy
- RZ `thetaMode` lasy
- legacy binary

这些变体提供历史输出基线，但不替代各自 analysis 对 envelope / FFT 主频的强断言。

### 3.2 prepare 脚本本质上是“外部 laser 文件生成器”

这批 prepare 脚本当前可以分成三类：

1. 普通 Gaussian lasy 文件生成
   - `inputs_test_1d_laser_injection_from_lasy_file_prepare.py`
   - `inputs_test_1d_laser_injection_from_lasy_file_boost_prepare.py`
   - `inputs_test_2d_laser_injection_from_lasy_file_prepare.py`
   - `inputs_test_3d_laser_injection_from_lasy_file_prepare.py`
   - `inputs_test_rz_laser_injection_from_lasy_file_prepare.py`
   - 都用 `Laser(dim="xyt") + GaussianProfile(...)`
   - 都写出 `gaussian_laser_3d`
2. legacy binary 文件生成
   - `inputs_test_2d_laser_injection_from_binary_file_prepare.py`
   - 手工按 WarpX binary 格式写出 `gauss_2d`
   - 这条线专门锚定 `binary_file_name` 后端
3. RZ `thetaMode` lasy 文件生成
   - `inputs_test_rz_laser_injection_from_RZ_lasy_file_prepare.py`
   - 用 `CombinedLongitudinalTransverseProfile` 和 `LaguerreGaussianTransverseProfile`
   - 写出 `laguerre_laser_RZ`
   - 专门给 `analysis_from_RZ_file.py` 和 `internal_fill_amplitude_uniform_cylindrical` 路径供输入

因此这批 `prepare.py` 不应再写成“待读取输入文件”，而应明确记录为：

- `prepare -> inject -> analysis`

三段式回归链的前置产物生成阶段。

## 4. `Examples/Physics_applications/laser_acceleration/`：多数是下游物理场景，不是注入场单元测试

### 4.1 大多数条目只有 checksum

`laser_acceleration/CMakeLists.txt` 显示，大多数变体都配置为：

- `analysis = OFF`
- `checksum = analysis_default_regression.py --path ...`

典型条目包括：

- `test_1d_laser_acceleration`
- `test_1d_laser_acceleration_picmi`
- `test_2d_laser_acceleration_boosted`
- `test_2d_laser_acceleration_mr`
- `test_2d_laser_acceleration_mr_picmi`
- `test_3d_laser_acceleration`
- `test_3d_laser_acceleration_python`
- `test_3d_laser_acceleration_picmi`
- `test_3d_laser_acceleration_single_precision_comms`
- `test_rz_laser_acceleration`
- `test_rz_laser_acceleration_picmi`

因此这些条目的真正语义是：

- 它们验证的是某个完整 LWFA/LPI 工作流在当前实现下的数值结果不漂移
- 不是把 laser 注入本身单独拿出来做解析断言

### 4.2 `analysis_1d_fluid_boosted.py` 是少数真正有理论对照的场景

`test_1d_laser_acceleration_fluid_boosted` 会调用 `analysis_1d_fluid_boosted.py`。

这个脚本不是在看 laser 包络，而是在 1D boosted fluid WFA 模型下：

- 求解理论 ODE
- 对比 `Ez`
- 对比 `Jz`
- 对比 `rho`
- 再构造 `Vz/c`

最后要求最大相对误差低于 `0.30`。

因此它验证的是：

1. laser 作为驱动器是否和 fluid-plasma / boosted-frame 联立工作
2. 场-电流-电荷响应是否与 1D 理论模型一致

它不是单独的 laser injection test，但它确实给了“laser 驱动后等离子体响应”的强物理断言。

### 4.3 `analysis_refined_injection.py` 验证的是 AMR 注入均匀性

`test_2d_refined_injection` 的 `analysis_refined_injection.py` 检查两件事：

1. 电子数是否等于 coarse streams 与 refined streams 预期叠加值
2. 在 refinement edge 附近取一条 `rho` 切片，要求相对波动小于 `0.5%`

因此它真正验证的是：

- `warpx.refine_plasma = 1`
- moving window 下连续注入
- refinement interface 附近粒子注入与电荷沉积是否仍保持均匀

这条 test 的 focus 在注入与 AMR 耦合，不在 laser envelope 本身。

### 4.4 `analysis_openpmd_rz.py` 验证的是 RZ openPMD diagnostics 合同

`test_rz_laser_acceleration_opmd` 会调用 `analysis_openpmd_rz.py`。

它检查的是：

- iteration 数量是否正确
- mesh 数量与维度顺序是否正确
- `j_t`、`part_per_grid`、`rho_<species>` 的 shape 是否正确
- `rho_electrons` 与 `rho_beam` 在轴向上的中心位置是否符合物理预期

因此它并不是在验证 laser 注入本身，而是在验证：

- RZ 场景下，被 laser 驱动后的多 species diagnostics
- openPMD writer 在 RZ geometry 下没有把 mesh 或 species 顺序写乱

### 4.5 `inputs_test_3d_laser_acceleration_python.py` 主要是 Python callback 工作流

这个 Python 输入脚本只是：

- `load_inputs_file("./inputs_test_3d_laser_acceleration")`
- 注册两个 `afterstep` callback
- 在 callback 中访问粒子容器和 `Efield_fp`

因此 `test_3d_laser_acceleration_python` 的核心边界更像：

- Python extension / callback workflow smoke test
- 加上最终 checksum

它不是激光物理断言，也不是 diagnostics 解析测试。

## 5. `Examples/Tests/boosted_diags/`：`laser_acceleration_btd` 在验证什么

`test_3d_laser_acceleration_btd` 用的是 `inputs_test_3d_laser_acceleration_btd`，analysis 在 `boosted_diags/analysis.py`。

这个 analysis 做两类硬检查：

1. 比较 BTD plotfile 与 BTD openPMD 的 `Ez` 数组，要求逐点 `allclose`
2. 检查 `beam.random_fraction = 0.5` 的粒子随机子采样确实生效

因此它真正验证的是：

- boosted-frame 下 back-transformed diagnostics 的 writer 一致性
- 而不是 laser 注入场本身的解析正确性

laser 在这里是背景驱动器，analysis 的焦点是 BTD 数据合同。

## 6. 这一组 tests 应怎样分类理解

如果从“laser 注入本体是否被强验证”这个问题出发，当前证据强弱大致是：

### 第一层：最强，直接验证注入场

- `Examples/Tests/laser_injection/` 的 1D/2D
- `Examples/Tests/laser_injection/` 的 implicit 1D/2D
- `Examples/Tests/laser_injection_from_file/` 的 1D/2D/3D/RZ

它们有明确的 envelope / frequency 断言。

### 第二层：中等，laser 作为驱动器，验证下游物理或几何响应

- `analysis_1d_fluid_boosted.py`
- `analysis_refined_injection.py`

它们不直接看注入场，但对 laser 驱动后的物理或 AMR 注入后果给出明确断言。

### 第三层：中等，验证 diagnostics / workflow 合同

- `analysis_openpmd_rz.py`
- `boosted_diags/analysis.py`
- `inputs_test_3d_laser_acceleration_python.py` + checksum

它们关心的是输出格式、BTD 一致性、Python callback 工作流，不是 laser 物理公式。

### 第四层：较弱，主要依赖 checksum

- 大多数 `laser_acceleration` 主例子
- 3D `laser_injection`

这些条目可以证明“当前实现没有明显数值漂移”，但不能单独证明某条 laser 注入数学合同。

## 7. 对当前书稿最重要的结论

当前本地 WarpX checkout 给 `Laser` 提供的 regression 证据并不平均：

- 注入本体：1D/2D 强，3D 弱
- `from_file`：强
- `parse_field_function`：有真实用例，但只有间接覆盖
- `laser_acceleration`：主要是下游工作流/场景回归，不应误写成“laser 注入公式已被逐一解析验证”

因此书稿和索引里需要避免两种误判：

1. 把 `laser_acceleration` 全部当成 laser injection 单元测试
2. 因为某个目录有 `analysis.py`，就默认它有强物理断言

## 8. 下一步最自然的工作

从 `Laser` 模块继续推进，最合理的下一步是：

1. 把 `docs/example-regression-map.md` 里 `laser_acceleration`、implicit laser injection、BTD 相关条目全部更新成“analysis 断言 / checksum 主导 / workflow smoke test”的明确表述。
2. 然后决定是继续补 `laser_ion`、`free_electron_laser` 这些 laser 驱动应用，还是切回 `ExternalField.*` / `WarpXMovingWindow.cpp`。
