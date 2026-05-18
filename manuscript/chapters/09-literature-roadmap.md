# 9. 文献路线与后续扩写计划

本书的文献不是装饰，而是每章判断物理正确性的证据。当前本地文献来源有三层：

1. `../warpx/Docs/source/refs.bib` 复制得到的 `../bibliography/warpx-refs.bib`。
2. `../references/` 中已经下载的开放 PDF。
3. 后续从 WarpX 官方文档、综述和章节问题继续补充的论文。

第一批核心引用按主题分组如下：

| 主题 | BibTeX key | 用途 |
|---|---|---|
| PIC 基础 | `Birdsalllangdon`, `HockneyEastwoodBook`, `DawsonRMP83`, `Birdsall1991` | 宏粒子、形函数、PIC-MCC、噪声和基础算法 |
| Yee/FDTD | `Yee` | 交错网格 Maxwell 求解 |
| 电流沉积 | `Villasenorcpc92`, `Esirkepovcpc01`, `VayJCP2013` | 电荷守恒沉积、谱空间 Vay deposition |
| 粒子推进 | `HigueraPOP2017` 和 Vay pusher 相关条目 | 相对论推进器 |
| PML | `Berengerjcp94`, `Berengerjcp96` | 开边界吸收 |
| AMR | `Vayjcp01`, `Vaylpb2002`, `Vaycpc04` | mesh refinement interface、substitution method |
| PSATD/NCI | `GodfreyJCP2014_PSATD`, `Lehe2016`, `GodfreyJCP2014_FDTD` | 谱求解器、数值 Cherenkov 抑制 |
| 数据和生态 | openPMD / PICMI / AMReX / PICSAR 相关条目 | I/O 标准、接口和 HPC 生态 |

PDF 处理规则：只要要深入讲解一篇论文，就按 `../docs/paper-reading-workflow.md` 执行。也就是先建论文专属目录，用 MinerU 转 Markdown，保存 `images/`，再写中文讲解笔记。不能把 PDF 摘要式看完后直接把结论写进正文。

下一轮最值得处理的论文：

1. Higuera-Cary pusher：支撑第 4 章。
2. Esirkepov current deposition：支撑第 5 章。
3. Yee 1966：支撑第 6 章。
4. Berenger PML：支撑第 7 章。
5. WarpX / AMReX / PICSAR 论文：支撑工程和性能章节。
6. PSATD 与 Galilean PSATD：支撑数值 Cherenkov 和 boosted-frame 章节。

扩写计划按风险排序：

1. 补全源码行号：每章都要从 `docs/source-map.md` 扩成精确函数表。
2. 补全参数入口：把 `Docs/source/usage/parameters.rst` 中相关参数映射到源码解析位置。
3. 补全运行验证：至少 Langmuir wave 和 uniform plasma 要有本地输出和分析脚本。
4. 补全论文笔记：优先处理能直接支撑核心算法的论文。
5. 再扩展多物理：碰撞、电离、QED、hybrid PIC 和 embedded boundary。

本版已经形成主线，但还不是最终可出版稿。它的价值在于把“物理方程、离散算法、WarpX 源码、示例、文献”放到同一条路径上，后续每章都可以沿这条路径加深。
