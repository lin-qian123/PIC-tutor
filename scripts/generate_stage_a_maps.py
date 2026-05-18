#!/usr/bin/env python3
"""Generate Stage A planning maps for the PIC-tutor WarpX book.

The output files are intentionally Markdown-first because they are meant to be
reviewed and edited while writing the book. This script only reads the sibling
WarpX checkout.
"""

from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WARPX = (ROOT / "../warpx").resolve()
DOCS = ROOT / "docs"
BIB = ROOT / "bibliography" / "warpx-refs.bib"


TARGET_SOURCE_SUFFIXES = {
    ".H",
    ".cpp",
    ".py",
}
TARGET_SOURCE_NAMES = {
    "CMakeLists.txt",
    "Make.package",
    "Make.WarpX",
}


@dataclass(frozen=True)
class ModuleRule:
    prefix: str
    module: str
    physical_theme: str
    chapters: str
    depth: str


MODULE_RULES = [
    ModuleRule("Source/main.cpp", "程序入口", "程序生命周期 / AMReX 初始化", "10", "逐行"),
    ModuleRule("Source/WarpX.H", "WarpX 主类", "全局状态 / 模块所有权", "11", "逐块"),
    ModuleRule("Source/WarpX.cpp", "WarpX 主类", "全局状态 / 初始化/析构", "11", "逐块"),
    ModuleRule("Source/Evolve/", "时间推进", "PIC 主循环 / 时间层 / subcycling", "12-16", "逐行"),
    ModuleRule("Source/Particles/Pusher/", "粒子推进器", "Lorentz 力 / Boris/Vay/Higuera-Cary", "22-26", "逐行"),
    ModuleRule("Source/Particles/Gather/", "场插值", "shape factor / gather / external fields", "27", "逐行"),
    ModuleRule("Source/Particles/Deposition/", "沉积", "charge/current/mass/temperature deposition", "36-45", "逐行"),
    ModuleRule("Source/Particles/Collision/", "碰撞", "MCC / binary collision / stopping / decay", "90-94", "逐块"),
    ModuleRule("Source/Particles/ElementaryProcess/", "基本过程", "ionization / QED photon emission / pair generation", "95-99", "逐块"),
    ModuleRule("Source/Particles/ParticleCreation/", "粒子初始化", "species sampling / density / momentum", "21, 83-84", "逐块"),
    ModuleRule("Source/Particles/Resampling/", "粒子重采样", "thinning / leveling / weight conservation", "34", "逐块"),
    ModuleRule("Source/Particles/Sorting/", "粒子排序", "load balance / deposition locality", "33, 77", "逐块"),
    ModuleRule("Source/Particles/ParticleThermalizer/", "粒子热边界", "thermal boundary / rethermalization", "29, 35", "逐块"),
    ModuleRule("Source/Particles/Filter/", "粒子过滤", "particle selection / filtering functors", "35", "逐块"),
    ModuleRule("Source/Particles/", "粒子系统", "species containers / boundaries / photon / laser particles", "17-35", "逐块"),
    ModuleRule("Source/FieldSolver/FiniteDifferenceSolver/HybridPICModel/", "Hybrid PIC 场求解", "Ohm 定律 / kinetic ion + fluid electron", "61, 104", "逐行"),
    ModuleRule("Source/FieldSolver/FiniteDifferenceSolver/MacroscopicProperties/", "宏观介质", "conductivity / epsilon / mu response", "51", "逐块"),
    ModuleRule("Source/FieldSolver/FiniteDifferenceSolver/FiniteDifferenceAlgorithms/", "FDTD 算法模板", "Yee / CKC / nodal / cylindrical / spherical", "50", "逐行"),
    ModuleRule("Source/FieldSolver/FiniteDifferenceSolver/", "FDTD 场求解", "Maxwell FDTD / PML / cleaning", "47-52", "逐行"),
    ModuleRule("Source/FieldSolver/SpectralSolver/", "谱场求解", "PSATD / Galilean / Hankel / FFT", "53-56", "逐行"),
    ModuleRule("Source/FieldSolver/ElectrostaticSolvers/", "静电求解", "Poisson / electrostatic PIC", "57", "逐块"),
    ModuleRule("Source/FieldSolver/MagnetostaticSolver/", "磁静态求解", "vector potential / magnetostatic fields", "58", "逐块"),
    ModuleRule("Source/FieldSolver/ImplicitSolvers/", "隐式求解", "theta/semi implicit / JFNK / Picard", "59", "逐块"),
    ModuleRule("Source/FieldSolver/", "场求解", "EM/ES/hybrid/implicit/QED field push", "46-62", "逐块"),
    ModuleRule("Source/BoundaryConditions/", "边界条件", "PML / PEC / PMC / Silver-Mueller / field BC", "63-67", "逐行"),
    ModuleRule("Source/EmbeddedBoundary/", "嵌入边界", "EB geometry / scraping / face extension", "68-70", "逐块"),
    ModuleRule("Source/Parallelization/", "并行与 AMR", "guard cells / communication / regrid", "71-77", "逐块"),
    ModuleRule("Source/Filter/", "滤波器", "bilinear / NCI Godfrey filter", "45, 53-56", "逐块"),
    ModuleRule("Source/Initialization/DivCleaner/", "散度清理初始化", "projection / div cleaner initialization", "86", "逐块"),
    ModuleRule("Source/Initialization/", "初始化", "geometry / species / profiles / external fields", "80-86", "逐块"),
    ModuleRule("Source/Laser/", "激光", "laser profiles / antenna / file input", "87-88", "逐块"),
    ModuleRule("Source/Fluids/", "流体模型", "cold fluid / MUSCL-Hancock / hybrid coupling", "101-104", "逐块"),
    ModuleRule("Source/Diagnostics/", "诊断与 I/O", "full/reduced/openPMD/BTD/checkpoint", "107-113", "逐块"),
    ModuleRule("Source/AcceleratorLattice/", "加速器晶格", "beamline elements / lattice finder", "105-106", "逐块"),
    ModuleRule("Source/NonlinearSolvers/", "非线性/线性求解器", "Newton/Picard/GMRES/PETSc/preconditioner", "59-60", "逐块"),
    ModuleRule("Source/Python/", "Python 接口", "callbacks / pybind / PICMI access", "114-116", "逐块"),
    ModuleRule("Source/Utils/", "工具与算法选择", "constants / moving window / parser helpers", "8, 80, 89", "逐块"),
    ModuleRule("Source/ablastr/", "ablastr 支撑层", "fields / particles / FFT / profiler / warnings", "71, 78, 107", "文件级+关键内核"),
    ModuleRule("Source/", "其他源码", "待进一步分类", "待定", "文件级"),
]


