# PIC-tutor 书稿

PIC-tutor 是一本从物理模型走到 WarpX 源码的 PIC 教程。它面向希望真正读懂 PIC 程序、设计可解释模拟并判断数值结果可信度的读者，而不是面向维护者的提交记录或测试报告集合。

## 阅读路径

1. 第 1 章建立 Vlasov-Maxwell、宏粒子、形函数、权重和统计误差的物理语言。
2. 第 2-3A 章把这些对象组织成时间推进和 WarpX 的初始化/演化调用链。
3. 第 4-7 章分别深入粒子推进器、沉积、场求解器、边界和 AMR；每章都先讲概念，再落到源码入口和可复现实验。
4. 第 8 章用 Langmuir、uniform plasma 和应用案例练习从输入到诊断的完整判断链。
5. 第 9 章说明文献如何支撑这些解释，以及哪些结论仍然需要更强的一手来源或 runtime 证据。

建议第一次阅读先跳过源码行号和审计合同，沿着每章的“本章任务、核心方程、最小案例、练习”完成主线；第二遍再回看源码路径和证据边界。这样读者先获得可用的物理模型，再把实现细节放回正确的位置。

## 准确性约定

书中明确区分四种说法：公式推导、当前源码行为、实际运行结果和尚未证明的推断。一个 case 通过 regression 只说明该 case 的指定 observable 在指定输入下满足 gate，不能自动推广到其他 geometry、shape、AMR、时间步或粒子数。所有重要的源码和运行结论都应能回到 `../warpx`、官方文档、输入文件、analysis 脚本或论文资产。

当前 v0.110 的正式收敛重复斜率 gate 已重跑并通过，但 formal numerical order、RZ axis-charge closure、若干 AMR route ledger 和部分论文发表版逐式核对仍在 [当前成书缺口登记](../docs/current-book-gap-register.md) 中。这里保留这些边界是为了帮助读者正确解释结果，而不是把项目状态冒充成教程结论。

## 构建

```bash
python scripts/build_v110.py
python scripts/verify_v110_build.py --build-log /tmp/pic-tutor-build-v110.log
```

当前合订产物位于 `dist/pic-tutor-v0.110.{md,html,pdf}`。版本历史、运行合同和发布审计属于仓库证据层，分别位于 `docs/`、`runs/` 和 `notes/`，不替代正文的教学叙事。
