# BACKLOG-006: Architect transformation planning (AS-IS → TO-BE → Roadmap)

**Status**: Open
**Priority**: P2
**Size**: L (complexity note: Phase 1A behavioral reconstruction materially increases scope beyond original L — closer to L+)
**Created**: 2026-04-08
**Owner**: PO + Architect (paired)

## Source
**PO ask (verbatim, 2026-04-08)**:
> "Would also like the architect be able to review a system and provide some guidance on what it should do."
> "IE: Current state -> Ideal future state -> Iterative steps to get there."

**PO follow-up (verbatim, 2026-04-08)**:
> "Another thing to think about is a system may have grown over time to the point that no one really understands how it works. As such we may need build the use cases based on the current state of the system."

## Problem Statement
The Architect skill today is effectively greenfield-only: its task_types (`design`, `decompose`, `model`, etc. — see `delivery-team/skills/architect/SKILL.md:519`) assume PRD → architecture. The closest brownfield-adjacent capability is `audit-preparation` (SKILL.md:262), which is compliance-focused, and `enterprise-patterns.md:27`'s passing mention of TOGAF transition architectures — neither produces a linked AS-IS → TO-BE → Roadmap artifact set.

Real-world brownfield work has a prior problem the original framing missed: on legacy systems nobody understands, structural analysis alone is blind. You can map modules and coupling, but you cannot judge whether they do the right things because you do not know what the system is **for**. Structural AS-IS without behavioral AS-IS is a map of unknown territory.

## Proposed Direction
New architect `task_type: transformation-planning` implemented as a **mini sub-workflow** (not a single invocation). Each phase is a separate agent invocation with file-based handoff:

1. **Scan** — enumerate modules/services/interactions from the codebase
2. **Phase 1A — Behavioral reconstruction (PO-led)** — reverse-engineer **use cases** from the current state before any structural modeling. Sources: existing tests (especially integration/e2e), user-facing strings and UI text, API endpoints, CLI commands, README/docs, commit message patterns, issue history, telemetry if available. Output: `as-is-use-cases.md` listing reconstructed use cases, each with: **actor, goal, preconditions, main flow, observed variations, evidence citations, confidence level (high/medium/low)**. This phase is a PO artifact (use cases live in product-delivery), executed by the PO with the Architect as a reviewer.
3. **Phase 1B — Structural AS-IS (Architect-led)** — explicit Model-First model (entities = current modules, state = volatility/coupling, **actions = use cases from 1A**, constraints = implicit rules the code follows today). Without 1A, the "actions" dimension is empty and the model is structurally incomplete.
4. **Model TO-BE** — explicit model of ideal target, same four elements, per chosen decomposition paradigm (volatility golden rule / DDD contexts / etc.)
5. **Derive roadmap** — ordered iterative steps bridging AS-IS → TO-BE
6. **Review** — architecture board pass over use cases, TO-BE, and roadmap

The four artifacts (**Use Cases**, AS-IS, TO-BE, Roadmap) are **diffable and traceable**: every structural AS-IS element should trace to at least one use case it supports; roadmap success is measured by AS-IS model progressively converging on TO-BE across iterations.

Each roadmap step must carry: scope, ordering rationale, reversibility, risk, incremental value delivered, invariants preserved during/after. No big-bang refactors.

### Legacy trigger (when does Phase 1A run?)
**Default: 1A runs unless explicitly skipped.** The cost of skipping when needed (building a structural model blind to purpose) is much higher than the cost of running when not needed (redundant confirmation of already-known use cases).

Phase 1A is **required** when ANY of:
- (a) System age > 3 years with no current use case documentation
- (b) Original authors no longer available or not on the delivery team
- (c) Tests + docs coverage of user-facing behavior below a "can a new engineer infer what it does" bar (PO judgment call)
- (d) PO explicitly invokes it

Phase 1A may be **skipped** only when the PO explicitly asserts current use case documentation exists, is trusted, and is cited in the transformation-planning invocation. Skipping is logged with justification.

