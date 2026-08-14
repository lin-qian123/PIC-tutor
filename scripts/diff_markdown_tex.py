#!/usr/bin/env python
"""Deterministic MD <-> TeX content-atom diff for the PIC-tutor LaTeX book.

Purpose: produce machine-verifiable evidence of content mismatches between a
Markdown source chapter and its converted native LaTeX chapter, so that human
or agent review works from concrete diffs instead of eyeballing thousands of
lines (anti-hallucination design).

Both documents are tokenized into a flat sequence of content atoms:
  H|<level>|<title text>     heading
  P|<text>                   paragraph / list item / card line text
  M|<math>                   display math ($$..$$  <->  \[..\])
  C|<lang>|<code text>       fenced code block  <->  codeblock/consoleblock
  T|<rows>                   pipe table  <->  tabularx (header deduplicated)
  I|<image path>             image

Normalization maps the *legitimate* converter transforms to the same atom
string (numbering stripped from headings, `\(..\)` -> `$..$`, code spans ->
\code/\cpath/\codeesc contents unescaped, bold markers removed, whitespace
collapsed, math spacing commands removed). Any residual difference between
the atom sequences is a candidate content issue.

Output: docs/latex-review/diff-<name>.json per chapter (aligned hunks +
multiset delta + structural counts), and a printed summary.

Usage: python scripts/diff_markdown_tex.py [chapter-name ...]
"""

from __future__ import annotations

import difflib
import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "latex-review"

PAIRS = [
    ("version-note", "manuscript/VERSION.md", "manuscript/latex/frontmatter/publishing-note.tex"),
    ("00-preface", "manuscript/chapters/00-preface.md", "manuscript/latex/chapters/00-preface.tex"),
    ("01-kinetic-models", "manuscript/chapters/01-kinetic-models.md", "manuscript/latex/chapters/01-kinetic-models.tex"),
    ("02-pic-loop", "manuscript/chapters/02-pic-loop.md", "manuscript/latex/chapters/02-pic-loop.tex"),
    ("03-warpx-evolve", "manuscript/chapters/03-warpx-evolve.md", "manuscript/latex/chapters/03-warpx-evolve.tex"),
    ("03a-warpx-initialization", "manuscript/chapters/03a-warpx-initialization.md", "manuscript/latex/chapters/03a-warpx-initialization.tex"),
    ("04-particle-pushers", "manuscript/chapters/04-particle-pushers.md", "manuscript/latex/chapters/04-particle-pushers.tex"),
    ("05-deposition-shapes", "manuscript/chapters/05-deposition-shapes.md", "manuscript/latex/chapters/05-deposition-shapes.tex"),
    ("06-field-solvers", "manuscript/chapters/06-field-solvers.md", "manuscript/latex/chapters/06-field-solvers.tex"),
    ("07-boundaries-amr", "manuscript/chapters/07-boundaries-amr.md", "manuscript/latex/chapters/07-boundaries-amr.tex"),
    ("08-diagnostics-cases", "manuscript/chapters/08-diagnostics-cases.md", "manuscript/latex/chapters/08-diagnostics-cases.tex"),
    ("09-literature-roadmap", "manuscript/chapters/09-literature-roadmap.md", "manuscript/latex/chapters/09-literature-roadmap.tex"),
    ("A-symbols", "manuscript/appendices/A-symbols.md", "manuscript/latex/appendices/A-symbols.tex"),
]

WS = re.compile(r"\s+")
HEADING_NUM_RE = re.compile(r"^\d+(?:\.\d+)*[a-z]?[.\s]\s*")
APPENDIX_PREFIX_RE = re.compile(r"^附录\s*[A-Za-z]?[：:]\s*")
MATH_SPACING = re.compile(r"\\[,;!]|\\quad+|\\qquad+|\\ ")
CODE_SPAN_RE = re.compile(r"`([^`]*)`")
SINGLE_LINE_DISPLAY_RE = re.compile(r"\$\$[^$]+\$\$")
MATH_PAREN_RE = re.compile(r"\\\((.+?)\\\)", re.DOTALL)
MATH_DOLLAR_RE = re.compile(r"(?<!\\)(?<!\$)\$(?!\$)(.+?)(?<!\\)(?<!\$)\$(?!\$)")
BOLD_RE = re.compile(r"\*\*(.+?)\*\*")
LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
TABLE_SEP_RE = re.compile(r"^\s*\|?[\s:|-]+\|?\s*$")
CARD_RE = re.compile(r"^(源码入口|源码文件|源码位置|源码原文|读取入口|函数|最小输入片段|典型目录树|适用场景|练习题)[：:]\s*(.*)$")


