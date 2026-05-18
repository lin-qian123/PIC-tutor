# `FieldGather.H` 的其余几何分支、energy/momentum 两族 gather 与 external particle fields

绑定源码：

- `../warpx/Source/Particles/Gather/FieldGather.H`
- `../warpx/Source/Particles/Gather/GetExternalFields.H`
- `../warpx/Source/Particles/Gather/GetExternalFields.cpp`
- `../warpx/Source/Particles/ExternalParticleFields.cpp`
- `../warpx/Source/Particles/PhysicalParticleContainer.cpp`
- `../warpx/Source/Particles/MultiParticleContainer.cpp`
- `../warpx/Docs/source/usage/parameters.rst`

对应 examples / regressions：

- `../warpx/Examples/Tests/energy_conserving_thermal_plasma/analysis.py`
- `../warpx/Examples/Tests/energy_conserving_thermal_plasma/inputs_test_1d_energy_conserving_thermal_plasma`
- `../warpx/Examples/Tests/energy_conserving_thermal_plasma/inputs_test_2d_energy_conserving_thermal_plasma`
- `../warpx/Examples/Tests/langmuir/analysis_utils.py`
- `../warpx/Examples/Tests/langmuir/inputs_test_2d_langmuir_multi_psatd_momentum_conserving`
- `../warpx/Examples/Tests/langmuir/inputs_test_3d_langmuir_multi_psatd_momentum_conserving`
- `../warpx/Examples/Tests/load_external_field/analysis_3d.py`
- `../warpx/Examples/Tests/load_external_field/analysis_rz.py`
- `../warpx/Examples/Tests/load_external_field/analysis_time_scaling.py`
- `../warpx/Examples/Tests/load_external_field/inputs_test_3d_load_external_field_particle_picmi.py`
- `../warpx/Examples/Tests/load_external_field/inputs_test_rz_load_external_field_particles`
- `../warpx/Examples/Tests/load_external_field/inputs_test_3d_load_external_field_particle_time`
- `../warpx/Examples/Tests/load_external_field/inputs_test_3d_load_external_field_particle_multi_time`

这一篇补的是 [02-gather-shape-deposition-kernels.md](/Volumes/PHILIPS/programs/PIC/PIC-tutor/notes/code-reading/particles/02-gather-shape-deposition-kernels.md) 还没系统落成文档的那一层：

1. `FieldGather.H` 在 `1D_Z / RCYLINDER / RSPHERE / 3D` 下的剩余 gather 结构
2. `energy-conserving` 与 `momentum-conserving` 在 WarpX 里的真实代码差异
3. implicit 路径为什么要按沉积算法切换 gather stencil
4. external particle fields 怎样真正进入 `PushPX()`

---

## 1. 运行时 wrapper 只是两件事：定阶数，定是否 Galerkin 降阶

`FieldGather.H:2116-2191` 的运行时入口：

```cpp
void doGatherShapeN (..., const int nox, const bool galerkin_interpolation)
{
    if (galerkin_interpolation) {
        if (nox == 1) { doGatherShapeN<1,1>(...); }
        else if (nox == 2) { doGatherShapeN<2,1>(...); }
        else if (nox == 3) { doGatherShapeN<3,1>(...); }
        else if (nox == 4) { doGatherShapeN<4,1>(...); }
    } else {
        if (nox == 1) { doGatherShapeN<1,0>(...); }
        else if (nox == 2) { doGatherShapeN<2,0>(...); }
        else if (nox == 3) { doGatherShapeN<3,0>(...); }
        else if (nox == 4) { doGatherShapeN<4,0>(...); }
    }
}
```

所以运行时真正决定 gather kernel 的只有两件事：

- shape order `nox`
- `galerkin_interpolation` 是否为真

`energy-conserving` 和 `momentum-conserving` 并不是在这里分派，而是更早通过 field centering / field allocation / index type 进入这套模板。

---

