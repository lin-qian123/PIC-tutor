# `Particles` 验证入口：`particle_pusher`、`single_particle`、`larmor`、`photon_pusher`

绑定源码：

- `../warpx/Examples/Tests/particle_pusher`
- `../warpx/Examples/Tests/single_particle`
- `../warpx/Examples/Tests/larmor`
- `../warpx/Examples/Tests/photon_pusher`
- `../warpx/Source/Particles/Pusher/PushSelector.H`
- `../warpx/Source/Particles/PhotonParticleContainer.cpp`
- `../warpx/Source/Evolve/WarpXEvolve.cpp`
- `../warpx/Docs/source/usage/parameters.rst`

这一组 regression 不是同一类测试。

- `particle_pusher`：强单粒子分析，直接验证带电粒子 momentum pusher。
- `single_particle`：拆成两个独立合同。
  - `inputs_test_2d_bilinear_filter` 验证 current filter。
  - `inputs_test_1d_synchronize_velocity` 验证 diagnostics 前的半步速度同步。
- `larmor`：当前没有独立 analysis，主要是应用级 checksum 基线。
- `photon_pusher`：强单粒子分析，直接验证 massless 位置推进与动量不变。

## 1. `particle_pusher`：Higuera-Cary 的 force-free 漂移约束

输入 `inputs_test_3d_particle_pusher` 做的事情很窄：

- `algo.particle_pusher = "higuera"`
- 单个 positron
- `u = (0, 19.9749843554, 0)`，对应 `gamma = 20`
- 外场
  $$
  B_z = 1,\qquad E_x = -v_y B_z
  $$
- `max_step = 10000`

analysis 只检查一件事：最终
$$
x \approx 0.
$$

这不是一般性的 orbit test，而是 force-free configuration 下的 drift-invariance test。它直接对应：

- `PushSelector.H` 里的 `ParticlePusherAlgo::HigueraCary`
- `UpdateMomentumHigueraCary(...)`
- 以及后续 `UpdatePosition(...)`

所以它真正验证的是：

1. `PushSelector.H` 的运行时分派确实走到 Higuera-Cary。
2. Higuera-Cary 在强 relativistic、`E + v\times B = 0` 的构型下不产生可见横向漂移误差。
3. 这个误差容差当前被固定在 `1e-3`。

`test_3d_particle_pusher.json` 只是对同一输出再加一层 checksum 基线，不增加新的物理断言。

把这条 regression 放回 Higuera-Cary 2017，会看到它在本地验证树里的位置非常明确：

- 它不是复现论文第 VI 节的 Poincare surface-of-section；
- 也不是完整测试 volume-preservation / resonance-island 结论；
- 它更像论文第 IV 节 `E\times B` / force-free preserving 边界在 WarpX 里的最小强断言。

也就是说，当前本地源码树里最能直接支撑 Higuera-Cary 论文主线的不是 `larmor`，而正是这条 `particle_pusher` force-free test。

## 2. `single_particle` 其实是两类不同验证

### 2.1 `inputs_test_2d_bilinear_filter`：单粒子电流滤波合同

这个 test 名字容易误导。它并不是在验证单粒子轨道。

输入只跑一步：

- 2D
- 一个沿 `x` 方向超 relativistic 的电子
- `warpx.use_filter = 1`
- `warpx.filter_npass_each_dir = 1 5`
- `algo.field_gathering = energy-conserving`

analysis 的做法是：

1. 先手工构造未滤波的 `Jx` 理论数组。
2. 再构造二维 bilinear filter 核。
3. 用 `signal.convolve2d(..., boundary="symm")` 得到理论 `Jx_filtered`。
4. 读 plotfile 里的 `jx`，比较两者的相对误差。

因此这条 regression 真正验证的是：

- 单粒子沉积后的 current stencil
- `warpx.use_filter`
- `warpx.filter_npass_each_dir`
- WarpX bilinear current filtering 的对称边界处理

它更接近 `deposition/filter` test，而不是 `pusher` test。

### 2.2 `inputs_test_1d_synchronize_velocity`：diagnostics 半步速度同步

另一个 `single_particle` test 完全不同：

- 1D
- `algo.maxwell_solver = none`
- 一个电子静止起步
- 常量外场 `E_z = -1`
- `warpx.synchronize_velocity_for_diagnostics = 1`
- diagnostics 在第 5 步输出

analysis 先在 Python 里手工做：

1. 半步 backward velocity shift
2. 5 步 leapfrog
3. diagnostics 前再加半步，得到 synchronized velocity

再和 plotfile 输出比较。

这条 regression 直接验证：

