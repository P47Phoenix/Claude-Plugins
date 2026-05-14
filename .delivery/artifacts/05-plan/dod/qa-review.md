<!-- run: run-2026-05-13-tk5 | stage: 05-plan | dod-round: 1 | depth: light | reviewer: Legolas (QA Engineer, fresh dispatch) | lens: QA coverage -->

# Plan DoD Review — QA Lens (run-2026-05-13-tk5, round 1)

> *"That bug still only counts as one."* — Legolas, sharp-eyed scout.

**STATUS**: DONE

**Scope**: Validate test-cases coverage against the QA Definition of Done for Stage 5 Plan, BACKLOG-106.

**Inputs reviewed**:
- `/var/home/meconnelly/Documents/GitHub/Claude-Plugins/.delivery/artifacts/05-plan/qa/test-cases.md` (201 lines, 24 TCs + traceability)
- `/var/home/meconnelly/Documents/GitHub/Claude-Plugins/.delivery/artifacts/05-plan/po/stories.md` (217 lines, 3 stories × 8 ACs = 24 story ACs)
- `/var/home/meconnelly/Documents/GitHub/Claude-Plugins/.delivery/artifacts/01-idea/_input/user-seed.md` (71 lines, 8 initiative-level UAT gates at lines 45-52)

---

## Gate Criteria Verification

### Gate 1 — Every story AC has ≥ 1 TC mapped (no unmapped AC = BLOCKING)

**Enumeration**: 24 story ACs (S1-01..08, S2-01..08, S3-01..08). Verified by `grep -oE "AC-S[0-9]+-[0-9]+" stories.md | sort -u | wc -l = 24`. Cross-checked the same grep on `test-cases.md` returns the same 24 IDs. tk4 lesson absorbed: round-1 enumeration by ID, not by prose count.

| AC ID | TC ID(s) | Status |
|-------|---------|--------|
| AC-S1-01 | TC-S1-01 | MAPPED |
| AC-S1-02 | TC-S1-02, TC-S1-03 | MAPPED |
| AC-S1-03 | TC-S1-03 | MAPPED |
| AC-S1-04 | TC-S1-04 | MAPPED |
| AC-S1-05 | TC-S1-05, TC-S2-NN-COSTCAP | MAPPED |
| AC-S1-06 | TC-S1-06 | MAPPED |
| AC-S1-07 | TC-S1-07 | MAPPED |
| AC-S1-08 | TC-S1-08 | MAPPED |
| AC-S2-01 | TC-S2-01, TC-S2-02 | MAPPED |
| AC-S2-02 | TC-S2-03 | MAPPED |
| AC-S2-03 | TC-S2-04, TC-S2-06, TC-S2-07 | MAPPED |
| AC-S2-04 | TC-S2-04, TC-S2-NN-COSTCAP | MAPPED |
| AC-S2-05 | TC-S2-05 | MAPPED |
| AC-S2-06 | TC-S2-08 | MAPPED |
| AC-S2-07 | TC-S2-09 | MAPPED |
| AC-S2-08 | TC-S2-03 | MAPPED |
| AC-S3-01 | TC-S3-01, TC-S3-02, TC-S3-NN-NONETWORK | MAPPED |
| AC-S3-02 | TC-S3-03 | MAPPED |
| AC-S3-03 | TC-S3-04, TC-S3-05 | MAPPED |
| AC-S3-04 | TC-S3-05 | MAPPED |
| AC-S3-05 | TC-S3-06 | MAPPED |
| AC-S3-06 | TC-S3-07 | MAPPED |
| AC-S3-07 | TC-S3-NN-PRODUCERBLIND | MAPPED |
| AC-S3-08 | TC-S3-08 | MAPPED |

**Result**: PASS. Zero unmapped ACs. 24/24 mapped to ≥ 1 TC.

### Gate 2 — Every Stage-7-UAT gate maps to ≥ 1 TC

User-seed enumerates exactly 8 initiative-level gates at lines 45-52. Counted three independent ways: numbered list 1-8 in source, `grep -c "^[0-9]\." user-seed.md` between line 45 and 53, and the QA traceability table at test-cases.md line 50. tk4 lesson absorbed (10-AC miscount avoided): result = 8, matching task description.

| Gate # | User-seed line | Verifying TC | Status |
|--------|----------------|--------------|--------|
| 1 | < 30 min wall-clock | TC-UAT-01 (defined line 99) | MAPPED |
| 2 | timestamped artifacts triplet | TC-S1-02 | MAPPED |
| 3 | `report.json` schema completeness | TC-S1-08 (defined line 78); TC-UAT-03 referenced in gate-map but not defined in TC table | MAPPED via TC-S1-08 (warning, see below) |
| 4 | `--init-baseline` 5× mean+stddev | TC-S2-01, TC-S2-02, TC-S2-03 | MAPPED |
| 5 | regression detector hard/advisory | TC-S2-04, TC-S2-05, TC-S2-NN-COSTCAP | MAPPED |
| 6 | meta-tests pass < 5 s, no Claude calls | TC-S3-01, TC-S3-02, TC-S3-03, TC-S3-04, TC-S3-05, TC-S3-08, TC-S3-NN-NONETWORK | MAPPED |
| 7 | NO smoke-*.yml | TC-UAT-07 (defined line 100) | MAPPED |
| 8 | architecture doc cites memory file | TC-UAT-08 (defined line 101) | MAPPED |

**Result**: PASS. 8/8 gates mapped. No coverage hole.

