# LeeCPC2015 公式核对清单

## 状态边界

本清单建立于 2026-06-29。当前仍没有 CPC 2015 授权 PDF、MinerU Markdown、图片或逐段中文讲解，因此这里不是论文内容复述，也不把 WarpX 源码公式伪称为论文公式。

本文件的用途是把后续拿到全文后的核对工作变成可执行表格：每一项都明确“论文应给出的证据”“WarpX 当前源码锚点”“现有 regression 能证明什么”和“正文写作边界”。

## 访问复核

| 路径 | v0.25 复核结果 | 结论 |
|---|---|---|
| CPC DOI `10.1016/j.cpc.2015.04.004` | 搜索仍未找到可直接下载的授权 PDF | 继续作为主引用和待获取全文 |
| OSTI `1246488` | 页面/API 仍是 metadata 与 citation links；未暴露 PDF/full text | 不能把 OSTI 记录写成已取得全文 |
| eScholarship `49m2k3vj` | 本地命令行访问仍受限 | 只能保留为 OpenAlex 指出的 submitted-version 线索 |
| AIP DOI `10.1063/1.4965625` | 官方 `pubs.aip.org/.../050002_1_online.pdf` 以浏览器 UA 访问仍返回 Cloudflare HTTP 403 | 不能作为 MinerU 输入 |

## 后续全文到位后的逐项核对表

| 核对项 | 论文应提供的证据 | WarpX 当前源码锚点 | regression / 文档证据 | 当前写作边界 |
|---|---|---|---|---|
| PML profile 与厚度定义 | `sigma` profile、层数、入射波设置、反射率测量方式 | `Source/BoundaryConditions/PML.cpp`、`Source/BoundaryConditions/SigmaBox.*` | `Examples/Tests/pml/inputs_base_2d`、`analysis_pml_*.py` | 只能写 WarpX PML profile 的实现位置，不能假定论文 profile 完全同构 |
| 高阶 finite-difference Maxwell solver | 高阶 FD stencil、阶数、PML 离散处理、反射率曲线 | `EvolveBPML.cpp`、`EvolveEPML.cpp`、Yee/CKC/nodal 分派 | `test_2d_pml_x_yee`、`test_2d_pml_x_ckc` 的 `<5%` reflectivity gate | 可说明 WarpX 有 FDTD/CKC PML regression，但论文参数空间仍待全文确认 |
| pseudo-spectral PML split-field 更新 | spectral PML update 是否推导到 split components 或 propagator matrix | `PML::PushPSATD()`、`PsatdAlgorithmPml.cpp:195-370` | `test_2d_pml_x_psatd` 的 energy oracle 与 `<1e-6` reflectivity gate | 若论文不给 `C1-C25` 等价式，正文必须把 `C1-C25` 标为 WarpX 实现公式 |
| `C1-C9` 投影结构 | 是否有等价的 longitudinal/transverse 投影或矩阵块 | `PsatdAlgorithmPml.cpp` 中 `C1-C9` | `16-psatd-pml-coefficient-atlas.md` | 当前只能由源码证明，等待论文符号对照 |
| `C10-C22` no-cleaning 交叉耦合 | 是否有无 cleaning 条件下的 split `E/B` cross coupling | `!dive_cleaning && !divb_cleaning` 分支 | `test_2d_pml_x_psatd` 间接覆盖 | regression 只证明组合结果，不证明逐系数 |
| `C23-C25` 与 `F/G` cleaning | 论文是否讨论 divergence cleaning fields | cleaning 分支和 `F/G` split components | `test_2d_pml_x_galilean` 间接覆盖；3D cleaning 目前 checksum-only | 若论文未覆盖，应写成 WarpX 实现扩展 |
| Galilean 相位 `T2` | 论文是否包含 moving/Galilean frame PML | `T2=exp(i k_c dot v_gal dt)` | `test_2d_pml_x_galilean` | 若论文未覆盖，不能归因给 LeeCPC2015 |
| RZ PML | 论文是否涉及 cylindrical/RZ geometry | `PsatdAlgorithmPmlRZ.cpp`、`PML_RZ::PushPSATD()` | `test_rz_pml_psatd` 的 residual gate | 不能拿 RZ regression 证明 Cartesian `C1-C25` |

## 写入正文时的判据

1. 如果论文只给反射率/效率结果，正文应写成“论文提供性能/误差证据，源码提供当前 WarpX 实现公式”。
2. 如果论文给出 pseudo-spectral PML 更新式，必须逐项标出论文符号到 `kx, ky, kz, C, S_ck, T2, C1-C25` 的映射。
3. 如果论文没有 Galilean 或 divergence-cleaning 内容，正文应把 `T2`、`F/G` 和 `C23-C25` 单独列为 WarpX 后续实现分支。
4. 如果论文参数空间和 WarpX regression 不一致，正文只能说 regression 覆盖了当前代码路径，不能说它复现实验论文图。

