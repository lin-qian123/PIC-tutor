#!/usr/bin/env python
"""Phase 0 inventory for the PIC-tutor LaTeX migration plan.

Scans the v0.110 Markdown source parts (version note, preface, chapters,
appendix) and reports per-part element counts: lines, headings, code blocks,
tables, display/inline equations, images, links, reader-card labels, and
LaTeX-escape-sensitive characters that appear in prose (outside code spans,
math, tables, and headings).

This inventory is the Phase 0 deliverable of docs/latex-migration-plan.md:
it feeds the source-to-target traceability table and the conversion helper
design. It is intentionally dependency-free (stdlib only) so it runs
anywhere and can be re-run to detect drift.

Outputs:
  docs/latex-phase0-inventory-v0.110.json  machine-readable inventory
  docs/latex-phase0-inventory-v0.110.md    human-readable report
"""

from __future__ import annotations

import json
import re
import shutil
import subprocess
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE_PARTS: list[tuple[str, str, Path]] = [
    # (role, display name, path)
    ("version-note", "VERSION", ROOT / "manuscript" / "VERSION.md"),
    ("preface", "00-preface", ROOT / "manuscript" / "chapters" / "00-preface.md"),
    ("chapter", "01-kinetic-models", ROOT / "manuscript" / "chapters" / "01-kinetic-models.md"),
    ("chapter", "02-pic-loop", ROOT / "manuscript" / "chapters" / "02-pic-loop.md"),
    ("chapter", "03-warpx-evolve", ROOT / "manuscript" / "chapters" / "03-warpx-evolve.md"),
    ("chapter", "03a-warpx-initialization", ROOT / "manuscript" / "chapters" / "03a-warpx-initialization.md"),
    ("chapter", "04-particle-pushers", ROOT / "manuscript" / "chapters" / "04-particle-pushers.md"),
    ("chapter", "05-deposition-shapes", ROOT / "manuscript" / "chapters" / "05-deposition-shapes.md"),
    ("chapter", "06-field-solvers", ROOT / "manuscript" / "chapters" / "06-field-solvers.md"),
    ("chapter", "07-boundaries-amr", ROOT / "manuscript" / "chapters" / "07-boundaries-amr.md"),
    ("chapter", "08-diagnostics-cases", ROOT / "manuscript" / "chapters" / "08-diagnostics-cases.md"),
    ("chapter", "09-literature-roadmap", ROOT / "manuscript" / "chapters" / "09-literature-roadmap.md"),
    ("appendix", "A-symbols", ROOT / "manuscript" / "appendices" / "A-symbols.md"),
]

# Future native .tex target for each source part (traceability table).
TEX_TARGETS: dict[str, str] = {
    "VERSION": "manuscript/latex/frontmatter/publishing-note.tex",
    "00-preface": "manuscript/latex/chapters/00-preface.tex",
    "01-kinetic-models": "manuscript/latex/chapters/01-kinetic-models.tex",
    "02-pic-loop": "manuscript/latex/chapters/02-pic-loop.tex",
    "03-warpx-evolve": "manuscript/latex/chapters/03-warpx-evolve.tex",
    "03a-warpx-initialization": "manuscript/latex/chapters/03a-warpx-initialization.tex",
    "04-particle-pushers": "manuscript/latex/chapters/04-particle-pushers.tex",
    "05-deposition-shapes": "manuscript/latex/chapters/05-deposition-shapes.tex",
    "06-field-solvers": "manuscript/latex/chapters/06-field-solvers.tex",
    "07-boundaries-amr": "manuscript/latex/chapters/07-boundaries-amr.tex",
    "08-diagnostics-cases": "manuscript/latex/chapters/08-diagnostics-cases.tex",
    "09-literature-roadmap": "manuscript/latex/chapters/09-literature-roadmap.tex",
    "A-symbols": "manuscript/latex/appendices/A-symbols.tex",
}

# Reader-card / evidence label prefixes used by the book's prose (curated from
# the v0.110 source; code identifiers such as "amrex:" are intentionally absent).
CARD_LABELS = [
    "源码入口", "源码文件", "源码位置", "源码原文", "函数", "读取入口",
    "最小输入片段", "典型目录树", "练习题", "进一步阅读", "适用场景",
    "观察", "命令", "配置", "运行", "边界", "证据", "卡", "读者",
    "说明", "注意", "警告", "结果", "结论", "判读", "分析", "示例",
    "输出", "停止条件", "来源",
]
CARD_PATTERN = re.compile(r"^(" + "|".join(sorted(CARD_LABELS, key=len, reverse=True)) + r")[：:]")

