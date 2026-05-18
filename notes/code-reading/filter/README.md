# Filter 源码精读入口

绑定源码：`../warpx/Source/Filter`。

## 模块边界

- 构建入口：`Filter/CMakeLists.txt`、`Filter/Make.package`。
- 主要文件：`Filter.*`、`BilinearFilter.*`、`NCIGodfreyFilter.*`。
- 关联模块：current/rho 同步、PSATD、NCI mitigation。

## 核心问题

- bilinear filter 如何定义 stencil 和多次 passes。
- Godfrey NCI filter 的表和 stencil 如何作用在场/电流上。
- filter 在时间推进中的调用顺序是什么。

## 精读顺序

1. `Filter.*` 基类和参数。
2. `BilinearFilter.*`。
3. `NCIGodfreyFilter.*` 与 `Utils/NCIGodfreyTables.H`。
4. 调用点：`SyncCurrentAndRho`、field push、PSATD。

## 输出目标

- `00-filter-dispatch.md`
- `01-bilinear-filter.md`
- `02-godfrey-nci-filter.md`

## 验证线索

- NCI stability examples。
- boosted-frame examples。
