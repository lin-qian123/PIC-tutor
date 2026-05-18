# `ElasticCollisionPerez`、Bremsstrahlung photon 初始化与 fusion product 动量初始化

绑定源码：

- `../warpx/Source/Particles/Collision/BinaryCollision/Coulomb/ElasticCollisionPerez.H`
- `../warpx/Source/Particles/Collision/BinaryCollision/Coulomb/UpdateMomentumPerezElastic.H`
- `../warpx/Source/Particles/Collision/BinaryCollision/Bremsstrahlung/PhotonCreationFunc.H`
- `../warpx/Source/Particles/Collision/BinaryCollision/NuclearFusion/TwoProductFusionInitializeMomentum.H`
- `../warpx/Source/Particles/Collision/BinaryCollision/NuclearFusion/ProtonBoronFusionInitializeMomentum.H`

对应 regression：

- `../warpx/Examples/Tests/collision/analysis_collision_1d.py`
- `../warpx/Examples/Tests/collision/analysis_collision_1d_correct_conservation.py`
- `../warpx/Examples/Tests/collision/analysis_collision_1d_Bremsstrahlung.py`
- `../warpx/Examples/Tests/nuclear_fusion/analysis_two_product_fusion.py`
- `../warpx/Examples/Tests/nuclear_fusion/analysis_proton_boron_fusion.py`

这一篇补的是上一轮 `20-coulomb-bremsstrahlung-stopping-and-fusion.md` 之后还没下钻到的 kernel 细节层：

1. `pairwisecoulomb` 的 Perez 弹性散射到底怎样确定碰撞尺度
2. `bremsstrahlung` 在 photon 创建尾部怎样把相对论 photon 动量真正写回 product SoA
3. `nuclearfusion` 的两产物与 p-B11 两套 product momentum initializer 怎样组织“多份宏粒子复制”

---

## 1. `ElasticCollisionPerez`：先定 Debye / 原子尺度，再做加权二体弹性散射

`PairWiseCoulombCollisionFunc` 本身只是壳，真正的物理准备都在 `ElasticCollisionPerez(...)` 里。

### 1.1 `CoulombLog < 0` 时并不是“自动给个默认值”，而是改走局域尺度闭合

若用户没有显式给正的 `CoulombLog`，源码会先决定 screening length：

- 若 `global_lamdb > 0`，直接用全局 Debye 长度
- 否则按两 species 的局域密度和温度计算
  $$
  \lambda_D^{-2}
  =
  \frac{n_1 q_1^2}{T_1\epsilon_0}
  +
  \frac{n_2 q_2^2}{T_2\epsilon_0}
  $$

然后再定义：

- `rmin`：由较大密度给出的原子间距
- `bmax = max(lmdD, rmin)`：screening length 不能小于原子间距
- `sigma_max = 1/(n_{\max} r_{\min})`：把 mean free path 压到原子尺度得到的最大截面

所以 Perez 路径不是只靠一个 `CoulombLog` 常数工作；在自动模式下，它先用局域 plasma state 闭合：

```text
local n,T
-> Debye length / atomic spacing
-> bmax / sigma_max
-> UpdateMomentumPerezElastic(...)
```

### 1.2 关键量不是原始 pair density，而是加权后的 `n12`

`ElasticCollisionPerez(...)` 里还有一个重要实现点：它不会把 cell 里 species 原始密度直接塞进单对碰撞公式，而是重新构造：

- `wpmax = max(w1, w2)`
- 若同 species，`n12 = wpmax * (min_N + max_N - 1) / dV`
- 若异 species，`n12 = wpmax * min_N / dV`

源码注释已经把这条写明为对 Takizuka-Abe / Perez 二体配对法的加权推广，用来保证：

- 在不做完整 `N x N` 配对的情况下
- 每个宏粒子的期望速度改变量仍与全配对法一致

因此对 WarpX 当前这套 weighted macroparticle collision，真正的“有效碰撞密度”不是物理输入密度本身，而是：

- 局域 species density 决定 Debye / atomic scale
- `n12` 决定这一次抽样 pair 的 momentum update 强度

这也解释了为什么 `analysis_collision_1d.py` 和 `analysis_collision_1d_correct_conservation.py` 的 strongest evidence 分别是：

- relaxation 速率
- 守恒

而不是只看某个截面参数。

---

## 2. Bremsstrahlung `PhotonCreationFunc`：尾部真正做的是“从离子静止系写回 photon 四动量”

上一轮已经写过：

- `BremsstrahlungFunc` 前半段给事件、权重、photon energy

这一篇补的是后半段最后几步。

### 2.1 photon 不是从表里直接拿 `ux,uy,uz`

`PhotonCreationFunc` 先在离子静止系内：

1. 根据给定 photon energy `Ephoton`
2. 解出 electron / ion / photon 三者满足守恒的最终动量

随后再把：

- 更新后的 electron
- 更新后的 ion
- photon 的三动量 `p3x_rel,p3y_rel,p3z_rel`

一起变回 lab frame。

关键尾部是：

```cpp
upx = p3x_rel / PhysConst::m_e;
upy = p3y_rel / PhysConst::m_e;
upz = p3z_rel / PhysConst::m_e;
```

这说明 WarpX 的 photon species 仍沿用统一的 `ux,uy,uz` 存储接口，但对 photon 来说，这里的量实际是

$$
u = \frac{p}{m_e},
$$

即以电子质量做归一化的无量纲动量变量，而不是“真正的 photon 质量”。这样做的目的不是修改 photon 物理，而是复用统一 SoA / diagnostics / gather-consumer 接口。

