# 7. 边界条件、PML 与 AMR

边界、PML、guard cell 与 AMR 不是若干彼此独立的开关：它们共同决定 Maxwell 更新和粒子推进如何在有限计算域、多个 patch 与多个网格层级中闭合。本章按一条读者可追踪的链展开：**输入怎样定义拓扑，场与粒子怎样在边界采取动作，数据怎样经过 guard cells/PML/AMR 迁移，最后用什么诊断判断这一闭合。**

关于 PML 的资料、WarpX 源码和 Cartesian/RZ 案例可以共同说明指定设置下的实现与可测结果；它们不能自动证明所有 PML 系数、所有 Galilean/cleaning 组合，或 transition zone 中每一条粒子路线都已被验证。阅读本章时，始终把“源码能定位的职责”“案例实际比较的量”和“可外推的物理结论”分开。

边界条件在 PIC 中同时作用于场和粒子。场边界控制 Maxwell 方程如何在计算域边缘闭合；粒子边界控制宏粒子离开、反射、吸收、周期穿越或被记录的方式。二者不能混为一谈。

WarpX 官方理论文档将 PML、PEC、PMC、Silver-Mueller、周期边界和嵌入边界说明在 `Docs/source/theory/boundary_conditions.rst`。初次阅读时可先用下面的源码入口定位问题：

- `Source/BoundaryConditions/`
- `Source/Particles/ParticleBoundaries.cpp`
- `Source/Particles/ParticleBoundaries_K.H`
- `Source/Evolve/WarpXEvolve.cpp::HandleParticlesAtBoundaries`

第一次阅读应先沿本章的因果链理解边界为何同时跨参数解析、主循环分派、场数组镜像和粒子沉积；需要实现细节时，再从本节列出的文件与函数向下追踪。

## 本章的阅读路线：边界是一个闭合系统

读者第一次读本章时，可以把所有边界问题放进同一条因果链：

```text
输入参数 -> field boundary / particle boundary -> guard cells 与 PML 子域
          -> 场更新与粒子处理 -> rho/J 同步与 AMR 重建 -> 输出诊断
```

这条链解释了三个容易混淆的现象。第一，`PEC`、`PML` 和 `embedded boundary` 不是同一类对象：前者是场边界条件，第二者是吸收层的离散子域，第三者还要先生成 cut-cell 几何和粒子侧距离判定。第二，粒子被吸收、被记录或穿过周期边界，和场的 Maxwell 边界是否正确是两条需要分别验证的路径。第三，AMR 的难点不只是细网格上的局部更新，还包括 coarse/fine ownership、guard-cell 填充、moving window 和粒子/源项同步。

因此每个边界案例都应按以下顺序阅读：

1. 先确认边界参数的 owner、默认值和方向配对；
2. 再确认边界进入哪个场/粒子分派，以及需要多少 guard cells；
3. 最后选择与问题相符的 observable：反射率、残余场、能量账本、重启重复性、scraped-particle buffer 或 AMR route ledger。

本章后面的案例段不是另一套理论，而是这条链上不同节点的检验。通过一个 PML 反射率 gate，不代表 RZ 残余场、粒子入 PML 或 AMR transition-zone route ledger 也已证明；读者应始终沿 producer/consumer 和 observable 的边界解释结果。

### 分段阅读：先闭合拓扑，再进入几何与 AMR

第 7 章的对象横跨参数、场、粒子、几何和并行数据迁移。第一次阅读可按下面五段前进，避免把某个边界名、一个 PML 参数或一次末态输出误当成完整边界验证：

1. **先读 7.0--7.3。** 从 `MakeWarpX()` 的 field/particle 拓扑开始，区分 periodic、PEC/PMC、Silver-Mueller 和 `rho/J` 镜像；这一步固定“哪个对象在哪个方向受什么条件约束”。
2. **再读 7.4--7.5。** 把 PML 作为参与时间推进的独立子域，区分 split field、PML 电流和反射率/残余场的观察量；不要以主域 curl 或单一场快照替代 PML 证据。
3. **按几何需求读 7.6--7.8。** Embedded boundary 先定义 cut-cell 几何与辅助标记，再处理 face extension、粒子 signed-distance、吸收和 scraped buffer；场边界与粒子命运必须分别核查。
4. **最后读 7.9。** AMR transition zone 要同时追踪 gather/deposition buffer、coarsen 和同步；最终 plotfile 或 checksum 只能说明末态一致，不能证明细粗网格路由逐项被命中。
5. **用 7.10--7.11 收束。** 为所选 case 写出“拓扑 -> 更新/迁移 -> observable -> 不可外推范围”；只有同时给出边界对象、时间层和比较量，才算完成本章阅读。

这条路线的停止条件是：能够区分 field boundary、particle boundary、PML/guard-cell 与 AMR route 分别改变的状态，并说明为什么一个通过的 case 不能替代另一类边界或几何的验证。

**从第 6 章场更新到第 7 章边界状态的交接卡。** “field push 已返回”不等于主域、PML、physical boundary 和所有 guard cell 已在同一时刻准备好给下一次粒子 gather 使用。应先辨认哪个操作施加物理边界，哪个操作交换或填充离散数组，再判断后续 consumer 实际读取的场状态。

1. **FDTD 的物理边界在每次场更新内施加。** `EvolveB()` 和 `EvolveE()` 都先更新 regular cells，并在启用 PML 时更新 PML cells；随后以 `new_time` 调用 `ApplyBfieldBoundary()` 或 `ApplyEfieldBoundary()`。第二半 `EvolveB()` 结束后，主循环会在 `do_pml` 路径执行 `DampPML()`，并对 `E/B/F/G` 做 moving-window 宽度的 `FillBoundary*()`。源码明确注明此时主域内 `E/B` 已更新、但 guard cells 不必全都仍然新鲜；无 PML 时 `m_safe_guard_cells` 只会额外请求 `FillBoundaryB()`。因此不能把一次 FDTD field update 概括成“所有数组和 ghost region 已闭合”。
2. **PSATD 的场边界和后续通信也分两层。** `PushPSATD()` 在谱空间更新后推进 PML box，并对每个 fine/coarse patch 施加 `ApplyEfieldBoundary()`、`ApplyBfieldBoundary()`；回到 `OneStep_nosub()` 后，普通 PSATD 路径才以 `ng_afterPushPSATD` 填充 `E/B`，并按 cleaning 选项填充 `F/G`。谱更新、physical boundary 和 guard-cell exchange 因而是相邻但不同的 consumer 交接点。
3. **`FillBoundary` 不是物理边界条件的别名。** `FillBoundaryE/B(lev, ...)` 会分别处理 fine 与 coarse patch；有 PML 时还先执行 valid-domain 与 PML 的 `Exchange()`，再填 PML 及主域 guard cells。它传播或同步已有数组，不能代替 PEC、PMC、Silver-Mueller、axis 或 embedded-boundary 规则本身。下一次 explicit 路径由 `ExplicitFillBoundaryEBUpdateAux()` 按 `ng_FieldGather` 准备 `E/B`，更新 auxiliary fields 后再填 auxiliary guard cells；粒子 gather 消费的是这一步准备好的表示。
4. **粒子边界仍是独立路径。** `HandleParticlesAtBoundaries()` 另行调用粒子 `ApplyBoundaryConditions()`、收集 domain/embedded-boundary scraping buffer 并重新分配粒子。即使场的 `E/B` 边界和 guard exchange 通过，也不能据此断言吸收、反射、记录或 AMR transition-zone 的粒子路由正确。

验证必须针对实际 consumer：PEC/PMC 可比较反射后解析振幅或能量账本，PML 可比较反射率或残余场，restart 应逐字段比较恢复后的输出，而 transition zone 仍需要 pre-sync route count、weight 与 `rho/J` buffer 的账本。一个主域场 snapshot 或一次 `FillBoundary` 成功都不能单独证明完整的 field-to-boundary 链已经闭合。

## 7.0 源码入口地图

本章不能只按“边界条件”这个名词归类，因为 WarpX 中的边界语义会穿过参数解析、场数组 guard cell、PML split field、粒子删除/反射/记录、诊断和 AMR 重建。以下列出读代码时需要反复回查的入口：

