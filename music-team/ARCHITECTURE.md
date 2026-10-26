# music-team Architecture

> **Status: scaffold (Wave 0).** Final diagrams land in Wave 5 (W5-3). Until then `docs/plans/music-team-plan.md` is the design source of truth.

The runtime data directory stays `.song/` by design (it is a data format, not the plugin name), so existing `.song/` projects keep working after the rename from song-team to music-team.

## Components (planned)

- `skills/music-flow` orchestrator (Tier A) and seven worker/leaf skills.
- `scripts/` deterministic gates sharing the `gate_common.py` contract.
- `hooks/` Claude Code hooks (SessionStart, PreToolUse, PostToolUse, SubagentStop, Stop).
- `references/shared/` orchestrator-visible doctrine, gate rules, routing matrix, config schema, originality policy.
