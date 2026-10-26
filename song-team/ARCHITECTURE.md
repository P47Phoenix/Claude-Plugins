# song-team Architecture

> **Status: scaffold (Wave 0).** Final diagrams land in Wave 5 (W5-3). Until then `docs/plans/song-team-plan.md` is the design source of truth.

## Components (planned)

- `skills/song-flow` orchestrator (Tier A) and seven worker/leaf skills.
- `scripts/` deterministic gates sharing the `gate_common.py` contract.
- `hooks/` Claude Code hooks (SessionStart, PreToolUse, PostToolUse, SubagentStop, Stop).
- `references/shared/` orchestrator-visible doctrine, gate rules, routing matrix, config schema, originality policy.
