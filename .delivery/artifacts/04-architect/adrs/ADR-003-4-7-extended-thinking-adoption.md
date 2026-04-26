# ADR-003 — Extended-Thinking Adoption Strategy: Document-Only, Defer Adoption

**Status:** Accepted
**Date:** 2026-04-20
**Architect:** Celebrimbor
**Engagement:** Opus 4.6 → 4.7 Transformation Plan
**Related:** PRD F-11, F-12, F-13, F-14, F-15, F-29; REQ-02 AC-02.2; Galadriel DX pillar P-3
**Supersedes:** none
**Superseded-by:** none

---

## Context

Adaptive thinking is the only supported thinking-on mode on Opus 4.7 (F-11). `thinking: {"type": "enabled", "budget_tokens": N}` returns 400. Adaptive thinking is off by default on 4.7 (F-12). Thinking content is omitted by default — the field is empty unless `display: "summarized"` is set (F-13). The `xhigh` effort lever is new (F-15) and Claude Code's default is already raised to `xhigh`. `<thinking>` tags remain valid as a manual CoT scaffold in few-shot examples (F-29).

Two scopes where 4.7 thinking could land in this repo:

1. **SKILL.md prose that teaches or references thinking behaviour** — `prompt-engineer/SKILL.md` PAT-01 (line 85) conflates `<thinking>` tags with reasoning visibility, which is inaccurate on 4.7. Other SKILL.md files do not mention thinking behaviour programmatically.
2. **API call sites that set `thinking` or `effort` parameters** — zero such call sites exist in this repo (PRD §3.1.1 SDK-import check).

## Decision

**Document-only adoption, in scope for this engagement. No runtime adoption of `thinking`/`effort` parameters, which is out of scope per PRD Non-Goals and Constraint 1.**

Specifically:

- **`prompt-engineer/SKILL.md` PAT-01 re-frame (Wave 3 edit, REQ-02 AC-02.2):** Re-word line 85 to cite `<thinking>` tags as a *manual CoT scaffold for few-shot examples* (F-29), not a reasoning-visibility mechanism. Add a new "Model-specific optimisation — Claude Opus 4.7" sub-section (Galadriel Pattern 4.5) that documents: (a) adaptive thinking is the only supported thinking-on mode and is off by default, (b) `xhigh` effort is the recommended default for coding/agentic use cases on 4.7, (c) `temperature`/`top_p`/`top_k` non-default ⇒ 400, (d) `budget_tokens` ⇒ 400.
- **No other SKILL.md is edited to add adaptive-thinking guidance.** The Galadriel P-3 "fail-soft on older / different models" pillar means SKILL.md files stay model-agnostic in their core instructions. Thinking is mentioned only where the skill's purpose is to teach prompt techniques (i.e., `prompt-engineer/` only).
- **No API call site is introduced.** The `task_budget` beta header and `memory` tool (F-18, F-19) are explicitly logged as NEW backlog (REQ-07), not absorbed into migration.

## Consequences

- **Positive:** Scope is contained to one SKILL.md file (`prompt-engineer/`). The rest of the marketplace remains model-agnostic — consistent with Galadriel P-3 and PRD non-goal on "no architecture rewrite."
- **Positive:** When Claude Code itself raises its default effort to `xhigh`, the repo benefits automatically without any local change.
- **Positive:** `<thinking>` tags retained in PAT-02, PAT-06 as manual CoT fallback — aligned with F-29, which explicitly endorses them for few-shot prompting.
- **Negative:** `prompt-engineer/SKILL.md` becomes 4.7-aware before other teaching surfaces. Acceptable: it is the *only* teaching surface that references thinking mechanics (PRD §3.3 confirmed no other file carries API-shape thinking patterns).
- **Negative:** Future 4.8 migration will re-touch the "Model-specific optimisation — Claude Opus 4.7" sub-section. Galadriel Pattern 4.5 deliberately isolates model-specific content in one sub-section per model, making the future edit a single-section swap rather than a file-wide hunt.

## Alternatives Considered

- **Adopt `xhigh` effort programmatically in agentic-flow-builder's `agent_registry.py`.** Rejected: violates PRD Non-Goal ("no net-new features" — introducing effort-setting is a new behaviour, not migration). Logged as BACKLOG candidate if/when SDK wiring lands.
- **Remove `<thinking>` tags from PAT-02, PAT-06 as "4.7 has adaptive thinking."** Rejected: F-29 explicitly endorses manual CoT as a fallback technique. The two concepts are distinct (API-level adaptive thinking is opaque by default; prompt-level `<thinking>` is a manual scaffold). Removing would degrade the pattern library for model-agnostic contexts.
- **Add a "4.7-era thinking sub-section" to every SKILL.md.** Rejected: violates Galadriel P-3 (fail-soft). Not every skill needs to teach thinking; most SKILL.md files describe behaviour, not knobs.

## Implementation Notes

- PAT-01 re-frame and new sub-section land together in the Wave 3 `prompt-engineer/SKILL.md` edit (WI-05).
- The new sub-section carries the P-1 header strip convention (ADR-006): if `last_audited: 2026-05-01` and `pattern_library_version: 4-7-1`, a future 4.8 migration bumps both.
- The PRD's existing language "on Opus 4.7" prefix (Galadriel Pattern 4.5 anti-pattern) is the linter target: grep for `adaptive thinking` / `xhigh` / `budget_tokens` across all SKILL.md files; each occurrence must live under a "Model-specific optimisation" sub-section or carry an "on Opus 4.7:" prefix.

---

*"A thinking-blade unused is no different from a thinking-blade unmade. We describe it for those who would wield it; we do not take it up ourselves in this forging."*

— Celebrimbor
