# 文献映射

生成来源：`bibliography/warpx-refs.bib` 与 `references/` PDF 文件。

- BibTeX 条目数：251
- 本地 PDF 数：42
- 分类为自动初筛；正式章节必须阅读论文或官方文档后再引用。

## 基础章节优先清单

为了避免第 1 / 2 章继续把基础来源散写在正文里，当前已经另外收口出一份窄清单：

- [基础章节文献清单](/Volumes/PHILIPS/programs/PIC/PIC-tutor/docs/foundations-literature-list.md)

这份清单只处理：

- `Birdsall-Langdon`
- `Hockney-Eastwood`
- `Dawson`
- `Yee`

并明确区分：

- 哪些条目当前已有本地 PDF / MinerU / 中文精读，可直接作为第 1 / 2 章正文证据；
- 哪些条目当前仍只到 acquisition / metadata / abstract-level 边界，不能在基础章节里冒充为已核实的一手来源。

## 当前 MinerU 转换状态

- `references/02_books_lecture_notes/` 下两份开放 lecture notes 已完成论文专属目录化与 MinerU 转 Markdown：
  - `no-year_PICSimulationNotesYoujunHu2019_Particle_In_Cell_PIC_simulation/`
  - `no-year_ComputationalMethodsPlasmaPhysicsNotes_Computational_Methods_in_Plasma_Physics_lecture_notes/`
- 现已额外 materialize 三份核心 PIC foundations 文献：
  - `references/02_books_lecture_notes/1985_BirdsallLangdon_Plasma_physics_via_computer_simulation/`
  - `references/03_pic_foundations/1979_TajimaDawson_Laser_Electron_Accelerator/`
  - `references/03_pic_foundations/1983_Dawson_Particle_simulation_of_plasmas/`
- 这些已 materialize 的目录当前都已具备：
  - 原 PDF
  - MinerU Markdown
  - `images/`
  - 中文讲解笔记骨架
  - `reading-log.md`
- 现已额外 materialize 两份 particle-pusher 核心文献：
  - `references/04_particle_pushers_deposition_shapes/2008_VayPOP2008_Simulation_of_beams_or_plasmas_crossing_at_relativistic_velocity/`
  - `references/04_particle_pushers_deposition_shapes/2017_HigueraPOP2017_Structure-preserving_second-order_integration_of_relativistic_charged_particle_trajectories_in_electromagnetic_fields/`
- 其中 `Birdsall 1985` 因原书 `469` 页超过 MinerU `200` 页限制，当前保留：
  - 原 PDF
  - `split_parts/*.pdf`
  - 三段分卷 Markdown 与 `images/`
- 当前这组核心基础文献里仍未 materialize 的缺口主要收缩为：
  - `Hockney-Eastwood`：已有 BibTeX，但当前在 `Zoteropaper`、`llm-for-zotero-mineru` 和更宽的 `Documents/` 扫描下都未发现本地合法 PDF
  - `TajimaDawson1982`：已有 BibTeX，且现已确认正式出版信息为 *AIP Conference Proceedings* `91(1):69-93`、`Sep 1982`、DOI `10.1063/1.33805`；但当前在 `Zoteropaper`、`llm-for-zotero-mineru`、更宽的 `Documents/` 和 `minerU/md_output` 扫描下都未发现本地 PDF 或 MinerU 产物
    - 另已确认一个 related-but-not-identical 的公开 conference note：
      - FNAL `p169.pdf`
      - *Laser accelerator by plasma waves for ultra-high energies*
      - `T. Tajima` 单作者
    - 这能为主题理解提供旁证，但不能替代 `TajimaDawson1982` 本文的 materialization
- 对 `Hockney-Eastwood` 这条缺口，当前已进一步明确出一组 article-level fallback targets：
  - `Hockney (1971)`：2d2v thermal-plasma long runs，`tau_s / tau_H / N_C / optimum path`
    - confirmed title: *Measurements of collision and heating times in a two-dimensional thermal computer plasma*
    - confirmed DOI path from landing metadata: `10.1016/0021-9991(71)90032-5`
    - abstract-level quantitative claims already visible:
      - `tau_coll / tau_pe = n(\lambda_D^2 + W^2)` at about 20 percent
      - `E^2` fluctuation level `0.12 / n(\lambda_D^2 + W^2)`
      - optimum path `( \omega_{pe}\Delta t )_{opt} = min[ H / (2\lambda_D), 1 ]`
      - `tau_H / tau_coll = K_2 / (H/\lambda_D)^2` with reported `K_2` values for NGP/HNGP/CIC/HCIC
  - `Hockney et al. (1974)`：improved heating times，`K_4 / QPM / potential correction`
    - confirmed title/DOI: *Quiet High-Resolution Computer Models of a Plasma*, `10.1016/0021-9991(74)90010-2`
  - `Eastwood and Hockney (1974)`：force anisotropy 与 shape comparison 图
    - confirmed title/DOI: *Shaping the force law in two-dimensional particle-mesh models*, `10.1016/0021-9991(74)90044-8`
  - `Abe et al. (1975)`：`delta F` heuristic self-heating estimate
  - `Peiravi and Birdsall (1978)`：heating time 对 smoothing cutoff 与 weighting order 的依赖
- 当前这些 fallback article 在本机常用文献目录里也尚未发现现成 PDF/MinerU 产物。
- 当前 web 证据层级已进一步明确：
  - `Hockney 1971 / 1974 / Eastwood-Hockney 1974` 已有正式题名、DOI 和 abstract-level 关键信息
  - 但项目内仍未建立可直接走 MinerU 的本地 full-text PDF
  - `Hockney et al. 1974` 虽然能搜到 ScienceDirect `.../pdf` 端点，但当前环境实际落到 download-preparation / browser-compatibility 页面，不能当成已可 materialize 的正文

## 主题统计

| 主题 | 条目数 |
|---|---:|
| AMR | 2 |
| Esirkepov current deposition | 2 |
| FDTD / Yee Maxwell solver | 9 |
| NCI / spectral stability | 6 |
| PIC foundations / collisions | 7 |
| PIC foundations / plasma simulation history | 3 |
| PML | 2 |
| PSATD | 6 |
| QED | 1 |
| Vay pusher / boosted frame / AMR / PSATD | 71 |
| charge-conserving current deposition | 1 |
| hybrid/fluid | 10 |
| laser/plasma acceleration | 42 |
| particle pusher | 5 |
| particle-mesh foundations | 1 |
| 待分类 | 83 |

## BibTeX 条目映射

