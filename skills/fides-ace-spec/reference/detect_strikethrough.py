#!/usr/bin/env python3
"""Detect struck-through (barré) text in the FIDES ACE spec PDF.

Two detection strategies are combined:

1. **StrikeOut / Highlight annotations** — proper PDF markup annotations.
2. **Vector strike lines** — thin, near-horizontal drawn lines whose y sits in
   the middle band of a text line and whose x-range overlaps that text. This is
   how the V06.09 "révoqué" passages are encoded (a drawn line over the glyphs,
   often with a yellow highlight rectangle behind).

Output: a report grouped by 1-based PDF page listing the struck text spans, so
the Markdown transcription can be updated with ``~~...~~``.

Run: python3 detect_strikethrough.py [first_page] [last_page]
"""
import sys
import fitz  # PyMuPDF

PDF = "SFG_FIDES_ACE_V06.09_version_fusionnée.pdf"

# A drawn line counts as a strike if it is nearly horizontal and thin.
MAX_LINE_HEIGHT = 2.5      # bbox height of the drawn line (points)
MID_BAND = (0.30, 0.72)    # fraction of span height the line must cross
MIN_X_OVERLAP = 0.45       # fraction of span width covered by the line


def horizontal_lines(page):
    """Return list of (x0, x1, y) for near-horizontal drawn line segments."""
    lines = []
    for d in page.get_drawings():
        for item in d["items"]:
            if item[0] == "l":  # line segment
                p1, p2 = item[1], item[2]
                if abs(p1.y - p2.y) <= 1.0:  # near horizontal
                    x0, x1 = sorted((p1.x, p2.x))
                    if x1 - x0 >= 3:
                        lines.append((x0, x1, (p1.y + p2.y) / 2))
            elif item[0] == "re":  # rectangle used as a thin strike bar
                r = item[1]
                if r.height <= MAX_LINE_HEIGHT and r.width >= 3:
                    lines.append((r.x0, r.x1, (r.y0 + r.y1) / 2))
    return lines


def span_is_struck(span, lines):
    bx0, by0, bx1, by1 = span["bbox"]
    h = by1 - by0
    if h <= 0:
        return False
    lo = by0 + MID_BAND[0] * h
    hi = by0 + MID_BAND[1] * h
    w = bx1 - bx0
    for lx0, lx1, ly in lines:
        if lo <= ly <= hi:
            ox0 = max(bx0, lx0)
            ox1 = min(bx1, lx1)
            if w > 0 and (ox1 - ox0) / w >= MIN_X_OVERLAP:
                return True
    return False


def annot_struck_rects(page):
    rects = []
    annot = page.first_annot
    while annot:
        t = annot.type[1] if isinstance(annot.type, (list, tuple)) else annot.type
        if t in ("StrikeOut", "Highlight"):
            rects.append((annot.rect, t))
        annot = annot.next
    return rects


def main():
    doc = fitz.open(PDF)
    first = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    last = int(sys.argv[2]) if len(sys.argv) > 2 else doc.page_count
    any_hit = False
    for pno in range(first - 1, last):
        page = doc[pno]
        lines = horizontal_lines(page)
        annots = annot_struck_rects(page)
        d = page.get_text("dict")
        struck = []
        for block in d["blocks"]:
            for line in block.get("lines", []):
                for span in line["spans"]:
                    text = span["text"].strip()
                    if not text:
                        continue
                    hit = span_is_struck(span, lines)
                    if not hit and annots:
                        sb = fitz.Rect(span["bbox"])
                        for ar, _t in annots:
                            if sb.intersects(ar) and sb.get_area():
                                inter = sb & ar
                                if inter.get_area() / sb.get_area() >= 0.4:
                                    hit = True
                                    break
                    if hit:
                        struck.append(text)
        if struck:
            any_hit = True
            print(f"\n=== PAGE {pno + 1} (PDF page) — {len(struck)} span(s) barré(s) ===")
            for s in struck:
                print(f"  ~~ {s}")
    if not any_hit:
        print(f"Aucun texte barré détecté entre les pages {first} et {last}.")


if __name__ == "__main__":
    main()
