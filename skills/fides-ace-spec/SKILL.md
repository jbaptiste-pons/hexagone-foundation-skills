---
name: fides-ace-spec
description: "Navigue et interroge la spécification fonctionnelle FIDES ACE (SFG FIDES — Facturation Individuelle Des Établissements de Santé, Actes et Consultations Externes, v06.08, GIE SESAM-Vitale). À utiliser quand l'utilisateur pose des questions sur la facturation FIDES, les domaines fonctionnels BS / IP / CF / VF / TF, les entités de données (EF_BS, EF_IP, EF_CF, EF_VF), les règles de valorisation, le contexte de facturation, les flux de transmission des factures, ou le dictionnaire de données FIDES. La doc est découpée en Markdown + figures dans le dépôt — ne pas répondre de mémoire."
version: 1.0.0
license: Proprietary
metadata:
  author: dedalus-erp-pas
  source-pdf: "SFG_FIDES_ACE_V06.08_version_fusionnée.pdf"
  docs-root: reference
allowed-tools: Read Grep Glob
---

# FIDES ACE — Spécifications Fonctionnelles Générales (navigation)

Ce skill donne accès à la **spécification fonctionnelle FIDES ACE v06.08** (GIE SESAM-Vitale, 380 pages) convertie en Markdown chunké + figures. Ton rôle est de **lire l'index puis la(les) section(s) pertinente(s)** avant de répondre — pas de répondre de mémoire.

## Emplacement de la doc

```
DOCS_ROOT = reference   # chemin relatif à ce skill (skills/fides-ace-spec/reference)
```

- `INDEX.md` — routeur : liste des domaines fonctionnels et plages de pages.
- `NN-<slug>.md` — un fichier par domaine fonctionnel.
- `figures/pNNN.png` — schémas, diagrammes de données et workflows rendus depuis le PDF (la page source est indiquée par `<!-- p.NNN -->` dans le Markdown et par le nom de fichier).

## Procédure (toujours dans cet ordre)

1. **Lire `reference/INDEX.md`** pour identifier le(s) domaine(s) concerné(s).
2. **Grep** le terme dans `reference/` pour localiser la/les section(s) :
   `grep -rin "<terme>" reference`
3. **Ouvrir uniquement** le(s) fichier(s) de section pertinent(s) (ne pas tout charger).
4. Pour un schéma/diagramme, **ouvrir la figure** `reference/figures/pNNN.png` correspondante. Les 4 diagrammes de données canoniques (DICO §3.1–3.4) ont aussi une **transcription Mermaid** dans `07-DICO-dictionnaire-donnees.md`.

## Carte des domaines fonctionnels

| Fichier | Domaine | Contenu |
|---|---|---|
| `01-PG-presentation-generale.md` | **PG** — Présentation Générale | Cadre, acteurs, flux d'échange (EPS / PNL), évolutions réglementaires, vue d'ensemble du processus. |
| `02-BS-beneficiaire-des-soins.md` | **BS** — Bénéficiaire des Soins | Identification du bénéficiaire, couverture AMO, médecin traitant, situations particulières, C2S/AME. Entités `EF_BS01`…`EF_BS25`. |
| `03-IP-informations-prestations.md` | **IP** — Informations des Prestations | Prescription, prestations CCAM/NGAP/NABM/LPP/Médicament, professionnels exécutant/prescripteur. Entités `EF_IP01`…`EF_IP17`. |
| `04-CF-contexte-facturation.md` | **CF** — Contexte de Facturation | Contexte AMO, parcours de soins, contexte de niveau prestation et niveau facture. Entités `EF_CF01`…`EF_CF13`. |
| `05-VF-valoriser-prestations.md` | **VF** — Valoriser les prestations | Base de remboursement, taux AMO, montant remboursable, participation assuré, règles de valorisation. Entités `EF_VF01`…`EF_VF06`. |
| `06-TF-transmettre-factures.md` | **TF** — Transmettre les Factures | Mise en forme, lots/fichiers, émission des messages, réception des retours (ARL/RSP). |
| `07-DICO-dictionnaire-donnees.md` | **DICO** — Dictionnaire de données | Diagrammes de données par domaine (Mermaid + figures), listes des données, abréviations. |

## Conventions utiles

- Les **entités fonctionnelles** sont codifiées `EF_<DOMAINE><NN>` (ex. `EF_BS02` = Bénéficiaire, `EF_VF01` = Regroupement de prestations).
- Les **sous-fonctions** sont codifiées par domaine (ex. `BS30`, `BS31`… dans le domaine BS).
- Chaque page source du PDF est balisée `<!-- p.NNN -->` pour retrouver la figure et citer la page.
- Acronymes fréquents : AMO (Assurance Maladie Obligatoire), TM (Ticket Modérateur), ETM (Exonération du TM), MTT (Médecin Traitant), CCAM/NGAP/NABM/LPP (nomenclatures), ARL (Accusé de Réception Logique), RSP (Retour Sécurité Paiement), EPS/PNL (Établissement Public de Santé / Privé Non Lucratif).

## Régénérer la doc

La doc a été générée depuis le PDF source (non versionné dans ce dépôt) via le script
`reference/build_docs.py` conservé pour référence. Pour régénérer, replacer le PDF source à
côté du script puis :

```bash
cd skills/fides-ace-spec/reference && python build_docs.py
```

> ⚠️ **Attention** : `build_docs.py` régénère tout depuis le PDF et **écrase** les fichiers
> Markdown. Sa détection de figures sur-déclenche (les tableaux dessinés en vectoriel sont
> pris pour des diagrammes), ce qui réintroduirait ~234 PNG et **supprimerait les tableaux
> transcrits à la main** (repérables par `<!-- transcrit de p.NNN (ex-figure) -->`). Ne
> relancer que sur une copie, puis reporter manuellement les transcriptions, ou corriger
> d'abord `is_figure_page()` pour exclure les pages purement tabulaires.
