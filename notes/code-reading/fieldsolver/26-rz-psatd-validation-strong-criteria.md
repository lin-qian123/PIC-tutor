# RZ PSATD validation 强判据表

绑定源码、测试与 analysis：

- `../warpx/Examples/Tests/nci_psatd_stability/CMakeLists.txt`
- `../warpx/Examples/Tests/pml/CMakeLists.txt`
- `../warpx/Examples/Tests/langmuir/CMakeLists.txt`
- `../warpx/Examples/Tests/nci_psatd_stability/analysis_galilean.py`
- `../warpx/Examples/Tests/langmuir/analysis_rz.py`
- `../warpx/Examples/Tests/langmuir/analysis_utils.py`
- `../warpx/Examples/Tests/pml/analysis_pml_psatd_rz.py`
- `../warpx/Examples/Tests/nci_psatd_stability/inputs_test_rz_*`

本笔记不再重复推导 RZ / Galilean RZ 的 `X1-X4/Theta2/T_rho` 系数。它只回答一个更直接的问题：**当前 WarpX 源码树里，哪些 active RZ PSATD regression 已经提供“强判据”，哪些仍只是 checksum 或 workflow 回归。**

## 目标

把第 6 章里已经拆开的 RZ PSATD 算法边界，继续推进到验证边界：

1. 哪些 regression 当前真的能支撑物理论断；
2. 哪些只能支撑输出/流程论断；
3. 写书时应该优先引用哪几条强 analysis；
4. 现有 RZ PSATD 哪一块仍明显缺独立主判据。

## 一页结论

当前 RZ PSATD active regression 可以先分成四层：

| 层级 | 代表测试 | 当前主判据 | 可支持的说法 |
|---|---|---|---|
| A. 强 NCI 抑制 | `test_rz_galilean_psatd*` | `analysis_galilean.py` 的全域末态 field-energy gate；`current_correction` 分支再加 `divE-rho/eps0` gate | 可直接支撑 RZ Galilean PSATD 对 drifting-plasma NCI 的强 regression 论断 |
| B. 强解析场 / 守恒 | `test_rz_langmuir_multi_psatd*` | `analysis_rz.py` 的解析 `Er/Ez` 对照；`current_correction` 分支再加 `analysis_utils.py` 的 charge gate | 可支撑 RZ PSATD 在 Langmuir 小振幅问题上的波形正确性与部分守恒论断 |
| C. 强 PML 残余场 | `test_rz_pml_psatd` | `analysis_pml_psatd_rz.py` 的全域残余 `Er/Ez` 上界 | 可支撑 RZ PSATD + radial PML 的吸收残余场论断 |
| D. checksum-only workflow | `test_rz_psatd_JRhom_LL2` | `analysis=OFF`，只有 final checksum | 只能支撑 RZ JRhom LL2 应用 workflow / 输出回归，不能支撑独立稳定性强论断 |

因此，**当前 RZ PSATD 最强的主动验证主线不是 JRhom LL2，而是 `RZ Galilean family + RZ Langmuir family + RZ PML PSATD` 这三条。**

## 1. RZ Galilean family：当前最强的 RZ PSATD NCI gate

`../warpx/Examples/Tests/nci_psatd_stability/CMakeLists.txt` 当前在 `WarpX_FFT` 打开时注册三条 active RZ Galilean sibling：

```cmake
add_warpx_test(
    test_rz_galilean_psatd
    RZ
    1
    inputs_test_rz_galilean_psatd
    "analysis_galilean.py diags/diag1000400"
    "analysis_default_regression.py --path diags/diag1000400 --rtol 1e-8"
    OFF
)

add_warpx_test(
    test_rz_galilean_psatd_current_correction
    RZ
    2
    inputs_test_rz_galilean_psatd_current_correction
    "analysis_galilean.py diags/diag1000400"
    "analysis_default_regression.py --path diags/diag1000400 --rtol 1e-8"
    OFF
)

add_warpx_test(
    test_rz_galilean_psatd_current_correction_psb
    RZ
    1
    inputs_test_rz_galilean_psatd_current_correction_psb
    "analysis_galilean.py diags/diag1000400"
    "analysis_default_regression.py --path diags/diag1000400 --rtol 1e-8"
    OFF
)
```

