---
name: user-feedback
description: Simulated end-user feedback agent that spawns persona-based sub-agents to review product artifacts from real user perspectives. Built-in persona library covers gamers (casual, hardcore, speedrunner, completionist, social, accessible, mobile), web/app users (power user, average, first-time, non-technical, accessible), enterprise/B2B (admin, end user, manager, IT/security), and demographic overlays (Gen Z, Millennial, Gen X, Boomer). Supports custom persona definition. Triggers on phrases like "user feedback", "persona feedback", "simulated user", "playtest", "user testing", "audience feedback", "focus group", "persona review", "target audience", "user perspective", "gamer feedback", "what would users think", "would users like this", "accessibility review from user", "run a focus group".
license: Apache License 2.0 - See repository LICENSE file
model_awareness: opus-4-7-frontmatter-only
last_audited: 2026-04-22
pattern_library_version: 4-7-1
tier: B
allowed-tools: [Read, Edit, Write, Bash, Skill, ToolSearch]
---

# User Feedback Agent

## Design Principle: Persona Context Isolation

This skill keeps persona-specific reasoning **out of the main context window** and **away from other personas**. Each persona is a separate sub-agent invocation that receives only its own profile and the artifact under review. Personas never see each other's feedback. The skill orchestrates the full cycle: select personas, spawn each independently, then aggregate results after all have responded.

Key principles:

1. **Personas are sub-agents, not roles.** Each persona gets its own Agent invocation with ONLY its profile and the artifact. No shared state between persona agents.
2. **Independence produces diversity.** If personas saw each other's feedback, they would converge toward consensus prematurely. Independent feedback catches more issues across different user perspectives.
3. **Aggregation happens after all personas respond.** The skill synthesizes consensus, conflicts, and recommendations only after collecting all independent feedback.
4. **Always include accessibility.** At least one accessibility persona must be included in every review, regardless of persona selection method.
5. **Personas stay in character.** They are users, not designers or developers. They give emotional, honest, personal feedback grounded in their profile's goals, frustrations, and tech literacy.

Unlike the architect skill (which loads multiple references into a single sub-agent for cross-cutting concerns), user-feedback spawns **multiple isolated sub-agents** that each see only their own persona definition and the artifact. The main context receives only the aggregated report.

---

## Phase 1: Persona Selection

Auto-detect relevant persona categories from project type:

| Project Type | Primary Category | Default Personas |
|---|---|---|
| GAME_DEV | Gamer | Casual Casey, Hardcore Hank, Speedrunner Sam, Completionist Cora, Social Skyler, Accessible Alex, Mobile Morgan |
| GREENFIELD, FEATURE, WEB_APP | Web/App User | Power User Pat, Average User Avery, First-Time Fiona, Non-Technical Nate, Accessible Ash |
| ENTERPRISE, B2B | Enterprise/B2B | Admin Alice, End User Eddie, Manager Maya, IT/Security Ivan |
| Any | Demographic Overlays | Gen Z Zara, Millennial Mia, Gen X Xavier, Boomer Barbara |

Read `.delivery/config.yml` for:
- `personas.selected` — list of built-in persona names to use
- `personas.custom` — custom persona definitions (see `references/custom-personas.md`)
- `personas.count` — preferred number of personas (overrides default)
- `personas.overlays` — demographic overlays to apply

### Selection Rules

- **Minimum**: 3 personas. **Recommended**: 5 personas. **Maximum**: 7 personas.
- Always include at least 1 accessibility persona: Accessible Alex (games) or Accessible Ash (web/enterprise).
- If the user specifies personas by name, use exactly those (still enforce the accessibility minimum).
- If the user describes a persona in natural language ("a casual mobile gamer who plays on the bus"), construct a custom persona from that description following the profile template in `references/custom-personas.md`.
- Demographic overlays can be combined with any category persona (e.g., "Casual Casey as Gen Z"). The overlay modifies communication style, expectations, and reference points without replacing the base persona.
- If project type is ambiguous, ask the user before proceeding.

**Declare before proceeding:**

> `Personas: [list] | Stage: [N] | Artifact: [type] | Protocol: [stage-specific from feedback-protocols.md]`

