---
name: presentation
description: Presentation Composer — assembles team contributions into cohesive presentations through a 6-step collaboration flow (Assemble, Content Gate, Draft, Compose, Review Gate, User Review). Supports 4 types: Sprint Review, Feature Pitch, Stakeholder Update, Technical Deep-Dive. Auto-detects type from user input or pipeline context. Produces structured markdown, Marp, or paste-ready output. Triggers on phrases like "create presentation", "sprint review", "sprint demo", "what we delivered", "pitch", "propose", "sell this feature", "why we should build", "status update", "executive update", "progress report", "technical presentation", "architecture overview", "deep dive", "how it works", "present", "slide deck", "stakeholder update".
license: Apache License 2.0 - See repository LICENSE file
---

# Presentation Composer

## Design Principle: Compose, Don't Create

This skill is a **mini-orchestrator**, not a content creator. The Composer assembles contributions from delivery team roles (PO, Data Analyst, Developer, Architect, QA) into a cohesive presentation. Each contributing role loads its own skill to produce domain-accurate content. The Composer shapes tone, flow, density, and format — the team creates the content.

**Context isolation**: Contributing roles run as sub-agents with only their relevant artifacts. The Composer reads their draft outputs from disk. No role's full context leaks into another.

**Signal**: `SKILL_LOADED: presentation`

---

## Presentation Type Detection

Detect type from user request using keyword matching. If ambiguous, ask — never guess.

| Type | Keywords |
|------|----------|
| Sprint Review | "sprint review", "what we delivered", "sprint demo", "end of sprint" |
| Feature Pitch | "pitch", "propose", "sell this feature", "why we should build", "feature pitch" |
| Stakeholder Update | "status update", "executive update", "progress report", "stakeholder" |
| Technical Deep-Dive | "technical presentation", "architecture overview", "deep dive", "how it works" |

### Pipeline Auto-Detection (when type not explicit)

| Current Stage | Default Type |
|---------------|-------------|
| Idea checkpoint | Feature Pitch |
| Design after DoD | Technical Deep-Dive |
| Plan after sprint planning | Stakeholder Update |
| UAT after acceptance | Sprint Review |
| UAT release | Stakeholder Update |

### GAME_DEV Vocabulary

When `project.type: GAME_DEV` in config, adapt vocabulary throughout all steps:
sprint -> milestone, features -> mechanics, UAT -> playtesting, modules -> systems, stories -> tasks, velocity -> throughput.

---

## 6-Step Collaboration Flow

### Step 1: Assemble (PO)

Output: `[1/6] Assembling presentation outline...`

Spawn a sub-agent with `delivery-team:product-delivery` (Product Owner role). Provide:
- User request (type, audience, format)
- Config context from `.delivery/config.yml`
- Pipeline state from `.delivery/state/` (if exists)

The PO produces a **Presentation Outline**:

| Column | Content |
|--------|---------|
| # | Slide number |
| Slide Title | Descriptive title |
| Content Owner | Role(s) responsible |
| Source Artifacts | File paths to read |

**Narrative adaptation**: The PO checks for problem signals in source data:
- Completion <80%: lead with "what we learned"
- Unresolved defects >5: quality slide before metrics
- Missed sprint goal: reframe around adjusted scope + rationale

Show adaptation status to user. User can say "no adaptation" to override.

Present outline to user. Wait for approval before proceeding.

### Step 2: Content Gate (Automated)

Output: `[2/6] Validating source artifacts...`

Validate required artifacts exist per type:

| Type | Required | Enhancing (optional) |
|------|----------|---------------------|
| Sprint Review | Sprint plan, UAT report/completion data | FKCs, metrics, retrospective, defect log |
| Feature Pitch | Idea brief or PRD | Architecture overview, competitive analysis |
| Stakeholder Update | Pipeline state, sprint plan/progress | Risk register, metrics, retrospective |
| Technical Deep-Dive | At least 1 architecture doc or ADR | Design decisions, code examples |

**Gate rules**:
- Missing required artifact: **STOP**. List what is missing, where it should be, how to create it.
- Empty/placeholder artifact: **WARN** + ask user to confirm proceeding.
- Stale artifact (>`staleness_warning_days`, default 7): **WARN** but proceed with notice.