这三条的共同点是：**主 analysis 都不是 checksum，而是 `analysis_galilean.py` 的全域末态场能消费者链。**

### 1.1 普通 RZ Galilean

`test_rz_galilean_psatd` 对应的可支持说法最直接：

- producer 是 RZ + Galilean PSATD 的 drifting-plasma scaffold；
- consumer 读取末态 `diag1000400` 的 `Er/Et/Ez`，重映成 `Ex/Ey/Ez` 口径；
- 主 gate 是

$$
\frac{\sum \epsilon_0 |\mathbf E|^2 / 2}{E_{\mathrm{ref}}} < 10^{-8}.
$$

它可以直接写成：**RZ Galilean PSATD 对 relativistic drifting plasma 的 NCI 抑制，当前已有强 regression gate。**

### 1.2 current correction 分支

`test_rz_galilean_psatd_current_correction` 比普通 RZ Galilean 多一层：

- 场能 gate 仍然保留；
- 再消费同一张末态 plotfile 里的 `divE` 与 `rho/epsilon_0`；
- 施加

$$
\frac{\|divE-\rho/\epsilon_0\|_\infty}{\max(\|divE\|_\infty,\|\rho/\epsilon_0\|_\infty)} < 3\times 10^{-4}.
$$

所以这条可以直接支撑：**RZ Galilean PSATD + current correction 同时通过了 NCI 抑制与离散 Gauss-law/continuity projection gate。**

### 1.3 PSB 分支

`test_rz_galilean_psatd_current_correction_psb` 进一步打开 `periodic_single_box_fft = 1`，而 `analysis_galilean.py` 对这条分支把 charge gate 收紧到 `1e-9`。

因此这条是当前 RZ PSATD 主线里**最强的 charge-conservation regression gate**，比 non-PSB sibling 更适合在书里用来说明：

- PSB 不是“另一个 solver family”；
- 它是在同一 RZ Galilean / current-correction 主线上，给出更强的 periodic-single-box charge gate。

## 2. RZ Langmuir family：当前最强的 RZ PSATD 波形正确性 gate

`docs/example-regression-map.md` 已经把 RZ Langmuir PSATD 三条 sibling 压实：

- `test_rz_langmuir_multi_psatd`
- `test_rz_langmuir_multi_psatd_current_correction`
- `test_rz_langmuir_multi_psatd_JRhom_LL4`

它们共同绑定到：

```cmake
analysis_rz.py diags/diag1000080
analysis_default_regression.py --path diags/diag1000080
```

这三条的价值和 `nci_psatd_stability` 不同。它们不主要验证“是否压住 NCI”，而主要验证：

1. RZ PSATD 的解析 `Er/Ez` 小振幅波形是否正确；
2. particle filter diagnostics 是否仍符合合同；
3. `current_correction` 分支是否继续通过 `divE-rho/epsilon_0` gate。

### 2.1 普通 RZ PSATD

`test_rz_langmuir_multi_psatd` 的主 gate 是：

- 同一张末态 `diag1000080` 上解析 `Er/Ez` 对照；
- `error_rel < 0.12`；
- 再叠三张 filter diagnostics side consumer；
- 不额外要求 charge gate。

这条更适合作为**RZ standard PSATD 波形正确性**的强验证引用，而不是 NCI 稳定性引用。

### 2.2 current correction

`test_rz_langmuir_multi_psatd_current_correction` 在同样的解析 `Er/Ez` 主链之外，还会由 `analysis_utils.py` 继续施加：

$$
divE-\rho/\epsilon_0
$$

的 `1e-9` 级守恒 gate。

因此这条可直接写成：**RZ PSATD current correction 在 Langmuir 解析波形问题上，同时守住了解析场与 charge-conservation。**

### 2.3 JRhom LL4

`test_rz_langmuir_multi_psatd_JRhom_LL4` 仍然是强 analysis，但它的“强”来自：

- 解析 `Er/Ez` 场；
- filter diagnostics；
- `JRhom CL4 + Nm=2` 的特定 producer scaffold。

