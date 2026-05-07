<!-- run: run-2026-05-05-tk3 | stage: 07-uat | depth: full | author: QA Engineer (Legolas Greenleaf) | role: qa-engineer | task: dogfood-report -->

# Dogfood Report — Caveman-Lite Prose Discipline (run-2026-05-05-tk3)

> "I do not see what others see — yet. The wind tells me what comes."
> — Legolas, on baselines and forecasts.

The empirical core of UAT. Pre-merge structural-only verification + post-merge measurement protocol carry-forward. Per UAT memory lesson 3, structural-only confidence is capped at 4/5 and carries a P1 follow-up.

## Section 1: Pre-merge baseline establishment

### Telemetry inspection

Read `.delivery/telemetry/skill-loads.jsonl` (BACKLOG-100 W0-1 hook output): 10 rows, all from a single 21-millisecond burst on 2026-05-04T02:55:05Z, all with `input_tokens: 0`, `cache_read_tokens: 0`, `cache_write_tokens: 0`, `model: null`. These are placeholder rows from hook-bring-up, not real dispatch measurements. **The telemetry file is unusable as a numeric prose-token baseline.**

### Archive fallback (per task spec)

Per the dispatch directive, fall back to `.delivery/memory/archive/run-2026-05-05-tk2.md` (Wave 2 archive, predecessor commit c2e7d5a). Citing the Wave 2 archive § "Pipeline cost notes":

> "Total Agent dispatches: ~50 (5 stage primaries + 5 implementations + 22+ DoD validators + revisions). Sonnet primaries, Haiku DoD validators per binding. Wave 2 the highest-cost wave to date due to story scope and DoD round-2/3/4 corrections."

The archive does NOT record per-dispatch prose-token figures explicitly. What it DOES establish:

- **Pre-Wave-2 SKILL.md size**: 999 lines (Story 1 reduced to 497).
- **Wave 2 doctrine extraction**: ~406 lines extracted to `references/shared/orchestrator-doctrine.md`.
- **Wave 2 first-try DoD pass-rate**: ~50% of stage-stories (regression vs Wave 1 ~55%).
- **Defect/story rate**: 0 blocking / 5 stories = 0.0 (well under 0.4 stop-rule).

### Documented baseline (proxy)

Since direct prose-token telemetry is unavailable, the de-facto Wave 2 baseline this run will be measured AGAINST is the running average prose-byte length of dispatch responses across the 50+ agent dispatches in Wave 2. The first 5 post-merge dispatches in `run-2026-05-05-tk4` (or whatever the next run-id is) become the post-merge sample. The reduction is computed against the Wave 2 mean.

**Baseline status**: documented but not numerically pinned. Post-merge measurement is the FIRST empirical pin; comparison is against Wave 2 narrative cost (qualitative reasoning informed by archive size deltas), then becomes self-comparable Wave-on-Wave once 2+ post-merge runs exist.

## Section 2: Synthetic structural dogfood (5 dispatches)

For each of these 5 synthetic dispatches, I verify the orchestrator's prompt-construction logic by:
1. Constructing what the Phase 4 Step 4 prompt WOULD be for a sample dispatch under each condition.
2. Checking that the PROSE STYLE block IS / IS NOT injected per the conditional logic.

This is structural-by-design — the PROSE STYLE block is in-prompt directive (ADR-tk3-001 Element 3); the agent itself is the detector. No real Agent dispatch is required to close AC-5 / AC-6 structurally.

### Dispatch 1 — Default config (prose_style absent → caveman-lite via v2.7→v2.9 migration default)

**Setup**: Read `.delivery/config.yml` — confirmed `config_version: "2.7"`, `prose_style:` key ABSENT.

**Verify Phase 0 directive**: SKILL.md L74:
> "Read `prose_style` (top-level; default `caveman-lite`; valid `caveman-lite | standard`); cache on loaded-config..."

**Verify pipeline-stages.md template (Primary, L72-74)**: Conditional line `{when config.prose_style == caveman-lite: inject the line below verbatim; when standard: omit this entire section}` followed by the verbatim PROSE STYLE block.

