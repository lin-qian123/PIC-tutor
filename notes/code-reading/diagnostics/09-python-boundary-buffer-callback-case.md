# Python `ParticleBoundaryBufferWrapper` 最小边界消费案例

绑定源码：

- `../warpx/Source/Python/WarpX.cpp`
- `../warpx/Source/Python/Particles/ParticleBoundaryBuffer.cpp`
- `../warpx/Python/pywarpx/particle_containers.py`

绑定文档：

- `../warpx/Docs/source/usage/workflows/python_particle_boundary_data.rst`

绑定 examples：

- `../warpx/Examples/Tests/particle_boundary_scrape/inputs_test_3d_particle_scrape_picmi.py`
- `../warpx/Examples/Physics_applications/spacecraft_charging/inputs_test_rz_spacecraft_charging_picmi.py`

前一篇已经把 `BoundaryScraping/openPMD` 的文件化路径固定成模板。这一篇只回答另一条并排路径：如果不想先写文件，而是直接在 Python 里消费 `ParticleBoundaryBuffer`，最小工作流到底长什么样。

## 两种 Python 使用模式

从本地 examples 看，`ParticleBoundaryBufferWrapper` 至少有两种稳定用法：

1. 运行结束后统一检查 buffer。
2. 在 simulation callback 或物理控制逻辑里，把 buffer 当成即时事件流。

这两种路径底层是同一份 `ParticleBoundaryBuffer`，区别只在消费时机。

## 模式 A：运行结束后统一检查 buffer

`particle_boundary_scrape` 是最小、最干净的例子。它的 species 只打开：

```python
electrons = picmi.Species(
    particle_type="electron",
    name="electrons",
    initial_distribution=uniform_plasma_elec,
    warpx_save_particles_at_xhi=1,
    warpx_save_particles_at_eb=1,
)
```

也就是说，不需要先开 `BoundaryScrapingDiagnostics`，只要打开 `save_particles_at_*`，WarpX 就会持续把 scraped particles 累积到内存 buffer。

运行结束后，例子直接：

```python
from pywarpx import particle_containers

particle_buffer = particle_containers.ParticleBoundaryBufferWrapper()
```

然后依次做三件事。

### A1. 先查 buffer 大小

```python
n = particle_buffer.get_particle_boundary_buffer_size("electrons", "eb")
```

这给的是累计到当前时刻的 scraped particle 数，不是“本步增量”。

### A2. 再按属性读取 tile 级数组

例如读取 `stepScraped`：

```python
scraped_steps = particle_buffer.get_particle_boundary_buffer(
    "electrons", "eb", "stepScraped", 0
)
```

或读取权重：

```python
weights = particle_buffer.get_particle_boundary_buffer(
    "electrons", "eb", "w", 0
)
```

这些返回值都是“每个 tile 一条数组”的列表，不是自动拼平的一整块数组。因此几乎所有真实用法都要自己做一次 tile 级归约，例如：

```python
n = sum(len(arr) for arr in weights)
```

### A3. 最后手动清空

```python
particle_buffer.clear_buffer()
```

这个清空动作是 Python 路径必须显式做的；否则 buffer 会继续累计。

## 模式 B：把 buffer 当即时事件流

`spacecraft_charging` 给了更像“真实应用”的例子。它同时做两件事：

1. 开一个 `ParticleBoundaryScrapingDiagnostic`，把 EB scraped particles 最终写成 openPMD。
2. 在 Python 里直接读取同一个 EB buffer，在线计算 spacecraft 的净收集电荷。

相关 species 只需要：

```python
electrons = picmi.Species(
    ...,
    warpx_save_particles_at_eb=1,
)

protons = picmi.Species(
    ...,
    warpx_save_particles_at_eb=1,
)
```

然后 diagnostics 侧是：

```python
part_scraping_boundary_diag = picmi.ParticleBoundaryScrapingDiagnostic(
    name="diag2",
    period=-1,
    species=[electrons, protons],
    warpx_format="openpmd",
)
```

注意这个例子把 `period=-1`，只在模拟末尾落盘一次。这样中间所有 scraped particles 都会继续留在同一个内存 buffer 里，供 Python 侧读取。

这组例子的 regression 也不是只检查“buffer 能不能读”。`Examples/Physics_applications/spacecraft_charging/analysis.py` 会把每个输出步的最小势值拿出来，拟合

$$
\phi(t)=v_0\left(1-e^{-t/\tau}\right),
$$

然后要求：

- 拟合得到的 `v0` 与基准值的相对误差小于 `4%`
- 拟合得到的 `tau` 与基准值的相对误差小于 `20%`

所以 `spacecraft_charging` 实际上同时验证了三层东西：

1. `ParticleBoundaryBufferWrapper` 在线累计 EB 收集电荷
2. Python callback 用 `set_potential_on_eb(...)` 动态改写导体势
3. 这样闭合出来的 RZ electrostatic charging 动力学是否还能回到正确的浮动电位时间尺度

真正的在线消费函数是：

