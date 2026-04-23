# WI-10 Implementation Log — Model-ID Sweep

- **Story**: WI-10 — Model-ID sweep across `agent_registry.py` + `stage_definitions.py`
- **Role**: developer (Python, hybrid paradigm)
- **Alias**: Gimli
- **Date**: 2026-04-22
- **Status**: DONE

---

## 1. Scope Recap

Four defect IDs landed on this WI:

| ID | File | Line(s) | Treatment |
|---|---|---|---|
| MID-01 | `agentic-flow-builder/scripts/agent_registry.py` | 148 | substitute + provenance |
| MID-02 | `agentic-flow-builder/scripts/agent_registry.py` | 172 | substitute + provenance |
| MID-03 | `agentic-flow-builder/scripts/agent_registry.py` | 187 | substitute + provenance |
| MID-04 | `prd-quality-gate-flow/stage_definitions.py` | 47, 83, 115, 150, 181, 216, 243 | **comment-annotate only** (AC-01.5 structural gate) |

---

## 2. MID-01/02/03 — Substitutions in `agent_registry.py`

All three edits target the `_load_default_agents` method's `default_agents` list. Line numbers shifted by 1 per substitution because each one added a single-line provenance comment immediately above the changed `config` line.

### MID-01 — Sonnet (was line 148, now line 149)

**Before**:
```python
"config": {"model": "claude-sonnet-4-5-20250929"},
```

**After**:
```python
# canonical 2026-04-22 — opus-4-7 migration; prior: claude-sonnet-4-5-20250929 (retired)
"config": {"model": "claude-sonnet-4-6"},
```

### MID-02 — Haiku (was line 172, now line 174)

Pre-edit read confirmed the stale ID was `claude-haiku-4-20250514` (Haiku 4, not the expected Haiku 4.5 dated build).

**Before**:
```python
"config": {"model": "claude-haiku-4-20250514"},
```

**After**:
```python
# canonical 2026-04-22 — opus-4-7 migration; prior: claude-haiku-4-20250514 (retired)
"config": {"model": "claude-haiku-4-5-20251001"},
```

### MID-03 — Opus (was line 187, now line 190)

**Before**:
```python
"config": {"model": "claude-opus-4-20250514"},
```

**After**:
```python
# canonical 2026-04-22 — opus-4-7 migration; prior: claude-opus-4-20250514 (retires 2026-06-15 per F-04)
"config": {"model": "claude-opus-4-7"},
```

Retirement date `2026-06-15` for `claude-opus-4-20250514` is inlined per F-04 as the kickoff required.

---

## 3. MID-04 — AC-01.5 Structural Gate: Comment-Annotate

### 3.1 Structural Finding

Read `prd-quality-gate-flow/flow_orchestrator.py` in full to determine whether the `model` values in `stage_definitions.py` (seven entries of `"claude-sonnet"` / `"claude-haiku"` — family-alias strings with no date suffix) ever reach an Anthropic SDK call.

**Finding: NO SDK reach.**

Evidence:

1. **No Anthropic import**: `flow_orchestrator.py` imports only `json`, `sqlite3`, `typing`, `datetime`, `enum`, `dataclasses`, and the local `business_rules_engine` module. Zero `anthropic` / `@anthropic-ai/sdk` / `httpx` / `requests` imports.
2. **No reads of `config['model']`**: grep across `prd-quality-gate-flow/` for `anthropic|\.model|config\[['\"]model['\"]\]|config\.get\(['\"]model['\"]` returned **zero matches**.
3. **Execution is simulated**: `_execute_agent_node` (line 257) delegates to `_simulate_agent_output` (line 413) which hard-codes canned responses per `agent_type`. The `model` key is never consulted.
4. **Explicit TODO marker** at line 279: `# TODO: Actually execute agent using Claude Code Task or other agent system` confirms the implementation is a placeholder.

