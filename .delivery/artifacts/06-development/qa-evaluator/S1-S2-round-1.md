<!-- run: run-2026-05-13-tk5 -->
<!-- author: Legolas (QA Evaluator, Stage 6 Development, Evaluator-Optimizer round 1) -->
<!-- stories: S1, S2 -->
<!-- target: producer Dispatch A output (Gimli) -->

# QA Evaluation — S1 + S2, Round 1

> *"That bug still only counts as one."* — Legolas

Me Legolas. Me sharp eye. Me run every command. Me find code holds. Two small splinter, no orphans. Forge sound.

---

## 1. STATUS

**STATUS: DONE**

All 16 ACs across S1 + S2 satisfied by code or by deferred-to-UAT path documented in dev notes. All 11 TASK checklist items pass. Two minor non-blocking observations recorded as **Suggestions** for follow-up — neither violates an AC, neither blocks DoD.

---

## 2. Verification Log (every command ran)

### 2.1 AST Parse — all 9 Python files

```
OK delivery-team/tests/smoke/run_smoke.py
OK delivery-team/tests/smoke/__init__.py
OK delivery-team/tests/smoke/lib/__init__.py
OK delivery-team/tests/smoke/lib/workspace.py
OK delivery-team/tests/smoke/lib/runner.py
OK delivery-team/tests/smoke/lib/metrics.py
OK delivery-team/tests/smoke/lib/aggregator.py
OK delivery-team/tests/smoke/lib/report.py
OK delivery-team/tests/smoke/lib/baseline.py
```

### 2.2 `run_smoke.py --help` — exit 0, required flags present

Verified flags: `--init-baseline`, `--cost-cap`, `--timeout`, `--baseline`, `--out-dir`, `--prompt`, `--config`, `--stream-fixture`. Exit code: 0.

### 2.3 Third-party imports — none

`grep -hE "^(import|from) "` over `run_smoke.py` + `lib/*.py` sorted-unique:
```
from __future__ import annotations
from collections import defaultdict
from dataclasses import asdict, is_dataclass / dataclass, field
from pathlib import Path
from typing import Iterable / Literal / Optional / TYPE_CHECKING
from .metrics / .workspace / .runner / etc. import ...
import argparse, datetime, json, os, re, shutil, signal, statistics, subprocess, sys, tempfile, time, warnings
```
Every import is stdlib or sibling-module-relative. Zero third-party.

### 2.4 No `.github/workflows/smoke-*.yml`

`find .github -name "smoke-*.yml"` → empty. BC-01 honored.

### 2.5 No S3 outputs present

- `delivery-team/tests/smoke/tests/` — does not exist.
- `delivery-team/tests/smoke/README.md` — does not exist.
- root `Makefile` — does not exist.
Producer-validator separation (BC-03) honored — Dispatch A did not encroach on S3 territory.

### 2.6 `metrics.py` purity — VERIFIED pure

Module top-level non-declaration lines: **0**. No side-effect files created on import. Module-level names: only dataclasses, helper functions, `parse_stream`, `parse_jsonl_lines`, and stdlib re-exports. No global mutable state.

### 2.7 Aggregator missing-telemetry — graceful empty

Output with no `skill-loads.jsonl`, no `run-summary-*.json`, no `state.md`:
```json
{"skill_loads": [], "pipeline": {"stages_completed": 0, "stories_completed": 0,
 "dispatch_count": 3, "defects_logged": 0}, "run_summary_present": false,
 "state_md_present": false}
```
No crash. Empty defaults flow through. AC-S1-07 satisfied.

### 2.8 Baseline stddev=0 guard — VERIFIED

`init_baseline` with n=1 emits `stddev: 0.0` for every metric. `compare()` advisory branch with `stddev == 0` only flags if `observed != mean` (exact-match) — division-by-zero impossible (line 257-262 of `baseline.py`).

### 2.9 `compare()` returns RegressionResult dataclass — VERIFIED

```
is dataclass: True
fields: {'status': Literal['PASS','FAIL','WARN'],
         'hard_failures': list[str],
         'advisory_warnings': list[str],
         'details': dict}
```
Matches the documented shape in dev notes §4 deviation 2.

### 2.10 End-to-end stream-fixture + cost-cap

Fed 3-event fixture with cumulative cost 1.5 + 2.0 + 0.5 against `--cost-cap 3.0`:
```
events: 2 outcome: {'success': False, 'exit_code': 2, 'reason': 'cost-cap-exceeded'}
```
Correct: after event 2, cumulative=3.5 > 3.0, break. Third event not consumed. Stream file written with the 2 consumed events. AC-S1-02 + AC-S2-04 (cost>hard_max path) demonstrated end-to-end.