## 2. `doGatherShapeN<depos_order, galerkin_interpolation>` 的第一性结构

模板主体 `FieldGather.H:348-826` 的关键不是“一个通用三重循环”，而是：

- 先为每个方向各自产生
  - 普通 shape arrays
  - Galerkin 降阶 shape arrays
- 再按每个场分量自己的 staggering 选择
  - node 或 cell
  - full order 或 `p-1`
- 最后每个几何分支分别做自己的一套累加

最关键的局部变量是：

```cpp
Compute_shape_factor<depos_order> const compute_shape_factor;
Compute_shape_factor<depos_order - galerkin_interpolation> const compute_shape_factor_galerkin;
```

因此 `galerkin_interpolation = 1` 时并不是“所有分量全部降一阶”，而只是那些在代码里拿 `*_galerkin` 数组的分量沿某些方向降一阶。

---

## 3. energy-conserving 与 momentum-conserving 的真实差别不在字符串，而在 index type

官方参数页 `parameters.rst:3286-3298` 给出的定义是：

- `energy-conserving`
  - 直接从网格点 gather
- `momentum-conserving`
  - 先把场从原网格中心化到 node
  - 再从 node gather

代码层对应的真实机制是：

1. `doGatherShapeN()` 并不自己判断“我是 energy 还是 momentum”
2. 它只读 `ex_type/ey_type/ez_type/bx_type/by_type/bz_type`
3. 因此两族 gather 的真正差异体现在：
   - 传进来的 `MultiFab` 是不是已经 nodal-centered
   - 对应 `IndexType` 是 `NODE` 还是 `CELL`

这也解释了为什么官方文档说：

- collocated grid 下两者等价
- hybrid grid 下默认必须 `momentum-conserving`

因为一旦所有分量都已经 collocated/nodal，`doGatherShapeN()` 看到的就是同一种 `IndexType` 组合，路径自然等价。

---

## 4. Galerkin 不是另一个 gather family，而是给部分分量沿部分方向降阶

`parameters.rst:3734-3739` 已经把官方合同说得很直接：

- collocated grid 默认 `galerkin_scheme = 0`
- momentum-conserving gather 默认 `galerkin_scheme = 0`
- `algo.current_deposition = direct` 默认 `galerkin_scheme = 0`
- 其他情况下才默认 `1`

在 `FieldGather.H` 里这件事落实成了非常具体的分量方向选择。

例如 3D 下：

- `Ex`
  - x 方向用 `p-1`
  - y/z 方向用 `p`
- `Ey`
  - y 方向用 `p-1`
  - x/z 方向用 `p`
- `Ez`
  - z 方向用 `p-1`
  - x/y 方向用 `p`
- `Bx/By/Bz`
  也各自沿与其 staggering 匹配的方向拿 `p-1`

所以 Galerkin 的真实语义是：

- 不是“换一套插值公式”
- 而是“在 staggered + direct/Esirkepov 这类组合里，用和离散 Maxwell/charge-current coupling 更匹配的低一阶 shape”

---

## 5. 剩余几何分支不是裁剪版 3D，而是各自有独立的物理坐标重建

### 5.1 `WARPX_DIM_1D_Z`

`FieldGather.H:526-544` 的 1D 分支最紧：

- `Ex/Ey/Bz` 用 full order
- `Ez/Bx/By` 用 `p-1` 或 full order，取决于 `galerkin_interpolation`

本质上这里只剩一个 `z` 方向 shape array，但仍保持：

- 纵向电场/横向磁场这组 staggered 变量可能走降阶

### 5.2 `WARPX_DIM_XZ`

XZ 分支 `FieldGather.H:546-580` 不是“把 3D 去掉 y”，而是显式保留：

- `Ey`：full/full
- `Ex/Bz`：x 方向可降阶，z 方向 full
- `Ez/Bx`：z 方向可降阶，x 方向 full
- `By`：x/z 都可能降阶

