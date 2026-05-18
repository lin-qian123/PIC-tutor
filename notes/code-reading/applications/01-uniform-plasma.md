# Uniform plasma：噪声、能量、性能和诊断

绑定源码、examples 与 analysis：

- `../warpx/Examples/Physics_applications/uniform_plasma/README.rst`
- `../warpx/Examples/Physics_applications/uniform_plasma/CMakeLists.txt`
- `../warpx/Examples/Physics_applications/uniform_plasma/inputs_base_3d`
- `../warpx/Examples/Physics_applications/uniform_plasma/inputs_test_2d_uniform_plasma`
- `../warpx/Examples/Physics_applications/uniform_plasma/inputs_test_3d_uniform_plasma`
- `../warpx/Examples/Physics_applications/uniform_plasma/inputs_test_3d_uniform_plasma_restart`
- `../warpx/Examples/analysis_default_regression.py`
- `../warpx/Examples/analysis_default_restart.py`

关联底层笔记：

- `../diagnostics/06-writer-comparison-and-minimal-cases.md`
- `../fieldsolver/13-fieldsolver-verification-map.md`
- `../particles/28-particle-diagnostics-python-interface-validation-map.md`

关联相邻测试树：

- `../warpx/Examples/Tests/energy_conserving_thermal_plasma/`
- `../warpx/Examples/Tests/nci_psatd_stability/inputs_test_3d_uniform_plasma_psatd_JRhom_CC1`

这一篇回答的不是“均匀热等离子体的一般理论”，而是当前本地 `uniform_plasma` 应用目录到底承担什么角色：

- 哪些是应用级 workflow baseline；
- 哪些是 writer/checkpoint/restart 的最小强断言；
- 哪些名字虽然带 `uniform_plasma`，其实属于别的验证树。

## 1. 物理问题：这里不是波动 benchmark，而是最小均匀热等离子体背景

`Examples/Physics_applications/uniform_plasma/README.rst` 的定位非常直接：

```text
This example evolves a uniformly distributed, hot plasma over time.
```

和 `Langmuir wave` 不同，这里没有刻意写入空间正弦微扰，也没有现成解析场解要逐点比较。最小 2D 输入只是设置：

```text
electrons.profile = constant
electrons.density = 1.e25
electrons.momentum_distribution_type = gaussian
electrons.ux_th = electrons.uy_th = electrons.uz_th = 0.01
```

因此它的出发点不是“拿一个解析模式检查求解器”，而是：

1. 在最简单的周期热等离子体背景下观察粒子噪声；
2. 给 diagnostics / writer / checkpoint / restart 提供最小工作流骨架；
3. 给并行分解、负载均衡和输出稳定性提供低几何复杂度基线。

## 2. 输入骨架：它是最小热等离子体 workflow，而不是物理 hard assert

当前应用目录里最稳定的两个原生输入是：

- `inputs_test_2d_uniform_plasma`
- `inputs_test_3d_uniform_plasma`

它们的公共结构非常简单：

```text
boundary.field_lo/hi = periodic
warpx.cfl = 1.0
algo.particle_shape = 1
particles.species_names = electrons
electrons.injection_style = NUniformPerCell
electrons.profile = constant
electrons.momentum_distribution_type = gaussian
```

和 Langmuir 的对比很重要：

- Langmuir 用 `parse_momentum_function` 主动写入解析微扰；
- uniform plasma 则刻意不写空间结构，只保留 thermal spread。

也正因为如此，这里最自然暴露出来的是：

- 粒子统计噪声；
- 周期热背景下的场起伏；
- writer/checkpoint 是否稳定；
- 并行 decomposition 或 load-balance 是否引入异常。

这条应用线和 Dawson 1983 里 `quiet starts` 的讨论也能直接接上。作者明确指出：对均匀热背景，纯 random spatial loading 会强烈过激发 long-wavelength small-`k` modes，因为它没有体现 Debye shielding 和局域 charge neutrality；quiet start 则通过在 phase space 中人为降低初始噪声，让弱效应和弱不稳定更容易被看见。反过来，quiet order 本身又会随时间退化，并可能带来自己的 beam-ordering instabilities。对当前本地 `uniform_plasma` 目录来说，这条文献边界的意义是：它更适合作为 noisy thermal background baseline，而不是 quiet-start benchmark。也就是说，当前目录天然暴露的是 noise floor、writer、restart 和并行稳定性，而不是“经过人工降噪后的最优弱信号探测能力”。

## 3. 当前应用目录的真实验证边界：2D/3D 本体是 checksum baseline

`Examples/Physics_applications/uniform_plasma/CMakeLists.txt` 当前只有三条 active tests：

1. `test_2d_uniform_plasma`
2. `test_3d_uniform_plasma`
3. `test_3d_uniform_plasma_restart`

其中前两条的注册方式都是：

```cmake
OFF  # analysis
"analysis_default_regression.py --path diags/diag1000010"  # checksum
```

