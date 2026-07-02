# FIDES ACE — Spécifications Fonctionnelles Générales (v06.08)

> Source : `SFG_FIDES_ACE_V06.08_version_fusionnée.pdf` (380 pages).
> Documentation découpée par domaine fonctionnel pour servir de contexte de développement.

## Domaines fonctionnels

- [PG — Présentation Générale](01-PG-presentation-generale.md) — pages 1–42, 12 figure(s)
- [BS — Acquérir les informations du Bénéficiaire des Soins](02-BS-beneficiaire-des-soins.md) — pages 43–86, 4 figure(s)
- [IP — Acquérir les Informations des Prestations](03-IP-informations-prestations.md) — pages 87–153, 8 figure(s)
- [CF — Déterminer le Contexte de Facturation](04-CF-contexte-facturation.md) — pages 154–203, 6 figure(s)
- [VF — Valoriser les prestations de la Facture](05-VF-valoriser-prestations.md) — pages 204–304, 17 figure(s)
- [TF — Transmettre les Factures](06-TF-transmettre-factures.md) — pages 305–355, 7 figure(s)
- [DICO — Dictionnaire de données](07-DICO-dictionnaire-donnees.md) — pages 356–380, 5 figure(s)

## Repères (commandes utiles)

- Recherche plein-texte : `grep -ri "<terme>" docs/`
- Les figures restantes (schémas, diagrammes de données, workflows) sont dans `docs/figures/` : **59 vrais diagrammes** conservés.
- Les pages auto-détectées comme « figures » mais ne contenant que du texte/des tableaux ont été **transcrites en Markdown** dans les fichiers de domaine (repérables par `<!-- transcrit de p.NNN (ex-figure) -->`) puis leur PNG supprimé.
- Total figures conservées : 59 (sur 234 extraites initialement).