| 问题 | 核心函数/文件 | 读者问题 |
|---|---|---|
| 边界解析 | `MakeWarpX()` | field periodic 为何约束 particle boundary？ |
| field 参数 | `FieldBoundaries` | 为何 periodic 必须在 lo/hi 成对闭合？ |
| particle 参数 | `ParticleBoundaries` | 何时继承 periodic，何时保持 absorbing？ |
| 场边界 | `WarpXFieldBoundaries` | PEC、PMC、Silver-Mueller 和轴边界怎样分派？ |
| 源项边界 | `ApplyRhoJ` | rho/J 何时镜像，何时在导体内清零？ |
| PML | `PML` / `DampPML()` | split field 和电流 damping 如何协同？ |
| guard cells | `WarpXComm` / `GuardCellManager` | 哪些物理和数值选择决定通信宽度？ |
| AMR 重建 | `RemakeLevel()` | 重映射后哪些场、粒子和 buffer 必须一起重建？ |
| scraping | `BoundaryScrapingDiagnostics` | 粒子何时被记录，而不只是被删除？ |

这些入口位于 WarpX 的 `Source/BoundaryConditions/`、`Source/Parallelization/`、`Source/Particles/` 与 `Source/Diagnostics/`；后文以文件路径和函数职责说明它们的关系，而不依赖随版本漂移的固定行号。

边界章节的主线可按以下闭合链阅读：

1. `WarpX::MakeWarpX()` 调用 `parse_field_boundaries()`，由 field 边界构造 periodicity array，再据此调用 `parse_particle_boundaries()`。
2. 场路径分别应用 `E/B` 边界、PEC/PMC/PECInsulator/Silver-Mueller/axis 条件和反射型 `rho/J` 边界；PML 则维护 split fields 与电流 damping。
3. `WarpXComm` 的 `FillBoundary` 与 PML exchange 让边界数据进入相邻 patch；`GuardCellManager` 据此决定 guard 宽度，AMR regrid、`RemakeLevel()` 与 EB factory 再重建相应状态。
4. 粒子路径由 `HandleParticlesAtBoundaries` 处理边界和 buffer；需要记录而非只删除的粒子进入 `BoundaryScrapingDiagnostics`。

因此，后续解释边界时要同时回答三类问题：输入参数如何被约束，场和粒子的运行时边界动作在哪里发生，以及这些动作怎样与 PML、guard cell、AMR 和 diagnostics 互相交叉。每一节都应能回到一个可观察量，例如反射率、残余场、scraped-particle buffer、能量账本或 AMR 的中间 route 账本；没有对应观察量时，只能把结论写成源码路径或未闭合边界。

## 7.1 field / particle 边界不是两套彼此独立的输入

`WarpX::MakeWarpX()` 在构造单例之前，先解析 field boundary，再从中提取 periodic 掩码，最后才解析 particle boundary：

```cpp
std::tie(field_boundary_lo, field_boundary_hi) =
    warpx::boundary_conditions::parse_field_boundaries();

const auto is_field_boundary_periodic =
    warpx::boundary_conditions::get_periodicity_array(field_boundary_lo, field_boundary_hi);

std::tie(particle_boundary_lo, particle_boundary_hi) =
    warpx::particles::parse_particle_boundaries(is_field_boundary_periodic);
```

源码入口：`Source/WarpX.cpp`。

这意味着 particle 边界不是“读完自己就结束”，而是依赖 field 边界的第二阶段配置。其后果有两条：

1. 某方向若 field 是 periodic，则 particle 必须两侧都 periodic；
2. 如果用户根本没写 `boundary.particle_lo/hi`，periodic 的 field 方向会自动把 particle 边界改成 periodic，而不是保留 absorbing。

对应的 field consistency 检查在 `FieldBoundaries.cpp`：

```cpp
WARPX_ALWAYS_ASSERT_WITH_MESSAGE(
    (is_lo_periodic == is_hi_periodic),
    "field boundary must be consistenly periodic in both lo and hi");
```

源码入口：`Source/BoundaryConditions/FieldBoundaries.cpp`。

而 field/particle 联合一致性检查在 `ParticleBoundaries.cpp`：

```cpp
WARPX_ALWAYS_ASSERT_WITH_MESSAGE(
    (particle_boundary_lo[idim] == ParticleBoundaryType::Periodic) &&
    (particle_boundary_hi[idim] == ParticleBoundaryType::Periodic),
    "field and particle boundary must be periodic in both lo and hi");
```

源码入口：`Source/Particles/ParticleBoundaries.cpp`。

因此，periodic 在 WarpX 中的真实语义不是“某一侧做周期延拓”，而是“整根坐标轴拓扑闭合”。

读参数时应把 `boundary.field_*`、`boundary.particle_*`、`boundary.potential_*`、PECInsulator parser、`particles.crop_on_PEC_boundary` 和 PML 参数作为同一组依赖来检查：先由 field periodicity 建立拓扑，再确认粒子侧继承和 PML/导体边界是否与所选 geometry 相容。

## 7.2 电磁 field boundary 的顶层分派

field boundary 参数解析完成后，真正把边界施加到场数组的入口在 `WarpXFieldBoundaries.cpp`。`ApplyEfieldBoundary()` 顶层首先按边界类型分派：

```cpp
if (::isAnyBoundary<FieldBoundaryType::PEC>(field_boundary_lo, field_boundary_hi)) {
    PEC::ApplyPECtoEfield(...);
}

if (::isAnyBoundary<FieldBoundaryType::PMC>(field_boundary_lo, field_boundary_hi)) {
    PEC::ApplyPECtoBfield(...);
}

if (::isAnyBoundary<FieldBoundaryType::PECInsulator>(field_boundary_lo, field_boundary_hi)) {
    pec_insulator_boundary->ApplyPEC_InsulatortoEfield(...);
}
```

源码入口：`Source/BoundaryConditions/WarpXFieldBoundaries.cpp`。

`ApplyBfieldBoundary()` 除了 PEC/PMC/PECInsulator 外，还处理 Silver-Mueller：

```cpp
if (lev == 0) {
    if (subcycling_half == SubcyclingHalf::FirstHalf) {
        if(::isAnyBoundary<FieldBoundaryType::Absorbing_SilverMueller>(field_boundary_lo, field_boundary_hi)){
            m_fdtd_solver_fp[0]->ApplySilverMuellerBoundary(...);
        }
    }
}
```

源码入口：`Source/BoundaryConditions/WarpXFieldBoundaries.cpp`。

这说明 Silver-Mueller 不是通用 field boundary post-process，而是挂在 Yee/FDTD 的 `B` first half-push 上的专用边界。

继续往下看其内部实现时，还要再补一层认识：它更新的不是域内最后一层 `B`，而是物理域外第一层 guard cell，并且按 Yee 交错把切向 `E` 递推到切向 `B`。因此检查 Silver-Mueller 时应同时查看 first-half B 更新、对应 guard cell 和离域后的残余场，而非只看边界参数名称。

## 7.3 PEC / PMC 不只是场边界，也是沉积对称性

官方理论文档对 PEC 的定义是：边界上切向 `E` 与法向 `B` 为零；guard 区对场做奇偶镜像；rho 和平行电流的边界处理还取决于粒子边界是 reflecting 还是 absorbing。见 `Docs/source/theory/boundary_conditions.rst`。

这意味着 PEC/PMC 的章节写法不能只停留在“某些分量置零”：

- 对 E/B，要讲边界值和 guard-cell 镜像；
- 对 rho/J，要讲镜像沉积与 image charge / reflective deposition；
- 对粒子，要讲 `ApplyBoundaryConditions()` 和沉积语义如何配套。

因此 PEC、PMC 与 PECInsulator 的阅读顺序应固定为：先看 E/B 的镜像或约束，再看 `rho/J` 的边界处理，最后检查粒子反射、吸收或 cropping 的配套语义。三层缺任一层，都不能把边界写成简单的“分量置零”。

PMC 还有一条很直接的场级 regression：`Examples/Tests/pec/inputs_test_3d_pmc_field`。它在 `z` 方向设 PMC、在局部区域初始化正弦 `Ey/Bx` 波包，然后用 `analysis_pec.py` 检查反射后的 standing wave 是否达到理论上的 constructive interference 振幅 `±2E_in`。因此这条测试验证的不是抽象“PMC 边界存在”，而是 PMC 通过交换 PEC 的 E/B 角色后，反射相位与站波振幅仍满足理论合同。

