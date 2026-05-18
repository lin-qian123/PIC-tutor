# `WarpXSolverDOF` 编号契约与 `MatrixPC::Assemble()` 的几何行写入模式

绑定源码：

- `../warpx/Source/FieldSolver/ImplicitSolvers/WarpXSolverDOF.H`
- `../warpx/Source/FieldSolver/ImplicitSolvers/WarpXSolverDOF.cpp`
- `../warpx/Source/FieldSolver/ImplicitSolvers/WarpXSolverVec.H`
- `../warpx/Source/FieldSolver/ImplicitSolvers/WarpXSolverVec.cpp`
- `../warpx/Source/NonlinearSolvers/MatrixPC.H`

前一篇 `04-petsc-matrixpc-assembly-chain.md` 已经说明，`pc_petsc` 真正显式装配的不是整个 Jacobian，而是 preconditioner 近似

$$
P \approx I + \nabla\times(\alpha\nabla\times \cdot) + M_{\rm PC}.
$$

但那一篇还停留在“谁调用谁”。这一篇继续下钻两层：

1. `WarpXSolverDOF` 怎样把 staggered `Efield_fp` 变成 local/global 自由度编号；
2. `MatrixPC::Assemble()` 在 1D、XZ/RZ、3D、RCYLINDER 下，怎样把 curl-curl 和 mixed-derivative 写成一行稀疏条目。

## 1. `WarpXSolverVec` 的数值容器和 `WarpXSolverDOF` 的编号容器是分开的

`WarpXSolverVec::Define()` 为解向量本身分配的是普通 `MultiFab`：

```cpp
m_array_vec[lev][n] = new amrex::MultiFab( this_array[n]->boxArray(),
                                           this_array[n]->DistributionMap(),
                                           this_array[n]->nComp(),
                                           amrex::IntVect::TheZeroVector() );
```

而编号对象 `m_dofs` 是一个静态共享的 `WarpXSolverDOF`：

```cpp
if (m_dofs == nullptr) {
    m_dofs = std::make_unique<WarpXSolverDOF>();
    m_dofs->Define(m_WarpX, m_num_amr_levels, m_vector_type_name, m_scalar_type_name);
}
```

这意味着：

- `WarpXSolverVec` 持有真实 `E/B/\phi` 数值；
- `WarpXSolverDOF` 持有“这些数值在线性代数向量里对应哪一号未知量”的映射；
- 多个 implicit solve 向量可以共享同一套 DOF 编号规则。

## 2. `WarpXSolverDOF::Define()` 给每个原始分量分配一对 `{local, global}` 编号槽

对 vector field，`WarpXSolverDOF::Define()` 不是复制场值，而是分配 `iMultiFab`：

```cpp
m_array[lev][n] = std::make_unique<amrex::iMultiFab>(this_array[n]->boxArray(),
                                                     this_array[n]->DistributionMap(),
                                                     2*ncomp,
                                                     this_array[n]->nGrowVect() );
```

这里 `2*ncomp` 的含义非常直接：

- 偶数分量 `2*v` 存 local DOF id；
- 奇数分量 `2*v+1` 存 global DOF id。

scalar path 也一样：

```cpp
m_scalar[lev] = std::make_unique<amrex::iMultiFab>(..., 2*ncomp, ...);
```

所以 `WarpXSolverDOF` 不是“每个网格点一个编号”，而是“每个有效网格点的每个物理分量，都有一对 local/global 编号槽”。

## 3. 编号不是对全部网格点生效，而是先被 dot-mask 裁掉

定义完 `iMultiFab` 之后，`WarpXSolverDOF::Define()` 立刻取对应 field 的 dot-mask：

```cpp
const auto* mask = a_WarpX->getFieldDotMaskPointer(m_array_type, lev, ablastr::fields::Direction{n});
fill_local_dof(*m_array[lev][n], *mask);
```

这一步很关键。它说明 DOF 编号只给 mask 允许的点分配，其他位置保持 invalid。

在 `fill_local_dof()` 里，初始化是：

```cpp
dof.setVal(std::numeric_limits<int>::lowest());
```

而真正分配编号时，只对 `m(i,j,k)` 为真的点写入：

```cpp
if (m(i,j,k)) {
    d(i,j,k,0) = ps + start_id;
}
```

因此后面只要看到

```cpp
const int ridx_l = dof_arr(i,j,k,0);
if (ridx_l < 0) { return; }
```

就知道这不是边角修补，而是“该 staggered 点根本不是当前线性系统里的未知量”。

## 4. local 编号是 tile 内 prefix-sum，但全局累加以 `MFIter` 顺序推进

