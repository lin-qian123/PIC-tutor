# 37 direct vs Villasenor boundary cropping and suborbit：为什么 near-boundary/implicit 不能退回 direct deposition

绑定源码：

- `../warpx/Source/Particles/WarpXParticleContainer.cpp`
- `../warpx/Source/Particles/Deposition/CurrentDeposition.H`
- `../warpx/Source/Particles/Pusher/ImplicitPushPX.cpp`

前置阅读：

- `../notes/code-reading/particles/05-current-deposition-algorithms-near-amr-buffer.md`
- `../notes/code-reading/particles/32-current-deposition-continuity-and-geometry-boundaries.md`

这一条笔记只追一个更窄的问题：第 5 章已经说明了 direct 不守恒、Villasenor 按 cell crossing 分段，但这还不足以解释为什么 WarpX 在 near-boundary、implicit gather/deposition 耦合、suborbit fallback 这些场景里不能简单退回 direct deposition。源码里真正决定这件事的，不只是“守恒或不守恒”，而是两条接口合同根本不同。

## 1. `DepositCurrent()` 在调用层就把两类接口分开了

`WarpXParticleContainer.cpp` 先统一构造：

- `domain_double`
- `do_cropping`

它们来自：

- `particles.crop_on_PEC_boundary`
- 当前 tile 是否贴着 `PEC / PECInsulator` 物理边界

源码位置：`../warpx/Source/Particles/WarpXParticleContainer.cpp:530-544`。

但这些几何/边界信息并不会传给所有算法。当前 dispatch 很明确：

- `Esirkepov implicit/explicit`：接收 `domain_double, do_cropping`
- `Villasenor implicit/explicit`：接收 `domain_double, do_cropping`
- `Direct explicit/implicit`：只接收 `relative_time` 或 `u_n/u_{n+1/2}`、`dinv`、`xyzmin`
- `Vay`：同样不接收 `domain_double, do_cropping`

对应调用点见：

- `../warpx/Source/Particles/WarpXParticleContainer.cpp:724-748`
- `../warpx/Source/Particles/WarpXParticleContainer.cpp:776-833`
- `../warpx/Source/Particles/WarpXParticleContainer.cpp:836-862`
- `../warpx/Source/Particles/WarpXParticleContainer.cpp:865-900`

这意味着上层虽然统一知道“此 tile 上哪些边界需要 crop”，但只有 charge-conserving 路径真正把这份边界语义带进 kernel。

## 2. direct deposition 的时间层只回到一个沉积点，不恢复一条可裁剪轨迹

direct kernel 的核心接口是：

```cpp
void doDepositionShapeNKernel(...,
                              const amrex::Real relative_time,
                              ...);
```

它只根据当前位置和 `relative_time` 构造一个沉积点：

```cpp
const double xmid = ((xp - xyzmin.x) + relative_time*vx)*dinv.x;
```

源码位置：`../warpx/Source/Particles/Deposition/CurrentDeposition.H:47-111`。

implicit direct 也没有改变这层合同。它只是把 `gaminv` 改成由 `u_n` 与 `u_{n+1/2}` 恢复，再把

```cpp
const amrex::Real relative_time = 0._rt;
```

喂回同一个 direct kernel。源码位置：`../warpx/Source/Particles/Deposition/CurrentDeposition.H:363-441`。

所以 direct 路径的真实语义是：

1. 确定一个时间层上的粒子速度；
2. 选一个与该时间层对应的沉积位置；
3. 把 \(qwv/\Delta V\) 按 staggering shape 直接原子加回去。

它并不会显式恢复 `x_old -> x_new` 的完整段，更没有 `crop_at_boundary(...)`、cell crossing、segment factor 之类的对象。

## 3. Villasenor kernel 则把“完整轨迹 + boundary crop + crossing segmentation”写进了接口

`VillasenorDepositionShapeNKernel` 的参数里直接有：

- `xp_old, yp_old, zp_old`
- `xp_new, yp_new, zp_new`
- `domain_double`
- `do_cropping`

源码位置：`../warpx/Source/Particles/Deposition/CurrentDeposition.H:1499-1518`。

