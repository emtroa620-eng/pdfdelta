from __future__ import annotations

import re
from collections import defaultdict

import fitz

from .models import LineBox, PageBox, WordBox


def _normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip()).lower()


def group_words_into_lines(
    raw_words: list[tuple],
    page_index: int,
) -> list[LineBox]:
    """Group PyMuPDF word tuples into :class:`LineBox` objects.

    Groups by ``(block_no, line_no)`` so that multi-column layouts are
    handled correctly — words in different columns get separate lines
    even when they share the same y-coordinate.
    """
    groups: defaultdict[tuple[int, int], list[tuple]] = defaultdict(list)
    for w in raw_words:
        x0, y0, x1, y1, text, block_no, line_no, word_no = w[:8]
        if not str(text).strip():
            continue
        groups[(int(block_no), int(line_no))].append(
            (x0, y0, x1, y1, str(text))
        )

    # Sort by (block_no, line_no) for stable ordering.
    # Using PyMuPDF's own block ordering keeps line order consistent
    # between two versions of the same document, even when figures
    # shift vertically by a few pixels.
    sorted_keys = sorted(groups.keys())

    lines: list[LineBox] = []
    for line_idx, key in enumerate(sorted_keys):
        word_items = sorted(groups[key], key=lambda t: t[0])  # sort by x0
        line_words: list[WordBox] = []
        plain_words: list[str] = []

        for word_idx, (x0, y0, x1, y1, text) in enumerate(word_items):
            word = WordBox(
                page_index=page_index,
                line_index=line_idx,
                word_index=word_idx,
                text=text,
                norm=_normalize(text),
                rect=(x0, y0, x1, y1),
            )
            line_words.append(word)
            plain_words.append(text)

        line_text = " ".join(plain_words)
        lines.append(
            LineBox(
                page_index=page_index,
                line_index=line_idx,
                text=line_text,
                norm_text=_normalize(line_text),
                words=line_words,
            )
        )

    return lines


def extract_document(path: str) -> list[PageBox]:
    doc = fitz.open(path)
    pages: list[PageBox] = []

    try:
        for page_index in range(len(doc)):
            page = doc[page_index]
            raw_words = page.get_text("words", sort=True)
            lines = group_words_into_lines(raw_words, page_index=page_index)
            pages.append(PageBox(page_index=page_index, lines=lines))
    finally:
        doc.close()

    return pages