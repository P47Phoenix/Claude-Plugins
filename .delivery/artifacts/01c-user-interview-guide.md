# User Interview Guide: Claude-Plugins Marketplace

**Prepared by**: Product Owner
**Date**: 2026-03-28
**Version**: 1.0
**Objective**: Validate assumptions and discover unmet needs for the Claude-Plugins marketplace

---

## Section 1: Interview Framework

### Interview Objectives

1. **Understand current workflows** -- How do users extend Claude Code today, and where do they hit walls?
2. **Identify unmet needs** -- What tasks do users repeatedly attempt that no existing plugin addresses?
3. **Validate marketplace assumptions** -- Is the plugin/skill distinction clear? Does the 3-level context loading model match how users think about extensibility?
4. **Discover adoption barriers** -- What prevents users from installing, configuring, or trusting plugins?
5. **Prioritize next investments** -- Which new capabilities would deliver the most value relative to effort?

### Target User Segments

| # | Segment | Selection Criteria | Sample Size | Rationale |
|---|---------|-------------------|-------------|-----------|
| 1 | **Solo developers / indie hackers** | Use Claude Code daily on personal or side projects; 0-1 plugins installed; less than 2 years professional experience OR self-taught | 5-7 | Represent the "long tail" of users. High volume, low configuration tolerance. Reveal onboarding friction. |
| 2 | **Team leads / engineering managers** | Manage 3+ developers; responsible for team tooling decisions; use or evaluate CI/CD pipelines | 4-6 | Gate-keepers for team-wide adoption. Reveal governance, compliance, and standardization needs. |
| 3 | **Consultants / freelancers** | Work across 2+ client codebases simultaneously; bill by deliverable or hour; client-facing reporting responsibilities | 4-5 | Multi-project users who stress-test isolation, context switching, and output formatting. |
| 4 | **Game developers** | Use Godot, Unity, or Unreal; ship or actively develop a game project; may or may not use Claude Code today | 3-5 | Specialized domain with unique vocabulary, toolchain, and artifact types. Tests whether the marketplace serves niche verticals effectively. |
| 5 | **AI/ML practitioners** | Build or maintain AI-powered features; use prompt engineering, agent frameworks, or LLM APIs regularly | 3-5 | Power users who understand the underlying technology. Reveal advanced extensibility needs and competitive alternatives. |

**Total target**: 19-28 interviews

### Interview Logistics

| Parameter | Value |
|-----------|-------|
| **Duration** | 35 minutes (5 warm-up + 15 discovery + 10 validation + 5 closing) |
| **Format** | 1-on-1 video call preferred; audio-only acceptable; asynchronous written responses as last resort |
| **Recording** | Request consent at start. Record audio for transcription. No video recording unless participant opts in. |
| **Compensation** | Offer early access to new plugins or a 30-minute "office hours" session with the team |
| **Scheduling** | Send calendar invite with a 1-paragraph context blurb. Do not share the interview questions in advance. |
| **Note-taking** | Dedicated note-taker (not the interviewer). Use the analysis template in Section 6. |
| **Consent script** | "We're interviewing Claude Code users to understand how they work and what they need. This conversation will be recorded for internal analysis only. You can skip any question or stop at any time. Nothing you say will be attributed to you by name without your permission. Is that okay?" |

---

## Section 2: Warm-Up Questions (5 min)

**Goal**: Establish rapport, understand the user's context, and calibrate the rest of the interview.

### Q1: Background and Role
**Ask**: "Tell me about your current role and what kind of projects you work on day to day."

- **Follow-up probes**:
  - "How large is the codebase you spend the most time in?"
  - "Do you work solo or with a team? How many people?"
  - "What languages or frameworks do you use most?"
- **Target segment**: All
- **Assumption check**: None -- this is purely contextual.

### Q2: Claude Code Usage Patterns
**Ask**: "Walk me through how you typically use Claude Code in a normal work session. What does that look like?"

- **Follow-up probes**:
  - "How often do you use it -- daily, weekly, occasionally?"
  - "What kinds of tasks do you use it for most?"
  - "Are there tasks where you start to use it but then switch to doing it manually? What makes you switch?"
- **Target segment**: All
- **Assumption check**: We assume users have established usage patterns. Some may be sporadic users -- note this.

