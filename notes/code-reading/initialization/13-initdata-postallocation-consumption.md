# `InitData()` 后半消费链：space-charge、external fields、callback、初始 diagnostics

绑定源码：

- `../warpx/Source/Initialization/WarpXInitData.cpp`

前两篇初始化笔记已经把：

- `ReadParameters()` 如何裁组合
- `AllocLevelMFs()` 如何把组合摊成字段和对象

写清了。这一篇只做最后一步：这些已经分配好的对象，在 `InitData()` 后半到底按什么顺序被消费，fresh run 和 restart 在这里如何分叉，以及第 0 步 diagnostics 到底是在什么状态上写出的。

## 1. `InitData()` 后半的总顺序

源码位置：`../warpx/Source/Initialization/WarpXInitData.cpp:800-947`。

```cpp
if (restart_chkfile.empty())
{
    ComputeDt();
    InitFromScratch();
    InitDiagnostics();
}
else
{
    InitFromCheckpoint();
    PostRestart();
    reduced_diags->InitData();
}

ComputeMaxStep();
ComputePMLFactors();
if (WarpX::use_fdtd_nci_corr) { WarpX::InitNCICorrector(); }
BuildBufferMasks();

if (m_em_solver_medium == MediumForEM::Macroscopic) { ... InitData(...); }
m_electrostatic_solver->InitData();
if (WarpX::electromagnetic_solver_id == ElectromagneticSolverAlgo::HybridPIC) {
    m_hybrid_pic_model->InitData(m_fields);
}

CheckGuardCells();
WriteUsedInputsFile();

if (m_do_initial_div_cleaning) { WarpX::ProjectionCleanDivB(); }

if (restart_chkfile.empty())
{
    ExecutePythonCallback("beforeInitEsolve");
    ...
    ComputeSpaceChargeField(reset_fields);
    ...
    ExecutePythonCallback("afterInitEsolve");
    for (int lev = 0; lev <= max_level; ++lev) {
        AddExternalFields(lev);
    }
}
else {
    ExecutePythonCallback("afterInitatRestart");
}

if (restart_chkfile.empty() || write_diagnostics_on_restart) {
    multi_diags->FilterComputePackFlush(istep[0] - 1);
    if (reduced_diags->m_plot_rd != 0) {
        reduced_diags->ComputeDiags(istep[0] - 1);
        reduced_diags->WriteToFile(istep[0] - 1);
    }
}
```

所以后半主链不是“初始化完粒子后就结束”，而是至少还分四层：

1. 运行态辅助结构收尾
   - `ComputeMaxStep`
   - `ComputePMLFactors`
   - `InitNCICorrector`
   - `BuildBufferMasks`
2. 已分配对象的首次 `InitData`
   - macroscopic medium
   - electrostatic solver
   - hybrid PIC model
3. 初始场修正与初始场求解
   - `ProjectionCleanDivB`
   - `ComputeSpaceChargeField`
   - `ComputeMagnetostaticField`
   - `AddExternalFields`
4. 第 0 步输出
   - full diagnostics
   - reduced diagnostics

## 2. restart 和 fresh run 在这里只共享“后处理骨架”，不共享场求解链

fresh run 和 restart 前半都要进：

- `ComputeMaxStep`
- `ComputePMLFactors`
- `BuildBufferMasks`
- `m_electrostatic_solver->InitData()`
- `CheckGuardCells()`

但后面的物理主链明显不同：

- fresh run：
  - 可做 `ProjectionCleanDivB`
  - 可做初始 self-field / electrostatic solve
  - 然后把 external grid fields 加进主场
- restart：
  - 不再重跑初始场求解
  - 只走 `ExecutePythonCallback("afterInitatRestart")`
  - 之后直接视 `write_diagnostics_on_restart` 决定要不要写一次 diagnostics

所以 `restart` 不是“重新执行一遍 fresh-run 初始化”，而是“恢复状态后做最小必要收尾”。

## 3. `m_electrostatic_solver->InitData()` 和 `ComputeSpaceChargeField()` 不是一回事

源码位置：`../warpx/Source/Initialization/WarpXInitData.cpp:852-860, 892-905`。

