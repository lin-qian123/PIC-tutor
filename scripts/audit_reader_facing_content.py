#!/usr/bin/env python
"""Audit whether the book entry points read like a tutorial rather than a changelog."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


def section_between(text: str, start_heading: str, end_heading: str) -> str:
    """Return a Markdown section without relying on its line number."""
    start = text.index(start_heading)
    end = text.index(end_heading, start)
    return text[start:end]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--output-md", type=Path, required=True)
    args = parser.parse_args()

    root = args.root.resolve()
    version = (root / "manuscript/VERSION.md").read_text(encoding="utf-8")
    readme = (root / "manuscript/README.md").read_text(encoding="utf-8")
    preface = (root / "manuscript/chapters/00-preface.md").read_text(encoding="utf-8")
    chapters = sorted((root / "manuscript/chapters").glob("*.md"))
    chapter_text = "\n".join(path.read_text(encoding="utf-8") for path in chapters)
    chapter_9 = (root / "manuscript/chapters/09-literature-roadmap.md").read_text(encoding="utf-8")
    chapter_4 = (root / "manuscript/chapters/04-particle-pushers.md").read_text(encoding="utf-8")
    chapter_5 = (root / "manuscript/chapters/05-deposition-shapes.md").read_text(
        encoding="utf-8"
    )
    chapter_6 = (root / "manuscript/chapters/06-field-solvers.md").read_text(encoding="utf-8")
    chapter_7 = (root / "manuscript/chapters/07-boundaries-amr.md").read_text(encoding="utf-8")
    chapter_8 = (root / "manuscript/chapters/08-diagnostics-cases.md").read_text(encoding="utf-8")
    chapter_1 = (root / "manuscript/chapters/01-kinetic-models.md").read_text(encoding="utf-8")
    chapter_2 = (root / "manuscript/chapters/02-pic-loop.md").read_text(encoding="utf-8")
    chapter_2_code_spans = re.findall(r"`([^`]*)`", chapter_2)
    chapter_3 = (root / "manuscript/chapters/03-warpx-evolve.md").read_text(encoding="utf-8")
    reader_entry_project_path_pattern = r"scripts/|notes/|runs/|docs/|references/|contract\\.\\{json,md\\}"
    chapter_1_project_path_markers = re.findall(reader_entry_project_path_pattern, chapter_1)
    chapter_2_project_path_markers = re.findall(reader_entry_project_path_pattern, chapter_2)
    chapter_3_project_path_markers = re.findall(reader_entry_project_path_pattern, chapter_3)
    chapter_2_stale_location_markers = re.findall(
        r"(?:\.\./warpx/)?Source/[A-Za-z0-9_./-]+\.(?:cpp|H):\d+", chapter_2
    )
    chapter_2_workspace_markers = re.findall(r"\.\./warpx/", chapter_2)
    chapter_3_stale_location_markers = re.findall(
        r"(?:\.\./warpx/)?Source/[A-Za-z0-9_./-]+\.(?:cpp|H):\d+", chapter_3
    )
    chapter_3_workspace_markers = re.findall(r"\.\./warpx/", chapter_3)
    chapter_3a = (root / "manuscript/chapters/03a-warpx-initialization.md").read_text(
        encoding="utf-8"
    )
    chapter_3a_opening = section_between(
        chapter_3a, "# 3A. WarpX 初始化链", "## 3A.1"
    )
    chapter_3a_stale_location_markers = re.findall(
        r"Source/[A-Za-z0-9_./-]+\.(?:cpp|H):\d+", chapter_3a
    )
    chapter_3a_project_path_markers = re.findall(
        r"scripts/|notes/code-reading|runs/stage-c-validation|docs/|references/|contract\.\{json,md\}",
        chapter_3a,
    )
    chapter_3a_project_narration_markers = re.findall(
        r"本地|本机|当前 checkout|当前分支|项目内|项目级|维护台账|交接记录|"
        r"源码笔记|初始化笔记|笔记编号",
        chapter_3a,
    )
    chapter_4_stale_location_markers = re.findall(
        r"Source/[A-Za-z0-9_./-]+\.(?:cpp|H):\d+", chapter_4
    )
    chapter_4_opening = section_between(chapter_4, "# 4. 粒子推进器", "## 4.1")
    chapter_5_stale_location_markers = re.findall(
        r"Source/[A-Za-z0-9_./-]+\.(?:cpp|H):\d+", chapter_5
    )
    chapter_6_stale_location_markers = re.findall(
        r"Source/[A-Za-z0-9_./-]+\.(?:cpp|H):\d+", chapter_6
    )
    chapter_7_stale_location_markers = re.findall(
        r"(?:Source/[A-Za-z0-9_./-]+\.(?:cpp|H)|Docs/[A-Za-z0-9_./-]+\.rst):\d+",
        chapter_7,
    )
    chapter_8_stale_location_markers = re.findall(
        r"(?:Source/[A-Za-z0-9_./-]+\.(?:cpp|H)|Docs/[A-Za-z0-9_./-]+\.rst):\d+",
        chapter_8,
    )
    chapter_8_opening = section_between(chapter_8, "# 8. 诊断、验证与案例", "## Langmuir wave")
    reader_chapters = [path for path in chapters if path.name != "00-preface.md"]
    chapter_openings = "\n".join(
        path.read_text(encoding="utf-8")[:2500] for path in reader_chapters
    )

    version_markers = re.findall(r"^### .*v0\.\d+", chapter_text, re.MULTILINE)
    versioned_prose_markers = re.findall(r"\bv0\.\d+", chapter_text)
    project_record_words = re.findall(r"发布|审计合同|当前版本|本版新增|本轮新增|运行合同", version + readme, re.MULTILINE)
    project_record_opening_markers = re.findall(
        r"v0\.\d+\s*(?:校准说明|源码基线|的本章目标)|可审校长草稿|正式书稿版|后续扩写计划|本章当前依据|本章当前按|本机现成 PDF/MinerU|本机源码位置|本章当前引用|当前源码入口|项目目录 .*access audit|项目级 helper|交接记录",
        chapter_openings,
    )
    project_record_body_markers = re.findall(
        r"current-checkout|维护台账|本机现成 PDF/MinerU|项目级 helper|交接记录",
        chapter_text,
    )
    front_matter_project_markers = re.findall(
        r"RZ/RSPHERE|repeat-slope|pkuHEDPbranch|scripts/|docs/|runs/|notes/|"
        r"Markdown-first|Quarto|LaTeX book",
        version + "\n" + preface,
    )
    chapter_4_evidence_sections = "\n".join(
        (
            section_between(chapter_4, "### 4.4.1", "## 4.5"),
            section_between(chapter_4, "### 4.13.7", "### 4.13.8"),
            section_between(chapter_4, "### 4.13.8", "### 4.13.9"),
            section_between(chapter_4, "### 4.13.9", "### 4.13.10"),
            section_between(chapter_4, "### 4.13.10", "### 4.13.11"),
            section_between(chapter_4, "### 4.13.11", "### 4.13.12"),
            section_between(chapter_4, "### 4.13.12", "### 4.13.13"),
            section_between(chapter_4, "### 4.13.13", "## 4.14"),
            section_between(chapter_4, "## 4.14", "## 4.15"),
            section_between(chapter_4, "## 4.15", "## 4.16"),
        )
    )
    chapter_4_project_record_markers = re.findall(
        r"runs/stage-c-validation|chapter-04-v0-evidence-ledger|资产合同|文献资产|FULLTEXT_PAPER_BACKED|access boundary",
        chapter_4_evidence_sections,
    )
    chapter_4_project_path_markers = re.findall(
        r"scripts/|notes/code-reading|runs/stage-c-validation|contract\.\{json,md\}",
        chapter_4,
    )
    chapter_4_project_narration_markers = re.findall(
        r"本地 checkout|原文精读",
        chapter_4,
    )
    chapter_5_opening = section_between(chapter_5, "# 5. 电荷、电流沉积与形函数", "## 5.1")
    chapter_5_opening_project_markers = re.findall(
        r"notes/code-reading|pkuHEDPbranch|8c488b1a9|本机|本轮|当前源码",
        chapter_5_opening,
    )
    chapter_5_project_path_markers = re.findall(
        r"scripts/|notes/|runs/|docs/|references/|contract\.\{json,md\}", chapter_5
    )
    chapter_5_project_narration_markers = re.findall(
        r"本机|本地 regression|项目用|项目在|项目独立|本地论文|对应的本地|"
        r"报告位于|汇总报告",
        chapter_5,
    )
    chapter_6_opening = section_between(chapter_6, "# 6. 电磁场求解器", "## 6.1")
    chapter_6_opening_project_markers = re.findall(
        r"notes/code-reading|pkuHEDPbranch|8c488b1a9|本机|本轮|当前源码|源码快照",
        chapter_6_opening,
    )
    chapter_6_closure = section_between(chapter_6, "### 6.11.9", "## 6.13") + chapter_6[
        chapter_6.index("## 6.13") :
    ]
    chapter_6_project_record_markers = re.findall(
        r"runs/stage-c-validation|scripts/audit_|contract\.json|维护边界|后续修改",
        chapter_6_closure,
    )
    chapter_6_project_path_markers = re.findall(
        r"scripts/|notes/code-reading|runs/stage-c-validation|docs/chapter-06-v0-evidence-ledger|contract\.\{json,md\}",
        chapter_6,
    )
    chapter_6_project_narration_markers = re.findall(
        r"全文笔记|逐式记录|证据台账",
        chapter_6,
    )
    chapter_7_opening = section_between(chapter_7, "# 7. 边界条件、PML 与 AMR", "## 7.1")
    chapter_7_closure = chapter_7[chapter_7.index("## 7.10") :]
    chapter_7_project_record_markers = re.findall(
        r"pkuHEDPbranch|8c488b1a9|accepted manuscript|scripts/audit_|正文-源码对应",
        chapter_7_opening + chapter_7_closure,
    )
    chapter_7_project_path_markers = re.findall(
        r"scripts/|notes/code-reading|runs/stage-c-validation|"
        r"docs/chapter-07-v0-evidence-ledger|contract\.\{json,md\}",
        chapter_7,
    )
    chapter_8_closure = chapter_8[chapter_8.index("## 8.14") :]
    chapter_8_project_record_markers = re.findall(
        r"本章正文与源码同步合同|交叉检查脚本|最小输入审计脚本|runs/stage-c-validation",
        chapter_8_closure,
    )
    chapter_8_project_path_markers = re.findall(
        r"scripts/|notes/code-reading|runs/stage-c-validation|"
        r"docs/chapter-08-v0-evidence-ledger|contract\.\{json,md\}",
        chapter_8,
    )
    chapter_8_project_narration_markers = re.findall(
        r"本地|本机|当前 checkout|当前分支|项目内|项目级|维护台账|交接记录|源码笔记",
        chapter_8,
    )
    chapter_9_project_path_markers = re.findall(
        r"docs/|references/|notes/|runs/|scripts/|public-evidence-index|literature-map",
        chapter_9,
    )
    chapter_9_project_narration_markers = re.findall(
        r"仓库|核心目录|文献地图|缺口登记|公开再分发|OPEN_EXTERNAL_ACCESS|"
        r"PRE_PHYSICS_BOUNDARY|RUNTIME_LEDGER_UNPROVEN|"
        r"CONVERGENCE_READINESS_WITH_FORMAL_ORDER_UNPROVEN",
        chapter_9,
    )
    checks = {
        "version_is_reader_facing": "不是开发日志" in version and "读者在本版可以学到什么" in version
        and "建议的阅读方式" in version and not front_matter_project_markers,
        "manuscript_readme_is_reader_facing": "PIC 教程" in readme and "阅读路径" in readme
        and "读者的核查顺序" in readme and "不是面向维护者的提交记录" in readme,
        "preface_has_learning_outcomes": "读者应当能够" in preface and "如何使用本书" in preface
        and "遇到一个新的输入或源码分支时" in preface and not front_matter_project_markers,
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
        "history_is_separated": (root / "docs/version-history-v0.110.md").is_file(),
        "chapter_openings_are_reader_facing": not project_record_opening_markers,
        "core_chapters_have_no_project_record_markers": not project_record_body_markers,
        "chapter_9_uses_reader_facing_evidence_language": not re.search(
            r"本机|本地资产|materialize|asset contract|access audit|metadata contract|source crosswalk|本地路径",
            chapter_9,
        )
        and not chapter_9_project_path_markers
        and not chapter_9_project_narration_markers
        and all(
            marker in chapter_9
            for marker in (
                "文献是论证工具，不是书目清单",
                "一张文献判读卡",
                "## 9.7 两条深读路线",
                "## 9.8 如何阅读证据边界",
                "第 8 章的验证矩阵",
            )
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
        ) and not chapter_9_project_path_markers and not chapter_9_project_narration_markers,
        "chapter_4_uses_reader_facing_evidence_language": not chapter_4_project_record_markers,
        "chapter_4_has_no_project_path_narration": not chapter_4_project_path_markers
        and not chapter_4_project_narration_markers,
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
        ) and not chapter_4_stale_location_markers,
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
        "chapter_5_opening_is_reader_facing": not chapter_5_opening_project_markers,
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
        )
        and not chapter_5_stale_location_markers
        and not chapter_5_project_path_markers
        and not chapter_5_project_narration_markers,
        "chapter_6_opening_is_reader_facing": not chapter_6_opening_project_markers,
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
        ) and not chapter_6_stale_location_markers and not chapter_6_project_path_markers
        and not chapter_6_project_narration_markers,
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
        ) and not chapter_6_project_path_markers and not chapter_6_project_narration_markers,
        "chapter_6_has_reader_facing_closure": all(
            marker in chapter_6_closure
            for marker in (
                "从源码入口回查验证量",
                "最小运行设计题",
                "跨章诊断题",
                "本章结论",
                "先确定几何和物理目标",
            )
        )
        and not chapter_6_project_record_markers,
        "chapter_7_has_reader_facing_boundary_closure": all(
            marker in chapter_7_opening + chapter_7_closure
            for marker in (
                "边界是一个闭合系统",
                "输入参数 -> field boundary / particle boundary",
                "## 7.11 本章结论",
                "拓扑是否一致",
                "观察量是否匹配问题",
                "PartitionParticlesInBuffers()",
            )
        )
        and not chapter_7_project_record_markers
        and not chapter_7_project_path_markers
        and not chapter_7_stale_location_markers,
        "chapter_7_current_boundary_route": all(
            marker in chapter_7
            for marker in (
                "本章按一条读者可追踪的链展开",
                "WarpX::MakeWarpX()",
                "本章的阅读路线：边界是一个闭合系统",
                "每一节都应能回到一个可观察量",
                "## 7.10 本章练习与源码定位",
            )
        )
        and not chapter_7_stale_location_markers
        and not chapter_7_project_path_markers,
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
        ) and not chapter_7_project_path_markers and not chapter_7_project_record_markers,
        "chapter_8_has_reader_facing_diagnostics_closure": all(
            marker in chapter_8_closure
            for marker in (
                "从诊断入口到可解释证据",
                "要测的物理量是什么，处在哪个时间层？",
                "三类 reduced diagnostics 的最小起点",
                "本章结论",
                "先写问题和比较对象",
            )
        )
        and not chapter_8_project_record_markers
        and not chapter_8_project_path_markers
        and not chapter_8_project_narration_markers
        and not chapter_8_stale_location_markers,
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
        and not chapter_8_project_path_markers
        and not chapter_8_project_narration_markers
        and not chapter_8_stale_location_markers,
        "chapter_2_3_have_reader_facing_routes": all(
            marker in chapter_2
            for marker in (
                "## 2.11 本章结论",
                "粒子与网格的交换方式",
                "与问题匹配的 observable",
                "**案例闭环题**",
            )
        ) and "pkuHEDPbranch" not in chapter_2[:2500]
        and "pkuHEDPbranch" not in chapter_3[:2500]
        and not chapter_2_project_path_markers
        and not chapter_3_project_path_markers
        and not chapter_2_stale_location_markers
        and not chapter_3_stale_location_markers
        and not chapter_2_workspace_markers
        and not chapter_3_workspace_markers
        and not any(
            re.search(r"\\(?:omega|lambda|Delta)", span) for span in chapter_2_code_spans
        ),
        "chapter_2_3_source_navigation_is_portable": all(
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
        and not chapter_3_project_path_markers,
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
        "chapter_1_has_no_project_path_narration": not chapter_1_project_path_markers,
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
        )
        and not chapter_3a_stale_location_markers
        and not chapter_3a_project_path_markers
        and not chapter_3a_project_narration_markers,
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
        "core_chapters_have_no_versioned_prose": not versioned_prose_markers,
        "core_chapters_have_exercises": all(
            marker in chapter_text
            for marker in ("练习", "源码定位", "复现实验")
        ),
    }
    result = {
        "contract": "reader-facing content audit",
        "checks": checks,
        "passed": all(checks.values()),
        "classification": "READER_FACING_CORE_CHAPTERS_PASS_HUMAN_FULL_READ_OPEN",
        "scope": "entry-point and learning-path audit; versioned evidence headings have been separated from core tutorial chapters",
        "versioned_chapter_heading_count": len(version_markers),
        "versioned_chapter_headings": version_markers,
        "versioned_prose_marker_count": len(versioned_prose_markers),
        "project_record_word_count_in_entry_points": len(project_record_words),
        "project_record_opening_markers": project_record_opening_markers,
        "project_record_body_markers": project_record_body_markers,
        "front_matter_project_markers": front_matter_project_markers,
        "chapter_4_project_record_markers": chapter_4_project_record_markers,
        "chapter_4_project_path_markers": chapter_4_project_path_markers,
        "chapter_4_project_narration_markers": chapter_4_project_narration_markers,
        "chapter_6_project_record_markers": chapter_6_project_record_markers,
        "chapter_6_project_path_markers": chapter_6_project_path_markers,
        "chapter_6_project_narration_markers": chapter_6_project_narration_markers,
        "chapter_7_project_record_markers": chapter_7_project_record_markers,
        "chapter_7_project_path_markers": chapter_7_project_path_markers,
        "chapter_7_stale_location_markers": chapter_7_stale_location_markers,
        "chapter_8_project_record_markers": chapter_8_project_record_markers,
        "chapter_8_project_path_markers": chapter_8_project_path_markers,
        "chapter_8_project_narration_markers": chapter_8_project_narration_markers,
        "chapter_8_stale_location_markers": chapter_8_stale_location_markers,
        "chapter_9_project_path_markers": chapter_9_project_path_markers,
        "chapter_9_project_narration_markers": chapter_9_project_narration_markers,
        "chapter_3_stale_location_markers": chapter_3_stale_location_markers,
        "chapter_1_project_path_markers": chapter_1_project_path_markers,
        "chapter_2_project_path_markers": chapter_2_project_path_markers,
        "chapter_2_stale_location_markers": chapter_2_stale_location_markers,
        "chapter_2_workspace_markers": chapter_2_workspace_markers,
        "chapter_3_project_path_markers": chapter_3_project_path_markers,
        "chapter_3_workspace_markers": chapter_3_workspace_markers,
        "chapter_3a_stale_location_markers": chapter_3a_stale_location_markers,
        "chapter_3a_project_path_markers": chapter_3a_project_path_markers,
        "chapter_3a_project_narration_markers": chapter_3a_project_narration_markers,
        "chapter_4_stale_location_markers": chapter_4_stale_location_markers,
        "chapter_5_opening_project_markers": chapter_5_opening_project_markers,
        "chapter_5_project_path_markers": chapter_5_project_path_markers,
        "chapter_5_project_narration_markers": chapter_5_project_narration_markers,
        "chapter_5_stale_location_markers": chapter_5_stale_location_markers,
        "chapter_6_opening_project_markers": chapter_6_opening_project_markers,
        "chapter_6_stale_location_markers": chapter_6_stale_location_markers,
        "open_items": [
            "需要人工通读术语、公式、代码上下文、章节过渡和练习",
        ],
    }
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# Reader-facing content audit",
        "",
        f"- classification: `{result['classification']}`",
        f"- scope: {result['scope']}",
        f"- versioned chapter headings remaining: `{len(version_markers)}`",
        "",
        "| check | status |",
        "|---|:---:|",
    ]
    lines.extend(f"| `{name}` | `{'PASS' if value else 'FAIL'}` |" for name, value in checks.items())
    lines.extend(["", "## Open editorial work", ""])
    lines.extend(f"- {item}" for item in result["open_items"])
    args.output_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