这正是 2D Yee staggering 在 `x-z` 平面上的最小完整版本。

### 5.3 `WARPX_DIM_RZ`

RZ 分支 `FieldGather.H:582-688` 的第一性结构是：

1. 先 gather 柱坐标分量
   - `Er`
   - `Etheta`
   - `Ez`
   - `Br`
   - `Btheta`
   - `Bz`
2. 对 mode 0 和 `m>0` 分别处理
3. 对 `m>0` 用
   $$
   e^{-im\theta}
   $$
   的实虚部重建 mode 贡献
4. 最后再转回粒子 pusher 需要的 Cartesian-like
   - `Exp/Eyp`
   - `Bxp/Byp`

因此 RZ gather 绝不是“直接把二维数组当 Cartesian XZ 用”，而是：

- 先 mode-sum
- 再柱坐标到笛卡尔分量变换

### 5.4 `WARPX_DIM_RCYLINDER`

RCYLINDER 分支 `FieldGather.H:690-719` 没有 azimuthal mode 求和，但仍保留：

- `Fr/Ftheta/Fz`
  的 gather
- 再用粒子角度把 `Fr/Ftheta` 转回 `Fx/Fy`

所以它比 RZ 少的是 Fourier 模式，不是柱坐标分量重建。

### 5.5 `WARPX_DIM_RSPHERE`

RSPHERE 分支 `FieldGather.H:721-760` 更进一步：

- 先 gather
  - `Er`
  - `Etheta`
  - `Ephi`
  - `Br`
  - `Btheta`
  - `Bphi`
- 再通过
  - `theta`
  - `phi`
  角把球坐标分量转回 `Ex/Ey/Ez` 和 `Bx/By/Bz`

这说明 WarpX 的 gather 层已经把 RCYLINDER / RSPHERE 的几何变换完全封装掉了，后面的 pusher 仍然吃统一的 Cartesian-like 六个分量。

---

## 6. implicit gather 不是复用显式 gather，而是按沉积算法切换 stencil

`FieldGather.H:2195-2328` 的 `doGatherShapeNImplicit(...)` 非常关键。

它不是简单地：

- 用半步位置调用一次 `doGatherShapeN`

而是先按 `depos_type` 分派：

- `Esirkepov`
  - `doGatherShapeNEsirkepovStencilImplicit<...>`
- `Villasenor`
  - `doGatherPicnicShapeN<...>`
- `Direct`
  - 直接在 `x^{n+1/2}` 用显式 `doGatherShapeN<...,0>`

这和前面 implicit deposition 的差异完全闭合：

- implicit 并不是“先用某个统一 gather，再换沉积公式”
- 它要求 gather stencil 与后续 charge-conserving deposition 的几何解释保持一致

也就是说：

- `Esirkepov implicit` 用 Esirkepov-compatible gather stencil
- `Villasenor implicit/suborbit` 用 Picnic/Villasenor-compatible gather stencil
- `Direct implicit` 才退回普通半步位置 gather

---

## 7. external particle fields 有三条入口，但只有两条真的在 gather kernel 里逐粒子相加

### 7.1 parser / repeated plasma lens：逐粒子 functor，直接在 `PushPX()` 里叠加

`GetExternalFields.H` 定义的 `GetExternalEBField` functor 支持三类 runtime 类型：

- `None`
- `Parser`
- `RepeatedPlasmaLens`

`PhysicalParticleContainer.cpp:1266-1285` 和 `:1495-1513` 的顺序是：

1. 先把常量外场
   - `m_E_external_particle`
   - `m_B_external_particle`
   写进 `Exp/Eyp/Ezp/Bxp/Byp/Bzp`
2. 若允许 gather，则调用 `doGatherShapeN(...)`
3. 若 `getExternalEB` 非空，再逐粒子执行：
   - parser 外场
   - repeated plasma lens
   - accelerator lattice