进入 kernel 后，第一层几何动作就是边界裁剪：

```cpp
ParticleUtils::crop_at_boundary(..., domain_double[...], do_cropping[...]);
```

源码位置：`../warpx/Source/Particles/Deposition/CurrentDeposition.H:1612-1625`。

随后才会：

1. 计算 `dxp/dyp/dzp`
2. 统计各方向 `cell_crossings`
3. 得到 `num_segments`
4. 逐 segment 恢复 `x0_old -> x0_new`
5. 对每一段分别计算 segment-local cell/node weights

源码位置：`../warpx/Source/Particles/Deposition/CurrentDeposition.H:1629-1775`。

也就是说，Villasenor 的“tighter stencil”并不只是数学品味差异，而是它真的把粒子轨迹当成一条可被边界截断、可被 crossing 拆段、并逐段输运电荷的对象。

## 4. explicit/implicit Villasenor 共享同一个 segment kernel，差别只在端点怎么恢复

显式入口：

```cpp
xp_new = xp + (relative_time + 0.5_rt*dt)*uxp[ip]*gaminv;
xp_old = xp_new - dt*uxp[ip]*gaminv;
```

源码位置：`../warpx/Source/Particles/Deposition/CurrentDeposition.H:2236-2241`。

隐式入口：

```cpp
const amrex::ParticleReal xp_np1 = 2._prt*xp_nph - xp_n;
```

源码位置：`../warpx/Source/Particles/Deposition/CurrentDeposition.H:2344-2350`。

但两条入口最后都会落到同一个：

```cpp
VillasenorDepositionShapeNKernel<depos_order>(...)
```

因此对 Villasenor 来说：

- `explicit/implicit` 改写的是端点恢复方式；
- `boundary crop + cell-crossing segmentation` 是两条路径都共享的核心合同。

## 5. 这正是 implicit suborbit 为什么强制改成 Villasenor 的原因

`ImplicitPushPX.cpp` 对 unconverged particles 的 suborbit fallback 直接写死：

```cpp
// Suborbit uses Villasenor current deposition only. For energy conservation,
// the push must use the matching gather, so we override depos_type here to
// Villasenor (instead of the runtime-selected type).
const auto depos_type = CurrentDepositionAlgo::Villasenor;
```

源码位置：`../warpx/Source/Particles/Pusher/ImplicitPushPX.cpp:735-738`。

这段注释说明 current deposition 的选择在这里不是“实现还没补齐”的偶然，而是一个耦合合同：

1. suborbit 需要 energy-conserving gather
2. 该 gather 需要与 Villasenor-compatible deposition stencil 配套
3. near-boundary / cropped orbit 时还要保留那条 segment-based trajectory contract

direct deposition 缺的不是一个 if 分支，而是整套：

- 可裁剪轨迹
- cell-crossing segment loop
- 与 Villasenor-compatible gather 对齐的离散几何

所以这里不能简单地“继续用 runtime-selected deposition，再补个 crop”。

## 6. 对第 5 章最重要的结论

第 5 章如果只写：

- direct 不守恒
- Villasenor 守恒

还不够。当前源码表明，二者还承担着不同的边界/轨迹语义：

1. **direct**
   - 在一个时间中心位置上沉积 \(qwv/\Delta V\)
   - explicit/implicit 只改变速度与时间层恢复
   - 不显式接收 `domain_double/do_cropping`
   - 不把轨迹视为可裁剪、可分段的对象

2. **Villasenor**
   - 以 `x_old -> x_new` 的完整轨迹为输入
   - kernel 内部直接做 `crop_at_boundary(...)`
   - 通过 cell crossing 把轨迹拆成多个局部 segment
   - 与 implicit/suborbit 的 matching gather 一起形成 near-boundary 的 energy-conserving 合同

因此，WarpX 里 direct 不是 Villasenor 的“简化版实现”，而是另一条物理和几何语义都更窄的 deposition 路线。也正因为如此，涉及 `particles.crop_on_PEC_boundary`、implicit suborbit、matching gather 或 boundary-local charge conservation 的地方，源码宁可强制退回 Villasenor，也不会让 direct 去充当一个近似替身。
