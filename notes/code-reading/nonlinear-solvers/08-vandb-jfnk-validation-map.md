# `analysis_vandb_jfnk_2d*` 验证地图：JFNK、Villasenor、filtering 与 cropping 到底在测什么

绑定源码与测试：

- `../warpx/Examples/Tests/implicit/analysis_vandb_jfnk_2d.py`
- `../warpx/Examples/Tests/implicit/analysis_vandb_jfnk_2d_cropping.py`
- `../warpx/Examples/Tests/implicit/inputs_test_2d_theta_implicit_jfnk_vandb`
- `../warpx/Examples/Tests/implicit/inputs_test_2d_theta_implicit_jfnk_vandb_filtered`
- `../warpx/Examples/Tests/implicit/inputs_test_2d_theta_implicit_jfnk_vandb_cropping`

前一篇 `07-implicit-regression-assertion-map.md` 已经把：

- `analysis_petsc_matrix.py`
- `analysis_planar_pinch.py`
- `analysis_implicit.py`

这些 regression 的验证口径区分开了。这一篇继续补另外一条未闭合的支线：`vandb_jfnk_2d` 与 `vandb_jfnk_2d_cropping` 到底在给哪段 implicit 粒子-场链路做硬断言。

## 1. 这组三个输入的公共核心不是 preconditioner，而是 `theta_implicit_em + newton + Villasenor`

三组输入都共享这些关键设置：

```text
algo.evolve_scheme = "theta_implicit_em"
implicit_evolve.nonlinear_solver = "newton"
algo.current_deposition = "villasenor"
algo.particle_shape = 2   # cropping 例外为 4
```

其中普通 `vandb` 和 `filtered` 还共同使用：

```text
boundary.field_lo = periodic periodic
boundary.field_hi = periodic periodic
warpx.use_filter = 0 or 1
```

因此这条 regression 主线不是为了测 `pc_petsc` 的矩阵装配，也不是为了测边界能量账本，而是为了在一个周期等离子体背景下，直接测试：

- JFNK 的粒子-场固定点主链
- Villasenor charge-conserving current deposition
- 能量守恒与 Gauss 定律

## 2. `analysis_vandb_jfnk_2d.py` 的断言口径和 `analysis_implicit.py` 很像，但测试前提更窄

脚本核心断言是：

```python
assert max_delta_E < tolerance_rel_energy
assert drho_rms < tolerance_rel_charge
```

容忍度是：

```python
tolerance_rel_energy = 2.0e-14
tolerance_rel_charge = 2.0e-15
```

也就是几乎机器精度的能量守恒和 charge conservation。

它和 `analysis_implicit.py` 的区别在于：

- `analysis_implicit.py` 是“exactly energy-conserving EM implicit method”的一般守恒基准；
- `analysis_vandb_jfnk_2d.py` 额外固定了
  - `current_deposition = villasenor`
  - `particle_shape = 2`
  - 2D periodic plasma

所以它更像是对 “JFNK + Villasenor 这条具体实现组合” 的专项守恒基准。

## 3. 这组测试实际上在给 `CurrentDeposition.H` 的 Villasenor 路径做硬断言

前面源码精读已经看到：

- Villasenor 路径会按 `cell crossings` 切轨迹
- 然后按 segment 局部沉积
- 目标是离散连续性和更紧 stencil

而 `analysis_vandb_jfnk_2d.py` 的两条 assert 恰好就是这条实现最关键的两个后果：

1. 若 Villasenor + implicit particle update 的 old/new 轨迹恢复是对的，则总能量应保持机器精度；
2. 若 Villasenor 的 charge-conserving deposition 和后续场更新链没有破坏离散约束，则

$$
\rho - \epsilon_0 \nabla\cdot E
$$

的 RMS 应保持在机器精度附近。

因此这不是一般意义上的“场解看起来正常”，而是直接在验证：

- `CurrentDeposition.H`
- `ImplicitPushPX.cpp`
- `SyncCurrentAndRho()` 后续消费链

是否共同维护了离散守恒结构。

## 4. `filtered` 变体主要验证 “加滤波后这条守恒链仍然成立”

`inputs_test_2d_theta_implicit_jfnk_vandb_filtered` 和基准输入的核心差别之一是：

```text
warpx.use_filter = 1
```

其他关键设置仍然保持：

- `theta_implicit_em`
- `newton`
- `villasenor`
- periodic boundary

而 `CMakeLists.txt` 仍然让它走同一个 `analysis_vandb_jfnk_2d.py`。

这意味着 filtered 变体不是为了测新的物理问题，而是为了在完全相同的守恒判据下检查：

- `PreRHSOp()` 里 `WarpX::use_filter`
- filtered `Efield_fp`
- 与 Villasenor deposition / JFNK 耦合

是否仍然保持能量与 Gauss 定律的机器精度。

换句话说，它给 filter 层加了一条很强的“不得破坏离散守恒”的 regression 约束。

## 5. 这也解释了为什么 `analysis_vandb_jfnk_2d.py` 没有单独检查 GMRES/Newton 次数

和 `analysis_petsc_matrix.py`、`analysis_planar_pinch.py` 不同，这个脚本根本不读 `newton_solver.txt`，只看：

- `field_energy.txt`
- `particle_energy.txt`
- plotfile 中的 `divE` / `rho`

所以它的重点不是 solver efficiency，而是 conservation structure。

这也说明如果这组测试失败，优先怀疑的不是：

