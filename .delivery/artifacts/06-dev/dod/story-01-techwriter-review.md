# Tech Writer DoD Review — Story 01: Architect SKILL.md

**Reviewer:** Bilbo (Technical Writer, Operations)
**Date:** 2026-04-04
**Artifact:** `/home/meconnelly/.claude/plugins/marketplaces/mec-claude-agent-skills/delivery-team/skills/architect/SKILL.md`

---

> "I think I'm quite ready for another documentation adventure." And what a journey this was — 613 lines of architectural chronicle, covering 11 roles, 4 decomposition strategies, game and software domains, and a Prior Art Analysis protocol that would make any cartographer proud.

---

## Criterion 1: Inline Documentation Present for Non-Obvious Logic

**Verdict: PASS**

The document explains the "why" behind non-obvious design choices thoroughly:

- **Role Context Isolation** (lines 9-11): Explains why architecture knowledge is kept out of the main context window — the sub-agent is the execution boundary.
- **Godot pattern** (lines 14-15): Explains the multi-reference loading pattern and why it differs from the developer skill's single-reference approach. The name "godot pattern" is internal jargon, but it is explained in context.
- **Prior Art Analysis conditional execution** (line 36): The "ONLY when" condition is clearly documented with specific examples of what counts as user-provided specs.
- **Classification rules** (lines 58-61): The distinction between "Decision Already Made" and "Open Question" is explicitly defined with classification rules and worked examples.
- **Deviation Protocol burden of proof** (lines 69-74): Explains the rationale — why the burden is on the Architect, not the user — and gives a concrete example of what "specific technical blocker" means.
- **Decision Matrix Inputs** (lines 169-178): Each input dimension explains what it influences and why, not just what values it takes.

No non-obvious logic is left unexplained. There and back again, every twist in the road is documented.

---

## Criterion 2: New Sections Are Well-Structured with Clear Headings and Consistent Formatting

**Verdict: PASS**

The document follows a clear hierarchical structure:

- **Top-level sections** use `##` headings: Phase 1, Prior Art Analysis, Phase 2, Architecture Style, Domain Discovery, Software Architecture Roles, Game Architecture Roles, Cross-Role Tasks, Output Contracts, Guardrails, Sub-Agent Interface, User Commands, References.
- **Sub-sections** consistently use `###` (e.g., Step 1-4 under Prior Art, Role --> Reference Mapping under each domain).
- **Tables** are used consistently for routing (Role --> Reference, Task Type Routing, Cross-Role combinations, Decision Matrix Inputs, Decomposition Strategy).
- **Code blocks** are used for templates (Sub-Agent Prompt, Output Contracts, Input/Output JSON schemas, config YAML).
- **Numbered lists** for sequential processes (Phase 2 steps, Prior Art steps, Domain Discovery process).
- **Bulleted lists** for non-sequential items (guardrails, assumptions, domain signals).

The formatting is internally consistent throughout. Heading levels do not skip (no `##` jumping to `####`). Each major section follows the same structural pattern.

---

## Criterion 3: Instructions Use Imperative Language Consistently

**Verdict: PASS**

The document uses imperative voice throughout:

- "Detect the relevant architect role(s) from..." (line 19)
- "If ambiguous, ask before proceeding. Do not assume." (line 26)
- "Declare before every task" (line 28)
- "Read ALL user-provided specifications in full. Produce a written summary of:" (line 42)
- "The Architect MUST NOT propose alternatives for these elements." (line 59)
- "The Architect MUST build architecture ON the user's existing design" (line 64)
- "For every architecture task, follow these steps exactly -- do not skip" (line 84)
- "Do not inline architecture knowledge into the main context." (line 90)
- "Every design must state its trade-offs" (line 489)
- "NFRs must be quantified" (line 493)
- "Performance budgets are mandatory" (line 501)

MUST, MUST NOT, "do not", "follow exactly" — the imperative voice is consistent. No passive constructions like "it is recommended that" or "one should consider" dilute the instructions.

---

## Criterion 4: Example Formats (Tables, Templates) Are Clear and Complete

**Verdict: PASS**

Tables and templates are well-formed and complete:

