#!/usr/bin/env python
"""Verify the v0.110 Markdown/HTML/PDF artifact contract after building."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

from pypdf import PdfReader

from audit_public_release_paths import inspect
from build_v110 import PAGE_BREAK_PARTS


ROOT = Path(__file__).resolve().parents[1]
SOURCE_CHAPTERS = sorted((ROOT / "manuscript" / "chapters").glob("*.md"))
MERGED_MARKDOWN = ROOT / "dist" / "pic-tutor-v0.110.md"
HTML = ROOT / "dist" / "pic-tutor-v0.110.html"
PDF = ROOT / "dist" / "pic-tutor-v0.110.pdf"
MANUAL_SPOTCHECK = ROOT / "docs" / "manual-editorial-spotcheck-v0.110.md"
# Reader-facing chapter openings, long-chapter navigation, and the Chapter 3
# cross-chapter state handoff yield 266 pages.
EXPECTED_PDF_PAGES = 266


def image_links(text: str) -> list[str]:
    return re.findall(r"!\[\]\(([^)]+figures/[^)]+)\)", text)


def chapter_subheading_numbers(path: Path, chapter: str) -> list[tuple[int, ...]]:
    pattern = re.compile(rf"^### ({re.escape(chapter)}\.\d+\.\d+)\b", re.MULTILINE)
    return [tuple(int(part) for part in match.split(".")) for match in pattern.findall(path.read_text(encoding="utf-8"))]


def chapter_heading_numbers(path: Path, chapter: str) -> list[int]:
    pattern = re.compile(rf"^## {re.escape(chapter)}\.(\d+)\b", re.MULTILINE)
    return [int(number) for number in pattern.findall(path.read_text(encoding="utf-8"))]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--build-log", type=Path)
    args = parser.parse_args()

    source = "\n".join(path.read_text(encoding="utf-8") for path in SOURCE_CHAPTERS)
    source += "\n" + (ROOT / "manuscript" / "VERSION.md").read_text(encoding="utf-8")
    source += "\n" + (ROOT / "README.md").read_text(encoding="utf-8")
    # Historical evidence was deliberately removed from the reader-facing front
    # matter; keep it in the verification surface without putting it back into
    # the tutorial's opening pages.
    source += "\n" + (ROOT / "docs" / "version-history-v0.110.md").read_text(encoding="utf-8")
    source += "\n" + (ROOT / "docs" / "chapter-04-v0-evidence-ledger.md").read_text(encoding="utf-8")
    source += "\n" + (ROOT / "docs" / "chapter-05-v0-evidence-ledger.md").read_text(encoding="utf-8")
    source += "\n" + (ROOT / "docs" / "chapter-06-v0-evidence-ledger.md").read_text(encoding="utf-8")
    source += "\n" + (ROOT / "docs" / "chapter-07-v0-evidence-ledger.md").read_text(encoding="utf-8")
    merged = MERGED_MARKDOWN.read_text(encoding="utf-8")
    html = HTML.read_text(encoding="utf-8", errors="ignore")
    reader = PdfReader(str(PDF))
    pdf_text = "\n".join(page.extract_text() or "" for page in reader.pages)
    manual_spotcheck = MANUAL_SPOTCHECK.read_text(encoding="utf-8") if MANUAL_SPOTCHECK.exists() else ""
    distribution_risk = (ROOT / "docs/public-distribution-risk-register-v0.110.md").read_text(encoding="utf-8")
    version = (ROOT / "manuscript" / "VERSION.md").read_text(encoding="utf-8")
    preface = (ROOT / "manuscript" / "chapters" / "00-preface.md").read_text(encoding="utf-8")
    front_matter_project_markers = re.findall(
        r"RZ/RSPHERE|repeat-slope|pkuHEDPbranch|scripts/|docs/|runs/|notes/|"
        r"Markdown-first|Quarto|LaTeX book",
        version + "\n" + preface,
    )
    chapter_5_numbers = chapter_subheading_numbers(
        ROOT / "manuscript" / "chapters" / "05-deposition-shapes.md", "5"
    )
    chapter_1_path = ROOT / "manuscript" / "chapters" / "01-kinetic-models.md"
    chapter_1 = chapter_1_path.read_text(encoding="utf-8")
    chapter_1_numbers = chapter_heading_numbers(chapter_1_path, "1")
    toc_text = reader.pages[0].extract_text() or ""
    chapter_6_numbers = chapter_subheading_numbers(
        ROOT / "manuscript" / "chapters" / "06-field-solvers.md", "6"
    )
    chapter_6 = (ROOT / "manuscript" / "chapters" / "06-field-solvers.md").read_text(
        encoding="utf-8"
    )
    chapter_6_stale_location_markers = re.findall(
        r"Source/[A-Za-z0-9_./-]+\.(?:cpp|H):\d+", chapter_6
    )
    chapter_6_opening = chapter_6[: chapter_6.index("## 6.1")]
    chapter_2 = (ROOT / "manuscript" / "chapters" / "02-pic-loop.md").read_text(encoding="utf-8")
    chapter_2_code_spans = re.findall(r"`([^`]*)`", chapter_2)
    chapter_3 = (ROOT / "manuscript" / "chapters" / "03-warpx-evolve.md").read_text(encoding="utf-8")
    reader_entry_project_path_pattern = (
        r"scripts/|notes/|runs/|docs/|references/|contract\\.\\{json,md\\}"
    )
    chapter_1_project_markers = re.findall(reader_entry_project_path_pattern, chapter_1)
    chapter_2_project_markers = re.findall(reader_entry_project_path_pattern, chapter_2)
    chapter_3_project_markers = re.findall(reader_entry_project_path_pattern, chapter_3)
    chapter_2_stale_location_markers = re.findall(
        r"(?:\.\./warpx/)?Source/[A-Za-z0-9_./-]+\.(?:cpp|H):\d+", chapter_2
    )
    chapter_2_workspace_markers = re.findall(r"\.\./warpx/", chapter_2)
    chapter_3_stale_location_markers = re.findall(
        r"(?:\.\./warpx/)?Source/[A-Za-z0-9_./-]+\.(?:cpp|H):\d+", chapter_3
    )
    chapter_3_workspace_markers = re.findall(r"\.\./warpx/", chapter_3)
    chapter_3a = (ROOT / "manuscript" / "chapters" / "03a-warpx-initialization.md").read_text(
        encoding="utf-8"
    )
    chapter_3a_opening = chapter_3a[: chapter_3a.index("## 3A.1")]
    chapter_3a_stale_location_markers = re.findall(
        r"Source/[A-Za-z0-9_./-]+\.(?:cpp|H):\d+", chapter_3a
    )
    chapter_3a_project_markers = re.findall(
        r"scripts/|notes/code-reading|runs/stage-c-validation|docs/|references/|contract\.\{json,md\}|"
        r"本地|本机|当前 checkout|当前分支|项目内|项目级|维护台账|交接记录|"
        r"源码笔记|初始化笔记|笔记编号",
        chapter_3a,
    )
    chapter_4 = (ROOT / "manuscript" / "chapters" / "04-particle-pushers.md").read_text(
        encoding="utf-8"
    )
    chapter_4_stale_location_markers = re.findall(
        r"Source/[A-Za-z0-9_./-]+\.(?:cpp|H):\d+", chapter_4
    )
    chapter_4_opening = chapter_4[: chapter_4.index("## 4.1")]
    chapter_5 = (ROOT / "manuscript" / "chapters" / "05-deposition-shapes.md").read_text(
        encoding="utf-8"
    )
    chapter_5_stale_location_markers = re.findall(
        r"Source/[A-Za-z0-9_./-]+\.(?:cpp|H):\d+", chapter_5
    )
    chapter_5_opening = chapter_5[: chapter_5.index("## 5.1")]
    chapter_5_project_markers = re.findall(
        r"scripts/|notes/|runs/|docs/|references/|contract\.\{json,md\}|"
        r"本机|本地 regression|项目用|项目在|项目独立|本地论文|对应的本地|报告位于|汇总报告",
        chapter_5,
    )
    chapter_7 = (ROOT / "manuscript" / "chapters" / "07-boundaries-amr.md").read_text(
        encoding="utf-8"
    )
    chapter_7_stale_location_markers = re.findall(
        r"(?:Source/[A-Za-z0-9_./-]+\.(?:cpp|H)|Docs/[A-Za-z0-9_./-]+\.rst):\d+",
        chapter_7,
    )
    chapter_8 = (ROOT / "manuscript" / "chapters" / "08-diagnostics-cases.md").read_text(
        encoding="utf-8"
    )
    chapter_8_opening = chapter_8[: chapter_8.index("## Langmuir wave")]
    chapter_8_stale_location_markers = re.findall(
        r"(?:Source/[A-Za-z0-9_./-]+\.(?:cpp|H)|Docs/[A-Za-z0-9_./-]+\.rst):\d+",
        chapter_8,
    )
    chapter_9 = (ROOT / "manuscript" / "chapters" / "09-literature-roadmap.md").read_text(
        encoding="utf-8"
    )
    chapter_3a_numbers = [
        int(number)
        for number in re.findall(
            r"^## 3A\.(\d+)\b",
            chapter_3a,
            re.MULTILINE,
        )
    ]

    checks = {
        "pdf_pages": len(reader.pages) == EXPECTED_PDF_PAGES,
        "source_image_links": len(image_links(source)) == 16,
        "merged_image_links": len(image_links(merged)) == 15,
        "image_links_relative": all(
            not link.startswith("/") for link in image_links(source) + image_links(merged)
        ),
        "html_embedded_images": html.count("data:image/png;base64,") >= 15,
        "figure_markers": all(f"图 8-{index}" in pdf_text for index in range(1, 13)),
        "appendix_marker": "附录 A：符号、时间层与源码变量" in pdf_text,
        "primary_sections_start_on_new_pdf_pages": merged.count("\\clearpage") == len(PAGE_BREAK_PARTS),
        "reader_facing_front_matter": all(
            marker in version + "\n" + preface
            for marker in ("# PIC-tutor", "建议的阅读方式", "如何使用本书", "遇到一个新的输入或源码分支时")
        ) and not front_matter_project_markers,
        "chapter_5_subheading_order": chapter_5_numbers == sorted(chapter_5_numbers)
        and len(chapter_5_numbers) == len(set(chapter_5_numbers)),
        "chapter_6_subheading_order": chapter_6_numbers == sorted(chapter_6_numbers)
        and len(chapter_6_numbers) == len(set(chapter_6_numbers)),
        "chapter_6_reader_closure": all(
            marker in chapter_6
            for marker in (
                "### 6.11.9 从源码入口回查验证量",
                "## 6.12 练习与运行验证",
                "**跨章诊断题**",
                "## 6.13 本章结论",
                "先确定几何和物理目标，再确定 source 时间模型",
            )
        ),
        "chapter_6_current_solver_route": all(
            marker in chapter_6
            for marker in (
                "场求解器把上一章已经同步的电荷与电流变成下一时刻的电磁场",
                "WarpX::OneStep_nosub()",
                "WarpX::PushPSATD()",
                "WarpX::OneStep_JRhom()",
                "读者主线：从同步源项到可检验的场",
                "选择路径前的检查表",
                "## 6.12 练习与运行验证",
            )
        ) and not chapter_6_stale_location_markers and not re.search(
            r"scripts/|notes/code-reading|runs/stage-c-validation|docs/chapter-06-v0-evidence-ledger|"
            r"contract\.\{json,md\}|全文笔记|逐式记录|证据台账",
            chapter_6,
        ),
        "chapter_6_opening_is_reader_facing": not re.search(
            r"notes/code-reading|pkuHEDPbranch|8c488b1a9|本机|本轮|当前源码|源码快照",
            chapter_6_opening,
        ),
        "chapter_2_3_reader_routes": all(
            marker in chapter_2
            for marker in ("## 2.11 本章结论", "先确定连续问题与可分辨尺度", "区分外层时间步和内部重复")
        ) and all(
            marker in chapter_3
            for marker in ("追踪它何时变成网格、场、粒子和诊断", "InitData()", "OneStep()")
        ) and not chapter_2_project_markers and not chapter_3_project_markers
        and not chapter_2_stale_location_markers and not chapter_3_stale_location_markers
        and not chapter_2_workspace_markers and not chapter_3_workspace_markers,
        "chapter_2_3_portable_source_navigation": all(
            marker in chapter_2
            for marker in (
                "`Source/...` 与 `Examples/...` 均相对于 WarpX 源码根目录",
                "`Source/Evolve/WarpXEvolve.cpp` 的 `WarpX::OneStep_nosub()`",
                "`Source/Evolve/WarpXComputeDt.cpp` 的 `WarpX::ComputeDt()`",
            )
        ) and not chapter_2_stale_location_markers and not chapter_3_stale_location_markers
        and not chapter_2_workspace_markers and not chapter_3_workspace_markers,
        "chapter_3_current_source_route": all(
            marker in chapter_3
            for marker in (
                "### 源码定位约定",
                "WarpX::ApplyDtLimiters()",
                "**没有** 显式设置 `algo.maxwell_solver`",
                "`test_1d_langmuir_multi`",
                "`analysis_1d.py diags/diag1000080`",
                "**案例闭环题。**",
            )
        ) and "UpdateDtFromParticleSpeeds" not in chapter_3
        and "`algo.maxwell_solver = yee`" not in chapter_3
        and not chapter_3_stale_location_markers
        and not chapter_3_workspace_markers
        and not chapter_3_project_markers,
        "chapter_3_cross_chapter_handoff": all(
            marker in chapter_3
            for marker in (
                "跨章交接卡：从调用图保留到可验证的状态",
                "输入动量在什么单位下被解释？",
                "显式粒子轨迹怎样变成 solver source？",
                "怎样判断这条路径可信？",
                "输入量纲与配置",
                "有独立 reference 的 observable",
            )
        ) and not chapter_3_stale_location_markers and not chapter_3_workspace_markers,
        "chapter_2_math_and_case_closure": all(
            marker in chapter_2
            for marker in (
                "$\\omega_p\\Delta t$",
                "$\\lambda_D/\\Delta x$",
                "`test_1d_langmuir_multi`",
                "`analysis_1d.py diags/diag1000080`",
                "**案例闭环题**",
            )
        ) and not any(
            re.search(r"\\(?:omega|lambda|Delta)", span) for span in chapter_2_code_spans
        ) and not chapter_2_stale_location_markers and not chapter_2_workspace_markers,
        "chapter_7_reader_closure": all(
            marker in chapter_7
            for marker in (
                "## 本章的阅读路线：边界是一个闭合系统",
                "## 7.11 本章结论",
                "**拓扑是否一致。**",
                "**观察量是否匹配问题。**",
                "rho_buf/current_buf",
            )
        ) and not chapter_7_stale_location_markers,
        "chapter_7_current_boundary_route": all(
            marker in chapter_7
            for marker in (
                "本章按一条读者可追踪的链展开",
                "WarpX::MakeWarpX()",
                "每一节都应能回到一个可观察量",
                "## 7.10 本章练习与源码定位",
            )
        )
        and not chapter_7_stale_location_markers
        and not re.search(
            r"scripts/|notes/code-reading|runs/stage-c-validation|"
            r"docs/chapter-07-v0-evidence-ledger|contract\.\{json,md\}",
            chapter_7,
        ),
        "chapter_8_current_diagnostics_route": all(
            marker in chapter_8
            for marker in (
                "本章不按文件格式罗列功能",
                "先定义想测的物理量",
                "WarpX::Evolve",
                "MultiDiagnostics",
                "ReducedDiags",
                "## 8.15 练习与复现实验",
            )
        )
        and not chapter_8_stale_location_markers
        and not re.search(
            r"scripts/|notes/code-reading|runs/stage-c-validation|"
            r"docs/chapter-08-v0-evidence-ledger|contract\.\{json,md\}|"
            r"本地|本机|当前 checkout|当前分支|项目内|项目级|维护台账|交接记录|源码笔记",
            chapter_8,
        ),
        "chapter_9_current_literature_route": all(
            marker in chapter_9
            for marker in (
                "文献是论证工具，不是书目清单",
                "一张文献判读卡",
                "## 9.7 两条深读路线",
                "## 9.8 如何阅读证据边界",
                "第 8 章的验证矩阵",
                "## 9.10 练习与复核",
            )
        )
        and not re.search(
            r"docs/|references/|notes/|runs/|scripts/|public-evidence-index|literature-map|"
            r"仓库|核心目录|文献地图|缺口登记|公开再分发|OPEN_EXTERNAL_ACCESS|"
            r"PRE_PHYSICS_BOUNDARY|RUNTIME_LEDGER_UNPROVEN|"
            r"CONVERGENCE_READINESS_WITH_FORMAL_ORDER_UNPROVEN",
            chapter_9,
        ),
        "chapter_3a_section_order": chapter_3a_numbers == list(range(1, 17)),
        "chapter_3a_current_initialization_route": all(
            marker in chapter_3a
            for marker in (
                "WarpX::MakeNewLevelFromScratch()",
                "m_implicit_solver->Define",
                'ExecutePythonCallback("allocdata")',
                "WarpX::LoadExternalFields(int lev)",
                "External fields from file are not compatible with the moving window.",
                "ProjectionDivCleaner::setSourceFromField()",
                "输入创建了什么初态？比较的 observable 是什么？",
            )
        ) and not chapter_3a_stale_location_markers and not chapter_3a_project_markers,
        "chapter_3a_8_long_chapter_reader_navigation": all(
            marker in chapter_3a_opening
            for marker in (
                "阅读路线：先构造初态，再追踪分支",
                "先读 3A.1--3A.3",
                "再读 3A.4--3A.5",
                "按输入类型读 3A.6--3A.12",
                "最后读 3A.13--3A.16",
            )
        ) and all(
            marker in chapter_8_opening
            for marker in (
                "阅读路线：从物理问题走到证据等级",
                "先读开头、Langmuir wave 与 Uniform plasma",
                "再按物理问题选案例族",
                "随后读“诊断在源码中的位置”到案例模板",
                "最后读 8.14--8.17",
            )
        ),
        "chapter_4_current_pusher_route": all(
            marker in chapter_4
            for marker in (
                "本章按一条读者可追踪的因果链展开",
                "GetExplicitPusherDisplacement()",
                "doParticleMomentumPush()",
                "getExternalEB(ip, Exp, Eyp, Ezp, Bxp, Byp, Bzp);",
                "FirstHalf/SecondHalf",
                "UpdateMomentumHigueraCary()",
                "## 4.16 练习与复现实验",
            )
        ) and not chapter_4_stale_location_markers and not re.search(
            r"本地 checkout|原文精读",
            chapter_4,
        ),
        "chapter_4_5_long_chapter_reader_navigation": all(
            marker in chapter_4_opening
            for marker in (
                "阅读路线：先定位一条带电粒子的时间链",
                "先读 4.1--4.4",
                "再读 4.5--4.10",
                "按需要进入 4.11--4.14",
                "最后用 4.15--4.16 收束",
            )
        ) and all(
            marker in chapter_5_opening
            for marker in (
                "阅读路线：先把守恒问题变成四个可回答的问题",
                "阅读 5.1--5.3",
                "阅读 5.4--5.8",
                "阅读 5.9--5.13",
                "阅读 5.14--5.16",
            )
        ),
        "chapter_4_has_no_project_path_narration": not re.search(
            r"scripts/|notes/code-reading|runs/stage-c-validation|contract\.\{json,md\}|"
            r"本地 checkout|原文精读",
            chapter_4,
        ),
        "chapter_5_current_deposition_route": all(
            marker in chapter_5
            for marker in (
                "本章按一条从粒子状态到求解器源项的因果链展开",
                "Compute_shape_factor",
                "Compute_shifted_shape_factor",
                "WarpXParticleContainer::DepositCurrent()",
                "WarpX::SyncCurrentAndRho()",
                "tile-loop 阶段",
                "## 5.16 练习与源码定位",
            )
        ) and not chapter_5_stale_location_markers and not chapter_5_project_markers,
        "chapter_5_opening_is_reader_facing": not re.search(
            r"notes/code-reading|pkuHEDPbranch|8c488b1a9|本机|本轮|当前源码",
            chapter_5_opening,
        ),
        "chapter_1_section_order": chapter_1_numbers == list(range(1, 15)),
        "chapter_1_pdf_toc_entries": all(
            marker in toc_text
            for marker in (
                "1.11 从连续模型到 PIC 离散变量",
                "1.12 这一章对后面源码章节的真正约束",
                "1.13 证据范围与继续阅读",
                "1.14 练习与源码定位",
            )
        ),
        "chapter_1_source_exercise": all(
            marker in chapter_1
            for marker in (
                "## 1.14 练习与源码定位",
                "`Source/Evolve/WarpXEvolve.cpp`",
                "`OneStep_nosub()`",
                "`SyncCurrentAndRho()`",
                "`PushPSATD()`",
            )
        ) and not chapter_1_project_markers,
        "chapter_9_exercises": all(
            marker in source
            for marker in (
                "## 9.10 练习与复核",
                "### 9.10.1 证据层分类练习",
                "### 9.10.2 证据边界复核练习",
                "### 9.10.3 延伸阅读排序练习",
            )
        ),
        "chapter_9_reading_priority_order": all(
            marker in source
            for marker in (
                "1. `Esirkepov 2001` 的 CPC 定稿 PDF",
                "2. `Yee 1966`",
                "3. `LeeCPC2015` 正文 PDF",
                "4. `Hockney-Eastwood` 或其 article-level fallback",
                "5. `Boris` 原始文献",
            )
        ),
        "chapter_9_literature_gap_count": (
            "这六条中，`LeeCPC2015` 的边界最容易被误读" in source
        ),
        "public_distribution_boundary_registered": (
            "PUBLIC_REPOSITORY_THIRD_PARTY_ASSETS_TRACKED_REMEDIATION_REQUIRED" in distribution_risk
            and (ROOT / "scripts/audit_public_distribution_boundary.py").is_file()
        ),
        "vay_2014_review_closure": all(
            marker in source
            for marker in (
                "### 4.4.2 v0.74 文献闭环：Vay--Godfrey 2014 review",
                "### 6.6.7 v0.74 文献闭环：Vay--Godfrey 2014 review",
                "9 页 PDF、MinerU 原文、43 张抽取图",
                "`psatd.current_correction` 是离散连续性/Gauss-law projection",
            )
        ),
        "chapter_5_algorithm_selection_matrix": all(
            marker in source
            for marker in (
                "### 5.14.3 v0.75 沉积算法选择矩阵",
                "geometry/grid 约束",
                "explicit/implicit 时间层",
                "Direct",
                "Esirkepov",
                "Villasenor",
                "Vay",
                "SOURCE_AND_RUNTIME_SELECTION_MATRIX_WITH_EXPLICIT_BOUNDARIES",
            )
        ),
        "chapter_8_reader_navigation": all(
            marker in source
            for marker in (
                "## 8.14 从诊断入口到可解释证据",
                "### 8.14.1 三类 reduced diagnostics 的最小起点",
                "## 8.17 本章结论",
                "先写问题和比较对象",
                "保留失败与不可外推范围",
            )
        ),
        "chapter_5_geometry_order_gap_register": all(
            marker in source
            for marker in (
                "### 5.14.2 覆盖范围与已知空白",
                "negative-space contract",
                "RZ 默认 axis correction 下的 charge residual",
                "跨 geometry/shape 的正式收敛阶",
                "Vay geometry/order family",
                "Cartesian 2D/3D 路径",
                "RZ/1D/implicit 的 guard",
                "单进程和两进程的 Cartesian Langmuir 分析",
                "shape 扩展到 `1..4` 的 sibling",
                "Vay + mesh refinement",
                "初始化阶段显式拒绝",
            )
        ),
        "esirkepov_publication_boundary_contract": all(
            marker in source
            for marker in (
                "发表版证据边界",
                "预印本公式、该源码快照和代表性运行案例",
                "publisher-PDF 的逐行比较仍未完成",
            )
        ),
        "andriyash_fourier_bessel_literature_closure": all(
            marker in source
            for marker in (
                "6.8.6 v0.74 文献闭环：Andriyash 2016 Fourier-Bessel PSATD",
                "FULL_TEXT_MINERU_CHINESE_NOTE_VERIFIED_WARPX_EQUIVALENCE_BOUNDARY",
                "Andriyash 2016",
            )
        ),
        "esirkepov_publisher_abstract_compare": all(
            marker in source
            for marker in (
                "发表版公开索引摘要与 arXiv 预印本摘要",
                "这个层级只支持摘要级结论",
                "仍保留 PDF 缺口",
            )
        ),
        "pml_evidence_gradient": all(
            marker in source
            for marker in (
                "### 7.5.10 v0.77 PML 证据梯度",
                "PML_EVIDENCE_GRADIENT_WITH_EXPLICIT_RUNTIME_BOUNDARIES",
                "不能逐项证明 `C1-C25`",
                "不能把 RZ 结果外推为 Cartesian PML",
                "不能隐藏负向 `Ex` 极值",
            )
        ),
        "deposition_evidence_gradient": all(
            marker in source
            for marker in (
                "### 5.14.4 v0.78 沉积证据梯度",
                "DEPOSITION_PAPER_SOURCE_RUNTIME_GRADIENT_WITH_EXPLICIT_GAPS",
                "不能写成 CPC 定稿逐式已核对",
                "不能把 RZ pre-physics boundary",
                "不能把 case-local sibling 写成上游注册项",
            )
        ),
        "deposition_convergence_readiness": all(
            marker in source
            for marker in (
                "### 5.14.5 v0.79 收敛研究就绪合同",
                "CONVERGENCE_READINESS_WITH_FORMAL_ORDER_UNPROVEN",
                "不能只凭单调下降",
                "不能把经验 order 当作论文或 WarpX 的正式收敛阶",
            )
        ),
        "cross_geometry_convergence_trends": all(
            marker in source
            for marker in (
                "### 5.14.6 v0.83 独立几何趋势合同",
                "EXPLORATORY_CROSS_GEOMETRY_RESOLUTION_TRENDS_FORMAL_ORDER_UNPROVEN",
                "不做跨几何 pooled fit",
                "RZ/RSPHERE",
            )
        ),
        "formal_convergence_preregistration": all(
            marker in source
            for marker in (
                "### 5.14.7 v0.84 正式收敛 study 预注册合同",
                "FORMAL_CONVERGENCE_REPEAT_SLOPE_GATE_PREREGISTERED_CHARGE_CLOSURE_OPEN",
                "repeat-slope comparison tolerance",
                "每种 geometry 至少有两组独立产生的 family",
                "不允许用 all-cell residual 替代 axis residual",
            )
        ),
        "repeat_family_runner": all(
            marker in source
            for marker in (
                "### 5.14.8 v0.85 第二组 family 的执行前提",
                "### 5.14.9 v0.94 第二组 family 的输入与产物合同",
                "REPEAT_FAMILY_RUNNER_BLOCKED_MPI_LAUNCHER_MISSING",
                "始终使用 `-n 2`",
                "不允许降级为单进程",
                "warpx_used_inputs",
                "在 `diags/` 下至少出现一个 `diag*` 目录",
            )
        ),
        "formal_convergence_second_family": all(
            marker in source
            for marker in (
                "### 5.14.10 v0.92 第二组 family slope 对照",
                "formal-convergence-second-family-v0.92/contract.{json,md}",
                "FORMAL_CONVERGENCE_REPEAT_SLOPE_GATE_PASS_CHARGE_CLOSURE_OPEN",
                "不做跨 geometry pooled fit",
                "FI_PROVIDER=tcp",
            )
        ),
        "formal_convergence_v0110_repeat_gate": all(
            marker in source
            for marker in (
                "### 5.14.26 v0.110 formal convergence repeat-slope gate re-execution",
                "formal-convergence-second-family-v0.110/contract.{json,md}",
                "formal-convergence-repeat-slope-gate-v0.110/contract.{json,md}",
                "2.0135e-11",
                "FORMAL_CONVERGENCE_REPEAT_SLOPE_GATE_PASS_CHARGE_CLOSURE_OPEN",
                "12 个 2-rank producer",
            )
        ),
        "rz_axis_charge_repeat_stability": all(
            marker in source
            for marker in (
                "### 5.14.11 v0.94 axis charge repeat stability",
                "rz-axis-charge-repeat-stability-v0.94/contract.{json,md}",
                "REPEAT_STABLE_AXIS_CHARGE_BOUNDARY_NOT_KERNEL_ROOT_CAUSE",
                "`1e-10` reader-side repeat gate",
                "axis residual 都高于 off-axis residual",
            )
        ),
        "rz_rho_observable_family": (
            (ROOT / "runs/stage-c-validation/esirkepov_langmuir_rz_rho-observable-family/contract.json").is_file()
            and all(marker in source for marker in (
                "将同一 reader-side observable 扩展到 shape=1/2/3/4 的统一 family 后",
                "这补齐的是 rho-side species decomposition 的 shape coverage",
                "同面 axis residual 仍保持 `BOUNDARY`",
            ))
        ),
        "rz_axis_residual_profile": (
            (ROOT / "runs/stage-c-validation/esirkepov_langmuir_rz_axis-residual-profile/contract.json").is_file()
            and all(marker in source for marker in (
                "对同一批 `256x512`、2-rank RZ sibling 做径向 profile",
                "8 个 case 的全局 profile maximum 都落在 `r=0`",
                "不区分 axis volume scaling、staggering/interpolation、mode handling 和 deposition kernel",
            ))
        ),
        "rz_axis_residual_time_profile": (
            (ROOT / "runs/stage-c-validation/esirkepov_langmuir_rz_axis-residual-time-profile/contract.json").is_file()
            and all(marker in source for marker in (
                "将该 profile 扩展到相同 8 个 case 的全部数值 plotfile",
                "16 个 evolved frames 的最大值全部仍在 `r=0`",
                "不关闭 `divE-rho`、current closure 或 formal convergence boundary",
            ))
        ),
        "rz_rho_species_time_profile": (
            (ROOT / "runs/stage-c-validation/esirkepov_langmuir_rz_rho-species-time-profile/contract.json").is_file()
            and all(marker in source for marker in (
                "对同一 8 个 case 的 `rho`、`rho_electrons` 和 `rho_ions` 做全时间 species decomposition",
                "16 个 evolved frames 的最大相对差",
                "仍不关闭独立的 `divE-rho` axis residual",
            ))
        ),
        "rz_axis_divergence_stencil_alignment": all(
            marker in source
            for marker in (
                "### 5.14.14 v0.98 axis divergence stencil alignment",
                "4*Er/dr + DownwardDz(Ez)",
                "RZ_AXIS_STENCIL_ALIGNMENT_OBSERVED_CHARGE_BOUNDARY_OPEN",
                "rz-axis-divergence-stencil-v0.98/contract.{json,md}",
                "79-rz-axis-divergence-stencil-alignment.md",
            )
        ),
        "rz_axis_divergence_resolution_alignment": all(
            marker in source
            for marker in (
                "### 5.14.15 v0.99 axis stencil cross-resolution alignment",
                "RZ_AXIS_STENCIL_ALIGNMENT_CROSS_RESOLUTION_OBSERVED_CHARGE_BOUNDARY_OPEN",
                "rz-axis-divergence-resolution-v0.99/contract.{json,md}",
                "80-rz-axis-divergence-resolution-alignment.md",
            )
        ),
        "rz_axis_divergence_fit_coefficient": all(
            marker in source
            for marker in (
                "### 5.14.16 v0.100 axis divergence fitted coefficient",
                "RZ_AXIS_STENCIL_FIT_COEFFICIENT_CROSS_RESOLUTION_OBSERVED_CHARGE_BOUNDARY_OPEN",
                "rz-axis-divergence-fit-v0.100/contract.{json,md}",
                "81-rz-axis-divergence-fitted-coefficient.md",
            )
        ),
        "rho_axis_correction_ratio_boundary": all(
            marker in source
            for marker in (
                "### 5.14.17 v0.101 rho-side axis correction ratio boundary",
                "RZ_RHO_AXIS_CORRECTION_RATIO_MISMATCH_BOUNDARY_OPEN",
                "rz-rho-axis-correction-ratio-v0.101/contract.{json,md}",
                "82-rz-rho-axis-correction-ratio-boundary.md",
            )
        ),
        "rho_axis_prescale_input_boundary": all(
            marker in source
            for marker in (
                "### 5.14.18 v0.102 rho-side scaling 前 axis 输入边界",
                "RZ_RHO_AXIS_PRESCALE_INPUT_BOUNDARY_OPEN",
                "rz-rho-axis-prescale-boundary-v0.102/contract.{json,md}",
                "83-rz-rho-axis-prescale-boundary.md",
                "1.133333",
            )
        ),
        "rho_particle_state_invariant": all(
            marker in source
            for marker in (
                "### 5.14.19 v0.103 rho axis particle-state invariant",
                "RZ_RHO_AXIS_DIAGNOSTIC_CONSUMER_BOUNDARY_OPEN",
                "rz-rho-particle-state-invariant-v0.103/contract.{json,md}",
                "84-rz-rho-particle-state-invariant.md",
                "58880/58880",
            )
        ),
        "axis_correction_default_explicit_true": all(
            marker in source
            for marker in (
                "### 5.14.20 v0.104 default versus explicit true axis correction",
                "RZ_AXIS_CORRECTION_DEFAULT_EXPLICIT_TRUE_EQUIVALENT_FALSE_BOUNDARY_OPEN",
                "rz-axis-correction-default-explicit-true-v0.104/contract.{json,md}",
                "85-rz-axis-correction-default-explicit-true.md",
                "default true vs explicit true",
            )
        ),
        "axis_correction_nonneutral_control": all(
            marker in source
            for marker in (
                "### 5.14.21 v0.105 non-neutral control exposes total-rho contribution",
                "RZ_NONNEUTRAL_AXIS_CORRECTION_REVEALS_TOTAL_RHO_CONTRIBUTION_BOUNDARY_OPEN",
                "rz-axis-correction-nonneutral-control-v0.105/contract.{json,md}",
                "86-rz-axis-correction-nonneutral-control.md",
                "delta(rho)",
            )
        ),
        "axis_correction_nonneutral_shape_family": all(
            marker in source
            for marker in (
                "### 5.14.22 v0.106 non-neutral shape family narrows the axis boundary",
                "RZ_NONNEUTRAL_AXIS_CORRECTION_SHAPE_DEPENDENT_AXIS_BOUNDARY_OPEN",
                "rz-axis-correction-nonneutral-shape-family-v0.106/contract.{json,md}",
                "87-rz-axis-correction-nonneutral-shape-family.md",
                "0.850000000/0.843478261/0.836500221/0.831672744",
            )
        ),
        "axis_correction_nonneutral_resolution_family": all(
            marker in source
            for marker in (
                "### 5.14.23 v0.107 non-neutral shape behavior across resolution",
                "RZ_NONNEUTRAL_AXIS_CORRECTION_SHAPE_DEPENDENT_CROSS_RESOLUTION_BOUNDARY_OPEN",
                "rz-axis-correction-nonneutral-shape-resolution-family-v0.107/contract.{json,md}",
                "88-rz-axis-correction-nonneutral-shape-resolution-family.md",
                "0.168327256",
            )
        ),
        "axis_correction_nonneutral_density_family": all(
            marker in source
            for marker in (
                "### 5.14.24 v0.108 non-neutral shape behavior across ion density",
                "RZ_NONNEUTRAL_AXIS_CORRECTION_TOTAL_RHO_CANCELLATION_DENSITY_SENSITIVE_BOUNDARY_OPEN",
                "rz-axis-correction-nonneutral-density-family-v0.108/contract.{json,md}",
                "89-rz-axis-correction-nonneutral-density-family.md",
                "0.25*n0",
            )
        ),
        "axis_correction_nonneutral_density_triple": all(
            marker in source
            for marker in (
                "### 5.14.25 v0.109 non-neutral shape behavior across three density ratios",
                "RZ_NONNEUTRAL_AXIS_CORRECTION_TOTAL_RHO_SAMPLED_AXIS_CANCELLATION_SPECIAL_RATIO_BOUNDARY_OPEN",
                "rz-axis-correction-nonneutral-density-triple-v0.109/contract.{json,md}",
                "90-rz-axis-correction-nonneutral-density-triple.md",
                "0.25*n0",
                "0.5*n0",
                "0.75*n0",
            )
        ),
        "editorial_quality_audit": all(
            marker in source
            for marker in (
                "PDF_LAYOUT_AUTOMATED_PASS_MANUAL_SPOTCHECK_RECORDED",
                "人工全书通读",
                "公开再分发",
            )
        ),
        "pdf_layout_audit": all(
            marker in source
            for marker in (
                "PDF_LAYOUT_AUTOMATED_PASS_MANUAL_SPOTCHECK_RECORDED",
                "第 7 章边界 regression 五列表格",
                "代表页",
            )
        ),
        "manual_editorial_spotcheck": all(
            marker in manual_spotcheck
            for marker in (
                "# v0.110 PDF manual editorial spotcheck",
                "| 174 |",
                "| 183 |",
                "| 189 |",
                "短页为附录结尾的预期留白",
                "全书人工通读、第三方材料许可和公开再分发仍需单独签收",
            )
        ),
        "public_path_hygiene_markdown": inspect(MERGED_MARKDOWN)["passed"],
        "current_gap_register": all(
            marker in source
            for marker in (
                "## 9.8 如何阅读证据边界",
                "formal numerical order",
                "第 8 章的验证矩阵",
            )
        ),
        "transition_zone_runtime_activation": all(
            marker in source
            for marker in (
                "RUNTIME_TRANSITION_ZONE_BRANCH_ACTIVATION_OBSERVED_ROUTE_LEDGER_UNPROVEN",
                "transition-zone-runtime-activation-v0.104/contract.{json,md}",
                "PartitionParticlesInBuffers",
                "OwnerMask()",
                "不能替代 route-count ledger",
            )
        ),
        "public_path_hygiene_html": inspect(HTML)["passed"],
    }

    if args.build_log:
        log = args.build_log.read_text(encoding="utf-8", errors="ignore")
        checks["build_log_clean"] = not any(
            marker in log
            for marker in (
                "Could not fetch resource",
                "Could not convert TeX math",
                "Missing character",
            )
        )

    print("v0.110 artifact verification")
    for name, passed in checks.items():
        print(f"  [{'PASS' if passed else 'FAIL'}] {name}")
    if not all(checks.values()):
        raise SystemExit("v0.110 artifact verification failed")
    print("[PASS] all v0.110 artifact checks")


if __name__ == "__main__":
    main()