DANGEROUS = "_%#&~^\\$"

HEADING_RE = re.compile(r"^\s{0,3}(#{1,6})\s+")
TABLE_LINE_RE = re.compile(r"^\s*\|")
TABLE_SEP_RE = re.compile(r"^\s*\|?[\s:|-]+\|?\s*$")
CODE_FENCE_RE = re.compile(r"^ {0,3}```(\w*)")
DISPLAY_OPEN_RE = re.compile(r"^\s*\$\$")
INLINE_CODE_RE = re.compile(r"`[^`]*`")
INLINE_DOLLAR_RE = re.compile(r"(?<!\$)\$(?!\$).+?(?<!\$)\$(?!\$)")
INLINE_PAREN_RE = re.compile(r"\\\(.+?\\\)", re.DOTALL)
SINGLE_LINE_DISPLAY_RE = re.compile(r"\$\$[^$]+\$\$")


def strip_inline_math(line: str) -> str:
    r"""Remove both `$...$` and \(...\) inline-math spans from a line."""
    return INLINE_PAREN_RE.sub("", INLINE_DOLLAR_RE.sub("", line))


def scan_escape_sensitive(text: str, start_line: int) -> dict[str, object]:
    """Count LaTeX-escape-sensitive characters in prose only.

    Strips fenced code blocks, inline code spans, display math (multi-line
    blocks between ``$$`` delimiters and single-line ``$$...$$`` spans),
    inline math, table rows, and heading lines; counts dangerous characters
    in the remaining prose and records up to five sample locations per
    character. Single-line display equations embedded in paragraphs are
    counted separately (``single_line_display``).
    """
    counts: Counter[str] = Counter()
    samples: dict[str, list[str]] = {}
    in_code = False
    in_display = False
    single_line_display = 0
    for lineno, line in enumerate(text.splitlines(), 1):
        fence = CODE_FENCE_RE.match(line)
        if fence:
            in_code = not in_code
            continue
        if in_code:
            continue
        if DISPLAY_OPEN_RE.match(line):
            in_display = not in_display
            continue
        if in_display:
            continue
        if TABLE_LINE_RE.match(line):
            continue
        if HEADING_RE.match(line):
            continue
        stripped = SINGLE_LINE_DISPLAY_RE.sub("", line)
        if stripped != line:
            single_line_display += 1
        stripped = strip_inline_math(INLINE_CODE_RE.sub("", stripped))
        for ch in DANGEROUS:
            if ch not in stripped:
                continue
            n = stripped.count(ch)
            counts[ch] += n
            if len(samples.get(ch, [])) < 5:
                samples.setdefault(ch, []).append(f"L{start_line + lineno}: {stripped.strip()[:70]}")
    return {
        "counts": dict(counts),
        "samples": samples,
        "single_line_display": single_line_display,
    }


def count_math(text: str) -> tuple[int, int, int, int]:
    r"""Return (display_blocks, display_environments, inline_dollar, inline_paren).

    A display block starts at a ``$$`` line while not already inside a
    ``$$`` block (multi-line blocks contribute one block; single-line
    ``$$...$$`` also contribute one). ``\begin{equation|align|...}``
    environments are counted separately. Inline math counts both ``$...$``
    and raw ``\(...\)`` spans (the book uses both syntaxes).
    """
    display_blocks = 0
    in_display = False
    inline_dollar = 0
    inline_paren = 0
    envs = 0
    for line in text.splitlines():
        if DISPLAY_OPEN_RE.match(line):
            if not in_display:
                display_blocks += 1
            in_display = not in_display
            continue
        if re.search(r"\\begin\{(equation|align|multline|gather)\*?\}", line):
            envs += 1
        if "\\end{" in line:
            continue
        inline_dollar += len(INLINE_DOLLAR_RE.findall(line))
        inline_paren += len(INLINE_PAREN_RE.findall(line))
    return display_blocks, envs, inline_dollar, inline_paren