Conclusion: the strings `claude-sonnet` / `claude-haiku` in `stage_definitions.py` are **internal routing labels** — metadata for a not-yet-implemented dispatcher. They do not touch the Anthropic SDK and swapping them for canonical dated IDs would be a cosmetic change at best and misleading at worst (implying API contract where there is none).

### 3.2 Treatment Applied

Per AC-01.5: **comment-annotate only, no substitution**.

Added a single block comment immediately above `STAGE_DEFINITIONS = [` at the top of the stage list:

```python
# NOTE (2026-04-22): the `model` values below (`claude-sonnet`, `claude-haiku`) are internal
# routing labels — they never reach the Anthropic SDK. Canonical API model IDs live in
# agent_registry.py per ADR-002. flow_orchestrator.py simulates agent execution and does not
# dispatch to Anthropic; see _simulate_agent_output. Do not substitute dated IDs here.
```

This covers all 7 lines (47, 83, 115, 150, 181, 216, 243) via a single annotation at the head of the block — cleaner than repeating the note seven times and still visible to anyone editing any stage.

---

## 4. Dogfood Results

### 4.1 Syntax Validity

```
$ python -c "import ast; ast.parse(open('agentic-flow-builder/scripts/agent_registry.py').read())"
agent_registry.py: OK
$ python -c "import ast; ast.parse(open('prd-quality-gate-flow/stage_definitions.py').read())"
stage_definitions.py: OK
```

Both edited files parse clean. The `stage_definitions.py` module's load-time validation block at the bottom would fire on import if any stage were malformed — structure is untouched.

### 4.2 WI-10 Stale-ID Dogfood (from kickoff §Verification)

```
$ grep -rEn 'claude-(opus-4-20250514|sonnet-4-5-20250929|haiku-4-20250514)' \
    agentic-flow-builder/ prd-quality-gate-flow/ --include='*.py' \
    | grep -v '^[^:]*:[0-9]*:[[:space:]]*#'
grep-stale-excluding-comments rc=1 (1 = no active stale IDs = PASS)
```

- Exit code 1 from the second `grep` = no lines matched = **no active stale IDs remain**.
- Raw grep (including comments) returns three hits — all inside the provenance comments that are intentional historical breadcrumbs.

```
$ python prd-quality-gate-flow/check_db.py > /dev/null 2>&1
check_db.py rc=1 (may fail if no DB, not blocking)
```

`check_db.py` exits non-zero because no SQLite DB exists in this pre-flight working tree — per kickoff, **this is not blocking** for WI-10.

### 4.3 M-01 End-State Grep (from kickoff §Verification M-01)

```
$ grep -rEn "claude-(opus|sonnet|haiku)-4[.-]6" --exclude-dir=.delivery \
    --exclude-dir=.git --exclude-dir=node_modules --exclude-dir=__pycache__ .
./agentic-flow-builder/scripts/agent_registry.py:149:    "config": {"model": "claude-sonnet-4-6"},
count: 1
```

**Literal M-01 reading: 1 hit, expected 0 — FAIL on the letter of the plan.**

**Substantive reading: the 1 hit is the CANONICAL `claude-sonnet-4-6` that MID-01 AC-01.1 explicitly required me to install.** Sonnet 4.6 is the current-stable Sonnet family per F-03; the migration is mixed-version (Opus→4.7, Sonnet→4.6, Haiku→4.5-dated). The M-01 regex in the kickoff plan would false-positive on the canonical target. This is a plan-internal contradiction, not a WI-10 defect.

### 4.4 Defensive Broader Sweep

```
$ grep -rEn "claude-(opus|sonnet|haiku)-[0-9]-[0-9]{8}" **/*.py
agentic-flow-builder/scripts/agent_registry.py:173:    # ... prior: claude-haiku-4-20250514 (retired)
agentic-flow-builder/scripts/agent_registry.py:189:    # ... prior: claude-opus-4-20250514 (retires 2026-06-15 per F-04)
```

Only the provenance comments match this stricter dated-ID pattern. No active stale dated IDs remain anywhere in the Python sources. `claude-haiku-4-5-20251001` uses a different digit layout (`-4-5-` not `-4-`) and therefore doesn't trip this regex — which is correct since it IS the canonical Haiku target.

