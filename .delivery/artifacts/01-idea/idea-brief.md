# Idea Brief — Alias Theme Not Injected into Agent Prompts

| Field | Value |
|-------|-------|
| **GitHub Issue** | #58 |
| **Type** | BUG_FIX |
| **Priority** | P1 — Core personality feature is non-functional |
| **Date** | 2026-04-04 |

## Problem Statement

The alias system promises personality injection into every agent the orchestrator dispatches. The promise is broken. When a user configures `aliases.theme: lotr` with `personality_strength: full`, the LOTR alias theme loads correctly in Phase 0, the orchestrator announces it — and then proceeds to ignore it for the vast majority of agent invocations.

Three failure modes have been observed:

1. **Partial injection** — A handful of agents receive hand-written personality fragments (missing catchphrase, style, or examples), violating the `personality_strength` contract.
2. **No injection** — Most agents (DoD validators, supporting agents, secondary dispatches) receive no personality whatsoever. They speak in default professional tone despite an active theme.
3. **Missing template structure** — The formal `--- ALIAS ---` block documented in SKILL.md Phase 4 Step 4 is never actually used. The orchestrator constructs prompts ad-hoc because `pipeline-stages.md` contains no Agent Invocation Template with an `--- ALIAS ---` placeholder.

**Root cause**: SKILL.md defines the alias injection protocol (Phase 4 Step 4), and `team-patterns.md` includes `--- ALIAS ---` blocks in collaboration pattern templates (Evaluator-Optimizer, Adversarial Review, Debate, Consensus, etc.). However, `pipeline-stages.md` — which defines the templates for *primary agent dispatch*, *supporting agent dispatch*, and *DoD validator dispatch* across all 7 stages — contains zero references to `ALIAS`, personality, or alias injection. The orchestrator has no template to follow for the most common dispatch paths.

## Target Users

- Any delivery-team user who configures a non-business alias theme and expects consistent personality across the full pipeline run.

## Goals

1. Every agent dispatched by the orchestrator — primary, supporting, and validator — receives the `--- ALIAS ---` block when a theme is active.
2. The personality content matches the configured `personality_strength` level (light / moderate / full) exactly as specified in SKILL.md Phase 4 Step 4.
3. The fix is structural (template-level), not behavioral (hoping the orchestrator remembers).

## Scope

### In Scope

- Add a standardized Agent Invocation Template to `pipeline-stages.md` that includes the `--- ALIAS ---` block for all dispatch types: primary agents, supporting agents, and DoD validators.
- Ensure the template structure aligns with the existing `--- ALIAS ---` pattern already established in `team-patterns.md`.
- Verify consistency with the alias injection protocol in SKILL.md Phase 4 Step 4.

### Out of Scope

- New alias themes or theme content changes.
- Changes to the alias loading logic in Phase 0 (that part works correctly).
- Changes to `team-patterns.md` collaboration templates (those already have the block).
- UI or notification changes.

## Acceptance Criteria

| # | Criterion | Validation |
|---|-----------|------------|
| AC-1 | `pipeline-stages.md` contains an Agent Invocation Template with `--- ALIAS ---` block for primary agent dispatch | Grep confirms `--- ALIAS ---` present in pipeline-stages.md |
| AC-2 | `pipeline-stages.md` contains `--- ALIAS ---` block for supporting agent dispatch | Grep confirms block in supporting agent template |
| AC-3 | `pipeline-stages.md` contains `--- ALIAS ---` block for DoD validator dispatch | Grep confirms block in validator template |
| AC-4 | Template alias block references the personality_strength protocol from SKILL.md Phase 4 Step 4 | Manual review of template content |
| AC-5 | Dogfooding: run a BUG_FIX pipeline with `aliases.theme: lotr`, `personality_strength: full` and confirm all dispatched agents display LOTR personality | UAT with live pipeline execution |
