# Retrospective: run-2026-05-05-tk2 — Skill Token-Economy Wave 2
**Format**: Start/Stop/Continue + Lessons Captured
**Date**: 2026-05-05
**Facilitator**: Aragorn
**Project type**: FEATURE (execution-of-pre-planned-waves)
**Routing**: 1 light · 2 light · 3 SKIP · 4 light · 5 light · 6 full · 7 full

## Stage-by-stage convergence

| Stage | First-try? | Rounds | Notes |
|-------|-----------|--------|-------|
| 1. Idea | YES | 1 | First-try; improvement vs Wave 0 and Wave 1 |
| 2. Refine | NO | 2 | Dev caught real math defect (673-175=498 not ≤300); led to Tier-B partial-compliance ruling |
| 3. Design | SKIP | n/a | DX-only |
| 4. Architect | NO | 2 | Gimli false-positive: treated W2-0 Stage 6 deliverable (skill-budgets.json entries) as Architect-stage prerequisite |
| 5. Plan | NO | 2 | PO caught compound sprint-goal sentence |
| 6. Dev (S1–S5) | MIXED | 1 pass / 2–4 DoD | All 5 stories code-DONE round 1; Stories 1+5 needed DoD rounds 2–4 (path lookup false-positive; QA "removed=good" misunderstanding; tier-consistency JSON vs frontmatter) |
| 7. UAT | NO | 2 | Sam wanted user-guide rollback (real finding); Legolas STATUS-grep admin issue (PO ruled PASS_WITH_NOTES) |

**Pipeline-level first-try DoD**: 6 of 12 stage-validations first-try (~50%). Slight regression in raw rate vs Wave 1's ~55%, but scope was materially larger (8 WIs vs 7; doctrine extraction vs frontmatter rollout) with harder cross-doc consistency demands.

## Start (do more of)

- **Tier-B partial-compliance rulings** — honest architecture with explicit Wave-3 deferral kept Wave 2 from over-scoping. Use this pattern whenever scope math is irreconcilable within a wave boundary.
- **Canonical path citations in validator prompts** — the repeat path-lookup failures across Wave 1 Story 1 and Wave 2 Story 1 confirm prompts must name the exact canonical path. Start doing this in every validator prompt at authoring time.
- **Single-source-of-truth for registry data** — JSON file + Python script divergence drove 4 rounds on Story 5. Start the Wave 3 governance work: JSON as SSoT, script generation or CI lint as validator.
- **Flexible STATUS grep** — DoD grep failures recur across waves. Use `-iE 'status:?\s*(done|pass)'` or a pipeline-standard STATUS format with an enforced canonical form.

## Stop (do less of)

- **Validators cross-examining Stage N prerequisites with Stage N+k deliverables** — Gimli's false-positive (Stage 4) wasted a round because he looked for a deliverable that belongs to Stage 6. Architect-stage validators MUST only examine spec/PRD conformance, not implementation outputs. Stop conflating "validate the spec" with "validate the implementation."
- **Compound sprint-goal sentences** — two waves running, two rounds on the same problem. Single-idea sprint goals only. PO must split on authoring, not at DoD.
- **Registry updates that touch JSON + script independently** — each Wave 2 Story 5 round found a new inconsistency because no lint enforced cross-file agreement. Stop hand-syncing; defer to CI or script generation.
- **STATUS-line format diversity** — every team member's STATUS signal uses a different form. Stop emitting ad-hoc status strings; standardize on `STATUS: DONE` / `STATUS: PASS`.

## Continue (keep doing)

- **Memory-as-contract** — Wave 1 lessons loaded cleanly into Wave 2; no re-debating known decisions
- **One Role = One Sub-Agent** throughout; no Prime Directive violations
- **LOTR theme** — no narrative-vs-content bleed across 7 stages
- **Sonnet primaries + Haiku DoD** model split
- **Cross-doc consistency gate at UAT TW** — Sam's user-guide rollback finding confirmed the gate is load-bearing; keep it
- **In-pipeline defect capture** — 5 defects caught before merge; 0 blocking; confirms the multi-round DoD pattern is earning its cost
- **Wave-scoped deferral via PRD** — Tier-B ruling + explicit Wave-3 backlog items kept scope bounded without silently dropping work