Silver-Mueller 的 regression 则是另一条完全不同的口径。`Examples/Tests/silver_mueller/analysis.py` 直接读取最终 Full diagnostics，并要求所有场分量在脉冲离域后都满足

$$
|E| < 0.01\ \mathrm{V/m},
$$

而这些输入里的入射激光峰值量级约为 `10 V/m`。所以这组测试检验的不是“反射后应形成某种驻波”，而是

$$
|E_{\mathrm{reflected}}| \ll |E_{\mathrm{incident}}|.
$$

该 family 共有四条最小基准：

- `test_1d_silver_mueller`
- `test_2d_silver_mueller_x`
- `test_2d_silver_mueller_z`
- `test_rz_silver_mueller_z`

它们分别覆盖 1D 轴向出射、2D `x` 向出射、2D `z` 向出射，以及 RZ `z` 向出射；其中 RZ 版本还同时把 `r_lo = none` 的轴线正则性和 `absorbing_silver_mueller` 开放边界放到同一最小回归里。

`PEC` 与 `PECInsulator` 的 regression 边界也应和上面区分开。`pec` family 里至少有两组强 analysis：

1. `test_3d_pec_field` 与 `test_3d_pec_field_mr`
   这两条分别用 `analysis_pec.py` 和 `analysis_pec_mr.py` 检查反射后 standing-wave 的 `Ey_max/Ey_min` 是否接近理论 `±2E_in`。单级版本容差为 `1%`，MR 版本放宽到 `5%`。因此它们真正验证的是 PEC 场边界反射后的波振幅合同，而不是抽象“边界条件被支持”。
2. `test_2d_pec_field_insulator_implicit` 与 `..._restart`
   这两条走 `analysis_pec_insulator_implicit.py`，把 `fieldenergy.txt` 与 `poyntingflux.txt` 合成完整能量账本，并要求相对误差低于 `10^{-13}`。因此它们真正验证的是 `pec_insulator` parser 边界、implicit 场推进和边界 Poynting flux reduced diagnostics 一起构成的精确能量记账合同。`..._restart` 版本说明从 checkpoint 恢复后同一合同仍成立，但它并不是独立的逐字段 restart 对照。

相比之下，`test_3d_pec_particle` 当前没有独立 analysis，仍应诚实记录为粒子侧 gather/deposition 的 checksum 基线，而不是被误写成强物理 benchmark。

PML 的物理目标是吸收入射电磁波，使开放边界尽量不反射。经典 PML 思想来自 Berenger。WarpX 在 `OneStep_nosub` 的场推进后处理 PML：FDTD 分支中，场推进后若 `do_pml` 为真，执行 `DampPML()` 并填充 E/B/F/G 的 moving-window guard cells。PSATD 分支中也有单独的 PML damping。

## 7.4 PML 在 WarpX 里是独立子域，不是单个边界公式

`PML` 类本身管理的是一整套 PML 子域、split fields 和阻尼系数缓存。读构造函数时，先把它的输入按职责归成四组：

```text
PML geometry:       ncell, delta
particle coupling:  pml_has_particles
in-domain mode:     do_pml_in_domain
cleaning coupling:  do_pml_dive_cleaning, do_pml_divb_cleaning
```

这不是完整函数签名，而是对 `PML` 构造参数中与本章因果链相关部分的阅读索引；其余网格、patch 和通信对象由调用侧提供。

源码入口：`Source/BoundaryConditions/PML.H`。

真正承载阻尼 profile 的核心数据结构是 `SigmaBox`，其中缓存了：

- `sigma` / `sigma_star`
- `sigma_cumsum` / `sigma_star_cumsum`
- `sigma_fac` / `sigma_star_fac`
- `sigma_cumsum_fac` / `sigma_star_cumsum_fac`

源码入口：`Source/BoundaryConditions/PML.H`。

`SigmaBox` 的 profile 在 `PML.cpp` 中按离边界距离平方增长：

```cpp
Real offset = static_cast<Real>(glo-i);
p_sigma[i-slo] = fac*(offset*offset);
...
offset = static_cast<Real>(glo-i) - 0.5_rt;
p_sigma_star[i-sslo] = fac*(offset*offset);
```

源码入口：`Source/BoundaryConditions/PML.cpp`。

所以 `warpx.pml_delta` 控制的是阻尼增长深度，而不是简单的总厚度。

## 7.5 PML split field 与 PML 电流

在主循环里，PML 阻尼入口是 `WarpX::DampPML()`，Cartesian 实际工作函数是 `DampPML_Cartesian()`。

源码入口：`Source/BoundaryConditions/WarpXEvolvePML.cpp`。

这个函数先取出 `pml_E`、`pml_B`、`sigba` 和每个分量的 stagger 信息，然后把它们送进 `warpx_damp_pml_ex/ey/ez/bx/by/bz`。例如 `Ex` 的 split 分量阻尼：

```cpp
if (sy == 0) {
    Ex(i,j,k,PMLComp::xy) *= sigma_star_fac_y[j-ylo];
} else {
    Ex(i,j,k,PMLComp::xy) *= sigma_fac_y[j-ylo];
}
```

源码入口：`Source/BoundaryConditions/WarpX_PML_kernels.H`。

这说明 PML 不是给整个 `E_x` 统一乘一个阻尼系数，而是对 `Exy`、`Exz` 这类 split components 按其离散位置和方向分别阻尼。

如果进一步允许粒子进入 PML，即 `warpx.pml_has_particles = 1`，那么粒子电流还要按 split 方式注入 PML 电场。`push_ex_pml_current()` 的形式是：

```cpp
alpha_xy = sigjy[k-ylo]/(sigjy[k-ylo]+sigjz[l-zlo]);
alpha_xz = sigjz[l-zlo]/(sigjy[k-ylo]+sigjz[l-zlo]);
Ex(j,k,l,PMLComp::xy) = Ex(j,k,l,PMLComp::xy) - mu_c2_dt  * alpha_xy * jx(j,k,l);
Ex(j,k,l,PMLComp::xz) = Ex(j,k,l,PMLComp::xz) - mu_c2_dt  * alpha_xz * jx(j,k,l);
```

源码入口：`Source/BoundaryConditions/PML_current.H`。

也就是说，PML 中的 `J_x` 不是直接加到“整体 `E_x`”上，而是要分摊到与阻尼方向一致的 split components 上。

PML 的 regression 入口也不能继续混成单一 checksum 桶。当前最稳定的五条验证线是：

1. `test_2d_pml_x_yee`
   - `analysis_pml_yee.py`
   - 从最终全场重建总电磁能量
   - 计算反射率 `R = E_end / E_start`
   - 要求其相对理论 `5.683000058954201e-07` 的误差低于 `5%`
2. `test_2d_pml_x_ckc`
   - `analysis_pml_ckc.py`
   - 做同一反射率检查
   - 但理论值变成 `1.8015e-06`
3. `test_2d_pml_x_psatd` 与 `test_2d_pml_x_galilean`
   - 共享 `analysis_pml_psatd.py`
   - 先从 `diag1000050` 复算初始电磁能量并要求与硬编码参考值一致到 `1e-14`
   - 再要求最终反射率低于 `1e-6`
   - 因而这里验证的是 `PSATD/Galilean PSATD + PML` 的低反射率合同
4. `test_rz_pml_psatd`
   - `analysis_pml_psatd_rz.py`
   - 不比较能量比，而是在脉冲离域后直接要求域内 `max(|Er|,|Ez|) < 2`
   - 它真正验证的是 RZ radial PML 的残余场衰减
5. `test_2d_pml_x_yee_restart` 与 `test_2d_pml_x_psatd_restart`
   - 复用顶层 `Examples/analysis_default_restart.py`
   - 逐字段比较 restart 与非 restart 输出
   - 因而这两条是在测 `PML + solver` 场景的 restart 可重复性，而不是新物理吸收判据

相比之下，`test_3d_pml_psatd_dive_divb_cleaning` 当前 `analysis=OFF`。它把 `psatd + pml + do_dive_cleaning + do_divb_cleaning + do_pml_dive/divb_cleaning` 组合在一起，但目前只应诚实记录为 workflow/output checksum 基线，不能写成与上面四条同等级的强吸收 benchmark。

### 7.5.1 用正确的 observable 判断 PML

PML 的问题不是“是否开了吸收边界”，而是出射波、不同 solver、几何和 restart 后的状态是否仍满足对应的物理目标。应先根据问题选择 observable，再解释 analysis 的结论。

