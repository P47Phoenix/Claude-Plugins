# UX Design: Presentation Skill

**Author**: UX Designer
**Date**: 2026-03-25
**Status**: Draft
**Input**: PRD v2.0

---

## 1. Skill Invocation UX

### 1.1 Invocation Modes

The skill has two invocation paths. Both execute the identical 6-step flow — the difference is how parameters arrive.

**Standalone invocation** (user invokes directly):

```
User: "create a sprint review presentation"
User: "generate a feature pitch for executives"
User: "presentation for stakeholder update, paste-ready format"
```

The skill parses the request for three parameters:

| Parameter | Detection Strategy | Fallback |
|-----------|-------------------|----------|
| Presentation type | Keyword match: "sprint review", "feature pitch", "stakeholder update", "technical deep-dive" | Ask the user. Do not guess. |
| Audience | Keyword match: "executive", "technical", "client-facing", "casual" | Default to `presentation.default_audience` from config, or "technical" if unset |
| Output format | Keyword match: "marp", "paste-ready", "structured" | Default to `presentation.default_format` from config, or "structured-markdown" if unset |

If the presentation type is ambiguous or missing, the skill asks exactly one question:

> What type of presentation? Options: Sprint Review, Feature Pitch, Stakeholder Update, Technical Deep-Dive

The skill does not ask about audience or format unless the user's request is explicitly contradictory (e.g., "executive casual" — which mode wins?). Defaults are good enough. Fewer questions means faster time-to-output.

**Pipeline invocation** (orchestrator invokes at checkpoint):

The delivery-flow orchestrator passes all parameters explicitly:

```
presentation_type: "sprint-review"
audience: "technical"
output_format: "structured-markdown"
artifacts: ["05-sprint-plan.md", "07-uat-report.md"]
speaker_notes: false
```

No questions asked. The orchestrator has full context. The skill executes silently through Steps 1-5 and surfaces only at Step 6 (User Review).

### 1.2 Auto-Detection (Pipeline Only)

When invoked at a pipeline checkpoint without an explicit type, the skill infers from stage context:

| Current Stage | Default Type |
|---------------|-------------|
| Idea checkpoint | Feature Pitch |
| Design after DoD | Technical Deep-Dive |
| Plan after sprint planning | Stakeholder Update |
| UAT after acceptance | Sprint Review |
| UAT release | Stakeholder Update |

The user always sees the detected type in Step 1 output and can override it.

### 1.3 User Journey (Standalone)

```
User request
    |
    v
[Parameter detection] -- type missing? --> Ask user (1 question max)
    |
    v
Step 1: Assemble -- user sees outline
    |
    v
Step 2: Content Gate -- user sees pass/fail
    |                          |
    | (pass)                   | (fail: STOP with error)
    v                          v
Step 3: Draft -- progress     [Error: missing artifacts list]
    |            indicator
    v
Step 4: Compose -- silent
    |
    v
Step 5: Review Gate -- user sees findings summary
    |
    v
Step 6: User Review -- full presentation + options
    |
    +-- Approve --> saved to .delivery/artifacts/presentations/
    +-- Request Changes --> returns to Step 1, 3, or 4
    +-- Abort --> discarded
```

### 1.4 Progress Communication

The user should never wonder "what is happening?" during the flow. Each step announces itself with a one-line status header:

```
[1/6] Assembling presentation outline...
[2/6] Validating source artifacts...
[3/6] Drafting slide content (5 roles contributing)...
[4/6] Composing final presentation...
[5/6] Reviewing draft (Technical Writer + UX Designer)...
[6/6] Ready for your review.
```

Steps 1, 2, 5, and 6 produce visible output. Steps 3 and 4 are internal — the user sees only the progress line, then the composed result at Step 6. This keeps the user informed without flooding them with intermediate drafts they cannot act on.

---

## 2. SKILL.md Structure

Target: under 300 lines. The SKILL.md is the Presentation Composer's instruction set. It delegates content creation to other roles and assembles the result.

### 2.1 Section Outline

