# Field Ionization 主链：ADK filter、product species 与 `ionizationLevel` 的后续消费

绑定源码：

- `../warpx/Source/Particles/ElementaryProcess/Ionization.H`
- `../warpx/Source/Particles/ElementaryProcess/Ionization.cpp`
- `../warpx/Source/Particles/PhysicalParticleContainer.cpp`
- `../warpx/Source/Particles/MultiParticleContainer.cpp`
- `../warpx/Source/Particles/WarpXParticleContainer.cpp`
- `../warpx/Source/Particles/Deposition/ChargeDeposition.H`
- `../warpx/Source/Particles/Deposition/CurrentDeposition.H`

代表性 examples / regressions：

- `../warpx/Examples/Tests/field_ionization/inputs_test_2d_ionization_lab`
- `../warpx/Examples/Tests/field_ionization/inputs_test_2d_ionization_boost`
- `../warpx/Examples/Tests/field_ionization/inputs_test_2d_ionization_picmi.py`
- `../warpx/Examples/Tests/field_ionization/inputs_test_2d_ionization_lab_restart`
- `../warpx/Examples/Tests/field_ionization/analysis.py`

## 1. 这条链改写的不只是电子数，而是 species 语义本身

field ionization 在 WarpX 里至少同时改写三层语义：

1. 源离子 species 运行时新增 `ionizationLevel`
2. 电离事件把 product electron 写到另一个 species
3. 源离子的有效电荷在 `rho/J` 沉积时按 `ionizationLevel` 动态重算

因此，它不是“附加 source term”，而是把 species 属性系统、粒子创建路径和沉积权重一起接进主循环。

## 2. 输入层的最小合同

`inputs_test_2d_ionization_lab` 的最小 WarpX 原生合同是：

```text
ions.do_field_ionization = 1
ions.ionization_initial_level = 2
ions.ionization_product_species = electrons
ions.physical_element = N
electrons.injection_style = none
```

这意味着：

- `ions` 自带初始电离态 `2`
- `electrons` 初始为空 species
- 后续电子全部来自电离事件

PICMI 版则把同一合同包装成：

```python
nitrogen_ionization = picmi.FieldIonization(
    model="ADK",
    ionized_species=ions,
    product_species=electrons,
)
sim.add_interaction(nitrogen_ionization)
```

所以 PICMI 没有另一套电离实现，只是另一种前端。

## 3. species 构造期只先记住 `do_field_ionization`

`PhysicalParticleContainer` 构造期只做：

```cpp
pp_species_name.query("do_field_ionization", do_field_ionization);
```

此时不会初始化 ADK 系数。原因是 ADK prefactor 依赖运行时 `dt`，而 species 构造期还拿不到最终时间步长。

## 4. `InitIonizationModule()` 才真正把 species 变成 ionizable species

`PhysicalParticleContainer::InitIonizationModule()` 会：

1. 若用户给了别的电荷，强制覆盖回 `charge = q_e`
2. 读取：
   - `do_adk_correction`
   - `ionization_initial_level`
   - `ionization_product_species`
   - `physical_element`
3. 若没有就动态加上：
   - `AddIntComp("ionizationLevel")`
4. 从内建表读取该元素全部 ionization energies
5. 根据当前 `dt` 构造：
   - `adk_power`
   - `adk_prefactor`
   - `adk_exp_prefactor`
   - 可选 `adk_correction_factors`

这一步的边界很重要：

- `ionizationLevel` 不是 `PIdx` builtin
- ADK tables 是按运行时 stage 存储的 GPU resident arrays
- Zhang correction 当前只允许氢

### 4.1 当前源码树没有独立 `OTB` 路径

这一点需要显式写出来，因为 TODO 里长期把 `ADK/OTB` 并列，很容易让人误以为 `Ionization.*` 里同时实现了两套场电离模型。

但从当前本地源码和官方参数文档看：

- `Docs/source/usage/parameters.rst` 对 `do_field_ionization` 的描述明确写的是
  `using the ADK theory`
- `PhysicalParticleContainer::InitIonizationModule()` 只读取
  `do_adk_correction`
- `IonizationFilterFunc` 只消费
  `adk_prefactor`
  `adk_exp_prefactor`
  `adk_power`
- 当前 `Source/Particles/ElementaryProcess/Ionization.*` 中没有独立的
  barrier-suppression / over-the-barrier / OTB 分支

因此当前更准确的说法不是“还有一条 OTB 实现待读”，而是：

1. 当前工作树里的 field ionization 主链是 `ADK`；
2. 可选修正只有 Zhang correction；
3. 若后续要谈 `OTB`，那属于“源码未实现或至少不在当前 `Ionization.*` 中”的边界说明，而不是现有主链的一部分。