TOPIC_KEYWORDS = [
    ("beam_beam", "beam-beam collision / luminosity", "105, 125"),
    ("capacitive_discharge", "capacitive discharge / PIC-MCC", "92, 125"),
    ("free_electron_laser", "free electron laser", "105, 125"),
    ("ion_beam_extraction", "ion beam extraction", "105, 125"),
    ("langmuir", "Langmuir wave / plasma oscillation", "9, 36-49, 124, 125"),
    ("uniform_plasma", "uniform plasma / noise / performance", "77, 107, 125"),
    ("particle_pusher", "particle pusher", "22-26"),
    ("single_particle", "single-particle orbit", "22-26"),
    ("larmor", "charged particle gyro-motion", "22-26"),
    ("vay_deposition", "Vay current deposition", "42"),
    ("collision", "collisions", "90-94"),
    ("mcc", "Monte Carlo collisions", "92"),
    ("ionization", "ionization", "95"),
    ("qed", "QED processes", "96-99"),
    ("breit_wheeler", "Breit-Wheeler pair generation", "97"),
    ("compton", "Compton / photon processes", "96-100"),
    ("pml", "PML", "52, 65"),
    ("silver_mueller", "Silver-Mueller boundary", "63-67"),
    ("pec", "PEC / conducting boundary", "63-67"),
    ("boundary", "boundary condition", "63-70"),
    ("embedded", "embedded boundary", "68-70"),
    ("electrostatic", "electrostatic / Poisson", "57"),
    ("implicit", "implicit solver", "59-60"),
    ("psatd", "PSATD / spectral solver", "53-56"),
    ("nci", "numerical Cherenkov instability", "53-56"),
    ("subcycling", "AMR subcycling", "15, 72"),
    ("mr", "mesh refinement", "71-76"),
    ("ohm_solver", "hybrid PIC / Ohm solver", "61, 104"),
    ("fluid", "fluid model", "101-104"),
    ("laser", "laser injection / LPI", "87-89, 125"),
    ("plasma_acceleration", "LWFA/PWFA", "88-89, 125"),
    ("laser_ion", "laser ion acceleration", "125"),
    ("plasma_mirror", "plasma mirror", "125"),
    ("accelerator_lattice", "accelerator lattice", "105-106"),
    ("reduced_diags", "reduced diagnostics", "110"),
    ("restart", "checkpoint/restart", "112"),
    ("python", "Python API / callbacks", "114-116"),
    ("openpmd", "openPMD output", "111"),
]


