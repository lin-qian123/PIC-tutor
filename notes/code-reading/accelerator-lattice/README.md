# AcceleratorLattice 源码精读入口

绑定源码：`../warpx/Source/AcceleratorLattice`。

## 模块边界

- 构建入口：`AcceleratorLattice/CMakeLists.txt`、`AcceleratorLattice/Make.package`。
- 子模块：`LatticeElements/`。
- 主要文件：`AcceleratorLattice.*`、`LatticeElementFinder.*`、`Drift.*`、`HardEdgedQuadrupole.*`、`HardEdgedPlasmaLens.*`。

## 核心问题

- beamline 元件如何读入、排序、查找和写入 device。
- drift、quadrupole、plasma lens 的物理力如何作用到粒子。
- lattice element finder 如何在粒子推进中快速定位元件。

## 精读顺序

1. `AcceleratorLattice.*`。
2. `LatticeElementBase.*`。
3. `Drift.*`。
4. `HardEdgedQuadrupole.*`。
5. `HardEdgedPlasmaLens.*`。
6. `LatticeElementFinder.*`。

## 输出目标

- `00-lattice-data-model.md`
- `01-lattice-elements.md`
- `02-element-finder-device-path.md`
- `03-validation-map.md`

当前状态：

- `00` 已压实递归 `lattice.elements/line/reverse` 输入图、`z_location -> zs/ze` 几何账本，以及 host/device 双层结构。
- `01` 已压实 `drift` 只贡献几何、`quad/plasmalens` 读取 `dEdx/dBdx`，以及 `hard_edged_fraction()` 的 residence correction。
- `02` 已压实 per-tile `LatticeElementFinder` lookup table、boosted-frame 坐标/场反变换，以及 runtime `E/B` 累加路径。
- `03` 已把 `hard_edged_quadrupoles` 的 lab-frame / boosted-frame / moving-window 三条强 regression 接回主链。

## 验证线索

- accelerator lattice examples/tests。
- `hard_edged_quadrupoles`：lab-frame / boosted-frame / moving-window 三条共享解析 quadrupole-chain 对照。
