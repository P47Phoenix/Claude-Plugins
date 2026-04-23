# Refine-Stage DoD Validation — PRD rev 2 (round 2)

**Validator**: Legolas (QA Engineer — DoD gate, round 2)
**Artifact under review**: `.delivery/artifacts/02-refine/po/prd.md` (Revision Log carries three rev-2 entries dated 2026-04-20; header label still reads "revision 1" — see F-DOD2-01)
**Prior DoD**: `.delivery/artifacts/02-refine/dod/qa-review.md` (round 1, DONE, 4 non-blocking findings), `.delivery/artifacts/02-refine/dod/developer-review.md` (round 1, NOT_DONE, DEV-01/DEV-02/DEV-03 blockers + DEV-04/DEV-05 informational)
**Grounding**: `.delivery/artifacts/02-refine/data/scope-baseline.md` (Elrond)
**Date**: 2026-04-20
**Alias**: Legolas — *"An arrow loosed at every criterion. Seven quivers, seven counts — and one more for the fletching of rev 2."*

---

## Summary

Rev 2 addresses the three Developer blockers (DEV-01 regex, DEV-02 alias path, DEV-03 `parallel_validators` semantics) through surgical edits localised to AC-01.4 / M-01, AC-05.1 / AC-05.2 / AC-05.3 / M-05 / R-03, and AC-03.3 / AC-09.1 / M-03 / R-02 / §3.8 respectively. I mechanically re-executed every round-1 gate check against the rev-2 text plus the Developer-proposed fixes to confirm none of my original PASSes regressed.

Mechanical verifications performed:

