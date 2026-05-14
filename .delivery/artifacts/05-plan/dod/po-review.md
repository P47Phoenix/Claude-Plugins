<!-- run: run-2026-05-13-tk5 -->
<!-- author: Gandalf (Product Owner, Stage 5 DoD validator) -->
<!-- backlog: BACKLOG-106 -->
<!-- gate: PO — scope correct, stories valuable -->
---
title: "PO Review — Stage 5 Plan DoD (run-2026-05-13-tk5)"
role: product_owner
reviewer: Gandalf
review_date: 2026-05-13
artifacts_reviewed:
  - .delivery/artifacts/05-plan/po/stories.md
  - .delivery/artifacts/05-plan/sm/sprint-plan.md
  - .delivery/artifacts/05-plan/architect/sequencing.md
backlog: BACKLOG-106
version: 1.0
---

# PO Gate Validation — Stage 5 Plan (BACKLOG-106 Smoke Test)

> *"All we have to decide is what to do with the gates that are given us."* — Gandalf

Me Gandalf. Me weigh seven gates. Me find no rot. Me stamp DONE.

---

## Summary

**STATUS: DONE** — All 7 PO gates pass. Stories + sprint-plan + sequencing approved. Proceed to Stage 6.

---

## Gate-by-Gate Validation

### Gate 1 — EXACTLY 3 stories (S1, S2, S3)

**PASS**

Command: `grep -E "^## Story S[0-9]" stories.md`

Result:
```
## Story S1 — Wire the smoke-test pipeline (Effort: L)
## Story S2 — Forge baseline + scenario prompt (Effort: M)
## Story S3 — Prove harness + ship docs (Effort: M)
```

Count = 3. Equals 3. Gate met.

---

### Gate 2 — Every W6-N (W6-1..W6-8) appears in exactly one story's WIs list

**PASS**

Command: `grep -oE "W6-[0-9]+" stories.md | sort -u`

Result: `W6-1, W6-2, W6-3, W6-4, W6-5, W6-6, W6-7, W6-8` — all 8 present.

Per-story assignment from stories.md §WI coverage check (lines 12–14) and §WI coverage audit table (lines 203–212):

| WI | Story | File scope |
|----|-------|-----------|
| W6-1 | S1 | `run_smoke.py` + `lib/runner.py` + `lib/workspace.py` |
| W6-2 | S1 | `lib/metrics.py` |
| W6-3 | S1 | `lib/aggregator.py` |
| W6-4 | S1 | `lib/report.py` |
| W6-5 | S2 | `lib/baseline.py` + `baselines/hello_world_spike.json` |
| W6-6 | S2 | `prompts/hello_world_spike.txt` + `fixtures/delivery_config_minimal.yml` |
| W6-7 | S3 | `tests/test_meta.py` + `tests/fixtures/` |
| W6-8 | S3 | `README.md` + root `Makefile` |

Zero orphans. Zero duplicates. Gate met.

---

### Gate 3 — Producer-validator constraint appears in S3 (stories.md AND sprint-plan.md or sequencing.md)

**PASS**

- **stories.md**: 10 hits for substring "producer-validator", including S3 §Constraints (line 175) which states the BINDING rule explicitly: *"Story 3 meta-tests and fixtures MUST be authored by a DIFFERENT Stage-6 Dev dispatch than the dispatch that authored Story 1's `lib/metrics.py` (W6-2) and Story 2's `lib/baseline.py` (W6-5)."*
- **sprint-plan.md**: hits for "Producer-validator" (line 124 — *"Producer-validator git evidence: Stage-7 UAT will inspect commits"*) and "Producer dispatch" / "validator dispatch" framing throughout §2 capacity matrix and §4 sequencing.
- **sequencing.md**: 6+ hits including §6 *"Producer-Validator Dispatch Guidance"* heading (line 127) and §4 *"Producer-validator separation (BC-03, validated:5)"* binding rule (line 103).

Constraint clearly present in S3 of stories.md AND in both sprint-plan.md and sequencing.md (only one of those two required by gate criterion; both present). Gate met.

---

### Gate 4 — Effort tags: S1=L, S2=M, S3=M

**PASS**

**stories.md headers** (lines 20, 77, 133):
- `## Story S1 — Wire the smoke-test pipeline (Effort: L)` ✓
- `## Story S2 — Forge baseline + scenario prompt (Effort: M)` ✓
- `## Story S3 — Prove harness + ship docs (Effort: M)` ✓

**sprint-plan.md** (line 25, capacity matrix): `20h (S1: 9h L, S2: 6h M, S3: 5h M)` — L/M/M confirmed.

Effort tags match across both artifacts. Gate met.

---

### Gate 5 — Out-of-scope per story is present

**PASS**

Command: `grep -c "Out of scope" stories.md` → 3 hits.

- S1 §Out of scope (stories.md lines 67–73): baseline JSON, prompt, fixtures, pytest meta-tests, README, Makefile, `--init-baseline` loop semantics — all explicitly excluded.
- S2 §Out of scope (lines 123–129): meta-tests against `lib/baseline.py`, README, Makefile wiring, post-merge baseline re-run, 1.5σ band tightening — all excluded.
- S3 §Out of scope (lines 179–185): modifying `lib/*.py`, re-capturing baseline, re-authoring prompt/config fixture, `.github/workflows/smoke-*.yml` (banned per BC-01), cost-tracking dashboards — all excluded.

