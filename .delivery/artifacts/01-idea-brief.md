## Idea Brief: Presentation Skill

**Project Type**: FEATURE
**Date**: 2026-03-25

### Problem Statement

The delivery team produces rich artifacts throughout the pipeline -- PRDs, architecture decisions, sprint plans, Feature Knowledge Cards, UAT reports, retrospectives, analytics dashboards -- but has no structured way to turn these into presentation-ready material. When stakeholders need a sprint review deck, a roadmap presentation, or a pitch for a new feature, team members must manually extract and reshape delivery artifacts into slide content outside of the pipeline.

This gap means:
- Presentation creation is ad-hoc and inconsistent across the team
- Product knowledge locked in `.delivery/` artifacts does not flow into stakeholder communication
- Sprint reviews, roadmap updates, and technical deep-dives are rebuilt from scratch each time instead of generated from existing pipeline state
- The Technical Writer role in operations covers documentation (API docs, runbooks, user guides, release notes) -- not presentation narratives, visual storytelling, or slide structure

### Target Users

1. **Product Owner** -- sprint review decks, roadmap presentations, stakeholder updates, feature pitch decks
2. **Architect** -- technical deep-dives, architecture decision presentations, system overviews for non-technical audiences
3. **Scrum Bag / Data Analyst** -- sprint metrics presentations, velocity reports, retrospective summaries
4. **Developer** -- demo walkthroughs, onboarding presentations for new team members
5. **External stakeholders** -- executives, clients, partners who receive formatted presentation output

### Proposed Scope

#### Presentation Types

The skill should support these presentation categories, each with a dedicated template and content strategy:

| Type | Source Artifacts | Typical Audience |
|------|-----------------|------------------|
| **Sprint Review** | Sprint plan, UAT report, FKCs, commit history | Team + stakeholders |
| **Roadmap** | PRD backlog, architecture decisions, pipeline analytics | Executives, clients |
| **Feature Pitch** | Idea brief, PRD, architecture overview | Decision-makers |
| **Technical Deep-Dive** | Architecture docs, design decisions, code patterns | Engineering teams |
| **Stakeholder Update** | Pipeline state, sprint metrics, risk register | Sponsors, management |
| **Product Demo** | UAT report, user flows, screenshots/descriptions | Customers, sales |
| **Onboarding** | CLAUDE.md, README, config, architecture overview | New team members |
| **Retrospective Summary** | Retro artifacts, memory entries, defect trends | Team + management |

#### Output Format

**Recommendation: Marp (Markdown-to-slides) as primary, with structured markdown as fallback.**

| Option | Pros | Cons | Verdict |
|--------|------|------|---------|
| **Marp markdown** | Native markdown (Claude writes it naturally); renders to HTML/PDF/PPTX via CLI; version-controllable; themeable; supports speaker notes, diagrams, code blocks | Requires marp-cli for conversion; less layout flexibility than native PPTX | **Primary format** |
| **python-pptx script** | True .pptx output; full layout control | Claude generates code, not slides; user must run script; harder to iterate on content; binary output not diffable | Secondary option for corporate-template compliance |
| **reveal.js HTML** | Rich interactivity; web-native; embeddable | Heavier toolchain; overkill for most team presentations | Out of scope for v1 |
| **Structured markdown outline** | Zero tooling needed; works everywhere | Not presentation-ready; requires manual conversion | **Fallback** when no tooling available |

The skill should detect whether `marp-cli` is available and adapt its output accordingly. When Marp is present, produce `.md` files with Marp frontmatter (`marp: true`, theme, paginate). When not available, produce structured markdown with clear slide breaks (`---`) and speaker notes that the user can paste into any slide tool.

#### Product Knowledge Sources

The skill draws content from these sources (read-only, never modifies them):

- `.delivery/artifacts/` -- idea briefs, PRDs, architecture docs, sprint plans, UAT reports
- `.delivery/memory/` -- team learnings, retrospective insights, defect patterns
- `.delivery/config.yml` -- project context (name, type, team, tech stack)
- Feature Knowledge Cards (FKCs) -- cross-cutting change history
- Pipeline state -- current stage, blockers, progress metrics
- Git history -- recent commits, PR summaries, changelog data

### Key Design Decisions

#### 1. Standalone skill (not an extension of Technical Writer)

