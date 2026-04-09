# Idea Brief — BACKLOG-006 Architect Transformation Planning

*Pipeline: run-2026-04-09-c4d1 · Stage 1 · Voice: Gandalf*

## The Burden
Hear me, for the hour is graver than it seems. Our Architect, wise though he is, knows only the bright dawn of greenfields — PRD in, architecture out, a clean road unwalked. Yet the world is not so kind. The codebases that trouble men and women are ancient things, grown crooked over years, their original makers long departed into the West. One cannot draw a map of unknown country by staring at its ridges alone; one must also know what roads the travellers took, and why. We have no capability that accepts "here is a system, here is where it ought to go, show me the path between." Brownfield is the true terrain. Greenfield is the exception.

## The Vision
A new Architect `task_type: transformation-planning`, yielding three **linked and diffable** artifacts. First, an **AS-IS model** in two sub-phases: behavioral reconstruction (PO-led — use cases reverse-engineered from tests, UI strings, endpoints, commits, docs, each bearing actor, goal, preconditions, flow, variations, evidence, and a confidence badge) and structural reconstruction (Architect-led — a Model-First explicit model whose *actions* dimension is fed directly by Phase 1A). Second, a **TO-BE model** expressed in the very same `constraints.yml` schema that BACKLOG-001 forged, so the future may be compared to the present element-for-element. Third, a **Roadmap** of ordered iterative steps, each independently shippable, each preserving named invariants, none daring a big-bang leap. The three artifacts converge: the roadmap is a constraint-preserving transformation from one model into the other.

## Scope IN
- New `transformation-planning` task_type registered in architect SKILL.md
- Three template artifacts (use cases, AS-IS constraints, TO-BE constraints, roadmap)
- Legacy trigger rule — default ON unless PO cites trusted current docs
- PO + Architect paired execution (behavioral + structural split)
- Reference docs beneath `architect/references/` for all four phases
- Dogfood against Claude-Plugins itself as the first invocation

## Scope OUT
BACKLOG-005 paradigm-as-skill restructure. Automated refactor tooling. Live migration execution — we produce plans, not machinery that walks the road for you.

## The Stakes (measurable)
Dogfood yields ≥5 reconstructed use cases with evidence citations; at least one carries `confidence=low` (we will not lie to ourselves about legacy systems we half-remember); the AS-IS structural model consumes 1A use cases as its actions dimension; TO-BE is expressed in `constraints.yml`; the roadmap names ≥3 steps, each shippable alone.

## Anti-scope
No rewriting of existing architect task_types. No automation of the migration itself. No fabricated use cases — evidence or silence, nothing in between. Reconstruction must cite or abstain.

## The Road
Refine (PRD + constraints, this run) → Design → Architect → Plan → Development (the task_type, templates, references, dogfood) → UAT. One does not simply implement transformation-planning; one walks it, stage by stage.
