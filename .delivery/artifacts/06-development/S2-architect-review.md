---
run: run-2026-05-28-o48m
story: S2 (keystone prose), AC-2.3b
role: architect (adversarial reviewer / DoD validator)
commits: 31ae759, 1e36eb2
date: 2026-09-20
verdict: S2_ARCH NOT_DONE
---

# S2 architect review

SKILL_LOADED: delivery-team:architect

## Verdict

`S2_ARCH: NOT_DONE`. Blocking: 1. One claim CONTRADICTED by live docs (`extended_thinking: { "effort" }`).

## 1. Independent doc re-fetch (WebFetch, all succeeded)

| # | Claim in edits | Result | Source quote |
|---|---|---|---|
| i | Latest Opus delegates to subagents more readily (doctrine, flow SKILL, PE line ~361) | VERIFIED | prompting-claude-opus-5 "Controlling subagent spawning": "Claude Opus 5 delegates to subagents more readily than prior models." Also "give explicit guidance on which scenarios warrant delegation, or set deterministic caps". URL: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5 |
| i-b | Explicit re-verification instructions cause over-verification; drop them | VERIFIED | Same page, "Task scope and over-verification": "instructions like these cause over-verification on Claude Opus 5, and removing them reduces wasted tokens with no loss in quality." |
| ii-a | Adaptive thinking is thinking-on mode of latest Opus; do not emit `budget_tokens` | VERIFIED | best-practices page: "On Claude 4.7 and later models, setting `budget_tokens` returns a 400 error." Models overview: Opus 5 Thinking = "Adaptive"; extended "not accepted on later models". |
| ii-b | Prefer `extended_thinking: { "effort": "<level>" }` (PE line 351) | CONTRADICTED | thinking-steering-and-cost: "Effort is set at `output_config.effort`, not inside the `thinking` object". effort page: `Set output_config.effort on the request`. No `extended_thinking` param exists in docs. Claim pre-dates S2 (was in 4.7 text) but S2 re-wrote the line and kept it as fact. |
| iii-a | Effort values `low/medium/high/xhigh/max` | VERIFIED (caveat) | effort page: five levels. Caveat: "Not every model that supports `max` supports `xhigh`" (Haiku/Sonnet 4.6 lack it). Line says valid values with no caveat; ok for "latest Opus". |
| iii-b | Removal of "xhigh recommended default"; "start from the API default" | VERIFIED | effort page, Opus 5: "Start with `high`, the default" and "The API default is `high`." Opus 4.7/4.8 said xhigh, so old text was wrong for latest Opus. |
| iii-c | Levels recalibrated between releases; do not copy per-model level | VERIFIED (inference) | Opus 5: "If you carried effort settings over from an earlier model, run a fresh effort sweep on your evals rather than reusing them." |
| iii-d | API has no evergreen "latest" alias for current models | VERIFIED (inference) | Models overview: "Every Claude model ID is a pinned snapshot, including the dateless IDs"; alias row repeats `claude-opus-5` etc.; no `latest` alias listed. Absence-based, not an explicit "there is no latest alias" sentence. |
| iv | Sampling: "do NOT raise temperature for agentic tool-use or code generation"; "re-test `temperature: 0`"; "treat API defaults as baseline" | NOT VERIFIABLE | Grepped best-practices page and Opus 5 prompting page: no temperature/top_p text. Written as prescriptive fact ("do NOT"). Not a factual API claim; classed warning, see W1. |
| v | "Serving infrastructure ... can change over time, so behaviour under a fixed ID is not a permanent guarantee" (PE Pattern 4.1) | NOT VERIFIABLE | Nothing in fetched pages. Soft hedge; warning W2. |
| vi | `high` = "deeper reasoning for multi-step agentic skill work" | VERIFIED | effort table: high = "Complex reasoning, difficult coding problems, agentic tasks". |

## 2. Adversarial diff read

