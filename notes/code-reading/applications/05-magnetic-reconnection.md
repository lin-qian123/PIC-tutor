# Magnetic reconnection：hybrid PIC 应用线，不是普通 `Fluids/` 验证页

绑定源码、examples 与 analysis：

- `../warpx/Examples/Tests/ohm_solver_magnetic_reconnection/README.rst`
- `../warpx/Examples/Tests/ohm_solver_magnetic_reconnection/CMakeLists.txt`
- `../warpx/Examples/Tests/ohm_solver_magnetic_reconnection/inputs_test_2d_ohm_solver_magnetic_reconnection_picmi.py`
- `../warpx/Examples/Tests/ohm_solver_magnetic_reconnection/analysis.py`

关联底层笔记：

- `../fieldsolver/10-implicit-and-hybrid.md`
- `../fieldsolver/12-hybrid-pic-model-deep-dive.md`
- `../fieldsolver/13-fieldsolver-verification-map.md`
- `../fieldsolver/14-fieldsolver-analysis-criteria.md`
- `../fluids/02-fluid-pic-coupling.md`

这一篇只回答当前 worktree 下最容易写错的三个问题：

1. `magnetic_reconnection` 到底属于哪条应用主线；
2. 它和 `Fluids/` 的关系到底是什么；
3. 当前 active regression 到底是强物理对照，还是 hybrid-PIC 物理案例加输出回归。

## 1. 物理定位：这是 hybrid-PIC space-plasma application，不是普通流体例子

`ohm_solver_magnetic_reconnection/README.rst` 已经把定位写得很直接：

- 这是 `Hybrid-PIC` code 的磁重联示例；
- 场景是 `force-free sheet`；
- 参考的是 `Le et al. (2016)`。

因此，这条应用线在当前项目里的正确角色不是：

- `Fluids/` 的简单 demo；
- 普通 `ohm_solver_*` 谱图测试中的一页附属说明；

而是：

- `hybrid-PIC space-plasma application line`

这点很关键，因为它决定了本章的组织重点必须是：

```text
kinetic ions
-> electron-fluid Ohm closure
-> externally imposed force-free-sheet field
-> reduced diagnostics for reconnection rate
-> image/checksum-level regression
```

而不是把它误写成“额外 cold-fluid species 的应用页”。

## 2. 它依赖的是 `HybridPICModel`，不是 `WarpXFluidContainer`

当前 worktree 里，`Fluids/` 和 hybrid PIC 不是同一件事。已有 `fluids/02-fluid-pic-coupling.md` 已经把边界压得很清楚：

- `HybridPICModel`
  - 是 field solver 内部的 electron-fluid closure；
- `Fluids/`
  - 是额外 cold-fluid species 的 runtime layer；
  - 有自己的 `N/NU` 状态；
  - 自己 gather `E/B`，再把 `rho/J` 沉积回普通场寄存器。

而 `magnetic_reconnection` 这条应用树走的是：

- `picmi.HybridPICSolver(...)`
- `ohm_solver_*`

也就是：

- kinetic ions
- inertialess/isothermal electron background fluid
- 用广义 Ohm 定律闭合 `E`
- 再按 Faraday + RK 子步推进 `B`

因此它在应用综合章里的最重要边界必须写成：

> 这是 `HybridPICModel` 的应用页，不是 `WarpXFluidContainer` 的应用页。

如果后面需要一个直接对应 `Fluids/` 的应用入口，当前 worktree 里更自然的还是：

- `langmuir_fluids`

而不是 `magnetic_reconnection`。

## 3. 当前 active tree 只有一条主入口：2D PICMI force-free-sheet setup

`CMakeLists.txt` 当前只有一条 active test：

```cmake
add_warpx_test(
    test_2d_ohm_solver_magnetic_reconnection_picmi
    2
    2
    "inputs_test_2d_ohm_solver_magnetic_reconnection_picmi.py --test"
    "analysis.py"
    "analysis_default_regression.py --path diags/diag1000020"
    OFF
)
```

这已经把当前验证层级写得很清楚：

1. 有独立 `analysis.py`
2. 同时也跑 checksum helper
3. 但不是那种脚本内带显式 `assert` 的强 regression

所以这条应用线当前更准确的 CI 角色是：

- `analysis + checksum`
- 但 analysis 偏 reader-side physical observable extraction
- 不是 fixed-tolerance scalar assert

## 4. 输入骨架：2D periodic-x / reflecting-z 的 force-free sheet

`inputs_test_2d_ohm_solver_magnetic_reconnection_picmi.py` 当前不是普通薄输入卡，而是完整的应用 driver。

它明确写出：

- `Cartesian2DGrid`
- `x` 方向周期边界
- `z` 方向 `dirichlet` 场边界与 `reflecting` 粒子边界
- `picmi.HybridPICSolver(...)`
- `plasma_resistivity`
- `substeps`