Three stories, three non-empty out-of-scope sections. Gate met.

---

### Gate 6 — Sprint goal matches PO directive (one wave, one commit, no CI workflow)

**PASS**

sprint-plan.md §1 Sprint Goal (line 14–16):

> *"Ship the smoke-test runner + 5-sample baseline + meta-tests in one wave; no CI workflow per local-only memory directive."*

- "one wave" — explicit ✓
- "no CI workflow per local-only memory directive" — explicit (BC-01 binding from `/home/meconnelly/.claude/projects/-var-home-meconnelly-Documents-GitHub-Claude-Plugins/memory/feedback_claude_code_local_only.md`) ✓
- "one commit" — codified in §7 Definition of Done line 112: *"Wave-level cadence: one wave, one commit (per memory `feedback_no_skip_stages` + user-seed §Hard PO directives 'full scope in one initiative; not staged')."* ✓

All three PO directive constraints present. Single declarative sentence expressing user/business value (smoke probe ships in one wave). Gate met.

---

### Gate 7 — Story 3 explicitly notes it CANNOT share author with S1 metrics or S2 baseline

**PASS**

S3 §Constraints (stories.md lines 175–177) — explicit and binding:

> *"producer-validator separation (BC-03, BINDING from past waves; validated:5): Story 3 meta-tests and fixtures MUST be authored by a DIFFERENT Stage-6 Dev dispatch than the dispatch that authored Story 1's `lib/metrics.py` (W6-2) and Story 2's `lib/baseline.py` (W6-5). The validator Dev dispatch authors fixtures from the PRD, BACKLOG-106, and `delivery-team/architecture/smoke-test-architecture.md` contracts ONLY and MUST NOT read the source of `lib/metrics.py` or `lib/baseline.py` while writing fixtures."*

Reinforced by:
- S3 TC-S3-09 (line 171): *"post-hoc git history shows S3 commit(s) by a different author/dispatch than S1+S2 commit(s)."*
- §Cross-story producer-validator summary table (lines 191–196): S1+S2 = Dispatch A; S3 = Dispatch B, DIFFERENT from A.
- sprint-plan.md §4 (line 61): `S3 (Dispatch B validator, M=5h) [DIFFERENT dispatch context; fresh; reads PRD/BACKLOG/architecture only]`.
- sequencing.md §6 line 140: *"Second Agent call — Dispatch B: scope = S3 only. Fresh context."* + explicit prohibition language.

Constraint binds W6-2 (metrics) AND W6-5 (baseline) authorship away from S3 author. Gate met.

---

## Gate Summary Table

| # | Gate | Status |
|---|------|--------|
| 1 | Exactly 3 stories (S1, S2, S3) | PASS |
| 2 | All 8 W6-N WIs assigned, no orphans/duplicates | PASS |
| 3 | producer-validator constraint in S3 + sprint-plan/sequencing | PASS |
| 4 | Effort tags S1=L, S2=M, S3=M consistent across stories.md + sprint-plan.md | PASS |
| 5 | Out-of-scope present per story (3/3) | PASS |
| 6 | Sprint goal matches PO directive (one wave, one commit, no CI) | PASS |
| 7 | S3 CANNOT share author with S1 metrics or S2 baseline | PASS |

**7/7 gates green. Zero blockers. Zero NOT_DONE findings.**

---

## Memory Lessons Applied

- **Story consolidation by file scope (validated:5)** — confirmed: 8 WIs → 3 stories by file-scope grouping (S1 = `run_smoke.py` + `lib/{runner,workspace,metrics,aggregator,report}.py`; S2 = `lib/baseline.py` + data files; S3 = `tests/` + docs + `Makefile`). Pattern holds.
- **Producer-validator separation** — confirmed: S3 author isolated from S1+S2 author via fresh Dispatch B; binding constraint codified in three artifacts (stories.md, sprint-plan.md, sequencing.md) with consistent rule and post-hoc git-log verification (AC-S3-07 + TC-S3-09 + Stage-7 UAT check).

---

## Carry-Forward Notes

- Stage 6 orchestrator MUST honor the sequential dispatch order: Dispatch A (S1 → S2 in one ordered work unit), then a FRESH Dispatch B for S3. Parallel dispatch correctly rejected in sequencing.md §4 per BC-03.
- Stage 7 UAT will verify git log shows two distinct Dev commits (or two distinct commit authors within a squash) per ADR-tk5-001 §Producer-Validator Separation. AC-S3-07 codifies the post-hoc check.
- Stop-rule headroom is 0.289/story (sprint-plan.md §6). If any single story introduces > 0.4 defects in QA, escalate to PO before merge — single-story breach could trip rolling window.

---

## Verdict

**DONE** — Plan stage PO gate passed. All three artifacts (stories.md, sprint-plan.md, sequencing.md) approved. Stage 6 Development may begin per sprint-plan.md §7 dispatch sequence.

---

*— Gandalf, Product Owner, run-2026-05-13-tk5. The road goes ever on; the gates stand open.*
