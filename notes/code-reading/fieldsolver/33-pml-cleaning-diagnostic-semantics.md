# 3D PSATD-PML cleaning 诊断语义审计

## 结论

当前 `test_3d_pml_psatd_dive_divb_cleaning` 的项目级 clean/control 对照可以证明：

- `divE`、`divB`、`rho`、E/B native diagnostics 都能有限地写出；
- 同一 2-rank 分解下，clean case 的 core normalized Gauss residual 为 `0.764365`，control 为 `1.274899`，`divE` 指标改善；
- 但 cell-centered native `divB` 的 clean/control 比值为 `12.8282`，没有显示改善，因此不能形成正向 cleaning physics gate。

这条结论不能简单写成“cleaning 失败”，因为输出诊断中的 `divE` 与 `divB` 并不是同一种离散语义，也不等同于 PML spectral state 中的 `F/G` 残差。

## 源码链

在当前 WarpX checkout `8c488b1a9` 中，`WarpX::ComputeDivE()` 对 PSATD 分支调用 `spectral_solver_fp[lev]->ComputeSpectralDivE(...)`，源码位置为 `../warpx/Source/WarpX.cpp:3327-3341`。这意味着 plotfile 中的 `divE` 由谱空间 Maxwell 状态回变换得到，而不是简单对 plotfile 的 cell-centered E 做有限差分。

相对地，`DivBFunctor::operator()` 先创建覆盖整个 level 的 cell-centered `divB` MultiFab，再调用 `WarpX::ComputeDivB(...)`，见 `../warpx/Source/Diagnostics/ComputeDiagFunctors/DivBFunctor.cpp:24-33`。`WarpX::ComputeDivB()` 最终进入 `warpx_computedivb(...)`，并根据 `grid_type` 选择 collocated/staggered 差分分支，见 `../warpx/Source/WarpX.cpp:3296-3323`。

诊断输出层还对 `divE` 做了位置和 coarsening 处理：Cartesian staggered/nodal 情况下，`DivEFunctor` 先在 node-centered box 上生成临时 MultiFab，再 coarsen/interpolate 到输出 MultiFab，见 `../warpx/Source/Diagnostics/ComputeDiagFunctors/DivEFunctor.cpp:38-51` 和 `:71-75`。因此 clean/control report 中的 `divE`/`divB` 比值是“不同离散算子经 diagnostics consumer 后的 reader-side 对照”，不是同一谱残差的两个实现。

PML cleaning 的真正 runtime state 还包括 `Fields.H` 中的 `F_fp/G_fp` 以及 AMR coarse-patch 的 `F_cp/G_cp`；这些量分别用于 divE/divB cleaning。当前官方输入只写出 `Bx By Bz Ex Ey Ez rho`，没有将 split PML fields 或 `F/G` 作为 plotfile consumer，因此 reader-side contract 无法直接观察 PML spectral cleaning state。

## 证据边界

项目报告 `runs/stage-c-validation/pml_psatd_3d_cleaning_contract_mpi2.{json,md}` 继续保留为：

1. native diagnostics finite/output completeness contract；
2. clean/control 的 `divE`、`divB` 和 field-energy 对照；
3. 不开启 strong cleaning physics gate。

要把结论升级为正向 physics gate，至少需要 solver-native spectral residual、可读出的 PML `F/G` 状态，或一个直接由上游维护的 cleaning analysis；仅仅把 cell-centered `divB` 的阈值再调宽不能完成这一步。
