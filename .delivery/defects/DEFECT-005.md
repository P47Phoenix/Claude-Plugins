# DEFECT-005: Broken Mermaid diagrams in architecture docs

**Pipeline**: run-2026-04-15-j1k8
**Severity**: Minor (docs; does not break functionality) but **High visibility** (contributor-facing; PO-flagged)
**Category**: Documentation / diagram syntax
**Logged by**: Gandalf (PO)
**Fixed by**: Gimli (Developer) — same pipeline run

---

## Description

Two Mermaid diagrams embedded in architecture docs contain invalid syntax that either fails to render or renders with visible escape artefacts. Both stem from the same class of authoring error: agents that produced these diagrams used `\n` as if it were a universal escape sequence for newlines, but Mermaid (and Markdown-embedded Mermaid) does NOT process backslash escapes in label text. A secondary issue in the mtg-commander diagram is the use of programmer-language type syntax (nullable `?`, `enum`) in a Mermaid classDiagram, which has a much simpler primitive type model.

---

## Issue 1 — `mtg-commander/ARCHITECTURE.md` classDiagram (Diagram #3)

Three syntax problems in the classDiagram block (lines ~98–127):

1. **`+float? max_card_price = null`** — the `?` nullable suffix is not valid Mermaid classDiagram type syntax. Mermaid classDiagram supports primitive types (`int`, `float`, `string`, `bool`) without nullable modifiers. Defaults of `null` cannot be expressed in the type position.
2. **`+enum budget_source = higher`** (and `+enum on_loop_exhaustion = warn`) — `enum` is not a valid Mermaid primitive. Mermaid parses `enum` as the type name (not a keyword), which at best renders oddly and at worst breaks the class definition. Mermaid does not model enum constraints; the allowed-values constraint belongs in a note or in prose.
3. **`note for X "text with \n in it"`** — the literal `\n` inside a quoted note string does NOT render as a newline in Mermaid. It renders as the two-character sequence `\` + `n`. Multi-line notes need actual newlines or `<br>` (support varies across renderers).

---

## Issue 2 — `delivery-team/architecture/empirical-lifecycle.md` flowchart (Diagram #1)

Decision nodes and terminal nodes contain literal `\n` inside the node-label shapes:

- `Q1{Can a static check verify it?\n schema / grep / parse / compile}`
- `Q2{Can a deterministic script verify it?\n fixture diff / CLI exit code}`
- `Q3{Requires human or runtime observation?\n render / playtest / telemetry}`
- `ANALYTICAL[Analytical AC\nverify at Dev]`
- `EMPIRICAL[Empirical AC\ndefer to UAT]`
- `MIXED[Mixed AC\nsplit structural vs behavioural]`

Mermaid flowchart labels do NOT interpret `\n` as a newline — it renders as literal `\n`. Correct approach: use `<br/>` for line breaks inside node labels.

---

## Root Cause

Common root cause across both diagrams: authoring agents treated `\n` as if it were a universally interpreted escape sequence for newlines. Mermaid does not process backslash escapes in label text. For multi-line labels, Mermaid's idioms are:

- **Flowchart node labels (`[...]`, `{...}`, `(...)`):** use `<br/>` for line breaks.
- **classDiagram notes:** use actual newlines inside the quoted string, or avoid multi-line notes altogether by keeping note text compact.
- **Primitive types in classDiagram:** stick to `int`/`float`/`string`/`bool`. Express nullability, defaults, and enumerated allowed-values in prose, notes, or trailing comments — not in the type position.

---

## Proposed Fix

See Gimli's fix log at `.delivery/artifacts/06-dev/developer/mermaid-fixes.md`. Summary:

- **`mtg-commander/ARCHITECTURE.md`** — drop nullable `?`, replace `enum` with `string`, strip defaults from type positions, compress notes to single-line, and add a brief prose paragraph immediately after the diagram documenting the defaults that were stripped (version=1; deck_builder/rules_judge/optimizer/price_evaluator default=2; max_card_price default=null; escalation default=true; budget_source default=higher; on_loop_exhaustion default=warn).
- **`delivery-team/architecture/empirical-lifecycle.md`** — replace every `\n` inside `{...}` and `[...]` node labels with `<br/>`.

---

## Status: CLOSED — fixed in run-2026-04-15-j1k8
