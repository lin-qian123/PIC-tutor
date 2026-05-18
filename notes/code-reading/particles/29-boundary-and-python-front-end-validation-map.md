# `particle_boundary_interaction`、`particle_boundary_process`、`particle_thermal_boundary` 与 `plasma_lens_python` 的验证边界

绑定对象：

- `../warpx/Examples/Tests/particle_boundary_interaction`
- `../warpx/Examples/Tests/particle_boundary_process`
- `../warpx/Examples/Tests/particle_thermal_boundary`
- `../warpx/Examples/Tests/plasma_lens/inputs_test_3d_plasma_lens_python.py`
- `../warpx/Source/Particles/ParticleBoundaries.cpp`
- `../warpx/Source/Particles/ParticleBoundaries_K.H`
- `../warpx/Python/pywarpx/particle_containers.py`
- `../warpx/Python/pywarpx/picmi.py`
- `../warpx/Source/Python/Particles/MultiParticleContainer.cpp`

这一组条目都落在粒子边界与 Python front-end 的交界处，但它们各自验证的对象不同：

- `particle_boundary_interaction`：Python callback + boundary buffer 驱动的自定义 EB 镜面反射
- `particle_boundary_process`：absorbing boundary 的随机反射模型与 scraped-particle buffer
- `particle_thermal_boundary`：thermal particle boundary 的总能量稳定性
- `plasma_lens_python`：纯 Python 参数 API 是否能把 repeated-plasma-lens 正确落到与 native/PICMI 相同的 external-particle-field 主链

---

## 1. `particle_boundary_interaction`：真正验证的是“用 Python callback 消费 scraped buffer 并自行重注入”

### 1.1 输入不是内建 reflecting boundary，而是 absorbing + afterstep callback

`inputs_test_rz_particle_boundary_interaction_picmi.py` 并没有直接把 EB 行为交给 WarpX 内部“自动反射”：

- 粒子边界是：
  - `upper_boundary_conditions_particles=["absorbing", "reflecting"]`
  - `lower_boundary_conditions_particles=["none", "reflecting"]`
- EB 是一个半径 `0.2` 的球：
  - `implicit_function="-(x**2+y**2+z**2-radius**2)"`
- species 打开：
  - `warpx_save_particles_at_eb=1`

真正关键的是 `callbacks.installafterstep(mirror_reflection)`。

`mirror_reflection()` 每步都会：

1. 用 `ParticleBoundaryBufferWrapper` 读出“这一时间步刚刚撞到 EB 的粒子”
2. 读取它们的：
   - `deltaTimeScraped`
   - `r/theta/z`
   - `ux/uy/uz`
   - `w`
   - `nx/ny/nz`
3. 根据法向做镜面反射
4. 按剩余时间 `dt - delta_t` 把反射后粒子推进到当前步末
5. 再 `electrons.add_particles(...)` 重新塞回主容器

所以这组 test 根本不是“WarpX 内建 reflecting EB”的 regression，而是：

- scraped buffer 是否带出了足够的几何和时间信息
- Python callback 是否能用这些信息构造一个自定义 boundary-interaction model

### 1.2 analysis 验证的是完整的几何反射轨道

`analysis.py` 读取最终一步 openPMD 输出中的电子位置，再从 `warpx_used_inputs` 里恢复：

- 球半径
- 初始位置
- 初始 proper velocity

然后解析地做三步：

1. 求直线轨道与球面的第一次交点
2. 按表面法向做镜面反射
3. 用剩余仿真时间继续推进

最后比较数值最终位置和解析最终位置，要求：

- `x` 相对误差 `< 0.02`
- `z` 相对误差 `< 0.02`
- `y` 仍接近 0

因此 `particle_boundary_interaction` 真正验证的是：

- `ParticleBoundaryBufferWrapper.get_particle_scraped_this_step(...)`
- EB buffer 中的 `deltaTimeScraped`
- EB buffer 中的表面法向 `nx/ny/nz`
- Python callback 重注入

这一整条“自定义交互模型”主链。

### 1.3 这组 regression 的定位

这不是普通 boundary-condition test，也不是普通 Python wrapper smoke test。

它更准确的分类应当是：

- `particles / boundary interaction / Python callback / scraped-buffer geometry`

---

## 2. `particle_boundary_process`：当前其实分成两条不同强度的合同

### 2.1 `test_2d_particle_reflection_picmi`：无独立 analysis，但输入脚本内自检很强

`inputs_test_2d_particle_reflection_picmi.py` 设置的是 domain particle boundary，不是 EB：

- `lower_boundary_conditions_particles=["open", "absorbing"]`
- `upper_boundary_conditions_particles=["open", "absorbing"]`

同时打开：

- `warpx_save_particles_at_zhi=1`
- `warpx_save_particles_at_zlo=1`
- `warpx_reflection_model_zhi="0.5"`

这里关键语义是：absorbing boundary 本身允许带随机反射概率，`reflection_model_zhi(E)` 在源码里最终会编译成 parser：

```cpp
data.reflection_model_zhi = reflection_model_zhi_parser->compile<1>();
```

而真正 kernel 行为在 `ParticleBoundaries_K.H` 里：

- absorbing boundary 默认把粒子判 lost
- 但可以用 `reflection_model_*` 给出随机反射概率

这个 test 虽然 `analysis = OFF`，但输入脚本自身在 `sim.step(max_steps)` 之后直接检查：

- `z_hi` buffer 中粒子数是 63
- `z_lo` buffer 中粒子数是 67
- `z_hi` 的 `stepScraped` 全都等于 4
- `z_lo` 的 `stepScraped` 全都等于 8

所以它不是纯 checksum，而是：

- `reflection_model_zhi="0.5"` 的随机反射语义
- zlo/zhi 两侧 scraped buffer 分流
- `stepScraped` 时间戳