同时，它用解析表达式直接定义初始 force-free-sheet 磁场：

- `Bx = B0 tanh(z/l_i) + perturbation`
- `By = sqrt(Bg^2 + B0^2 - (B0 tanh(z/l_i))^2)`
- `Bz = perturbation`

也就是说，这条应用树当前真正串起来的是：

1. hybrid-PIC field solver
2. 外加解析初始磁场
3. kinetic ion loading
4. reduced diagnostics
5. reader-side reconnection-rate extraction

而不是单独某一个 solver knob 的 isolated unit test。

## 5. reduced diagnostics 是这条应用线的核心，不是附属输出

这条输入最重要的 diagnostics 不是 full plotfile，而是：

- `picmi.ReducedDiagnostic(diag_type="FieldProbe", name="plane", ...)`

它在 X 点附近取一个 plane probe，用来构造：

- `plane.dat`

随后 `analysis.py` 直接消费这份 reduced diagnostic：

```python
plane_data = np.loadtxt("diags/plane.dat", skiprows=1)
times = plane_data[:, 0, 1]
plt.plot(
    times / sim.t_ci,
    np.mean(plane_data[:, :, Ey_idx], axis=1) / (sim.vA * sim.B0),
    "o-",
)
```

因此这条应用线最核心的 reader-side observable 是：

$$
R(t)=\frac{\langle E_y\rangle}{v_A B_0}.
$$

也就是归一化重联率。

这和 `laser_ion` 依赖 time-averaged `Ez` diagnostics consistency、`capacitive_discharge` 依赖 Turner profile 重建一样，说明：

- diagnostics 合同本身就是应用线的一部分；
- 不是“物理都正确了以后顺手输出一点图”。

## 6. 当前 analysis 的强度：有物理量提取，但没有显式 assert

`analysis.py` 当前会做两件事：

1. 画出 `reconnection_rate.png`
2. 在非 `--test` 模式下进一步生成磁场演化动画
   - `mag_reconnection.mp4`

但它没有：

- fixed reference curve 的数值 `assert`
- 增长率 / 阻尼率 RMS error 这类显式容差比较

所以它的真实层级必须写成：

- `physics-informed visualization / observable extraction`

而不是：

- `hard numerical benchmark`

这点和已有 `fieldsolver/14-fieldsolver-analysis-criteria.md` 保持一致：

- `ohm_solver_em_modes/analysis_rz.py`
  - 是强 assert
- `ion_beam_instability/analysis.py`
  - 是强 assert
- `magnetic_reconnection/analysis.py`
  - 不是

## 7. checksum 仍然是 active coverage 的另一半

`CMakeLists.txt` 还显式跑：

- `analysis_default_regression.py --path diags/diag1000020`

因此这条应用树的 active coverage 当前应被准确理解为两层：

1. `analysis.py`
   - 提取并可视化重联率；
   - 在非 test 模式下输出磁场演化动画；
2. checksum helper
   - 兜底输出稳定性；
   - 保证当前历史基线不漂移。

这就是为什么它在应用综合章里更适合被写成：

- `hybrid-PIC physical case + output regression`

而不是：

- “已经独立证明某个 Ohm 项精确正确”。

## 8. 和邻近 `ohm_solver_*` 目录的分工

当前 `ohm_solver_*` 树已经在 `fieldsolver/13-14` 里压出了分层：

- `ohm_solver_em_modes`
  - normal-mode / RZ spectral checks
- `ohm_solver_ion_beam_instability`
  - instability growth-rate hard assert
- `ohm_solver_ion_Landau_damping`
  - damping-curve visualization + checksum
- `ohm_solver_cylinder_compression`
  - checksum-only workflow baseline
- `ohm_solver_magnetic_reconnection`
  - reconnection-rate extraction + checksum

因此 `magnetic_reconnection` 在应用综合章里承担的角色，正好不是“最强的 solver correctness proof”，而是：

- hybrid-PIC 在真实 space-plasma 场景里的代表性应用入口

它把谱、增长率、阻尼率这些更“局部”的 verification，向上收束成了一个完整物理案例。

## 9. 当前 worktree 下这条应用线真正成立的结论

把这一页压成最保守也最准确的一句话：

```text
magnetic_reconnection
= hybrid-PIC application line
= HybridPICModel electron-fluid closure, not Fluids/ runtime layer
= force-free-sheet + reduced FieldProbe + reconnection-rate extraction
= physics-informed visualization plus checksum
!= scalar hard-assert benchmark
```

所以在后续书稿里，这条应用线最合理的组织方式不是：

```text
fluid/PIC coupling demo
```

而应该是：

```text
hybrid-PIC space-plasma application
-> kinetic ions + electron-fluid Ohm closure
-> force-free-sheet initial field
-> reduced diagnostics for reconnection rate
-> analysis/animation/checksum layered regression
```