- Hard-pinned versions in prose: none left in the 3 files' prose (grep `opus 4`, `4.7`, `claude-opus`, `F-08`, `xhigh` prose). Remaining `opus-4-7` / `4-7-1` are frontmatter stamps (line 5/7/9 in the three SKILL.md), S3-owned. OK.
- PE lines 413-417 (Pattern 4.6): the YAML example still shows `model_awareness: opus-4-7` while the bullet below says the stamp is `latest`. Self-inconsistent until S3. Warning W3 (S3 must update the example block too, else AC-3 grep on the example may fail).
- Dangling refs: `Phase 4`, `dod_validators.<stage>`, `Model-specific optimisation` heading cross-refs (Pattern 4.3, 4.5) all match the renamed heading. No dangling refs found. F-xx cites retained; fine.
- Budget/structure: `wc -l` delivery-flow 499 (<= 500 Tier A), prompt-engineer 520. Block 2 still 4 lines. PE Tier: pre-existing 520; diff is net line-neutral (35 changed each way); no growth. OK.
- Block 2 vs ADR-lmr-005 / plan D13: text matches architecture.md lines 127-128 exactly. Contains `dod_validators`, cap word ("cap", "at most"), `subagents`. "per DoD checkpoint" and "MUST NOT exceed" present; "MUST equal" dropped. Devops already ran AC-2.5 regexes true. PASS.
- Doctrine block: reads "fusion is the highest-confidence regression mode" and also "over-spawning" breaks it; consistent with flow block. The Opus-5-specific claim "under-dispatch" was flipped to over-delegation; matches docs. PASS.
- PE line 361 "state the delegation scope and a spawn cap": matches docs advice. PASS.

## Blocking issues

B1. `prompt-engineer/SKILL.md` line 351: "Prefer `extended_thinking: { "effort": "<level>" }`" is CONTRADICTED. Effort lives at `output_config.effort`; there is no `extended_thinking.effort`. Fix: `output_config: { "effort": "<level>" }` with `thinking: { "type": "adaptive" }`. (Also check `Pattern 4.2`/other spots for the same wrong shape; grep showed only line 351 plus delivery-flow frontmatter key `extended_thinking: false`, which is a repo-local flag, not an API param.)

## Warnings

- W1. Sampling guidance (line 359) is unsourced; soften to "in our experience" or drop "do NOT"; or cite. Not blocking (advice, not API fact).
- W2. Pattern 4.1 infra-change hedge unsourced; acceptable as hedge, consider removing.
- W3. PE Pattern 4.6 YAML example still `opus-4-7` (S3).
- W4. `xhigh` not available on every model; add "on models that support it" if the block is ever used beyond latest Opus.
- W5. No-evergreen-alias claim is inferred from absence; phrase as "the models overview lists only pinned IDs" if exactness wanted.

## 3. Ledger verdicts (3-file prose review)

| Row | Verdict | Reason |
|---|---|---|
| delivery-team/skills/delivery-flow/SKILL.md | REVIEWED_CHANGED | Two model-awareness blocks made family-relative and Opus-5-correct (over-delegation, cap by dod_validators); 499 lines held; claims verified vs docs. |
| prompt-engineer/SKILL.md | REVIEWED_CHANGED | Version-free latest-Opus guidance and Pattern 4.1 config-sourced ID; verdict conditional on fixing B1 (`extended_thinking.effort` contradicted) before DoD. |
| delivery-team/skills/product-delivery/SKILL.md | NO_CHANGE_NEEDED | Confirmed by own grep: only mentions are stamp lines 5 and 7 (S3-owned) and `phase_1_detector_model: haiku` (family alias, not a version); prose has no model/version claims. |

Also changed and covered: delivery-team/references/shared/orchestrator-doctrine.md (REVIEWED_CHANGED, block renamed "latest Opus", verified).

## Evidence

- `git show 31ae759 1e36eb2`; `wc -l` 499 / 520.
- WebFetch OK: platform.claude.com/docs/en/build-with-claude/prompt-engineering/{claude-prompting-best-practices,prompting-claude-opus-5}, /build-with-claude/effort, /build-with-claude/thinking-steering-and-cost, /docs/en/about-claude/models/overview.
- Note: `.delivery/artifacts/06-development/S2-tech-writer-review.md` and `dispatch-manifest-S2.txt` untracked by others; not touched. Nothing committed by this review.
