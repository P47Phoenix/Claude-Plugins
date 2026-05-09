# QA DoD Review — Stage 4 (Architect, light), Round 2

**Pipeline**: run-2026-05-09-tk4
**Reviewer**: QA Engineer (DoD validator, FRESH dispatch round 2)
**Lens**: testability + AC traceability + round-2 regression check (LIGHT, blocking only)
**Date**: 2026-05-09

**Artifacts validated (revised)**:
- ADR-tk4-001 (revised) — `.delivery/artifacts/04-architect/adrs/ADR-tk4-001-tier-b-closure-approach.md`
- ADR-tk4-002 — `.delivery/artifacts/04-architect/adrs/ADR-tk4-002-paradigm-sub-skill-pattern.md`
- ADR-tk4-003 (revised) — `.delivery/artifacts/04-architect/adrs/ADR-tk4-003-governance-frontmatter-shape.md`
- Architecture summary (revised) — `.delivery/artifacts/04-architect/solution/architecture-tk4-wave-3.md`

**Round-1 baseline**: `.delivery/artifacts/04-architect/dod/qa-review.md` (gates 1-3 PASS, gates 4-5 NOT_PASS)

**Upstream traced**: PRD `.delivery/artifacts/02-refine/po/prd.md` §6 AC-1..AC-7; BACKLOG-104 init ACs 1..10.

---

## STATUS: DONE

All 5 blocking gates PASS. Both round-1 NOT_PASS gates are remediated with surgical, runnable additions. Gates 1-3 regression check confirms no perturbation.

---

## Gate-by-gate verdict (round 2)

### Gate 1 — Every Decision element across all 3 ADRs is TESTABLE: **PASS** (regression)

Round-1 PASS verdict is preserved. Round-2 revisions did NOT remove or weaken any Decision element:

| ADR | Round-1 testable elements | Round-2 delta | Verdict |
|---|---|---|---|
| tk4-001 | 7 per-file extractions (W3-1..W3-7) with `before → -Δ + router-Δ = after`; per-file `wc -l ≤ ceiling`; ~42-input dogfood router regression set | W3-7 godot deepened (236 → 197 instead of 198) via one extra 1-line `Architecture Guardrails` consolidation; math `236 → -38 -1 = 197` cited (line 97); cross-file headroom table (line 99) re-asserts ≥9-line margins on the other 6 files | PASS — strengthened, not weakened |
| tk4-002 | Canonical `<plugin>/skills/<axis>/<variant>/SKILL.md` shape + 7-key frontmatter contract + parent router contract + marketplace lint regex | Untouched in round 2 (no revisions detected by content scan) | PASS |
| tk4-003 | 3 frontmatter keys + per-file +50-byte impact + sequencing gate + `regenerate_cache_prefix_hash.py` regeneration command + ISO-8601 + `context_budget`-matches-`tier` lint | New §"Post-Story-5 budget verification" subsection added (lines 78-86) — adds a NEW testable element, does not weaken any existing one | PASS — strengthened |

Every Decision element across all 3 ADRs has either an explicit runnable verification command or an artifact-level invariant. No narrative-only decisions detected.

---

### Gate 2 — Cache-prefix re-freeze verification step exists in ADR-tk4-003: **PASS** (regression)

Round-1 PASS verdict is preserved. ADR-tk4-003 §"Cumulative cache-prefix re-freeze procedure" (lines 48-68) is byte-identical to round-1 in substance:

- **Step 2 (regeneration command)** — line 64: `python3 scripts/regenerate_cache_prefix_hash.py --target governance/cache-prefix-hash.txt --files delivery-team/skills/*/SKILL.md delivery-team/skills/*/paradigms/*/SKILL.md`. Explicit, runnable.
- **Step 3 (verification)** — line 67: "Stage 6 DoD validator MUST cite the regenerated hash file's actual byte counts, NOT the +650-byte projection." Binding.
- **Step 4 (gate)** — line 68: hash file updated ONCE at end of Story 5.

