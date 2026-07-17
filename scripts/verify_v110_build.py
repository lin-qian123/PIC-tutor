#!/usr/bin/env python
"""Verify the v0.110 Markdown/HTML/PDF artifact contract after building."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

from pypdf import PdfReader

from audit_public_release_paths import inspect


ROOT = Path(__file__).resolve().parents[1]
SOURCE_CHAPTERS = sorted((ROOT / "manuscript" / "chapters").glob("*.md"))
MERGED_MARKDOWN = ROOT / "dist" / "pic-tutor-v0.110.md"
HTML = ROOT / "dist" / "pic-tutor-v0.110.html"
PDF = ROOT / "dist" / "pic-tutor-v0.110.pdf"
MANUAL_SPOTCHECK = ROOT / "docs" / "manual-editorial-spotcheck-v0.110.md"
# Reader-facing edits removed obsolete process narration; the verified v0.110 layout is 269 pages.
EXPECTED_PDF_PAGES = 269


def image_links(text: str) -> list[str]:
    return re.findall(r"!\[\]\(([^)]+figures/[^)]+)\)", text)


def chapter_subheading_numbers(path: Path, chapter: str) -> list[tuple[int, ...]]:
    pattern = re.compile(rf"^### ({re.escape(chapter)}\.\d+\.\d+)\b", re.MULTILINE)
    return [tuple(int(part) for part in match.split(".")) for match in pattern.findall(path.read_text(encoding="utf-8"))]


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
    chapter_5_numbers = chapter_subheading_numbers(
        ROOT / "manuscript" / "chapters" / "05-deposition-shapes.md", "5"
    )
    chapter_6_numbers = chapter_subheading_numbers(
        ROOT / "manuscript" / "chapters" / "06-field-solvers.md", "6"
    )
    chapter_3a_numbers = [
        int(number)
        for number in re.findall(
            r"^## 3A\.(\d+)\b",
            (ROOT / "manuscript" / "chapters" / "03a-warpx-initialization.md").read_text(encoding="utf-8"),
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
        "chapter_5_subheading_order": chapter_5_numbers == sorted(chapter_5_numbers)
        and len(chapter_5_numbers) == len(set(chapter_5_numbers)),
        "chapter_6_subheading_order": chapter_6_numbers == sorted(chapter_6_numbers)
        and len(chapter_6_numbers) == len(set(chapter_6_numbers)),
        "chapter_3a_section_order": chapter_3a_numbers == list(range(1, 17)),
        "chapter_9_exercises": all(
            marker in source
            for marker in (
                "## 9.10 练习与复核",
                "### 9.10.1 证据层分类练习",
                "### 9.10.2 证据边界复核练习",
                "### 9.10.3 延伸阅读排序练习",
            )
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
        "chapter_8_source_contract_heading": "## 8.14 本章正文与源码同步合同" in source
        and "### 8.14.1 本章正文与源码同步合同" not in source,
        "chapter_8_minimal_diagnostics_section": "### 8.14.1 reduced diagnostics 最小输入合同" in source,
        "chapter_5_geometry_order_gap_register": all(
            marker in source
            for marker in (
                "### 5.14.2 覆盖范围与已知空白",
                "negative-space contract",
                "RZ 默认 axis correction 下的 charge residual",
                "跨 geometry/shape 的正式收敛阶",
                "Vay 官方 wiring",
                "SOURCE_REGRESSION_WIRING_PARTIAL_RUNTIME_FAMILY",
                "RUNTIME_SINGLE_RANK_OFFICIAL_ANALYSIS_PASS_2D_3D",
                "RUNTIME_SINGLE_RANK_VAY_SHAPE_FAMILY_PASS_2D_3D",
                "RUNTIME_OFFICIAL_CMAKE_SCALE_2RANK_ANALYSIS_PASS_2D_3D",
                "RUNTIME_2RANK_VAY_SHAPE_FAMILY_PASS_2D_3D_CASE_LOCAL",
                "SOURCE_GUARD_AMR_RUNTIME_INTENTIONALLY_REJECTED",
            )
        ),
        "esirkepov_publication_boundary_contract": all(
            marker in source
            for marker in (
                "发表版缺口审计契约",
                "PREPRINT_FORMULA_SOURCE_RUNTIME_PUBLISHER_BOUNDARY_EXPLICIT",
                "publisher-PDF line-by-line compare 仍未完成",
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
                "63-esirkepov-publisher-abstract-compare.md",
                "publication-metadata + indexed-abstract verified",
                "PUBLISHER_METADATA_ABSTRACT_VERIFIED_PREPRINT_SOURCE_RUNTIME_PDF_MISSING",
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
                "## 9.8 成书的已知证据边界",
                "两条 publisher access、三条 runtime/source boundary",
                "formal numerical order",
                "缺口表的内部一致性检查",
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
