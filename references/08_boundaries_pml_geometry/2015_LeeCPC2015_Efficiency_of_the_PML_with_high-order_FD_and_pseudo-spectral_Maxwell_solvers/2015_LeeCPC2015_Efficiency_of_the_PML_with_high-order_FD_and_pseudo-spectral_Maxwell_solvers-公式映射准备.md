# LeeCPC2015 公式映射准备

## 状态

本文件不是论文逐段讲解。当前尚未取得授权 PDF，也没有 MinerU Markdown。因此这里只记录 v0.23 可以先完成的“映射框架”：拿到全文后，应该把哪些论文公式映射到哪些 WarpX 源码层。

## 映射框架

| 论文中应查找的内容 | WarpX / PIC-tutor 对应层 | 当前可核源码 |
|---|---|---|
| 高阶有限差分 Maxwell solver 中 PML 的离散反射率或效率指标 | FDTD/CKC/Nodal PML 的离散导数和 `sigma` profile | `EvolveBPML.cpp`、`EvolveEPML.cpp`、`PML.cpp`、`SigmaBox` |
| pseudo-spectral Maxwell solver 中 PML 的 split-field 更新 | PSATD PML 子域的 split component spectral push | `PML::PushPSATD()`、`PsatdAlgorithmPml.cpp` |
| PML 厚度、吸收剖面和入射角对反射率的影响 | WarpX PML regression 中的 final reflectivity gate | `Examples/Tests/pml/analysis_pml_psatd.py`、`analysis_pml_yee.py`、`analysis_pml_ckc.py` |
| Galilean 或 moving-frame 影响 | `PsatdAlgorithmPml` 内的 `T2=exp(i k_c dot v_gal dt)` 相位因子 | `PsatdAlgorithmPml.cpp:450-453` |
| divergence-cleaning 变量如何进入 PML spectral update | `C23-C25` 与 `F/G` split components | `PsatdAlgorithmPml.cpp:285-369` |

## `C1-C25` 源码分组

- `C1-C9`: 由 `C=cos(c|k|dt)` 和方向余弦组成的投影/耦合系数，用于 split components 的 longitudinal/transverse 重组。
- `C10-C22`: 由 `S_ck=sin(c|k|dt)/(c|k|)` 与 `dt-S_ck` 组成的电磁交叉耦合系数，用于无 PML divergence cleaning 的 split `E/B` 更新。
- `C23-C25`: `i c^2 k_x S_ck`、`i c^2 k_y S_ck`、`i c^2 k_z S_ck`，只在 `dive_cleaning && divb_cleaning` 分支中把 `F/G` 纳入谱推进。

## 后续全文到位后的必做项

1. 逐段阅读 LeeCPC2015，标出论文中的 solver family、PML profile、reflection metric、finite-order order dependence 和 pseudo-spectral update 公式。
2. 判断论文中的 pseudo-spectral PML 公式是否直接对应 WarpX 当前 `PsatdAlgorithmPml.cpp`，还是对应较早版本/不同符号约定。
3. 把公式中的每个 `k`、`C`、`S`、`sigma`、`dt` 和 split component 写入正文符号表，避免和第 6 章主域 PSATD 的 `X1-X4` 系数混淆。
4. 若论文只给出效率/反射率结果而不直接给出 `C1-C25` 形式，则正文应写成“论文提供数值效率证据，源码提供实现公式”，不能把源码公式伪称为论文公式。

