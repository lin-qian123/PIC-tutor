# `Tools/QedTablesUtils`：QED lookup-table 的生成与回读工具

绑定源码：

- `../warpx/Tools/QedTablesUtils/CMakeLists.txt`
- `../warpx/Tools/QedTablesUtils/Source/QedTableGenerator.cpp`
- `../warpx/Tools/QedTablesUtils/Source/QedTableReader.cpp`
- `../warpx/Tools/QedTablesUtils/Source/QedTableCommons.H`
- `../warpx/Tools/QedTablesUtils/Source/ArgParser/QedTablesArgParser.cpp`
- `../warpx/Tools/QedTablesUtils/Source/ArgParser/QedTablesArgParser.H`

绑定现有项目笔记：

- `notes/code-reading/particles/14-qed-entrypoints.md`
- `notes/code-reading/particles/15-qed-kernels-and-wrapper-contracts.md`
- `notes/code-reading/particles/16-qed-table-generation-and-serialization.md`

`Tools/QedTablesUtils` 是当前 top-level `Tools/*` 里最像“独立小程序模块”的一块。它不是 notebook，也不是 reader-side 辅助脚本，而是两个真正编译出来的可执行文件：

- `qed_table_generator`
- `qed_table_reader`

## 1. 构建边界：这里只有两个小工具

`CMakeLists.txt` 很直接：

- 公共 `ArgParser` 源：
  - `QedTablesArgParser.cpp/.H`
- 可执行程序：
  - `qed_table_generator`
  - `qed_table_reader`
- 两者都链接：
  - `PXRMP_QED`

因此这里不是一个 runtime library 层，而是：

- `command-line table utility`

## 2. 命令行 parser 是本地私有的最小实现

`QedTablesArgParser.cpp` 定义的是很薄的一层：

- `ParseArgs(keys, argc, argv)`
- `PrintHelp(cmd_list)`
- `WarnMsg/ErrMsg`
- `GetArgType/ReadArg`

当前支持的值类型只有：

- `NoArg`
- `String`
- `Integer`
- `Double`

这层 parser 的真实语义应写得保守：

- 重复 key 只会 warning 然后覆盖
- 无法识别的 token 只会 warning
- parse error 直接 `exit(1)`

所以它是 QED table 工具自带的私有命令行 parser，不是通用设施。

## 3. `qed_table_generator` 的核心：BW/QS 二选一，再按 SP/DP 分派

`QedTableGenerator.cpp` 的入口参数表明确要求：

- `--table`
  - `BW` 或 `QS`
- `--mode`
  - `DP` 或 `SP`
- `-o`
  - 输出文件名

然后 `GenerateTable(args)` 做两层分派：

1. `BW` vs `QS`
2. `double` vs `float`

所以当前 generator 的主合同就是：

- `table family dispatch`
- `precision dispatch`

## 4. BW/QS 两条生成路径的真实输出结构

### 4.1 BW

`GenerateTableBW<RealType>` 要求全部参数齐全：

- `--dndt_chi_min/max/how_many`
- `--pair_chi_min/max/how_many`
- `--pair_frac_how_many`

然后构造两张 PICSAR table：

- `dndt_lookup_table`
- `pair_prod_lookup_table`

两张表都 `generate(true)`，即带进度条生成。

### 4.2 QS

`GenerateTableQS<RealType>` 则要求：

- `--dndt_chi_min/max/how_many`
- `--em_chi_min/max`
- `--em_frac_min`
- `--em_chi_how_many`
- `--em_frac_how_many`

对应两张表：

- `dndt_lookup_table`
- `photon_emission_lookup_table`

## 5. 二进制布局：前半张表大小 + 两段序列化 payload

无论 BW 还是 QS，最终文件布局都遵循同一个简单协议：

1. 先写入第一张表序列化字节数 `uint64_t`
2. 再写第一张表 payload
3. 最后把第二张表 payload 直接接上

也就是：

```text
[size_first][payload_first][payload_second]
```

其中：

- BW:
  - `payload_first = dndt`
  - `payload_second = pair_prod`
- QS:
  - `payload_first = dndt`
  - `payload_second = photon_emission`

这条文件协议正好和 `particles/16` 里 runtime 侧的 builtin/load/generate 生命周期接起来。

## 6. `qed_table_reader` 的核心：把同一协议拆回人类可读表

`QedTableReader.cpp` 用同样的参数：

- `--table`
- `--mode`
- `-i`
- `-o`

读入整个二进制文件后，先：

- 取出 `size_first`
- 用它切开第一、第二段 payload

再按 BW/QS 路径分别用 PICSAR table ctor 反序列化。

这说明 reader 的真实合同不是“参与 runtime 读表”，而是：

- `offline inspection / dump utility`

## 7. 输出的人类可读格式

reader 不只是打印 metadata，而是把插值表导成可绘图文本。

### 7.1 BW

- 输出 `<outfile>_dndt`
  - 遍历全部 coordinate，写 `coord interp(coord)`
- 输出 `<outfile>_pair`
  - 用 wrapper 访问受保护底层表
  - 写出
    - `exp(xcoord)`
    - `ycoord * exp(xcoord)`
    - `val`

### 7.2 QS

- 输出 `<outfile>_dndt`
- 输出 `<outfile>_phot_em`
  - wrapper 访问表
  - 写出
    - `exp(xcoord)`
    - `exp(ycoord) * exp(xcoord)`
    - `exp(val)`

这些 `exp(...)` 说明底层表内部坐标/值并不总是按物理量原样存储，reader 在这里承担了“还原成可读物理坐标”的责任。

## 8. 与现有 QED 主线的关系

到当前 worktree 为止，这块最重要的边界是：

1. `particles/14-17`
   - 负责 runtime QED 主链
   - `InitQED()`、wrapper、event path、table 生命周期
2. `Tools/QedTablesUtils`
   - 负责离线表文件的生成与人工检查

因此它不是新的物理 event 主线，而是：

- `QED table artifact toolchain`

## 9. 当前收口结论

`Tools/QedTablesUtils` 这一块现在已经可以压成以下三句话：

1. 生成器做的是：
   - `BW/QS` 二选一
   - `SP/DP` 二选一
   - 两张 PICSAR table 的二进制序列化拼接
2. 读取器做的是：
   - 按相同协议切开 payload
   - 反序列化
   - 导出可读文本表
3. 它和 runtime 的关系是：
   - 为 QED lookup table 文件提供离线生成/审查工具链
   - 不参与 WarpX 主循环内的粒子事件推进
