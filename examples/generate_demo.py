"""Generate a pair of simulated two-column academic PDFs for the README demo.

old2.pdf  — the "original" version
new2.pdf  — the "revised" version with several kinds of changes:
  1. A word swap in the abstract
  2. A sentence insertion in section 2
  3. A sentence reworded across a column break
  4. Cross-page text reflow (paragraph pushed down by the insertion)
"""
from __future__ import annotations

import fitz  # PyMuPDF

# ── Layout constants (Letter page, IEEE-ish two-column) ──────────
W, H = 612, 792
MARGIN_TOP = 72
MARGIN_BOT = 72
MARGIN_L = 54
MARGIN_R = 54
COL_GAP = 24
COL_W = (W - MARGIN_L - MARGIN_R - COL_GAP) / 2

TITLE_FONTSIZE = 16
SECTION_FONTSIZE = 11
BODY_FONTSIZE = 9.5
LEADING = 13  # line spacing

# ── Text content ────────────────────────────────────────────────
TITLE = "On the Dynamics of Placeholder Text in Academic Typesetting"
AUTHORS = "A. Lorem and B. Ipsum"

ABSTRACT_OLD = (
    "Abstract — This paper investigates the role of placeholder text in "
    "modern document processing systems. We present a comprehensive analysis "
    "of text reflow behavior across multi-column layouts typically found in "
    "academic publications. Our method achieves robust detection of content "
    "changes while correctly handling text that shifts between columns and "
    "pages due to formatting adjustments. Experimental results demonstrate "
    "that our approach significantly reduces false positives compared to "
    "naive line-by-line differencing."
)

ABSTRACT_NEW = (
    "Abstract — This paper investigates the role of placeholder text in "
    "modern document processing pipelines. We present a comprehensive analysis "
    "of text reflow behavior across multi-column layouts typically found in "
    "academic publications. Our method achieves robust detection of content "
    "changes while correctly handling text that shifts between columns and "
    "pages due to formatting adjustments. Experimental results demonstrate "
    "that our approach significantly reduces false positives compared to "
    "naive line-by-line differencing."
)

SEC1_TITLE = "1. Introduction"
SEC1_OLD = (
    "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod "
    "tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim "
    "veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea "
    "commodo consequat. Duis aute irure dolor in reprehenderit in voluptate "
    "velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint "
    "occaecat cupidatat non proident, sunt in culpa qui officia deserunt "
    "mollit anim id est laborum. Curabitur pretium tincidunt lacus. Nulla "
    "gravida orci a odio. Nullam varius, turpis et commodo pharetra, est "
    "eros bibendum elit, nec luctus magna felis sollicitudin mauris. Integer "
    "in mauris eu nibh euismod gravida. Duis ac tellus et risus vulputate "
    "vehicula. Donec lobortis risus a elit."
)
SEC1_NEW = SEC1_OLD  # no change

SEC2_TITLE = "2. Related Work"
SEC2_OLD = (
    "Pellentesque habitant morbi tristique senectus et netus et malesuada "
    "fames ac turpis egestas. Vestibulum tortor quam, feugiat vitae, "
    "ultricies eget, tempor sit amet, ante. Donec eu libero sit amet quam "
    "egestas semper. Aenean ultricies mi vitae est. Mauris placerat eleifend "
    "leo. Quisque sit amet est et sapien ullamcorper pharetra. Vestibulum "
    "erat wisi, condimentum sed, commodo vitae, ornare sit amet, wisi. "
    "Aenean fermentum, elit eget tincidunt condimentum, eros ipsum rutrum "
    "orci, sagittis tempus lacus enim ac dui."
)
SEC2_NEW = (
    "Pellentesque habitant morbi tristique senectus et netus et malesuada "
    "fames ac turpis egestas. Vestibulum tortor quam, feugiat vitae, "
    "ultricies eget, tempor sit amet, ante. Donec eu libero sit amet quam "
    "egestas semper. Aenean ultricies mi vitae est. Recent studies by Zhang "
    "et al. [12] have shown that cross-page reflow detection can be improved "
    "using global sequence alignment rather than per-page comparison. "
    "Mauris placerat eleifend "
    "leo. Quisque sit amet est et sapien ullamcorper pharetra. Vestibulum "
    "erat wisi, condimentum sed, commodo vitae, ornare sit amet, wisi. "
    "Aenean fermentum, elit eget tincidunt condimentum, eros ipsum rutrum "
    "orci, sagittis tempus lacus enim ac dui."
)