### Q3: Current Pain Points
**Ask**: "What's the most frustrating part of your workflow right now -- whether or not it involves Claude Code?"

- **Follow-up probes**:
  - "How often does that happen?"
  - "What have you tried to work around it?"
  - "If that problem disappeared tomorrow, what would change for you?"
- **Target segment**: All
- **Assumption check**: We assume pain points exist. If the user says "nothing, it's great," probe: "Tell me about the last time something took longer than you expected."

---

## Section 3: Feature Discovery Questions (15 min)

**Goal**: Uncover unmet needs using Jobs-to-be-Done framing. Never describe a feature -- let the user describe their problems.

### Q4: Unmet Needs (JTBD)
**Ask**: "Think about the last time you were trying to get something done with Claude Code and it didn't work the way you expected, or you had to do a bunch of extra steps. What were you trying to accomplish?"

- **Follow-up probes**:
  - "What did you end up doing instead?"
  - "How long did the workaround take compared to what you expected?"
  - "Has that happened more than once?"
- **Target segment**: All
- **Assumption check**: We assume users have encountered friction. If they haven't, pivot to: "What's a task you wish you could hand off to Claude Code but haven't tried yet?"

### Q5: Workflow Gaps
**Ask**: "Are there parts of your development workflow where you don't use Claude Code at all, even though you use it for other things? What are those parts and why?"

- **Follow-up probes**:
  - "Is that because you tried and it didn't work, or because you assumed it wouldn't?"
  - "What would need to be true for you to use it there?"
  - "What tool or process do you use for that part instead?"
- **Target segment**: All
- **Assumption check**: We assume gaps exist in adoption. This question tests whether the marketplace's current plugin coverage matches real workflow stages.

### Q6: Frustration Recall
**Ask**: "Tell me about the last time you spent way too long on something that felt like it should have been automated or easier."

- **Follow-up probes**:
  - "What specifically made it take so long?"
  - "Was it a one-time thing or does it recur?"
  - "If someone built a tool that handled that, what would it need to do to earn your trust?"
- **Target segment**: All
- **Assumption check**: We assume repetitive manual work exists. Note whether the frustration is about Claude Code specifically or about development tooling generally.

### Q7: Scenario -- New Project Setup
**Ask**: "Imagine you're starting a brand new project tomorrow. Walk me through how you'd set up your development environment and workflow from scratch. Where does Claude Code fit in?"

- **Follow-up probes**:
  - "What's the first thing you configure?"
  - "Are there things you copy from previous projects? What are they?"
  - "What takes the longest to set up?"
- **Target segment**: Solo developers, consultants
- **Assumption check**: We assume users want opinionated project scaffolding. This may not be true -- some users prefer minimal setups.

### Q8: Scenario -- Cross-Cutting Concerns
**Ask**: "Think about the last time you had to make a change that touched multiple parts of your system -- like updating a shared API, changing an authentication pattern, or refactoring a data model. How did you coordinate that?"

- **Follow-up probes**:
  - "How did you keep track of what needed to change?"
  - "Did anything get missed? How did you find out?"
  - "How long did the whole process take compared to the original change?"
- **Target segment**: Team leads, consultants
- **Assumption check**: We assume cross-cutting changes are painful and poorly supported. The delivery-team's Feature Knowledge System addresses this -- but we must not mention it.

### Q9: Workaround Discovery
**Ask**: "Have you ever written a script, a prompt template, or a set of instructions that you reuse with Claude Code? Tell me about it."

- **Follow-up probes**:
  - "What problem does it solve?"
  - "How did you figure out that approach?"
  - "Have you shared it with anyone? Why or why not?"
  - "What's brittle about it -- what breaks when you use it in a new context?"
- **Target segment**: All, especially AI/ML practitioners
- **Assumption check**: We assume power users have built ad-hoc extensions. The density and sophistication of these workarounds indicates market readiness for a plugin system.

### Q10: Collaboration Patterns
**Ask**: "When you're working with other people -- teammates, clients, stakeholders -- how does Claude Code fit into that collaboration? Or does it?"

