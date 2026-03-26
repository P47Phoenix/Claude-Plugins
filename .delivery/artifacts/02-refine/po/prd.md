## PRD: Presentation Skill
**Version**: 2.0
**Author**: Product Owner (Gandalf)
**Date**: 2026-03-25
**Status**: Draft — revised from adversarial review + user requirements

### Revision History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-03-25 | Initial draft — 8 types, single Presentation Designer role, 12 user stories |
| 2.0 | 2026-03-25 | Scope reduction to 4 types. Team collaboration flow (6-step). Minimum artifact validation. Narrative adaptation for problem signals. Error states. Incremental dogfooding. Renamed role to Presentation Composer. Deferred 5 types to v1.1. |

### 1. Overview

**Problem**: The delivery team produces rich artifacts throughout the pipeline -- PRDs, architecture decisions, sprint plans, FKCs, UAT reports, retrospectives -- but has no structured way to turn these into presentation-ready material. Team members spend 90 minutes to 6 hours per week manually extracting content from delivery artifacts and reshaping it into slides. The content assembly is the real pain point: pulling information from multiple sources, organizing it into a coherent narrative, and adapting language for the target audience. Every presentation is rebuilt from scratch.

**Solution**: A `presentation` skill under `delivery-team/skills/presentation/` that treats presentation creation as a **team collaboration flow**, not a solo design task. The skill orchestrates contributions from multiple delivery team roles through a 6-step gated process: Assemble, Content Gate, Draft (parallel), Compose, Review Gate, User Review.

The skill reads delivery artifacts (read-only), validates minimum artifact requirements before proceeding, structures content into one of 4 presentation types (v1), adapts tone and vocabulary for the target audience, and produces output in two co-primary formats: structured markdown (paste-ready for any slide tool) and Marp-enhanced markdown (for users with marp-cli installed). Every slide cites its source artifacts so users can verify accuracy before presenting.

**Key change from v1.0**: The "Presentation Designer" role is replaced by a **Presentation Composer** role. The Composer assembles contributions from PO, Data Analyst, Developer, Architect, QA, Technical Writer, and UX Designer into a cohesive deck. The Composer does not create content alone -- the team creates the content, the Composer shapes it into a presentation.

**v1 Scope**: 4 presentation types only:
1. Sprint Review
2. Feature Pitch
3. Stakeholder Update
4. Technical Deep-Dive

**Target Users**:
- **Product Owner** -- sprint review decks, stakeholder updates, feature pitch decks
- **Architect** -- technical deep-dives, architecture decision presentations
- **Scrum Bag / Data Analyst** -- sprint metrics presentations, stakeholder updates
- **Developer** -- technical deep-dives, feature pitch contributions
- **Consultants / Freelancers** -- client status reports (via Stakeholder Update type)

### 2. Goals & Success Metrics

1. **Reduce content assembly time by 70%+.** Success: a sprint review deck that previously took 90 minutes to assemble manually can be generated as a first draft in under 15 minutes, requiring only minor edits before use.

2. **100% content accuracy from source artifacts.** Success: zero hallucinated metrics, features, or claims in generated presentations. Every data point traces to a source artifact. Users trust the output enough to present it without line-by-line manual verification.

3. **Support 4 presentation types with appropriate narrative structure.** Success: each presentation type produces output that follows a recognizable, audience-appropriate narrative arc (not generic bullet dumps).

4. **Co-primary format parity between structured markdown and Marp.** Success: structured markdown output is first-class -- not degraded, not missing content, not labeled "fallback." Users who never install Marp get the same content quality as those who do.

5. **Tone adaptation matches audience expectations.** Success: a sprint review for executives uses different vocabulary than a technical deep-dive for engineers. Game dev presentations use "milestone" not "sprint," "mechanics" not "features," "playtesting" not "UAT."

6. **Opt-in pipeline integration with zero disruption.** Success: the skill works standalone (invoked directly) and integrates at pipeline checkpoints without adding mandatory steps or slowing down teams that do not need presentations.

7. **Team collaboration produces higher-quality output than solo generation.** Success: presentations include domain-accurate content from each contributing role, not surface-level summaries from a single generalist. QA slides cite real test results, metric slides cite real velocity data, architecture slides cite real ADRs.

### 3. Team Collaboration Flow

Presentation creation follows a 6-step gated flow. Each step has defined roles, inputs, outputs, and failure conditions.

#### Step 1: Assemble (PO)

**Owner**: Product Owner
**Purpose**: Determine presentation type, audience, and narrative arc. Identify which artifacts to pull from. Produce a presentation outline.

**Inputs**:
- User request (presentation type, audience, occasion)
- `.delivery/config.yml` (project context, team, tech stack)
- Pipeline state (current stage, recent activity)

**Outputs** (Presentation Outline):
- Presentation type (one of: Sprint Review, Feature Pitch, Stakeholder Update, Technical Deep-Dive)
- Target audience and tone
- Slide titles (ordered)
- Key points per slide
- Source artifact per slide (where to pull data from)
- Which team roles contribute to which slides

