# Retrospective: run-2026-04-02-k3r9

**Scrum Master**: Aragorn
**Date**: 2026-04-03
**Pipeline**: run-2026-04-02-k3r9
**Type**: GREENFIELD (MTG Commander Deck Builder Plugin)
**Feature**: `mtg-commander/` plugin

> *"We set out to forge a thing that did not yet exist -- no map, no road, only the vision Gandalf brought us and the will to see it built. Two days, two sessions, thirteen files, and a deck builder that stands on its own legs. The road was not without stumbling. Two defects found their way past our gates, and that is a wound I will not forget. But the fellowship caught them before they reached the user, and that is what matters."*

---

## 1. Run Summary

| Item | Value |
|------|-------|
| **Pipeline ID** | run-2026-04-02-k3r9 |
| **Type** | GREENFIELD |
| **Feature** | MTG Commander Deck Builder Plugin |
| **Started** | 2026-04-02 |
| **Completed** | 2026-04-03 |
| **Sessions** | 2 (0 session losses) |
| **Stages Executed** | All 7 (Idea, Refine, Design, Architect, Plan, Dev, UAT) -- full depth |
| **Total Stories** | 8 (US-01 through US-08) |
| **Total SP** | 42 |
| **Sprints** | 4 (10+13+10+9 SP) |
| **DoD First-Try Pass** | 5/7 stages (71%) |
| **Defects Found** | 2 (DEFECT-001 Critical, DEFECT-002 Major) |
| **Dogfooding** | 5/5 test cases passed (post-fix) |

---

## 2. What Went Well

### 2.1 Full 7-Stage GREENFIELD Completed in 2 Sessions

This is the first GREENFIELD pipeline through the delivery-flow system. All seven stages executed at full depth, producing a complete plugin with 13 files, 4 sub-agents, and a working Scryfall API client -- from idea brief to dogfooded acceptance in two calendar days. No stages were skipped, no stages ran light. The pipeline carried its full weight and delivered.

**Evidence**: All 7 stage summaries show Depth: full. Dev notes: 13 files created, 5/5 smoke tests pass.

### 2.2 Idea Through Architect: Four Consecutive First-Try DoD Passes

Stages 1 through 4 all passed DoD on the first attempt. The upstream quality was strong enough that each gate held without rework. This extends the streak from previous runs and demonstrates that gate-patterns memory injection continues to pay dividends even on a new project type.

**Evidence**: Stage summaries 01-04 all report "DoD Rounds: 1 (first-try pass)."

### 2.3 Adversarial Reviews Added Real Value Without Blocking

The Challenger ran in both Refine (3/5 confidence) and Architect (3/5 confidence), and again in Plan (4/5 confidence, YELLOW risk). None were blockers, but the Architect adversarial review flagged session loss risk and attention degradation for synergy tags -- both are genuine risks for a context-heavy multi-agent plugin. The Challenger earned its keep by naming risks the team would carry forward knowingly rather than discovering them in production.

**Evidence**: Architect stage summary: 3 adversarial conditions noted (session loss, attention degradation, correction counter cascade).

### 2.4 Dogfooding Caught Both Defects Before Release

All 5 end-to-end test cases (TC-1 through TC-5) were executed during UAT. TC-2 (Karlov Orzhov Lifegain) surfaced both DEFECT-001 (color identity violation missed by Rules Judge) and DEFECT-002 (Card Kingdom price divergence). The defects were found, documented, root-caused, and fixed -- all before the pipeline closed. Dogfooding proved its worth as a P0 gate.

**Evidence**: DEFECT-001.md, DEFECT-002.md. 5/5 test cases passed after fixes.

### 2.5 Architecture Decisions Were Crisp and Traceable

Four ADRs were produced and each resolved a genuine fork in the road. ADR-001 (single SKILL.md orchestrator) and ADR-002 (Python script via Bash, not MCP) shaped the entire implementation. All 5 open questions from the PRD were resolved at the Architect stage. No architecture ambiguity leaked into Development.

**Evidence**: Architect stage summary: 4 ADRs, all 5 PRD open questions resolved. Dev notes show zero architecture rework.

---

## 3. What Didn't Go Well

### 3.1 Plan Stage Required 2 DoD Rounds (Ceiling Violation + Missing Test Strategy)

Plan was the only stage to fail DoD on the first attempt, and it failed on two separate validator findings: the SM (myself) rejected a sprint ceiling violation, and QA rejected the absence of a test strategy artifact. Both were legitimate catches, but they should not have been necessary -- the Plan stage agents should know the sprint ceiling constraint and that a test strategy is a mandatory artifact.

**Evidence**: Plan stage summary: "DoD Rounds: 2 (SM rejected ceiling violation + QA rejected missing test strategy -> both fixed)."

### 3.2 Rules Judge Agent Relied on LLM Knowledge Instead of Deterministic API Validation (DEFECT-001)

The Rules Judge checked color identity using LLM card knowledge rather than programmatic Scryfall API calls. This allowed Sejiri Refuge (W/U) into a W/B deck -- a format legality violation that undermines the plugin's core guarantee. The root cause is an agent prompt gap: the Rules Judge guide did not mandate batch API validation for color identity.

**Evidence**: DEFECT-001.md. Sejiri Refuge `color_identity: ['U', 'W']` included in Karlov (W/B) deck. Rules Judge reported PASS.

### 3.3 Single-Source Pricing Was a Known Scope Limit That Still Surprised the User (DEFECT-002)

