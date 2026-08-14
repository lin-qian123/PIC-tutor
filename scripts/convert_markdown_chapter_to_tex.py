#!/usr/bin/env python
r"""Markdown chapter -> native LaTeX draft converter for the PIC-tutor book.

Produces a *reviewable draft* only; per docs/latex-migration-plan.md a
converted chapter must be manually normalized and visually reviewed before
its source ownership changes. The converter is intentionally conservative:
it maps the constructs actually present in the v0.110 source (see
docs/latex-phase0-inventory-v0.110.md) and leaves anything unusual in a
``% TODO(review)`` comment instead of guessing.

Handled:
  - headings (chapter/section/subsection/subsubsection, label on chapters)
  - display math (``$$`` blocks) -> unnumbered ``\[ ... \]``
  - inline math: both ``$...$`` and ``\(...\)`` -> ``$...$``
  - inline code `` `...` `` -> ``\\code{...}``
  - bold ``**...**`` -> ``\\textbf{...}``
  - fenced code blocks (cpp/text -> codeblock, bash -> consoleblock)
  - pipe tables -> longtable (booktabs rules, repeated header)
  - ordered/unordered lists with one nesting level
  - images -> figure + includegraphics (graphicspath points at assets/figures)
  - intra-book links ``[..](XX-....md)`` -> ``\\chref{chap:XX-....}{..}``
  - external links -> ``\\url{..}``
  - reader-card label lines (源码入口/源码文件/函数/源码位置/...) -> ``\\sourceline``
  - standalone bold lines -> ``\\cardlabel`` / ``\\cardstep``
  - ``%`` in prose escaped as ``\\%``

Usage:
  python scripts/convert_markdown_chapter_to_tex.py <in.md> <out.tex>
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

HEADING_RE = re.compile(r"^\s{0,3}(#{1,4})\s+(.*)$")
FENCE_RE = re.compile(r"^ {0,3}```(\w*)")
TABLE_RE = re.compile(r"^\s*\|")
CODE_SPAN_RE = re.compile(r"`([^`]*)`")
SINGLE_LINE_DISPLAY_RE = re.compile(r"\$\$[^$]+\$\$")
MATH_PAREN_RE = re.compile(r"\\\((.+?)\\\)", re.DOTALL)
MATH_DOLLAR_RE = re.compile(r"(?<!\$)\$(?!\$)(.+?)(?<!\$)\$(?!\$)")
BOLD_RE = re.compile(r"\*\*(.+?)\*\*")
EMPH_RE = re.compile(r"(?<!\*)\*(?!\*)([^*\n]+?)(?<!\*)\*(?!\*)")
IMAGE_RE = re.compile(r"^!\[([^\]]*)\]\(([^)]+)\)\s*$")
LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
CARD_LABELS = ["源码入口", "源码文件", "源码位置", "源码原文", "读取入口",
               "函数", "最小输入片段", "典型目录树", "适用场景", "练习题"]
CARD_RE = re.compile(r"^(" + "|".join(sorted(CARD_LABELS, key=len, reverse=True)) + r")[：:](.*)$")
ESCAPE_RE = re.compile(r"(?<!\\)([%_#])")

CHAPTER_LABEL = re.compile(r"^(\d+|[0-9]+[a-z])-")


def inline(text: str) -> str:
    """Convert inline markup in a prose fragment.

    Code spans and math spans are stashed first so that escaping and bold
    processing never touch their contents (e.g. ``_`` inside math or code
    must stay literal); plain prose is escaped afterwards.
    """
    tokens: list[str] = []

    def stash(m: re.Match[str]) -> str:
        tokens.append(m.group(0))
        return f"\x00{len(tokens) - 1}\x00"

    t = CODE_SPAN_RE.sub(stash, text)
    t = SINGLE_LINE_DISPLAY_RE.sub(stash, t)   # $$...$$ on one line (e.g. in table cells)
    t = MATH_PAREN_RE.sub(stash, t)
    t = MATH_DOLLAR_RE.sub(stash, t)

    def link(m: re.Match[str]) -> str:
        label, target = m.group(1), m.group(2)
        if target.endswith(".md"):
            base = Path(target).stem
            return rf"\chref{{chap:{base}}}{{{label}}}"
        if target.startswith("http"):
            return rf"\url{{{target}}}"
        return label

    t = LINK_RE.sub(link, t)
    t = BOLD_RE.sub(lambda m: r"\textbf{" + m.group(1) + "}", t)
    t = EMPH_RE.sub(lambda m: r"\emph{" + m.group(1) + "}", t)
    # escape dangerous characters in plain prose (placeholders are \x00 digits)
    t = ESCAPE_RE.sub(r"\\\1", t)

    def restore(m: re.Match[str]) -> str:
        tok = tokens[int(m.group(1))]
        if tok.startswith("`"):
            inner = tok[1:-1]
            # 1) space-free ASCII of URL-safe chars -> \cpath (underscores
            #    pre-escaped; seqsplit in the macro breaks long identifiers)
            if re.fullmatch(r"[A-Za-z0-9_./:()\[\]+=*\-<>]+", inner):
                return r"\cpath{" + inner.replace("_", r"\_") + "}"
            # 2) token with TeX-special chars that would break a braced
            #    argument scan (% # & ~ ^ \ { }) -> pre-escaped \codeesc
            if re.search(r"[%#&~^\\{}$]", inner):
                esc = (inner.replace("\\", r"\textbackslash{}")
                            .replace("{", r"\{").replace("}", r"\}")
                            .replace("%", r"\%").replace("#", r"\#")
                            .replace("&", r"\&").replace("_", r"\_")
                            .replace("~", r"\textasciitilde{}")
                            .replace("^", r"\textasciicircum{}")
                            .replace("$", r"\$"))
                return r"\codeesc{" + esc + "}"
            # 3) otherwise (spaces / CJK, no specials) -> literal \code
            return r"\code{" + inner + "}"
        if tok.startswith("$$"):
            return "$" + tok[2:-2] + "$"   # single-line $$..$$ -> inline math
        if tok.startswith("\\("):
            return "$" + tok[2:-2] + "$"
        return "$" + tok[1:-1] + "$"

    return re.sub(r"\x00(\d+)\x00", restore, t)


HEADING_NUM_RE = re.compile(r"^\d+(?:\.\d+)*[a-z]?[.\s]\s*")

MATH_TO_UNICODE = {
    "omega": "ω", "lambda": "λ", "Delta": "Δ", "rho": "ρ", "gamma": "γ",
    "sigma": "σ", "tau": "τ", "mu": "μ", "epsilon": "ε", "phi": "φ",
    "nabla": "∇", "cdot": "·", "times": "×", "qquad": " ", "quad": " ",
    "left": "", "right": "", "mathbf": "", "mathrm": "", "text": "",
    "boldsymbol": "", "bm": "",
}


def math_to_text(math: str) -> str:
    """Best-effort plain-text rendering of a math span for PDF bookmarks."""
    s = math
    for cmd, sym in MATH_TO_UNICODE.items():
        s = s.replace("\\" + cmd, sym)
    s = re.sub(r"\\[a-zA-Z]+", "", s)     # remaining commands
    s = s.replace("{", "").replace("}", "")
    s = s.replace("\\", "")
    s = re.sub(r"\s+", " ", s).strip()
    return s


def heading_tex(body: str) -> str:
    r"""Wrap inline math and code in heading text with bookmark-safe fallbacks.

    ``\url``-based ``\cpath`` is illegal in moving arguments (ToC / PDF
    bookmarks), so code spans in headings are rendered as plain escaped
    ``\texttt{...}``; math spans get a ``\texorpdfstring`` fallback.
    """

    def wrap_math(m: re.Match[str]) -> str:
        math = m.group(1)
        return r"\texorpdfstring{$" + math + r"$}{" + math_to_text(math) + "}"

    def wrap_code(m: re.Match[str]) -> str:
        cmd, inner = m.group(1), m.group(2)
        if cmd in ("cpath", "codeesc"):
            return r"\texttt{" + inner + "}"  # already pre-escaped by restore()
        esc = (inner.replace("\\", r"\textbackslash{}")
                    .replace("_", r"\_")
                    .replace("%", r"\%")
                    .replace("#", r"\#")
                    .replace("&", r"\&"))
        return r"\texttt{" + esc + "}"

    body = MATH_DOLLAR_RE.sub(wrap_math, body)
    body = re.sub(r"\\(cpath|code|codeesc)\{([^}]*)\}", wrap_code, body)
    return body


def heading(level: int, text: str, name: str) -> list[str]:
    # LaTeX auto-numbers headings; strip the manual "1.1 " / "2.3.1 " prefixes
    # and the "附录 A：" chapter prefix (ctexbook adds its own 附录 numbering).
    text = HEADING_NUM_RE.sub("", text)
    text = re.sub(r"^附录\s*[A-Za-z]?[：:]\s*", "", text)
    body = heading_tex(inline(text))
    if level == 1:
        if name.startswith("00-"):
            return [r"\chapter*{" + body + "}",
                    r"\addcontentsline{toc}{chapter}{" + body + "}"]
        label = f"chap:{name}"
        return [r"\chapter{" + body + "}", rf"\label{{{label}}}"]
    if level == 2:
        return [r"\section{" + body + "}"]
    if level == 3:
        return [r"\subsection{" + body + "}"]
    return [r"\subsubsection{" + body + "}"]


def card_line(line: str) -> list[str] | None:
    m = CARD_RE.match(line.strip())
    if not m:
        return None
    return [rf"\sourceline{{{m.group(1)}}}{{{inline(m.group(2))}}}"]


def split_table_row(line: str) -> list[str]:
    r"""Split a pipe-table row on ``|`` outside inline code/math spans.

    Cells may contain literal ``|`` inside ``$...$``/``$$...$$``/``\\(...\\)``
    math or backtick code (e.g. ``末态 $\max|x|$``); those must not split.
    """
    cells: list[str] = []
    cur: list[str] = []
    i, n = 0, len(line)
    while i < n:
        ch = line[i]
        if ch == "`":
            j = line.find("`", i + 1)
            j = n - 1 if j == -1 else j
            cur.append(line[i:j + 1])
            i = j + 1
            continue
        if ch == "$":
            if line[i:i + 2] == "$$":
                j = line.find("$$", i + 2)
                j = n if j == -1 else j
                cur.append(line[i:j + 2])
                i = j + 2
            else:
                j = line.find("$", i + 1)
                j = n - 1 if j == -1 else j
                cur.append(line[i:j + 1])
                i = j + 1
            continue
        if ch == "\\" and i + 1 < n and line[i + 1] == "(":
            j = line.find("\\)", i + 2)
            j = n if j == -1 else j
            cur.append(line[i:j + 2])
            i = j + 2
            continue
        if ch == "|":
            cells.append("".join(cur))
            cur = []
            i += 1
            continue
        cur.append(ch)
        i += 1
    cells.append("".join(cur))
    return cells


def table_block(lines: list[str], name: str, lineno: int) -> list[str]:
    cells = []
    for raw in lines:
        parts = split_table_row(raw.strip())
        # drop leading/trailing empty cell from pipe-wrapped rows
        if parts and parts[0].strip() == "":
            parts = parts[1:]
        if parts and parts[-1].strip() == "":
            parts = parts[:-1]
        cells.append([inline(p.strip()) for p in parts])
    header = cells[0]
    sep = cells[1] if len(cells) > 1 and all(re.fullmatch(r":?-{2,}:?", c) for c in cells[1]) else None
    body = cells[2:] if sep else cells[1:]
    ncol = len(header)
    align = []
    if sep:
        for i, c in enumerate(sep):
            if i >= ncol:
                break
            align.append("c" if c.startswith(":") and c.endswith(":") else "r" if c.endswith(":") else "l")
    else:
        align = ["l"] * ncol
    colspec = "".join(align[:ncol])
    # Use tabularx with paragraph X columns so CJK cells wrap and long tables
    # keep paginating (ltablex). Column alignment from the separator is kept
    # only for non-`l` cells; l maps to the ragged-right L column.
    cols = "".join("c" if a == "c" else "r" if a == "r" else "L" for a in colspec)
    out = [f"% <-- table block (source: {name} L{lineno})",
           r"\begin{tabularx}{\textwidth}{" + cols + "}",
           r"\toprule"]
    out += [r" & ".join(header) + r" \\"]
    out += [r"\midrule", r"\endfirsthead", r"\toprule"]
    out += [r" & ".join(header) + r" \\"]
    out += [r"\midrule", r"\endhead"]
    for r_ in body:
        out += [r" & ".join(r_) + r" \\"]
    out += [r"\bottomrule", r"\end{tabularx}"]
    return out


def convert(text: str, name: str) -> list[str]:
    lines = text.splitlines()
    out: list[str] = []
    i = 0
    in_list: list[tuple[str, int]] = []  # (type, depth); len = open environments

    def close_lists(keep: int = 0) -> None:
        while len(in_list) > keep:
            typ, _ = in_list.pop()
            out.append(r"\end{" + ("enumerate" if typ == "o" else "itemize") + "}")

    def open_list(typ: str, depth: int) -> None:
        # Reuse the open list at this depth when type matches (siblings);
        # otherwise close back to depth and start a fresh list.
        if len(in_list) > depth + 1:
            close_lists(depth + 1)
        if in_list and len(in_list) == depth + 1 and in_list[-1] == (typ, depth):
            return
        close_lists(depth)
        env = "enumerate" if typ == "o" else "itemize"
        out.append(r"\begin{" + env + "}")
        in_list.append((typ, depth))

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        # fenced code
        fence = FENCE_RE.match(line)
        if fence:
            lang = fence.group(1) or "text"
            body = []
            i += 1
            while i < len(lines) and not FENCE_RE.match(lines[i]):
                body.append(lines[i])
                i += 1
            i += 1  # closing fence
            close_lists()
            env = "consoleblock" if lang == "bash" else "codeblock"
            out.append(f"% <-- fenced code ({lang})")
            out.append(r"\begin{" + env + "}")
            out.extend(body)
            out.append(r"\end{" + env + "}")
            continue

        # display math
        if re.match(r"^\s*\$\$", line):
            body = []
            i += 1
            while i < len(lines) and not re.match(r"^\s*\$\$", lines[i]):
                body.append(lines[i])
                i += 1
            i += 1  # closing $$
            close_lists()
            out.append(r"\[")
            out.extend(body)
            out.append(r"\]")
            continue

        # blank line
        if not stripped:
            close_lists()
            out.append("")
            i += 1
            continue

        # heading
        h = HEADING_RE.match(line)
        if h:
            close_lists()
            out.extend(heading(len(h.group(1)), h.group(2), name))
            i += 1
            continue

        # table (collect consecutive pipe lines)
        if TABLE_RE.match(line):
            block = []
            while i < len(lines) and TABLE_RE.match(lines[i]):
                block.append(lines[i])
                i += 1
            close_lists()
            out.extend(table_block(block, name, i - len(block) + 1))
            continue

        # image
        img = IMAGE_RE.match(stripped)
        if img:
            close_lists()
            alt, src = img.group(1), img.group(2)
            out.append(r"\begin{figure}[htbp]")
            out.append(r"\centering")
            out.append(rf"\includegraphics[width=0.8\linewidth]{{{src}}}")
            if alt:
                out.append(rf"\caption{{{inline(alt)}}}")
            out.append(r"\end{figure}")
            i += 1
            continue

        # lists
        ul = re.match(r"^(\s*)[-*]\s+(.*)$", line)
        ol = re.match(r"^(\s*)\d+[.)]\s+(.*)$", line)
        if ul or ol:
            m = ul or ol
            depth = len(m.group(1)) // 2
            typ = "o" if ol else "u"
            open_list(typ, depth)
            out.append(r"\item " + inline(m.group(2)))
            i += 1
            continue

        # reader-card source lines
        cl = card_line(line)
        if cl:
            close_lists()
            out.extend(cl)
            i += 1
            continue

        # standalone bold line -> card label/step
        b = BOLD_RE.fullmatch(stripped)
        if b and len(stripped) < 120:
            close_lists()
            out.append(r"\cardstep{" + b.group(1) + "}")
            i += 1
            continue

        # plain paragraph
        close_lists()
        out.append(inline(stripped))
        i += 1

    close_lists()
    return out


def main() -> None:
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(2)
    src = Path(sys.argv[1])
    dst = Path(sys.argv[2])
    text = src.read_text(encoding="utf-8")
    name = src.stem
    if not CHAPTER_LABEL.match(name):
        name = "00-" + name if name == "preface" else name
    body = convert(text, name)
    header = [
        f"% AUTOGENERATED DRAFT from manuscript source: {src.resolve().relative_to(ROOT)}",
        f"% Converter: scripts/convert_markdown_chapter_to_tex.py",
        f"% Review gate: docs/latex-migration-plan.md (Phase 2 per-chapter gate)",
        "",
    ]
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text("\n".join(header + body) + "\n", encoding="utf-8")
    print(f"wrote {dst} ({len(body)} lines)")


if __name__ == "__main__":
    main()
