---
name: loop-until-done
description: "Force l'agent a travailler en boucle iterative avec auto-evaluation stricte jusqu'a ce que tous les criteres de qualite soient atteints (score 8+/10). Inspire du Karpathy Loop."
version: 1.0.0
license: MIT
metadata:
  author: Foundation Skills
---

# Loop Until Done

This skill forces the AI to work in a self-evaluating iterative loop until the output meets a strict quality bar. Instead of producing a single-shot answer, the agent plans, executes, scores its own work against explicit criteria, and iterates on the weakest point until every criterion scores 8 or higher.

Inspired by Andrej Karpathy's AutoResearch loop and the "Bilevel Autoresearch" paper — applying the principle that repetition with honest self-evaluation produces dramatically better results than single-pass generation.

## When to Use This Skill

Activate when the user:
- Says "loop until done", "iterate until perfect", "keep improving until it's good"
- Asks for high-quality output that must meet specific criteria
- Wants exhaustive refinement without manual back-and-forth
- Needs production-grade deliverables (documentation, code, architecture, specs)
- Says "don't stop until it's right" or "be strict with yourself"

## How It Works

The agent enters a structured loop with four phases per iteration:

```
+-------------------------------------------+
|  1. PLAN   - Identify the single next     |
|               improvement to make          |
|  2. DO     - Produce or improve the work   |
|  3. VERIFY - Score each criterion 1-10     |
|               List what is still weak      |
|  4. DECIDE - All 8+? -> FINAL and stop     |
|               Otherwise -> ITERATING       |
|               Fix weakest point first      |
+-------------------------------------------+
```

## Workflow

### Step 1: Define the Task and Criteria

When the user provides a task, extract or define:
- **TASK**: What exactly must be produced
- **SUCCESS CRITERIA**: 3-7 measurable criteria the output must satisfy

If the user does not provide explicit criteria, infer strict criteria appropriate to the task type:
- For **code**: correctness, readability, edge-case handling, performance, idiomatic style
- For **documentation**: completeness, clarity, accuracy, structure, actionability
- For **architecture**: scalability, separation of concerns, simplicity, extensibility
- For **writing**: clarity, conciseness, engagement, accuracy, structure

### Step 2: Execute the Loop

Apply the following protocol on every turn:

```
LOOP PROTOCOL -- repeat every turn:

1. PLAN
   - State the single next step to improve the work.
   - On the first pass, this is producing the initial draft.
   - On subsequent passes, this targets the weakest criterion.

2. DO
   - Produce or improve the work.
   - Make meaningful changes -- do not make cosmetic tweaks
     to inflate scores.

3. VERIFY
   - Score the result 1-10 on EACH criterion.
   - Be brutally honest. Err on the side of harsh.
   - List exactly what is still weak or missing.
   - A score of 10 means professional-grade, publishable as-is.
   - A score of 7 means "okay but not good enough".
   - A score of 5 means "significant gaps remain".

4. DECIDE
   - If EVERY criterion is 8 or higher -> print FINAL and stop.
   - Otherwise -> print ITERATING and go again,
     fixing the weakest score first.
```

### Step 3: Rules (Strictly Enforced)

- **Never call it done** until every criterion is 8 or higher.
- **Each pass must fix the weakest score** from the last VERIFY.
- **Do not ask questions**. Make a sensible assumption and keep going.
- **Do not inflate scores**. If something is mediocre, score it mediocre.
- **Maximum iterations**: 7. If after 7 passes some criteria are still below 8, print BEST EFFORT with a clear explanation of what remains weak and why.
- **Show your scoring** every iteration so the user can follow progress.

## Output Format

Each iteration should be clearly labeled:

```
--- ITERATION 1 ---

PLAN: [what you will do]

DO:
[the actual work output]

VERIFY:
- Criterion 1: [score]/10 -- [brief justification]
- Criterion 2: [score]/10 -- [brief justification]
- Criterion 3: [score]/10 -- [brief justification]
Weakest point: [what needs the most improvement]

DECIDE: ITERATING -- fixing [weakest point]

--- ITERATION 2 ---
...
```

Final output:

```
--- ITERATION N ---

PLAN: [final refinement]

DO:
[final polished output]

VERIFY:
- Criterion 1: 9/10 -- [justification]
- Criterion 2: 8/10 -- [justification]
- Criterion 3: 9/10 -- [justification]

DECIDE: FINAL -- All criteria met.
```

## Examples

### Example 1: Code Generation

```
User: Loop until done -- write a TypeScript retry utility with exponential backoff.

Success criteria:
- Handles all error types gracefully
- Configurable (max retries, base delay, jitter)
- Well-typed with generics
- Has JSDoc documentation
- Handles abort/cancellation
```

The agent will iterate: first draft -> score -> identify weakest (e.g., missing cancellation support) -> add it -> re-score -> repeat until all 8+.

### Example 2: Documentation

```
User: Loop until done -- write an ADR for migrating from REST to GraphQL.

(Agent infers criteria: completeness, clarity, decision justification,
alternatives analysis, consequences documented)
```

### Example 3: Architecture Design

```
User: Loop until done -- design a message queue architecture for our
order processing system. Criteria: handles 10k msg/s, at-least-once
delivery, dead letter queue, monitoring, simple to operate.
```

## Important Notes

- This skill trades speed for quality. A single pass takes one turn; the loop may take 3-7 turns. Use it when quality matters more than speed.
- The agent grades its own work -- this is an inherent limitation. The scores are directional, not absolute. The value comes from forced iteration, not perfect scoring.
- For even better results, combine with a second reviewer agent (sub-agent pattern) to separate the maker from the checker.
- The 7-iteration cap prevents infinite loops and token waste. If the task genuinely cannot reach 8/10 in 7 passes, it may need to be decomposed into smaller tasks.
- When used inside a CI/CD or automation context, the VERIFY step can be replaced with actual test results, lint scores, or build status -- making the loop objective rather than self-assessed.
