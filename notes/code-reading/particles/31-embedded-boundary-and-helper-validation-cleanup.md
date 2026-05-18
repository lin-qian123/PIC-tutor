# `embedded_boundary` 余下条目、`electrostatic_sphere_eb` 与辅助绘图脚本的验证边界

绑定对象：

- `../warpx/Examples/Tests/particle_absorbing_boundary`
- `../warpx/Examples/Tests/embedded_boundary_cube`
- `../warpx/Examples/Tests/embedded_boundary_rotated_cube`
- `../warpx/Examples/Tests/embedded_boundary_diffraction`
- `../warpx/Examples/Tests/embedded_boundary_em_particle_absorption`
- `../warpx/Examples/Tests/embedded_boundary_python_api`
- `../warpx/Examples/Tests/electrostatic_sphere_eb`
- `../warpx/Examples/Tests/scraping`

这一组条目此前大多还停留在：

- `boundary condition`
- `electrostatic / Poisson`
- `general / to classify`

这样的粗标签上。

但实际看完 CMake、analysis 和输入以后，它们测的对象并不一样：

- 有些是解析场解对照
- 有些是 `BoundaryScraping` 记录链
- 有些是 EB 吸收粒子后 `divE` 是否留下伪电荷
- 有些只是辅助绘图脚本，不属于 regression 断言
- 还有一类虽然 CMake `analysis = OFF`，但 PICMI 输入脚本自己就在运行期做了 wrapper 断言

---

## 1. `particle_absorbing_boundary/plot_2d.py` 与 `plot_phase.py`：只是可视化 helper

这两个脚本都不该继续被当成“analysis 脚本”。

### 1.1 `plot_2d.py`

它只做：

- 打开一个 full diagnostics plotfile
- 对 `Ez` 画 `yt.SlicePlot`
- 保存 `particle_absorbing_boundary_2d_Ez.png`

因此它的角色只是：

- 2D 吸收边界算例的人工可视化 helper

不提供任何自动断言。

### 1.2 `plot_phase.py`

它只做：

- 读取 `diags/reducedfiles/PhaseSpaceElectrons`
- 取第 `8000` 步的 reduced diagnostic
- 画 `log10(data)` 相空间图

因此它的角色只是：

- 1D `PhaseSpaceElectrons` reduced diagnostic 的相图 helper

同样不提供自动断言。

---

## 2. `embedded_boundary_cube` 与 `embedded_boundary_rotated_cube`：PEC cavity 模式的解析场对照

这两组都不是“普通 EB 几何冒烟测试”，而是在测：

- ECT/EB 几何处理后
- PEC cavity 中电磁模态
- 是否仍与解析本征模一致

### 2.1 `embedded_boundary_cube`

`analysis_fields.py` 和 `analysis_fields_2d.py` 都显式构造了解析磁场模态：

- 2D：比较 `By`，并顺手比较 `Ey / c`
- 3D：比较 `By` 与 `Bz`
- 3D `macroscopic` 版本只是在同一 cavity 模态上把频率按 `epsilon_r = 1.5` 修正

因此这组最准确的标签应是：

- `embedded boundary / PEC cavity eigenmode`

### 2.2 `embedded_boundary_rotated_cube`

这组不是简单复制前一组，而是在测：

- cavity 几何绕轴旋转后
- EB cut-cell 几何与 ECT 场更新
- 是否仍能恢复旋转后的解析模态

2D/3D analysis 都显式做了坐标旋转，再比较 `By` 或 `By/Bz` 的相对 `L2` 误差。

因此更准确的标签应是：

- `embedded boundary / rotated PEC cavity eigenmode`

---

## 3. `embedded_boundary_diffraction`：RZ 衍射角强分析

`embedded_boundary_diffraction` 当前只有一个 RZ test，但它不是 checksum-only。

`analysis_fields.py` 直接：

- 从 openPMD 读取 `Ex`
- 对 `E^2` 做轴向平滑
- 提取衍射图样第一极小值对应的半径
- 与 Airy pattern 预测
  $$
  \theta \approx \arcsin(1.22\lambda/d)/2
  $$
  做比较

因此它测的是：

- `embedded boundary / diffraction / Airy first minimum`

而不是泛化的 boundary condition。

---

## 4. `embedded_boundary_em_particle_absorption`：吸收粒子后不应留下静态伪电荷

这组最关键的 analysis 是：

- 对 `divE` 在若干时间步上做时间平均
- 去掉沿 EB 传播的真实电磁波成分
- 只保留可能静止在吸收位置附近的伪 `divE`

然后分维度断言：

- 2D
- 3D
- RZ

的最大误差都低于维度相关阈值。

所以它真正测的是：

- `embedded boundary / EM particle absorption / no spurious charge build-up`

而不是一般的“粒子被吸收了”。

此外 `sh_factor_1/2/3` 不是不同物理问题，而是在重复覆盖不同 particle shape factor 组合。

---

## 5. `embedded_boundary_python_api`：PICMI wrapper 断言，不是 plotfile analysis

这组 CMake 里 `analysis = OFF`，因此如果只看 CMake 很容易误判成纯 checksum。

