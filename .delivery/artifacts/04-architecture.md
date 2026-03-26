# Architecture Decision Document: Presentation Skill

**Author**: Architect
**Date**: 2026-03-25
**Stage**: Architecture (Light)
**Inputs**: PRD v2.0, UX Design

---

## 1. File Layout

```
delivery-team/skills/presentation/
├── SKILL.md                          # Presentation Composer instructions (~290 lines)
└── references/
    ├── slide-structure.md            # Slide types, density rules, sequencing (~150 lines)
    ├── narrative-patterns.md         # Per-type narrative arcs, adaptation rules (~180 lines)
    ├── marp-templates.md             # Marp syntax, directives, layouts (~150 lines)
    └── data-visualization.md         # Charts, Mermaid, metric patterns (~140 lines)
```

**Decision**: Layout confirmed as proposed. No additional files needed.

**Rationale**: Four references follow the selective-loading pattern from the UX design (Section 3.1). `slide-structure.md` and `narrative-patterns.md` load always; `marp-templates.md` loads only for Marp output; `data-visualization.md` loads only when metric/architecture slides are present. This keeps context budget under control per NFR-003.

No `hooks/` directory -- the presentation skill is stateless and read-only (NFR-005). No hook behavior required.

No `scripts/` directory -- no Python automation needed. The skill is pure SKILL.md + references.

---

## 2. Integration Points

### 2.1 Delivery-flow invokes presentation skill

**Mechanism**: Agent tool, same invocation template as all other skill delegations (see existing architecture Section 3 "Agent Invocation Template").

**Agent Invocation Template fields**:

| Field | Value |
|-------|-------|
| SKILL | `delivery-team:presentation` |
| TASK_TYPE | `presentation` |
| ROLE | `Presentation Composer` |
| INPUT ARTIFACTS | Artifact paths determined by pipeline stage context |
| OUTPUT | `.delivery/artifacts/presentations/{type}-{date}.md` |

**Additional parameters** passed in the TASK section of the prompt (not standard template fields -- these are presentation-specific):
- `presentation_type`: sprint-review / feature-pitch / stakeholder-update / technical-deep-dive (or "auto" for stage-based detection)
- `audience`: technical / executive / client-facing / casual
- `output_format`: structured-markdown / marp / paste-ready
- `speaker_notes`: true / false

**Standalone invocation**: User triggers via natural language ("create a sprint review presentation"). The skill parses parameters from the request per UX design Section 1.1. No orchestrator involvement.

### 2.2 Skill reads .delivery/artifacts

**Mechanism**: Direct file reads by path. The orchestrator passes artifact paths in the Agent Invocation Template. The Presentation Composer (and its sub-agents) read files from disk using the Read tool.

**No content passed through orchestrator**: Follows the existing artifact channel pattern -- orchestrator passes paths, not content. Sub-agents read from disk.

**Scope constraint** (FR-019): Only read from CWD's `.delivery/` directory. Never traverse parent or sibling repos.

### 2.3 Draft step spawns sub-agents for parallel contributions

**Mechanism**: The Presentation Composer acts as a mini-orchestrator during Step 3 (Draft). It spawns up to 5 sub-agents in parallel using multiple Agent tool calls in a single message:

| Sub-agent | Skill | Role | Contributes To |
|-----------|-------|------|----------------|
| PO | `delivery-team:product-delivery` | Product Owner | Narrative slides |
| Data Analyst | `delivery-team:product-delivery` | Data Analyst | Metric slides |
| Developer | `delivery-team:developer` | Developer | Feature slides |
| Architect | `delivery-team:architect` | Architect | Architecture slides |
| QA | `delivery-team:quality` | QA Engineer | Quality slides |

Each sub-agent receives:
- Its assigned slide numbers and titles from the Step 1 outline
- Paths to its relevant source artifacts only (context isolation)
- The presentation type, audience, and content rules