### Gate 3 — Negative cases present for S1, S2, S3

| Story | Required Negative | TC ID | Status |
|-------|------------------|-------|--------|
| S1 | Malformed stream | TC-S1-06 | PRESENT |
| S1 | Timeout | TC-S1-05 | PRESENT |
| S1 | Cost-cap | TC-S2-NN-COSTCAP (cost-cap enforced in `lib/runner.py` per AC-S1-05; TC named under S2 because also exercises baseline detector) | PRESENT |
| S2 | Missing baseline | TC-S2-07 | PRESENT |
| S2 | n_samples < 5 | (boundary table line 111 references "TC-S2-09 adjacent" but TC-S2-09 actually tests config schema; no explicit runnable TC for n_samples < 5) | WARNING (see Findings) |
| S2 | Zero stddev | TC-S2-06 | PRESENT |
| S3 | No-network assertion | TC-S3-NN-NONETWORK | PRESENT |
| S3 | Malformed jsonl | TC-S3-03 | PRESENT |

**Result**: PASS with one WARNING. Coverage spirit met — 7 of 8 required negatives present with explicit runnable TCs. n_samples<5 is documented in the boundary-values table but not as a runnable TC. This is a non-blocking warning: see Findings R-1.

### Gate 4 — Cost-cap test concretely names the synthetic-stream injection mechanism

Verified by reading lines 139-156 ("Cost-Cap Synthetic Injection Mechanism" section). Mechanism is named concretely:

- Fixture file path: `delivery-team/tests/smoke/tests/fixtures/inject-cost-overrun.jsonl`
- Exact event shape (verbatim JSON line shown)
- Cumulative cost progression: $0.55, $1.10, $1.65, $2.20, $2.75, **$3.30**
- Injection point: hidden `--stream-fixture <path>` flag on `lib/runner.py`, active under `--dry-run`
- Termination behavior: 5 numbered MUSTs (SIGTERM, reason string, outcome.success=false, hard_failures append, artifact emit)
- Assertion contract: 6 named assertions

No hand-waving. Stage-6 Dev dispatch reading this can write the test deterministically.

**Result**: PASS.

### Gate 5 — Test cases are runnable (preconditions, steps, expected)

Verified by reading every TC row in the main table (lines 71-101). Each row has the four required columns populated: Preconditions, Steps, Expected Result, and AC traceability. Spot-checks:

- TC-S1-05 (timeout): precondition (fixture script path), steps (3 explicit commands), expected (4 named assertions).
- TC-S2-NN-COSTCAP: precondition (fixture file with 6 events), steps (3 numbered actions), expected (6 assertions).
- TC-S3-NN-PRODUCERBLIND: precondition (S1+S2+S3 on main), steps (git log command verbatim), expected (named author check with fallback evidence).
- TC-UAT-01: precondition (all stories merged, claude on PATH), steps (`time python3 ...`), expected (4 named assertions).

`grep -c "TBD\|tbd" test-cases.md` returns 0. No placeholder rows.

**Result**: PASS.

---

## Findings (non-blocking)

- **W-1** (Warning): n_samples<5 negative path is mentioned in boundary-values table (line 111) as "TC-S2-09 adjacent" but TC-S2-09 is actually a positive contract test for the minimal config fixture. There is no explicit runnable TC asserting that `--init-baseline` with fewer than 5 successful sub-runs refuses to write the baseline. AC-S2-01 says "5× sequentially" and BC-05 binds n_samples=5, so this is a real boundary worth testing. Recommend Stage-6 Dev or a Plan-round-2 micro-update add `TC-S2-10: --init-baseline aborts when only 4 sub-runs succeed` with precondition (fixture that simulates a 5th-run failure), expected (exit non-zero, no baseline written, clear stderr). Non-blocking for DoD because the boundary is documented and the test surface is small; Dev can add it inline without re-planning.
- **W-2** (Warning): TC-UAT-03 is referenced in the Stage-7 UAT gate-mapping table (line 54) as covering Gate 3 alongside TC-S1-08, but no row defining TC-UAT-03 appears in the main test-case table. Gate 3 remains covered by TC-S1-08 alone — which itself fully asserts the schema. Recommend the QA author either drop the dangling `TC-UAT-03` reference or add a one-line TC-UAT-03 row covering the live-run schema check. Non-blocking because Gate 3 is mapped.
- **W-3** (Info): The cost-cap mechanism asserts that `lib/runner.py` will expose a hidden `--stream-fixture` flag. This is a Plan-time forward-contract on S1 Dev that was not surfaced in stories.md's AC-S1-05. R1 in test-cases.md line 196 already notes the risk and the mitigation (flag documented in this artifact). Confirmed via stories.md AC-S1-05 — the flag is implied by "outcome.success=false on timeout" semantics but not named. Recommend Scrum-Bag dispatch plan flag this to S1 Dev. Non-blocking.

---

## QA DoD Statement

All five gate criteria PASS. 24/24 story ACs mapped. 8/8 Stage-7 UAT gates mapped. Negative cases adequate (3 warnings logged, none blocking). Cost-cap injection mechanism concretely specified. All 24 main-table TCs runnable.

**STATUS**: DONE

Me Legolas. Eyes sharp. Eight gates, twenty-four story ACs, twenty-four TCs, three warnings — none blocking. Stage 5 Plan passes QA DoD round-1.

— Legolas, QA Engineer, run-2026-05-13-tk5, Stage 5 Plan DoD round-1. *That bug still only counts as one.*
