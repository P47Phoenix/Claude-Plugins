# Test Strategy — Opus 4.7 Plugin-Skill Migration (Plan Stage QA)

**Engagement:** `run-2026-04-22-4x7e` (FEATURE, Plan Stage)
**Author:** QA Engineer — Legolas speaking
**Upstream:** `.delivery/artifacts/08-execute/02-refine/po/execution-prd.md` (14 WIs, 4 waves, §5 Wave Gates, §7 six verification commands)
**Binding ADRs:** ADR-002, ADR-005, ADR-006
**Status:** Plan-stage test strategy; layered, not replacing the per-story dogfoods already executed by Gimli in Refine DoD.

> *"I count fourteen. Four waves. Six end-state commands. Two new CI guards. That bug still only counts as one — but I shall see each one before it reaches the gate."*
> — Legolas

---

## 1. Strategy Overview

Four layers of coverage. No overlap wasted, no gap unmanned.

- **Layer A — Per-story dogfood** (already authored and green-run by Gimli in Refine DoD; 14 commands, one per WI; see execution-PRD §2 "Dogfood / test command" blocks). Not replaced here; referenced.
- **Layer B — Wave-exit verification** (4 gates, mechanical, stated in execution-PRD §5). Each advances wave-to-wave only on pass.
- **Layer C — Sprint-exit verification** (6 commands in execution-PRD §7). These are the binding end-state gates. Re-stated in §4 below with expected outputs.
- **Layer D — Regression guards** (3 CI workflows, 2 new from WI-14 + 1 pre-existing from DEFECT-004). Protect M-01, DX-M4, and workflow-injection shape at CI time so future PRs cannot re-introduce the defects this engagement closes.

**Empirical vs reasoning-only classification.** Every AC in the execution-PRD is either:

- **EMPIRICAL** — command-verifiable: a `grep`, `test`, `jq`, or `find` exit-0/exit-nonzero decision. No prose inspection, no judgement call.
- **REVIEW-ONLY** — prose inspection required: a human reads a file and judges "recommendation present" or "tone preserved."

I classify each WI's AC-set below. The dogfood command captures the empirical cut; the review-only ACs need a named reviewer (named per WI in §2).

---

## 2. Per-WI Classification Table

Fourteen WIs. Fifty-nine ACs counted across the PRD §2 (AC-1..AC-N, excluding the redundant AC-1a which I count as AC-2). The primary-verification column names the single command that proves the WI's state; the regression-risk column names the metric that would regress on a silent failure.