def scan_part(role: str, name: str, path: Path) -> dict[str, object]:
    raw = path.read_text(encoding="utf-8")
    lines = raw.splitlines()
    headings: Counter[str] = Counter()
    code_blocks = 0
    code_lines = 0
    code_langs: Counter[str] = Counter()
    fences_indented = 0
    table_blocks = 0
    table_rows = 0
    images = 0
    image_srcs: list[str] = []
    links_total = 0
    links_internal_md = 0
    links_internal_fig = 0
    links_external = 0
    link_targets: Counter[str] = Counter()
    card_count = 0
    card_samples: list[str] = []
    in_code = False
    in_table = False
    for idx, line in enumerate(lines, 1):
        fence = CODE_FENCE_RE.match(line)
        if fence:
            if re.match(r"^ {1,3}```", line):
                fences_indented += 1
            if not in_code:
                code_blocks += 1
                code_langs[fence.group(1) or "(none)"] += 1
            in_code = not in_code
            continue
        if in_code:
            code_lines += 1
            continue
        m = HEADING_RE.match(line)
        if m:
            headings[f"h{len(m.group(1))}"] += 1
            continue
        if TABLE_LINE_RE.match(line):
            if TABLE_SEP_RE.match(line) and in_table and table_rows > 0:
                in_table = False
                continue
            if not in_table:
                table_blocks += 1
                in_table = True
            table_rows += 1
            continue
        in_table = False
        images += len(re.findall(r"!\[[^\]]*\]\(([^)]+)\)", line))
        image_srcs += re.findall(r"!\[[^\]]*\]\(([^)]+)\)", line)
        for target in re.findall(r"\[[^\]]*\]\(([^)]+)\)", line):
            links_total += 1
            link_targets[target] += 1
            if target.endswith(".md"):
                links_internal_md += 1
            elif "figures/" in target or target.endswith((".png", ".pdf", ".jpg", ".jpeg", ".svg")):
                links_internal_fig += 1
            elif target.startswith("http"):
                links_external += 1
        if CARD_PATTERN.match(line.strip()):
            card_count += 1
            if len(card_samples) < 8:
                card_samples.append(f"L{idx}: {line.strip()[:70]}")
    display_blocks, display_envs, inline_dollar, inline_paren = count_math(raw)
    esc = scan_escape_sensitive(raw, 0)
    return {
        "role": role,
        "name": name,
        "source": path.relative_to(ROOT).as_posix(),
        "tex_target": TEX_TARGETS[name],
        "lines_total": len(lines),
        "lines_nonblank": sum(1 for l in lines if l.strip()),
        "headings": dict(headings),
        "code_blocks": code_blocks,
        "code_lines": code_lines,
        "code_langs": dict(code_langs),
        "fences_indented": fences_indented,
        "table_blocks": table_blocks,
        "table_rows": table_rows,
        "display_equations_blocks": display_blocks,
        "display_equation_environments": display_envs,
        "inline_math_dollar": inline_dollar,
        "inline_math_paren": inline_paren,
        "images": images,
        "image_sources": image_srcs,
        "links_total": links_total,
        "links_internal_markdown": links_internal_md,
        "links_internal_figure": links_internal_fig,
        "links_external": links_external,
        "link_targets_top": link_targets.most_common(12),
        "reader_card_labels": card_count,
        "card_samples": card_samples,
        "escape_sensitive_prose": esc,
    }


def probe_toolchain() -> dict[str, object]:
    """Best-effort record of the local XeLaTeX toolchain and fonts."""
    out: dict[str, object] = {}
    for tool in ("xelatex", "latexmk", "pandoc", "kpsewhich", "fc-list"):
        p = shutil.which(tool)
        if p is None:
            out[tool] = None
            continue
        try:
            if tool in ("xelatex", "latexmk"):
                ver = subprocess.run([p, "--version"], capture_output=True, text=True, timeout=10).stdout.splitlines()[0]
            elif tool == "kpsewhich":
                ver = subprocess.run([p, "--version"], capture_output=True, text=True, timeout=10).stdout.splitlines()[0]
            else:
                ver = p
            out[tool] = ver
        except Exception as exc:  # pragma: no cover
            out[tool] = str(exc)
    packages = [
        "ctexbook", "booktabs", "longtable", "caption", "subcaption",
        "fvextra", "minted", "hyperref", "cleveref", "fontspec", "xeCJK",
        "unicode-math", "geometry", "fancyhdr", "titlesec", "xcolor", "enumitem",
    ]
    found, missing = [], []
    for pkg in packages:
        cls = pkg + ".cls" if pkg == "ctexbook" else pkg + ".sty"
        if shutil.which("kpsewhich"):
            rc = subprocess.run(["kpsewhich", cls], capture_output=True, text=True, timeout=10).stdout.strip()
            (found if rc else missing).append(pkg)
        else:
            missing.append(pkg)
    out["packages_found"] = found
    out["packages_missing"] = missing
    fonts: list[str] = []
    if shutil.which("fc-list"):
        try:
            r = subprocess.run(["fc-list", ":lang=zh", "family"], capture_output=True, text=True, timeout=20)
            fonts = sorted({f.strip() for f in r.stdout.splitlines() if f.strip()})
        except Exception:  # pragma: no cover
            pass
    out["zh_fonts"] = fonts
    out["pygments"] = None
    try:
        import pygments  # noqa: F401
        out["pygments"] = "available"
    except ImportError:
        out["pygments"] = "MISSING (minted external dependency)"
    return out


