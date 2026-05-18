# `Tools/Parser`、`Tools/PostProcessing`、`Tools/Algorithms` 的真实边界

绑定源码：

- `../warpx/Tools/Parser/input_file_parser.py`
- `../warpx/Tools/PostProcessing/read_raw_data.py`
- `../warpx/Tools/PostProcessing/plot_timestep_duration.py`
- `../warpx/Tools/Algorithms/stencil.py`
- `../warpx/Tools/Algorithms/psatd.ipynb`
- `../warpx/Tools/Algorithms/psatd_pml.ipynb`

绑定现有项目笔记：

- `notes/code-reading/utils/01-parser-system.md`
- `notes/code-reading/diagnostics/07-output-layouts-and-reading-tools.md`
- `notes/code-reading/fieldsolver/11-psatd-coefficient-derivation.md`

这一节的重点不是把 `Tools/*` 当成又一个 runtime 模块，而是把它和已经精读过的 `Source/*` 主链区分开。

## 1. `Tools/Parser` 不是运行时 parser

当前 top-level `Tools/Parser` 只有一个脚本：

- `input_file_parser.py`

它的 `parse_input_file(input_file)` 很薄：

- 按行读文件。
- 以第一个 `=` 切分。
- 跳过注释、空行和没有 `=` 的行。
- 把右端值拆成 token list。
- 遇到行内 `#` 后截断。

文件头 TODO 也已经明确写着当前缺口：

- `FILE = ...` include 支持还没合并进来。
- multiline string 还不支持。
- 这条 helper 和 `read_dims_from_file` 还没真正统一。

因此 top-level `Tools/Parser` 的真实定位只能是：

- `input-file helper script`

它不是 `Source/Utils/Parser/*`、`ParserUtils.*`、`IntervalsParser.*`、`queryWithParser/queryArrWithParser` 这些真正运行时 parser 设施的替代物。

## 2. `stencil.py` 说明 top-level Parser 的主要用途是轻量前处理

`Tools/Algorithms/stencil.py` 直接：

```python
sys.path.append("../Parser/")
from input_file_parser import parse_input_file
```

然后用这个轻量 parser 读取 WarpX 输入卡里的：

- 维度
- 网格尺寸
- `psatd_order`
- `gamma_boost`
- `v_gal`

再做两件事：

1. 复现有限阶 centered / staggered Fornberg 系数。
2. 估算 PSATD stencil 在给定误差阈值下需要的最小 guard cells。

也就是说，`Tools/Parser` 当前最稳定的消费者不是 runtime，而是：

- tools 层脚本
- notebook / estimate helper

## 3. `Tools/PostProcessing` 里最关键的是 reader-side helper

`Tools/PostProcessing` 不是统一框架，而是一组松散脚本。

### 3.1 `read_raw_data.py`

这条脚本是真正不可替代的：

- 读取 `<plotfile>/raw_fields/Level_*`
- 解析 `*_H` header
- 恢复 raw staggered `MultiFab` 的 boxes、offsets、ghost cells、component count
- 最后把 AMReX raw field block 拼回 `numpy` arrays

因此它的真实定位是：

- `plotfile raw_fields reader`

这条 reader-side contract 已经在 `diagnostics/07` 里作为 diagnostics 读者侧主线记录。

### 3.2 `plot_timestep_duration.py`

这条脚本不碰 plotfile/openPMD/checkpoint。

它只做：

- 用 regex 从 WarpX stdout/stderr log 中提取
  - `STEP ... Avg. per step = ... s`
- 生成
  - timestep duration
  - cumulative duration
  两张图

因此它的真实定位是：

- `runtime log postprocessor`

它属于性能/运行态 reader-side helper，不属于物理 diagnostics reader。

## 4. 其他 `PostProcessing` 脚本更像专题 helper

按当前项目已有覆盖：

- `plot_distribution_mapping.py`
- `plot_parallel.py`
- `plot_particle_path.py`
- `video_yt.py`
- `yt3d_mpi.py`

已经在 diagnostics 或 parallelization 笔记里接到各自最合适的消费场景：

- distribution mapping / load balance
- checkpoint particle debug
- yt 动画和 3D 读者侧工作流

因此这里不再重复把它们当成“未读源码主线”。

## 5. `Tools/Algorithms` 不是运行时 algorithm 目录

`Tools/Algorithms` 当前只有：

- `psatd.ipynb`
- `psatd_pml.ipynb`
- `stencil.py`

它们都不是 runtime solver。

### 5.1 `psatd.ipynb`

这条已经由 `fieldsolver/11` 完整覆盖。它的角色是：

- 符号推导 PSATD 系数来源

不是 runtime spectral algorithm 本身。

### 5.2 `psatd_pml.ipynb`

当前 worktree 里它是同类 notebook：

- 用于推导/核对 PML 相关 PSATD 系数
- 仍属于 derivation artifact

在项目状态上，它更适合被视为：

- `fieldsolver/11` 的邻接推导材料

而不是一条新的 Tools 主线。

### 5.3 `stencil.py`

这条不是系数推导，而是：

- 读输入卡
- 估算 guard-cell / stencil extent

所以它是：

- `algorithm utility script`

不是谱推进主算法实现。

## 6. 对 `Tools/*` 的当前收口结论

到当前 worktree 为止，`Tools/*` 最合理的源码结论是：

1. `Tools/Parser`
   - 轻量输入卡脚本
   - 为 tools/notebooks 服务
   - 不代表 runtime parser 语义
2. `Tools/PostProcessing`
   - reader-side / log-side helper 集合
   - 主要消费 diagnostics 输出或 stdout log
3. `Tools/Algorithms`
   - 推导 notebook 与估计脚本
   - 不属于 runtime field solver 实现

因此：

- `Tools/PostProcessing` 的主要 reader-side 价值已经由 diagnostics 笔记覆盖。
- `Tools/Algorithms/psatd.ipynb` 的主价值已经由 fieldsolver 笔记覆盖。
- top-level `Tools/*` 里这轮真正新补的实质缺口，主要是：
  - `input_file_parser.py`
  - `stencil.py`
  以及它们和现有主线的边界。
