<!-- run: run-2026-05-13-tk5 | backlog: BACKLOG-107 | stage: 06-development | author: Gimli (Developer, follow-up dispatch) -->

# BACKLOG-107 — D-tk5-04 fix + live retry probe

> *"And my code!"* — Gimli

Me Gimli. Me patch `workspace.py`. Me run probe once. Probe still fail. Me NOT retry. Me write honest marker.

---

## 1. Patch summary

**File**: `delivery-team/tests/smoke/lib/workspace.py`
**Change scope**: `subprocess_env()` method + module docstring. No other lib/*.py touched. No tests touched.

### What changed

- HOME no longer overridden. Parent process's HOME is inherited so Claude Code's credential lookup at `~/.claude/.credentials.json` (or system keychain) keeps resolving.
- `XDG_CONFIG_HOME` and `XDG_DATA_HOME` still pointed at the tmpdir, so non-credential config/data the spawned subprocess writes is sandboxed.
- New env var `CLAUDE_PROJECT_DIR=<workdir>` set so the spawned Claude Code instance (if it honors the var) treats the sandbox workdir as its project root.
- Module docstring updated to call out the D-tk5-04 / BACKLOG-107 fix rationale.
- `subprocess_env` precondition tightened: now also requires `self.workdir is not None` (because `CLAUDE_PROJECT_DIR` depends on it).

### Diff (load-bearing lines)

Before (D-tk5-04 broken path):
```python
def subprocess_env(self, base_env: Optional[dict] = None) -> dict:
    """Build the env dict for subprocess.Popen with HOME overridden."""
    if self.home is None:
        raise RuntimeError("Workspace.setup() must run before subprocess_env()")
    env = dict(base_env or os.environ)
    env["HOME"] = str(self.home)
    env["XDG_CONFIG_HOME"] = str(self.home / ".config")
    env["XDG_DATA_HOME"] = str(self.home / ".local" / "share")
    return env
```

After (fix path (a) per Legolas' UAT recommendation):
```python
def subprocess_env(self, base_env: Optional[dict] = None) -> dict:
    """Build env dict for subprocess.Popen.

    IMPORTANT (D-tk5-04 / BACKLOG-107): HOME is NOT overridden. Claude Code
    reads credentials from ``~/.claude/.credentials.json`` (or the system
    keychain via its libsecret/Keychain backend), so the spawned process
    must inherit the parent's HOME to authenticate. Isolation is achieved
    via:

    - ``cwd_for_subprocess`` (the spawned process is chdir'd into a tmp
      workdir; ``.delivery/`` inside that workdir is the pipeline scratch
      area).
    - ``XDG_CONFIG_HOME`` / ``XDG_DATA_HOME`` redirected into the tmp tree
      so any *non-credential* config or data the subprocess writes lands
      in the sandbox instead of the user's real XDG dirs.
    - ``CLAUDE_PROJECT_DIR`` set to the workdir so the spawned Claude Code
      instance (if it honors the env var) treats the sandbox workdir as
      its project root.
    """
    if self.home is None or self.workdir is None:
        raise RuntimeError("Workspace.setup() must run before subprocess_env()")
    env = dict(base_env or os.environ)
    # Deliberately DO NOT override HOME — preserves Claude auth path.
    env["XDG_CONFIG_HOME"] = str(self.home / ".config")
    env["XDG_DATA_HOME"] = str(self.home / ".local" / "share")
    env["CLAUDE_PROJECT_DIR"] = str(self.workdir)
    return env
```

### Patch verification (pre-probe)

```
$ python3 -c "import ast; ast.parse(open('delivery-team/tests/smoke/lib/workspace.py').read()); print('SYNTAX_OK')"
SYNTAX_OK

$ cd delivery-team/tests/smoke && python3 -m pytest tests/test_meta.py -v --tb=short
============================= test session starts ==============================
collected 3 items
tests/test_meta.py::test_malformed_stream_fault_injection PASSED         [ 33%]
tests/test_meta.py::test_baseline_comparison_demo PASSED                 [ 66%]
tests/test_meta.py::test_aggregator_fixture_parsing PASSED               [100%]
============================== 3 passed in 0.02s ===============================
EXIT=0
```

Three meta-tests stay green; runtime well under the 5-second budget.

---

## 2. Live probe

### Command

```
$ rm -rf /tmp/tk5-probe-2 && mkdir -p /tmp/tk5-probe-2
$ python3 delivery-team/tests/smoke/run_smoke.py --timeout 300 --cost-cap 3.00 --out-dir /tmp/tk5-probe-2
EXIT=1
DURATION_SEC=6
```

Wall clock from the runner itself: **5.612 s**. Outer `date` delta: 6 s (rounding). No retries — single probe per dispatch budget.

### Probe report.json (verbatim)

```json
{
  "schema_version": "1",
  "run_id": "smoke-20260514T005258Z",
  "git_sha": "91e1297",
  "claude_cli_version": "2.1.139 (Claude Code)",
  "plugin_load_strategy": "plugin-dir",
  "outcome": {
    "success": false,
    "exit_code": 1,
    "reason": "subprocess-exit-1"
  },
  "wall_clock_seconds": 5.612241389928386,
  "cost_usd": 0.0,
  "tokens": {
    "input": 0,
    "output": 0,
    "cache_creation": 0,
    "cache_read": 0
  },
  "model_usage": [],
  "pipeline": {
    "stages_completed": 0,
    "stories_completed": 0,
    "dispatch_count": 0,
    "defects_logged": 0
  },
  "skill_loads": [],
  "advisory_warnings": [],
  "hard_failures": []
}
```

`stream.jsonl`: **0 bytes** (no events emitted).

### Probe classification

Per dispatch decision tree:

- Exit non-zero (1).
- Wall clock 5.6 s (fast death, longer than the original 0.57 s but still well before any pipeline work could begin).
- `stream.jsonl` empty.
- `cost_usd == 0.0`, `dispatch_count == 0`.

→ **auth_still_broken** (the patched HOME path is necessary but not sufficient).

### Baseline-update decision

**Do NOT update** `delivery-team/tests/smoke/baselines/hello_world_spike.json`. Per dispatch rule: "Auth still fails: exit non-zero quickly, stream empty. → log as D-tk5-04 retry fail; do NOT update baseline." Baseline remains in `sample_status: "deferred"` with `n_samples: 0`. Honest readiness marker preserved.

---

## 3. New defect surfaced — D-tk5-05

> NOTE: per dispatch rule "DO NOT update memory files, BACKLOG-106, or any tk5-named artifact — those are sealed," this new defect is documented here in the BACKLOG-107 notes (the active artifact for this dispatch) rather than appended to `.delivery/defects/sprint-tk5.md`. Recommend the next planning pass promote it into the sprint defect log (or into a fresh sprint log) with a non-tk5 ID.

**D-tk5-05 — Spawned `claude` subprocess still exits 1 even with parent HOME preserved**

- **Severity**: HIGH (blocks the live `--init-baseline` path; the entire smoke-test live-run surface).
- **Status**: OPEN (newly surfaced 2026-05-13 by BACKLOG-107 probe at git sha `91e1297`).
- **Location**: still in the `workspace.py` ↔ `runner.py` ↔ Claude Code CLI seam; root cause is now *below* the HOME-isolation layer.
- **Pre-conditions verified during this dispatch**:
  - `~/.claude/.credentials.json` exists (`-rw------- 471 bytes`, owned by `meconnelly`).
  - Outer `claude --version` works (`2.1.139 (Claude Code)`).
  - `workspace.py` capability probe picks `plugin-dir` strategy correctly (`plugin_load_strategy: "plugin-dir"` in report.json).
  - Inherited HOME = `/home/meconnelly` (parent shell env), so credentials are now reachable from the subprocess perspective.
- **Symptom**: subprocess exits 1 in ~5.6 s with zero stream events. Cost zero, tokens zero. No `hard_failures` or `advisory_warnings` populated because the subprocess died before any event was parsed.
- **Hypotheses for D-tk5-05 root cause** (not validated this dispatch — would require capturing subprocess stderr or running the same command interactively, which is out of scope for the single-probe budget):
  1. **Plugin-load contract**: `--plugin-dir` flag is offered by `--help` but the spawned `claude --print --output-format stream-json --plugin-dir <repo>/delivery-team` invocation may fail because the plugin path is a single plugin dir, not a marketplace root. Claude Code may expect `<root>/.claude-plugin/marketplace.json` shape. Worth printing stderr next iteration.
  2. **Stream-json mode + interactive prompt**: with `--print --output-format stream-json`, Claude Code may require additional flags (model, system prompt, or `--no-interactive`) we are not passing. The 5.6 s duration is consistent with "start up, complain about missing required flag, exit 1".
  3. **Project-trust prompt**: spawned `claude` in a fresh tmp workdir may hit a one-time "trust this folder" prompt that exits 1 in non-interactive mode. The new `CLAUDE_PROJECT_DIR` env may or may not bypass it.
  4. **Settings inheritance**: outer Claude Code session has `.claude/settings.local.json` permissions; spawned process running in tmp workdir under a different cwd may be denied tool use it expects.
- **Diagnostic gap**: `runner.py`'s `_spawn_and_tee` captures `stdout` for stream JSON but `stderr` is collected via `subprocess.PIPE` without being persisted to disk. Adding a `<run-dir>/stderr.log` tee in the next iteration would resolve D-tk5-05 root-cause analysis in one more probe.
- **Recommended next dispatch (NOT this one)**:
  1. Patch `runner.py` to persist subprocess stderr to `<run-dir>/stderr.log` (no live-API spend; pure plumbing).
  2. Run the meta-tests + a `--stream-fixture` smoke to confirm the stderr-tee does not regress anything.
  3. Then spend one more $2 probe to capture stderr from the spawned `claude`, which should expose the exact exit-1 reason.
- **Stop-rule impact**: D-tk5-05 is *the same surface* as D-tk5-04 (auth/spawn path) — it is the bug-behind-the-bug. Whether to count as a separate defect-on-merge depends on PO/team policy; per Legolas' principle ("that bug still only counts as one"), this is arguably one bug surface across two dispatches. PO call.

---

## 4. Artifacts produced

| Path | Change |
|---|---|
| `delivery-team/tests/smoke/lib/workspace.py` | Patched: `subprocess_env` no longer overrides HOME; adds `CLAUDE_PROJECT_DIR`. Module docstring updated. |
| `delivery-team/tests/smoke/baselines/hello_world_spike.json` | **Unchanged** (probe failed; honest marker preserved). |
| `.delivery/artifacts/06-development/developer/BACKLOG-107-notes.md` | This file. |
| `/tmp/tk5-probe-2/20260514T005258Z/report.json` | Live probe result (kept on disk for reference; not checked in). |

---

## 5. DoD self-check (Developer)

- [x] Patch applied to the named file only (`workspace.py`); no other lib/*.py touched.
- [x] Tests not modified.
- [x] Syntax check (`ast.parse`) passes.
- [x] Meta-test suite (3 tests) passes in 0.02 s.
- [x] Single live probe executed; no retries.
- [x] Live spend ≤ $2 budget (actual: $0.00 — subprocess died before token emission).
- [x] No `.github/workflows/` file created.
- [x] No memory file, BACKLOG-106, or sealed tk5 artifact modified.
- [x] Baseline JSON left in deferred state (probe failed, no update warranted).
- [x] New defect (D-tk5-05) documented in this notes file for PO triage.

---

— Gimli (Developer, follow-up dispatch), run-2026-05-13-tk5, BACKLOG-107. *And my code!* Patch shipped. Probe honest. Bug-behind-the-bug logged. No retry. Stop here.
