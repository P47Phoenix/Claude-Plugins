# ADR-002: Router Detection Priority Chain

**Status:** Proposed
**Date:** 2026-04-10
**Deciders:** Celebrimbor (Architect), Gandalf (PO)
**Pipeline:** run-2026-04-10-d5e2 (FEATURE XL)
**Traced to:** FR-3; roadmap STEP-02, STEP-03

---

## Context

The architect SKILL.md must detect which decomposition paradigm to use when a `decompose` or `design` task arrives. Multiple signals can indicate the paradigm: the user's explicit words, the project's `.delivery/config.yml` setting (`architecture.decomposition`), and the characteristics of the problem domain. These signals may conflict -- a config says `ddd` but the user says "decompose by volatility." A deterministic priority chain is needed to resolve conflicts without asking the user every time.

The business rules engine pattern established in this codebase mandates that gate decisions be rule-based and deterministic, not AI-inferred. The detection priority must follow this principle.

---

## Decision

Detection priority for paradigm selection is:

1. **Explicit user intent** -- If the user's prompt contains an unambiguous paradigm reference ("use volatility", "DDD decomposition", "IDesign"), that paradigm is selected. User intent overrides all other signals.
2. **Config value** -- If no explicit intent is detected, read `architecture.decomposition` from `.delivery/config.yml`. If set to a specific paradigm (`volatility`, `ddd`, `team-topology`, `event-storming`, `business-capability`), use it.
3. **Decision matrix** -- If config is `auto` or absent, evaluate the decision matrix inputs (`domain_complexity`, `change_rate`, `team_size`, `deploy_independence`) from config or prompt context to recommend a paradigm.

At each level, if the signal is present and unambiguous, routing is immediate -- no further levels are consulted. If ambiguous at any level, fall through to the next.

---

## Consequences

### What becomes easier

- **User override is frictionless** -- a user who knows they want volatility simply says so. No config change needed for a one-off override.
- **Config provides stable defaults** -- teams that always use DDD set it once and forget it. Every pipeline run uses DDD unless explicitly overridden.
- **Decision matrix remains available** -- teams that do not know which paradigm to use get a recommendation based on project characteristics, without needing to understand paradigm theory.
- **Determinism** -- given the same inputs, the same paradigm is selected. No AI variance in routing.

### What becomes harder

- **Implicit config override** -- a user who says "decompose this" with `decomposition: ddd` in config will get DDD, not a decision-matrix recommendation. If they wanted the matrix, they must set `decomposition: auto`. This is intentional but may surprise users who forget their config.
- **Decision matrix accuracy** -- the matrix is a heuristic. It may recommend volatility when DDD would be better. Mitigation: the matrix is a starting point, not a gate. Users can override at level 1.

---

## Alternatives Considered

| Alternative | Pros | Cons | Why Rejected |
|-------------|------|------|--------------|
| **(a) Config-only** (no user override, no matrix) | Simplest implementation; fully deterministic | No runtime flexibility; user must edit config to change paradigm per-task; friction for exploratory work | Too rigid; violates the principle that user intent should be honoured |
| **(b) AI-inferred from PRD** (analyse problem statement, pick paradigm) | Zero-config; feels intelligent | Non-deterministic; same PRD may route to different paradigms across runs; violates business rules engine pattern; untestable | Determinism is a hard requirement per `as-is-constraints.yml` and business rules engine conventions |
| **(c) Always ask the user** (prompt before every decomposition) | Maximum user control; no wrong guesses | Friction on every decomposition task; blocks automation; incompatible with light-mode stages where depth is reduced | Excessive friction; most teams know their paradigm and set it in config once |
| **(d) Config overrides user** (config > explicit intent) | Config is authoritative; no surprise overrides | User cannot override without editing config; poor DX for exploration and learning; breaks the "explicit is better than implicit" principle | User intent should be supreme -- the human at the keyboard knows what they want right now |

---

## References

- `as-is-constraints.yml`: business rules engine pattern (deterministic gate decisions)
- SKILL.md lines 132-178: existing decomposition strategy routing table and decision matrix
- `constraints.yml` (Refine): invariant "No new config keys introduced"
- PRD FR-3: architect SKILL.md paradigm router detection logic