### 2.2 创建后还要补 runtime attributes

在 kernel 尾部，`PhotonCreationFunc` 会对新增 product tile 调：

```cpp
ParticleCreation::DefaultInitializeRuntimeAttributes(...)
```

所以这条分支也和前面几篇统一起来了：

- product 不是只写 `x/y/z/w/ux/uy/uz`
- 用户额外 runtime attributes 仍会走统一默认初始化合同

对 bremsstrahlung 来说，这一步本身没有新物理，但它确保 collision-created photons 与其他 product species 在容器语义上保持一致。

---

## 3. `TwoProductFusionInitializeMomentum`：两产物 fusion 的“4 宏粒子”复制不是新的动力学，只是复制同一对动量

`TwoProductFusionInitializeMomentum(...)` 的结构比前面 `ParticleCreationFunc` 那一层更简单：

1. 先调一次
   `TwoProductComputeProductMomenta(...)`
2. 得到两只真实 products 的唯一一组动量
3. 再把这组动量各写两次

也就是：

- product species 1 在 `idx1_out_start` 和 `idx1_out_start+1` 写同一组 `ux,uy,uz`
- product species 2 在 `idx2_out_start` 和 `idx2_out_start+1` 写同一组 `ux,uy,uz`

原因不是有四个不同物理 products，而是：

- WarpX 在这条 Higginson-style event accounting 里
- 会在两个 parent 位置各放一份 child 宏粒子

所以“4 宏粒子”是统计实现语义，不是动力学自由度翻倍。

这正好和上一轮 `LinearBreitWheeler` 那个“4 宏粒子实现”形成对照：

- 两者都会出现 4 个宏粒子
- 但 fusion 这里 4 份只是两组 products 在两个 parent 位置上的复制
- 不涉及新的 product-type-specific kinematics

---

## 4. `ProtonBoronFusionInitializeMomentum`：p-B11 是显式两步反应，不再是一行 `TwoProductComputeProductMomenta`

`ProtonBoronFusionInitializeMomentum(...)` 明确没有复用“两产物 fusion”的简化结构，因为 p-B11 这里的 dominant path 被显式建模为两步：

1. `p + B11 -> alpha1 + Be8*`，释放约 `5.56 MeV`
2. `Be8* -> alpha2 + alpha3`，再释放约 `3.12 MeV`

### 4.1 第一步仍用 `TwoProductComputeProductMomenta`

源码先把：

- 第一个 alpha
- 激发态 `Be8*`

当作普通两产物问题处理，调用一次：

```cpp
TwoProductComputeProductMomenta(...)
```

得到：

- `ux_alpha1, uy_alpha1, uz_alpha1`
- `ux_Be, uy_Be, uz_Be`

### 4.2 第二步在 `Be8*` 静止系随机各向同性衰变

然后它再：

- 在 `Be8*` 静止系内，按 `E_decay/2` 给 `alpha2/alpha3` 的动量模长
- 用 `ParticleUtils::RandomizeVelocity(...)` 给 `alpha2` 一个各向同性方向
- 再由总动量守恒补出 `alpha3`
- 最后把 `alpha2/alpha3` 从 `Be8*` 静止系变回 lab frame

因此这条 initializer 的真实物理结构不是“直接从 reactants 到 3 alphas 的闭式解”，而是：

```text
reactants
-> alpha1 + Be8*
-> alpha2 + alpha3 in Be8* rest frame
-> boost back to lab
```

### 4.3 最后不是 3 个 alpha，而是 6 个宏粒子

和上一节同理，最后写 SoA 时：

- `alpha1` 写两次
- `alpha2` 写两次
- `alpha3` 写两次

总共 6 个 alpha 宏粒子。

这不是因为一次 p-B11 物理上会产生 6 个 alpha，而是因为 WarpX 继续沿用了：

- 在两个 parent 位置各复制一套 products

的宏粒子事件记账方式。

因此 `analysis_proton_boron_fusion.py` 里对：

- 总产额
- 能量守恒
- 三 alpha 统计
- 低密度极限
- `probability_threshold` 过大导致的故意欠产额

这些检查，本质上都同时在约束：

- 事件概率层
- 两步 kinematics 层
- 多份宏粒子复制层

---

## 5. 这一轮补出的结构结论

到这里，前两篇 collision 笔记里尚未落到 kernel 细节的几处关键空白已经补上：

1. `pairwisecoulomb`
   - 自动模式下先用局域 `n,T` 闭合 Debye / atomic scale
   - 再用加权 `n12` 驱动 Perez 散射
2. `bremsstrahlung`
   - event pass 存的是 photon energy
   - photon 真正的 `ux,uy,uz` 在 `PhotonCreationFunc` 尾部由守恒解写回
3. 两产物 fusion
   - 核心动力学只算一组 products 动量
   - 4 宏粒子只是双 parent 位置复制
4. p-B11 fusion
   - 显式两步反应
   - 6 宏粒子是三组 alpha 在双 parent 位置复制

所以接下来如果还要继续精读 `Particles/Collision/`，最自然的下一层已经不是“再分支归类”，而是：

- `UpdateMomentumPerezElastic.H` 的具体散射角/扩散步
- `BremsstrahlungEvent(...)` 的截面采样与 photon-energy 分布
- `SingleNuclearFusionEvent.H` 的概率裁剪与 multiplier 缩放细节

这些正好对应当前 `TODO.md` 里 collision 主线剩余的未完成细节层。
