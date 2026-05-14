# Project Type Patterns

**Entries**: 12 | **Last updated**: 2026-04-23

## GREENFIELD

- GREENFIELD pipelines benefit from all 7 stages at full depth. No stage felt unnecessary. Idea established scope, Refine tightened ACs, Design mapped FRs, Architect resolved open questions, Plan caught sizing issues, Dev delivered clean, UAT found real defects. (validated: 2, last: run-2026-04-12-hw01)
- Cross-plugin skill invocation should be verified at Refine (not deferred to Architect) when the entire architecture depends on it. hw01 adversarial challenger caught this at confidence 2/5. A 15-minute live test resolved it and prevented PRD rewrite. (validated: 1, last: run-2026-04-12-hw01)
- Plugin GREENFIELD projects produce primarily markdown + Python scripts. Calibrate estimates accordingly — markdown-heavy work is one tier lower than code. Sprint capacity planning confirmed this in hw01 (85% markdown, 15% Python). (validated: 1, last: run-2026-04-12-hw01)

## DESIGN + transformation-planning

- DESIGN project type with transformation-planning sub-workflow is the right fit for brownfield migration PLANNING (not implementation). End state is a roadmap artifact, not PRs. Route: Idea → Refine → Design (light if no UI surface) → Architect (transformation-planning). Plan/Dev/UAT skipped. (validated: 1, last: run-2026-04-20-o4v7)

- When the design surface is not a UI (e.g., skill-author DX, operator DX), Stage 3 runs LIGHT with a single artifact + 2-validator DoD (UX + PO). The "design" is a DX artifact: personas, pillars, authoring flows, pattern sketches, DX metrics, open questions. Feeds directly into Architect's TO-BE. Full stage would be over-ceremony. (validated: 1, last: run-2026-04-20-o4v7)

- Model-migration engagements (e.g., Opus 4.6→4.7) are a natural fit for this project type. PRD researches external model differences + repo-surface inventory; Architect produces AS-IS/TO-BE/Roadmap; implementation is a separate FEATURE engagement that inherits the plan. (validated: 1, last: run-2026-04-20-o4v7)

- For modest-scope transformation planning (≤ 10 plugins, ≤ 10k LOC), single transformation-plan.md + 4-6 ADRs beats the 4-phase document split. The 4-doc split earns its cost on multi-team brownfield. (validated: 1, last: run-2026-04-20-o4v7)

## FEATURE (execution of approved transformation plan)

- **When a DESIGN pipeline's terminus is a transformation plan, the execution engagement runs as a FEATURE** — not a new GREENFIELD or a new DESIGN. Inputs are the plan + ADRs + upstream PRD; the FEATURE pipeline's Refine (light) decomposes the plan's WIs into Sprint stories rather than re-authoring requirements. Used namespace `08-execute/` to preserve upstream `01-idea/` through `04-architect/` artifacts verbatim. (validated: 1, last: run-2026-04-22-4x7e)

- **Stage 3 Design skipped is a valid routing deviation for DX-only migrations.** No UX surface means no user flows, wireframes, component specs. Record the skip at state-entry with reason ("DX-only routing deviation"); do not conflate with silent fusion (R-09). (validated: 1, last: run-2026-04-22-4x7e)

- **Per-wave commit cadence is defensible for mechanically-independent WI batches.** 14 WIs in 4 waves with deterministic wave-exit gates: per-wave commits (4 total) trade per-WI revert-granularity for audit-trail readability on the winning side. Pair with a Tier-1b partial-wave surgical-revert procedure to close the granularity gap. Rule of thumb: per-WI commits for behaviourally-coupled WIs; per-wave commits for mechanically-independent batches. (validated: 1, last: run-2026-04-22-4x7e)

- **Honest readiness markers beat uniform readiness markers.** When migration scope splits across prose-reviewed keystones and mechanical backfills, use a two-tier stamp (`opus-4-7` vs `opus-4-7-frontmatter-only`) so a future reader can tell them apart. Pair with a backlog item tracking the upgrade path; do NOT mechanically restamp in a sweep. (validated: 1, last: run-2026-04-22-4x7e)

