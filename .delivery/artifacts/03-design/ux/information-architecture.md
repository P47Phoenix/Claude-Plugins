# Information Architecture — Configurable Architecture Board (LIGHT)

*Forged by Celebrimbor, Stage 3 Design (light). Run: run-2026-04-08-b2c7.*

## Flow 1 — Reviewer Persona Author

1. Author opens `delivery-team/skills/delivery-flow/references/architecture-board-personas.md`.
2. Copies an existing H2 persona block as template.
3. Fills: `id`, `name`, `perspective` (one line), `context-files-to-load`, `review-prompt-template`, `gate-criteria`, `signal-format`.
4. Validates distinct perspective against siblings (R1 mitigation).

## Flow 2 — Judge Synthesis

1. Orchestrator dispatches N reviewers in parallel; each writes one artifact.
2. Orchestrator invokes judge with the N artifact paths (not inlined — isolation, NFR-3).
3. Judge reads each, cites each finding individually, declares agreement/disagreement, emits verdict.
4. On deadlock → fall back to existing debate pattern's DEADLOCK rule.

## Flow 3 — Config-Writer (human enabling the board)

1. Human opens `.delivery/config.yml`.
2. Adds `architecture_board:` block (see ADR-001 schema).
3. Sets `enabled: true`, picks ≥1 persona IDs from the library.
4. Runs pipeline — Stage 4 auto-dispatches the board after primary architect.
5. Absence of the block = backwards-compat no-op (NFR-2).

## Artifact Layout

```
.delivery/artifacts/04-architect/
├── solution/architecture.md          # primary architect (unchanged)
└── board/                            # NEW
    ├── <persona-id>-review.md        # one per reviewer (N files)
    └── judge-verdict.md              # single synthesized verdict
```

No wireframes — this feature is text-artifact-only.

---

# Information Architecture — transformation-planning (LIGHT)

*Forged by Celebrimbor, Stage 3 Design (light). Run: BACKLOG-006 transformation-planning.*

## File layout (canonical, namespaced)

```
.delivery/artifacts/08-transform/
├── as-is-use-cases.md          # Phase 1A (PO)     — behavioral AS-IS
├── as-is-constraints.yml       # Phase 1B (Arch)   — structural AS-IS
├── to-be-constraints.yml       # Phase 2  (Arch)   — target model
└── roadmap.md                  # Phase 3  (Arch)   — AS-IS → TO-BE path
```

`08-transform/` sits after UAT in the pipeline layout; when invoked standalone, substitute `transform/`.

## Author-flow (per phase, file-handoff sequential)

1. **Phase 1A — PO** mines codebase evidence → writes `as-is-use-cases.md`.
2. **Phase 1B — Architect** reads `as-is-use-cases.md` → writes `as-is-constraints.yml` (actions field cites use-case IDs).
3. **Phase 2 — Architect** reads `as-is-constraints.yml` → writes `to-be-constraints.yml`.
4. **Phase 3 — Architect** reads both AS-IS and TO-BE yml → writes `roadmap.md`.

Two-channel rule: no phase assumes in-memory state; every handoff by path.

## Cross-artifact navigation

- **AS-IS → TO-BE diff:** both yml files share the BACKLOG-001 schema; diffable field-by-field.
- **TO-BE → Roadmap trace:** each roadmap step cites the TO-BE deltas it closes.
- **Roadmap → AS-IS back-link:** each step cites touched AS-IS subsystems for the big-bang check.

## Consumer-flow (downstream engineer)

Engineer opens `roadmap.md` → picks a step → follows citations back to `to-be-constraints.yml` (target) and `as-is-constraints.yml` (current) → reads `as-is-use-cases.md` to understand user-visible behavior that must survive the step. Reading order: roadmap-first, model-second. No wireframes — text artifacts only.

---

# Information Architecture — Paradigm-as-Skill Restructure (STEP-02 + STEP-03)

**Stage:** 3 Design (UX) | **Pipeline:** run-2026-04-10-d5e2 | **Date:** 2026-04-10
**Designer:** Galadriel | **Traced to:** FR-1 through FR-7

*I have looked into the Mirror of the architect's monolith and seen 29 references bound together where they need not be. What follows is the shape of their unbinding.*

## 1. Directory Structure Proposal

```
delivery-team/skills/architect/
├── SKILL.md                          # STAYS — becomes paradigm router + all non-decomposition logic
├── references/                       # STAYS — shared references (25 files remain)
│   ├── architecture-patterns.md
│   ├── c4-model.md
│   ├── adr-template.md, adr-lifecycle.md
│   ├── quality-attributes.md
│   ├── enterprise-patterns.md
│   ├── data-modeling.md
│   ├── security-patterns.md, security-requirements.md
│   ├── compliance-frameworks.md, privacy-patterns.md, incident-response.md
│   ├── technology-evaluation.md
│   ├── domain-discovery.md           # Shared — paradigms extract their own question subsets
│   ├── team-topology.md, event-storming.md
│   ├── game-systems.md, level-world.md, network-multiplayer.md, graphics-rendering.md
│   ├── transformation-planning.md, transformation-phase-*.md (4 files)
│   ├── volatility-decomposition.md   # REDIRECT STUB (FR-5)
│   └── strategic-ddd.md              # REDIRECT STUB (FR-5)
└── paradigms/
    ├── volatility/
    │   ├── SKILL.md                  # Volatility-specific decomposition skill
    │   └── references/
    │       ├── volatility-decomposition.md   # MOVED from architect/references/
    │       └── domain-discovery-volatility.md # EXTRACTED from domain-discovery.md
    └── ddd/
        ├── SKILL.md                  # DDD-specific decomposition skill
        └── references/
            ├── strategic-ddd.md              # MOVED from architect/references/
            └── domain-discovery-ddd.md       # EXTRACTED from domain-discovery.md
```