**Narrative adaptation rule**: If the PO detects problem signals in source data (low completion rate, high defect count, missed sprint goals, unresolved blockers), the narrative arc shifts automatically:
- Low completion (<80%): lead with "what we learned" not "what we delivered"
- High defects (>5 unresolved): add a quality-focused slide before metrics
- Missed sprint goal: reframe around adjusted scope and rationale
- The PO does not hide problems -- the narrative acknowledges them constructively

#### Step 2: Content Gate (Automated)

**Purpose**: Validate that required artifacts exist and contain usable data before investing effort in content generation. If minimum artifact set is not met, STOP and tell the user what is missing.

**Minimum Artifact Requirements by Type**:

| Presentation Type | Required Artifacts | Optional (Enhancing) Artifacts |
|---|---|---|
| Sprint Review | Sprint plan (`05-sprint-plan.md` or equivalent), UAT report or completion data | FKCs, commit history, retrospective, sprint metrics, defect log |
| Feature Pitch | Idea brief or PRD | Architecture overview, competitive analysis, user research |
| Stakeholder Update | Pipeline state (`.delivery/state/`), sprint plan or progress data | Risk register, metrics, retrospective summary |
| Technical Deep-Dive | Architecture docs or ADRs (at least 1) | Design decisions, code examples, Mermaid-diagrammable content |

**Gate behavior**:
- ALL required artifacts must exist and be non-empty
- If any required artifact is missing: STOP. Output a clear error listing exactly which artifacts are missing, where they should be, and how to create them
- If required artifacts exist but are stale (>7 days old by default, configurable): WARN but proceed. Include staleness notice in the presentation outline
- If required artifacts exist but appear to contain placeholder/template content only: WARN and ask user to confirm proceeding

#### Step 3: Draft (Parallel — Multiple Roles)

**Purpose**: Multiple team roles contribute content to their relevant slides simultaneously. Each role writes content for the slides assigned to them in the Assemble step.

**Role Contributions**:

| Role | Contributes To | Content Type |
|------|---------------|-------------|
| **Product Owner** | Narrative slides | Sprint goals, priorities, strategic context, next steps, "why this matters" framing |
| **Data Analyst** | Metric slides | Velocity, completion rates, defect trends, KPIs, before/after comparisons, charts |
| **Developer** | Technical slides | Features delivered, implementation highlights, key code decisions, demo talking points |
| **Architect** | Architecture slides | Design decisions, system changes, trade-off analysis, Mermaid diagrams, technical debt updates |
| **QA Engineer** | Quality slides | Test results summary, defects found/fixed, coverage data, UAT outcomes, quality trends |

**Parallel execution**: All role contributions are generated in parallel. Each role reads only the artifacts relevant to its slides. No role depends on another role's output during this step.

**Content rules for all roles**:
- Every data point must cite its source artifact
- If data is missing from the source, use `[TBD]` placeholder -- never fabricate
- Write content at the detail level appropriate for the presentation type and audience
- Stay within the slide's assigned scope (do not duplicate another role's content)

#### Step 4: Compose (Presentation Composer)

**Owner**: Presentation Composer
**Purpose**: Assemble all role contributions into a cohesive deck with consistent tone, narrative flow, and output format.

**Inputs**:
- Presentation outline from Step 1
- All role contributions from Step 3
- Output format preference (structured markdown, Marp, paste-ready)

**Composer responsibilities**:
- Ensure consistent tone and vocabulary across all slides (translate role-specific jargon if audience requires it)
- Enforce narrative arc (slides flow logically, transitions make sense)
- Apply output format conventions (slide boundaries, citation format, frontmatter for Marp)
- Enforce information density limits (max 5-7 bullets per slide, max 1 key message per slide)
- Add opening slide (title, date, context) and closing slide (next steps, CTA)
- Resolve any content overlaps or gaps between role contributions
- Apply narrative adaptation if problem signals were flagged in Step 1

**Outputs**: Complete presentation draft in the requested output format.

#### Step 5: Review Gate (Two Reviewers)

**Purpose**: Two specialized reviewers evaluate the composed draft before presenting to the user.

**Reviewer 1: Technical Writer**
- Reviews for clarity and audience-appropriateness
- Flags jargon that was not translated for the target audience
- Checks that slide titles are descriptive and scannable
- Verifies speaker notes (if requested) include useful talking points
- Validates that every slide has a clear single message

**Reviewer 2: UX Designer**
- Reviews slide composition and information density
- Flags slides with too many bullets, too much text, or competing messages
- Checks visual hierarchy (titles, emphasis, whitespace via markdown structure)
- Validates that the slide sequence tells a coherent visual story
- Flags slides that would be hard to read in a projected presentation

**Gate behavior**:
- Each reviewer produces a list of issues (if any)
- Issues are categorized: MUST-FIX (blocks user review) or SUGGESTION (included as notes)
- If MUST-FIX issues exist, the Composer addresses them before proceeding
- SUGGESTION items are included as comments in the draft for user awareness

#### Step 6: User Review

**Purpose**: Present the complete draft to the user for final decision.

**User options**:
- **Approve**: Presentation is saved to `.delivery/artifacts/presentations/` with timestamped filename
- **Request Changes**: User provides specific feedback. Flow returns to the appropriate step (Compose for formatting issues, Draft for content issues, Assemble for structural issues)
- **Abort**: Presentation is discarded. No artifacts saved.