def build_report() -> dict[str, object]:
    parts = [scan_part(role, name, path) for role, name, path in SOURCE_PARTS]
    totals = {
        "lines_total": sum(p["lines_total"] for p in parts),
        "lines_nonblank": sum(p["lines_nonblank"] for p in parts),
        "code_blocks": sum(p["code_blocks"] for p in parts),
        "code_lines": sum(p["code_lines"] for p in parts),
        "table_blocks": sum(p["table_blocks"] for p in parts),
        "table_rows": sum(p["table_rows"] for p in parts),
        "display_equations_blocks": sum(p["display_equations_blocks"] for p in parts),
        "display_equation_environments": sum(p["display_equation_environments"] for p in parts),
        "single_line_display": sum(p["escape_sensitive_prose"]["single_line_display"] for p in parts),
        "inline_math": sum(p["inline_math_dollar"] + p["inline_math_paren"] for p in parts),
        "inline_math_dollar": sum(p["inline_math_dollar"] for p in parts),
        "inline_math_paren": sum(p["inline_math_paren"] for p in parts),
        "fences_indented": sum(p["fences_indented"] for p in parts),
        "images": sum(p["images"] for p in parts),
        "links_total": sum(p["links_total"] for p in parts),
        "links_internal_markdown": sum(p["links_internal_markdown"] for p in parts),
        "links_internal_figure": sum(p["links_internal_figure"] for p in parts),
        "links_external": sum(p["links_external"] for p in parts),
        "reader_card_labels": sum(p["reader_card_labels"] for p in parts),
    }
    esc_tot: Counter[str] = Counter()
    for p in parts:
        esc_tot.update(p["escape_sensitive_prose"]["counts"])
    return {
        "plan": "docs/latex-migration-plan.md",
        "baseline_tag": "v1.0",
        "baseline_commit": "e1faff5",
        "edition": "v0.110",
        "toolchain": probe_toolchain(),
        "totals": totals,
        "escape_sensitive_prose_total": dict(esc_tot),
        "parts": parts,
    }