这意味着：

- `test_2d_uniform_plasma`
- `test_3d_uniform_plasma`

当前都没有独立 physics analysis。它们的真实角色应写成：

- `uniform plasma / noise / performance`
- `full diagnostics / output stability baseline`

而不是：

- 热等离子体理论 hard benchmark
- 独立能量守恒强回归

从应用综合章角度，这一点必须写实，否则会把应用目录本身的证据强度说过头。

## 4. restart 才是这个目录里最强的一条断言

当前应用目录里真正的强断言在：

- `inputs_test_3d_uniform_plasma_restart`

它的输入结构很简单：

```text
FILE = inputs_test_3d_uniform_plasma
amr.restart = "../test_3d_uniform_plasma/diags/chk000006"
```

而 `CMakeLists.txt` 对应地跑：

```cmake
"analysis_default_restart.py diags/diag1000010"  # analysis
"analysis_default_regression.py --path diags/diag1000010 --rtol 1e-12"  # checksum
```

因此 `uniform_plasma` 应用目录里最强的本地合同不是热等离子体物理量，而是：

- 从 checkpoint 恢复后，
- restart 输出与非 restart 输出逐字段一致，
- 相对误差阈值是 `1e-12`。

这也是为什么 `uniform_plasma` 应更准确地理解成：

```text
热等离子体最小工作流
-> full diagnostics
-> checkpoint
-> restart reproducibility
```

而不是“单独证明某个 plasma theory”。

## 5. writer 与诊断：这条应用主线天然覆盖 plotfile/checkpoint 基础链

`uniform_plasma` 在当前项目里真正重要的一点，是它把 writer 角色压得很干净：

1. 2D/3D 本体
   - 提供 full diagnostics 最小骨架；
2. 3D restart 变体
   - 提供 checkpoint/restart 强对照；
3. 周期、单 species、均匀 thermal distribution
   - 避免复杂几何和多物理分叉干扰 writer 分析。

这也是为什么现有 diagnostics 笔记已经把它接回：

- `plotfile/openPMD/checkpoint` 三类 writer 的最小案例；
- `checkpoint` 不是普通 diagnostics view，而是运行态序列化；
- `analysis_default_restart.py` 是 field-level reproducibility helper，而不是某个目录独有脚本。

因此在应用综合章里，`uniform_plasma` 最自然承担的是“诊断与持久化基础案例”，而不是“最漂亮的物理图像案例”。

## 6. “能量”这条要求的真实边界：强断言在邻近测试树，不在应用目录本体

`TODO` 里对 uniform plasma 的要求包括：

- 噪声
- 能量
- 性能
- 诊断

其中最容易误写的是“能量”。

当前本地 worktree 下，应用目录 `uniform_plasma/` 自己并没有独立的能量守恒 analysis。真正直接做热等离子体总能量强断言的是相邻测试树：

- `Examples/Tests/energy_conserving_thermal_plasma/`

现有笔记已经记录过，这组测试的强断言是：

- 从 reduced diagnostics 读 `field energy` 与 `particle energy`
- 要求总能量相对初值的漂移小于 `0.3%`

因此，对“uniform plasma / 能量”最准确的项目内写法应该是：

1. `uniform_plasma` 应用目录本体：
   - 主要承担噪声、writer、checkpoint、restart、性能骨架；
2. 与之物理相邻的 `energy_conserving_thermal_plasma`：
   - 承担热等离子体总能量强断言。

这样才能既满足应用综合章的物理叙述，又不把 `uniform_plasma` 目录自己的证据强度说大。

## 7. “性能”这条要求：当前更像工作流和并行稳定性基线

应用目录本体没有专门的 scaling analysis 脚本，但它天然适合作为并行与性能背景例子，原因有三：

1. 周期、均匀、单 species
   - 几何和物理复杂度最低；
2. 热噪声存在
   - 可用于观察不同并行划分下统计涨落是否异常；
3. full diagnostics + checkpoint
   - 让 I/O 与 persistence 路径也一起被覆盖。

所以当前 worktree 下，`uniform_plasma` 的“性能”应理解成：

- 并行噪声
- 输出成本
- checkpoint/restart 稳定性

的最小 workflow baseline，而不是已经具备专门的强 scaling benchmark 报告。

## 8. 与 `nci_psatd_stability` 的边界：名字里带 `uniform_plasma` 不代表属于应用目录

这一点必须单独记下。

名字里带 `uniform_plasma` 的：

- `test_3d_uniform_plasma_psatd_JRhom_CC1`

并不属于 `Examples/Physics_applications/uniform_plasma/` 应用目录，而属于：

- `Examples/Tests/nci_psatd_stability/`

它的 analysis 不是检查热噪声或 writer，而是：

- 用 `analysis_psatd_CC1.py`
- 比较最终电场能量相对已知不稳定参考值是否足够小
- 从而验证 `JRhom = CC1 + div cleaning` 的 NCI 抑制