`fill_local_dof()` 的 local 编号核心是：

```cpp
auto ndofs = Scan::PrefixSum<int>(
    npts,
    [=] AMREX_GPU_DEVICE (int offset) -> int
    {
        auto [i,j,k] = boxindex(offset);
        return m(i,j,k) ? 1 : 0;
    },
    [=] AMREX_GPU_DEVICE (int offset, int ps)
    {
        auto [i,j,k] = boxindex(offset);
        if (m(i,j,k)) {
            d(i,j,k,0) = ps + start_id;
        }
    },
    Scan::Type::exclusive, Scan::retSum);
```

这里的语义是：

- 单个 valid box 内，用 prefix sum 只给 mask 有效点编号；
- `start_id` 是当前 box 开始前已经累计的 local DOF 数；
- box 完成后再用
  `m_nDoFs_l += Long(ndofs)*ncomp;`
  把本 box、所有物理分量的 DOF 总数加进去。

因此 local 编号顺序由两层构成：

- box 内：按 `BoxIndexer` 展平顺序；
- box 间：按当前 `MFIter` 遍历顺序串接。

## 5. 多分量场不是“重新扫一遍 mask”，而是按第一分量平移整块编号

若 `ncomp > 1`，后续分量不重新 prefix-sum，而是直接在第一分量的局部编号上平移：

```cpp
d(i,j,k,2*(n+1)) = d(i,j,k,0) + ndofs*(n+1);
```

这说明同一 `MultiFab` 上多个物理分量共享同一批有效点，但在扁平线性向量里分成相邻分量块。换句话说：

- 先编号第 0 个物理分量的所有有效点；
- 第 1 个物理分量整体偏移 `ndofs`；
- 第 2 个物理分量整体再偏移 `ndofs`。

这也是为什么 `MatrixPC::Assemble()` 可以安全地把“同一空间位置、不同方向分量”的耦合写成跨分量列索引。

## 6. global 编号只是 local 编号加上 MPI rank 偏移

`fill_global_dof()` 没有重新做几何分析，而是：

1. `MPI_Allgather` 收集各 rank 的 `m_nDoFs_l`；
2. 计算当前 rank 之前的累计 `proc_begin`；
3. 对所有 valid local id 执行

```cpp
dof[b](i,j,k,2*n+1) = dof[b](i,j,k,2*n) + int(proc_begin);
```

因此 global 编号契约很简单：

$$
\text{global id} = \text{local id} + \text{rank prefix}.
$$

它不是图划分意义上的重编号，而是“每个 rank 保持本地顺序，再按 rank 拼接”。

## 7. `FillBoundaryAndSync()` 只同步 global id，不同步 local id

`Define()` 末尾只对奇数分量调用：

```cpp
for (int comp = 1; comp < dof->nComp(); comp += 2) {
    dof->FillBoundaryAndSync(comp, 1, dof->nGrowVect(), a_WarpX->Geom(lev).periodicity());
}
```

这一步也很关键。local id 只在本 rank 内有意义，不需要跨 patch 一致；global id 需要在 guard / periodic / overlap 处保持一致，否则同一个物理列会被不同 patch 写成不同编号。

所以 `WarpXSolverDOF` 的最终契约是：

- local id: 只服务本地线性代数缓存；
- global id: 服务跨 patch、跨 rank 的稀疏矩阵列索引。

## 8. `copyFrom()` / `copyTo()` 证明 DOF 对象就是 `WarpXSolverVec <-> PETSc Vec` 的唯一桥

`WarpXSolverVec::copyFrom()` 的核心是：

```cpp
const int dof = dof_arr(i,j,k,2*v); // local
if (dof >= 0) {
    data_arr(i,j,k,v) = a_arr[dof];
}
```

`copyTo()` 则反过来：

```cpp
const int dof = dof_arr(i,j,k,2*v); // local
if (dof >= 0) {
    a_arr[dof] = data_arr(i,j,k,v);
}
```

这说明对 WarpX 来说，线性向量从来不是独立对象；它始终是“由 `WarpXSolverDOF` 把 staggered `MultiFab` 展平后的视图”。

因此 `MatrixPC::Assemble()` 的所有 row/column 含义，最终都必须回到这套 DOF 编号规则上解释。

## 9. `MatrixPC::Assemble()` 的每一行都从同一个模板开始：先写 `I`

进入 `MatrixPC::Assemble()` 后，第一步不是 curl-curl，也不是 mass matrix，而是给每个有效 DOF 行写单位对角：

