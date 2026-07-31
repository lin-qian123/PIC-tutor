# PIC-tutor

PIC-tutor 是一本中文的 Particle-In-Cell（PIC）教程：从 Vlasov--Maxwell 模型和离散算法出发，逐步走到 WarpX 的源码职责、输入设计和可解释的验证。它面向希望读懂 PIC 程序、设计模拟并判断结果证据强度的读者，不是开发日志或测试报告的汇编。

当前可审阅版本为 `v0.110`，包含 275 页 PDF、合订 Markdown 和自包含 HTML。书稿内容、构建产物和当前发行哈希由同一 release manifest 固定。

## 阅读书稿

- [PDF 书稿](dist/pic-tutor-v0.110.pdf)：适合连续阅读和打印。
- [HTML 书稿](dist/pic-tutor-v0.110.html)：适合浏览器检索和跳转。
- [Markdown 合订稿](dist/pic-tutor-v0.110.md)：适合检索、批注和版本比较。
- [章节源文件](manuscript/chapters/)：适合按主题阅读或追溯书稿改动。

第一次阅读可从 [前言](manuscript/chapters/00-preface.md) 的三条路线中任选一条：

1. **最小 case 解释**：从尺度、PIC step、输入到 diagnostics，学会说明一个运行结果为何可信。
2. **源码链阅读**：从粒子状态到同步后的 `rho/J` 和场更新，追踪 producer 与 consumer。
3. **验证合同设计**：将 source residual、解析场、checksum 和收敛趋势分开，建立可审查的结论边界。

## 这本书讲什么

| 部分 | 内容 | 读者完成后应能回答的问题 |
|---|---|---|
| 第 1--3A 章 | 动理学模型、PIC 离散循环、WarpX 初始化与演化 | 连续量怎样成为粒子、网格、时间层和主循环状态？ |
| 第 4--7 章 | 粒子推进、沉积、场求解器、边界与 AMR | 一个状态由谁产生、经过哪些同步、被哪个模块消费？ |
| 第 8 章 | diagnostics、验证与物理案例 | 输出测量了什么，reference、容差与不可外推范围是什么？ |
| 第 9 章与附录 | 文献判读、符号与时间层 | 公式、源码和案例证据各能支持到什么程度？ |

书中一贯区分四类对象：**source** 是场方程实际消费的离散状态，**producer** 创建或变换该状态，**consumer** 使用它更新场或形成比较，**observable** 才是用来判断物理或数值结论的量。找到数组、函数或输出文件本身，不等于已经得到物理验证。

## 准确性约定

每项重要结论都会尽量回到物理方程、离散公式、WarpX 源码、输入参数、示例/测试和文献之一或多者。书中明确区分：

- 公式或文献说明某个近似为什么成立及其假设；
- 源码映射说明 WarpX 在哪个职责路径实现该近似；
- 指定 case 的 analysis 只验证该输入、几何、算法、时间层和容差下的 observable；
- 未覆盖的 geometry、AMR、shape、并行布局或物理模型不会被写成已证明。

因此，一次 regression PASS 不是通用物理正确性；一个解析公式也不自动覆盖所有实现分支。读者可在 [书稿说明](manuscript/README.md) 和第 9 章查看这一证据层级的完整用法。

## 构建与检查

本项目默认使用 `python`。从仓库根目录运行：

```bash
python scripts/build_v110.py
python scripts/verify_v110_build.py
python scripts/audit_reader_facing_content.py \
  --output-json /tmp/pic-tutor-reader-facing.json \
  --output-md /tmp/pic-tutor-reader-facing.md
python scripts/audit_release_consistency.py
```

构建会生成 `dist/pic-tutor-v0.110.{md,html,pdf}`。读者化审计、结构/版式审计和 release 一致性检查是编辑回归防线；它们不能替代新物理分支的 runtime 验证或人工判断。

## 当前状态与边界

- 书稿已完成目录、前言、第 1--9 章和附录的 262 页基线连续阅读，并对当前 275 页候选的受影响内容进行增量版式复核；记录见 [人工审读记录](docs/manual-editorial-spotcheck-v0.110.md)。
- 当前核心开放问题包括部分 publisher-formatted 论文的访问边界、RZ axis-charge correctness、完整 transition-zone route ledger、若干 geometry/algorithm runtime coverage 和公开发行权利。它们的证据与关闭条件见 [当前缺口登记](docs/current-book-gap-register.md)。
- 本仓库的公开再分发尚未签收：public branch 已跟踪第三方 `references/` 资产，且尚无项目许可证。发行阻断的事实和维护者决策路径见 [公开发行审计](docs/public-repo-release-audit.md) 与 [风险登记](docs/public-distribution-risk-register-v0.110.md)。书稿可供审阅不等于这些第三方材料已获再分发授权。

## 目录结构

```text
manuscript/     书稿章节、附录与排版资源
dist/           当前版本的 Markdown、HTML 和 PDF
scripts/        构建、内容、版式与发行一致性检查
docs/           读者审读、版本、缺口和发行边界记录
notes/          供维护者追溯的源码阅读与证据笔记
references/     第三方材料；公开再分发权利尚未签收
TODO.md         开发记录、开放项和接续线索
```

## 维护记录

根 README 只保留当前的读者入口和项目状态。历史版本、旧构建页数、旧哈希和阶段性结论请查阅 [版本历史](docs/version-history-v0.110.md)；开发任务、阻塞项和下一步线索位于 [TODO.md](TODO.md)。WarpX 相邻源码树仅作只读证据入口，本项目不修改它。
