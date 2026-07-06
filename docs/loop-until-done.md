# Loop Until Done

Ce skill force l'agent IA à travailler en **boucle itérative auto-évaluée** jusqu'à ce que le résultat atteigne un niveau de qualité strict. Inspiré du Karpathy Loop (AutoResearch) et du paper "Bilevel Autoresearch".

## Cas d'usage

- **Code de qualité production** : générer du code qui doit être correct, performant et bien typé
- **Documentation exhaustive** : ADR, specs techniques, guides utilisateur
- **Architecture** : concevoir des systèmes qui satisfont plusieurs contraintes simultanées
- **Rédaction** : articles, présentations, emails importants nécessitant plusieurs passes

## Déclenchement

Ce skill s'active quand vous :
- Dites **"loop until done"** / **"itère jusqu'à ce que ce soit bon"** / **"boucle jusqu'à satisfaction"**
- Demandez une qualité stricte avec des critères explicites
- Utilisez les phrases : **"don't stop until it's right"** / **"be strict with yourself"** / **"keep improving"**

## Comment ça fonctionne

L'agent entre dans une boucle structurée à 4 phases :

```
PLAN   → Identifie la prochaine amélioration à faire
DO     → Produit ou améliore le travail
VERIFY → Note chaque critère de 1 à 10 (honnêtement)
DECIDE → Tout est 8+ ? FINAL. Sinon ? ITERATING.
```

### Règles strictes

- Ne jamais déclarer "terminé" tant qu'un critère est sous 8/10
- Chaque passe corrige le point le plus faible en priorité
- Maximum 7 itérations (sécurité anti-boucle infinie)
- Pas de questions posées — l'agent fait des hypothèses raisonnables

## Critères par défaut (si non fournis)

| Type de tâche | Critères inférés |
|---------------|-----------------|
| Code | Correction, lisibilité, edge cases, performance, style idiomatique |
| Documentation | Complétude, clarté, exactitude, structure, actionnabilité |
| Architecture | Scalabilité, séparation des responsabilités, simplicité, extensibilité |
| Rédaction | Clarté, concision, engagement, exactitude, structure |

## Exemple

```
Utilisateur : "Loop until done — écris un utilitaire TypeScript de retry
avec backoff exponentiel.

Critères :
- Gère tous les types d'erreurs
- Configurable (max retries, délai, jitter)
- Bien typé avec génériques
- Documenté avec JSDoc
- Supporte l'annulation"

Agent :
--- ITERATION 1 ---
PLAN: Produire le premier draft complet
DO: [code...]
VERIFY:
- Gestion erreurs: 7/10 — manque le cas AbortError
- Configurable: 8/10
- Typage: 6/10 — le générique ne propage pas le type retour
- JSDoc: 5/10 — seulement la fonction principale documentée
- Annulation: 3/10 — pas encore implémenté
Weakest: Annulation (3/10)
DECIDE: ITERATING — ajout du support AbortSignal

--- ITERATION 2 ---
[continue jusqu'à FINAL...]
```

## Avantages

- **Qualité garantie** : force l'agent à ne pas se contenter du premier jet
- **Transparence** : scoring visible à chaque itération
- **Progression** : chaque passe améliore objectivement le résultat
- **Autonomie** : pas de va-et-vient manuel nécessaire

## Limites

- **Coût en tokens** : 3-7 itérations consomment plus qu'une réponse unique
- **Auto-évaluation** : l'agent note son propre travail (biais possible)
- **Pas un substitut aux tests** : pour du code, combiner avec de vrais tests automatisés

## Conseils

- Fournissez des critères explicites pour de meilleurs résultats
- Combinez avec un second agent reviewer pour séparer le créateur du vérificateur
- Pour les tâches complexes, décomposez en sous-tâches avant d'appliquer la boucle