- `warpx.synchronize_velocity_for_diagnostics`
- `WarpXEvolve.cpp` 里 diagnostics 前的 `SynchronizeVelocityWithPosition()`
- diagnostics 写出的 `u` 不是平时 leapfrog 中滞后半步的速度，而是与位置同时间层的速度

因此它不是验证 Boris/Vay/Higuera-Cary 的物理轨道精度，而是验证 diagnostics contract。

## 3. `larmor`：当前主要是应用级 checksum

`inputs_test_2d_larmor` 打开的是：

- 2D
- `electron` 与 `positron` 各一个
- 常量外部粒子磁场 `B_y`
- `algo.particle_shape = 3`
- `warpx.do_dive_cleaning = 1`
- PML
- `amr.max_level = 1`
- 同时写 normal diagnostics 和 `plot_raw_fields`

这个组合说明它并不只是“最小回旋半径公式单测”。它把下面这些一起绑进去了：

- 外部粒子磁场 gather
- 带电正负粒子相反旋向
- mesh refinement
- PML
- `div(E)` cleaning
- raw/full diagnostics 一致性

但当前 `CMakeLists.txt` 没有独立 analysis，只有：

- `analysis = OFF`
- `checksum = analysis_default_regression.py`

因此它当前应被归类为：

- charged particle gyro-motion / external particle field / MR / PML 的应用级 checksum 基线

而不是“已经有解析半径/回旋频率强断言”的 test。

## 4. `photon_pusher`：massless 直线传播与动量守恒

`inputs_test_3d_photon_pusher` 建了 16 个 photon species，覆盖：

- 六个坐标轴正负方向
- 对角方向
- 动量大小 `1` 和 `10`

analysis 的理论解非常直接：

$$
\mathbf{x}(t)=\mathbf{x}_0 + ct\,\hat{\mathbf{u}},
\qquad
\mathbf{p}(t)=\mathbf{p}_0.
$$

然后逐 species 比较：

- 位置相对误差
- 动量相对误差

所以这条 regression 直接打到：

- `PhotonParticleContainer::PushPX()`
- `UpdatePosition(...)` 里的 massless branch
- photon 不做 charge/current deposition 的合同
- photon 动量在无场情况下保持不变

它不是 QED photon emission test，也不是 diagnostics test；它验证的是最基本的 photon transport kernel。

## 5. 这一组 test 和 `Particles` 主线的对应关系

把这四组合起来看，当前它们覆盖的是四种不同层次：

1. `particle_pusher`
   - 带电粒子 momentum pusher 的强单粒子物理断言
2. `single_particle/inputs_test_2d_bilinear_filter`
   - 单粒子沉积之后的 current filter 合同
3. `single_particle/inputs_test_1d_synchronize_velocity`
   - diagnostics 输出时间层合同
4. `photon_pusher`
   - massless particle transport kernel
5. `larmor`
   - 当前仍主要是外部粒子场 + MR/PML/div-cleaning 的 checksum 基线

也就是说，这一组验证入口并不能被统称为“single-particle orbit tests”。更准确的说法是：

- 一部分在测 pusher
- 一部分在测 diagnostics contract
- 一部分在测 filter
- 一部分在测 photon transport
- `larmor` 目前只是把这些机制组合进一个稳定性基线

## 6. 当前验证边界

这轮阅读后，当前本地源码树里这一组 test 的边界可以明确成：

- `particle_pusher`：有强 analysis，不只是 checksum。
- `single_particle`：有两条强 analysis，但验证对象不是同一个。
- `photon_pusher`：有强 analysis，不只是 checksum。
- `larmor`：当前没有独立解析 analysis，仍主要依赖 checksum。

因此后续书稿里如果要写“WarpX 已经用 regression 显式验证了某某单粒子轨道”，可以直接说：

- Higuera-Cary 的 force-free relativistic push：有。
- diagnostics 速度同步：有。
- photon 直线传播：有。
- bilinear filter 的单粒子沉积后滤波：有。
- Larmor 半径/频率的独立解析对照：当前这组里没有看到，不能夸大。

进一步收束到 Higuera-Cary 这篇文献时，当前最准确的项目内配对是：

- `particle_pusher`
  - 对应 Higuera-Cary 在 relativistic force-free / drift-preservation 构型下的最小本地强证据；
- `larmor`
  - 目前还只是 charged-particle gyro-motion / external-B / MR / PML 的 checksum 基线，
  - 不能冒充论文第 VI 节 practical-timestep topology / resonance-island 结论的 dedicated reproduction；
- 论文里的 volume-preservation 与 topology 比较
  - 当前主要仍由文献论证承担，
  - 本地还缺一个直接按 Poincare section 或 invariant drift 组织的专门 regression。