def collapse(s: str) -> str:
    return WS.sub("", s)


def norm_math(s: str) -> str:
    s = re.sub(r"\\\\|\\begin\{aligned\}|\\end\{aligned\}|\\begin\{multline\*\}|\\end\{multline\*\}", "", s)
    return collapse(MATH_SPACING.sub("", s))


def norm_code(s: str) -> str:
    return collapse(s)


def md_inline(text: str) -> str:
    """Normalize inline MD markup to plain text (code -> content, math -> M)."""
    tokens: list[str] = []

    def stash(m: re.Match[str]) -> str:
        tokens.append(m.group(1))
        return f"\x01{len(tokens) - 1}\x01"

    text = CODE_SPAN_RE.sub(stash, text)          # protect code (may contain $)
    text = SINGLE_LINE_DISPLAY_RE.sub(lambda m: "⟦M⟧" + norm_math(m.group(0)[2:-2]) + "⟦M⟧", text)
    text = MATH_PAREN_RE.sub(lambda m: "⟦M⟧" + norm_math(m.group(1)) + "⟦M⟧", text)
    text = MATH_DOLLAR_RE.sub(lambda m: "⟦M⟧" + norm_math(m.group(1)) + "⟦M⟧", text)
    text = LINK_RE.sub(lambda m: m.group(1), text)
    text = BOLD_RE.sub(lambda m: m.group(1), text)
    text = re.sub(r"(?<!\*)\*(?!\*)([^*\n]+?)(?<!\*)\*(?!\*)", r"\1", text)
    text = re.sub(r"\x01(\d+)\x01", lambda m: tokens[int(m.group(1))], text)
    return collapse(text)


TEX_ESCAPES = [
    (r"\%", "%"), (r"\_", "_"), (r"\&", "&"), (r"\#", "#"), (r"\$", "$"),
    (r"\{", "{"), (r"\}", "}"),
    (r"\textasciitilde{}", "~"), (r"\textasciicircum{}", "^"),
    (r"\textbackslash{}", "\\"),
]


def unescape_code(s: str) -> str:
    for a, b in TEX_ESCAPES:
        s = s.replace(a, b)
    return s


def strip_tex_comments(line: str) -> str:
    """Remove % comments; \% is a literal percent (codeesc output)."""
    out = []
    i, n = 0, len(line)
    while i < n:
        if line[i] == "\\":
            out.append(line[i])
            if i + 1 < n:
                out.append(line[i + 1])
            i += 2
            continue
        if line[i] == "%":
            break
        out.append(line[i])
        i += 1
    return "".join(out)


def _extract_group(s: str, start: int) -> tuple[str, int] | None:
    """Return (content, end_index) of the braced group starting at s[start]=='{'."""
    if start >= len(s) or s[start] != "{":
        return None
    depth = 0
    i = start
    while i < len(s):
        if s[i] == "{":
            depth += 1
        elif s[i] == "}":
            depth -= 1
            if depth == 0:
                return s[start + 1:i], i + 1
        i += 1
    return None


def _expand_single(text: str, cmd: str, handler) -> str:
    """Expand \\cmd{group} (single braced argument), brace-aware."""
    out = []
    i, n = 0, len(text)
    pat = "\\" + cmd + "{"
    while i < n:
        j = text.find(pat, i)
        if j < 0:
            out.append(text[i:])
            break
        out.append(text[i:j])
        g = _extract_group(text, j + len(cmd) + 1)
        if g is None:
            out.append(text[j:j + len(pat)])
            i = j + len(pat)
            continue
        content, end = g
        out.append(handler(content))
        i = end
    return "".join(out)


def _expand_double(text: str, cmd: str, handler) -> str:
    """Expand \\cmd{A}{B} (two braced arguments), brace-aware."""
    out = []
    i, n = 0, len(text)
    pat = "\\" + cmd + "{"
    while i < n:
        j = text.find(pat, i)
        if j < 0:
            out.append(text[i:])
            break
        out.append(text[i:j])
        g1 = _extract_group(text, j + len(cmd) + 1)
        if g1 is None:
            out.append(text[j:j + len(pat)])
            i = j + len(pat)
            continue
        a, end1 = g1
        g2 = _extract_group(text, end1) if end1 < n and text[end1] == "{" else None
        if g2 is None:
            out.append(text[j:end1])
            i = end1
            continue
        b, end2 = g2
        out.append(handler(a, b))
        i = end2
    return "".join(out)