### 4.2 电离能表不是运行时输入，而是编译进来的元素表

`InitIonizationModule()` 里真正做的不是“从 input 文件读一串 ionization energies”，而是：

```cpp
const int ion_element_id = utils::physics::ion_map_ids.at(physical_element);
ion_atomic_number = utils::physics::ion_atomic_numbers[ion_element_id];
const int offset = utils::physics::ion_energy_offsets[ion_element_id];
for(int i=0; i<ion_atomic_number; i++){
    h_ionization_energies[i] =
        utils::physics::table_ionization_energies[i+offset];
}
```

这说明 `physical_element` 的真实语义是：

1. 先在内建 element map 中定位元素 ID；
2. 再用 `ion_energy_offsets` 在全局拼接表里切出该元素全部 successive ionization energies；
3. 最后把这段 host vector 拷到 device side `ionization_energies`

因此 field ionization 当前不是“用户可自由给任意 ionization table”的框架，而是：

- WarpX 内建元素表
- `physical_element` 只作为查表 key
- `ionization_initial_level` 只决定从哪一级开始演化，不改写整张表

### 4.3 ADK prefactor 真正依赖的是运行时 `dt`

这也是 species 构造期只先记 `do_field_ionization` 的原因。

源码里 ADK 系数是在 `InitIonizationModule()` 里按当前 `dt` 现算的：

```cpp
const Real dt = WarpX::GetInstance().getdt(0);
...
p_adk_prefactor[i] = dt * wa * C2 * ( Uion/(2._rt*UH) )
    * std::pow(2._rt*std::pow((Uion/UH),3._rt/2._rt)*Ea,2._rt*n_eff - 1._rt);
p_adk_exp_prefactor[i] = -2._rt/3._rt * std::pow( Uion/UH,3._rt/2._rt) * Ea;
```

所以当前 ADK 实现的一个关键边界是：

- 它不是纯粹的 field-only rate lookup
- 而是已经把本步 `dt` 吸收到 `w_dtau` 的 prefactor 里
- 这也是 restart / boosted / adaptive-step 场景下必须单独看初始化时机的原因

## 5. `IonizationFilterFunc` 真正决定单粒子是否电离

`getIonizationFunc()` 只负责把 tile 上下文打包成 `IonizationFilterFunc`。

真正的 `operator()` 对每个粒子会：

1. 读当前 `ionizationLevel`
2. gather 网格 `E/B`
3. 叠加 external particle field
4. 用当前 `ux/uy/uz` 计算粒子系中的场幅值
5. 用 ADK 公式构造概率并做随机抽样

核心不是实验室系 `|E|`，而是粒子系场幅值：

```cpp
const Real E = std::sqrt(
    - (u·E)^2 / c^2
    + (ga*Ex + uy*Bz - uz*By)^2
    + (ga*Ey + uz*Bx - ux*Bz)^2
    + (ga*Ez + ux*By - uy*Bx)^2 );
```

因此 boosted-frame test 不是“换个坐标再跑一遍”，而是在验证这层相对论一致性。

## 6. `IonizationTransformFunc` 很小，但语义很重

transform 本体只有一句：

```cpp
src.m_runtime_idata[0][i_src] += 1;
```

它只负责把源离子的 `ionizationLevel` 加一。

product electron 的真正创建不是在这个 functor 里手写完成，而是交给：

```cpp
filterCopyTransformParticles<1>(...)
```

因此，一次电离事件在源码里被刻意拆成：

- 修改源离子的 charge state
- 把新电子写到 product species

两部分。

## 7. `doFieldIonization()` 怎样把 event 落成 product species

`MultiParticleContainer::doFieldIonization()` 对每个开启 `do_field_ionization` 的 species：

1. 找到 `ionization_product_species` 对应的容器
2. 建 `SmartCopyFactory`
3. 取 `Filter = getIonizationFunc(...)`
4. 取 `Transform = IonizationTransformFunc()`
5. 调 `filterCopyTransformParticles<1>(...)`
6. 给新粒子设新 IDs

也就是说，field ionization 没有自己发明一套粒子插入 API，而是复用 WarpX 通用的：

- filter
- copy
- transform

三段式粒子创建框架。

## 8. `ionizationLevel` 会继续直接改写 `rho/J`

`WarpXParticleContainer::DepositCurrent()` 和 `DepositCharge()` 都会把：

```cpp
ion_lev = pti.GetiAttribs("ionizationLevel").dataPtr();
```

传给底层沉积 kernel。

而沉积层会做：