SEC3_TITLE = "3. Method"
SEC3_OLD = (
    "Fusce dapibus, tellus ac cursus commodo, tortor mauris condimentum "
    "nibh, ut fermentum massa justo sit amet risus. Etiam porta sem "
    "malesuada magna mollis euismod. Donec sed odio dui. Aenean lacinia "
    "bibendum nulla sed consectetur. Cras mattis consectetur purus sit amet "
    "fermentum. Cras justo odio, dapibus ut facilisis in, egestas eget "
    "quam. Nullam id dolor id nibh ultricies vehicula ut id elit. Nulla "
    "vitae elit libero, a pharetra augue. Praesent commodo cursus magna, "
    "vel scelerisque nisl consectetur et. Morbi leo risus, porta ac "
    "consectetur ac, vestibulum at eros."
)
SEC3_NEW = (
    "Fusce dapibus, tellus ac cursus commodo, tortor mauris condimentum "
    "nibh, ut fermentum massa justo sit amet risus. Etiam porta sem "
    "malesuada magna mollis euismod. Donec sed odio dui. Aenean lacinia "
    "bibendum nulla sed consectetur. Cras mattis consectetur purus sit amet "
    "fermentum. Cras justo odio, dapibus ut facilisis in, egestas eget "
    "quam. Nullam id dolor id nibh ultricies vehicula ut id elit. Nulla "
    "vitae elit libero, a pharetra augue. Praesent commodo cursus magna, "
    "vel scelerisque nisl consectetur et. Morbi leo risus, porta ac "
    "consectetur ac, vestibulum at eros."
)

SEC4_TITLE = "4. Experiments"
SEC4_OLD = (
    "Maecenas sed diam eget risus varius blandit sit amet non magna. "
    "Integer posuere erat a ante venenatis dapibus posuere velit aliquet. "
    "Vivamus sagittis lacus vel augue laoreet rutrum faucibus dolor auctor. "
    "Cum sociis natoque penatibus et magnis dis parturient montes, nascetur "
    "ridiculus mus. Donec ullamcorper nulla non metus auctor fringilla. "
    "Sed posuere consectetur est at lobortis. Praesent commodo cursus "
    "magna, vel scelerisque nisl consectetur et."
)
SEC4_NEW = (
    "Maecenas sed diam eget risus varius blandit sit amet non magna. "
    "Integer posuere erat a ante venenatis dapibus posuere velit aliquet. "
    "Vivamus sagittis lacus vel augue laoreet rutrum faucibus dolor auctor. "
    "Cum sociis natoque penatibus et magnis dis parturient montes, nascetur "
    "ridiculus mus. Donec ullamcorper nulla non metus auctor fringilla. "
    "Sed posuere consectetur est at lobortis. Our results confirm a 23% "
    "improvement over the baseline method."
)

SEC5_TITLE = "5. Conclusion"
SEC5_TEXT = (
    "Vivamus sagittis lacus vel augue laoreet rutrum faucibus dolor auctor. "
    "Cras mattis consectetur purus sit amet fermentum. Aenean eu leo quam. "
    "Pellentesque ornare sem lacinia quam venenatis vestibulum. Sed posuere "
    "consectetur est at lobortis. Cras mattis consectetur purus sit amet "
    "fermentum. Integer posuere erat a ante venenatis dapibus posuere velit "
    "aliquet. Duis mollis, est non commodo luctus, nisi erat porttitor "
    "ligula, eget lacinia odio sem nec elit."
)


