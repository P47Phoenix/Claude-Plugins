# Adversarial Challenge: Sprint Plan for MTG Commander Deck Builder

**Challenger**: Adversarial Reviewer
**Date**: 2026-04-01
**Artifacts Reviewed**: Sprint Plan v1.0 (Aragorn/SM), User Stories v1.0 (Gandalf/PO)
**Scope**: 8 user stories, 42 SP across 3 sprints, GREENFIELD plugin (Python script + prompt engineering + markdown references)

---

## Challenge 1: Sprint 2 at 22 SP When Ceiling Is 13 -- Parallelism Justification Under Scrutiny

**Confidence**: 4/5 (significant doubts)

The SM commits Sprint 2 at 138% of the 80% ceiling, arguing that 3-way parallelism of US-05/06/07 reduces the effective serial path to 13 SP. The math is correct. The assumption behind the math is not.

**Evidence**:

- The parallelism argument assumes US-05, US-06, and US-07 are truly independent. They share zero files -- true. They load different reference subsets -- true. But they all conform to the same verdict format, the same correction routing interface, and the same deck state schema defined by US-04. If US-04's output format changes during development (and 8 SP orchestrators frequently evolve during implementation), all three agents need to adapt. The "identical agent template structure" confirmed by architecture review is a design intent, not a delivered artifact. Until US-04 is complete and stable, the template structure is aspirational.

- The 80% ceiling exists to absorb unknowns. The SM explicitly acknowledges this in the Capacity section ("80% ceiling assumes serial execution") but then immediately overrides it. The ceiling is not just about serial vs. parallel -- it is about estimation uncertainty, integration friction, and the unexpected. Even with perfect parallelism, 22 SP of work in a single sprint means 22 SP of things that can go wrong. A defect in the verdict format ripples across all three agents simultaneously.

- The "effective serial path is 13 SP" framing conflates elapsed time with risk exposure. If US-05 finishes on time but US-06 discovers that the synergy counting logic requires a deck state field that US-04 did not provide, the rework affects US-04 (the serial bottleneck) and potentially US-05 and US-07 as well. Parallelism amplifies blast radius when the shared dependency (US-04) has an integration gap.

- Historical precedent from this very plan: Sprint 1 also uses parallelism (US-02 + US-03 after US-01) but only commits to 15 SP (94% ceiling). The SM was more conservative with a simpler fan-out (2-way, after a 2 SP dependency). Sprint 2 has a wider fan-out (3-way) after a more complex dependency (8 SP) but is less conservative. The risk tolerance is inverted relative to the complexity.

**What should change**: Cap Sprint 2 at 18 SP by deferring US-07 (Price Evaluator, 4 SP, the simplest of the three agents) to Sprint 3. Sprint 3 becomes 9 SP (US-07 + US-08), still well within ceiling. This preserves the 2-way parallelism of US-05 + US-06 (which is defensible -- both are validation agents with similar complexity) while eliminating the 138% ceiling violation. Alternatively, if the SM insists on 22 SP, the risk register must explicitly state: "If US-04's deck state schema changes after US-05/06/07 begin, all three agents require rework. Mitigation: freeze US-04's output interface before starting parallel work."

---

## Challenge 2: 42 SP for a GREENFIELD Plugin -- Realistic or Aggressive?

**Confidence**: 3/5 (moderate doubts)

42 SP across 3 sprints for a plugin that produces no compiled code, no database, no UI, and no infrastructure. The deliverables are: 1 Python script (stdlib HTTP client), 1 SKILL.md (prompt engineering), 3 agent prompt templates, 7 reference markdown files, and 5 dogfooding runs. Let me stress-test whether 42 SP is right-sized.

**Evidence**:

- **In favor of 42 SP**: The Python script (US-02) has 14 acceptance criteria, 6 CLI commands, rate limiting, retry logic with exponential backoff, batch splitting, double-faced card handling, and a normalized data model. This is legitimately complex stdlib Python -- no `requests`, no `httpx`, raw `urllib` with error handling. 8 SP is defensible. The orchestrator (US-04) has 19 acceptance criteria spanning intake modes, commander validation, agent sequencing, correction routing, and output assembly. 8 SP is defensible. These two stories alone are 16 SP, nearly 40% of the total.

