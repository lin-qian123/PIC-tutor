# 第 4 章版本化证据台账

本台账保存从第 4 章读者正文移出的版本化文献闭环记录。它保留论文资产、来源定位和证据边界；正文只说明这条综述如何帮助读者比较推进器与整个 PIC 离散链。

## Vay--Godfrey 2014 review 记录

### 4.4.2 v0.74 文献闭环：Vay--Godfrey 2014 review

Vay 与 Godfrey 的 2014 review 把粒子推进器放回完整 PIC 离散链：Maxwell 场更新、粒子 push、current deposition、field gather、filtering 和数值稳定性必须一起讨论。该文的 Boris relativistic rotation（式 29--35）与 Lorentz-invariant formulation（式 36--38）为本节的 Vay 2008 源码公式提供了历史和算法上下文，但 review 本身不是 `UpdateMomentumVay.H` 的函数级实现证明。

本书已将 9 页 PDF、MinerU 原文、43 张抽取图、论文顺序中文精读和访问边界保存在 `references/01_reviews_surveys/2014_VayFRACAD2014_Modeling_of_relativistic_plasmas_with_the_Particle-In-Cell_method/`，并由 `scripts/audit_vay_2014_review_asset_contract.py` 验收。出版信息以期刊记录为准：*Comptes Rendus Mécanique* 342 (2014), 610--618，DOI `10.1016/j.crme.2014.07.006`。

因此第 4 章的证据分层是：Vay 2008 负责 relativistic pusher 的原始算法，Vay--Godfrey 2014 review 负责把 Boris、Lorentz-invariant pusher 与场/源项/稳定性放入同一张方法谱系，WarpX 源码负责当前 kernel 的变量和时间层语义，case-local contract 负责有限运行证据。不能把 review 中的历史算法图或其他 PIC code 的结果直接写成当前 WarpX runtime PASS。