def _build_pdf(path: str, sections: list[tuple[str, str, str]],
               abstract: str) -> None:
    doc = fitz.open()

    # We'll write column by column, page by page
    page = doc.new_page(width=W, height=H)
    y = MARGIN_TOP

    # ── Title ────────────────────────────────────────────────────
    r = fitz.Rect(MARGIN_L, y, W - MARGIN_R, y + 24)
    page.insert_textbox(r, TITLE, fontsize=TITLE_FONTSIZE,
                        fontname="helv", align=fitz.TEXT_ALIGN_CENTER)
    y += 28

    # ── Authors ──────────────────────────────────────────────────
    r = fitz.Rect(MARGIN_L, y, W - MARGIN_R, y + 16)
    page.insert_textbox(r, AUTHORS, fontsize=10,
                        fontname="helv", align=fitz.TEXT_ALIGN_CENTER)
    y += 24

    # ── Abstract (full width) ────────────────────────────────────
    r = fitz.Rect(MARGIN_L + 20, y, W - MARGIN_R - 20, y + 200)
    used = page.insert_textbox(r, abstract, fontsize=BODY_FONTSIZE,
                               fontname="helv", align=fitz.TEXT_ALIGN_JUSTIFY)
    # Estimate actual height
    abs_height = 200 + used  # used is negative remaining
    if abs_height < 40:
        abs_height = 80
    y += abs_height + 8

    # ── Two-column body ──────────────────────────────────────────
    col = 0  # 0 = left, 1 = right
    col_x = [MARGIN_L, MARGIN_L + COL_W + COL_GAP]

    for sec_title, sec_marker, sec_body in sections:
        # Section heading
        needed_head = SECTION_FONTSIZE + 8
        if y + needed_head > H - MARGIN_BOT:
            if col == 0:
                col = 1
                y = MARGIN_TOP + abs_height + 8 if page == doc[0] else MARGIN_TOP
            else:
                page = doc.new_page(width=W, height=H)
                col = 0
                y = MARGIN_TOP

        x0 = col_x[col]
        r = fitz.Rect(x0, y, x0 + COL_W, y + SECTION_FONTSIZE + 4)
        page.insert_textbox(r, sec_title, fontsize=SECTION_FONTSIZE,
                            fontname="helv")
        y += SECTION_FONTSIZE + 8

        # Section body — fill column, overflow to next
        remaining = sec_body
        while remaining:
            avail_h = H - MARGIN_BOT - y
            if avail_h < LEADING * 2:
                if col == 0:
                    col = 1
                    y = MARGIN_TOP + abs_height + 8 if page == doc[0] else MARGIN_TOP
                else:
                    page = doc.new_page(width=W, height=H)
                    col = 0
                    y = MARGIN_TOP
                avail_h = H - MARGIN_BOT - y

            x0 = col_x[col]
            r = fitz.Rect(x0, y, x0 + COL_W, y + avail_h)
            rc = page.insert_textbox(r, remaining, fontsize=BODY_FONTSIZE,
                                     fontname="helv",
                                     align=fitz.TEXT_ALIGN_JUSTIFY)
            if rc >= 0:
                # All text fit
                used_h = avail_h - rc
                y += used_h + 10
                remaining = ""
            else:
                # Overflowed — figure out what fit
                y += avail_h
                # Estimate chars that fit based on column area
                chars_per_line = int(COL_W / (BODY_FONTSIZE * 0.5))
                lines_fit = int(avail_h / LEADING)
                chars_fit = chars_per_line * lines_fit
                # Find word boundary
                if chars_fit < len(remaining):
                    cut = remaining.rfind(' ', 0, chars_fit)
                    if cut <= 0:
                        cut = chars_fit
                    remaining = remaining[cut:].lstrip()
                else:
                    remaining = ""

                if col == 0:
                    col = 1
                    y = MARGIN_TOP + abs_height + 8 if page == doc[0] else MARGIN_TOP
                else:
                    page = doc.new_page(width=W, height=H)
                    col = 0
                    y = MARGIN_TOP

    n_pages = len(doc)
    doc.save(path, garbage=4, deflate=True)
    doc.close()
    print(f"Wrote {path} ({n_pages} pages)")


def main():
    sections_old = [
        (SEC1_TITLE, "sec1", SEC1_OLD),
        (SEC2_TITLE, "sec2", SEC2_OLD),
        (SEC3_TITLE, "sec3", SEC3_OLD),
        (SEC4_TITLE, "sec4", SEC4_OLD),
        (SEC5_TITLE, "sec5", SEC5_TEXT),
    ]
    sections_new = [
        (SEC1_TITLE, "sec1", SEC1_NEW),
        (SEC2_TITLE, "sec2", SEC2_NEW),
        (SEC3_TITLE, "sec3", SEC3_NEW),
        (SEC4_TITLE, "sec4", SEC4_NEW),
        (SEC5_TITLE, "sec5", SEC5_TEXT),
    ]

    _build_pdf("examples/old.pdf", sections_old, ABSTRACT_OLD)
    _build_pdf("examples/new.pdf", sections_new, ABSTRACT_NEW)


if __name__ == "__main__":
    main()
