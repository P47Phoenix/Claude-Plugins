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

### 5. Traction-Opportunity-Ask

**Best for**: Investor Pitches

Structure:
- **Traction**: Prove the problem is real. Show validated demand -- user numbers, revenue, engagement metrics, waitlist size. Lead with evidence, not vision.
- **Opportunity**: Size the market. TAM/SAM/SOM, growth trends, competitive landscape gaps. Frame the opportunity as urgent and underserved.
- **Ask**: State the funding request. Amount, use of funds, milestones the funding unlocks, timeline to next raise or profitability.

Arc: proof -> scale -> commitment.

Audience-specific tone: Future-focused, metrics-driven. Use investor vocabulary: "runway", "traction", "unit economics", "burn rate", "MRR/ARR". Frame features as market advantages, not technical achievements. Every slide should answer "why now?" and "why this team?"

Key emphasis areas: Traction proof slides carry the highest weight. Investors fund evidence, not ideas. The Ask slide must be specific -- vague asks lose credibility.

### 6. Now-Next-Later

**Best for**: Roadmaps

Structure:
- **Now**: What is actively in progress. Current sprint/phase deliverables, active work items, completion status.
- **Next**: What is planned for the upcoming 1-2 cycles. Committed items with estimated timelines.
- **Later**: Horizon items. Exploratory, tentative, subject to change. Clearly labeled as provisional.

Arc: certainty -> commitment -> possibility.

Audience-specific tone: Confidence gradient -- "Now" speaks with certainty ("we are delivering"), "Next" speaks with commitment ("we plan to"), "Later" speaks with possibility ("we are exploring"). Never overpromise on Later items.

Key emphasis areas: Timeline slides are the structural backbone. Now/Next/Later positions are locked during narrative passes. Dependencies and risks deserve their own slide -- never bury them in content slides.

### 7. Hook-Show-Impact

**Best for**: Product Demos

Structure:
- **Hook**: Open with the user problem or a compelling scenario. Make the audience feel the pain or excitement before showing the solution.
- **Show**: Live demonstration or walkthrough. Feature by feature, with `[DEMO]` placeholders and timing. Let the product speak.
- **Impact**: Close with measured results. Adoption metrics, performance improvements, user feedback. Connect the demo back to business value.

Arc: attention -> demonstration -> proof.

Audience-specific tone: Energetic but grounded. The Hook creates anticipation, the Show delivers on it, the Impact proves it matters. For GAME_DEV: the Hook is a gameplay scenario, the Show is mechanics in action, the Impact is player engagement data.

Key emphasis areas: Demo slides are the centerpiece. Speaker notes must include timing and fallback plans. Impact metrics should directly reference what was demonstrated -- never disconnect the demo from the numbers.

### 8. Context-Landscape-Pathways

**Best for**: Onboarding

Structure:
- **Context**: Why this project exists. Business problem, users served, project history. Assume zero prior knowledge.
- **Landscape**: What the system looks like. Architecture overview, key components, integration points, technology stack. Orient the newcomer in the codebase.
- **Pathways**: How to start contributing. Dev environment setup, workflow conventions, first tasks, who to ask for help.

Arc: purpose -> orientation -> action.

Audience-specific tone: Welcoming and practical. Default audience is technical. Avoid jargon that assumes project-specific knowledge (explain acronyms, name systems explicitly). Every slide should answer "what do I need to know to be productive?"

Key emphasis areas: The Landscape slide (architecture overview) is the anchor -- newcomers reference it repeatedly. Pathways must include specific, actionable first tasks, not vague guidance. Resources/Links slide is critical -- a dead link on day one is worse than no link.

### 9. Celebrate-Learn-Commit

**Best for**: Retrospective Summaries

Structure:
- **Celebrate**: What went well. Team wins, individual highlights, process improvements that paid off. Start with positive energy.
- **Learn**: What we discovered. Surprises, failures reframed as lessons, process gaps identified. Honest but constructive.
- **Commit**: What we will do differently. Specific action items with owners and deadlines. Measurable commitments, not vague intentions.

Arc: gratitude -> honesty -> accountability.

Audience-specific tone: For "technical" or "casual" audiences -- candid, team-internal, specific names and details preserved. For "executive" or "client-facing" audiences -- generalized, process-focused, anonymized (see Sensitivity Filter Rules below).

Key emphasis areas: Commit slides carry the most weight -- retrospectives without commitments are theater. Previous action review (if available) builds accountability chain. Celebrate slides prevent the retro from being purely corrective.

---

## Default Framework by Presentation Type