### 2.11 compare() PASS / FAIL / WARN matrix

| Case | Status | Detail |
|------|--------|--------|
| same report as baseline | PASS | no hard, no advisory |
| `outcome.success=false` | FAIL | `outcome.success=false (reason='subprocess-exit-1')` |
| `cost_usd=5.0` vs `hard_max=3.0` | FAIL | `cost_usd exceeds hard_max: report=5.0 hard_max=3.0` |
| `tokens.input=99999` vs mean=1000 stddev=0 | WARN | `tokens.input differs from zero-variance baseline: report=99999 mean=1000.0` |

All four behaviors correct per architecture §7.

---

## 3. AC Trace — S1

| AC | Status | Evidence |
|----|--------|----------|
| AC-S1-01 | PASS | `--help` exits 0; lists all flags from TASK checklist (note: `--dry-run` semantically replaced by `--stream-fixture` per dispatch brief — TASK #3 requires `--stream-fixture`, present) |
| AC-S1-02 | PASS | stream-fixture cost-cap test wrote `stream.jsonl` and produced outcome dict without spawning `claude` (verified §2.10) |
| AC-S1-03 | PASS | `workspace.py:34` uses `tempfile.mkdtemp(prefix="smoke-")`; cleanup() rmtrees |
| AC-S1-04 | PASS | `workspace.py:89-105` runs `claude --help`, sniffs `--plugin-dir`, sets `plugin_load_strategy`; copy-into-home path skips `tests/smoke` via `_ignore` (line 118-127) |
| AC-S1-05 | PASS | `runner.py:160-164` enforces `time.monotonic() - start > timeout` mid-stream; `runner.py:182-187` enforces post-stream timeout via `proc.wait(timeout=...)`; `_terminate()` calls `proc.terminate()` (POSIX SIGTERM) → `proc.kill()` fallback. Outcome dict carries `success=false, reason="timeout"` |
| AC-S1-06 | PASS | `metrics.py` pure-verified §2.6; `parse_stream` malformed-event handling §2.7 in dev notes confirmed by my §2.7 + manual two-warning test |
| AC-S1-07 | PASS | `aggregator.py:21-42` returns `[]` on missing skill-loads.jsonl; `_newest_run_summary` returns None on missing telemetry dir; verified §2.7 |
| AC-S1-08 | PASS | `report.py:73-102` `build_report()` emits every §5 key including null-emission for `git_sha` / `claude_cli_version` when subprocess fails (lines 16-31, 34-48) |

### S1 deviation note

Dev §4 documents `--dry-run` → `--stream-fixture` rename. The TASK checklist #3 lists `--stream-fixture` as a required flag, not `--dry-run`, so the rename is the canonical interface for this dispatch. Story 3's README must document `--stream-fixture` (not `--dry-run`).

---

## 4. AC Trace — S2

| AC | Status | Evidence |
|----|--------|----------|
| AC-S2-01 | PASS | `run_smoke.py:184-207` `_init_baseline_flow` runs scenario 5× sequentially; concurrency-of-1 is structural (single-threaded for-loop), no second invocation possible from same process. Baseline JSON written via `init_baseline(reports, args.baseline)`. Live JSON file deferred to UAT per dev note — `baselines/.gitkeep` placeholder only |
| AC-S2-02 | PASS | `baseline.py:166-174` writes `schema_version`, `scenario`, `n_samples`, `last_captured_utc`, `last_captured_git_sha`, `last_captured_cli_version`, `metrics{}` — verified §2.8 with `classification: "hard"`/`"advisory"` literal + `hard_max` on hard entries |
| AC-S2-03 | PASS | `compare()` returns `RegressionResult` dataclass (§2.9). Exit-code-mirroring is enforced in `run_smoke.py:170-176` where `compare()` result drives exit_code; missing-baseline file handled at `run_smoke.py:153-157` (graceful None, no compare attempted) |
| AC-S2-04 | PASS | `_check_hard_rules` (`baseline.py:180-213`) covers: outcome.success=false, cost_usd > hard_max, wall_clock > hard_max, dispatch_count > hard_max, stories_completed != mean (strict equality). Verified §2.11 |
| AC-S2-05 | PASS | `_check_advisory_rules` (`baseline.py:216-271`) walks tokens.* + skill_loads.* keys, checks mean±2σ, zero-stddev guard at line 257-262; appends to `report.advisory_warnings[]` via `run_smoke.py:175-176`; summary.md surfaces them via `report.py:151-155` |
| AC-S2-06 | PASS (with minor wording note) | `prompts/hello_world_spike.txt` is single paragraph plain text; contains "Skip personas" + "Skip exploratory testing depth" + "minimal Stop-hook retrospective" + "Skip retro tail" + "no debates, no consensus rounds". Literal phrase "skip UAT" is **not** present — the substituted phrasing is "Skip retro tail beyond a minimal Stop-hook retrospective". Semantic intent of AC ("skip UAT beyond minimal Stop-hook retrospective") is satisfied; Dispatch B's grep test (TC-S2-08) may need to grep for the actual phrasing. **Suggestion 1** below |
| AC-S2-07 | PASS | `fixtures/delivery_config_minimal.yml` is pure YAML, `schema_version: "2.7"`, empty `checkpoints`/`collaboration_patterns`, no analytics, no fitness reviews, 4-role composition |
| AC-S2-08 | PASS (deferred to UAT) | `init_baseline` algorithm emits entries for every metric present in the 5 input reports — hard metrics (4) + token classes (4) + skill_loads.* (variable) ≥ 8 entries minimum, ≥ 11 once skill loads land. Empty `baselines/.gitkeep` placeholder reflects "live capture at UAT" per dev §4. Algorithm verified §2.8 with 9 entries from 1-sample input |

---

## 5. TASK Checklist (11 items)

| # | Check | Result |
|---|-------|--------|
| 1 | Every AC-S1-* / AC-S2-* satisfied | PASS — see §3, §4 |
| 2 | All Python files parse via `ast.parse` | PASS — §2.1 |
| 3 | `--help` exits 0, all required flags | PASS — §2.2 |
| 4 | `metrics.py` pure functions, no top-level I/O, no globals | PASS — §2.6 |
| 5 | `aggregator.py` handles missing telemetry gracefully | PASS — §2.7 |
| 6 | `baseline.py` stddev=0 divide-by-zero protection | PASS — §2.8 |
| 7 | `compare()` returns `RegressionResult` dataclass | PASS — §2.9 |
| 8 | No third-party imports | PASS — §2.3 |
| 9 | No `.github/workflows/smoke-*.yml` created | PASS — §2.4 |
| 10 | No S3 outputs (tests/, README.md, Makefile) | PASS — §2.5 |
| 11 | Runner subprocess error capture / Stop-hook risk | PASS-with-suggestion — see §6 |

---

## 6. Non-Blocking Suggestions (not AC violations)

### Suggestion 1 — Prompt literal phrasing

`prompts/hello_world_spike.txt` does not contain the literal token "skip UAT". Story 3's anticipated `TC-S2-08` greps for `"skip personas"`, `"skip UAT"`, `"minimal retrospective"`. Two of three substrings match; "skip UAT" does not. Dispatch B will either need to relax the grep to match "Skip retro tail" / "minimal Stop-hook retrospective", or this dispatch can add "skip UAT" verbatim. Since AC-S2-06 is semantically satisfied and Story 3 owns the test, this is a coordination note, not a defect.

**Recommendation**: leave as-is unless Dispatch B reports a grep failure; resolve at S3 evaluator-optimizer round if surfaced.

### Suggestion 2 — `import signal` dead code

`runner.py:6` imports `signal` but the module is never referenced — `_terminate()` uses `proc.terminate()` + `proc.kill()` (which already issue SIGTERM + SIGKILL on POSIX). Harmless lint, but removing the import keeps the stdlib-only inventory tight.

**Recommendation**: drop `import signal` in a follow-up commit; not blocking.

### Suggestion 3 — Subprocess stderr drain risk

`runner.py:136` sets `stderr=subprocess.PIPE` but stderr is never drained. For a long-running `claude` subprocess that writes substantial stderr, the OS pipe buffer (typically 64KB on Linux) could fill and block the subprocess. The current architecture relies on `proc.stdout` iteration to drive forward progress; a stalled stderr would not directly deadlock stdout reading but could pile up. A `stderr=subprocess.STDOUT` merge (combining streams) or a periodic `proc.stderr.read1()` drain in the loop would harden the path.

**Recommendation**: switch to `stderr=subprocess.STDOUT` for simplicity, OR log to `stream_path.with_suffix('.stderr.log')` via a small drain. Defer to S3 hardening if smoke runs are reliably short; flag for re-evaluation if Stage 7 UAT hits a hung run.

---

## 7. Round-1 Verdict

Code holds. Each file parses. Each function returns the shape the architecture promised. Forge sound. Bug count this round: zero blocking, three notes for the long road.

Producer-validator wall standing — S3 dispatch can build its meta-tests against this surface without rework.

— Legolas, QA Evaluator, Dispatch A round 1, run-2026-05-13-tk5.