**Constructed dispatch prompt (excerpt)**: under v2.7→v2.9 migration default, `prose_style` resolves to `caveman-lite` → PROSE STYLE block IS injected. The `--- PROSE STYLE ---` delimiter and verbatim block (33-line caveman-lite directive with auto-clarity exemption clause) appears between `--- ALIAS ---` (L69) and `--- OUTPUT ---` (L76).

**PASS condition**: caveman-lite directive would be active by default. **PASS** — confirmed structurally.

### Dispatch 2 — Auto-clarity exemption: security warning context

**Setup**: Construct sample agent prompt that includes a security-related instruction (e.g., "the new `prose_style` key must NOT contain user input — config values are static enum; no injection vector").

**Verify exemption clause**: PROSE STYLE block contains verbatim:
> "Auto-clarity exemptions apply: standard prose for security warnings, irreversible-op confirmations, multi-step sequences, user clarifications."

`grep -F "security warnings"` in `pipeline-stages.md` → 3 matches (one per template). `references/prose-style.md` L12 contains the verbatim block; `references/prose-style.md` L15-17 codifies "the four exempt contexts ... revert to standard prose even when caveman-lite is active. The agent itself is the detector (per ADR-tk3-001 Element 3)."

**PASS condition**: directive itself instructs agent to use STANDARD prose for security warnings; exemption mechanism is in-prompt per ADR Element 3. **PASS** — verbatim clause present in all three template slots and codified in canonical reference.

### Dispatch 3 — Auto-clarity exemption: destructive-op confirmation

**Setup**: Construct sample agent prompt that includes a `git revert` confirmation or `rm -rf` dogfood instruction.

**Verify exemption clause**: same PROSE STYLE block contains verbatim "irreversible-op confirmations" — `grep -F "irreversible-op confirmations"` in `pipeline-stages.md` → 3 matches.

**PASS condition**: directive contains the verbatim clause. **PASS** — verbatim clause present in all three template slots.

### Dispatch 4 — Auto-clarity exemption: multi-step sequences

**Setup**: Construct sample agent prompt that includes a 4-step migration sequence (e.g., the v2.7→v2.9 config migration steps in this very run).

**Verify exemption clause**: same PROSE STYLE block contains verbatim "multi-step sequences" — `grep -F "multi-step sequences"` in `pipeline-stages.md` → 3 matches.

**PASS condition**: directive contains the verbatim clause. **PASS** — verbatim clause present.

### Dispatch 5 — Opt-out: `prose_style: standard`

**Setup**: Construct hypothetical config with `prose_style: standard` (would be added as a top-level key in `.delivery/config.yml`).

**Verify SKILL.md Phase 0 + Step 4 logic**: SKILL.md L338 reads:
> "if `standard`, omit the block entirely (no placeholder line). Same rule applies uniformly to Primary (this Step 4), Supporting (Step 5), and DoD Validator (Step 7) dispatches."

**Verify pipeline-stages.md conditional**: L73, L120, L172 each contain the verbatim conditional `{when config.prose_style == caveman-lite: inject the line below verbatim; when standard: omit this entire section}`.

**Constructed dispatch prompt (excerpt)**: under `prose_style: standard`, the orchestrator OMITS the entire `--- PROSE STYLE ---` section. The dispatch goes directly from `--- ALIAS ---` to `--- OUTPUT ---` with no PROSE STYLE delimiter and no verbatim block.

**PASS condition**: opt-out path structurally present and unambiguous. **PASS** — confirmed in all four authoritative locations (3 templates + SKILL.md Step 4).

## Section 3: Post-merge measurement plan (carry-forward)

The empirical AC-13 sub-clause (BACKLOG-102 initiative AC-1 token reduction; AC-2 DoD review byte reduction) cannot close pre-merge. Documented protocol for the next full pipeline run:

### Source of post-merge sample

Telemetry from the next pipeline run's most recent 5 dispatches (any role, any stage). Use BACKLOG-100 W0-1 hook output at `.delivery/telemetry/skill-loads.jsonl`. **Important**: the 10 zero-token rows currently in the file from the 2026-05-04 hook bring-up should be ignored or archived; the post-merge sample begins with the first dispatch in the next run-id (`run-2026-05-05-tk4` or successor).

