# Challenger Review: MTG Commander Deck Builder Architecture

**Reviewer**: Challenger (Adversarial Reviewer)
**Architecture Under Review**: Architecture v1.0 + ADR-001 through ADR-004
**Date**: 2026-04-01
**Confidence in Decision**: 3 / 5

---

## Verdict

**The architecture is structurally sound but has three material risks the Architect under-analyzed.** The plugin structure follows repo conventions correctly, the ADRs are well-reasoned for v1 scope, and the pipeline design is coherent. However, the no-persistence decision, the synergy-in-context assumption, and the global correction counter each carry more risk than the architecture document acknowledges. None are fatal, but collectively they narrow the margin for error in a pipeline that already depends on LLM reliability for multi-step sequential processing.

The decision STANDS WITH CONDITIONS documented below.

---

## Challenge 1: No Disk Persistence for Deck State -- Session Loss Risk

**Architect's claim** (Section 6.4): "No disk persistence in v1. The deck state lives entirely in the conversation context. This is sufficient because the pipeline completes in a single session (G-05, NFR-07)."

**Challenge**: The architecture assumes the session will complete. But a Commander deck build pipeline is a *long* operation. Consider the sequence:

1. Intake extraction with commander validation (Scryfall call)
2. Deck Builder sub-agent builds 100 cards, validating each against Scryfall (~2 batch calls + targeted searches)
3. Rules Judge batch-validates all 100 cards (2 batch calls) + synergy audit
4. Optimization Reviewer evaluates all synergy tags
5. Price Evaluator fetches prices (2 batch calls)
6. If ANY agent returns FAIL, the Deck Builder re-runs, and the failing agent re-runs

Each sub-agent spawn loads reference files (4-6 per agent). Each Scryfall call requires a Python process spawn. A single pass through the pipeline involves 4 sub-agent spawns, 6+ Scryfall API calls, and 4-6 reference file reads. A correction cycle adds 2 more sub-agent spawns and 2-4 more API calls.

**What happens when:**
- The user's internet drops during the Price Evaluator's batch-price call?
- Claude Code hits a timeout or session limit mid-pipeline?
- The user accidentally closes their terminal after the Deck Builder finishes but before the Rules Judge runs?

In all cases, the entire deck state is lost. The user must re-run the full pipeline from scratch, including all Scryfall API calls and all sub-agent processing. There is no checkpoint.

**The Architect's mitigation** ("the structured deck state format is designed to be file-compatible if needed") is a v2 hand-wave. The format being file-compatible does not mean a file is written.

**Severity**: MODERATE. The PRD explicitly says "completes in a single session" (NFR-07), and G-05 measures "no manual user intervention between agents." The architecture is technically compliant with the PRD. But the PRD assumes the session will complete -- it does not address what happens when it does not.

**Recommendation**: Add a lightweight checkpoint after each agent completes. Write the deck state to `.delivery/artifacts/mtg-commander/deck-state.yml` (or a temp file) after each pipeline stage. This costs one `Write` tool call per stage (4 total, negligible) and enables manual recovery. The orchestrator can check for an existing checkpoint file at startup and offer to resume. This is not "multi-session workflows" (which the PRD defers) -- it is crash recovery. There is a meaningful difference.

**Impact on decision**: Does not change the plugin structure or agent design. Adds one file write per stage. Low implementation cost, high resilience value.

---

## Challenge 2: Synergy Tags in Conversation Context -- Token Budget Risk

**Architect's claim** (Section 6.4, Risk Analysis): "Deck state is ~100 entries x ~5 lines = ~500 lines. Well within window." and "100-card deck state fits comfortably in context. Estimated at ~15-20K tokens with synergy tags and rationale."

**Challenge**: The 15-20K estimate is for the deck state *alone*. Let me reconstruct the actual context budget for the heaviest sub-agent spawn:

| Content | Estimated Tokens |
|---------|-----------------|
| SKILL.md orchestrator instructions | ~3-4K |
| Agent prompt template | ~1-2K |
| `archetype-patterns.md` (18 archetypes x card categories x synergy patterns) | ~4-6K |
| `synergy-taxonomy.md` (6 categories x definitions x examples x edge cases) | ~2-3K |
| `structural-minimums.md` (4 tiers x targets) | ~1-2K |
| `intake-questions.md` (7 questions x validation rules x defaults) | ~1-2K |
| Deck state (100 cards x name + category + mana + rationale + tags + price) | ~15-20K |
| Violation list from failing agent (if correction cycle) | ~1-3K |

