# Gate 2 Evaluation — Round 1

**Reviewer**: Legolas (QA Evaluator)
**Artifact**: `.delivery/artifacts/02-refine/po/prd.md` — Orchestration Discipline Bundle
**Date**: 2026-04-05
**Round**: 1 of N

> *"That bug still only counts as one."*

The wind carries the scent of this PRD from a great distance. I draw the bowstring and look closely at each Gate 2 criterion. What I see, I name precisely.

---

## Criterion 1: Every FR has clear, testable acceptance criteria

**VERDICT: PASS**

I sighted each of the 16 FRs and confirmed each carries an `**Acceptance**:` clause bound to an observable artifact state.

| FR | Acceptance present? | Testable? | Notes |
|----|---|---|---|
| FR-01 | Yes | Yes | Fresh config has no `project_type`, `schema_version: 2.7` — file inspection |
| FR-02 | Yes | Yes | v2.6 config with `project_type: GREENFIELD` runs without error — fixture test |
| FR-03 | Yes | Yes | Two consecutive runs with different request types produce different routing — observable |
| FR-04 | Yes | Yes | 9-question wizard, no `project_type` in output — file inspection |
| FR-05 | Yes | Yes | Grep returns only deprecation/Phase 1 hits — deterministic |
| FR-06 | Yes | Yes | Section exists, first prose block, referenced from 3 downstream sections |
| FR-07 | Yes | Yes | Step 4.5 contains rejection clause and links to FR-08 section |
| FR-08 | Yes | Yes | Section exists with all 6 anti-patterns named, described, resolved |
| FR-09 | Yes | Yes | Three concrete cases: orchestrator Write blocked, sub-agent Write allowed, state.md allowed |
| FR-10 | Yes | Yes | Rule exists, visually distinct, referenced by name from 3 docs |
| FR-11 | Yes | Yes | Each of 3 reference docs contains dispatch rule in specified locations |
| FR-12 | Yes (conditional) | Yes | Fires on synthetic compound prompt; not on single-role prompt — properly gated as MAY |
| FR-13 | Yes | Yes | Pattern exists with all 4 protocol steps and no-context-leak guarantee |
| FR-14 | Yes | Yes | Stage 4 references new pattern by name and bounds loop count |
| FR-15 | Yes | Yes | v2.7 config-schema documents `max_self_correction` with Architect use listed |
| FR-16 | Yes | Yes | Grep for `2.6` returns only changelog/historical; live docs say 2.7 |

Each acceptance criterion is bound to a file-state, grep result, or hook behavior. No hand-waving. No "should feel right."

**Memory lesson check**: "Test cases must cover ALL functional requirements explicitly." All 16 FRs are individually addressed. None blur into another. Even FR-12 — the optional one — has its own acceptance gated on the conditional. The arrow flies true.

---

## Criterion 2: NFRs are measurable (not vague)

**VERDICT: PASS**

| NFR | Measurable? | Evidence |
|---|---|---|
| NFR-01 | Yes | "p95 ≤ 50ms on Write/Edit, wall-clock around hook entry/exit, no regression vs v2.6 baseline" — quantified, methodology stated |
| NFR-02 | Yes | "pure Python stdlib, no new dependencies" — binary check (import audit) |
| NFR-03 | Yes | "v2.6 config with or without `project_type` loads without error" — fixture test |
| NFR-04 | Yes | "no PR mergeable while CLAUDE.md/README.md/marketplace.json/config-schema.md reference v2.6 as current" — DoD validator, grep-based |
| NFR-05 | Yes | "wrap main() in try/except, sys.exit(0) on failure" — code inspection |
| NFR-06 | Yes | "zero self-writes, one role per sub-agent, isolated loops at Architect, no frozen project_type" — observable in dogfood run logs |
| NFR-07 | Yes | "plugin-dev:skill-development / hook-development loaded before any SKILL.md or hook edits" — process check at developer-stage DoD |
| NFR-08 | Yes | "all four issues' file changes ship as one cohesive set" — single PR / single merge commit verifiable |

NFR-01 is the gold standard: a number, a method, and a baseline. The others are not all numeric, but each is binary-decidable, which is the second-best form of measurable. None say "fast" or "robust" without a concrete check behind them.

