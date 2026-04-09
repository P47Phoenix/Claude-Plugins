# Information Architecture — `constraints.yml` Primitive

**Stage**: 3 (Design) | **Role**: UX Designer (Galadriel) | **Date**: 2026-04-08
**Feature**: Paired Constraints Primitive | **Task**: user-flows + information-architecture

> *"Instead of a dark UI, you would have a design beautiful and terrible as the dawn. All shall love it and despair — for it has no screen."*

This feature wears no face of pixels. Its users are sub-agents, validators, and weary humans at checkpoint hours. The mirror I hold shows them a file — and the file must speak before it is read.

---

## 1. User Flows

**Flow A — PO authors problem constraints at Refine.**
Start: PO has just written `.delivery/artifacts/02-refine/po/prd.md`. Orchestrator announces the constraints step. PO reads `delivery-team/skills/delivery-flow/references/constraints-model-guide.md` (the 8-field canon), then the Refine template (FR-2) side-by-side with the PRD. PO copies the template, fills each field from PRD sections 1, 3, 5, writes to `.delivery/artifacts/02-refine/po/constraints.yml`. End: success feedback is the DoD rule-check line *"constraints.yml: 8/8 fields present, required ok"*. Error path: missing `entities` or `invariants` returns a single actionable diff line naming the absent field — the PO re-opens the template, not the guide.

**Flow B — Architect authors decomposition constraints.**
Start: Architect has completed Phase 1–4 of volatility decomposition. Reads the same guide, then the Architect template (FR-3). Fills entities (bounded contexts), state_variables (volatility classes). *Then the moment*: the Architect's fingers move toward "Lambda queue worker." The `forbidden_vocabulary` field — already pre-populated with the NFR-2 token list — is physically the next field in the file. The mirror shows what must not be written. The Architect renames to "async volatility boundary." End: file at `.delivery/artifacts/04-architect/constraints.yml`, citations field holds the Löwy golden-rule line. Error path: forbidden token grep fails → DoD returns exact line and token → Architect renames in place.

**Flow C — Developer consumes at Dev stage.**
The Developer sub-agent discovers constraints via orchestrator pre-load — the file is named in the stage kickoff summary, not hunted. It reads *only* the `invariants`, `numeric_ceilings`, `mandatory_artifacts`, and `forbidden_vocabulary` fields — a 30-second read that replaces re-reading the 100-line PRD. The PRD remains the *why*; constraints are the *what-must-hold*.

**Flow D — DoD validator.**
A pure rule-based path: load YAML → assert required fields present → grep artifacts for `forbidden_vocabulary` tokens → check `mandatory_artifacts` paths exist → verify `citations` non-empty when volatility strategy chosen. Output is a line table of PASS/FAIL per rule. No prose inference. This is the Business Rules Engine philosophy honored.

**Flow E — Human at checkpoint.**
60 seconds. They open the file, eye scans top-down. If they can answer *"what did this stage commit to?"* from the first 20 lines alone, the IA has won. If they must scroll or cross-reference the PRD, it has failed.

## 2. Field Layout Proposal (physical order)

Recommend the file be written in this order for scan-ability:

1. `entities` — the nouns; the eye grounds here first
2. `invariants` — the truths that must not break; load-bearing
3. `forbidden_vocabulary` — the visible fence; placed early so the author *sees it while authoring the rest*
4. `numeric_ceilings` — small, quantitative, quick to verify
5. `state_variables` — needs entities already in mind
6. `actions` — transitions between state_variables, so must follow them
7. `mandatory_artifacts` — downstream-facing; natural tail
8. `citations` — footer by convention; closes the document

Rationale: a human at checkpoint reading the first third of the file gets entities + invariants + forbidden vocabulary — the three most commitment-dense fields. The Architect authoring Flow B sees `forbidden_vocabulary` *before* writing `state_variables`, which is where the temptation strikes.

## 3. Naming Clarity Check (first-time author perspective)