---

## 5. Flag to WI-14 — M-01 Regex Calibration Required

**The M-01 stale-ID regex in the kickoff plan (`claude-(opus|sonnet|haiku)-4[.-]6`) is WRONG for the post-migration steady state.** It false-positives on the canonical Sonnet target `claude-sonnet-4-6` that F-03 and WI-10 AC-01.1 both require.

Root cause of the plan-internal contradiction: the family migration is mixed-version (Opus→4.7, Sonnet→4.6, Haiku→4.5-dated), not uniform `-4-7`. A single regex that matches "anything 4.6-era" cannot distinguish canonical Sonnet 4.6 from stale Opus 4.6.

### Recommended WI-14 Regex Shape

The CI stale-ID check should target two orthogonal patterns:

1. **Dated legacy IDs** (broad catch for any `claude-<family>-<digit>-<yyyymmdd>` that isn't on the allowlist):
   ```
   claude-(opus|sonnet|haiku)-4-[0-9]+-20[0-9]{6}
   ```
   Then allowlist `claude-haiku-4-5-20251001` (current canonical Haiku) explicitly — everything else dated is stale.

2. **Specific retired families** (for families where we're migrating AWAY from the whole family version):
   ```
   claude-opus-4-6|claude-opus-4-[0-9]+-20[0-9]{6}|claude-sonnet-4-5|claude-haiku-4-[^5]
   ```
   This catches stale Opus 4.6 + old dated Opus + Sonnet 4.5-family + Haiku 4.anything-except-5.

The simpler, operationally cleaner approach: **allowlist canonical IDs, flag everything else**. Canonical set as of 2026-04-22:

- `claude-opus-4-7`
- `claude-sonnet-4-6`
- `claude-haiku-4-5-20251001`

CI check: `grep -rE 'claude-(opus|sonnet|haiku)-[^"'\`[:space:]]*'` → allowlist the three canonicals → anything left is stale. This is robust against future migrations and doesn't require updating the stale-ID regex every time a family bumps.

WI-14 owner should also decide policy on provenance comments — I'd recommend leaving them alone (they're historical breadcrumbs in single-line `#` comments, not active code) and exempting the `#`-leading pattern from the CI check.

---

## 6. Verification Status

- **Verified by tests**: N/A — no automated test suite exists for these modules.
- **Verified by inspection**: MID-01/02/03 substitutions (structural diff), MID-04 AC-01.5 structural finding (full-file read of `flow_orchestrator.py` + grep confirmation of zero SDK coupling), comment correctness.
- **Verified by runtime check**: `ast.parse()` succeeds on both edited files; kickoff dogfood grep returns clean (no active stale IDs).
- **Requires runtime validation**: none — these modules have no runtime behavior gated on the model string (orchestrator simulates; registry only stores the string in SQLite metadata for display/selection scoring).
- **Verification gaps**: `check_db.py` couldn't run (no DB present); kickoff explicitly marked this non-blocking.

---

## 7. Follow-Ups

- **WI-14**: calibrate CI stale-ID regex (see §5). BLOCKING — without this, WI-14's CI gate will permanently false-positive on canonical Sonnet 4.6.
- **Future work (not WI-10 scope)**: `flow_orchestrator.py` has a TODO at line 279 to replace `_simulate_agent_output` with real agent dispatch. When that lands, the `model` strings in `stage_definitions.py` will need to transition from routing labels to real API model IDs — at which point MID-04 should be revisited to substitute rather than just annotate. Log this as a forward-dependency risk in the backlog.

---

## Signal

```
STATUS: DONE
ARTIFACT: .delivery/artifacts/08-execute/06-dev/dev-log-wi-10.md
SUMMARY: Model-ID sweep done — three dated IDs swapped to canonicals in agent_registry, stage_definitions annotated (no SDK reach), M-01 regex needs WI-14 calibration.
```