On PASS, show what was found (required + enhancing) and any warnings.

### Step 3: Draft (Parallel — 5 Roles)

Output: `[3/6] Drafting slide content (N roles contributing)...`

Dispatch sub-agents **in parallel** based on the outline's role assignments. Only dispatch roles that have assigned slides.

| Sub-agent | Skill | Contributes |
|-----------|-------|-------------|
| Product Owner | `delivery-team:product-delivery` | Narrative slides (goals, priorities, next steps) |
| Data Analyst | `delivery-team:product-delivery` | Metric slides (velocity, completion, trends) |
| Developer | `delivery-team:developer` | Feature slides (implementation highlights) |
| Architect | `delivery-team:architect` | Architecture slides (decisions, diagrams) |
| QA Engineer | `delivery-team:quality` | Quality slides (test results, defect data) |

Each sub-agent receives:
- Its assigned slide numbers and titles from the outline
- Paths to its relevant source artifacts only
- Presentation type, audience mode, and content rules

Each sub-agent writes output to: `.delivery/artifacts/presentations/.drafts/{role}-slides.md`

**Content rules for all sub-agents**:
- Every data point must cite its source artifact
- Missing data: use `[TBD]` — never fabricate
- Stay within assigned slide scope
- Write at the detail level appropriate for audience

Show the user which roles contribute to which slides (progress indicator), then proceed silently.

### Step 4: Compose (Composer — this skill)

Output: `[4/6] Composing final presentation...`

Read all draft files from `.delivery/artifacts/presentations/.drafts/`. Assemble into final deck:

1. **Load references**: Always load `slide-structure.md` and `narrative-patterns.md`. Load `marp-templates.md` if format is Marp. Load `data-visualization.md` if metric or architecture slides exist.
2. **Apply narrative arc** from `narrative-patterns.md` for the detected type
3. **Add opening slide** (title, date, project context from config) and **closing slide** (next steps, CTA)
4. **Normalize tone** across all role contributions for the target audience
5. **Enforce density**: max 5-7 bullets per slide, 1 key message per slide, max 2 visualizations
6. **Write transitions** between slides for narrative flow
7. **Apply output format** (structured markdown, Marp, or paste-ready conventions)
8. **Insert citations** per slide in the format appropriate for the output mode
9. **Add speaker notes** only if requested (off by default)

Write composed draft to `.delivery/artifacts/presentations/.drafts/composed-draft.md`.

### Step 5: Review Gate (TW + UX)

Output: `[5/6] Reviewing draft (Technical Writer + UX Designer)...`

Dispatch two reviewer sub-agents **in parallel**:

| Reviewer | Skill | Focus |
|----------|-------|-------|
| Technical Writer | `delivery-team:operations` | Clarity, jargon for audience, scannable titles, single message per slide |
| UX Designer | `delivery-team:ui` | Density, hierarchy, visual story, readability when projected |

Each reviewer reads `composed-draft.md` and returns findings as:
- **MUST-FIX**: Blocks user review. Composer fixes these automatically before Step 6.
- **SUGGESTION**: Included as notes for user awareness.

Show review summary to user (issues found, what was fixed, suggestions preserved).

### Step 6: User Review

Output: `[6/6] Ready for your review.`

Present to the user:
1. The complete presentation between `--- PRESENTATION START ---` and `--- PRESENTATION END ---`
2. A **Collaboration Summary** table: role | slides contributed | artifacts consumed
3. Warnings (staleness, [TBD] count)
4. Suggestions from Review Gate
5. Options:
   - **approve** — save to `.delivery/artifacts/presentations/{type}-{date}.md`
   - **changes** — describe what to adjust
   - **abort** — discard draft

**Change routing** (when user says "changes"):

| Feedback Type | Routes To | Example |
|---------------|----------|---------|
| Structural (add/remove/reorder slides) | Step 1 | "Add a demo slide after features" |
| Content (wrong data, different emphasis) | Step 3 | "Velocity should be in story points" |
| Formatting/tone (layout, wording) | Step 4 | "Make slide 3 more concise" |

