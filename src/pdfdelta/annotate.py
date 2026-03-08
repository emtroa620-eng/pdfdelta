from __future__ import annotations

import fitz

from .models import RectTuple


def add_highlight(
    page: fitz.Page,
    rect_tuple: RectTuple,
    color: tuple[float, float, float],
    opacity: float = 0.35,
) -> None:
    rect = fitz.Rect(rect_tuple)
    annot = page.add_highlight_annot(quads=[rect])
    annot.set_colors(stroke=color)
    annot.set_opacity(opacity)
    annot.update()


def apply_annotations(
    input_pdf: str,
    output_pdf: str,
    page_to_rects: dict[int, list[RectTuple]],
    color: tuple[float, float, float],
    opacity: float = 0.35,
) -> None:
    doc = fitz.open(input_pdf)
    try:
        for page_index, rects in page_to_rects.items():
            if page_index >= len(doc):
                continue
            page = doc[page_index]
            for rect in rects:
                add_highlight(page, rect, color=color, opacity=opacity)

        doc.save(output_pdf, garbage=4, deflate=True)
    finally:
        doc.close()