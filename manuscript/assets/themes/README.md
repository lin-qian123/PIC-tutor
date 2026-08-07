# PDF Themes

These XeLaTeX header files style the one canonical Markdown manuscript. They do not contain chapter content and must not change factual claims, equations, figure files, or source links.

| Theme | Paper and density | Intended use |
|---|---|---|
| `technical` | US Letter, moderate density | Continuous screen reading and the current release-compatible format |
| `academic` | A4, wider inner margin, relaxed leading | Formal printing, annotation, and bound copies |
| `compact` | A4, narrow margin, dense code and tables | Source lookup and local reference printing |

Build all three variants with:

```bash
python scripts/build_pdf_themes.py
python scripts/audit_pdf_themes.py --output-dir dist/themes
```

The output filenames retain the manuscript source edition (`v0.110`) so they cannot be mistaken for independent content releases. Git tag `v1.0` freezes the canonical technical render that preceded this theme system.