**Total for Deck Builder correction cycle**: ~28-40K tokens of input context.

The Deck Builder then needs to *produce* a new 100-card deck state (~15-20K tokens of output).

**Is this within limits?** Yes, for Claude's context window. But "within limits" and "reliably high quality" are different questions. As context grows, the model's attention to individual card synergy tags in the middle of a 100-card list degrades. Cards 40-70 in a list of 100 get less attention than cards 1-10 and 90-100 (the well-documented "lost in the middle" effect).

**This matters specifically for synergy tags.** The Optimization Reviewer evaluates synergy tags that the Deck Builder produced. If the Deck Builder's attention flagged for cards in the middle of the list, those cards will have weaker synergy tags, the Optimization Reviewer will flag them as isolated, and the correction cycle will fire -- consuming one of the 3 correction cycles on an attention artifact rather than a genuine quality issue.

**Severity**: MODERATE. The architecture is not wrong -- the data does fit in context. But the Architect should have analyzed the quality-at-scale risk, not just the fits-in-context risk. The PRD requires synergy score >= 3.0 across *all* non-land cards (G-02). If mid-list attention degradation causes 10-15 cards to have weak tags, the synergy score drops and correction cycles are spent on what is essentially an LLM attention problem.

**Recommendation**: Two mitigations:

1. **Instruct the Deck Builder to build in categorical blocks** rather than a flat list. Build all Ramp cards, then all Draw cards, then Removal, etc. Each block keeps related cards in proximity, improving attention to cross-block synergies.

2. **Have the Optimization Reviewer output its isolated-card list in a structured format that the correction cycle can target.** Instead of re-generating the entire 100-card deck, the correction Deck Builder should receive "keep these 85 cards, replace these 15" -- reducing the output size and focusing attention on the problem cards.

**Impact on decision**: Does not change the architecture. These are prompt engineering refinements for the agent templates in SKILL.md. But they should be documented as architectural guidance, not left for the developer to discover during implementation.

---

## Challenge 3: Python Script via Bash vs. MCP Server -- Trade-off Analysis is Correct but Incomplete

**ADR-002 Decision**: Python script via Bash tool. Rationale: no dependencies, simpler deployment, sufficient for v1 volumes, follows existing patterns.

**Challenge**: The ADR correctly identifies the trade-offs. The decision is sound for v1. However, the consequences section omits one practical issue:

**Process spawn overhead compounds in correction cycles.** Each `card_lookup.py` invocation spawns a new Python process, imports `urllib.request`, `json`, `time`, `sys`, `argparse`, and then makes HTTP requests. The import/startup overhead is ~100-200ms per invocation on typical systems. In a happy-path pipeline:

- Commander validation: 1 invocation
- Deck Builder batch validation: 2-3 invocations
- Rules Judge batch validation: 2 invocations
- Price Evaluator batch pricing: 2 invocations

That is 7-8 process spawns in the happy path. Each correction cycle adds 4-6 more. At 3 correction cycles, that is 19-26 process spawns.

**Is this a problem?** For wall-clock time, no -- the Scryfall network latency (~200-500ms per request) dominates. The process spawn overhead is noise. For Bash tool call budget, it is more relevant -- each invocation consumes a tool call, and Claude Code has practical limits on tool call density within a sub-agent.

**Severity**: LOW. The ADR's decision is correct. The process spawn overhead is negligible compared to network latency. But the ADR should have noted that the *number of tool calls* (not wall-clock time) is the binding constraint.

**Impact on decision**: NONE. ADR-002 stands.

---

## Challenge 4: No Agent Definition Files -- Maintainability at 400-600 Lines

**ADR-001 Decision**: Single SKILL.md with inline agent prompt templates. Rationale: agents are pipeline stages, not independent skills; follows existing patterns; no `agents/` directory convention in repo.

**Challenge**: The ADR acknowledges SKILL.md will be 400-600 lines and compares to delivery-flow's SKILL.md. But delivery-flow's SKILL.md is an *orchestrator* -- its sub-agent prompt templates are relatively short because the domain knowledge lives in reference files. The mtg-commander SKILL.md is also an orchestrator, but each agent template includes:

1. Role instructions (personality, constraints)
2. Reference file injection markers (the orchestrator reads and injects)
3. Tool usage instructions (how to invoke card_lookup.py)
4. Input/output format specifications (deck state format, verdict format)
5. Specific behavioral rules (e.g., Rules Judge's deterministic requirement, Optimization Reviewer's taxonomy enforcement)

