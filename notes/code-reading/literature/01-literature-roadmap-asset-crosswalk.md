# 第 9 章文献路线与本地资产交叉核对

本笔记把第 9 章的路线图声明绑定到仓库内可以直接检查的对象。它不是论文内容正确性的替代证明，也不把 metadata、摘要或相关会议稿提升为目标论文的正文证据。

## 1. 交叉核对范围

合同脚本 `scripts/audit_literature_roadmap_asset_contract.py` 当前检查 12 项：

- A/B/C/D 四层证据定义和“只有 A 层才可写成已核实一手证据”的规则；
- `Birdsall 1985`、`Tajima-Dawson 1979`、`Dawson 1983`、`Vay 2008`、`Higuera-Cary 2017`、`Godfrey 2014`、`Kirchen 2016`、`Lehe 2016` 八条核心文献目录；
- 章节名称、总文献表和生成式 inventory 是否仍保有对应锚点；
- `Tajima-Dawson 1982`、`Esirkepov 2001`、`LeeCPC2015`、`Yee 1966`、`Hockney-Eastwood` 的缺口边界；
- acquisition 计划是否仍回指 `docs/literature-map.md` 与 `references/00_index/books_to_locate.md`。

## 2. 证据边界

通过该合同只说明“章节路线图与仓库资产状态一致”。它不证明：

1. 中文讲解已经完成逐式审校；
2. 预印本与出版社排版版逐页等价；
3. WarpX runtime 结果已经验证某篇论文的全部物理结论。

因此，`Esirkepov 2001` 的作者预印本、`LeeCPC2015` 的 accepted manuscript，以及 Tajima 相关 FNAL 会议稿仍按章节中声明的边界使用。

## 3. 运行命令

```bash
python scripts/audit_literature_roadmap_asset_contract.py \
  --project-root . \
  --output-json runs/stage-c-validation/literature-roadmap-asset-contract/contract.json \
  --output-md runs/stage-c-validation/literature-roadmap-asset-contract/contract.md
```

当前合同输出应为 `12/12 PASS`。后续新增或替换 primary source 时，应先更新本合同，再更新第 9 章和 `references/00_index`。
