# pdfcompare

A visual diff tool for born-digital PDFs.  Given an *old* and *new* version of a PDF, **pdfcompare** highlights every changed word directly on the original pages — deletions in red, additions in green — so you can review revisions at a glance.

Built for **academic papers** (IEEE, ACM, Springer, etc.) where formatting matters and changes are often subtle, but works with any born-digital PDF.

## What It Does

| Old (deletions in red) | New (additions in green) |
|:-:|:-:|
| ![old](examples/old_marked.pdf) | ![new](examples/new_marked.pdf) |

pdfcompare handles the tricky parts of comparing formatted PDFs:

- **Multi-column layouts** — Changes in a two-column paper are detected per-column without bleeding highlights across the gutter.
- **Cross-page reflow** — When an edit on page 3 pushes text onto page 4, only the actual edit is highlighted. Reflowed-but-unchanged text is left clean.
- **Line-break hyphenation** — Words split by hyphens at line breaks (e.g. `aver-` / `age`) are rejoined before comparison.
- **Moved paragraphs** — Text that appears in both documents but at different positions (e.g. a paragraph that moved from page 5 to page 6) is recognized and excluded from the diff.
- **Sub-word precision** — When a single word is partially changed (e.g. `systems` → `pipelines`), only the differing characters are highlighted, not the entire word.

## Install

```sh
pip install pdfcompare
```

Requires Python 3.10+ and [PyMuPDF](https://pymupdf.readthedocs.io/).

## Usage

```sh
pdfcompare old.pdf new.pdf
```

This writes two annotated files:

- `old_marked.pdf` — original pages with deletions highlighted in red
- `new_marked.pdf` — revised pages with additions highlighted in green

### Options

```sh
pdfcompare old.pdf new.pdf --old-out old_diff.pdf --new-out new_diff.pdf --opacity 0.5
```

| Flag | Default | Description |
|------|---------|-------------|
| `--old-out` | `old_marked.pdf` | Output path for the annotated old PDF |
| `--new-out` | `new_marked.pdf` | Output path for the annotated new PDF |
| `--opacity` | `0.35` | Highlight opacity (0.0–1.0) |

### As a Library

```python
from pdfcompare import extract_document, compare_documents, apply_annotations

old_pages = extract_document("old.pdf")
new_pages = extract_document("new.pdf")

old_diffs, new_diffs = compare_documents(old_pages, new_pages)

apply_annotations("old.pdf", "old_diff.pdf", old_diffs, color=(1.0, 0.75, 0.75))
apply_annotations("new.pdf", "new_diff.pdf", new_diffs, color=(0.75, 1.0, 0.75))
```

## How It Works

1. **Extract** — Text is extracted word-by-word from each page using PyMuPDF, preserving exact bounding-box coordinates.
2. **Flatten & Diff** — All lines from all pages are flattened into a single sequence and compared globally using `difflib.SequenceMatcher`. This lets the algorithm see across page boundaries.
3. **Word-level refinement** — Within each changed block, a second word-level diff isolates the individual words (and sub-word regions) that actually changed.
4. **Reflow suppression** — A second pass examines page-boundary candidates and suppresses highlights on text that merely reflowed to an adjacent page without changing.
5. **Annotate** — Surviving diff rects are written back as native PDF highlight annotations on the original pages.

## License

MIT
