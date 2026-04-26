# QA Evaluation — PRD revision 1 (Round 2)

**Artifact**: QA Evaluation (Legolas / QA Engineer) — **round 2**
**Stage**: 2 / Refine — Evaluator-Optimizer (iteration 2)
**Date**: 2026-04-20
**Inputs**:
- `.delivery/artifacts/02-refine/po/prd.md` (577 lines, Gandalf, **revision 1**)
- `.delivery/artifacts/02-refine/qa/evaluation.md` (round-1 QA evaluation, 11 defects)
**Alias**: Legolas — *"The ground has changed. I will count again, more carefully."*

---

> *"I named eleven defects. The Fellowship has answered them. I will walk the ground once more and see which wounds have closed and which still bleed — and I will watch for the tracks the revision may have cut through still-green turf."*

---

## Summary Verdict

**ACCEPT** — all eleven round-1 defects are addressed with concrete artifact changes. Instruments that were leaky (greps) are now complement-of-allowlist with explicit `*.db` exclusion. Subjective gates ("sharpness", "recognisable theme voice") are now binary: AC-04.2 is a named-count checklist, AC-05.1 extracts marker lists from the theme reference files. Baseline-missing metrics (M-04, M-05, M-07) are anchored to a new **REQ-10** that captures a 4.7 reference on the first implementation run. Sizing hints have been demoted out of acceptance criteria. The only structurally new concern is scope growth (six keystones vs two, two new REQs, one new risk) — which is *better* coverage, not a regression, and every addition is traceable to either a QA defect or a Challenger finding. I found **zero new testability defects** introduced by the revision. The Architect may proceed.

Eleven defects, eleven answers. *My count was exact. Their answer is exact. Go.*

---

## Round-1 Findings Traceability Table