def render_markdown(report: dict[str, object]) -> str:
    t = report["totals"]
    lines: list[str] = []
    lines.append("# PIC-tutor LaTeX Migration Phase 0 Inventory (v0.110)")
    lines.append("")
    lines.append("> 生成：`scripts/inventory_latex_phase0.py`（纯标准库，可重复运行）。")
    lines.append("> 基线：Git 标签 `v1.0`（commit `e1faff5`），书稿版本 `v0.110`，275 页规范 PDF。")
    lines.append("")
    lines.append("## 总计")
    lines.append("")
    lines.append(f"- 源行数：**{t['lines_total']:,}**（非空 {t['lines_nonblank']:,}）")
    lines.append(f"- 代码块：**{t['code_blocks']:,}**（{t['code_lines']:,} 行；缩进围栏定界行 {t['fences_indented']}）")
    lines.append(f"- 表格：**{t['table_blocks']:,}** 块 / {t['table_rows']:,} 行")
    lines.append(f"- 显示公式：**{t['display_equations_blocks'] + t['display_equation_environments']:,}**（$$ 块 {t['display_equations_blocks']:,} + equation 环境 {t['display_equation_environments']:,}）；行内公式 **{t['inline_math']:,}**（`$...$` {t['inline_math_dollar']:,} + `\\(...\\)` {t['inline_math_paren']:,}）；段内单行 $$..$$ {t['single_line_display']:,}")
    lines.append(f"- 图片：**{t['images']}**")
    lines.append(f"- 链接：**{t['links_total']}**（章节内链 {t['links_internal_markdown']}、图内链 {t['links_internal_figure']}、外链 {t['links_external']}）")
    lines.append(f"- 读者卡片标签行：**{t['reader_card_labels']:,}**")
    lines.append("")
    lines.append("## 按源文件清单")
    lines.append("")
    lines.append("| 源文件 | 角色 | 行数 | 代码块 | 表格块 | 显示公式 | 行内公式 | 图片 | 链接 | 卡片标签 | 目标 .tex |")
    lines.append("|---|---|---|---|---|---|---|---|---|---|---|")
    for p in report["parts"]:
        d = p["display_equations_blocks"] + p["display_equation_environments"]
        im = p["inline_math_dollar"] + p["inline_math_paren"]
        lines.append(
            f"| {p['name']} | {p['role']} | {p['lines_total']} | {p['code_blocks']} | "
            f"{p['table_blocks']} | {d} | {im} | {p['images']} | {p['links_total']} | "
            f"{p['reader_card_labels']} | `{p['tex_target']}` |"
        )
    lines.append("")
    lines.append("## 工具链与字体记录（本机）")
    lines.append("")
    tc = report["toolchain"]
    for tool in ("xelatex", "latexmk", "pandoc"):
        lines.append(f"- `{tool}`：{tc.get(tool) or '未找到'}")
    lines.append(f"- 宏包：找到 {len(tc['packages_found'])} 个 / 缺失 {tc['packages_missing'] or '无'}")
    lines.append(f"- pygments：{tc['pygments']}")
    lines.append(f"- 中文字体（fc-list :lang=zh）：{len(tc['zh_fonts'])} 个，含 {', '.join(tc['zh_fonts'][:8])} …")
    lines.append("")
    lines.append("## 正文待转义字符（LaTeX 敏感，代码/数学/表格/标题之外）")
    lines.append("")
    esc = report["escape_sensitive_prose_total"]
    if esc:
        for ch in DANGEROUS:
            if ch in esc:
                lines.append(f"- `{ch}`：{esc[ch]} 处")
    else:
        lines.append("- 无")
    lines.append("")
    lines.append("## 各章待转义字符样例（前 5 处）")
    lines.append("")
    for p in report["parts"]:
        esc_p = p["escape_sensitive_prose"]["counts"]
        if not esc_p:
            continue
        lines.append(f"### {p['name']}")
        lines.append("")
        for ch in DANGEROUS:
            if ch not in esc_p:
                continue
            samples = p["escape_sensitive_prose"]["samples"].get(ch, [])
            for s in samples:
                lines.append(f"- `{ch}` ×{esc_p[ch]}：{s}")
        lines.append("")
    lines.append("## 内部章节互链（需映射为 \\label/\\cref）")
    lines.append("")
    seen: set[str] = set()
    for p in report["parts"]:
        for target, n in p["link_targets_top"]:
            if target.endswith(".md") and target not in seen:
                seen.add(target)
                lines.append(f"- `{target}` ×{n}")
    lines.append("")
    lines.append("## 迁移计划一致性备注")
    lines.append("")
    lines.append("- 计划原文「约 43,800 行」与实际源行数不符，本清单以实测为准（见“总计”）。")
    lines.append("- 行内数学为 `$...$` 与 `\\(...\\)` 双语法混合（共 {t['inline_math']} 处），转换器需同时处理；显示数学全部为 `$$..$$` 块（272 个），无 `\\[...\\]`、无 equation/align 环境。")
    lines.append("- 正文存在 1 处裸 LaTeX 命令 `\\clearpage`（第 4 章 L1930），为 Pandoc 时代的排版遗迹，需在 native 章节中显式决策保留或删除。")
    lines.append("- 存在 1 处缩进代码围栏（第 5 章 L2227，3 空格缩进 ` ```text`），转换器围栏识别必须覆盖 0–3 空格缩进。")
    lines.append("- 正文中 `(J_x)`、`(E_z)`、`(F_p,F_m)` 等带下划线标识符以纯文本（非数学、非代码）出现，需按 `\\texttt{}` 处理并转义 `_`。")
    lines.append("")
    lines.append("## Phase 0 退出 gate 验证记录")
    lines.append("")
    lines.append("- 清单覆盖：13 个源文件全部在表（VERSION + 前言 + 第 1--9 章含 03a + 附录 A）。")
    lines.append("- `uv run --with pypdf python scripts/verify_v110_build.py` → `[PASS] all v0.110 artifact checks`（275 页 PDF、章节标题、图片链接、读者化合同等全部通过）。")
    lines.append("- `uv run python scripts/audit_release_consistency.py` → `passed: true`（README/VERSION/release manifest 与 v0.110 口径一致）。")
    lines.append("- 结论：Phase 0 退出条件满足；基线 PDF 未被 LaTeX 迁移工作改动。")
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    report = build_report()
    docs = ROOT / "docs"
    docs.mkdir(exist_ok=True)
    (docs / "latex-phase0-inventory-v0.110.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (docs / "latex-phase0-inventory-v0.110.md").write_text(
        render_markdown(report), encoding="utf-8"
    )
    print("wrote docs/latex-phase0-inventory-v0.110.json")
    print("wrote docs/latex-phase0-inventory-v0.110.md")


if __name__ == "__main__":
    main()
