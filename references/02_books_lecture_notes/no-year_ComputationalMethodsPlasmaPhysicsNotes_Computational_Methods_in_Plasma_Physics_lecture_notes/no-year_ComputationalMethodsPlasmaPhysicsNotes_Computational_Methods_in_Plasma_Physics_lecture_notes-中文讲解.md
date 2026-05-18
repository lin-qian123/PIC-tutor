# Computational Methods in Plasma Physics lecture notes 笔记

## 0. 资料信息

- 原题：Computational Methods in Plasma Physics lecture notes
- 作者：Ammar Hakim
- 年份：按讲义正文可见版本记为 2020.8
- 类型：开放 lecture notes / course material
- 本地 PDF：`no-year_ComputationalMethodsPlasmaPhysicsNotes_Computational_Methods_in_Plasma_Physics_lecture_notes.pdf`
- MinerU Markdown：`no-year_ComputationalMethodsPlasmaPhysicsNotes_Computational_Methods_in_Plasma_Physics_lecture_notes.md`
- 图片目录：`images/`
- 对 PIC-tutor 的用途：
  - Part I：Vlasov-Maxwell 大图景
  - Part V：FDTD / Maxwell background
  - Part X：fluid moments / hyperbolic PDE 视角

## 1. 当前状态

- MinerU 转换已完成。
- 当前还没有按 lecture 顺序做中文精读。
- 这份讲义更像“课程总览”，适合先抽取：
  - Vlasov-Maxwell 大图景
  - FDTD / ODE integrators
  - fluid / finite-volume / hyperbolic PDE 背景

## 2. 后续精读入口

优先关注：

1. `Lecture 1: Introduction and the Big-Picture`
   - 服务本书开篇对 plasma-computation landscape 的定位。
2. `Lecture 2: Special ODE Integrators, FDTD Scheme`
   - 服务 pushers 与 FDTD 主线。
3. 后续 fluid / hyperbolic PDE 相关 lecture
   - 服务 `Fluids/` 和数值方法章节。

## 3. 章节用途记录

- `manuscript/chapters/01-kinetic-models.md`
  - 可用于补 Vlasov-Maxwell 全景式引导。
- `manuscript/chapters/04-particle-pushers.md`
  - 可用于补 special ODE integrators 的课程背景。
- `manuscript/chapters/06-field-solvers.md`
  - 可用于补 FDTD / Maxwell lecture-style 叙述。
- `manuscript/chapters/04-particle-pushers.md` 与未来 fluid 章节
  - 可用于补 moments、closure、hyperbolic PDE 视角。

## 4. 待办

- [ ] 按 lecture 顺序逐段写中文总结。
- [ ] 在首次引用处插入关键图片说明。
- [ ] 对关键公式补 `$$ ... $$` 推导与变量解释。
- [ ] 把可直接服务 `PIC-tutor` 正文的段落摘到相应章节草稿。
