# FIDES ACE — Spécification fonctionnelle

## Vue d'ensemble

Le skill FIDES ACE donne aux agents IA un accès navigable à la **spécification fonctionnelle générale FIDES ACE v06.08** (SFG FIDES — Facturation Individuelle Des Établissements de Santé, Actes et Consultations Externes, GIE SESAM-Vitale, ~380 pages). Le PDF source a été converti en Markdown chunké + figures pour permettre une lecture ciblée section par section.

## Ce qu'il fait

- **Route** les questions vers le bon domaine fonctionnel via `INDEX.md`
- **Recherche** un terme dans la documentation (`grep` sur `reference/`)
- **Explique** les entités fonctionnelles, règles de valorisation, contexte de facturation et flux de transmission
- **Cite** la page source du PDF et affiche les figures/diagrammes associés

## Quand l'utiliser

Utilisez ce skill quand vous avez besoin de :

- Comprendre la facturation FIDES ACE et son processus global
- Explorer un domaine fonctionnel (BS, IP, CF, VF, TF)
- Consulter une entité de données (`EF_BS02`, `EF_VF01`, etc.)
- Comprendre les règles de valorisation (base de remboursement, taux AMO, ticket modérateur)
- Analyser le contexte de facturation ou les flux de transmission des factures (ARL/RSP)
- Retrouver un diagramme de données ou un schéma de workflow

## Contenu de la documentation

| Fichier | Domaine | Contenu |
|---------|---------|---------|
| `01-PG-presentation-generale.md` | PG — Présentation Générale | Cadre, acteurs, flux EPS/PNL, vue d'ensemble |
| `02-BS-beneficiaire-des-soins.md` | BS — Bénéficiaire des Soins | Identification, couverture AMO, C2S/AME, `EF_BS01`…`EF_BS25` |
| `03-IP-informations-prestations.md` | IP — Informations des Prestations | Prescription, CCAM/NGAP/NABM/LPP, `EF_IP01`…`EF_IP17` |
| `04-CF-contexte-facturation.md` | CF — Contexte de Facturation | Contexte AMO, parcours de soins, `EF_CF01`…`EF_CF13` |
| `05-VF-valoriser-prestations.md` | VF — Valoriser les prestations | Base de remboursement, taux AMO, `EF_VF01`…`EF_VF06` |
| `06-TF-transmettre-factures.md` | TF — Transmettre les Factures | Lots/fichiers, émission, retours ARL/RSP |
| `07-DICO-dictionnaire-donnees.md` | DICO — Dictionnaire de données | Diagrammes de données (Mermaid + figures), abréviations |

Les figures (schémas, diagrammes, workflows) sont dans `reference/figures/pNNN.png`, la page source du PDF étant indiquée dans le Markdown par `<!-- p.NNN -->`.

## Conventions

- **Entités fonctionnelles** : `EF_<DOMAINE><NN>` (ex. `EF_BS02`, `EF_VF01`)
- **Sous-fonctions** : codifiées par domaine (ex. `BS30`, `BS31`)
- **Acronymes** : AMO (Assurance Maladie Obligatoire), TM (Ticket Modérateur), ETM (Exonération du TM), MTT (Médecin Traitant), ARL (Accusé de Réception Logique), RSP (Retour Sécurité Paiement), EPS/PNL (Établissement Public de Santé / Privé Non Lucratif)

## Procédure recommandée

1. Lire `reference/INDEX.md` pour identifier le domaine
2. `grep` le terme dans `reference/`
3. Ouvrir uniquement la section pertinente
4. Ouvrir la figure `reference/figures/pNNN.png` si un schéma est nécessaire