```
Line Range   Section
---------    -------
  1-12       Frontmatter (name, description, triggers, license)
 13-30       # Presentation Composer
             Role definition, design principle (context isolation),
             what the Composer does vs. what contributing roles do

 31-70       ## Presentation Type Detection
             Type detection from user request (keyword table)
             Auto-detection from pipeline stage (stage mapping table)
             Ambiguity handling: ask, never guess
             GAME_DEV vocabulary adaptation flag

 71-150      ## 6-Step Collaboration Flow
             Step 1: Assemble (PO sub-agent, outline output contract)
             Step 2: Content Gate (artifact validation rules, error formats)
             Step 3: Draft (role-to-slide mapping, parallel execution, content rules)
             Step 4: Compose (assembly instructions, tone enforcement, density limits)
             Step 5: Review Gate (TW + UX reviewer criteria, MUST-FIX vs SUGGESTION)
             Step 6: User Review (output presentation, approve/change/abort)

151-200      ## Output Format Specifications
             Structured markdown conventions (slide boundaries, citations)
             Marp conventions (frontmatter, directives, theme)
             Paste-ready conventions (slide blocks, no markdown)
             Citation format per mode
             Speaker notes syntax (off by default)

201-240      ## Error Handling
             Error state table (missing config, missing artifacts, empty,
             stale, unknown type, no pipeline state, partial data)
             Error message format: what is wrong, where to fix it, how

241-270      ## User Commands
             Command table (approve, changes, abort, format, audience,
             notes, regenerate)

271-290      ## References
             Reference file index with descriptions
             Loading rules: which files load when

291-300      ## Config Integration
             Config keys consumed (presentation.*)
             Default behavior when no config exists
```

**Estimated total: 290 lines.**

### 2.2 Key Design Decisions in SKILL.md Structure

**Why type detection comes before the flow**: The type determines which narrative pattern loads, which artifacts the Content Gate checks, and which roles contribute to which slides. It is the routing decision for everything downstream.

**Why the flow is a single section, not six**: The 6 steps are a linear protocol. Splitting them across the file would force the model to jump between sections. A single section with clear step headers reads top-to-bottom, matching execution order.

**Why output format is separate from the flow**: Format is orthogonal to content. The same content renders in three modes. Keeping format conventions in their own section avoids duplicating formatting rules inside each step.

**Why error handling is its own section**: Error states span multiple steps (Content Gate, Draft, Compose). A consolidated error section is easier to maintain and audit than scattered error clauses.

---

## 3. Reference File Architecture

Four reference files, each under 200 lines, loaded selectively based on context.

### 3.1 Loading Strategy

Not all references load for every invocation. The Composer loads references based on what the current task requires:

| Reference File | Loaded When | Consumed By |
|----------------|------------|-------------|
| `slide-structure.md` | Always | Composer (Step 4), UX Reviewer (Step 5) |
| `narrative-patterns.md` | Always | PO (Step 1), Composer (Step 4), TW Reviewer (Step 5) |
| `marp-templates.md` | Output format is "marp" | Composer (Step 4) |
| `data-visualization.md` | Presentation contains metric or architecture slides | Data Analyst (Step 3), Architect (Step 3), Composer (Step 4) |

This means a structured-markdown Sprint Review with no metric slides loads only 2 of 4 references. A Marp Technical Deep-Dive with Mermaid diagrams loads all 4. Context budget is spent only when needed.

### 3.2 File Designs

#### `slide-structure.md` (~150 lines)

The structural grammar of slides. This file answers: "What goes on a slide and how is it arranged?"

```
Section                          ~Lines   Content
-------                          ------   -------
Slide Type Catalog                 40     10 slide types (title, content, comparison,
                                          metric, timeline, table, diagram, image,
                                          section divider, closing). Each type:
                                          name, when to use, structural template,
                                          max content limits.

Information Density Rules          25     Bullet limits (5-7), one key message rule,
                                          max data visualizations (2), text-to-
                                          whitespace ratio guidance, "if it needs
                                          scrolling it needs splitting" rule.

Slide Sequencing Patterns          30     Opening sequence (context > agenda > content),
                                          closing sequence (summary > next steps > CTA),
                                          transition patterns between slide types.

Slide Boundary Conventions         20     Separator format for each output mode
                                          (---, ===, Marp ---), citation placement,
                                          speaker note placement.

Image Placeholder Conventions      15     Syntax: ![description](path), placement
                                          rules, alt-text guidelines, sizing hints
                                          for Marp vs structured markdown.

Presentation Length Guidelines     20     Type-to-length mapping: Sprint Review
                                          8-15 slides, Feature Pitch 6-10,
                                          Stakeholder Update 5-8, Technical
                                          Deep-Dive 8-20. "Add slides for content,
                                          not for padding."
```