1. **DEV-01 regex fix**: executed the rev-2 canonical command verbatim from AC-01.4. Returns **exactly 3 hits** — MID-01 line 148, MID-02 line 172, MID-03 line 187 — matching M-01's stated baseline of 3. The `[.-]` character class accepts MID-01's `sonnet-4-5-20250929` (dash separator on a two-part version) as well as MID-02/03's `haiku-4-20250514` / `opus-4-20250514` (dash between single-digit major and date). Allowlist `grep -v 'claude-haiku-4-5-20251001'` still correctly excludes the canonical current Haiku ID.
2. **DEV-02 path fix**: verified `delivery-team/skills/delivery-flow/references/aliases/` contains all 13 named theme YAML files. Verified `lotr.yml` contains `catchphrase` and `examples` fields per role (exact quote: `catchphrase: "A product owner is never late, nor early. They prioritize precisely when they mean to."`). Marker-extraction path from `yq '.roles[].catchphrase'` is executable as stated in AC-05.1.
3. **DEV-03 validator-set source fix**: confirmed `.delivery/config.yml` holds `parallel_validators: true` (boolean, DEV-03's evidence stands) *and* holds a `dod_validators:` block listing validator roles per stage — `idea: [po, architect]` (length 2), `refine: [po, architect, developer, qa]` (4), `design: [ux, po, qa, developer, architect]` (5), `architect: [architect, qa, developer, devops, security]` (5), `plan: [sm, po, qa, developer, devops]` (5), `development: [developer, qa, architect, tech-writer]` (4), `uat: [qa, devops, po, tech-writer]` (4). AC-09.1's per-stage counts (2/4/5/5/5/4/4) match the config exactly. Rev 2 re-pointed the "expected count source" to `dod_validators.<stage>` list length (DEV-03 fix option (a)-equivalent — existing schema key, no new key needed, Constraint 5 schema-freeze preserved).

Gate-evenness concerns from round 1 (F-DOD-01 keystone AC granularity, F-DOD-02 MID-04 routing-safety, F-DOD-03 AC-03B.2 tool-count floor, F-DOD-04 M-06 scope) are unchanged in rev 2 — no rev-2 edit touched those surfaces. All four remain non-blocking as previously recorded.

Seven round-1 criteria. One round-2 regression-check criterion. **Eight passes. One new non-blocking finding (F-DOD2-01) recorded.**

Verdict: **DONE**.

---

## Per-Criterion Evaluation

| # | Criterion | Round-1 verdict | Round-2 verdict | Rationale (one line) |
|---|---|---|---|---|
| 1 | Testable ACs | PASS | **PASS** | Rev 2's AC-01.4 regex fix strengthens testability (baseline of 3 now actually returns 3); AC-03.3 expected-count source is now a concrete list-length, not a boolean miscount; AC-05.1 marker extraction now points at real YAML files with a real `yq` one-liner. No new untestable AC introduced. |
| 2 | Evidence-linked ACs | PASS | **PASS** | All rev-2 edits preserve Finding/Inventory citations. AC-01.4 still cites F-01/F-03/F-04/Section 3.9; AC-03.3 still cites F-08; AC-05.1/2 still cite F-27/DISP-03. Revision Log entries explicitly cite DEV-01/DEV-02/DEV-03 provenance. |
| 3 | Metric baselining | PASS | **PASS** | M-01 baseline=3 now **mechanically reproducible** (rev 1 claimed 3 but regex returned 2 — regression closed); M-02 regression-guard baseline=1 unchanged; M-03 POST-BASELINE label retained with concrete source (`dod_validators.<stage>` list length); M-05 marker extraction now points at files that exist. |
| 4 | Regression detection | PASS | **PASS** | AC-01.4 canonical regex now catches MID-01/02/03 (was 2/3); M-02 regression-guard unchanged; AC-03.3 pairs actual dispatch count with expected-count source **from the config that ships in the repo** — fusion detection now has a real denominator, not a boolean. |
| 5 | Empirical validation plan | PASS | **PASS** | Six dogfood obligations unchanged in location; REQ-05's alias dogfood gained mechanical specificity (paths that exist, fields that exist, a `yq` command that runs). REQ-03/REQ-09's AS-IS count capture now has a concrete source of truth. |
| 6 | No untestable "improved" language | PASS | **PASS** | No new vague comparatives introduced. Rev 2's edits are all toward *more* mechanical specificity (regex precision, file paths, list-length counts), not less. |
| 7 | Adversarial findings addressed | PASS (F-DOD-01 non-blocking) | **PASS** (F-DOD-01 carries forward, non-blocking) | Rev 2 did not touch keystone AC-granularity, MID-04 routing-safety framing, AC-03B.2 tool-count floor, or M-06 scope — all four round-1 findings remain with their original severity. None escalated. |
| **8 (new)** | No round-2 regressions on prior fixes | — | **PASS (with F-DOD2-01)** | Rev 2's three surgical fixes do not weaken: DEF-01 regex completeness (now *more* correct); DEF-05 marker-based M-05 definition (now *executable* as stated); DEF-06 `.db` exclusion (preserved in rev-2 regex); DEF-07 M-02 regression-guard shape (untouched); DEF-08 baseline-anchored M-07 (untouched); C-04 AS-IS count capture REQ-09 (now backed by a real config key). F-DOD2-01 records the header/revision-label cosmetic drift. |

---

## Verdict

**DONE.**

Rev 2 passes all seven round-1 DoD criteria plus the round-2 no-regression criterion. The three Developer blockers from DoD round 1 are mechanically closed: the AC-01.4 regex now returns the stated baseline of 3 against the live repo; the alias marker-extraction path now resolves to 13 real YAML files with real `catchphrase` + `examples` fields; and the validator-dispatch-count denominator now points at `dod_validators.<stage>` — an existing v2.7 schema key that preserves Constraint 5's schema-freeze.

The PRD is ready for Architect consumption.

*An arrow for every count, loosed at both the original seven and the new eighth. The range is clear; the mark is struck.*

---

## Findings

### F-DOD2-01 — Revision label cosmetic drift (non-blocking, informational)

**Severity**: Low / cosmetic
**Location**: Front matter line 3 (`**Artifact**: PRD (Gandalf / Product Owner) — **revision 1**`) vs Revision Log (Section 9) which contains three `Rev 2 (DoD round 1, DEV-01/02/03)` entries dated 2026-04-20.
**Detail**: The PRD's top-of-file revision label still reads "revision 1" while the bottom-of-file Revision Log has logged three rev-2 edits. Neither the Gandalf's Closing Counsel section nor the end-of-PRD marker ("End of PRD — revision 1.") was updated in rev 2. This is a label-mismatch, not a content defect: every rev-2 change is correctly described and cited in the Revision Log and in the affected AC's inline `*(… rev 2 per Developer DEV-…)*` annotation.
**Impact**: Downstream readers (Architect Phase 1A) may be briefly confused about which version they are consuming. The content is the rev-2 content either way — the DEV-01/02/03 fixes are in the AC text, not only in the log.
**Recommendation**: Optional — Gandalf may update the header, Closing Counsel, and end-of-PRD marker to "revision 2" in a future no-op rev if the Architect requests it. Not a gate blocker.
**Blocking?**: No.

---

### F-DOD-01 — Keystone AC granularity is uneven (carried forward from round 1, non-blocking)

**Severity**: Low
**Location**: Section 4 REQ-02
**Round-2 status**: **Unchanged**. Rev 2 did not touch REQ-02's AC structure. AC-02.2 still singles out `prompt-engineer/SKILL.md`, AC-02.3 still singles out `product-delivery/SKILL.md`; the other four keystones still route through AC-02.1 + AC-02.4 plus sibling REQs. Coverage remains sufficient, granularity remains uneven, recommendation (Architect adds per-file rows in Phase 1A) remains unchanged.
**Blocking?**: No.

### F-DOD-02 — MID-04 routing-safety framing (carried forward, informational)

**Severity**: Informational
**Location**: Section 3.1, §6.3 UV-01, Open Question 3, REQ-01 AC-01.1
**Round-2 status**: **Unchanged**. Rev 2 did not touch MID-04 framing. Addressed-and-logged shape preserved.
**Blocking?**: No.

### F-DOD-03 — AC-03B.2 tool-count floor sanity-check (carried forward, informational)

**Severity**: Informational
**Location**: REQ-03B AC-03B.2
**Round-2 status**: **Unchanged**. Rev 2 did not touch REQ-03B. Floor of `>=2 WebFetch or WebSearch tool calls` with F-28-tuned escalation clause preserved.
**Blocking?**: No.

### F-DOD-04 — M-06 scan scope callout (carried forward, informational)

**Severity**: Informational
**Location**: Success Metrics M-06
**Round-2 status**: **Unchanged**. Rev 2 did not touch M-06. Scope remains Claude-Code-harness-level error scan; appropriate for this repo's zero-SDK-import state.
**Blocking?**: No.

---

## Mechanical Re-verification Log (round 2)

For reproducibility, the exact commands I executed against the current working tree on 2026-04-20 while evaluating rev 2:

1. **AC-01.4 regex verification:**
   ```bash
   grep -rnE 'claude-(opus|sonnet|haiku)-[0-9]([.-][0-9])?-[0-9]{8}' \
     --include='*.py' --include='*.json' --include='*.md' --include='*.yml' --include='*.yaml' \
     --exclude='*.db' --exclude-dir=.delivery --exclude-dir=.git --exclude-dir=__pycache__ \
     agentic-flow-builder/ prd-quality-gate-flow/ \
     | grep -v 'claude-haiku-4-5-20251001'
   ```
   Result: 3 hits — `agent_registry.py:148` (MID-01), `:172` (MID-02), `:187` (MID-03). **Matches M-01 baseline=3.** DEV-01 closed.

2. **AC-05.1 marker source verification:**
   ```bash
   ls delivery-team/skills/delivery-flow/references/aliases/
   grep -E 'catchphrase|examples' delivery-team/skills/delivery-flow/references/aliases/lotr.yml
   ```
   Result: 13 YAML files present (`breaking-bad`, `bulls-jordan`, `business`, `dilbert`, `funny`, `lotr`, `mandalorian`, `marvel`, `mtg`, `nfl`, `snl`, `star-wars`, `the-office`); `lotr.yml` has `catchphrase` + `examples` per role. **Matches AC-05.1 + M-05.** DEV-02 closed.

3. **AC-03.3 / AC-09.1 validator-count source verification:**
   ```bash
   grep -E 'parallel_validators|^dod_validators:' .delivery/config.yml -A 8
   ```
   Result: `parallel_validators: true` (boolean, confirms DEV-03's evidence) *plus* `dod_validators:` block with lists of lengths 2/4/5/5/5/4/4 for stages `idea`/`refine`/`design`/`architect`/`plan`/`development`/`uat` — exactly matching AC-09.1's per-stage count table. **DEV-03 closed via existing schema key (Constraint 5 preserved).**

---

## Findings Count (canonical for orchestrator)

- **Blocking defects**: 0
- **Non-blocking findings**: 5 (F-DOD-01, F-DOD-02, F-DOD-03, F-DOD-04 carried forward; F-DOD2-01 new)
- **Total findings recorded**: 5
- **Rev-2 regressions detected**: 0

*Eight criteria. Eight passes. The quiver is empty; the rev-2 fletching holds true.*

— **Legolas**, QA / DoD validator (round 2)
