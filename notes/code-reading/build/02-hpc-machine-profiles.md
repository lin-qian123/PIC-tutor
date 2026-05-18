# `Tools/machines/*`：HPC profile、依赖安装与 batch 模板

绑定源码与文档：

- `../warpx/Tools/machines/desktop/spack-macos-openmp.yaml`
- `../warpx/Tools/machines/frontier-olcf/frontier_warpx.profile.example`
- `../warpx/Tools/machines/frontier-olcf/install_dependencies.sh`
- `../warpx/Tools/machines/frontier-olcf/submit.sh`
- `../warpx/Docs/source/install/hpc.rst`
- `../warpx/Docs/source/install/hpc/frontier.rst`
- `../warpx/Docs/source/install/cmake.rst`

## 1. `Tools/machines/*` 不是“随手脚本”，而是 HPC quick-start 的源码侧承载

`Docs/source/install/hpc.rst` 当前明确把 HPC 安装文档组织成：

1. `warpx.profile`
2. machine-specific guides
3. batch system cheat sheets

而每台机器文档又大量 `literalinclude`：

- `Tools/machines/<machine>/<profile>`
- `install_dependencies.sh`
- `submit.sh/.sbatch/.pbs/.flux`

因此 `Tools/machines/*` 的真实定位是：

- `documentation-backed machine recipes`

## 2. 三件套：profile / install / submit

从当前 `frontier-olcf` 代表样本看，机器脚本不是一堆互不相关文件，而是稳定三件套：

### 2.1 `warpx.profile.example`

职责是：

- `module load ...`
- 设置编译器和 MPI/ROCm/CUDA 环境
- 补 `CMAKE_PREFIX_PATH`
- 配 Python venv
- 定义交互式 node alias

也就是：

- `interactive environment contract`

### 2.2 `install_dependencies.sh`

职责是：

- 检查 profile 已被正确 source
- 安装或更新额外依赖
- 创建 machine-local software prefix
- 建 Python venv / pip stack

也就是：

- `machine-local dependency provisioning`

### 2.3 `submit.sh` / `.sbatch` / `.pbs` / `.flux`

职责是：

- 编码 scheduler 语法
- 指定 node/task/GPU 资源
- 设置运行期环境 workaround
- 给出 `srun`/`mpirun` 模板

也就是：

- `batch execution template`

## 3. Frontier 样本的真实工程语义

`frontier_warpx.profile.example` 当前做的不是“推荐设置”，而是带强约束的系统匹配：

- 固定 `cmake`、ROCm、Cray MPICH、CCE 版本
- 修 `LD_LIBRARY_PATH`
- 为 RZ+PSATD 额外挂 `blaspp/lapackpp`
- 为 QED table generation load `boost`
- 为 openPMD load `adios2/hdf5`
- 最后把 `CC/CXX/FC/CFLAGS/CXXFLAGS/LDFLAGS` 指向 HIP/Cray toolchain

说明这里的 profile 已经承担了：

- build prerequisite normalization

`install_dependencies.sh` 则进一步证明机器脚本不是只装 Python：

- 先删旧 prefix
- 编译安装 BLAS++ / LAPACK++
- 再建 venv
- 再装 CuPy-ROCm、mpi4py、openpmd-api、yt、requirements.txt

`submit.sh` 的真实价值则是把：

- `FI_MR_CACHE_MONITOR`
- `MPICH_SMP_SINGLE_COPY_MODE`
- `FI_CXI_RX_MATCH_MODE`
- `ROCFFT_RTC_CACHE_PATH`

这些 machine-specific runtime workaround 固化成模板，而不是让用户每次手抄。

## 4. desktop 目录说明 `Tools/machines/*` 不只针对超算

`Tools/machines/desktop/spack-macos-openmp.yaml` 显示这一层并不局限于 batch supercomputer。

它其实也承载：

- desktop development environment recipes

这个文件直接定义：

- specs
- providers
- compiler entries
- mirrors
- concretizer policy

所以 desktop 子目录在工具层里更像：

- `package-manager environment recipe`

而不是 scheduler 模板。

## 5. 与 `install/cmake.rst` 的关系

`install/cmake.rst` 给的是通用 build 路线：

- 依赖安装
- `cmake -S . -B build ...`
- package manager 选择

`Tools/machines/*` 则是把这条通用路线具体化到特定系统：

- 哪个 module 版本
- 哪个 compiler
- 哪个 MPI
- 哪个 GPU backend
- 哪个 batch syntax

也就是说：

- `install/cmake.rst` 是 generic workflow
- `Tools/machines/* + install/hpc/*.rst` 是 machine-specialized instantiation

## 6. 与维度变体/feature matrix 的关系

HPC 文档中的 machine 示例普遍直接使用：

- `-DWarpX_COMPUTE=CUDA|HIP|SYCL|OMP`
- `-DWarpX_FFT=ON`
- `-DWarpX_QED_TABLE_GEN=ON`
- `-DWarpX_DIMS="1;2;RZ;3"`
- 可选 `-DWarpX_APP=OFF -DWarpX_PYTHON=ON`

因此 machines 层不只是“如何登录和提交作业”，它还是：

- feature matrix 的落地模板

## 7. 当前收口结论

到当前 worktree 为止，`Tools/machines/*` 最准确的工程定位是：

1. 文档侧 quick-start recipes 的源码承载；
2. 三件套：
   - environment profile
   - dependency installer
   - batch template
3. desktop 子目录则承担 package-manager 环境模板。

所以这块不该被写成“零散 HPC 脚本收藏夹”，而应被视为：

- WarpX build/deploy workflow 的 machine-specialized layer
