# Dev Log — WI-13: NEW-BACKLOG registration + GitHub issues (dual-write)

**Role:** Product Owner (alias: Gandalf)
**Engagement:** run-2026-04-22-4x7e
**Date:** 2026-04-22
**Story:** WI-13 — NEW-BACKLOG registration + GitHub issues (dual-write deviation)

---

## Part A — Local backlog files

9 files created under `.delivery/backlog/` (all 6 REQUIRED + all 3 OPTIONAL Galadriel on-ramp items, since time permitted).

| # | Title | Local path | Issue # |
|---|-------|------------|---------|
| 1 | Evaluate `task_budget` (beta) adoption across agentic flows | `.delivery/backlog/BACKLOG-47-task-budget-eval.md` | [#77](https://github.com/P47Phoenix/Claude-Plugins/issues/77) |
| 2 | Evaluate client-side `memory` tool adoption | `.delivery/backlog/BACKLOG-47-memory-tool-eval.md` | [#78](https://github.com/P47Phoenix/Claude-Plugins/issues/78) |
| 3 | Anthropic SDK adoption pathway via `claude-api` skill | `.delivery/backlog/BACKLOG-47-sdk-wiring-routing-via-claude-api.md` | [#79](https://github.com/P47Phoenix/Claude-Plugins/issues/79) |
| 4 | Narrow cyber-safeguard refusal check for architect security/IR references | `.delivery/backlog/BACKLOG-47-r-06-cyber-safeguard.md` | [#80](https://github.com/P47Phoenix/Claude-Plugins/issues/80) |
| 5 | Upgrade 11 backfill SKILL.md files from `opus-4-7-frontmatter-only` to `opus-4-7` via prose skim | `.delivery/backlog/BACKLOG-47-frontmatter-only-prose-skim.md` | [#81](https://github.com/P47Phoenix/Claude-Plugins/issues/81) |
| 6 | Keystone SKILL.md audit for `CRITICAL:/MUST/NEVER/ALWAYS` over-pressure patterns | `.delivery/backlog/BACKLOG-47-overpressure-audit.md` | [#82](https://github.com/P47Phoenix/Claude-Plugins/issues/82) |
| 7 | Add 4.7-awareness note to CONTRIBUTING guidance (optional Galadriel on-ramp) | `.delivery/backlog/BACKLOG-47-contributing-4-7-note.md` | [#83](https://github.com/P47Phoenix/Claude-Plugins/issues/83) |
| 8 | Publish a 4.6 → 4.7 migration guide stub (optional Galadriel on-ramp) | `.delivery/backlog/BACKLOG-47-migration-guide-stub.md` | [#84](https://github.com/P47Phoenix/Claude-Plugins/issues/84) |
| 9 | Designate a canonical "4.7 exemplar" skill (optional Galadriel on-ramp) | `.delivery/backlog/BACKLOG-47-4-7-example-skill-designation.md` | [#85](https://github.com/P47Phoenix/Claude-Plugins/issues/85) |

## Part B — GitHub issues

- Label `backlog-47` was ensured (color `#FBCA04`, description "Deferred scope from run-2026-04-22-4x7e Opus 4.7 migration"). The `gh label create` call returned no error; label was either newly created or already present (`|| true` semantics preserved via non-blocking output).
- 9 issues created via `gh issue create ... --label backlog-47 --body "$(cat <file>)"`. All returned 200 OK with URLs captured above.
- Verification via `gh issue list --label backlog-47 --state all`:
  ```
  85: BACKLOG-47: Designate a canonical 4.7 exemplar skill
  84: BACKLOG-47: Publish a 4.6 to 4.7 migration guide stub
  83: BACKLOG-47: Add 4.7-awareness note to CONTRIBUTING guidance
  82: BACKLOG-47: Keystone SKILL.md audit for CRITICAL/MUST/NEVER/ALWAYS over-pressure patterns
  81: BACKLOG-47: Upgrade 11 backfill SKILL.md files from frontmatter-only to opus-4-7 via prose skim
  80: BACKLOG-47: Narrow cyber-safeguard refusal check for architect security/IR references
  79: BACKLOG-47: Anthropic SDK adoption pathway via claude-api skill
  78: BACKLOG-47: Evaluate client-side memory tool adoption
  77: BACKLOG-47: Evaluate task_budget (beta) adoption across agentic flows
  ```

## Part C — Dogfood + dual-write invariant

Ran the WI-13 dogfood check:

```
LOCAL=$(ls .delivery/backlog/BACKLOG-47-*.md 2>/dev/null | wc -l)
ISSUES=$(gh issue list --label backlog-47 --state all --json number --jq 'length')
echo "local=$LOCAL issues=$ISSUES"
test "$LOCAL" -ge "6" && test "$ISSUES" -ge "6" && test "$LOCAL" = "$ISSUES"
```

**Result:**
- `local=9 issues=9`
- Dogfood exit code: **0**
- Both counts ≥ 6: **yes**
- `LOCAL == ISSUES`: **yes**

**Dual-write invariant: PASS**

## Source anchor traceability

| File | Source anchor |
|---|---|
| task-budget-eval | PRD REQ-07 AC-07.1; §1 Non-Goals |
| memory-tool-eval | PRD REQ-07 AC-07.2; §1 Non-Goals |
| sdk-wiring-routing-via-claude-api | ADR-004 + PRD Open Question 8 |
| r-06-cyber-safeguard | Challenger loop2 Finding #3; PRD §6.1 R-06 |
| frontmatter-only-prose-skim | Fresh-challenger F-C-08 priority #3 |
| overpressure-audit | PRD REQ-06 AC-06.2 (Architect deferred DX-M5) |
| contributing-4-7-note | Galadriel on-ramp P-2 |
| migration-guide-stub | Galadriel on-ramp P-1 |
| 4-7-example-skill-designation | Galadriel on-ramp P-4 |

## Notes

- `gh` auth was active (account P47Phoenix, token scopes include `repo`). No auth-failure fallback was needed.
- Issues were created in the authorized upstream (`P47Phoenix/Claude-Plugins`) per user config (`github.create_issues: true`).
- Issue numbers are sequential #77–#85, suggesting no concurrent issue creation during the run.