LITERATURE_TOPICS = [
    ("Yee|finite-difference|FDTD", "FDTD / Yee Maxwell solver", "46-50"),
    ("Boris|particle pusher|particle trajector", "particle pusher", "22-26"),
    ("Higuera", "Higuera-Cary pusher", "25"),
    ("Vay", "Vay pusher / boosted frame / AMR / PSATD", "24, 42, 55, 72"),
    ("Villasenor|Buneman", "charge-conserving current deposition", "40"),
    ("Esirkepov", "Esirkepov current deposition", "41"),
    ("Berenger|PML|perfectly matched", "PML", "52, 65"),
    ("Godfrey|Cherenkov|NCI", "NCI / spectral stability", "53-56"),
    ("Lehe|PSATD|pseudo-spectral|spectral", "PSATD", "53-56"),
    ("Hockney|Eastwood", "particle-mesh foundations", "6, 36"),
    ("Birdsall|Langdon|PIC-MCC", "PIC foundations / collisions", "1-7, 90-92"),
    ("Dawson", "PIC foundations / plasma simulation history", "1-7"),
    ("AMR|mesh refinement|Colella", "AMR", "71-76"),
    ("QED|Breit|Wheeler|synchrotron|Schwinger", "QED", "96-100"),
    ("openPMD", "openPMD", "111"),
    ("AMReX|Exascale|GPU|load balancing", "HPC / AMReX / performance", "71-79, 121-123"),
    ("hybrid|Ohm|reconnection|fluid", "hybrid/fluid", "101-104"),
    ("laser|wakefield|LWFA|plasma acceleration", "laser/plasma acceleration", "87-89, 125"),
]


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def warpx_rel(path: Path) -> str:
    return path.relative_to(WARPX).as_posix()


def target_source_files() -> list[Path]:
    files: list[Path] = []
    for path in (WARPX / "Source").rglob("*"):
        if not path.is_file():
            continue
        if path.name in TARGET_SOURCE_NAMES or path.suffix in TARGET_SOURCE_SUFFIXES:
            files.append(path)
    return sorted(files)


def classify_module(warp_rel: str) -> ModuleRule:
    for rule in MODULE_RULES:
        if warp_rel == rule.prefix.rstrip("/") or warp_rel.startswith(rule.prefix):
            return rule
    return MODULE_RULES[-1]


def extract_symbols(path: Path) -> str:
    if path.suffix not in {".H", ".cpp", ".py"}:
        return ""
    try:
        text = path.read_text(errors="ignore")
    except UnicodeDecodeError:
        return ""
    patterns = [
        r"\b(?:class|struct|enum)\s+([A-Za-z_][A-Za-z0-9_]*)",
        r"^\s*(?:[A-Za-z_][A-Za-z0-9_:<>,\s*&~]+)\s+([A-Za-z_][A-Za-z0-9_:]*)\s*\([^;]*\)\s*(?:\{|$)",
        r"^\s*def\s+([A-Za-z_][A-Za-z0-9_]*)\s*\(",
    ]
    found: list[str] = []
    for pattern in patterns:
        for match in re.finditer(pattern, text, re.MULTILINE):
            name = match.group(1)
            if name not in found and name not in {"if", "for", "while", "switch"}:
                found.append(name)
            if len(found) >= 8:
                break
        if len(found) >= 8:
            break
    return ", ".join(found[:8])