- **Against 42 SP**: US-03 (7 reference files) at 5 SP is generous. These are markdown files containing domain knowledge. The content requires MTG expertise (or research), but the actual authoring is straightforward -- no logic, no integration, no error handling. The banned list (AC 3.2) is a copy from mtgcommander.net. The archetype patterns (AC 3.3) and structural minimums (AC 3.4) are well-documented in the MTG community. 3 SP would be more appropriate, saving 2 SP.

- **Against 42 SP**: US-05/06/07 (agent prompt templates) at 5+5+4 = 14 SP total. These are prompt templates -- markdown files with structured instructions that tell an LLM what to do. They are not code. They do not execute. The acceptance criteria describe what the agent should check, but the "implementation" is writing clear instructions. The architecture already defined the verdict format, the reference file loading pattern, and the correction routing interface. The prompt engineer is filling in a template, not designing a system. 3+3+3 = 9 SP would be more appropriate, saving 5 SP.

- **Counterpoint**: The PO's estimation rationale explicitly calls out that prompt engineering stories are estimated at a higher tier than markdown-only stories. The argument is that prompt engineering requires iterative refinement -- you write the template, test it, discover the LLM misinterprets an instruction, revise, retest. This iteration is real and unpredictable. The estimates may be accounting for this iteration overhead.

**Verdict**: The total is at the upper bound of reasonable. If the prompt engineering stories execute cleanly on first draft, the team will finish early. If they require 2-3 revision cycles each (likely for US-04), the estimates are accurate. The highest risk of inflation is US-03 (reference files) at 5 SP -- this should be 3 SP. Net adjusted total: 40 SP. Not a material difference, but the plan should not claim 42 SP is tight when 2 SP of it is padding in a markdown-only story.

---

## Challenge 3: US-02 (Scryfall Client) at 8 SP -- Right-Sized for stdlib Python HTTP?

**Confidence**: 3/5 (moderate doubts, leaning toward "it's fine")

8 SP is the highest single-story estimate in the backlog. The SM places it as the heaviest code-complexity item. Let me examine whether the complexity justifies the cost.

**Evidence**:

- **Complexity drivers that justify 8 SP**: (1) 6 CLI commands with distinct API endpoints and query patterns. (2) Rate limiting at 75ms intervals -- requires a stateful delay mechanism across calls. (3) Exponential backoff on 429 with 3 retries -- non-trivial error handling logic. (4) Batch splitting for `/cards/collection` (75-card POST limit) -- requires chunking and response merging. (5) Double-faced card handling -- name matching, oracle text combination, color identity merging. (6) Normalized data model output -- consistent JSON schema across all commands. (7) Null-price fallback chain (USD > USD foil > other printings > "unavailable"). These are genuine complexities that stdlib Python (raw `urllib.request`, manual JSON parsing) makes harder than they would be with `requests` or `httpx`.

- **Complexity drivers that argue for less**: (1) The script is stateless -- no database, no file I/O beyond stdout. (2) Each CLI command is largely independent -- `validate` does not share logic with `search` beyond the HTTP wrapper. (3) The Scryfall API is well-documented with consistent response schemas. (4) Rate limiting is a simple `time.sleep()` call between requests. (5) Error handling follows a pattern: check status code, branch on 404/422/429/5xx, retry or return. Once the pattern is established for one command, the others follow.

- **Comparison benchmark**: A similar stdlib Python HTTP client with rate limiting and retry logic is typically a 200-300 line script. With 6 commands and the batch splitting logic, this is likely 400-500 lines. At 8 SP, this estimates roughly 50-60 lines per story point for Python. That is within normal range for well-tested utility scripts.

**Verdict**: 8 SP is at the upper end of reasonable but defensible. The stdlib constraint (no `requests`) adds genuine friction -- raw `urllib` error handling is verbose and error-prone. The batch splitting and double-faced card handling are non-trivial edge cases. If the script were allowed to use `requests`, I would argue for 5 SP. With the stdlib constraint, 8 SP accounts for the additional boilerplate and testing overhead. The risk noted in the sprint plan (US-02 bleeds into Sprint 2, blocks US-04) is the real concern -- the estimate is less important than the mitigation.

---

