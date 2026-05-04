# ADR-tk0e-001: Telemetry JSONL Schema v1

**Status**: Accepted (Architect DoD — 2026-05-03)
**Deciders**: Architect (solution_architect), Product Owner
**PRD refs**: FR-01, FR-02, FR-03, FR-04, FR-11, NFR-01, NFR-02
**Binds**: `delivery-team/hooks/telemetry.py`, `delivery-team/references/telemetry-schema.md`

---

## Context

The delivery-team plugin has no token-usage telemetry. FR-01 requires a PreToolUse hook that
fires on every `Skill` invocation and writes exactly one JSONL row. An architectural choice
must be made about how `prefix_hash` is computed: PreToolUse fires **before** the Skill loads,
so the running context does not yet contain the SKILL.md content at hook execution time.

Two options were evaluated:

- **(a) Disk-read at PreToolUse time** — parse the incoming tool input to extract the skill
  name/path, derive the SKILL.md file path on disk, read the first ~2 KB, and compute
  sha256 truncated to 8 hex chars.
- **(b) Two-row deferred approach** — emit a partial row at PreToolUse (no hash), then emit a
  completion row at PostToolUse with the hash.

The PRD explicitly notes: "Hook captures requested skill name, NOT the loaded content;
`prefix_hash` MUST be computed from the SKILL.md path on disk, not from context" (§7, risk row 3).

Gate-patterns memory lesson 4 requires telemetry rows to be written **early** so truncation
does not lose them.

---

## Decision

**Option (a) — compute prefix_hash from disk at PreToolUse time.**

The hook parses the `tool_input` payload (field `skill` or equivalent path identifier) to
resolve the SKILL.md absolute path. It reads the first 2048 bytes of that file, computes
`sha256(content[:2048]).hexdigest()[:8]`, and includes the result in the single emitted row.

The two-row approach (option b) is rejected because: it requires a stateful matching mechanism
between PreToolUse and PostToolUse events (session_id + skill name correlation), doubles hook
complexity, and violates the "emit early" principle — the PostToolUse row would be the one
containing `prefix_hash`, defeating early telemetry capture.

---

## Schema v1 — Exact Field Specification

```
version:             string  — literal "1"            — NOT NULL
skill:               string  — marketplace skill name  — NOT NULL
model:               string  — model ID string         — NULLABLE (unknown at PreToolUse)
prefix_hash:         string  — sha256[:8] of first 2048B of SKILL.md  — NULLABLE (if file not found)
input_tokens:        integer — estimated from file size proxy; 0 at PreToolUse  — NOT NULL (default 0)
cache_read_tokens:   integer — 0 at PreToolUse (not yet resolvable)              — NOT NULL (default 0)
cache_write_tokens:  integer — 0 at PreToolUse (not yet resolvable)              — NOT NULL (default 0)
timestamp:           string  — ISO 8601 UTC, e.g. "2026-05-03T14:22:01.123456Z" — NOT NULL
session_id:          string  — $CLAUDE_SESSION_ID env var; "unknown" if absent   — NOT NULL
```

All token count fields default to 0 at PreToolUse because the API response has not yet been
received. Wave 1 PostToolUse enrichment (out of scope for Wave 0) will backfill these fields.

**Schema version field** must appear as the literal string `"1"` in every row. Migration path:
- Wave 3 may introduce v2 (e.g., adding `cache_ttl_seconds`). Scripts MUST filter by `version`
  field to handle mixed files.
- `telemetry-schema.md` MUST be bumped and a new ADR filed before any v2 row is emitted.

---

## File Path and Rotation Policy

- **Path**: `.delivery/telemetry/skill-loads.jsonl`
- **Mode**: append-only. The hook opens in `'a'` mode.
- **Rotation**: none in Wave 0. File growth will be assessed in the Wave 3 retro.
  A 13-skill shop running ~100 invocations/day produces ~1 KB/day; rotation is not urgent.
- **Directory creation**: hook MUST `os.makedirs('.delivery/telemetry', exist_ok=True)` on
  startup so the first invocation succeeds without manual setup.

---

## Failure Mode

- If the hook raises any exception (disk full, encoding error, file permission, JSON encoding):
  - MUST catch the exception
  - MUST write the error message to `sys.stderr`
  - MUST NOT re-raise — the Skill invocation proceeds unblocked (FR-11)
- A failed write does NOT cause a JSONL row (no partial rows).

---

## Consequences

**Positive**:
- Single-row model is simple, auditable, and early (satisfies gate-patterns lesson 4).
- Disk-read approach requires no inter-event state; hook is stateless.
- `prefix_hash` is meaningful even before model responds — it captures the SKILL.md prefix
  stability, which is the cache-prefix freeze metric (Ruling 1).

**Negative/Trade-offs**:
- Token counts (`input_tokens`, `cache_read_tokens`, `cache_write_tokens`) are always 0 in
  Wave 0 rows. Actual API token counts require PostToolUse enrichment (Wave 1).
- Disk read adds ~1–3 ms overhead; overall hook MUST remain < 50 ms mean (NFR-01).

---

## Alternatives Considered

| Option | Decision | Reason rejected |
|--------|----------|-----------------|
| Two-row PreToolUse + PostToolUse | Rejected | Requires stateful correlation; late telemetry row violates early-emit principle |
| Hash from in-context content | Rejected | Context does not contain SKILL.md at PreToolUse; violates PRD §7 binding |
| Async file write | Rejected | Adds threading complexity; < 50 ms budget is achievable synchronously |

---

*Authors must build via `plugin-dev:hook-development` (CLAUDE.md load-bearing routing constraint).*
