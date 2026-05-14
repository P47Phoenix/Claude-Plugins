<!-- run: run-2026-05-13-tk5 | backlog: BACKLOG-107 | defect: D-tk5-05 | stage: 06-development | author: Gimli (Developer, iter2 dispatch) -->

# BACKLOG-107 iter2 — D-tk5-05 fix (stderr-tee + `--verbose` flag)

> *"And my code!"* — Gimli

Me Gimli. Me dwarf. Me patch `runner.py` with stderr-tee. Me probe once — stderr say *"requires --verbose"*. Me add `--verbose`. Me probe twice — green. Total spend: two probes, ~$0 (no usage events). Baseline now partial-1-of-5.

---

## 1. Patch 1 — Stderr-tee in `runner.py`

**File**: `delivery-team/tests/smoke/lib/runner.py`
**Scope**: live-spawn path only. Fixture path and stream.jsonl tee untouched.

### Diff summary

- Added module docstring note for D-tk5-05.
- Imported `threading`.
- Added helper `_stderr_log_path(stream_path) -> Path` (returns `<run-dir>/stderr.log`).
- Added helper `_drain_stderr_to_file(stderr_stream, stderr_path)` — drains the spawned subprocess's stderr into the file line-by-line in a background daemon thread (avoids deadlock on a full stderr pipe).
- Added helper `_write_stderr_header(stderr_path, cmd, cwd)` — seeds stderr.log with `# argv: [...]`, `# cwd: ...`, and a `# --- stderr stream begins ---` separator, BEFORE the subprocess is spawned. Survives even `FileNotFoundError`/`OSError` spawn failures (which now also append `# spawn-failed: ...`).
- Modified `_spawn_and_tee`:
  - Call `_write_stderr_header` before `subprocess.Popen`.
  - After spawn, start a `threading.Thread(target=_drain_stderr_to_file, daemon=True)` reading `proc.stderr`.
  - In the `finally` block, `stderr_thread.join(timeout=2.0)` to let the drain flush without blocking shutdown.

### Diff (load-bearing additions)

```python
def _stderr_log_path(stream_path: Path) -> Path:
    """Stderr log lives next to stream.jsonl inside the run dir."""
    return stream_path.parent / "stderr.log"


def _drain_stderr_to_file(stderr_stream, stderr_path: Path) -> None:
    if stderr_stream is None:
        return
    try:
        with stderr_path.open("a", encoding="utf-8") as fh:
            for raw_line in stderr_stream:
                fh.write(raw_line)
                fh.flush()
    except (OSError, ValueError):
        return


def _write_stderr_header(stderr_path: Path, cmd: list[str], cwd: str) -> None:
    stderr_path.parent.mkdir(parents=True, exist_ok=True)
    header_lines = [
        f"# argv: {json.dumps(cmd)}\n",
        f"# cwd:  {cwd}\n",
        f"# --- stderr stream begins ---\n",
    ]
    with stderr_path.open("w", encoding="utf-8") as fh:
        fh.writelines(header_lines)
        fh.flush()
```

Inside `_spawn_and_tee`:

```python
cwd = str(workspace.cwd_for_subprocess)
stderr_path = _stderr_log_path(stream_path)
_write_stderr_header(stderr_path, cmd, cwd)
# ...
stderr_thread = threading.Thread(
    target=_drain_stderr_to_file,
    args=(proc.stderr, stderr_path),
    name="smoke-stderr-tee",
    daemon=True,
)
stderr_thread.start()
# ...finally:
stderr_thread.join(timeout=2.0)
```

### Why a thread, not inline reading

`subprocess.Popen` allocates separate OS pipes for stdout and stderr. If we read stdout in a `for raw_line in proc.stdout` loop without draining stderr, a chatty subprocess can fill the stderr pipe buffer (~64 KB on Linux) and block forever. The daemon thread drains stderr concurrently. `daemon=True` means it never blocks interpreter shutdown if the subprocess is forcibly killed.

### Pre-probe verification

```
$ python3 -c "import ast; ast.parse(open('delivery-team/tests/smoke/lib/runner.py').read()); print('SYNTAX_OK')"
SYNTAX_OK

$ cd delivery-team/tests/smoke && python3 -m pytest tests/test_meta.py -v --tb=short
collected 3 items
tests/test_meta.py::test_malformed_stream_fault_injection PASSED         [ 33%]
tests/test_meta.py::test_baseline_comparison_demo PASSED                 [ 66%]
tests/test_meta.py::test_aggregator_fixture_parsing PASSED               [100%]
============================== 3 passed in 0.02s ===============================
EXIT=0
```

