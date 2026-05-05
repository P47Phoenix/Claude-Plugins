---
title: "Telemetry JSONL Schema"
version: 1
status: active
adr: ADR-tk0e-001
file: .delivery/telemetry/skill-loads.jsonl
---

# Telemetry JSONL Schema v1

Each line in `skill-loads.jsonl` is a self-contained JSON object (JSONL format).
One row is written per `Skill` tool invocation at PreToolUse time.

## Field Reference

| Field               | Type    | Nullable | Description |
|---------------------|---------|----------|-------------|
| `version`           | string  | No       | Schema version literal — always `"1"` |
| `timestamp`         | string  | No       | ISO 8601 UTC, e.g. `"2026-05-03T14:22:01.123456Z"` |
| `session_id`        | string  | No       | `$CLAUDE_SESSION_ID` env var; `"unknown"` if absent |
| `skill`             | string  | No       | Marketplace skill name, e.g. `"delivery-team:developer"` |
| `model`             | string  | Yes      | `$CLAUDE_MODEL` env var; `null` if absent |
| `prefix_hash`       | string  | Yes      | `sha256(SKILL.md[:2048])[:8]`; `null` if SKILL.md not found |
| `input_tokens`      | integer | No       | Always `0` in Wave 0 (PostToolUse enrichment planned for Wave 1) |
| `cache_read_tokens` | integer | No       | Always `0` in Wave 0 |
| `cache_write_tokens`| integer | No       | Always `0` in Wave 0 |

## Example Row

```json
{
  "version": "1",
  "timestamp": "2026-05-03T14:22:01.123456Z",
  "session_id": "sess-abc123",
  "skill": "delivery-team:developer",
  "model": "claude-sonnet-4-6",
  "prefix_hash": "a1b2c3d4",
  "input_tokens": 0,
  "cache_read_tokens": 0,
  "cache_write_tokens": 0
}
```

## prefix_hash Computation

```python
import hashlib
data = open("delivery-team/skills/developer/SKILL.md", "rb").read(2048)
prefix_hash = hashlib.sha256(data).hexdigest()[:8]
```

The hash covers only the first 2048 bytes of SKILL.md.  It is computed at
PreToolUse time from the file on disk (ADR-tk0e-001 option a) because the
Skill has not yet loaded when the hook fires.

## Reading the File

```python
import json
rows = [json.loads(line) for line in open(".delivery/telemetry/skill-loads.jsonl")]
v1_rows = [r for r in rows if r.get("version") == "1"]
```

Always filter by `version` to handle future mixed-version files.

## Migration Path

- **v1 → v2**: A new ADR must be filed and `telemetry-schema.md` bumped before
  any v2 row is emitted.  Expected additions: `cache_ttl_seconds` (Wave 3).
- Reading scripts MUST filter `version == "1"` to remain forward-compatible.

## Safety Properties

- Hook always exits 0 — a write failure never blocks the Skill invocation.
- Directory `.delivery/telemetry/` is created automatically on first write.
- No external dependencies; stdlib only (`json`, `hashlib`, `os`, `sys`, `datetime`).