它当前**没有独立的额外 charge gate**，所以它比 `current_correction` sibling 弱一层，但仍明显强于 checksum-only 的 `test_rz_psatd_JRhom_LL2`。

## 3. RZ PML PSATD：当前最清楚的边界吸收 gate

`test_rz_pml_psatd` 当前在 `../warpx/Examples/Tests/pml/CMakeLists.txt` 中绑定：

```cmake
"analysis_pml_psatd_rz.py diags/diag1000500"
"analysis_default_regression.py --path diags/diag1000500"
```

主 analysis 读取末态全域 `Er/Ez`，直接断言

$$
\max(\max|Er|,\max|Ez|) < 2.0.
$$

这条是当前 RZ PSATD 路线中最适合支持以下说法的 regression：

- radial PML 打开后，脉冲离开主域后域内残余场足够小；
- 这条结论来自全域 residual field gate，而不是某个局部 probe；
- 它验证的是 **RZ PSATD + PML**，不是普通 RZ PSATD bulk dispersion。

所以这条不该和 `nci_psatd_stability` 混成一个“RZ stability”桶，而应单列成 **边界/PML 强判据**。

## 4. RZ JRhom LL2：当前仍是 checksum-only

`test_rz_psatd_JRhom_LL2` 当前 wiring 很明确：

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

这条路径虽然 producer 很重：

- moving window
- rigid beam + background species
- `psatd.do_time_averaging = 1`
- `psatd.update_with_rho = 1`
- `psatd.JRhom = "LL2"`
- `divE/divB cleaning`

但它当前**没有独立 analysis**。因此它最多只能支撑：

- 输出回归；
- workflow 仍能跑通；
- 末态 surface 没漂。

它**不能**单独支撑：

- RZ JRhom LL2 稳定性强论断；
- RZ JRhom LL2 的解析正确性强论断；
- `do_time_averaging + update_with_rho` 的独立物理 gate。

这也是当前 RZ PSATD validation 主线上最明显的缺口。

## 5. 当前最值得写进第 6 章的判据结构

如果第 6 章下一步继续收口 RZ validation，当前最稳妥的写法应分成三条：

1. **RZ Galilean / current-correction family**
   - 用 `analysis_galilean.py` 写 NCI 抑制与 Gauss-law gate。
2. **RZ Langmuir PSATD family**
   - 用 `analysis_rz.py + analysis_utils.py` 写解析波形与 charge gate。
3. **RZ PML PSATD**
   - 用 `analysis_pml_psatd_rz.py` 写残余场上界。

相对地，`test_rz_psatd_JRhom_LL2` 应继续被写成：

- **RZ JRhom 应用 workflow 的 checksum regression**

而不是已经具备独立强判据的 validation baseline。

## 6. 下一步最该补的不是更多表，而是 RZ JRhom 的主 analysis

从“验证强度”的角度看，当前最值得推进的不是再补一张 RZ coefficient 表，而是给 `test_rz_psatd_JRhom_LL2` 找一条真正的主 analysis。优先级可以写成：

1. 若目标是稳定性：
   - 增加一个类似 `analysis_galilean.py` / `analysis_psatd_CC1.py` 的末态 field-energy gate；
   - 先说明 reference sibling 是什么，而不是直接抄一个常数。
2. 若目标是 `update_with_rho + do_time_averaging + JRhom_LL2` 正确性：
   - 优先设计 RZ application-specific reduced diagnostic 或解析 proxy；
   - 不要继续只靠 checksum。
3. 若这条线一时补不出来：
   - 第 6 章就应明确写成“RZ JRhom LL2 当前仍只有 workflow/output regression，而非强物理 gate”。

## 当前结论

**RZ PSATD 现在已经有三条可以直接写进正文的强 validation 主线：**

- `test_rz_galilean_psatd*`：RZ NCI suppression / current-correction / PSB gate；
- `test_rz_langmuir_multi_psatd*`：RZ PSATD 解析波形与部分 charge gate；
- `test_rz_pml_psatd`：RZ PSATD + radial PML residual-field gate。

**当前最明显的缺口不是 RZ Galilean，也不是 RZ PML，而是 `test_rz_psatd_JRhom_LL2` 还没有自己的独立 main analysis。**
