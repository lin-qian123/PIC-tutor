# `UpdateMomentumPerezElastic`、`BremsstrahlungEvent` 与 `SingleNuclearFusionEvent`

绑定源码：

- `../warpx/Source/Particles/Collision/BinaryCollision/Coulomb/UpdateMomentumPerezElastic.H`
- `../warpx/Source/Particles/Collision/BinaryCollision/Bremsstrahlung/BremsstrahlungFunc.H`
- `../warpx/Source/Particles/Collision/BinaryCollision/Bremsstrahlung/BremsstrahlungFunc.cpp`
- `../warpx/Source/Particles/Collision/BinaryCollision/NuclearFusion/SingleNuclearFusionEvent.H`

对应 regression：

- `../warpx/Examples/Tests/collision/analysis_collision_2d.py`
- `../warpx/Examples/Tests/collision/analysis_collision_3d.py`
- `../warpx/Examples/Tests/collision/analysis_collision_3d_isotropization.py`
- `../warpx/Examples/Tests/collision/analysis_collision_rz.py`
- `../warpx/Examples/Physics_applications/capacitive_discharge/analysis_1d.py`

这一篇补的是前两篇 collision 笔记之后还没落成文档的三层细节：

1. Perez 弹性散射怎样把 `s12` 变成具体散射角分布
2. `BremsstrahlungEvent(...)` 怎样从截面表抽样 photon 能量，并决定 event probability
3. `SingleNuclearFusionEvent.H` 怎样做 probability 裁剪、multiplier 回退和 product weight 缩放

同时把剩余的 2D/3D/isotropization/RZ Coulomb regression，以及 `background_mcc` 的 capacitive-discharge checksum 边界压实。

---

## 1. `UpdateMomentumPerezElastic`：`s12` 不是直接当概率，而是先进入分段散射角模型

`ElasticCollisionPerez(...)` 的上游已经在上一篇里补过：

- 局域 Debye length / atomic spacing
- `bmax`
- `sigma_max`
- 加权后的 `n12`

真正把这些量变成一次二体散射的，是：

```cpp
UpdateMomentumPerezElastic(...)
```

### 1.1 先变到 COM frame，再用 `sigma_eff * n12 * dt` 得到 `s12`

这个 kernel 的总结构是：

1. 用两粒子的 `u = gamma v` 先求 lab-frame `gamma`
2. 变到 center-of-momentum frame
3. 在 COM frame 里构造
   - `muRst`
   - `vrelst`
   - `vrelst_invar`
4. 再由
   $$
   \sigma_{\mathrm{eff}} = \min\left(\pi b_0^2 \ln\Lambda,\ \sigma_{\max}\right)
   $$
   和
   $$
   s_{12} = \sigma_{\mathrm{eff}}\, n_{12}\, dt\,
   v_{\mathrm{rel}}^\ast \frac{\gamma_1^\ast \gamma_2^\ast}{\gamma_1 \gamma_2}
   $$
   得到归一化散射长度 `s12`

这里 `s12` 的角色不是“这对粒子是否碰撞”的 Bernoulli 概率，而是 Perez/Nanbu 散射模型里的连续强度参数。后面的角分布完全由 `s12` 所处区间决定。

### 1.2 散射角是四段式近似，不是一套统一公式

源码把 `cosXs` 的抽样分成四段：

- `s12 <= 0.1`
  - 用
    $$
    \cos\chi_s = 1 + s_{12}\ln r
    $$
  - 并在 `cosXs < -1` 时重抽随机数
- `0.1 < s12 <= 3`
  - 用五次多项式近似给出 `Ainv`
  - 再对双曲正弦形式做反演
- `3 < s12 <= 6`
  - 改用
    $$
    A = 3 e^{-s_{12}}
    $$
  - 再做另一段对数反演
- `s12 > 6`
  - 直接退化成
    $$
    \cos\chi_s = 2r - 1
    $$
    即各向同性散射

所以当前 WarpX 的 Perez kernel 不是“先算一个小角度散射，再加修正”，而是明确的四段 piecewise model。

### 1.3 最后不是无条件同时更新两粒子，而是按宏粒子权重做 rejection