#### `narrative-patterns.md` (~180 lines)

The storytelling engine. This file answers: "What story does each presentation type tell, and how does the story change when the data signals problems?"

```
Section                          ~Lines   Content
-------                          ------   -------
Sprint Review Narrative Arc        30     Slide sequence: goal recap > committed vs
                                          delivered > feature highlights > metrics >
                                          quality summary > risks > next sprint.
                                          Slide-by-role assignment matrix.
                                          Opening hook patterns (goal-anchored).

Feature Pitch Narrative Arc        25     Problem (with evidence) > solution >
                                          benefit > implementation approach > ask.
                                          Audience adaptation: executive (ROI-led),
                                          technical (feasibility-led), client
                                          (value-led).

Stakeholder Update Narrative Arc   25     Executive summary > progress vs plan >
                                          risks and mitigations > metrics >
                                          milestones > decisions needed.
                                          Traffic-light status conventions.

Technical Deep-Dive Narrative Arc  25     Context/problem > options evaluated >
                                          decision + rationale > trade-offs >
                                          architecture diagram > migration path.
                                          Diagram-first vs narrative-first
                                          decision tree.

Narrative Adaptation Rules         35     Problem signal thresholds and responses:
                                          - Completion <80%: lead with learnings
                                          - Defects >5 unresolved: quality slide
                                            before metrics
                                          - Missed sprint goal: reframe to adjusted
                                            scope + rationale
                                          Detection rules (where to find these
                                          signals in artifacts). Override mechanism
                                          (user can disable adaptation in Step 1).

Tone/Vocabulary Adaptation         20     Audience mode definitions (technical,
                                          executive, client-facing, casual).
                                          Jargon translation table: blocker >
                                          delay, spike > investigation, DoD >
                                          completion criteria, UAT > acceptance
                                          testing. GAME_DEV vocabulary swaps:
                                          sprint > milestone, features > mechanics,
                                          UAT > playtesting.

Audience Detection Heuristics      20     How to infer audience when not explicit:
                                          pipeline stage signals, config hints,
                                          presentation type defaults. Fallback
                                          chain: explicit > config > type default.
```

#### `marp-templates.md` (~150 lines)

The Marp rendering reference. This file answers: "How do I produce valid, well-formatted Marp markdown?"

```
Section                          ~Lines   Content
-------                          ------   -------
Frontmatter Reference              25     Required directives (marp: true),
                                          optional directives (theme, paginate,
                                          header, footer, class, backgroundColor).
                                          Per-presentation-type frontmatter
                                          templates.

Slide-Level Directives             20     _class (lead, invert), _backgroundColor,
                                          _color. When to use each. Section
                                          divider styling.

Layout Patterns                    30     Two-column layout (CSS class pattern),
                                          three-column layout, image-beside-text,
                                          centered content. Code examples for
                                          each layout.

Code and Diagram Blocks            25     Syntax-highlighted code blocks,
                                          Mermaid diagram embedding (```mermaid),
                                          diagram sizing considerations,
                                          fallback for renderers without Mermaid.

Image Handling                     20     Sizing: ![w:500](path), background
                                          images: ![bg right](path), image
                                          positioning, placeholder conventions
                                          for images that do not exist yet.

Speaker Notes                      15     Syntax: <!-- notes: text -->,
                                          placement (after slide content,
                                          before ---), content guidelines
                                          (talking points, transition cues,
                                          data context).

Theme Guide                        15     default (clean, corporate), gaia
                                          (bold, dark option), uncover
                                          (minimal). Type-to-theme
                                          recommendation matrix.
