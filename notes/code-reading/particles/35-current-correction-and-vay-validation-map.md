# 35 current correction and vay validation map：`Langmuir` 与 `vay_deposition` 怎样把 source-synchronization 合同压成回归断言

绑定源码与回归：

- `../warpx/Examples/Tests/langmuir/analysis_utils.py`
- `../warpx/Examples/Tests/langmuir/analysis_2d.py`
- `../warpx/Examples/Tests/langmuir/analysis_3d.py`
- `../warpx/Examples/Tests/langmuir/inputs_test_2d_langmuir_multi_psatd_current_correction`
- `../warpx/Examples/Tests/langmuir/inputs_test_3d_langmuir_multi_psatd_current_correction`
- `../warpx/Examples/Tests/langmuir/inputs_test_rz_langmuir_multi_psatd_current_correction`
- `../warpx/Examples/Tests/vay_deposition/analysis.py`
- `../warpx/Examples/Tests/vay_deposition/inputs_test_2d_vay_deposition`
- `../warpx/Examples/Tests/vay_deposition/inputs_test_3d_vay_deposition`

前置阅读：

- `../notes/code-reading/particles/32-current-deposition-continuity-and-geometry-boundaries.md`
- `../notes/code-reading/particles/34-sync-current-rho-and-source-synchronization.md`

这一轮不再继续解释 deposition kernel 本身，而是收：

- 哪些 regression 真正在验证 source-synchronization / charge-conservation 合同；
- 哪些只是“跑了 PSATD / Vay”的目录名。

## 1. `Langmuir` 家族不是只看解析场解，current-correction 变体还会额外做 charge-conservation helper

`analysis_2d.py` 和 `analysis_3d.py` 的主断言首先是解析 Langmuir 场解比较：

- `Ex/Ez` 或 `Ex/Ey/Ez` 的相对误差；
- 再在脚本尾部统一调用 `check_charge_conservation(data)`。

源码位置：

- `../warpx/Examples/Tests/langmuir/analysis_2d.py`
- `../warpx/Examples/Tests/langmuir/analysis_3d.py`

因此对 current-correction 变体来说，真实验证合同不是单一的：

1. 解析 Langmuir-wave 场解仍要对；
2. `divE` 与 `rho/\epsilon_0` 的离散一致性还要额外过关。

## 2. `analysis_utils.py` 明确写死了 charge-conservation helper 的触发条件

`check_charge_conservation(data)` 会先读 `warpx_used_inputs`，再决定是否运行：

```python
check_charge_conservation = (
    (
        current_deposition_esirkepov
        and not (geometry_dims_rz or maxwell_solver_psatd)
    )
    or current_correction
    or current_deposition_vay
)
```

源码位置：`../warpx/Examples/Tests/langmuir/analysis_utils.py:31-45`。

这条判断把三类情况分开了：

1. **Esirkepov**
   - 只在非 RZ、非 PSATD 时启用；
2. **PSATD current correction**
   - 直接启用；
3. **Vay deposition**
   - 直接启用。

反过来说，这个 helper 刻意不把：

- `Esirkepov + RZ`
- `Esirkepov + PSATD`

当成当前可用的 charge-conservation 强断言组合。

## 3. `Langmuir + current_correction` 的容差比默认弱，但仍是强 source-consistency 断言

同一个 helper 里，默认容差是：

```python
tolerance = 1e-11
if current_correction:
    tolerance = 1e-9
elif current_deposition_vay:
    tolerance = 1e-3
```

源码位置：`analysis_utils.py:48-53`。

因此：

- `current correction`
  - 断言的还是
    $$
    \frac{\max|\nabla\cdot E-\rho/\epsilon_0|}{\max|\rho/\epsilon_0|}
    $$
    足够小；
  - 但容差从 `1e-11` 放宽到 `1e-9`。

这说明它不是“只要不炸就算过”，而是一个仍然很硬的 source-consistency regression，只是承认 current-correction 路径的数值误差比最理想的显式守恒组合更大。

## 4. `Langmuir + current_correction` 的输入组合也写得很窄

2D 输入：

```text
algo.current_deposition = esirkepov
algo.maxwell_solver = psatd
psatd.current_correction = 1
psatd.periodic_single_box_fft = 1
```

见：

- `../warpx/Examples/Tests/langmuir/inputs_test_2d_langmuir_multi_psatd_current_correction`

3D 输入同样是：

```text
algo.current_deposition = esirkepov
algo.maxwell_solver = psatd
psatd.current_correction = 1
psatd.periodic_single_box_fft = 1
```

见：

- `../warpx/Examples/Tests/langmuir/inputs_test_3d_langmuir_multi_psatd_current_correction`

RZ 版本则改成：