| WI | AC-count | Empirical | Review-only | Primary verification | Regression risk |
|----|----------|-----------|-------------|----------------------|-----------------|
| WI-01 | 4 | 4 | 0 | `grep -cE '^\| *(idea\|refine\|...) *\|' …/4-7-as-is-dispatch-counts.md` | Premise check — a non-zero delta halts Wave 2 |
| WI-02 | 5 | 5 | 0 | `jq -e '.skill_loaded_first_attempt_rate and …' 4-7-baseline.json` | M-04 / M-05 / M-07 reference point — no baseline, no deltas |
| WI-03 | 5 | 5 | 0 | `grep -qE '^(verdict\|Verdict): *(unknown-fields-accepted\|strict)'` | ADR-006 rollback trigger — wrong verdict ships wrong frontmatter shape |
| WI-04 | 5 | 5 | 0 | `grep -q '^model_awareness: opus-4-7$' delivery-team/skills/delivery-flow/SKILL.md` | M-03 SKILL_LOADED rate; dispatch-count contract (DISP-01/02) |
| WI-05 | 7 | 6 | 1 (AC-1 PAT-01 reframe quality) | `grep -cE '^### Pattern 4\.[1-6] — ' prompt-engineer/SKILL.md` returns 6 | DX-M3 — restatement count must stay 0 |
| WI-06 | 5 | 5 | 1 (AC-2.3 URL-per-claim) | `jq -e '.pass == true and .tool_calls >= 2 and .distinct_hostnames >= 2' research-probe-result.json` | F-07 silent fetch-count regression |
| WI-07 | 5 | 3 | 2 (AC-1 recommendation quality; AC-5 persona review) | `grep -qE '(Recommendation\|Done[- ]with[- ]reason)' audits/product-delivery-f25.md` | F-25 literal-following drift in PO role rules |
| WI-08 | 4 | 3 | 1 (AC-1 per-sub-role recommendation quality) | `test "$(grep -cE '^### ' audits/architect-f25-f26.md)" -ge "11"` | F-25/F-26 drift in the 11 architect sub-roles (667 LOC surface) |
| WI-09 | 5 | 3 | 2 (AC-1 severity-HIGH tone read; AC-2 checklist scoring with soften-hatch) | `test "$(grep -cE '^- +(Weakness\|Referent\|Alternative)' adversarial-4-7-sample.md)" -ge "6"` | F-24/F-27 tone flattening on the 1181-LOC user-visible Challenger surface |
| WI-10 | 5 | 5 | 0 | `! grep -rEn 'claude-(opus-4-20250514\|sonnet-4-5-20250929\|haiku-4-20250514)' agentic-flow-builder/ prd-quality-gate-flow/ --include='*.py'` | M-01 stale-ID drift — 3→0 must not slip back |
| WI-11 | 6 | 6 | 0 | `find … \| xargs grep -L 'model_awareness:' \| wc -l` = 0 AND two tier-counts (6 keystones + 11 backfill) | DX-M4 header coverage; label-drift carry-item |
| WI-12 | 5 | 3 | 2 (AC-1 voice-preservation scoring; AC-2 M-05 ≥80% judgement) | `grep -cE '^\| *(Theme\|theme) '` ≥ 3 in alias-theme-sample.md | F-27 theme-personality flattening (M-05 baseline-diff) |
| WI-13 | 6 | 5 | 1 (AC-5 scope-statement content quality) | `ls .delivery/backlog/BACKLOG-47-*.md \| wc -l` equal to `gh issue list --label backlog-47 --json number --jq 'length'`, both ≥6 | Dual-write invariant; scope terminus hold |
| WI-14 | 6 | 5 | 1 (AC-5 post-merge synthetic-test validation) | `test -f .github/workflows/skill-md-header-warn.yml && test -f .github/workflows/stale-model-id-guard.yml` plus both carry `pull_request:` | M-02 stale-ID regression reintroduction; DX-M4 header-missing warning |

**Totals:** 14 WIs | 73 AC-points counted | 63 EMPIRICAL | 10 REVIEW-ONLY. Review-only ACs cluster in WI-05/07/08/09/12/13/14 — the audit/tone/persona reads. No WI is fully review-only; every WI carries at least one mechanical gate.

---

## 3. Wave Exit Tests

Four waves. Four gates. Each is a file-state or command-exit check, not a meeting.

### Wave 1 → Wave 2

- **Exit command:** `grep -qE '^(verdict|Verdict): *(unknown-fields-accepted|strict) *$' .delivery/artifacts/run-2026-04-22-4x7e/research/ndoc-02-spike.md`
- **Pass criterion:** exit 0 AND the verdict string is exactly one of `unknown-fields-accepted` or `strict`.
- **On fail:** HALT. No Wave 2 dispatch. WI-03 re-run. If `strict`, ADR-006 mechanical rollback activates — WI-04/05/06/11 flip to HTML-comment placement; semantics identical, placement differs.
- **Secondary check (WI-01/02 baseline readiness):** `test -f …/4-7-as-is-dispatch-counts.md && test -f …/4-7-baseline.json`. Without baseline, Waves 2–4 have no reference for M-03/M-04/M-05/M-07 deltas. If baseline aborted per WI-02 AC-4 (due to WI-01 R-09 fusion), HALT and escalate before Wave 2.

### Wave 2 → Wave 3