| 目标 | 代表性 consumer | 可以支持的结论 | 不能替代 |
|---|---|---|---|
| Cartesian FDTD 反射 | `analysis_pml_yee.py`、`analysis_pml_ckc.py` | 末态能量反射率与相应理论值的偏差小于 `5%` | PSATD、RZ 或其他入射角 |
| Cartesian PSATD/Galilean 反射 | `analysis_pml_psatd.py` | 初始能量重建一致，末态反射率小于 `1e-6` | 每个 PML 系数的逐项证明 |
| RZ PML 残余场 | `analysis_pml_psatd_rz.py` | 脉冲离域后 `max(|Er|,|Ez|) < 2` | Cartesian 反射率或完整轴向诊断 |
| checkpoint/restart | `analysis_default_restart.py` | 恢复后输出序列与基线一致 | 新的吸收精度结论 |
| particles in PML | 专用 `analysis_particles_in_pml.py` 和绝对值复核 | 指定层级/字段的残余量满足 consumer | 粒子轨迹守恒或完整 AMR 覆盖 |

因此，一个低反射率 PASS 不能被写成“PML 在所有场景都正确”。它只说明指定 solver、输入、网格、诊断和阈值构成的组合通过。特别是 3D AMR particles-in-PML 的官方 signed gate 通过而更强 absolute gate 仍越界，说明 consumer 的定义本身也是结论范围的一部分。

### 7.5.2 从 split field 到 runtime evidence

前文的 `PML`、`SigmaBox`、`DampPML()` 与 `push_ex_pml_current()` 解释了吸收层如何在源码中被构造和推进：每个 split component 按自身 staggering 和阻尼方向更新，粒子电流也要分摊到对应的 split field。源码入口说明“程序有这条机制”，运行 consumer 才回答“这条机制在某个 case 中的可观测结果”。

读者应把 PML 证据固定为三层：理论或文献解释吸收的目标，源码路径解释系数和分派，regression/analysis 限定一个 measurable outcome。LeeCPC2015 的 accepted manuscript 与 PSATD-PML 源码可以支持机制和公式映射的讨论，但 publisher-formatted PDF 的逐式差异仍未完成；同样，Cartesian、RZ、cleaning 和粒子入 PML 也必须保持各自的 observable 边界。

### 7.5.3 PML 配置与验证卡：先选问题，再满足依赖

下面这张卡不是可不加判断地复制的万能输入，而是把官方参数约束、源码中的运行时检查和已有最小测试连成一次配置审查。开始前先写清楚：要吸收的是无源出射波，还是带电粒子离域后留下的场；采用 Cartesian 还是 RZ；以及最终要比较反射率、残余场还是 restart 输出。不同问题不应靠累加开关来解决。

1. **无源电磁脉冲离开 Cartesian 主域。** 对相应方向设 `boundary.field_lo/hi = pml`；`warpx.pml_ncell` 是 PML 的 cell 厚度，`warpx.pml_delta` 是吸收系数增长的特征深度。默认 `do_pml_in_domain = 0` 时，不应无理由同时打开粒子相关开关。可从 `test_2d_pml_x_yee`/`..._ckc` 的末态能量反射率，或 `test_2d_pml_x_psatd` 的初始能量重建和末态 `R < 10^{-6}` 开始。这种波动测试不能证明粒子离域、AMR 或另一种几何下的电荷残余也正确。

2. **宏粒子必须穿过吸收层，并检验离域后的残余场。** `warpx.do_pml_in_domain = 1` 使 PML 与主域边缘最后 `pml_ncell` 个 cells 重叠；据官方参数约束，`pml_has_particles = 1` 只能在此条件下使用。若问题是 PML 中电流的阻尼，则还要显式设 `do_pml_j_damping = 1`，它同样要求 in-domain PML。`particles_in_pml/inputs_test_2d_particles_in_pml` 同时打开这三个开关，并以粒子离域后全域 `max(E)` 的绝对阈值为 consumer；它不能证明任意粒子轨迹、守恒量或任意 AMR 配置均已验证。

3. **Cartesian PSATD 的开放 3D 边界伴随 divergence cleaning。** `do_pml_dive_cleaning` 与 `do_pml_divb_cleaning` 必须取相同值；这对 PML cleaning 只在 Cartesian PSATD 实现，FDTD 不能开启 divB cleaning。上一节列出的 3D PSATD PML-cleaning 组合输入是这里的起点；因当前没有独立 analysis，它只能提供 workflow/output 基线，不能替代强吸收 gate。两个参数在某次运行不报错，也不能推出该组合的 Nyquist 稳定性已经被定量证明。

4. **RZ 的径向开放边界。** RZ PML 只可与 PSATD 使用，且 `z` 方向没有 PML；PML cleaning 开关必须保持关闭。`test_rz_pml_psatd` 在脉冲离域后检查 `max(|Er|,|Ez|) < 2`。这个 RZ 残余场阈值不是 Cartesian 能量反射率，也不覆盖轴向 PML。

这里有两个常见的误读需要立即排除。第一，`pml_ncell` 和 `pml_delta` 都以 cells 为单位，但前者决定吸收层的几何厚度，后者决定阻尼 profile 增长的特征深度；把二者设成相同数值只是某个输入的选择，并非定义上的等价。第二，`do_pml_in_domain = 1` 会让 PML 覆盖物理主域或 fine patch 边缘最后的 `ncell` 个 cells，源码还要求边缘 box 的长度严格大于这段宽度。因此它改变的不只是“吸收是否更强”，还改变了哪一段主域可供粒子和场更新使用。

带 AMR 的粒子入 PML 还应额外检查 warning，而不是把 warning 当作成功信息。当前源码在 `max_level > 0`、`particle_shape > 1` 且 `do_pml_j_damping = 1` 时明确记录 coarse/fine interface 上可能出现数值伪影，并建议用一阶 shape 避开该问题。这是一个有条件的数值风险提示，不是该组合被禁止，也不是 AMR-PML 完整正确性的证明；应以相应的 particles-in-PML consumer、网格收敛和界面诊断另行判断。

**配置后的最小验收顺序。** 先让输入解析的 geometry/solver guard 自己拒绝非法组合；再确认输出中实际存在所选 consumer 所需的 Full diagnostics；最后只报告该 consumer 的量，例如 `R = E_{end}/E_{start}`、离域后的 `max(E)`、RZ 的 `max(|Er|,|Ez|)` 或 restart 的逐字段差异。若改变了 solver、几何、PML 是否在主域内、是否允许粒子进入或是否加入 AMR，就回到本卡重新选择 observable，不能沿用上一种 case 的 PASS 句子。


## 7.6 Embedded boundary 先是几何初始化和辅助标记系统

前面讨论的 PML、PEC、PMC、Silver-Mueller 都作用在计算域外边界上，而 embedded boundary 的第一步不是“给某个边界类型分派更新公式”，而是先把几何对象嵌入到 AMReX cut-cell 数据结构。

运行时总开关在 `EmbeddedBoundary/Enabled.cpp`：

```cpp
std::string eb_implicit_function;
bool eb_enabled = pp_warpx.query("eb_implicit_function", eb_implicit_function);

std::string eb_stl;
eb_enabled |= pp_eb2.query("geom_type", eb_stl);
```

源码入口：`Source/EmbeddedBoundary/Enabled.cpp`。

这说明 EB 的启用条件不是单一布尔量，而是：

1. 编译时必须有 `AMREX_USE_EB`；
2. 运行时必须提供 `warpx.eb_implicit_function`，或者走 `eb2.geom_type` / `eb2.stl_file` 的 AMReX EB2 参数路径。

几何真正初始化在 `WarpX::InitEB()`：

```cpp
if (! impf.empty()) {
    auto eb_if_parser = utils::parser::makeParser(impf, {"x", "y", "z"});
    ParserIF const pif(eb_if_parser.compile<3>());
    auto gshop = amrex::EB2::makeShop(pif, eb_if_parser);
    amrex::EB2::Build(gshop, Geom(maxLevel()), maxLevel(), maxLevel()+20);
} else {
    amrex::ParmParse pp_eb2("eb2");
    if (!pp_eb2.contains("geom_type")) {
        std::string const geom_type = "all_regular";
        pp_eb2.add("geom_type", geom_type);
    }
    amrex::EB2::Build(Geom(maxLevel()), maxLevel(), maxLevel()+20);
}
```

