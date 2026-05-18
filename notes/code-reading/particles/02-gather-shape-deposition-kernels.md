# 02. Field gather、shape factor 与沉积 kernel

## 1. Shape factor 基础入口

`Source/Particles/ShapeFactors.H:27-84` 定义 `Compute_shape_factor<depos_order>`。

| 行号 | 作用 |
|---|---|
| `:36-40` | 0 阶形函数：只写一个网格点，权重为 1。 |
| `:41-47` | 1 阶形函数：`sx[0]=1-xint`，`sx[1]=xint`，对应 CIC 线性权重。 |
| `:48-56` | 2 阶 B-spline 权重，返回 `j-1` 作为最左写入点。 |
| `:57-66` | 3 阶 B-spline 权重。 |
| `:67-77` | 4 阶 B-spline 权重。 |
| `:78-82` | 非法阶数 abort。 |

`ShapeFactors.H:93-156` 的 `Compute_shifted_shape_factor` 用于 Esirkepov 等需要 old/new 形函数对齐的算法；`ShapeFactors.H:158-240` 的 `Compute_shape_factor_pair` 用于 Villasenor 横向 segment 权重。

## 2. Field gather 运行时 wrapper

`Source/Particles/Gather/FieldGather.H:2119-2192` 是运行时 wrapper：

- 如果 `galerkin_interpolation` 为真，调用 `doGatherShapeN<nox,1>()`。
- 否则调用 `doGatherShapeN<nox,0>()`。
- `nox` 支持 1 到 4 阶。

因此 `PushPX()` 中传入的运行时 `nox` 会在这里转为编译期模板实例，避免在内层粒子循环里用动态分支选择 shape 阶数。

## 3. Field gather 模板主体

`Source/Particles/Gather/FieldGather.H:348-760` 是 `doGatherShapeN<depos_order, galerkin_interpolation>()` 主体。

关键事实：

- `:387-388` 构造普通 shape factor 和 Galerkin 降阶 shape factor。
- `:390-439` 在 x 方向按 node/cell centering 分别计算 `sx_node/sx_cell`，并为不同场分量选不同数组。
- `:442-520` 对 y/z 方向做同类处理。
- `:522-760` 按编译维度执行真正 gather。Cartesian XZ、RZ、RCYLINDER、RSPHERE 都有专门分支。
- RZ 分支先 gather \(E_r,E_\theta,B_r,B_\theta\)，再用粒子角度转换到 Cartesian \(E_x,E_y,B_x,B_y\)，见 `:682-686`。

## 4. Charge deposition kernel

`Source/Particles/Deposition/ChargeDeposition.H:36-172` 是 `doChargeDepositionShapeN<depos_order>()`。

关键事实：

- `:54` 计算 `invvol = dinv.x*dinv.y*dinv.z`。
- `:63-65` 对粒子并行。
- `:67-70` 计算 `wq = q*wp[ip]*invvol`，电离时再乘 `ion_lev[ip]`。
- `:72-126` 读取粒子位置并按 rho 的 node/cell centering 计算各方向 shape factor。
- `:129-169` 按维度把 `sx*sy*sz*wq` 原子加到 `rho_arr`。

这就是电荷沉积最直接的离散公式实现。

## 5. Direct current deposition

`Source/Particles/Deposition/CurrentDeposition.H:47-274` 是 direct current deposition kernel。

关键事实：

- `:74-108` 把粒子速度和电荷组合成 `wqx/wqy/wqz`；在 RZ/RCYLINDER/RSPHERE 中会转换坐标分量。
- `:117-151` 计算 x 方向 shape factor，使用 `relative_time` 把粒子位置临时移到沉积时间。
- `:154-208` 对 y/z 做同类处理。
- `:211-273` 按维度把 `sx*sy*sz*wq?` 原子加到 `jx/jy/jz`。

Direct deposition 是最直观的电流沉积：用时间中心位置和速度加权沉积电流，但它不是严格 charge-conserving 轨迹积分。

## 6. Esirkepov deposition 入口

`Source/Particles/Deposition/CurrentDeposition.H:675-1085` 是 `doEsirkepovDepositionShapeN<depos_order>()` 的前半段和各维度沉积公式。

关键事实：

- `:707-709` 定义 `invdtd`，它含 \(1/\Delta t\) 和横向面积因子，是把电荷变化转为电流的尺度。
- `:724-726` 对粒子并行。
- `:728-735` 计算相对论 `gaminv` 与加权电荷 `wq`。
- `:740-804` 从当前粒子位置和 `relative_time` 反推出 `x_new/x_old` 等网格坐标。
- `:866-935` 为 old/new 位置计算 shape factor；靠近 EB 时可降阶到 order 1。
- `:938-953` 根据 old/new 最左索引差异确定循环范围。
- `:955-1085` 用 old/new shape factor 差分构造 \(J_x,J_y,J_z\)，这是 charge-conserving 的核心。

后续正式推导要从离散连续性方程解释 `sx_old - sx_new` 为什么产生电流分量。