| Presentation Type | Default Framework | Rationale |
|-------------------|-------------------|-----------|
| Sprint Review | SCR | Natural fit: sprint goal (situation), challenges (complication), delivered work (resolution) |
| Feature Pitch | Problem-Solution-Benefit | Persuasion structure: establish need, present approach, prove value |
| Stakeholder Update | Pyramid Principle | Executives want the answer first, details on demand |
| Technical Deep-Dive | Before-After-Bridge | Engineers want to understand what changed and the reasoning behind it |
| Investor Pitch | Traction-Opportunity-Ask | Investors fund evidence: prove traction, size the opportunity, make the ask |
| Roadmap | Now-Next-Later | Natural time horizon: certainty gradient from active work to exploratory |
| Product Demo | Hook-Show-Impact | Demo-centric: create anticipation, deliver the product, prove the value |
| Onboarding | Context-Landscape-Pathways | Newcomer-centric: explain purpose, orient in system, enable contribution |
| Retrospective Summary | Celebrate-Learn-Commit | Retro-native: honor wins, extract lessons, commit to actions |

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

---

## Sensitivity Filter Rules (Retrospective Summary)

The sensitivity filter applies **only** to the Retrospective Summary type and **only** when the audience mode is "executive" or "client-facing". It does NOT apply for "technical", "casual", or "investor" audiences.

### When Filter is ACTIVE (executive, client-facing)

| Rule | Action |
|------|--------|
| Individual feedback | Generalize to team patterns. Replace "Alice said X" with "Team members noted X" |
| Named contributors | Omit names from specific feedback. Use role references ("a developer noted") or team references ("the team found") |
| Challenges/frustrations | Frame as process improvements, not personnel issues. Replace "We struggled with code reviews" with "The code review process has improvement opportunities" |
| Interpersonal friction | Omit entirely. These are team-internal and not appropriate for external audiences |
| Specific failure attribution | Replace with systemic framing. "The deploy failed because X didn't test" becomes "A gap in the testing process was identified" |
| Action item owners | Keep role-level ownership ("Developer lead will...") but omit individual names for client-facing. Executive audiences may keep names if they know the team |

### When Filter is INACTIVE (technical, casual)

Full detail from retrospective notes is preserved. Names, specific feedback, candid language, and individual attributions remain intact. These audiences are team-internal and benefit from specificity.

### Disclaimer (Always Active)

Regardless of audience mode, every Retrospective Summary presentation displays:

> "This presentation summarizes team retrospective themes. Individual feedback has been anonymized and generalized."

This disclaimer appears on the title slide or as the first line after the title slide.

---

## Audience Framing Rules

These rules govern Pass 3 (Audience-Specific Framing) in Step 4 (Compose). Framing goes beyond vocabulary swaps — it restructures the *argument* within each slide based on what the audience values. Applied to all surviving slides after cutting.

### Investor Framing

| Aspect | Rule |
|--------|------|
| Lead | Market opportunity or traction impact. Every slide opens with "why this matters to the market." |
| Features | Frame as competitive advantages, not technical achievements. "We built X" becomes "X gives us a defensible advantage in Y market." |
| Metrics | Quantify in business terms: revenue impact, growth rate, market share gained, CAC/LTV, unit economics. Internal metrics (velocity, story points) are omitted. |
| Technical detail | Minimize. Architecture is relevant only when it creates a moat or scalability advantage. |
| Framing verb | "captures", "unlocks", "positions", "validates" |
| Slide structure | Claim (1 line) > Evidence (2-3 bullets with numbers) > So-what (1 line connecting to investment thesis) |

### Executive Framing

| Aspect | Rule |
|--------|------|
| Lead | Business value or cost impact. Every slide opens with the ROI angle. |
| Features | Frame as business capabilities delivered. "JWT rotation" becomes "Reduced security incident response time by 40%." |
| Metrics | Show trends over absolutes. "Velocity increased 15% over 3 sprints" over "Velocity is 42 points." Decision-ready data. |
| Technical detail | Abstract to capability level. Name the capability, not the implementation. |
| Framing verb | "delivered", "reduced", "improved", "enabled", "recommend" |
| Slide structure | Outcome (1 line) > Supporting data (2-3 bullets) > Recommendation or decision needed (1 line) |

### Technical Framing

| Aspect | Rule |
|--------|------|
| Lead | Architecture decisions, patterns, and trade-offs. Show the "why" behind choices. |
| Features | Explain the implementation approach, patterns used, and alternatives considered. |
| Metrics | Raw metrics: latency (p50/p95/p99), throughput, error rates, test coverage, code complexity scores. |
| Technical detail | Full depth. System names, version numbers, dependency graphs, ADR references. |
| Framing verb | "implemented", "refactored", "migrated", "resolved", "trade-off" |
| Slide structure | Decision/Change (1 line) > Rationale with alternatives considered (2-3 bullets) > Impact on system (1 line) |

### Customer / Client-Facing Framing

| Aspect | Rule |
|--------|------|
| Lead | Outcomes the customer requested or benefits they experience directly. |
| Features | Frame in terms of the customer's workflow. "New export API" becomes "You can now export reports in 3 formats directly from your dashboard." |
| Metrics | Customer-relevant only: response time improvements, new capabilities, resolved issues from their feedback. |
| Technical detail | None. Zero internal process references (no "sprint", no "retro", no "pipeline"). |
| Framing verb | "now available", "resolved", "improved for you", "based on your feedback" |
| Slide structure | What changed for you (1 line) > How it helps (2-3 bullets) > What's coming next (1 line) |

