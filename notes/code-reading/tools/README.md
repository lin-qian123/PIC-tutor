# Tools 工具层源码精读入口

绑定源码：`../warpx/Tools`。

## 模块边界

- `Tools/Parser/`
  - top-level Python helper，不是 `Source/Utils/Parser/*` 的运行时实现。
- `Tools/PostProcessing/`
  - 读者侧后处理脚本集合，服务 `plotfile/openPMD/checkpoint/log`。
- `Tools/Algorithms/`
  - 推导/估计脚本与 notebook，不是运行时代码。
- `Tools/QedTablesUtils/`
  - 独立小工具，可生成/读取 PICSAR QED lookup tables。

## 核心问题

- top-level `Tools/*` 和 `Source/*` 正式运行时代码的边界是什么。
- 哪些工具只是 reader-side / derivation helper，哪些工具会生成运行时真正消费的文件。
- `QedTablesUtils` 怎样把命令行参数变成二进制表，再把表回读成人类可读格式。

## 精读顺序

1. `Tools/Parser/input_file_parser.py`
2. `Tools/PostProcessing/read_raw_data.py`
3. `Tools/PostProcessing/plot_timestep_duration.py`
4. `Tools/Algorithms/stencil.py`
5. `Tools/QedTablesUtils/*`

## 输出目标

- `00-parser-postprocessing-algorithms-boundary.md`
- `01-qed-tables-utils.md`

## 当前状态

- 已完成 `00-parser-postprocessing-algorithms-boundary.md`：明确 top-level `Tools/Parser` 只是轻量输入文件脚本，`PostProcessing` 里真正关键的是 `read_raw_data.py`、`plot_timestep_duration.py` 这类 reader-side helper，而 `psatd.ipynb` 已由 `fieldsolver/11` 覆盖，`stencil.py` 则是基于 Parser helper 的 guard-cell 估计脚本。
- 已完成 `01-qed-tables-utils.md`：明确 `qed_table_generator` / `qed_table_reader` 的命令行参数、BW/QS 分派、二进制布局和可读导出路径，并把它接回现有 QED runtime/table 生命周期主线。

## 验证线索

- `notes/code-reading/diagnostics/07-output-layouts-and-reading-tools.md`
- `notes/code-reading/fieldsolver/11-psatd-coefficient-derivation.md`
- `notes/code-reading/particles/16-qed-table-generation-and-serialization.md`