| Key | 初步主题 | 计划章节 | 年份 | 作者 | 标题 | DOI |
|---|---|---|---|---|---|---|
| `TajimaDawson1982` | PIC foundations / plasma simulation history | 1-7 | 1982 | Tajima, T. and Dawson, J. M. | Laser accelerator by plasma waves | 10.1063/1.33805 |
| `Esarey1996` | 待分类 | 待定 | 1996 | Esarey, E. and Sprangle, P. and Krall, J. and Ting, A. | Overview of plasma-based accelerator concepts | 10.1109/27.509991 |
| `Birdsall1991` | PIC foundations / collisions | 1-7, 90-92 | 1991 | Birdsall, C. K. | Particle-in-cell charged-particle simulations, plus Monte Carlo collisions with neutral atoms, PIC-MCC | 10.1109/27.106800 |
| `Janssen2016` | 待分类 | 待定 | 2016 | Janssen, J. F. J. and Pitchford L. C. and Hagelaar G. J. M. and van Dijk J. | Evaluation of angular scattering models for electron-neutral collisions in Monte Carlo simulations | 10.1088/0963-0252/25/5/055026 |
| `Lim2007` | 待分类 | 待定 | 2007 | Lim, Chul-Hyun | The interaction of energetic charged particles with gas and boundaries in the particle simulation of plasmas |  |
| `Turner2013` | 待分类 | 待定 | 2013 | Turner, M. M. and Derzsi, A. and Donkó, Z. and Eremin, D. and Kelly, S. J. and Lafleur, T. and Mussenbrock, T. | Simulation benchmarks for low-pressure plasmas: Capacitive discharges | 10.1063/1.4775084 |
| `Nielson1976` | 待分类 | 待定 | 1976 | Clair W. Nielson and H. Ralph Lewis | Controlled Fusion | 10.1016/B978-0-12-460816-0.50015-4 |
| `MUNOZ2018` | hybrid/fluid | 101-104 | 2018 | P. A. Muñoz and N. Jain and P. Kilian and J. Büchner | A new hybrid code (CHIEF) implementing the inertial electron fluid equation without approximation | 10.1016/j.cpc.2017.10.012 |
| `Le2016` | hybrid/fluid | 101-104 | 2016 | Le, A. and Daughton, W. and Karimabadi, H. and Egedal, J. | Hybrid simulations of magnetic reconnection with kinetic ions and fluid electron pressure anisotropy | 10.1063/1.4943893 |
| `LandauVol4` | particle pusher | 22-26 | 2012, publisher=Elsevier, doi = 10.1016/C2009-0-24486-2 | Berestetskii, Vladimir Borisovich and Pitaevskii, Lev Petrovich and Lifshitz, Evgenii Mikhailovich, volume=4, year=2012, | Quantum Electrodynamics: Volume 4, author=Berestetskii, Vladimir Borisovich and Pitaevskii, Lev Petrovich and Lifshitz, Evgenii Mikhailovich, volume=4, year=2012, publisher=Elsevie | 10.1016/C2009-0-24486-2 |
| `Kicsiny2024` | 待分类 | 待定 | 2024, month = Sep, publisher = American Physical Society, doi = 10.1103/PhysRevAccelBeams.27.091001, url = https://link.aps.org/doi/10.1103/PhysRevAccelBeams.27.091001 | Kicsiny, Peter and Buffat, Xavier and Schulte, Daniel and Burkhardt, Helmut and Pieloni, Tatiana and Seidel, Mike, journ | Multiturn simulation of radiative Bhabha scattering in the equivalent photon approximation, author = Kicsiny, Peter and Buffat, Xavier and Schulte, Daniel and Burkhardt, Helmut and | 10.1103/PhysRevAccelBeams.27.091001, url = https://link.aps.org/doi/10.1103/PhysRevAccelBeams.27.091001 |
| `Stanier2020` | hybrid/fluid | 101-104 | 2020 | A. Stanier and L. Chacón and A. Le | A cancellation problem in hybrid particle-in-cell schemes due to finite particle size | 10.1016/j.jcp.2020.109705 |
| `Stix1992` | 待分类 | 待定 | 1992 | Stix, T. H., bdsk-url-1 = https://books.google.com/books?id=OsOWJ8iHpmMC, date-added = 2023-06-29 13:51:16 -0700, date-m | Waves in Plasmas |  |
| `Macchi2013` | laser/plasma acceleration | 87-89, 125 | 2013 | Macchi, Andrea and Borghesi, Marco and Passoni, Matteo | Ion acceleration by superintense laser-plasma interaction | 10.1103/RevModPhys.85.751 |
| `Wilks2001` | PIC foundations / collisions | 1-7, 90-92 | 2001 | Wilks, S. C. and Langdon, A. B. and Cowan, T. E. and Roth, M. and Singh, M. and Hatchett, S. and Key, M. H. and Penningt | Energetic proton generation in ultra-intense laser–solid interactions | 10.1063/1.1333697 |
| `Bulanov2008` | laser/plasma acceleration | 87-89, 125 | 2008 | Bulanov, S. S. and Brantov, A. and Bychenkov, V. Yu. and Chvykov, V. and Kalinchenko, G. and Matsuoka, T. and Rousseau,  | Accelerating monoenergetic protons from ultrathin foils by flat-top laser pulses in the directed-Coulomb-explosion regime | 10.1103/PhysRevE.78.026412 |
| `Dromey2004` | laser/plasma acceleration | 87-89, 125 | 2004 | Dromey, B. and Kar, S. and Zepf, M. and Foster, P. | The plasma mirror—A subpicosecond optical switch for ultrahigh power lasers | 10.1063/1.1646737 |
| `Roedel2010` | laser/plasma acceleration | 87-89, 125 | 2010 | R\"odel, C. and Heyer, M. and Behmke, M. and K\"ubel, M. and J\"ackel, O. and Ziegler, W. and Ehrt, D. and Kaluza, M. C. | High repetition rate plasma mirror for temporal contrast enhancement of terawatt femtosecond laser pulses by three orders of magnitude | 10.1007/s00340-010-4329-7 |
| `SandbergPASC24` | Vay pusher / boosted frame / AMR / PSATD | 24, 42, 55, 72 | 2024 | Sandberg, Ryan and Lehe, Remi and Mitchell, Chad and Garten, Marco and Myers, Andrew and Qiang, Ji and Vay, Jean-Luc and | Synthesizing Particle-In-Cell Simulations through Learning and GPU Computing for Hybrid Particle Accelerator Beamlines | 10.1145/3659914.3659937 |
| `SandbergIPAC23` | Vay pusher / boosted frame / AMR / PSATD | 24, 42, 55, 72 | 2023 | Ryan Sandberg and Remi Lehe and Chad E Mitchell and Marco Garten and Ji Qiang and Jean-Luc Vay and Axel Huebl | Proc. 14th International Particle Accelerator Conference | 10.18429/JACoW-IPAC2023-WEPA101 |
| `HigueraPOP2017` | particle pusher | 22-26 | 2017 | Higuera, A. V. and Cary, J. R. | Structure-preserving second-order integration of relativistic charged particle trajectories in electromagnetic fields | 10.1063/1.4979989 |
| `ShuJCP1988` | 待分类 | 待定 | 1988 | Chi-Wang Shu and Stanley Osher | Efficient implementation of essentially non-oscillatory shock-capturing schemes | 10.1016/0021-9991(88)90177-5 |
| `VanLeerBookChapter1997` | 待分类 | 待定 | 1997 | Van Leer, Bram | Upwind and High-Resolution Schemes | 10.1007/978-3-642-60543-7_3 |
| `Yakimenko2019` | QED | 96-100 | 2019 | Yakimenko, V. and Meuren, S. and Del Gaudio, F. and Baumann, C. and Fedotov, A. and Fiuza, F. and Grismayer, T. and Hoga | Prospect of Studying Nonperturbative QED with Beam-Beam Collisions | 10.1103/PhysRevLett.122.190404 |
| `Groenewald2023` | 待分类 | 待定 | 2023 | Groenewald, R. E. and Veksler, A. and Ceccherini, F. and Necas, A. and Nicks, B. S. and Barnes, D. C. and Tajima, T. and | Accelerated kinetic model for global macro stability studies of high-beta fusion reactors | 10.1063/5.0178288 |
| `PerezPOP2012` | 待分类 | 待定 | 2012 | Pérez, F. and Gremillet, L. and Decoster, A. and Drouin, M. and Lefebvre, E. | Improved modeling of relativistic collisions and collisional ionization in particle-in-cell codes | 10.1063/1.4742167 |
| `HigginsonJCP2019` | 待分类 | 待定 | 2019 | Drew Pitney Higginson and Anthony Link and Andrea Schmidt | A pairwise nuclear fusion algorithm for weighted particle-in-cell plasma simulations | 10.1016/j.jcp.2019.03.020 |
| `VerboncoeurJCP2001` | 待分类 | 待定 | 2001 | J.P. Verboncoeur | Symmetric Spline Weighting for Charge and Current Density in Particle Simulation | 10.1006/jcph.2001.6923 |
| `MuravievCPC2021` | 待分类 | 待定 | 2021 | A. Muraviev and A. Bashinov and E. Efimenko and V. Volokitin and I. Meyerov and A. Gonoskov | Strategies for particle resampling in PIC simulations | 10.1016/j.cpc.2021.107826 |
| `AkturkOE2004` | 待分类 | 待定 | 2004 | Selcuk Akturk and Xun Gu and Erik Zeek and Rick Trebino | Pulse-front tilt caused by spatial and temporal chirp | 10.1364/OPEX.12.004399 |
| `XiaoIEEE2005` | 待分类 | 待定 | 2005 | Tian Xiao and Qing Huo Liu | 2005 IEEE Antennas and Propagation Society International Symposium | 10.1109/APS.2005.1551259 |
| `GrismayerNJP2021` | 待分类 | 待定 | 2021 | T Grismayer and R Torres and P Carneiro and F Cruz and R A Fonseca and L O Silva | Quantum Electrodynamics vacuum polarization solver | 10.1088/1367-2630/ac2004 |
| `QiangPhysRevSTAB2006` | 待分类 | 待定 | 2006, month = Apr, publisher = American Physical Society, doi = 10.1103/PhysRevSTAB.9.044204 | Qiang, Ji and Lidia, Steve and Ryne, Robert D. and Limborg-Deprey, Cecile, journal = Phys. Rev. ST Accel. Beams, volume  | Three-dimensional quasistatic model for high brightness beam dynamics simulation, author = Qiang, Ji and Lidia, Steve and Ryne, Robert D. and Limborg-Deprey, Cecile, journal = Phys | 10.1103/PhysRevSTAB.9.044204 |
| `QiangPhysRevSTAB2006err` | 待分类 | 待定 | 2007, month = Dec, publisher = American Physical Society, doi = 10.1103/PhysRevSTAB.10.129901 | Qiang, Ji and Lidia, Steve and Ryne, Robert D. and Limborg-Deprey, Cecile, journal = Phys. Rev. ST Accel. Beams, volume  | Erratum: Three-dimensional quasistatic model for high brightness beam dynamics simulation [Phys. Rev. ST Accel. Beams 9, 044204 (2006)], author = Qiang, Ji and Lidia, Steve and Ryn | 10.1103/PhysRevSTAB.10.129901 |
| `Wiedemann2015` | 待分类 | 待定 | 2015 | Wiedemann, H., isbn = 978-3-319-18317-6, publisher = Springer Cham, title = Particle Accelerator Physics, doi = 10.1007/ | Particle Accelerator Physics, doi = 10.1007/978-3-319-18317-6, year = 2015 | 10.1007/978-3-319-18317-6, year = 2015 |
| `Vranic2015` | 待分类 | 待定 | 2015, issn = 0010-4655, doi = 10.1016/j.cpc.2015.01.020 | M. Vranic and T. Grismayer and J.L. Martins and R.A. Fonseca and L.O. Silva, journal = Computer Physics Communications,  | Particle merging algorithm for PIC codes, author = M. Vranic and T. Grismayer and J.L. Martins and R.A. Fonseca and L.O. Silva, journal = Computer Physics Communications, volume =  | 10.1016/j.cpc.2015.01.020 |
| `Fallahi2020` | laser/plasma acceleration | 87-89, 125 | 2020, eprint=2009.13645, archivePrefix=arXiv, primaryClass=physics.acc-ph | Arya Fallahi, year=2020, eprint=2009.13645, archivePrefix=arXiv, primaryClass=physics.acc-ph | MITHRA 2.0: A Full-Wave Simulation Tool for Free Electron Lasers, author=Arya Fallahi, year=2020, eprint=2009.13645, archivePrefix=arXiv, primaryClass=physics.acc-ph |  |
| `VayFELA2009` | Vay pusher / boosted frame / AMR / PSATD | 24, 42, 55, 72 | 2009, month = 4 | Fawley, William M and Vay, Jean-Luc, journal = , abstractNote = Numerical simulation of some systems containing charged  | FULL ELECTROMAGNETIC SIMULATION OF FREE-ELECTRON LASER AMPLIFIER PHYSICS VIA THE LORENTZ-BOOSTED FRAME APPROACH, author = Fawley, William M and Vay, Jean-Luc, journal = , abstractN |  |
| `VayFELB2009` | Vay pusher / boosted frame / AMR / PSATD | 24, 42, 55, 72 | 2009, month = 01, abstract = "Recently [1] it has been pointed out that numerical simulation of some systems containing charged particles with highly relativistic directed motion can by speeded up by orders of magnitude by choice of the proper Lorentz boosted frame. A particularly good example is that of short wavelength free‐electron lasers (FELs) in which a high energy (E0⩾250 MeV) electron beam interacts with a static magnetic undulator. In the optimal boost frame with Lorentz factor γF, the red‐shifted FEL radiation and blue shifted undulator have identical wavelengths and the number of required time‐steps (presuming the Courant condition applies) decreases by a factor of γF2 for fully electromagnetic simulation.We have adapted the WARP code [2] to apply this method to several FEL problems including coherent spontaneous emission (CSE) from pre‐bunched e‐beams, and strong exponential gain in a single pass amplifier configuration. We discuss our results and compare with those from the “standard” FEL simulation approach which adopts the eikonal approximation for propagation of the radiation field.", issn = 0094-243X, doi = 10.1063/1.3080930 | Fawley, W. M. and Vay, J.‐L., title = "Use of the Lorentz‐Boosted Frame Transformation to Simulate Free‐Electron Laser A | Use of the Lorentz‐Boosted Frame Transformation to Simulate Free‐Electron Laser Amplifier Physics", journal = AIP Conference Proceedings, volume = 1086, number = 1, pages = 346-350 | 10.1063/1.3080930 |
| `Barnes2021` | 待分类 | 待定 | 2021, issn = 0021-9991, doi = 10.1016/j.jcp.2020.109852, url = https://www.sciencedirect.com/science/article/pii/S0021999120306264 | D.C. Barnes, journal = Journal of Computational Physics, volume = 424, pages = 109852, year = 2021, issn = 0021-9991, do | Improved C1 shape functions for simplex meshes, author = D.C. Barnes, journal = Journal of Computational Physics, volume = 424, pages = 109852, year = 2021, issn = 0021-9991, doi = | 10.1016/j.jcp.2020.109852, url = https://www.sciencedirect.com/science/article/pii/S0021999120306264 |
| `Rhee1987` | 待分类 | 待定 | 1987, month = 02, issn = 0034-6748, doi = 10.1063/1.1139314, eprint = https://pubs.aip.org/aip/rsi/article-pdf/58/2/240/19154912/240\_1\_online.pdf | Rhee, M. J. and Schneider, R. F. and Weidman, D. J., title = "Simple time‐resolving Thomson spectrometer", journal = Rev | Simple time‐resolving Thomson spectrometer", journal = Review of Scientific Instruments, volume = 58, number = 2, pages = 240-244, year = 1987, month = 02, issn = 0034-6748, doi =  | 10.1063/1.1139314, eprint = https://pubs.aip.org/aip/rsi/article-pdf/58/2/240/19154912/240\_1\_online.pdf |
| `holmstrom2013handlingvacuumregionshybrid` | hybrid/fluid | 101-104 | 2013, eprint=1301.0272, archivePrefix=arXiv, primaryClass=physics.space-ph | M. Holmstrom, year=2013, eprint=1301.0272, archivePrefix=arXiv, primaryClass=physics.space-ph | Handling vacuum regions in a hybrid plasma solver, author=M. Holmstrom, year=2013, eprint=1301.0272, archivePrefix=arXiv, primaryClass=physics.space-ph |  |
| `QuickpicParallel` | NCI / spectral stability | 53-56 | 2009 | Feng, B. and Huang, C. and Decyk, V. and Mori, W. B. and Muggli, P. and Katsouleas, T. | Enhancing parallel quasi-static particle-in-cell simulations with a pipelining algorithm | 10.1016/j.jcp.2009.04.019 |
| `HockneyEastwoodBook` | particle-mesh foundations | 6, 36 | 1988 | Hockney, R W and Eastwood, J W | Computer simulation using particles |  |
| `Parkerjcp1991` | PIC foundations / collisions | 1-7, 90-92 | 1991 | Parker, S E and Birdsall, C K | Numerical Error In Electron Orbits With Large Omega-Ce Delta-T | 10.1016/0021-9991(91)90040-R |
| `Fawleyipac10` | Vay pusher / boosted frame / AMR / PSATD | 24, 42, 55, 72 | 2010 | Fawley, W M and Vay, J.-L. | Proc. Ipac 2010, Paper Tupec064 |  |
| `Godfreyjcp74` | NCI / spectral stability | 53-56 | 1974 | Godfrey, B B | Numerical Cherenkov Instabilities In Electromagnetic Particle Codes | 10.1016/0021-9991(74)90076-X |
| `Quickpic` | laser/plasma acceleration | 87-89, 125 | 2006 | Huang, C and Decyk, V K and Ren, C and Zhou, M and Lu, W and Mori, W B and Cooley, J H and Antonsen, Jr, T M and Katsoul | Quickpic: A Highly Efficient Particle-In-Cell Code For Modeling Wakefield Acceleration In Plasmas | 10.1016/J.Jcp.2006.01.039 |
| `Lundprstab2009` | 待分类 | 待定 | 2009 | Lund, Steven M and Kikuchi, Takashi and Davidson, Ronald C | Generation Of Initial Kinetic Distributions For Simulation Of Long-Pulse Charged Particle Beams With High Space-Charge Intensity | 10.1103/Physrevstab.12.114801 |
| `CowanPRSTAB13` | 待分类 | 待定 | 2013 | Cowan, Benjamin M and Bruhwiler, David L and Cary, John R and Cormier-Michel, Estelle and Geddes, Cameron G R | Generalized algorithm for control of numerical dispersion in explicit time-domain electromagnetic simulations | 10.1103/PhysRevSTAB.16.041303 |
| `Esareyrmp09` | laser/plasma acceleration | 87-89, 125 | 2009 | Esarey, E and Schroeder, C B and Leemans, W P | Physics Of Laser-Driven Plasma-Based Electron Accelerators | 10.1103/Revmodphys.81.1229 |
| `YuPRL2014` | Vay pusher / boosted frame / AMR / PSATD | 24, 42, 55, 72 | 2014 | Yu, L.-L. and Esarey, E and Schroeder, C B and Vay, J.-L. and Benedetti, C and Geddes, C G R and Chen, M and Leemans, W  | Two-Color Laser-Ionization Injection | 10.1103/PhysRevLett.112.125001 |
| `Vaynim2007` | Vay pusher / boosted frame / AMR / PSATD | 24, 42, 55, 72 | 2007 | Vay, J.-L. and Furman, M A and Seidl, P A and Cohen, R H and Friedman, A and Grote, D P and Covo, M Kireeff and Molvik,  | Self-Consistent Simulations Of Heavy-Ion Beams Interacting With Electron-Clouds | 10.1016/J.Nima.2007.02.013 |
| `Vay2000` | Vay pusher / boosted frame / AMR / PSATD | 24, 42, 55, 72 | 2000 | Vay, Jean-Luc | A New Absorbing Layer Boundary Condition for the Wave Equation | 10.1006/jcph.2000.6623 |
| `Vayjcp2011` | Vay pusher / boosted frame / AMR / PSATD | 24, 42, 55, 72 | 2011 | Vay, J-L and Geddes, C G R and Cormier-Michel, E and Grote, D P | Numerical Methods For Instability Mitigation In The Modeling Of Laser Wakefield Accelerators In A Lorentz-Boosted Frame | 10.1016/J.Jcp.2011.04.003 |
| `Krallpre1993` | laser/plasma acceleration | 87-89, 125 | 1993 | Krall, J and Ting, A and Esarey, E and Sprangle, P | Enhanced Acceleration In A Self-Modulated-Laser Wake-Field Accelerator | 10.1103/Physreve.48.2157 |
| `Dennisw1997585` | 待分类 | 待定 | 1997 | Dennis W. Hewett | The Embedded Curved Boundary Method For Orthogonal Simulation Meshes | 10.1006/Jcph.1997.5835 |
| `Habib2016` | Vay pusher / boosted frame / AMR / PSATD | 24, 42, 55, 72 | 2016 | Habib, Salman and Roser, Robert and Gerber, Richard and Antypas, Katie and Riley, Katherine and Williams, Tim and Wells, | ASCR/HEP Exascale Requirements Review Report |  |
| `Shadwickpop09` | laser/plasma acceleration | 87-89, 125 | 2009 | Shadwick, B A and Schroeder, C B and Esarey, E | Nonlinear Laser Energy Depletion In Laser-Plasma Accelerators | 10.1063/1.3124185 |
| `Leemansaac2010` | Vay pusher / boosted frame / AMR / PSATD | 24, 42, 55, 72 | 2010 | Leemans, W P and Duarte, R and Esarey, E and Fournier, S and Geddes, C G R and Lockhart, D and Schroeder, C B and Toth,  | The Berkeley Lab Laser Accelerator (Bella): A 10 GeV Laser Plasma Accelerator | 10.1063/1.3520352 |
| `Marderjcp87` | 待分类 | 待定 | 1987 | Marder, B | A Method For Incorporating Gauss Law Into Electromagnetic Pic Codes | 10.1016/0021-9991(87)90043-X |
| `Ohmurapiers2010` | PSATD | 53-56 | 2010 | Ohmura, Y and Okamura, Y | Staggered Grid Pseudo-Spectral Time-Domain Method For Light Scattering Analysis |  |
| `Adamjcp1982` | PIC foundations / collisions | 1-7, 90-92 | 1982 | Adam, J C and Serveniere, Ag and Langdon, A B | Electron Sub-Cycling In Particle Simulation Of Plasma | 10.1016/0021-9991(82)90076-6 |
| `Tajimaprl79` | PIC foundations / plasma simulation history | 1-7 | 1979 | Tajima, T and Dawson, J M | Laser Electron-Accelerator | 10.1103/PhysRevLett.43.267 |
| `Benedetti09` | laser/plasma acceleration | 87-89, 125 | 2009 | C. Benedetti and P. Londrillo and V. Petrillo and L. Serafini and A. Sgattoni and P. Tomassini and G. Turchetti | PIC simulations of the production of high-quality electron beams via laser–plasma interaction | 10.1016/j.nima.2009.05.064 |
| `Godfreyicnsp80` | NCI / spectral stability | 53-56 | 1980 | Godfrey, B B | Proc. Ninth Conf. On Num. Sim. Of Plasmas |  |
| `Blumenfeld2007` | laser/plasma acceleration | 87-89, 125 | 2007 | Blumenfeld, Ian and Clayton, Christopher E and Decker, Franz-Josef and Hogan, Mark J and Huang, Chengkun and Ischebeck,  | Energy doubling of 42[thinsp]GeV electrons in a metre-scale plasma wakefield accelerator | 10.1038/nature05538 |
| `Vayicap2002` | Vay pusher / boosted frame / AMR / PSATD | 24, 42, 55, 72 | 2005 | Vay, J-L and Friedman, A and Grote, D P | Computational Accelerator Physics 2002 |  |
| `VayFRACAD2014` | Vay pusher / boosted frame / AMR / PSATD | 24, 42, 55, 72 | 2014 | Vay, Jean-Luc and Godfrey, Brendan B | Modeling of relativistic plasmas with the Particle-In-Cell method | 10.1016/j.crme.2014.07.006 |
| `AndriyashPoP2016` | PSATD | 53-56 | 2016 | Andriyash, Igor A. and Lehe, Remi and Lifschitz, Agustin | Laser-plasma interactions with a Fourier-Bessel particle-in-cell method | 10.1063/1.4943281 |
| `DawsonRMP83` | PIC foundations / plasma simulation history | 1-7 | 1983 | Dawson, J M | Particle Simulation Of Plasmas | 10.1103/RevModPhys.55.403 |
| `Qiang` | 待分类 | 待定 |  | Qiang, Ji | LCLS-II Accelerator Physics meeting, SLAC, April 13, 2016. |  |
| `Geddespac09` | 待分类 | 待定 | 2009 | C. G. R. Geddes and E. Cormier-Michel and E. Esarey and C. B. Schroeder and W. P. Leemans | Proc. Particle Accelerator Conference |  |
| `LotovPRSTAB2003` | laser/plasma acceleration | 87-89, 125 | 2003 | Lotov, K. V. | Fine wakefield structure in the blowout regime of plasma wakefield accelerators | 10.1103/PhysRevSTAB.6.061301 |
| `Godfreyjcp75` | NCI / spectral stability | 53-56 | 1975 | Godfrey, B B | Canonical Momenta And Numerical Instabilities In Particle Codes |  |
| `Kishekprl2012` | 待分类 | 待定 | 2012 | Kishek, R A | Ping-Pong Modes: A New Form Of Multipactor | 10.1103/Physrevlett.108.035003 |
| `Zhang2016` | AMR | 71-76 | 2016 | Zhang, Weiqun and Almgren, Ann and Day, Marcus and Nguyen, Tan and Shalf, John and Unat, Didem | BoxLib with Tiling: An AMR Software Framework |  |
| `Cohennim2009` | Vay pusher / boosted frame / AMR / PSATD | 24, 42, 55, 72 | 2009 | Cohen, R H and Friedman, A and Grote, D P and Vay, J-L | An Implicit ``Drift-Lorentz\''\ Mover For Plasma And Beam Simulations | 10.1016/J.Nima.2009.03.083 |
| `Osiris` | 待分类 | 待定 | 2002 | Fonseca, R. A. and Silva, L. O. and Tsung, F. S. and Decyk, V. K. and Lu, W. and Ren, C. and Mori, W. B. and Deng, S. an | Computational Science --- ICCS 2002 | 10.1007/3-540-47789-6_36 |
| `LifschitzJCP2009` | laser/plasma acceleration | 87-89, 125 | 2009 | Lifschitz, A F and Davoine, X and Lefebvre, E and Faure, J and Rechatin, C and Malka, V | Particle-in-Cell modelling of laser-plasma interaction using Fourier decomposition | 10.1016/j.jcp.2008.11.017 |
| `Nurmbergjpcs2010` | laser/plasma acceleration | 87-89, 125 | 2010 | N\"Urnberg, Frank and Friedman, A and Grote, D P and Harres, K and Logan, B G and Schollmeier, M and Roth, M | Warp Simulations For Capture And Control Of Laser-Accelerated Proton Beams | 10.1088/1742-6596/244/2/022052 |
| `GeddesPRL2008` | 待分类 | 待定 | 2008 | Geddes, C G R and Nakamura, K and Plateau, G R and Toth, Cs. and Cormier-Michel, E and Esarey, E and Schroeder, C B and  | Plasma-Density-Gradient Injection of Low Absolute-Momentum-Spread Electron Bunches | 10.1103/PhysRevLett.100.215004 |
| `Vay2001` | FDTD / Yee Maxwell solver | 46-50 | 2001 | Vay, Jean-Luc | An Extended FDTD Scheme for the Wave Equation: Application to Multiscale Electromagnetic Simulation |  |
| `Huebl2015` | Vay pusher / boosted frame / AMR / PSATD | 24, 42, 55, 72 | 2015 | Huebl, Axel and Lehe, Remi and Vay, Jean-Luc and Grote, David P. and Sbalzarini, Ivo and Kuschel, Stephan and Bussmann,  | openPMD: A meta data standard for particle and mesh based data. | 10.5281/zenodo.591699 |
| `Huangscidac09` | Vay pusher / boosted frame / AMR / PSATD | 24, 42, 55, 72 | 2009 | Huang, C and An, W and Decyk, V K and Lu, W and Mori, W B and Tsung, F S and Tzoufras, M and Morshed, S and Antonsen, T  | Recent Results And Future Challenges For Large Scale Particle-In-Cell Simulations Of Plasma-Based Accelerator Concepts |  |
| `Fawleyfel10` | Vay pusher / boosted frame / AMR / PSATD | 24, 42, 55, 72 | 2010 | Fawley, W M and Vay, J.-L. | Proc. Fel 2010, Paper Mopb01 |  |
| `Cormierprstab10` | laser/plasma acceleration | 87-89, 125 |  | Cormier-Michel, E and Esarey, E and Geddes, C G R and Schroeder, C B and Leemans, W P | Propagation Of Higher Order Modes In Plasma Channels And Shaping Of The Transverse Field In Laser Plasma Accelerators |  |
| `Yee` | FDTD / Yee Maxwell solver | 46-50 | 1966 | Yee, K S | Numerical Solution Of Initial Boundary Value Problems Involving Maxwells Equations In Isotropic Media | 10.1109/TAP.1966.1138693 |
| `GodfreyJCP2013` | Vay pusher / boosted frame / AMR / PSATD | 24, 42, 55, 72 | 2013 | Godfrey, Brendan B and Vay, Jean-Luc | Numerical stability of relativistic beam multidimensional \PIC\ simulations employing the Esirkepov algorithm | 10.1016/j.jcp.2013.04.006 |
| `Cormieraac08` | 待分类 | 待定 | 2009 | Cormier-Michel, E and Geddes, C G R and Esarey, E and Schroeder, C B and Bruhwiler, D L and Paul, K and Cowan, B and Lee | Aip Conference Proceedings |  |
| `Bruhwileraac08` | Vay pusher / boosted frame / AMR / PSATD | 24, 42, 55, 72 | 2009 | Bruhwiler, D L and Cary, J R and Cowan, B M and Paul, K and Geddes, C G R and Mullowney, P J and Messmer, P and Esarey,  | Aip Conference Proceedings |  |
| `Vaynim2005` | Vay pusher / boosted frame / AMR / PSATD | 24, 42, 55, 72 | 2005 | Vay, J-L and Friedman, A and Grote, D P | Application Of Adaptive Mesh Refinement To Pic Simulations In Heavy Ion Fusion | 10.1016/J.Nima.2005.01.232 |
| `BulanovSV2014` | Esirkepov current deposition | 41 | 2014 | Bulanov, S V and Wilkens, J J and Esirkepov, T Zh and Korn, G and Kraft, G and Kraft, S D and Molls, M and Khoroshkov, V | Laser ion acceleration for hadron therapy |  |
| `Furmanprstab2002` | 待分类 | 待定 | 2002 | Furman, M A and Pivi, M T F | Probabilistic Model For The Simulation Of Secondary Electron Emission | 10.1103/Physrevstab.5.124404 |
| `Qiang2014` | 待分类 | 待定 | 2014 | Qiang, J. and Corlett, J. and Mitchell, C. E. and Papadopoulos, C. F. and Penn, G. and Placidi, M. and Reinsch, M. and R | Start-to-end simulation of x-ray radiation of a next generation light source using the real number of electrons | 10.1103/PhysRevSTAB.17.030701 |
| `Fawleyaac08` | Vay pusher / boosted frame / AMR / PSATD | 24, 42, 55, 72 | 2009 | Fawley, W M and Vay, J.-L. | Aip Conference Proceedings |  |
| `Bruhwilerpc08` | 待分类 | 待定 | 2008 | Bruhwiler, D L | No Title |  |
| `Yu2014` | PSATD | 53-56 | 2014 | Yu, Peicheng and Xu, Xinlu and Decyk, Viktor K. and An, Weiming and Vieira, Jorge and Tsung, Frank S. and Fonseca, Ricar | Modeling of laser wakefield acceleration in Lorentz boosted frame using EM-PIC code with spectral solver | 10.1016/j.jcp.2014.02.016 |
| `Vaypop2011` | Vay pusher / boosted frame / AMR / PSATD | 24, 42, 55, 72 | 2011 | Vay, J.-L. and Geddes, C G R and Esarey, E and Schroeder, C B and Leemans, W P and Cormier-Michel, E and Grote, D P | Modeling Of 10 GeV-1 TeV Laser-Plasma Accelerators Using Lorentz Boosted Simulations | 10.1063/1.3663841 |
| `LehePRSTAB13` | PSATD | 53-56 | 2013 | Lehe, R and Lifschitz, A and Thaury, C and Malka, V and Davoine, X | Numerical growth of emittance in simulations of laser-wakefield acceleration | 10.1103/PhysRevSTAB.16.021301 |
| `Langdoncpc92` | PIC foundations / collisions | 1-7, 90-92 | 1992 | Langdon, A B | On Enforcing Gauss Law In Electromagnetic Particle-In-Cell Codes | 10.1016/0010-4655(92)90105-8 |
| `Colellajcp2010` | AMR | 71-76 | 2010 | Colella, Phillip and Norgaard, Peter C | Controlling Self-Force Errors At Refinement Boundaries For Amr-Pic | 10.1016/J.Jcp.2009.07.004 |
| `Coleieee1997` | FDTD / Yee Maxwell solver | 46-50 | 1997 | Cole, J. B. | A High-Accuracy Realization Of The Yee Algorithm Using Non-Standard Finite Differences | 10.1109/22.588615 |
| `Coleieee2002` | FDTD / Yee Maxwell solver | 46-50 | 2002 | Cole, J. B. | High-Accuracy Yee Algorithm Based On Nonstandard Finite Differences: New Developments And Verifications | 10.1109/Tap.2002.801268 |
| `HajimaNIM09` | laser/plasma acceleration | 87-89, 125 | 2009 | Hajima, R and Kikuzawa, N and Nishimori, N and Hayakawa, T and Shizuma, T and Kawase, K and Kando, M and Minehara, E and | Detection of radioactive isotopes by using laser Compton scattered gamma-ray beams | 10.1016/j.nima.2009.05.063 |
| `MatlisJOSA11` | 待分类 | 待定 | 2011 | Matlis, N H and Plateau, G R and van Tilborg, J and Leemans, W P | Single-shot spatiotemporal measurements of ultrashort THz waveforms using temporal electric-field cross correlation | 10.1364/JOSAB.28.000023 |
| `Quickpic2` | 待分类 | 待定 | 2013 | An, Weiming and Decyk, Viktor K. and Mori, Warren B. and Antonsen, Thomas M. | An improved iteration loop for the three dimensional quasi-static particle-in-cell algorithm: QuickPIC | 10.1016/j.jcp.2013.05.020 |
| `Cowanpriv2010` | 待分类 | 待定 | 2010 | Cowan, B | No Title |  |
| `Geddesscidac09` | Vay pusher / boosted frame / AMR / PSATD | 24, 42, 55, 72 | 2009 | Geddes, Cameron G.R. and Cormier-Michel, Estelle and Esarey, Eric H and Schroeder, Carl B and Vay, Jean-Luc and Leemans, | Scidac Review 13 |  |
| `Gomberoffpop2007` | Vay pusher / boosted frame / AMR / PSATD | 24, 42, 55, 72 | 2007 | Gomberoff, K and Fajans, J and Friedman, A and Grote, D and Vay, J.-L. and Wurtele, J S | Simulations Of Plasma Confinement In An Antihydrogen Trap | 10.1063/1.2778420 |
| `Morapop1997` | laser/plasma acceleration | 87-89, 125 | 1997 | Mora, P and Antonsen, T M | Kinetic Modeling Of Intense, Short Laser Pulses Propagating In Tenuous Plasmas | 10.1063/1.872134 |
| `Cowanaac08` | 待分类 | 待定 | 2009 | Cowan, B and Bruhwiler, D and Cormier-Michel, E and Esarey, E and Geddes, C G R and Messmer, P and Paul, K | Aip Conference Proceedings |  |
| `Cohenprstab2009` | Vay pusher / boosted frame / AMR / PSATD | 24, 42, 55, 72 | 2009 | Cohen, R H and Friedman, A and Grote, D P and Vay, J-L | An Implicit ``Drift-Lorentz\''\ Mover For Plasma And Beam Simulations | 10.1016/J.Nima.2009.03.083 |
| `Kaganovich2012` | Vay pusher / boosted frame / AMR / PSATD | 24, 42, 55, 72 | 2012 | Kaganovich, Igor D. and Massidda, Scott and Startsev, Edward A. and Davidson, Ronald C. and Vay, Jean-Luc and Friedman,  | Effects of errors in velocity tilt on maximum longitudinal compression during neutralized drift compression of intense beam pulses: I. General description |  |
| `VincentiCPC2017` | Vay pusher / boosted frame / AMR / PSATD | 24, 42, 55, 72 | 2017 | H. Vincenti and M. Lobet and R. Lehe and R. Sasanka and J.-L. Vay | An efficient and portable SIMD algorithm for charge/current deposition in Particle-In-Cell codes | 10.1016/j.cpc.2016.08.023 |
| `Vaypop2008` | Vay pusher / boosted frame / AMR / PSATD | 24, 42, 55, 72 | 2008 | Vay, J-L | Simulation Of Beams Or Plasmas Crossing At Relativistic Velocity | 10.1063/1.2837054 |
| `Wieland2016` | 待分类 | 待定 | 2016 | Wieland, Volkmar and Pohl, Martin and Niemiec, Jacek and Rafighi, Iman and Nishikawa, Ken-Ichi | NONRELATIVISTIC PERPENDICULAR SHOCKS MODELING YOUNG SUPERNOVA REMNANTS: NONSTATIONARY DYNAMICS AND PARTICLE ACCELERATION AT FORWARD AND REVERSE SHOCKS | 10.3847/0004-637X/820/1/62 |
| `Vay` | Vay pusher / boosted frame / AMR / PSATD | 24, 42, 55, 72 |  | Vay, J.-L. | Traditional HPC needs: particle accelerators |  |
| `Faurenature04` | laser/plasma acceleration | 87-89, 125 | 2004 | Faure, J and Glinec, Y and Pukhov, A and Kiselev, S and Gordienko, S and Lefebvre, E and Rousseau, J P and Burgy, F and  | A Laser-Plasma Accelerator Producing Monoenergetic Electron Beams | 10.1038/Nature02963 |
| `Greenwoodjcp04` | 待分类 | 待定 | 2004 | Greenwood, A D and Cartwright, K L and Luginsland, J W and Baca, E A | On The Elimination Of Numerical Cerenkov Radiation In Pic Simulations | 10.1016/J.Jcp.2004.06.021 |
| `GodfreyIEEE2014` | Vay pusher / boosted frame / AMR / PSATD | 24, 42, 55, 72 | 2014 | Godfrey, Brendan B. and Vay, Jean-Luc and Haber, Irving | Numerical stability improvements for the pseudospectral EM PIC algorithm | 10.1109/TPS.2014.2310654 |
| `Cowanicap09` | 待分类 | 待定 | 2009 | Cowan, B | Poster \$10\^\Th\\$ Internat. Comput. Accel. Phys. Conf. |  |
| `Wuprstab2011` | 待分类 | 待定 | 2011 | Wu, H-C and Meyer-Ter-Vehn, J and Hegelich, B M and Fernandez, J C | Nonlinear Coherent Thomson Scattering From Relativistic Electron Sheets As A Means To Produce Isolated Ultrabright Attosecond X-Ray Pulses | 10.1103/Physrevstab.14.070702 |
| `VayAAC2010` | Vay pusher / boosted frame / AMR / PSATD | 24, 42, 55, 72 | 2010 | Vay, J.‐L. and Geddes, C. G. R. and Benedetti, C. and Bruhwiler, D. L. and Cormier‐Michel, E. and Cowan, B. M. and Cary, | Modeling Laser Wakefield Accelerators In A Lorentz Boosted Frame | 10.1063/1.3520322 |
| `Vayprl07` | Vay pusher / boosted frame / AMR / PSATD | 24, 42, 55, 72 | 2007 | Vay, J.-L. | Noninvariance Of Space- And Time-Scale Ranges Under A Lorentz Transformation And The Implications For The Study Of Relativistic Interactions |  |
| `VayJCP2013` | Vay pusher / boosted frame / AMR / PSATD | 24, 42, 55, 72 | 2013 | Vay, Jean-Luc and Haber, Irving and Godfrey, Brendan B. | A domain decomposition method for pseudo-spectral electromagnetic simulations of plasmas | 10.1016/j.jcp.2013.03.010 |
| `Kaganovichpop2004` | 待分类 | 待定 | 2004 | Kaganovich, I D and Startsev, E A and Davidson, R C | Nonlinear Plasma Waves Excitation By Intense Ion Beams In Background Plasma | 10.1063/1.1758945 |
| `Cohenpop2005` | Vay pusher / boosted frame / AMR / PSATD | 24, 42, 55, 72 | 2005 | Cohen, R H and Friedman, A and Covo, M K and Lund, S M and Molvik, A W and Bieniosek, F M and Seidl, P A and Vay, J-L an | Simulating Electron Clouds In Heavy-Ion Accelerators | 10.1063/1.1882292 |
| `Vayfed1996` | Vay pusher / boosted frame / AMR / PSATD | 24, 42, 55, 72 | 1996 | Vay, J-L and Deutsch, C | A Three-Dimensional Electromagnetic Particle-In-Cell Code To Simulate Heavy Ion Beam Propagation In The Reaction Chamber | 10.1016/S0920-3796(96)00502-9 |
| `Fengjcp09` | NCI / spectral stability | 53-56 | 2009 | Feng, B and Huang, C and Decyk, V and Mori, W B and Muggli, P and Katsouleas, T | Enhancing Parallel Quasi-Static Particle-In-Cell Simulations With A Pipelining Algorithm | 10.1016/j.jcp.2009.04.019 |
| `BESAC2013` | 待分类 | 待定 | 2013 | BESAC | Directing Matter and Energy: Five Challenges for Science and the Imagination A | 10.1037/a0034573 |
| `Prostprstab2005` | 待分类 | 待定 | 2005 | Prost, L R and Seidl, P A and Bieniosek, F M and Celata, C M and Faltens, A and Baca, D and Henestroza, E and Kwan, J W  | High Current Transport Experiment For Heavy Ion Inertial Fusion | 10.1103/Physrevstab.8.020101 |
| `Bassetti_Erskine` | 待分类 | 待定 | 1980 | Bassetti, M and Erskine, G A | Cern Report No. Cern-Isrth/80-06 |  |
| `Godfrey2013PPPS` | Vay pusher / boosted frame / AMR / PSATD | 24, 42, 55, 72 | 2013 | Godfrey, B.\~B. and Haber, I and Vay, J.-L. | Proc. IEEE Pulsed Power and Plasma Science Conference |  |
| `Vaypop04` | Vay pusher / boosted frame / AMR / PSATD | 24, 42, 55, 72 | 2004 | Vay, J.-L. and Colella, P and Kwan, J W and Mccorquodale, P and Serafini, D B and Friedman, A and Grote, D P and Westens | Application Of Adaptive Mesh Refinement To Particle-In-Cell Simulations Of Plasmas And Beams | 10.1063/1.1689669 |
| `Friedmanjcp90` | 待分类 | 待定 | 1990 | Friedman, A | A 2Nd-Order Implicit Particle Mover With Adjustable Damping | 10.1016/0021-9991(90)90168-Z |
| `Rittershoferpop2010` | laser/plasma acceleration | 87-89, 125 | 2010 | Rittershofer, W and Schroeder, C B and Esarey, E and Gruner, F J and Leemans, W P | Tapered Plasma Channels To Phase-Lock Accelerating And Focusing Forces In Laser-Plasma Accelerators | 10.1063/1.3430638 |
| `Vorpal` | 待分类 | 待定 | 2004 | Nieter, C and Cary, J R | No Title |  |
| `LiCPC2017` | 待分类 | 待定 | 2017 | Fei Li and Peicheng Yu and Xinlu Xu and Frederico Fiuza and Viktor K. Decyk and Thamine Dalichaouch and Asher Davidson a | Controlling the numerical Cerenkov instability in PIC simulations using a customized finite difference Maxwell solver and a local FFT based current correction | 10.1016/j.cpc.2017.01.001 |
| `XuJCP2013` | 待分类 | 待定 | 2013 | Xu, Xinlu and Yu, Peicheng and Martins, Samual F and Tsung, Frank S and Decyk, Viktor K and Vieira, Jorge and Fonseca, R | Numerical instability due to relativistic plasma drift in EM-PIC simulations | 10.1016/j.cpc.2013.07.003 |
| `Cormierpre08` | laser/plasma acceleration | 87-89, 125 | 2008 | Cormier-Michel, Estelle and Shadwick, B A and Geddes, C G R and Esarey, E and Schroeder, C B and Leemans, W P | Unphysical Kinetic Effects In Particle-In-Cell Modeling Of Laser Wakefield Accelerators | 10.1103/Physreve.78.016404 |
| `Berengerjcp96` | PML | 52, 65 | 1996 | Berenger, J P | Three-Dimensional Perfectly Matched Layer For The Absorption Of Electromagnetic Waves | 10.1006/jcph.1996.0181 |
| `Kalmykovprl09` | 待分类 | 待定 | 2009 | Kalmykov, S. and Yi, S. A. and Khudik, V. and Shvets, G. | Electron Self-Injection and Trapping into an Evolving Plasma Bubble | 10.1103/PhysRevLett.103.135004 |
| `Geddes2015` | Vay pusher / boosted frame / AMR / PSATD | 24, 42, 55, 72 | 2015 | Geddes, Cameron G R and Rykovanov, Sergey and Matlis, Nicholas H. and Steinke, Sven and Vay, Jean-Luc and Esarey, Eric H | Compact quasi-monoenergetic photon sources from laser-plasma accelerators for nuclear detection and characterization | 10.1016/j.nimb.2015.01.013 |
| `Antonsenprl1992` | laser/plasma acceleration | 87-89, 125 | 1992 | Antonsen, T M and Mora, P | Self-Focusing And Raman-Scattering Of Laser-Pulses In Tenuous Plasmas | 10.1103/Physrevlett.69.2204 |
| `GodfreyCPC2015` | Vay pusher / boosted frame / AMR / PSATD | 24, 42, 55, 72 | 2015 | Godfrey, Brendan B. and Vay, Jean-Luc | Improved numerical Cherenkov instability suppression in the generalized PSTD PIC algorithm | 10.1016/j.cpc.2015.06.008 |
| `VayCSD12` | Vay pusher / boosted frame / AMR / PSATD | 24, 42, 55, 72 | 2012 | Vay, J.-L. and Grote, D P and Cohen, R H and Friedman, A | Novel methods in the particle-in-cell accelerator code-framework warp |  |
| `Esirkepovcpc01` | Esirkepov current deposition | 41 | 2001 | Esirkepov, T Z | Exact Charge Conservation Scheme For Particle-In-Cell Simulation With An Arbitrary Form-Factor | 10.1016/S0010-4655(00)00228-9 |
| `Martinspop10` | laser/plasma acceleration | 87-89, 125 | 2010 | Martins, S F and Fonseca, R A and Vieira, J and Silva, L O and Lu, W and Mori, W B | Modeling Laser Wakefield Accelerator Experiments With Ultrafast Particle-In-Cell Simulations In Boosted Frames | 10.1063/1.3358139 |
| `Habericnsp73` | particle pusher | 22-26 | 1973 | Haber, I and Lee, R and Klein, H H and Boris, J P | Proc. Sixth Conf. Num. Sim. Plasmas |  |
| `Martinscpc10` | laser/plasma acceleration | 87-89, 125 | 2010 | Martins, Samuel F and Fonseca, Ricardo A and Silva, Luis O and Lu, Wei and Mori, Warren B | Numerical Simulations Of Laser Wakefield Accelerators In Optimal Lorentz Frames | 10.1016/J.Cpc.2009.12.023 |
| `Vaycpc04` | Vay pusher / boosted frame / AMR / PSATD | 24, 42, 55, 72 | 2004 | Vay, J.-L. and Adam, J.-C. and Heron, A | Asymmetric Pml For The Absorption Of Waves. Application To Mesh Refinement In Electromagnetic Particle-In-Cell Plasma Simulations | 10.1016/J.Cpc.2004.06.026 |
| `GodfreyJCP2014_PSATD` | Vay pusher / boosted frame / AMR / PSATD | 24, 42, 55, 72 | 2014 | Godfrey, Brendan B. and Vay, Jean-Luc and Haber, Irving | Numerical stability analysis of the pseudo-spectral analytical time-domain PIC algorithm | 10.1016/j.jcp.2013.10.053 |
| `PruetJAP06` | 待分类 | 待定 | 2006 | Pruet, J and McNabb, D P and Hagmann, C A and Hartemann, F V and Barty, C P J | Detecting clandestine material with nuclear resonance fluorescence | 10.1063/1.2202005 |
| `YuCPC2015-Circ` | hybrid/fluid | 101-104 | 2015 | Yu, Peicheng and Xu, Xinlu and Tableman, Adam and Decyk, Viktor K. and Tsung, Frank S. and Fiuza, Frederico and Davidson | Mitigation of numerical Cerenkov radiation and instability using a hybrid finite difference-FFT Maxwell solver and a local charge conserving current deposit | 10.1016/j.cpc.2015.08.026 |
| `Berengerjcp94` | PML | 52, 65 | 1994 | Berenger, J P | A Perfectly Matched Layer For The Absorption Of Electromagnetic-Waves | 10.1006/jcph.1994.1159 |
| `Rubel2016` | Vay pusher / boosted frame / AMR / PSATD | 24, 42, 55, 72 | 2016 | Rubel, Oliver and Loring, Burlen and Vay, Jean-Luc and Grote, David P. and Lehe, Remi and Bulanov, Stepan and Vincenti,  | In situ Visualization and Analysis of Ion Accelerator Simulations using Warp and VisIt |  |
| `Geddesnature04` | laser/plasma acceleration | 87-89, 125 | 2004 | Geddes, C G R and Toth, C and Van Tilborg, J and Esarey, E and Schroeder, C B and Bruhwiler, D and Nieter, C and Cary, J | High-Quality Electron Beams From A Laser Wakefield Accelerator Using Plasma-Channel Guiding | 10.1038/Nature02900 |
| `Munzjcp2000` | 待分类 | 待定 | 2000 | Munz, C D and Omnes, P and Schneider, R and Sonnendrucker, E and Voss, U | Divergence Correction Techniques For Maxwell Solvers Based On A Hyperbolic Model | 10.1006/Jcph.2000.6507 |
| `DavidsonJCP2015` | hybrid/fluid | 101-104 | 2015 | Davidson, A. and Tableman, A. and An, W. and Tsung, F. S. and Lu, W. and Vieira, J. and Fonseca, R. A. and Silva, L. O.  | Implementation of a hybrid particle code with a PIC description in r–z and a gridless description in \Phi into OSIRIS | 10.1016/j.jcp.2014.10.064 |
| `GodfreyJCP2014` | Vay pusher / boosted frame / AMR / PSATD | 24, 42, 55, 72 | 2014 | Godfrey, Brendan B and Vay, Jean-Luc and Haber, Irving | Numerical stability analysis of the pseudo-spectral analytical time-domain \PIC\ algorithm | 10.1016/j.jcp.2013.10.053 |
| `Godfrey2013` | Vay pusher / boosted frame / AMR / PSATD | 24, 42, 55, 72 | 2013 | Godfrey, Brendan B. and Vay, Jean-Luc | Numerical stability of relativistic beam multidimensional PIC simulations employing the Esirkepov algorithm | 10.1016/j.jcp.2013.04.006 |
| `Gilsonpop2010` | 待分类 | 待定 | 2010 | Gilson, Erik P and Davidson, Ronald C and Dorf, Mikhail and Efthimion, Philip C and Majeski, Richard and Chung, Moses an | Studies Of Emittance Growth And Halo Particle Production In Intense Charged Particle Beams Using The Paul Trap Simulator Experiment | 10.1063/1.3354109 |
| `Cowanjcp11` | laser/plasma acceleration | 87-89, 125 | 2011 | Cowan, Benjamin M and Bruhwiler, David L and Cormier-Michel, Estelle and Esarey, Eric and Geddes, Cameron G R and Messme | Characteristics Of An Envelope Model For Laser-Plasma Accelerator Simulation | 10.1016/J.Jcp.2010.09.009 |
| `Geddesjp08` | Vay pusher / boosted frame / AMR / PSATD | 24, 42, 55, 72 | 2008 | Geddes, C G R and Bruhwiler, D L and Cary, J R and Mori, W B and Vay, J.-L. and Martins, S F and Katsouleas, T and Cormi | Journal of Physics: Conference Series |  |
| `Steinke2016` | laser/plasma acceleration | 87-89, 125 | 2016 | Steinke, S and van Tilborg, J and Benedetti, C and Geddes, C G R and Schroeder, C B and Daniels, J and Swanson, K K and  | Multistage coupling of independent laser-plasma accelerators | 10.1038/nature16525 |
| `Benedettiaac2010` | laser/plasma acceleration | 87-89, 125 | 2010 | Benedetti, C and Schroeder, C B and Esarey, E and Geddes, C G R and Leemans, W P | Efficient Modeling Of Laser-Plasma Accelerators With Inf\&Rno | 10.1063/1.3520323 |
| `Genonioppj2010` | 待分类 | 待定 | 2010 | Genoni, T.\~C. and Clark, R.\~E. and Van Welch, D.\~R. | A Fast Implicit Algorithm For Highly Magnetized Charged Particle Motion | 10.2174/1876534301003010036 |
| `LewisJCP1972` | 待分类 | 待定 | 1972 | Lewis, H. Ralph | Variational algorithms for numerical simulation of collisionless plasma with point particles including electromagnetic interactions | 10.1016/0021-9991(72)90044-7 |
| `Vay2002` | Vay pusher / boosted frame / AMR / PSATD | 24, 42, 55, 72 | 2002 | Vay, Jean-Luc | Asymmetric Perfectly Matched Layer for the Absorption of Waves☆ | 10.1006/jcph.2002.7175 |
| `Manglesnature04` | laser/plasma acceleration | 87-89, 125 | 2004 | Mangles, S P D and Murphy, C D and Najmudin, Z and Thomas, A G R and Collier, J L and Dangor, A E and Divall, E J and Fo | Monoenergetic Beams Of Relativistic Electrons From Intense Laser-Plasma Interactions | 10.1038/Nature02939 |
| `Schroederaac08` | 待分类 | 待定 | 2009 | Schroeder, C B and Esarey, E and Geddes, C G R and Toth, C and Leemans, W P | Aip Conference Proceedings |  |
| `Vaypop98` | Vay pusher / boosted frame / AMR / PSATD | 24, 42, 55, 72 | 1998 | Vay, J.-L. and Deutsch, C | Charge Compensated Ion Beam Propagation In A Reactor Sized Chamber | 10.1063/1.872648 |
| `Friedmanjcp1991` | PIC foundations / collisions | 1-7, 90-92 | 1991 | Friedman, A and Parker, S E and Ray, S L and Birdsall, C K | Multiscale Particle-In-Cell Plasma Simulation | 10.1016/0021-9991(91)90265-M |
| `Liumotl1997` | 待分类 | 待定 | 1997 | Liu, Q H | The PSTD Algorithm: A Time-Domain Method Requiring Only Two Cells Per Wavelength | 10.1002/(Sici)1098-2760(19970620)15:3<158::Aid-Mop11>3.3.Co;2-T |
| `Karkicap06` | 待分类 | 待定 | 2006 | Karkkainen, M and Gjonaj, E and Lau, T and Weiland, T | Proc. Of International Computational Accelerator Physics Conference |  |
| `Schroederprstab10` | laser/plasma acceleration | 87-89, 125 | 2010 | Schroeder, C.\~B. and Esarey, E and Geddes, C.\~G.\~R. and Benedetti, C and Leemans, W.\~P. | Physics Considerations For Laser-Plasma Linear Colliders | 10.1103/PhysRevSTAB.13.101301 |
| `Leemansphysicstoday10` | laser/plasma acceleration | 87-89, 125 | 2009 | Leemans, Wim and Esarey, Eric | Laser-Driven Plasma-Wave Electron Accelerators |  |
| `Martinspac09` | 待分类 | 待定 | 2009 | Martins, S F and Fonseca, R A and Silva, L O and Mori, W B | Proc. Particle Accelerator Conference |  |
| `Vayscidac09` | Vay pusher / boosted frame / AMR / PSATD | 24, 42, 55, 72 | 2009 | Vay, J.-L. and Bruhwiler, D L and Geddes, C G R and Fawley, W M and Martins, S F and Cary, J R and Cormier-Michel, E and | Simulating Relativistic Beam And Plasma Systems Using An Optimal Boosted Frame | 10.1088/1742-6596/180/1/012006 |
| `Rykovanov2014` | 待分类 | 待定 |  | Rykovanov, S.\~G. | No Title |  |
| `Sprangleprl90` | laser/plasma acceleration | 87-89, 125 | 1990 | Sprangle, P and Esarey, E and Ting, A | Nonlinear theory of intense laser-plasma interactions |  |
| `Molvikpop2007` | Vay pusher / boosted frame / AMR / PSATD | 24, 42, 55, 72 | 2007 | Molvik, A W and Covo, M Kireeff and Cohen, R and Friedman, A and Lund, S M and Sharp, W and Vay, J-L and Baca, D and Bie | Quantitative Experiments With Electrons In A Positively Charged Beam | 10.1063/1.2436850 |
| `QuiterJAP08` | 待分类 | 待定 | 2008 | Quiter, B J and Prussin, S G and Pohl, B and Hall, J and Trebes, J and Stone, G and Descalle, M-A | A method for high-resolution x-ray imaging of intermodal cargo containers for fissionable materials | 10.1063/1.2876028 |
| `Taflove2000` | FDTD / Yee Maxwell solver | 46-50 | 2000 | Allen Taflove and Susan C. Hagness | Computational Electrodynamics: The Finite-Difference Time-Domain Method |  |
| `Schroederprl2011` | laser/plasma acceleration | 87-89, 125 | 2011 | Schroeder, C B and Benedetti, C and Esarey, E and Leemans, W P | Nonlinear Pulse Propagation And Phase Velocity Of Laser-Driven Plasma Waves | 10.1103/Physrevlett.106.135002 |
| `Logannim2007` | Vay pusher / boosted frame / AMR / PSATD | 24, 42, 55, 72 | 2007 | Logan, B G and Bieniosek, F M and Celata, C M and Coleman, J and Greenway, W and Henestroza, E and Kwan, J W and Lee, E  | Recent Us Advances In Ion-Beam-Driven High Energy Density Physics And Heavy Ion Fusion | 10.1016/J.Nima.2007.02.070 |
| `Yu2016` | laser/plasma acceleration | 87-89, 125 | 2016 | Yu, Peicheng and Xu, Xinlu and Davidson, Asher and Tableman, Adam and Dalichaouch, Thamine and Li, Fei and Meyers, Micha | Enabling Lorentz boosted frame particle-in-cell simulations of laser wakefield acceleration in quasi-3D geometry | 10.1016/j.jcp.2016.04.014 |
| `Borisjcp73` | particle pusher | 22-26 | 1973 | Boris, J P and Lee, R | Nonphysical Self Forces In Some Electromagnetic Plasma-Simulation Algorithms | 10.1016/0021-9991(73)90174-5 |
| `BorisICNSP70` | particle pusher | 22-26 | 1970 | Boris, J P | Proc. Fourth Conf. Num. Sim. Plasmas |  |
| `Vaya` | Vay pusher / boosted frame / AMR / PSATD | 24, 42, 55, 72 |  | Vay, Jean-Luc and Godfrey, Brendan and Haber, Irving and Lehe, R\'emi and Vincenti, Henri | In preparation |  |
| `Vayjcp01` | FDTD / Yee Maxwell solver | 46-50 | 2001 | Vay, J.-L. | An Extended Fdtd Scheme For The Wave Equation: Application To Multiscale Electromagnetic Simulation | 10.1006/jcph.2000.6659 |
| `Posinstlbl2002` | 待分类 | 待定 | 2002 | Furman, M and Pivi, M T F | Lbnl-49771/Cbp Note-4151 |  |
| `Kirchen2016` | PSATD | 53-56 | 2016 | Kirchen, Manuel and Lehe, R\'emi | Accelerating a Spectral Algorithm for Plasma Physics with Python/Numba on GPU |  |
| `Leemansnature06` | 待分类 | 待定 | 2006 | Leemans, W P and Nagler, B and Gonsalves, A J and Toth, Cs. and Nakamura, K and Geddes, C G R and Esarey, E and Schroede | GeV electron beams from a centimetre-scale accelerator | 10.1038/Nphys418 |
| `ChenPRSTAB13` | laser/plasma acceleration | 87-89, 125 | 2013 | Chen, M and Esarey, E and Geddes, C G R and Schroeder, C B and Plateau, G R and Bulanov, S S and Rykovanov, S and Leeman | Modeling classical and quantum radiation from laser-plasma accelerators | 10.1103/PhysRevSTAB.16.030701 |
| `Hipace` | 待分类 | 待定 | 2014 | Mehrling, T and Benedetti, C and Schroeder, C B and Osterhoff, J | HiPACE: a quasi-static particle-in-cell code | 10.1088/0741-3335/56/8/084012 |
| `Morsenielson1971` | hybrid/fluid | 101-104 | 1971 | Morse, R L and Nielson, C W | Numerical Simulation Of Weibel Instability In One And 2 Dimensions | 10.1063/1.1693518 |
| `Vaydpf09` | Vay pusher / boosted frame / AMR / PSATD | 24, 42, 55, 72 | 2009 | Vay, J.-L. and Fawley, W. M. and Geddes, C. G. R. and Cormier-Michel, E. and Grote, D. P. | Meeting of the Division of Particles and Fields of the American Physical Society (DPF 2009) |  |
| `Vay2014` | Vay pusher / boosted frame / AMR / PSATD | 24, 42, 55, 72 | 2014 | Vay, Jean-Luc and Godfrey, Brendan B. | Comptes Rendus - Mecanique |  |
| `Friedman2014` | Vay pusher / boosted frame / AMR / PSATD | 24, 42, 55, 72 | 2014 | Friedman, Alex and Cohen, Ronald H. and Grote, David P. and Lund, Steven M. and Sharp, William M. and Vay, Jean-Luc and  | Computational methods in the warp code framework for kinetic simulations of particle beams and plasmas | 10.1109/TPS.2014.2308546 |
| `Lcode` | 待分类 | 待定 | 1998 | Lotov, K. V. | Simulation of ultrarelativistic beam dynamics in plasma wake-field accelerator | 10.1063/1.872765 |
| `GodfreyJCP2014_2` | FDTD / Yee Maxwell solver | 46-50 | 2014 | Godfrey, Brendan B and Vay, Jean-Luc | Suppressing the numerical Cherenkov instability in \FDTD\ \PIC\ codes | 10.1016/j.jcp.2014.02.022 |
| `Turbowave` | laser/plasma acceleration | 87-89, 125 | 2000 | Gordon, Daniel F and Mori, W B and Antonsen, Thomas M | A Ponderomotive Guiding Center Particle-in-Cell Code for Efficient Modeling of Laser–Plasma Interactions |  |
| `Habernim2009` | 待分类 | 待定 | 2009 | Haber, I and Bernal, S and Beaudoin, B and Cornacchia, A and Feldman, D and Feldman, R B and Fiorito, R and Fiuza, K and | Scaled Electron Studies At The University Of Maryland | 10.1016/J.Nima.2009.03.220 |
| `Folegatijpcs2011` | 待分类 | 待定 | 2011 | Folegati, Paola and Xu, Jia and Weber, Marc H and Lynn, Kelvin G | Positron Storage In Micro-Traps With Long Aspect Ratio: Results Of Computer Simulations | 10.1088/1742-6596/262/1/012021 |
| `YuCPC2015` | PSATD | 53-56 | 2015 | Yu, Peicheng and Xu, Xinlu and Decyk, Viktor K. and Fiuza, Frederico and Vieira, Jorge and Tsung, Frank S. and Fonseca,  | Elimination of the numerical Cerenkov instability for spectral EM-PIC codes | 10.1016/j.cpc.2015.02.018 |
| `PukhovJPP99` | laser/plasma acceleration | 87-89, 125 | 1999 | Pukhov, A | Three-dimensional electromagnetic relativistic particle-in-cell code VLPL (Virtual Laser Plasma Lab) | 10.1017/S0022377899007515 |
| `Vayipac10` | Vay pusher / boosted frame / AMR / PSATD | 24, 42, 55, 72 | 2010 | Vay, J.-L. and Byrd, J.\~M. and Furman, M.\~A. and Secondo, R and Venturini, M and Fox, J.\~D. and Rivetta, C.\~H. and H | Proc. 1St International Particle Accelerator Conference |  |
| `Cormierprstab2011` | laser/plasma acceleration | 87-89, 125 | 2011 | Cormier-Michel, E and Esarey, E and Geddes, C G R and Schroeder, C B and Paul, K and Mullowney, P J and Cary, J R and Le | Control Of Focusing Fields In Laser-Plasma Accelerators Using Higher-Order Modes | 10.1103/Physrevstab.14.031303 |
| `Lehe2016` | Vay pusher / boosted frame / AMR / PSATD | 24, 42, 55, 72 | 2016 | Lehe, R\'emi and Kirchen, Manuel and Andriyash, Igor A. and Godfrey, Brendan B. and Vay, Jean-Luc | A spectral, quasi-cylindrical and dispersion-free Particle-In-Cell algorithm | 10.1016/j.cpc.2016.02.007 |
| `Birdsalllangdon` | PIC foundations / collisions | 1-7, 90-92 | 1991 | Birdsall, C K and Langdon, A B | Plasma Physics Via Computer Simulation |  |
| `Grote2005` | Vay pusher / boosted frame / AMR / PSATD | 24, 42, 55, 72 | 2005 | Grote, David P. and Friedman, Alex and Vay, Jean-Luc and Haber, Irving | AIP Conference Proceedings |  |
| `Villasenorcpc92` | charge-conserving current deposition | 40 | 1992 | Villasenor, J and Buneman, O | Rigorous Charge Conservation For Local Electromagnetic-Field Solvers |  |
| `Spitkovsky:Icnsp2011` | 待分类 | 待定 | 2011 | Sironi, L and Spitkovsky, A | No Title |  |
| `LeemansPRL2014` | Vay pusher / boosted frame / AMR / PSATD | 24, 42, 55, 72 | 2014 | Leemans, W P and Gonsalves, A J and Mao, H.-S. and Nakamura, K and Benedetti, C and Schroeder, C B and T\'oth, Cs. and D | Multi-GeV Electron Beams from Capillary-Discharge-Guided Subpetawatt Laser Pulses in the Self-Trapping Regime | 10.1103/PhysRevLett.113.245002 |
| `Abejcp86` | 待分类 | 待定 | 1986 | Abe, H and Sakairi, N and Itatani, R and Okuda, H | High-Order Spline Interpolations In The Particle Simulation | 10.1016/0021-9991(86)90193-2 |
| `LeeCPC2015` | Vay pusher / boosted frame / AMR / PSATD | 24, 42, 55, 72 | 2015 | Lee, P and Vay, J.-L. | Efficiency of the Perfectly Matched Layer with high-order finite difference and pseudo-spectral Maxwell solvers | 10.1016/j.cpc.2015.04.004 |
| `Vaylpb2002` | Vay pusher / boosted frame / AMR / PSATD | 24, 42, 55, 72 | 2002 | Vay, J-L and Colella, P and Mccorquodale, P and Van Straalen, B and Friedman, A and Grote, D P | Mesh Refinement For Particle-In-Cell Plasma Simulations: Applications To And Benefits For Heavy Ion Fusion | 10.1017/S0263034602204139 |
| `Vaypac11` | Vay pusher / boosted frame / AMR / PSATD | 24, 42, 55, 72 | 2011 | Vay, J.-L. and Furman, M.\~A. and Venturini, M | Proc. Particle Accelerator Conference |  |
| `Tzoufrasprl2008` | 待分类 | 待定 | 2008 | Tzoufras, M and Lu, W and Tsung, F S and Huang, C and Mori, W B and Katsouleas, T and Vieira, J and Fonseca, R A and Sil | Beam Loading In The Nonlinear Regime Of Plasma-Based Acceleration Rid C-6436-2009 Rid B-7680-2009 Rid C-3169-2009 | 10.1103/Physrevlett.101.145002 |
| `Bulanovphysfluid1992` | hybrid/fluid | 101-104 | 1992 | Bulanov, S V and Inovenkov, I N and Kirsanov, V I and Naumova, N M and Sakharov, A S | Nonlinear Depletion Of Ultrashort And Relativistically Strong Laser-Pulses In An Underdense Plasma | 10.1063/1.860046 |
| `Martinsnaturephysics10` | laser/plasma acceleration | 87-89, 125 | 2010 | Martins, S F and Fonseca, R A and Lu, W and Mori, W B and Silva, L O | Exploring Laser-Wakefield-Accelerator Regimes For Near-Term Lasers Using Particle-In-Cell Simulation In Lorentz-Boosted Frames | 10.1038/Nphys1538 |
| `Friedmanpop10` | Vay pusher / boosted frame / AMR / PSATD | 24, 42, 55, 72 | 2010 | Friedman, A and Barnard, J J and Cohen, R H and Grote, D P and Lund, S M and Sharp, W M and Faltens, A and Henestroza, E | Beam Dynamics Of The Neutralized Drift Compression Experiment-Ii, A Novel Pulse-Compressing Ion Accelerator | 10.1063/1.3292634 |
| `Schroederpop2006` | 待分类 | 待定 | 2006 | Schroeder, C B and Esarey, E and Shadwick, B A and Leemans, W P | Trapping, Dark Current, And Wave Breaking In Nonlinear Plasma Waves | 10.1063/1.2173960 |
| `Friedmanpfb92` | hybrid/fluid | 101-104 | 1992 | Friedman, A and Grote, D P and Haber, I | 3-Dimensional Particle Simulation Of Heavy-Ion Fusion Beams | 10.1063/1.860024 |
| `Gustafssonkreissoliger` | 待分类 | 待定 | 1995 | Gustafsson, B and Kreiss, H.-O. and Oliger, J | Time Dependent Problems And Difference Methods |  |
| `Winklehnerji2010` | hybrid/fluid | 101-104 | 2010 | Winklehner, D and Todd, D and Benitez, J and Strohmeier, M and Grote, D and Leitner, D | Comparison Of Extraction And Beam Transport Simulations With Emittance Measurements From The Ecr Ion Source Venus | 10.1088/1748-0221/5/12/P12001 |
| `Vaypac09` | Vay pusher / boosted frame / AMR / PSATD | 24, 42, 55, 72 | 2009 | Vay, J-L and Fawley, W M and Geddes, C G R and Cormier-Michel, E and Grote, D P | Proc. Particle Accelerator Conference |  |
| `VincentiCPC2017a` | FDTD / Yee Maxwell solver | 46-50 | 2016 | Vincenti, H. and Vay, J.-L. | Detailed analysis of the effects of stencil spatial variations with arbitrary high-order finite-difference Maxwell solver | 10.1016/j.cpc.2015.11.009 |
| `Vayjcp02` | Vay pusher / boosted frame / AMR / PSATD | 24, 42, 55, 72 | 2002 | Vay, J.-L. | Asymmetric Perfectly Matched Layer For The Absorption Of Waves | 10.1006/Jcph.2002.7175 |
| `Felsenmarcuvitz` | 待分类 | 待定 | 1994 | Felsen, L.\~B. and Marcuvitz, N | Radiation And Scattering Of Waves |  |
| `Geddesdissertation05` | laser/plasma acceleration | 87-89, 125 | 2005 | Geddes, C G R | Plasma Channel Guided Laser Wakefield Accelerator |  |
| `Tsungpop06` | laser/plasma acceleration | 87-89, 125 | 2006 | Tsung, F. S. and Lu, W. and Tzoufras, M. and Mori, W. B. and Joshi, C. and Vieira, J. M. and Silva, L. O. and Fonseca, R | Simulation Of Monoenergetic Electron Generation Via Laser Wakefield Accelerators For 5-25 TW Lasers | 10.1063/1.2198535 |
| `INFERNO` | 待分类 | 待定 | 2012 | Benedetti, Carlo and Schroeder, Carl B. and Esarey, Eric and Leemans, Wim P. | ICAP |  |
| `GonsalvesNP2011` | laser/plasma acceleration | 87-89, 125 | 2011 | Gonsalves, A J and Nakamura, K and Lin, C and Panasenko, D and Shiraishi, S and Sokollik, T and Benedetti, C and Schroed | Tunable laser plasma accelerator based on longitudinal density tailoring | 10.1038/NPHYS2071 |
| `Ohtsuboprstab2010` | 待分类 | 待定 | 2010 | Ohtsubo, S and Fujioka, M and Higaki, H and Ito, K and Okamoto, H and Sugimoto, H and Lund, S M | Experimental Study Of Coherent Betatron Resonances With A Paul Trap | 10.1103/Physrevstab.13.044201 |
| `Warp` | Vay pusher / boosted frame / AMR / PSATD | 24, 42, 55, 72 | 2005 | Grote, D P and Friedman, A and Vay, J-L and Haber, I | Aip Conference Proceedings |  |
| `Mccorquodalejcp2004` | Vay pusher / boosted frame / AMR / PSATD | 24, 42, 55, 72 | 2004 | Mccorquodale, P and Colella, P and Grote, D P and Vay, J-L | A Node-Centered Local Refinement Algorithm For Poisson's Equation In Complex Geometries | 10.1016/J.Jcp.2004.04.022 |
| `Londrillo2010` | 待分类 | 待定 | 2010 | Londrillo, P. and Benedetti, C. and Sgattoni, A. | Charge preserving high order PIC schemes | 10.1016/j.nima.2010.01.055 |
| `GodfreyJCP2014_FDTD` | FDTD / Yee Maxwell solver | 46-50 | 2014 | Godfrey, Brendan B. and Vay, Jean-Luc | Suppressing the numerical Cherenkov instability in FDTD PIC codes | 10.1016/j.jcp.2014.02.022 |
| `Shortley-Weller` | 待分类 | 待定 | 1938 | Shortley, G H and Weller, R | The Numerical Solution Of Laplace's Equation | 10.1063/1.1710426 |
| `VayPOPL2011` | Vay pusher / boosted frame / AMR / PSATD | 24, 42, 55, 72 | 2011 | Vay, J.-L. and Geddes, C. G. R. and Cormier-Michel, E. and Grote, D. P. | Effects of hyperbolic rotation in Minkowski space on the modeling of plasma accelerators in a Lorentz boosted frame | 10.1063/1.3559483 |
| `KirchenPOP2016` | Vay pusher / boosted frame / AMR / PSATD | 24, 42, 55, 72 | 2016 | Kirchen, M. and Lehe, R. and Godfrey, B. B. and Dornmair, I. and Jalas, S. and Peters, K. and Vay, J.-L. and Maier, A. R | Stable discrete representation of relativistically drifting plasmas | 10.1063/1.4964770 |
| `LehePRE2016` | Vay pusher / boosted frame / AMR / PSATD | 24, 42, 55, 72 | 2016 | Lehe, Remi and Kirchen, Manuel and Godfrey, Brendan B. and Maier, Andreas R. and Vay, Jean-Luc | Elimination of numerical Cherenkov instability in flowing-plasma particle-in-cell simulations by using Galilean coordinates | 10.1103/PhysRevE.94.053305 |
| `godfrey1985iprop` | NCI / spectral stability | 53-56 | 1985 | Godfrey, B. B. | The IPROP Three-Dimensional Beam Propagation Code |  |
| `shapovalPRE2024` | Vay pusher / boosted frame / AMR / PSATD | 24, 42, 55, 72 | 2024 | Shapoval, Olga and Zoni, Edoardo and Lehe, Remi and Thevenet, Maxence and Vay, Jean-Luc | Pseudospectral particle-in-cell formulation with arbitrary charge and current-density time dependencies for the modeling of relativistic plasmas | 10.1103/PhysRevE.110.025206 |
| `Ammosov1986` | 待分类 | 待定 | 1986 | Ammosov, M. V. and Delone, N. B. and Krainov, V. P. | Tunnel ionization of complex atoms and of atomic ions in an alternating electromagnetic field | 10.1117/12.938695 |
| `zhang_empirical_2014` | 待分类 | 待定 | 2014 | Zhang, Qingbin and Lan, Pengfei and Lu, Peixiang | Empirical formula for over-barrier strong-field ionization | 10.1103/PhysRevA.90.043410 |
| `Mulser2010` | laser/plasma acceleration | 87-89, 125 | 2010 | Mulser, Peter and Bauer, Dieter | High Power Laser-Matter Interaction | 10.1007/978-3-540-46065-7 |
| `Zhang2017` | 待分类 | 待定 | 2017 | Zhang, Peng and Valfells, Agust and Ang, L.K. and Luginsland, J. W. and Lau, Y. Y | 100 years of the physics of diodes | 10.1063/1.4978231 |