Meta-tests green. Stream-fixture path untouched. Cost-cap path untouched.

---

## 2. Probe 1 — Diagnostic (with stderr tee)

```
$ rm -rf /tmp/tk5-probe-3 && mkdir -p /tmp/tk5-probe-3
$ python3 delivery-team/tests/smoke/run_smoke.py --timeout 300 --cost-cap 3.00 --out-dir /tmp/tk5-probe-3
EXIT=1
```

### `stderr.log` (verbatim)

```
# argv: ["claude", "--print", "--output-format", "stream-json", "--plugin-dir", "/var/home/meconnelly/Documents/GitHub/Claude-Plugins/delivery-team"]
# cwd:  /tmp/smoke-o0wijvjc/work
# --- stderr stream begins ---
Error: When using --print, --output-format=stream-json requires --verbose
```

### `report.json` (verbatim)

```json
{
  "schema_version": "1",
  "run_id": "smoke-20260514T005641Z",
  "git_sha": "91e1297",
  "claude_cli_version": "2.1.139 (Claude Code)",
  "plugin_load_strategy": "plugin-dir",
  "outcome": {
    "success": false,
    "exit_code": 1,
    "reason": "subprocess-exit-1"
  },
  "wall_clock_seconds": 5.93865065893624,
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

`stream.jsonl`: 0 bytes (subprocess died before emitting any event).

---

## 3. Root-cause classification

**Category (b) — Missing required flag.**

Claude Code CLI v2.1.139 enforces that `--print --output-format=stream-json` requires `--verbose`. The runner was building `["claude", "--print", "--output-format", "stream-json", "--plugin-dir", ...]` — missing `--verbose`. Subprocess died at startup with exit 1 in ~5.6s before any stream event. This is below the HOME-isolation layer (D-tk5-04 was a prerequisite but not sufficient), consistent with iter1's diagnostic gap recommendation.

This category is "fixable in same dispatch" per the dispatch rules. Applied follow-up fix below.

---

## 4. Patch 2 — Add `--verbose` to claude command

**Same file**: `delivery-team/tests/smoke/lib/runner.py`
**Scope**: `_build_claude_command` only.

```python
def _build_claude_command(workspace: Workspace, prompt_path: Path) -> list[str]:
    # D-tk5-05 fix (BACKLOG-107 iter2): `--print --output-format=stream-json`
    # requires `--verbose` per Claude Code CLI contract; absence caused the
    # subprocess to exit 1 with "When using --print, --output-format=stream-json
    # requires --verbose" before emitting any stream events.
    cmd = ["claude", "--print", "--output-format", "stream-json", "--verbose"]
    if workspace.plugin_load_strategy == PLUGIN_LOAD_PLUGIN_DIR:
        cmd.extend(["--plugin-dir", str(workspace.plugin_path)])
    return cmd
