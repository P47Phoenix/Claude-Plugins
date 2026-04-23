# BACKLOG-47-migration-guide-stub: Publish a 4.6 → 4.7 migration guide stub

**Label:** backlog-47
**Status:** deferred
**Created:** 2026-04-22
**Engagement:** run-2026-04-22-4x7e
**Source anchors:**
- Galadriel on-ramp pillar P-1 (migration recipe surfaced for future model bumps)
- Transformation-plan artifacts under `.delivery/artifacts/04-architect/`
- PRD Section 3 findings (F-01 through F-28 — the raw material)

## Context

This engagement produced a transformation plan, six ADRs, and a fresh-challenger loop that collectively encode the recipe for a 4.6 → 4.7 migration. That knowledge currently lives in `.delivery/artifacts/` — excellent for traceability, suboptimal for discoverability. The next model bump (4.7 → 4.8 or 5.0) will re-solve most of these questions from scratch if the recipe isn't distilled into a guide.

Galadriel pillar P-1 recommended a short, standalone migration guide at `docs/migrations/4.6-to-4.7.md` (or similar) that captures: what changed in the model, which patterns needed updating, what we deferred (this backlog label!), and the process we used. This item is that stub.

## Proposed scope

- Create `docs/migrations/4.6-to-4.7.md` (path negotiable) containing:
  - **What changed** — succinct summary of the ≤10 findings that drove migration work (F-01 API ID, F-11 `budget_tokens` → 400, F-12 adaptive thinking default off, F-18/19 new features, F-22 cyber-safeguard, F-25 prose landmines, F-28 over-pressure).
  - **What we did** — enumerate the waves of work and the ADRs that resulted.
  - **What we deferred** — link to this backlog label (`gh issue list --label backlog-47`).
  - **The playbook** — the Refine→Architect→Execute process we followed, so the next migration can reuse it.
- Link the guide from CLAUDE.md.
- Keep it ≤500 lines; this is a recipe, not a textbook.

## Out of scope for this item

- Re-litigating any of the 4.7 findings; the guide distills existing artifacts.
- Model-bump automation or tooling (a possible much-later item).
- Migration guides for other model families (non-Opus lines).

## Success criteria

- `docs/migrations/4.6-to-4.7.md` exists, is linked from CLAUDE.md, and passes a fresh-eyes review ("could someone who wasn't in the engagement run the same migration from this doc?").
- The guide links to ≥6 ADRs and to the `backlog-47` label.
- A future model-bump engagement can cite this doc as the template.

## Priority & effort (rough)

- Priority: low
- T-shirt: S (distillation, not new thinking).
- Depends on: engagement completion (all ADRs must be finalised).