源码入口：`Source/EmbeddedBoundary/WarpXInitEB.cpp`。

这里的结构很清楚：

- 若给出 `warpx.eb_implicit_function`，WarpX 自己负责把解析函数包装成 `ParserIF` 再交给 `AMReX EB2::GeometryShop`；
- 若没有隐式函数，就沿用 `eb2.*` 参数，由 AMReX EB2 直接构几何；
- `maxLevel()+20` 是为了让 EB2 尽量向粗层 coarsen，服务 multigrid，而不是某个物理精度参数。

EB 几何建立后，WarpX 还会把 signed distance 场填进 field registry：

```cpp
const amrex::EB2::IndexSpace& eb_is = amrex::EB2::IndexSpace::top();
for (int lev=0; lev<=maxLevel(); lev++) {
    const amrex::EB2::Level& eb_level = eb_is.getLevel(Geom(lev));
    auto const eb_fact = fieldEBFactory(lev);
    amrex::FillSignedDistance(*m_fields.get(FieldType::distance_to_eb, lev), eb_level, eb_fact, 1);
}
```

源码入口：`Source/EmbeddedBoundary/WarpXInitEB.cpp`。

所以 `distance_to_eb` 不是附加诊断，而是后续 scraping、近壁沉积和 cut-cell 处理可以直接复用的几何辅助场。

更关键的是，`EmbeddedBoundaryInit.*` 在初始化阶段就为后续 solver / deposition 准备了几类辅助标记：

- `MarkReducedShapeCells`：若高阶 shape 可能覆盖到部分或完全 cut cell，就强制降成一阶沉积；
- `MarkUpdateCellsStairCase`：对非 ECT solver，只要 field 自由度邻接到非 regular cell，就停止更新；
- `MarkUpdateECellsECT` / `MarkUpdateBCellsECT`：ECT solver 不看 stair-case 邻域，而是直接看对应 edge length 或 face area 是否为零。

例如 `MarkReducedShapeCells()` 的混合区域逻辑是：

```cpp
if ( !flag(i_cell, j_cell, k_cell).isRegular() ) {
    reduce_shape = 1;
}
```

源码入口：`Source/EmbeddedBoundary/EmbeddedBoundaryInit.cpp`。

而 `MarkUpdateCellsStairCase()` 的核心是：

```cpp
if ( !flag(i_cell, j_cell, k_cell).isRegular() ) {
    eb_update_flag = 0;
}
```

源码入口：`Source/EmbeddedBoundary/EmbeddedBoundaryInit.cpp`。

这说明 EB 在 WarpX 里的第一层实现不是“直接改 Maxwell 更新式”，而是先把 cut-cell 几何转换成：

1. 粒子沉积是否降阶；
2. 场自由度是否允许更新；
3. edge/face 几何量是否还存在。

因此 embedded boundary 必须先作为几何与辅助标记系统阅读，再进入 `WarpXFaceExtensions.cpp` 的 face-extension 稳定性标志、intrusion 判据和 cut-face 修正。把 EB 简化成某一个 field boundary 会遗漏它对数组布局和粒子距离判定的前置影响。

## 7.7 Embedded boundary 的 face extension：把不稳定 cut face 变成 enlarged face

对 ECT solver 来说，仅仅知道某个 face 被 cut 还不够，因为部分 cut face 的有效面积可能小到破坏稳定性。WarpX 的处理不是简单禁用这些 face，而是尝试把它们扩成 enlarged face。

初始化侧先在 `MarkExtensionCells()` 中定义两个标志：

```cpp
flag_ext_face_data(i, j, k) = int(S(i, j, k) < S_stab && S(i, j, k) > 0);
if(flag_ext_face_data(i, j, k)){
    flag_info_face_data(i, j, k) = 0;
}
if(int(S(i, j, k) > 0 && !flag_ext_face_data(i, j, k))) {
    flag_info_face_data(i, j, k) = 1;
}
```

源码入口：`Source/EmbeddedBoundary/EmbeddedBoundaryInit.cpp`。

其中：

- `flag_ext_face = 1` 表示这个 cut face 本身不稳定，必须扩展；
- `flag_info_face = 0` 表示它当前是借方面；
- `flag_info_face = 1` 表示它是可出借面积的稳定面；
- 在 extension 过程中，被别人侵入的 lender 会再改成 `2`。

真正的 extension 在 `WarpX::ComputeFaceExtensions()` 里按三步进行：先初始化 `m_borrowing`，再依次尝试 `ComputeOneWayExtensions()` 和 `ComputeEightWaysExtensions()`，最后收缩并整理 borrowing 记录。这条顺序很重要：第二阶段只能处理第一阶段尚未稳定的 face，不能把 two-stage extension 误读成两个独立开关。

源码入口：`Source/EmbeddedBoundary/WarpXFaceExtensions.cpp`。

第一步是 one-way extension，只允许从一个正交邻居一次性借满所需面积 `S_ext`。如果存在这样的 lender，就直接把 lender 的 `S_mod` 扣掉 `S_ext`，把 borrower 的 `S_mod` 增加 `S_ext`，并把 lender 标成 `2`。见 `Source/EmbeddedBoundary/WarpXFaceExtensions.cpp`。

第二步是 eight-ways extension。若单邻居借不满，就在 `3x3` 邻域内筛选所有可用 lender，按原始 face 面积比例分摊：

```cpp
const amrex::Real patch = S_ext * ::GetNeigh(S, i, j, k, i_n, j_n, idim) / denom;
```

源码入口：`Source/EmbeddedBoundary/WarpXFaceExtensions.cpp`。

但 WarpX 还会反复剔除那些按该比例借出后会把自己 `S_mod` 减成非正的邻居，因此 eight-ways 不是机械加权，而是“保正性的面积分摊”。见 `Source/EmbeddedBoundary/WarpXFaceExtensions.cpp`。

如果 one-way 和 eight-ways 都失败，就进入 BCK fallback：

```cpp
if (flag_ext_face_max_lev_idim(i, j, k)) {
    S(i, j, k) = ::ComputeSStab<idim>(i, j, k, lx, ly, lz, dx, dy, dz);
    flag_info_face_max_lev_idim(i, j, k) = -1;
}
```

源码入口：`Source/EmbeddedBoundary/WarpXFaceExtensions.cpp`。

源码注释说明这是 Benkler-Chavannes-Kuster correction，精度低于常规 ECT extension，但仍优于纯 staircasing。

extension 的借用关系不会散落在若干数组里，而是统一压进 `FaceInfoBox`：

```cpp
struct FaceInfoBox {
    amrex::Gpu::DeviceVector<Neighbours> neigh_faces;
    amrex::Gpu::DeviceVector<amrex::Real> area;
    amrex::Gpu::DeviceVector<int> inds;
    amrex::BaseFab<int> size;
    amrex::BaseFab<int*> inds_pointer;
```

源码入口：`Source/EmbeddedBoundary/WarpXFaceInfoBox.H`。

它记录的是“这个 enlarged face 向哪些邻居借了多少面积”。后续 ECT `B` 更新时，`WarpX::EvolveB()` 把 `m_flag_info_face` 和 `m_borrowing` 直接送进 solver：

```cpp
m_fdtd_solver_fp[lev]->EvolveB( m_fields,
                                lev,
                                patch_type,
                                m_flag_info_face[lev], m_borrowing[lev], a_dt );
```

源码入口：`Source/FieldSolver/WarpXPushFieldsEM.cpp`。

在 `FiniteDifferenceSolver::EvolveBCartesianECT()` 中，不稳定 face 会先聚合 enlarged face 的有效电荷：

```cpp
Venl_dim(i, j, k) = Rho(i, j, k) * S(i, j, k);
...
Venl_dim(i, j, k) += Rho(ip, jp, kp) * borrowing_dim_area[ind];
...
rho_enl = Venl_dim(i, j, k) / S_mod(i, j, k);
```

源码入口：`Source/FieldSolver/FiniteDifferenceSolver/EvolveB.cpp`。

因此，WarpX 的 face extension 不是“把几何修漂亮一点”，而是直接决定 ECT solver 如何构造 enlarged face 的有效 `rho` 并推进 `B`。

## 7.8 Embedded boundary 的粒子侧：signed-distance 判定、默认吸收与 scraped buffer