**What the user sees**:
- The complete presentation in the requested format
- A summary of the collaboration: which roles contributed, which artifacts were consumed
- Any SUGGESTION items from the Review Gate
- Any staleness warnings from the Content Gate
- Source citation summary (all artifacts referenced)

### 4. User Stories

**US-01: Sprint review deck from pipeline artifacts**
As a Product Owner, I want to generate a sprint review deck from this sprint's delivery artifacts using the team collaboration flow, so that the deck includes accurate contributions from each team role rather than a single-perspective summary.

Acceptance criteria:
- Skill reads sprint plan, UAT report, FKCs, and commit history from `.delivery/artifacts/`
- PO contributes narrative slides (goals, priorities, next steps)
- Data Analyst contributes metric slides (velocity, completion, defect trends)
- Developer contributes feature highlight slides
- QA contributes quality summary slides
- Presentation Composer assembles into cohesive deck
- Technical Writer and UX Designer review before user sees draft
- Output includes: sprint goal recap, committed vs delivered summary, feature highlights with descriptions, metrics, quality summary, risks/blockers, next sprint preview
- Every slide cites which artifact(s) it drew from
- Output is available in both structured markdown and Marp format
- Content Gate validates sprint plan and UAT report exist before proceeding

**US-02: Feature pitch deck for stakeholders**
As a Product Owner, I want to generate a feature pitch deck from the idea brief and PRD, so that I can get stakeholder buy-in without spending hours on slide creation.

Acceptance criteria:
- Content Gate validates idea brief or PRD exists
- Skill reads idea brief, PRD, and architecture overview (if available)
- PO contributes problem/solution/benefit narrative
- Architect contributes technical feasibility and design approach (if architecture docs exist)
- Output follows problem-solution-benefit narrative arc
- Tone adapts to the specified audience (executive, technical, client-facing)
- No claims about features or metrics that are not in the source artifacts

**US-03: Technical deep-dive for engineering audience**
As an Architect, I want to generate a technical deep-dive presentation from architecture docs, so that I can present design decisions to the engineering team with accurate diagrams and trade-off analysis.

Acceptance criteria:
- Content Gate validates at least 1 architecture doc or ADR exists
- Architect contributes design decisions, trade-offs, system context
- Developer contributes implementation details and code highlights (if relevant)
- Output includes: context/problem, options considered, decision rationale, trade-offs, system diagrams (Mermaid syntax where applicable)
- Technical vocabulary preserved (no dumbing-down for non-technical audience)
- Mermaid diagram blocks included where architecture docs contain diagrammable content

**US-04: Stakeholder update from pipeline state**
As a Scrum Bag, I want to generate a stakeholder update from current pipeline state and sprint metrics, so that management gets consistent, accurate progress reports.

Acceptance criteria:
- Content Gate validates pipeline state and sprint plan/progress data exist
- PO contributes strategic context and next steps
- Data Analyst contributes velocity/throughput data and trend analysis
- QA contributes quality perspective (if quality data available)
- Output includes: progress summary, velocity/throughput data, risk status, upcoming milestones
- Executive-appropriate language (no internal jargon like "DoD," "spike," "blocker" without translation)
- Source citations on every data point
- If problem signals detected (low velocity, high defects), narrative adapts automatically

**US-05: Paste-ready content for corporate templates**
As an Enterprise Tech Lead, I want presentation content structured for pasting into my corporate PowerPoint template, so that I can comply with branding requirements without reformatting.

Acceptance criteria:
- Paste-ready mode produces clean content with no Marp frontmatter, no markdown formatting artifacts
- Clear slide boundaries with slide titles and content blocks
- Content maps 1:1 to a predictable slide structure (title, bullets, tables, notes)
- Output includes instructions like "Slide 1: [Title Slide]" with content to paste

**US-06: Speaker notes on demand**
As a Presenter preparing for a high-stakes meeting, I want to optionally include speaker notes with my generated presentation, so that I have talking points for each slide.

Acceptance criteria:
- Speaker notes are OFF by default
- When requested (via parameter or prompt), each slide includes speaker notes in Marp comment syntax (`<!-- notes: -->`) or as a separate section in structured markdown
- Notes include key talking points, data context, and transition cues

**US-07: Narrative adaptation for problem signals**
As a Product Owner, I want the presentation to automatically shift its narrative arc when delivery data signals problems, so that stakeholder communication is honest and constructive rather than misleading.

Acceptance criteria:
- Low completion rate (<80%): narrative leads with "what we learned" not "what we delivered"
- High unresolved defects (>5): quality-focused slide added before metrics
- Missed sprint goal: narrative reframes around adjusted scope and rationale
- Adaptation is visible to user in the outline (Step 1) so they can override if desired
- Problems are acknowledged constructively, never hidden

**US-08: Content Gate stops generation when artifacts are missing**
As a User, I want the skill to refuse to generate a presentation when required source artifacts do not exist, so that I never get a deck full of placeholder content that wastes my time.

