# QA DoD Review — Stage 4 (Architect, light), Round 1

**Pipeline**: run-2026-05-09-tk4
**Reviewer**: QA Engineer (DoD validator, FRESH dispatch)
**Lens**: testability + AC traceability (LIGHT, blocking only)
**Date**: 2026-05-09

**Artifacts validated**:
- ADR-tk4-001 — `.delivery/artifacts/04-architect/adrs/ADR-tk4-001-tier-b-closure-approach.md`
- ADR-tk4-002 — `.delivery/artifacts/04-architect/adrs/ADR-tk4-002-paradigm-sub-skill-pattern.md`
- ADR-tk4-003 — `.delivery/artifacts/04-architect/adrs/ADR-tk4-003-governance-frontmatter-shape.md`
- Architecture summary — `.delivery/artifacts/04-architect/solution/architecture-tk4-wave-3.md`

**Upstream traced**:
- PRD — `.delivery/artifacts/02-refine/po/prd.md` (§6 AC-1..AC-7)
- BACKLOG-104 — `.delivery/backlog/BACKLOG-104-skill-token-economy-delivery-team-wave-3.md` (§"Acceptance Criteria (initiative-level)" 1..10; PRD §6 collapses these into AC-1..AC-7)

---

## STATUS: NOT_DONE

Two of five blocking gate criteria fail. Both are remediable inside Stage 4 with surgical additions to the existing ADRs (no re-architecture). Gates 1, 2, 3 PASS.

---

## Gate-by-gate verdict

### Gate 1 — Every Decision element in each ADR is TESTABLE: **PASS**

| ADR | Decision elements | Testable check (cited from ADR text) | Verdict |
|---|---|---|---|
| tk4-001 | 7 per-file extractions (W3-1..W3-7) with explicit batching math (`before → -Δ + router-overhead-Δ = after`) and named target ceiling | `wc -l <file> ≤ ceiling` per file (300 for Tier-B; 200 for Tier-C); per-file dogfood router regression set (~42 inputs total) cited in §"Stage 6 dogfood checklist" | PASS |
| tk4-002 | Canonical directory shape `<plugin>/skills/<axis>/<variant>/SKILL.md` + 7-key frontmatter contract + parent router contract + marketplace invariant | §"Marketplace discoverability invariant" cites the explicit lint: `grep -l "disable-model-invocation: true" $(find . -name SKILL.md)` regex-matched against `.*/skills/[^/]+/[^/]+/SKILL.md` or grandfathered legacy path; sub-skill `disable-model-invocation: true` verifiable via `grep -l` per file | PASS |
| tk4-003 | 3 new frontmatter keys + per-file +50-byte impact + sequencing gate + hash regeneration command | §"Frontmatter contract" CI lint validates presence + well-formedness + `context_budget` matches tier + `fitness_review_due` parses as ISO-8601; verifiable per-file via `grep -l "^maintainer:"`, `grep -l "^fitness_review_due:"`, `grep -l "^context_budget:"` | PASS |

Every Decision element across the three ADRs has either an explicit runnable verification command or a verifiable artifact-level invariant. No narrative-only decisions detected.

---

### Gate 2 — Cache-prefix re-freeze verification step exists in ADR-tk4-003: **PASS**

ADR-tk4-003 §"Cumulative cache-prefix re-freeze procedure" specifies:

- **Step 2 (regeneration command)**: `python3 scripts/regenerate_cache_prefix_hash.py --target governance/cache-prefix-hash.txt --files delivery-team/skills/*/SKILL.md delivery-team/skills/*/paradigms/*/SKILL.md` — explicit, runnable.
- **Step 3 (verification)**: "Stage 6 DoD validator MUST cite the regenerated hash file's actual byte counts, NOT the +650-byte projection. Caveman-lite caught a byte-offset INVERSION in tk3 because the architect cited a position from the wrong file; this DoD gate is binding."
- **Step 4 (gate)**: hash file updated ONCE at end of Story 5 (not per-file, not per-Story-1..4 trim).

The verification step is concrete: re-run the regeneration, diff against the prior hash, cite actual byte counts. PASS.

---

### Gate 3 — All 7 PRD AC-1..AC-7 (= BACKLOG-104 init ACs) map to ADR contract elements OR Stage 6/7 dogfood: **PASS**