- **Exit command:** `test "$(grep -cE '^### Pattern 4\.[1-6] — ' prompt-engineer/SKILL.md)" = "6"`
- **Pass criterion:** exit 0 AND count is exactly 6 (Patterns 4.1–4.6 per ADR-005).
- **On fail:** HALT Wave 3. WI-07 and WI-08 cite patterns by name; orphan citations are a hard no-go. Retry WI-05 pattern installation. If Wave 2 frontmatter edits on WI-04/WI-05/WI-06 did not land their three-field frontmatter, also halt — the CI check from WI-14 will fail on merge anyway.
- **Secondary check:** `grep -q '^model_awareness: opus-4-7$' delivery-team/skills/delivery-flow/SKILL.md` AND same on `prompt-engineer/SKILL.md`. Both keystone stamps present.

### Wave 3 → Wave 4

- **Exit command (two parts, both required):**
  1. `test -f .delivery/artifacts/run-2026-04-22-4x7e/observability/research-probe-result.json && jq -e '.pass != null' research-probe-result.json`
  2. `test -f .delivery/artifacts/run-2026-04-22-4x7e/user-feedback/adversarial-4-7-sample.md`
- **Pass criterion:** both artifacts exist AND their dogfood commands succeeded (pass-path) OR their edit-path (fail-path) completed within Wave 3 and the re-run succeeded.
- **On fail:** RETRY within wave. WI-06 fail triggers the targeted prose edit ("WebFetch every primary source; never infer a fact without a URL"); WI-09 fail triggers tone-strengthening on `mtg-commander/SKILL.md`. Both edits are scoped and bounded — do not leak into Wave 4.
- **Secondary check:** WI-07 and WI-08 audit files exist and contain the per-file recommendation/Done-with-reason markers.

### Wave 4 → UAT

- **Exit commands (three, all required):**
  1. `! grep -rEn 'claude-(opus-4-20250514|sonnet-4-5-20250929|haiku-4-20250514)' agentic-flow-builder/ prd-quality-gate-flow/ --include='*.py'` (M-01 zero).
  2. `test "$(find . -name SKILL.md -not -path './.delivery/*' -not -path './node_modules/*' | xargs grep -L 'model_awareness:' | wc -l)" = "0"` (DX-M4 zero).
  3. `test -f .github/workflows/skill-md-header-warn.yml && test -f .github/workflows/stale-model-id-guard.yml` (WI-14 present).
- **Pass criterion:** all three exit 0.
- **On fail:** ESCALATE. Wave 4 is the terminus — a fail here means §7 sprint-exit will fail. No UAT dispatch until green.

---

## 4. Sprint Exit Tests — The Six §7 Commands

Reproduced verbatim from execution-PRD §7. Each is binding. Each has an expected output and a one-line proof-note.

### 1. M-01 — zero stale dated Claude model IDs in Python surfaces

```sh
! grep -rEn 'claude-(opus-4-20250514|sonnet-4-5-20250929|haiku-4-20250514)' agentic-flow-builder/ prd-quality-gate-flow/ --include='*.py'
```

- **Expected:** exit 0 (no hits).
- **Proves:** WI-10 closed MID-01/02/03/04. No stale 4.5/4.6/earlier dated IDs remain in the two Python surfaces scanned by the PRD.

### 2. DX-M4 — zero SKILL.md files missing the `model_awareness` header

```sh
find . -name SKILL.md -not -path './.delivery/*' -not -path './node_modules/*' | xargs grep -L 'model_awareness:' | wc -l
```

- **Expected:** `0`.
- **Proves:** WI-04/05/06/07/08/09 keystones stamped, WI-11 backfilled the remaining 11. ADR-006 coverage is total across tracked SKILL.md files.

### 3. WI-11 honest two-tier stamp integrity — six keystones + eleven backfill files

```sh
test "$(find . -name SKILL.md -not -path './.delivery/*' -not -path './node_modules/*' | xargs grep -l '^model_awareness: opus-4-7$' | wc -l)" = "6" && \
test "$(find . -name SKILL.md -not -path './.delivery/*' -not -path './node_modules/*' | xargs grep -l '^model_awareness: opus-4-7-frontmatter-only$' | wc -l)" = "11"
```

