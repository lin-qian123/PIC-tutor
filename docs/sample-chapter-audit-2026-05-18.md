# 样章严格审查记录（2026-05-18）

本轮只审样章范围，不把全书一起混进来。依据的是计划文档对“样章”的要求：

- [master-plan.md](/Volumes/PHILIPS/programs/PIC/PIC-tutor/docs/master-plan.md)
- [warpx-full-code-reading-book-plan.md](/Volumes/PHILIPS/programs/PIC/PIC-tutor/docs/warpx-full-code-reading-book-plan.md)

当前样章对象锁定为：

- [02-pic-loop.md](/Volumes/PHILIPS/programs/PIC/PIC-tutor/manuscript/chapters/02-pic-loop.md)
- [03-warpx-evolve.md](/Volumes/PHILIPS/programs/PIC/PIC-tutor/manuscript/chapters/03-warpx-evolve.md)

## 审查标准

按计划文档，样章至少应闭合这些层次：

1. 公式推导
2. 代码路径
3. 调用链图
4. 参数示例
5. 最小运行案例
6. 参考文献
7. 进一步阅读
8. 练习题
9. 源码版本声明

## 审查结果

| 项目 | 第 2 章 | 第 3 章 | 结论 |
|---|---|---|---|
| 公式推导 | 已有 | 已有 | 通过 |
| 代码路径 | 已有 | 已有 | 通过 |
| 调用链图 | 以主循环层次表述为主 | 已有 Mermaid 调用图 | 通过 |
| 参数示例 | 本轮补入 Langmuir 参数骨架 | 本轮补入 Langmuir runtime 参数骨架 | 通过 |
| 最小运行案例 | 本轮补入本地 Langmuir 实跑命令与检查量 | 本轮补入同一运行闭环落点 | 通过 |
| 参考文献 | 已有基础文献清单 | 之前较弱，本轮仍主要依赖代码笔记与相邻章节 | 基本通过 |
| 进一步阅读 | 本轮补入 | 本轮补入 | 通过 |
| 练习题 | 本轮补入 | 本轮补入 | 通过 |
| 源码版本声明 | 本轮补入 commit | 本轮补入 commit | 通过 |

## 本轮实际修补

### 第 2 章

本轮新增：

- 源码版本声明
- `2.8 参数示例与最小运行案例`
- `2.10 进一步阅读与练习`

因此第 2 章现在已经同时具备：

- 连续模型和离散公式
- WarpX 主循环源码入口
- 本地参数例子
- 本地最小实跑证据
- 文献清单
- 进一步阅读与练习题

### 第 3 章

本轮新增：

- 源码版本声明
- `3.12 参数示例与最小运行闭环`
- `3.13 进一步阅读与练习`

因此第 3 章现在已经同时具备：

- `main.cpp -> WarpX::Evolve()` 调用链
- 关键源码路径与源码原文
- 参数入口
- 本地最小实跑命令和输出路径
- 进一步阅读与练习题

## 当前剩余边界

这轮审查收掉的是“样章结构缺口”，不是“全书终审”。

仍然保留的更高层剩余项：

1. 第 2/3 章之外，其他章节还没做同等级严格审查。
2. `uniform_plasma` 的 checksum 脚本本机还没完整复跑，因为当前环境缺：
   - `yt`
   - `openpmd_viewer`
3. `Yee 1966` 与 `Hockney-Eastwood` 的 primary-source acquisition 还没闭环，因此基础章节文献层仍有明确缺口。

## 审查结论

对“样章”这一层而言，第 2/3 章现在已经比本轮之前更接近计划文档定义的可审阅状态。下一步不该再回到泛化扩写，而应优先做：

1. 把这轮样章审查完成态写回项目状态文件；
2. 再决定是否把同等级审查扩展到第 4/5/6 章。