Acceptance criteria:
- Content Gate checks minimum artifact requirements per presentation type
- If required artifacts are missing: generation stops with a clear error message
- Error message lists: which artifacts are missing, where they should be located, how to create them
- If artifacts exist but are stale: warning is shown but generation proceeds
- If artifacts exist but appear to be templates/placeholders: warning + user confirmation required

### 5. Functional Requirements

| ID | Requirement | Priority | Notes |
|----|-------------|----------|-------|
| FR-001 | Read delivery artifacts from `.delivery/artifacts/`, `.delivery/memory/`, `.delivery/config.yml`, `.delivery/state/`, and git history (read-only, never modify) | P0 | Core input mechanism |
| FR-002 | Support 4 presentation types: Sprint Review, Feature Pitch, Stakeholder Update, Technical Deep-Dive | P0 | Each type has a dedicated narrative structure defined in `narrative-patterns.md` |
| FR-003 | Execute the 6-step team collaboration flow: Assemble, Content Gate, Draft (parallel), Compose, Review Gate, User Review | P0 | Core workflow — not optional |
| FR-004 | Content Gate: validate minimum artifact requirements per presentation type before proceeding. Stop with clear error if requirements not met. | P0 | Gate — generation must not proceed without required artifacts |
| FR-005 | Produce structured markdown output as a co-primary format (not fallback) with clear slide boundaries, slide titles, and paste-ready content blocks | P0 | Default output when no format preference specified |
| FR-006 | Produce Marp-enhanced markdown output with frontmatter (`marp: true`, theme, paginate), directives, and slide separators | P0 | Generated when user requests Marp or marp-cli is detected |
| FR-007 | Include source citations on every slide: "Generated from: [artifact-path-1], [artifact-path-2]" | P0 | Trust mechanism — non-negotiable |
| FR-008 | Never hallucinate data. If a metric, feature, or claim is not present in source artifacts, output "[TBD]" or "[insert X]" placeholder instead | P0 | Content accuracy guardrail |
| FR-009 | Parallel Draft step: PO, Data Analyst, Developer, Architect, and QA contribute content to their assigned slides simultaneously | P0 | Team collaboration — not sequential |
| FR-010 | Compose step: Presentation Composer assembles role contributions into cohesive deck with consistent tone and narrative flow | P0 | Single point of composition |
| FR-011 | Review Gate: Technical Writer reviews clarity/audience-appropriateness, UX Designer reviews composition/density. MUST-FIX issues block user review. | P0 | Quality gate before user sees output |
| FR-012 | User Review step: present draft to user with approve/request-changes/abort options | P0 | User always has final say |
| FR-013 | Support audience-based tone adaptation with at least 4 audience modes: technical, executive, client-facing, casual | P0 | Affects vocabulary, formality, jargon level |
| FR-014 | Narrative adaptation: automatically shift narrative arc when data signals problems (low completion, high defects, missed goals) | P1 | Honest communication — never hide problems |
| FR-015 | Auto-detect GAME_DEV project type from config and adapt vocabulary: milestone/sprint, mechanics/features, playtesting/UAT, systems/modules | P1 | Vocabulary layer, not just template swap |
| FR-016 | Produce paste-ready content mode: no Marp frontmatter, no raw markdown formatting, structured as "Slide N: [Title]" with content blocks | P1 | For corporate template users |
| FR-017 | Support image placeholders: `![description](path/to/image.png)` with contextual instructions for manual insertion | P1 | Critical for game dev and product demo types |
| FR-018 | Include Mermaid diagram blocks for architecture and system diagrams when source artifacts contain diagrammable structures | P1 | Auto-generated from architecture docs |
| FR-019 | Scope strictly to current repo's `.delivery/` directory; never read artifacts from parent directories or sibling repos | P1 | Multi-project isolation guardrail |
| FR-020 | Generate speaker notes only when explicitly requested (off by default) | P1 | Per user interview finding |
| FR-021 | Translate internal delivery jargon to audience-appropriate language when audience is set to client-facing or executive | P1 | "blocker" -> "delay," "spike" -> "investigation," etc. |
| FR-022 | Include staleness warning when source artifacts are older than 7 days (configurable) | P2 | Flag: "Warning: [artifact] last modified N days ago" |
| FR-023 | Support presentation regeneration: when invoked again for the same type, produce updated content from current artifact state | P2 | Avoids stale decks across sprints |
| FR-024 | Save generated presentations to `.delivery/artifacts/presentations/` with timestamped filenames | P2 | Enables sprint-over-sprint comparison |
| FR-025 | Auto-detect presentation type from pipeline context when invoked at a pipeline checkpoint (e.g., UAT stage defaults to Sprint Review) | P2 | Convenience — user can always override |

### 6. Error States

The skill must handle these error conditions gracefully. No silent failures.