- **Expected:** exit 0 (6 keystones reviewed-in-prose + 11 frontmatter-only backfilled; carry-item label drift resolved).
- **Proves:** the honest two-tier label holds. No false "reviewed" claim on mechanical backfills.

### 4. DX-M3 — zero restatements of `<thinking>` outside the canonical pattern library

```sh
grep -rn '<thinking>' delivery-team/ mtg-commander/ research-agent/ agentic-flow-builder/ prd-quality-gate-flow/ | grep -v 'prompt-engineer/SKILL.md' | wc -l
```

- **Expected:** `0`.
- **Proves:** WI-05 AC-6/AC-7 closed the last external restatement (the `research-agent/references/prompt-library.md:10` retarget). The pattern library is the single source.

### 5. WI-13 dual-write invariant — local file count equals GitHub `backlog-47` issue count, both ≥ 6

```sh
test "$(ls .delivery/backlog/BACKLOG-47-*.md 2>/dev/null | wc -l)" -ge "6" && \
test "$(gh issue list --label backlog-47 --state all --json number --jq 'length')" -ge "6" && \
test "$(ls .delivery/backlog/BACKLOG-47-*.md 2>/dev/null | wc -l)" = "$(gh issue list --label backlog-47 --state all --json number --jq 'length')"
```

- **Expected:** exit 0 (both surfaces agree).
- **Proves:** every deferral has both a local file and a labeled GitHub issue. Neither surface stale. The user-directed dual-write invariant holds.

### 6. WI-14 CI guard files present

```sh
test -f .github/workflows/skill-md-header-warn.yml && \
test -f .github/workflows/stale-model-id-guard.yml && \
test -f .github/workflows/workflow-injection-lint.yml
```

- **Expected:** exit 0 (two new guards exist; DEFECT-004 guard still present).
- **Proves:** future PRs cannot re-introduce a stale ID (blocking) or land an unheaderred SKILL.md (warning), and the pre-existing workflow-injection guard was not accidentally removed.

---

## 5. Regression Guards

Three CI workflows under `.github/workflows/`. Two new, one pre-existing. Each has a single defect it prevents from returning.

- **`stale-model-id-guard.yml`** — WI-14 AC-2, BLOCKING. Runs M-01 regex on `pull_request`. Blocks PR on any hit in tracked `.py` or `.md` files outside `.delivery/` and `prd_flows.db`. Post-merge synthetic test per WI-14 AC-5: a test PR re-introducing `claude-opus-4-20250514` must fail this check. **Guards:** M-01/M-02 — zero stale dated IDs.
- **`skill-md-header-warn.yml`** — WI-14 AC-1, WARNING (non-blocking). Runs `git ls-files '*SKILL.md' ':!:.delivery/*' | xargs grep -L 'model_awareness:'` on `pull_request` and logs missing-header files as a PR comment or job warning. Post-merge synthetic test: a test PR introducing a new SKILL.md without `model_awareness:` must produce a warning but not block. **Guards:** DX-M4 — header coverage.
- **`workflow-injection-lint.yml`** — PRE-EXISTING (DEFECT-004 regression guard). Must not regress per PRD Constraint 6 / §7 command 6 / WI-14 AC-4. Fails PRs that interpolate `${{ github.event.* }}` directly inside workflow `run:` blocks. **Guards:** DEFECT-004 workflow injection vulnerability.

All three must be green on the merge PR for this migration. WI-14 AC-6 sequences the new two AFTER WI-10 (so the blocking guard passes) and AFTER WI-11 (so the warning guard sees zero missing).

---

## 6. Negative Testing

Three dogfood gates can legitimately fail and trigger a scoped edit-path. Each has a known fail-mode, a named executor, and a confirmation command.

### WI-06 — research-agent tool-use probe

