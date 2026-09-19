# Architect DoD Review: Idea Stage (PR #88 CI fixes)

Role: Solution | Task: dod-validation | Reviewed: `.delivery/artifacts/01-idea/po/idea-brief.md`
All commands run from the worktree root.

## Criteria

| # | Criterion | Result |
|---|-----------|--------|
| 1 | Feasibility: Fix A (move Step 4/5 dispatch text to references/, meet 500-line budget, no behavior change) | PASS |
| 2 | Feasibility: Fix B (`claude-sonnet-4-5` to `claude-sonnet-4-6` in smoke-test doc is safe) | PASS |
| 3 | No obvious blockers or hidden dependencies | PASS (with two notes) |

## Evidence

### 1. Fix A: PASS
- `python3 scripts/check_skill_budgets.py` reproduces `BUDGET VIOLATION: delivery-flow/SKILL.md 514/500 lines (Tier-A)`.
- `git diff origin/main...HEAD` on SKILL.md: 18 insertions, 3 deletions. Step 4 gains a role-agent-first paragraph and an orchestrator hand-off paragraph. Step 5 gains a 3-line "same rule" addendum. All of it is self-contained prose, so it can be moved verbatim.
- Main is 499 lines, so 1 net line of headroom exists. Moving about 15 lines into a reference and leaving a 1-line pointer gives about 500 lines, which is at the cap and passes (cap is inclusive: the violation is reported only above 500). Tightening one other line is cheap insurance.
- `references/` holds 30+ files and `manifest.yml` indexes them (`file` + `purpose` entries). A new `references/role-agent-dispatch.md` fits the Level-3 convention. Register it in `manifest.yml`.
- Behavior risk: the Step 4 text says "Required fields either way", which refers to the field list that stays in SKILL.md. The moved paragraph must be reworded minimally or the pointer must keep that sentence in place. Keep the fallback sentence ("fall back to the Agent Invocation Template") in the pointer, because it is the load-bearing instruction. This is an authoring detail, not a blocker.
- `delivery-team/agents/` contains all 10 role agents plus `delivery-orchestrator.md`, matching the list in the moved text.

### 2. Fix B: PASS
- Guard pipeline reproduced with `/usr/bin/grep` (see note 1). Exactly one hit: `delivery-team/architecture/smoke-test-architecture.md:116`. Nothing else in the tracked tree.
- Simulated the edit (sed to a stream, not applied): the same pipeline yields zero hits, so the guard goes clean.
- Consumers of that string: `grep -rn "sonnet-4-5"` outside `.delivery/` finds only line 116 and a `#` provenance comment in `agent_registry.py` (already exempt). `smoke-test-architecture.md` is referenced only by `delivery-team/tests/smoke/README.md` (prose links, lines 79 and 160). `model_usage` is consumed by `tests/smoke/lib/metrics.py` and `report.py`, which key on the runtime model string from the run and read no fixture from this doc. No test, fixture or JSON schema pins the value.
- `claude-sonnet-4-6` is on the workflow allowlist. The JSON line does not start with `#` or `>`, so a provenance comment is not viable; the value swap is correct.

### 3. Blockers and notes: PASS
1. The `grep` in this shell is `ugrep`, and it rejects `\b` in the guard's `grep -vE 'claude-sonnet-4-6(\b|[^0-9-])'`. My first run errored. The Developer DoD must use `/usr/bin/grep` or the CI-equivalent GNU grep, or the local guard run will produce false results. Do not conclude "clean" from an errored pipeline.
2. The stale-id-guard workflow path filter excludes `.delivery/**` but the local pipeline also excludes it via `':!:.delivery/*'`; matching, no action.

## Verdict
PASS. Both fixes are feasible with no behavior change. Recommended for Plan: new `references/role-agent-dispatch.md`, 1-line pointer in Step 4 (plus Step 5 folded into it or reduced to zero net), register in `manifest.yml`, re-run budget check and the guard with GNU grep.