Four agents x 5 sections each = 20 content blocks in a single file, plus the orchestrator logic (intake, sequencing, correction routing, output formatting, post-output actions).

**The real concern is not length -- it is cognitive load during modification.** When a developer needs to change how the Rules Judge handles double-faced cards, they must:
1. Open SKILL.md (400-600 lines)
2. Find the Rules Judge section (buried among 3 other agent templates)
3. Understand the context boundaries (what this agent sees vs. what others see)
4. Modify without accidentally affecting other agents' prompts

The ADR mitigates this with "clear section headers" and "agent behavior is primarily driven by reference files." The second point is crucial and correct -- if the reference files carry the domain knowledge, the SKILL.md templates become thin orchestration glue.

**Severity**: LOW. The ADR's analysis is sound. The mitigation (domain knowledge in reference files, thin templates in SKILL.md) is the right pattern. But the ADR should have been more explicit about what the templates contain vs. what the references contain. If templates creep toward domain knowledge, maintainability degrades.

**Recommendation**: Add an explicit constraint to the architecture: "Agent prompt templates in SKILL.md must not exceed 40 lines each. All domain knowledge resides in reference files. If a template grows beyond 40 lines, the excess content should be extracted to a reference file." This creates an enforceable boundary.

**Impact on decision**: NONE. ADR-001 stands with the template size constraint as guidance.

---

## Challenge 5: Scryfall Rate Limiting in stdlib -- Implementation Soundness

**Architecture claim** (Section 5.4): RateLimiter class using `time.monotonic()` with 75ms default delay.

**Challenge**: The rate limiter design is correct *within a single process invocation*. The `last_request_time` resets to 0 on every new process spawn. Since each `card_lookup.py` invocation is a new process (ADR-002), the rate limiter only throttles requests *within* a single CLI command (e.g., within a `batch` call that makes 2 requests for 100 cards).

**Cross-invocation rate limiting does not exist.** If the Deck Builder's `batch` call finishes and the Rules Judge immediately calls `batch`, there is no delay between the last request of the first call and the first request of the second call.

**Is this a problem?** The ADR-002 consequences section addresses this: "the natural latency of spawning a Python process provides implicit throttling" and "Scryfall's generous 10 req/s limit." Both are true. A Python process spawn takes ~100-200ms, which exceeds the 75ms rate limit. And 10 req/s is generous when the pipeline makes 7-8 calls total.

**However**, there is one scenario the architecture does not address: the `batch` command splits 100 cards into 2 requests (75 + 25). The rate limiter handles the delay between these 2 requests correctly. But if a `search` command immediately follows a `batch` command *within the same sub-agent* (e.g., the Optimization Reviewer does `batch` to validate tags, then `search` to find replacement candidates for each isolated card), the sub-agent may issue `search` calls in rapid succession -- each in its own process, each starting its rate limiter at 0.

If the Optimization Reviewer finds 5 isolated cards and searches for replacements, that is 5 rapid-fire `card_lookup.py search` invocations. With process spawn latency of ~100-200ms each, the effective rate is 5-10 req/s -- right at Scryfall's limit.

**Severity**: LOW. Even in the worst case, the rate is at the limit, not vastly exceeding it. Scryfall returns 429 with a retry-after header, and the script handles 429 with exponential backoff (Section 5.5). The system self-corrects.

**Impact on decision**: NONE. The architecture's error handling covers the edge case. But the Architect should note that rapid sequential `search` calls during replacement finding are the highest-risk scenario for rate limit hits.

---

## Challenge 6: Global Correction Counter -- Unfair Penalization Risk

**Architecture claim** (Section 6.2): "One counter for the entire pipeline run, not per-agent. If the Rules Judge uses 1 cycle and the Price Evaluator uses 2, the total is 3 (max reached)."

**Challenge**: This creates a structural bias. The pipeline is sequential: Deck Builder > Rules Judge > Optimization Reviewer > Price Evaluator. Earlier agents consume correction cycles that later agents cannot use.

**Scenario**: The Deck Builder produces a deck that passes Rules Judge (0 cycles used) and passes Optimization Reviewer (0 cycles used), but is $30 over budget. The Price Evaluator returns FAIL with 5 over-budget cards. The correction cycle replaces those 5 cards. Now the Optimization Reviewer re-checks and finds 2 of the replacement cards are isolated (< 3 synergy interactions). FAIL -- 1 cycle used. Another correction fixes the synergy but introduces a color identity violation. Rules Judge FAIL -- 2 cycles used. The correction fixes the color violation but goes over budget again. Price Evaluator FAIL -- 3 cycles used. Max reached.