COM frame 里抽完极角和方位角后，kernel 会：

1. 构造 post-collision `p1fs/p2fs`
2. Lorentz 变回 lab frame 得到 `p1f/p2f`
3. 再用两次 rejection：

```cpp
if (w2 > r * max(w1, w2)) update particle 1
if (w1 > r * max(w1, w2)) update particle 2
```

这意味着 weighted macroparticle Coulomb collision 的最终语义不是“这一对粒子总是同时改动”，而是：

- 事件强度由 `n12` 和 `s12` 决定
- 但 reactant 的真正写回仍按 `w1/w2` 做随机接受

这也解释了为什么 2D/3D/RZ Coulomb regressions 的检查量更接近统计 relaxation，而不是逐粒子轨迹对照。

---

## 2. `BremsstrahlungEvent(...)`：先做等离子体频率 cutoff，再从表驱动能谱里反演 photon 能量

前一篇已经补过：

- `BremsstrahlungFunc` 前半段只给 `p_mask`
- `p_pair_reaction_weight`
- `p_product_data = Ephoton`

这里再往下看，会发现 event kernel 本身已经做了三层采样：

1. 是否允许这个 electron energy 产生可逃逸 photon
2. 总截面有多大
3. 若事件发生，photon 能量落在哪个 `k/T1` 区间

### 2.1 截面不是单参数函数，而是 `KE_eV + wpe cutoff + Z-table` 的组合

构造期 `BremsstrahlungFunc.cpp` 会：

- 读入 target `Z`
- 调 `UploadCrossSection(Z)`
- 把 Seltzer-Berger 的 energy-weighted differential cross section 表传到 device

运行时 `BremsstrahlungEvent(...)` 先：

1. 把 electron 变到 ion rest frame
2. 计算 electron kinetic energy `KE_eV`
3. 用电子密度 `n1` 构造
   $$
   \omega_{pe}
   $$
4. 再把 cutoff photon energy 设成
   $$
   E_{\mathrm{cut}} = \hbar \omega_{pe}
   $$

如果 `KE_eV < E_cut`，`CalculateCrossSection(...)` 直接返回 0。也就是说，当前实现明确把低于 plasma-frequency cutoff 的软光子全部裁掉，不让它们进入 event sampling。

### 2.2 photon 能量不是查最近点，而是对累计截面做逐段反演

`CalculateCrossSection(...)` 先得到：

- electron-energy 方向的插值权重 `w0`
- photon-energy cutoff 所在的 `i0_cut`
- 截止点的 `k dsigma/dk`
- 整体 `sigma_total`

然后 `Photon_energy(...)` 会在 `koT1` 网格上逐段累积 trapezoidal integral，直到：

$$
r \sigma_{\mathrm{total}}
$$

落进当前区间，再在该区间内对线性近似的 `dsigma/dk` 做局部反演，解出实际的 `k/T1`。因此 `p_product_data[pair_index]` 存进去的 `Ephoton` 不是离散表点，而是表积分下的一次连续抽样结果。

### 2.3 `arg > 1` 时当前实现是 probability saturation，不是真正的 multiplier 回退

event probability 的核心量是：

$$
\mathrm{arg}
=
f_{\mathrm{multi}}\, v_1\, \sigma_{\mathrm{total}}\, n_2\, dt\,
\frac{\gamma_1^{\mathrm{rel}}}{\gamma_1 \gamma_2}
$$

代码随后做：

```cpp
if (arg > 1) {
    arg = 1;
    fmulti = fmulti / arg;
    if (fmulti < 1) fmulti = 1;
}
q12 = arg;
```

按当前实现，这一分支的直接效果是：

- `q12` 被饱和到 1
- 但 `arg` 被先改成 1 以后，后面的 `fmulti = fmulti / arg` 不再真正缩小 multiplier

所以这一段当前更准确的描述应当是：

- 已实现 event-probability saturation
- 但没有像 `SingleNuclearFusionEvent.H` 那样形成真正有效的 multiplier backoff

这应被记录为当前源码边界，而不是误写成“Bremsstrahlung 已实现高概率下的 multiplier 自适应回退”。