```cpp
m_electrostatic_solver->InitData();

...

if( (electrostatic_solver_id != ElectrostaticSolverAlgo::None ||
     has_initialize_self_fields ||
     has_boundary_potential)
    && WarpX::electromagnetic_solver_id != ElectromagneticSolverAlgo::HybridPIC)
{
    bool const reset_fields = false;
    ComputeSpaceChargeField(reset_fields);
    if (electrostatic_solver_id == ElectrostaticSolverAlgo::LabFrameElectroMagnetostatic) {
        ComputeMagnetostaticField();
    }
}
```

这两步很容易被误读成“先 `InitData()`，后 solve，一回事”。其实不是：

- `m_electrostatic_solver->InitData()`
  - 属于 solver 对象自己的初始化
  - 发生在所有路径上，包括 restart
- `ComputeSpaceChargeField(reset_fields=false)`
  - 属于 fresh-run 的初始自洽场构造
  - 只在需要时触发

触发条件也不是“只有 electrostatic solver 才会跑”。源码实际上允许三种来源触发：

1. `electrostatic_solver_id != None`
2. 任意 species 打开 `initialize_self_fields`
3. Poisson boundary handler 指定了 boundary potential

但它又明确排除了：

- `electromagnetic_solver_id == HybridPIC`

所以这里的真实语义是：初始化阶段允许为普通 PIC/electrostatic 路径构造一次初始 self-field，但 hybrid PIC 不走这一条。

## 4. `reset_fields = false` 说明初始自洽场是在“保留已有外加场”的前提下解的

源码位置：`../warpx/Source/Initialization/WarpXInitData.cpp:900-904`。

```cpp
bool const reset_fields = false; // Do not erase previous user-specified values on the grid
ComputeSpaceChargeField(reset_fields);
```

这里的关键不是布尔值本身，而是注释直接说明：

- 初始 self-field solve 默认不会先擦掉用户已经写到网格上的值

因此初始化语义不是“先清空主场，再纯粹解一个 space-charge 场”，而是：

- 保留当前已经存在的 grid state
- 再叠加或修正 self-field

这和后面的 `AddExternalFields()` 配合起来，构成了一个很重要的初始化合同：

- 一部分外加/解析场已经在前面写进字段或辅助寄存器
- 初始 self-field solve 默认不把它们抹掉
- 最后再把 `fp_external` 统一加到 fine-patch 主场上

## 5. `ProjectionCleanDivB()` 发生在初始 field solve 之前

源码位置：`../warpx/Source/Initialization/WarpXInitData.cpp:882-885, 892-905`。

```cpp
if (m_do_initial_div_cleaning) {
    WarpX::ProjectionCleanDivB();
}

if( ... ) {
    ComputeSpaceChargeField(reset_fields);
    ...
}
```

这意味着初态 `B` 场的 divergence cleaning 顺序非常明确：

1. 先完成外部场读入、PML/buffer/solver 初始化等基础收尾
2. 若需要，先对加载的外部 `B` 场做 `ProjectionCleanDivB()`
3. 再进入初始 electrostatic / self-field solve

所以 `ProjectionCleanDivB()` 不是最终输出前的 cosmetic 修补，而是在任何 fresh-run 初始 field solve 之前就要完成的前置修正。

## 6. Python callback 只包裹 fresh-run 的初始场求解窗口

源码位置：`../warpx/Source/Initialization/WarpXInitData.cpp:887-907, 915`。

```cpp
if (restart_chkfile.empty())
{
    ExecutePythonCallback("beforeInitEsolve");
    ...
    ComputeSpaceChargeField(reset_fields);
    ...
    ExecutePythonCallback("afterInitEsolve");
    ...
}
else {
    ExecutePythonCallback("afterInitatRestart");
}
```

这三类 callback 的语义边界很清楚：

- `beforeInitEsolve`
  - 只在 fresh run
  - 发生在初始 self-field / electrostatic solve 之前
- `afterInitEsolve`
  - 只在 fresh run
  - 发生在初始 solve 之后、`AddExternalFields()` 之前
- `afterInitatRestart`
  - 只在 restart
  - 表示“恢复完状态后的钩子”，不是初始求解窗口的一部分

所以 callback 这里不是一个统一“初始化完成后调一下 Python”的接口，而是明确把：

- fresh-run 初始场求解窗口
- restart 后处理窗口

拆成了不同事件名。

## 7. `AddExternalFields()` 是在初始 solve 之后，把 `fp_external` 加回 fine-patch 主场

源码位置：`../warpx/Source/Initialization/WarpXInitData.cpp:908-912, 951-985`。