这组边界 buffer 合同的脚本内自检。

### 2.2 `test_3d_particle_absorption`：analysis 只检查“粒子被吸收消失”

`inputs_test_3d_particle_absorption` 与 `analysis_absorption.py` 这组则更简单：

- 初始是一束电子撞向一个立方体 EB
- `analysis_absorption.py` 只检查：
  - 第 40 步有 612 个电子
  - 第 60 步电子数变成 0

这和 `particle_boundary_scrape` native 入口在物理断言上很接近，但这里的命名更偏“boundary process / absorption”。

### 2.3 当前能得出的保守结论

`particle_boundary_process` 当前不是一个统一的“边界处理 test”，而是两条不同强度的路径：

1. 2D PICMI 反射模型：
   - 主要验证 `reflection_model_zhi(E)` + scraped buffer 时间戳
2. 3D absorption：
   - 主要验证 EB 吸收后粒子从主 species 中消失

因此索引里不应简单标成 `boundary condition`。

---

## 3. `particle_thermal_boundary`：真正验证的是 thermal particle boundary 下的能量账本稳定性

### 3.1 输入打开的是 domain thermal boundary，不是 `ParticleThermalizer`

`inputs_test_2d_particle_thermal_boundary` 设置的是：

- `boundary.particle_lo = thermal thermal`
- `boundary.particle_hi = thermal thermal`
- `boundary.electrons.u_th = uth_e`
- `boundary.C.u_th = uth_C`

这不是上一轮已经整理过的 `particle_thermalizer.*` 局部热化层，而是粒子域边界本身就是 thermal boundary。

对应源码在：

- `ParticleBoundaries.cpp`
  - `SetThermalVelocity(...)`
- `ParticleBoundaries_K.H`
  - 边界命中后 `thermalize_boundary_particle(...)`

实现结构是：

1. 先像反射边界一样处理位置
2. 再用 `generateGaussianFluxDist` 和高斯切向速度重采样出新的动量分量

### 3.2 analysis 不是看单粒子，而是看总能量是否失控

`analysis.py` 读取两个 reduced diagnostics：

- `EF.txt`：field energy
- `EN.txt`：particle energy

然后断言：

- 最终场能不能无限长大：
  - `final_Fenergy / init_Fenergy < 40`
  - `final_Fenergy < 5e-5`
- 粒子总能量相对初值偏离不超过 2%

因此这组 regression 的真正验证对象是：

- thermal particle boundary 在长时间粒子出入边界时，不应导致粒子总能量明显漂移
- 同时也不能把数值噪声注入成不可接受的场能增长

这是一个总量稳定性 test，不是单次边界散射几何 test。

### 3.3 当前最准确的分类

它更适合记成：

- `particles / thermal boundary / reduced-diagnostic energy stability`

而不是与 `ParticleThermalizer` 混写。

---

## 4. `plasma_lens_python`：physics analysis 沿用不变，新增的是纯 Python 参数前端覆盖

### 4.1 它复用同一个 `analysis.py`

`test_3d_plasma_lens_python` 在 `CMakeLists.txt` 里直接复用：

- 与 native 版本同一个 `analysis.py`
- 与其它 plasma-lens 条目同一个 checksum helper

所以它验证的物理量没有变化，仍然是：

- 两颗测试电子穿过 lens 序列后的
  - 最终 `x/y`
  - 最终 `ux/uy`
- 与解析 lens 串联模型比较

### 4.2 这条变体真正新增的东西是 Python front-end

`inputs_test_3d_plasma_lens_python.py` 不是 PICMI，也不是 native inputs，而是直接用 `pywarpx` 参数对象：

- `particles.E_ext_particle_init_style = "repeated_plasma_lens"`
- `particles.B_ext_particle_init_style = "repeated_plasma_lens"`
- `particles.repeated_plasma_lens_* = ...`
- 最后 `warpx.init(); warpx.step(max_step)`

因此它新增覆盖的不是物理主链，而是：

- 纯 Python front-end 参数 API
- 到 C++ `MultiParticleContainer` / `GetExternalEBField` 主链的接线

### 4.3 当前本地源码树里，这条接线的关键证据

在 `pywarpx/picmi.py` 之外，WarpX 还暴露了 Python 侧直接改 lens 参数的接口：

- `Source/Python/Particles/MultiParticleContainer.cpp`
  - `set_plasma_lens_strength(...)`

虽然这个测试输入本身没有调用 `set_plasma_lens_strength(...)`，但它说明 Python front-end 并不只是“把配置写到输入文件”，而是本来就预留了直接改 repeated-plasma-lens 强度的 runtime API。

所以 `plasma_lens_python` 更准确的意义是：

- 与 native / PICMI / boosted / hard-edged / short-lens 一样共享同一 physics analysis
- 但额外证明了纯 Python 参数前端也能把 repeated-plasma-lens 正确接到同一 external-particle-field 主链

---

## 5. 这组条目对 `Particles` validation 图景的补充

把这四组连起来之后，当前 `Particles` 的边界与 Python 验证层可以清楚分成三类：

1. `particle_boundary_interaction`
   - scraped buffer + `deltaTimeScraped` + `nx/ny/nz`
   - Python callback 自定义重注入模型
2. `particle_boundary_process` 与 `particle_thermal_boundary`
   - boundary kernel 自带的 absorbing / probabilistic reflection / thermalization 合同
   - 分别用 buffer 时间戳或 reduced-diag 能量账本验证
3. `plasma_lens_python`
   - 物理 analysis 不变
   - 新增的是 pure Python front-end 到 external-particle-field 主链的覆盖

因此它们都不该再停留在 `general / to classify`，但也不该被混成同一类“边界条件测试”。
