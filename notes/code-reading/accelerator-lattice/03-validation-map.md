# AcceleratorLattice 03: hard-edged quadrupole validation map

绑定源码与示例：

- `../warpx/Source/AcceleratorLattice/AcceleratorLattice.*`
- `../warpx/Source/AcceleratorLattice/LatticeElements/HardEdgedQuadrupole.*`
- `../warpx/Source/AcceleratorLattice/LatticeElementFinder.*`
- `../warpx/Examples/Tests/accelerator_lattice/analysis.py`
- `../warpx/Examples/Tests/accelerator_lattice/inputs_test_3d_hard_edged_quadrupoles`
- `../warpx/Examples/Tests/accelerator_lattice/inputs_test_3d_hard_edged_quadrupoles_boosted`
- `../warpx/Examples/Tests/accelerator_lattice/inputs_test_3d_hard_edged_quadrupoles_moving`

这篇只回答一个问题：当前本地 checkout 里，accelerator lattice 这条线有没有已经接到 examples/regressions 的强验证入口。

答案是有，而且最硬的一组就是 `hard_edged_quadrupoles`。

## 1. 这组测试不是纯 checksum

`Examples/Tests/accelerator_lattice/CMakeLists.txt` 里三条测试：

- `test_3d_hard_edged_quadrupoles`
- `test_3d_hard_edged_quadrupoles_boosted`
- `test_3d_hard_edged_quadrupoles_moving`

都同时接了：

- `analysis.py`
- `analysis_default_regression.py --path diags/diag1000050`

因此 checksum 只是输出基线，真正的物理断言在 `analysis.py`。

## 2. `analysis.py` 的真实断言对象

`analysis.py` 的结构很直接：

1. 从 plotfile 读取最终粒子：
   - `particle_position_x`
   - `particle_position_z`
   - `particle_momentum_x`
2. 从输入参数里重新读出 lattice：
   - `lattice.elements`
   - `line*.elements`
   - `drift*.ds`
   - `quad*.ds`
   - `quad*.dEdx`
3. 在 Python 里按解析 hard-edged quadrupole 透镜公式逐段积分：
   - drift 里做自由传播
   - quad 里用 `cos/sin` 或 `cosh/sinh` 的解析解
4. 最后把解析结果和模拟结果比较：
   - `x` 相对误差 `< 1%`
   - `u_x` 相对误差 `< 0.2%`

所以它验证的不是“lattice 能读进来”，而是：

- `HardEdgedQuadrupole` 的聚焦/散焦动力学
- `LatticeElementFinder` 的元件定位
- 以及粒子推进过程中 lattice force 的真实应用

## 3. 三个输入变体分别覆盖什么

### 3.1 `inputs_test_3d_hard_edged_quadrupoles`

这是最直接的 lab-frame 基准：

- `warpx.do_electrostatic = labframe`
- 单电子 `SingleParticle`
- 两段 drift + 两段 quad
- `quad1.dEdx = +1.e4`
- `quad2.dEdx = -1.e4`

它最直接覆盖：

- `lattice.elements`
- `line.type = line`
- `drift.type = drift`
- `quad.type = quad`
- `quad.dEdx`

### 3.2 `inputs_test_3d_hard_edged_quadrupoles_boosted`

这个变体显式打开：

- `warpx.gamma_boost = 2.`
- `warpx.boost_direction = z`

`analysis.py` 里会把输出的 `z` 位置反变换回 lab frame，再继续套同一套解析透镜串联模型。

因此它验证的不只是 quadrupole 本身，还验证：

- boosted-frame 下 accelerator lattice 作用后
- diagnostics 读出的粒子轨道
- 仍能回到同一个 lab-frame 解析解

### 3.3 `inputs_test_3d_hard_edged_quadrupoles_moving`

这个变体显式打开：

- `warpx.do_moving_window = 1`
- `warpx.moving_window_dir = z`
- `warpx.moving_window_v = 0.1`

它对应的关键边界不是新透镜公式，而是：

- moving window 改变几何参考后
- lattice element finder 仍能把粒子映射到正确元件

这也和 `evolve/05-moving-window.md` 里已经梳理过的“窗口移动后需要更新 accelerator lattice finder”正好闭合。

## 4. 这组回归对书稿最重要的意义

这组 regression 最值得保留的不是“又一个单粒子轨道图”，而是它把 accelerator lattice 这条源码链真正闭到了可检验合同：

```text
lattice.elements / line / drift / quad parameters
-> AcceleratorLattice object model
-> LatticeElementFinder runtime lookup
-> HardEdgedQuadrupole force application
-> final particle orbit
-> analytic quadrupole chain comparison
```

也就是说，当前本地 accelerator lattice 已经不只是“源码里有这个模块”，而是有：

- lab-frame
- boosted-frame
- moving-window

三种运行态下共享同一解析轨道对照的强 regression。

## 5. 当前边界

这组 tests 当前集中验证的是：

- hard-edged `quad`

而不是整个 lattice 家族的所有元件。特别是：

- `plasmalens`
- 更复杂 beamline 组合

还需要后续结合 `plasma_lens_hard_edged` 等条目继续压实。