```python
def compute_actual_charge_on_spacecraft():
    charge = {"electrons": -scc.e, "protons": scc.e}
    q_spacecraft = 0
    particle_buffer = ParticleBoundaryBufferWrapper()
    for species in charge.keys():
        weights = particle_buffer.get_particle_boundary_buffer(species, "eb", "w", 0)
        sum_weights_over_tiles = sum([w.sum() for w in weights])
        ntot = float(mpi.COMM_WORLD.allreduce(sum_weights_over_tiles, op=mpi.SUM))
        q_spacecraft += ntot * charge[species]
    return q_spacecraft
```

这里的关键不是语法，而是语义：

- 它读的是累计到当前时刻的 EB buffer；
- 它按 tile 先局部求和，再 MPI 汇总；
- 它没有在函数里 `clear_buffer()`，因为后面还要把同一批事件交给 diagnostics 末尾落盘。

## `get_particle_scraped_this_step()` 何时更合适

如果逻辑要求“只处理本步新撞到边界的粒子”，就不该先读全部累计 buffer 再自己比 `stepScraped`。高层 wrapper 已经给了更直接的入口：

```python
data = particle_buffer.get_particle_scraped_this_step(
    "electrons", "eb", "w", 0
)
```

它内部做的事情其实很简单：

1. 读取当前 `istep(level)`。
2. 读取请求的 `comp_name`。
3. 再读取同一批粒子的 `stepScraped`。
4. 对每个 tile 做 `data[step == current_step]`。

因此它适合：

- 二次发射；
- 边界反应；
- 每步通量统计；
- callback 内只想处理“这一步刚发生的撞边界事件”。

## 最小并排模板

如果只想把 Python 路径最小化到能直接复用，模板可以压成下面这样。

### 模板 1：运行后统一检查

```python
from pywarpx import particle_containers

particle_buffer = particle_containers.ParticleBoundaryBufferWrapper()
n = particle_buffer.get_particle_boundary_buffer_size("electrons", "eb")
weights = particle_buffer.get_particle_boundary_buffer("electrons", "eb", "w", 0)
total_weight = sum(w.sum() for w in weights)
particle_buffer.clear_buffer()
```

适用场景：

- regression 自检；
- 模拟结束后统一统计；
- 不需要每步即时响应的后处理逻辑。

### 模板 2：每步或在线消费

```python
from pywarpx.particle_containers import ParticleBoundaryBufferWrapper

particle_buffer = ParticleBoundaryBufferWrapper()
weights_this_step = particle_buffer.get_particle_scraped_this_step(
    "electrons", "eb", "w", 0
)
charge_this_step = sum(w.sum() for w in weights_this_step)
```

适用场景：

- callback 驱动的边界物理；
- secondary emission；
- 在线电荷/粒子通量控制。

## 和 `BoundaryScrapingDiagnostics` 的分工

现在可以把两条路径的边界写得更干净：

- `BoundaryScrapingDiagnostics`
  - 负责文件化持久输出；
  - flush 后自动清空对应 boundary buffer；
  - 适合 detector、谱仪、离线分析。
- `ParticleBoundaryBufferWrapper`
  - 负责 Python 侧即时访问；
  - 默认不会自动清空；
  - 适合 callback、控制回路、在线统计。

`spacecraft_charging` 证明这两条路可以并行存在，但前提是你得清楚谁在什么时候清空 buffer。

如果 diagnostics 设成频繁 flush，那么 Python 侧读到的累计事件会被 writer 周期性截断；如果 diagnostics 设成 `period=-1` 或根本不开 writer，Python 才能把它当长期累计事件池来用。

## `secondary_ion_emission`：scraped buffer 被直接拿来实现边界物理

前面的 `particle_boundary_interaction` 更像“用 scraped buffer 自己实现反射模型”，而 `Examples/Tests/secondary_ion_emission/` 则更进一步：它直接把 `ParticleBoundaryBufferWrapper` 变成边界物理源项。

这组 RZ PICMI 输入里，离子 species 打开：

- `warpx_save_particles_at_eb = 1`

然后在 `afterstep` callback 中读取：

- `r/theta/z`
- `ux/uy/uz`
- `nx/ny/nz`
- `deltaTimeScraped`
- `w`

接着按给定的次级发射模型 `sigma_nascap(energy)` 决定每个撞击离子产生多少次级电子，再按热分布加法向镜像规则重注入电子。

这组 regression 的 analysis 不是只看“callback 能不能跑”，而是做两层硬断言：

1. 对当前固定随机种子与 4 个入射离子，最终必须恰好产生 2 个电子；
2. 把每个电子按其速度反向传播到离子撞击球形 EB 的时刻后，要求它与解析撞击点的相对距离低于 `2%`

因此 `secondary_ion_emission` 的意义非常具体：

1. `ParticleBoundaryBufferWrapper` 不只是诊断接口，它足以承载真正的边界二次发射物理；
2. `deltaTimeScraped + normal + impact position` 这组几何元数据已经足够支持“本步撞击、本步再发射”的 callback 闭环；
3. 当前本地 checkout 对 scraped-buffer 驱动边界物理的最直接强基准，不是 `spacecraft_charging`，而是这一组次级电子发射 test。
