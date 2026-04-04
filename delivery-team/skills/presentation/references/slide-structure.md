# Slide Structure Reference

Defines slide types, density rules, and recommended sequencing for each presentation type.

---

## Slide Types

### 1. Title Slide

**Purpose**: Establish presentation identity and context.
**When**: Always first slide.
**Structure**:
- Presentation title (concise, under 10 words)
- Subtitle (type + sprint/milestone/date context)
- Date
- Presenter name or team name
**Density**: No bullets. Four text elements maximum.

### 2. Agenda/Overview Slide

**Purpose**: Set expectations for what the audience will see.
**When**: Second slide for presentations with 8+ slides.
**Structure**:
- Numbered list of major sections (not individual slides)
- Group related slides under section headings
**Density**: Max 5 items. Max 8 words per item. No sub-bullets.

### 3. Section Divider Slide

**Purpose**: Visual break signaling a topic shift.
**When**: Between major sections in presentations with 10+ slides.
**Structure**:
- Section title (3-5 words)
- Optional one-line context sentence
**Density**: Two text elements maximum. No bullets.

### 4. Content Slide

**Purpose**: Convey information through structured bullet points.
**When**: Standard information delivery -- goals, features, findings, next steps.
**Structure**:
- Slide title stating the key message (not the topic)
- 3-5 bullets supporting the title claim
- Optional: one supporting detail line per bullet (indented)
**Density**: Max 5 bullets. Max 10 words per bullet. Max 7 words per sub-detail.

### 5. Metrics Slide

**Purpose**: Present quantitative data with trend context.
**When**: Velocity, completion rates, defect counts, KPIs, adoption data.
**Structure**:
- Slide title with the headline finding (e.g., "Velocity up 15% over 3 sprints")
- 2-3 data points with labels and values
- Trend indicator per data point (up/down/stable + magnitude)
- One highlight callout for the most important finding
**Density**: Max 3 data points. One callout. No bullet lists -- use data layout.

### 6. Comparison Slide

**Purpose**: Show contrast between two states or options.
**When**: Before/after, planned vs actual, option A vs B, risk assessment.
**Structure**:
- Slide title framing the comparison
- Two-column layout with clear column headers
- 3-5 rows of parallel items
- Optional: summary row or verdict line
**Density**: Max 5 rows. Max 8 words per cell. Two columns only.

### 7. Timeline Slide

**Purpose**: Show chronological sequence or roadmap.
**When**: Sprint milestones, release roadmap, project phases, delivery schedule.
**Structure**:
- Slide title indicating the time scope
- 4-6 milestones with dates/labels
- Current position marker (where we are now)
- Status per milestone (done, in progress, upcoming)
**Density**: Max 6 milestones. Max 6 words per milestone label. One timeline per slide.

### 8. Architecture Slide

**Purpose**: Visualize system structure, data flow, or component relationships.
**When**: System diagrams, integration views, deployment topology, data flow.
**Structure**:
- Slide title naming the view (e.g., "Payment Service Integration")
- One Mermaid diagram block
- 2-3 bullet annotations calling out key design decisions
**Density**: One diagram per slide. Max 3 annotation bullets. Max 10 words per annotation.

### 9. Demo/Screenshot Slide

**Purpose**: Placeholder for visual content the presenter will show live or paste.
**When**: Feature demos, UI walkthroughs, before/after screenshots.
**Structure**:
- Slide title describing what is shown
- `[DEMO]` or `[SCREENSHOT]` placeholder with description of expected content
- 1-2 bullet callouts highlighting what to notice
**Density**: One visual placeholder. Max 2 callout bullets.

### 10. Call-to-Action Slide

**Purpose**: Drive decisions, approvals, or next steps from the audience.
**When**: Final substantive slide (before optional Q&A). Pitch asks, decision requests, next steps.
**Structure**:
- Slide title as a direct statement (e.g., "We need budget approval by Friday")
- 2-4 specific action items with owners and deadlines
- Optional: one context line connecting back to the presentation narrative
**Density**: Max 4 action items. Max 10 words per item. Every item has an owner.

---

## Slide Sequencing by Presentation Type

### Sprint Review

1. Title Slide
2. Agenda/Overview
3. Content Slide -- Sprint Goals (planned vs achieved)
4. Metrics Slide -- Velocity, completion rate, defect trends
5. Content Slide -- Features Delivered (one per major feature, or grouped)
6. Demo/Screenshot Slide -- Key feature demonstration
7. Content Slide -- Quality Summary (test results, resolved defects)
8. Content Slide -- Next Sprint (upcoming goals, carry-overs)
9. Call-to-Action Slide -- Q&A / feedback requests

### Feature Pitch

1. Title Slide
2. Content Slide -- Problem Statement (user pain, business gap)
3. Content Slide -- Proposed Solution (what we build, how it solves the problem)
4. Architecture Slide -- Technical approach (high-level system view)
5. Metrics Slide -- Expected Impact (projected KPIs, adoption, cost savings)
6. Timeline Slide -- Delivery roadmap (phases, milestones, target dates)
7. Call-to-Action Slide -- The Ask (budget, approval, team allocation)

### Stakeholder Update

1. Title Slide
2. Agenda/Overview
3. Metrics Slide -- Progress against plan (completion %, milestones hit)
4. Comparison Slide -- Risks and mitigations (risk vs mitigation, or planned vs actual)
5. Call-to-Action Slide -- Decisions Needed (blockers requiring stakeholder input)
6. Timeline Slide -- Upcoming milestones (next 2-4 weeks)
7. Content Slide -- Next Steps (team actions, follow-ups)

