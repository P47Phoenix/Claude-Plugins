# Dev Notes

## US-3: CHANGELOG entry + dev-notes

Skill loads: `delivery-team:developer` loaded. `plugin-dev:skill-development` loaded first per repo CLAUDE.md (FR-10). No SKILL.md touched in US-3; load recorded for US-1 (prompt-engineer/SKILL.md:368).

### Changes
- `CHANGELOG.md`: `[Unreleased]` placeholder line replaced with `### Changed` entry naming `claude-opus-5`, `claude-sonnet-5`, `claude-fable-5-1` (allowlisted, not adopted), `stale-model-id-guard` (positive allowlist). Retired IDs not named; tier wording plus `>` blockquote. History untouched.
- No commit (staged into US-1 shipping commit later).

### AC results
| AC | Command | Result |
|---|---|---|
| AC-25 | `grep -c 'plugin-dev:skill-development' dev-notes.md` | >=1 (this file mentions it) |
| AC-28a | `grep -cE 'claude-opus-5\|claude-sonnet-5\|stale-model-id-guard' CHANGELOG.md` | 2 (>=1, pass) |
| AC-28b | `git diff CHANGELOG.md \| grep -E '^-[^-]' \| grep -vc 'No unreleased changes'` | 0 (pass) |
| T-C3 | `git grep -nE 'claude-(opus-4-7\|sonnet-4-6)' -- CHANGELOG.md \| grep -vE '^[^:]+:[0-9]+:[[:space:]]*[#>]'` | no output (pass) |

Note: CHANGELOG mentions `claude-fable-5-1` on a non-`>` line; AC-07 excludes CHANGELOG.md, so ok. Guard allowlists fable-5-1 so it passes.