def tex_inline(text: str) -> str:
    text = strip_tex_comments(text)
    # 1) protect math first: replace $..$ with indexed placeholders so macro
    #    expansion never touches math content (math may contain \texttt etc.
    #    that must be preserved verbatim on both sides)
    math_tokens: list[str] = []

    def stash_math(m: re.Match[str]) -> str:
        math_tokens.append(norm_math(m.group(1)))
        return f"\x02{len(math_tokens) - 1}\x02"

    text = MATH_DOLLAR_RE.sub(stash_math, text)
    # 2) single-argument macros, innermost first
    text = _expand_single(text, "codeesc", lambda c: unescape_code(c))
    text = _expand_single(text, "cpath", lambda c: unescape_code(c))
    text = _expand_single(text, "code", lambda c: unescape_code(c))
    text = _expand_single(text, "texttt", lambda c: c)
    text = _expand_single(text, "textbf", lambda c: c)
    text = _expand_single(text, "emph", lambda c: c)
    text = _expand_single(text, "url", lambda c: c)
    # 3) two-argument macros
    text = _expand_double(text, "sourceline", lambda a, b: a + "：" + b)
    text = _expand_double(text, "texorpdfstring", lambda a, b: a)
    text = _expand_double(text, "chref", lambda a, b: b)
    # 4) remaining markup
    text = re.sub(r"\\cardstep\{([^}]*)\}", r"\1", text)
    text = re.sub(r"\\cardlabel\{([^}]*)\}", r"\1", text)
    text = re.sub(r"\\allowbreak|\\item\b", "", text)
    text = text.replace("~", "")
    for a, b in TEX_ESCAPES:
        text = text.replace(a, b)
    # 5) restore math placeholders
    text = re.sub(r"\x02(\d+)\x02", lambda m: "⟦M⟧" + math_tokens[int(m.group(1))] + "⟦M⟧", text)
    return collapse(text)


# ---------------- MD tokenizer ----------------

def tokenize_md(text: str) -> list[dict]:
    atoms: list[dict] = []
    lines = text.splitlines()
    i, n = 0, len(lines)
    pending_par: list[str] = []

    def flush_par() -> None:
        if pending_par:
            body = "\n".join(pending_par)
            atoms.append({"kind": "P", "key": "P|" + md_inline(body), "line": max(1, i - len(pending_par))})
            pending_par.clear()

    while i < n:
        line = lines[i]
        stripped = line.strip()
        fence = re.match(r"^ {0,3}```(\w*)", line)
        if fence:
            flush_par()
            lang = fence.group(1) or "text"
            body = []
            i += 1
            while i < n and not re.match(r"^ {0,3}```", lines[i]):
                body.append(lines[i])
                i += 1
            i += 1
            atoms.append({"kind": "C", "key": "C|" + lang + "|" + norm_code("\n".join(body)),
                          "line": max(1, i - len(body) - 1)})
            continue
        if re.match(r"^\s*\$\$", line):
            flush_par()
            body = []
            i += 1
            while i < n and not re.match(r"^\s*\$\$", lines[i]):
                body.append(lines[i])
                i += 1
            i += 1
            atoms.append({"kind": "M", "key": "M|" + norm_math("\n".join(body)), "line": max(1, i - len(body) - 1)})
            continue
        if not stripped:
            flush_par()
            i += 1
            continue
        h = re.match(r"^\s{0,3}(#{1,4})\s+(.*)$", line)
        if h:
            flush_par()
            title = HEADING_NUM_RE.sub("", h.group(2))
            title = APPENDIX_PREFIX_RE.sub("", title)
            atoms.append({"kind": "H", "key": f"H|{len(h.group(1))}|{md_inline(title)}", "line": i + 1})
            i += 1
            continue
        if re.match(r"^\s*\|", line):
            flush_par()
            rows = []
            while i < n and re.match(r"^\s*\|", lines[i]):
                if not TABLE_SEP_RE.match(lines[i]):
                    rows.append(lines[i])
                i += 1
            cells = []
            for r in rows:
                parts = [md_inline(p) for p in split_md_row(r)]
                cells.append("␟".join(parts))
            atoms.append({"kind": "T", "key": "T|" + "␞".join(cells), "line": max(1, i - len(rows))})
            continue
        img = re.match(r"^!\[([^\]]*)\]\(([^)]+)\)\s*$", stripped)
        if img:
            flush_par()
            atoms.append({"kind": "I", "key": "I|" + img.group(2), "line": i + 1})
            i += 1
            continue
        # list item -> its own paragraph atom (converter emits \item ...)
        item = re.match(r"^(\s*)(?:[-*]|\d+[.)])\s+(.*)$", line)
        if item:
            flush_par()
            atoms.append({"kind": "P", "key": "P|" + md_inline(item.group(2)), "line": i + 1})
            i += 1
            continue
        pending_par.append(stripped)
        i += 1
    flush_par()
    return atoms