- **Follow-up probes**:
  - "Do other people on your team use Claude Code? In the same way you do?"
  - "How do you share context, decisions, or outputs from Claude Code with others?"
  - "Have you ever had a situation where Claude Code's output conflicted with what a teammate expected?"
- **Target segment**: Team leads, consultants, game developers
- **Assumption check**: We assume collaboration is a gap. The delivery-team plugin addresses this heavily -- but some users may not need team coordination at all.

### Q11: Domain-Specific Needs
**Ask**: "Are there specialized aspects of your work -- specific to your industry, tech stack, or problem domain -- where general-purpose tools fall short? What does that look like?"

- **Follow-up probes**:
  - "Can you give me a concrete example from the last month?"
  - "What would a tool that understood your domain need to know?"
  - "How much would you trust an AI tool with domain-specific decisions versus general coding tasks?"
- **Target segment**: Game developers, AI/ML practitioners
- **Assumption check**: We assume domain specialization is valuable. This tests whether the Godot plugin model (deep vertical) or the developer plugin model (broad horizontal) is the right pattern to replicate.

---

## Section 4: Concept Validation Questions (10 min)

**Goal**: Test specific hypotheses without leading. Present trade-offs, not features.

### Q12: Plugin Discovery and Trust
**Ask**: "If you found out there was a marketplace of extensions for Claude Code -- things other people built to add capabilities -- what's the first thing you'd want to know before trying one?"

- **Follow-up probes**:
  - "What would make you trust an extension built by someone you don't know?"
  - "Have you installed extensions or plugins for other tools (VS Code, browser, etc.)? What was that experience like?"
  - "What would make you NOT install something?"
- **Target segment**: All
- **Assumption check**: We assume users want a marketplace. Some users may prefer to build their own extensions or may distrust third-party additions to an AI tool. **Flag**: This question contains an embedded assumption that a marketplace model is desirable -- note if users push back on the premise.

### Q13: Automation vs. Control
**Ask**: "Think about the tasks you do repeatedly in your workflow. For each one, would you rather have a tool that does it automatically in the background, or one that you trigger manually and review the output before it takes effect?"

- **Follow-up probes**:
  - "Are there tasks where you'd be comfortable with full automation? Which ones?"
  - "What about tasks where you'd always want to review first? Why?"
  - "Has an automated tool ever done something you didn't expect? What happened?"
- **Target segment**: All
- **Assumption check**: We assume users want a mix of hooks (automatic) and skills (manual). This question calibrates the balance. **Flag**: If users uniformly prefer manual control, our hook-heavy architecture may create friction.

### Q14: Prioritization
**Ask**: "I'm going to describe three capabilities. Tell me which one you'd want first and why."

Present these neutrally, without connecting them to existing plugins:

- **A**: "A system that helps you go from a rough idea to a structured plan with clear requirements, design decisions, and implementation steps -- all before you write code."
- **B**: "A system that reviews your code changes and catches issues that your normal review process misses -- things like architectural drift, security patterns, or inconsistencies across the codebase."
- **C**: "A system that generates documentation, reports, and presentations from the work you've already done, so you never have to summarize or reformat manually."

- **Follow-up probes**:
  - "What makes that one the most valuable to you?"
  - "For the one you ranked last -- is that because you already have a solution, or because the problem isn't important?"
  - "If you could combine two of them, which two?"
- **Target segment**: All
- **Assumption check**: A maps to delivery-flow + prd-quality-gate, B maps to developer + quality, C maps to presentation + operations. We are testing whether our current investment allocation matches user priority. **Flag**: If users consistently rank C last, the presentation skill may be lower priority than assumed.

### Q15: Trade-Off -- Depth vs. Breadth
**Ask**: "Would you rather have one tool that deeply understands your specific tech stack and workflow, or a collection of lighter tools that each cover a different part of your process?"

- **Follow-up probes**:
  - "What if the deep tool took longer to set up and configure?"
  - "What if the collection of lighter tools sometimes didn't work well together?"
  - "Have you experienced either pattern? What was that like?"
- **Target segment**: All
- **Assumption check**: We assume users want both (hence the marketplace model with deep plugins like delivery-team alongside focused ones like prompt-engineer). This question tests whether the hybrid approach resonates or confuses.

