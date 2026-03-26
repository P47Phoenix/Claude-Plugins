# Narrative Patterns

Reference for the Presentation Composer (Step 4). Defines narrative frameworks, type mappings, adaptation rules, audience tone, and jargon translation.

---

## Narrative Frameworks

### 1. Situation-Complication-Resolution (SCR)

**Best for**: Sprint Reviews, Stakeholder Updates

Structure:
- **Situation**: Where we were at the start of the sprint/period. Context, goals, constraints.
- **Complication**: What challenged us. Scope changes, blockers, discoveries, trade-offs.
- **Resolution**: What we delivered. Outcomes, metrics, artifacts produced.

Arc: grounded opening -> honest tension -> concrete resolution.

### 2. Pyramid Principle (Minto)

**Best for**: Executive audiences, Stakeholder Updates

Structure:
- **Conclusion first**: Lead with the answer. What happened, what it means.
- **Supporting arguments**: 2-3 key points that back the conclusion.
- **Evidence**: Data, metrics, artifacts that prove each argument.

Arc: answer -> reasoning -> proof. Top-down, never bottom-up.

### 3. Problem-Solution-Benefit

**Best for**: Feature Pitches

Structure:
- **Problem**: The pain point. Who suffers, how much, what it costs.
- **Solution**: Our approach. What we built or propose, how it works.
- **Benefit**: The value delivered. Quantified impact, user outcomes, competitive advantage.

Arc: empathy -> clarity -> motivation.

### 4. Before-After-Bridge

**Best for**: Technical Deep-Dives

Structure:
- **Before**: How the system/process was. Architecture, limitations, pain points.
- **After**: How it is now. New architecture, capabilities, improvements.
- **Bridge**: What changed and why. Decisions made, trade-offs accepted, ADRs referenced.

Arc: context -> transformation -> rationale.

---

## Default Framework by Presentation Type

| Presentation Type | Default Framework | Rationale |
|-------------------|-------------------|-----------|
| Sprint Review | SCR | Natural fit: sprint goal (situation), challenges (complication), delivered work (resolution) |
| Feature Pitch | Problem-Solution-Benefit | Persuasion structure: establish need, present approach, prove value |
| Stakeholder Update | Pyramid Principle | Executives want the answer first, details on demand |
| Technical Deep-Dive | Before-After-Bridge | Engineers want to understand what changed and the reasoning behind it |

The Composer applies the default framework unless the user explicitly requests a different one.

---

## Narrative Adaptation Rules

When source data signals problems, the Composer shifts the narrative arc. These rules apply automatically during Step 4 (Compose). The PO may also apply them during Step 1 (Assemble).

### Completion Rate < 80%

Shift from "celebration" to "progress + learnings."

- Lead with what WAS delivered, not what was planned
- Acknowledge the gap directly: "We completed N of M planned items"
- Frame incomplete items as scope adjustment, not failure
- Add a "What We Learned" slide before "Next Steps"
- Never use phrases like "we failed to" or "unfortunately"

### Unresolved Defects > 5

Add a "Quality Focus" section.

- Insert a quality slide before the metrics slide
- Frame defects as investment in quality: "We identified N issues and resolved M"
- Show defect resolution rate, not just defect count
- If resolution rate > 70%, frame as "active quality management"
- If resolution rate < 50%, frame as "quality items carrying forward" with a plan

### Missed Sprint Goal

Reframe around learning and adjusted priorities.

- Address the miss directly in the first 3 slides -- never bury it
- Use language: "We adjusted our sprint goal based on [reason]"
- Show what WAS accomplished despite the goal change
- Include a root cause slide (scope creep, estimation, external dependency)
- Close with corrective action for the next sprint

### All Green (Completion > 95%, Defects < 2)

Full celebration arc.

- Lead with the achievement: "Sprint goal met with [X]% completion"
- Highlight individual and team contributions
- Show trend data if available (velocity over time, quality trend)
- Keep "Next Steps" forward-looking and ambitious

---

## Audience Tone Adaptation

### Technical

- Use precise technical terms without simplification
- Include code references, architecture details, system names
- Acceptable: "We refactored the auth middleware to use JWT rotation"
- Data format: raw metrics, percentages, technical benchmarks

### Executive

- No jargon. Lead with business impact.
- Metrics first, explanation second
- Use "delivered value" not "closed stories"
- Use "on track" / "needs attention" not "green" / "red"
- Acceptable: "Authentication improvements reduced support tickets by 40%"

### Investor

- Future-focused. Market opportunity, growth metrics.
- Competitive positioning and differentiation
- Use "runway", "traction", "unit economics" vocabulary
- Frame features as market advantages, not technical achievements

### Client-Facing

- Professional, outcomes-focused
- Translate all internal terms (see Jargon Translation Table)
- No internal process references (no "retro", no "standup")
- Acceptable: "The latest release includes three improvements your team requested"

### Casual

- Conversational, team-focused
- Celebrate wins informally
- First-person plural: "we shipped", "we learned"
- Acceptable: "Big win this sprint -- the new dashboard is live"

---

## Jargon Translation Table

Use this table when composing for non-technical audiences. The Composer replaces internal terms with audience-appropriate alternatives based on audience mode.

| Internal Term | Executive | Client-Facing | Investor | Casual |
|---------------|-----------|---------------|----------|--------|
| Sprint | Development cycle | Release period | Iteration | Sprint (keep) |
| DoD | Quality criteria | Acceptance standards | Quality bar | Definition of done |
| Blocker | Impediment | Delay | Risk item | Blocker (keep) |
| Spike | Research phase | Investigation | Exploratory work | Spike (keep) |
| Technical debt | Maintenance backlog | System improvements | Infrastructure investment | Tech debt (keep) |
| Velocity | Delivery rate | Team throughput | Development capacity | Velocity (keep) |
| Retro / Retrospective | Process review | (omit) | (omit) | Retro (keep) |
| Standup | Daily sync | (omit) | (omit) | Standup (keep) |
| PR / Pull request | Code review | Quality check | (omit) | PR (keep) |
| CI/CD | Automated deployment | Release automation | DevOps pipeline | CI/CD (keep) |
| ADR | Architecture decision | Design decision | Technical strategy | ADR (keep) |
| FKC | Feature summary | Feature documentation | (omit) | FKC (keep) |
| UAT | User acceptance testing | Validation | Quality assurance | UAT (keep) |
| Backlog | Planned work | Upcoming features | Product roadmap | Backlog (keep) |
| Story points | Effort estimate | (omit) | (omit) | Points (keep) |

**(omit)** means the term should not appear for that audience. Rephrase the sentence to avoid it entirely.

### GAME_DEV Vocabulary Override

When `project.type: GAME_DEV` in config, apply these replacements globally before audience adaptation:

| Standard Term | GAME_DEV Replacement |
|---------------|---------------------|
| Sprint | Milestone |
| Features | Mechanics |
| UAT | Playtesting |
| Modules | Systems |
| Stories | Tasks |
| Velocity | Throughput |

These replacements apply first, then audience tone adaptation applies on top.
