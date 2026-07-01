#!/usr/bin/env python3
"""Convert the FIDES ACE spec PDF into chunked, searchable Markdown + figure PNGs.

Output layout (under fides/docs/):
  INDEX.md                 router / table of contents
  NN-<slug>.md             one file per top-level functional domain
  figures/pNNN.png         rendered images of diagram/schema pages

Run: .venv/bin/python build_docs.py
"""
import re
import fitz  # PyMuPDF
from pathlib import Path

PDF = "SFG_FIDES_ACE_V06.08_version_fusionnée.pdf"
OUT = Path("docs")
FIG = OUT / "figures"

# Top-level sections: (start_page_1based, slug, human title)
SECTIONS = [
    (1,   "01-PG-presentation-generale",     "PG — Présentation Générale"),
    (43,  "02-BS-beneficiaire-des-soins",    "BS — Acquérir les informations du Bénéficiaire des Soins"),
    (87,  "03-IP-informations-prestations",  "IP — Acquérir les Informations des Prestations"),
    (154, "04-CF-contexte-facturation",      "CF — Déterminer le Contexte de Facturation"),
    (204, "05-VF-valoriser-prestations",     "VF — Valoriser les prestations de la Facture"),
    (305, "06-TF-transmettre-factures",      "TF — Transmettre les Factures"),
    (356, "07-DICO-dictionnaire-donnees",    "DICO — Dictionnaire de données"),
]

# Lines that are page furniture / legal boilerplate -> dropped.
BOILER = re.compile(
    r"^(Référence\s*:|Sécurité\s*:|GIE SESAM-Vitale|www\.sesam-vitale\.fr|"
    r"5, boulevard Marie|Établissements\s*$|SPECIFICATIONS FONCTIONNELLES|"
    r"FIDES\s*$|ACE et activités|urgences\s*$|SFG - FIDES|ETS-SFG-\d|"
    r"Version\s*:|Ce document ne peut|Ce document a été élaboré|"
    r"Conformément à l|représentation ou reproduction|support utilisé|"
    r"Il en est de même|Tout manquement|articles L 335|"
    r"\d+\s*/\s*\d+\s*$|^\d{2}/\d{2}/\d{4}\s*$|^Date\s*:)",
)