**Decision**: Create a new `presentation` skill under `delivery-team/skills/`.

**Rationale**:
- Technical Writer's domain is *documentation* -- reference material, guides, runbooks. These are structured for reading and searching. Presentations are structured for *narrating and persuading* -- different information architecture, different output contracts, different guardrails.
- The operations skill already has 3 roles with 12 reference files and 21 task types. Adding presentation concerns would bloat its context and dilute role detection accuracy.
- A standalone skill follows the existing pattern: one skill per distinct competency (developer writes code, architect designs systems, quality tests, UI designs interfaces, presentations present).
- The skill can still collaborate with Technical Writer via the cross-role pattern when a presentation needs documentation excerpts.

#### 2. Role: Presentation Designer

A single role (not multi-role like operations or UI) because presentation creation is a cohesive competency. The variation is in *presentation type*, not in fundamentally different roles.

#### 3. Reference file structure

| Reference | Content |
|-----------|---------|
| `slide-structure.md` | Slide composition patterns: title slides, content slides, comparison slides, timeline slides, metric slides, quote slides, section dividers |
| `narrative-patterns.md` | Storytelling frameworks: situation-complication-resolution, pyramid principle, problem-solution-benefit, demo flow, before/after |
| `marp-templates.md` | Marp syntax, theme configuration, directives, speaker notes, image placement, multi-column layouts, code highlighting |
| `data-visualization.md` | Presenting metrics in slides: chart type selection, Mermaid diagram integration, table formatting, metric highlight patterns |

### Pipeline Integration

The presentation skill integrates at specific pipeline stages:

| Pipeline Stage | Trigger | Presentation Type |
|----------------|---------|-------------------|
| **Idea** (checkpoint) | PO requests pitch deck for stakeholder buy-in | Feature Pitch |
| **Design** (after) | Architect presents design decisions to team | Technical Deep-Dive |
| **Plan** (after sprint planning) | Scrum Bag prepares sprint kickoff slides | Stakeholder Update |
| **UAT** (after acceptance) | PO prepares sprint review deck | Sprint Review, Product Demo |
| **UAT** (release) | Release Manager prepares release summary | Stakeholder Update |
| **Cross-stage** | On demand at any checkpoint | Roadmap, Onboarding, Retrospective Summary |

**Integration mechanism**: The delivery-flow orchestrator can invoke the presentation skill as an optional step at checkpoints, passing the relevant artifacts as context. This is *opt-in* -- presentations are generated when requested, not automatically at every stage.

**Agentic flow**: The skill exposes the standard input/output contract pattern used by all delivery-team skills, accepting `prd_reference`, `architecture_reference`, and a new `pipeline_artifacts` context field.

### Risks & Open Questions

#### Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| Marp not installed on user's system | Slides render as raw markdown | Detect tooling availability; fallback to structured markdown; provide installation guidance in skill output |
| Presentations become stale if artifacts change | Misleading stakeholder content | Presentations reference source artifacts by path; include "generated from" metadata; recommend regeneration at each checkpoint |
| Scope creep into visual design territory | Overlap with UI skill, bloated skill | Guardrail: presentation skill handles *content and structure*, not pixel-level visual design. Theme customization is limited to Marp themes. |
| Corporate template compliance | Some orgs require branded .pptx | python-pptx script generation as secondary output path; document as future enhancement |

#### Open Questions

1. **Should the skill auto-detect presentation type from pipeline context?** (e.g., if invoked during UAT, default to Sprint Review) Or always require explicit type selection?
2. **How deep should Mermaid diagram integration go?** Architecture diagrams, flow charts, and sequence diagrams could be embedded directly in Marp slides via Mermaid. Worth investing in for v1?
3. **Speaker notes**: Should the skill always generate speaker notes, or only when requested? Speaker notes add significant value for less-experienced presenters but add generation time.
4. **Presentation versioning**: Should generated presentations be saved to `.delivery/artifacts/presentations/` and tracked across sprints? This would enable "diff this sprint review vs last sprint" but adds storage.
5. **python-pptx path**: Should v1 include python-pptx script generation for corporate template compliance, or defer to v2?
6. **Dogfooding plan**: The team should use this skill to generate its own sprint review deck for at least one full sprint cycle before considering it shippable. What is the first real presentation we can generate to validate the skill?
