# AcceleratorLattice 00: lattice data model and recursive input graph

绑定源码：

- `../warpx/Source/AcceleratorLattice/AcceleratorLattice.H`
- `../warpx/Source/AcceleratorLattice/AcceleratorLattice.cpp`
- `../warpx/Source/AcceleratorLattice/LatticeElements/LatticeElementBase.H`
- `../warpx/Source/AcceleratorLattice/LatticeElements/LatticeElementBase.cpp`
- `../warpx/Source/AcceleratorLattice/README.rst`

这篇先回答三个最基本的问题：

1. accelerator lattice 在当前源码里的对象图是什么。
2. `lattice.elements`、`line`、`reverse` 这些输入是怎么变成 beamline 的。
3. host/device 双层结构为什么存在。

## 1. 顶层对象并不复杂

当前 worktree 里，`AcceleratorLattice` 本身只是一个很薄的 owner：

- host 侧持有三类元件容器：
  - `Drift h_drift`
  - `HardEdgedQuadrupole h_quad`
  - `HardEdgedPlasmaLens h_plasmalens`
- 若 beamline 已定义，再按 grid 建：
  - `LayoutData<LatticeElementFinder>`

也就是说，这个目录当前并不是“通用加速器框架”，而是一个只支持少数 hard-edged 元件的薄运行层。

## 2. 构造函数只做两件事

`AcceleratorLattice::AcceleratorLattice()` 的逻辑很短：

```text
z_location = 0
ReadLattice("lattice", z_location)
h_quad.WriteToDevice()
h_plasmalens.WriteToDevice()
```

这有两个直接结论。

第一，beamline 的一维几何坐标不是用户逐个手填 `zs/ze`，而是从 `z_location = 0` 开始沿着 `ds` 递推出来。

第二，只有会真正产生外场的元件需要拷到 device：

- `quad`
- `plasmalens`

`drift` 不需要额外 device arrays，因为它只贡献几何长度，不直接返回场。

## 3. `ReadLattice()` 是递归 beamline parser

`ReadLattice(root_name, z_location)` 会：

1. 对 `root_name` 做 `ParmParse`
2. 读取 `elements`
3. 可选读取 `reverse`
4. 逐个元素展开

它支持 4 种 `type`：

- `drift`
- `quad`
- `plasmalens`
- `line`

其中 `line` 不是新元件，而是递归子 beamline：

```text
if type == line:
    ReadLattice(element_name, z_location)
```

因此 `lattice.elements` 和 `line*.elements` 共同构成的是一棵递归输入树，而不是单层数组。

## 4. `reverse` 真正改变的是遍历顺序

`ReadLattice()` 先拿到 `lattice_elements`，然后若 `reverse = 1`，直接：

```text
std::reverse(lattice_elements.begin(), lattice_elements.end())
```

所以 `reverse` 的语义不是“把已有 `zs/ze` 倒过来”，而是：

- 先反转子元素顺序
- 再按新的顺序继续用同一个 `z_location` 递推

这意味着 beamline 几何仍然是从当前 `z_location` 向前累加，只是元件排列顺序变了。

## 5. `LatticeElementBase` 统一提供几何账本

所有元件都继承 `LatticeElementBase`。真正的通用几何逻辑都在：

- `LatticeElementBase::AddElementBase`
- `LatticeElementBase::WriteToDeviceBase`

`AddElementBase()` 的行为很清楚：

```text
read ds
h_zs.push_back(z_location)
z_location += ds
h_ze.push_back(z_location)
nelements += 1
```

所以每个元件共享同一条最核心合同：

- `ds` 决定长度
- `zs/ze` 由运行中的 `z_location` 自动生成
- `nelements` 只是该类型元件计数

## 6. host/device 双层结构的原因

`README.rst` 已经把设计目的说得很直接：

- host 类负责读输入、管理复杂容器、组织 lookup tables
- device 类只保留简单 POD 风格数据和指针

在当前实现里，这个双层结构主要体现在两处：

1. 元件类
   - host：`HardEdgedQuadrupole`、`HardEdgedPlasmaLens`
   - device：`HardEdgedQuadrupoleDevice`、`HardEdgedPlasmaLensDevice`
2. finder
   - host：`LatticeElementFinder`
   - device：`LatticeElementFinderDevice`

这不是抽象设计偏好，而是 GPU 路径的硬要求：

- host 侧需要 `std::vector`、递归读参、`LayoutData`
- device 侧只允许轻量可拷贝结构

## 7. 当前源码树边界

从当前目录内容看，accelerator lattice 这条线的 active element family 只有：

- `drift`
- `quad`
- `plasmalens`

再加上一个运行期 finder。

因此这条主线在项目里最合适的拆法是：

1. `00`：数据模型、递归输入树、host/device 拆分
2. `01`：各元件自己的场语义
3. `02`：finder 如何在 push 前把这些元件转成粒子可用外场

而不是把整个目录误判成一个巨大子系统。
