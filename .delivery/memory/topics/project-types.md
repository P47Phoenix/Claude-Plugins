# Project Type Patterns

**Entries**: 8 | **Last updated**: 2026-04-23

## GREENFIELD

- GREENFIELD pipelines benefit from all 7 stages at full depth. No stage felt unnecessary. Idea established scope, Refine tightened ACs, Design mapped FRs, Architect resolved open questions, Plan caught sizing issues, Dev delivered clean, UAT found real defects. (validated: 2, last: run-2026-04-12-hw01)
- Cross-plugin skill invocation should be verified at Refine (not deferred to Architect) when the entire architecture depends on it. hw01 adversarial challenger caught this at confidence 2/5. A 15-minute live test resolved it and prevented PRD rewrite. (validated: 1, last: run-2026-04-12-hw01)
- Plugin GREENFIELD projects produce primarily markdown + Python scripts. Calibrate estimates accordingly — markdown-heavy work is one tier lower than code. Sprint capacity planning confirmed this in hw01 (85% markdown, 15% Python). (validated: 1, last: run-2026-04-12-hw01)

## DESIGN + transformation-planning

- DESIGN project type with transformation-planning sub-workflow is the right fit for brownfield migration PLANNING (not implementation). End state is a roadmap artifact, not PRs. Route: Idea → Refine → Design (light if no UI surface) → Architect (transformation-planning). Plan/Dev/UAT skipped. (validated: 1, last: run-2026-04-20-o4v7)

- When the design surface is not a UI (e.g., skill-author DX, operator DX), Stage 3 runs LIGHT with a single artifact + 2-validator DoD (UX + PO). The "design" is a DX artifact: personas, pillars, authoring flows, pattern sketches, DX metrics, open questions. Feeds directly into Architect's TO-BE. Full stage would be over-ceremony. (validated: 1, last: run-2026-04-20-o4v7)

- Model-migration engagements (e.g., Opus 4.6→4.7) are a natural fit for this project type. PRD researches external model differences + repo-surface inventory; Architect produces AS-IS/TO-BE/Roadmap; implementation is a separate FEATURE engagement that inherits the plan. (validated: 1, last: run-2026-04-20-o4v7)

- For modest-scope transformation planning (≤ 10 plugins, ≤ 10k LOC), single transformation-plan.md + 4-6 ADRs beats the 4-phase document split. The 4-doc split earns its cost on multi-team brownfield. (validated: 1, last: run-2026-04-20-o4v7)

## BUG_FIX

- Consolidating 2-4 small open defects + follow-ups into one BUG_FIX sweep is more efficient than per-defect pipelines when they share a domain. Light DoD sufficient. (validated: 1, last: run-2026-04-11-g8h5)

## Documentation patterns

- Per-plugin ARCHITECTURE.md with Mermaid diagrams: Architect leads (not Tech Writer) when content is technical-structural; Tech Writer handles cross-links + diagram conventions. Pair similar plugins (e.g., agentic-flow-builder + prd-quality-gate-flow) for efficient parallel dispatch. (validated: 1, last: run-2026-04-11-h9i6)

- Detailed architecture flow docs work as a SUPPLEMENT to a high-level ARCHITECTURE.md (hard line cap). Use a `<plugin>/architecture/` subdirectory. Honor multi-author brainstorms via MERGE docs citing both contributors. (validated: 1, last: run-2026-04-11-i0j7)
