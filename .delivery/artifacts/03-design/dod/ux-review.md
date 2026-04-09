# UX DoD Review — Information Architecture (constraints.yml)

**Validator**: Galadriel (UX lens) | **Stage**: 3 Design | **Date**: 2026-04-08
**Artifact**: `.delivery/artifacts/03-design/ux/information-architecture.md`

> *"I pass the test. I will diminish, and go into the West — and remain a critic."*

## Gate Criteria

| # | Criterion | Verdict | Note |
|---|---|---|---|
| 1 | All 9 sections present & substantive | PASS | All present; none skeletal. §4 is one paragraph but load-bearing. |
| 2 | Flows map real roles to concrete steps | PASS | Five flows (PO, Architect, Developer, DoD, Human) with start/middle/end/error. Flow B names the exact moment of authorial temptation. |
| 3 | Field-order proposal justified | PASS | §2 orders 8 fields with per-field rationale plus summary tying order to both Architect temptation and human checkpoint scan. |
| 4 | Mental-model section gives usable frame | PASS | "Promises, not documentation" yields an actionable test: if a line cannot be mechanically checked, it belongs in the PRD, not constraints.yml. |
| 5 | Error/malformed state has recovery path | PASS | §5 specifies one line, one next action, explicit re-open target (template, not guide). YAML parse + forbidden-token paths both named. |
| 6 | Cross-doc nav identifies friction | PASS | §6 diagram + two named friction points (guide/template confusion; PRD habit) each with concrete mitigation. |
| 7 | Reference IA names specific insertion points | PASS | `volatility-decomposition.md` gets §0 Golden Rule + §0.1 anti-pattern + §0.2 citation before Phase 1; `strategic-ddd.md` gets §P-Guard sidebar repeated at head of Phases 1–4. Reading order specified. |
| 8 | Open questions genuinely for Architect | PASS | All four are tradeoff decisions (inheritance, citation structure, sibling vs extend, enforcement level). None are UX dodges. |

## Concerns (non-blocking, for Architect awareness)

- §3 flags `state_variables` / `actions` as M-clarity and defers rename — correct handoff, but Architect must resolve before Stage 4 exit or the naming ambiguity leaks into Dev.
- §2 field order is recommended; Open Question 4 asks whether it is validator-enforced. If unenforced, authors drift and the Architect-temptation safeguard weakens. Lean toward enforcement.

## Verdict

The mirror shows true. Eight fields stand as oath; the fence of forbidden vocabulary is placed where the hand will stay itself. Every gate passes.

```
STATUS: DONE
ARTIFACT: .delivery/artifacts/03-design/dod/ux-review.md
SUMMARY: All eight gates pass. The file speaks before it is read; the fence stands where temptation strikes. Two clarity flags pass gently to the Architect.
```