Each sub-agent writes its contribution to a temporary path:
`.delivery/artifacts/presentations/.drafts/{role}-slides.md`

The Composer reads all draft files in Step 4 (Compose) to assemble the final deck.

**Not all 5 roles run for every presentation type.** The PO determines the role-to-slide mapping in Step 1. A Feature Pitch may only need PO + Architect. A Sprint Review uses all 5. The Composer dispatches only the roles assigned in the outline.

### 2.4 Review Gate spawns reviewer sub-agents

Two reviewer sub-agents in Step 5, dispatched in parallel (their concerns are orthogonal):

| Reviewer | Skill | Focus |
|----------|-------|-------|
| Technical Writer | `delivery-team:operations` | Clarity, jargon, audience fit |
| UX Designer | `delivery-team:ui` | Density, hierarchy, visual story |

Each reviewer reads the composed draft from `.delivery/artifacts/presentations/.drafts/composed-draft.md` and returns findings categorized as MUST-FIX or SUGGESTION. The Composer addresses MUST-FIX items before Step 6.

### 2.5 Compose step (Step 4)

The Composer (SKILL.md itself, not a sub-agent) reads all draft outputs from `.delivery/artifacts/presentations/.drafts/`, assembles them into the final deck following narrative-patterns.md and slide-structure.md, applies tone normalization, enforces density limits, and writes the result to `.delivery/artifacts/presentations/.drafts/composed-draft.md`.

**No sub-agent for composition**: The Composer role IS the SKILL.md. It has all the context it needs (outline from Step 1, draft files on disk, reference files loaded). Spawning another agent would waste context budget.

---

## 3. Key ADRs

### ADR-PRES-001: Presentation skill uses sub-agents for team collaboration

**Status**: Accepted

**Context**: PRD requires 5 roles to contribute content in parallel during Step 3, plus 2 reviewers in Step 5. The skill could either (a) generate all content inline as a single agent wearing multiple hats, or (b) spawn sub-agents that load the actual role skills.

**Decision**: Spawn sub-agents. Each contributing role loads its own skill (product-delivery, developer, architect, quality) to produce domain-accurate content.

**Consequences**:
- (+) Each role brings its full skill context. Developer slides cite real code patterns. Architect slides produce real Mermaid diagrams. QA slides reference actual test data.
- (+) Follows the same orchestrator + sub-agent pattern as delivery-flow. Architecture is familiar.
- (+) Parallel dispatch in Step 3 keeps latency manageable (NFR-002: under 90 seconds).
- (-) SKILL.md is more complex than single-file skills. Must include orchestration logic for dispatch, draft file coordination, and sub-agent failure handling.
- (-) Total context budget is higher (Composer context + N sub-agent contexts). Mitigated by selective reference loading and scoped artifact paths per role.
- (Risk) If latency exceeds 90 seconds, reduce to 3 parallel sub-agents by merging PO+Data Analyst and Developer+Architect. Measure in dogfooding Phase 1.

### ADR-PRES-002: Draft artifacts use temporary .drafts directory

**Status**: Accepted

**Context**: Sub-agents in Step 3 need to write contributions somewhere that Step 4 (Compose) can read.

**Decision**: Sub-agents write to `.delivery/artifacts/presentations/.drafts/{role}-slides.md`. The `.drafts/` directory is cleaned up after the user approves or aborts in Step 6.

**Consequences**:
- Follows the existing artifact channel pattern (file paths, not content through orchestrator)
- Draft files are inspectable for debugging during dogfooding
- The Composer is responsible for cleanup

### ADR-PRES-003: Composer is the SKILL.md, not a separate sub-agent

**Status**: Accepted

**Context**: The Compose step (Step 4) could be delegated to a separate "Composer" sub-agent, or the SKILL.md itself could perform composition.

**Decision**: SKILL.md performs composition directly. The "Presentation Composer" role described in the PRD maps to the SKILL.md's own execution, not a spawned agent.

