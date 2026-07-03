# FIDES ACE — Spécifications Fonctionnelles Générales (v06.09)

> Source : `SFG_FIDES_ACE_V06.09_version_fusionnée.pdf` (374 pages).
> Documentation découpée par domaine fonctionnel pour servir de contexte de développement.

## Domaines fonctionnels

- [PG — Présentation Générale](01-PG-presentation-generale.md) — pages 1–42, 12 figure(s)
- [BS — Acquérir les informations du Bénéficiaire des Soins](02-BS-beneficiaire-des-soins.md) — pages 43–83, 4 figure(s)
- [IP — Acquérir les Informations des Prestations](03-IP-informations-prestations.md) — pages 84–146, 8 figure(s)
- [CF — Déterminer le Contexte de Facturation](04-CF-contexte-facturation.md) — pages 147–200, 6 figure(s)
- [VF — Valoriser les prestations de la Facture](05-VF-valoriser-prestations.md) — pages 201–299, 17 figure(s)
- [TF — Transmettre les Factures](06-TF-transmettre-factures.md) — pages 300–349, 7 figure(s)
- [DICO — Dictionnaire de données](07-DICO-dictionnaire-donnees.md) — pages 350–374, 5 figure(s)

## Repères (commandes utiles)

- Recherche plein-texte : `grep -ri "<terme>" reference/`
- Les figures (schémas, diagrammes de données, workflows) sont dans `reference/figures/` : **59 diagrammes** conservés.
- Le script `build_docs.py` (détection de figures par légende) repère 62 diagrammes ; la doc versionnée en conserve 59 (sous-ensemble curé).
- Les pages auto-détectées comme « figures » mais ne contenant que du texte/des tableaux ont été **transcrites en Markdown** dans les fichiers de domaine (repérables par `<!-- transcrit de p.NNN (ex-figure) -->`) puis leur PNG écarté.
- Total figures conservées : 59.