### Technical Deep-Dive

1. Title Slide
2. Content Slide -- Context (why this matters, what problem is being solved)
3. Architecture Slide -- System design (primary diagram + key components)
4. Comparison Slide -- Design Decisions (options evaluated, trade-offs, rationale)
5. Content Slide -- Implementation Details (approach, patterns, constraints)
6. Metrics Slide -- Results or benchmarks (performance, quality, adoption data)
7. Call-to-Action Slide -- Q&A / next steps

### Investor Pitch

1. Title Slide
2. Content Slide -- Traction / Problem Validation (evidence that the problem is real and users care)
3. Content Slide -- Market Opportunity (TAM/SAM/SOM or market sizing, growth trends)
4. Content Slide -- Solution / Product (what we build, how it solves the validated problem)
5. Content Slide -- Business Model (revenue model, unit economics, pricing strategy)
6. Metrics Slide -- Metrics / Traction Proof (growth metrics, adoption data, revenue trajectory)
7. Content Slide -- Team *(optional)* (key team members, relevant experience, why this team wins)
8. Content Slide -- The Ask (funding amount, use of funds, timeline to milestones)
9. Call-to-Action Slide -- Next Steps (follow-up meeting, due diligence process, contact)

### Roadmap

1. Title Slide
2. Content Slide -- Strategic Context (vision, goals, why this roadmap matters now)
3. Content Slide -- Now (current sprint/phase work, active deliverables)
4. Content Slide -- Next (upcoming 1-2 sprints/phases, planned deliverables)
5. Content Slide -- Later (horizon items, exploratory, tentative)
6. Comparison Slide -- Dependencies / Risks (dependency vs mitigation, risk vs contingency)
7. Timeline Slide -- Timeline Overview (milestones across Now/Next/Later with dates)
8. Call-to-Action Slide -- Decisions Needed (approvals, resource asks, priority calls)

**Note**: Now/Next/Later slides are structural backbone slides. Their positions are locked during narrative tension passes -- the Composer must not reorder them.

### Product Demo

1. Title Slide
2. Content Slide -- The Hook (attention-grabbing problem or user story that sets up the demo)
3. Demo/Screenshot Slide -- Feature Demo 1 (`[DEMO]` placeholder + presenter timing notes in speaker notes)
4. Demo/Screenshot Slide -- Feature Demo 2 *(optional, repeat as needed)* (`[DEMO]` placeholder)
5. Metrics Slide -- Impact (adoption metrics, performance improvements, user feedback data)
6. Content Slide -- What's Next (upcoming features, iteration plans)
7. Call-to-Action Slide -- Try It / Next Steps (access instructions, feedback channels)

**`[DEMO]` placeholder conventions**:
- Use `[DEMO: description of what to show]` in slide body where a live demo occurs
- Add `**Timing**: ~N minutes` in speaker notes for each demo slide
- Add `**Fallback**: [SCREENSHOT: description]` in speaker notes in case live demo fails
- When `project.type: GAME_DEV`: replace "Feature Demo" titles with "Gameplay Demo", structure around mechanics not feature lists, use "publisher milestone" vocabulary

### Onboarding

1. Title Slide
2. Content Slide -- Project Context (why this project exists, business problem, users served)
3. Architecture Slide -- System Landscape (high-level architecture overview, key components)
4. Content Slide -- Key Decisions (important ADRs, design rationale, constraints accepted)
5. Content Slide -- Development Pathways (how to start contributing, dev setup, workflow)
6. Content Slide -- Resources / Links (documentation, team contacts, tools, glossary)
7. Call-to-Action Slide -- First Tasks (specific onboarding actions with owners and timelines)

### Retrospective Summary

1. Title Slide
2. Content Slide -- Celebrate (wins, achievements, team highlights)
3. Content Slide -- Learn (key lessons, what surprised us, process discoveries)
4. Content Slide -- Commit (action items with owners and deadlines)
5. Metrics Slide -- Trends *(optional)* (velocity trends, defect trends, improvement metrics over time)
6. Comparison Slide -- Previous Actions Review *(optional)* (last retro actions: planned vs actual progress)
7. Call-to-Action Slide -- Next Steps (top 3 commitments for next sprint/period)

---

## Density Rules

These rules apply across all slide types and presentation types. The Composer enforces them during Step 4 (Compose). Reviewers validate them in Step 5 (Review Gate).

| Rule | Limit |
|------|-------|
| Bullets per slide | Max 5 |
| Words per bullet | Max 10 |
| Data points per metrics slide | Max 3 |
| Diagrams per architecture slide | 1 |
| Action items per CTA slide | Max 4 |
| Timeline milestones per slide | Max 6 |
| Comparison rows per slide | Max 5 |
| Columns per comparison slide | 2 |

**Speaker notes carry the detail, slides carry the headlines.** If a bullet needs explanation, move the explanation to speaker notes. If a data point needs context, the speaker provides it verbally. The slide is a visual anchor, not a document.

**Overflow handling**: When content exceeds density limits, split into multiple slides of the same type rather than cramming. Title the continuation slides with the same base title plus a qualifier (e.g., "Features Delivered (continued)" or "Features Delivered -- Backend").
