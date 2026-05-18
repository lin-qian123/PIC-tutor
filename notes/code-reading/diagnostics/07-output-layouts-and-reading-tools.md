# Diagnostics 输出目录树与读取工具对照

绑定源码：

- `../warpx/Source/Diagnostics/FlushFormats/FlushFormatPlotfile.cpp`
- `../warpx/Source/Diagnostics/WarpXOpenPMD.cpp`
- `../warpx/Source/Diagnostics/FlushFormats/FlushFormatCheckpoint.cpp`

绑定文档与工具：

- `../warpx/Docs/source/dataanalysis/formats.rst`
- `../warpx/Docs/source/dataanalysis/yt.rst`
- `../warpx/Docs/source/dataanalysis/openpmd.rst`
- `../warpx/Docs/source/dataanalysis/openpmdviewer.rst`
- `../warpx/Docs/source/dataanalysis/openpmdapi.rst`
- `../warpx/Docs/source/usage/parameters.rst`
- `../warpx/Docs/source/usage/faq.rst`
- `../warpx/Tools/PostProcessing/read_raw_data.py`
- `../warpx/Tools/PostProcessing/plot_distribution_mapping.py`
- `../warpx/Tools/PostProcessing/plot_parallel.py`
- `../warpx/Tools/PostProcessing/video_yt.py`
- `../warpx/Tools/PostProcessing/yt3d_mpi.py`

## 1. 三类输出的落盘对象根本不同

同样是 `diags/` 下面的文件，三类 writer 面向的对象并不一样：

- `plotfile`
  面向分析视图，核心是 cell-centered diagnostics fields，加上可选粒子与 raw fields。
- `openPMD`
  面向标准化交换与生态工具，核心是 openPMD series 中的 `fields/particles` records。
- `checkpoint`
  面向 restart 恢复，核心是 WarpX 真实运行态，不是筛选后的 diagnostics view。

因此目录树也不能混着读。

## 2. `plotfile` 的典型目录树

按照 `FlushFormatPlotfile.cpp`，一次普通 full diagnostics 输出的典型结构可以概括成：

```text
diags/
  diag1NNNNNN/
    Header
    Level_0/
    Level_1/
    ...
    <species_name>/
    warpx_job_info
    WarpXHeader
    raw_fields/              # 仅在 plot_raw_fields=1 时出现
      Level_0/
      Level_1/
      ...
```

这里需要区分三层：

- `Header` 和 `Level_*`
  是 AMReX plotfile 主体，对应 cell-centered diagnostics 数据。
- `<species_name>/`
  是 AMReX 粒子 plotfile 路径，对应 writer 中 `tmp.WritePlotFile(...)` 的粒子输出。
- `raw_fields/`
  是 WarpX 额外挂出的原始 staggered/raw `MultiFab` 树，不属于标准 plotfile 主字段树。

另外同级还有：

- `warpx_job_info`
- `WarpXHeader`

前者偏运行记录，后者偏 WarpX 自己的附加状态说明。

## 3. `plotfile` 最典型的读取工具是 `yt`

WarpX 文档 `yt.rst` 里给出的标准入口就是：

```python
import yt
ds = yt.load('./diags/plotfiles/plt00000/')
```

典型用途分三类：

- 直接看 cell-centered fields：
  `yt.SlicePlot(...)`
- 读全域网格到 `numpy`：
  `ds.covering_grid(...).to_ndarray()`
- 看粒子相图：
  `yt.ParticlePhasePlot(...)`

这条工具链主要适合：

- full diagnostics / plotfile
- 以 field/particle analysis 为主的后处理
- AMR-aware 读取

## 4. `plotfile` 的 raw fields 需要专门工具，不是普通 `yt` 主路径

`raw_fields/` 不是默认 `yt.load(plotfile)` 那条主树的一部分。WarpX 自带的：

- `Tools/PostProcessing/read_raw_data.py`

就是专门为这一层服务的。它会去找：

```text
<plotfile>/raw_fields/Level_*/
```

并按 `*_H` header 解析 staggered/raw field 数据块。

所以：

- 要做普通物理分析，用 `yt` 主 plotfile 即可
- 要看 Yee/CKC/aux/cp 这类原始网格布局，就要转向 `raw_fields` 专用 reader

## 5. `openPMD` 的典型目录树

`WarpXOpenPMD.cpp` 里的 `GetFileName()` 和 `CloseStep()` 给出的目录信号很明确。典型结构可以概括成：

```text
diags/
  diag1/
    paraview.pmd
    openpmd_%06T.h5         # file-based HDF5 举例
```

如果 backend 不是 `h5`，后缀可能变成：

- `.bp5`
- `.bp4`
- `.json`

如果 encoding 不是 file-based，而是 group/variable based，则“一个 step 一个文件”这件事本身也会变化。但目录的核心仍然是：

- 一个 series 根目录
- 一个 `paraview.pmd` helper
- 一个或多个 openPMD backend 文件

真正的 fields/particles 记录结构主要在文件内部，而不在目录层级展开。

## 6. `openPMD` 的典型读取工具有两类

文档 `openpmd.rst` 明确把生态分成两条：

1. `openPMD-viewer`
2. `openPMD-api`