| Error | Detection | Behavior |
|-------|-----------|----------|
| **Missing config** | `.delivery/config.yml` does not exist or is unreadable | STOP. Output: "No delivery config found at `.delivery/config.yml`. Run the setup wizard or create a config file before generating presentations." |
| **Missing required artifacts** | Content Gate finds required artifact paths do not exist | STOP. Output: list of missing artifacts, expected locations, and instructions for creating them. Do not generate partial presentations. |
| **Empty artifacts** | Required artifact file exists but is 0 bytes or contains only whitespace/template headers | WARN + prompt user: "The following artifacts exist but appear empty: [list]. Proceed anyway? Content for these slides will use [TBD] placeholders." |
| **Stale artifacts** | Required artifact last modified > staleness threshold (default 7 days) | WARN but proceed. Include staleness notice in presentation header and affected slide citations. |
| **Unknown presentation type** | User requests a type not in the v1 set | STOP. Output: "Presentation type '[X]' is not supported in v1. Supported types: Sprint Review, Feature Pitch, Stakeholder Update, Technical Deep-Dive. [Investor Pitch, Roadmap, Product Demo, Onboarding, Retrospective Summary are planned for v1.1.]" |
| **No pipeline state** | Stakeholder Update or Sprint Review requested but `.delivery/state/` is empty or missing | WARN: "No pipeline state found. Stakeholder Update will rely on sprint plan and artifacts only. Progress tracking data will use [TBD] placeholders." |
| **Partial data in draft** | A contributing role finds its assigned artifacts contain insufficient data for meaningful slides | Role outputs what it can with `[TBD]` for gaps. Composer flags this in the review: "Note: [Role] slides have limited data — [N] of [M] data points are [TBD]." |

### 7. Output Format Specification

The skill produces presentations in three output modes. The user selects a mode explicitly, or the skill defaults to **structured markdown**.

#### 7.1 Structured Markdown (co-primary)

Clean, paste-ready content organized by slide. No tooling required.

```markdown
# Sprint Review: Project Phoenix — Sprint 14

---

## Slide 1: Sprint Goal

**Goal**: Implement user authentication and role-based access control

**Status**: Delivered (5 of 5 stories completed)

> Generated from: 05-sprint-plan.md

---

## Slide 2: Features Delivered

| Feature | Status | Notes |
|---------|--------|-------|
| OAuth 2.0 login flow | Done | Supports Google and GitHub providers |
| Role-based permissions | Done | Admin, Editor, Viewer roles |
| Session management | Done | 24-hour token expiry with refresh |
| Password reset flow | Done | Email-based with 1-hour expiry |
| Audit logging | Done | All auth events logged to database |

> Generated from: 05-sprint-plan.md, 07-uat-report.md

---

## Slide 3: Sprint Metrics

- **Velocity**: 34 story points (vs 30 planned)
- **Completion rate**: 100% (5/5 stories)
- **Defects found in UAT**: 2 minor (both resolved)

> Generated from: 07-uat-report.md, .delivery/memory/sprint-metrics.md

---
```

#### 7.2 Marp-Enhanced Markdown (co-primary)

Full Marp syntax with frontmatter, directives, and theme support. Requires marp-cli to render.

```markdown
---
marp: true
theme: default
paginate: true
header: 'Sprint Review — Sprint 14'
footer: 'Project Phoenix | 2026-03-25'
---

# Sprint Review: Project Phoenix
## Sprint 14 — 2026-03-25

<!-- Generated from: 05-sprint-plan.md -->

---

## Sprint Goal

**Implement user authentication and role-based access control**

Status: **Delivered** (5 of 5 stories completed)

<!-- Generated from: 05-sprint-plan.md -->

---

## Features Delivered

| Feature | Status | Notes |
|---------|--------|-------|
| OAuth 2.0 login flow | Done | Google + GitHub |
| Role-based permissions | Done | Admin, Editor, Viewer |
| Session management | Done | 24h token + refresh |
| Password reset flow | Done | Email, 1h expiry |
| Audit logging | Done | All auth events |

<!-- Generated from: 05-sprint-plan.md, 07-uat-report.md -->

---
```

#### 7.3 Paste-Ready Mode

Optimized for copying into corporate templates or slide tools. No markdown formatting, no frontmatter. Pure content blocks.

```
=== SLIDE 1: Title Slide ===
Title: Sprint Review — Sprint 14
Subtitle: Project Phoenix
Date: 2026-03-25

=== SLIDE 2: Sprint Goal ===
Headline: Implement user authentication and role-based access control
Body: Delivered — all 5 planned stories completed this sprint.
Source: 05-sprint-plan.md

=== SLIDE 3: Features Delivered ===
Bullet 1: OAuth 2.0 login flow — supports Google and GitHub providers
Bullet 2: Role-based permissions — Admin, Editor, Viewer roles
Bullet 3: Session management — 24-hour token expiry with refresh
Bullet 4: Password reset flow — email-based, 1-hour expiry
Bullet 5: Audit logging — all auth events captured
Source: 05-sprint-plan.md, 07-uat-report.md

=== SLIDE 4: Sprint Metrics ===
Metric 1: Velocity — 34 story points (vs 30 planned)
Metric 2: Completion rate — 100% (5/5 stories)
Metric 3: UAT defects — 2 minor (both resolved)
Source: 07-uat-report.md
```

#### Source Citation Format

All three modes include source citations per slide. Format:

- **Structured markdown**: `> Generated from: artifact-1.md, artifact-2.md` (blockquote, end of slide)
- **Marp**: `<!-- Generated from: artifact-1.md, artifact-2.md -->` (HTML comment, end of slide)
- **Paste-ready**: `Source: artifact-1.md, artifact-2.md` (labeled line, end of slide block)

