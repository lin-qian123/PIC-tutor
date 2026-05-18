# 论文阅读与 Markdown 转换流程

本项目阅读和讲解论文时，采用 `research-paper-explainer` skill 的结构，并结合本项目的 `references/` 文献库组织方式执行。

## 1. 基本原则

- PDF 论文默认先用 MinerU 转换成 Markdown，不直接用 `pdftotext`、`pypdf` 等本地抽取替代。
- 只有 MinerU 不可用、被阻塞、PDF 不适合 MinerU，或用户明确要求本地转换时，才使用本地抽取作为 fallback。
- 转换得到的 Markdown、图片和中文讲解笔记必须保存在论文所在目录，不集中放到全局 `notes/`。
- 中文讲解笔记必须按论文自然顺序逐段整理，从摘要开始，按 section/subsection 顺序推进。
- 重要公式必须用 `$$ ... $$` 的 TeX display math 格式，并给出变量说明、推导过程、物理直觉和关键意义。
- 图片必须插入到首次引用处，不能集中放到文末。
- 长论文可以分段并行处理，但最终合并时必须保持原文顺序。

## 2. 目录组织

对 `references/<category>/<paper>.pdf` 这类已经下载好的 PDF，阅读前先建立论文专属子目录：

```text
references/<category>/<paper_stem>/
  <paper_stem>.pdf
  <paper_stem>.md
  images/
  <paper_stem>-中文讲解.md
  reading-log.md
```

如果 PDF 已经位于论文专属目录内，则不再额外嵌套新目录。

这样做的原因：

- MinerU 默认把图片输出到 `images/`，多篇论文共用一个分类目录会发生图片命名冲突。
- Markdown 中图片路径可以稳定写成 `images/<actual_image_file>`。
- 后续写书稿时可以直接引用论文目录，不会丢失上下文。

## 3. 转换流程

1. 确认 PDF 路径和主题分类。
2. 如果 PDF 还在分类目录根部，创建同级论文目录并把 PDF 移入或复制进去。
3. 在论文目录内运行 MinerU 转换：

```bash
cd references/<category>/<paper_stem>/
python /Users/yuxiangzhang/.agents/skills/research-paper-explainer/scripts/convert_mineru.py <paper_stem>.pdf
```

4. 检查输出：

```bash
ls
ls images 2>/dev/null
```

5. 读取 `<paper_stem>.md`，分析：
   - 标题、作者、年份、DOI/arXiv；
   - section/subsection 结构；
   - 图表出现位置；
   - 关键公式；
   - 与 PIC-tutor 书稿哪一章相关；
   - 与 WarpX 哪些源码路径或参数相关。

## 4. 中文讲解笔记格式

中文讲解笔记命名为：

```text
<paper_stem>-中文讲解.md
```

推荐结构：

```markdown
# <论文中文题名> 笔记

## 0. 论文信息

- 原题：
- 作者：
- 年份：
- DOI / arXiv：
- 本地 PDF：
- MinerU Markdown：
- 所属主题：
- 对 PIC-tutor 的用途：

## 1. 摘要

逐段总结摘要，不压缩成一句话。

## 2. <原文 Section Title>

### 2.1 <Subsection Title>

按段落顺序总结。

### 图 <n>: <图题>

![图像描述](images/<actual_image_filename>)

**图像描述：**

**物理含义：**

**关键解读：**

**与论文内容的关联：**

#### <公式名称>

$$
<formula>
$$

**变量说明：**

- `<symbol>`：

**推导过程：**

1. ...

**物理直觉：**

**关键点/物理意义：**

## N. 开放问题与个人理解

### N.1 理论端

### N.2 数值/实现端

### N.3 与 WarpX/PIC-tutor 的连接

## N+1. 复习用速记
```

## 5. 与书稿章节的连接

每篇论文读完后，在笔记中明确标出：

- 可支持的书稿章节；
- 对应的物理模型；
- 对应的算法；
- 可能对应的 WarpX 源码路径；
- 可能对应的 WarpX 输入参数；
- 是否需要后续复现实验或源码验证。

## 6. 质量检查

完成一篇论文的 Markdown 和中文讲解后，至少检查：

- Markdown 文件是否存在；
- `images/` 中图片路径是否能被笔记正确引用；
- 公式是否使用 `$$ ... $$`；
- 是否按原文顺序逐段整理；
- 是否记录文献信息和本地路径；
- 是否说明与 PIC-tutor 的用途；
- 是否存在需要回到 WarpX 源码验证的点。
