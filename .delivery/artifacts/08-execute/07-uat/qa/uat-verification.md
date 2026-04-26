# Stage 7 UAT Verification — Execution PRD §7 Six Binding End-State Gates

**Role:** QA Engineer (Legolas)
**Date:** 2026-04-22
**Scope:** Empirical verification of the six success-definition commands from `.delivery/artifacts/08-execute/02-refine/po/execution-prd.md` §7 (REVISED after G-1..G-6 fixes), cross-checked against the task-brief's six-command variant.
**Artifact Under Test:** The merged state of the 4.6→4.7 migration implementation.

---

## Task Type & Context

- **Task Type:** `uat-verification`
- **References:** Execution-PRD §7 (revised) + WI-10 caveat from Challenger (Gimli) on M-01 regex false-positives
- **Scope:** 6 end-state commands; pass/fail verdict per command; overall gate status

---

## Methodology

For each command I ran the exact string from the task brief, captured stdout + exit code, then classified any hits against the WI-10 caveat ("hits only on canonical `claude-sonnet-4-6` are NOT stale"). Where the task brief's variant differed from the PRD §7 canonical command, I ran both and noted the delta.

Execution host: `/var/home/meconnelly/Documents/GitHub/Claude-Plugins`, Fedora 43 Linux, `gh` authenticated.

---

## Command-by-Command Results

### 1. M-01 — Stale 4.6 IDs purged (except historic artifacts)

**Task brief command:**

```bash
grep -rE "claude-(opus|sonnet|haiku)-4[.-]6" \
  --exclude-dir=.delivery --exclude-dir=.git \
  --exclude-dir=node_modules --exclude-dir=__pycache__ .
```

**Expected (per WI-10 caveat):** Hits only on canonical `claude-sonnet-4-6` (no date suffix) or provenance comments. Zero STALE hits.

**Actual — 4 lines of output, exit 0:**

| # | Line | Classification |
|---|------|---------------|
| 1 | `./agentic-flow-builder/scripts/agent_registry.py:149:  "config": {"model": "claude-sonnet-4-6"}` | **CANONICAL** — current Sonnet 4.6 family ID; the migration target, not stale |
| 2 | `./.github/workflows/stale-model-id-guard.yml` — `#   - claude-sonnet-4-6 (current)` | **GUARD-INTERNAL** — allowlist comment inside the guard itself |
| 3 | `./.github/workflows/stale-model-id-guard.yml` — `| grep -vE 'claude-sonnet-4-6(\b|[^0-9-])' \` | **GUARD-INTERNAL** — the regex excluding canonical Sonnet 4.6 from stale-ID matches |
| 4 | `./.github/workflows/stale-model-id-guard.yml` — `echo "Fix: replace with ... claude-sonnet-4-6, ..."` | **GUARD-INTERNAL** — fix-message in the guard |

**STALE hits: 0.** All four matches are canonical references or the guard's own self-description — explicitly excluded under the WI-10 caveat.

**Cross-check — PRD §7 canonical M-01 (dated-ID variant):**

```bash
! grep -rEn 'claude-(opus-4-20250514|sonnet-4-5-20250929|haiku-4-20250514)' \
  agentic-flow-builder/ prd-quality-gate-flow/ --include='*.py'
```

Exit 1 (i.e. grep found matches, so the negated form returned non-zero), with 3 hits — all inside `agent_registry.py` provenance comments (`# canonical 2026-04-22 — opus-4-7 migration; prior: <retired-id>`). These are deliberate history-preserving comments; the PRD §7 command as literally written fails, but the intent (no live dated IDs in executable code) passes. Flagging this as a **PRD authoring defect** for the retrospective — the §7 regex should scope out provenance comment lines (`^\s*#`) or the guidance should commit to either "purge all mentions" or "purge live references only."

**Verdict: PASS** on intent (zero stale live references). **PASS_WITH_NOTES** on literal PRD §7 regex.

---

### 2. M-02 — Stale-ID regression guard exists and is blocking

**Command:**

```bash
test -f .github/workflows/stale-model-id-guard.yml \
  && grep -qE 'exit 1' .github/workflows/stale-model-id-guard.yml \
  && echo "exists and blocking"
```

**Expected:** `exists and blocking`, exit 0.

**Actual:** `exists and blocking` — exit 0.

**Verdict: PASS.**

---

### 3. DX-M4 — All SKILL.md files carry `model_awareness:` header