所以 parser/repeated-lens 这类 external particle field 的真实合同是：

- 主网格场先 gather
- 然后把 external fields 直接加到粒子上的六个分量

### 7.2 boosted-frame 外场不是在别处预变换，而是在 functor 里现算

`GetExternalFields.H` 对 parser 外场的 boosted-frame 处理很明确：

1. 先把 `(z,t)` 变回 lab-frame
2. 用 parser 求 lab-frame `E/B`
3. 再把 `Ex/Ey/Bx/By` Lorentz 变回 boosted frame

因此 external particle fields 的 boost 一致性不是靠输入文件预处理，而是 gather 时逐粒子在线完成。

### 7.3 `read_from_file` 是第三条入口，但它不会进 `GetExternalEBField` kernel

这条分支最容易误解。

`GetExternalFields.cpp` 里明确写着：

- 当 `m_E_ext_particle_s == "read_from_file"`
- 或 `m_B_ext_particle_s == "read_from_file"`

就把 runtime type 设成 `None`。

注释直接说明原因：

- 这类外场不会在 gather kernel 里逐粒子加
- 而是先加到 `Efield_aux/Bfield_aux` 这类 `MultiFab`
- 粒子随后像 gather 主场一样去 gather 它们

因此 external particle fields 实际上分成两族：

1. `parse_*_ext_particle_function` / `repeated_plasma_lens`
   - particle-side direct add
2. `read_from_file`
   - grid-side pre-add to aux fields, then ordinary gather

---

## 8. `ExternalParticleFields.cpp` 解决的是 metadata，不是 gather 数学

`ExternalParticleFields::ReadParameters()` 只做三件事：

1. 读取 `particles.E_ext_particle_init_style/B_ext_particle_init_style`
2. 解析单 field 或 named multi-field 的 `read_fields_from_path`
3. 为每个 field 构造时间依赖 parser
   - `read_fields_E_dependency(t)`
   - `read_fields_B_dependency(t)`

所以这层并不决定粒子怎样加场，它只决定：

- 有几张外场 map
- 每张 map 的文件路径
- 每张 map 的时间缩放函数

真正的几何和逐粒子消费发生在：

- grid-side `LoadExternalFields() / AddExternalFields()`
- 或 particle-side `GetExternalEBField`

---

## 9. runtime 约束：有些物理过程要求 momentum-conserving gather，不只是建议

`MultiParticleContainer::doQEDSchwinger()` 里有硬断言：

```cpp
WARPX_ALWAYS_ASSERT_WITH_MESSAGE(
    warpx.grid_type == GridType::Collocated ||
    warpx.field_gathering_algo == GatheringAlgo::MomentumConserving,
    "ERROR: Schwinger process only implemented for warpx.grid_type=collocated"
    "or algo.field_gathering = momentum-conserving");
```

所以 `momentum-conserving gather` 在 WarpX 里不只是某种“可能更稳”的数值选项，而是某些物理过程的实现前提。

这也和前面 initialization 阶段里看到的组合约束一致：

- collocated grid
- nodal-centered fields
- momentum-conserving gather

本质上是一整组可执行合同。

---

## 10. regression 证据怎样对应这几条 gather 分叉

### 10.1 `energy_conserving_thermal_plasma`

`analysis.py` 检查：

$$
\frac{|E(t)-E(0)|}{E(0)} < 0.003
$$

其中

- `E = field_energy + particle_energy`
- 输入显式设
  - `warpx.do_electrostatic = labframe`
  - `algo.field_gathering = energy-conserving`
  - `algo.particle_shape = 2`

所以这组 tests 真正在给：

- `energy-conserving gather`
- electrostatic thermal plasma

提供能量增长受控的 regression。

### 10.2 `langmuir_multi_psatd_momentum_conserving`

这组输入显式设：

- `algo.field_gathering = momentum-conserving`
- `algo.maxwell_solver = psatd`

对应 `analysis_utils.py` 里的关键逻辑是：