```cpp
if (do_ionization) { wq *= ion_lev[ip]; }
```

因此，field ionization 的闭环是：

$$
\text{ADK event}
\rightarrow \texttt{ionizationLevel}
\rightarrow \text{effective source charge}
\rightarrow \rho, J
\rightarrow \text{fields and diagnostics}.
$$

这就是为什么它不该被理解成“只多了一些电子”。

## 8.1 `ionization_initial_level` 会在所有初始化路径里先写进粒子

field ionization 的权重处理，不是等第一步发生电离后才临时开始。

当前工作树里至少有三条初始化路径，会在粒子创建时就把
`ionization_initial_level` 写进 `ionizationLevel`：

1. `DefaultInitialization.H`
   - runtime int attribute 初始化阶段，若当前 int comp 是
     `ionizationLevel`
     就统一写成 `ionization_initial_level`
2. `AddParticles.cpp`
   - 常规 plasma injection 路径在新粒子生成后直接写 `pi[ip] = loc_ionization_initial_level`
3. `AddGaussianBeam()` / 其它显式列表注入路径
   - 也在对应的 SoA int data 上写入 `p_ion_level[ip] = loc_ionization_initial_level`

这意味着源离子一进入主循环，就已经带着可用于沉积的有效离化态，而不是“默认中性、等第一次 ADK event 才开始计价”。

## 8.2 权重处理的真实语义是“宏粒子权重不变，有效物理电荷变”

源码里 `field ionization` 不会改写 parent 粒子的宏粒子权重 `w`。

真正变化的是沉积时的 `wq` / `qp`：

- `ChargeDeposition.H`、`CurrentDeposition.H` 会在 `do_ionization` 时乘上 `ion_lev[ip]`
- `PhysicalParticleContainer.cpp`、`ImplicitPushPX.cpp`、`RigidInjectedParticleContainer.cpp` 的若干入口也会在构造 `qp` 或传给 push/deposition helper 时乘 `ion_lev`

因此当前语义应写成：

1. 宏粒子统计权重 `w` 继续代表“这个 macro 代表多少 physical particles”
2. `ionizationLevel` 改写的是每个 physical particle 的有效电荷态
3. 最终沉积的源强是

$$
w q_{\mathrm{elementary}} \times \texttt{ionizationLevel}
$$

而不是“把 `w` 本身乘大”。

这也是为什么 `charge != q_e` 会在 `InitIonizationModule()` 中被强制改回 `q_e`：
源码要把离化态计价统一放在 `ionizationLevel` 这层，而不是允许用户同时改写 base charge 和 charge state，导致双重计数。

## 9. `analysis.py` 真正在验证什么

`Examples/Tests/field_ionization/analysis.py` 的核心断言是：

```python
N5_fraction = ilev[ilev == 5].size / float(ilev.size)
assert abs(N5_fraction - 0.32) / 0.32 < 0.07
```

因此它直接验证的是：

- 最终 `ionizationLevel` 分布
- 也就是 ADK 概率、粒子系场幅值、source-level 更新、product species 创建 这整条链

它还顺手检查可选 runtime attribute `orig_z` 是否合理，所以同一个 regression 也覆盖了产品电子的属性初始化。

## 10. lab / boost / restart / PICMI 四组证据各补哪一层

### 10.1 `inputs_test_2d_ionization_lab`

最直接的 lab-frame ADK 基准。

### 10.2 `inputs_test_2d_ionization_boost`

重点在验证 boosted frame 下，`IonizationFilterFunc` 的粒子系场幅值路径仍能给出正确 ionization fraction。

### 10.3 `inputs_test_2d_ionization_lab_restart`

重点在：

- `ionizationLevel`
- product species
- checkpoint/restart

之间的保真。

### 10.4 `inputs_test_2d_ionization_picmi.py`

重点在验证 PICMI `FieldIonization(model="ADK")` 最终确实落回 WarpX 原生 product-species 主链。

## 11. 这条链在书稿里的更合理归位

field ionization 不应继续放在 `Laser/` 目录里解释，因为它的核心实现根本不在 laser profile 或 antenna。

更合理的归位是：

1. `Laser/` 只说明 `laser_ion` 给了一个应用骨架
2. `Particles/` 说明：
   - `InitIonizationModule()`
   - `IonizationFilterFunc`
   - `IonizationTransformFunc`
   - `doFieldIonization()`
   - `ionizationLevel -> rho/J`
3. regression 索引再把 lab / boost / restart / PICMI 四层证据补齐

这样，field ionization 才真正从“laser_ion 输入里的注释块”提升成独立的粒子多物理主模块。