Re-execute from the routed step forward, not from the beginning.

**On approve**: Save final presentation. Clean up `.drafts/` directory.
**On abort**: Clean up `.drafts/` directory. No artifacts saved.

---

## Output Format Specifications

### Structured Markdown (default)

```markdown
# [Type]: [Project] — [Context]

---

## Slide N: [Title]

[Content — bullets, tables, text]

> Generated from: artifact-1.md, artifact-2.md

---
```

Speaker notes (when enabled): `**Notes**: [talking points]` after citation.

### Marp

Load `references/marp-templates.md` for full syntax. Key conventions:
- Frontmatter: `marp: true`, `theme`, `paginate: true`, `header`, `footer`
- Slide separator: `---`
- Citations: `<!-- Generated from: artifact.md -->`
- Speaker notes: `<!-- notes: talking points -->`
- Theme from `presentation.marp_theme` config (default: "default")

### Paste-Ready

```
=== SLIDE N: [Title] ===
Headline: [key message]
Body: [content]
Source: artifact-1.md, artifact-2.md
```

No markdown formatting. No frontmatter. Clean content blocks for corporate templates.

---

## Error Handling

| Error | Detection | Behavior |
|-------|-----------|----------|
| Missing config | `.delivery/config.yml` not found | STOP: "No delivery config found. Run setup wizard or create config." |
| Missing required artifacts | Content Gate: required paths do not exist | STOP: list missing artifacts, expected locations, creation instructions |
| Empty artifacts | File exists but 0 bytes or template-only | WARN + ask user to confirm. Affected slides use [TBD]. |
| Stale artifacts | Last modified > staleness threshold | WARN but proceed. Staleness notice on affected slides. |
| Unknown type | Type not in v1 set | STOP: list supported types + planned v1.1 types |
| No pipeline state | `.delivery/state/` empty or missing | WARN: proceed with artifacts only, [TBD] for progress data |
| Partial data | Role finds insufficient data for slides | Role outputs what it can with [TBD]. Composer flags in summary. |

Error message format: **what** is wrong, **where** to fix it, **how** to fix it.

---

## User Commands

| Command | Action |
|---------|--------|
| `present` | Start presentation flow (detect type from context) |
| `present [type]` | Start with explicit type |
| `present --format [fmt]` | Set output format: structured-markdown, marp, paste-ready |
| `present --audience [mode]` | Set audience: technical, executive, investor, client-facing, casual |
| `present --notes` | Enable speaker notes |
| `approve` | Accept presentation, save to artifacts |
| `changes` | Provide feedback, re-enter flow at appropriate step |
| `abort` | Discard draft, clean up |
| `regenerate` | Re-run full flow with current artifacts |

---

## References

| File | Loaded When | Purpose |
|------|------------|---------|
| `references/slide-structure.md` | Always | Slide types, density rules, sequencing, boundary conventions |
| `references/narrative-patterns.md` | Always | Per-type narrative arcs, adaptation rules, tone/vocabulary |
| `references/marp-templates.md` | Format is Marp | Marp syntax, directives, layouts, themes |
| `references/data-visualization.md` | Metric or architecture slides exist | Chart patterns, Mermaid diagrams, data accuracy rules |

---

## Config Integration

Read from `.delivery/config.yml` at start of Step 1. User's explicit request overrides config. Config overrides hardcoded defaults.

| Key | Type | Default | Purpose |
|-----|------|---------|---------|
| `presentation.default_format` | string | structured-markdown | Default output format |
| `presentation.default_audience` | string | technical | Default audience mode |
| `presentation.speaker_notes` | boolean | false | Enable speaker notes by default |
| `presentation.save_to_artifacts` | boolean | true | Save approved output to artifacts dir |
| `presentation.marp_theme` | string | default | Marp theme (default, gaia, uncover) |
| `presentation.staleness_warning_days` | integer | 7 | Days before staleness warning |
| `presentation.vocabulary_overrides` | map | {} | Custom term replacements (term -> replacement) |

**Precedence**: explicit request > `presentation.*` config > hardcoded defaults.

**No config?** Skill works with all defaults. Config is optional.
