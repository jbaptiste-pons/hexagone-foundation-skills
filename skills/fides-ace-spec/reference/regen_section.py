#!/usr/bin/env python3
"""Regenerate a single section's Markdown from the PDF using build_docs helpers.

Usage: python3 regen_section.py <slug> <out_path>
  e.g. python3 regen_section.py 05-VF-valoriser-prestations /tmp/vf_regen.md
"""
import sys
import fitz
import build_docs as bd


def main():
    slug, out_path = sys.argv[1], sys.argv[2]
    doc = fitz.open(bd.PDF)
    n = doc.page_count
    bounds = [(s[0], bd.SECTIONS[i + 1][0] - 1 if i + 1 < len(bd.SECTIONS) else n, s[1], s[2])
              for i, s in enumerate(bd.SECTIONS)]
    target = next((b for b in bounds if b[2] == slug), None)
    if target is None:
        valid = ", ".join(b[2] for b in bounds)
        sys.exit(f"Erreur : slug inconnu '{slug}'. Slugs valides : {valid}")
    start, end, _slug, title = target

    lines = [f"# {title}", "", f"_Pages {start}\u2013{end} du PDF source._", ""]
    for pno in range(start, end + 1):
        page = doc[pno - 1]
        md = bd.page_to_md(page)
        body = [l for l in md if l.strip()]
        if body:
            lines.append(f"\n<!-- p.{pno} -->")
            lines.extend(md)
        if bd.is_figure_page(page, pno):
            fname = f"p{pno:03d}.png"
            cap = bd.caption_for(page) or f"Sch\u00e9ma / diagramme page {pno}"
            lines += ["", f"![{cap}](figures/{fname})", f"*Figure (p.{pno}) : {cap}*"]
            if pno in bd.MERMAID:
                lines += ["", "> Transcription Mermaid (depuis la figure ci-dessus) :", "", bd.MERMAID[pno]]
            lines.append("")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print(f"wrote {out_path}  pages {start}-{end}")


if __name__ == "__main__":
    main()