### AC-1 reduction calculation (≥20% target)

```
pre_mean  = Wave 2 archive narrative-prose-byte average across 5 sampled dispatches
            (sample from .delivery/artifacts/06-dev/developer/*.md non-fenced prose
             across run-2026-05-05-tk2 if telemetry rows are missing per-dispatch
             token figures)
post_mean = mean(response_prose_tokens) over 5 most recent rows in
            .delivery/telemetry/skill-loads.jsonl with run_id starting
            'run-2026-05-05-tk4' (or successor)
reduction = (pre_mean - post_mean) / pre_mean
PASS      iff reduction >= 0.20
WARNING   iff 0.15 <= reduction < 0.20
STOP-RULE iff reduction < 0.15  → pause Tier-2 A/B; root-cause retro
```

### AC-2 DoD review byte reduction (≥25% target)

```
pre_bytes  = mean over 5 .delivery/artifacts/*/dod/*-review.md from run-2026-05-05-tk2
             (find . -path '*/dod/*-review.md' -path '*tk2*')
post_bytes = same across run-2026-05-05-tk4 (or successor)
reduction  = (pre_bytes - post_bytes) / pre_bytes
PASS       iff reduction >= 0.25
WARNING    iff 0.20 <= reduction < 0.25
STOP-RULE  iff reduction < 0.20 OR any post-merge review missing a finding
           that the Wave 2 equivalent flagged (over-compression failure)
```

### AC-3 DoD pass-rate preserved (≥4/7 first-try baseline)

```
post_pass_rate = grep -h '^STATUS: DONE' across run-2026-05-05-tk4 dod review files
                 / total validator dispatches in tk4
threshold      = >= 4/7 (matches memory/index.md baseline)
PASS           iff post_pass_rate >= threshold
STOP-RULE      iff any post-merge review missing a finding due to over-compression
```

### AC-4 downstream artifact quality

```
PASS iff next run's PRD/ADR/release-notes are read by downstream agents without
        re-read or clarification dispatches; UAT spot-checks transcript bytes for
        clarification round-trips that did not occur in Wave 2 baseline
```

### Where to record the measurement

After the next full pipeline run closes, record results in:
1. `.delivery/memory/topics/skill-token-economy.md` — append Tier-1 measurement results section with PASS/WARNING/STOP outcomes.
2. `.delivery/memory/archive/run-2026-05-05-tk4.md` (or successor) — record reduction percentages in §"Pipeline cost notes".
3. If STOP-RULE fires: also create `.delivery/defects/backlog-102-stop-rule-retro.md` with root-cause analysis.

## Section 4: Confidence rating

**Structural confidence**: 5/5 — all 8 TCs pass; all 5 synthetic dispatches verify conditional logic; all 6 ADR-tk3-001 contract elements structurally complete.

**Empirical confidence**: capped at 4/5 per UAT memory lesson 3 — the AC-13 sub-clause (BACKLOG-102 initiative AC-1/AC-2 telemetry deltas) requires a post-merge pipeline run that cannot happen pre-merge by definition.

**Aggregate confidence**: **4/5** (capped).

### Carry-forward (P1 follow-up)

Empirical AC-13 measurement deferred to next pipeline run; expected ≥20% reduction per Wave 0/1/2 telemetry trends (Wave 2 doctrine extraction reduced SKILL.md from 999→497 lines, structural baseline already favorable for further per-response reduction); if the first post-merge run shows <15% prose-token reduction OR <20% DoD review byte reduction, trigger BACKLOG-102 stop-rule retro and pause Tier-2 A/B (per BACKLOG-102 §Stop-rule and §Sequencing relative to BACKLOG-101).

**Owner**: PO + QA jointly at the close of the next pipeline run. Surface as the first agenda item of the next-run UAT.

---

STATUS: CODE_COMPLETE
ARTIFACT: .delivery/artifacts/07-uat/qa/dogfood-report.md
SUMMARY: 5/5 synthetic dispatches PASS structurally; AC-13 telemetry carry-forward to next run; confidence 4/5 capped per UAT memory lesson 3.
