# `ParticleThermalizer` 的真实验证入口与 checksum helper 边界

绑定源码与验证入口：

- `../warpx/Source/Particles/ParticleThermalizer/ParticleThermalizer.cpp`
- `../warpx/Source/Evolve/WarpXEvolve.cpp`
- `../warpx/Docs/source/usage/parameters.rst`
- `../warpx/Examples/Tests/particle_absorbing_boundary/inputs_test_1d_particle_absorbing_boundary`
- `../warpx/Examples/Tests/particle_absorbing_boundary/analysis.py`
- `../warpx/Examples/Tests/particle_absorbing_boundary/CMakeLists.txt`
- `../warpx/Examples/Tests/particle_absorbing_boundary/analysis_default_regression.py`
- `../warpx/Examples/Tests/resampling/analysis_default_regression.py`
- `../warpx/Examples/Physics_applications/capacitive_discharge/analysis_default_regression.py`

这一篇只做一件事：把上一轮对 thermalizer 的验证边界从“没有本地 example-level 入口”修正成更准确的说法。

结论先写在前面：

- `ParticleThermalizer` 在本地 WarpX checkout 里并不是完全没有 examples 覆盖。
- 现成入口是 `particle_absorbing_boundary`。
- 但这条覆盖是“吸收边界 + field-function laser + reduced diagnostic + thermalizer”的耦合 regression，不是隔离出来的 thermalizer-only 单元测试。

---

## 1. `particle_absorbing_boundary` 确实打开了 `particle_thermalizer.*`

`inputs_test_1d_particle_absorbing_boundary` 里直接给了：

```text
particle_thermalizer.normal = "z"
particle_thermalizer.start = 40e-6
particle_thermalizer.end = 50e-6
particle_thermalizer.momentum_threshold = 0.1
particle_thermalizer.theta = 0.02
particle_thermalizer.species = electrons
```

所以这里不是文档样例，也不是注释死代码，而是真正进入 regression 的运行参数。

同时这个输入还叠加了：

- `boundary.field_lo/hi = absorbing_silver_mueller`
- `boundary.particle_lo/hi = absorbing`
- `laser1.profile = parse_field_function`
- reduced diagnostic `PhaseSpaceElectrons = ParticleHistogram2D`

因此它从一开始就不是“纯 thermalizer 最小样例”，而是边界吸收问题里的一段局部热化吸收层。

---

## 2. analysis 断言的物理量确实依赖 thermalizer

`Examples/Tests/particle_absorbing_boundary/analysis.py` 的核心断言是：

- 读 `PhaseSpaceElectrons` 这个二维粒子直方图
- 只看
  - `z in [0, 50] um`
  - `uz in [-5, -1]`
  这块相空间区域
- 断言该区域总权重
  $$
  W_{\mathrm{fast,backward}} < 3.2\times 10^{20}
  $$

更关键的是脚本里有一句直接注释：

```python
# Without the thermalizer the total weight of particles in this region is > 1e22.
```

这说明 analysis 的目标不是单纯“边界吸收后剩余粒子要少”，而是更具体地在看：

- 靠近吸收边界的高速反向电子
- 是否被 thermalizer 显著压低

因此这条 regression 对 thermalizer 不是零覆盖，而是有明确断言对象的间接覆盖。

---

## 3. 当前最准确的验证边界

结合 `CMakeLists.txt` 可以把当前证据强度分成三层：

1. `analysis.py`
   - 真正的物理断言
   - 断言吸收边界附近的反向高速电子权重被压低
   - 因而间接验证 `ParticleThermalizer`
2. `analysis_default_regression.py --path diags/diagInst008000/`
   - 只是通用 checksum helper
   - 为同一输入再提供字段/粒子快照基线
3. 输入本身
   - 还同时覆盖 `parse_field_function` laser、absorbing particle boundary、Silver-Mueller field boundary 和 `ParticleHistogram2D`

所以当前对 thermalizer 最稳妥的说法应该是：

- 有本地 example-level regression 入口；
- 这条入口不是 isolated thermalizer test，而是 application-style coupled regression；
- 目前仍然缺少“只改 thermalizer、不耦合边界与 laser”的 dedicated validation。

---

## 4. checksum helper 的边界也要单独说清

这轮顺手把三个最容易被误写成“analysis = physics assertion”的 helper 重新压实了：

- `Examples/Tests/particle_absorbing_boundary/analysis_default_regression.py`
- `Examples/Tests/resampling/analysis_default_regression.py`
- `Examples/Physics_applications/capacitive_discharge/analysis_default_regression.py`

它们的共同点都是：

- 负责把当前输出和 benchmark JSON 做字段/粒子 checksum 对比；
- 本身不新增独立物理判据；
- 真正的 physics assertion 仍然在同目录下的专门 `analysis.py` 或同类脚本里。

这对后面继续清理 `example-regression-map.md` 很重要，因为不能把所有 `analysis_default_regression.py` 都混成“有物理断言的 analysis”。

---

## 5. 对第 4 章和 regression map 的回填结论

本轮之后，第 4 章里关于 thermalizer 的一句话应理解成：

- 不是“当前没有本地 thermalizer regression”
- 而是“当前没有 dedicated thermalizer-only regression，但 `particle_absorbing_boundary` 已提供一条耦合式的强间接验证”

对应地，`example-regression-map.md` 里 `particle_absorbing_boundary` 这一组条目也应该从单纯 `boundary condition` 提升成更准确的“absorbing boundary + thermalizer + reduced diagnostic”入口。
