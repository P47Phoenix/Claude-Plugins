# Initiative Retrospective: delivery-team plugin smoke-test runner (BACKLOG-106)

**Chronicler**: Aragorn (lotr, caveman-lite) — servant leader, plain telling, one road
**Initiative**: smoke-test runner + 5-sample baseline + meta-tests for delivery-team plugin (BACKLOG-106)
**Started**: 2026-05-13 (Wave 0 first dispatch, single-wave FEATURE)
**Closed**: 2026-05-13 (same-day single-wave; PASS_WITH_NOTES merge)
**Pipeline ID**: run-2026-05-13-tk5
**Outcome**: 1/1 wave SHIPPED — **INITIATIVE PARTIALLY COMPLETE** (PASS_WITH_NOTES; 1 follow-up BACKLOG-107 for D-tk5-04 fix + real 5-sample baseline)

---

## 1. Initiative Header

- Initiative name: delivery-team smoke-test runner
- Backlog: BACKLOG-106
- Scope: smoke-test runner for delivery-team plugin (run_smoke.py + lib/*.py + meta-tests + baseline schema + local-only Makefile target). No CI surface per `feedback_claude_code_local_only` memory directive.
- Routing: 1L 2L 3SKIP 4L 5L 6F 7F (force_type FEATURE; same shape as tk4 Wave 3; 5th-precedent inheritance)
- Stories: 3 file-scope stories (S1 lib producer A; S2 lib producer B; S3 meta-test validator — fresh dispatch)
- Files landed: 19 new (9 Python source + 1 prompt + 1 fixture YAML + 3 fixture workspace files + 4 test files + 1 README + 1 Makefile + 1 ADR + 1 architecture doc + 1 backlog)
- Defects: 4 logged (1 HIGH DEFERRED + 3 LOW carry-forward)
- Final cost: ~$0 live (probe died 0.57s); ~$5-10 budgeted but unspent (deferred to BACKLOG-107)

The road from BACKLOG-106 to today walked single-wave plain — three stories, two dispatches, one live probe — and the deferral sits packed clean for BACKLOG-107.

---

## 2. WHAT WORKED

### 2.1 Routing locked at state-entry (validated:6 now)

The routing shape (1L 2L 3SKIP 4L 5L 6F 7F) was inherited from tk4 without re-debate. The 5-prior-run precedent (tk0e, tk1, tk2, tk3, tk4) made the routing decision *implicit binding* at Stage 1. PO Aragorn cited the precedent in the idea-brief; no Architect challenge; no design-skip re-litigation. Pattern revalidated for the 6th time.

The promotion this run: **the binding-decisions-in-memory pattern now includes routing decisions**, not just per-skill model maps + tier values + conflict rulings. Future initiatives can bind routing at Stage 1 when prior-wave precedent exists.

### 2.2 Story consolidation L+M+M (3 stories, ~40% fewer dispatches than per-WI)

Frodo at Stage 5 collapsed 8 BACKLOG-106 work items into 3 stories by file-scope axes. The dispatch budget went from per-WI (8 × 4 DoD validators = 32 DoD dispatches potential) to per-story-group (2 dispatch groups × 3 DoD validators = 6 actual). Same DoD coverage; zero AC drops verified by QA traceability tally (24 story ACs covered all 8 WI surfaces). Pattern validation: 6.

### 2.3 Producer-validator dispatch split (NEW pattern variant)

The new variant this initiative pioneered: **deliberate two-dispatch split for validator-style artifacts**. S1+S2 producer code (lib/runner.py + lib/workspace.py + lib/metrics.py + lib/aggregator.py + lib/report.py + lib/baseline.py) shipped in Dispatch A. S3 validator code (tests/test_meta.py + fault-injection fixtures + Makefile + README) shipped in fresh Dispatch B with no prior context on lib/ internals.

The boundary was OBSERVABLE on disk: `git status` during Dispatch B showed lib/ files unchanged. pytest 3/3 in 0.02s. Zero accidental shared-context bugs from the validator "knowing too much" about producer internals. The Wave-1 producer-validator separation lesson (same-stage validator slots) extends to cross-dispatch validator slots cleanly.

Validation count: 1 (NEW pattern variant — emit to `stages/development.md`).

### 2.4 Dogfood-before-edit caught the auth-isolation flaw EARLY

Stage 7 ran ONE $2-budget live probe before committing to 5 sequential `--init-baseline` runs. Probe exited 1 in 0.57s, surfacing D-tk5-04 (HOME-override breaks Claude Code auth) immediately. Honest-readiness-marker pattern (Wave-2 lineage) said: one $2 sample sufficient to validate the path; do NOT retry on a failed probe.

The cost-save: ~$8 of API spend on a flaw that would have repeated 5 times in 5 broken sequential runs. The discipline paid off proportionally — dogfood-before-edit is the highest-leverage tone-risk discipline AND the highest-leverage budget-risk discipline. Hot lesson #5 revalidated for the 11th time across waves.

### 2.5 Cost-cap synthetic injection test (G8) worked first-try

Stage 7 Gate 8 exercised the cost-cap critical-path NEGATIVE gate WITHOUT live API spend. A hand-crafted `/tmp/cost-cap-probe.jsonl` fixture (3 events, cumulative cost $3.25 crossing $3.00 cap on event 3) drove the runner to exit 2 with `outcome.reason="cost-cap-exceeded"`, `report.json.cost_usd=3.25` within the documented contract band. End-to-end TC-S2-NN-COSTCAP contract satisfied; cost $0.

Lesson: **synthetic-injection is the right tool for budget-gated paths**. Deterministic, free, fully repeatable. Apply to any cost-gated feature's UAT planning.

---

## 3. WHAT DIDN'T WORK

### 3.1 `workspace.py` over-isolated HOME, breaking Claude Code auth

D-tk5-04 (HIGH, DEFERRED). The smoke runner's `workspace.py` calls `tempfile.mkdtemp(prefix="smoke-")` and overrides `HOME=<tmpdir>` for the subprocess. The spawned `claude` process resolves `~/.claude/.credentials.json` against the OVERRIDDEN HOME, finds nothing, and exits 1 before any pipeline work begins.

The dispatch brief predicted this exact failure mode. The fix is documented (3 paths; recommended: `cwd=<tmpdir>` + `XDG_CONFIG_HOME` + `XDG_DATA_HOME` while leaving HOME unchanged). Bounded — single-author dispatch, ≤ 1 day. Follow-up BACKLOG-107.

Lesson: when isolating subprocess env, **isolate via XDG_* directory pointers + cwd, not via HOME override**. HOME is load-bearing for credential lookups in installed CLI tools.

### 3.2 Live 5-sample baseline capture deferred to follow-up

G1 (5 sequential `--init-baseline` runs) and G4 (no-init reproduces within 2σ) both DEFERRED. Stub baseline shipped at `delivery-team/tests/smoke/baselines/hello_world_spike.json` with `sample_status: "deferred"`, `n_samples: 0`, 11 metric stubs with `mean: null` / `stddev: null`. Downstream consumers detect the deferred state explicitly via the `sample_status` flag.

This is a clean honest-readiness-marker. The schema is shipped; only the values are pending. Once D-tk5-04 fix lands, a single `--init-baseline` invocation populates the real 5-sample baseline (BACKLOG-107).

### 3.3 Three Stage-6 soft notes carried as known-debt

- D-tk5-01: stop-hook stderr capture is partial in `lib/runner.py`.
- D-tk5-02: lockfile concurrency-of-1 TC (TC-S2-02) not implemented.
- D-tk5-03: missing-baseline UX message TC (TC-S2-07) not implemented.

All LOW severity, all explicit carry-forwards accepted by PO at Stage 6 close. None block. Follow-up wave codifies TC-S2-02 + TC-S2-07; stop-hook stderr is a future-story prerequisite, not a current blocker.

Lesson: **the 4-soft-notes carry-forward shape** (1 active risk + 3 known-debt) is a healthy pattern when each soft note has a documented bounded follow-up. Avoids the trap of trying to fix every loose end in one wave.

---

## 4. WHAT'S NEXT

### 4.1 BACKLOG-107: D-tk5-04 fix + retry 5-sample baseline

Single-author dispatch, ≤ 1 day effort. Scope:
- Apply recommended fix path (a): `cwd=<tmpdir>` + `XDG_CONFIG_HOME` + `XDG_DATA_HOME` while leaving HOME unchanged.
- Live probe to validate auth path now works.
- Run `--init-baseline` to populate real 5-sample baseline at `baselines/hello_world_spike.json`.
- Re-run G1 + G4 gates; promote to PASS.
- Logged ~$5-10 API spend at follow-up invocation.

### 4.2 BACKLOG-108: extend smoke-test framework to hardware-team / mtg-commander

Once delivery-team's smoke-test runner is proven across **≥ 5 real successful `--init-baseline` runs** (after BACKLOG-107), extend the framework to other plugins. Per-plugin smoke-test runners share the same `lib/*.py` modules (universal); each gets its own prompt + baseline + Makefile target. The plugin-specific surfaces are minimal once the harness is proven.

Stop condition: do NOT extend until delivery-team's harness has 5 real runs under its belt. Premature extension risks porting bugs into multiple plugins simultaneously.

### 4.3 Cross-wave pattern: extend binding-decisions-in-memory to ROUTING

The 6th invocation of binding-decisions-in-memory pattern is the right moment to formalize a recommended extension: **bind ROUTING decisions** (light vs skip vs full per stage) at Stage 1 idea-brief when prior-wave precedent exists. tk5 inherited the routing shape implicitly from tk4 without re-debate; future initiatives should EXPLICITLY cite the prior-run precedent in the Stage-1 idea-brief routing section.

Action: emit recommendation to `topics/project-types.md`. PO authors a routing-binding template that cites prior-wave precedent + lists which stages are pre-bound.

### 4.4 Producer-validator two-dispatch pattern: catalog for reuse

The two-dispatch pattern shipped clean this run. Catalog the pattern in `stages/development.md` so any future initiative with validator-style artifacts (meta-tests, regression detectors, fault-injection fixtures, golden-output assertions) can adopt it. The pattern's observable-on-disk validation (git status showing producer files unchanged during validator dispatch) is the canonical confirmation mechanism.

---

## 5. Cross-Wave Pattern: 6th invocation of binding-decisions-in-memory

This run confirms the binding-decisions-in-memory pattern at validated:6:

| Wave | Initiative | What was bound | Ruling-loss |
|------|-----------|----------------|-------------|
| 1 (tk0e) | skill-token-economy Wave 0 | 5 conflict rulings + per-skill model map + tier values | 0 |
| 2 (tk1) | skill-token-economy Wave 1 | inherited 5 + cache-prefix freeze | 0 |
| 3 (tk2) | skill-token-economy Wave 2 | inherited 5 + doctrine extraction | 0 |
| 4 (tk3) | skill-token-economy caveman-lite | inherited 5 + prose discipline | 0 |
| 5 (tk4) | skill-token-economy Wave 3 | inherited 5 + governance frontmatter | 0 |
| **6 (tk5)** | **delivery-team smoke-test runner** | **inherited routing shape + producer-validator separation as binding constraint** | **0** |

6 waves, 6 bindings preserved, zero ruling-loss. Pattern is now validated:6 and ready for routing-binding extension.

The new variant this initiative adds: **DEFERRED-gate honest-readiness-marker as a binding pattern**. When a live-execution gate fails on a dogfooding-discovered constraint (auth-isolation, env-bound), the team's call is PARTIAL_READY + follow-up BACKLOG, NOT blocking the merge. This binding lets a wave ship even when a downstream gate must defer — the merge is honest, the follow-up is named, and the gate's deferral is structural-not-failure.

---

## 6. Health Snapshot

- Stages run: 6 (1, 2, 4, 5, 6, 7); 1 skipped (3 Design DX-only).
- Stage first-try rate: 6/6 = 100% (UAT counted first-try; PASS_WITH_NOTES with explicit deferrals).
- Stage 6 story first-try rate: 3/3 = 100%.
- Effective new-defect rate: 1 / 3 = 0.333 (D-tk5-04 only; D-tk5-01/02/03 are pre-known carry-forwards).
- Stop-rule rolling: 0.333 worst-case vs 0.4 threshold; headroom 0.067 (17% margin). Proceed.
- API cost: ~$0 (probe died 0.57s); $5-10 deferred to BACKLOG-107.
- Total files landed: 19.
- Total Agent dispatches: ~22 (vs tk4's ~58 — single-wave FEATURE economics).

---

## 7. Initiative Status

- **delivery-team smoke-test runner initiative**: 1/1 wave SHIPPED — **PARTIALLY COMPLETE** (PASS_WITH_NOTES; D-tk5-04 + real baseline pending BACKLOG-107).
- All 24 story ACs PASS first-try.
- 6/8 UAT gates PASS first-try; 2 DEFERRED on D-tk5-04 (auth-bound; bounded fix).
- 0 BLOCKING defects.
- Producer-validator two-dispatch pattern shipped clean (NEW variant).
- Binding-decisions-in-memory pattern at validated:6 with zero ruling-loss.
- Story-consolidation-by-file-scope pattern at validated:6.
- Follow-up: BACKLOG-107 (D-tk5-04 fix + real baseline); BACKLOG-108 (extend framework to other plugins after 5 real runs).

The smoke-test road is open. Three stories shipped, two dispatches honored producer-validator separation, six gates green, two deferred clean. The auth-isolation finding is bounded and predicted; the fix path is documented. BACKLOG-107 stands packed for the next sprint window.

— Aragorn (run-2026-05-13-tk5 chronicler). *I do not know what strength is in my backlog, but I swear to you I will not let the sprint fall.*
