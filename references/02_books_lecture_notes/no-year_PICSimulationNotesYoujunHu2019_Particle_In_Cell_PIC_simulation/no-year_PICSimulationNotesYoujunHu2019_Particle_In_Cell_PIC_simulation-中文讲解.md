# Particle In Cell (PIC) simulation 笔记

## 0. 资料信息

- 原题：Particle In Cell (PIC) simulation
- 作者：Youjun Hu
- 年份：2019（按文件名与讲义内容暂记）
- 类型：开放 lecture notes
- 本地 PDF：`no-year_PICSimulationNotesYoujunHu2019_Particle_In_Cell_PIC_simulation.pdf`
- MinerU Markdown：`no-year_PICSimulationNotesYoujunHu2019_Particle_In_Cell_PIC_simulation.md`
- 图片目录：`images/`
- 对 PIC-tutor 的用途：
  - Part I：PIC foundations
  - Part III：粒子表示、权重与 phase-space sampling
  - Part IV：shape / deposition 的基础直觉

## 1. 当前状态

- MinerU 转换已完成。
- 当前还没有做逐段中文精读。
- 这份讲义篇幅较长，后续应按原文顺序从 `Abstract`、`Particle methods`、`Phase-space sampling` 等部分开始逐段整理。

## 2. 后续精读入口

优先关注以下部分：

1. `Abstract`
   - 先确认作者怎样定义 PIC 与 particle methods 的关系。
2. `1 Particle methods`
   - 作为本书 Part I/II 里“为什么既需要粒子又需要网格”的背景材料。
3. `2 Phase-space sampling and markers' weight`
   - 对应本书里宏粒子权重、采样体积与 phase-space representation 的基础说明。

## 3. 章节用途记录

- `manuscript/chapters/01-kinetic-models.md`
  - 可用于补 PIC 作为 hybrid particle-mesh method 的讲义型背景叙述。
- `manuscript/chapters/02-pic-loop.md`
  - 可用于补“粒子沿 characteristic 线推进、场在网格上求解”的概念来源。
- `manuscript/chapters/04-particle-pushers.md`
  - 可用于补 marker weight、sampling 与 orbit-based interpretation 的前置背景。

## 4. 待办

- [ ] 按 `research-paper-explainer` 工作流逐段写中文总结。
- [ ] 在首次引用处插入关键图片说明。
- [ ] 对重要公式补 `$$ ... $$` 推导与变量解释。
- [ ] 把可直接服务 `PIC-tutor` 正文的段落摘到章节草稿里。