```cpp
const int ridx_l = dof_arr(i,j,k,0);
const int ridx_g = dof_arr(i,j,k,1);
...
r_indices_g_ptr[ridx_l] = ridx_g;
...
const int cidx_g_lhs = dof_arr(i,j,k,1);
const amrex::Real val = 1.0_rt;
```

也就是说，每一行的最低结构都是：

$$
P_{ii} \leftarrow 1.
$$

然后才在这一行上继续叠加 curl-curl 和 `M_{\rm PC}`。

## 10. `insertOrAdd()` 决定了装配语义是“汇总到同一行”，不是“逐模板覆盖”

所有条目都通过

```cpp
MatrixPCUtils::insertOrAdd(...)
```

写入。它先查当前列号是否已存在：

- 存在则把值相加；
- 不存在则新开一列。

所以 `MatrixPC::Assemble()` 的本质不是“固定 stencil 输出”，而是“同一物理行的多来源局域耦合汇总”。这尤其重要，因为：

- 单位阵贡献和 curl-curl 对角项会落到同一对角列；
- mixed derivative 与 mass matrix 也可能打到已经存在的列上。

## 11. 1D `Z` 几何下只有横向电场参与 curl-curl

`WARPX_DIM_1D_Z` 分支写得非常直接：

```cpp
if (dir != 2) {
    // diagonal
    val =  2.0_rt*alpha * dxi[0]*dxi[0] * BC_mask_Edir_arr(i,j,k,0);
    // left/right
    val = -alpha * dxi[0]*dxi[0] * BC_mask_Edir_arr(i,j,k,1);
}
```

源码旁注也明确：

- `dir = 0`: `xhat·[curl curl E] = -d2Ex/dx2`
- `dir = 1`: `yhat·[curl curl E] = -d2Ey/dx2`
- `dir = 2`: `zhat·[curl curl E] = 0`

因此 1D 情况下：

- `Ex`、`Ey` 各自只形成三点二阶差分；
- `Ez` 行只有单位阵和后续 mass matrix，不带 curl-curl stencil。

## 12. RCYLINDER 下没有 mixed derivative，差异主要是径向几何因子

`WARPX_DIM_RCYLINDER` 分支只处理 `dir != 0`：

- `Er` 行没有 curl-curl；
- `Etheta`、`Ez` 行分别有径向二阶项。

对角系数例如：

```cpp
if (dir == 1) {
    geom_factor = i_real / (i_real - 0.5_rt) + i_real / (i_real + 0.5_rt);
}
else if (dir == 2) {
    geom_factor = 2.0_rt;
}
```

左右邻居则带

```cpp
1.0_rt +- 0.5_rt / i_real
```

这样的半径修正。也就是说，RCYLINDER 的矩阵结构仍是“对角 + 左右邻点”，但每一项都乘上来自

$$
\frac{1}{r}\frac{\partial}{\partial r}\left(r \frac{\partial}{\partial r}\right)
$$

的离散几何因子。

## 13. XZ / RZ 的关键区别是：`dir=0,2` 会跨分量写四个 mixed-derivative 角点

XZ / RZ 分支先选一个横向分量：

```cpp
if  (dir == 0) { tdir = 2; }
else if (dir == 2) { tdir = 0; }
else { tdir = 1; }
```

对 `dir=0` 或 `dir=2`，先写本分量的二阶差分三点模板，再额外写四个 mixed-derivative 条目：

```cpp
const int cidx_g_rhs = ... dof_tdir_arr(...,1);
const amrex::Real val = +- geom_* alpha * dxi[0] * dxi[1] * BC_mask_Edir_arr(i,j,k,2);
```

这四个点就是二维交叉导数

$$
\partial_x \partial_z
$$

离散后的四角模板。

因此在 XZ / RZ 下：

- `Er/Ex` 与 `Ez` 不是块对角耦合；
- 两者会通过四个 corner-like 列条目相互耦合。

## 14. RZ 不是换个名字而已，`Ez` 和 `Etheta` 还额外带 `1/r` 修正

RZ 分支在 XZ 的基础上继续乘几何因子。例如 `dir==2` 的左右二阶项用：

```cpp
const amrex::Real geom_factor = (dir == 2 && i != 0 ? 1.0_rt +- 0.5_rt / i_real : 1.0_rt);
```

mixed derivative 也有对应的

```cpp
geom_m, geom_p
```

修正。`dir==1` 的 `Etheta` 行则把径向和轴向二阶项直接相加：

```cpp
val = geom_factor * alpha * dxi[0]*dxi[0] * ...
    +      2.0_rt * alpha * dxi[1]*dxi[1] * ...
```

因此 RZ 的真实结构不是“二维 Cartesian 模板套上圆柱坐标解释”，而是：

