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
APPENDIX_SYMBOLS = ROOT / "manuscript" / "appendices" / "A-symbols.md"
MERGED_MARKDOWN = ROOT / "dist" / "pic-tutor-v0.110.md"
HTML = ROOT / "dist" / "pic-tutor-v0.110.html"
PDF = ROOT / "dist" / "pic-tutor-v0.110.pdf"
MANUAL_SPOTCHECK = ROOT / "docs" / "manual-editorial-spotcheck-v0.110.md"
# Reader-facing chapter openings, long-chapter navigation, and declared source
# The Chapter 5 convergence reading card yields 257 pages.
EXPECTED_PDF_PAGES = 257


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
    appendix_symbols = APPENDIX_SYMBOLS.read_text(encoding="utf-8")
    merged = MERGED_MARKDOWN.read_text(encoding="utf-8")
    html = HTML.read_text(encoding="utf-8", errors="ignore")
    reader = PdfReader(str(PDF))
    pdf_text = "\n".join(page.extract_text() or "" for page in reader.pages)
    chapter_8_conclusion_pages = [
        page.extract_text() or ""
        for page in reader.pages
        if "8.17 本章结论" in (page.extract_text() or "")
        and "诊断的价值不在于输出文件越多" in (page.extract_text() or "")
    ]
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
    chapter_2_project_narration_markers = re.findall(
        r"本书采用的源码快照|本书后续章节的阅读规则", chapter_2
    )
    chapter_3_stale_location_markers = re.findall(
        r"(?:\.\./warpx/)?Source/[A-Za-z0-9_./-]+\.(?:cpp|H):\d+", chapter_3
    )
    chapter_3_workspace_markers = re.findall(r"\.\./warpx/", chapter_3)
    chapter_3_project_narration_markers = re.findall(
        r"当前实现限制最多两个 level|当前 subcycling 只支持|"
        r"当前实现把 `max_particle_iterations=1`|当前源码禁止",
        chapter_3,
    )
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
    chapter_3a_application_record_markers = re.findall(
        r"runtime matrix|active tests|checksum baseline",
        chapter_3a,
    )
    chapter_4 = (ROOT / "manuscript" / "chapters" / "04-particle-pushers.md").read_text(
        encoding="utf-8"
    )
    chapter_4_stale_location_markers = re.findall(
        r"Source/[A-Za-z0-9_./-]+\.(?:cpp|H):\d+", chapter_4
    )
    chapter_4_workspace_markers = re.findall(r"\.\./warpx/", chapter_4)
    chapter_4_opening = chapter_4[: chapter_4.index("## 4.1")]
    chapter_5 = (ROOT / "manuscript" / "chapters" / "05-deposition-shapes.md").read_text(
        encoding="utf-8"
    )
    chapter_5_stale_location_markers = re.findall(
        r"Source/[A-Za-z0-9_./-]+\.(?:cpp|H):\d+", chapter_5
    )
    chapter_5_workspace_markers = re.findall(r"\.\./warpx/", chapter_5)
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
    chapter_8_applications = chapter_8[
        chapter_8.index("## 激光与束流驱动的尾场加速") :
        chapter_8.index("## 诊断在源码中的位置")
    ]
    chapter_8_application_record_markers = re.findall(
        r"当前 CI|active tree|runtime matrix|workflow matrix|当前最硬断言|当前最强",
        chapter_8_applications,
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
        "appendix_distinguishes_plotfile_from_checkpoint": all(
            marker in appendix_symbols
            for marker in (
                "分析用的网格/粒子输出；不可 restart，重启使用 `Full` checkpoint",
            )
        ),
        "primary_sections_start_on_new_pdf_pages": merged.count("\\clearpage") == len(PAGE_BREAK_PARTS),
        "chapter_8_conclusion_is_not_orphaned": (
            len(chapter_8_conclusion_pages) == 1
            and "保留失败与不可外推范围" in chapter_8_conclusion_pages[0]
            and "8.16 延伸验证路线" in chapter_8_conclusion_pages[0]
        ),
        "reader_facing_front_matter": all(
            marker in version + "\n" + preface
            for marker in ("# PIC-tutor", "建议的阅读方式", "如何使用本书", "遇到一个新的输入或源码分支时")
        ) and not front_matter_project_markers,
        "preface_defines_cross_chapter_terms": all(
            marker in preface
            for marker in (
                "四个跨章节术语",
                "被某个场或方程更新实际消费的离散源项或状态",
                "在确定的生命周期阶段创建、推进、沉积、同步或归约某个状态的代码路径",
                "读取该状态以更新场、写诊断、作比较或产生后续状态的代码路径",
                "为回答一个物理问题而定义、可与解析解、守恒关系、reference 或实验量比较的量",
                "源码可以定位职责，指定案例可以检验给定条件下的 observable，全文文献可以支撑公式或机制",
            )
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
        "chapter_5_6_source_to_field_handoff": all(
            marker in chapter_6
            for marker in (
                "从第 5 章同步 source 到第 6 章场更新的交接卡",
                "不是所有求解器都在同一函数内取得最终 source 的同义句",
                "`CopyJPML()`、`DampJPML()`",
                "非 periodic-single-box 的 current-correction 或 Vay deposition 路径会把最终整理延后到 `PushPSATD()`",
                "`current_fp_vay` 的 D-field 重构 `current_fp`",
                "`OneStep_JRhom()` 先完整推进粒子却设置 `skip_deposition=true`",
                "`J_0`、suborbit current 与 mass-matrix 线性化",
                "一次 nonlinear trial 不是独立的场更新样本",
            )
        ) and not chapter_6_stale_location_markers and not re.search(
            r"scripts/|notes/code-reading|runs/stage-c-validation|docs/chapter-06-v0-evidence-ledger|"
            r"contract\.\{json,md\}|全文笔记|逐式记录|证据台账",
            chapter_6,
        ),
        "chapter_6_long_chapter_reader_navigation": all(
            marker in chapter_6
            for marker in (
                "阅读路线：先锁定离散表示，再把选择接到证据",
                "先读 6.1--6.4。",
                "再读 6.5--6.8。",
                "按物理模型选择 6.9 或 6.10。",
                "最后读 6.11。",
                "用 6.12--6.13 收束。",
                "几何与表示 -> source 时间模型 -> 边界/同步 -> observable",
            )
        ) and not re.search(
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
        "chapter_2_time_contract_reader_route": all(
            marker in chapter_2
            for marker in (
                "读者的时间层判断卡",
                "先不要按函数出现次数数“执行了多少步”",
                "细层的真实推进、source 的时间积分，或非线性求解的试探",
                "`OneStep_sub1()` 的这一路径明确限定：只支持两级 mesh refinement",
                "不能把 Poisson/electrostatic 路径的源项和场解时序悄悄套进来",
                "从 `WarpX::OneStep()` 的分派和各路径的函数职责看",
                "应按下面三条路径分别阅读",
                "一次 RHS 评估不是一次物理时间步",
            )
        ) and "| 路径 | 外层入口 | 源项/粒子时间组织 | 场推进特点 | 组合边界 |" not in chapter_2
        and not chapter_2_project_narration_markers,
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
        "chapter_3_lifecycle_reader_route": all(
            marker in chapter_3
            for marker in (
                "读者的生命周期检查卡",
                "输入参数先决定求解器、几何和 AMR 分支",
                "初始化负责创建可被第一步消费的离散状态",
                "外层步只定义 $t^n\\to t^{n+1}$ 的提交边界",
                "单步分派才决定实际进入哪条时间合同",
                "该函数拒绝超过两个 level，且要求 2:1 refinement ratio",
            )
        ) and not chapter_3_project_narration_markers,
        "chapter_3_reader_code_examples_are_wrapped": all(
            marker in chapter_3
            for marker in (
                "moving_window_x += (moving_window_v - WarpX::beta_boost * PhysConst::c)\n",
                "EvolveB(0.5_rt * dt[0], SubcyclingHalf::SecondHalf,\n",
                "FieldType::current_cp, finest_level, skip_lev0_coarse_patch),",
                "EvolveB(fine_lev, PatchType::fine, 0.5_rt*dt[fine_lev],\n",
                "mypc->DepositCurrent(\n        m_fields.get_mr_levels_alldirs(current_string, finest_level),",
            )
        ) and all(
            marker not in chapter_3
            for marker in (
                "moving_window_x += (moving_window_v - WarpX::beta_boost * PhysConst::c)/(1 -",
                "EvolveB(0.5_rt * dt[0], SubcyclingHalf::SecondHalf, a_cur_time",
                "FieldType::current_cp, finest_level, skip_lev0_coarse_patch), fine_lev);",
                "EvolveB(fine_lev, PatchType::fine, 0.5_rt*dt[fine_lev], SubcyclingHalf::SecondHalf",
                "mypc->DepositCurrent( m_fields.get_mr_levels_alldirs(current_string, finest_level)",
            )
        ) and all(
            marker in pdf_text
            for marker in (
                "moving_window_v * WarpX::beta_boost / PhysConst::c",
                "skip_lev0_coarse_patch",
                "t_deposit_current",
                "fluid 的 MultiFab",
            )
        ) and "`E/B/current/PML/F/G/rho/fluid`" not in chapter_3,
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
        "chapter_1_2_model_to_loop_handoff": all(
            marker in chapter_1
            for marker in (
                "跨章交接卡：从连续对象进入离散循环",
                "第 1 章回答“哪些物理对象必须被表示”；第 2 章回答“这些对象在一个离散时间步的什么时刻交换”",
                "一次 charge deposition 不能替代守恒的 current deposition 或 source synchronization",
                "CFL 可通过不表示",
            )
        ) and all(
            marker in chapter_2
            for marker in (
                "从第 1 章进入本章：先写状态，再读调用顺序",
                r"当前粒子状态是 \(x^n,p^{n-1/2},w\)",
                r"\(\omega_p\Delta t\)、\(\lambda_D/\Delta x\)、CFL 和统计粒子数",
                "状态转换的实现，而不是可以脱离物理和时间层独立记忆的调用顺序",
            )
        ),
        "chapter_1_continuous_model_reader_route": all(
            marker in chapter_1
            for marker in (
                "本章的读者路线",
                "什么量在相空间中守恒、哪些矩成为场的 source",
                "程序实际表示什么、与哪一个连续量比较、该比较还不能保证什么",
                "dN_s=f_s",
                "传播的电磁辐射和激光等效应不被捕获",
                "看起来近静电",
            )
        ) and not chapter_1_project_markers,
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
        "chapter_6_7_field_to_boundary_handoff": all(
            marker in chapter_7
            for marker in (
                "从第 6 章场更新到第 7 章边界状态的交接卡",
                "不等于主域、PML、physical boundary 和所有 guard cell 已在同一时刻准备好",
                "FDTD 的物理边界在每次场更新内施加",
                "`DampPML()`，并对 `E/B/F/G` 做 moving-window 宽度的 `FillBoundary*()`",
                "普通 PSATD 路径才以 `ng_afterPushPSATD` 填充 `E/B`",
                "`FillBoundary` 不是物理边界条件的别名",
                "`ExplicitFillBoundaryEBUpdateAux()` 按 `ng_FieldGather` 准备 `E/B`",
                "粒子边界仍是独立路径",
                "一个主域场 snapshot 或一次 `FillBoundary` 成功都不能单独证明",
            )
        ) and not chapter_7_stale_location_markers and not re.search(
            r"scripts/|notes/code-reading|runs/stage-c-validation|"
            r"docs/chapter-07-v0-evidence-ledger|contract\.\{json,md\}",
            chapter_7,
        ),
        "chapter_7_long_chapter_reader_navigation": all(
            marker in chapter_7
            for marker in (
                "分段阅读：先闭合拓扑，再进入几何与 AMR",
                "先读 7.0--7.3。",
                "再读 7.4--7.5。",
                "按几何需求读 7.6--7.8。",
                "最后读 7.9。",
                "用 7.10--7.11 收束。",
                "拓扑 -> 更新/迁移 -> observable -> 不可外推范围",
            )
        ) and not re.search(
            r"scripts/|notes/code-reading|runs/stage-c-validation|"
            r"docs/chapter-07-v0-evidence-ledger|contract\.\{json,md\}",
            chapter_7,
        ),
        "chapter_7_reader_indexes_are_declared": all(
            marker in chapter_7
            for marker in (
                "这不是完整函数签名，而是对 `PML` 构造参数",
                "`Source/EmbeddedBoundary/WarpXInitEB.cpp`",
                "这段是控制流摘录，不是可编译源码",
            )
        ) and "`Source/WarpXInitEB.cpp`" not in chapter_7,
        "chapter_8_current_diagnostics_route": all(
            marker in chapter_8
            for marker in (
                "本章不按文件格式罗列功能",
                "先定义想测的物理量",
                "WarpX::Evolve",
                "MultiDiagnostics",
                "ReducedDiags",
                "### 8.14.2 一张诊断记录卡",
                "producer 与时间层",
                "consumer 与比较量",
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
        "chapter_7_8_boundary_to_diagnostics_handoff": all(
            marker in chapter_8
            for marker in (
                "从第 7 章边界状态到第 8 章证据的交接卡",
                "并不天然代表同一采样时刻或同一组运行态",
                "`multi_diags->FilterComputePackFlush(step, false, true)`",
                "再执行 `MoveWindow()` 与 `HandleParticlesAtBoundaries()`",
                "边界状态先形成，普通诊断随后读取",
                "`SynchronizeVelocityWithPosition()`",
                "`BoundaryScrapingDiagnostics::DoComputeAndPack()` 则固定返回 false",
                "写入按边界命名的目录，然后清空 buffer",
                "任何一份末态 plotfile、reduced scalar 或空的 scraping 目录都不能单独证明",
            )
        ) and not re.search(
            r"scripts/|notes/code-reading|runs/stage-c-validation|"
            r"docs/chapter-08-v0-evidence-ledger|contract\.\{json,md\}|"
            r"本地|本机|当前 checkout|当前分支|项目内|项目级|维护台账|交接记录|源码笔记",
            chapter_8,
        ),
        "chapter_8_application_cases_are_reader_facing": all(
            marker in chapter_8_applications
            for marker in (
                "先把诊断问题写成四项",
                "先用解析尺度或文献给出场、相位和能谱的预期",
                "源码案例承担“如何搭建和输出”的职责",
                "却不是自动成立的统一物理基准",
            )
        )
        and not chapter_8_application_record_markers,
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
        "chapter_9_reader_navigation": all(
            marker in chapter_9
            for marker in (
                "阅读路线：先分类证据，再把一条主张接回教程",
                "先读 9.1。",
                "再读 9.2 与当前章节对应的一条主线。",
                "用 9.3--9.5 确认缺口与优先级。",
                "用 9.6--9.10 输出一张判读卡。",
                "能支持",
                "不能支持",
            )
        ) and not re.search(
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
        ) and not chapter_3a_stale_location_markers and not chapter_3a_project_markers and not chapter_3a_application_record_markers,
        "chapter_3a_laser_cases_are_reader_facing": all(
            marker in chapter_3a
            for marker in (
                "选择激光案例：先匹配问题，再读取输入",
                "问题与几何假设",
                "只对该 reference 覆盖的 observable 下结论",
                "应用输入提供的是搭建起点，而不是已经完成的物理说明",
                "激光在应用输入中的四种角色",
                "每一层只为相应的 producer/consumer 接口提供证据",
            )
        ) and not chapter_3a_application_record_markers,
        "chapter_3a_reader_code_examples_are_wrapped": all(
            marker in chapter_3a
            for marker in (
                "auto const& pos = plasma_injector->single_particle_pos;",
                "const auto max_new_particles =\n    amrex::Scan::ExclusiveSum(",
                "先略去只负责几何维度开关的预处理",
                "目录：`Examples/Tests/particle_absorbing_boundary/`",
                "| `3A ES1` 阶段 | WarpX 的现代映射与不能直接等同的部分 |",
            )
        ) and all(
            marker not in chapter_3a
            for marker in (
                "const amrex::Long max_new_particles = amrex::Scan::ExclusiveSum(counts.size(), counts.data(), offset.data());",
                "const amrex::Vector<ParticleReal> uxp = {plasma_injector->single_particle_u[0]};",
                "Examples/Tests/particle_absorbing_boundary/inputs_test_1d_particle_absorbing_boundary",
                "| `3A ES1` 阶段 | 历史程序的物理职责 | WarpX 中最接近的阶段 | 不能直接等同的部分 |",
            )
        ) and all(
            marker in pdf_text
            for marker in (
                "const auto max_new_particles",
                "position_offset_unit_x",
                "particle_absorbing_boundary",
                "WarpX 的现代映射与不能直接等同的部分",
            )
        ),
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
        ) and not chapter_4_stale_location_markers and not chapter_4_workspace_markers and not re.search(
            r"本地 checkout|原文精读|本书采用的实现",
            chapter_4,
        ),
        "chapter_4_particle_state_reader_route": all(
            marker in chapter_4
            for marker in (
                "读者的单粒子状态检查卡",
                "决定轨道的量”和“决定它对网格 source 的量",
                r"有效电荷 \(q_{\mathrm{eff}}=q\,\texttt{ionizationLevel}\)",
                r"并不接收宏粒子权重 \(w\)",
                "只有 `PositionPushType::Full` 才会",
                r"随后的 charge/current deposition 才构造 \(wq=q\,w\,\texttt{ionizationLevel}\)",
                r"相同的单粒子轨道、不同的 \(\rho/\mathbf J\) 贡献",
                "不能单独证明宏粒子 source、连续性或自洽场演化正确",
            )
        ) and not re.search(r"本地 checkout|原文精读|本书采用的实现", chapter_4),
        "chapter_4_reader_extracts_are_declared": all(
            marker in chapter_4
            for marker in (
                "为阅读重排的核心节选",
                "为阅读压缩的核心节选",
                "等价的阅读伪代码",
                "x 方向有效计算的阅读伪代码",
                "component_needs_node",
            )
        ) and "源码原文如下：" not in chapter_4,
        "chapter_4_multiphysics_state_reader_route": all(
            marker in chapter_4
            for marker in (
                "读者的多物理状态交接卡",
                "先区分“事件何时提交”与“新状态何时被 solver 消费”",
                "`doFieldIonization()` -> QED event pass -> `particleinjection` -> `OneStep()`",
                "`doQEDEvents()` 只消费已经由 pusher 演化到触发条件的 optical depth",
                "`collisions.split_momentum_push` 只在 explicit 路径中组织半步动量",
                "`OneStep_JRhom()` 与 `OneStep_sub1()` 都要求关闭 split momentum push",
                "photon container 能演化位置和 Breit-Wheeler optical depth，却自身不沉积 charge/current",
                "一次 nonlinear trial 不是新的物理外层步",
            )
        ) and not re.search(r"本地 checkout|原文精读|本书采用的实现", chapter_4),
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
                "阅读 5.14--5.15",
            )
        ),
        "chapter_4_has_no_project_path_narration": not chapter_4_workspace_markers and not re.search(
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
                "核查练习。",
            )
        ) and not chapter_5_stale_location_markers and not chapter_5_workspace_markers and not chapter_5_project_markers,
        "chapter_5_convergence_reader_card": all(
            marker in chapter_5
            for marker in (
                "### 5.14.7 收敛判读卡：先检验斜率，再讨论阶数",
                "相邻两档网格上的局部斜率",
                "不同 geometry 也不能合并拟合成一个共同的",
                "逐区间报告",
                "把重复性和正确性分开",
                "正式阶数与 axis-charge closure 仍未建立",
            )
        ) and not chapter_5_stale_location_markers and not chapter_5_workspace_markers and not chapter_5_project_markers,
        "chapter_5_reader_extracts_are_declared": all(
            marker in chapter_5
            for marker in (
                "等价的阅读伪代码",
                "等价阅读伪代码",
                "完整签名还接收",
                "不是可编译源码",
                "完整的 x/y/z 三层循环",
            )
        ) and "源码原文如下：" not in chapter_5,
        "chapter_4_5_multiphysics_source_handoff": all(
            marker in chapter_5
            for marker in (
                "从第 4 章状态到第 5 章 source 的交接卡",
                "多物理过程只要改变了粒子，并不自动等于它已经改变了网格 source",
                "外层 `doFieldIonization()` 在 `OneStep()` 前同时增加源离子的 `ionizationLevel`",
                r"两类 kernel 都从 \(wq=q\,w\) 出发再乘该离化态",
                "photon container 本身的 `DepositCharge()` / `DepositCurrent()` 是空实现",
                "第一半动量 push 显式设置 `skip_deposition=true`",
                "只有收敛路径及其专门的 `current_fp_non_suborbit` / suborbit 沉积拼装才进入场方程",
                "一次 charge deposition 也不能替代守恒的 current deposition 或 source synchronization",
            )
        ) and not chapter_5_stale_location_markers and not chapter_5_workspace_markers and not chapter_5_project_markers,
        "chapter_5_opening_is_reader_facing": not re.search(
            r"notes/code-reading|pkuHEDPbranch|8c488b1a9|本机|本轮|当前源码",
            chapter_5_opening,
        ),
        "chapter_1_section_order": chapter_1_numbers == list(range(1, 15)),
        "chapter_1_inline_math_is_not_code": (
            "finite `\\Delta x`" not in chapter_1
            and "finite `\\Delta t`" not in chapter_1
            and "finite \\(\\Delta x\\)" in chapter_1
            and "finite \\(\\Delta t\\)" in chapter_1
            and "`lambda_D/delta_x = 0.5`" not in chapter_1
            and "`v_t Delta t/delta_x = 1.2`" not in chapter_1
            and "\\(\\lambda_D/\\Delta x=0.5\\)" in chapter_1
            and "\\(v_t\\Delta t/\\Delta x=1.2\\)" in chapter_1
        ),
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
                "预印本公式、当前源码实现和代表性运行案例",
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
                "本轮连续阅读已覆盖当前 PDF 第 1--257 页",
                "| 1--6 |",
                "| 120--164 |",
                "| 165--200 |",
                "| 214--249 |",
                "| 250--254 |",
                "| 255--257 |",
                "第三方材料许可确认、公开再分发签收",
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
