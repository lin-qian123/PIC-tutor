# 顶层 CMake：option 矩阵、依赖 superbuild 与模块聚合

绑定源码：

- `../warpx/CMakeLists.txt`
- `../warpx/Source/FieldSolver/CMakeLists.txt`
- `../warpx/Source/Python/CMakeLists.txt`
- `../warpx/Docs/source/developers/repo_organization.rst`
- `../warpx/Docs/source/install/cmake.rst`

## 1. 顶层 `CMakeLists.txt` 不是简单“列源文件”

WarpX 的顶层 CMake 先做四件事：

1. 读 `dependencies.json` 取版本号；
2. 设置构建前置策略：
   - 禁止 in-source build
   - 推 C++20 到 superbuild 依赖
   - 处理 `ccache`、默认 build/install 目录
3. 建 option / variant 矩阵；
4. 通过依赖脚本和子目录，把真实 target 拼起来。

所以它更像：

- `configuration graph + superbuild driver`

而不是常见的小项目 `add_executable(main.cpp)`。

## 2. 第一层：feature 选项矩阵

当前 worktree 里最核心的顶层选项包括：

- `WarpX_APP`
- `WarpX_LIB`
- `WarpX_MPI`
- `WarpX_OPENPMD`
- `WarpX_FFT`
- `WarpX_PYTHON`
- `WarpX_QED`
- `WarpX_QED_TABLE_GEN`
- `WarpX_QED_TOOLS`
- `WarpX_EB`
- `WarpX_PETSC`

以及几条高阶矩阵轴：

- `WarpX_DIMS = 1;2;3;RZ;RCYLINDER;RSPHERE`
- `WarpX_PRECISION = SINGLE|DOUBLE`
- `WarpX_PARTICLE_PRECISION = SINGLE|DOUBLE`
- `WarpX_COMPUTE = NOACC|OMP|CUDA|SYCL|HIP`

这说明 WarpX 的顶层构建不是单一 binary 配置，而是：

- feature matrix

## 3. `WarpX_DIMS` 支持一次构建多个几何 target

顶层 CMake 不是只接受一个维度，而是允许：

```cmake
set(WarpX_DIMS 3 CACHE STRING ...)
list(REMOVE_DUPLICATES WarpX_DIMS)
foreach(D IN LISTS WarpX_DIMS)
    ...
endforeach()
```

而且开发者文档也明确写出可以：

```text
-DWarpX_DIMS="1;2;3;RZ;RCYLINDER;RSPHERE"
```

再把这组维度映射到 AMReX 维度：

- `RZ -> 2`
- `RCYLINDER -> 1`
- `RSPHERE -> 1`

因此 CMake 语义不是“编译一个几何”，而是：

- `build a set of dimension-specialized libraries/targets`

## 4. 第二层：依赖 superbuild

顶层 `CMakeLists.txt` 会顺序 include：

- `cmake/dependencies/AMReX.cmake`
- `PICSAR.cmake`
- `openPMD.cmake`
- `FFT.cmake`

这条链说明：

- 依赖解析是顶层做的
- 源码子目录只假设相应 target 已存在

例如：

- `WarpX_FFT=ON`
  会先打开 AnyFFT/FFTW/rocFFT/cuFFT 这条依赖图
- `WarpX_QED` / `WarpX_QED_TABLE_GEN`
  会先要求 PICSAR QED 链就位

## 5. 第三层：子目录把源码挂到按维度分裂的库 target

关键点不在顶层，而在子目录写法。

例如 `Source/FieldSolver/CMakeLists.txt`：

```cmake
foreach(D IN LISTS WarpX_DIMS)
    warpx_set_suffix_dims(SD ${D})
    target_sources(lib_${SD}
      PRIVATE
        WarpXPushFieldsEM.cpp
        WarpXPushFieldsHybridPIC.cpp
        WarpX_QED_Field_Pushers.cpp
        WarpXSolveFieldsES.cpp
    )
endforeach()
```

这说明：

- 真实核心 target 不是单个 `warpx`
- 而是一组按维度后缀分裂的 `lib_${SD}`

每个源码模块只负责把自己的 `.cpp` 挂到这些已有库 target 上。

## 6. Python 绑定是另一组按维度分裂的 target

`Source/Python/CMakeLists.txt` 进一步证明这一点：

- 所有维度都会往 `lib_${SD}` 增加 runtime callback 源；
- 只有在 `WarpX_PYTHON=ON` 时，才额外挂到：
  - `pyWarpX_${SD}`

也就是说：

1. C++ runtime 库一直按维度存在；
2. Python pybind 模块是附加在这组维度 target 之上的第二层构建产物。

## 7. `WarpX_APP` / `WarpX_LIB` / `WarpX_PYTHON` 的关系

顶层 CMake 明确强制：

```cmake
if(WarpX_APP OR WarpX_PYTHON)
    set(WarpX_LIB ON ... FORCE)
endif()
```

这条语义很关键：

- app 和 Python 都建立在库 target 之上
- `WarpX_LIB` 才是中间稳定层

所以最真实的构建分层是：

1. `lib_${SD}`
2. `WarpX executable` 和/或 `pyWarpX_${SD}`

## 8. 当前 worktree 下的构建源码图

从 `Source/` 当前目录看，几乎每个主要模块都同时有：

- `CMakeLists.txt`
- `Make.package`

例如：

- `FieldSolver/`
- `Particles/`
- `Initialization/`
- `Diagnostics/`
- `Python/`
- `Fluids/`
- `AcceleratorLattice/`
- `ablastr/`

这和开发者文档里的说法一致：

- CMake 是主构建系统
- GNUmake 是 legacy 支线
- 新增 `.cpp` 时两边都要补

## 9. 当前收口结论

到当前 worktree 为止，顶层 CMake 最应被理解成三层：

1. option / variant 矩阵
2. dependency superbuild
3. dimension-specialized target aggregation

其中真正稳定的核心不是单个 binary，而是一组：

- `lib_${SD}`
- 可选 `pyWarpX_${SD}`

子模块 `Source/*/CMakeLists.txt` 做的不是自成系统的构建，而是向这组共享 target 注入源码。
