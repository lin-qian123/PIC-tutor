# ablastr 支撑层源码精读入口

绑定源码：`../warpx/Source/ablastr`。

## 模块边界

- 构建入口：`ablastr/CMakeLists.txt`、`ablastr/Make.package`。
- 子模块：`fields/`、`coarsen/`、`math/`、`parallelization/`、`particles/`、`utils/`、`warn_manager/`。

## 核心问题

- `MultiFabRegister` 如何成为 WarpX field registry 的底层。
- ablastr Poisson solvers、coarsen、FFT、communication 如何服务 field solver 和 AMR。
- warning/logging/timer/signal handling 如何影响运行时诊断。

## 精读顺序

1. `fields/MultiFabRegister.*`。
2. `fields/*PoissonSolver*`。
3. `coarsen/*`。
4. `math/fft/*`。
5. `particles/*`。
6. `utils/Communication.*`。
7. `warn_manager/*`、`utils/msg_logger/*`。

## 输出目标

- `00-multifab-register.md`
- `01-poisson-and-coarsen.md`
- `02-communication-logging-runtime.md`

## 验证线索

- field registry 使用点：`WarpX.H`、`Fields.H`、field solvers、diagnostics。
