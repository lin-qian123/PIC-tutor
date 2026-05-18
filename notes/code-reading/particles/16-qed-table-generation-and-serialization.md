# QED lookup table 的生成、加载与序列化合同

绑定源码：

- `../warpx/Source/Particles/MultiParticleContainer.cpp`
- `../warpx/Source/Particles/ElementaryProcess/QEDInternals/QuantumSyncEngineWrapper.cpp`
- `../warpx/Source/Particles/ElementaryProcess/QEDInternals/BreitWheelerEngineWrapper.cpp`
- `../warpx/Examples/Tests/qed/inputs_test_2d_qed_quantum_sync`
- `../warpx/Examples/Tests/qed/inputs_base_2d_breit_wheeler`
- `../warpx/Examples/Tests/qed/inputs_base_3d_breit_wheeler`

这篇笔记只处理一个问题：WarpX 里 QED engine 依赖的 lookup tables 到底怎样在 `builtin / load / generate` 三条路径之间流动，以及这些表最终怎样落成所有 MPI rank 都能消费的统一二进制格式。

## 1. wrapper 内部实际持有的不是一张表，而是两张子表

`QuantumSyncEngineWrapper.cpp` 和 `BreitWheelerEngineWrapper.cpp` 都不是只包一张 lookup table。

Quantum Synchrotron wrapper 内部真正持有的是：

- `m_dndt_table`
- `m_phot_em_table`
- `m_qs_minimum_chi_part`

Breit-Wheeler wrapper 内部真正持有的是：

- `m_dndt_table`
- `m_pair_prod_table`
- `m_bw_minimum_chi_phot`

这解释了为什么前一篇笔记里看到的：

- `build_optical_depth_functor()`
- `build_phot_em_functor()`
- `build_pair_functor()`

都先断言 `m_lookup_tables_initialized == true`。WarpX 不是“有个 engine 就能跑 QED”，而是必须先把两张子表和最小 `chi` 门槛一起装进 wrapper。

## 2. builtin / load / generate 都必须先走 `lookup_table_mode`

`MultiParticleContainer::InitQuantumSync()` 和 `InitBreitWheeler()` 都要求输入显式提供：

- `qed_qs.lookup_table_mode`
- `qed_bw.lookup_table_mode`

支持的模式只有三种：

- `builtin`
- `load`
- `generate`

这里的分工很清楚：

- `builtin`：直接调用 wrapper 里硬编码的低分辨率测试表
- `load`：从外部二进制文件读 raw bytes，再反序列化成两张子表
- `generate`：运行时按 `ParmParse` 参数现生成两张表，再序列化到文件，并把同一份 raw bytes 广播给所有 rank

源码还显式提醒了一个边界：`builtin` 只适合测试，不是高分辨率生产表。

## 3. `builtin` 不是“默认空表”，而是 wrapper 里硬编码的低分辨率常量数组

`init_builtin_tables(...)` 在两个 wrapper `.cpp` 里都直接写了 hard-coded 数组。

这说明：

- builtin 模式不依赖外部文件
- builtin 模式也不依赖 `WARPX_QED_TABLE_GEN`
- builtin 模式不是“没有表就先凑合跑”

它本质上是 WarpX 内嵌的一组低分辨率参考表，只是源码自己也承认它主要面向测试。

## 4. `load` 与 `generate` 最终收敛到同一个 raw binary 格式

两个 wrapper 都提供：

- `init_lookup_tables_from_raw_data(...)`
- `export_lookup_tables_data()`

这两个接口说明了 WarpX 真正统一的表交换格式不是 C++ 对象，而是一段 bytes。

原始格式的第一层结构是：

1. 先写一个 `uint64_t size_first`
2. 紧跟第一张子表的序列化字节流
3. 再跟第二张子表的序列化字节流

也就是说，raw blob 的最前 8 字节只做一件事：告诉接收方“第一张子表多长”，这样 wrapper 才能把后面的剩余字节自动切给第二张子表。

对应到两类 engine：

- Quantum Synchrotron：`dndt` 表在前，photon-emission 表在后
- Breit-Wheeler：`dndt` 表在前，pair-production 表在后

这也是为什么 `load` 和 `generate` 最后其实没有两套消费路径。只要 raw bytes 格式一样，后面重建 wrapper 的逻辑就是同一套。

## 5. `generate` 不是内存分支，而是 “生成 -> 写文件 -> 广播同格式 bytes”

`MultiParticleContainer::QuantumSyncGenerateTable()` 和 `BreitWheelerGenerateTable()` 都是同一个结构：

