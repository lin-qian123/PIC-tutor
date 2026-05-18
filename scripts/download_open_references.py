#!/usr/bin/env python3
"""Download legally available open PDFs for the PIC-tutor reference library.

The script is intentionally conservative: it only downloads direct PDF URLs,
arXiv PDFs, or open-access URLs reported by OpenAlex. Paywalled or ambiguous
book/article records are kept in the manifest without a downloaded PDF.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass, asdict
from pathlib import Path


OPENALEX_MAILTO = os.environ.get("OPENALEX_MAILTO", "pic-tutor@example.local")

CATEGORIES = [
    ("01_reviews_surveys", [
        "review", "overview", "fundamentals", "modeling of relativistic plasmas",
        "methods in astrophysics", "survey", "modern", "state of the art"
    ]),
    ("02_books_lecture_notes", [
        "book", "lecture", "notes", "textbook", "course", "introduction"
    ]),
    ("03_pic_foundations", [
        "particle-in-cell", "particle in cell", "pic", "macroparticle",
        "vlasov", "plasma simulation", "computer simulation"
    ]),
    ("04_particle_pushers_deposition_shapes", [
        "boris", "vay", "higuera", "cary", "esirkepov", "deposition",
        "current", "shape factor", "charge conserving", "villasenor"
    ]),
    ("05_field_solvers_fdtd_psatd_poisson", [
        "yee", "fdtd", "psatd", "pseudo-spectral", "poisson", "maxwell",
        "spectral", "galilean", "solver"
    ]),
    ("06_stability_filtering_nci", [
        "numerical cherenkov", "nci", "instability", "filter", "smoothing",
        "dispersion", "finite-grid", "aliasing"
    ]),
    ("07_amr_parallel_hpc_gpu", [
        "amr", "adaptive mesh", "mesh refinement", "gpu", "exascale",
        "load balancing", "parallel", "scaling", "summit", "frontier"
    ]),
    ("08_boundaries_pml_geometry", [
        "pml", "perfectly matched", "boundary", "embedded boundary",
        "silver-mueller", "pec", "pmc", "geometry"
    ]),
    ("09_multiphysics_collisions_ionization_qed", [
        "collision", "coulomb", "ionization", "qed", "breit", "wheeler",
        "compton", "bremsstrahlung", "fusion", "adk"
    ]),
    ("10_applications_laser_plasma_acceleration", [
        "laser", "wakefield", "lwfa", "pwfa", "accelerator", "acceleration",
        "beam", "plasma-based", "ion acceleration", "free electron laser"
    ]),
    ("11_codes_ecosystem_standards", [
        "warpx", "amrex", "picsar", "openpmd", "picmi", "smilei",
        "vpic", "osiris", "epoch", "picon", "fbpic", "hipace", "psc"
    ]),
    ("12_hybrid_fluid_models", [
        "hybrid", "fluid-kinetic", "fluid kinetic", "fluid electron",
        "kinetic-fluid", "kinetic fluid", "ohm"
    ]),
    ("13_theses_dissertations", [
        "thesis", "doctoral", "dissertation", "algorithms for plasma simulations"
    ]),
    ("14_general_numerical_methods", [
        "eno", "weno", "shock-capturing", "finite volume", "finite element",
        "runge-kutta", "numerical method"
    ]),
]

CURATED_SEEDS = [
    {
        "key": "WarpXDocsLatest",
        "title": "WarpX Documentation PDF",
        "category": "11_codes_ecosystem_standards",
        "pdf_url": "https://readthedocs.org/projects/warpx/downloads/pdf/latest/",
        "source": "WarpX Read the Docs",
    },
    {
        "key": "PICMethodsAstrophysics2021",
        "title": "PIC methods in astrophysics: simulations of relativistic jets and kinetic physics in astrophysical systems",
        "category": "01_reviews_surveys",
        "doi": "10.1007/s41115-021-00012-0",
        "pdf_url": "https://link.springer.com/content/pdf/10.1007/s41115-021-00012-0.pdf",
        "source": "Springer Open Access",
    },
    {
        "key": "PSC2013",
        "title": "The Plasma Simulation Code: A modern particle-in-cell code with load-balancing and GPU support",
        "category": "11_codes_ecosystem_standards",
        "arxiv": "1310.7866",
        "pdf_url": "https://arxiv.org/pdf/1310.7866",
        "source": "arXiv",
    },
    {
        "key": "Smilei2017",
        "title": "SMILEI: a collaborative, open-source, multi-purpose particle-in-cell code for plasma simulation",
        "category": "11_codes_ecosystem_standards",
        "arxiv": "1702.05128",
        "pdf_url": "https://arxiv.org/pdf/1702.05128",
        "source": "arXiv",
    },
    {
        "key": "MLAcceleratedPIC2021",
        "title": "Machine learning accelerated particle-in-cell plasma simulations",
        "category": "06_stability_filtering_nci",
        "arxiv": "2110.12444",
        "pdf_url": "https://arxiv.org/pdf/2110.12444",
        "source": "arXiv",
    },
    {
        "key": "PICXeonPhi2015",
        "title": "Particle-in-Cell Laser-Plasma Simulation on Xeon Phi Coprocessors",
        "category": "07_amr_parallel_hpc_gpu",
        "arxiv": "1505.07271",
        "pdf_url": "https://arxiv.org/pdf/1505.07271",
        "source": "arXiv",
    },
    {
        "key": "WarpXGPU2021_eScholarship",
        "title": "Porting WarpX to GPU-accelerated platforms",
        "category": "07_amr_parallel_hpc_gpu",
        "doi": "10.1016/j.parco.2021.102833",
        "pdf_url": "https://escholarship.org/content/qt4f28s6b2/qt4f28s6b2.pdf",
        "source": "eScholarship open access",
    },
    {
        "key": "WarpXHPCBestPractices",
        "title": "Our Road to Exascale: WarpX",
        "category": "07_amr_parallel_hpc_gpu",
        "pdf_url": "https://ideas-productivity.org/assets/artifacts/hpcbp/hpcbp-072-warpx.pdf",
        "source": "IDEAS Productivity",
    },
    {
        "key": "WarpXSemiImplicitPosterSC24",
        "title": "New Semi-Implicit Electrostatic Particle-In-Cell Method to Extend Scope of the Exascale WarpX Code",
        "category": "05_field_solvers_fdtd_psatd_poisson",
        "pdf_url": "https://sc24.supercomputing.org/proceedings/poster/poster_files/post233s2-file2.pdf",
        "source": "SC24 proceedings poster",
    },
    {
        "key": "FiniteGridEnergyConservingPIC2019",
        "title": "Finite spatial-grid effects in energy-conserving particle-in-cell algorithms",
        "category": "06_stability_filtering_nci",
        "doi": "10.48550/arXiv.1910.10833",
        "arxiv": "1910.10833",
        "pdf_url": "https://arxiv.org/pdf/1910.10833",
        "source": "arXiv",
    },
    {
        "key": "PICShearedExpandingEscapingAstro2026",
        "title": "Particle-In-Cell Methods for Simulations of Sheared, Expanding, or Escaping Astrophysical Plasma",
        "category": "01_reviews_surveys",
        "arxiv": "2602.15939",
        "pdf_url": "https://arxiv.org/pdf/2602.15939",
        "source": "arXiv",
    },
    {
        "key": "FullyKineticPICFusionReview2024",
        "title": "Recent development of fully kinetic particle-in-cell method and its application to fusion plasma instability study",
        "category": "01_reviews_surveys",
        "doi": "10.3389/fphy.2024.1340736",
        "pdf_url": "https://public-pages-files-2025.frontiersin.org/journals/physics/articles/10.3389/fphy.2024.1340736/pdf",
        "source": "Frontiers open access",
    },
    {
        "key": "PICSimulationNotesYoujunHu2019",
        "title": "Particle In Cell (PIC) simulation",
        "category": "02_books_lecture_notes",
        "pdf_url": "https://youjunhu.github.io/research_notes/particle_simulation/particle_simulation.pdf",
        "source": "Author lecture notes",
    },
    {
        "key": "ParticleInCellAlgorithmsHeterogeneousArchitectures2016",
        "title": "Particle-in-cell algorithms for plasma simulations on heterogeneous architectures",
        "category": "13_theses_dissertations",
        "pdf_url": "https://upcommons.upc.edu/bitstreams/2a425370-c9c8-4396-a94d-4b81300208e0/download",
        "source": "UPC open thesis",
    },
    {
        "key": "PlasmaPropulsionSimulationUsingParticles2023",
        "title": "Plasma propulsion simulation using particles",
        "category": "01_reviews_surveys",
        "arxiv": "2304.05103",
        "pdf_url": "https://arxiv.org/pdf/2304.05103",
        "source": "arXiv",
    },
    {
        "key": "PICRelativisticBeamsPlasmasReview2014",
        "title": "Review and Recent Advances in PIC Modeling of Relativistic Beams and Plasmas",
        "category": "01_reviews_surveys",
        "arxiv": "1408.1146",
        "pdf_url": "https://arxiv.org/pdf/1408.1146",
        "source": "arXiv",
    },
    {
        "key": "PicFoamOpenFOAMPIC2020",
        "title": "picFoam: An OpenFOAM based electrostatic Particle-in-Cell solver",
        "category": "11_codes_ecosystem_standards",
        "arxiv": "2012.14724",
        "pdf_url": "https://arxiv.org/pdf/2012.14724",
        "source": "arXiv",
    },
    {
        "key": "KineticTheoryPICEnsembleAveraging2022",
        "title": "Kinetic theory of particle-in-cell simulation plasma and the ensemble averaging technique",
        "category": "03_pic_foundations",
        "arxiv": "2208.06375",
        "pdf_url": "https://arxiv.org/pdf/2208.06375",
        "source": "arXiv",
    },
    {
        "key": "FluidKineticPICSolver2013",
        "title": "The Fluid-Kinetic Particle-in-Cell Solver for Plasma Simulations",
        "category": "12_hybrid_fluid_models",
        "arxiv": "1306.1089",
        "pdf_url": "https://arxiv.org/pdf/1306.1089",
        "source": "arXiv",
    },
    {
        "key": "PIFE-PIC2020",
        "title": "PIFE-PIC: Parallel Immersed-Finite-Element Particle-In-Cell For 3-D Kinetic Simulations of Plasma-Material Interactions",
        "category": "08_boundaries_pml_geometry",
        "arxiv": "2011.10214",
        "pdf_url": "https://arxiv.org/pdf/2011.10214",
        "source": "arXiv",
    },
    {
        "key": "BoundElectronEffectsPIC2022",
        "title": "Modeling of bound electron effects in particle-in-cell simulation",
        "category": "09_multiphysics_collisions_ionization_qed",
        "arxiv": "2208.08038",
        "pdf_url": "https://arxiv.org/pdf/2208.08038",
        "source": "arXiv",
    },
    {
        "key": "ComputationalMethodsPlasmaPhysicsNotes",
        "title": "Computational Methods in Plasma Physics lecture notes",
        "category": "02_books_lecture_notes",
        "pdf_url": "https://cmpp.readthedocs.io/_/downloads/en/latest/pdf/",
        "source": "Read the Docs lecture notes",
    },
]


@dataclass
class Entry:
    key: str
    title: str = ""
    doi: str = ""
    url: str = ""
    year: str = ""
    author: str = ""
    journal: str = ""
    category: str = "99_unclassified"
    source: str = "warpx_refs_bib"
    pdf_url: str = ""
    pdf_path: str = ""
    status: str = "pending"
    note: str = ""
    sha256: str = ""


def clean_text(value: str) -> str:
    value = value.replace("\n", " ")
    value = re.sub(r"[{}]", "", value)
    value = re.sub(r"\s+", " ", value).strip()
    return value


def parse_bibtex(path: Path) -> list[Entry]:
    text = path.read_text(encoding="utf-8", errors="replace")
    entries: list[Entry] = []
    for match in re.finditer(r"@(\w+)\s*\{\s*([^,\s]+)\s*,", text):
        start = match.end()
        depth = 1
        i = start
        while i < len(text) and depth > 0:
            if text[i] == "{":
                depth += 1
            elif text[i] == "}":
                depth -= 1
            i += 1
        body = text[start:i - 1]
        fields = extract_fields(body)
        entry = Entry(
            key=match.group(2),
            title=clean_text(fields.get("title", "")),
            doi=clean_text(fields.get("doi", "")).lower().replace("https://doi.org/", ""),
            url=clean_text(fields.get("url", "")),
            year=clean_text(fields.get("year", "")),
            author=clean_text(fields.get("author", "")),
            journal=clean_text(fields.get("journal", fields.get("booktitle", ""))),
        )
        entry.category = classify(entry)
        entries.append(entry)
    return entries


def extract_fields(body: str) -> dict[str, str]:
    fields: dict[str, str] = {}
    i = 0
    while i < len(body):
        m = re.search(r"([A-Za-z][A-Za-z0-9_-]*)\s*=", body[i:])
        if not m:
            break
        name = m.group(1).lower()
        i += m.end()
        while i < len(body) and body[i].isspace():
            i += 1
        if i >= len(body):
            break
        if body[i] == "{":
            depth = 1
            i += 1
            start = i
            while i < len(body) and depth > 0:
                if body[i] == "{":
                    depth += 1
                elif body[i] == "}":
                    depth -= 1
                i += 1
            value = body[start:i - 1]
        elif body[i] == '"':
            i += 1
            start = i
            while i < len(body) and body[i] != '"':
                i += 1
            value = body[start:i]
            i += 1
        else:
            start = i
            while i < len(body) and body[i] not in ",\n":
                i += 1
            value = body[start:i]
        fields[name] = value.strip()
        while i < len(body) and body[i] not in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz":
            i += 1
    return fields


def classify(entry: Entry) -> str:
    haystack = " ".join([entry.key, entry.title, entry.journal]).lower()
    for category, needles in CATEGORIES:
        if any(n in haystack for n in needles):
            return category
    return "99_unclassified"


def safe_filename(entry: Entry) -> str:
    year = entry.year or "no-year"
    title = entry.title or entry.key
    title = re.sub(r"[^A-Za-z0-9._ -]+", "", title)
    title = re.sub(r"\s+", "_", title).strip("._-")
    title = title[:120] or entry.key
    return f"{year}_{entry.key}_{title}.pdf"


def request_json(url: str) -> dict | None:
    req = urllib.request.Request(url, headers={"User-Agent": f"PIC-tutor/0.1 mailto:{OPENALEX_MAILTO}"})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read().decode("utf-8", errors="replace"))
    except Exception:
        return None


def find_pdf_url(entry: Entry) -> str:
    if entry.pdf_url:
        return entry.pdf_url
    if entry.url.lower().endswith(".pdf"):
        return entry.url
    arxiv_from_doi = re.search(r"10\.48550/arxiv\.([0-9.]+)", entry.doi, re.I)
    if arxiv_from_doi:
        return f"https://arxiv.org/pdf/{arxiv_from_doi.group(1)}"
    data = None
    if entry.doi:
        doi_url = urllib.parse.quote(f"https://doi.org/{entry.doi}", safe="")
        data = request_json(f"https://api.openalex.org/works/{doi_url}?mailto={urllib.parse.quote(OPENALEX_MAILTO)}")
    if data is None and entry.title:
        q = urllib.parse.quote(entry.title)
        search = request_json(f"https://api.openalex.org/works?search={q}&per-page=1&mailto={urllib.parse.quote(OPENALEX_MAILTO)}")
        if search and search.get("results"):
            data = search["results"][0]
    if not data:
        return ""
    for loc_key in ("best_oa_location", "primary_location"):
        loc = data.get(loc_key) or {}
        if loc.get("pdf_url"):
            return loc["pdf_url"]
    for loc in data.get("locations") or []:
        if loc and loc.get("pdf_url"):
            return loc["pdf_url"]
    oa_url = (data.get("open_access") or {}).get("oa_url") or ""
    if oa_url.lower().endswith(".pdf") or "arxiv.org/pdf" in oa_url:
        return oa_url
    return ""


def download_pdf(url: str, dest: Path, max_mb: int) -> tuple[bool, str, str]:
    headers = {"User-Agent": f"PIC-tutor/0.1 mailto:{OPENALEX_MAILTO}"}
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=25) as resp:
            content_length = resp.headers.get("Content-Length")
            if content_length and int(content_length) > max_mb * 1024 * 1024:
                return False, "", f"too large: {content_length} bytes"
            data = resp.read(max_mb * 1024 * 1024 + 1)
            if len(data) > max_mb * 1024 * 1024:
                return False, "", f"too large: >{max_mb} MB"
            if not data.startswith(b"%PDF"):
                return False, "", "downloaded content is not a PDF"
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(data)
            sha = hashlib.sha256(data).hexdigest()
            return True, sha, ""
    except urllib.error.HTTPError as exc:
        return False, "", f"HTTP {exc.code}"
    except Exception as exc:
        return False, "", str(exc)


def ensure_dirs(root: Path) -> None:
    for category, _ in CATEGORIES:
        (root / category).mkdir(parents=True, exist_ok=True)
    for extra in ("00_index", "99_unclassified"):
        (root / extra).mkdir(parents=True, exist_ok=True)


def write_readme(root: Path) -> None:
    lines = [
        "# References",
        "",
        "This directory stores legally available open PDFs and metadata for the PIC-tutor book project.",
        "Paywalled books and articles should be listed in the manifest, not downloaded from unauthorized sources.",
        "",
        "## Categories",
        "",
    ]
    for category, _ in CATEGORIES:
        lines.append(f"- `{category}/`")
    lines.extend([
        "- `99_unclassified/`",
        "",
        "## Index Files",
        "",
        "- `00_index/manifest.jsonl`: one record per attempted reference.",
        "- `00_index/download_log.md`: human-readable summary.",
        "",
    ])
    (root / "README.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--bib", default="../warpx/Docs/source/refs.bib")
    parser.add_argument("--out", default="references")
    parser.add_argument("--limit", type=int, default=80)
    parser.add_argument("--max-mb", type=int, default=80)
    parser.add_argument("--sleep", type=float, default=0.4)
    parser.add_argument("--curated-only", action="store_true")
    args = parser.parse_args()

    out = Path(args.out)
    ensure_dirs(out)
    write_readme(out)

    entries: list[Entry] = []
    for seed in CURATED_SEEDS:
        entry = Entry(
            key=seed["key"],
            title=seed["title"],
            doi=seed.get("doi", ""),
            url=seed.get("pdf_url", ""),
            category=seed["category"],
            source=seed.get("source", "curated_seed"),
            pdf_url=seed.get("pdf_url", ""),
        )
        entries.append(entry)

    if not args.curated_only:
        entries.extend(parse_bibtex(Path(args.bib)))

    manifest_path = out / "00_index" / "manifest.jsonl"
    log_path = out / "00_index" / "download_log.md"

    attempted = 0
    downloaded = 0
    skipped = 0
    records: list[Entry] = []

    for entry in entries:
        if attempted >= args.limit:
            entry.status = "not_attempted_limit_reached"
            records.append(entry)
            continue
        attempted += 1
        pdf_url = find_pdf_url(entry)
        entry.pdf_url = pdf_url
        if not pdf_url:
            entry.status = "no_open_pdf_found"
            skipped += 1
            records.append(entry)
            time.sleep(args.sleep)
            continue
        dest = out / entry.category / safe_filename(entry)
        if dest.exists() and dest.stat().st_size > 0:
            entry.status = "already_exists"
            entry.pdf_path = str(dest)
            downloaded += 1
            records.append(entry)
            continue
        ok, sha, note = download_pdf(pdf_url, dest, args.max_mb)
        if ok:
            entry.status = "downloaded"
            entry.pdf_path = str(dest)
            entry.sha256 = sha
            downloaded += 1
        else:
            entry.status = "download_failed"
            entry.note = note
            skipped += 1
        records.append(entry)
        time.sleep(args.sleep)

    with manifest_path.open("w", encoding="utf-8") as f:
        for entry in records:
            f.write(json.dumps(asdict(entry), ensure_ascii=False, sort_keys=True) + "\n")

    by_status: dict[str, int] = {}
    by_category: dict[str, int] = {}
    for entry in records:
        by_status[entry.status] = by_status.get(entry.status, 0) + 1
        if entry.pdf_path:
            by_category[entry.category] = by_category.get(entry.category, 0) + 1

    log_lines = [
        "# Download Log",
        "",
        f"- Attempt limit: {args.limit}",
        f"- Attempted now: {attempted}",
        f"- Downloaded or already present: {downloaded}",
        f"- Skipped/failed/no OA PDF: {skipped}",
        "",
        "## Status Counts",
        "",
    ]
    for status, count in sorted(by_status.items()):
        log_lines.append(f"- `{status}`: {count}")
    log_lines.extend(["", "## Downloaded By Category", ""])
    for category, count in sorted(by_category.items()):
        log_lines.append(f"- `{category}`: {count}")
    log_lines.extend(["", "## Notes", ""])
    log_lines.append("- Only direct/open PDFs are downloaded.")
    log_lines.append("- Paywalled or ambiguous records remain in the manifest for later manual checking.")
    log_path.write_text("\n".join(log_lines), encoding="utf-8")

    print(f"attempted={attempted} downloaded_or_present={downloaded} skipped={skipped}")
    print(f"manifest={manifest_path}")
    print(f"log={log_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
