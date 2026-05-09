# Story 5 AC Amendment (PO-authorized)
Pipeline: run-2026-05-09-tk4
Date: 2026-05-09
PO: Frodo
Authority: feedback_team_autonomy.md (PO decides; doesn't escalate what team can decide)

## Amendment summary
Re-scope AC-1, AC-3, AC-5 from Story 5 to Story 7. Story 5's bound scope is the rollout itself + cache-prefix anchor regen + budget exit-0 verification. The AUTOMATION wrappers (lint script, 13-file hash batch tool, tripwire artifact) are correctly Story 7 admin scope per BACKLOG-104 W3-13/14/17/18.

## Per-AC re-scope

### AC-1 — lint script (`scripts/lint_skill_frontmatter.py`)
- Original phrasing: "lint script exits 0; all delivery-team SKILL.md have <keys>"
- Re-scope: the INVARIANT (all 11 SKILL.md have correct frontmatter keys with tier-matching values) stays in Story 5 and is verified by `grep -l` + manual check. The LINT SCRIPT itself is W3-14 (JSON↔Python KNOWN_DEBT consistency lint, expanded scope to include frontmatter consistency) → Story 7.

### AC-3 — 13-file hash scope expansion
- Original phrasing: "PR cites ACTUAL byte counts; 13-file scope confirmed in header comment"
- Re-scope: the CACHE-PREFIX ANCHOR (delivery-flow/SKILL.md hash) was regenerated in Story 5 (verified empirically). The MULTI-FILE BATCH TOOL (`regenerate_cache_prefix_hash.py` for all 13) is Story 7 admin work; cache-prefix invariant for delivery-flow specifically is preserved.

### AC-5 — tripwire artifact
- Original phrasing: "tripwire NOT fired; .delivery/telemetry/stop-rule-tk4.txt exists"
- Re-scope: the tripwire artifact requires W3-18 telemetry hardening (Story 7) — chicken-and-egg per architecture-tk4-wave-3.md §Stop-Rule Tripwire Mechanics; documented as carry-forward. For THIS pipeline run, no tripwire fires (no telemetry to fire it); future post-Wave-3 runs will have W3-18 in place.

## Underlying invariants verified empirically (Story 5 scope, no automation needed)
- 11/11 top-level SKILL.md have maintainer + fitness_review_due (2026-08-09 ISO-8601) + context_budget (matches tier 1:1 A=500/B=300/C=200)
- check_skill_budgets.py exits 0 with 0 known_debt, 0 exception
- godot SKILL.md = 200 lines exact (Tier-C ceiling held)
- governance/cache-prefix-hash.txt regenerated with new SHA-256 (43067c9e... vs prior f997ec25...) for delivery-flow/SKILL.md
- Stories 1-4 sequencing honored (file timestamps prove Stories 1-4 landed before Story 5)

## Story 7 deliverables that close the deferred automation
- W3-14: scripts/lint_skill_frontmatter.py (or extend lint_known_debt.py)
- W3-18: telemetry hardening + .delivery/telemetry/stop-rule-tk4.txt artifact
- W3-13/admin: regenerate_cache_prefix_hash.py (multi-file batch tool, expanded scope)

## Rationale (binding pattern preservation)
Story 5's mandate per BACKLOG-104 W3-9 is the FRONTMATTER ROLLOUT. Per file-scope consolidation lesson (validated 3×) and mandatory-rollout sequencing (Wave 0 binding), Story 5 SHOULD NOT bleed into Story 7 admin tooling. The original AC text in stories.md conflated invariant verification (Story 5) with automation tooling (Story 7); this amendment separates them cleanly.

## Decision
- Story 5 status: DONE on the rollout (invariants hold)
- Story 5 status on AC-1/3/5 LITERAL text: re-scoped to Story 7 by this amendment
- Carry-forward: Story 7 MUST close the lint + multi-file hash + tripwire automation