- `Er/Ez` 保留交叉耦合；
- `Etheta` 单独带圆柱径向拉伸；
- `1/r` 因子已经进入具体矩阵条目。

## 15. 3D 分支把每一行拆成“本分量二阶项 + 两组横向 mixed-derivative”

3D 先定义：

```cpp
const int tdir1 = (dir + 1) % 3;
const int tdir2 = (dir + 2) % 3;
```

然后对本分量行：

1. 先写对角项：

```cpp
val = 2.0_rt * alpha * (
    dxi[dvec[1]]*dxi[dvec[1]] * ...
  + dxi[dvec[2]]*dxi[dvec[2]] * ... );
```

2. 再写两个横向方向上的左右邻居：

```cpp
for (int ctr = -1; ctr <= 1; ctr += 2) {
    for (int tdir = 1; tdir <= 2; tdir++) {
        ...
        val = -alpha * dxi[dvec[tdir]]*dxi[dvec[tdir]] * ...
    }
}
```

3. 最后写 mixed derivative：

```cpp
for (int ctr_dir = -1; ctr_dir <= 0; ctr_dir++) {
    for (int ctr_tdir = -1; ctr_tdir <= 0; ctr_tdir++) {
        for (int tdir = 1; tdir <= 2; tdir++) {
            ...
            const auto sign = std::copysign(1,ctr_dir) * std::copysign(1,ctr_tdir);
            val = sign * alpha * dxi[dvec[0]]*dxi[dvec[tdir]] * ...
        }
    }
}
```

这表示每个分量行会同时耦合到另外两个分量的若干角点列。可以把它理解成：

- 本分量负责离散 `-\partial_{t1}^2 - \partial_{t2}^2`；
- 横向分量列负责离散 `\partial_dir \partial_{t1}` 和 `\partial_dir \partial_{t2}`。

## 16. `BC_mask_Edir_arr` 不是装饰项，而是逐条 stencil 的边界裁剪开关

无论 1D、XZ/RZ、3D 还是 RCYLINDER，每个模板值都乘了某个 `BC_mask_Edir_arr(i,j,k,comp)`。这意味着 `MatrixPC` 不是先装“满 stencil”再单独处理边界，而是边装边裁剪：

- 某个方向允许该邻接时，对应 mask 为 1；
- 某个方向被 PEC/边界裁掉时，对应条目直接乘成 0。

所以从矩阵角度看，WarpX 的 curl-curl 边界条件已经嵌进每一行条目生成逻辑里。

## 17. `MassMatrices_PC` 是在 curl-curl 之后，按同分量局域 stencil 追加的

mass matrix 部分取的是：

```cpp
auto sigma_ii_arr = (*m_bcoefs)[lev][dir]->const_array(mfi);
```

然后按 `GetMassMatricesPCnComp(dir,space_dir)` 给出的窗口宽度遍历 `iv_shift`：

```cpp
const int cidx_g_rhs = dof_arr(iv_base + iv_shift,1);
const amrex::Real val = sigma_ii_arr(iv_base,mm_comp);
```

这里列索引仍然来自同一个 `dof_arr`，不是跨到其他方向分量。也就是说当前 `MatrixPC` 只把 `sigma_ii` 这类“同分量局域耦合”直接写入 `P`；它不是在这里显式组装全三乘三块张量耦合。

## 18. 现在可以把 DOF 编号与矩阵装配合成一句话

对 `pc_petsc` 路径，WarpX 实际做的是：

1. 用 `WarpXSolverDOF` 只给 dot-mask 允许的 staggered `Efield_fp` 点编号；
2. 让每个有效点的每个物理分量拥有 `{local, global}` 两套编号；
3. 在 `MatrixPC::Assemble()` 中，用 local id 选“这一行写到哪”，用 global id 选“这一列对应哪个物理未知量”；
4. 把 `I`、curl-curl stencil、边界裁剪和 `MassMatrices_PC` 统统累加到这一行。

因此 `MatrixPC` 不是抽象算子，而是“建立在 staggered `Efield_fp` 编号之上的显式局域稀疏行生成器”。

## 19. 下一层最自然的继续方向

- `GetCurl2BCmask()` 的具体 mask 生成规则，还可以继续追到边界模块。
- `MassMatrices_PC` 的 `GetMassMatricesPCnComp()` 和 `sigma_ii` 具体窗口宽度，还可以继续追回 implicit solver 的 deposition / synchronization 逻辑。
- 如果后面要解释 PETSc 行列分布性能问题，则还需要继续看 `assemblePCMatrix()` 到 `MatSetValues()` 的 host/device 拷贝和 row ownership。