- 如果是 `current_correction`
- 或 `vay deposition`
- 或非 RZ、非 PSATD 的 `Esirkepov`

就检查
$$
\nabla\cdot E \approx \rho/\varepsilon_0
$$

并且它还明确说明：

- `Esirkepov + PSATD` 一般不做这个 charge conservation check
- 除非特殊谱阶组合

所以这组 regression 的真实作用不是“momentum-conserving gather 本身单测”，而是：

- 在 `PSATD + momentum-conserving gather` 组合下
- 继续拿 Langmuir 主问题做守恒/稳定性基线

从 Birdsall-Langdon 的文献脉络看，这组回归最该挂到两条边界上：

1. Chapter 10
   - `momentum-conserving` 不是“更普通的 gather wrapper”，而是优先保留零总力/动量结构的那条离散合同；
2. Chapter 8 / 12
   - Langmuir 解析场解与 `divE-rho/\varepsilon_0` 检查，让它非常适合观察 sampled density、aliasing 和 collective response 有没有把系统带离受控区。

也就是说，`langmuir_multi_psatd_momentum_conserving` 不是在证明“这套组合永远更稳定”，而是在最干净的解析波问题上继续盯：

- charge-conservation 误差
- 主模解析场解
- solver/deposition/gather 组合后的数值守恒边界

这正是 Birdsall 那条 “从 dispersion relation 到 fluctuation / effective collision” 主线在 WarpX 本地最可操作的最小对照树之一。

### 10.3 `load_external_field`

这一组 tests 刚好把 external particle fields 的三条合同都覆盖到了：

- `analysis_3d.py`
  - 3D 磁镜单粒子轨道
  - 验证 particle external field 真被粒子消费
- `analysis_rz.py`
  - RZ/theta-mode 版本的同一磁镜轨道
- `analysis_time_scaling.py`
  - 只看两个时刻 `B` 的缩放比
  - 验证 `read_fields_B_dependency(t)` 与 multi-field superposition

尤其：

- `inputs_test_3d_load_external_field_particle_picmi.py`
  覆盖 3D single-field particle external field
- `inputs_test_rz_load_external_field_particles`
  覆盖 RZ read-from-file particle external field
- `inputs_test_3d_load_external_field_particle_time`
  覆盖单 field 时间依赖
- `inputs_test_3d_load_external_field_particle_multi_time`
  覆盖 named multi-field + 不同频率叠加

---

## 11. 当前阶段最稳妥的结论

到这里，`Particles/Gather` 这一块可以更准确地分成四层：

1. **显式普通 gather**
   - `doGatherShapeN<order, galerkin>`
2. **几何分支**
   - `1D_Z / XZ / RZ / RCYLINDER / RSPHERE / 3D`
3. **隐式 gather**
   - 按 deposition 算法切换 stencil
4. **外场叠加**
   - constant
   - parser
   - repeated plasma lens
   - read-from-file pre-add to aux field

因此这一层已经不该再简化成“把场插值到粒子位置”。

更准确的说法是：

- WarpX 的 gather 是一个把
  - grid centering
  - geometry
  - Galerkin 降阶
  - implicit deposition compatibility
  - external particle fields
  统一折叠到单粒子 `Exp/Eyp/Ezp/Bxp/Byp/Bzp` 的接口层。

如果再把 regression 证据压成一句话，当前最稳妥的分工是：

- `energy_conserving_thermal_plasma`
  - 更像 Chapter 10 的局部能量账本探针
  - 直接问总能量漂移是否被压住
- `langmuir_multi_psatd_momentum_conserving`
  - 更像 Chapter 8 / 10 / 12 的解析模与离散守恒探针
  - 直接问解析模结构、Gauss-law 误差和 solver/gather/deposition 组合是否还在受控边界内

这样写，比把两者都笼统归成“gather regression”更接近它们在本地 worktree 里的真实分工。