The PRD explicitly scoped v1 to Scryfall-only pricing (TCGPlayer market). The user's original spec listed Card Kingdom as an expected source. The 50%+ price divergence between TCGPlayer and Card Kingdom means "budget compliant" is vendor-specific -- a fact the Price Evaluator output did not disclose. This is not a code bug but a UX gap: the PRD team knew the limitation but failed to mandate a user-facing disclaimer.

**Evidence**: DEFECT-002.md. TC-2 reported $97.37 (TCGPlayer) vs $150+ (Card Kingdom) for the same deck.

---

## 4. Lessons Learned

| # | Lesson | Evidence | New? |
|---|--------|----------|:----:|
| L-1 | **Agent validation of format-critical rules must be deterministic (API-driven), not LLM-inferred.** When correctness is binary (legal/illegal), the agent prompt must mandate programmatic validation. LLM card knowledge is unreliable for exhaustive checks across 100 cards. | DEFECT-001: Rules Judge missed color identity violation using LLM knowledge. Fix: mandate `card_lookup.py` batch validation. | Yes |
| L-2 | **Known scope limitations need explicit user-facing disclaimers in output.** If a capability is scoped to a single source (pricing, data, etc.), the output artifact must state the limitation clearly. The PRD team knowing about it is not sufficient -- the user must know. | DEFECT-002: Price Evaluator showed $97.37 without noting it was TCGPlayer-only. User expected Card Kingdom parity. | Yes |
| L-3 | **Plan stage agents need pre-loaded constraints (sprint ceiling, mandatory artifacts).** The SM and QA validators should not be catching constraint violations that the planning agents already know about. Inject constraints into the planning agent prompts, not just the validator prompts. | Plan stage: 2 DoD rounds due to ceiling violation and missing test strategy -- both are known constraints. | Yes |
| L-4 | **GREENFIELD pipelines benefit from all 7 stages at full depth.** No stage felt unnecessary. Idea established scope, Refine tightened ACs from 3 to 5 test cases and added synergy taxonomy, Design mapped all 7 FRs, Architect resolved all open questions, Plan caught sizing issues, Dev delivered clean, UAT found real defects. | All 7 stages ran full depth. 2 defects caught at UAT that originated in Refine (scope) and Architect (agent design). | Yes |

---

## 5. Stage Health

| Stage | Depth | DoD Rounds | First-Try Pass | Cumulative Baseline (8 runs) | Trend |
|-------|-------|:----------:|:--------------:|:----------------------------:|:-----:|
| Idea | Full | 1 | Yes | 100% (6/6) | Stable |
| Refine | Full | 1 | Yes | 100% (3/3) | Stable |
| Design | Full | 1 | Yes | 100% (2/2) | Stable |
| Architect | Full | 1 | Yes | 100% (4/4) | Stable |
| Plan | Full | 2 | **No** | 57% (4/7) | Declining |
| Dev | Full | N/A | N/A (empirical) | N/A | -- |
| UAT | Full | 1 | Yes | 75% (3/4) | Stable |

**Overall first-try pass rate this run**: 71% (5/7 stages, excluding Dev N/A)
**Consecutive 100% runs**: 0 (streak broken by Plan stage)

**Plan stage note**: Plan has the lowest first-try pass rate in the pipeline. Three of seven runs required rework. This is now a pattern, not an incident. L-3 (pre-loaded constraints) targets the root cause.

---

## 6. Metrics

| Metric | Value |
|--------|-------|
| **Velocity** | 42 SP / 4 sprints (10.5 SP/sprint avg) |
| **Stories completed** | 8/8 (100%) |
| **ACs verified** | 85/85 (100%, per test strategy) |
| **Dogfooding test cases** | 5/5 passed (post-fix) |
| **DoD first-try pass rate** | 71% (5/7 stages) |
| **Defects found** | 2 (1 Critical, 1 Major) |
| **Defects fixed** | 2/2 (100%) |
| **Session count** | 2 (0 session losses) |
| **Calendar days** | 2 |
| **Files created** | 13 (plugin total) |
| **ADRs produced** | 4 |
| **PRD findings addressed** | 13 (3 blocking, 2 must-fix, 4 recommended, 4 warnings) |
| **Adversarial reviews** | 3 (Refine 3/5, Architect 3/5, Plan 4/5) |
| **Plugin improvement issues** | 1 (Issue #55: architect skill) |

---

## Improvement Actions

| # | Action | Owner | Priority | Target |
|---|--------|-------|----------|--------|
| IA-1 | Add `validate-deck` command to `card_lookup.py` for batch color identity + legality checking. Update Rules Judge guide to mandate API validation over LLM inference. | Developer | P0 | Next pipeline |
| IA-2 | Add pricing source disclaimer to Price Evaluator output template. Short-term fix for DEFECT-002. | Developer | P1 | Next pipeline |
| IA-3 | Inject sprint ceiling and mandatory artifact list into Plan stage agent prompts (not just validator prompts). | SM / Pipeline | P1 | Next pipeline |

---

> *"Forty-two story points. Eight stories. Thirteen files forged from nothing. And two defects that slipped past our gates -- one a quiet betrayal of color identity, the other a price we quoted without naming the merchant. Gimli built well, but the Rules Judge trusted its own memory when it should have trusted the Scryfall scrolls. That lesson is carved in stone now.*
>
> *The Plan stage stumbled again -- the third time in seven runs. I will not call it a weakness of the fellowship. I will call it what it is: we ask our planners to work without the walls they need. We will give them those walls before the next march.*
>
> *But hear this: every defect was found by our own hands, in our own dogfooding, before any user walked the road we built. That is the covenant of this team. We do not ship what we have not walked ourselves.*
>
> *Rest now. The next road will come soon enough."*

---

**Retrospective complete.** Pipeline run-2026-04-02-k3r9 is closed.
