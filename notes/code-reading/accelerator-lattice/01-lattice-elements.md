# AcceleratorLattice 01: drift, quadrupole, plasma lens, and hard-edged residence correction

绑定源码：

- `../warpx/Source/AcceleratorLattice/LatticeElements/LatticeElementBase.H`
- `../warpx/Source/AcceleratorLattice/LatticeElements/LatticeElementBase.cpp`
- `../warpx/Source/AcceleratorLattice/LatticeElements/Drift.H`
- `../warpx/Source/AcceleratorLattice/LatticeElements/Drift.cpp`
- `../warpx/Source/AcceleratorLattice/LatticeElements/HardEdgedQuadrupole.H`
- `../warpx/Source/AcceleratorLattice/LatticeElements/HardEdgedQuadrupole.cpp`
- `../warpx/Source/AcceleratorLattice/LatticeElements/HardEdgedPlasmaLens.H`
- `../warpx/Source/AcceleratorLattice/LatticeElements/HardEdgedPlasmaLens.cpp`
- `../warpx/Source/AcceleratorLattice/LatticeElements/HardEdged_K.H`

这篇只看元件本体，不看 finder。

## 1. `drift` 只有几何，没有场

`Drift::AddElement()` 只有一行核心调用：

```text
AddElementBase(pp_element, z_location)
```

也就是说，`drift` 的存在意义只有：

- 读 `ds`
- 在 beamline 上推进 `z_location`
- 记录一段无场区间

它没有：

- `dEdx`
- `dBdx`
- device field getter

所以当前 accelerator lattice 的一个关键事实是：

- `drift` 参与几何账本
- 但不参与运行时 field lookup

## 2. quadrupole 和 plasma lens 共享同一套“长度 + 梯度”骨架

`HardEdgedQuadrupole::AddElement()` 和 `HardEdgedPlasmaLens::AddElement()` 结构几乎一样：

1. 先 `AddElementBase(...)`
2. 再可选读：
   - `dEdx`
   - `dBdx`
3. 存入 host arrays：
   - `h_dEdx`
   - `h_dBdx`

因此它们的输入合同都很简单：

- `ds` 决定轴向范围
- `dEdx/dBdx` 决定横向聚焦场强梯度

## 3. `WriteToDevice()` 只是把 host arrays 平移到 GPU

`quad` 和 `plasmalens` 的 `WriteToDevice()` 都分两段：

1. `WriteToDeviceBase()`
   - 拷 `zs`
   - 拷 `ze`
2. 拷各自的：
   - `dEdx`
   - `dBdx`

这里没有任何数值加工。也就是说：

- 元件物理量在 host 侧就已经是最终离散参数
- device 侧只做只读访问

## 4. hard-edged 不是“粒子必须落在元件内部”才受力

`HardEdged_K.H` 里的 `hard_edged_fraction(...)` 是这条主线最容易漏掉的数值细节。

它的输入是：

- 当前 `z`
- 估计下一步 `zpvdt = z + v_z dt`
- 元件 `zs`
- 元件 `ze`

返回的是：

- 本步有多少比例时间处于元件内部

源码显式说明了它要处理这件事：

- 粒子可能一步跨过元件边界
- 甚至跨过一个很短的元件，但步末不落在元件内部

因此 hard-edged 语义并不是“inside / outside 的布尔开关”，而是：

- 用 `frac in [0,1]` 对一个时间步做 residence correction

## 5. quadrupole 的场对称性

`HardEdgedQuadrupoleDevice::get_field()` 先算：

- `frac`
- `dEdx = frac * stored_dEdx`
- `dBdx = frac * stored_dBdx`

然后返回：

```text
Ex = +x * dEdx
Ey = -y * dEdx
Bx = +y * dBdx
By = +x * dBdx
```

这对应的是标准 hard-edged quadrupole 的横向聚焦/散焦对称性：

- 一个横向方向聚焦
- 另一个横向方向散焦

## 6. plasma lens 的场对称性

`HardEdgedPlasmaLensDevice::get_field()` 的 residence correction 完全相同，但场符号不同：

```text
Ex = +x * dEdx
Ey = +y * dEdx
Bx = +y * dBdx
By = -x * dBdx
```

和 quadrupole 相比，区别在于：

- `Ey` 不再带负号
- `By` 改成带负号

也就是说，当前源码并不是把 plasma lens 当成“quad 的别名”，而是给了它独立的横向对称性。

## 7. 对书稿最重要的两个边界

### 7.1 `drift` 不产场

这点必须写清。

因为 examples 里常见的 beamline 形式是：

```text
drift + quad + drift + quad
```

但真正 runtime 会对粒子返回场的，只有：

- `quad`
- `plasmalens`

`drift` 只参与长度账本和解析对照的几何段。

### 7.2 hard-edged discontinuity 被 residence correction 弱化

当前源码并不是在粒子位置上做纯粹的 step-function 开关，而是用：

- `hard_edged_fraction(z, zpvdt, zs, ze)`

把一个大时间步内“在元件里待了多久”折算成有效梯度。

因此这条主线更准确的说法是：

- hard-edged 是几何定义
- 数值实现仍然通过 step-residence fraction 做了离散时间修正

这也是后面 `analysis.py` 能在较大时间步下仍和解析串联模型对上的关键原因之一。