## Challenge 4: US-08 (Dogfooding) at 5 SP -- Enough for 5 End-to-End API-Dependent Tests?

**Confidence**: 4/5 (significant doubts)

US-08 requires 5 full pipeline executions with live Scryfall API calls, each producing a 100-card decklist that must pass all quality gates. The SM allocates 5 SP and an entire sprint. The SP estimate is low. The sprint allocation is correct. These two facts are in tension.

**Evidence**:

- **Each test case is a full pipeline run**: Invoke skill with parameters > intake extraction > commander validation (API call) > Deck Builder agent (100 card lookups via batch API) > Rules Judge (batch validation API call) > Optimization Reviewer (synergy analysis + replacement search API calls) > Price Evaluator (batch pricing API call) > correction cycles (potentially 3 rounds of Deck Builder > all agents again). A single run with one correction cycle involves 5-8 API calls and 4 agent invocations. Five test cases = 25-40 API calls minimum.

- **The test cases increase in constraint difficulty**: TC1 (mono-black, $150) is a smoke test. TC5 (4-color, $50, $5/card cap) is designed to stress the budget-synergy negotiation logic. If TC5 fails (highly likely on first attempt given the extreme constraints), the team must diagnose whether the failure is in the Deck Builder's card selection, the Price Evaluator's replacement logic, or the correction routing's priority resolution. This diagnosis is the real work -- not the test execution.

- **5 SP implies roughly half a sprint's worth of effort at the 13 SP ceiling**. But the SM explicitly says "low SP but high elapsed time" and "budget deliberately low to absorb correction cycles." This is an honest acknowledgment that the SP estimate understates the actual work. If correction cycles are needed (and they will be -- TC5 is designed to force them), the analysis, diagnosis, and fix work is not captured in the 5 SP estimate.

- **What 5 SP actually covers**: Run 5 tests, capture logs, run plugin-validator. What 5 SP does not cover: diagnosing why TC5's budget constraint produces a deck with synergy score 1.8 instead of 2.0, determining whether the fix belongs in the Deck Builder template, the Optimization Reviewer's threshold logic, or the Price Evaluator's replacement suggestions, implementing the fix, and re-running TC5 (and potentially TC2-TC4 to confirm no regression).

- **The sprint plan's own risk register lists "TC5 budget constraint forces unacceptably low synergy" as High likelihood**. A High likelihood risk in the only story of Sprint 3, estimated at 5 SP with no buffer, is a planning contradiction.

**What should change**: Either (a) increase US-08 to 8 SP to account for diagnosis and correction work that the High-likelihood TC5 risk will almost certainly trigger, or (b) split US-08 into two stories: US-08a (3 SP, run TC1-TC4 as validation) and US-08b (5 SP, run TC5 as stress test + diagnose and fix constraint negotiation issues). Option (b) is better because it separates "prove the pipeline works" from "prove the pipeline handles edge cases." If the SM keeps 5 SP, the risk register must acknowledge that Sprint 3 may need to extend or that TC5 acceptance criteria may need negotiation with the PO.

---

## Challenge 5: Critical Path Is 28 SP Serial -- Any Way to Reduce?

**Confidence**: 3/5 (moderate doubts -- some reduction is possible, but not dramatic)

The critical path runs US-01 (2) > US-02 (8) > US-04 (8) > US-05 (5) > US-08 (5) = 28 SP. This is 67% of the total 42 SP on the serial path, meaning only 33% of work benefits from parallelism. Can we compress?

**Evidence**:

- **US-01 (2 SP) is irreducible**. It is pure scaffolding and already minimal.

- **US-02 (8 SP) on the critical path is questionable**. The critical path runs through US-02 because US-04 depends on US-02 (the orchestrator needs `card_lookup.py` for commander validation). But US-04's dependency on US-02 is partial -- US-04 needs to *reference* the script's CLI interface, not to have it complete. The orchestrator's intake mode detection (AC 4.1, 4.2), agent sequencing logic (AC 4.13), correction routing (AC 4.14, 4.15, 4.16), and output formatting (AC 4.17, 4.18) are all independent of `card_lookup.py`. Only AC 4.3 (commander validation), AC 4.12 (card name validation during construction), and the agent prompt templates that invoke the script depend on US-02 being complete.

  This means US-04 could start in parallel with US-02 if the script's CLI interface is defined (but not implemented) as a contract. The orchestrator would reference `card_lookup.py validate --name <name>` in its prompt template without needing the script to exist. Integration testing would still require US-02 complete, but the prompt engineering work (the bulk of US-04's 8 SP) could proceed.