def write_module_inventory() -> None:
    files = target_source_files()
    counts = Counter(classify_module(warpx_rel(path)).module for path in files)
    lines = [
        "# WarpX 源码模块索引",
        "",
        "生成来源：`../warpx/Source`",
        "",
        f"- 源码状态：`{get_git_state()}`",
        f"- 目标文件数：{len(files)}",
        "- 阅读状态含义：`未读`、`已定位`、`已做笔记`、`已入正文`、`已验证`。",
        "",
        "## 模块统计",
        "",
        "| 模块 | 文件数 |",
        "|---|---:|",
    ]
    for module, count in sorted(counts.items()):
        lines.append(f"| {module} | {count} |")
    lines += [
        "",
        "## 文件清单",
        "",
        "| 文件 | 模块 | 物理/算法主题 | 计划章节 | 讲解深度 | 初步符号 | 阅读状态 |",
        "|---|---|---|---|---|---|---|",
    ]
    for path in files:
        wrel = warpx_rel(path)
        rule = classify_module(wrel)
        symbols = extract_symbols(path).replace("|", "\\|")
        lines.append(
            f"| `{wrel}` | {rule.module} | {rule.physical_theme} | {rule.chapters} | {rule.depth} | {symbols} | 未读 |"
        )
    (DOCS / "module-inventory.md").write_text("\n".join(lines) + "\n")


def parse_parameters() -> list[dict[str, str]]:
    path = WARPX / "Docs/source/usage/parameters.rst"
    text = path.read_text(errors="ignore").splitlines()
    params: list[dict[str, str]] = []
    i = 0
    anchor = ""
    while i < len(text):
        line = text[i]
        if line.startswith(".. _"):
            anchor = line.strip()
        match = re.match(r"^\.\. pp:param::\s+(.+?)\s*$", line)
        if not match:
            i += 1
            continue
        name = match.group(1).strip()
        start = i + 1
        block: list[str] = []
        i += 1
        while i < len(text) and not re.match(r"^\.\. pp:param::\s+", text[i]):
            if text[i].startswith(".. _"):
                break
            block.append(text[i])
            i += 1
        params.append(parse_param_block(name, block, start, anchor))
    return params


def parse_param_block(name: str, block: list[str], line_no: int, anchor: str) -> dict[str, str]:
    ptype = ""
    default = ""
    optional = ""
    summary_lines: list[str] = []
    for raw in block:
        stripped = raw.strip()
        if stripped.startswith(":type:"):
            ptype = stripped.replace(":type:", "", 1).strip()
        elif stripped.startswith(":default:"):
            default = stripped.replace(":default:", "", 1).strip()
        elif stripped.startswith(":optional:"):
            optional = "yes"
        elif stripped and not stripped.startswith(":"):
            if not stripped.startswith(".. ") and len(summary_lines) < 2:
                summary_lines.append(re.sub(r"\s+", " ", stripped))
    return {
        "name": name,
        "line": str(line_no),
        "anchor": anchor,
        "type": ptype,
        "default": default,
        "optional": optional,
        "summary": " ".join(summary_lines),
    }


def source_text_index() -> list[tuple[str, str]]:
    indexed: list[tuple[str, str]] = []
    for path in target_source_files():
        if path.suffix not in {".H", ".cpp", ".py"}:
            continue
        try:
            text = path.read_text(errors="ignore")
        except OSError:
            continue
        indexed.append((warpx_rel(path), text))
    return indexed


def probable_chapters_for_param(name: str) -> str:
    lowered = name.lower()
    if lowered.startswith("algo."):
        if "deposition" in lowered:
            return "36-45"
        if "field_gather" in lowered or "particle_shape" in lowered:
            return "27, 36"
        if "evolve" in lowered:
            return "12-16, 59"
        return "80"
    if lowered.startswith("boundary."):
        return "63-67"
    if lowered.startswith("amr.") or lowered.startswith("geometry."):
        return "71-76, 80-82"
    if lowered.startswith("warpx."):
        if "cfl" in lowered or "dt" in lowered or "max_step" in lowered:
            return "16"
        if "pml" in lowered:
            return "52, 65"
        if "diagnostic" in lowered or "plot" in lowered or "checkpoint" in lowered:
            return "107-113"
        if "boost" in lowered or "moving" in lowered:
            return "89"
        return "80-82"
    if lowered.startswith("psatd."):
        return "53-56"
    if lowered.startswith("particles.") or "<species>" in lowered or "species" in lowered:
        return "17-35, 83-84"
    if lowered.startswith("laser") or ".laser" in lowered:
        return "87-88"
    if lowered.startswith("qed") or "qed" in lowered:
        return "96-100"
    if lowered.startswith("collisions") or "collision" in lowered:
        return "90-94"
    if lowered.startswith("diagnostics") or lowered.startswith("diag"):
        return "107-113"
    return "待定"