Paths are relative to `.delivery/artifacts/` when artifacts live there, or absolute from repo root otherwise.

### 8. Reference File Design

Four reference files, each under 200 lines, stored at `delivery-team/skills/presentation/references/`.

#### 8.1 `slide-structure.md`

Slide composition patterns and information density guidelines.

Content outline:
- **Slide types**: Title slide, content slide (bullets), comparison slide (two-column), metric/KPI slide, timeline slide, table slide, diagram slide, image showcase slide, section divider, closing/CTA slide
- **Information density rules**: Max 5-7 bullets per slide, max 1 key message per slide, max 2 data visualizations per slide
- **Slide sequencing**: Opening pattern (context -> agenda -> content), closing pattern (summary -> next steps -> CTA)
- **Image placeholder conventions**: `![description](path)` syntax, contextual placement instructions, alt-text guidelines
- **Slide boundary conventions**: Consistent separator format across all 3 output modes

#### 8.2 `narrative-patterns.md`

Storytelling frameworks mapped to presentation types. v1 covers 4 types.

Content outline:
- **Sprint Review**: Goal recap -> Committed vs Delivered -> Feature highlights -> Metrics -> Quality summary -> Demo highlights -> Risks -> Next sprint
- **Feature Pitch**: Problem (with evidence) -> Solution -> Benefit -> Implementation approach -> Ask/next steps
- **Stakeholder Update**: Executive summary -> Progress vs plan -> Risks and mitigations -> Metrics -> Upcoming milestones -> Decisions needed
- **Technical Deep-Dive**: Context/problem -> Options evaluated -> Decision + rationale -> Trade-offs -> Architecture diagram -> Migration path
- **Narrative adaptation patterns**: Problem-signal detection rules and narrative arc adjustments (low completion, high defects, missed goals)

#### 8.3 `marp-templates.md`

Marp syntax reference and template patterns.

Content outline:
- **Frontmatter directives**: `marp: true`, `theme`, `paginate`, `header`, `footer`, `class`, `backgroundColor`
- **Slide-level directives**: `<!-- _class: lead -->`, `<!-- _backgroundColor: #f0f0f0 -->`
- **Multi-column layouts**: CSS class patterns for 2-column and 3-column slides
- **Code block highlighting**: Language-specific syntax highlighting in Marp
- **Mermaid integration**: Embedding Mermaid diagrams in Marp slides (inline code blocks)
- **Image sizing and positioning**: `![w:500](image.png)`, `![bg right](image.png)`
- **Speaker notes syntax**: `<!-- notes: Your talking points here -->`
- **Theme recommendations**: Default, gaia, uncover — when to use each

#### 8.4 `data-visualization.md`

Presenting metrics and data in slides.

Content outline:
- **Chart type selection**: When to use bar, line, pie, table — decision matrix based on data type
- **Mermaid diagram types for presentations**: Flowcharts, sequence diagrams, Gantt charts, pie charts, mindmaps
- **Metric highlight patterns**: Single big number, comparison (before/after), trend (sparkline description), target vs actual
- **Table formatting**: Max columns, row limits, highlighting conventions for slides
- **Data accuracy rules**: Always cite source, never extrapolate, use "[TBD]" for missing data, include date/sprint context for all metrics

### 9. Pipeline Integration

The presentation skill integrates with delivery-flow as an **opt-in capability** at pipeline checkpoints. It is never mandatory and never blocks pipeline progression.

#### Integration Points

| Pipeline Stage | Trigger Condition | Default Presentation Type | Artifacts Consumed |
|----------------|-------------------|---------------------------|-------------------|
| Idea (checkpoint) | PO requests pitch deck | Feature Pitch | Idea brief |
| Design (after DoD) | Architect requests review deck | Technical Deep-Dive | Architecture docs, ADRs |
| Plan (after sprint planning) | SM requests kickoff slides | Stakeholder Update | Sprint plan, risk register |
| UAT (after acceptance) | PO requests review deck | Sprint Review | Sprint plan, UAT report, FKCs, commits |
| UAT (release) | Release Manager requests summary | Stakeholder Update | Release notes, metrics, changelog |
| Any stage (on demand) | User explicitly invokes | User-specified type | User-specified artifacts |

#### Invocation Mechanism

The delivery-flow orchestrator invokes the presentation skill as a sub-agent, passing:
- `presentation_type`: one of the 4 v1 types (or auto-detect from stage context)
- `audience`: tone/vocabulary target (technical, executive, client-facing, casual)
- `output_format`: structured-markdown, marp, paste-ready
- `artifacts`: list of artifact paths to consume (or "auto" to use stage-appropriate defaults)
- `speaker_notes`: boolean (default: false)

The skill executes the full 6-step collaboration flow internally, presenting the User Review step as its final output. The result is saved to `.delivery/artifacts/presentations/` when the user approves.

#### Standalone Invocation

The skill also works outside the pipeline. When invoked directly (not via delivery-flow), it:
1. Reads `.delivery/config.yml` for project context (project type, tech stack, team)
2. Accepts user-specified artifact paths and presentation parameters
3. Executes the same 6-step collaboration flow
4. Produces output to stdout or a specified file path
5. Does not interact with pipeline state or stage tracking