---

## 3. `SingleNuclearFusionEvent.H`：先估算 probability，再按 threshold 回退 multiplier，再用 `expm1` 得到真实事件率

这一层和 bremsstrahlung 最大的不同是：fusion 这里明确实现了 event-probability control，而不是只做简单饱和。

### 3.1 `probability_estimate` 先带着 `fusion_multiplier` 和 unsampled-pair 修正计算

event kernel 先通过：

```cpp
BinaryCollisionUtils::get_collision_parameters(...)
```

得到：

- `E_coll`
- `v_coll`
- `lab_to_COM_factor`

再从对应截面模型取：

- `BoschHaleFusionCrossSection(...)`
- 或 `ProtonBoronFusionCrossSection(...)`

第一版估计概率是：

$$
P_{\mathrm{est}}
=
\mathrm{multiplier\_ratio}\,
f_{\mathrm{mult}}\,
\mathrm{lab\_to\_COM\_factor}\,
w_{\max}\,
\sigma_f(E_{\mathrm{coll}})\,
v_{\mathrm{coll}}\,
\frac{dt}{dV}
$$

其中：

- `multiplier_ratio` 负责补偿未抽样到的 pairs
- `fusion_multiplier` 负责故意放大事件数、减小单个 product 权重

### 3.2 超过阈值时，fusion 真正会把 multiplier 往回收

若：

$$
P_{\mathrm{est}} > \texttt{probability_threshold}
$$

源码会设置：

$$
f_{\mathrm{mult,eff}}
=
\max\left(
f_{\mathrm{mult}}\,
\frac{\texttt{probability\_target\_value}}{P_{\mathrm{est}}},
1
\right)
$$

并把 `probability_estimate` 同步乘上

$$
\frac{f_{\mathrm{mult,eff}}}{f_{\mathrm{mult}}}.
$$

这和 bremsstrahlung 的当前实现边界不同：在 fusion 里，threshold/target-value 这套参数确实参与了有效倍率回退，而不是只停留在接口层。

### 3.3 真正事件概率用的是 `-expm1(-x)`，不是线性近似

最终事件概率不是直接把估计值截到 `[0,1]`，而是：

$$
P = 1 - e^{-P_{\mathrm{est}}}
$$

代码实现写成：

```cpp
const probability = -std::expm1(-probability_estimate);
```

这样在 `probability_estimate` 很小时不会因为浮点消减而错误回零。只有抽到 `random_number < probability` 时：

- `p_mask[pair_index] = true`
- `p_pair_reaction_weight[pair_index] = w_min / fusion_multiplier_eff`

所以 fusion 的 product weight 语义也清楚了：

- 事件数可以被 multiplier 放大
- 但单个 product 的权重要按 `fusion_multiplier_eff` 反缩小

---

## 4. 剩余 2D/3D/RZ Coulomb regression 的真实断言口径

这轮还补掉了前面回归索引里几条一直停留在“待读取输入文件”的 collision analysis。

### 4.1 `analysis_collision_2d.py`

对应输入是：

- `inputs_test_2d_collision_xz`
- `inputs_test_2d_collision_xz_picmi.py`
- `inputs_test_2d_collision_xz_global_debye`

它检查的是 electron-ion 温度松弛过程中：

- `vxe - vxi` 的时间序列
- 与预先拟合好的
  $$
  a e^{b j}
  $$
  的平均偏差

并顺手复用同一份最后时刻 plotfile 去检查：

- parser particle filter
- uniform filter
- random filter

所以它的真实回归口径是：

- 2D Coulomb relaxation benchmark
- 加上 Full diagnostics 粒子过滤合同

### 4.2 `analysis_collision_3d.py`

3D 版检查的物理量和 2D 类似，也是：

- electron / ion 平均 `p_x`
- 转成 `vxe - vxi`
- 对照一条预拟合的指数衰减曲线

区别在于输入：

- `inputs_test_3d_collision_xyz`

显式打开了：

- `collision{1,2,3}.ndt_supercycle = 10`

因此这条 regression 不是泛泛的“3D Coulomb test”，而是在覆盖：