## New lessons captured (route to memory chunks)

1. **Validator path-lookup false positives are a recurrence pattern** — Wave 1 Story 1 AND Wave 2 Story 1 both had validators look in wrong directories. Canonical rule: pipeline artifacts live at `.delivery/artifacts/<NN>-<stage>/`; extracted references live at `<plugin>/references/` or `delivery-team/references/shared/`. Validator prompts MUST cite the correct canonical path at time of authoring. → `memory/topics/gate-patterns.md` (append — second occurrence elevates to must-fix).

2. **Spec validation ≠ implementation validation** — Architect-stage validators examine the spec/PRD/ADR for conformance. Stage 6 validators examine whether implementation satisfies AC. Validator prompts must explicitly name their target. The pattern: _"Validate that the [PRD / ADR / plan] is well-formed and internally consistent — do NOT check whether the implementation exists."_ → `memory/stages/architect.md` (append).

3. **Registry consistency is a multi-source problem** — JSON file + Python script must stay in sync. Manual updates reliably drift. Solution path: JSON as single source of truth + script generation OR CI lint that validates JSON ↔ script consistency at merge time. This is Wave 3 governance work. → `memory/topics/gate-patterns.md` (append).

4. **DoD STATUS-line format diversity causes grep failures** — `STATUS: DONE` vs `Status: PASS` vs `Gate Status: DONE` all appear in the same pipeline. Two options: (a) standardize on a single canonical form (`STATUS: DONE`) enforced by a hook, or (b) use a flexible grep (`-iE 'status:?\s*(done|pass)'`). Pick one; enforce it. → `memory/topics/gate-patterns.md` (append).

5. **Honest partial-compliance rulings are the right call** — Tier-B ruling in Stage 2 was validated by Stage 7. The pattern: if scope math is irreconcilable, state the tier, explain the gap, defer explicitly to next wave. Don't silently drop or silently stretch. → `memory/stages/architect.md` (append).

## Action items

| # | Action | Owner | Due | Status |
|---|--------|-------|-----|--------|
| 1 | Author BACKLOG-104 for Wave 3 (registry SSoT: JSON + CI lint or script generation) | PO | next session | Open |
| 2 | Standardize STATUS-line format: pick canonical form + add hook or flexible grep to DoD gate prompts | Architect + Dev | next session | Open |
| 3 | Append canonical-path rule to all validator prompt templates (both artifact and reference paths) | Dev | next session | Open |
| 4 | Add "validate spec not implementation" guard clause to Architect-stage DoD prompt template | Architect | next session | Open |
| 5 | File issue: plugin-dev:skill-development invocation pattern (carried from Wave 0 + Wave 1) | PO | post-Wave-2 | Open |

## Defects logged this run

None blocking. 5 real defects caught and fixed in-pipeline:
- D1 (Stage 2): PRD math error — 673-175=498, not ≤300 budget; corrected to Tier-B partial-compliance
- D2 (Stage 6 Story 1): Dev path lookup false-positive; canonical path clarified
- D3 (Stage 7): Missing user-guide rollback procedure; Sam finding; backlog item opened
- D4 (Stage 6 Story 5): QA misread "token count removed = good news" as a defect; reframed
- D5 (Stage 6 Story 5): Tier-consistency gap between JSON registry and frontmatter; corrected

## Defects/story rate

5 defects caught / 5 stories = 1.0 catch rate; 0 escapes. 0 blocking defects. Under 0.4 stop-rule (escapes only).

## Follow-up from Wave 1 retro (run-2026-05-04-tk1)

| # | Action | Status |
|---|--------|--------|
| 1 | Backport ADR-tk1-002 + BACKLOG-101 W1-7 line target (-1 → -2) and W1-3/W1-5 filename correction | DONE in W2 Stage 6+7 |
| 2 | Wire pre-merge git hook for skill-budget local check | NOT YET — carry to Wave 3 |
| 3 | Cross-doc consistency check as UAT TW gate criteria | DONE — held Wave 2; Sam finding confirms gate is load-bearing |
| 4 | File plugin-dev:skill-development invocation pattern issue | NOT YET — carry to Wave 3 |
