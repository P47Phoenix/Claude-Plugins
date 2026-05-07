# Development Stage — Memory

## Lessons Learned

- Consolidating 2-4 small open defects + follow-ups into one BUG_FIX sweep is more efficient than per-defect pipelines when they share a domain (here: delivery-flow wizard + scripts + CI). Light DoD sufficient. (validated: 1, last: run-2026-04-11-g8h5)
- Per-plugin ARCHITECTURE.md with Mermaid diagrams: Architect leads (not Tech Writer) when content is technical-structural; Tech Writer handles cross-links + diagram conventions. Pair similar plugins (e.g., agentic-flow-builder + prd-quality-gate-flow) for efficient parallel dispatch. (validated: 1, last: run-2026-04-11-h9i6)
- Detailed architecture flow docs work well as a SUPPLEMENT to a high-level ARCHITECTURE.md (which has a hard line cap). Use a `<plugin>/architecture/` subdirectory. Honor multi-author brainstorms via MERGE docs that cite both contributors. (validated: 1, last: run-2026-04-11-i0j7)
- **Mid-implementation reference-extraction is a clean budget-compensation mechanism.** When an in-body directive would breach the Tier-A 500-line ceiling, extracting the verbatim block to a reference file (e.g., `references/prose-style.md`) restores headroom without changing functional contract. Wave 2 doctrine-externalization pattern applies inside Stage 6, not just Stage 4 ADR authoring. At run-2026-05-05-tk3, initial 9-line Phase 4 Step 4 directive pushed SKILL.md to 506; compensating extraction restored to 500/500 exactly. (validated: 1, last: run-2026-05-05-tk3)
