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
    manual_spotcheck = (root / "docs/manual-editorial-spotcheck-v0.110.md").read_text(
        encoding="utf-8"
    )
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
    chapter_3a_application_record_markers = re.findall(
        r"runtime matrix|active tests|checksum baseline",
        chapter_3a,
    )
    chapter_4_stale_location_markers = re.findall(
        r"Source/[A-Za-z0-9_./-]+\.(?:cpp|H):\d+", chapter_4
    )
    chapter_4_workspace_markers = re.findall(r"\.\./warpx/", chapter_4)
    chapter_4_opening = section_between(chapter_4, "# 4. 粒子推进器", "## 4.1")
    chapter_5_stale_location_markers = re.findall(
        r"Source/[A-Za-z0-9_./-]+\.(?:cpp|H):\d+", chapter_5
    )
    chapter_5_workspace_markers = re.findall(r"\.\./warpx/", chapter_5)
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
    chapter_8_applications = section_between(
        chapter_8, "## 激光与束流驱动的尾场加速", "## 诊断在源码中的位置"
    )
    chapter_8_application_record_markers = re.findall(
        r"当前 CI|active tree|runtime matrix|workflow matrix|当前最硬断言|当前最强",
        chapter_8_applications,
    )
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
        r"本地 checkout|原文精读|本书采用的实现",
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
    chapter_8_restart_record_markers = re.findall(
        r"归档的 2D 运行|MPICH|2\.8631e-16|rank-invariant field gate 不通过",
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
        "chapter_9_evidence_routes_reader_card": all(
            marker in chapter_9
            for marker in (
                "### 9.6.1 三条从文献走到可观察量的读者路线",
                "并不证明所有 shape、二维或 RZ",
                "不是解析 NCI growth rate",
                "不是对 LeeCPC2015 所有系数或扫描的复现",
                "论文 -> 实现 -> 输入 -> consumer",
            )
        ) and not chapter_9_project_path_markers and not chapter_9_project_narration_markers,
        "chapter_4_uses_reader_facing_evidence_language": not chapter_4_project_record_markers,
        "chapter_4_has_no_project_path_narration": not chapter_4_project_path_markers
        and not chapter_4_project_narration_markers
        and not chapter_4_workspace_markers,
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
        ) and not chapter_4_project_narration_markers,
        "chapter_4_pusher_validation_ladder_reader_card": all(
            marker in chapter_4
            for marker in (
                "### 4.13.8.1 推进器修改后的验证阶梯：先选对 consumer，再解释结果",
                "第一层：带质量粒子的 momentum--position 链。",
                "第二层：输出时间层，而不是轨道算法。",
                "第三层：无质量粒子是另一条容器链。",
                "第四层：checksum 仍有价值，但不是解析 gate。",
                "单粒子通过不能完成验证",
            )
        ) and not chapter_4_project_path_markers,
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
        ) and not chapter_4_project_narration_markers,
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
                "核查练习。",
            )
        )
        and not chapter_5_stale_location_markers
        and not chapter_5_project_path_markers
        and not chapter_5_project_narration_markers
        and not chapter_5_workspace_markers,
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
        ) and not chapter_5_project_narration_markers,
        "chapter_5_rz_axis_reader_card": all(
            marker in chapter_5
            for marker in (
                "### 5.14.5.1 RZ 轴线判读卡：把一个 residual 拆成三条链",
                "粒子如何写入未缩放 source，几何体积如何把 source 转成密度，以及 field diagnostic 如何在",
                "4E_r(0)",
                "纯体积因子预测",
                "axis 比稳定为 `0.85`",
                "比 naive 的 `2` 更接近源码的 `4`",
                "没有关闭 charge correctness",
            )
        ) and not chapter_5_project_narration_markers,
        "chapter_5_vay_configuration_reader_card": all(
            marker in chapter_5
            for marker in (
                "### 5.14.2.1 Vay 配置判读卡：先分开 pusher 和 deposition",
                "配置接受、算法分派和物理验证是三道不同的门",
                "初始化阶段显式拒绝",
                "一个 Cartesian PASS 证明的是那个输入和 observable",
            )
        ) and not chapter_5_project_narration_markers,
        "chapter_5_rz_implicit_villasenor_reader_card": all(
            marker in chapter_5
            for marker in (
                "### 5.14.2.2 RZ implicit Villasenor 判读卡：初始化停止不等于沉积失败",
                "当前分类是 **pre-physics boundary**",
                "不应把没有产生的 `divE-rho/epsilon_0` 当作一次失败的测量",
                "隐式 PIC 的配置、solver definition、nonlinear residual、粒子推进、source synchronization 和物理 observable 是连续但不同的阶段",
            )
        ) and not chapter_5_project_narration_markers,
        "chapter_5_deposition_validation_ladder_reader_card": all(
            marker in chapter_5
            for marker in (
                "### 5.14.2.3 修改沉积后的验证阶梯：先核 source，再解释场",
                "第一层：先确认配置能够到达对应 kernel",
                "第二层：把 `divE-rho/epsilon_0` 当作 source consumer",
                "第三层：解析场是 field consumer",
                "第四层：checksum 是回归 consumer",
                "未执行检查”误读为 PASS",
            )
        ) and not chapter_5_project_narration_markers,
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
        ) and not chapter_5_stale_location_markers and not chapter_5_project_path_markers
        and not chapter_5_project_narration_markers and not chapter_5_workspace_markers,
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
        "chapter_6_field_solver_validation_ladder_reader_card": all(
            marker in chapter_6
            for marker in (
                "### 6.11.10 场求解器修改后的验证阶梯：先匹配场量，再解释通过",
                "第一层：FDTD/PML 应先看反射率，而不是 checksum",
                "第二层：改 PSATD、Galilean frame 或 current correction 时看 NCI consumer",
                "第三层：改 Poisson 求解或 $\\phi\\to\\mathbf E$ 离散梯度时看解析场",
                "第四层：restart 和 checksum 是生命周期回归 consumer",
                "不是 PASS",
            )
        ) and not chapter_6_stale_location_markers and not chapter_6_project_path_markers
        and not chapter_6_project_narration_markers,
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
        ) and not chapter_7_stale_location_markers and not chapter_7_project_path_markers,
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
        "chapter_7_pml_configuration_reader_card": all(
            marker in chapter_7
            for marker in (
                "### 7.5.3 PML 配置与验证卡：先选问题，再满足依赖",
                "`warpx.pml_ncell` 是 PML 的 cell 厚度",
                "`pml_has_particles = 1` 只能在此条件下使用",
                "`do_pml_dive_cleaning` 与 `do_pml_divb_cleaning` 必须取相同值",
                "RZ PML 只可与 PSATD 使用，且 `z` 方向没有 PML",
                "配置后的最小验收顺序",
            )
        ) and not chapter_7_project_path_markers and not chapter_7_stale_location_markers,
        "chapter_7_transition_zone_reader_card": all(
            marker in chapter_7
            for marker in (
                "### 7.9.1 Transition-zone 判读卡：分支被进入，不等于每条 route 已验证",
                "gather 与 deposition 分别有自己的 buffer mask",
                "ledger 不应只报告一个“buffer particle count”",
                "route ledger 才说明每条 route",
            )
        ) and not chapter_7_project_path_markers and not chapter_7_stale_location_markers,
        "chapter_7_load_balance_validation_reader_card": all(
            marker in chapter_7
            for marker in (
                "### 7.8.1 修改 load balance 或 `RemakeLevel()` 后的验证卡：效率、迁移与物理量分开检查",
                "每个 subdomain 本身保持不变",
                "第一层：先确认 producer 有足够的 boxes、实际生成成本记录",
                "第二层：用正确的 consumer 判断映射效率",
                "第三层：把“提议”与“真正迁移的状态”分开",
                "第四层：按改动对象补上状态或物理 consumer",
                "不能写成“load balance 后的物理结果已经验证”",
            )
        ) and not chapter_7_project_path_markers and not chapter_7_stale_location_markers,
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
        ) and not chapter_8_project_path_markers and not chapter_8_project_narration_markers
        and not chapter_8_stale_location_markers,
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
        "chapter_8_validation_contract_reader_card": all(
            marker in chapter_8
            for marker in (
                "### 验证合同判读卡：相同的“通过”并不表示相同的正确性",
                "归一化时间积分 Poynting-flux 形状",
                "Python Poisson callback 是可单独运行的接口路径",
                "interior RMS relative error `< 6%`",
                "`phi[1:]`",
                "不能把一次 PASS 推广成“该应用已经验证”",
            )
        ) and not chapter_8_project_path_markers and not chapter_8_project_narration_markers,
        "chapter_8_restart_reader_card": all(
            marker in chapter_8
            for marker in (
                "### Checkpoint/restart 的读者合同：续跑一致性与跨布局比较不是同一问题",
                "同一 CTest 布局下",
                "不能从 `epsilon_f < 1e-12` 自动推出",
                "输出回归",
            )
        )
        and not chapter_8_project_path_markers
        and not chapter_8_project_narration_markers
        and not chapter_8_restart_record_markers,
        "chapter_8_diagnostics_validation_ladder_reader_card": all(
            marker in chapter_8
            for marker in (
                "### 8.14.3 修改诊断后的验证阶梯：先核 producer，再解释输出",
                "第一层：先确认调度与时间层真的到达",
                "第二层：改 compact reduced observable 时，以 full state 作 reference",
                "第三层：改 bin、轴标签或 openPMD reduced mesh 时，用解析谱而非文件形状验收",
                "第四层：改 sampling geometry、gather 或时间积分时，让 observable 匹配采样定义",
                "第五层：有跨步状态时，restart 与 checksum 只检查各自的生命周期",
                "不能把缺少 comparison 写成通过",
            )
        ) and not chapter_8_project_path_markers and not chapter_8_project_narration_markers,
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
        "chapter_2_first_run_reader_card": all(
            marker in chapter_2
            for marker in (
                "### 2.8.1 第一次运行的读者路线：构建、CTest 与手动分析各自回答什么",
                "-DWarpX_DIMS=1",
                "ctest --test-dir",
                "-N -R '^test_1d_langmuir_multi\\..*'",
                "零项不是一次通过的 Langmuir 验证",
                "test_1d_langmuir_multi.checksum",
                "warpx_used_inputs",
                "程序退出为零",
                "### 2.8.2 受控修改路线：一个命令行覆盖会改变哪一份证据",
                "原来注册的 `diags/diag1000080` 不会由此产生",
                "建立新合同",
            )
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
        "chapter_3_lifecycle_trace_reader_card": all(
            marker in chapter_3
            for marker in (
                "### 3.12.1 生命周期追踪卡：一项输入何时成为可解释的证据",
                "参数被读取。",
                "初始化已经越过记录点。",
                "参数实际限制外层循环。",
                "consumer 给出可支持的结论。",
                "不能统一归因成“参数无效”或“Langmuir 物理失败”",
            )
        ) and not chapter_3_project_narration_markers,
        "chapter_3_subcycling_validation_reader_card": all(
            marker in chapter_3
            for marker in (
                "### 3.11.3 AMR subcycling 修改后的验证卡：先分清时间层、source 和回归",
                "第一层：先确认这真的是受支持的两级分支",
                "第二层：把一个 coarse 步按 source 生命周期阅读",
                "第三层：正确解读官方测试的 consumer",
                "第四层：按改动对象补上缺失的比较",
                "不能写成“AMR subcycling 的物理正确性已经验证”",
            )
        ) and not chapter_3_project_narration_markers and not chapter_3_project_path_markers,
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
        ) and not chapter_1_project_path_markers,
        "chapter_1_electrostatic_model_validation_reader_card": all(
            marker in chapter_1
            for marker in (
                "### 1.5.1 模型选择与验证卡：Poisson 可解不等于完整电磁问题已被解决",
                "第一层：先判断问题是否仍需传播电磁自由度",
                "第二层：明确实际解的是什么",
                "第三层：用一个有解析 reference 的 producer 检查指定对象",
                "第四层：让 consumer 与所问问题一一对应",
                "Poisson 残差小，所以激光传播也正确",
            )
        ) and not chapter_1_project_path_markers,
        "chapter_1_thermal_plasma_energy_validation_reader_card": all(
            marker in chapter_1
            for marker in (
                "### 1.9.1 统计噪声与能量账本验证卡：能量漂移小不等于热平衡或低噪声",
                "第一层：先固定它实际产生了什么",
                "第二层：再核对 consumer 到底比较了什么",
                "第三层：明确这张账本没有测量什么",
                "第四层：修改后重新建立两本账",
                "原来的 `0.003` 已不再是自动有效的合同",
            )
        ) and not chapter_1_project_path_markers,
        "chapter_1_thermal_plasma_resolution_reader_card": all(
            marker in chapter_1
            for marker in (
                "### 1.10.1 尺度计算卡：能量回归通过不等于 Debye 屏蔽已分辨",
                "测试名和物理判据必须分开读",
                "先读这四个数各自回答的问题",
                "建立新的分辨率合同",
                "并不运行 WarpX，也不宣布某个通用的",
            )
        ) and not chapter_1_project_path_markers,
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
        and not chapter_3a_project_narration_markers
        and not chapter_3a_application_record_markers,
        "chapter_3a_initialization_two_contract_reader_card": all(
            marker in chapter_3a
            for marker in (
                "### 3A.13.1 初始化验证卡：分布统计和初始自场是两份合同",
                "合同 A：粒子分布。",
                "合同 B：初始自场。",
                "producer -> observable -> consumer 链",
                "不能合并成“初始化失败”",
            )
        ) and not chapter_3a_project_path_markers,
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
        )
        and not chapter_3a_application_record_markers,
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
        "baseline_read_and_current_incremental_review_are_recorded": all(
            marker in manual_spotcheck
            for marker in (
                "基线 262 页快照已完成连续阅读",
                "当前增量复核（273 页候选）",
                "| 1--6 |",
                "| 7--8 |",
                "| 219--254 |",
                "| 13--14 |",
                "| 15--16 |",
                "| 16--17 |",
                "| 30--31 |",
                "| 31--32 |",
                "| 33--34 |",
                "| 48--51 |",
                "| 75--77 |",
                "| 113--114 |",
                "| 172--173 |",
                "| 210--211 |",
                "| 226--227 |",
                "| 263--264 |",
                "| 260--262 |",
                "| 231 |",
                "| 236 |",
                "| 265 |",
                "| 271 |",
            )
        ),
    }
    incremental_review_recorded = checks["baseline_read_and_current_incremental_review_are_recorded"]
    result = {
        "contract": "reader-facing content audit",
        "checks": checks,
        "passed": all(checks.values()),
        "classification": (
            "READER_FACING_CORE_CHAPTERS_PASS_BASELINE_READ_INCREMENTAL_REVIEW_RECORDED"
            if incremental_review_recorded
            else "READER_FACING_CORE_CHAPTERS_PASS_BASELINE_READ_INCREMENTAL_REVIEW_OPEN"
        ),
        "scope": (
            "entry-point and learning-path audit; versioned evidence headings have been separated "
            "from core tutorial chapters; a 262-page baseline has a complete recorded manual read and "
            "the current 273-page candidate has recorded Chapter 1, Chapter 2, Chapter 3, Chapter 3A, Chapter 4, Chapter 5, Chapter 6, Chapter 7, Chapter 8, and Chapter 9 incremental reviews"
            if incremental_review_recorded
            else "entry-point and learning-path audit; versioned evidence headings have been separated from core tutorial chapters"
        ),
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
        "chapter_8_restart_record_markers": chapter_8_restart_record_markers,
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
        "chapter_3_project_narration_markers": chapter_3_project_narration_markers,
        "chapter_3a_stale_location_markers": chapter_3a_stale_location_markers,
        "chapter_3a_project_path_markers": chapter_3a_project_path_markers,
        "chapter_3a_project_narration_markers": chapter_3a_project_narration_markers,
        "chapter_3a_application_record_markers": chapter_3a_application_record_markers,
        "chapter_4_stale_location_markers": chapter_4_stale_location_markers,
        "chapter_5_opening_project_markers": chapter_5_opening_project_markers,
        "chapter_5_project_path_markers": chapter_5_project_path_markers,
        "chapter_5_project_narration_markers": chapter_5_project_narration_markers,
        "chapter_5_stale_location_markers": chapter_5_stale_location_markers,
        "chapter_6_opening_project_markers": chapter_6_opening_project_markers,
        "chapter_6_stale_location_markers": chapter_6_stale_location_markers,
        "open_items": ([] if incremental_review_recorded else [
            "需要人工通读术语、公式、代码上下文、章节过渡和练习",
        ]),
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
    if result["open_items"]:
        lines.extend(["", "## Open editorial work", ""])
        lines.extend(f"- {item}" for item in result["open_items"])
    else:
        lines.extend([
            "",
            "## Recorded Manual Review",
            "",
            "- A 262-page baseline has a complete recorded manual read; the current 273-page candidate has recorded Chapter 1, Chapter 2, Chapter 3, Chapter 3A, Chapter 4, Chapter 5, Chapter 6, Chapter 7, Chapter 8, and Chapter 9 incremental reviews. External-source and redistribution boundaries remain documented separately.",
        ])
    args.output_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
