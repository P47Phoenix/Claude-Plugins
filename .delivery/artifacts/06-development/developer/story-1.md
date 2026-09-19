SKILL_LOADED: delivery-team:developer

# Story 1 notes: delivery-flow SKILL.md under Tier-A budget

## Changes
- delivery-flow/SKILL.md: 514 -> 497 lines. Step 4 first paragraph and delivery-orchestrator hand-off moved out; Step 4 now has a 2-line pointer ("prefer the matching delivery-<role> agent via Agent tool, else fall back to the inline Agent Invocation Template", names delivery-orchestrator and references/role-agent-dispatch.md). Step 5 sentence replaced by "Role-agent-first rule as Step 4: prefer delivery-<role> agents (pointer)". PROSE STYLE paragraph, signal block, Verify signal untouched.
- New references/role-agent-dispatch.md: moved text verbatim (only hard-wrap of Step 5 sentence and "Agent Invocation Template" joined onto one line).
- references/manifest.yml: added role-agent-dispatch.md entry.
- Count claims: SKILL.md "22 files" and manifest self-entry "22 entries" changed to 24 (actual entry count was already 23 before this change, so claim had drifted; now accurate).

## AC results (run)
- AC-1.1 `python3 scripts/check_skill_budgets.py; echo $?` -> "BUDGET CHECK PASSED: 17 file(s) checked, 0 known-debt, 0 exception(s)." EXIT 0
- AC-1.2 wc -l = 497
- AC-1.3 ok
- AC-1.4 SKILL.md count 2; manifest.yml count 1 (a duplicate entry from an earlier edit was found and removed; manifest now has 24 `- file:` entries, matching the updated claim).
- AC-1.5 counts in new file: delivery-developer 1, delivery-presentation 1, delivery-alias-creator 1, delivery-orchestrator 2, Agent Invocation Template 1, role-agent-first 2. Whitespace-normalized comparison against HEAD SKILL.md text: True for para 1, hand-off, Step 5 sentence.
- AC-1.6 "prefer" appears on Step 4 (line 335) and Step 5 (line 368).
- AC-1.7 no KNOWN_DEBT; git diff on governance/ empty.
- AC-1.8 lint_known_debt.py: "LINT OK", exit 0. header-warn command lists 9 SKILL.md files lacking model_awareness (user-feedback personas x4, research-types x5); none are files I touched or added (delivery-flow SKILL.md has the header). Pre-existing, no new warnings.
- TC-1.3 lines 1-332 identical to HEAD (prefix-same).
- TC-1.5 delivery-orchestrator still mentioned in SKILL.md Step 4 pointer.
- TC-1.7 yaml.safe_load(manifest.yml) FAILS at line 49 (git-integration.md purpose has an unquoted colon). Verified identical failure on HEAD version: pre-existing, not introduced here. Not fixed (out of scope).
- TC-2.4 stale-id: new file has 0 4.x model IDs.