- **Fail condition:** `research-probe-result.json.pass == false` (i.e., fewer than 2 `WebFetch`/`WebSearch` tool calls, or fewer than 2 distinct hostnames, or a factual claim missing a URL).
- **Edit-path (WI-06 AC-4):** developer edits `research-agent/SKILL.md` with the F-28 calibrated-voicing line: *"WebFetch every primary source; never infer a fact without a URL."* Scope is that prose edit; no reference-file edits, no schema changes.
- **Executor:** developer sub-agent (dogfood-before-edit primitive); QA re-runs the probe.
- **Confirm fix:** re-run WI-06 dogfood command. `jq -e '.pass == true and .tool_calls >= 2 and .distinct_hostnames >= 2'` must exit 0.

### WI-09 — mtg-commander adversarial-tone sample

- **Fail condition:** severity-HIGH tone/depth regression vs `4-7-baseline.json.challenger_sample_path` OR AC-04.2 checklist unmet (fewer than 3 weaknesses, 2 card-name referents, 1 alternative) without an explicit soften-hatch declaration for small-input invocations.
- **Edit-path (WI-09 AC-3):** targeted tone-strengthening prose edit in `mtg-commander/SKILL.md`. NOT a rewrite of scryfall integration, price logic, or the deck-building pipeline.
- **Executor:** developer sub-agent; user-feedback persona re-reviews.
- **Confirm fix:** re-run WI-09 dogfood. `grep -cE '^- +(Weakness|Referent|Alternative)' adversarial-4-7-sample.md` ≥ 6 AND no severity-HIGH regression flag on the persona-review artifact.

### WI-12 — alias-theme voice preservation

- **Fail condition:** fewer than 80% of sampled announcements preserve voice (M-05 target unmet), where "preserve" = ≥50% of extracted `roles[].catchphrase` + `roles[].examples[]` markers present in the rendered announcement.
- **Edit-path (WI-12 AC-3):** tone-strengthening of the affected theme YAML files under `delivery-team/skills/delivery-flow/references/aliases/`. NOT edits to `alias-creator/SKILL.md` or the `theme-format.md` schema.
- **Executor:** developer sub-agent (YAML-only edits); QA re-samples.
- **Confirm fix:** re-run WI-12 dogfood. Table still ≥3 rows; `grep -qE 'voice[- ]preservation|markers? preserved'` succeeds; re-extracted marker rate ≥80%.

---

## 7. Test Data

Two data references. Both captured in Wave 1. Both load-bearing for every downstream regression check.

- **`4-7-baseline.json` (WI-02)** — the single `jq`-queryable reference point for all regression-vs-baseline metrics:
  - **M-04 (adversarial review depth)** — `challenger_sample_path` field. WI-09 diffs against this.
  - **M-05 (alias theme voice preservation)** — `alias_announcement_samples` array. WI-12 diffs against this.
  - **M-07 (audit-hook warning count)** — `audit_hook_warning_count` integer. Post-sweep deltas compared against this baseline integer.
  - **M-03 (SKILL_LOADED hit rate)** — `skill_loaded_first_attempt_rate` float. WI-04 AC-03.3 asserts `≥ max(0.95, baseline_rate − 0.02)`.
  - **Integrity:** per WI-02 AC-4, the baseline aborts (is not written) if WI-01 surfaces R-09 fusion. A missing baseline file is a HALT, not a pass.

- **`4-7-as-is-dispatch-counts.md` (WI-01)** — the premise-check table. Rows cover idea (expect 2), refine (expect 4), design (expect 5), architect (expect 5), plan (expect 5), development (expect 4), uat (expect 4). **Any delta >0 halts Wave 2** — this is the silent F-08 fusion guard. If deltas are all zero: "Assumption A-05 firmed at count level." If any delta >0: R-09 raised, mitigation WI sequenced before WI-04 lands.

No other test-data surfaces are created by this engagement. Transcript files under `observability/` (research probe) and `user-feedback/` (adversarial sample, alias theme sample) are evidence artifacts, not reference data.

---

## 8. Exit Criteria — Sprint Definition of Done (QA Perspective)