# Mermaid transcriptions of the canonical domain data-model (ER) diagrams.
# Keyed by 1-based PDF page; emitted next to the rendered figure so the model
# diagrams are searchable as text. Cardinalities transcribed from the figures.
MERMAID = {
    366: """```mermaid
erDiagram
    EF_BS02["EF_BS02 Bénéficiaire"] ||--|| EF_BS01["EF_BS01 Venue"] : a
    EF_BS02 ||--o| EF_BS06["EF_BS06 Accidents de droits communs"] : a
    EF_BS02 ||--o| EF_BS08["EF_BS08 Organisme AT par défaut"] : a
    EF_BS08 ||--o| EF_BS07["EF_BS07 Période AT par défaut"] : a
    EF_BS02 ||--o{ EF_BS09["EF_BS09 Accident du travail déclaré"] : a
    EF_BS09 ||--o| EF_BS11["EF_BS11 Période AT"] : a
    EF_BS09 ||--o| EF_BS10["EF_BS10 Organisme gestionnaire de l AT"] : a
    EF_BS02 ||--|| EF_BS16["EF_BS16 Maternité"] : a
    EF_BS02 ||--o| EF_BS24["EF_BS24 Organisme AMO maternité"] : a
    EF_BS24 ||--o{ EF_BS25["EF_BS25 Période maternité"] : a
    EF_BS02 ||--o{ EF_BS12["EF_BS12 Exonération du TM"] : a
    EF_BS12 ||--|{ EF_BS13["EF_BS13 Période ETM"] : a
    EF_BS02 ||--o{ EF_BS22["EF_BS22 Contrat particulier"] : a
    EF_BS22 ||--o{ EF_BS23["EF_BS23 Période contrat particulier"] : a
    EF_BS02 ||--|| EF_BS03["EF_BS03 Assuré"] : a
    EF_BS03 ||--o| EF_BS04["EF_BS04 Organisme AMO maladie"] : a
    EF_BS04 ||--|{ EF_BS05["EF_BS05 Période droits AMO"] : a
    EF_BS03 ||--o{ EF_BS14["EF_BS14 Modulation du TM"] : a
    EF_BS14 ||--|{ EF_BS15["EF_BS15 Période MTM"] : a
    EF_BS02 ||--o| EF_BS17["EF_BS17 Médecin Traitant"] : a
    EF_BS17 ||--o| EF_BS18["EF_BS18 Période MTT"] : a
    EF_BS02 ||--o{ EF_BS19["EF_BS19 Situation Particulière"] : a
    EF_BS19 ||--|{ EF_BS20["EF_BS20 Période SP"] : a
    EF_BS02 ||--o{ EF_BS21["EF_BS21 Organisme Complémentaire"] : a
```""",
    367: """```mermaid
erDiagram
    EF_IP05["EF_IP05 Prestation"] ||--o| EF_IP01["EF_IP01 Prescription"] : a
    EF_IP01 ||--|{ EF_IP02["EF_IP02 Professionnel de Santé (prescripteur)"] : a
    EF_IP01 ||--|| EF_IP17["EF_IP17 Etablissement de rattachement (prescripteur)"] : a
    EF_IP05 ||--|| EF_IP03["EF_IP03 Professionnel de Santé exécutant"] : a
    EF_IP03 ||--o{ EF_IP15["EF_IP15 Etablissement de rattachement (exécutant)"] : a
    EF_IP05 ||--|| EF_IP16["EF_IP16 Lieu d exécution de la prestation"] : a
    EF_IP05 ||--|| EF_IP14["EF_IP14 Contexte de l entente préalable"] : a
    EF_IP05 ||--o{ EF_IP13["EF_IP13 Prestation Médicament"] : "est une"
    EF_IP05 ||--o{ EF_IP11["EF_IP11 Prestation NABM"] : "est une"
    EF_IP05 ||--o{ EF_IP08["EF_IP08 Prestation CCAM"] : "est une"
    EF_IP05 ||--o{ EF_IP06["EF_IP06 Prestation NGAP"] : "est une"
    EF_IP05 ||--o{ EF_IP12["EF_IP12 Prestation LPP"] : "est une"
    EF_IP08 ||--|| EF_IP07["EF_IP07 Contexte tarifaire CCAM"] : a
    EF_IP08 ||--o{ EF_IP10["EF_IP10 CCAM-Dentaire (0..16)"] : a
    EF_IP08 ||--o{ EF_IP09["EF_IP09 CCAM-Modificateur (0..4)"] : a
```""",
    368: """```mermaid
erDiagram
    %% CF - Contexte de facturation de niveau prestation (regroupement)
    NIV_PRESTATION["Contexte de facturation de niveau prestation"] ||--|| EF_CF01["EF_CF01 Date de référence AMO"] : a
    NIV_PRESTATION ||--|| EF_CF02["EF_CF02 Contexte AMO du Bénéficiaire"] : a
    NIV_PRESTATION ||--|| EF_CF04["EF_CF04 Contexte de la prestation"] : a
    NIV_PRESTATION ||--|| EF_CF03["EF_CF03 Contexte du parcours de soins"] : a
    NIV_PRESTATION ||--|| EF_CF05["EF_CF05 Complément de prestations"] : a
    EF_CF02 ||--o{ EF_CF10["EF_CF10 Situation particulière valide à la date de référence"] : a
    EF_CF02 ||--o{ EF_CF11["EF_CF11 ETM valide à la date de référence"] : a
    EF_CF02 ||--o{ EF_CF12["EF_CF12 MTM valide à la date de référence"] : a
    EF_CF02 ||--o{ EF_CF13["EF_CF13 Contrat particulier valide à la date de référence"] : a
    EF_CF05 ||--o| EF_CF06["EF_CF06 Détails complément Forfait Technique"] : a
    EF_CF05 ||--o{ EF_CF07["EF_CF07 Etablissement (exécutant / exploitant)"] : a
    %% CF - Contexte de facturation de niveau Facture (regroupement)
    NIV_FACTURE["Contexte de facturation de niveau Facture"] ||--|| EF_CF08["EF_CF08 Contexte AMO facture"] : a
    NIV_FACTURE ||--|| EF_CF09["EF_CF09 Contexte du Facturant"] : a
```

```mermaid
erDiagram
    %% VF - Valoriser les prestations de la facture
    EF_VF01["EF_VF01 Regroupement de prestations"] ||--|{ EF_VF01 : "est liée à"
    EF_VF01 ||--|| EF_VF02["EF_VF02 Informations Financières"] : a
    EF_VF01 ||--|| EF_VF03["EF_VF03 Base de remboursement"] : a
    EF_VF01 ||--|| EF_VF04["EF_VF04 Taux de Remboursement AMO"] : a
    EF_VF01 ||--|| EF_VF05["EF_VF05 Montant remboursable"] : a
    EF_VF01 ||--|| EF_VF06["EF_VF06 Code participation assuré"] : a
```""",
}


HEADING_INLINE = re.compile(r"^(\d+(?:\.\d+){0,4})\s+(\S.*)$")
HEADING_NUM = re.compile(r"^(\d+(?:\.\d+){0,4})\.?$")
DOTLEADER = re.compile(r"\.{4,}")


def is_boiler(line: str) -> bool:
    s = line.strip()
    if not s:
        return True
    if DOTLEADER.search(s):  # table-of-contents dotted leaders
        return True
    if s.upper() == "SOMMAIRE":
        return True
    return bool(BOILER.match(s))


def heading_level(num: str) -> int:
    return min(num.count(".") + 1, 4)