def split_md_row(line: str) -> list[str]:
    """Reuse converter-aware splitting (math/code pipes are not separators)."""
    import sys as _sys
    _sys.path.insert(0, str(ROOT / "scripts"))
    from convert_markdown_chapter_to_tex import split_table_row  # noqa
    parts = split_table_row(line.strip())
    if parts and parts[0].strip() == "":
        parts = parts[1:]
    if parts and parts[-1].strip() == "":
        parts = parts[:-1]
    return parts


# ---------------- TeX tokenizer ----------------

def tokenize_tex(text: str) -> list[dict]:
    atoms: list[dict] = []
    lines = text.splitlines()
    i, n = 0, len(lines)
    pending_par: list[str] = []

    def flush_par() -> None:
        if pending_par:
            body = "".join(pending_par)
            atoms.append({"kind": "P", "key": "P|" + tex_inline(body), "line": max(1, i - len(pending_par))})
            pending_par.clear()

    while i < n:
        line = lines[i]
        stripped = line.strip()
        if re.match(r"^\\begin\{(codeblock|consoleblock)\}", stripped):
            flush_par()
            lang = "bash" if "console" in stripped else "text"
            # the converter emits "% <-- fenced code (<lang>)" just before
            cm = re.search(r"fenced code \((\w+)\)", lines[i - 1] if i > 0 else "")
            if cm:
                lang = cm.group(1)
            body = []
            i += 1
            while i < n and not re.match(r"^\\end\{(codeblock|consoleblock)\}", lines[i].strip()):
                body.append(lines[i])
                i += 1
            i += 1
            atoms.append({"kind": "C", "key": "C|" + lang + "|" + norm_code("\n".join(body)), "line": max(1, i - len(body) - 1)})
            continue
        if stripped == r"\[":
            flush_par()
            body = []
            i += 1
            while i < n and lines[i].strip() != r"\]":
                body.append(lines[i])
                i += 1
            i += 1
            atoms.append({"kind": "M", "key": "M|" + norm_math("\n".join(body)), "line": max(1, i - len(body) - 1)})
            continue
        if re.match(r"^\\begin\{multline\*?\}", stripped):
            flush_par()
            body = []
            i += 1
            while i < n and not re.match(r"^\\end\{multline\*?\}", lines[i].strip()):
                body.append(lines[i])
                i += 1
            i += 1
            atoms.append({"kind": "M", "key": "M|" + norm_math("\n".join(body)), "line": max(1, i - len(body) - 1)})
            continue
        if re.match(r"^\\begin\{tabularx\}", stripped):
            flush_par()
            rows: list[str] = []
            i += 1
            skip_header = False
            while i < n and not re.match(r"^\\end\{tabularx\}", lines[i].strip()):
                s = lines[i].strip()
                if s == r"\endfirsthead":
                    skip_header = True
                    i += 1
                    continue
                if s == r"\endhead":
                    skip_header = False
                    i += 1
                    continue
                if skip_header or not s or s in (r"\toprule", r"\midrule", r"\bottomrule",
                                                 r"\endlastfoot") or s.startswith(r"\multicolumn"):
                    i += 1
                    continue
                if s.endswith(r"\\"):
                    rows.append(s[:-2])
                i += 1
            i += 1
            cells = []
            for r in rows:
                parts = [tex_inline(p) for p in r.replace(r"\&", "\x03").split("&")]
                parts = [p.replace("\x03", "&") for p in parts]
                cells.append("␟".join(parts))
            atoms.append({"kind": "T", "key": "T|" + "␞".join(cells), "line": max(1, i - len(rows) - 1)})
            continue
        if re.match(r"^\\begin\{figure\}", stripped):
            flush_par()
            i += 1
            while i < n and not re.match(r"^\\end\{figure\}", lines[i].strip()):
                m = re.search(r"\\includegraphics(?:\[[^\]]*\])?\{([^}]*)\}", lines[i])
                if m:
                    atoms.append({"kind": "I", "key": "I|" + m.group(1), "line": i + 1})
                i += 1
            i += 1  # consume \end{figure}
            continue
        # list environment boundaries are structure, not content
        if re.match(r"^\\(begin|end)\{(itemize|enumerate)\}", stripped):
            flush_par()
            i += 1
            continue
        if re.match(r"^\\item\b", stripped):
            flush_par()
            atoms.append({"kind": "P", "key": "P|" + tex_inline(stripped), "line": i + 1})
            i += 1
            continue
        h = re.match(r"^\\(chapter|section|subsection|subsubsection)\*?\{", stripped)
        if h:
            flush_par()
            level = {"chapter": 1, "chapter*": 1, "section": 2, "section*": 2,
                     "subsection": 3, "subsection*": 3, "subsubsection": 4, "subsubsection*": 4}[h.group(1)]
            m = re.match(r"^\\(?:chapter|section|subsection|subsubsection)\*?\{(.*)\}$", stripped)
            atoms.append({"kind": "H", "key": f"H|{level}|{tex_inline(m.group(1))}", "line": i + 1})
            i += 1
            continue
        if stripped.startswith(r"\label{") or stripped.startswith("%") or stripped.startswith(r"\addcontentsline"):
            i += 1
            continue
        if not stripped:
            flush_par()
            i += 1
            continue
        pending_par.append(line)
        i += 1
    flush_par()
    return atoms


