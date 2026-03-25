# Feedback Protocols by Pipeline Stage

How persona feedback works at each stage of the delivery pipeline. Each protocol defines what personas receive, what they're asked, and what they produce.

---

## General Protocol (applies at all stages)

### Before Invoking Personas

1. Select personas based on project type and config (see SKILL.md Phase 1)
2. Minimum 3, recommended 3-5, maximum 7 personas per review
3. Always include at least 1 accessibility persona
4. If project has custom personas defined in `.delivery/config.yml`, include those
5. Read each persona's full profile from persona-library.md or custom definition

### Persona Independence

- Each persona is spawned as a SEPARATE sub-agent
- Personas do NOT see each other's feedback
- Each receives ONLY: their persona profile + the artifact to review + the stage-specific prompt
- This ensures genuinely independent perspectives

### Feedback Structure (all stages)

Every persona produces feedback in this format:

```markdown
### [Persona Name] -- [Category]

**Satisfaction**: X/5
**First Impression**: [1-2 sentence gut reaction]

**What Works**:
- [Positive observation with specific reference]

**Issues**:
1. **[Issue title]**: [What they noticed] -> [How it makes them feel] -> [What they'd expect instead]
   - Severity: deal-breaker / annoying / minor / nice-to-have

**What's Missing**:
- [Feature or consideration they expected but didn't find]

**Would Recommend**: yes / no / maybe -- [brief reason]
```

---

## Stage 2: Refine -- PRD Review

### What Personas Receive
- Problem statement
- User stories with acceptance criteria
- Success metrics
- Target personas section (they review how well THEY are represented)

### Prompt Focus
"You are [PERSONA]. Read this Product Requirements Document. Does it capture what YOU need? What's missing from YOUR perspective?"

### Key Questions Personas Answer
1. Does the problem statement describe a problem YOU actually have?
2. Do the user stories cover YOUR key tasks and goals?
3. Are the acceptance criteria testable from YOUR perspective as a user?
4. What edge cases would YOU encounter that aren't covered?
5. Are YOU represented in the target personas? Accurately?
6. What would make you NOT use this product?

### What This Catches
- Wrong assumptions about user needs
- Missing user stories for underserved segments
- Acceptance criteria that sound complete but miss real-world usage
- Personas that are stereotypes instead of realistic representations

---

## Stage 3: Design -- UX Review

### What Personas Receive
- User flows (diagrams or text descriptions)
- Wireframes (text-based or image descriptions)
- UI patterns and component specs
- Navigation structure

### Prompt Focus
"You are [PERSONA]. Walk through this design as yourself. Narrate your experience step by step. Where do you get confused, stuck, or frustrated?"

### Key Questions Personas Answer
1. Can you find the main action on each screen?
2. Is the navigation clear? Do you know where you are?
3. Where would you get stuck and need help?
4. Is the information hierarchy correct for YOUR priorities?
5. Can you complete your PRIMARY task without confusion?
6. Accessibility: Can you use this with your specific needs?
7. What would you try that the flow doesn't support?

### What This Catches
- Usability issues before code is written
- Accessibility gaps in the design phase
- Navigation confusion for different user types
- Missing flows for secondary tasks
- Design assumptions that don't match real user behavior

---

## Stage 6: Dev -- Implementation Review

### What Personas Receive
- Feature descriptions (what was built)
- Interaction patterns (how it works)
- UI descriptions or screenshots
- Known limitations
- Dev notes on trade-offs made

### Prompt Focus
"You are [PERSONA]. Based on what's been built, would this work for you? Does the implementation match what you'd expect?"

### Key Questions Personas Answer
1. Does this feature do what YOU need it to do?
2. Are there interaction patterns that surprise you?
3. Is anything harder to use than it should be?
4. Do the trade-offs made by developers affect YOUR experience?
5. What would you try that this implementation doesn't support?
6. Any performance or responsiveness concerns for YOUR setup?

### What This Catches
- Gap between design intent and implementation reality
- Performance issues affecting specific user types
- Missing interactions that weren't in the spec but users expect
- Trade-offs that disproportionately hurt specific personas

---

## Stage 7: UAT -- Acceptance Review

### What Personas Receive
- Full product description
- Feature list with status (complete, partial, known issues)
- Test results summary
- Known issues and workarounds
- Release notes

### Prompt Focus
"You are [PERSONA]. This product is about to be released. Would you use it? Would you recommend it? What's your honest assessment?"

### Key Questions Personas Answer
1. Overall satisfaction (1-5 with justification)
2. Would you use this product regularly?
3. Would you recommend it to someone like you?
4. What's the single biggest improvement you'd want?
5. Are there deal-breakers that would make you stop using it?
6. Known issues: do any of them significantly affect YOUR experience?
7. What would make you switch to a competitor?

### What This Catches
- Product-market fit issues before launch
- Deal-breakers for specific audience segments
- Gaps between "technically complete" and "user-ready"
- Risk assessment for known issues
- Baseline satisfaction scores for future comparison

---

## Persona Count Guidelines

| Project Type | Primary Personas | Secondary | Accessibility | Total |
|-------------|-----------------|-----------|---------------|-------|
| GAME_DEV | 3 gamer types | 1 demographic | 1 (Accessible Alex) | 5 |
| Web App | 3 web user types | 1 demographic | 1 (Accessible Ash) | 5 |
| Enterprise | 3 B2B types | 1 demographic | 1 (Accessible Ash) | 5 |
| Mobile App | 2 web + Mobile Morgan | 1 demographic | 1 accessibility | 5 |
| API/Backend | Admin + IT/Security + End User | -- | -- | 3 |

For light stages (BUG_FIX, DOCS_ONLY), use 3 personas minimum.

---

## Trigger Phrases for Persona Feedback

These phrases should trigger the user-feedback skill at any point:
- "get user feedback on this"
- "what would [persona name] think?"
- "run a focus group"
- "playtest this"
- "persona review"
- "audience feedback"
- "would users like this?"
- "test with real users" (simulated)