def page_to_md(page) -> list[str]:
    """Return markdown lines for a content page, detecting numbered headings.

    Headings are emitted as bold-large lines. The section number and its title
    are often on separate lines, so a lone number line is merged with the
    following bold-large title line(s).
    """
    # Flatten to visual lines with style info.
    rows = []  # (text, bold, size)
    for b in page.get_text("dict")["blocks"]:
        for ln in b.get("lines", []):
            spans = [s for s in ln["spans"] if s["text"].strip()]
            if not spans:
                continue
            text = "".join(s["text"] for s in ln["spans"]).rstrip()
            first = spans[0]
            rows.append((text, "Bold" in first["font"], first["size"]))

    out = []
    i = 0
    while i < len(rows):
        text, bold, size = rows[i]
        s = text.strip()
        if is_boiler(text):
            i += 1
            continue
        big = bold and size >= 11.5
        # Case A: "2.2  Title" on one line.
        m = HEADING_INLINE.match(s)
        if big and m and not HEADING_NUM.match(s):
            lvl = heading_level(m.group(1))
            out += ["", "#" * (lvl + 1) + f" {m.group(1)} {m.group(2).strip()}", ""]
            i += 1
            continue
        # Case B: lone number line, merge with following big lines as title.
        mn = HEADING_NUM.match(s)
        if big and mn:
            num = mn.group(1)
            title_parts = []
            j = i + 1
            while j < len(rows):
                t2, b2, sz2 = rows[j]
                if b2 and sz2 >= 11.5 and t2.strip() and not HEADING_NUM.match(t2.strip()) \
                        and not is_boiler(t2):
                    title_parts.append(t2.strip())
                    j += 1
                else:
                    break
            if title_parts:
                lvl = heading_level(num)
                out += ["", "#" * (lvl + 1) + f" {num} {' '.join(title_parts)}", ""]
                i = j
                continue
        out.append(text)
        i += 1
    return out


def is_figure_page(page) -> bool:
    dr = len(page.get_drawings())
    # count non-trivial raster images (skip tiny logos by area)
    big_img = 0
    for img in page.get_images(full=True):
        try:
            w, h = img[2], img[3]
        except Exception:
            w = h = 0
        if w * h > 60000:
            big_img += 1
    return dr >= 40 or big_img >= 1


def caption_for(page) -> str:
    """Best-effort caption from a 'Schéma…/Diagramme…/Figure…' bold line."""
    for b in page.get_text("dict")["blocks"]:
        for ln in b.get("lines", []):
            txt = "".join(s["text"] for s in ln["spans"]).strip()
            if re.match(r"^(Schéma|Diagramme|Figure|Workflow|Processus|Diagramme d)", txt, re.I):
                return txt[:160]
    return ""


def main():
    OUT.mkdir(exist_ok=True)
    FIG.mkdir(exist_ok=True)
    doc = fitz.open(PDF)
    n = doc.page_count
    bounds = [(s[0], SECTIONS[i + 1][0] - 1 if i + 1 < len(SECTIONS) else n, s[1], s[2])
              for i, s in enumerate(SECTIONS)]

    index = ["# FIDES ACE — Spécifications Fonctionnelles Générales (v06.08)",
             "",
             "> Source : `SFG_FIDES_ACE_V06.08_version_fusionnée.pdf` (380 pages).",
             "> Documentation découpée par domaine fonctionnel pour servir de contexte de développement.",
             "",
             "## Domaines fonctionnels", ""]

    figdense = re.compile(r"")  # placeholder
    fig_count = 0
    for (start, end, slug, title) in bounds:
        lines = [f"# {title}", "", f"_Pages {start}–{end} du PDF source._", ""]
        sec_figs = 0
        for pno in range(start, end + 1):
            page = doc[pno - 1]
            md = page_to_md(page)
            # drop pages that became empty after de-boilerplating
            body = [l for l in md if l.strip()]
            if body:
                lines.append(f"\n<!-- p.{pno} -->")
                lines.extend(md)
            if is_figure_page(page):
                pix = page.get_pixmap(dpi=130)
                fname = f"p{pno:03d}.png"
                pix.save(str(FIG / fname))
                cap = caption_for(page) or f"Schéma / diagramme page {pno}"
                lines.append("")
                lines.append(f"![{cap}](figures/{fname})")
                lines.append(f"*Figure (p.{pno}) : {cap}*")
                if pno in MERMAID:
                    lines.append("")
                    lines.append("> Transcription Mermaid (depuis la figure ci-dessus) :")
                    lines.append("")
                    lines.append(MERMAID[pno])
                lines.append("")
                sec_figs += 1
                fig_count += 1
        (OUT / f"{slug}.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
        index.append(f"- [{title}]({slug}.md) — pages {start}–{end}, {sec_figs} figure(s)")
        print(f"wrote {slug}.md  pages {start}-{end}  figures={sec_figs}")

    # Append the detailed DICO sub-TOC for quick lookup.
    index += ["", "## Repères (commandes utiles)", "",
              "- Recherche plein-texte : `grep -ri \"<terme>\" docs/`",
              "- Les figures (schémas, diagrammes de données, workflows) sont dans `docs/figures/`.",
              f"- Total figures extraites : {fig_count}.", ""]
    (OUT / "INDEX.md").write_text("\n".join(index) + "\n", encoding="utf-8")
    print(f"\nTotal figures: {fig_count}")
    print("Done.")


if __name__ == "__main__":
    main()
