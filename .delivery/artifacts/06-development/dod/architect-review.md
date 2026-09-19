# Architect DoD Review: role-agent-dispatch extraction

Verdict: PASS (5/5), one non-blocking note.

| # | Criterion | Result | Evidence |
|---|-----------|--------|----------|
| 1 | Three-level loading | PASS | New file is level-3 resource in references/. SKILL.md keeps 2-line pointer in Step 4 and Step 5. Content moved verbatim. |
| 2 | Cache-prefix / Volatile rules | PASS | No check script exists that verifies the hash. Direct check: first 2048 bytes of SKILL.md sha256 8c2ebf97... identical to HEAD (and 2047/2049 differ, so boundary test is sensitive). Edits are in Phase 4 (~line 332+), well past Phase 3 end (~249). |
| 3 | One Role = One Sub-Agent | PASS | Heading at line 253 untouched; changed hunks only Step 4/5/459. |
| 4 | manifest.yml entry | PASS | Same `- file:` / `purpose:` shape as siblings (folded `>` used by others). Line 49 YAML error (unquoted colon in purpose) is identical on origin/main (col 29). New entry adds no second error: parse fails at line 49 in both. Count 23 -> 24 entries; self-entry text updated to 24. |
| 5 | PR #88 semantics | PASS | "Prefer delivery-<role> agent, else inline Agent Invocation Template" preserved in SKILL.md Step 4 and full text in reference; orchestrator hand-off and required fields kept; Step 5 rule kept. |

## Reference-count docs
- SKILL.md line 459 updated 22 -> 24 files (matches actual 24 manifest entries; main text said 22 but had 23, so old count was already stale).
- No other "22 files/entries" refs found outside .delivery artifacts.

## Notes (non-blocking)
- governance/cache-prefix-hash.txt holds sha256 43067c9e... of whole SKILL.md, matching neither HEAD (f3e626e5) nor working tree (0a7a92f4). Stale before this change; not a regression. Whole-file hash would need regeneration only if policy is whole-file; prefix bytes are unchanged.
- Pre-existing manifest line 49 YAML error should be fixed separately (quote or use `>` on purpose).
- Step 4 pointer text in SKILL.md is terse; acceptable.