```

Re-verify: `SYNTAX_OK` + 3 meta-tests pass in 0.02s.

---

## 5. Probe 2 — Verification (after `--verbose` fix)

```
$ rm -rf /tmp/tk5-probe-3b && mkdir -p /tmp/tk5-probe-3b
$ python3 delivery-team/tests/smoke/run_smoke.py --timeout 300 --cost-cap 3.00 --out-dir /tmp/tk5-probe-3b
EXIT=0
```

### `stderr.log` (verbatim)

```
# argv: ["claude", "--print", "--output-format", "stream-json", "--verbose", "--plugin-dir", "/var/home/meconnelly/Documents/GitHub/Claude-Plugins/delivery-team"]
# cwd:  /tmp/smoke-y6b2dz3e/work
# --- stderr stream begins ---
```

(Empty stderr stream — subprocess ran cleanly.)

### `report.json` (verbatim)

```json
{
  "schema_version": "1",
  "run_id": "smoke-20260514T005710Z",
  "git_sha": "91e1297",
  "claude_cli_version": "2.1.139 (Claude Code)",
  "plugin_load_strategy": "plugin-dir",
  "outcome": {
    "success": true,
    "exit_code": 0,
    "reason": null
  },
  "wall_clock_seconds": 44.565676964004524,
  "cost_usd": 0.0,
  "tokens": {
    "input": 6,
    "output": 1092,
    "cache_creation": 47619,
    "cache_read": 46561
  },
  "model_usage": [
    {
      "model": "unknown",
      "dispatches": 1,
      "input_tokens": 6,
      "output_tokens": 1092,
      "cache_creation_tokens": 47619,
      "cache_read_tokens": 46561
    }
  ],
  "pipeline": {
    "stages_completed": 0,
    "stories_completed": 0,
    "dispatch_count": 1,
    "defects_logged": 0
  },
  "skill_loads": [],
  "advisory_warnings": [],
  "hard_failures": []
}
```

`stream.jsonl`: **37,074 bytes** with valid stream events (`hook_started`, `hook_response`, `init`, assistant turns).

### Notable observations

- `cost_usd: 0.0` despite 1092 output tokens. The `init` event and assistant events did not carry `usage.cost_usd` fields in this CLI version, so `parse_stream` reported 5 `UserWarning`s of the form `parse_stream: event N type='assistant' missing 'usage' key; skipping usage extraction`. The token counts came from elsewhere in the stream. Not a regression; just a CLI-version delta in stream shape. Worth a separate ticket if the team wants cost-tracking accuracy.
- `pipeline.stages_completed: 0` / `pipeline.stories_completed: 0` because the smoke prompt is a minimal "hello world" spike — it doesn't drive a full pipeline run. `dispatch_count: 1` confirms one model dispatch happened.
- `plugin_load_strategy: "plugin-dir"` — the `--plugin-dir` flag worked; `init` event's `plugins[]` list shows `delivery-team` was loaded with source `delivery-team@inline`. Hypothesis (1) from iter1 (plugin-load contract) is **disproven** in addition to hypothesis (2) being confirmed.

---

## 6. Baseline update

Per dispatch instruction: probe ultimately succeeded → update baseline with `n_samples=1`, `sample_status="partial-1-of-5"`, `mean=sample_value`, `stddev=0.0` per metric.

**File**: `delivery-team/tests/smoke/baselines/hello_world_spike.json`

- `sample_status`: `deferred` → `partial-1-of-5`
- `n_samples`: `0` → `1`
- `last_captured_utc`: `null` → `"2026-05-14T00:57:10Z"`
- `last_captured_git_sha`: `null` → `"91e1297"`
- `last_captured_cli_version`: `null` → `"2.1.139 (Claude Code)"`
- All metric `mean` values populated from probe 2.
- All metric `stddev` values set to `0.0` (n=1).
- `deferred_reason`: removed (set to `null`).
- `_header_comment` rewritten to describe the partial baseline state and reference iter2.

Validated: `json.load` succeeds, schema preserved.

---

## 7. DoD self-check (Developer)

- [x] Patches applied to the named file only (`runner.py`); no other lib/*.py touched.
- [x] Tests not modified. Meta-tests (3) pass twice (once per patch).
- [x] Syntax check (`ast.parse`) passes after each patch.
- [x] Stderr tee writes argv header + cwd before subprocess spawn (survives spawn-failures).
- [x] Stream-fixture path untouched (verified by reading `_run_from_fixture` left alone).
- [x] Cost-cap mid-stream termination logic untouched.
- [x] Stderr drain thread is a daemon with `.join(timeout=2.0)` — non-blocking shutdown.
- [x] Total live probes: 2 (budget ≤ 2). Spend: ~$0.00 reported (no `usage.cost_usd` in events).
- [x] Baseline JSON updated to `partial-1-of-5` per dispatch instruction.
- [x] No `.github/workflows/` file created.
- [x] No memory file, BACKLOG-106, or sealed tk5 artifact modified.
- [x] Honest readiness markers preserved (partial-1-of-5, not pretend-5-of-5).

---

## 8. Recommendation for next steps (not this dispatch)

1. **Collect remaining 4 baseline samples**: run `python3 delivery-team/tests/smoke/run_smoke.py --init-baseline` to drive the 5-sample loop and replace the partial baseline with real mean+stddev. Each sample is ~45s wall clock at ~$0 cost; total ~4 minutes.
2. **Cost-tracking accuracy** (minor follow-up): the smoke aggregator emits 5 `UserWarning`s because assistant events lack `usage` in CLI v2.1.139's stream-json schema. Either:
   - Update `parse_stream` to silently skip assistant events without `usage` (lower warning noise), or
   - File a CLI-side issue if the team expects `usage` on every assistant event.
3. **Smoke prompt**: `pipeline.stages_completed=0` means the current spike prompt doesn't exercise the pipeline. If the goal is a smoke that actually walks 1+ stage of delivery-flow, the prompt needs to invoke the orchestrator. Out of scope for this dispatch — flag for the Architect/QA pair on the next sprint.
4. **D-tk5-05 closure**: this defect is now closed — root cause confirmed, fix applied, fix verified. Promote to "Resolved" on the next planning pass.

---

— Gimli (Developer, BACKLOG-107 iter2), run-2026-05-13-tk5. *And my code!* Stderr tee shipped. `--verbose` flag landed. Bug-behind-the-bug killed. Baseline partial. Stop here.