- **US-05 (5 SP) on the critical path vs US-06 or US-07**: The SM places US-05 (Rules Judge) on the critical path as max(US-05, US-06, US-07). This is correct -- US-05 and US-06 are both 5 SP, so either could be on the critical path. But US-07 (4 SP) is definitively not on the critical path, which means the actual critical path length does not change regardless of which 5 SP story is selected.

- **Potential reduction**: If US-04 starts after US-01 (overlapping with US-02), the critical path becomes US-01 (2) > US-04 (8, starting with non-script-dependent ACs) > US-05 (5) > US-08 (5) = 20 SP serial, with US-02 (8) running in parallel. This saves 8 SP of serial time. However, this requires US-02's CLI interface to be defined as a contract before US-04 starts -- essentially a 0.5 SP interface specification task extracted from US-02.

- **Risk of compression**: Starting US-04 before US-02 is complete means the orchestrator is written against an interface contract, not a working script. If the script's actual behavior diverges from the contract (e.g., the error response format changes, the batch splitting produces a different JSON structure than expected), US-04 needs rework. This is the classic interface-vs-implementation risk.

**What should change**: The critical path can be reduced from 28 SP to approximately 20 SP by defining US-02's CLI interface contract early and allowing US-04 to start in parallel. This is a moderate-risk optimization. If the SM chooses not to pursue it (reasonable -- interface contracts add coordination overhead for a solo contributor), the 28 SP critical path should be accepted as-is with the explicit note that it represents 2.15 sprints of serial work against a 3-sprint plan, leaving only 0.85 sprints of float across the entire project.

---

## Challenge 6: PO Story Map Declares "Sprint count: 1" -- Contradicts SM's 3-Sprint Plan

**Confidence**: 4/5 (confident this is a documentation defect, not a planning conflict)

The PO's user stories document (Capacity Declaration table, line 19-25) states "Sprint count: 1 (single sprint delivery)." The SM's sprint plan distributes the same 42 SP across 3 sprints. These artifacts contradict each other.

**Evidence**:

- The PO's story map does not assign stories to specific sprints -- there is no sprint column in the Story Map table. The "Sprint count: 1" appears to mean "one release" rather than "one sprint." This interpretation is supported by the fact that the PO does not provide sprint-level capacity calculations (no velocity baseline, no ceiling).

- However, a future reader (or a DoD reviewer) will see "Sprint count: 1" in the PO artifact and "Sprint count: 3" in the SM artifact and flag the inconsistency. The SM's plan is clearly authoritative for sprint planning, but the PO's document should not make sprint count claims.

**What should change**: Update the PO's Capacity Declaration to either remove the "Sprint count" row (sprint planning is the SM's domain) or change it to "Release: 1 (single release delivery)" to avoid the contradiction. This is a minor documentation fix.

---

## Challenge 7: Risk Register Declares GREEN -- Warranted?

**Confidence**: 4/5 (significant doubts)

The risk register lists 7 risks, rates most as Medium likelihood, and declares overall health GREEN. This assessment does not account for compound risk or the ceiling violation.

**Evidence**:

- Sprint 2 at 138% ceiling is listed as a risk ("Medium likelihood / Medium impact") but the overall health remains GREEN. A ceiling violation is not a Medium risk -- it is a plan exception. The SM provides a sound justification (parallelism), but GREEN health means "executing within normal parameters." A sprint that exceeds ceiling by 38% is not normal parameters, regardless of parallelism.

- The risk register lists US-02 bleed as "Medium likelihood / High impact" (blocks US-04, blocks Sprint 2). A single Medium/High risk with the potential to cascade across two sprints should, by itself, prevent a GREEN rating.

- TC5 is listed as "High likelihood / Medium impact." A High-likelihood risk in Sprint 3 combined with US-08's 5 SP estimate (Challenge 4) and no buffer within the sprint creates a planning gap.