---

## Criterion 3: Success metrics are quantified

**VERDICT: PASS**

Section 2 ("Goals & Success Metrics") gives an 8-row table. Every row has a Metric column and a Target column.

- G1: 100% of pipeline runs re-detect — quantified
- G2: 0 unblocked self-writes, all attempts logged — quantified
- G3: 0 false-negatives in dogfood run — quantified
- G4: 100% of Architect stages execute ≥1 isolated loop — quantified
- G5: Zero contradictions in adversarial review — quantified
- G6: 100% of legacy configs tolerated — quantified
- G7: Verified in DoD — process gate (binary)
- G8: ≤ 50ms p95, no regression — quantified, mirrors NFR-01

G7 is the softest of the eight, but it is bound to a DoD validator (NFR-04), so the binary check is locatable. The rest are sharp numbers.

---

## Criterion 4: Out of scope is explicit

**VERDICT: PASS**

Section 6 ("Out of Scope") gives 9 explicit exclusions, each naming a specific thing the bundle will not do:

1. Rewriting Phase 1 detection logic (only invocation cadence changes)
2. New collaboration patterns beyond Isolated Adversarial Loop
3. Adversarial loops at non-Architect stages
4. General-purpose migration tool for old configs
5. Refactoring unrelated hooks
6. Net-new analytics / telemetry / dashboards
7. Changes to non-`delivery-flow` plugins
8. New alias theme (Gandalf borrowed only)
9. Changing `max_self_correction` default

These are precise. Each exclusion is a thing a reviewer might reasonably ask for, named and refused. Good fence.

---

## Criterion 5: Dependencies identified

**VERDICT: PASS**

Section 7 lists 4 dependencies (D1–D4):

- D1: plugin-dev skills loaded before edits
- D2: existing `enforce_pipeline_scope.py` `hook_utils` and active-pipeline detection reused
- D3: existing `max_self_correction` config key reused
- D4: existing checkpoint mechanism reused for human review

Each dependency names a concrete artifact or capability the bundle relies on. The risks table (R1–R8) is also strong — 8 rows with likelihood, impact, and mitigation. R6 in particular catches the load-bearing technical unknown (orchestrator-vs-subagent context detection) and explicitly defers it to Architect, which is the right escalation.

---

## Criterion 6: Open questions tracked

**VERDICT: PASS**

Section 8 lists 7 questions, each tagged with the downstream stage that owns its resolution:

- OQ-1 (Architect): self-write detection mechanism
- OQ-2 (Architect): FR-12 false-positive risk acceptability
- OQ-3 (Design): deprecation log line location
- OQ-4 (Design): Step 4.5 location and post-renumbering survival
- OQ-5 (Plan): dogfood Architect stage — 2 loop iterations or 1 clean pass?
- OQ-6 (Operations): does `marketplace.json` mention schema version at all?
- OQ-7 (Quality): test fixture location (committed or inline)?

Each question is routed. Each is non-blocking (the PRD explicitly says so in the section preamble). OQ-1 is the most consequential — it gates FR-09's implementation entirely — and it is correctly marked as Architect-stage homework, with R6 mirroring it in the risk table. Good cross-referencing.

**Minor observation (not a FAIL)**: OQ-7 (test fixture location) intersects with Criterion 1, but the PRD's acceptance criteria are file-inspection and grep-based, which the repo can validate today without a test runner. So this OQ is genuinely a Plan/Quality decision and not a hidden gap in Gate 2 coverage.

---

## Overall Verdict

| Criterion | Verdict |
|---|---|
| 1. FRs have testable acceptance criteria | PASS |
| 2. NFRs are measurable | PASS |
| 3. Success metrics are quantified | PASS |
| 4. Out of scope is explicit | PASS |
| 5. Dependencies identified | PASS |
| 6. Open questions tracked | PASS |

**ALL SIX CRITERIA PASS. The PRD is ready for adversarial review.**

The bowstring is at rest. I see no flaw from this distance, and my distance is great. If the adversarial reviewer finds something I missed, that bug still only counts as one — and I will not be ashamed to learn from it. But from where I stand on the ridge, this PRD is fit to advance.

---

*— Legolas, QA Evaluator, Round 1*
