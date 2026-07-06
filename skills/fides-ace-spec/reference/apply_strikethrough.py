#!/usr/bin/env python3
"""Apply ``~~strikethrough~~`` to a section Markdown file from PDF detection.

Reuses the detection logic in ``detect_strikethrough.py``. For each struck text
span it records the PDF page(s) where the strike occurs, then walks the target
Markdown (tracking the current page via ``<!-- p.NNN -->`` markers) and wraps a
line in ``~~ … ~~`` when its "core" text matches a span struck on that same page.

Page-scoping makes duplicated lines safe: a line is only marked on the page
where it was actually struck. Lines already containing ``~~`` are skipped.
Spans with no exact md line (reflow / figure captions) are reported for manual
review rather than guessed.

Usage: python3 apply_strikethrough.py <md_file> <first_page> <last_page>
"""
import re
import sys
import fitz
import detect_strikethrough as det

MINLEN = 15
# Leading bullet / list glyphs stripped when comparing a line to a span.
BULLETS = " \t\u00a0\uf0b7\u25cb\u2022\u25aa\u2013\u2014-\u2192\u279c\u2b95"
PAGE_RE = re.compile(r"<!--\s*p\.(\d+)\s*-->")


def core(line: str) -> str:
    return line.strip().lstrip(BULLETS).strip()


def struck_span_pages(first, last):
    """Return {span_text: set(pages)} for struck spans of length >= MINLEN."""
    doc = fitz.open(det.PDF)
    out = {}
    for pno in range(first - 1, last):
        page = doc[pno]
        lines = det.horizontal_lines(page)
        annots = det.annot_struck_rects(page)
        for block in page.get_text("dict")["blocks"]:
            for line in block.get("lines", []):
                for span in line["spans"]:
                    text = span["text"].strip()
                    if len(text) < MINLEN:
                        continue
                    hit = det.span_is_struck(span, lines)
                    if not hit and annots:
                        sb = fitz.Rect(span["bbox"])
                        for ar, _t in annots:
                            if sb.intersects(ar) and sb.get_area():
                                if (sb & ar).get_area() / sb.get_area() >= 0.4:
                                    hit = True
                                    break
                    if hit:
                        out.setdefault(text, set()).add(pno + 1)
    return out


def main():
    md, first, last = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
    span_pages = struck_span_pages(first, last)

    with open(md, encoding="utf-8") as f:
        lines = f.read().split("\n")
    cur_page = None
    wrapped = 0
    marked = set()
    for i, line in enumerate(lines):
        m = PAGE_RE.search(line)
        if m:
            cur_page = int(m.group(1))
            continue
        c = core(line)
        if c in span_pages and "~~" not in line and cur_page in span_pages[c]:
            pre_ws = line[: len(line) - len(line.lstrip())]
            lines[i] = f"{pre_ws}~~{line.strip()}~~"
            wrapped += 1
            marked.add(c)

    with open(md, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    unmatched = sorted(s for s in span_pages if s not in marked)
    print(f"== {md}  (pages {first}-{last}) ==")
    print(f"lignes barrées marquées : {wrapped}")
    if unmatched:
        print(f"\nSpans barrés non marqués (reflow / figure / page sans repère) : {len(unmatched)}")
        for s in unmatched:
            print(f"  · [{','.join(map(str, sorted(span_pages[s])))}] {s[:80]}")


if __name__ == "__main__":
    main()
