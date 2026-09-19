# PO UAT DoD Review - model literals refresh (PR #88)

Role: product-owner | Verdict: DONE (no must-fix)

## Evidence run independently
- grep of `claude-(opus|sonnet|haiku|fable)-[0-9]` outside .git/.delivery: 16 text hits (plus binary .pyc, untracked cache, ignored).
- `python3 scripts/check_skill_budgets.py`: PASSED (17 files, 0 debt, 0 exceptions).
- `git diff --stat -- . ':!.delivery'`: 7 files, +43/-31 (guard yml, CHANGELOG, agent_registry.py, smoke-test-architecture.md, telemetry-schema.md, conftest.py, prompt-engineer/SKILL.md).

## Hit classification
| Location | Class |
|---|---|
| agent_registry.py:149, 190 (sonnet-5, opus-5) | live, allowlisted |
| agent_registry.py:174 (haiku-4-5-20251001) | live, allowlisted (pinned Haiku) |
| agent_registry.py:148, 173, 189 | `#` provenance, exempt (retired IDs only in comments) |
| smoke-test-architecture.md:115-116, telemetry-schema.md:36, conftest.py:105/117/129/151, prompt-engineer/SKILL.md:368 | live, allowlisted |
| CHANGELOG.md:12-14 | doc, allowlisted IDs only (opus-5, sonnet-5, fable-5-1) |
No non-allowlisted live literal remains.

## Criteria
1. All hard-coded literals migrated: PASS. Zero stale live IDs; guard is now positive allowlist (opus-5, sonnet-5, fable-5-1, haiku-4-5-20251001), so regressions fail CI.
2. Fable 5.1 allowlisted: PASS (guard ALLOW list; CHANGELOG:13-14).
3. Fable not-adopted honestly disclosed with rationale: PASS. CHANGELOG states "allowlisted only, not adopted"; BACKLOG-112 records rationale (2x Opus 5 cost, forced tool_choice 400, always-on thinking, refusal handling, no ZDR/Priority Tier) and adoption conditions. Note: user said "we have fabel now"; not adopting is a deliberate deviation, so PR body must say so up front (non-blocking).
4. Deferred items captured with ACs: PASS. BACKLOG-109 (25 stamps, Should), BACKLOG-110 (cache-prefix-hash, Could), BACKLOG-111 (live baseline, local-only), BACKLOG-112 (Fable). ACs are checkable (stamp bumped-with-evidence or reason recorded; hash equals `sha256sum` of delivery-flow/SKILL.md or file removed). Minor: 109/110 ACs lack literal command strings; nice-to-have.
5. BACKLOG-108 handling coherent: PASS. SUPERSEDED record maps retarget, carries forward decisions, splits S3->109, S5->111, drops re-freeze->110. Caveat: original 108 file is untracked in main checkout and not edited here; owner must apply header block.
6. Residual risks prioritized, non-blocking: PASS. Release-plan risks (accidental staging, allowlist tightness) have mitigations; deferrals ranked Should/Could/Won't. Stamps stay stale until 109, honestly not bulk-bumped.
7. Budget + diff scope: PASS (see evidence).

## Non-blocking follow-ups
- State Fable decision in PR body.
- Apply 108 header block in main checkout.
- Add literal verify commands to 109/110 ACs.
