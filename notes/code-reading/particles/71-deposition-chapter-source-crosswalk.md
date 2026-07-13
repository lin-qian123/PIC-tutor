# 第 5 章 deposition 正文与源码 crosswalk

新增合同 `scripts/audit_deposition_chapter_source_crosswalk.py`，将第 5 章的代表性正文主张与当前 `../warpx` checkout 的源码表面绑定。覆盖：

- `WarpXParticleContainer::DepositCharge()` 的 `icomp/time_shift_delta/LowerCorner` 时间层桥接；
- ABLASTR `deposit_charge(...)` 的 level、CPU/GPU 暂存和 `lockAdd` 合同；
- explicit/implicit Esirkepov 与 Villasenor 的 shape=4 入口；
- implicit endpoint reconstruction、Villasenor shared segment kernel 和 boundary cropping；
- `ChargeDeposition.H`、`ShapeFactors.H` 的普通/shared kernel 与 shape helper；
- `RZ/RCYLINDER/RSPHERE/1D_Z` geometry surface。

该合同只防止正文引用随源码漂移，不宣称 C++ 语义等价、完整 geometry/order runtime 覆盖或论文逐行复现。
