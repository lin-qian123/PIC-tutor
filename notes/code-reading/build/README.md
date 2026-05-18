# Build 构建系统源码精读入口

绑定源码：`../warpx/CMakeLists.txt`、`../warpx/Source/Make.WarpX`、`../warpx/Source/*/CMakeLists.txt`、`../warpx/Source/*/Make.package`、`../warpx/Tools/machines/*`。

## 模块边界

- 顶层 `CMakeLists.txt`
  - 负责选项、依赖、维度矩阵和顶层 target 组织。
- `Source/*/CMakeLists.txt`
  - 每个源码子目录把 `.cpp` 挂到对应维度库 target。
- `Source/Make.WarpX` 与 `Source/*/Make.package`
  - GNUmake 旧构建链的模块聚合、维度宏和 feature 宏入口。
- `Tools/machines/*`
  - 面向具体机器的环境 profile、依赖安装脚本和 batch 模板。

## 核心问题

- CMake 怎样把 `WarpX_DIMS`、`WarpX_COMPUTE`、`WarpX_QED`、`WarpX_PYTHON` 这些选项变成一组真实构建目标。
- GNUmake 怎样用 `DIM/USE_RZ/USE_FFT/QED/USE_PYTHON_MAIN` 复现近似的 feature matrix。
- `Tools/machines/*` 怎样把 profile / install / submit 三件套与 `Docs/source/install/hpc*.rst` 对起来。

## 精读顺序

1. 顶层 `CMakeLists.txt`
2. `Source/*/CMakeLists.txt`
3. `Docs/source/developers/gnumake.rst`
4. `Source/Make.WarpX`
5. `Tools/machines/desktop/*`
6. 代表性 HPC machine 三件套

## 输出目标

- `00-cmake-superbuild-and-module-aggregation.md`
- `01-gnu-make-and-dimension-variants.md`
- `02-hpc-machine-profiles.md`

## 当前状态

- 已完成 `00-cmake-superbuild-and-module-aggregation.md`：把顶层 `CMakeLists.txt` 的 option/variant 矩阵、`WarpX_DIMS` 多维构建、依赖 superbuild 和 `Source/*/CMakeLists.txt -> lib_${SD}` 聚合链压实。
- 已完成 `01-gnu-make-and-dimension-variants.md`：把 `Source/Make.WarpX` 的旧构建语义、`DIM/USE_RZ/QED/USE_FFT/USE_PYTHON_MAIN` 的宏路径，以及它与 CMake `WarpX_DIMS/WarpX_COMPUTE/WarpX_QED/WarpX_PYTHON` 的对应边界压实。
- 已完成 `02-hpc-machine-profiles.md`：把 `Tools/machines` 的 `warpx.profile.example -> install_dependencies.sh -> submit.sh/.sbatch/.pbs/.flux` 三件套、desktop Spack 环境和 `Docs/source/install/hpc*.rst` 的文档链接关系压实。

## 验证线索

- `Docs/source/developers/repo_organization.rst`
- `Docs/source/developers/gnumake.rst`
- `Docs/source/developers/dimensionality.rst`
- `Docs/source/install/cmake.rst`
- `Docs/source/install/hpc.rst`