## Research lineage
- **Model-First (arXiv:2512.14474)**: Use cases ARE the "actions" dimension of the Model-First explicit model. The 1A/1B split makes the four-element model explicit as a workflow: 1A builds actions (and implicit goals), 1B builds entities + state + constraints. BOTH AS-IS and TO-BE remain explicit problem models, and AS-IS constraints / TO-BE constraints are instances of the same `constraints.yml` schema from BACKLOG-001/004 — the roadmap is a constraint-preserving transformation. This is the **third domain** pressure-testing that primitive.
- **MAR (arXiv:2512.20845)**: Use case reconstruction from legacy code is high-uncertainty work where persona-diverse review matters most. Phase 1A review board uses a **code archaeologist** persona (reads commits/history), a **user advocate** persona (reads UI strings and docs), and a **skeptical tester** persona (challenges confidence levels and gaps). Different personas catch different reconstruction gaps. The TO-BE and roadmap reviews remain BACKLOG-003 architecture board territory (Volatility/DDD/Evolutionary/Risk Architects).

## Acceptance Criteria
1. Invoked against Claude-Plugins itself, produces an AS-IS model explicitly naming the **delivery-flow orchestrator / worker-skills split**, the **two-channel communication pattern**, and the **tiered memory system**
2. AS-IS gap analysis flags at least one issue already logged in `.delivery/defects/` (proving it found real things)
3. TO-BE model cites the volatility golden rule (once BACKLOG-004 lands) and is expressed using the shared `constraints.yml` schema from BACKLOG-001
4. Roadmap produces ≥3 ordered iterative steps, each with: scope, ordering rationale, reversibility, risk, incremental value, preserved invariants
5. Each roadmap step is independently shippable (no step requires a future step to be value-positive)
6. Roadmap passes a "no big-bang" check: no single step changes more than X% of subsystems (X tbd in spike)
7. TO-BE and roadmap both run through the BACKLOG-003 architecture board with persona-diverse review
8. **Phase 1A dogfood**: run against Claude-Plugins produces **≥5 reconstructed use cases with evidence citations** (e.g., "invoke delivery-flow setup wizard" cited to `references/setup-wizard.md` + quick-start mode in SKILL.md)
9. **Honest uncertainty**: ≥1 reconstructed use case MUST carry `confidence=low` with a written reason. If all use cases on a legacy system are high-confidence, the capability is lying to itself — this criterion fails.
10. **Behavioral-structural traceability**: the reconstructed use cases MUST explain at least one architectural choice observed in the structural AS-IS (e.g., "two-channel communication exists because of use case X")

## Dependencies
- **Depends on BACKLOG-004** (decomposition guidance / golden rule must exist so TO-BE can cite it)
- **Depends on BACKLOG-001** (`constraints.yml` primitive — AS-IS and TO-BE both emit constraint instances)
- **Benefits from BACKLOG-003** (architecture board) for use case, TO-BE, and roadmap review — strongly recommended, not strictly blocking
- **Feeds BACKLOG-005** — dogfood run produces AS-IS use cases + structural model of the current architect skill topology, which BACKLOG-005 consumes as canonical input
- **Requires PO+Architect pairing** in execution — this is a partial instantiation of the PO+Architect Design Sprint sub-workflow that BACKLOG-005 will formalize. This strengthens the case for BACKLOG-005 but does NOT unblock -005 from -006; sequence remains -006 → -005.

## Dogfood Plan
First invocation MUST run against Claude-Plugins itself. The delivery-team plugin is a complex system with real AS-IS state, real tech debt (see `.delivery/defects/`), and a clear evolving direction (BACKLOG-001/003/004/005 describe the TO-BE). Phase 1A will reconstruct use cases of delivery-flow and its sibling skills from SKILL.md files, references, hooks, and commit history. The dogfood run's outputs (Use Cases, AS-IS, TO-BE, Roadmap) become canonical inputs for BACKLOG-005.

## Links
- Current architect skill: `delivery-team/skills/architect/SKILL.md` (line 519 task_type list; line 262 audit-preparation; references/enterprise-patterns.md:27 transition architectures)
- Use cases live in: `delivery-team/skills/product-delivery/` (PO artifact, not architect)
- Depends on: BACKLOG-001, BACKLOG-004
- Benefits from: BACKLOG-003
- Feeds: BACKLOG-005
- Sequencing memo: `.delivery/artifacts/research/po-revision-research-integration.md`
