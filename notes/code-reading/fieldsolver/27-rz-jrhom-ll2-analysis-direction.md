# RZ JRhom LL2 独立 analysis 方向判定

绑定源码、测试与相邻 analysis：

- `../warpx/Examples/Tests/nci_psatd_stability/CMakeLists.txt`
- `../warpx/Examples/Tests/nci_psatd_stability/inputs_base_rz`
- `../warpx/Examples/Tests/nci_psatd_stability/inputs_test_rz_psatd_JRhom_LL2`
- `../warpx/Examples/Tests/nci_psatd_stability/analysis_galilean.py`
- `../warpx/Examples/Tests/nci_psatd_stability/analysis_psatd_CC1.py`
- `../warpx/Examples/Tests/langmuir/analysis_rz.py`
- `../warpx/Examples/Tests/langmuir/analysis_utils.py`
- `../warpx/Examples/Tests/langmuir/inputs_test_rz_langmuir_multi_psatd*`

本笔记只回答一个具体问题：**如果下一步要给 `test_rz_psatd_JRhom_LL2` 补独立 main analysis，第一阶段更应该走哪条路。**

结论先写在前面：**更适合先走 `analysis_psatd_CC1.py` / `analysis_galilean.py` 这一类 stability-style 末态 field-energy gate，而不是直接仿照 `analysis_rz.py` 去写解析场 gate。**

## 1. 当前缺口

`test_rz_psatd_JRhom_LL2` 现在仍是纯 checksum wiring：

```cmake
add_warpx_test(
    test_rz_psatd_JRhom_LL2
    RZ
    2
    inputs_test_rz_psatd_JRhom_LL2
    OFF  # analysis
    "analysis_default_regression.py --path diags/diag1000025"
    OFF
)
```

因此它当前只能支撑：

- 输出回归；
- workflow 可运行；
- 末态 plotfile 不漂。

它还不能支撑：

- RZ JRhom LL2 的独立稳定性强论断；
- `update_with_rho + do_time_averaging` 的独立 correctness gate；
- RZ application workflow 的物理主判据。

## 2. 为什么它不像 Langmuir 那样适合直接写解析场 gate

`analysis_rz.py` 能成立，依赖的是一组非常强的结构前提：

1. producer 是小振幅、周期、解析可写的 Langmuir scaffold；
2. 脚本已知理论 `Er/Ez` 的闭式表达式；
3. geometry/diagnostics 是围绕这组解析场布置的；
4. side diagnostics 还顺手覆盖了 particle filter function。

`test_rz_psatd_JRhom_LL2` 不具备这些前提。它的 input 不是简化 modal scaffold，而是：

- `warpx.do_moving_window = 1`
- `particles.rigid_injected_species = driver`
- `driver + driver_back + plasma_e + plasma_p` 四个 species
- `boundary.field_lo/hi = none damped / none damped`
- `psatd.do_time_averaging = 1`
- `psatd.update_with_rho = 1`
- `psatd.JRhom = "LL2"`
- `warpx.do_dive_cleaning = 1`
- `warpx.do_divb_cleaning = 1`

这更像 application workflow，不像解析基准。

更关键的是，当前 diagnostics 只输出：

```ini
diag1.fields_to_plot = Er Ez Bt jr jz rho rho_driver rho_plasma_e rho_plasma_p
```

这里没有：

- `divE`
- `phi`
- 用于直接回代理论波形的专门 reduced diagnostic
- 类似 Langmuir family 那样的解析振幅/频率 scaffold

因此，若第一步就强行走 `analysis_rz.py` 路线，反而需要先额外定义“理论上应该长什么样”。这一步并不比直接补 main analysis 更轻。

## 3. 为什么它更像 stability-style gate 候选

它和 `analysis_galilean.py` / `analysis_psatd_CC1.py` 有三个更直接的相似点。

### 3.1 同属 `nci_psatd_stability` 家族

`test_rz_psatd_JRhom_LL2`、`test_rz_galilean_psatd*` 与 `test_3d_uniform_plasma_psatd_JRhom_CC1` 都注册在同一个 `nci_psatd_stability/` family 里。

