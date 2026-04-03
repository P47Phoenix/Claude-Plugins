# Sprint Plan: MTG Commander Deck Builder Plugin

**Version**: 2.0
**Author**: Aragorn (Scrum Master)
**Date**: 2026-04-01
**Status**: Committed
**Pipeline**: GREENFIELD
**Input**: User Stories v1.0 (Gandalf/PO), Architecture v1.0 (Celebrimbor/Architect), SM Review v1.0 (ceiling rejection)

> *"I would rather the fellowship arrive in four steady marches than attempt three at a pace that breaks them."*

---

## 1. Sprint Goals

| Sprint | Goal |
|--------|------|
| Sprint 1 | Plugin scaffold established and Scryfall API client operational -- the tooling foundation upon which every agent depends |
| Sprint 2 | All 7 reference files authored and SKILL.md orchestrator complete -- the pipeline brain can intake, validate, and sequence agents |
| Sprint 3 | Rules Judge and Optimization Reviewer agents operational -- two of three validation agents produce structured verdicts |
| Sprint 4 | Price Evaluator complete and full dogfooding validation -- the pipeline produces legal, synergy-dense, budget-compliant decklists with evidence |

---

## 2. Capacity

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| Velocity baseline | 16 SP / sprint | Mixed workload: Python script (US-02, highest tier), prompt engineering (US-04/05/06/07, mid-high tier), markdown reference files (US-01/03, one tier lower). Weighted baseline accounts for the blend. |
| 80% ceiling | 13 SP | 16 x 0.80 = 12.8, rounded to 13 SP |
| Sprint count | 4 | 42 SP / 13 SP ceiling = 3.23. With no sprint permitted to exceed 13 SP, 4 sprints required. |
| Sprint 1 commitment | 10 SP (77% ceiling) | Scaffold (2 SP) + Python script (8 SP). Focused sprint: US-02 is the heaviest single story (8 SP, 14 ACs) and gets full attention alongside the trivial scaffold. |
| Sprint 2 commitment | 13 SP (100% ceiling) | Reference files (5 SP) + orchestrator (8 SP). Sequential within sprint: US-03 completes first, then US-04 begins with all inputs available. At ceiling but not over -- zero parallelism argument needed. |
| Sprint 3 commitment | 10 SP (77% ceiling) | Rules Judge (5 SP) + Optimization Reviewer (5 SP). Parallel execution: both depend only on US-04 (done), share zero files, load different references. |
| Sprint 4 commitment | 9 SP (69% ceiling) | Price Evaluator (4 SP) + dogfooding (5 SP). Sequential: US-07 completes first, then US-08 validates the full integrated pipeline. Low ceiling utilization absorbs correction cycles and API edge cases. |

**Total committed**: 42 SP across 4 sprints (10 + 13 + 10 + 9).

**No sprint exceeds the 13 SP ceiling.** The v1.0 plan's parallelism argument has been retired. Parallelism remains an execution strategy within sprints (Sprint 3: US-05 and US-06 in parallel), but it no longer justifies over-commitment. The ceiling buffers total committed work against estimation error, not serial path length.

---

## 3. Sprint Breakdown

### Sprint 1: Foundation (10 SP)

| Order | Story | SP | Dependency | Deliverables |
|-------|-------|----|------------|--------------|
| 1 | US-01: Plugin Scaffold | 2 | None | `mtg-commander/` directory, SKILL.md stub, LICENSE.txt, marketplace.json entry, `references/` and `scripts/` dirs |
| 2 | US-02: Scryfall API Client | 8 | US-01 | `scripts/card_lookup.py` -- 6 CLI commands, rate limiter, retry logic, batch splitting |

**Sprint 1 goal**: Plugin skeleton exists and `card_lookup.py` passes all 9 test cases (T2.1-T2.9). The Scryfall API client is the heaviest single story in the backlog. It gets a dedicated sprint with the scaffold, giving the developer full focus on the Python script without competing prompt engineering work.

**Why this grouping**: US-01 is the zero-dependency foundation -- nothing can start without it. US-02 is the single most complex story (8 SP, 14 acceptance criteria, rate limiting, retry logic, batch splitting, DFC handling). Pairing it only with the trivial scaffold (2 SP) gives 3 SP of headroom below ceiling for the inevitable edge cases in API integration. Reference files (US-03) move to Sprint 2 where they directly precede the orchestrator that consumes them.

### Sprint 2: References + Orchestrator (13 SP)

| Order | Story | SP | Dependency | Deliverables |
|-------|-------|----|------------|--------------|
| 1 | US-03: Reference Files | 5 | US-01 | 7 reference files: commander-rules, banned-list, archetype-patterns, structural-minimums, synergy-taxonomy, intake-questions, api-reference |
| 2 | US-04: SKILL.md Orchestrator + Deck Builder | 8 | US-02, US-03 | Complete SKILL.md with intake modes, commander validation, agent sequencing, correction routing, output assembly, export formatting |