- Missing risk: "Prompt template iteration cycles." The agent prompt templates (US-05/06/07) are instructions to an LLM. LLMs are unpredictable in how they interpret structured prompts. The first draft of the Rules Judge template may produce verdicts that miss edge cases, requiring prompt revision and retesting. This iteration is unbudgeted in the estimates and unlisted in the risk register.

- Missing risk: "Scryfall API behavioral changes between Sprint 1 development and Sprint 3 dogfooding." If Scryfall changes response formats, rate limits, or endpoint behavior between the time `card_lookup.py` is written and the time it is used in dogfooding, the script may fail. Low likelihood but non-zero for a multi-sprint plan.

**What should change**: Downgrade overall health to YELLOW. Add "prompt template iteration cycles" as Medium likelihood / Medium impact with mitigation: "budget first revision cycle into the estimate; if second revision needed, flag to SM for scope negotiation." The plan is executable at YELLOW -- it just needs to be honest about the ceiling exception and compound risk profile.

---

## Summary Scorecard

| # | Challenge | Confidence | Recommendation |
|---|-----------|:----------:|----------------|
| 1 | Sprint 2 at 138% ceiling -- parallelism amplifies blast radius | 4/5 | Defer US-07 to Sprint 3 (cap Sprint 2 at 18 SP) or freeze US-04 interface before parallel start |
| 2 | 42 SP may be 2 SP inflated (US-03 reference files) | 3/5 | Reduce US-03 from 5 to 3 SP; net total 40 SP. Not material. |
| 3 | US-02 at 8 SP is upper-bound reasonable | 3/5 | Accept. stdlib constraint justifies the premium. Monitor velocity. |
| 4 | US-08 at 5 SP understates dogfooding work | 4/5 | Increase to 8 SP or split into US-08a (validation) + US-08b (stress test + fix) |
| 5 | 28 SP critical path can compress to ~20 SP | 3/5 | Define US-02 CLI contract early; allow US-04 parallel start. Optional optimization. |
| 6 | PO says "Sprint count: 1", SM says 3 | 4/5 | Documentation fix -- PO should remove sprint count or say "Release: 1" |
| 7 | GREEN health rating is optimistic | 4/5 | Downgrade to YELLOW; add prompt iteration and compound risk |

**Overall Confidence: 4/5**

The sprint plan is well-structured with sound dependency analysis, honest acknowledgment of the ceiling exception, and appropriate risk identification for individual risks. The SM demonstrates strong planning judgment in story grouping, execution ordering, and the Sprint 3 buffer. However, the plan has two material weaknesses that elevate confidence to 4/5 (significant doubts):

1. **Sprint 2's 138% ceiling violation** is the primary concern. The parallelism argument is mathematically sound but operationally fragile -- it assumes US-04's output interface is stable before the three downstream agents begin, which is an assumption about an 8 SP story that has not been built yet. The blast radius of an interface change is 3x wider than in Sprint 1's 2-way fan-out.

2. **US-08 at 5 SP with a High-likelihood risk in TC5** is a planning contradiction. The sprint plan budgets low SP "to absorb correction cycles" but does not actually budget SP for the correction work itself. The sprint allocation (a full sprint) is correct; the SP estimate is not.

Neither weakness is plan-breaking. Both are addressable: defer US-07 to reduce Sprint 2 to 18 SP, and increase US-08 to 8 SP (total becomes 43 SP across 3 sprints, average 14.3 SP, still within 16 SP velocity baseline). The plan is executable as written, but it is a YELLOW plan calling itself GREEN.

**Escalation required**: No. Confidence is 4/5, but all concerns are addressable within the SM's authority. The PO should be informed of the US-08 estimate concern (it affects Sprint 3 scope and TC5 acceptance criteria negotiation) but does not need to approve the sprint structure changes. The team makes prioritization and execution decisions autonomously.

```
STATUS: DONE
ARTIFACT: .delivery/artifacts/05-plan/challenger/challenge.md
SUMMARY: 7 challenges, overall confidence 4/5. Primary concerns: Sprint 2 at 138% ceiling with fragile parallelism assumption, US-08 at 5 SP contradicts High-likelihood TC5 risk. Recommendations: defer US-07 to cap Sprint 2 at 18 SP, increase US-08 to 8 SP, downgrade health to YELLOW. No escalation required.
```