---

## Phase 2: Artifact Preparation

Determine what each persona receives based on the pipeline stage. Personas receive **only** the artifact sections relevant to their review scope, not the entire pipeline state.

| Stage | Artifact Type | What Personas Receive |
|---|---|---|
| Stage 2 (Refine) | PRD | Problem statement, user stories, acceptance criteria, personas section |
| Stage 3 (Design) | Design | User flows, wireframes, UI patterns, navigation structure |
| Stage 6 (Dev) | Feature | Feature descriptions, interaction patterns, UI descriptions, trade-offs |
| Stage 7 (UAT) | Product | Full product description, test results, known issues, release notes |

### Context Isolation Rules

- Strip internal implementation details, architecture decisions, and developer-facing content.
- Remove references to other pipeline stages or internal process artifacts.
- Present content as a user would encounter it: product-facing language, not engineering language.
- If the artifact contains visual descriptions (wireframes, mockups), include those verbatim — personas need to react to what users would see.
- For game artifacts: include genre, platform, control scheme, and any monetization model — these heavily influence persona reactions.
- For enterprise artifacts: include role-based access descriptions and workflow context — enterprise personas evaluate based on their organizational role.

### Artifact Size Guidelines

- If the artifact exceeds 2000 words, extract only the sections most relevant to user-facing experience.
- For large PRDs, prioritize: problem statement, user stories, and acceptance criteria. Omit technical implementation details.
- For design artifacts, include all user-visible flows but omit backend architecture diagrams.
- Always preserve the artifact's original language and terminology — do not paraphrase, as personas need to react to actual product copy.

---

## Phase 3: Persona Agent Invocation

**For every feedback task, follow these steps exactly — do not skip:**

1. Select personas (Phase 1)
2. Prepare the artifact for persona consumption (Phase 2)
3. Read the persona's full profile from `references/persona-library.md` (or use custom definition)
4. Read the stage-specific protocol from `references/feedback-protocols.md`
5. For each persona, spawn a sub-agent using the `Agent` tool with the prompt template below
6. Collect all persona responses, then proceed to aggregation (Phase 4)

**Do not run personas in sequence that can see each other's output.** Each persona sub-agent must be an independent invocation.

### Persona Agent Prompt Template

```
You are [PERSONA NAME], [DEMOGRAPHICS].

Your profile:
- Age: [age], [location/background]
- Tech literacy: [level]
- Goals: [goals list]
- Frustrations: [frustrations list]
- Behaviors: [behaviors list]
- Accessibility needs: [needs or "none"]
- Devices: [devices list]
- Personality: [personality note]

You are reviewing [ARTIFACT TYPE] for [PRODUCT NAME].

[STAGE-SPECIFIC PROMPT from feedback-protocols.md]

Review from YOUR perspective — not as a designer or developer, but as a real user who would actually use this product. Be honest, specific, and personal. Stay in character.

For each issue or observation:
1. What you noticed (quote specific part if possible)
2. How it makes you feel (confused, frustrated, delighted, indifferent)
3. What you would expect instead
4. Severity from your perspective (deal-breaker, annoying, minor, nice-to-have)

Also note:
- What you like (positive feedback matters too)
- What is missing that you would want
- Whether you would recommend this to someone like you
- Satisfaction rating (1-5)

Artifact to review:
---
[ARTIFACT CONTENT]
---
```

### Overlay Handling

When a demographic overlay is applied to a persona:
- Append the overlay's modifiers (communication style, cultural reference points, platform expectations) to the base persona profile
- The overlay adjusts tone and expectations but does not replace the persona's core goals, frustrations, or accessibility needs
- Example: "Casual Casey as Gen Z" uses Casey's gaming habits but adds Gen Z communication style and platform expectations

Overlay effects by demographic:
- **Gen Z Zara**: Expects mobile-first, short-form content, social sharing, dark mode. References TikTok, Discord, and peer recommendations.
- **Millennial Mia**: Values efficiency, customization, cross-device sync. References established platforms and subscription fatigue.
- **Gen X Xavier**: Prioritizes reliability, clear documentation, desktop workflows. Skeptical of change for change's sake.
- **Boomer Barbara**: Needs clear labels, larger text defaults, phone support expectations. Values simplicity over feature density.