因此从应用综合章角度看：

- `uniform_plasma` 应用目录
  - 是热背景 workflow baseline
- `uniform_plasma_psatd_JRhom_CC1`
  - 是谱求解器稳定性测试

两者名字接近，但物理目标和证据强度完全不同。

## 9. 对书稿最重要的总结构

把当前 worktree 证据压成一句话，`Uniform plasma` 在本项目里真正代表的是：

```text
均匀热等离子体背景
-> 最小粒子噪声与并行稳定性
-> full diagnostics / plotfile 基线
-> checkpoint / restart reproducibility
-> 相邻 energy-conserving thermal plasma 给出总能量强断言
-> 相邻 nci_psatd_stability 给出 PSATD/JRhom 稳定性强断言
```

所以它适合作为应用综合章的第二篇，不是因为它自己的 physics analysis 最强，而是因为它把：

- 噪声
- writer
- checkpoint/restart
- 性能背景
- 与相邻稳定性/能量测试树的边界

同时压得最清楚。

## 10. 当前边界

当前这条应用主线还没做的，不是源码阅读，而是更高一层的收口：

1. 如果后续要满足“至少一个本地运行记录”，还需要补：
   - 命令
   - 环境
   - 输出目录
   - 物理检查量
2. 如果后续要把“性能”写得更实，还需要单独增加：
   - decomposition / load-balance / I/O 成本的本地 run note

但从 `TODO` 当前要求的“噪声、能量、性能和诊断”来看，现有 worktree 已经足够把它压成正式应用级主线，只是要把各子要求的证据来源写实：有些来自应用目录本体，有些来自相邻测试树。

## 10A. 本地最小运行记录

2026-05-18 已做一条最小真实运行记录，工作目录：

- `/Volumes/PHILIPS/programs/PIC/PIC-tutor/runs/stage-c-validation/uniform_plasma_2d`

实际命令：

```bash
env OMP_NUM_THREADS=1 FI_PROVIDER=tcp \
  /Volumes/PHILIPS/programs/PIC/warpx/build_full/bin/warpx.2d.MPI.OMP.DP.PDP.OPMD.FFT.EB.QED.GENQEDTABLES \
  /Volumes/PHILIPS/programs/PIC/warpx/Examples/Physics_applications/uniform_plasma/inputs_test_2d_uniform_plasma
```

和 Langmuir 一样，这里也必须绕开默认沙箱下 MPI/OFI 对 `utun6` 的权限限制；切到无沙箱运行后，2D case 正常完成，并产出：

- `diags/diag1000010`
- `warpx_used_inputs`

但这条运行记录的验证强度必须写得更准确：

1. 它不是解析场强断言；
2. `CMakeLists.txt` 里本来就把 `test_2d_uniform_plasma` 写成：
   - `analysis = OFF`
   - `checksum = "analysis_default_regression.py --path diags/diag1000010"`
3. 当前本机直接可用的 Python 还缺：
   - `yt`
   - `openpmd_viewer`

所以这轮没有完成官方 checksum 脚本复跑，而是把它记成：

- 已完成主程序实跑
- 已确认输出目录和输入骨架
- 已确认官方 regression 语义本来就是 checksum-only baseline
- 尚未在本机当前 Python 环境里补完 checksum 脚本执行

这正好再次说明 `uniform_plasma` 的真实角色：

- 它是最小 thermal-background workflow baseline；
- 它能证明：
  - case 可运行
  - diagnostics 会落盘
  - writer/workflow 主链正常
- 但它本身不提供像 `Langmuir` 那样的解析物理 hard assert。

## 11. 用 Birdsall 重新读 `uniform_plasma`

Birdsall Chapter 12 的统计层结论，正好能把 `uniform_plasma` 这棵应用树写得更准确。

当前应用目录本体只有：

- 2D / 3D checksum baseline
- 3D restart 强对照

这说明它并不是独立热等离子体 physics benchmark。  
但如果把它和 Birdsall 的 `(\rho^2)_{k,\omega}`、`1/2\,\rho\phi`、drag / diffusion / entropy production 放在一起看，它的角色就很清楚了：

- 它给的是最干净的 thermal background workflow；
- 适合观察并行分解、writer、restart 是否会把本应平稳的 noise floor 搞坏；
- 它本体不做强 analysis，正好说明这里更多是在守“工作流与统计背景稳定”，而不是直接守某条解析物理解。

这也解释了为什么：

- 热等离子体总能量硬断言要去看 `energy_conserving_thermal_plasma`
- PSATD/NCI 稳定性硬断言要去看 `nci_psatd_stability`
- 而 `uniform_plasma` 自己更适合被当成
  - noise / writer / checkpoint / restart baseline

如果后面要把 Birdsall 的 fluctuation / correlation / noise floor 真正配到具体案例，这棵树就是本地最自然的承载点之一。