In this scenario, the budget constraint cascaded into synergy and legality failures. The global counter penalizes the Price Evaluator for problems it did not cause. The deck ships with budget violations because the counter was exhausted by cascading corrections.

**Is this the Architect's fault?** Partially. The PRD mandates using the existing pipeline config mechanism (FR-07.3), and that mechanism has a single counter. The Architect correctly followed this constraint. But the architecture should have analyzed the cascade risk and proposed mitigation.

**More critically**: the correction re-entry point (Section 6.2) says "the pipeline re-enters at the agent that failed." This means after a Price Evaluator correction, the deck goes back through Rules Judge and Optimization Reviewer again. Each of those can FAIL and consume another cycle. The re-entry design amplifies the cascade problem.

**Severity**: MODERATE. The PRD's budget priority rule (FR-07.4) mitigates this by relaxing synergy thresholds when budget conflicts arise. But the priority rule only activates "if max correction cycles are exhausted." It does not prevent cycles from being consumed by cascades *before* exhaustion. A deck could use 2 cycles on cascading corrections and then get 1 genuine correction attempt.

**Recommendation**: Two options (not mutually exclusive):

1. **Apply budget priority rule *before* exhaustion.** If the Price Evaluator returns FAIL and the correction counter is at 2/3, preemptively relax synergy thresholds for budget-forced swaps. Do not wait until exhaustion.

2. **Separate the counter into "correction cycles" (modifications to the deck) and "re-validation passes" (re-running agents after corrections).** Count the modification events, not the validation events. A cascade that re-triggers Rules Judge and Optimization Reviewer after a Price Evaluator correction is 1 modification cycle, not 3.

**Impact on decision**: The first recommendation is a SKILL.md orchestration logic change -- no structural impact. The second would deviate from the existing pipeline config mechanism (FR-07.3), which the PO may reject. Both are worth discussing in the Plan stage.

---

## Summary of Findings

| # | Challenge | Severity | Impact on Architecture Decision |
|---|-----------|----------|-------------------------------|
| 1 | No disk persistence -- session loss loses all state | **Moderate** | Add lightweight checkpoint writes after each stage |
| 2 | Synergy tags in context -- mid-list attention degradation risk | **Moderate** | Add categorical block-building and targeted correction guidance |
| 3 | Python script vs. MCP -- process spawn overhead | Low | None -- ADR-002 stands |
| 4 | No agent definition files -- template maintainability | Low | Add 40-line template size constraint |
| 5 | Rate limiting across invocations | Low | None -- error handling covers the edge case |
| 6 | Global correction counter -- cascade penalization | **Moderate** | Consider early budget priority activation or counter redesign |

---

## Conditions for Acceptance

The Challenger accepts this architecture (Confidence: 3/5) with these conditions:

1. **Checkpoint writes** -- The architecture must specify that the orchestrator writes the deck state to a temp file after each pipeline stage completes. This is crash recovery, not multi-session workflow. One `Write` call per stage, zero structural changes.

2. **Categorical block-building guidance** -- The Deck Builder agent template must instruct the model to build cards in category blocks (Ramp, then Draw, then Removal, etc.) rather than a flat interleaved list. This is prompt engineering, not architecture, but it must be documented as an architectural constraint.

3. **Template size boundary** -- Agent prompt templates in SKILL.md must be capped at 40 lines each. Domain knowledge goes in reference files. This is enforceable during code review.

4. **Cascade correction analysis in Plan stage** -- The Plan stage must include a user story or spike to validate the correction cycle behavior with the 5 test cases. Specifically: test case 5 (Atraxa, $50 budget, 4 colors) is the highest cascade risk and should be used to validate that 3 correction cycles are sufficient.

If conditions 1-3 are addressed in the architecture or carried as explicit constraints into the Plan stage, the architecture is APPROVED. If any of conditions 1-3 are rejected without alternative mitigation, confidence drops to 2/5 and escalation to the human is required.

---

```
STATUS: DONE
ARTIFACT: .delivery/artifacts/04-architect/dod/challenger-review.md
CONFIDENCE: 3/5
DECISION: APPROVED WITH CONDITIONS
ESCALATION: NOT REQUIRED (contingent on conditions 1-3 being addressed)
```
