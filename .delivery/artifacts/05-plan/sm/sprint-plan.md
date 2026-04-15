# Sprint Plan — Plugin ARCHITECTURE.md Authoring (DOCS_ONLY)

> *"A day may come when the context of this codebase fails. But it is not this day.
> This day we document."* — Aragorn, son of Arathorn, to the assembled team.

Six stories. Three sprints. One ARCHITECTURE.md per plugin. Audience: **human
contributors and advanced users** — NOT Claude. Render on GitHub with live Mermaid.

## Sprint 1 — The Great Works

**ARCH-1 — `delivery-team/ARCHITECTURE.md`**
- Diagrams: **4** (flowchart 7-stage pipeline + DoD gates, component boundary,
  state diagram for resume, sequence for adversarial loop).
- Length cap: **~250 lines**. Cross-link to each of the 11 sub-skill SKILL.md paths.
- DoD: file exists; ≥1 valid ```` ```mermaid ```` block; components + key flows
  explained; linked from `delivery-team/README.md`.

**ARCH-2 — `mtg-commander/ARCHITECTURE.md`**
- Diagrams: **3** (flowchart 4-stage adversarial pipeline, sequence for one
  primary-vs-challenger loop, class/entity for `.mtg-commander.yml` schema v1).
- Length cap: **~150 lines**. Link to `references/` guides and `scripts/card_lookup.py`.
- DoD: as ARCH-1 template; linked from `mtg-commander/README.md`.

## Sprint 2 — The Agentic Kin (paired — shared patterns)

**ARCH-3 — `agentic-flow-builder/ARCHITECTURE.md`**
- Diagrams: **3** (component: registry/orchestrator/BRE/DB; class: SQLite schema;
  sequence: one flow execution).
- Length cap: **~150 lines**. Link to each of the 4 scripts and `complete_example.py`.
- DoD: as template; linked from `agentic-flow-builder/README.md`.

**ARCH-4 — `prd-quality-gate-flow/ARCHITECTURE.md`**
- Diagrams: **3** (flowchart: 7 gates + 8 agents; class: SQLite schema; state:
  PRD lifecycle).
- Length cap: **~150 lines**. Link to each `.py` module + `QUICKSTART.md`.
- Note: the current README ASCII diagram is the reference — render it in Mermaid.
- DoD: as template; linked from `prd-quality-gate-flow/README.md`.

## Sprint 3 — The Lean Blades (paired — smaller plugins)

**ARCH-5 — `prompt-engineer/ARCHITECTURE.md`**
- Diagrams: **1-2** (flowchart: 5-step router Analyze → Design → Display → Explain →
  Iterate; optional taxonomy of techniques).
- Length cap: **~150 lines**. Single-skill plugin — keep it tight.
- DoD: as template; linked from `prompt-engineer/README.md`.

**ARCH-6 — `research-agent/ARCHITECTURE.md`**
- Diagrams: **2** (flowchart: research-type decision tree with framework overlay;
  sequence: one ReAct Reason → Act → Observe cycle).
- Length cap: **~150 lines**. Link to each of the 4 reference files.
- DoD: as template; linked from `research-agent/README.md`.

## Diagram Conventions (all stories)

- Every diagram in a ```` ```mermaid ```` fenced code block — no exceptions.
- `flowchart TD` for component/pipeline diagrams; `sequenceDiagram` for agent
  interactions and ReAct/adversarial loops; `stateDiagram-v2` for state machines
  (pipeline resume, PRD lifecycle); `classDiagram` for schemas.
- Keep node labels short (≤ 3 words typical). Explanatory prose lives OUTSIDE
  the diagram — the diagram is a map, not a manual.
- **One diagram per concept.** Do not attempt to show architecture + flow +
  schema in one chart. If it needs a paragraph of legend, it needs two diagrams.
- In prose, link to the authoritative source by path (e.g., `delivery-flow/SKILL.md`,
  `scripts/business_rules_engine.py`) so a reader can verify diagram against truth.
- No architecture invented. If the source doesn't state it, don't draw it.

## Team DoD (all 6 stories)

1. Target file exists at `<plugin>/ARCHITECTURE.md`.
2. Contains ≥ 1 Mermaid fenced block (count per story above is the target).
3. Documents internal components (skills, scripts, references, hooks as applicable).
4. Documents at least one key flow (pipeline, loop, decision tree, or lifecycle).
5. Linked from that plugin's `README.md` (one-line reference under "Architecture").
6. Length within stated cap. Over-cap drafts return to Development for pruning.

---

STATUS: DONE
ARTIFACT: .delivery/artifacts/05-plan/sm/sprint-plan.md
SUMMARY: Celebrimbor — 6 plugins inventoried, ~16 diagrams est across 3 sprints. ARCH-1 delivery-team (4), ARCH-2 mtg-commander (3), ARCH-3/4 paired agentic (3+3), ARCH-5/6 lean (1-2+2).