The newly-added §"Post-Story-5 budget verification" (Gate 4 closure) is *additive* — it does not displace or modify the re-freeze procedure. PASS.

---

### Gate 3 — All 7 PRD AC-1..AC-7 map to ADR contract element OR Stage 6/7 dogfood: **PASS** (regression)

Round-1 PASS verdict is preserved. Re-validated traceability matrix (PRD §6 numbering; BACKLOG-104 init ACs 1..10 collapsed into PRD's 7 per Refine):

| PRD AC | BACKLOG-104 init AC(s) | Source WI | Mapped to | Round-2 specific element |
|---|---|---|---|---|
| AC-1 | 1 | W3-1..7 + W3-9 budgets clear (`check_skill_budgets.py` exits 0) | **ADR-tk4-001** + **ADR-tk4-003** | tk4-001 §W3-1..W3-7 per-file math (godot revised to 197); tk4-003 §"Mandatory-rollout sequencing" (line 74-76) + new §"Post-Story-5 budget verification" (lines 78-86) close the round-1 Gate-4 gap |
| AC-2 | 2 | W3-12 CLAUDE.md ≤150 lines | **Stage 6 dogfood** (mechanical) | unchanged from round 1 |
| AC-3 | 3 | W3-9 governance frontmatter on all delivery-team SKILL.md | **ADR-tk4-003** | §"Frontmatter contract" + §"CI lint" (line 46) |
| AC-4 | 4 | W3-13..16 (Wave 2 carry-forwards) | **Architecture summary** §"Open questions" #2 (W3-15 standardize ruling, line 94) + Stage 6 dogfood | unchanged from round 1 |
| AC-5 | 5 | W3-17 + W3-18 + DEFECT-006 close | **Architecture summary** §"Open questions" #3 (W3-17 Option A ruling, line 95) + Stage 6 dogfood (W3-18 telemetry) | new round-2 §"Stop-Rule Tripwire Mechanics" tail (line 81) folds the `--baseline pre-caveman-lite` flag addition into W3-18 — tightens AC-5 contract |
| AC-6 | 6 | W3-8 paradigm sub-skill ≥3 axes | **ADR-tk4-002** | §"Canonical directory shape" Wave-3 table (research-agent 5, user-feedback 4, presentation conditional) |
| AC-7 | 7 + 10 | NFR-4 ≥50% telemetry-measured cumulative reduction + W3-11 fitness review | **Architecture summary** §"Cache-prefix impact summary" + new §"Stop-Rule Tripwire Mechanics" + Stage 6 dogfood | tripwire mechanics now name `python3 scripts/compute_token_reduction.py --baseline pre-caveman-lite --window 3 --output .delivery/telemetry/stop-rule-tk4.txt` and the comparison baseline (`.delivery/memory/archive/run-2026-05-05-tk2.md`) — strengthens AC-7 |

BACKLOG-104 init ACs 8 (no first-try DoD pass-rate regression) and 9 (defects/story ≤0.4) remain pipeline-runtime KPIs (correctly omitted from PRD §6 collapse and not flagged here). PASS.

---

### Gate 4 — Post-Story-5 `check_skill_budgets.py` exit-0 verification step exists: **PASS** (round-1 NOT_PASS → round-2 PASS)

**Round-1 finding**: An explicit post-Story-5 verification step was missing; godot was projected to land at 198 + 3 frontmatter = 201, +1 over Tier-C ceiling, with the §W3-7 escape hatch only described as conditional in tk4-001 ("if buffer is tighter than the math suggests").

**Round-2 closure (TWO complementary fixes)**:

1. **ADR-tk4-001 §W3-7 deepened** (lines 90-97). Round-2 revision retargets godot to ≤197 (not 198) by folding **one additional 1-line trim** in `## Architecture Guardrails` (consolidate the two performance-budgets/frame-time-awareness bullets into one composite line; semantic loss = nil per Stage 6 Dev confirmation). Math: `236 → -38 -1 = 197`. The escape hatch is now MOOT at PR time — the round-1 conditional 5-line guardrails fold is RETAINED only as a Stage-6 *reserve* if measured `wc -l` exceeds the projection by 1-2 lines.

2. **ADR-tk4-003 §"Post-Story-5 budget verification" added** (lines 78-86, round-2 addition). Mandates:
   ```bash
   python3 scripts/check_skill_budgets.py
   ```
   exit 0 BEFORE the Story 5 PR merges. Explicitly states: "Post-Wave-3 `governance/skill-budgets.json known_debt` MUST be empty; any non-empty `known_debt` entry blocks AC-1." Cross-file headroom is re-asserted (architect 291/300; ui 276/300; operations 258/300; quality 279/300; user-feedback 253/300; presentation ~163/300; godot 200/200 exactly).

**Empirical re-check** with revised godot target:

| File | tk4-001 round-2 after | + frontmatter (+3) | Tier ceiling | Status |
|---|---:|---:|---:|---|
| architect | 288 | 291 | 300 | OK (margin 9) |
| presentation | ~160 | ~163 | 300 | OK (margin ~137) |
| ui | 273 | 276 | 300 | OK (margin 24) |
| operations | 255 | 258 | 300 | OK (margin 42) |
| quality | 276 | 279 | 300 | OK (margin 21) |
| user-feedback | 250 | 253 | 300 | OK (margin 47) |
| **godot (revised)** | **197** | **200** | **200** | **OK (held EXACTLY at 200)** |

All 7 in-scope files clear with `after + 3 ≤ ceiling` satisfied. The contract for Stage 6 to test is now: run `check_skill_budgets.py` and verify exit 0. **PASS.**

---

### Gate 5 — Stop-rule tripwire detection mechanism is testable (<15% prose-token reduction): **PASS** (round-1 NOT_PASS → round-2 PASS)

**Round-1 finding**: BACKLOG-104 §Stop-rule trigger #2 specified the gate but no ADR or architecture artifact specified HOW Stage 6 detects the <15% condition, making the gate narrative-only.

**Round-2 closure**: architecture-tk4-wave-3.md §"Stop-Rule Tripwire Mechanics" added (lines 72-81, round-2 addition). The section operationalizes the tripwire end-to-end:

| Tripwire element | Specification (line in architecture-tk4-wave-3.md) |
|---|---|
| Source telemetry | `.delivery/telemetry/skill-loads.jsonl` post-merge dispatches; `prose_tokens` field made reliable by W3-18 (line 76) |
| Calculation | mean response-prose tokens across the **first 3 post-merge dispatches** (line 77) |
| Runnable command | `python3 scripts/compute_token_reduction.py --baseline pre-caveman-lite --window 3 --output .delivery/telemetry/stop-rule-tk4.txt` (line 77) |
| Comparison baseline | Wave 2 archive `.delivery/memory/archive/run-2026-05-05-tk2.md` (line 78) |
| Threshold | `<15%` reduction → HALT pipeline before W3-9 PR opens (line 79); Stories 1–4 + Story 7 admin may continue |
| Recovery path | Trigger BACKLOG-102 stop-rule retro on caveman-lite; architect re-evaluates; outcome → Stage 4 round 3 or Wave 4 deferral (line 80) |
| DoD citation artifact | `.delivery/telemetry/stop-rule-tk4.txt` MUST be present and parsed before Story 5 PR opens; narrative "looks fine" claims rejected (line 81) |
| Flag-availability fallback | If `compute_token_reduction.py` lacks `--baseline pre-caveman-lite` support today, that flag addition folds into W3-18 telemetry hardening and ships before Story 5 (line 81) |

The contract a Stage 6 Dev would now run is fully specified: command + baseline + window + threshold + output path + halt/proceed semantics. The gate is no longer narrative-only. **PASS.**

---

## Summary scoreboard

| Gate | Round 1 | Round 2 | Blocking? |
|---|---|---|---|
| 1. Decision elements TESTABLE across all 3 ADRs | PASS | **PASS** (regression) | — |
| 2. Cache-prefix re-freeze verification step in ADR-tk4-003 | PASS | **PASS** (regression) | — |
| 3. PRD AC-1..AC-7 traceability to ADR / Stage 6 dogfood | PASS | **PASS** (regression) | — |
| 4. Post-Story-5 `check_skill_budgets.py` exit-0 verification | NOT_PASS | **PASS** (closed) | — |
| 5. <15% prose-token reduction stop-rule tripwire mechanism | NOT_PASS | **PASS** (closed) | — |

**Overall STATUS: DONE.** All 5 gates PASS. No NOT_PASS gates remain.

---

## Round-2 traceability matrix (closure evidence)

| Round-1 NOT_PASS gate | Required remediation | Round-2 artifact change | Location | Verifiable contract |
|---|---|---|---|---|
| Gate 4 — post-Story-5 budget exit-0 | Explicit step mandating `check_skill_budgets.py` exit 0 + godot escape hatch as MANDATORY (not conditional) | (a) ADR-tk4-001 §W3-7 deepened: godot 236 → 197 via extra `Architecture Guardrails` 1-line consolidation, escape hatch demoted to Stage-6 reserve. (b) ADR-tk4-003 new §"Post-Story-5 budget verification". | (a) ADR-tk4-001 lines 90-97; (b) ADR-tk4-003 lines 78-86 | `python3 scripts/check_skill_budgets.py` → exit 0 BEFORE Story 5 PR merges; `governance/skill-budgets.json known_debt` MUST be empty post-Wave-3 |
| Gate 5 — <15% prose-tripwire detection mechanism | Specify runnable command + baseline + window + threshold + halt semantics for the BACKLOG-104 §Stop-rule trigger #2 | architecture-tk4-wave-3.md new §"Stop-Rule Tripwire Mechanics" | architecture-tk4-wave-3.md lines 72-81 | `python3 scripts/compute_token_reduction.py --baseline pre-caveman-lite --window 3 --output .delivery/telemetry/stop-rule-tk4.txt`; if `<15%` → HALT before Story 5 PR; output file is binding DoD citation artifact |

---

## TARGET vs CURRENT discipline check (regression)

Round-1 verdict preserved: ADRs continue to distinguish TARGET (post-extraction line counts) from CURRENT (verified `wc -l` snapshot from PRD §3). Round-2 godot revision (236 → 197) explicitly cites the verified CURRENT (236 from PRD §3) and projects TARGET (197) with the Δ math written out (`-38 -1 = 197`). No conflation introduced. Round-2 §"Cross-file headroom check" table (ADR-tk4-001 line 99-109) re-asserts the +3 frontmatter overlay against tier ceilings cleanly. Lesson honored.

---

**Verdict (≤3 sentences)**: All 5 blocking gates now PASS — both round-1 NOT_PASS gaps are closed with surgical, runnable additions (godot deepened to 197 + new §"Post-Story-5 budget verification" in ADR-tk4-003 for Gate 4; new §"Stop-Rule Tripwire Mechanics" in architecture-tk4-wave-3.md for Gate 5) and Gates 1-3 show no regression. The contracts a Stage 6 Dev must run are now fully specified end-to-end (commands, baselines, windows, thresholds, output artifacts, halt semantics), and the godot escape hatch is correctly demoted to a Stage-6 reserve rather than a PR-time conditional. Stage 4 Architect (LIGHT) round-2 DoD: **DONE** — pipeline may proceed to Stage 5.

— QA Engineer (DoD validator, FRESH dispatch round 2), run-2026-05-09-tk4, Stage 4 (Architect, LIGHT) round 2.