### 10. Config Schema Extension

New config keys under `presentation.*`, added to the config schema at version 2.2.

| Key | Type | Required | Default | Valid Values | Consumed By |
|-----|------|----------|---------|-------------|-------------|
| `presentation.default_format` | string | no | "structured-markdown" | structured-markdown, marp, paste-ready | presentation (output format selection) |
| `presentation.default_audience` | string | no | "technical" | technical, executive, client-facing, casual | presentation (tone adaptation) |
| `presentation.speaker_notes` | boolean | no | false | true/false | presentation (speaker note generation) |
| `presentation.save_to_artifacts` | boolean | no | true | true/false | presentation (save to `.delivery/artifacts/presentations/`) |
| `presentation.marp_theme` | string | no | "default" | default, gaia, uncover, or custom theme path | presentation (Marp theme selection) |
| `presentation.staleness_warning_days` | integer | no | 7 | 1-30 | presentation (artifact freshness check) |
| `presentation.vocabulary_overrides` | map[string, string] | no | {} | term -> replacement pairs | presentation (custom jargon translation) |

These keys are all optional. The skill works with sensible defaults when no `presentation.*` keys are configured. The setup wizard does not need to ask about these -- they are expert-level customizations.

### 11. Out of Scope (v1)

| Item | Rationale | Target Version |
|------|-----------|----------------|
| **Investor Pitch type** | High-risk type requiring careful narrative calibration. Defer until core 4 types are validated through dogfooding. | v1.1 |
| **Roadmap type** | Overlaps with Stakeholder Update. Validate whether Stakeholder Update covers the need before adding a dedicated type. | v1.1 |
| **Product Demo type** | Requires image/video placeholder patterns that need dogfooding validation first. | v1.1 |
| **Onboarding type** | Valuable but lower-frequency use case. Core 4 types serve weekly/biweekly cadence first. | v1.1 |
| **Retrospective Summary type** | Sensitive content (team candor). Needs careful dual-audience handling. Build trust with simpler types first. | v1.1 |
| **python-pptx script generation** | Enterprise users accept paste-ready content as interim. Full .pptx scripting adds complexity and a Python dependency. | v2 |
| **reveal.js HTML output** | Heavier toolchain, overkill for most use cases. No interview persona requested it. | v2+ |
| **Live presentation mode / presenter view** | Beyond the scope of content generation. Users present with their own tools. | Out of scope |
| **Automatic screenshot capture** | Requires system-level tooling (headless browser, Godot capture). Image placeholders are sufficient for v1. | v2 |
| **Cross-repo presentation aggregation** | Multi-project scenario handled by generating per-repo presentations. Aggregating across repos requires a multi-repo orchestration layer. | v2+ |
| **Custom Marp themes / CSS** | Users can apply custom themes after generation. The skill provides theme selection from Marp built-ins only. | v1.1 |
| **Presentation diffing** (sprint-over-sprint comparison) | Valuable but adds complexity. Deferred until presentation persistence (FR-024) is validated. | v1.1 |
| **Interactive chart generation** | Slides are static. Interactive dashboards are a different artifact type. | Out of scope |
| **Video / GIF embedding** | Marp supports image embedding but video/GIF requires export tooling. Image placeholders cover the use case. | v2 |

### 12. Risks & Mitigations

| # | Risk | Impact | Likelihood | Mitigation |
|---|------|--------|------------|------------|
| R1 | **Content hallucination** -- skill generates metrics, features, or claims not in source artifacts | Critical -- trust destruction | Medium | FR-008: explicit "[TBD]" placeholders. FR-007: mandatory source citations per slide. Content Gate (Step 2) validates artifacts exist before generation starts. Each contributing role cites its sources independently. |
| R2 | **Marp not installed** -- user cannot render Marp output to HTML/PDF/PPTX | High -- raw markdown with Marp directives confuses non-technical users | High | FR-005/FR-006: co-primary formats. Structured markdown is the default. Marp is an enhancement. |
| R3 | **Vocabulary mismatch** -- enterprise jargon in game dev presentations or internal team language in client-facing decks | Medium -- undermines professionalism | Medium | FR-013/FR-015/FR-021: audience-based tone adaptation with vocabulary layer. GAME_DEV auto-detection. Review Gate catches jargon leaks. |
| R4 | **Stale artifact content** -- presentations generated from outdated data | Medium -- misleading stakeholder communication | Medium | FR-022: staleness warning. Content Gate (Step 2) checks artifact freshness. Source citations enable user verification. |
| R5 | **Missing artifacts cause partial/useless output** | High -- user wastes time on a deck full of [TBD] placeholders | Medium | Content Gate (Step 2) is a hard stop. Required artifacts must exist. The skill refuses to generate rather than producing garbage. |
| R6 | **Context budget overflow** -- collaboration flow + references + artifact content exceeds sub-agent context | Medium -- degraded output quality | Medium | NFR-003: SKILL.md under 300 lines, references under 200 lines each. Artifacts loaded selectively per role. Parallel draft step limits each role's context to its assigned slides only. |
| R7 | **Cross-project context leakage** -- in multi-repo environments, skill pulls artifacts from wrong project | Medium -- wrong data in client presentations | Low | FR-019: strict scoping to current repo. Only read from CWD's `.delivery/` directory. |
| R8 | **Collaboration overhead** -- 6-step flow is slower than single-agent generation | Low-Medium -- if total time exceeds 60 seconds, value proposition weakens | Medium | Parallel Draft step (Step 3) mitigates. Target: full flow completes in a single agent invocation under 90 seconds. Monitor during dogfooding. |
| R9 | **Narrative adaptation misjudges problem severity** -- shifts narrative when data is actually fine, or fails to shift when it should | Medium -- misleading framing | Low | Adaptation rules use explicit thresholds (completion <80%, defects >5). User sees the outline (Step 1) and can override before content is drafted. |

