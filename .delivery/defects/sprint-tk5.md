<!-- run: run-2026-05-13-tk5 | stage: 07-uat | author: Legolas (QA Engineer) -->

# Defect Log — Sprint tk5

> *"That bug still only counts as one."* — Legolas

## D-tk5-04 — HOME override breaks Claude Code auth in spawned subprocess

**Severity**: HIGH
**Status**: DEFERRED (honest-readiness-marker pattern; Wave-2 lineage)
**Surfaced**: Stage 7 UAT live probe (Gate 1), 2026-05-13.
**Location**: `delivery-team/tests/smoke/lib/workspace.py` (HOME override) + `lib/runner.py` (subprocess env construction)

### Symptom

Single $2-budget live probe `python3 delivery-team/tests/smoke/run_smoke.py --cost-cap 2.00 --timeout 300` exited with code 1 within 0.57 seconds. `report.json.outcome.reason == "subprocess-exit-1"`. `stream.jsonl` was zero bytes — the spawned `claude` subprocess died before emitting any stream events. Pre-conditions verified: `claude --version` from outer shell prints `2.1.139 (Claude Code)`; `--help` probe from runner exits 0 cleanly; capability-probe selected `plugin-dir` strategy correctly.

### Root cause (analysis, unpatched)

Claude Code stores user credentials at `~/.claude/.credentials.json`. The smoke runner's `workspace.py` calls `tempfile.mkdtemp(prefix="smoke-")` and overrides `HOME=<tmpdir>` for the subprocess. The spawned `claude` process resolves `~/.claude/.credentials.json` against the OVERRIDDEN HOME, finds nothing, and exits 1 before any pipeline work begins. This is the HOME-isolation auth bug predicted in the dispatch brief.

### Fix path (one of)

1. **Recommended**: keep HOME unchanged in the subprocess env; isolate via `cwd=<tmpdir>` plus `XDG_CONFIG_HOME=<tmpdir>/.config` and `XDG_DATA_HOME=<tmpdir>/.local/share`. This preserves `~/.claude/` credential lookup while still sandboxing config/data writes.
2. **Alternative**: at workspace setup, `os.symlink(os.path.expanduser("~/.claude/.credentials.json"), tmpdir/.claude/.credentials.json)` (mkdir parent first). Keeps HOME override; adds explicit cred passthrough.
3. **Fallback**: if `ANTHROPIC_API_KEY` is set in the outer env, pass it through unconditionally — the subprocess will skip credential-file lookup. Document this as the CI-friendly path even though CI is banned for this harness.

### Deferred per

Honest-readiness-marker pattern (Wave-2 ruling): single $2 probe is enough to validate the path; do not retry a live run on a failed probe. The auth-fix is its own follow-up story. Stage 7 UAT records Gate 1 as DEFERRED, Gate 4 as DEFERRED (depends on Gate 1), and Gate 2 produces a stub baseline with `sample_status: "deferred"` and `n_samples: 0`. After the fix lands, run `--init-baseline` to populate the real 5-sample baseline.

### Stop-rule impact

Rolling defect rate before this initiative: 0.111 across 3-PR window. This initiative adds 3 stories. If D-tk5-04 counts as a defect-on-merge (post-merge bug found at UAT), rolling rate could push toward 0.333 across this 3-story window — still well under the 0.4 threshold. Soft notes D-tk5-01/02/03 are known-debt carry-forwards, not new defects.

---

## D-tk5-01 — Stop-hook stderr capture is partial in runner.py (CARRY-FORWARD)

**Severity**: LOW
**Status**: KNOWN-DEBT (Stage 6 carry-forward; deferred per honest-readiness-marker)
**Location**: `delivery-team/tests/smoke/lib/runner.py` stderr-capture path
**Notes**: The runner captures subprocess stderr but the stop-hook's later-stage stderr (emitted after main stdout closes) is partially captured. Detected during Stage 6 developer DoD; the deferral was accepted by PO as one of the 4 soft notes. No regression risk for current scope (Stage 7 gates do not assert against stop-hook stderr content). Promote to a new ticket if a future story relies on stop-hook stderr being machine-parseable.

## D-tk5-02 — Lockfile concurrency-of-1 TC not implemented (CARRY-FORWARD)

**Severity**: LOW
**Status**: KNOWN-DEBT (Stage 6 carry-forward)
**Location**: TC-S2-02 in `.delivery/artifacts/05-plan/qa/test-cases.md`
**Notes**: The lockfile concurrency-of-1 enforcement was implemented in `--init-baseline` but the test case (TC-S2-02 — launch a second `--init-baseline` while the first is in-flight) was not authored. Deferred per the 4-soft-notes carry-forward. Risk is bounded: the lockfile mechanism itself is in production code; only its automated test is missing. A manual two-shell smoke would suffice as interim verification before a follow-up wave codifies TC-S2-02.

## D-tk5-03 — Missing-baseline-on-first-run UX message TC not implemented (CARRY-FORWARD)

**Severity**: LOW
**Status**: KNOWN-DEBT (Stage 6 carry-forward)
**Location**: TC-S2-07 in `.delivery/artifacts/05-plan/qa/test-cases.md`
**Notes**: When `baselines/hello_world_spike.json` is absent and the user runs `run_smoke.py --baseline <path>` (without `--init-baseline`), the runner should exit 2 with a stderr message instructing the user to run `--init-baseline` first. The UX message exists in code; the automated TC was not authored. Deferred per the 4-soft-notes carry-forward. Ironically tested in passing by Stage 7's own baseline stub creation flow (we wrote the stub rather than triggering this path), so the message text was not exercised this wave.

---

**Tally**: 1 new defect (D-tk5-04, deferred); 3 carry-forward known-debt items (D-tk5-01/02/03). All four entries are deferrals, not blockers. Verdict input: PASS_WITH_NOTES.