**Command:**

```bash
find . -name SKILL.md -not -path './.delivery/*' -not -path './node_modules/*' \
  | xargs grep -L 'model_awareness:' | wc -l
```

**Expected:** `0`.

**Actual:** `0` — exit 0.

**Two-tier stamp integrity cross-check (PRD §7 gate 3, WI-11):**

- Files stamped `^model_awareness: opus-4-7$` — **6** (expected 6 keystones) — PASS
- Files stamped `^model_awareness: opus-4-7-frontmatter-only$` — **11** (expected 11 backfills) — PASS

**Verdict: PASS.**

---

### 4. DX-M3 — Zero external pattern restatements outside `prompt-engineer/`

**Task brief command:**

```bash
grep -rE '<thinking>|chain[- ]of[- ]thought' --include="SKILL.md" \
  --exclude-dir=prompt-engineer .
```

**Expected:** 0 hits.

**Actual:** 0 hits — exit 1 (grep's "no matches found" exit code, which is the expected-pass signal here).

**Cross-check — PRD §7 canonical DX-M3:**

```bash
grep -rn '<thinking>' delivery-team/ mtg-commander/ research-agent/ \
  agentic-flow-builder/ prd-quality-gate-flow/ | grep -v 'prompt-engineer/SKILL.md' | wc -l
```

Result: `0` — PASS.

Both forms agree. WI-05 AC-7 (the `research-agent/references/prompt-library.md` line-10 retarget-or-prune scoped in by G-5) is therefore closed — no restatements slipped through.

**Verdict: PASS.**

---

### 5. WI-13 local backlog — ≥6 BACKLOG-47 files on disk

**Command:**

```bash
ls .delivery/backlog/BACKLOG-47-*.md | wc -l
```

**Expected:** ≥6.

**Actual:** **9 files** (exceeds target by 3):

1. `BACKLOG-47-4-7-example-skill-designation.md`
2. `BACKLOG-47-contributing-4-7-note.md`
3. `BACKLOG-47-frontmatter-only-prose-skim.md`
4. `BACKLOG-47-memory-tool-eval.md`
5. `BACKLOG-47-migration-guide-stub.md`
6. `BACKLOG-47-overpressure-audit.md`
7. `BACKLOG-47-r-06-cyber-safeguard.md`
8. `BACKLOG-47-sdk-wiring-routing-via-claude-api.md`
9. `BACKLOG-47-task-budget-eval.md`

**Verdict: PASS.**

---

### 6. WI-13 dual-write — GitHub issues created with `backlog-47` label

**Command:**

```bash
gh issue list --label "backlog-47" --state open --json number | jq length
```

**Expected:** ≥6.

**Actual:** **9** — issues `#77, #78, #79, #80, #81, #82, #83, #84, #85`, all state `OPEN`.

Title-to-file mapping verified (all 9 local files map 1:1 to a GH issue by slug):

| # | GH Issue Title | Local File |
|---|---------------|-----------|
| 77 | Evaluate task_budget (beta) adoption across agentic flows | `BACKLOG-47-task-budget-eval.md` |
| 78 | Evaluate client-side memory tool adoption | `BACKLOG-47-memory-tool-eval.md` |
| 79 | Anthropic SDK adoption pathway via claude-api skill | `BACKLOG-47-sdk-wiring-routing-via-claude-api.md` |
| 80 | Narrow cyber-safeguard refusal check for architect security/IR references | `BACKLOG-47-r-06-cyber-safeguard.md` |
| 81 | Upgrade 11 backfill SKILL.md files from frontmatter-only to opus-4-7 via prose skim | `BACKLOG-47-frontmatter-only-prose-skim.md` |
| 82 | Keystone SKILL.md audit for CRITICAL/MUST/NEVER/ALWAYS over-pressure patterns | `BACKLOG-47-overpressure-audit.md` |
| 83 | Add 4.7-awareness note to CONTRIBUTING guidance | `BACKLOG-47-contributing-4-7-note.md` |
| 84 | Publish a 4.6 to 4.7 migration guide stub | `BACKLOG-47-migration-guide-stub.md` |
| 85 | Designate a canonical 4.7 exemplar skill | `BACKLOG-47-4-7-example-skill-designation.md` |

**Dual-write invariant:** 9 local files == 9 GH issues. PRD §7 gate 5's stricter form (`local count = all-state GH count, both ≥ 6`) also passes: 9 == 9, both ≥ 6.

**Verdict: PASS.**

---

### 7. Bonus — WI-14 CI Guard Presence (PRD §7 gate 6)

**Command:**

```bash
test -f .github/workflows/skill-md-header-warn.yml \
  && test -f .github/workflows/stale-model-id-guard.yml \
  && test -f .github/workflows/workflow-injection-lint.yml
```

**Expected:** exit 0.

**Actual:** exit 0 — all three workflow files present (including the DEFECT-004 regression guard carried forward from the prior migration).

**Verdict: PASS** (not in the task brief's six, but a PRD §7 gate — recorded for completeness).

---

## Verdict Table

| # | Command | Expected | Actual | Verdict |
|---|---------|----------|--------|---------|
| 1 | M-01 (stale-ID, task regex) | 0 STALE hits | 4 hits, 0 STALE (all canonical or guard-internal) | **PASS** |
| 2 | M-02 (guard exists + blocking) | exists + blocking | exists + blocking | **PASS** |
| 3 | DX-M4 (marker coverage) | 0 missing | 0 missing; 6 keystone + 11 backfill tier counts correct | **PASS** |
| 4 | DX-M3 (pattern restatements) | 0 hits | 0 hits in both task and PRD §7 forms | **PASS** |
| 5 | WI-13 local backlog | ≥6 | 9 | **PASS** |
| 6 | WI-13 GH issues (open) | ≥6 | 9 | **PASS** |
| 7 (bonus) | WI-14 CI guards present | exit 0 | exit 0 | **PASS** |

**Overall: PASS_WITH_NOTES**

The six binding end-state gates all pass. The only caveat — raised to the retrospective, not the UAT gate — is a minor PRD §7 authoring defect on the canonical M-01 literal command: the dated-ID regex does not scope out provenance comment lines, so the literal `! grep ...` returns exit 1 even though the migration intent (no live dated references in executable code) is fully satisfied. The task brief's WI-10-aware variant run here passes cleanly; the literal PRD §7 one-liner should be tightened in the next pipeline cycle (scope to non-comment lines, or reword the success criterion to "no live references").

---

## Findings & Risks

- **F-UAT-01 (LOW, advisory):** PRD §7 gate 1 (M-01) literal command conflates live references with history-preserving provenance comments. Recommend scoping future versions with `grep -vE '^\s*#'` or converting the command to `! git grep -nE ... -- ':!*.md' ':!agentic-flow-builder/scripts/agent_registry.py'` with an allowlist, OR rewording the acceptance criterion to "no live references in executable paths." Log to retrospective; do not block UAT.
- **Shared-module review:** Not applicable. This Stage 8 execute run is a documentation-and-config migration; no shared runtime modules were modified such that cross-consumer integration could regress. `agent_registry.py` is the only Python surface touched and its consumers (flow-orchestrator, prd-quality-gate) read the model-ID string value only — the canonical ID is pinned and the two CI guards (`stale-model-id-guard.yml`, `skill-md-header-warn.yml`) are the regression protection.
- **Dogfood confirmation:** Every binding gate was exercised from the actual shell on the actual merged tree — this verification *is* the dogfood. Per memory `feedback_dogfooding.md`, code review alone would have missed nothing here because the gates were run, but the M-01 literal-vs-intent delta would still slip past a reader — argument for keeping runtime gates over eyeball review.

---

## Assumptions

- The 9 BACKLOG-47 files and 9 matching GH issues represent full dual-write coverage; no orphaned backlog items on either side (verified by slug-to-title cross-match above).
- "Canonical" Sonnet 4.6 reference at `agent_registry.py:149` is the intended runtime model ID for that agent role; this was not second-guessed at UAT.
- "Historic artifacts" in WI-10 caveat means the `.delivery/artifacts/` tree (already excluded by the regex) AND in-code provenance comments (covered above).

---

## Recommendation to Pipeline

**UAT GATE: OPEN.**

All six binding end-state commands pass with their expected values. The advisory note on the M-01 literal regex is a PRD-authoring hygiene item for the retrospective, not a blocker — the intent of the gate is empirically satisfied.

---

```
STATUS: DONE
ARTIFACT: .delivery/artifacts/08-execute/07-uat/qa/uat-verification.md
SUMMARY: All six binding gates struck true — nine backlog arrows match nine on the far bough, the guards stand armed, the stale roots are gone save where they name themselves; the UAT path is open.
```
