# Esirkepov 2001 bounded compare contract

本 note 固化当前可以自动复核的 Esirkepov 2001 证据边界。脚本为 `scripts/audit_esirkepov_bounded_compare.py`，报告归档于 `runs/stage-c-validation/esirkepov-bounded-compare/contract.{json,md}`。

## 已通过的结构检查

- 本地作者预印本和 MinerU Markdown 存在；
- 预印本题名、Section 1-5、`Eq.(23)` 和 second-order spline 段落均可检索；
- CPC 发表题名、DOI `10.1016/S0010-4655(00)00228-9` 和卷期页码已记录；
- access audit 明确记录 publisher-formatted PDF 仍缺失。

## 证据边界

该 contract 的 `passed=true` 表示“预印本结构 + 发表元数据 + 缺失状态”内部一致，不表示 CPC publisher PDF 已获得，也不表示完成逐页、逐式或版式 compare。第 5 章仍应使用 `preprint-backed + source-grounded + publication metadata verified` 的证据等级。

真正取得发表版 PDF 后，仍需重新执行 title / abstract / section numbering / `Eq.(23)` / second-order spline 五项 bounded compare，并将结果与本 contract 并列保存。