- `pc_petsc`
- `MatrixPC`
- LU / ASM 配置

而更可能是：

- Villasenor old/new trajectory reconstruction
- implicit particle push
- filtering 与 deposition 的组合
- charge conservation 在 field update / deposition / boundary 之间被破坏

## 6. `cropping` 变体是另一类测试：它不是周期守恒，而是边界 + 吸收 + suborbit 的 charge-only 约束测试

`inputs_test_2d_theta_implicit_jfnk_vandb_cropping` 和前两者的差异非常大：

```text
boundary.field_lo = pec pec
boundary.field_hi = pec pec
boundary.particle_lo = absorbing absorbing
boundary.particle_hi = absorbing absorbing
particles.crop_on_PEC_boundary = 1
implicit_evolve.particle_suborbits = 1
algo.particle_shape = 4
```

这里已经不再是 periodic 守恒箱子，而是：

- PEC 场边界
- 吸收粒子边界
- 启用 `crop_on_PEC_boundary`
- 启用 suborbit fallback

因此这个用例的设计目标已经从“机器精度总能量守恒”切到了“复杂边界与轨道修正下，charge conservation 不能坏”。

## 7. 所以 `analysis_vandb_jfnk_2d_cropping.py` 故意只检查 `drho_max`

cropping 脚本没有能量断言，只有：

```python
drho_max = np.abs(drho).max()
assert drho_max < tolerance_max_charge
```

并且容忍度是：

```python
tolerance_max_charge = 1.0e-13
```

这说明这个回归的目标是：

- 在有 PEC + 吸收 + cropping + suborbits 的组合下
- 即使轨道、沉积、边界处理都更复杂
- Gauss 定律仍不能出现显著局部破坏

它不再要求机器精度总能量守恒，因为这个场景本来就不是闭合的周期守恒箱子。

## 8. `cropping` 变体把前面源码精读过的三条线绑在了一起

这个输入会同时触发：

1. `particles.crop_on_PEC_boundary = 1`
   对应粒子越界 / PEC cropping 逻辑；
2. `implicit_evolve.particle_suborbits = 1`
   对应 `ImplicitPushPX.cpp` 的 suborbit fallback；
3. `algo.current_deposition = villasenor`
   对应 charge-conserving current deposition；
4. `boundary.field_* = pec`
   对应边界字段和可能的沉积/guard 处理。

所以 `analysis_vandb_jfnk_2d_cropping.py` 的意义并不在于“只看一个简单数值”，而在于它用最直接的

$$
\rho - \epsilon_0 \nabla\cdot E
$$

最大误差，把：

- PEC boundary
- particle cropping
- suborbit fallback
- Villasenor deposition

四条复杂路径绑成了一条 regression 链。

## 9. 从源码覆盖角度看，这组测试补的是 `pc_petsc` 和 `planar_pinch` 覆盖不到的区域

`analysis_petsc_matrix.py` 强覆盖的是：

- `pc_petsc`
- `MatrixPC`
- `WarpXSolverDOF`

`analysis_planar_pinch.py` 强覆盖的是：

- 能量账本
- preconditioner 效率
- Gauss 定律

但它们都没有专门把：

- Villasenor deposition
- filtering
- `crop_on_PEC_boundary`
- suborbits

这些路径逐个单独拉出来。

`vandb_jfnk_2d` / `cropping` 正好把这部分补上：

- `vandb_jfnk_2d` 检查 periodic + Villasenor + JFNK + optional filter 的守恒结构；
- `cropping` 检查 PEC + absorbing + Villasenor + suborbits + cropping 的局部电荷守恒。

## 10. 可以把这三组 `vandb` regression 的验证边界总结成一句话

- `inputs_test_2d_theta_implicit_jfnk_vandb`
  验证 JFNK + Villasenor 在 periodic 2D 下的能量守恒和 Gauss 定律。
- `inputs_test_2d_theta_implicit_jfnk_vandb_filtered`
  验证加 filter 后，上述守恒结构仍成立。
- `inputs_test_2d_theta_implicit_jfnk_vandb_cropping`
  验证 PEC + absorbing + cropping + suborbits 的复杂粒子边界路径下，局部 charge conservation 仍成立。

## 11. 对当前书稿最重要的启发

这一组 regression 说明，前面写过的几个源码主题其实不是分散的：

- `CurrentDeposition.H` 的 Villasenor kernel
- `ImplicitPushPX.cpp` 的 suborbit fallback
- `particles.crop_on_PEC_boundary`
- `WarpX::use_filter`

它们已经在官方 regression 里被组合成多条断言链。

所以后面写第 4、5、6、7 章时，不能把这些实现只当作“局部技巧”；应该把它们放在“哪些 regression 在替它们兜底”这一层一起讲。

## 12. 下一步最自然的继续方向

- 回到 `Particles/` 笔记，把 `analysis_vandb_jfnk_2d_cropping.py` 直接链接到 `09-radiation-reaction-implicit-photon-pushers.md` 和 `10-implicit-suborbit-mass-matrices-jfnk.md` 里关于 suborbit 的部分。
- 回到 `boundary/` 或 `particles/`，补 `crop_on_PEC_boundary`、particle absorbing boundary、sorting/buffer 与 Villasenor 的交界层。
- 如果后面要进入真实运行验证阶段，这组三测应被列为：
  - periodic Villasenor 守恒基准
  - filtered Villasenor 守恒基准
  - PEC/suborbit/cropping 电荷守恒基准