```

#### `data-visualization.md` (~140 lines)

The data presentation reference. This file answers: "How do I present metrics, charts, and diagrams effectively in slides?"

```
Section                          ~Lines   Content
-------                          ------   -------
Chart Type Decision Matrix         30     When to use: table (comparison, small
                                          datasets), bar (categorical comparison),
                                          line (trends over time), pie (composition,
                                          max 5 segments). Decision tree: data
                                          type > comparison type > chart type.
                                          "When in doubt, use a table" rule.

Mermaid Diagram Patterns           30     Presentation-appropriate Mermaid types:
                                          flowchart (architecture), sequence
                                          (process flows), gantt (timelines),
                                          pie (proportions), mindmap (concept
                                          overview). Syntax examples sized for
                                          slides (not documentation).

Metric Highlight Patterns          30     Single big number (KPI spotlight),
                                          before/after comparison, target vs
                                          actual with delta, trend description
                                          (narrative sparkline), traffic light
                                          status (red/amber/green). Template
                                          for each pattern.

Table Formatting for Slides        25     Max 5 columns, max 8 rows, header
                                          row always bold. Column alignment
                                          conventions. When to split a table
                                          across slides. Highlighting
                                          conventions (bold for emphasis,
                                          not color — markdown limitation).

Data Accuracy Rules                25     Always cite source artifact. Never
                                          extrapolate or project from partial
                                          data. Use [TBD] for missing values.
                                          Include time context (sprint number,
                                          date range) for all metrics.
                                          Round to meaningful precision
                                          (34 points, not 34.2857).
```

---

## 4. Collaboration Flow UX

This section designs what the user sees at each step. The principle: show the user what they need to act on, hide what they cannot act on.

### 4.1 Step 1: Assemble (User Sees Outline)

The PO produces a presentation outline. The user sees it immediately because this is the first decision point — the user can redirect before any content is generated.

**User-visible output:**

```
[1/6] Assembling presentation outline...

## Presentation Outline

**Type**: Sprint Review
**Audience**: Technical
**Format**: Structured Markdown
**Narrative adaptation**: None detected (completion 95%, 1 open defect)

| # | Slide Title              | Content Owner    | Source Artifacts                  |
|---|--------------------------|------------------|-----------------------------------|
| 1 | Title                    | Composer         | config.yml                        |
| 2 | Sprint Goal              | PO               | 05-sprint-plan.md                 |
| 3 | Committed vs Delivered   | PO, Data Analyst | 05-sprint-plan.md, sprint-metrics |
| 4 | Feature: OAuth Flow      | Developer        | FKC-auth-oauth.md                 |
| 5 | Feature: RBAC            | Developer        | FKC-auth-rbac.md                  |
| 6 | Architecture Changes     | Architect        | ADR-015.md                        |
| 7 | Sprint Metrics           | Data Analyst     | sprint-metrics.md, UAT report     |
| 8 | Quality Summary          | QA               | 07-uat-report.md                  |
| 9 | Risks & Blockers         | PO               | risk-register.md                  |
| 10| Next Sprint Preview      | PO               | backlog, sprint planning notes    |

Proceed with this outline? (or provide feedback to adjust)
```

**Design rationale**: The outline table shows slide titles, who creates the content, and where the data comes from. This lets the user catch structural problems before the expensive Draft step. The narrative adaptation line is always visible so the user knows whether problem-signal reframing is active.

**If narrative adaptation is triggered:**

```
**Narrative adaptation**: Active
  - Completion rate 72% (<80% threshold): leading with "what we learned"
  - 7 unresolved defects (>5 threshold): quality slide moved before metrics
  Override? (say "no adaptation" to use standard narrative)
```

### 4.2 Step 2: Content Gate (Pass/Fail)

The Content Gate runs automatically after the user approves the outline. Two possible outcomes:

**Pass:**

```
[2/6] Validating source artifacts...

Content Gate: PASSED
  Found: 05-sprint-plan.md, 07-uat-report.md (required)
  Found: FKC-auth-oauth.md, FKC-auth-rbac.md, ADR-015.md, sprint-metrics.md (enhancing)
  Warning: risk-register.md last modified 9 days ago (staleness threshold: 7 days)

