# Laser ion / plasma mirror / RPA/TNSA：边界、靶、强场、多物理

绑定源码、examples 与 analysis：

- `../warpx/Examples/Physics_applications/laser_ion/README.rst`
- `../warpx/Examples/Physics_applications/laser_ion/CMakeLists.txt`
- `../warpx/Examples/Physics_applications/laser_ion/inputs_test_2d_laser_ion_acc`
- `../warpx/Examples/Physics_applications/laser_ion/inputs_test_2d_laser_ion_acc_picmi.py`
- `../warpx/Examples/Physics_applications/laser_ion/analysis_test_laser_ion.py`
- `../warpx/Examples/Physics_applications/laser_ion/analysis_histogram_2D.py`
- `../warpx/Examples/Physics_applications/laser_ion/plot_2d.py`
- `../warpx/Examples/Physics_applications/plasma_mirror/README.rst`
- `../warpx/Examples/Physics_applications/plasma_mirror/CMakeLists.txt`
- `../warpx/Examples/Physics_applications/plasma_mirror/inputs_test_2d_plasma_mirror`
- `../warpx/Docs/source/glossary.rst`

关联底层笔记：

- `../laser/05-application-and-diagnostic-cases.md`
- `../laser/07-laser-ion-multiphysics-switches.md`
- `../particles/12-field-ionization-adk-pipeline.md`
- `../particles/13-collision-handler-stepping-and-regression-map.md`
- `../particles/14-qed-entrypoints.md`
- `../diagnostics/05-reduced-diagnostic-case-studies.md`
- `../diagnostics/06-writer-comparison-and-minimal-cases.md`

这一篇的目标不是再重复 Laser 模块的注入细节，而是把当前本地 worktree 里最像“强场靶”应用的一组案例收束成清晰的应用边界：

- 哪些是真正的 laser-target application entry；
- 哪些已经有强 analysis；
- 哪些还只是 workflow/checksum baseline；
- `RPA/TNSA` 在当前本地证据里到底处在什么层级。

## 1. 当前 worktree 里真正的本地入口只有两条

如果只看当前 `Examples/Physics_applications/`，这条应用线真正可落到本地目录的入口只有：

1. `laser_ion`
   - laser-ion acceleration with planar target
2. `plasma_mirror`
   - plasma mirror with planar solid target

当前 worktree 里没有独立的：

- `rpa_*`
- `tnsa_*`

应用目录或 regression 目录。`RPA`/`TNSA` 只作为术语出现在：

- `Docs/source/glossary.rst`
- `laser_ion/README.rst` 的文献语境里

这决定了本章必须写得很克制：`RPA/TNSA` 在当前项目里只能作为 `laser_ion` 这类 laser-solid target 场景的机制标签，而不能冒充成已经有独立本地应用树和强 regression 的条目。

## 2. `laser_ion`：当前最强的 laser-target 应用入口

`laser_ion/README.rst` 明确写的是：

```text
Laser-Ion Acceleration with a Planar Target
```

而且 README 自己已经写死一个重要边界：

- acceleration mechanism depends on target parameters

也就是说，当前目录本身并不承诺“这里只验证 TNSA”或“这里只验证 RPA”。它只承诺：

- 激光打到固体平面靶；
- 目标是 laser-ion acceleration；
- 具体机制取决于 target 条件。

### 2.1 这条输入骨架真正覆盖了什么

`inputs_test_2d_laser_ion_acc` 当前把以下对象绑在一起：

1. 2D Gaussian laser antenna
2. planar solid-density target
3. full diagnostics
4. time-averaged diagnostics
5. reduced diagnostics
   - `FieldProbe`
   - `ParticleHistogram`
   - `ParticleHistogram2D`
   - `LoadBalanceCosts`
6. openPMD field output

因此这条应用主线当前最强的价值不是：

- 已经证明某条离子加速标度律

而是：

- 把 laser target 场景和 diagnostics 组合完整接通。

### 2.2 当前 CI 里的最硬断言不是 ion spectrum，而是 diagnostics 合同

`laser_ion/CMakeLists.txt` 当前两条 active tests：

- `test_2d_laser_ion_acc`
- `test_2d_laser_ion_acc_picmi`

都跑同一条 analysis：

```cmake
"analysis_test_laser_ion.py diags/diagInst/"
```

这条 analysis 当前真正检查的是：

- 把 `diagInst` 最后 5 个 snapshot 的瞬时 `Ez` 做时间平均；
- 与 `diagTimeAvg` 里的 time-averaged `Ez` 逐点比较。

因此，它的最硬合同是：

- `TimeAveragedFieldDiagnostic`
- field output
- diagnostics 时序一致性

不是：

- proton cutoff energy
- ion conversion efficiency
- TNSA energy scaling
- RPA hole-boring/light-sail threshold

这条边界必须写死，否则会把 README 里的物理叙述和 CI 里的实际断言混成一回事。

### 2.3 `analysis_histogram_2D.py` 和 `plot_2d.py` 是用户后处理 helper，不是 regression

`laser_ion/README.rst` 的 `Analyze` 和 `Visualize` 确实给了：

- `analysis_histogram_2D.py`
- `plot_2d.py`

这说明当前目录不仅有 CI regression，还有面向用户的后处理脚本：

- `analysis_histogram_2D.py`
  - 用于读 phase-space histogram；
- `plot_2d.py`
  - 用于看密度和电磁场结构。

但它们当前都没有在 `CMakeLists.txt` 里作为回归 analysis 注册。因此在应用综合章里更准确的写法是：

