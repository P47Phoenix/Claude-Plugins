# Architecture — Configurable Architecture Board Review Pattern

*Forged by Celebrimbor of the Gwaith-i-Mírdain, Stage 4 Architect (light). Run: run-2026-04-08-b2c7.*

## 1. Context

The existing Multi-Perspective Review Board in `delivery-team/skills/delivery-flow/references/team-patterns.md` (Pattern 3, line 334) is frozen to a fixed Technical/Business/Risk trio. PRD FR-1..FR-8 demand a configurable roster, a persona library, a judge, MAR-style iteration-2 cross-persona routing (BACKLOG-002 absorbed), and Stage 4 Architect integration — without breaking callers that know it not.

## 2. `architecture_board` Config Schema

Added to `delivery-team/skills/delivery-flow/references/config-schema.md` under a new top-level optional block. Absent block = disabled (NFR-2).

```yaml
architecture_board:
  enabled: false
  reviewers:
    - volatility-architect
    - ddd-architect
    - risk-architect
  max_iterations: 2
  convergence: all-done        # all-done | judge-pass | majority-pass
  judge: chief-architect
  cross_persona_iteration2: true
```

Ceilings: `max_iterations ≤ 3`, `len(reviewers) ≤ 6` (NFR-1 token cap).

## 3. Persona Library File Structure

Single file: `delivery-team/skills/delivery-flow/references/architecture-board-personas.md`. Each persona is one H2 section:

```
## <persona-id>
- id: volatility-architect
- name: Volatility Architect
- perspective: "Decompose along axes of change, per Lowy's Golden Rule"
- context-files-to-load:
    - delivery-team/skills/architect/references/volatility-strategy.md
    - .delivery/artifacts/04-architect/solution/architecture.md
- review-prompt-template: |
    You are the {name}. Evaluate architecture.md solely through {perspective}.
    Apply gate-criteria below. Emit signal-format verbatim.
- gate-criteria:
    - Every service boundary aligns with a volatility axis
    - No functional decomposition leakage
- signal-format: |
    VERDICT: PASS | CONDITIONAL | BLOCK
    FINDINGS: - <bullet>
    CITATIONS: - <file:line>
```

## 4. Judge Persona Structure

Same file, one H2 marked `## chief-architect (judge)`, with: synthesis protocol (cite each reviewer's findings individually; declare per-finding agreement; emit aggregated verdict), deadlock rule (links to `team-patterns.md` Pattern 4 Debate DEADLOCK), final verdict schema `{PASS | CONDITIONAL | BLOCK, synthesized_findings[], dissent[]}`. Full protocol in ADR-002.

## 5. `team-patterns.md` Augmentation

New section **Pattern 3b: Configurable Architecture Board** inserted immediately after Pattern 3 (line 416), referencing but not replacing it. Protocol:

1. Orchestrator reads `architecture_board` from config; if `enabled: false`, skip.
2. Dispatch each persona in `reviewers` as a parallel sub-agent (single message, isolated context per NFR-3).
3. Each writes `.delivery/artifacts/04-architect/board/<persona-id>-review.md`.
4. Judge sub-agent reads all N paths, writes `.delivery/artifacts/04-architect/board/judge-verdict.md`.
5. Loop per `convergence` until `max_iterations` or verdict PASS.

Triggers: Stage 4 Architect only (MVP). Loop rules: any BLOCK verdict → correction round; iteration 2 applies §7 routing.

## 6. `pipeline-stages.md` Stage 4 Integration

New sub-step **2b. Architecture Board Review** inserted after step 2 (Invoke Architect, line 355) and before Team DoD Validation. Conditional on `architecture_board.enabled`. On BLOCK, orchestrator triggers self-correction loop against the primary architect.

## 7. MAR Iteration-2 Cross-Persona Routing

On round 2 of self-correction, the orchestrator selects a *different* persona from `reviewers` (round-robin, skipping the round-1 reviewer whose BLOCK triggered correction) to review the corrected `architecture.md`. Absorbs BACKLOG-002. Disabled by `cross_persona_iteration2: false`.

## 8. Non-Goals (LIGHT)

- No changes to the existing fixed Multi-Perspective Review Board (Pattern 3 stays).
- No integration beyond Stage 4 Architect (Plan/Dev stages out of scope).
- No dynamic persona generation — library is curated Markdown.
- No automated token-budget enforcement beyond documented ceilings.

## 9. Risks (blocking only)

- **Persona echo chamber** — mitigated by FR-3 distinct `perspective` lines + reviewer-set overlap warning (deferred).
- **Judge deadlock** — fallback: invoke existing debate pattern's DEADLOCK handler in `team-patterns.md` Pattern 4.

*"A ring of three voices is stronger than a single hammer; but only if each voice sings a different note."* — C.
