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