**Sprint 2 goal**: All 7 reference files pass content validation (T3.1-T3.7) and the SKILL.md orchestrator can intake parameters (Mode A/B/C), validate commanders, and define the full agent sequencing pipeline. The orchestrator is built with its reference inputs fresh -- US-03 completes first within the sprint, then US-04 begins with every input available.

**Why this grouping**: US-04 depends on both US-02 (done in Sprint 1) and US-03. Placing US-03 and US-04 in the same sprint is sequential, not parallel -- US-03 finishes first, US-04 follows. This eliminates the cross-sprint dependency gap that v1.0 had (where US-03 finished in Sprint 1 but US-04 didn't start until Sprint 2). At exactly 13 SP (100% ceiling), this is the tightest sprint in the plan, but there is no parallelism gamble -- pure sequential execution with clear handoff.

### Sprint 3: Validation Agents (10 SP)

| Order | Story | SP | Dependency | Deliverables |
|-------|-------|----|------------|--------------|
| 1a | US-05: Rules Judge Agent | 5 | US-04 | Rules Judge prompt template: 7 validation checks, structured verdict, synergy audit |
| 1b | US-06: Optimization Reviewer Agent | 5 | US-04 | Optimization Reviewer prompt template: synergy counting, structural validation, mana curve, replacements |

**Sprint 3 goal**: Two of three validation agents are operational. The Rules Judge validates legality (card names, color identity, banned list, singleton rule, format legality, synergy audit) and the Optimization Reviewer validates quality (synergy scoring, structural minimums, mana curve, isolation flagging, replacements). Both produce structured verdicts that the orchestrator's correction routing can consume.

**Why this grouping**: US-05 and US-06 both depend only on US-04 (complete). They are genuinely parallel: different reference file loads (`commander-rules.md` + `banned-list.md` for US-05; `synergy-taxonomy.md` + `structural-minimums.md` for US-06), different validation domains, identical verdict format. Parallelism here is an execution optimization, not a capacity argument -- the sprint is at 10 SP (77% ceiling) regardless of execution order.

### Sprint 4: Price Evaluator + Dogfooding (9 SP)

| Order | Story | SP | Dependency | Deliverables |
|-------|-------|----|------------|--------------|
| 1 | US-07: Price Evaluator Agent | 4 | US-04 | Price Evaluator prompt template: batch pricing, cap logic, budget alternatives, category breakdown |
| 2 | US-08: Dogfooding Validation | 5 | US-05, US-06, US-07 | 5 end-to-end test case runs (K'rrik, Karlov, Bruvac, Korvold, Atraxa), plugin-validator pass, run logs as evidence |

**Sprint 4 goal**: The Price Evaluator completes the 4-agent pipeline, then dogfooding proves it works end-to-end. All 5 test cases from PRD Section 8 produce legal, synergy-dense, budget-compliant 100-card decklists with zero hallucinated names, zero banned cards, synergy score >= 3.0 (>= 2.0 for Atraxa budget stress), and total cost within budget. Plugin passes `plugin-validator` with zero errors and zero warnings.

**Why this grouping**: US-07 (Price Evaluator) is the lightest agent template at 4 SP and the last dependency gate for US-08. Placing both in the final sprint creates a clean sequential flow: build the last agent, then validate the whole pipeline. At 9 SP (69% ceiling), there is 4 SP of headroom -- deliberately generous because dogfooding involves live API calls, correction cycles, and integration surprises that are hard to estimate. Code review alone is not sufficient; we ship what we have proven works.

---

## 4. Execution Order (Within Sprints)

### Sprint 1 Execution

1. **US-01 (Plugin Scaffold)** -- Start here. Create `mtg-commander/` directory, SKILL.md stub with frontmatter and `api.scryfall.com` domain note, LICENSE.txt, marketplace.json entry, `references/` and `scripts/` subdirectories. Run T1.1-T1.4 immediately. This is a 30-minute story -- get it done and unblock US-02.

2. **US-02 (Scryfall API Client)** -- Build `card_lookup.py` in this order: (a) rate limiter class, (b) HTTP request wrapper with error handling and retry logic, (c) `validate` command, (d) `search` command, (e) `batch` command with 75-card splitting, (f) `price` command with null-price fallback, (g) `batch-price` command, (h) `random-commander` command. Run T2.1-T2.9 after each command is added.

**Sprint 1 exit check**: (1) `card_lookup.py validate --name "Sol Ring"` returns `found: true`. (2) `card_lookup.py batch --names "Sol Ring" "Totally Fake"` correctly splits found/not_found. (3) Marketplace.json is valid JSON with the `mtg-commander` entry. (4) All directories exist per US-01 ACs.

### Sprint 2 Execution

1. **US-03 (Reference Files)** -- Author reference files in this order: (a) `api-reference.md` first (verify alignment with completed `card_lookup.py`), (b) `commander-rules.md`, (c) `banned-list.md` (source from mtgcommander.net), (d) `archetype-patterns.md` (10+ archetypes), (e) `structural-minimums.md` (4 power tiers), (f) `synergy-taxonomy.md` (6 categories + 3 exclusion rules), (g) `intake-questions.md` (7 questions with Mode A/B/C logic). Run T3.1-T3.7 as each file completes.

2. **US-04 (SKILL.md Orchestrator + Deck Builder)** -- Begins after US-03 completes. Build in this order: (a) intake extraction with Mode A/B/C detection, (b) commander validation via `card_lookup.py`, (c) banned list check, (d) partner rejection, (e) Deck Builder agent prompt template with reference file loading, (f) agent sequencing logic (Deck Builder > Rules Judge > Optimization Reviewer > Price Evaluator), (g) correction routing with cycle counting, (h) output formatting with export block. Test with T4.1-T4.7 -- especially T4.3 (invalid commander), T4.4 (banned commander), and T4.5 (partner rejection).

**Sprint 2 exit check**: (1) All 7 reference files exist and pass content spot-checks per T3.1-T3.7. (2) SKILL.md has complete intake logic, commander validation, and agent sequencing defined. (3) Correction routing handles FAIL verdicts with re-entry to Deck Builder. (4) Export block format defined (one card name per line).

### Sprint 3 Execution

**US-05 and US-06 -- in parallel**:
- **US-05 (Rules Judge)**: Build prompt template loading `commander-rules.md` and `banned-list.md`. Implement 7 checks: card count, name verification (batch), color identity, banned list, singleton, format legality, synergy audit. Define verdict format (PASS/FAIL with violations and suggested replacements).
- **US-06 (Optimization Reviewer)**: Build prompt template loading `synergy-taxonomy.md` and `structural-minimums.md`. Implement: synergy tag counting per non-land card, isolation flagging (< 3 interactions), structural minimum validation, land count validation (34-40), mana curve distribution, replacement search via `card_lookup.py search`, synergy score calculation.

**Sprint 3 exit check**: (1) Rules Judge produces a structured PASS/FAIL verdict with violations list. (2) Optimization Reviewer produces a synergy score and structural validation. (3) Both verdict formats conform to the orchestrator's correction routing expectations.

### Sprint 4 Execution

1. **US-07 (Price Evaluator)** -- Build prompt template loading `api-reference.md`. Implement: batch pricing via `card_lookup.py batch-price`, total cost calculation, budget validation, per-card cap logic (explicit or 15% default), null-price handling, replacement suggestions, category price breakdown.

2. **US-08 (Dogfooding Validation)** -- Begins after US-07 completes. Execute the 5 test cases in order of increasing constraint difficulty:
   - **TC1: K'rrik (Mono-Black Graveyard)** -- $150 budget, power 7. Single color identity, generous budget. Smoke test.
   - **TC2: Karlov (Orzhov Lifegain)** -- $100 budget, $10 per-card cap, power 6. Two-color identity, per-card cap stress.
   - **TC3: Bruvac (Mono-Blue Mill)** -- $75 budget, power 5, no infinite combos. Card restriction mechanism test.
   - **TC4: Korvold (Jund Sacrifice)** -- $200 budget, power 8. Three-color identity (BRG) with W/U exclusion.
   - **TC5: Atraxa (4-Color Budget Stress)** -- $50 budget, $5 per-card cap, power 7. Four-color identity (WUBG, no R). Synergy threshold may relax to 2.0 per FR-07.4. Hardest test -- run last.

   After all 5 test cases: run `plugin-validator` on `mtg-commander/`. Preserve all run logs as evidence in `.delivery/artifacts/06-dev/developer/`.

**Sprint 4 exit check**: (1) All 5 test cases produce 100-card legal decklists. (2) Zero hallucinated card names across all runs. (3) Zero banned cards. (4) Synergy score >= 3.0 (>= 2.0 for TC5). (5) Total cost within budget for all 5. (6) `plugin-validator` returns zero errors and zero warnings. (7) Zero manual intervention between agent handoffs.

---

## 5. Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Scryfall API rate limiting during US-02 development and US-08 dogfooding | Medium | Medium | 75ms delay baked into `card_lookup.py`. Batch endpoints reduce call count. Exponential backoff on 429. Development can use cached responses for iterative testing. |
| US-02 (8 SP Python script) takes longer than estimated | Medium | High | Sprint 1 has 3 SP headroom below ceiling (10 SP committed vs 13 SP ceiling). If US-02 bleeds into Sprint 2, it blocks US-04 but not US-03. Mitigation: prioritize `validate` and `batch` commands first (most critical for downstream agents), defer `random-commander` if needed. |
| Sprint 2 at 100% ceiling (13 SP) leaves no buffer | Medium | Medium | US-03 and US-04 are sequential, so progress is linear and visible -- no late-sprint surprise from parallel work converging. If US-04 proves harder than estimated, the first action is to descope US-04's correction routing to a basic version and refine in Sprint 3 alongside agent work. |
| Hallucinated card names survive the pipeline | Low | High | Three layers of defense: (1) Deck Builder validates every name via `card_lookup.py` during construction, (2) Rules Judge batch-validates all 100 names, (3) dogfooding TC1-TC5 catch survivors. Zero tolerance -- any hallucinated name is a pipeline failure. |
| Budget constraint in TC5 (Atraxa, $50, $5/card cap) forces unacceptably low synergy | High | Medium | FR-07.4 explicitly allows synergy threshold relaxation to 2.0 for budget-forced cards. TC5 acceptance criteria already accounts for this (>= 2.0 acceptable). The pipeline's budget > synergy priority rule handles irreconcilable conflicts gracefully. |
| Banned list currency -- `banned-list.md` may be stale | Low | Medium | Source from mtgcommander.net during US-03. Include a "last verified" date in the file header. The Rules Judge also checks Scryfall's `legalities.commander` field as a second layer. |
| Correction cycle exhaustion (max 3 cycles) | Medium | Low | US-04 implements best-effort output with warnings when cycles exhaust. Budget-forced cards get relaxed synergy threshold. The pipeline degrades gracefully rather than failing silently. |
| Sprint 4 dogfooding reveals integration defects | Medium | Medium | Sprint 4 is at 69% ceiling (4 SP headroom). Dogfooding is deliberately last with generous buffer. Defects found in TC1-TC2 (simpler cases) can be fixed before TC4-TC5 (harder cases). |

**Overall sprint health**: GREEN. The four-sprint plan eliminates all ceiling violations. Every sprint is at or below 100% ceiling, with three of four sprints providing meaningful headroom (77%, 77%, 69%). The tightest sprint (Sprint 2 at 100%) uses pure sequential execution with no parallelism gamble. The critical path is unchanged but better distributed.

---

## 6. Critical Path

```
Sprint 1:  US-01 (2) ── US-02 (8)
                                    \
Sprint 2:              US-03 (5) ── US-04 (8)
                                              \
Sprint 3:              US-05 (5) ──────────────┐
                       US-06 (5) ──────────────┤
                                               │
Sprint 4:              US-07 (4) ── US-08 (5) ─┘
```

**Critical path length**: US-01 (2) > US-02 (8) > US-04 (8) > US-05 (5) > US-08 (5) = **28 SP serial**

The critical path is unchanged from v1.0. What changed is the distribution: no sprint carries more than the ceiling permits. US-03 moves from Sprint 1 to Sprint 2 (where it directly precedes its consumer, US-04). US-07 moves from Sprint 2 to Sprint 4 (where it directly precedes the dogfooding that proves the whole pipeline).

---

## 7. Changes from v1.0

| Change | v1.0 | v2.0 | Reason |
|--------|------|------|--------|
| Sprint count | 3 | 4 | 42 SP / 13 SP ceiling requires 4 sprints. Rounding to 3 and arguing parallelism was rejected by SM DoD validator. |
| Sprint 1 | 15 SP (115%) | 10 SP (77%) | US-03 moved to Sprint 2. Sprint now contains only scaffold + API client. |
| Sprint 2 | 22 SP (138%) | 13 SP (100%) | US-05/06/07 moved out. Sprint now contains references + orchestrator (sequential). |
| Sprint 3 | 5 SP (31%) | 10 SP (77%) | Now carries US-05 + US-06 (the two larger validation agents). |
| Sprint 4 | N/A | 9 SP (69%) | New sprint: US-07 + US-08. Price Evaluator completes the pipeline, then dogfooding validates it. |
| Parallelism argument | Used to justify ceiling exceptions | Execution strategy only | Parallelism reduces elapsed time, not total committed work. The ceiling buffers estimation error, not serial path. |

---

*Forty-two points. Four sprints. Eight stories. The road is one march longer, but every march is within the strength of the fellowship. I will not ask more of the team than the ceiling permits -- not because I doubt their skill, but because I have learned that haste and overcommitment are the enemies that break more sprints than any orc ever could. We march steady, we march sure, and we arrive with strength to spare.*

```
STATUS: DONE
ARTIFACT: .delivery/artifacts/05-plan/sm/sprint-plan.md
SUMMARY: Redistributed 42 SP across 4 sprints (10+13+10+9), all at or below 13 SP ceiling. Parallelism argument retired. Critical path unchanged at 28 SP.
```