### Q16: Trade-Off -- Opinionated vs. Flexible
**Ask**: "When you use a development tool, do you prefer one that makes decisions for you and gives you a clear path to follow, or one that gives you building blocks and lets you assemble your own workflow?"

- **Follow-up probes**:
  - "Does your answer change depending on whether you're starting a new project vs. maintaining an existing one?"
  - "What's an example of a tool that got this balance right for you?"
  - "What about one that got it wrong?"
- **Target segment**: All
- **Assumption check**: The delivery-team plugin is highly opinionated (7 stages, defined DoD, mandatory validators). Some users may find this constraining. This question reveals the tolerance range.

### Q17: Willingness to Invest Time
**Ask**: "How much time would you be willing to spend setting up and learning a new tool if it promised to save you significant time in the long run? What's the threshold where you'd give up?"

- **Follow-up probes**:
  - "What's the longest you've spent configuring a development tool? Was it worth it?"
  - "Do you usually read documentation before using a tool, or do you just try it and see what happens?"
  - "What's the fastest a tool has ever impressed you? What did it do?"
- **Target segment**: All, especially solo developers
- **Assumption check**: The delivery-team setup wizard has 10 questions. The config file has a versioned schema. This may be too much for some segments. Note the tolerance threshold per segment.

---

## Section 5: Closing (5 min)

### Q18: Magic Wand
**Ask**: "If you could wave a magic wand and have Claude Code do one thing it can't do today -- anything at all, no constraints -- what would it be?"

- **Follow-up probes**:
  - "What would that change about your day-to-day?"
  - "How much time would that save you per week?"
  - "Have you looked for a solution to that? What did you find?"
- **Target segment**: All
- **Assumption check**: None -- this is deliberately unconstrained. Note whether answers cluster around themes already addressed by existing plugins or reveal entirely new territory.

### Q19: Biggest Miss
**Ask**: "Is there anything I should have asked you about but didn't? Anything about how you work that you think would be important for us to understand?"

- **Follow-up probes**:
  - Allow silence. Let the participant think.
  - "You mentioned [X] earlier -- is there more to that story?"
- **Target segment**: All
- **Assumption check**: This catches our blind spots. Treat every response here as high-signal.

### Q20: Referral and Follow-Up
**Ask**: "Do you know anyone else who uses Claude Code in a different way than you do -- someone who might have a different perspective? Would you be willing to connect us?"

- **Follow-up**: "Would it be okay if we reached out to you again in a few weeks to show you what we've built based on these conversations?"
- **Target segment**: All

---

## Section 6: Analysis Framework

### Per-Interview Notes Template

Complete this for each interview immediately after the session:

```
Participant ID: [P##]
Segment: [solo dev / team lead / consultant / game dev / AI-ML]
Date: [YYYY-MM-DD]
Duration: [minutes]

## Key Quotes (verbatim, with timestamps)
- [timestamp] "[quote]" -- context: [what prompted this]

## Jobs to Be Done (what they were trying to accomplish)
1. [Job] -- Frequency: [daily/weekly/monthly] -- Current solution: [what they do now]
2. ...

## Pain Points (ranked by emotional intensity)
1. [Pain point] -- Intensity: [mild / moderate / strong / extreme]
2. ...

## Workarounds Discovered
1. [Workaround] -- Sophistication: [ad-hoc / scripted / systematic]
2. ...

## Unmet Needs (not addressed by any current plugin)
1. [Need]
2. ...

## Reactions to Validation Questions
- Q12 (marketplace trust): [summary]
- Q13 (automation vs control): [preference and reasoning]
- Q14 (prioritization): [ranking: A > B > C or similar]
- Q15 (depth vs breadth): [preference]
- Q16 (opinionated vs flexible): [preference]
- Q17 (setup time tolerance): [threshold in minutes/hours]

## Surprises (things we didn't expect)
1. [Surprise]

## Segment-Specific Notes
- [Anything relevant to their specific segment]
```

### Cross-Interview Synthesis Process

**Step 1: Affinity Mapping (after 5+ interviews)**
- Extract all pain points, jobs, workarounds, and unmet needs onto individual cards
- Group cards by theme, not by participant or segment
- Name each cluster with a verb phrase (e.g., "Coordinating cross-cutting changes across multiple files")
- Count frequency: how many participants mentioned each cluster?

