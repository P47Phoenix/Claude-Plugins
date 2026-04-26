# ADR-005 — Pattern-Library Location: Centralised in `prompt-engineer/` with Citation-by-Name

**Status:** Accepted
**Date:** 2026-04-20
**Architect:** Celebrimbor
**Engagement:** Opus 4.6 → 4.7 Transformation Plan
**Related:** PRD REQ-02; Galadriel DX pillar P-2; Pattern sketch §4 (Patterns 4.1–4.6); Open Question 1 (Galadriel §7)
**Supersedes:** none
**Superseded-by:** none

---

## Context

Galadriel's DX design proposes six reusable 4.7-era patterns (Patterns 4.1–4.6) spanning versioned model references, role-prompt skeletons, manual CoT fallback, calibrated voicing, model-specific sub-sections, and forward-compatibility headers. The open question (Galadriel §7 Q1) is where the library physically lives:

- **Option A — Single home in `prompt-engineer/SKILL.md`** (centralised). Other skills cite by name.
- **Option B — Stubs in each plugin's `references/` citing `prompt-engineer/`** (distributed with hub-and-spoke).
- **Option C — Co-owned with `plugin-dev:*` skills** (outside this repo).

`prompt-engineer/SKILL.md` is already 440 LOC with seven existing patterns (PAT-01..PAT-07). It is the obvious home but currently lacks the 4.7-era patterns Galadriel named. `plugin-dev:*` skills live outside this repo (PRD §3.6) and are explicitly out-of-scope. The six in-scope plugins have no shared pattern surface today.

Past memory lesson (`feedback_dogfooding.md`, `feedback_route_through_po.md`): plans route through the PO and the team; changes are validated by use. A library that is harder to find is harder to use — distributed stubs risk drift if not maintained in lockstep.

## Decision

Adopt **Option A — centralised in `prompt-engineer/SKILL.md`** with **citation-by-name** from any SKILL.md that uses a pattern.

Specifically:

- **`prompt-engineer/SKILL.md` is the single home** for 4.7-era prompt patterns. Wave 3 edit (WI-05) adds Galadriel Patterns 4.1–4.6 to its body, each as a named sub-section (`### Pattern N.M — <name>`).
- **Every pattern gets a stable anchor** via markdown heading. Other SKILL.md files cite by path + anchor: `see prompt-engineer/SKILL.md#pattern-4-2-4-7-aware-role-prompt-skeleton`.
- **No other SKILL.md restates a pattern body.** A CI-able convention: `grep -rn '<thinking>' delivery-team/ mtg-commander/ research-agent/ agentic-flow-builder/ prd-quality-gate-flow/` should return only lines carrying a `prompt-engineer/SKILL.md` citation or be empty (Galadriel DX metric DX-M3).
- **The `plugin-dev:*` skill set (outside this repo) is consulted, not co-owned.** If plugin-dev's own skill-development guide teaches 4.7 patterns, our citations can reference theirs by URL; but our marketplace is self-contained — no repo file depends on a plugin-dev skill being installed.

## Consequences

- **Positive:** Single source of truth. A future pattern update (4.7 → 4.8) edits one file, not N. Satisfies Galadriel P-2 (Pattern-Library Singleton for 4.7-Sensitive Techniques).
- **Positive:** Citation-by-name creates a readable dependency graph — a reader of any SKILL.md can trace every 4.7-sensitive concept back to its definition in one hop.
- **Positive:** `prompt-engineer/` becomes the authoritative teaching surface for prompt craft in this marketplace. Reinforces its existing positioning as the repo's prompt-engineering skill.
- **Negative:** `prompt-engineer/SKILL.md` grows from 440 LOC to ~550 LOC (estimated +110 LOC for six patterns). Still well under the 1000+ LOC keystone band. Acceptable.
- **Negative:** Citations are text, not mechanically enforced. A reviewer must verify links by hand. Mitigation: Galadriel DX-M3 grep script is the enforcement layer; run pre-commit or in CI.
- **Negative:** If a pattern applies only to one plugin (e.g., mtg-commander's Challenger tone), centralising it in `prompt-engineer/` may feel misplaced. Mitigation: Pattern body lives in `prompt-engineer/`; plugin-specific instantiation lives in the plugin's own SKILL.md with a citation.

## Alternatives Considered

- **Option B (distributed stubs with citations).** Rejected: duplicates overhead without duplicating authority. Maintaining stubs-plus-source is strictly worse than source-only. If a future need emerges (e.g., an offline plugin distribution that loses the cross-reference), revisit.
- **Option C (co-owned with `plugin-dev:*`).** Rejected: `plugin-dev:*` skills are outside this repo (PRD §3.6) and the marketplace cannot depend on their installation. CLAUDE.md already names them as "consulted as authoring tools" — not as content dependencies.
- **Option D (new `patterns/` directory at repo root).** Rejected: violates PRD Constraint 2 (no architecture rewrite). A new top-level directory reshuffles the marketplace registry; our existing `prompt-engineer/` already has the semantics.
- **Option E (inline patterns in each SKILL.md, no central home).** Rejected: exactly the drift problem Galadriel P-2 warns against. PAT-01's current 4.6-era framing is a real-world example of what happens when patterns live in N places.

## Implementation Notes

- Wave 3 WI-05 (`prompt-engineer/SKILL.md` edit) scope includes:
  - PAT-01 re-frame (ADR-003).
  - New sub-sections for Patterns 4.1 (Versioned Model Reference), 4.2 (Role Prompt Skeleton), 4.3 (Manual CoT Fallback), 4.4 (Calibrated Instruction Voicing), 4.5 (Model-Specific Optimisation), 4.6 (Forward-Compatibility Header).
  - Stable anchor for each: `### Pattern 4.1 — Versioned Model Reference` etc.
- Citation format in other SKILL.md files: full path + anchor, e.g., `[Manual CoT Fallback](../../prompt-engineer/SKILL.md#pattern-4-3-manual-cot-fallback)`. Relative paths so the link resolves in GitHub rendering and editors.
- Galadriel DX-M3 (pattern-duplication count) is the post-implementation measurement. Target: 0 restatements outside `prompt-engineer/SKILL.md`.
- Future growth: if a seventh pattern emerges (e.g., from 4.8 migration), it appends in `prompt-engineer/SKILL.md` under a sibling heading. No architectural change required.

---

*"One library, many hands. Each ring-wearer knows where the forge stands — though they themselves need never swing the hammer. A citation is a lantern hung on the door; follow it, and the inscription is found."*

— Celebrimbor
