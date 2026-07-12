# Hockney 1971 摘要级中文讲解

## 证据范围

本笔记只使用 IBM Research 的作者机构页面所公开的摘要和书目信息，不把摘要扩写成论文正文推导。原文 PDF、图表和逐段 MinerU 笔记仍未取得。

## 摘要主线

论文比较了 NGP、CIC 以及对势函数做平滑后的 HNGP、HCIC 四种二维热等离子体粒子模型。摘要给出的第一条工程结论是：碰撞时间对模型本身只弱依赖，主要由密度、Debye 长度和粒子宽度共同控制；因此粒子形状并不是只影响瞬时插值误差，也会改变长期统计演化的时间尺度。

第二条主线是数值加热。摘要把电场能量涨落写成与 `n(lambda_D^2 + W^2)` 相关的缩放，并把空间网格尺度 `H/lambda_D` 与时间步长 `omega_pe Delta t` 放到同一个参数平面中，给出一条 optimum path。对本书而言，这条关系的作用是把“shape、网格和时间步长共同决定数值健康度”从经验性提醒提升为可引用的摘要级设计约束。

摘要还报告了 optimum path 上 `tau_H/tau_coll` 的模型相关系数 `K_2`，并按允许的能量误差给出不同模型的适用区间。当前只能使用这些摘要级数值做路线图或参数解释，不能据此复现论文中的图、拟合过程或完整误差预算。

## 与 PIC-tutor 的连接

- 第 1 章：把 `lambda_D / Delta x`、粒子宽度和热等离子体长期时间尺度连接起来；
- 第 5 章：说明 shape order 与 smoothing 影响的不只是局部沉积，还包括统计噪声和长期 heating；
- 第 6 章：把 `tau_H/tau_coll` 作为稳定性和数值健康度的文献背景，而不是把短时 field regression 当作长期 thermal validation。

当前证据等级：`abstract-backed + metadata-verified; full-text missing`。
