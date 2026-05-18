# GNUmake 与维度变体：旧构建链的真实语义

绑定源码：

- `../warpx/Source/Make.WarpX`
- `../warpx/Source/Make.package`
- `../warpx/Docs/source/developers/gnumake.rst`
- `../warpx/Docs/source/developers/dimensionality.rst`

## 1. GNUmake 仍是支持链，但已经被文档降格

开发者文档当前写得很明确：

- CMake 是 primary build system
- GNUmake 是 legacy
- 不建议新用户再以它为主

所以这里最重要的不是“它还能不能用”，而是：

- 它怎样表达与 CMake 近似的 feature matrix

## 2. `Source/Make.WarpX` 是旧构建链的主汇总点

这个文件当前承担四层职责：

1. 默认第三方依赖路径：
   - `AMREX_HOME`
   - `PICSAR_HOME`
   - `OPENBC_HOME`
2. 旧式 feature flags：
   - `USE_MPI`
   - `USE_GPU`
   - `USE_FFT`
   - `QED`
   - `USE_OPENPMD`
   - `USE_PYTHON_MAIN`
3. 维度宏和 suffix
4. 聚合 `Source/*/Make.package`

因此它不是简单的“编译参数文件”，而是：

- `legacy build aggregator`

## 3. CMake 的 `WarpX_DIMS` 在 GNUmake 里被拆成宏组合

GNUmake 不直接用 `WarpX_DIMS="1;2;3;RZ"` 这种多值缓存变量。

它走的是：

- `DIM = 1|2|3`
- `USE_RZ = TRUE|FALSE`

并进一步映射到编译宏：

- `DIM=3 -> -DWARPX_DIM_3D -DWARPX_ZINDEX=2`
- `DIM=2 && USE_RZ=FALSE -> -DWARPX_DIM_XZ -DWARPX_ZINDEX=1`
- `DIM=2 && USE_RZ=TRUE -> -DWARPX_DIM_RZ -DWARPX_ZINDEX=1`
- `DIM=1 -> -DWARPX_DIM_1D_Z -DWARPX_ZINDEX=0`

这和 CMake 的语义差别很大：

- CMake 可以一次构建多个维度 target
- GNUmake 每次只编译一个维度变体

## 4. feature 变体通过宏和 `USERSuffix` 叠加

`Source/Make.WarpX` 会用 feature 开关同时做两件事：

1. 加 `DEFINES`
2. 在 `USERSuffix` 上追加标签

例如：

- `USE_EB -> .EB`
- `QED -> .QED`
- `QED_TABLE_GEN -> .GENTABLES`
- `PRECISION=FLOAT -> .SP`
- `USE_SINGLE_PRECISION_PARTICLES -> .pSP`
- `USE_OPENPMD -> .OPMD`
- `USE_FFT -> .PSATD`
- `USE_RZ -> .rz`

所以 GNUmake 的产物命名本身就是一条 feature 编码链。

## 5. Python main 在 GNUmake 里不是单独 pybind 目标，而是切换 shared lib 模式

旧构建链的关键开关是：

- `USE_PYTHON_MAIN`

语义不是“额外编译一个 Python target”，而是：

- 不再把 `main.cpp` 加进 `CEXE_sources`
- 打开 `-fPIC`
- 改成生成：
  - `libwarpx.$(PYDIM).a`
  - `libwarpx.$(PYDIM).so`

并通过：

- `installwarpx`

把动态库拷贝到 `Python/pywarpx` 再走 `setup.py install`。

因此 GNUmake 下的 Python 支持是：

- `library-first + setup.py install`

这和 CMake 的：

- `lib_${SD}` + `pyWarpX_${SD}`

是近似等价但不完全同构的两套表达。

## 6. `Make.package` 的职责与子目录 `CMakeLists.txt` 对应

旧文档和当前 worktree 都说明：

- 每个 `Source/*` 子目录有自己的 `Make.package`
- 根 `Source/Make.WarpX` 逐个 include 它们

例如当前顺序就是：

- `Source/Make.package`
- `Source/ablastr/Make.package`
- `Source/AcceleratorLattice/Make.package`
- `Source/BoundaryConditions/Make.package`
- ...
- `Source/Python/Make.package`
- `Source/Utils/Make.package`
- `Source/Evolve/Make.package`

这正对应 CMake 里每个子目录的：

- `add_subdirectory(...)`
- `target_sources(lib_${SD} PRIVATE ...)`

## 7. 旧构建链的边界比 CMake 更硬

当前开发者文档已经直接提醒：

- GNUmake 不容易扩展到 WarpX 全 feature set

从源码层看，这个判断是合理的：

1. 维度一次只能编一个变体；
2. Python 走的是 shared-lib + `setup.py` 特殊路径；
3. feature matrix 主要靠宏和 suffix，组合爆炸风险更高；
4. 依赖发现更偏环境变量和 pkg-config。

因此它更适合：

- experienced developer fast path

而不是今天的主工程接口。

## 8. 当前收口结论

到当前 worktree 为止，GNUmake 最准确的定位是：

1. `Source/Make.WarpX`
   - legacy build aggregator
2. `DIM/USE_RZ`
   - 单变体几何编译入口
3. `USERSuffix`
   - feature matrix 编码到产物名
4. `USE_PYTHON_MAIN`
   - shared library / pywarpx 安装路径

所以它不是 CMake 的语法替身，而是：

- 一套更线性的、宏驱动的旧构建表达方式

## 9. 与书稿现有维度说明的关系

第 3A 章和 root/fieldsolver 笔记已经多次用到：

- `WARPX_DIM_*`
- `WARPX_ZINDEX`

这轮构建笔记把这些宏的工程来源补清了：

- 它们不是任意散落在源码里的实现细节
- 而是 GNUmake 和 CMake 都会在构建期决定的几何变体 contract