**Consequences**:
- (+) No extra context overhead for a Composer sub-agent
- (+) The Composer has full visibility of the outline (Step 1) and all draft paths -- it is already the orchestrator
- (-) SKILL.md must contain both orchestration logic and composition logic, pushing toward the 300-line target

---

## 4. Marketplace Registration

Add one entry to the `skills` array in the `delivery-team` plugin in `.claude-plugin/marketplace.json`:

```json
"./delivery-team/skills/presentation"
```

Update the plugin description to reference 11 skills (currently says 10).

No new plugin entry -- presentation is a skill within the existing `delivery-team` plugin.

---

## 5. Config Schema

### Version bump: 2.1 -> 2.2

### New keys (all optional, no wizard questions needed)

| Key | Type | Default | Valid Values | Consumed By |
|-----|------|---------|-------------|-------------|
| `presentation.default_format` | string | "structured-markdown" | structured-markdown, marp, paste-ready | presentation |
| `presentation.default_audience` | string | "technical" | technical, executive, client-facing, casual | presentation |
| `presentation.speaker_notes` | boolean | false | true/false | presentation |
| `presentation.save_to_artifacts` | boolean | true | true/false | presentation |
| `presentation.marp_theme` | string | "default" | default, gaia, uncover | presentation |
| `presentation.staleness_warning_days` | integer | 7 | 1-30 | presentation |
| `presentation.vocabulary_overrides` | map[string, string] | {} | term -> replacement | presentation |

### Config template addition

```yaml
presentation:
  default_format: structured-markdown
  default_audience: technical
  speaker_notes: false
  save_to_artifacts: true
  marp_theme: default
  staleness_warning_days: 7
  vocabulary_overrides: {}
```

### Version history entry

| 2.2 | 2026-03-25 | Added `presentation.*` keys (default_format, default_audience, speaker_notes, save_to_artifacts, marp_theme, staleness_warning_days, vocabulary_overrides) for opt-in presentation skill configuration |

### Extension protocol compliance

1. Schema table: 7 new keys documented above
2. Version bump: 2.1 -> 2.2
3. Wizard: No questions -- all keys are optional with defaults (per PRD Section 10, UX design Section 5.1)
4. Pipeline config table: N/A -- presentation skill reads these directly, not via delivery-flow
5. Migration note: Version history entry added
6. Consuming skill: Presentation SKILL.md will reference config-schema.md for defaults
7. JSON schema regeneration: Run `python delivery-team/scripts/generate-schema.py` after updating config-schema.md

---

## 6. Output Directory Convention

```
.delivery/artifacts/presentations/
├── sprint-review-2026-03-25.md          # Final approved output
├── feature-pitch-2026-03-25.md
└── .drafts/                             # Temporary, cleaned up after approve/abort
    ├── po-slides.md
    ├── data-analyst-slides.md
    ├── developer-slides.md
    ├── architect-slides.md
    ├── qa-slides.md
    └── composed-draft.md               # Intermediate composed version (pre-review)
```

Filenames: `{type}-{date}.md`. Collision: append counter (`sprint-review-2026-03-25-2.md`).

---

## Decisions Summary

| # | Decision | Rationale |
|---|----------|-----------|
| 1 | File layout: SKILL.md + 4 references, no hooks/scripts | Read-only skill, pure instruction set, selective loading |
| 2 | Sub-agents for Draft (up to 5 roles) and Review Gate (2 reviewers) | Domain-accurate content requires actual role skill loading |
| 3 | Composer is the SKILL.md itself, not a sub-agent | Avoids unnecessary context overhead |
| 4 | Draft artifacts in .drafts/ temp directory | Follows artifact channel pattern, debuggable |
| 5 | Config schema v2.2 with 7 optional keys | All opt-in, zero disruption to existing configs |
| 6 | Marketplace: add 1 skill path to delivery-team plugin | Standard registration, update skill count to 11 |
