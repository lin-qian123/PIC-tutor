# Capacitive discharge：PIC-MCC 低温等离子体

绑定源码、examples 与 analysis：

- `../warpx/Examples/Physics_applications/capacitive_discharge/README.rst`
- `../warpx/Examples/Physics_applications/capacitive_discharge/CMakeLists.txt`
- `../warpx/Examples/Physics_applications/capacitive_discharge/inputs_base_1d_picmi.py`
- `../warpx/Examples/Physics_applications/capacitive_discharge/inputs_test_2d_background_mcc`
- `../warpx/Examples/Physics_applications/capacitive_discharge/inputs_test_2d_background_mcc_picmi.py`
- `../warpx/Examples/Physics_applications/capacitive_discharge/analysis_1d.py`
- `../warpx/Examples/Physics_applications/capacitive_discharge/analysis_dsmc.py`

关联底层笔记：

- `../particles/19-backgroundmcc-pulseddecay-and-dsmc-branches.md`
- `../particles/22-perez-bremsstrahlungevent-and-fusion-probability-control.md`
- `../diagnostics/06-writer-comparison-and-minimal-cases.md`

这一篇要解决的不是 MCC/DSMC 算法细节本身，而是当前本地 `capacitive_discharge` 应用树到底承担什么角色：

- 哪些条目是真正的 Turner benchmark 强对照；
- 哪些只是 workflow/checksum baseline；
- Python callback solver、`background_mcc` 和 DSMC 分支怎样挂到同一低温等离子体骨架上。

## 1. 物理定位：这是 PIC-MCC 低温等离子体应用树，不是普通 collision 单元测试

`capacitive_discharge/README.rst` 的定位非常明确：

- 基于 Turner et al. 2013 的 benchmark cases；
- 模拟 parallel-plate capacitive discharge；
- 重点是 MCC 模型如何复现实验/benchmark 里的 ion density profile。

所以它当前在应用综合章里的正确角色不是：

- 通用 `collision/*` 回归目录的附属例子；

而是：

- `PIC-MCC low-temperature plasma application tree`

这点很重要，因为它决定了应用层主线必须同时覆盖：

1. 电极边界与静电求解；
2. `background_mcc`；
3. 可选 DSMC 分支；
4. Turner case 对照；
5. native / PICMI 前端分裂。

## 2. 当前最强入口是 1D PICMI Turner benchmark

当前 worktree 里，这条应用树最强的证据来自：

- `test_1d_background_mcc_picmi`
- `test_1d_dsmc_picmi`

它们都走同一个 1D PICMI 脚本：

- `inputs_base_1d_picmi.py`

只是通过命令行开关切不同路径：

- `--pythonsolver`
- `--dsmc`

### 2.1 这条脚本不是普通输入卡，而是完整的 benchmark driver

`inputs_base_1d_picmi.py` 当前同时负责：

1. 选择 Turner case `N=1..4`
2. 组装 1D electrostatic grid
3. 可选安装 Python level Poisson solver callback
4. 打开 `background_mcc`
5. 可选把 ionization 分支切成 DSMC
6. 收集最终离子密度并写出
   - `ion_density_case_N.npy`

因此它在当前 worktree 里更像：

```text
benchmark driver
-> setup
-> run
-> callback solver
-> density accumulation
-> benchmark output
```

而不是简单的 `inputs_*.py` 前端薄壳。

### 2.2 Python callback solver 是当前这条应用树里最独特的工程边界

脚本里定义了：

- `PoissonSolver1D`

它不是抽象 demo，而是真的通过：

- `callbacks.installpoissonsolver(self._run_solve)`

把一个 Python level 线性求解器接到 WarpX 主循环。

当前 CI `--test --pythonsolver` 模式下还会显式检查：

- `self.solver` 确实跑过；
- 即最终 `phi` 属性已经被写回。

这使 `capacitive_discharge` 不只是 MCC benchmark，也同时是当前 worktree 中最直接的：

- PICMI + external Python Poisson callback

应用级入口之一。

## 3. 当前 strongest analysis：case-1 ion-density profile 重建

这条应用树最强的 regression 合同并不在 field energy 或 particle spectrum，而在：

- `analysis_1d.py`
- `analysis_dsmc.py`

两者都会直接读取：