Proceeding to draft...
```

**Fail:**

```
[2/6] Validating source artifacts...

Content Gate: FAILED — missing required artifacts

  MISSING (required):
  - 05-sprint-plan.md
    Expected at: .delivery/artifacts/05-plan/05-sprint-plan.md
    Create with: Run the Plan stage of the delivery pipeline

  - UAT report or completion data
    Expected at: .delivery/artifacts/07-uat/ (any file)
    Create with: Run the UAT stage or manually create a UAT summary

  FOUND (enhancing):
  - FKC-auth-oauth.md, ADR-015.md

Cannot generate Sprint Review without required artifacts.
Fix the missing items above and invoke the skill again.
```

**Design rationale**: The fail message is actionable — it says what is missing, where it should be, and how to create it. The user is never left wondering "now what?" The pass message confirms what was found so the user can spot if the wrong version of an artifact was picked up.

### 4.3 Step 3: Draft (Progress Indicator)

The Draft step runs five roles in parallel. The user cannot act on intermediate role outputs — they are internal. The user sees only a progress indicator.

```
[3/6] Drafting slide content (5 roles contributing)...
  PO: narrative slides (2, 3, 9, 10)
  Data Analyst: metric slides (3, 7)
  Developer: feature slides (4, 5)
  Architect: architecture slides (6)
  QA: quality slides (8)
```

This is the last thing the user sees until Step 6. Steps 4 and 5 run silently.

**Design rationale**: Showing which roles contribute to which slides gives the user confidence that the collaboration is real — not a single agent wearing five hats. But the actual draft content is not shown because: (a) it is pre-composition and will change, (b) showing raw role outputs before composition would be confusing, (c) the user's decision point is the final composed deck, not individual contributions.

### 4.4 Step 4: Compose (Silent)

The Composer assembles role contributions. The user sees nothing beyond:

```
[4/6] Composing final presentation...
```

**Design rationale**: The Composer's work is editorial — tone normalization, transition writing, density enforcement. None of this requires user input. Showing intermediate composition states would slow the flow and create false decision points.

### 4.5 Step 5: Review Gate (Findings Summary)

Two reviewers evaluate the composed draft. If there are MUST-FIX issues, the Composer addresses them automatically before Step 6. The user sees only the final review summary.

**No issues:**

```
[5/6] Reviewing draft (Technical Writer + UX Designer)...

Review Gate: PASSED — no issues found.
```

**Suggestions only (no MUST-FIX):**

```
[5/6] Reviewing draft (Technical Writer + UX Designer)...

Review Gate: PASSED with suggestions
  SUGGESTION: Slide 6 — "Architecture Changes" title could be more specific
              (e.g., "Auth Service: Hexagonal Refactor")
  SUGGESTION: Slide 7 — consider splitting metrics table across 2 slides
              (currently 6 columns, may be hard to read projected)
```

**MUST-FIX issues found and resolved:**

```
[5/6] Reviewing draft (Technical Writer + UX Designer)...

Review Gate: 2 issues found, both resolved
  FIXED: Slide 3 — "DoD" jargon used in executive-audience deck (replaced with
         "completion criteria")
  FIXED: Slide 7 — 9 bullets exceeded density limit (split into 2 slides)
  SUGGESTION: Slide 10 — next sprint preview could include tentative dates
```

**Design rationale**: The user sees review findings as a trust signal — it proves the deck was reviewed, not just generated. MUST-FIX items are shown as already resolved (the Composer fixed them) so the user knows quality issues were caught and handled. SUGGESTIONs are preserved as comments for the user to consider.

### 4.6 Step 6: User Review (Full Presentation + Summary)

The user sees the complete presentation followed by a collaboration summary and action options.

**Output structure:**

```
[6/6] Ready for your review.

--- PRESENTATION START ---

[Full presentation content in the requested format]

--- PRESENTATION END ---

## Collaboration Summary

