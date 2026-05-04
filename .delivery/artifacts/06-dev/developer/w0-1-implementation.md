---
story: W0-1
stage: 06-dev
author: Gimli (developer skill, python_developer)
created: 2026-05-04
status: DONE
---

# W0-1 Implementation Notes

## Files Created / Edited

| File | Lines | Action |
|------|-------|--------|
| `delivery-team/hooks/telemetry.py` | 127 | Created |
| `delivery-team/hooks/telemetry_report.py` | 98 | Created |
| `delivery-team/references/telemetry-schema.md` | 76 | Created |
| `delivery-team/hooks/hooks.json` | 90 | Edited (additive) |

## Schema v1 Implementation Notes

- `version` field is the string literal `"1"` (not integer) per ADR-tk0e-001.
- `prefix_hash` = `sha256(SKILL.md[:2048]).hexdigest()[:8]` — Option (a) disk-read at
  PreToolUse time. `null` if the SKILL.md file cannot be resolved.
- Skill name resolution: strips plugin prefix (`delivery-team:developer` → `developer`),
  maps paradigm sub-skills via `_PARADIGM_MAP` dict for `ddd` and `volatility`.
- All token fields default to `0` in Wave 0; Wave 1 PostToolUse enrichment will populate.
- JSONL row is written and flushed EARLY — before any optional enrichment (memory lesson 3).
- `--dry-run` flag suppresses file write; used for overhead benchmarking (AC-3).
- Hook always exits 0; exceptions are written to stderr only (ADR-tk0e-001 failure mode).

## hooks.json Edit (additive only)

Added one `command` hook entry under the existing `PreToolUse → Skill` matcher.
The new entry runs before the existing `prompt` hook (parallel execution; order not
guaranteed by Claude Code, but both run).

```json
{
  "type": "command",
  "command": "python ${CLAUDE_PLUGIN_ROOT}/hooks/telemetry.py",
  "timeout": 5
}
```

Existing entries are unchanged (verified by diff).

## Dogfood Evidence Summary

All 8 ACs verified against real execution.  See evidence file:
`.delivery/artifacts/06-dev/dogfood-evidence/w0-1-telemetry-evidence.md`

| Test | Result | Key Metric |
|------|--------|------------|
| TC-W0-1-1 Hook fires + writes row | PASS | Row written, exit 0 |
| TC-W0-1-2 All 9 fields present | PASS | 0 missing fields |
| TC-W0-1-3 Overhead < 50 ms | PASS | 18.7 ms mean |
| TC-W0-1-4 Read-only dir resilience | PASS | Exit 0; stderr log |
| TC-W0-1-5 prefix_hash determinism | PASS | Stable 8-char hex |
| TC-W0-1-6 No LLM imports | PASS | grep exits 1 |
| TC-W0-1-7 No phantom paths | PASS | 7/7 paths exist |
| AC-5 Schema version documented | PASS | `version: 1` found |
| AC-6 Report script non-empty | PASS | 4-row table printed |

## Known Limitations / Wave 1 Follow-ups

1. **Token counts always 0** — Wave 1 must add a PostToolUse hook to backfill
   `input_tokens`, `cache_read_tokens`, `cache_write_tokens` from the API response.
2. **`skill` field from tool_input only** — if Claude Code changes the Skill tool's
   field name from `skill`/`skill_name`, the hook will silently skip (exits 0).
   Wave 1 should add a stderr warning when skill_name is blank.
3. **No log rotation** — ADR-tk0e-001 defers rotation to Wave 3 retro.
4. **`model` always null in Wave 0** — `CLAUDE_MODEL` env is not set by Claude Code
   at hook time; Wave 1 may explore alternative model detection.