**Step 2: Segment Comparison Matrix**
- Build a matrix: rows = theme clusters, columns = user segments
- Mark each cell: strong need / mild need / not mentioned / explicitly rejected
- Identify themes that cut across all segments (universal needs) vs. segment-specific needs

**Step 3: Priority Scoring**

Score each theme on three dimensions:

| Dimension | Weight | Scale |
|-----------|--------|-------|
| **Frequency** -- How many participants mentioned it? | 40% | 1 (1-2 users) to 5 (75%+ of users) |
| **Intensity** -- How emotionally strong were the reactions? | 35% | 1 (mild annoyance) to 5 (described as "blocking" or "deal-breaker") |
| **Breadth** -- How many segments does it span? | 25% | 1 (single segment) to 5 (all segments) |

**Composite score** = (Frequency x 0.4) + (Intensity x 0.35) + (Breadth x 0.25)

Themes scoring 3.5+ are strong candidates for immediate investment.

**Step 4: Gap Analysis Against Current Plugins**

For each high-scoring theme, answer:
1. Does an existing plugin already address this? Fully, partially, or not at all?
2. If partially, what's missing? Is it a feature gap, discoverability gap, or trust gap?
3. If not at all, is this a new plugin opportunity, an enhancement to an existing plugin, or a platform-level capability?

**Step 5: Opportunity Sizing**

For themes not addressed by current plugins, estimate:
- **Reach**: What percentage of the total addressable user base would benefit?
- **Effort**: T-shirt size (S/M/L/XL) for building the solution
- **Confidence**: How confident are we in the need based on interview evidence? (high/medium/low)

Plot on a 2x2 matrix: Reach x Effort. Prioritize high-reach / low-effort quadrant first.

### Decision Criteria for Feature Pursuit

A feature moves from "interview insight" to "backlog item" when it meets ALL of the following:

1. **Evidence threshold**: Mentioned by 3+ participants across 2+ segments, OR mentioned with extreme intensity by 2+ participants in the same segment
2. **Alignment**: Fits within the Claude-Plugins marketplace mission (extending Claude Code capabilities through modular, composable plugins)
3. **Feasibility**: The team can articulate a plausible technical approach within the existing plugin architecture (skills, hooks, agents, MCP servers)
4. **Differentiation**: Not already well-served by an existing Claude Code built-in feature or widely-available alternative

A feature is deprioritized (but not discarded) when:
- Mentioned by only 1 participant with mild intensity
- Requires platform-level changes outside the plugin system's control
- Conflicts with an architectural constraint (e.g., deterministic business rules engine)
- Addresses a need that users have already solved with an acceptable workaround

### Red Flags to Watch For

- **Participant describes a feature we already ship but doesn't know about it** -- This is a discoverability problem, not a feature gap. Track separately.
- **Participant says "I would use that" without describing a current pain point** -- Hypothetical demand is unreliable. Weight actual workarounds more heavily than stated preferences.
- **All participants in a segment give the same answer to Q14** -- May indicate the segment is too narrowly defined. Consider splitting or broadening.
- **Interviewer catches themselves explaining the product** -- Stop. Reframe as a question. The participant should talk 80%+ of the time.
- **Participant asks "can it do X?" repeatedly** -- They are feature-shopping, not describing needs. Redirect: "Tell me about the last time you needed to do X."

---

## Appendix: Question-to-Objective Mapping

| Question | Primary Objective | Secondary Objective |
|----------|-------------------|---------------------|
| Q1-Q3 | Understand current workflows | Calibrate segment placement |
| Q4-Q6 | Identify unmet needs | Discover workarounds |
| Q7-Q8 | Identify unmet needs (scenario-based) | Validate marketplace assumptions |
| Q9 | Discover workarounds | Assess market readiness |
| Q10 | Validate marketplace assumptions | Identify unmet needs |
| Q11 | Identify unmet needs (domain-specific) | Prioritize next investments |
| Q12-Q13 | Validate marketplace assumptions | Discover adoption barriers |
| Q14-Q17 | Prioritize next investments | Validate marketplace assumptions |
| Q18-Q19 | Identify unmet needs (unconstrained) | Catch blind spots |
| Q20 | Expand interview pool | -- |
