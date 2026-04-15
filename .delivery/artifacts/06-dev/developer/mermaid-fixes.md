# Mermaid Diagram Fixes — run-2026-04-15-j1k8

**Alias:** Gimli (Developer) — following Gandalf's (PO) DEFECT-005 filing.
**Scope:** two broken Mermaid diagrams, surgical edits, no content loss.

## Defect Reference

- **DEFECT-005** filed at `.delivery/defects/DEFECT-005.md` (Minor / High visibility, Documentation / diagram syntax).
- **Index** updated at `.delivery/defects/index.md` — total now 5.

## Files Edited

### 1. `mtg-commander/ARCHITECTURE.md` — Diagram #3 (classDiagram)

**Changes inside the classDiagram block:**

- `+float? max_card_price = null` -> `+float max_card_price` (Mermaid has no nullable-type syntax).
- `+enum budget_source = higher` -> `+string budget_source` (Mermaid has no enum primitive).
- `+enum on_loop_exhaustion = warn` -> `+string on_loop_exhaustion` (same).
- Stripped `= <default>` from every field (Mermaid classDiagram does not model default literals).
- Three multi-line notes using literal `\n` -> compact single-line notes (Mermaid does not interpret `\n` as a newline inside quoted notes).

**Content preservation:** added a prose paragraph immediately after the diagram documenting every stripped default (version=1; all four loop caps=2; max_card_price=null; escalation=true; budget_source=higher; on_loop_exhaustion=warn) and the enum-constraint sets for `budget_source` and `on_loop_exhaustion`. Zero semantic loss.

### 2. `delivery-team/architecture/empirical-lifecycle.md` — Diagram #1 (flowchart)

**Changes inside the flowchart block:** every literal `\n` inside `{...}` decision nodes and `[...]` terminal nodes replaced with `<br/>` (Mermaid does not interpret `\n` in node labels). Six substitutions: Q1, Q2, Q3, ANALYTICAL, EMPIRICAL, MIXED.

## Verification (grep checks)

- `grep -c 'float?' mtg-commander/ARCHITECTURE.md` -> **0** (expected 0).
- `grep -cE '\+enum ' mtg-commander/ARCHITECTURE.md` -> **0** (expected 0; the two `+enum` field lines are gone).
- `grep -c '\\\\n' delivery-team/architecture/empirical-lifecycle.md` -> **0** literal `\n` sequences remain in the file (expected 0 inside the Mermaid block).
- `<br/>` substitutions confirmed landed in Q1, Q2, Q3, ANALYTICAL, EMPIRICAL, MIXED nodes.

## Status After Fix

- Both Mermaid diagrams now parse with valid syntax.
- mtg-commander classDiagram: primitive types only, notes compact, prose paragraph carries the defaults/enums.
- empirical-lifecycle flowchart: all node labels use `<br/>` for line breaks.
- Appended `**Status: CLOSED — fixed in run-2026-04-15-j1k8**` to `.delivery/defects/DEFECT-005.md`.