1. 要求用户提供 `save_table_in`
2. 读取 `chi_min`
3. 只在 IOProcessor 上拼 PICSAR control struct
4. 调 wrapper 的 `compute_lookup_tables(...)`
5. 调 `export_lookup_tables_data()` 得到 raw bytes
6. 把 bytes 写入二进制文件
7. 用 `ReadAndBcastFile(...)` 把同一份 bytes 发给所有 rank
8. 非 IOProcessor 再用 `init_lookup_tables_from_raw_data(...)` 重建本地 wrapper

这条链最值得记的点是：

- `generate` 最终也会落成和 `load` 完全一样的二进制文件
- IOProcessor 直接保留内存中刚生成好的表
- 非 IOProcessor 不重新生成，而是靠广播后的 raw bytes 反序列化

因此 `generate` 与 `load` 的根本区别只在“这份 raw bytes 最初是谁造出来的”，而不在“后续运行期如何消费”。

## 6. `generate` 还受编译宏 `WARPX_QED_TABLE_GEN` 限制

两个 wrapper 的 `compute_lookup_tables(...)` 都有同一个边界：

- 只有编译了 `WARPX_QED_TABLE_GEN` 才能真正现生成表
- 否则直接 abort，并给出显式报错

所以：

- `builtin` 不要求 table-generation 编译支持
- `load` 也不要求
- 只有 `generate` 依赖这个编译路径

这也是为什么 examples 里常把 `generate/load` 段留成可切换模板，而默认 regression 更常走 builtin 或预生成文件。

## 7. Quantum Synchrotron 与 Breit-Wheeler 的 `generate` 参数不是同一张表的重命名

`QuantumSyncGenerateTable()` 读取两组子表参数：

- `tab_dndt_chi_min`
- `tab_dndt_chi_max`
- `tab_dndt_how_many`

以及

- `tab_em_chi_min`
- `tab_em_chi_max`
- `tab_em_chi_how_many`
- `tab_em_frac_min`
- `tab_em_frac_how_many`

其中第二组是 photon emission 的二维表，变量本质上是：

- source lepton `chi`
- emitted photon energy fraction

`BreitWheelerGenerateTable()` 的第一组 `tab_dndt_*` 类似，但第二组变成：

- `tab_pair_chi_min`
- `tab_pair_chi_max`
- `tab_pair_chi_how_many`
- `tab_pair_frac_how_many`

这里第二张表描述的是：

- source photon `chi`
- 产生对时的能量分配 fraction

所以虽然两者都有：

- 一张 `dndt` 表
- 一张二维采样表

但第二张表的物理含义并不相同，不能把 `tab_em_*` 和 `tab_pair_*` 看成相同参数族。

## 8. `photon_creation_energy_threshold` 不属于表本身，但会改变最终 product 统计

`InitQuantumSync()` 还额外读取：

- `qed_qs.photon_creation_energy_threshold`

它会从 `m_e c^2` 单位转成 SI，并传给后续 photon emission 路径。前一篇笔记已经看到，event pass 后还有：

- `cleanLowEnergyPhotons()`

因此这个阈值并不控制 lookup table 的生成，而是控制：

- 哪些已触发的 emission event 最终保留为 photon products

从 regression 角度看，这意味着：

- table 决定采样分布
- threshold 决定最终输出统计

两者不能混写成一层机制。

## 9. regression 输入文件里注释掉的 `generate/load` 段，本质上是在切同一生命周期的不同入口

`Examples/Tests/qed/inputs_test_2d_qed_quantum_sync`、`inputs_base_2d_breit_wheeler`、`inputs_base_3d_breit_wheeler` 里都能看到：

- `lookup_table_mode = builtin`
- 以及可切到 `load` / `generate` 的模板参数段

这说明这些 regression 不只是“验证某一套默认表”，还在给开发者保留一个明确的切换面：

- 用 builtin 跑快速默认回归
- 用 load 验证表文件读取合同
- 用 generate 验证 table-generation 编译路径和序列化合同

因此，QED regression 真正覆盖的不只 product physics，也隐含覆盖了 wrapper 的 table 生命周期。

## 10. 这一层与前一篇 QED kernel 笔记怎么接

前一篇已经说明：

- push 中先演化 `opticalDepthQSR/BW`
- event pass 中再调用 PICSAR-QED functor

这一篇补的是更早的前提：

1. `InitQED()` 先决定 `lookup_table_mode`
2. wrapper 必须先拿到两张子表和最小 `chi`
3. `build_*_functor()` 才能合法返回 device functor
4. push/event kernels 才真正有表可查

所以从主链上看，完整顺序已经变成：

```text
species runtime attrs
-> map/check product species
-> InitQED()
-> builtin/load/generate tables
-> build device functors
-> evolve optical depth in PushPX()
-> trigger events when optical depth < 0
-> update source and create products
```

这才是 WarpX 当前 QED 路径在“对象图 -> 表 -> kernel”三个层次上的完整闭环。