| # | Defect | Status round 2 | Note |
|---|---|---|---|
| DEF-01 | AC-01.4 regex malformed + `.db` false-positive | **ADDRESSED** | AC-01.4 (line 295–305 of rev 1 PRD) replaced with complement-of-allowlist grep. Literal command includes `--exclude='*.db'`, `--exclude-dir=.delivery`, `--exclude-dir=.git`, `--exclude-dir=__pycache__`, and a `grep -v 'claude-haiku-4-5-20251001'` filter on the canonical Haiku 4.5 dated ID. The regex `claude-(opus\|sonnet\|haiku)-[0-9](\.[0-9])?-[0-9]{8}` catches MID-01's `claude-sonnet-4-5-20250929` (the rev-0 false-negative) because `-5-20250929` matches `-[0-9]-[0-9]{8}`, and the allowlist filter correctly spares `claude-haiku-4-5-20251001`. Verified by hand. |
| DEF-02 | Sizing sub-claims (S/M/L) embedded in ACs | **ADDRESSED** | Section 4 preamble (lines 284) explicitly states "PO sizing hypothesis (non-binding on Architect)". All per-REQ sizing claims now live in a "Rationale (PO sizing hint, non-binding):" footer on each REQ (e.g., REQ-01 line 307, REQ-02 line 320, REQ-03 line 333, REQ-03B line 345, REQ-04 line 358, REQ-05 line 370). No AC text now reads "size = S/M/L". |
| DEF-03 | M-04 "sharpness" undefined + no 4.6 baseline | **ADDRESSED** | M-04 (line 439) rewritten as a concrete binary checklist: "(i) ≥3 distinct weaknesses named, (ii) ≥2 specific referents cited (card names / file paths / REQ IDs), (iii) ≥1 concrete alternative proposed. Binary per invocation. Target: 3/3 invocations pass." AC-04.2 mirrors this (line 354). The baseline gap is additionally closed by the new REQ-10. |
| DEF-04 | AC-04.1 dogfood gate had no pass criterion | **ADDRESSED** | AC-04.1 (line 353) now names three gate conditions: (a) persona review on file at `.delivery/artifacts/<impl-run>/user-feedback/adversarial-4-7-sample.md`, (b) no severity-HIGH tone/depth regression vs REQ-10 baseline, (c) AC-04.2 checklist criteria met. Gate fails on any (a)/(b)/(c) miss. Mechanically verifiable. |
| DEF-05 | M-05 / AC-05.1 "recognisable theme voice" undefined | **ADDRESSED** | AC-05.1 (line 366) now defines voice preservation via marker extraction: "≥2 signature markers (distinctive catchphrase, register, or typical noun/verb choice) from the theme's own reference file". Threshold is a two-level rule: "rendered announcement preserves voice iff ≥50% of that theme's markers appear" and "target: ≥80% of sampled announcements preserve voice". M-05 (line 440) mirrors this with the explicit sample size "≥1 announcement per theme × 3 sampled themes". Measurable by a tiny grep. |
| DEF-06 | M-01 boundary-char defect + `.db` false-positive + misses MID-01 | **ADDRESSED** | M-01 (line 436) rewritten identically to the AC-01.4 fix — complement-of-allowlist regex, same `*.db`/`.delivery`/`.git` exclusions, same Haiku-4.5 allowlist pass-through. Current baseline explicitly stated as "**3** (MID-01..03 per Elrond §2)"; target "**0**". MID-01 is now caught by construction. |
| DEF-07 | M-02 measures a vacuous condition | **ADDRESSED** | M-02 (line 437) re-scoped as a regression guard: "No regression: `claude-opus-4-6` or `claude-sonnet-4-5-20250929` strings must not *re-enter* non-archival code after being removed by the sweep. Target: 0 new introductions." Current baseline clarified as 1 (MID-01 only). This is now a *forward-guard* metric, not a trivially-true assertion. |
| DEF-08 | M-07 95% target lacked a baseline anchor | **ADDRESSED** | M-07 (line 442) rewritten as "Post-implementation first-attempt rate ≥ `max(0.95, baseline_rate − 0.02)`. `baseline_rate` is the rate captured in REQ-10 AC-10.1(a) on the first dogfood run." Baseline-anchored floor; 95% retained as a hard minimum. |
| DEF-09 | R-01 mitigation inherited DEF-03/DEF-04 defects | **ADDRESSED (derived)** | R-01 (line 456) explicitly cites "REQ-04 enforces dogfood-before-edit with the AC-04.2 concrete checklist (QA DEF-03 resolved) and AC-04.1 concrete gate criterion (QA DEF-04 resolved)." Inheriting fix automatically flows through. |
| DEF-10 | R-05 "sequence first" is prose, not testable | **ADDRESSED** | R-05 (line 460) re-scored Low/Low per Challenger C-01 evidence — the retirement-urgency premise itself dissolved because Section 3.1.1 confirms zero Anthropic SDK imports in `agentic-flow-builder/` and `prd-quality-gate-flow/`. AC-01.2 (line 293) re-framed from "retirement-urgency" to "drift-hygiene" and explicitly requires a roadmap grep to confirm both "drift-hygiene" AND a reference to Section 3.1.1. The date-bounded test I proposed is moot now — the more correct fix was to dissolve the urgency, which they did. |
| DEF-11 | R-08 "contingency slot" structurally vague | **ADDRESSED** | R-08 (line 463) now requires "a section titled **'Contingency — Dogfood Findings'** with at least one placeholder item ID reserved (e.g., `TBD-CONTINGENCY-01`). If section is missing or empty, reviewer should reject." Structural, grep-checkable. |

**Tally:** 11 ADDRESSED / 0 PARTIALLY-ADDRESSED / 0 NOT-ADDRESSED.

---

## Regressions (new testability defects introduced by the revision)

**None found.** I walked each new/changed section looking for the kinds of defects my round-1 pass flagged (subjective gates, malformed greps, unreferenced baselines, sizing-masquerading-as-acceptance, prose mitigations without structural checks). The revision introduces:

