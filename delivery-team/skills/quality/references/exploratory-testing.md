# Exploratory Testing

Session-based exploratory testing (SBET) patterns for discovering bugs that structured test cases miss. Exploratory testing is unscripted, curiosity-driven testing that finds interaction effects, visual glitches, cross-story regressions, and "it just feels wrong" issues.

## Session Charter Format

Every exploratory testing session starts with a charter:

```
Explore [area/feature] with [resource/tool/approach] to discover [information/bugs/behaviors]
```

Examples:
- "Explore the combat system with two tanks and an infantry unit to discover edge cases in attack priority"
- "Explore the login flow with invalid credentials to discover error handling gaps"
- "Explore the dashboard with slow network conditions to discover loading state issues"
- "Explore cross-story interactions between movement (S-32) and terrain costs (S-33) to discover value conflicts"

## Session Structure

Each session is time-boxed:
- **Short session**: 15-30 minutes (focused on one feature/area)
- **Standard session**: 30-60 minutes (broader exploration)
- **Deep dive**: 60-90 minutes (complex interaction testing)

### Session Note Template

```markdown
## Exploratory Testing Session

**Charter**: [charter text]
**Tester**: [persona or role]
**Duration**: [time-box]
**Date**: [date]

### Observations
1. [timestamp] [observation -- what was noticed]
2. [timestamp] [observation]

### Bugs Found
- **BUG**: [description] -- Severity: [CRITICAL/HIGH/MEDIUM/LOW]
  - Steps: [how to reproduce]
  - Expected: [what should happen]
  - Actual: [what happened]

### Questions
- [question that arose during testing -- needs follow-up]

### Ideas
- [improvement ideas discovered during testing]

### Areas Not Covered
- [what was planned but not reached due to time]
```

## Heuristics

### HICCUPPS

Use these consistency heuristics to evaluate what you observe:

| Heuristic | Question | Example |
|-----------|----------|---------|
| **H**istory | Is this consistent with past versions? | "This button used to be here..." |
| **I**mage | Does this match the user's mental model? | "I'd expect clicking this to..." |
| **C**omparable | Is this consistent with similar products? | "In [competitor], this works differently..." |
| **C**laims | Does this match what the spec/docs say? | "The PRD says this should..." |
| **U**ser expectations | Would the target user expect this? | "A casual gamer would expect..." |
| **P**roduct | Is this consistent with other parts of this product? | "On the other screen, this works differently..." |
| **P**urpose | Does this serve the product's purpose? | "This doesn't help the user achieve..." |
| **S**tandards | Does this meet applicable standards? | "WCAG says contrast should be..." |

### FEW HICCUPPS (Extended)

Add these to HICCUPPS for deeper analysis:

| Heuristic | Question |
|-----------|----------|
| **F**amiliarity | How does this feel to someone who's used it before? |
| **E**xplainability | Can you explain why this behaves this way? |
| **W**orld | Is this consistent with how the real world works? |

## Tour-Based Exploration

Structured approaches to exploring a system:

| Tour | Focus | What to Do |
|------|-------|-----------|
| **Feature Tour** | Core features | Use every feature at least once |
| **Garbage Collector Tour** | Edge cases | Find the least-used, most-neglected areas |
| **Landmark Tour** | Navigation | Visit every screen/page, check you can get back |
| **Money Tour** | Critical paths | Follow the path that generates value (purchase, signup, core loop) |
| **Intellectual Tour** | Complex logic | Find the hardest, most complex features and stress them |
| **Bad Neighborhood Tour** | Bug clusters | Where bugs were found before, look for more nearby |
| **Antisocial Tour** | Misuse | Try to break things: wrong inputs, rapid clicking, back button abuse |
| **Obsessive-Compulsive Tour** | Repetition | Do the same thing over and over -- does it degrade? |

## Cross-Story Regression Heuristic

When a story modifies a shared value, check if prior stories depend on the old value:

### Detection Pattern

1. Identify all values/constants modified by the current story
2. For each modified value, search completed stories for dependencies on that value
3. If a dependency exists, flag it for cross-story testing

### Example

- Story S-32 sets tank movement to 3
- Story S-33 sets tank mountain terrain cost to 4
- Cross-story check: tank movement (3) < mountain cost (4) -- tanks can NEVER enter mountains
- This was not caught by per-story testing because each story passed individually

### Heuristic Questions

- "What other stories touch the same data/constants this story modified?"
- "If I change this value, what else breaks?"
- "Are there stories that were completed before this one that assumed the old value?"
- "Would the Product Owner expect these two stories to work together?"

## Game-Specific Exploratory Patterns

For GAME_DEV projects, these patterns catch common issues:

### Visual/Rendering
- Play through with fog of war -- does it reveal AI positions during AI turn?
- Zoom to min/max -- do UI elements scale correctly?
- Move camera to map edges -- any visual artifacts?
- Stack multiple visual effects -- do they render correctly together?

### AI Behavior
- Watch the AI play 5 turns without intervening -- does it make sensible moves?
- Give the AI an overwhelming advantage -- does it still act normally?
- Give the AI a losing position -- does it give up or fight?
- Put AI units in unusual positions -- does pathfinding handle it?

### Cross-System Interaction
- Select a unit, then immediately trigger combat -- does selection state persist correctly?
- Move a unit onto a tile with multiple overlapping effects -- which takes priority?
- Trigger multiple signals in rapid succession -- do all handlers fire?
- Pause during an animation -- does state survive resume?

### Input/Controls
- Click rapidly on multiple units -- does selection get confused?
- Right-click during a left-click action -- what happens?
- Use keyboard shortcuts during mouse interaction -- any conflicts?
- Tab through UI elements -- is focus order logical?

## Integration with Delivery Pipeline

### Stage 7 (UAT) Exploratory Testing

After structured test cases execute:

**For GAME_DEV projects** -- run 2 sessions:
1. Feature Tour session: play through all implemented features
2. Cross-story regression session: test interactions between stories that modify shared values

**For all project types** -- run 1 session:
1. Cross-story interaction session: test that independently-completed stories work together

### Producing Output

Exploratory testing produces observation notes (not pass/fail results). Any bugs found are logged to `.delivery/defects/` immediately. Observations feed into the retrospective.