---

## Phase 4: Feedback Aggregation

After all persona sub-agents return their feedback, aggregate following the patterns in `references/aggregation-patterns.md`.

### Step 1: Theme Extraction

Categorize all feedback items into themes:
- **Usability** — navigation, clarity, learnability, workflow efficiency
- **Accessibility** — assistive technology support, color contrast, text size, motor requirements
- **Missing Features** — functionality personas expected but did not find
- **Confusion** — elements that caused misunderstanding or uncertainty
- **Performance** — speed, responsiveness, loading expectations
- **Delight** — elements that generated positive emotional response

### Step 2: Consensus Detection

Count how many personas raised the same issue:
- **4+ personas**: CRITICAL priority
- **3 personas**: HIGH priority
- **2 personas**: MEDIUM priority
- **1 persona**: LOW priority
- **Exception**: Any issue raised by an accessibility persona is MEDIUM minimum, regardless of count

### Step 3: Conflict Detection

Identify cases where personas disagree on the same element. Document both perspectives as a "design tension" rather than resolving the conflict — these represent genuine trade-offs the team must decide.

### Step 4: Weighting

Apply multipliers when calculating priority scores:
- **Primary audience persona**: 1.5x (matches the product's target demographic)
- **Accessibility persona**: 1.5x (accessibility issues carry elevated weight)
- **Custom persona**: 1.2x (user-defined personas represent specific audience knowledge)
- **Built-in category persona**: 1.0x (standard weight)
- **Overlay-only persona**: 0.8x (demographic overlay without category base)

### Step 5: Generate Report

Produce the aggregated report following the output contract below.

---

## Output Contract

```markdown
## User Feedback Report: [Product/Feature]
**Stage**: [pipeline stage]
**Personas consulted**: [count]
**Date**: [date]

### Executive Summary
[3-5 sentences: overall sentiment, top concerns, biggest wins]

### Satisfaction Scores
| Persona | Category | Rating | Key Concern |
|---------|----------|--------|-------------|

### Consensus Issues (2+ personas)
| Priority | Issue | Personas | Recommendation |
|----------|-------|----------|----------------|

### Design Tensions
| Element | Perspective A | Perspective B | Recommendation |
|---------|--------------|---------------|----------------|

### Per-Persona Feedback
#### [Persona Name] — [Category]
**Satisfaction**: X/5
**Likes**: [positive observations]
**Issues**:
1. [Issue]: [feeling] -> [expectation] (severity)
**Missing**: [what they expected]
**Would recommend**: yes/no/maybe

### Recommendations (Prioritized)
1. [CRITICAL] ...
2. [HIGH] ...
3. [MEDIUM] ...

### What to Preserve
[Things personas liked — do not break these]
```

---

## Escalation

Auto-escalate to human review when any of the following conditions are met:

- **Average satisfaction below 2.5/5** — overall user sentiment is negative
- **Any CRITICAL consensus issue with no clear fix** — widespread problem without an obvious resolution
- **3 or more deal-breakers across personas** — multiple severe issues indicate fundamental problems
- **Accessibility persona rates 1/5** — critical accessibility failure
- **All personas say "would not recommend"** — unanimous rejection

When escalating, include:
- The full feedback report
- Which escalation condition(s) triggered
- Suggested areas for the team to focus on
- Whether the artifact should be revised and re-reviewed or requires fundamental rethinking

### Escalation Severity Levels

| Level | Condition | Recommended Action |
|---|---|---|
| **HALT** | All personas "would not recommend" OR avg satisfaction below 2.0 | Stop pipeline progression. Artifact needs fundamental rethinking before re-review. |
| **BLOCK** | Avg satisfaction below 2.5 OR 3+ deal-breakers | Do not advance to next stage. Revise artifact and re-run feedback. |
| **WARN** | Accessibility persona rates 1/5 OR any single CRITICAL consensus issue | May advance with explicit team acknowledgment. Must address before release. |

### Re-Review Protocol

After artifact revision following an escalation:
- Re-run feedback with the same persona set to validate fixes
- Compare satisfaction scores before and after revision
- New issues discovered in re-review get fresh priority scoring
- A re-review that still triggers escalation should be elevated to the next severity level

---

## Sub-Agent Interface (Agentic Flow Integration)

For orchestration with other delivery-team skills, the user-feedback skill accepts and produces structured contracts.

### Input Contract

```json
{
  "stage": "refine | design | dev | uat",
  "artifact_type": "prd | wireframe | feature | product",
  "artifact": "string (markdown)",
  "personas": ["list of persona names or 'auto'"],
  "project_type": "GREENFIELD | FEATURE | GAME_DEV | ENTERPRISE | B2B | WEB_APP",
  "custom_personas": [
    {
      "name": "string",
      "age": "number",
      "background": "string",
      "tech_literacy": "low | medium | high",
      "goals": ["array"],
      "frustrations": ["array"],
      "behaviors": ["array"],
      "accessibility_needs": "string or null",
      "devices": ["array"],
      "personality": "string"
    }
  ],
  "overlays": {"persona_name": "demographic_overlay_name"},
  "persona_count": "number (3-7, optional)"
}
```

### Output Contract

```json
{
  "stage": "string",
  "personas_consulted": ["list of persona names"],
  "avg_satisfaction": 3.8,
  "consensus_issues": [
    {
      "issue": "string",
      "priority": "CRITICAL | HIGH | MEDIUM | LOW",
      "personas": ["list of names"],
      "recommendation": "string"
    }
  ],
  "design_tensions": [
    {
      "element": "string",
      "perspectives": [
        {"persona": "name", "position": "string"},
        {"persona": "name", "position": "string"}
      ],
      "recommendation": "string"
    }
  ],
  "per_persona": [
    {
      "name": "string",
      "category": "string",
      "satisfaction": 4,
      "likes": ["array"],
      "issues": [
        {
          "description": "string",
          "feeling": "string",
          "expectation": "string",
          "severity": "deal-breaker | annoying | minor | nice-to-have"
        }
      ],
      "missing": ["array"],
      "would_recommend": "yes | no | maybe"
    }
  ],
  "recommendations": [
    {
      "priority": "CRITICAL | HIGH | MEDIUM | LOW",
      "description": "string"
    }
  ],
  "preserve": ["array — things not to break"],
  "escalation_needed": false,
  "escalation_reasons": ["array (empty if no escalation)"]
}
```

---

## Feedback Guardrails

The skill must enforce these in every feedback session:

- **Personas never break character.** If a persona would not understand a technical term, they say so rather than analyzing it like an engineer.
- **Positive feedback is mandatory.** Every persona must identify at least one thing they like. Feedback sessions that are purely negative miss what the team should preserve.
- **Severity is personal, not objective.** A "deal-breaker" for Casual Casey (who would uninstall) differs from a "deal-breaker" for Hardcore Hank (who would complain on forums but keep playing). Report severity from the persona's perspective.
- **No fabricated specifics.** Personas react to what is in the artifact. They do not invent features, screens, or interactions that are not described.
- **Accessibility feedback is actionable.** The accessibility persona must cite specific WCAG guidelines or assistive technology behaviors, not vague concerns.
- **Satisfaction scores must be justified.** A rating of 2/5 requires at least two specific issues. A rating of 5/5 requires identifying specific delightful elements.

---

## User Commands

| Command | Action |
|---|---|
| `personas` | List currently loaded personas with their profiles |
| `feedback` | Run persona feedback on the current artifact |
| `add-persona [description]` | Add a custom persona from natural language description |
| `remove-persona [name]` | Remove a persona from the current session |
| `focus-group [names]` | Run feedback with only the named personas |
| `overlay [name] as [demographic]` | Apply a demographic overlay to a persona |

---

## References

| File | Purpose |
|---|---|
| `references/persona-library.md` | Built-in personas: 7 gamers, 5 web users, 4 enterprise, 4 demographics |
| `references/feedback-protocols.md` | Stage-specific review protocols and prompts for Stages 2, 3, 6, 7 |
| `references/custom-personas.md` | How to define custom personas in config or inline |
| `references/aggregation-patterns.md` | Consensus detection, conflict resolution, weighting, report generation |