- **Classification table** (lines 49-56): Includes header, separator, and 4 worked examples covering both classifications with clear rationale.
- **Decomposition Strategy table** (lines 158-166): Maps config value to reference file and method — all 6 values covered.
- **Decision Matrix Inputs table** (lines 172-178): Low/Medium/High ranges with what each influences — complete for all 4 inputs.
- **Task Type Routing Tables**: Both software (lines 223-241) and game (lines 280-288) tables have consistent 4-column structure (Signal, Type, Role, References).
- **Output Contract templates** (lines 329-477): 5 distinct templates (Design, ADR, Game, Review, Technology Evaluation), each with labeled sections and placeholder guidance.
- **JSON schemas** (lines 517-556): Input and Output contracts with typed fields, optional annotations, and descriptive comments.
- **Config YAML example** (lines 147-153): Shows style_overrides with per-component override syntax.

All tables have proper Markdown formatting (header row, separator row, data rows). No truncated or placeholder-only examples.

---

## Criterion 5: New Content Follows the Existing Document's Style and Conventions

**Verdict: PASS**

Comparing the Architect SKILL.md against the Operations SKILL.md (the sibling skill in the same plugin), the conventions align:

- **YAML frontmatter**: Both use `name`, `description`, `license` fields in identical format.
- **Design Principle section**: Both open with a "Design Principle: Role Context Isolation" section explaining the sub-agent pattern.
- **Phase structure**: Both use Phase 1 (Role Detection) and Phase 2 (Sub-Agent Invocation) with identical formatting.
- **Routing tables**: Same 4-column format (Request Signal, Task Type, Roles, References Loaded).
- **Output Contracts**: Same markdown template pattern with Role/Task header and structured sections.
- **Guardrails**: Same format — domain-grouped guardrails with bold lead-in and dash explanation.
- **Sub-Agent Interface**: Same JSON schema format for Input/Output contracts.
- **User Commands**: Same 2-column table (Command, Action).
- **References section**: Same grouped-by-domain listing with inline descriptions.

The Architect skill's additions (Prior Art Analysis, Architecture Style from Config, Domain Discovery, Game Architecture Roles, Decomposition Strategy) follow the same patterns established by the base structure. Style conventions are preserved.

---

## Criterion 6: No Broken Cross-References Within the Document

**Verdict: PASS**

All internal cross-references resolve correctly:

- "see routing tables below" (line 22) references the Software and Game Task Type Routing Tables that follow.
- "see output contract below" (line 118) references the Output Contracts section.
- "see config" (line 228) references the Architecture Style and Decomposition from Config section.
- "configured decomposition reference" (line 228) maps to the Decomposition Strategy table.
- Reference file paths (e.g., `references/architecture-patterns.md`, `references/domain-discovery.md`) are listed in the References section and match the routing tables.
- "godot pattern" references are consistent — introduced in the Design Principle section and referenced in Cross-Role Tasks.
- Phase references ("Phase 1", "Phase 2") are sequential and correctly numbered.
- All role names used in routing tables appear in the Role --> Reference Mapping tables.
- `references/adr-lifecycle.md` is listed in References but not referenced in any routing table — however, this is a supplementary reference, not a broken cross-reference (it exists as supporting material, not a dangling pointer).

No broken links, no references to non-existent sections, no circular dependencies.

---

## Summary

| # | Criterion | Verdict |
|---|-----------|---------|
| 1 | Inline documentation present for non-obvious logic | **PASS** |
| 2 | New sections well-structured with clear headings and consistent formatting | **PASS** |
| 3 | Instructions use imperative language consistently | **PASS** |
| 4 | Example formats (tables, templates) clear and complete | **PASS** |
| 5 | New content follows existing document's style and conventions | **PASS** |
| 6 | No broken cross-references within the document | **PASS** |

**Overall: 6/6 PASS**

---

## Observations (Non-Blocking)

> "Now, a hobbit notices things that bigger folk might miss on the road..."

1. **Scope disclaimer**: The Architect SKILL.md covers compliance, privacy, and incident response roles. These are valuable but inherently limited compared to dedicated professional compliance/legal review. The skill does include guardrails ("Security is not optional", burden-of-proof for deviations), but there is no explicit disclaimer that outputs from compliance/privacy roles are not a substitute for professional legal or regulatory counsel. Per the memory lesson about scope limitations needing user-facing disclaimers, this is worth noting — though it does not fail any Gate 6 criterion.

2. **`adr-lifecycle.md` in References**: Listed in the References section but not routed to by any task type. It appears to be supplementary material for ADR management. Not a broken reference, but worth confirming it is intentionally available as a standalone resource rather than an oversight in routing.

> "And so concludes this chapter of the documentation review. A fine adventure — the Architect's chronicle is well-told, well-structured, and ready for the road ahead."
