# Lee & Vay 2016 PML / pseudo-spectral solver 中文讲解记录

## 处理状态

本笔记是 v0.22 的取证占位与中文讲解骨架，不是完整逐段 MinerU 讲解。2026-06-29 本机尝试下载 AIP 官方 PDF 时返回 HTTP 403，因此尚未保存 PDF、MinerU Markdown 或图片。后续取得授权 PDF 后，应按项目论文工作流补齐：

1. 保存原始 PDF 到本目录。
2. 使用 `scripts/mineru_convert_stdlib.py` 或 MinerU 标准流程生成 Markdown。
3. 把图片保存在本目录的 `images/`。
4. 将本文扩展为逐段中文讲解，并在首次引用图片处插图。

## 和 WarpX / PIC-tutor 的关系

这篇文献的核心用途是连接三层内容：

- 理论层：PML 不是简单外边界阻尼，而是通过 split-field 或等价的各向异性吸收介质，使入射波在连续介质极限下匹配阻抗并进入吸收层。
- 数值层：高阶有限差分和 pseudo-spectral Maxwell solver 的离散色散不同，PML 的实际反射率不只由连续公式决定，还会受离散导数、时间推进和层厚影响。
- WarpX 层：`PsatdAlgorithmPml.cpp` 中 `C1-C25` 不是普通 FDTD PML 的 `sigma_fac`，而是 PML 子域中 split `E/B/F/G` components 的谱空间解析推进系数；真实阻尼剖面仍在 `PML.cpp` / `SigmaBox` / `ComputePMLFactors*()` 一侧生成。

## 当前可引用证据

WarpX 官方文档 `Docs/source/theory/boundary_conditions.rst` 已给出 PML 理论基线：

- `Perfectly Matched Layer` 小节把 open electromagnetic boundary 追溯到 Berenger PML。
- 文档先写出 2D TE split-field 方程，再推广到 APML 形式。
- 当 `c_x=c_x^*`、`c_y=c_y^*`、广义电导匹配且 `sigma/epsilon_0 = sigma^*/mu_0` 时，连续介质阻抗与真空匹配，理论上无反射。
- 离散化后这种完全匹配不再自动保持，WarpX 文档继续给出指数形式的 split-field leapfrog 更新。

WarpX 源码层的对应关系是：

- `PML.cpp` 和 `SigmaBox` 负责 PML 几何、`sigma/sigma_star` profile、`sigma_fac` / `sigma_cumsum_fac` 阻尼因子。
- `PML::PushPSATD()` 负责普通 Cartesian PML 子域的 split component forward transform、`PsatdAlgorithmPml` 谱推进和 backward transform。
- `PML_RZ::PushPSATD()` 负责 RZ PSATD PML 的径向谱推进。
- `PsatdAlgorithmPml.cpp` 在 `knorm != 0` 时构造 `C=cos(c|k|dt)`、`S_ck=sin(c|k|dt)/(c|k|)`、`inv_k2=1/|k|^2`，再派生 `C1-C22`；开启 `dive_cleaning && divb_cleaning` 时额外构造 `C23-C25` 并推进 `F/G` split components。

## v0.22 写作边界

v0.22 可以据此说明“源码系数属于哪一层”和“还缺哪篇论文的逐段推导”，但不应声称已经从 Lee & Vay 的 PDF 中逐段抽取了公式。完整论文闭环的下一步是取得 `LeeCPC2015` 或 AIP 会议版的授权 PDF，并把 pseudo-spectral PML 反射率/效率公式逐项映射到 WarpX 当前 `PsatdAlgorithmPml.cpp`。