| Field | Clarity | Notes / alt (for Architect review only) |
|---|---|---|
| `entities` | H | Universally understood as domain nouns. Keep. |
| `state_variables` | M | Engineers will read "program variables"; consider `observable_state` or `state_signals`. |
| `actions` | M | Ambiguous vs. "user actions" / "CLI actions"; consider `state_transitions`. |
| `numeric_ceilings` | H | Self-documenting. Keep. |
| `mandatory_artifacts` | H | Clear. Keep. |
| `invariants` | H | Precise term of art; authors who don't know it *should* learn it. Keep. |
| `forbidden_vocabulary` | H | Vivid, unambiguous. Keep. |
| `citations` | H | Standard. Keep. |

Two M-rated fields (`state_variables`, `actions`) — flag for Architect, do not rename unilaterally.

## 4. Mental Model (one paragraph)

*This file is not documentation. It is a list of promises the stage makes to every stage after it.* An author should open it thinking "what will I be held to?" not "what should I explain?" Every field is a contract a future DoD grep will enforce. If a line cannot be mechanically checked, it does not belong in constraints.yml — it belongs in the PRD. The guide is the map; the template is the mold; the file is the oath.

## 5. Error / Malformed-State UX

When a required field is missing, the validator returns a single line: `constraints.yml: FAIL — missing required field 'invariants' (see constraints-model-guide.md §3.2)`. The sub-agent re-opens the template, not the guide. YAML parse errors return line+column. Forbidden-vocabulary hits return the exact token and artifact path. There is no silent failure — every malformed state has exactly one feedback message with exactly one next action. The author is never asked to choose between recoveries.

## 6. Cross-Document Navigation Map

```
          prd.md  (the WHY)
             |
             v
  constraints-model-guide.md  (the canon — read once per role)
             |
             v
     [role template]  (Refine or Architect)
             |
             v
       constraints.yml  (the OATH)
          /     \
         v       v
   DoD findings   downstream agent (Dev, QA, Ops)
         |
         v
   stage-summary.md  (the glance)
```

**Friction points**: (1) Authors may confuse the guide with the template — mitigate by naming templates `constraints-template-refine.md` and `constraints-template-architect.md`. (2) Downstream agents may still open the PRD out of habit — mitigate by having the orchestrator cite the constraints.yml path in every stage kickoff, *before* the PRD path.

## 7. Reference Content IA (FR-4, FR-5)

**`volatility-decomposition.md`** — insert a new **§0 "The Golden Rule"** before the existing Phases 1–4. One paragraph stating Löwy's rule verbatim, one paragraph citation (*Righting Software*, Ch. 2), one worked anti-pattern: functional-decomposition trap with a before/after. Phases 1–4 remain untouched structurally; §0 is the frame through which they are re-read.

**`strategic-ddd.md`** — insert **§P-Guard "No Implementation Nouns at Decomposition"** as a sidebar repeated at the head of each of Phases 1–4 (short box, 4 lines: rule, token list reference, example swap, link to forbidden_vocabulary field). Repetition is intentional — the temptation strikes in every phase.

Proposed reading order in `volatility-decomposition.md`: §0 Golden Rule → §0.1 Anti-Pattern (Functional Trap) → §0.2 Citation → existing Phase 1 → existing Phase 2 → … → existing §Anti-Patterns (augmented).

## 8. Accessibility / Inclusivity

First-day authors: the guide's §1 should be titled **"What this file is (read first)"** in plain words — no "primitive," no "canonical schema." Non-native English authors: every field description in the guide uses ≤15-word sentences and one worked example per field. Term-of-art words (`invariant`, `volatility`) carry a parenthetical gloss on first appearance. No clever metaphors in the guide itself — save those for the alias voices.

## 9. Open Questions for Architect (Stage 4)

1. Should `forbidden_vocabulary` be **inherited** from a shared default list (NFR-2 tokens) or **restated** in every file? Tradeoff: DRY vs. glance-ability at checkpoint.
2. Should `citations` be free-form strings or structured `{work, chapter, page}` objects? Scan-ability favors free-form; rule-checking favors structure.
3. Where does the Refine↔Architect constraints handoff physically live — does Architect *extend* the Refine file, or write a sibling? IA depends on this choice.
4. Should the physical field order in §2 above be enforced by validator or merely conventional?

---

STATUS: DONE
ARTIFACT: .delivery/artifacts/03-design/ux/information-architecture.md
SUMMARY: The mirror is set — eight fields ordered as oath, not documentation; forbidden_vocabulary placed where the Architect's hand will stay itself before the word is written.