### `openPMD-viewer`

最轻便的入口是：

```python
from openpmd_viewer import OpenPMDTimeSeries
ts = OpenPMDTimeSeries('./diags/diag1/')
```

它适合：

- 交互式浏览
- Jupyter 中快速取 field/particle `numpy` 数组
- 读标准 openPMD particle/field 数据

### `openPMD-api`

适合：

- 保留完整 metadata
- 更精确控制 record/component 读取
- 并行/chunk 读取
- 与 pandas / dask / RAPIDS 等更深集成

也就是说：

- 想快速看结果，用 `viewer`
- 想写严肃 reader、调试 metadata、做并行数据流，用 `api`

## 7. `openPMD` 对 RZ 比 `plotfile` 更原生

FAQ 明确写了：

- openPMD 支持 detailed RZ modes
- AMReX plotfiles 默认给的是 `theta=0` 的重建 Cartesian slice

因此在 RZ 场景下，若目标是：

- 保留所有 mode
- 让后处理自行 reconstruction

优先级应是 openPMD，而不是 plotfile。

## 8. `checkpoint` 的典型目录树

从 `FlushFormatCheckpoint.cpp` 可以直接抽出典型结构：

```text
diags/
  chkNNNNNN/
    WarpXHeader
    warpx_job_info
    Level_0/
      Ex_fp
      Ey_fp
      Ez_fp
      Bx_fp
      ...
      DM
    Level_1/
      Ex_fp
      ...
      Ex_cp
      ...
      pml
      DM
    <species_name>/
    <laser_name>/
```

还会包含：

- synchronized `jx/jy/jz`
- `*_avg_*`
- PML checkpoint blocks
- reduced diagnostics checkpoint data

这不是给分析工具优雅浏览的目录，而是给 WarpX 自己恢复状态的目录。

## 9. `checkpoint` 最典型的“读取工具”其实不是 Python，而是 `amr.restart`

对 checkpoint 来说，首要读取者不是 `yt` 或 `openPMD-viewer`，而是 WarpX 本身：

```text
amr.restart = "../test_xxx/diags/chk000006"
```

因此 checkpoint 的首要使用场景是：

- 继续跑
- 崩溃恢复
- restart regression

而不是直接做终态分析。

当然，如果要读某些 checkpoint 粒子布局，WarpX 自带工具例如：

- `Tools/PostProcessing/plot_particle_path.py`

能解析 AMReX 粒子 header / particle data。但这属于辅助调试，不是 checkpoint 的主要消费方式。

## 10. `LoadBalanceCosts` 的读取链本身又是一类独立工具流

虽然 `LoadBalanceCosts` 属于 reduced diagnostics，不属于这三类 full diagnostics writer，但它在“读取工具”层面很有代表性，因为 WarpX 已经把它的后处理固化成：

- `Docs/source/usage/workflows/plot_distribution_mapping.rst`
- `Tools/PostProcessing/plot_distribution_mapping.py`

这条链的特点是：

- 直接读 `LBC.txt`
- 重建 `cost_arr` / `rank_arr`
- 画 distribution mapping 和负载热图

它提醒一个事实：并不是所有 diagnostics 都应该往 `yt` 或 openPMD 生态里塞。表格型 reduced diagnostics 往往就应该用专门的轻量 reader。

## 11. 一页对照：目录树、工具、场景

### `plotfile`

目录：

```text
diag1NNNNNN/
  Header
  Level_*/
  <species>/
  warpx_job_info
  WarpXHeader
  raw_fields/   # optional
```

典型工具：

- `yt`
- `Tools/PostProcessing/plot_parallel.py`
- `Tools/PostProcessing/video_yt.py`
- `Tools/PostProcessing/yt3d_mpi.py`
- `Tools/PostProcessing/read_raw_data.py`（仅 raw fields）

适用场景：

- 常规场/粒子分析
- AMR-aware 可视化
- raw staggered debug

### `openPMD`

目录：

```text
diag1/
  paraview.pmd
  openpmd_%06T.h5|bp5|bp4|json
```

典型工具：

- `openPMD-viewer`
- `openPMD-api`
- 也可被部分 `yt` 读取，但文档明确说 openPMD HDF5 在 yt 中无 mesh refinement 支持

适用场景：

- 标准化交换格式
- 读取粒子上的 `phi/E/B`
- RZ modes / richer metadata
- 与外部数据生态对接

### `checkpoint`

目录：

```text
chkNNNNNN/
  WarpXHeader
  warpx_job_info
  Level_*/
  <species>/
  <lasers>/
```

典型工具：

- WarpX 本体 `amr.restart`
- 少量辅助调试脚本

适用场景：

- restart
- 崩溃恢复
- regression continuity

## 12. 选择建议

如果目标是：

- “我要稳定分析场和粒子，并方便和现有 WarpX Python 后处理接轨”
  先选 `plotfile`
- “我要标准化文件、要粒子上的场、要 RZ mode 或要和外部数据工具链对接”
  先选 `openPMD`
- “我要接着跑、恢复状态、保留完整运行态”
  只能选 `checkpoint`

这三类输出不是“同一份数据的三个皮肤”，而是三种不同契约。