- 3D pairing 几何
- `ndt_supercycle` 降低碰撞调用频率后的 relaxation 合同
- 外加 3D particle filter diagnostics

### 4.3 `analysis_collision_3d_isotropization.py`

对应：

- `inputs_test_3d_collision_iso`
- `inputs_test_3d_collision_iso_subcycle`

这里不再看 electron-ion 温度松弛，而是单电子 species 的各向异性温度各向同性化：

- 初态 `T_par != T_per`
- 分析脚本按解析系数 `mu` 迭代 100 步
- 最后检查 `Tx, Ty` 与解析结果的相对误差

`inputs_test_3d_collision_iso_subcycle` 进一步把：

- PIC timestep 放大 10 倍
- `collision1.ndt_subcycle = 10`

以保持同一个 collision timestep。因此这对 regression 真正验证的是：

- Perez kernel 的 isotropization 速率
- `ndt_subcycle` 对 collision time resolution 的合同

### 4.4 `analysis_collision_rz.py`

对应：

- `inputs_test_rz_collision`

这个输入的构造很刻意：

- 只有 electron species
- `do_not_push = 1`
- 初始动量是纯径向解析函数
- RZ 几何、`field` 不推进

分析脚本只比较 step 0 和 step 150 的：

- `particle_momentum_x`
- `particle_momentum_y`

最大差值是否接近 0。

所以它验证的不是普通 relaxation，而是更窄的一条几何合同：

- 在 RZ 的 cylindrical-cell 配对和临时动量旋转假设下
- 若所有粒子局域上共线同向，碰撞率应极低，宏观动量分布基本不变

---

## 5. `background_mcc` 当前在回归索引里的正确位置

`capacitive_discharge` 里的：

- `inputs_test_2d_background_mcc`
- `inputs_test_2d_background_mcc_picmi.py`
- 对应 checksum `test_2d_background_mcc*.json`

不应再写成“Monte Carlo collisions，需反查”。

当前源码树里它们的更准确位置是：

- 应用级 `capacitive discharge / PIC-MCC`
- 2D native input 和 2D PICMI input 都没有独立 analysis
- 主要依赖 checksum
- `test_2d_background_mcc_dp_psp` 当前整条 `add_warpx_test(...)` 仍在 `CMakeLists.txt` 中被注释掉，只能按遗留 checksum 名记录

只有：

- `test_1d_background_mcc_picmi`
- `test_1d_dsmc_picmi`

这两条 1D PICMI 入口带了：

- `analysis_1d.py`
- `analysis_dsmc.py`

它们都直接把最终 `ion_density_case_1.npy` 和内置的 case-1 reference density profile 做 `allclose`，本质上是在验证：

- PICMI 接口
- specialized external Poisson solver callback
- `background_mcc`
- 以及可切换进同一骨架里的 DSMC 变体
- 对 Turner benchmark case 1 的离子密度 profile 重建

因此 `background_mcc` 当前在索引里的正确写法应是：

- 1D PICMI `background_mcc` / `dsmc`：有 case-1 profile-level analysis
- 2D native / PICMI：应用级 checksum baseline
- `dp_psp`：当前是被注释掉的遗留 benchmark 名，不应再冒充活跃 test

---

## 6. 这一轮补出的结构结论

到这里，`Particles/Collision` 当前又补齐了一层关键空白：

1. Perez kernel
   - `s12` 进入四段式散射角模型
   - reactant 写回按宏粒子权重 rejection 完成
2. Bremsstrahlung event
   - 先做 plasma-frequency photon cutoff
   - 再从 differential cross-section table 反演 photon energy
   - 当前只有 probability saturation，没有真正有效的 multiplier backoff
3. Fusion event
   - `probability_threshold / probability_target_value` 确实会回退有效 multiplier
   - 真实事件率用 `-expm1(-x)` 保持小概率数值稳定
4. Regression map
   - 2D/3D 看 relaxation exponential fit
   - 3D isotropization 看解析各向同性化
   - RZ 看 cylindrical-cell 几何假设下的近零碰撞效应
   - background-MCC 要区分 1D PICMI analysis 和 2D 应用级 checksum