```text
algo.current_deposition = direct
algo.maxwell_solver = psatd
psatd.current_correction = 1
psatd.periodic_single_box_fft = 1
```

见：

- `../warpx/Examples/Tests/langmuir/inputs_test_rz_langmuir_multi_psatd_current_correction`

这和 `analysis_utils.py` 的条件是对齐的：

- `Esirkepov + PSATD` 本身不拿 charge-conservation helper 做一般结论；
- RZ current-correction 直接换成 `direct`，避免把 helper 明确排除的组合写成“当前强断言”。

## 5. 这组 `Langmuir` regression 对应的是哪条 source-synchronization 边界

对 `current correction` 变体来说，它最直接对应的是：

1. `PSATD + periodic single box`
   - `SyncCurrentAndRho()` 中即使开了 current correction，也仍会立刻同步；
2. 同步后
   - `divE` 与 `rho/\epsilon_0` 必须继续匹配；
3. 同时解析 Langmuir-wave 场解不能被 current-correction 路径破坏。

因此它不是纯 field-solver 回归，也不是纯 deposition 回归，而是：

- `deposition + source synchronization + PSATD current-correction` 的组合回归。

## 6. `vay_deposition` 的 analysis 比 `Langmuir` 更窄：只测 charge conservation，不测解析波

`../warpx/Examples/Tests/vay_deposition/analysis.py` 做的事情非常单纯：

```python
rho = data[("boxlib", "rho")].to_ndarray()
divE = data[("boxlib", "divE")].to_ndarray()
error_rel = np.amax(np.abs(divE - rho / epsilon_0)) / np.amax(np.abs(rho / epsilon_0))
tolerance = 1e-3
assert error_rel < tolerance
```

也就是说它完全不看：

- 单粒子解析轨道；
- 场解理论值；
- 频谱或能量账本。

它只看一件事：

$$
\frac{\max|\nabla\cdot E-\rho/\epsilon_0|}{\max|\rho/\epsilon_0|} < 10^{-3}.
$$

所以 `vay_deposition` 的真实角色不是 “Vay pusher 效果测试”，而是：

- Vay current deposition + PSATD + collocated-grid source consistency test

## 7. `vay_deposition` 的输入也写死了它是专门验证 current deposition 的窄场景

2D 输入包含：

```text
algo.current_deposition = vay
algo.maxwell_solver = psatd
algo.particle_pusher = vay
warpx.grid_type = collocated
psatd.periodic_single_box_fft = 0
psatd.update_with_rho = 0
warpx.use_filter = 1
```

见：

- `../warpx/Examples/Tests/vay_deposition/inputs_test_2d_vay_deposition`

3D 输入是对应的三维扩展：

- `../warpx/Examples/Tests/vay_deposition/inputs_test_3d_vay_deposition`

并且两类输入都只放了：

- 一对权重相等、动量相反的 electron / ion 单粒子
- 周期边界
- collocated grid

这说明它不是在复现实验或应用，而是在最小可控环境下验证：

- `current_fp_vay`
- collocated PSATD
- filter
- source synchronization

这整条窄合同最终能否保住离散 Gauss law。

## 8. `vay_deposition` 与 `SyncCurrentAndRho()` 的对应关系比一般 Langmuir 更直接

`SyncCurrentAndRho()` 在非 periodic single-box 的 `PSATD + Vay deposition` 分支里，不会立刻做普通 `SyncCurrent("current_fp")`，而是：

- 先保留 `current_fp_vay`
- 只在这里做 `ApplyFilterMF(...)`
- 更完整的同步留给后续 PSATD 路径

这正是为什么 `vay_deposition` regression 的价值很高：它直接检验这条专门的

- Vay deposition
- non-periodic-single-box PSATD
- collocated-grid
- filter-first

路径最后是否仍能把 `divE-rho/\epsilon_0` 压到 `1e-3` 以内。

## 9. 两组 regression 的职责分工

到这里可以把它们分开写清：

### `Langmuir + current_correction`

- 验证对象：
  - 解析 Langmuir-wave 场解
  - `divE-rho/\epsilon_0`
- 组合特征：
  - PSATD
  - current correction
  - 常见是 periodic single-box
- 角色：
  - 宽一点的 physics + source-consistency 组合验证

### `vay_deposition`

- 验证对象：
  - 只看 `divE-rho/\epsilon_0`
- 组合特征：
  - Vay current deposition
  - Vay pusher
  - PSATD
  - collocated grid
  - non periodic single box
- 角色：
  - 更窄、更直接的 source-synchronization / charge-conservation 验证

## 10. 当前前沿

最自然的下一步有两条：

1. 把这两组 regression 的职责分工回填到 `manuscript/chapters/05-deposition-shapes.md`。
2. 然后把 `TODO.md` 里这条验证项标为完成，并在 `README.md` 同步本轮进展。