- Two new REQs (REQ-03B, REQ-09, REQ-10). Each has mechanically-verifiable ACs with concrete file paths and binary pass conditions. REQ-10's AC-10.1 names the output artifact path (`.delivery/artifacts/<impl-run>/observability/4-7-baseline.json`), required contents (a–e enumerated), and sequencing ("captured *before* any prose or model-ID edit lands"). REQ-09's AC-09.1 names the AS-IS table shape (stage × expected count × actual count). REQ-03B's AC-03B.2 specifies a measurable tool-call floor (≥2 WebFetch/WebSearch).
- One new risk (R-09). Mitigation is REQ-09 AC-09.1 / AC-09.2 — a concrete data-collection step, not prose.
- One new Constraint (9, dogfood cost budget 1.0–1.35x). This is a planning guideline, not an AC. Non-testable-by-design but also not an acceptance criterion, so the DEF-02 class of concern does not apply.
- Expanded keystone set (2 → 6 files). Each new keystone is tied to a specific Finding (F-07 for `research-agent`, F-25 for `product-delivery`, prose-weight for `architect` and `mtg-commander`). REQ-02 ACs enumerate per-file checks.
- Revision-history table (line 519) is commendably thorough — each rev-1 change cites either a DEF-NN or a C-NN identifier, making traceability mechanical.

No regressions. No new leaky instruments. No new "sub-agent opinion" gates without a concrete pass criterion.

---

## Remaining Defects

**None blocking.** A few extremely minor observations, none of which rise to a defect and none of which should delay Architect hand-off:

- **Observation 1 (cosmetic, non-blocking):** AC-01.4 (line 297) specifies the regex `claude-(opus\|sonnet\|haiku)-[0-9](\.[0-9])?-[0-9]{8}`. This will match future IDs like `claude-opus-5-0-YYYYMMDD` if Anthropic ever ships a major-version-dated Opus; the allowlist would not include that and it would be flagged. Given the allowlist is a small explicit set that the PO/Architect will maintain, this is the right behaviour (fail loudly on unknown dated IDs). Not a defect — desired future-brittle.
- **Observation 2 (cosmetic, non-blocking):** M-05's "≥1 announcement per theme × 3 sampled themes" is a minimum-sample of 3 announcements across 3 themes. At that sample size, a single regression flips 33% to 67% preservation rate, and the 80% target is statistically under-powered. The PO already caveats this is "spot-sampling, not full audit" (REQ-05 rationale). Acceptable as a first-pass gate; Architect may widen the sample if they want confidence. Not a defect at this phase.
- **Observation 3 (cosmetic, non-blocking):** M-04 target "3/3 invocations pass" — if the implementation run captures fewer than 3 adversarial invocations, the denominator is undefined. Recommend Architect document a floor: "If fewer than 3 invocations are produced in the implementation run, M-04 defers to the next dogfood run." This is a roadmap-phase concern, not a PRD defect.

None of these require another PRD revision. They can be handled in the Architect's roadmap phase (sample-size decisions, invocation-count floors) or are desired-behaviour (fail-closed on unknown dated IDs).

---

## Verdict for Architect

**Proceed.**

The PRD's structural testability was already sound in round 0; round 1's fixes were instrument calibration; round 1's revision landed every calibration precisely and also improved coverage (six keystones vs two, new REQ-10 baseline, REQ-09 AS-IS count capture, REQ-03B research-agent tool-use probe). The Architect now has:

- A grep that actually catches MID-01 (the round-0 false-negative) and excludes the SQLite binary (the round-0 false-positive).
- A baseline-capture REQ (REQ-10) that makes the three "regression vs baseline" metrics (M-04, M-05, M-07) meaningful for the first time.
- Binary, enumerable checklists in place of "sharpness" and "recognisable voice".
- Sizing hints that clearly say "non-binding on Architect".
- A contingency structure (R-08) that a reviewer can verify by grep.
- An explicit keystone set of six files with per-file Findings attached.
- Traceability from every rev-1 change back to either a DEF-NN (QA) or C-NN (Challenger) identifier.

No further PO revision required. Architect begins Phase 1A Behavioral AS-IS (which REQ-09 now formalises), then Phase 1B Structural AS-IS, then Phase 2 TO-BE, then Phase 3 Roadmap. Dogfood-and-baseline sequencing in Phase 3 is tightly specified by REQ-10 and the per-REQ gates.

*Eleven defects named. Eleven defects answered. The road is clear. Go.*

— **Legolas**, QA Engineer (round 2)

---

**End of Evaluation (round 2).**
