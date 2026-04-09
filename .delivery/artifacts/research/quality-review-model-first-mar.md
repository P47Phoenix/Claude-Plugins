# QA Review: Model-First Reasoning & Multi-Agent Reflexion

**Reviewer**: QA Engineer (delivery-team:quality) | **Date**: 2026-04-08
**Papers**: arXiv:2512.14474 (Model-First), arXiv:2512.20845 (MAR)

## 1. Model-First Reasoning — Constraint Violations

**Do agents violate their own stated constraints today?** Yes, and memory proves it.
- `memory/stages/plan.md`: "Plan has the lowest first-try pass rate (57%, 4/7 runs). Three of seven runs required rework for **constraints the agents already knew** (sprint ceiling, mandatory artifacts)." This is a textbook implicit-state-tracking failure — the PRD/config carries the constraint in prose, but the agent doesn't surface it into working state before acting.
- `run-r4x2`: PO proposed a 169% ceiling plan; SM corrected to 3 sprints; adversarial challenger still caught Sprint 1 at 100%. Two rounds to reach an exact-delivery plan against a constraint that was stated upfront.
- `defect-patterns.md` DEFECT-001 "Agent validation gap": correctness was binary (legal/illegal) but the agent inferred instead of checking — same pattern, constraint known, not modeled.

**Would an explicit constraints-model artifact help?** Strongly yes. We already see the fix working piecemeal: "gate-patterns memory injection before Design" produced the first 100% run (r4x2). That is Model-First in miniature — pre-load the constraint set before acting. Formalizing it as a first-class artifact (`constraints.yml` per stage: numeric ceilings, mandatory artifact list, FR IDs, NFR thresholds, ADR invariants) lets DoD validators do **deterministic checks against the model** instead of re-reading prose. This turns several DoD gates from LLM-judged into rule-engine-judged — matching the Business Rules Engine philosophy already enshrined in `prd-quality-gate-flow`.

## 2. MAR — Self-Correction Degeneration

**Direct single-agent degeneration evidence**: **Weak/mixed**. Most round-2 self-corrections in memory actually succeed (k3r9 Plan fixed round 2; h3k7 Plan fixed round 2). Same-agent retry with aggregated findings is mostly working when findings are concrete.

**Indirect / cross-run degeneration**: **Strong**. `team-review/sm-review.md` flags "Installed-vs-source sync gap: recurring 3 times, not systemically fixed" and "Stale derived artifacts keep recurring — c8f2 first logged it, p5v8 hit it again." These are the macro-scale equivalent of MAR's "degeneration of thought": the same mental model keeps producing the same blind spot even after being told. A different-persona reflection pass (route iteration-2 correction through an alias from a different theme, or through the challenger instead of the original author) is directly applicable here — especially for stages with ≥2 historical round-2 occurrences.

## 3. Testability (A/B on `.delivery/memory/`)

| Paper | A/B design | Metric (exists today) | Success criterion |
|---|---|---|---|
| Model-First | Run same PRD through Refine→Plan with and without `constraints.yml` pre-load | `memory/index.md` stage **first-try pass rate**; `run-*.md` self-correction round count | Plan first-try ≥80% over 5 runs (current 57%); avg correction rounds ↓ |
| MAR | On iteration 2 of any self-correction, route through a different alias/persona vs. same agent | `run-*.md` round-2 success rate; recurrence count in `topics/defect-patterns.md` | Round-2 success ↑; zero 3-peat recurrences |

Both metrics already exist in memory — no new instrumentation needed.

## 4. Verdicts

- **Model-First — ADOPT.** Evidence is overwhelming (57% Plan first-try, 3/7 constraint-rework runs, gate-patterns injection already proves the mechanism). Low cost: add `constraints.yml` artifact + rule-based DoD checks. Highest expected quality lift of any recent proposal.
- **MAR — INVESTIGATE.** Single-round degeneration is not the dominant failure mode, but cross-run recurrence is. Pilot: on 2nd self-correction iteration, swap primary agent to a different alias; measure recurrence reduction over 5 runs before full adoption.

---
**File**: `/var/home/meconnelly/Documents/GitHub/Claude-Plugins/.delivery/artifacts/research/quality-review-model-first-mar.md`