def find_source_hits(param: str, index: list[tuple[str, str]]) -> str:
    if any(ch in param for ch in "<>{}[]/,"):
        return ""
    literal = param.split()[0]
    hits: list[str] = []
    tail = literal.split(".")[-1]
    candidates = [literal]
    if tail != literal:
        candidates.append(f'"{tail}"')
        candidates.append(f'"{literal}"')
    for rel_path, text in index:
        if any(candidate in text for candidate in candidates):
            hits.append(rel_path)
        if len(hits) >= 4:
            break
    return ", ".join(f"`{hit}`" for hit in hits)


def write_parameter_map() -> None:
    params = parse_parameters()
    index = source_text_index()
    lines = [
        "# WarpX 参数映射",
        "",
        "生成来源：`../warpx/Docs/source/usage/parameters.rst` 与 `../warpx/Source` 字符串检索。",
        "",
        f"- 参数条目数：{len(params)}",
        "- 源码命中是自动文本检索结果，只作为起点；正式章节必须重新读取解析函数确认。",
        "",
        "| 参数 | 文档行 | 类型 | 默认值 | 可选 | 计划章节 | 初步源码命中 | 摘要 |",
        "|---|---:|---|---|---|---|---|---|",
    ]
    for param in params:
        name = param["name"].replace("|", "\\|")
        ptype = param["type"].replace("|", "\\|")
        default = param["default"].replace("|", "\\|")
        summary = param["summary"].replace("|", "\\|")
        hits = find_source_hits(param["name"], index).replace("|", "\\|")
        chapters = probable_chapters_for_param(param["name"])
        lines.append(
            f"| `{name}` | {param['line']} | {ptype} | {default} | {param['optional']} | {chapters} | {hits} | {summary} |"
        )
    (DOCS / "parameter-map.md").write_text("\n".join(lines) + "\n")


def classify_topic(text: str) -> tuple[str, str]:
    lowered = text.lower()
    for key, topic, chapters in TOPIC_KEYWORDS:
        if key in lowered:
            return topic, chapters
    return "general / to classify", "待定"


def write_example_regression_map() -> None:
    example_files = sorted(
        path for path in (WARPX / "Examples").rglob("*")
        if path.is_file() and (path.name.startswith("inputs") or path.suffix in {".py", ".ipynb"})
    )
    benchmark_files = sorted((WARPX / "Regression/Checksum/benchmarks_json").glob("*.json"))
    lines = [
        "# Examples 与 Regression 映射",
        "",
        "生成来源：`../warpx/Examples` 与 `../warpx/Regression/Checksum/benchmarks_json`。",
        "",
        f"- Example 输入/脚本条目数：{len(example_files)}",
        f"- Regression benchmark JSON 条目数：{len(benchmark_files)}",
        "",
        "## Examples",
        "",
        "| 路径 | 初步主题 | 计划章节 | 验证用途 |",
        "|---|---|---|---|",
    ]
    for path in example_files:
        wrel = warpx_rel(path)
        topic, chapters = classify_topic(wrel)
        lines.append(f"| `{wrel}` | {topic} | {chapters} | 待读取输入文件并记录物理检查量 |")
    lines += [
        "",
        "## Regression Checksum Benchmarks",
        "",
        "| Benchmark | 初步主题 | 计划章节 | 验证用途 |",
        "|---|---|---|---|",
    ]
    for path in benchmark_files:
        topic, chapters = classify_topic(path.stem)
        lines.append(f"| `{path.name}` | {topic} | {chapters} | checksum 基线；需反查对应 inputs 和分析脚本 |")
    (DOCS / "example-regression-map.md").write_text("\n".join(lines) + "\n")