Traceability matrix (PRD §6 numbering used; BACKLOG-104 1..10 collapsed into PRD's 7 per Refine):

| PRD AC | BACKLOG-104 AC(s) | Source WI | Mapped to | Specific element |
|---|---|---|---|---|
| AC-1 | 1 | W3-1..7 + W3-9 budgets clear (`check_skill_budgets.py` exits 0) | **ADR-tk4-001** + **ADR-tk4-003** | tk4-001 §Decision per-file math (W3-1..W3-7); tk4-003 §"Mandatory-rollout sequencing" gates frontmatter on trims-first; **see Gate 4 NOT_PASS for residual concern** |
| AC-2 | 2 | W3-12 CLAUDE.md ≤150 lines | **Stage 6 dogfood** (mechanical) | BACKLOG-104 §Story 6; not architecturally novel; arch summary §"Open questions" omits but acceptable per gate-3 criterion |
| AC-3 | 3 | W3-9 governance frontmatter on all delivery-team SKILL.md | **ADR-tk4-003** | §"Frontmatter contract" + §"CI lint" |
| AC-4 | 4 | W3-13..16 (4 Wave 2 carry-forwards) | **Architecture summary** §"Open questions" #2 (W3-15 standardize ruling) + **Stage 6 dogfood** (W3-13, W3-14, W3-16 mechanical) | Standardize ruling for W3-15 explicitly cited; remainder Story 7 admin |
| AC-5 | 5 | W3-17 + W3-18 + DEFECT-006 close | **Architecture summary** §"Open questions" #3 (W3-17 Option A ruling) + **Stage 6 dogfood** (W3-18 telemetry) | Option A (banner each stale file) explicitly chosen; W3-18 mechanical |
| AC-6 | 6 | W3-8 paradigm sub-skill ≥3 axes | **ADR-tk4-002** | §"Canonical directory shape" Wave-3 table: research-agent (5), user-feedback (4), presentation (9 conditional) |
| AC-7 | 7 + 10 | NFR-4 ≥50% telemetry-measured cumulative reduction + W3-11 fitness review process operational | **Architecture summary** §"Cache-prefix impact summary" §"Justification" + **Stage 6 dogfood** (telemetry) | ~13,200-token reduction math cited; W3-11 fitness review keys land in tk4-003 frontmatter; full telemetry measurement is Stage 6 |

BACKLOG-104 init ACs 8 (no first-try DoD pass-rate regression) and 9 (defects/story ≤0.4) are pipeline-runtime KPIs, not architect-stage testable contracts; correctly omitted from PRD §6 collapse and not flagged here.

All 7 PRD ACs map to either an ADR contract element or a Stage 6/7 dogfood/admin task. PASS.

---

### Gate 4 — Mandatory-rollout sequencing has a verification step: **NOT_PASS**

**Required**: After Story 5 (W3-9 frontmatter), `check_skill_budgets.py` must still exit 0 (no file pushed over budget by added frontmatter lines).

**Found in ADRs**:

- ADR-tk4-001 §"Sequencing with ADR-tk4-003" correctly states: "frontmatter rollout adds ~3 lines per file. If W3-9 ran first, files already AT-budget after this ADR's trims would land 3 lines OVER budget."
- ADR-tk4-001 §W3-7 godot identifies the tightest case: "after = 198 ≤ 200. COMPLIANT. (Margin = 2 lines; Stage 6 Dev runs the command and confirms; if buffer is tighter than the math suggests, fold a second 5-line trim from `## Architecture Guardrails`.)"
- ADR-tk4-003 §"Mandatory-rollout sequencing" repeats the gating rationale.

**What is missing**: An EXPLICIT post-Story-5 verification step in ADR-tk4-003 stating: "After Story 5 frontmatter rollout lands in the working tree, Stage 6 Dev runs `python3 scripts/check_skill_budgets.py` and confirms exit 0. If godot lands at 201 (post-frontmatter +3 from 198), the §W3-7 escape hatch (fold a 5-line `## Architecture Guardrails` trim) is invoked before merge."

**Empirical evidence the gap matters**: Per-file post-frontmatter projections from ADR-tk4-001 math + tk4-003 +3 lines/file:

| File | tk4-001 after | + frontmatter | Tier ceiling | Status |
|---|---:|---:|---:|---|
| architect | 288 | 291 | 300 | OK (margin 9) |
| presentation | ~160 | ~163 | 300 | OK (margin ~137) |
| ui | 273 | 276 | 300 | OK (margin 24) |
| operations | 255 | 258 | 300 | OK (margin 42) |
| quality | 276 | 279 | 300 | OK (margin 21) |
| user-feedback | 250 | 253 | 300 | OK (margin 47) |
| **godot** | **198** | **201** | **200** | **OVER by 1 — escape hatch must trigger** |

Six files clear with margin; godot is +1 over Tier-C without invoking the §W3-7 escape hatch. The escape hatch IS in tk4-001, but neither ADR ties it to an explicit post-Story-5 `check_skill_budgets.py` exit-0 verification. Stage 6 Dev could plausibly read tk4-001 §W3-7 as conditional ("if buffer is tighter than the math suggests") and skip the trim, then the post-frontmatter command exits non-zero, blocking AC-1.

**Remediation (≤5 lines into ADR-tk4-003)**: Add a §"Post-Story-5 budget verification" subsection: "After frontmatter rollout lands, Stage 6 Dev MUST run `python3 scripts/check_skill_budgets.py` and confirm exit 0. Godot is the only file with <3-line margin per tk4-001 math; the §W3-7 escape hatch (fold a 5-line `## Architecture Guardrails` trim) is MANDATORY (not conditional) before Story 5 PR merges. Other 6 files are projected to clear with margin ≥9."

NOT_PASS.

---

### Gate 5 — Stop-rule tripwire is testable (ADR or architecture must specify HOW to detect <15% prose-token reduction at first dispatches): **NOT_PASS**

**Required**: ADR or architecture must specify HOW to detect <15% prose-token reduction at first dispatches (per BACKLOG-104 §Stop-rule trigger #2 carried from caveman-lite/BACKLOG-102).

**Found in artifacts**:
- BACKLOG-104 §Stop-rule trigger #2: "first post-Wave-3 dispatches showing <15% prose-token reduction vs pre-caveman-lite baseline triggers stop-rule retro on caveman-lite BEFORE Wave 3 W3-9 governance work proceeds. W3-1..W3-8 content trims may continue under this trigger; only W3-9 (and downstream W3-10..12 that depend on frontmatter rollout) holds."
- ADR-tk4-001/002/003: NO mention of `<15% prose-token reduction` or how to detect it.
- Architecture-tk4-wave-3.md: NO stop-rule tripwire section.
- PRD §6 AC-7: cites `python3 scripts/compute_token_reduction.py --baseline pre-W0 --window 5` for the cumulative ≥50% NFR-4 measurement, but this is a different metric (cumulative cross-wave vs caveman-lite-only post-W3 prose tripwire).

**Why this matters**: BACKLOG-104 makes W3-9 (and the entire ADR-tk4-003 frontmatter rollout) GATED on this tripwire. If the architect does not specify HOW Stage 6 detects the <15% condition, Stage 6 cannot test the gate before kicking off Story 5. The gate becomes narrative-only.

**Remediation (≤5 lines into architecture-tk4-wave-3.md or as new ADR-tk4-003 subsection)**: Add: "Stop-rule tripwire detection (BACKLOG-104 §Stop-rule #2): before Story 5 (W3-9) PR opens, Stage 6 runs `python3 scripts/compute_token_reduction.py --baseline pre-caveman-lite --window <N>` over the first N post-Wave-3 dispatches (N ≥ 3). If reduction < 15%, Story 5 holds; Stories 1–4 + Story 7 admin proceed. Tripwire output is logged to `.delivery/telemetry/stop-rule-tk4.txt` for Stage 6 DoD citation." (If `compute_token_reduction.py` does not yet support `--baseline pre-caveman-lite`, that flag addition is a Stage 6 W3-18 telemetry-hardening sub-task.)

NOT_PASS.

---

## Summary scoreboard

| Gate | Verdict | Blocking? |
|---|---|---|
| 1. Decision elements TESTABLE across all 3 ADRs | PASS | — |
| 2. Cache-prefix re-freeze verification step in ADR-tk4-003 | PASS | — |
| 3. PRD AC-1..AC-7 traceability to ADR / Stage 6 dogfood | PASS | — |
| 4. Post-Story-5 `check_skill_budgets.py` exit-0 verification step | NOT_PASS | YES |
| 5. <15% prose-token reduction stop-rule tripwire detection mechanism | NOT_PASS | YES |

**Overall STATUS: NOT_DONE.** Two NOT_PASS gates, both blocking.

---

## TARGET vs CURRENT discipline check

The ADRs correctly distinguish TARGET (post-extraction line counts) from CURRENT (verified `wc -l` snapshot from PRD §3). ADR-tk4-001 math uses verified CURRENT (500/545/496/420/418/399/236) and projects TARGET (288/~160/273/255/276/250/198). No conflation detected. PRD §3 is cited as the source of CURRENT. Lesson honored.

---

## Recommended next round (round 2)

Architect spawns FRESH dispatch with two surgical edits:

1. **ADR-tk4-003 § new "Post-Story-5 budget verification"**: ~5 lines mandating post-frontmatter `check_skill_budgets.py` exit-0 + godot escape hatch as MANDATORY (not conditional).
2. **architecture-tk4-wave-3.md § new "Stop-rule tripwire detection" OR ADR-tk4-003 §new subsection**: ~5 lines specifying the runnable command + threshold for the <15% prose-token reduction tripwire, gated before Story 5 opens.

No re-architecture needed; both are testability additions to existing decisions. Round 2 estimated cost: <100 lines of architect output.

---

**Verdict (≤3 sentences)**: Three ADRs and the architecture summary land sound architectural decisions with verified math and clean cache-prefix discipline, and Gates 1–3 (testability, re-freeze procedure, AC traceability) all PASS. Gates 4 and 5 fail because two BLOCKING-style verifications — post-Story-5 budget exit-0 (godot is +1 over Tier-C without the §W3-7 escape hatch firing) and the <15%-prose-reduction stop-rule tripwire detection mechanism — are present in ADR rationale prose but missing from the explicit verification-step contract a Stage 6 Dev would run. Both gaps are surgically remediable in round 2 with two ≤5-line ADR additions and require no re-design.

— QA Engineer (DoD validator, FRESH dispatch), run-2026-05-09-tk4, Stage 4 (Architect, LIGHT) round 1.