对粒子来说，embedded boundary 的关键并不是 face extension，而是“什么时候认定粒子已经撞进了 EB，以及撞进去之后怎样处理”。

`ParticleScraper.H` 的核心逻辑非常直接：

```cpp
ablastr::particles::compute_weights<amrex::IndexType::NODE>(
    xp, yp, zp, plo, dxi, i, j, k, W);
amrex::Real const phi_value = ablastr::particles::interp_field_nodal(i, j, k, W, phi);

if (phi_value < 0.0)
{
    ...
    amrex::RealVect normal = DistanceToEB::interp_normal(i, j, k, W, ic, jc, kc, Wc, phi, dxi);
    DistanceToEB::normalize(normal);
    ...
    f(ptd, ip, pos, normal, engine);
}
```

源码入口：`Source/EmbeddedBoundary/ParticleScraper.H`。

这说明 WarpX 的粒子撞墙检测并不是拿粒子坐标去直接查解析几何，而是：

1. 在 nodal `distance_to_eb` 上插值；
2. 若 `phi_value < 0`，认定粒子进入了需要刮擦的 EB 区域；
3. 再用 `DistanceToEB::interp_normal()` 从 signed-distance 的离散梯度重建法向。

`DistanceToEB.H` 本身也只做这件事。它的 `interp_normal()` 对 `phi` 做差分加权，`normalize()` 再把法向单位化。也就是说，粒子侧法向来自 signed-distance 场，而不是 STL 面片直接投影。

默认处理器在 `ParticleBoundaryProcess.H` 里只有两个最小版本：

```cpp
struct NoOp { ... };

struct Absorb {
    ...
    amrex::ParticleIDWrapper{ptd.m_idcpu[i]}.make_invalid();
}
```

源码入口：`Source/EmbeddedBoundary/ParticleBoundaryProcess.H`。

因此，当前主源码链上的默认 EB 粒子边界语义其实很朴素：不是复杂反射模型，而是“把撞进 EB 的粒子标成 invalid”。真正删除发生在后续 `deleteInvalidParticles()` 或 `Redistribute()`，而不是 `Absorb()` 本身立即擦除数据。

这一逻辑会在多处触发：

- `WarpXParticleContainer` 在 `Redistribute()` 后立刻做一轮 EB 吸收；
- `MultiParticleContainer::ScrapeParticlesAtEB()` 可以对所有 species 统一刮擦；
- `AddParticles.cpp` 在新增粒子或 flux 注入后，也会先对临时容器做 `scrapeParticlesAtEB(..., Absorb())`。

因此 WarpX 的策略是“新粒子一旦进入容器，就尽快排除已经落在 EB 内部的非法粒子”。

如果用户想把这些 scraped 粒子保留下来做诊断，就可以设置：

- `<species_name>.save_particles_at_eb = 1`

官方文档说明这会把撞到 EB 的粒子复制到 scraped particle buffer，可供 `BoundaryScrapingDiagnostic` 或 Python 接口使用。见 `Docs/source/usage/parameters.rst`。

更重要的是，`ParticleBoundaryBuffer.cpp` 在把粒子放进 EB buffer 时，不是简单复制当前状态，而是用二分法沿粒子轨迹回溯到 `phi = 0` 的真实交点：

```cpp
amrex::Real const dt_fraction = amrex::bisect( 0.0, 1.0,
    [=] (amrex::Real dt_frac) {
        ...
        UpdatePosition(x_temp, y_temp, z_temp, ux, uy, uz, -dt_frac*dt, mass);
        ...
        amrex::Real const phi_value = ablastr::particles::interp_field_nodal(i, j, k, W, phiarr);
        return phi_value;
    } );
```

源码入口：`Source/Particles/ParticleBoundaryBuffer.cpp`。

随后它还会记录 scraping 发生的 step、时间偏移、真实时间和表面法向。也就是说，scraped particle buffer 保存的不是“死前最后一帧粒子”，而是“与 EB 表面交点处的粒子诊断样本”。

因此，embedded boundary 的粒子侧主链可以概括为：

1. `distance_to_eb` 判定粒子是否进入 EB；
2. `DistanceToEB` 重建边界法向；
3. 默认 `Absorb` 仅把粒子标成 invalid；
4. 后续删除逻辑真正清除粒子；
5. 若启用 `save_particles_at_eb`，则 `ParticleBoundaryBuffer` 回溯到 `phi=0` 交点并记录 scraped 事件。

`Examples/Tests/embedded_circle/` 为这条链提供了一个实用但证据层级较弱的入口。它不是 `electrostatic_sphere_eb` 那类解析 `phi/Er` 强基准，也不是 `point_of_contact_eb` 那类直接检查交点几何的强 analysis，而是一个 2D circular EB workflow baseline：

- `eb_implicit_function` 定义圆形导体
- `eb_potential = -10` 进入电静求解
- 电子/氩离子都先 `initialize_self_fields = 1`
- 双物种 `background_mcc` 持续运行
- 两个 species 都打开 `save_particles_at_eb = 1`
- `diag3` 用 `BoundaryScraping` openPMD 写出 scraped 粒子

该 `CMakeLists.txt` 中的 test 没有独立 `analysis.py`，只保留 checksum helper。因此它在本章里更适合承担：

- EB geometry + electrostatic + MCC + BoundaryScraping 的联合工作流基线

而不是承担解析电势或表面碰撞物理的强验证。

domain boundary buffer 的收集时机也要一起记住。`WarpXEvolve.cpp` 里先执行 `mypc->ApplyBoundaryConditions()`，随后立刻调用 `m_particle_boundary_buffer->gatherParticlesFromDomainBoundaries(*mypc, cur_time)`，最后才在 EB 路径后统一 `deleteInvalidParticles()`。因此 buffer 记录依赖的是“粒子还在容器里、但已经越界或即将失效”的中间态，而不是从被删除后的粒子列表回溯出来。对 `save_particles_at_xlo/.../eb`、`BoundaryScrapingDiagnostic` 和 Python buffer 接口来说，这个顺序决定了 scraped 数据为什么能同时保留 step、时间偏移和边界法向。

周期边界有一个关键规则：如果某个方向的场边界是 periodic，该方向粒子边界也必须 periodic；非周期边界则不要求 field 和 particle 边界字面一致。这一规则由本章 7.1 的参数解析和断言直接约束，不能从“某次运行没有报错”反推。

AMR 的目标是把计算资源集中在物理上需要高分辨率的区域。但 PIC 的 AMR 比流体 AMR 更难，因为宏粒子穿过 refinement interface 时会看到不同网格上的插值场，容易产生 self-force、短波反射和电荷/电流不一致。WarpX 官方 `Docs/source/theory/amr.rst` 特别强调两个问题：mesh refinement interface 附近的 spurious self-force，以及电磁波在粗细网格界面处的反射和放大。

在真正进入 coarse-fine interface 之前，还必须先把并行层的 guard-cell 通信模型看清。WarpX 不是“所有字段都统一 FillBoundary 一次”这么简单，而是把通信语义分成两类：

- E/B/F/G/Aux 这类场变量：guard cells 用 `FillBoundary` 风格的复制/同步；
- J/rho 这类源项：重叠区域必须做 `SumBoundary` / `ParallelAdd` 风格的累加，因为粒子靠近 box 边缘时，同一 `(i,j,k)` 可能同时被沉积到一个 box 的 guard 区和另一个 box 的 valid 区。

这一层的统一预算由 `Parallelization/GuardCellManager.*` 管理。它先区分：

- `ng_alloc_*`：每类 MultiFab 实际分配多少 guard cells；
- `ng_FieldSolver`、`ng_FieldGather`、`ng_UpdateAux`、`ng_MovingWindow` 等：PIC 循环不同阶段真正交换多少。

这些配额不是拍脑袋常数，而是共同受以下因素控制：

- 粒子 shape 阶数与 subcycling；
- moving window 位移；
- Galilean / comoving 修正；
- NCI / bilinear filter；
- FDTD stencil 或 PSATD 局部 FFT stencil。

例如 `SyncCurrent()` 的源码注释就明确说明，多层 AMR 下不能简单把 finer coarse-patch current 直接 `ParallelAdd` 到当前 level 的 fine patch，因为 nodal overlap 会双计数；WarpX 为此引入临时 `fine_lev_cp` 和 `OwnerMask` 去重。也就是说，coarse-fine current 同步本身就已经是 AMR 物理一致性的一部分，而不是纯粹 MPI 细节。