## 本地 PDF 清单

| PDF | 初步主题 | 计划章节 | MinerU 状态 |
|---|---|---|---|
| `references/01_reviews_surveys/2014_VayFRACAD2014_Modeling_of_relativistic_plasmas_with_the_Particle-In-Cell_method.pdf` | Vay pusher / boosted frame / AMR / PSATD | 24, 42, 55, 72 | 待 MinerU |
| `references/01_reviews_surveys/2016_Habib2016_ASCRHEP_Exascale_Requirements_Review_Report.pdf` | HPC / AMReX / performance | 71-79, 121-123 | 待 MinerU |
| `references/01_reviews_surveys/no-year_FullyKineticPICFusionReview2024_Recent_development_of_fully_kinetic_particle-in-cell_method_and_its_application_to_fusion_plasma_instability_study.pdf` | 待分类 | 待定 | 待 MinerU |
| `references/01_reviews_surveys/no-year_PICMethodsAstrophysics2021_PIC_methods_in_astrophysics_simulations_of_relativistic_jets_and_kinetic_physics_in_astrophysical_systems.pdf` | 待分类 | 待定 | 待 MinerU |
| `references/01_reviews_surveys/no-year_PICRelativisticBeamsPlasmasReview2014_Review_and_Recent_Advances_in_PIC_Modeling_of_Relativistic_Beams_and_Plasmas.pdf` | 待分类 | 待定 | 待 MinerU |
| `references/01_reviews_surveys/no-year_PICShearedExpandingEscapingAstro2026_Particle-In-Cell_Methods_for_Simulations_of_Sheared_Expanding_or_Escaping_Astrophysical_Plasma.pdf` | 待分类 | 待定 | 待 MinerU |
| `references/01_reviews_surveys/no-year_PlasmaPropulsionSimulationUsingParticles2023_Plasma_propulsion_simulation_using_particles.pdf` | 待分类 | 待定 | 待 MinerU |
| `references/02_books_lecture_notes/no-year_ComputationalMethodsPlasmaPhysicsNotes_Computational_Methods_in_Plasma_Physics_lecture_notes.pdf` | 待分类 | 待定 | 待 MinerU |
| `references/02_books_lecture_notes/no-year_PICSimulationNotesYoujunHu2019_Particle_In_Cell_PIC_simulation.pdf` | 待分类 | 待定 | 待 MinerU |
| `references/03_pic_foundations/2015_Vranic2015_Particle_merging_algorithm_for_PIC_codes.pdf` | 待分类 | 待定 | 待 MinerU |
| `references/03_pic_foundations/2016_AndriyashPoP2016_Laser-plasma_interactions_with_a_Fourier-Bessel_particle-in-cell_method.pdf` | laser/plasma acceleration | 87-89, 125 | 待 MinerU |
| `references/03_pic_foundations/2020_Stanier2020_A_cancellation_problem_in_hybrid_particle-in-cell_schemes_due_to_finite_particle_size.pdf` | hybrid/fluid | 101-104 | 待 MinerU |
| `references/03_pic_foundations/2021_MuravievCPC2021_Strategies_for_particle_resampling_in_PIC_simulations.pdf` | 待分类 | 待定 | 待 MinerU |
| `references/03_pic_foundations/2024_SandbergPASC24_Synthesizing_Particle-In-Cell_Simulations_through_Learning_and_GPU_Computing_for_Hybrid_Particle_Accelerator_Beamlines.pdf` | HPC / AMReX / performance | 71-79, 121-123 | 待 MinerU |
| `references/03_pic_foundations/no-year_KineticTheoryPICEnsembleAveraging2022_Kinetic_theory_of_particle-in-cell_simulation_plasma_and_the_ensemble_averaging_technique.pdf` | 待分类 | 待定 | 待 MinerU |
| `references/04_particle_pushers_deposition_shapes/2017_HigueraPOP2017_Structure-preserving_second-order_integration_of_relativistic_charged_particle_trajectories_in_electromagnetic_fields/2017_HigueraPOP2017_Structure-preserving_second-order_integration_of_relativistic_charged_particle_trajectories_in_electromagnetic_fields.pdf` | Higuera-Cary pusher | 25 | 已 materialize / 已 MinerU |
| `references/04_particle_pushers_deposition_shapes/2008_VayPOP2008_Simulation_of_beams_or_plasmas_crossing_at_relativistic_velocity/2008_VayPOP2008_Simulation_of_beams_or_plasmas_crossing_at_relativistic_velocity.pdf` | Vay pusher | 24 | 已 materialize / 已 MinerU |
| `references/06_stability_filtering_nci/no-year_FiniteGridEnergyConservingPIC2019_Finite_spatial-grid_effects_in_energy-conserving_particle-in-cell_algorithms.pdf` | 待分类 | 待定 | 待 MinerU |
| `references/06_stability_filtering_nci/no-year_MLAcceleratedPIC2021_Machine_learning_accelerated_particle-in-cell_plasma_simulations.pdf` | 待分类 | 待定 | 待 MinerU |
| `references/07_amr_parallel_hpc_gpu/no-year_PICXeonPhi2015_Particle-in-Cell_Laser-Plasma_Simulation_on_Xeon_Phi_Coprocessors.pdf` | laser/plasma acceleration | 87-89, 125 | 待 MinerU |
| `references/07_amr_parallel_hpc_gpu/no-year_WarpXHPCBestPractices_Our_Road_to_Exascale_WarpX.pdf` | HPC / AMReX / performance | 71-79, 121-123 | 待 MinerU |
| `references/08_boundaries_pml_geometry/no-year_PIFE-PIC2020_PIFE-PIC_Parallel_Immersed-Finite-Element_Particle-In-Cell_For_3-D_Kinetic_Simulations_of_Plasma-Material_Interactions.pdf` | 待分类 | 待定 | 待 MinerU |
| `references/09_multiphysics_collisions_ionization_qed/2013_Turner2013_Simulation_benchmarks_for_low-pressure_plasmas_Capacitive_discharges.pdf` | 待分类 | 待定 | 待 MinerU |
| `references/09_multiphysics_collisions_ionization_qed/2019_Yakimenko2019_Prospect_of_Studying_Nonperturbative_QED_with_Beam-Beam_Collisions.pdf` | QED | 96-100 | 待 MinerU |
| `references/09_multiphysics_collisions_ionization_qed/2024_Kicsiny2024_Multiturn_simulation_of_radiative_Bhabha_scattering_in_the_equivalent_photon_approximation.pdf` | 待分类 | 待定 | 待 MinerU |
| `references/09_multiphysics_collisions_ionization_qed/no-year_BoundElectronEffectsPIC2022_Modeling_of_bound_electron_effects_in_particle-in-cell_simulation.pdf` | 待分类 | 待定 | 待 MinerU |
| `references/10_applications_laser_plasma_acceleration/2020_Fallahi2020_MITHRA_2.0_A_Full-Wave_Simulation_Tool_for_Free_Electron_Lasers.pdf` | laser/plasma acceleration | 87-89, 125 | 待 MinerU |
| `references/11_codes_ecosystem_standards/no-year_PSC2013_The_Plasma_Simulation_Code_A_modern_particle-in-cell_code_with_load-balancing_and_GPU_support.pdf` | NCI / spectral stability | 53-56 | 待 MinerU |
| `references/11_codes_ecosystem_standards/no-year_PicFoamOpenFOAMPIC2020_picFoam_An_OpenFOAM_based_electrostatic_Particle-in-Cell_solver.pdf` | 待分类 | 待定 | 待 MinerU |
| `references/11_codes_ecosystem_standards/no-year_Smilei2017_SMILEI_a_collaborative_open-source_multi-purpose_particle-in-cell_code_for_plasma_simulation.pdf` | 待分类 | 待定 | 待 MinerU |
| `references/12_hybrid_fluid_models/2013_holmstrom2013handlingvacuumregionshybrid_Handling_vacuum_regions_in_a_hybrid_plasma_solver.pdf` | hybrid/fluid | 101-104 | 待 MinerU |
| `references/12_hybrid_fluid_models/2016_Le2016_Hybrid_simulations_of_magnetic_reconnection_with_kinetic_ions_and_fluid_electron_pressure_anisotropy.pdf` | hybrid/fluid | 101-104 | 待 MinerU |
| `references/12_hybrid_fluid_models/2018_MUNOZ2018_A_new_hybrid_code_CHIEF_implementing_the_inertial_electron_fluid_equation_without_approximation.pdf` | hybrid/fluid | 101-104 | 待 MinerU |
| `references/12_hybrid_fluid_models/no-year_FluidKineticPICSolver2013_The_Fluid-Kinetic_Particle-in-Cell_Solver_for_Plasma_Simulations.pdf` | hybrid/fluid | 101-104 | 待 MinerU |
| `references/13_theses_dissertations/no-year_ParticleInCellAlgorithmsHeterogeneousArchitectures2016_Particle-in-cell_algorithms_for_plasma_simulations_on_heterogeneous_architectures.pdf` | 待分类 | 待定 | 待 MinerU |
| `references/14_general_numerical_methods/1988_ShuJCP1988_Efficient_implementation_of_essentially_non-oscillatory_shock-capturing_schemes.pdf` | 待分类 | 待定 | 待 MinerU |