- 目录已经具备 user-facing post-processing scaffold；
- 但 CI 强断言仍主要是 diagnostics time-average contract。

### 2.4 `laser_ion` 还有 PICMI 版，但并非所有 reduced diagnostics 都完全对齐

当前 `laser_ion` 有：

- native input
- PICMI input

这比 `plasma_mirror` 更强，因为说明 front-end parity 至少部分已经存在。

但本地源码证据同时也表明一个边界：

- `inputs_test_2d_laser_ion_acc_picmi.py` 里还有
  - `TODO: make ParticleHistogram2D available`

因此不能把 `laser_ion` 简单写成“PICMI 与 native 全量等价”。更准确的说法是：

- PICMI 版已经能覆盖主工作流和 `analysis_test_laser_ion.py` 的 diagnostics 合同；
- 但某些 reduced diagnostics 仍未完全对齐 native input 的完整能力。

## 3. `plasma_mirror`：典型 laser-solid surface-plasma 应用骨架，但当前只有 checksum

`plasma_mirror/README.rst` 明确写的是：

```text
This example shows how to model a plasma mirror,
using a planar target of solid density.
```

它在应用语义上非常明确：

- laser-solid interaction
- planar overdense target
- surface plasma

但当前 worktree 里的验证层级明显弱于 `laser_ion`。

### 3.1 当前目录没有强 analysis，也没有 PICMI 版

当前 `plasma_mirror/CMakeLists.txt` 只有：

- `test_2d_plasma_mirror`
- `analysis = OFF`
- `analysis_default_regression.py --path diags/diag1000020`

同时，`README.rst` 里明确写着：

- Python PICMI input `TODO`
- `Analyze` `TODO`
- `Visualize` `TODO`

所以 `plasma_mirror` 当前只能诚实记成：

- `laser-solid surface-plasma workflow baseline`

不能写成：

- reflectivity benchmark
- high-harmonic benchmark
- experiment-level plasma mirror regression

### 3.2 这条输入骨架真正覆盖的内容

`inputs_test_2d_plasma_mirror` 当前实际覆盖的是：

1. Gaussian laser antenna
2. solid-density target
3. front exponential ramp
4. overdense plateau
5. rear exponential ramp
6. PML
7. field filter
8. dual species target
9. full diagnostics

所以它在应用综合章里最有价值的角色是：

- 作为最小过密靶 / 表面等离子体工作流骨架；
- 给 laser-solid 场景留下一个本地 native-input baseline。

## 4. `RPA/TNSA`：当前只能当作机制标签，不能当作独立本地应用树

这条 TODO 如果不拆清，很容易写过头。

当前本地证据只支持以下结论：

1. `laser_ion/README.rst`
   - 说明这是 laser-ion acceleration with planar targets；
   - acceleration mechanism depends on target parameters。
2. `Docs/source/glossary.rst`
   - 给出 `RPA` 和 `TNSA` 的术语定义。
3. 当前 `Examples/` 里没有独立 `rpa_*` 或 `tnsa_*` 应用目录。

因此，当前 book project 里关于 `RPA/TNSA` 的最准确写法只能是：

- `RPA/TNSA` 是理解 `laser_ion` 物理图像时需要引入的机制标签；
- 但当前本地 worktree 并没有把它们实现成独立的应用目录或强 regression 树；
- 所以它们现在属于“物理解释层”，不属于“本地应用目录层”。

这点和 `LWFA/PWFA` 不同。`LWFA/PWFA` 在 worktree 里至少有：

- `laser_acceleration`
- `plasma_acceleration`

两条真正的 application trees。`RPA/TNSA` 目前没有这一级的本地对象。

## 5. 多物理边界：`laser_ion` 是可分叉骨架，不是多物理全开 benchmark

`laser_ion` 当前最重要的另一层价值是：它是一个可分叉的 laser-target 骨架。

现有本地笔记已经压实：

1. field ionization
   - 通过 `do_field_ionization`
   - 接到 `InitIonizationModule()` 与 `doFieldIonization()`
2. collisions
   - 通过 `collision_names`
   - 接到 `CollisionHandler`
3. QED
   - 通过 `#ifdef WARPX_QED`
   - 接到 runtime attributes、product mapping 与 `InitQED()`

但当前 active regression 版本里，这些开关并没有一起打开。因此 `laser_ion` 当前更准确的定位是：

- `laser + target + diagnostics + multiphysics-ready boundary`

而不是：

- `field ionization + collisions + QED` 已被它单独完整证明。

它们各自的物理正确性仍主要由独立测试树兜底：

- `field_ionization`
- `collision`
- `qed`

## 6. 对应用综合章最重要的结论

把这条应用线收束之后，当前本地证据支持的最强结论是：

1. `laser_ion`
   - 是当前最强的 laser-target application entry；
   - CI 最硬断言是 diagnostics contract；
   - 还提供 PICMI front-end 和用户后处理脚手架；
   - 但不应被误写成已证明 `RPA/TNSA` 标度的强 benchmark。
2. `plasma_mirror`
   - 是典型 laser-solid surface-plasma application skeleton；
   - 当前只有 checksum baseline；
   - 还没有 PICMI 和独立 analysis。
3. `RPA/TNSA`
   - 在当前 worktree 里只是机制标签；
   - 不是独立 application tree。

因此，这条 TODO 最准确的收口方式不是写成：

```text
RPA/TNSA examples
```

而应该写成：

```text
laser-target applications
-> laser_ion
-> plasma_mirror
-> RPA/TNSA as mechanism labels, not standalone local trees
```
