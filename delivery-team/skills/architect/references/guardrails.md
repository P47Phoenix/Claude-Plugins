# Architecture Guardrails

The sub-agent MUST enforce these guardrails in every output. Guardrails are split into software and game variants. When the sub-agent loads cross-role references (per `references/contracts/cross-role-tasks.md`), the corresponding guardrail set MUST also be enforced.

## Software Architecture Guardrails

- **Every design must state its trade-offs** — "No trade-offs" is not acceptable; every decision has costs.
- **Every component must have a clear responsibility** — single responsibility at the architecture level.
- **Prefer composition over inheritance in system design** — services composed via APIs/events, not tightly coupled.
- **State assumptions explicitly** — unstated assumptions are the primary source of architecture failures.
- **NFRs must be quantified** — "fast" is not an NFR; "p99 latency under 200ms" is.
- **Data flows must be described** — if data moves between components, specify format, protocol, and error handling.
- **Security is not optional** — every design should address authentication, authorization, data protection, and audit.
- **Failure modes must be addressed** — what happens when each component fails? Circuit breakers, retries, fallbacks.
- **Respect user-provided specifications** — when a user provides an existing design or specification, the Architect must build on it. Proposing alternatives to settled design decisions is only permitted when a specific, documented technical blocker makes the original decision infeasible. The burden of proof is on the Architect to justify any deviation.

## Game Architecture Guardrails

- **Performance budgets are mandatory** — every system must declare its frame time, memory, and bandwidth budget.
- **Frame time awareness** — all designs must consider impact on the game loop; specify whether work runs per-frame, per-tick, or async.
- **Platform constraints must be stated** — minimum spec assumptions for PC, console generation, or mobile tier.
- **Scalability direction must be explicit** — player count, entity count, world size — what dimension scales?
- **Hot path identification** — mark critical paths that run every frame and must be optimized.
- **Memory allocation patterns** — prefer pooling and pre-allocation over runtime allocation in hot paths.
- **Determinism requirements** — state whether the system must be deterministic (critical for netcode, replays, save/load).

## Enforcement

The sub-agent prompt template (Phase 2 in parent SKILL.md) requires the sub-agent to produce trade-offs, assumptions, risks, and open questions. The guardrails above are the substantive checklist behind those structural slots — every guardrail violation in the artifact MUST be flagged in the review pass before the artifact returns to the orchestrator.