这意味着最自然的第一阶段补洞方式，不是把它拖去模拟 Langmuir family 的解析波形 contract，而是先在同 family 内找一致的判据口径：

- `analysis_galilean.py`：stable vs unstable energy ordering
- `analysis_psatd_CC1.py`：末态电场能量相对参考能量

### 3.2 producer 形状更接近 workflow stability probe

相对 `inputs_base_rz` 的纯 drifting-plasma scaffold，`inputs_test_rz_psatd_JRhom_LL2` 已经叠加了：

- moving window
- rigid injected beam
- background return beam
- continuous plasma injection
- damped longitudinal boundary

这说明它天然更像“复杂 workflow 在当前 solver 组合下是否仍稳定”的 probe，而不是“某个解析模式的场误差比较器”。

### 3.3 已有输出足够支持第一阶段 energy/spike 类 gate

当前输出没有 `divE`，所以不适合第一步就写 charge-conservation gate；
但它已经有：

- `Er`
- `Ez`
- `Bt`
- `rho`
- `j`

这足够支撑一个更克制的第一阶段 main analysis，例如：

1. `finite-field sanity`
2. `electric/magnetic field energy ceiling`
3. `spike ratio` 或类似 envelope 异常指标

这类 gate 不需要先构造完整解析解，也不需要先改 writer 去加 `divE`。

## 4. 第一阶段最合理的方向

因此，`test_rz_psatd_JRhom_LL2` 的独立 main analysis 更合理的顺序是：

1. **第一阶段：stability-style gate**
   - 先补一个类似 `analysis_psatd_CC1.py` 的末态 field-energy gate；
   - 若局部异常比总能量更有区分力，再补 `spike ratio`；
   - 先把“analysis=OFF”改成“至少有一条独立 main gate”。

2. **第二阶段：若需要更强 correctness claim**
   - 再考虑是否新增 `divE` 输出，补 charge / Gauss-law drift gate；
   - 或新增更贴近应用物理的 reduced diagnostic，而不是直接套 Langmuir 解析解。

3. **第三阶段：若仍想讲 `JRhom_LL2 + update_with_rho + do_time_averaging` 本身**
   - 再单独设计更细的 algorithm-specific proxy。

## 5. reference sibling 应该怎么找

第一阶段如果走 stability-style gate，关键不在脚本框架，而在 reference sibling 的定义。

当前最值得优先比较的不是“凭空发明一个解析公式”，而是先在同一 workflow 上找最小改动 sibling，例如：

1. 保持 producer 基本不变，切掉 `psatd.JRhom = "LL2"` 或切换到更普通的时间依赖路径；
2. 保持 moving window / rigid driver / plasma injection 不变，只改变 JRhom / averaging 组合；
3. 观察是否能形成稳定的末态 field-energy ordering。

这和 comoving 第一阶段 patch 的经验一致：**先把 sibling 和 provenance 找稳，再决定阈值是否值得写进 analysis。**

## 6. 当前最保守、也最可执行的写法

因此，第 6 章和 TODO 里对这条线最稳妥的表述应是：

- `test_rz_psatd_JRhom_LL2` 现在仍是 checksum-only；
- 若下一步要补主判据，优先补 stability-style field-energy gate；
- 不建议第一步就按 Langmuir family 去写解析 `Er/Ez` gate；
- `divE` / charge gate 应视为后续增强项，而不是第一阶段 prerequisite。

## 当前结论

**`test_rz_psatd_JRhom_LL2` 的第一阶段独立 main analysis，更适合走 `analysis_psatd_CC1.py` / `analysis_galilean.py` 这一类 stability-style 末态 field-energy 路线，而不是直接走 `analysis_rz.py` 式解析场路线。**

更具体地说：

- 它当前不是解析基准，而是 application workflow；
- 当前 diagnostics 不够支撑直接的解析场或 charge gate；
- 但已经足够支撑 `finite + energy (+ optional spike)` 的第一阶段主判据。
