# S6 cache re-freeze (PA-19, ADR-lmr-001 decision 3 and 7)

Command: `sha256sum delivery-team/skills/delivery-flow/SKILL.md > governance/cache-prefix-hash.txt`

| Value | Before (pre-S2) | After (post S2+S3) |
|---|---|---|
| whole-file sha256 (= governance file) | 43067c9e07e0b988cd976432dd07d5bb3d2336c41ad08a1b0064fb2fbd0b8328 | 31ad503d935bc99b21a98d6d2c71e0d090ad6b926de49de114f93a34ac53c3d8 |
| telemetry prefix (`head -c 2048`, full sha256) | 8c2ebf9705bc0c7f94ee5049e1cc0030cdc5615a868b8bc07097021064837750 | 9402fd57171e5eaf96e92b577a36e93caa5640e9f85c9443e9962e0eb8229284 |
| telemetry `prefix_hash` (first 8 hex) | 8c2ebf97 | 9402fd57 |
| `wc -l` | 499 | 499 |

AC-6.1: `sha256sum ... | diff - governance/cache-prefix-hash.txt && echo MATCH` printed `MATCH`.
AC-6.2: ADR-lmr-001 exists (Accepted).
All 13 stamped delivery-team skills show a new telemetry `prefix_hash` at ship (ADR decision 7). telemetry.py unchanged.
Re-freeze again if delivery-flow SKILL.md changes before S5b or ship.