| Role             | Slides Contributed | Artifacts Consumed                    |
|------------------|--------------------|---------------------------------------|
| Product Owner    | 2, 3, 9, 10       | 05-sprint-plan.md, risk-register.md   |
| Data Analyst     | 3, 7              | sprint-metrics.md, 07-uat-report.md   |
| Developer        | 4, 5              | FKC-auth-oauth.md, FKC-auth-rbac.md   |
| Architect        | 6                  | ADR-015.md                            |
| QA Engineer      | 8                  | 07-uat-report.md                      |
| Composer         | 1 (title), all (tone/transitions) | config.yml             |
| TW Reviewer      | — (review only)    | —                                     |
| UX Reviewer      | — (review only)    | —                                     |

**Warnings**: risk-register.md is 9 days old (staleness threshold: 7 days)
**Suggestions**: 2 (see Review Gate output above)
**[TBD] placeholders**: 0

Options:
- **approve** — save to .delivery/artifacts/presentations/sprint-review-2026-03-25.md
- **changes** — describe what to adjust (I'll route to the right step)
- **abort** — discard this draft
```

**Design rationale**: The collaboration summary serves two purposes: (1) it proves the deck is not single-source — multiple roles and artifacts contributed, and (2) it gives the user a quick audit trail to verify coverage. The [TBD] count is a trust metric — zero means every data point has a source. The options are verbs, not buttons, because this is a CLI interaction.

### 4.7 Request Changes Routing

When the user says "changes," the skill routes feedback to the appropriate step:

| Feedback Type | Routes To | Example |
|---------------|----------|---------|
| Structural (add/remove/reorder slides) | Step 1 (Assemble) | "Add a demo highlights slide after features" |
| Content (wrong data, missing info, different emphasis) | Step 3 (Draft) | "The velocity number on slide 7 should be story points, not hours" |
| Formatting/tone (layout, wording, density) | Step 4 (Compose) | "Make slide 3 more concise" or "Switch to paste-ready format" |

The skill re-executes from the routed step forward, not from the beginning. This is efficient — structural changes require a new outline, but formatting changes only require recomposition.

---

## 5. Config Integration

### 5.1 Setup Wizard: Not Included

Per PRD Section 10, all `presentation.*` config keys are optional with sensible defaults. The setup wizard does not ask about presentation configuration. This is intentional:

- The skill works out of the box with zero config
- Power users discover `presentation.*` keys through documentation or after using the skill and wanting to customize defaults
- Adding 7 questions to the wizard for an opt-in skill would slow down initial setup for all teams

### 5.2 Config Consumption

The SKILL.md documents which config keys exist and what they do. The skill reads them at the start of Step 1 (Assemble) and applies them as defaults that the user's explicit request overrides.

**Precedence chain** (highest to lowest):

1. Explicit user request ("make it paste-ready for executives")
2. `presentation.*` config keys
3. Hardcoded defaults (structured-markdown, technical audience, no speaker notes)

### 5.3 GAME_DEV Vocabulary

When `project.type: GAME_DEV` is detected in config, the skill activates vocabulary adaptation automatically. This is not a presentation config key — it reads the existing project type config. No new config needed for this behavior.

---

## Design Validation Checklist

| PRD Requirement | Addressed In |
|-----------------|-------------|
| FR-001: Read-only artifact access | Section 4.2 (Content Gate shows what was read) |
| FR-002: 4 presentation types | Section 2.1 (type detection), Section 3.2 (narrative-patterns.md) |
| FR-003: 6-step collaboration flow | Section 4 (full flow UX) |
| FR-004: Content Gate hard stop | Section 4.2 (fail output design) |
| FR-005/006: Co-primary formats | Section 2.1 (output format section in SKILL.md) |
| FR-007: Source citations | Section 4.6 (collaboration summary), Section 3.2 (citation formats in each reference) |
| FR-008: No hallucination | Section 3.2 (data-visualization.md accuracy rules) |
| FR-009: Parallel draft | Section 4.3 (progress indicator shows parallel roles) |
| FR-010: Composer assembly | Section 4.4 (silent compose step) |
| FR-011: Review Gate | Section 4.5 (findings summary UX) |
| FR-012: User Review | Section 4.6 (approve/changes/abort) |
| NFR-003: Context efficiency | Section 2 (290 lines), Section 3.1 (selective loading) |
| NFR-006: Format consistency | Section 3.2 (slide-structure.md boundary conventions) |
