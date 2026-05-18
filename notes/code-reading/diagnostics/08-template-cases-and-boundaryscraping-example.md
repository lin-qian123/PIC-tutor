# Diagnostics 固定模板案例页与 `BoundaryScraping/openPMD` 例子

绑定源码：

- `../warpx/Source/Diagnostics/BoundaryScrapingDiagnostics.cpp`
- `../warpx/Source/Diagnostics/FlushFormats/FlushFormatPlotfile.cpp`
- `../warpx/Source/Diagnostics/FlushFormats/FlushFormatOpenPMD.cpp`
- `../warpx/Source/Diagnostics/FlushFormats/FlushFormatCheckpoint.cpp`
- `../warpx/Source/Diagnostics/ParticleIO.cpp`

绑定文档：

- `../warpx/Docs/source/usage/parameters.rst`

绑定 examples：

- `../warpx/Examples/Physics_applications/thomson_parabola_spectrometer/inputs_test_3d_thomson_parabola_spectrometer`
- `../warpx/Examples/Physics_applications/thomson_parabola_spectrometer/analysis.py`
- `../warpx/Examples/Tests/point_of_contact_eb/analysis.py`
- `../warpx/Examples/Tests/scraping/analysis_rz_filter.py`

## 目标

把前几篇 diagnostics 笔记里分散出现的 writer 说明压成固定模板。今后书稿里遇到一类输出，优先按同一组问题组织：

1. 最小输入片段是什么。
2. 典型目录树长什么样。
3. 读者侧最直接的读取入口是什么。
4. 最适合解决什么问题。

## 模板 1：`plotfile`

### 最小输入片段

```text
diagnostics.diags_names = diag1

diag1.diag_type = Full
diag1.intervals = 10
diag1.fields_to_plot = Ex Ey Ez Bx By Bz rho
diag1.write_species = 1
```

如果不显式写 `diag1.format`，`FullDiagnostics` 默认就走 plotfile writer。

### 典型目录树

```text
diags/diag1/
  diag1000000/
    Header
    Level_0/
    <species>/
    warpx_job_info
    WarpXHeader
    raw_fields/   # optional
```

### 读取入口

常规分析入口：

```python
import yt
ds = yt.load("./diags/diag1/diag1000000/")
```

如果开了 `plot_raw_fields = 1`，再额外用：

```text
../warpx/Tools/PostProcessing/read_raw_data.py
```

### 适用场景

- 默认 field/particle 后处理。
- 需要 AMR-aware 的 `yt` 工作流。
- 需要同时看 diagnostics 视图和可选 `raw_fields`。

## 模板 2：`openPMD`

### 最小输入片段

```text
diagnostics.diags_names = diag1

diag1.diag_type = Full
diag1.format = openpmd
diag1.openpmd_backend = h5
diag1.intervals = 10
diag1.fields_to_plot = Ex Ey Ez Bx By Bz rho
diag1.write_species = 1
```

如果还想把场 gather 到粒子，可继续加：

```text
diag1.plot_phi = 1
diag1.plot_E = 1
diag1.plot_B = 1
```

但这条能力只允许 `diag_type = Full`。

### 典型目录树

```text
diags/diag1/
  paraview.pmd
  openpmd_000000.h5
  openpmd_000010.h5
```

也可能是 `bp4`、`bp5` 或 group/variable-based 编码。

### 读取入口

Jupyter/快速浏览：

```python
from openpmd_viewer import OpenPMDTimeSeries
ts = OpenPMDTimeSeries("./diags/diag1/")
```

需要完整 metadata 或并行读取时，用 `openPMD-api`。

### 适用场景

- 需要标准化输出格式。
- 需要 richer metadata、RZ mode 信息或对外交换。
- 需要 writer 阶段附加 `phi` / `E` / `B` on particles。

## 模板 3：`checkpoint`

### 最小输入片段

```text
diagnostics.diags_names = chk

chk.diag_type = Full
chk.format = checkpoint
chk.intervals = 100
```

重启时：

```text
amr.restart = ./diags/chk/chk000100
```

### 典型目录树

```text
diags/chk/
  chk000100/
    WarpXHeader
    warpx_job_info
    Level_0/
    <species>/
    <lasers>/
```