guard-cell 宽度由场求解、PML、滤波、particle gather/deposition 和 AMR 同时约束；因此一项输入变更可能改变通信宽度，即使主域更新公式不变。

继续往下看 `Parallelization/WarpXComm.cpp`，会发现 WarpX 对 current / rho 的 coarse-fine 同步并不是简单的“restrict 一下再加回去”。`SyncCurrent()` 的大段注释明确说明：

- finest level 先把 fine-patch current restriction 到同层 coarse patch；
- 若有 current buffer，则 coarse-patch current 先并入 buffer，再把 buffer 当作更粗层的通信源；
- 更粗层接收 finer 数据时，先写到临时 `fine_lev_cp`；
- 由于 nodal 点可能在多个 box 中重叠，不能直接加回 `J_fp`，而要借助 `OwnerMask` 只让 owner box 接管该点数据。

因此，WarpX 的 coarse-fine source 同步真实更接近：

`restriction -> optional buffer merge -> temporary receive -> owner-mask de-dup -> same-level SumBoundary`

而不是单一的 restriction/prolongation 二步法。

rho 路径在 `SyncRho()` 中基本平行，只是 bilinear filter 与 `SumBoundary` 被折叠成 `ApplyFilterandSumBoundaryRho()`。这意味着 J 和 rho 虽然共享 AMR 同步框架，但在 filter 实现上仍有细微差异。

继续顺着 `WarpXRegrid.cpp` 往下读时，问题就不再是“数据如何同步”，而会转成“`DistributionMapping` 改变后，fields、particles、EB、boundary buffer 和 diagnostics 如何整体重建”。这也是为什么 regrid 不能只用末态场图来判断正确性。

`WarpXRegrid.cpp` 的顶层入口是 `WarpX::CheckLoadBalance(step)`。它的读者级控制流可写成：

```text
if step hits load_balance_intervals:
    LoadBalance()
    ResetCosts()
if timing costs are available:
    RescaleCosts(step)
```

这段是控制流摘录，不是可编译源码；它刻意省略类型、花括号和容器细节，只保留“何时触发搬迁”和“何时重标定成本”两件会影响后续解释的事。

源码入口：`Source/Parallelization/WarpXRegrid.cpp`。

这说明 WarpX 的 load balance 不是“到点直接重分布”，而是：

1. 周期性检查当前 step 是否命中 `load_balance_intervals`；
2. 若命中，则执行 `LoadBalance()`；
3. 之后清零 costs；
4. timer 模式下还会继续对 costs 做 running-average 式重标定。

`LoadBalance()` 内部先按 level 构造候选 `DistributionMapping`，支持：

- SFC
- knapsack

然后比较 `currentEfficiency` 和 `proposedEfficiency`，只有满足：

```cpp
proposedEfficiency > load_balance_efficiency_ratio_threshold*currentEfficiency
```

时才真正采纳新映射。源码入口：`Source/Parallelization/WarpXRegrid.cpp`。

因此，WarpX 当前策略更接近“收益足够大才搬”，而不是粗暴地按固定周期强制改 rank 图。

更关键的是 `RemakeLevel()` 的边界。它当前只支持：

- `BoxArray` 不变；
- `DistributionMapping` 改变。

因为函数内部直接写着：

```cpp
if (ba == boxArray(lev)) {
    ...
} else
{
    WARPX_ABORT_WITH_MESSAGE("RemakeLevel: to be implemented");
}
```

源码入口：`Source/Parallelization/WarpXRegrid.cpp`。

这意味着当前这里讨论的还不是“任意 AMR regrid”，而是“同一 patch 拓扑下的 rank 重映射”。

一旦某个 level 真的采纳新映射，WarpX 重建的远不只是粒子容器。`RemakeLevel()` 里会依次重做：

- `m_fields.remake_level(lev, dm)`：field registry 的 level 场数据；
- EB 相关的 `m_eb_reduce_particle_shape`、`m_eb_update_E/B`、ECT `m_borrowing`；
- `m_field_factory[lev]` 与 `InitializeEBGridData(lev)`；
- PSATD 的 fine/coarse spectral solver real-space 容器；
- `m_accelerator_lattice[lev]->InitElementFinder(...)`；
- `current_buffer_masks` / `gather_buffer_masks` 与 `BuildBufferMasks()`；
- `multi_diags->InitializeFieldFunctors(lev)`。

源码入口：`Source/Parallelization/WarpXRegrid.cpp`。

随后若至少有一个 level 完成了 load balance，WarpX 才统一做：

```cpp
mypc->Redistribute();
mypc->defineAllParticleTiles();
m_particle_boundary_buffer->redistribute();
reduced_diags->LoadBalance();
```

源码入口：`Source/Parallelization/WarpXRegrid.cpp`。

因此，WarpX 的 load balance 不是“先搬粒子再说”，而是一次多子系统一致提交：

`candidate DM -> efficiency check -> remake field/EB/solver/masks -> redistribute particles -> redistribute boundary buffer -> refresh diagnostics`

这一阶段的正确性依赖多子系统共同完成迁移；只确认某个 particle count 或 field checksum 保持不变，不能证明 boundary buffer、EB factory 和 diagnostics 的 ownership 也已同步。

### 7.8.1 修改 load balance 或 `RemakeLevel()` 后的验证卡：效率、迁移与物理量分开检查

动态 load balance 要改变的是 **box 的 MPI owner**，不是连续物理模型，也不是网格加密规则。官方参数说明明确：`algo.load_balance_intervals` 命中时，WarpX 尝试重新分配 subdomains；每个 subdomain 本身保持不变。因而首先要把“计划一次重映射”“采纳了新的 `DistributionMapping`”和“迁移后的物理状态仍可解释”分成三层，而不是看到一次性能诊断或末态 checksum 就统称为 load balance 正确。

**第一层：先确认 producer 有足够的 boxes、实际生成成本记录。**官方 `test_3d_reduced_diags_load_balance_costs_{heuristic,timers}` 都是 3D、2-rank case。基础输入设 `amr.n_cell = 128 32 128` 与 `amr.max_grid_size = 32`，所以 level 0 被拆成多个 box；`algo.load_balance_intervals = 2`，并以 overlay 分别选择 heuristic 或 timers 成本。`warpx.reduced_diags_names = LBC`、`LBC.type = LoadBalanceCosts`、`LBC.intervals = 1` 使每步写出 box cost、owner rank、level 和 box 位置。若 box 数不多于 rank，或 `load_balance_intervals = 0`，即使配置了 `LBC`，也不能把静态 rank 布局解释成动态重映射已被检验。

**第二层：用正确的 consumer 判断映射效率。**该 CTest 的 `analysis_reduced_diags_load_balance_costs.py` 从 `LBC.txt` 按 rank 汇总 cost，并定义

$$
\eta = \frac{\operatorname{mean}_r C_r}{\max_r C_r}.
$$

它比较 load-balance step 前后的 \(\eta\)，并断言 `efficiency_before < efficiency_after`。这是一条明确的性能/映射 consumer：它说明这个指定 3D、2-rank、固定 box 拓扑、uniform-plasma 输入下，记录的 cost 分布在该次迁移后更均匀。它不比较 \(E/B\)、\(\rho/J\)、粒子相空间、EB scraping buffer 或解析解，也不能推出 wall-clock 总时间必然下降，更不能推出物理误差减小。

**第三层：把“提议”与“真正迁移的状态”分开。**`CheckLoadBalance()` 只有在步号命中 interval 时才进入 `LoadBalance()`；候选 SFC/knapsack mapping 还必须满足 `proposedEfficiency > threshold * currentEfficiency`，才调用 `RemakeLevel()`。后者当前只接受 **相同 `BoxArray`、不同 `DistributionMapping`**；若 patch 拓扑改变会直接拒绝。因此本节说的不是任意 AMR regrid。映射被采纳后，源码重建 field registry、EB factory、PSATD real-space 容器、buffer masks 和 field diagnostic functors；随后才 `Redistribute()` 粒子和 particle boundary buffer，并刷新 reduced diagnostics。普通 full diagnostics 没有在这一处调用 `multi_diags->LoadBalance()`，所以修改 diagnostics 或其 writer 时不能假定性能 consumer 已经检查了所有诊断 ownership。