def parse_bib_entries() -> list[dict[str, str]]:
    if not BIB.exists():
        return []
    text = BIB.read_text(errors="ignore")
    entries = re.split(r"\n(?=@)", text)
    parsed: list[dict[str, str]] = []
    for entry in entries:
        header = re.match(r"@(\w+)\s*\{\s*([^,\s]+)", entry)
        if not header:
            continue
        fields = {"type": header.group(1), "key": header.group(2)}
        for field in ["title", "author", "year", "doi", "journal", "booktitle"]:
            match = re.search(field + r"\s*=\s*[\{\"](.+?)[\}\"]\s*,?\s*(?=\n\w+\s*=|\n\}|$)", entry, re.IGNORECASE | re.DOTALL)
            if match:
                value = re.sub(r"\s+", " ", match.group(1)).strip()
                value = value.replace("{", "").replace("}", "")
                fields[field] = value
        parsed.append(fields)
    return parsed


def classify_literature(entry: dict[str, str]) -> tuple[str, str]:
    haystack = " ".join(entry.get(k, "") for k in ["key", "title", "author", "journal", "booktitle"])
    for pattern, topic, chapters in LITERATURE_TOPICS:
        if re.search(pattern, haystack, re.IGNORECASE):
            return topic, chapters
    return "待分类", "待定"


def write_literature_map() -> None:
    entries = parse_bib_entries()
    pdfs = sorted((ROOT / "references").rglob("*.pdf"))
    topic_counts = Counter()
    rows: list[str] = []
    for entry in entries:
        topic, chapters = classify_literature(entry)
        topic_counts[topic] += 1
        title = entry.get("title", "").replace("|", "\\|")
        author = entry.get("author", "").replace("|", "\\|")
        year = entry.get("year", "")
        doi = entry.get("doi", "")
        rows.append(
            f"| `{entry['key']}` | {topic} | {chapters} | {year} | {author[:120]} | {title[:180]} | {doi} |"
        )
    lines = [
        "# 文献映射",
        "",
        "生成来源：`bibliography/warpx-refs.bib` 与 `references/` PDF 文件。",
        "",
        f"- BibTeX 条目数：{len(entries)}",
        f"- 本地 PDF 数：{len(pdfs)}",
        "- 分类为自动初筛；正式章节必须阅读论文或官方文档后再引用。",
        "",
        "## 主题统计",
        "",
        "| 主题 | 条目数 |",
        "|---|---:|",
    ]
    for topic, count in sorted(topic_counts.items()):
        lines.append(f"| {topic} | {count} |")
    lines += [
        "",
        "## BibTeX 条目映射",
        "",
        "| Key | 初步主题 | 计划章节 | 年份 | 作者 | 标题 | DOI |",
        "|---|---|---|---|---|---|---|",
        *rows,
        "",
        "## 本地 PDF 清单",
        "",
        "| PDF | 初步主题 | 计划章节 | MinerU 状态 |",
        "|---|---|---|---|",
    ]
    for pdf in pdfs:
        topic, chapters = classify_literature({"key": pdf.name, "title": pdf.name})
        md_candidates = list(pdf.parent.glob("*.md"))
        state = "已有 Markdown" if md_candidates else "待 MinerU"
        lines.append(f"| `{rel(pdf)}` | {topic} | {chapters} | {state} |")
    (DOCS / "literature-map.md").write_text("\n".join(lines) + "\n")


def get_git_state() -> str:
    import subprocess

    try:
        branch = subprocess.check_output(["git", "-C", str(WARPX), "rev-parse", "--abbrev-ref", "HEAD"], text=True).strip()
        commit = subprocess.check_output(["git", "-C", str(WARPX), "rev-parse", "HEAD"], text=True).strip()
        return f"{branch} / {commit}"
    except Exception:
        return "unknown"


def main() -> None:
    DOCS.mkdir(exist_ok=True)
    write_module_inventory()
    write_parameter_map()
    write_example_regression_map()
    write_literature_map()
    print("Generated:")
    for name in [
        "module-inventory.md",
        "parameter-map.md",
        "example-regression-map.md",
        "literature-map.md",
    ]:
        path = DOCS / name
        print(f"- {path.relative_to(ROOT)} ({path.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