**MOVES (2 files):** `volatility-decomposition.md` (14.6KB), `strategic-ddd.md` (16.6KB) move into their paradigm directories.
**CREATES (2 files):** `domain-discovery-volatility.md`, `domain-discovery-ddd.md` extracted from `domain-discovery.md` (11.4KB shared).
**STAYS (25 files):** All 11 role references, 4 game architecture refs, ADR templates, quality-attributes, technology-evaluation, domain-discovery (shared), transformation-planning suite (5 files), team-topology, event-storming.
**REDIRECT STUBS (2 files):** Original paths become single-line redirects per FR-5.

## 2. Author Flows

### Flow A — Orchestrator Routing to Paradigm

1. Delivery-flow Stage 4 invokes `architect` skill (unchanged entry point)
2. Architect `SKILL.md` detects task type. If `decompose` or `design` with decomposition:
   - Read `architecture.decomposition` from `.delivery/config.yml`
   - If `volatility` -- delegate to `paradigms/volatility/SKILL.md`
   - If `ddd` -- delegate to `paradigms/ddd/SKILL.md`
   - If `auto` or unset -- run decision matrix, then delegate to selected paradigm
3. Non-decomposition tasks (review, document, evaluate, etc.) route through existing logic untouched

### Flow B — Paradigm Author (Adding a New Paradigm)

1. Create `paradigms/<name>/SKILL.md` with: scope declaration, loading trigger, output contract (must match architect output contract from current `SKILL.md` lines 329-430)
2. Create `paradigms/<name>/references/` with paradigm-specific refs
3. Extract paradigm-specific questions from `domain-discovery.md` into `domain-discovery-<name>.md`
4. Add the paradigm value to the router's dispatch table in architect `SKILL.md`
5. No registration in `plugin.json` required (router-discovered, not top-level)

### Flow C — Developer Consuming Decomposition Output

Output path is unchanged: `.delivery/artifacts/04-architect/`. The paradigm that produced the artifact is invisible to downstream consumers. Developers and validators navigate to the same location regardless of which paradigm was selected.

## 3. Context Isolation Check

**Current monolithic load:** Architect SKILL.md (615 lines) + up to 29 reference files (~305KB total).
**Paradigm load (volatility example):** Paradigm SKILL.md (~80 lines) + 2 paradigm refs (~26KB) + task-relevant shared refs (architecture-patterns 10KB, c4-model 11KB, domain-discovery 11KB) = ~58KB.
**Estimated reduction:** ~80% fewer reference tokens in the decomposition sub-agent context. DDD references (16.6KB) excluded from volatility; volatility references (14.6KB) excluded from DDD. The invariant "sub-agents receive only role-scoped references" now holds at paradigm granularity.

## 4. Design Sprint Sub-Workflow IA (FR-4)

**Reference location:** `delivery-team/skills/delivery-flow/references/design-sprint.md` (to be created)
**Flow:** PO defines problem scope/constraints --> Architect router detects paradigm from config --> paradigm skill produces decomposition --> architecture board review (if configured) --> artifact at standard path --> DoD validates --> handoff to Plan stage.
**Trigger:** Stage 4 (Architect) when project type involves decomposition (GREENFIELD, FEATURE, GAME_DEV). Does not trigger for BUG_FIX, DOCS_ONLY, SPIKE, or DESIGN (terminates after Architect per v2.7).

## 5. Backwards Compatibility Check

When an existing pipeline invokes `architect` without paradigm awareness:
1. Router reads `architecture.decomposition` from config
2. If `auto` or absent -- router uses existing decision matrix logic to select paradigm, then delegates
3. If `paradigms/` directory does not exist (pre-migration) -- router falls back to inline logic entirely
4. Non-decomposition task types never enter paradigm routing

*The old roads still lead to the same halls. Only the halls within have been reordered.*

## 6. Open Questions for Architect (Stage 4)

**Q1: Sub-skill registration model.** Should paradigm SKILL.md files register in `plugin.json` as top-level skills, or remain internal sub-skills discovered only by the router? *Non-binding recommendation:* internal. External registration creates a public API surface constraining future restructuring.

**Q2: Shared reference loading strategy.** Does the paradigm SKILL.md list shared refs to load, or does the router pre-load them before delegating? *Non-binding recommendation:* router pre-loads task-relevant shared refs (architecture-patterns, c4-model, domain-discovery) and passes them to the paradigm sub-agent. Paradigm SKILL.md declares only its own refs.

**Q3: Domain-discovery extraction boundary.** The shared `domain-discovery.md` (11.4KB) contains strategy-agnostic interview protocol plus strategy-specific question sets. Only the question sets are paradigm-specific. How much moves?

*These questions I leave for the smith. The mirror shows the shape; only the forge reveals the metal's true temper.*

