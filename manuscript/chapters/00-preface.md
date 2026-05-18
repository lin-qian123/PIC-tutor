# 0. 写作说明

本书不是 WarpX 官方文档的翻译，也不是只讲公式的 PIC 理论笔记。它的主线是：先从 Vlasov-Maxwell / Vlasov-Poisson 这类连续模型出发，说明为什么需要宏粒子；再把宏粒子、网格、形函数、沉积和场求解拼成 PIC 算法；最后回到本机 `../warpx` 的真实源码，解释一个现代高性能 PIC 程序如何把这些步骤组织成可运行、可扩展、可验证的模拟软件。

当前书稿绑定的源码状态是：

- WarpX 分支：`pkuHEDPbranch`
- WarpX commit：`063f8b586f04321e13150ae3e730e0794ca75cb1`
- 主要源码入口：`../warpx/Source/`
- 官方文档入口：`../warpx/Docs/source/`
- 示例入口：`../warpx/Examples/`
- regression 入口：`../warpx/Regression/`

本书的每个技术判断都应尽量落到六类证据：物理方程、离散公式、WarpX 源码路径、输入参数、示例或测试、文献。DeepWiki、Zread 等 AI 解读页面可以用来快速找到模块名，但不能作为最终依据。

本版先采用 Markdown-first 写法。这样做的原因是正文、源码路径、公式、后续 MinerU 论文笔记和本地运行记录都可以在同一个目录中增量维护。等样章和主线稳定后，再迁移到 Quarto 或 LaTeX book。

本书默认使用以下记号：粒子位置为 $$\mathbf{x}_p$$，粒子动量为 $$\mathbf{u}_p=\gamma\mathbf{v}_p$$，电磁场为 $$\mathbf{E},\mathbf{B}$$，电荷和电流密度为 $$\rho,\mathbf{J}$$，粒子权重为 $$w_p$$，形函数为 $$S$$。网格量的上标表示时间层，例如 $$\mathbf{B}^{n+1/2}$$；粒子量一般按 leapfrog 交错在位置和动量时间层上。

阅读建议：先读第 1-3 章建立“物理-算法-代码调用链”的整体图，再读第 4-7 章理解各个核心模块，最后用第 8 章的 Langmuir wave 和 uniform plasma 案例检查自己是否真正能把输入参数、源码和输出诊断连起来。