- `ion_density_case_1.npy`

并和内置 Turner case-1 参考 profile 做：

- `np.allclose(...)`

因此当前最硬的本地合同是：

- final averaged ion density profile
- against Turner benchmark case 1

这条对照在当前项目里应该写成：

- `profile-level strong analysis`

而不是笼统写成“有 MCC/DSMC test”。

### 3.1 MCC 版与 DSMC 版共用同一 benchmark scaffold

这两条 1D tests 的真正区别不是几何，而是 collision realization：

1. `test_1d_background_mcc_picmi`
   - `background_mcc`
   - Python callback solver
   - Turner case-1 ion profile 对照
2. `test_1d_dsmc_picmi`
   - 在同一骨架里把 ionization 变成 DSMC 分支
   - 仍然回到同一 case-1 ion profile 对照

这意味着当前 worktree 已经证明的不是“DSMC branch can run”，而是：

- `background_mcc`
- DSMC ionization branch
- external Python Poisson solver callback

都能在同一个低温等离子体骨架上重建 Turner benchmark case 1 的离子密度 profile。

## 4. 2D native / PICMI 入口当前仍是 workflow baseline

和 1D 强对照相比，当前 2D 分支的证据层级要弱得多。

活跃条目只有：

- `test_2d_background_mcc`
- `test_2d_background_mcc_picmi`

并且两者都是：

- `analysis = OFF`
- checksum helper

这意味着它们当前更准确的角色是：

- `2D capacitive-discharge workflow baseline`

而不是：

- 2D Turner strong benchmark
- 2D low-temperature plasma physics hard assert

### 4.1 当前 PICMI 2D 版仍应诚实视为 scaffold

2D PICMI 版虽然属于同一应用树，但当前 worktree 下它并没有和 1D 一样拿出独立强 analysis。更准确的写法只能是：

- 2D native / PICMI 输入树已经存在；
- 工作流与输出链已经被 checksum 覆盖；
- 但 profile-level 强物理断言当前仍集中在 1D Turner benchmark。

### 4.2 遗留 `dp_psp` 不能再当作活跃 test

`CMakeLists.txt` 里还保留着：

- `test_2d_background_mcc_dp_psp`

但整条 `add_warpx_test(...)` 当前仍然被注释掉。

因此它在当前项目里只能记成：

- inactive legacy variant

不能再写成活跃回归分支。

## 5. `background_mcc` 与 DSMC：在应用章里该怎样和粒子多物理主线分工

当前本地笔记已经在 `particles/19`、`particles/22` 里把：

- `BackgroundMCC`
- `PulsedDecay`
- DSMC

的实现分叉与 analysis-vs-checksum 边界压实了。

应用综合章不需要再重复那些 kernel-level 细节，它当前更应该回答：

1. 为什么这些粒子多物理分叉会在 `capacitive_discharge` 里同时出现；
2. 哪些在本地 worktree 里已经形成强应用合同；
3. 哪些还只是应用骨架。

因此最准确的分工是：

- `particles/19`、`particles/22`
  - 负责 runtime algorithm / branch / regression 细节；
- `applications/04-capacitive-discharge.md`
  - 负责说明它们怎样共同组成一条 PIC-MCC 低温等离子体应用主线。

## 6. 当前 worktree 下这条应用树真正成立的结论

把 `capacitive_discharge` 收束之后，当前最强、也最保守的结论是：

1. 这不是普通 `collision` 附属例子，而是一条独立的 PIC-MCC 低温等离子体应用树；
2. 最强的本地强断言在 1D PICMI Turner benchmark：
   - case-1 ion density profile 重建；
3. Python callback Poisson solver 是这条应用树的重要工程边界；
4. DSMC 分支不是孤立小 test，而是在同一 benchmark scaffold 里被强对照覆盖；
5. 2D native / PICMI 当前仍主要是 workflow/checksum baseline；
6. `dp_psp` 目前只是被注释掉的遗留分支。

因此，这条应用综合章最准确的组织方式不是：

```text
capacitive discharge = generic collision example
```

而应该是：

```text
PIC-MCC low-temperature plasma application tree
-> 1D Turner benchmark with strong profile analysis
-> Python callback Poisson solver boundary
-> DSMC branch on the same scaffold
-> 2D native/PICMI workflow baselines
```
