#!/usr/bin/env python
"""Audit the PIC-tutor native LaTeX book PDF against the Phase 1 exit gate.

Checks (docs/latex-migration-plan.md, Phase 1):
  - PDF exists and has pages
  - no missing-character warnings in the log
  - no undefined references / multiply-defined labels / broken hyperlinks
  - no missing figure files in the log
  - overfull/underfull hbox report (informational; gate on overfull count)
  - extracted text has no U+FFFD replacement characters
  - expected chapter/section anchors present in extracted text
  - empty-page scan (pages with almost no extractable text)

Usage:
  python scripts/audit_latex_book.py --pdf dist/latex/pic-tutor-<edition>-<theme>.pdf
                                     --log build/latex/src/main-<theme>.log
                                     [--max-overfull 40]
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

from pypdf import PdfReader

EXPECTED_ANCHORS = [
    # preface + ch1-2
    "写作说明",
    "动理学模型与 PIC 的基本思想",
    "Vlasov 方程首先是相空间守恒律",
    "PIC 总循环：从 Vlasov-Maxwell 到离散时间推进",
    "leapfrog 时间层",
    "AMR subcycling",
    # ch3 / ch3a / appendix A (Phase 2)
    "主演化路径：生命周期、初始化与",
    "顶层入口",
    "OneStep_nosub",
    "参数示例与最小运行闭环",
    "初始化",
    "源码文件",
    "符号、时间层与源码变量",
    "连续模型符号",
    # ch4-9 (Phase 3)
    "粒子推进器：从 Lorentz 方程到",
    "电荷、电流沉积与形函数",
    "电磁场求解器",
    "边界条件",
    "诊断、验证与案例",
    "文献路线与延伸阅读",
    "FDTD 差分算子",
    "Langmuir wave",
    "关键来源的已知边界",
]


def check(name: str, passed: bool, detail: str = "") -> bool:
    print(f"  [{'PASS' if passed else 'FAIL'}] {name}" + (f" — {detail}" if detail else ""))
    return passed


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--pdf", type=Path, required=True)
    ap.add_argument("--log", type=Path, required=True)
    ap.add_argument("--max-overfull", type=int, default=40)
    args = ap.parse_args()

    results: list[bool] = []
    if not args.pdf.exists():
        raise SystemExit(f"missing pdf: {args.pdf}")

    reader = PdfReader(str(args.pdf))
    pages = len(reader.pages)
    results.append(check("pdf exists", True, str(args.pdf)))
    results.append(check("pages > 0", pages > 0, f"{pages} pages"))

    text_all = "\n".join((p.extract_text() or "") for p in reader.pages)
    results.append(check("no U+FFFD replacement chars", "\ufffd" not in text_all))
    empty = [i for i, p in enumerate(reader.pages, 1) if len((p.extract_text() or "").strip()) < 8]
    results.append(check("no empty pages", not empty, f"empty pages: {empty}" if empty else ""))

    missing_anchors = [a for a in EXPECTED_ANCHORS if a not in text_all]
    results.append(check("expected anchors present", not missing_anchors,
                         f"missing: {missing_anchors}" if missing_anchors else ""))

    log = args.log.read_text(encoding="utf-8", errors="ignore")
    missing_chars = len(re.findall(r"Missing character", log))
    results.append(check("no missing characters", missing_chars == 0, f"{missing_chars} occurrences" if missing_chars else ""))

    undef_refs = len(re.findall(r"Reference `[^']*' on page .* undefined", log))
    results.append(check("no undefined references", undef_refs == 0, f"{undef_refs} undefined refs" if undef_refs else ""))

    multidef = len(re.findall(r"multiply defined", log))
    results.append(check("no multiply-defined labels", multidef == 0, f"{multidef} multiply defined" if multidef else ""))

    nofile = len(re.findall(r"LaTeX Warning: File `[^']*' not found", log))
    results.append(check("no missing files/figures", nofile == 0, f"{nofile} missing files" if nofile else ""))

    overfull = len(re.findall(r"Overfull \\hbox", log))
    underfull = len(re.findall(r"Underfull \\hbox", log))
    results.append(check("overfull hbox within policy", overfull <= args.max_overfull,
                         f"{overfull} overfull / {underfull} underfull (policy ≤ {args.max_overfull})"))

    bad = len(re.findall(r"^! .*", log, re.M))
    # file:line:error style messages (xelatex -file-line-error)
    bad += len(re.findall(r"^[./\w-]+\.\w+:\d+: (Undefined|Missing|Runaway|LaTeX Error|Package \S+ Error)", log, re.M))
    results.append(check("no hard errors in log", bad == 0, f"{bad} error lines" if bad else ""))

    ok = all(results)
    print(f"[{'PASS' if ok else 'FAIL'}] latex book audit")
    raise SystemExit(0 if ok else 1)


if __name__ == "__main__":
    main()