**第四层：按改动对象补上状态或物理 consumer。**只改 interval、cost model、SFC/knapsack 或效率阈值时，先保留 `LBC` 的 pre/post \(\eta\) 与 mapping 记录；改 `RemakeLevel()` 中的 fields、EB、PSATD、buffer mask、粒子或 boundary-buffer 迁移时，应在一个确实采纳 mapping 的 case 中，对迁移前后同一物理时间的 Full field/particle state、必要的 scraping buffer 和 reduced diagnostic 输出做独立比较；改 coarse-fine topology、regrid tagging 或 transition-zone 时，则回到 7.9 的 route ledger，而不是复用本卡。最终 checksum 只可作为指定输出的回归补充。没有“映射被采纳 + 对应状态比较 + 与问题匹配的 observable”三项，就只能说 producer 或性能分支被检查，不能写成“load balance 后的物理结果已经验证”。

## 7.9 AMR transition zone：为什么最终 plotfile 不足以证明路由正确

AMR 的 transition zone 同时影响 gather 和 deposition。粒子在细网格 interior 时从 `E/Bfield_aux` gather 并向 `rho_fp/current_fp` deposition；进入 buffer 后，gather 和 deposition 可以分别切换到 coarse `E/Bfield_cax` 与 `rho_buf/current_buf`。这两个分界不必相同，因此“场看起来正常”不能证明粒子经过了正确的 coarse/fine route。

`PartitionParticlesInBuffers()` 是理解这条路径的关键入口。它在一个 tile 内给出 `nfine_gather` 与 `nfine_deposit`，随后同步阶段才会把 buffer 与 coarse/fine 数据合并。因而强验证需要在分区之后、同步之前观察 route counts 或中间账本；只读取最终 plotfile，只能给出间接证据。

| 证据层 | 能说明什么 | 仍不能说明什么 |
|---|---|---|
| 源码路径 | buffer mask、`nfine_gather/nfine_deposit`、`aux/cax/fp/buf` 和同步入口存在且相互对应 | 每个 route 在真实 case 中都被独立命中 |
| 现有 MR case | subcycling、moving window、PML 或解析场 consumer 可验证整体运行完整性 | `fine/coarse gather/deposit` 的逐粒子分区 |
| route-count schema | 专用 diagnostic 应检查 count、weight、`rho/J` 与 post-sync closure | WarpX 已经输出这些数据 |
| runtime activation | 已有 AMR workflow 确实调用了 partition/sync 分支 | 没有 route id、pre-sync buffer 或 owner-mask 数值账本 |

因此，本章对 transition zone 的准确结论是：源码路径已核、整体 MR workflow 有运行证据、专用 route ledger 仍未实现。不要把末态 checksum、解析场误差或 profiling marker 写成 branch-level route proof。

### 7.9.1 Transition-zone 判读卡：分支被进入，不等于每条 route 已验证

transition zone 的难点不在于给粒子贴上“fine”或“coarse”一个标签，而在于 **gather 与 deposition 分别有自己的 buffer mask**。因此读者应把一次 AMR 粒子步骤写成两个独立判断：粒子从哪一组场数组 gather，以及它向哪一组 source 数组 deposition。没有在同步之前留下记录时，最终的场或 `rho/J` 不能倒推出这两个判断曾如何发生。

1. **先在分区点定义账本，而不是在 plotfile 末态猜路由。** 对每个 step、level 和 species，先记录 `np_before_partition`、总权重、`nfine_gather` 与 `nfine_deposit`，并显式给出两个补数 `nbuffer_gather = np_before_partition - nfine_gather`、`nbuffer_deposit = np_before_partition - nfine_deposit`。这四个数首先只检验分区记账是否完整；它们不是电荷守恒或场正确性的替代品。

2. **再把两个计数接回不同的 producer。** fine gather 消费 `E/Bfield_aux`，buffer gather 消费 coarse `E/Bfield_cax`；fine deposition 写入 `rho_fp/current_fp`，buffer deposition 写入 `rho_buf/current_buf`。同一个粒子在这两条判断上可能有不同标签，因此 ledger 不应只报告一个“buffer particle count”。读者需要能看出每个步骤是否出现 fine-gather/fine-deposit、fine-gather/buffer-deposit、buffer-gather/fine-deposit 或 buffer-gather/buffer-deposit 这四类标签；未命中的标签必须如实报告为未覆盖。

3. **把同步前后的 source 分开保存。** 在 `SyncCurrent()` / `SyncRho()` 前，分别记录 `rho_fp`、`rho_buf`、`current_fp`、`current_buf` 的相应积分或逐分量范数；随后记录 coarsened fine contribution、buffer merge、`OwnerMask()` 去重和 post-sync source。这里不能只做一次总和比较，因为多个 box 的 nodal overlap 正是 `OwnerMask()` 存在的原因。

4. **正确解释已有 runtime marker。** 一个二层、2-rank、subcycling 的 AMR producer 已记录 `PartitionParticlesInBuffers` 与 `OwnerMask()` 的运行标记，因而可以说分区和同步分支被实际经过。它没有给出粒子 route ID、四类 route 的 count/weight、pre-sync buffer 数值或逐项 post-sync ledger，所以不能写成“transition zone 已验证”或“所有 route 都通过”。

5. **用受控情形关闭 route 级结论。** 专用测试应让粒子初态和 buffer 宽度有意覆盖需要的标签，逐 step 输出上述记录，并用独立的 source 或场 observable 检查同步后的结果。只有“预期 route 被命中 + 分区计数/权重自洽 + pre/post-sync source 可追踪 + 独立 observable 通过”同时成立，才可把一条具体 route 标为已验证。

这张卡给出的是正确的证据顺序：**源码分派说明哪些 route 可以存在，runtime marker 说明相关分支曾被进入，route ledger 才说明每条 route 在受控条件下怎样贡献到同步后的 source。** 三者不能互相代替。

## 7.10 本章练习与源码定位

1. **边界分派题**：给定一个 field boundary 和一个 particle boundary，分别沿 `parse_field_boundaries()`、`parse_particle_boundaries()` 定位它们如何进入 solver/particle container；说明 periodic 继承为什么不能只看输入字符串。
2. **PML 证据题**：对照 `pml/analysis_pml_yee.py`、`analysis_pml_psatd.py` 和 RZ analysis，区分反射率强判据、末态 residual 判据和 checksum-only 证据。
3. **AMR route 题**：阅读 `BuildBufferMasks()` 与 `PartitionParticlesInBuffers()`，画出一个粒子分别进入 fine gather、coarse gather、fine deposit 和 coarse deposit 的条件；说明为什么当前没有 dedicated route-count regression 时不能声称每条 route 已被单独验证。

## 7.11 本章结论

边界问题的正确读法不是先问“这个边界有没有打开”，而是顺序确认下列四件事：

1. **拓扑是否一致。**field 与 particle 的 periodicity 必须沿同一坐标轴成对闭合；PEC、PMC、Silver-Mueller 和 embedded boundary 则对应不同的场或几何条件，不能用同一组输入语义代替。
2. **离散更新是否在边界闭合。**PML 的 split fields、guard-cell 交换、rho/J 镜像或清零，以及粒子反射、吸收和 scraping 分属不同路径。需要分别知道哪一个数组在何时更新，而不能只观察最终粒子数或一个场快照。
3. **AMR 状态是否共同迁移。**regrid 或 load balance 会同时影响 fields、粒子、buffer masks、PML/solver 容器和 diagnostics。coarse/fine 的 gather 与 deposition 也可在不同条件下切换，因此一个平滑的末态场不是 route 正确性的充分证据。
4. **观察量是否匹配问题。**PML 可用反射率或残余场，边界粒子可用 scraping buffer，重启可用输出重复性，AMR transition zone 则需要分区后的 route count、weight、`rho/J` buffer、coarsened-fine 与 owner-mask 的共同账本。checksum 只能补充这些判据，不能替代它们。

这四层构成本章与前后章节的连接：第 5、6 章决定沉积 source 和 Maxwell 更新如何生成，第 7 章检查这些量如何穿过边界、通信和网格层级，第 8 章再选择诊断把结果转化为可解释的证据。当前 AMR case 可以支持整体 workflow 已经走通，但仍不能把它写成 transition zone 的逐 route 验证；在 `PartitionParticlesInBuffers()` 之后没有对应账本之前，这个边界必须保留。
