# Challenger loop 2: BACKLOG-108 Stage 4 architecture

Reviewer: fresh adversarial challenger. Scope: architecture.md + ADR-lmr-001..005 as on disk. Attack surfaces 1-8 from the brief. Not all sections received equal depth (see "Coverage and limits").

## Findings

### F1 (testability, minor): gate step 2 exit-code contradiction
ADR-lmr-005 item 8 says "any non-zero exit stops the ship" and step 2 requires `git ls-files -v | grep -c '^[a-zS]'` to print `0`. Evidence:
```
$ git ls-files -v | grep -c '^[a-zS]'
0
exit=1
```
`grep -c` exits 1 when the count is 0, i.e. in the CLEAN case. An exit-status-driven executor stops the ship on a healthy tree; a reader who works around it may drop the check. Required fix: rewrite as `! git ls-files -v | grep -q '^[a-zS]'` (or `test "$(... | grep -c ... || true)" = 0`), and state that the S7 log records printed values for count commands.

### F2 (security, significant): NO-PR direct push is detect-and-fix-forward, not prevent
Prevention controls are bypassable by the pusher: `.githooks/pre-push` is opt-in via `core.hooksPath` and skipped by `--no-verify` (ADR-005 says so); the S7 gate is run by the same orchestrator that pushes; manifests are self-produced text files. The only non-pusher control, S7b, runs AFTER `git push origin main`; the `push: main` workflow (ADR-002 D7) is also post-push. Construction: commit a pin in a `.py` file, push with `--no-verify` (or hooksPath unset), skipping the gate; only S7b or CI notice, with the violation already on main. Design is honest about fix-forward but calls the gate a "control". Required fix: state explicitly in architecture.md and ADR-005 that this is detection for a careless or hostile pusher, record prevention (branch protection / server-side hook) as accepted residual risk with an owner. Not blocking: threat model is drift, not adversary.

### F3 (coupling, minor): guard scope misses extensionless tracked executables
D3 filters to `.py .md .yml .yaml .txt .sh`. Tracked files outside it (excluding `.delivery/`): 17 `.json`, `Makefile`, `.githooks/pre-commit`, `.gitattributes`, `.example`, `.jsonl`. I grepped json/toml/js/ts/html for `claude-(opus|sonnet|haiku)-[0-9]|opus-4|sonnet-4`: no hits today, so no current false negative. But `Makefile` and `.githooks/pre-commit` are executable code, and a pin there passes every gate. Required fix: add `Makefile` and `.githooks/*` to scope or name them in the declared out-of-scope list with a reason.

### F4 (docs, minor): alias set includes `fable`
Live sub-agents page: `model` accepts `sonnet`, `opus`, `haiku`, `fable`, a full ID, or `inherit`. I found no hard-coded enumeration excluding `fable` in what I read. Required fix: when MODEL_TIER_ALIAS is defined, state whether `fable` is intentionally excluded.

### F5 (docs, minor): `model_awareness` semantics vs value `latest`
Repo-wide readers/definers beyond SKILL.md stamps: `.github/workflows/skill-md-header-warn.yml` lines 21-35 (presence-only check, survives `latest`), `prompt-engineer/SKILL.md` lines 420-422 (defines `model_awareness` as "the model generation the skill was authored or last re-audited against"), `delivery-flow/SKILL.md:491`. That definition contradicts a `latest` stamp semantically. Required fix: ADR-003 must update or declare consistent the prompt-engineer/SKILL.md:420 wording.

No blocking findings.

## Verified correct (commands run)
- ADR-001: whole-file sha256 of delivery-flow/SKILL.md equals `governance/cache-prefix-hash.txt` (`43067c9e...b8328`). 499 lines, 28,616 bytes. `head -c 2048 | sha256sum | cut -c1-8` = `8c2ebf97`. `grep -rIln` consumers: telemetry.py (only code), telemetry-schema.md, SKILL.md, fitness-review.md, CHANGELOG.md, two stale artifacts. Matches ADR. Did not re-run the 25-file scratch simulation.
- `python3 scripts/check_skill_budgets.py` -> `BUDGET CHECK PASSED: 17 file(s) checked, 0 known-debt, 0 exception(s).` Did not re-simulate edits; line-neutral claims taken from ADR's own runs.
- ADR-004 vs code: `lib/metrics.py` reads top-level `model`/`usage`, buckets missing as `"unknown"` (line 117), event types `assistant|message|tool_use|result` (line 86); `runner.py::_build_claude_command` takes no model/effort/cap; `run_smoke.py` exit codes 0/1/2/3/4, `--cost-cap` default 3.00. Matches the ADR's defect description.
- ADR-005: clean-tree, not-behind, pushed-sha==HEAD, S7b fresh clone by a different role are coherent for accidental drift. Producer-validator separation proves distinct dispatch ids, not that commands were run; ADR states this limit.

## Class summary
| Class | Blocking | Significant | Minor |
|---|---|---|---|
| security | 0 | 1 (F2) | 0 |
| testability | 0 | 0 | 1 (F1) |
| coupling | 0 | 0 | 1 (F3) |
| docs | 0 | 0 | 2 (F4, F5) |

## Doc re-fetch
| URL | Claim | Live page | Verdict |
|---|---|---|---|
| https://code.claude.com/docs/en/model-config | high default except Opus 4.7; xhigh default on Opus 4.7 | "The default on every model except Opus 4.7" / "The default on Opus 4.7" | MATCH |
| https://code.claude.com/docs/en/model-config | aliases resolve to recommended version, update over time | "Aliases point to the recommended version for your provider and update over time." (resolution differs per provider) | MATCH |
| https://code.claude.com/docs/en/headless | system/init reports model; subagent msgs carry non-null parent_tool_use_id | "The `system/init` event reports session metadata including the model, tools, MCP servers, and loaded plugins." / "`parent_tool_use_id` field is the ID of the tool call that spawned the subagent. Messages from the main conversation carry `null`" | MATCH |
| https://code.claude.com/docs/en/headless | json output has total_cost_usd + per-model breakdown | "includes `total_cost_usd` and a per-model cost breakdown ... client-side estimates" | MATCH |
| https://code.claude.com/docs/en/sub-agents | `model:` accepted values | "`sonnet`, `opus`, `haiku`, `fable`, a full model ID such as `claude-opus-5`, or `inherit`" | MATCH (fable noted, F4) |

`--max-budget-usd` and `message.id` not in the headless page text retrieved; ADR-004 marks both UNVERIFIED, consistent.

## Coverage and limits
Read in full: ADR-001. Targeted extracts: ADR-002 (D1-D9), ADR-004, ADR-005 (items 7, 8, 40-41, 55, 61). NOT deeply attacked: architecture.md PRD-conflict/Plan-carry lists (surface 7), S1..S7 parallelism ordering, repo-wide `model:` frontmatter sweep. No contradiction surfaced in sampled parts; that is absence of evidence for the rest.

## Confidence: 4/5
Ready for Plan. One significant residual-risk documentation item, four minor. Lowered from 5 because surfaces 6-7 were sampled.
