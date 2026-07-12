# 43 Villasenor entrypoints and shared segment kernel：显式/隐式的差别在端点恢复，不在 segment 数学

绑定源码：

- `../warpx/Source/Particles/Deposition/CurrentDeposition.H`

前置阅读：

- `../notes/code-reading/particles/32-current-deposition-continuity-and-geometry-boundaries.md`
- `../notes/code-reading/particles/42-villasenor-segment-loop-and-esirkepov-contrast.md`

第 5 章已经讲到：

- Villasenor 的核心是 crossing-driven segment loop；
- explicit/implicit 的第一层差别是时间层恢复。

这一条笔记只把两件事压实：`doVillasenorDepositionShapeNExplicit(...)` 和 `doVillasenorDepositionShapeNImplicit(...)` 到底各自负责什么，以及它们怎样汇入同一个 `VillasenorDepositionShapeNKernel(...)`。

## 1. explicit 入口只做三件事：算 `gaminv`、回推端点、转交共同 kernel

显式入口的主体很短：

```cpp
const amrex::Real gaminv = 1.0_rt/std::sqrt(...);
...
amrex::Real const xp_new = xp + (relative_time + 0.5_rt*dt)*uxp[ip]*gaminv;
amrex::Real const xp_old = xp_new - dt*uxp[ip]*gaminv;
...
VillasenorDepositionShapeNKernel<depos_order>(xp_old, ..., xp_new, ..., wq,
                                              uxp[ip], uyp[ip], uzp[ip], gaminv,
                                              ...);
```

源码位置：`../warpx/Source/Particles/Deposition/CurrentDeposition.H:2218-2250`。

这说明 explicit 入口自己并不做 segment loop，也不做 cell/node 权重构造。它只负责：

1. 用当前 `u_{n+1/2}` 恢复 `gaminv`；
2. 用 `relative_time` 和 `dt` 回推出 `x_old -> x_new`；
3. 把端点、速度和 `gaminv` 交给共同 kernel。

## 2. implicit 入口同样不改 segment 数学，只改端点恢复链

隐式入口的主体是：

```cpp
const amrex::ParticleReal gaminv = GetImplicitGammaInverse(...);
...
const amrex::ParticleReal xp_np1 = 2._prt*xp_nph - xp_n;
...
VillasenorDepositionShapeNKernel<depos_order>(xp_n, ..., xp_np1, ..., wq,
                                              uxp_nph[ip], uyp_nph[ip], uzp_nph[ip], gaminv,
                                              ...);
```

源码位置：`../warpx/Source/Particles/Deposition/CurrentDeposition.H:2323-2354`。

也就是说，implicit 入口真正改写的只有：

- `gaminv` 的来源：不再直接用 `u_{n+1/2}`，而是由 `u_n` 和 `u_{n+1/2}` 共恢复；
- 轨迹端点：不再用 `relative_time` 回推，而是从 `x_n` 和 `x_{n+1/2}` 恢复 `x_{n+1}`。

但一旦端点恢复完成，后面的 segment kernel 和 explicit 完全相同。

## 3. 两条入口都把同一组“共享合同”传给共同 kernel

不管 explicit 还是 implicit，最后传给 `VillasenorDepositionShapeNKernel(...)` 的关键合同都相同：

- old/new 轨迹端点
- `wq`
- 一组中间时间层动量 `uxp_mid/uyp_mid/uzp_mid`
- `gaminv`
- `dt/dinv/xyzmin`
- `domain_double/do_cropping`
- `lo/invvol`

因此，对共同 kernel 来说：

- 它不关心这些端点是怎么恢复出来的；
- 它只消费“已经恢复好的整条轨迹”和“可以裁剪的边界语义”。

这也是为什么正文里最稳妥的说法应该是：

- explicit/implicit Villasenor 不是两套 segment 算法；
- 而是两个不同的 endpoint-reconstruction front-end，共享同一个 segment-deposition back-end。

## 4. 这和 Esirkepov implicit 的接口位置正好形成对照

Esirkepov implicit 同样也是“先恢复整条轨迹，再交给守恒沉积”，但它交给的是 old/new shape-difference 累加结构。Villasenor 则交给 crossing-driven segment loop。

因此：

- explicit/implicit 这条分界，回答的是“轨迹端点怎么恢复”；
- Esirkepov/Villasenor 这条分界，回答的是“恢复出来的轨迹怎样被压成守恒电流”。

这两层边界不能混写。

## 5. 对第 5 章最值得带走的结论

1. `doVillasenorDepositionShapeNExplicit(...)`
   - 不是一套完整沉积算法；
   - 它只是显式时间层下的端点恢复前端。

2. `doVillasenorDepositionShapeNImplicit(...)`
   - 也不是另一套 segment 公式；
   - 它只是隐式时间层下的端点恢复前端。

3. 两者真正共享的是
   - `VillasenorDepositionShapeNKernel(...)`
   - 也就是 crossing 统计、segment 终点推进、cell/node 权重构造和局部 `this_J*` 写回这一整套共同后端。
