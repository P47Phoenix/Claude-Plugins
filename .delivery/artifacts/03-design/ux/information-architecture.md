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