### 读取入口

首要入口不是 Python，而是 WarpX 本体：

```text
amr.restart = ./diags/chk/chk000100
```

### 适用场景

- 保留完整运行态。
- 中断后续跑。
- restart/reduced-diag checkpoint 状态恢复。

不要把它当成“另一种分析格式”。它序列化的是 restart contract，不是用户筛选后的 diagnostics 视图。

## 模板 4：`BoundaryScraping/openPMD`

### 最小输入片段

`thomson_parabola_spectrometer` 给出了最清楚的真实骨架：

```text
diagnostics.diags_names = screen

screen.diag_type = BoundaryScraping
screen.format = openpmd
screen.intervals = 1

hydrogen1_1.save_particles_at_zhi = 1
carbon12_6.save_particles_at_zhi = 1
carbon12_4.save_particles_at_zhi = 1
```

这里 `screen` 不是 field diagnostics，而是把从 `zhi` 边界离开的粒子写成 detector hit 记录。

### 典型目录树

```text
diags/screen/
  particles_at_zhi/
    paraview.pmd
    openpmd_000001.h5
    openpmd_000002.h5
    ...
```

如果是 EB scraping，则目录会变成 `particles_at_eb/`。

### 读取入口

`thomson_parabola_spectrometer/analysis.py` 的真实入口是：

```python
from openpmd_viewer import OpenPMDTimeSeries
series = OpenPMDTimeSeries("./diags/screen/particles_at_zhi/")
```

EB 几何接触点案例也是同一路径：

```python
ts_scraping = OpenPMDTimeSeries("./diags/diag2/particles_at_eb/")
```

常见读取变量包括：

- `x`, `y`, `z`
- `ux`, `uy`, `uz`
- `w`
- `id`
- `stepScraped`
- `deltaTimeScraped`
- `timeScraped`
- `nx`, `ny`, `nz` 仅 EB scraping 有

这里还要补一条容易漏掉的边界：`thomson_parabola_spectrometer` 不只是 writer 示例，它本身就是一条强 regression。`CMakeLists.txt` 里 active test 会同时跑：

- `analysis.py`
- `analysis_default_regression.py --path diags/diag1`

前者会：

1. 从 `screen/particles_at_zhi/` 读取 detector hit 的 `x/y/z/id`
2. 从 `diag0` 的初始 full diagnostic 读取同一批粒子的 `uz/id/mass`
3. 按 `id` 回连 hit 和初始粒子
4. 用初始 `uz` 计算入射能量
5. 在 detector 平面重建按 species 和初始能量着色的 TPS 分离图

因此这组例子当前更准确的定位是：

- `BoundaryScraping/openPMD + prescribed-field test-particle optics`

而不是：

- 普通 `PEC / conducting boundary` test
- 或仅仅一个 writer smoke test

### 适用场景

- 探测器、屏幕、谱仪末端 hit 记录。
- 吸收边界通量统计。
- EB 接触点位置和法向验证。
- Python callback 之外的持久化 scraped-particle 输出。

## `BoundaryScraping` 的实现边界

和前面三类模板相比，`BoundaryScraping` 还要额外记住四条边界：

1. 只支持 `openPMD`。
2. 只写粒子，不写场。
3. species 必须先打开 `save_particles_at_xlo/.../eb` 之类的收集开关。
4. filter 在写出时才应用，因此 `plot_filter_function` 里的 `t` 是 flush 时间，不是粒子真正撞边界的时间。

## 与 Python buffer 路径的分工

`BoundaryScrapingDiagnostics` 和 Python `sim.extension.get_particle_boundary_buffer()` 共享同一份 `ParticleBoundaryBuffer`，但消费语义不同：

- diagnostics flush 后会自动清空对应 boundary buffer；
- Python wrapper 需要用户手动 `clear_buffer()`；
- diagnostics 适合持久化输出；
- Python wrapper 适合 step-by-step callback 或在线控制逻辑。

因此，“是要开 `BoundaryScraping` writer，还是直接读 Python buffer”，本质上是在选：

- 文件化的持久记录；
- 还是内存中的即时事件流。