### 13. Non-Functional Requirements

| ID | Requirement | Notes |
|----|-------------|-------|
| NFR-001 | **Content accuracy**: Every data point, metric, feature claim, and status in generated output must trace to a specific source artifact. No inference, extrapolation, or fabrication. | Top priority from all interview personas |
| NFR-002 | **Generation speed**: The full 6-step collaboration flow should complete within a single agent invocation. Target: under 90 seconds for a typical sprint review. | Speed is the value proposition — collaboration must not make it slow |
| NFR-003 | **Context efficiency**: The skill's SKILL.md + loaded references must fit within a sub-agent context budget. Target: SKILL.md under 300 lines, each reference file under 200 lines. | Follows existing skill pattern |
| NFR-004 | **Zero external dependencies**: The skill must produce useful output with no tooling installed. Marp-cli is an enhancement, not a requirement. | Tooling barriers kill adoption |
| NFR-005 | **Idempotent reads**: The skill must never modify source artifacts, config, memory, or pipeline state. Read-only access to all delivery data. | Safety constraint |
| NFR-006 | **Format consistency**: All 4 presentation types must use the same output structure conventions (slide boundaries, citation format, placeholder syntax) regardless of content differences. | Predictability for automation and parsing |
| NFR-007 | **Multi-project isolation**: The skill must not access `.delivery/` directories outside the current working repository. No cross-repo context leakage. | Consultant with multiple client repos |

### 14. Dogfooding Plan

The team validates the presentation skill by using it to produce real presentations before shipping. Code review alone is not sufficient. Dogfooding is **incremental**: build Sprint Review first, validate it works, then expand to other types.

#### Phase 1: Sprint Review (build first, dogfood first)

Sprint Review is the highest-frequency, most artifact-rich presentation type. If the collaboration flow works for Sprint Review, it will work for the others.

1. **Build Sprint Review type end-to-end**: Implement the full 6-step collaboration flow for Sprint Review only. All other types return "not yet implemented."

2. **Generate a sprint review for the current sprint**: Use the presentation skill to generate a sprint review deck for the sprint that builds the presentation skill itself. This is the primary dogfooding artifact.

3. **Validate the collaboration flow**: Confirm that each role (PO, Data Analyst, Developer, Architect, QA) contributes meaningfully distinct content. If any role's contribution is redundant or empty, adjust role assignments.

4. **Validate the Content Gate**: Intentionally invoke the skill with missing artifacts and verify it refuses to generate. Then provide artifacts and verify it proceeds.

5. **Validate error states**: Test missing config, empty artifacts, stale artifacts. Verify error messages are clear and actionable.

6. **Use the deck in a real meeting**: Present the generated sprint review in an actual sprint review meeting. Evaluate: Did it save time? Was content accurate? Did the narrative flow make sense? Did each role's contribution add value?

#### Phase 2: Remaining v1 types

After Sprint Review is validated:

7. **Feature Pitch**: Generate a feature pitch for the presentation skill using the idea brief and this PRD. Evaluate problem-solution-benefit arc.

8. **Technical Deep-Dive**: Generate a technical deep-dive covering the presentation skill's architecture. Evaluate architecture content accuracy and Mermaid diagram quality.

9. **Stakeholder Update**: Generate a stakeholder update from current pipeline state. Evaluate executive tone adaptation and metric presentation.

#### Phase 3: Format and tone validation

10. **Format parity**: Generate the same sprint review in all three formats (structured markdown, Marp, paste-ready). Verify content parity -- no format gets degraded content.

11. **Tone adaptation**: Generate the same content for technical, executive, and casual audiences. Verify vocabulary and formality differences.

#### Exit Criteria

- Sprint Review type fully validated through real use (Phase 1 complete)
- All 4 v1 types generate accurate, useful output (Phase 2 complete)
- All 3 output formats produce equivalent content (Phase 3 complete)
- Content accuracy: zero hallucinated data points across all generated presentations
- Time savings: at least 50% reduction vs manual assembly for sprint review deck
- Content Gate correctly blocks generation for missing artifacts (tested)
- Error states produce clear, actionable messages (tested)
- At least one presentation actually used in a real meeting (not just generated and reviewed)
- Collaboration flow produces measurably better output than single-role generation (at least 2 roles contribute non-trivial unique content)
- Any defects found during dogfooding are fixed before the skill ships