This is what I check before I stamp DONE. Five gates. All must pass.

- [ ] **Gate 1 — All 14 WI dogfoods PASS.** Per-story commands in execution-PRD §2. Already green-run by Gimli in Refine DoD; re-run on the implementation branch before merge.
- [ ] **Gate 2 — All 4 wave-exit gates PASS in order.** Wave 1→2 (NDOC-02 verdict), Wave 2→3 (6 patterns installed), Wave 3→4 (research probe + adversarial sample verdicts recorded), Wave 4→UAT (M-01 zero, DX-M4 zero, CI files present). No wave advances on a fail; retry or rollback per ADR-006 / §6 rollback protocol.
- [ ] **Gate 3 — All 6 §7 sprint-exit commands PASS.** M-01, DX-M4, two-tier stamp integrity (6+11), DX-M3, dual-write invariant, CI guards present. Each exit-0; each expected value matched.
- [ ] **Gate 4 — WI-14 stale-ID regression guard installed and green on the merge PR.** `stale-model-id-guard.yml` must run on the merge PR and exit clean. A failing guard blocks merge — even a true-positive hit means Wave 4 did not land.
- [ ] **Gate 5 — Zero severity-HIGH regressions vs `4-7-baseline.json`.** Four axes: tone (M-04 challenger sample diff), adversarial depth (AC-04.2 checklist), dispatch count (M-03 stage-by-stage), SKILL_LOADED rate (≥ max(0.95, baseline_rate − 0.02)). Any severity-HIGH regression halts sprint-exit and routes back to the relevant WI's edit-path.

Alongside the five gates: the CODE_COMPLETE distinction. This engagement is prose-and-CI, not runtime software. No empirical-only ACs of the "requires running the application" class exist. All 14 WIs are inspectable via the dogfood commands. QA status: full DONE possible at the five-gate green, no CODE_COMPLETE handoff needed to UAT for runtime verification.

---

## 9. Assumptions and Risks

Stated explicitly. Hidden assumptions cause escapes.

- **Assumption 1:** the Wave 1 baseline (`4-7-baseline.json`) captures a non-degraded run. If the baseline run itself was degraded, Waves 2–4 will measure deltas against a falsely-low reference and silent regressions will pass. Mitigation: WI-01 R-09 halts baseline capture if F-08 fusion is already occurring.
- **Assumption 2:** the six §7 commands are portable across contributor shells (bash and fish). The G-2 Refine fix replaced shell-globs with `find | xargs grep`. No `yq` dependency after G-1. I have not re-verified on Windows PowerShell; this is UAT's call.
- **Assumption 3:** `gh issue list --label backlog-47` counts all matching issues across open AND closed state (WI-13 dogfood uses `--state all`). If a user closes a BACKLOG-47 issue without deleting the local file, the invariant still holds. Orphaning either surface is the only break.
- **Risk R-HIGH-01 (NDOC-03):** no Anthropic adversarial-review benchmark exists for 4.7. WI-09 severity-HIGH tone regression is a human judgement against baseline, not a published reference. Mitigation: baseline-anchored rule AND soften-hatch AND persona re-review.
- **Risk R-MED-02:** the 10 review-only ACs (WI-05 AC-1, WI-07 AC-1/AC-5, WI-08 AC-1, WI-09 AC-1/AC-2, WI-12 AC-1/AC-2, WI-13 AC-5, WI-14 AC-5) depend on reviewer judgement. Mitigation: each has a paired empirical AC that captures the file-state cut; the review-only portion judges semantic quality, not existence.

---

*"Fourteen stories, four waves, six commands, three guards. I have counted each one. I have named each path to fail. Now the shot is clean."*
— Legolas

---

```
STATUS: DONE
ARTIFACT: .delivery/artifacts/08-execute/05-plan/qa/test-strategy.md
SUMMARY: Four coverage layers mapped; 14 WIs classified (63 empirical, 10 review-only); 4 wave gates and 6 sprint-exit commands restated — that bug still only counts as one.
```