# ---------------- diff ----------------

def build_report(name: str, md_path: Path, tex_path: Path) -> dict:
    md_atoms = tokenize_md(md_path.read_text(encoding="utf-8"))
    tex_atoms = tokenize_tex(tex_path.read_text(encoding="utf-8"))
    md_keys = [a["key"] for a in md_atoms]
    tex_keys = [a["key"] for a in tex_atoms]
    sm = difflib.SequenceMatcher(a=md_keys, b=tex_keys, autojunk=False)
    hunks = []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            continue
        hunks.append({
            "tag": tag,
            "md": [{"key": a["key"], "line": a["line"]} for a in md_atoms[i1:i2]],
            "tex": [{"key": a["key"], "line": a["line"]} for a in tex_atoms[j1:j2]],
        })
    md_counts = Counter(a["kind"] for a in md_atoms)
    tex_counts = Counter(a["kind"] for a in tex_atoms)
    # multiset delta: atoms whose MD count exceeds TeX count (potential loss)
    missing = []
    md_counter = Counter(a["key"] for a in md_atoms)
    tex_counter = Counter(a["key"] for a in tex_atoms)
    for key, c in md_counter.items():
        if c > tex_counter.get(key, 0):
            missing.append({"key": key[:200], "md_count": c, "tex_count": tex_counter.get(key, 0)})
    extra = []
    for key, c in tex_counter.items():
        if c > md_counter.get(key, 0):
            extra.append({"key": key[:200], "tex_count": c, "md_count": md_counter.get(key, 0)})
    return {
        "name": name,
        "md": str(md_path),
        "tex": str(tex_path),
        "md_atoms": len(md_atoms),
        "tex_atoms": len(tex_atoms),
        "kind_counts_md": dict(md_counts),
        "kind_counts_tex": dict(tex_counts),
        "hunks": hunks,
        "missing_atoms": missing[:200],
        "extra_atoms": extra[:200],
        "clean": not hunks and not missing,
    }


def main() -> None:
    names = sys.argv[1:] or [p[0] for p in PAIRS]
    OUT.mkdir(parents=True, exist_ok=True)
    summary = []
    for name, md, tex in PAIRS:
        if name not in names:
            continue
        report = build_report(name, ROOT / md, ROOT / tex)
        out = OUT / f"diff-{name}.json"
        out.write_text(json.dumps(report, ensure_ascii=False, indent=1), encoding="utf-8")
        summary.append((name, len(report["hunks"]), len(report["missing_atoms"]), len(report["extra_atoms"])))
        print(f"{name:22s} hunks={len(report['hunks']):3d} missing={len(report['missing_atoms']):3d} extra={len(report['extra_atoms']):3d} atoms MD={report['md_atoms']} TeX={report['tex_atoms']}")
    print("\n输出目录: docs/latex-review/")


if __name__ == "__main__":
    main()