### Casual Framing

| Aspect | Rule |
|--------|------|
| Lead | Team wins and shared accomplishments. Conversational energy. |
| Features | Celebrate the work. "We shipped the new dashboard — it's live!" |
| Metrics | Keep it light. Highlight wins, not granular data. "Tests passing, no regressions" over "Coverage at 87.3%." |
| Technical detail | Light touch — enough for the team to follow, not a deep dive. |
| Framing verb | "shipped", "nailed", "figured out", "knocked out" |
| Slide structure | Win (1 line) > Quick context (1-2 bullets) > Shout-out or fun note (1 line) |

### Type-Specific Emphasis Weight Modifiers

When audience framing combines with presentation type, certain slide categories carry extra weight:

| Type | Highest-Weight Slides | Rationale |
|------|----------------------|-----------|
| Sprint Review | Achievement slides, metrics slides | The audience wants to know what was delivered |
| Feature Pitch | Problem slides, benefit slides | Persuasion requires strong problem framing and clear payoff |
| Stakeholder Update | Status slides, risk slides | Decision-makers need current state and risk awareness |
| Technical Deep-Dive | Architecture slides, trade-off slides | Engineers value the "why" and the alternatives |
| Investor Pitch | Traction slides, market opportunity slides | Investors fund evidence and scale potential |
| Roadmap | Timeline slides, dependency slides | Planning audiences need sequencing and risk |
| Product Demo | Demo slides, impact slides | Show-don't-tell; the demo IS the argument |
| Onboarding | Landscape slides, pathways slides | Newcomers need orientation and actionable first steps |
| Retrospective Summary | Commit slides, learn slides | Retros without commitments are theater |

---

## Narrative Tension Patterns

These rules govern Pass 4 (Narrative Tension) in Step 4 (Compose). Tension creates a narrative arc that builds toward a key insight rather than presenting information flatly.

### Core Tension Rule

Identify the **climax slide** — the single most important insight, decision, or result — and position it at the **60-70% point** of the presentation. This creates a build-up (rising action), a peak (the climax), and a resolution (denouement/next steps).

**Minimum threshold**: Skip this pass if the presentation has fewer than 6 slides. Tension arcs need runway.

### Tension Patterns by Type

| Type | Pattern | Climax Identification | Example Arc |
|------|---------|----------------------|-------------|
| Sprint Review | Tension-Resolution | The key achievement that best represents the sprint's value. Look for the slide with the strongest metric or highest user impact. | Goals > Challenges > Work items > **Key Achievement** > Remaining items > Next sprint |
| Feature Pitch | Problem-Solution-Result | The solution slide — the moment the pitch "answers" the problem. | Problem depth > Market evidence > Alternatives rejected > **Our Solution** > Benefits > CTA |
| Stakeholder Update | Tension-Resolution | The most significant status change or decision needed. | Context > Progress > **Key Risk or Decision** > Mitigation > Next steps |
| Technical Deep-Dive | Before-After | The architecture decision that resolved the core technical challenge. | Legacy state > Pain points > Alternatives > **Architecture Decision** > New state > Trade-offs |
| Investor Pitch | Problem-Solution-Result | The traction proof slide — the moment the pitch shifts from vision to evidence. | Market problem > Opportunity size > **Traction Proof** > Solution > Business model > The Ask |
| Roadmap | Tension-Resolution | The most impactful "Next" item — the commitment that creates the most anticipation. | Strategic context > Now (certainty) > **Key Next commitment** > Later (possibility) > Dependencies > Timeline |
| Product Demo | Before-After | The demo moment — the slide where the product speaks for itself. | Hook/problem > Context > **[DEMO] Core Feature** > Supporting features > Impact metrics > CTA |
| Onboarding | Tension-Resolution | The architecture landscape slide — the "aha" moment where the system clicks. | Project context > **System Landscape** > Key decisions > Development pathways > Resources |
| Retrospective Summary | Tension-Resolution | The most impactful commitment — the action item that addresses the biggest learning. | Celebrations > Learnings > **Key Commitment** > Supporting actions > Accountability |

### Reordering Rules for Tension

1. **Position-locked slides never move**: Title, Opening, CTA, Next Steps, and framework-locked positions (e.g., Now/Next/Later boundaries in Roadmaps) stay fixed.
2. **Reorder within unconstrained groups**: Slides between locked positions can be reordered to build tension. Move supporting/context slides before the climax, move resolution/outcome slides after it.
3. **Preserve logical dependencies**: If slide B references content from slide A, A must remain before B regardless of tension positioning.
4. **Single climax**: Only one climax slide per presentation. If multiple slides compete, choose the one with the strongest data backing.
5. **Output**: Append to emphasis log: `"Climax: {slide title} positioned at {N}/{total} ({percentage}%)"`