但真正的断言在输入脚本
[inputs_test_3d_embedded_boundary_picmi.py](/Volumes/PHILIPS/programs/PIC/warpx/Examples/Tests/embedded_boundary_python_api/inputs_test_3d_embedded_boundary_picmi.py)
内部：

- 运行 `sim.step(1)`
- 直接从 Python wrapper 取：
  - `edge_lengths`
  - `face_areas`
- 在中间切片上重建 cavity 截面的：
  - perimeter
  - area
- 与解析几何值比较

因此它真正测的是：

- `embedded boundary / PICMI Python wrapper / edge_lengths-face_areas`

而 checksum 只是补一个输出基线。

---

## 6. `electrostatic_sphere_eb`：分成 3D sphere-charge、RZ log-potential 和 mixed-BC checksum 包装

这组不能再笼统写成 `electrostatic / Poisson`。

### 6.1 3D `analysis.py`

3D analysis 的断言其实有两层：

1. reduced diagnostics `eb_charge.txt` 与理论球导体电荷
   $$
   q = 4\pi \epsilon_0 \phi_0 R
   $$
   的比较
2. `eb_covered` 场是否满足：
   - 内部为 `1`
   - 外部为 `0`
   - 取值始终在 `[0,1]`

因此 3D native / PICMI 版本测的是：

- `embedded boundary / electrostatic sphere charge`
- `eb_covered` 几何占据场

### 6.2 RZ `analysis_rz.py` 与 `analysis_rz_mr.py`

RZ 版本不是球，而是圆柱壳电势问题，解析解是：
$$
\phi(r)=A+B\log r,\qquad E_r(r)=-B/r.
$$

`analysis_rz.py` 在 level 0 比较：

- `phi`
- `Er`

`analysis_rz_mr.py` 则把同一对照推广到：

- 每个 refinement level
- patch 内非零有效区域

因此 RZ 两个 test 应记成：

- `embedded boundary / electrostatic cylinder / analytic phi-Er`
- `embedded boundary / electrostatic cylinder / MR analytic phi-Er`

### 6.3 `mixed_bc`

`inputs_test_3d_electrostatic_sphere_eb_mixed_bc` 当前没有独立 analysis。

它的价值在于：

- 对同一 EB electrostatic sphere 场景
- 覆盖 `pec/pec/neumann` 与 `pec/neumann/neumann`
  这类 mixed field boundary condition 组合

因此它当前最准确的表述应当是：

- `embedded boundary / electrostatic sphere / mixed-BC checksum baseline`

---

## 7. `scraping`：RZ EB scraping 与 `plot_filter_function` 的 writer 合同

这组和前面的 `point_of_contact_eb` 不一样。

它不关心接触点几何，而关心：

- 粒子是否在撞到 RZ embedded boundary 后被删除
- `BoundaryScraping` 是否完整记录这些被删粒子
- `plot_filter_function` 是否只保留指定半域中的 scraped particles

### 7.1 `analysis_rz.py`

它做三类检查：

1. 最终 simulation box 里应只剩 `512` 个粒子
2. 对每个 iteration，`remaining + scraped = initial`
3. 初始 `id` 与 “最终 box 中 + scraped buffer 中”的 `id` 集合完全一致

因此它测的是：

- `embedded boundary / BoundaryScraping / particle accounting`

### 7.2 `analysis_rz_filter.py`

它保留上面的计数逻辑，但额外要求：

- 只有 `z > 0` 半域的 scraped particles 被记录
- 因此满足
  $$
  2 n_{\rm scraped} + n_{\rm remaining} = n_{\rm total}
  $$
- 并且 scraped buffer 中没有 `z <= 0` 粒子

因此 filter 变体最准确的标签应是：

- `embedded boundary / BoundaryScraping / plot_filter_function`

---

## 8. 这一轮清理后，剩余 EB 条目应如何理解

这组条目现在至少应分成以下几类：

- `particle_absorbing_boundary/plot_*.py`
  - 只是 visualization helper
- `embedded_boundary_cube` / `embedded_boundary_rotated_cube`
  - PEC cavity eigenmode analytic checks
- `embedded_boundary_diffraction`
  - Airy diffraction-angle analysis
- `embedded_boundary_em_particle_absorption`
  - no-spurious-charge check after EB absorption
- `embedded_boundary_python_api`
  - PICMI wrapper geometry-field access contract
- `electrostatic_sphere_eb`
  - 3D sphere charge + `eb_covered`
  - RZ analytic `phi/Er`
  - mixed-BC checksum baseline
- `scraping`
  - scraped-particle accounting
  - scraped-particle filter contract
- `embedded_boundary_removal_depth_*`
  - 当前本地 checkout 中只剩 benchmark JSON
  - 未看到对应 `Examples/Tests` 目录
  - 应先记成 legacy checksum-only names，而不是继续挂在“待反查 inputs/analysis”名下

所以它们不应再继续挤在：

- `boundary condition`
- `electrostatic / Poisson`
- `general / to classify`

这三个过粗的占位桶里。
