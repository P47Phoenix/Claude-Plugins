# Adversarial Review — PRD rev 1 (Opus 4.6 → 4.7 Skill Update Plan)

**Artifact:** `.delivery/artifacts/02-refine/challenger/loop2/review.md`
**Reviewer:** Fresh adversarial reviewer (iteration 2 — no knowledge of prior reviews)
**Date:** 2026-04-20
**Input PRD:** `.delivery/artifacts/02-refine/po/prd.md` (rev 1, 577 lines)
**Input baseline:** `.delivery/artifacts/02-refine/data/scope-baseline.md` (Elrond / Data Analyst)

---

## TL;DR

1. Load-bearing Anthropic citations (context window, pricing, breaking-change 400s, retirement dates, tokeniser range, adaptive-thinking default-off, interleaved-thinking-no-beta-header, prompt-cache specs) spot-check **match exactly**. Numbers and verbatim quotes reproduce the source pages on 2026-04-20.
2. The PRD is an unusually disciplined plan-only document — testable ACs, concrete grep commands, non-binding sizing hints kept out of ACs, explicit baseline-capture REQ-10 to unblock all delta metrics, explicit non-goals that foreclose scope creep.
3. Remaining concerns are tactical (one Sonnet-dated ID that M-02's regex misses post-sweep; one scope ambiguity around `prompt-engineer/SKILL.md` — keystone prose-read listed in REQ-02 but REQ-02 does not *require* its edits, so the AC-02.2 sub-requirement bears the edit weight alone). None rise to the level that blocks the Architect.

## Confidence Score: **4 / 5**

**Justification:** every citation I spot-checked matched. Every inventory line I verified in the repo (three model-ID sites in `agent_registry.py` at exactly lines 148/172/187, seven alias lines in `stage_definitions.py` at exactly the seven line numbers listed) matched. The PRD correctly re-scored MID-03 after discovering zero Anthropic SDK imports — that's a self-correction the rev-1 changelog documents honestly. REQ-09 (AS-IS validator-dispatch count) and REQ-10 (baseline capture) are well-placed closures of real gaps. The six-file keystone set is properly justified on both API-shape and behavioural grounds. I dropped one point for a small set of tactical gaps listed below — worth a light rev-2 touch if desired but not blocking the Architect. **Proceed.**

---

## Findings Table

| # | Category | Finding | Blast Radius | Fix |
|---:|---|---|---|---|
| 1 | Testability | **M-02 regex under-specifies "regression guard."** The command `grep -rnE 'claude-opus-4-6\|claude-sonnet-4-5-20250929'` will not catch regressions like `claude-sonnet-4-5` (alias form), `claude-haiku-4-20250514` (MID-02's own string — never a real Anthropic ID but still should not re-enter), or any *new* dated legacy ID. M-01's complement-of-allowlist regex is stronger; M-02 could borrow that shape. | Low — guard is a backstop, not a primary gate | Rev M-02 to use the M-01 regex (dated-ID wildcard minus the Haiku 4.5 allowlist) applied after sweep. Keep M-02 as the "re-entry" sentinel but use the structural regex, not the literal-string alternation. |
| 2 | Scope clarity | **REQ-02 AC-02.3 adds a product-delivery-specific clause but no equivalent for `architect/SKILL.md` or `mtg-commander/SKILL.md`.** The rev-1 upgrade correctly brought all six files into the keystone set, but the file-specific ACs only cover `prompt-engineer` (AC-02.2) and `product-delivery` (AC-02.3). `architect/` (667 LOC), `mtg-commander/` (1181 LOC), `research-agent/` (handled in REQ-03B), `delivery-flow/` (handled in REQ-03) — only two of six have file-specific ACs. The Architect could interpret AC-02.1 as "just list them" rather than "read each one and produce recommendations." | Medium — Architect might produce a thinner audit than PO intends | Add one file-specific AC per keystone (AC-02.5 for `architect/`, AC-02.6 for `mtg-commander/`) or widen AC-02.1 to require "per-file, at minimum: which Findings to check AND at least one concrete recommendation or explicit Done-with-reason." |
| 3 | Under-scope | **No research/inventory of `architect/references/*security*` or `compliance` docs under F-22 (cyber safeguards).** R-06 acknowledges the risk but defers to REQ-02 "optionally"; no REQ actually commits to examining whether any prose in `architect/references/` could read as offensive-cyber framing and trigger refusals. This is a narrow but real 4.7 surface that the scope-baseline confirms exists (`architect/` is the largest-referent skill with compliance/security/IR sub-roles). | Low — "optional" framing in R-06 is defensible; genuine refusal risk is probably near-zero | Either (a) upgrade R-06 mitigation from "Architect may optionally" to "Architect must spot-read the three security/compliance reference docs for offensive-cyber framing; document no-change as no-change," or (b) log this as a `BACKLOG-*` candidate per REQ-07 precedent. |
| 4 | Testability | **AC-03B.2 sets gate at "≥2 WebFetch or WebSearch tool calls" — but 4.7's documented behaviour (F-07) is "fewer tool calls by default."** If the 4.7 research-agent reasons instead of fetching, the *intended* sufficient signal (hallucination-risk) triggers the gate correctly. But 2 is a very low floor; a single complex research query on 4.6 routinely used 5–10 fetches. The gate will pass even with a substantially degraded research agent that fetches only 2 sources where it would have fetched 8. | Medium — false-pass on a real regression | Either raise to ≥4 (calibrated to "demonstrably ≥2" framing in AC-03B.1 which suggests the 4.6 baseline was already higher), or pair the count with a *unique-domain* assertion (≥2 distinct hostnames fetched) so that a single-source collapse fails the gate. |
| 5 | Assumption fragility | **UV-01/UV-02 remain unvalidated** but REQ-01 AC-01.1 requires a sweep of all 10 lines regardless. That's defensible, but `prd-quality-gate-flow/stage_definitions.py`'s aliases may be *intentional* internal routing labels — removing them without understanding `flow_orchestrator.py`'s resolution could silently break local routing. The PO correctly flagged this as Architect Phase 1B, but AC-01.1 says "line number appears in a task description" — it doesn't require the Architect to gate the edit on "SDK-wire analysis first." | Medium — could cause the sweep PR to accidentally break `prd-quality-gate-flow` internal routing | Add an AC-01.5 or amend AC-01.1: "Roadmap sequences the 7 MID-04 edits behind a structural AS-IS check of `flow_orchestrator.py`. If the strings are internal routing labels, the edit is documentation/comment-only ('will need a real model ID if ever wired to SDK'). If the strings are API-bound via any indirection, the edit substitutes a current canonical ID." |
| 6 | Regression risk | **AC-04.2's concrete checklist is good, but M-04 requires "3/3 invocations pass" across ≥3 sampled invocations.** One rubric-level failure (e.g., a Challenger naming only 2 weaknesses on an ambiguous edge case) fails the whole gate. In practice, adversarial reviewers do miss the 3-weakness bar on narrow artifacts — this loop 2 review itself names six findings, well above the floor, but a thinner artifact might not support three distinct weaknesses honestly. | Low — only fires as a false-fail on small artifacts | Soften to "≥2 of 3 invocations pass" OR keep 3/3 but add an escape hatch: "if an invocation has <3 weaknesses because the input is small, Challenger documents that explicitly and the invocation counts as pass." |
| 7 | Over-scope (none) | **No over-scope findings.** The PRD's Section 1 Non-Goals, Section 7 Constraints, REQ-07's NEW-BACKLOG discipline, and Constraint 8 "plan-only terminus" collectively hold the line. REQ-10 (baseline capture) is the closest thing to an expansion, and it's correctly scoped to the implementation run, not this engagement. | — | — |
| 8 | Research gap | **NDOC-01 (Claude Code release notes) is fair to defer, but NDOC-02 (SKILL.md frontmatter contract changes on 4.7) is potentially load-bearing** — if the Skill tool's SKILL.md discovery or frontmatter validation changed silently, every plugin in this repo is affected. The PRD defers this to a "narrow follow-up research task" if Architect's inventory surfaces schema-sensitive patterns. That's reactive; a one-fetch proactive check would close the gap cheaply. | Medium — all 17 SKILL.md files could be affected if frontmatter contract changed | Add a pre-Architect research spike: WebFetch `https://docs.claude.com/en/docs/claude-code/plugins` (or equivalent) and the current SKILL.md frontmatter reference page; if unchanged from what the repo uses, record "NDOC-02 closed, no change." If changed, escalate. |

---

## Citation Spot-Check

| URL | PRD claim (quote or paraphrase) | Source verdict |
|---|---|---|
| `https://platform.claude.com/docs/en/about-claude/models/overview` | `claude-opus-4-7` is the canonical Opus 4.7 API ID; Sonnet 4.6 ID is `claude-sonnet-4-6`; Haiku 4.5 dated ID is `claude-haiku-4-5-20251001` and context is 200k. (F-01, F-03, F-06) | **Match** — "Claude API ID: claude-opus-4-7", "claude-sonnet-4-6", "claude-haiku-4-5-20251001", "200k tokens" all verbatim in the Latest models comparison table. |
| `https://platform.claude.com/docs/en/about-claude/models/overview` (Legacy table warning) | Opus 4 (`claude-opus-4-20250514`) and Sonnet 4 retire **June 15, 2026**; Haiku 3 retired **April 19, 2026**. (F-04) | **Match** — Warning block quotes both dates exactly. PRD's characterisation that Haiku 3 retired "yesterday" (run date 2026-04-20, retirement 2026-04-19) is correct. |
| `https://platform.claude.com/docs/en/about-claude/models/migration-guide` | Opus 4.7 provides "a 1M context window at standard API pricing with no long-context premium." (F-05) | **Match** — verbatim in the "Updated token counting" section. |
| `https://platform.claude.com/docs/en/about-claude/models/whats-new-claude-4-7` | "Fewer tool calls by default, using reasoning more. Raising effort increases tool usage." (F-07) and "Fewer subagents spawned by default. Steerable through prompting." (F-08) | **Match** — both bullets appear verbatim under "Behavior changes." PRD quotes are precise. |
| `https://platform.claude.com/docs/en/about-claude/models/whats-new-claude-4-7` | `thinking: {"type": "enabled", "budget_tokens": N}` returns a 400 error on 4.7. (F-11) | **Match** — verbatim in "Extended thinking budgets removed" section: "Setting `thinking: {"type": "enabled", "budget_tokens": N}` will return a 400 error." |
| `https://platform.claude.com/docs/en/build-with-claude/adaptive-thinking` | Adaptive thinking is off by default on Opus 4.7; automatic interleaved thinking without `interleaved-thinking-2025-05-14` beta header; switching modes breaks message cache breakpoints. (F-12, F-14, F-17) | **Match** — all three statements verbatim on the adaptive thinking page. |
| `https://platform.claude.com/docs/en/build-with-claude/prompt-caching` | Opus 4.7: 4096-token min, 4 cache_control breakpoints, 20-block lookback, 5-min / 1-hour TTL. (F-16) | **Match** — all four numeric specs verbatim on the prompt caching page, plus pricing confirmed ($5/$25 input/output, $6.25 / $10 / $0.50 caching). |
| `https://platform.claude.com/docs/en/about-claude/models/whats-new-claude-4-7` | Tokeniser uses "roughly 1x to 1.35x as many tokens … up to ~35% more." (F-21) | **Match** — verbatim in "Updated token counting" section. |

**All 8 spot-checked sources matched.** I found no fabricated citations, no URL-quote mismatches, no stale numbers.

---

## Closing — Top 3 Remaining Concerns

Confidence 4/5 → the PRD is ready for the Architect, but three items are worth addressing either in a light rev-2 or absorbed into the Architect's Phase 1A scope:

1. **Finding #5 (UV-01/UV-02 sequencing):** AC-01.1 should gate the MID-04 sweep on a structural AS-IS check of `flow_orchestrator.py` to avoid the sweep PR accidentally breaking internal routing. This is the highest-blast-radius tactical gap — accidentally removing a label that `flow_orchestrator.py` dispatches on would be a real regression.
2. **Finding #2 (keystone per-file ACs incomplete):** REQ-02 has file-specific ACs for `prompt-engineer` and `product-delivery` but not for the other four keystones. The Architect could produce a thin audit that satisfies AC-02.1's letter without satisfying its spirit. Add one AC per keystone or tighten AC-02.1 to require per-file outputs.
3. **Finding #4 (AC-03B.2 floor too low):** "≥2 WebFetch/WebSearch" is lax given F-07's documented "fewer tool calls" regression direction. Pair the count with a unique-domain assertion (≥2 distinct hostnames) or raise to ≥4.

None of these require rework. The Architect can absorb all three into Phase 1A without further PO intake.

**Verdict:** STATUS = DONE.

— End of fresh adversarial review, iteration 2.