- **FEATURE-execution-of-pre-planned-waves with binding-decisions-in-memory pattern**: when a multi-wave initiative pre-loads its conflict rulings + per-skill model map + tier values into a memory topic file (e.g., `topics/skill-token-economy.md`), the FEATURE pipeline runs WITHOUT re-debating decisions during stage execution. At run-2026-05-03-tk0e Wave 0, 4 of 7 stages passed first-try DoD; at run-2026-05-04-tk1 Wave 1, similar 5/9 stage-stories first-try with 2 real defects caught and 1 false-positive corrected. Wave 3 (run-2026-05-09-tk4) closed the initiative with 5 binding rulings preserved through 5 waves and zero ruling-loss. Action: for any multi-wave initiative, author a `topics/<initiative>.md` memory file BEFORE invoking delivery-flow; treat it as binding context. tk5 promoted the pattern with a DEFERRED-gate honest-readiness-marker variant: when a live-execution gate fails on a dogfooding-discovered constraint (auth-isolation, env-bound), the team's call is PARTIAL_READY + follow-up BACKLOG, not blocking the merge. (validated: 6, last: run-2026-05-13-tk5)

- **Story consolidation by file scope (not by WI count) is the right pattern for FEATURE-execution-of-pre-planned-waves.** When a wave has N mechanically-independent WIs and M < N file-scope groups, collapse into M stories rather than dispatching N separate developer implementations. Wave 1 (run-2026-05-04-tk1) had 7 WIs collapsed into 3 file-scope stories. Wave 2 (run-2026-05-05-tk2) had 8 WIs collapsed into 5 file-scope stories. Wave caveman-lite (run-2026-05-05-tk3) is the canonical 3-WI-into-1-story example. Wave 3 (run-2026-05-09-tk4) collapsed 18 WIs into 7 stories with zero AC drops verified by QA traceability. Same DoD coverage, ~40-50% fewer Agent dispatches. tk5 collapsed 8 WIs into 3 file-scope stories with a deliberate two-dispatch split (producer-validator separation for validator-style artifacts). (validated: 6, last: run-2026-05-13-tk5)

- **Honest partial-compliance rulings work for budget-constrained refactors.** When a target file's required line reduction exceeds what the current wave's extraction plan can deliver (e.g., architect Tier-B 300-line target but only 175 lines of extractable content), the right call is: accept partial compliance against a higher tier (Tier-A 500), explicitly document the residual debt with target_wave=<next>, and surface the math in the PRD. Wave 2 ruling: architect 500 (Tier-A ceiling met; Tier-B 200-line residual deferred to Wave 3) — caught at Stage 2 Refine via Dev runs-the-command discipline. PO + PRD + ADR + retro all aligned on partial-compliance language. Pattern preserves audit trail integrity over scope-pressure overclaiming. (validated: 1, last: run-2026-05-05-tk2)

## BUG_FIX

- Consolidating 2-4 small open defects + follow-ups into one BUG_FIX sweep is more efficient than per-defect pipelines when they share a domain. Light DoD sufficient. (validated: 1, last: run-2026-04-11-g8h5)

## Documentation patterns

- Per-plugin ARCHITECTURE.md with Mermaid diagrams: Architect leads (not Tech Writer) when content is technical-structural; Tech Writer handles cross-links + diagram conventions. Pair similar plugins (e.g., agentic-flow-builder + prd-quality-gate-flow) for efficient parallel dispatch. (validated: 1, last: run-2026-04-11-h9i6)

- Detailed architecture flow docs work as a SUPPLEMENT to a high-level ARCHITECTURE.md (hard line cap). Use a `<plugin>/architecture/` subdirectory. Honor multi-author brainstorms via MERGE docs citing both contributors. (validated: 1, last: run-2026-04-11-i0j7)