```cpp
for (int lev = 0; lev <= max_level; ++lev) {
    AddExternalFields(lev);
}
```

`AddExternalFields()` 本身只操作 `Efield_fp/Bfield_fp`：

```cpp
if (m_p_ext_field_params->E_ext_grid_type == ExternalFieldType::constant) {
    Efield_fp[lev][0]->plus(...);
}
else {
    amrex::MultiFab::Add(*Efield_fp[lev][0], *m_fields.get(FieldType::Efield_fp_external, Direction{0}, lev), ...);
}
```

这里有两个边界：

1. 它处理的是 grid external fields，不处理 particle-only external fields。
2. 它发生在 `afterInitEsolve` 之后，所以 fresh-run 第 0 步最终主场是：
   - 初始 self-field / electrostatic solve 结果
   - 再加上 `fp_external`

因此 `fp_external` 的角色不是“供 solver 读的边界条件场”，而是“在初始化求解结束后显式加回主场的外加项”。

## 8. `LoadExternalFields()` 先装填 external buffers，`AddExternalFields()` 后叠加到主场

源码位置：`../warpx/Source/Initialization/WarpXInitData.cpp:1428-1714`。

`LoadExternalFields(lev)` 会做三类事情：

1. 把 external grid fields 读到：
   - `Efield_fp_external`
   - `Bfield_fp_external`
2. 在 finest level 触发：
   - `ExecutePythonCallback("loadExternalFields")`
3. 把 particle external fields 读到：
   - `E_external_particle_field`
   - `B_external_particle_field`

所以它和 `AddExternalFields()` 的关系是：

- `LoadExternalFields()`：准备 external buffers
- `AddExternalFields()`：把 grid external buffers 合并进主场

二者不是重复逻辑，而是“装填”和“提交”的两步。

## 9. 第 0 步 diagnostics 写在所有这些消费动作之后

源码位置：`../warpx/Source/Initialization/WarpXInitData.cpp:918-927`。

```cpp
if (restart_chkfile.empty() || write_diagnostics_on_restart) {
    multi_diags->FilterComputePackFlush(istep[0] - 1);

    if (reduced_diags->m_plot_rd != 0)
    {
        reduced_diags->ComputeDiags(istep[0] - 1);
        reduced_diags->WriteToFile(istep[0] - 1);
    }
}
```

这意味着第 0 步 diagnostics 的写出状态已经包含：

- fresh run：
  - `ProjectionCleanDivB`
  - 初始 self-field / electrostatic solve
  - magnetostatic solve（若适用）
  - `AddExternalFields()`
- restart：
  - checkpoint 恢复态
  - `PostRestart()` 后的最小收尾
  - 可选 `write_diagnostics_on_restart`

因此第 0 步 diagnostics 不是“输入初值快照”，而是“初始化主链完成后的第一份可运行状态快照”。

## 10. 结尾的 `CheckKnownEMSolverIssues(...)` 不是初始化主链的一部分，而是告警审计尾声

源码位置：`../warpx/Source/Initialization/WarpXInitData.cpp:939-947`。

```cpp
::CheckKnownEMSolverIssues(
    electromagnetic_solver_id, current_deposition_algo,
    is_any_boundary_pml, external_particle_field_used);
```

这一步发生在 diagnostics 之后，输入只是：

- solver 类型
- current deposition
- 是否有 PML
- 是否使用 external particle fields

所以它不参与初态构造，而是对当前组合做一次已知问题告警审计。放在阅读顺序上，应该把它归到“初始化尾声的风险提示”，不要和前面的物理初始化动作混在一起。

## 11. 小结：`InitData()` 后半真正闭合了初始化合同

把这篇和前两篇连起来，`Initialization` 这条主线现在可以压成四段：

1. 启动层与 `ReadParameters()`
   - 锁定全局契约
   - 裁掉非法组合
2. `AllocLevelMFs()`
   - 把组合摊成字段和对象
3. `InitData()` 后半消费链
   - buffer/PML/NCI/macroscopic/electrostatic/hybrid 初始化
   - divergence cleaning
   - initial self-field solve
   - external field 提交
   - callback
4. 第 0 步 diagnostics
   - 对“已完成初始化的可运行状态”做第一次输出

也就是说，到这一层为止，初始化不再只是“建网格、加粒子、读外场”。它已经完整闭合成：

- 参数约束
- 字段分配
- 初态修正
- 初态场求解
- 初始输出

这一整条真实执行链。
