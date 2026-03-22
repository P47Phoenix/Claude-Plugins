# Empirical Validation Registry

Patterns that require runtime verification across technology stacks. Code inspection and static analysis cannot verify these — the application must be running.

This registry is referenced by:
- The `SubagentStop` hook (automatic detection when developer/godot agents complete)
- The QA DoD validator (to produce CODE_COMPLETE instead of DONE)
- The developer and godot skills (to self-report verification gaps)

---

## Technology Validation Matrix

| Technology | Empirical Signals (keywords in acceptance criteria) | What Needs Runtime Verification |
|-----------|-----------------------------------------------------|--------------------------------|
| **Godot** | "scene renders", "visible", "appears", "click", "input", "animation plays", "collision", "physics", "tilemap displays", "camera follows", "sound plays", "particle effect", "UI shows/hides" | Scene rendering, input handling, signal runtime behavior, TileMap/TileSet display, animation playback, physics interactions, camera behavior, audio playback |
| **Unity** | "prefab instantiates", "UI renders", "physics", "animation", "raycast hits", "collider triggers", "canvas displays", "shader renders" | Scene composition, prefab instantiation, physics, UI layout, shader rendering, particle systems |
| **Unreal** | "blueprint executes", "widget displays", "material renders", "AI navigates", "level streams", "physics simulates" | Blueprint runtime, UMG widget rendering, material/shader display, AI behavior, level streaming |
| **Web/React** | "component renders", "click triggers", "displays correctly", "responsive", "loads", "navigates to", "form submits", "modal opens", "animation runs", "scroll behavior" | Component rendering, browser layout, click/event handlers, responsive behavior, navigation, form submission |
| **API/Backend** | "returns 200", "responds with", "database query returns", "auth flow completes", "webhook fires", "email sends", "queue processes", "cron executes" | HTTP responses, database queries, authentication flows, webhook delivery, async job processing |
| **Mobile** | "gesture recognized", "scroll works", "touch triggers", "haptic fires", "notification appears", "push received", "deep link opens" | Touch/gesture interactions, platform-specific behaviors, push notifications, deep linking |
| **CLI** | "outputs to stdout", "prints", "exit code", "interactive prompt works", "pipe works", "flag accepted" | Terminal output, exit codes, interactive behavior, pipe/redirect compatibility |
| **Desktop** | "window opens", "menu displays", "drag-and-drop works", "tray icon appears", "shortcut triggers" | Window management, native UI rendering, system integration |

---

## Keyword Patterns for Auto-Detection

Regex patterns for matching empirical criteria in acceptance criteria text:

### Visual / Rendering
```
renders?|displays?|visible|appears?|shows?|hides?|screen|layout|responsive|styled|themed|animated|animation plays
```

### User Interaction
```
clicks?|taps?|swipes?|drags?|scrolls?|hovers?|selects?|triggers action|input handling|gesture|touch|keyboard shortcut works
```

### Runtime Behavior
```
returns \d{3}|responds with|fires|executes|processes|runs|plays|navigates to|redirects|loads correctly|streams
```

### State / Side Effects
```
saves to|writes to database|sends email|queues|publishes|notifies|syncs|updates in real.time|persists
```

### Physics / Simulation
```
collision|physics|gravity|velocity|raycast|pathfinding|navigation|AI behaves|spawns at|moves to
```

### Audio / Media
```
sound plays|audio|music|video plays|stream loads|media renders
```

---

## Severity Classification

| Severity | Description | Examples | Pipeline Impact |
|----------|-------------|---------|-----------------|
| **Blocking** | Core functionality that defines the feature | "Scene renders with tiles", "API returns user data", "Login form submits" | Must be validated before release; CODE_COMPLETE until verified |
| **Warning** | Important but not feature-defining | "Animation is smooth", "Responsive on mobile", "Loading state appears" | Should be validated; can release with known gaps if documented |
| **Suggestion** | Nice-to-have polish | "Hover effect on buttons", "Transition animation", "Subtle particle effect" | Document for future validation; does not block release |

### Classification Rules
- If the acceptance criterion uses "must" or "shall" with an empirical keyword → **Blocking**
- If it uses "should" with an empirical keyword → **Warning**
- If it uses "nice to have", "optional", or "polish" → **Suggestion**
- If uncertain → default to **Warning**

---

## Recommended Validation Approaches

| Technology | Validation Tool | What It Covers |
|-----------|----------------|----------------|
| Godot | `godot --headless --quit` | Scene loading, autoload init, _ready() errors, signal connections |
| Godot | GodotIQ MCP server | Static analysis, dependency graphs, signal flow, scene structure |
| Godot | Manual editor playtest | Visual rendering, input handling, game feel, camera behavior |
| Web/React | Playwright / Cypress | Component rendering, click handlers, navigation, form submission |
| Web/React | Lighthouse / axe | Accessibility, performance, SEO, best practices |
| API | curl / httpie / Postman | HTTP responses, status codes, response bodies |
| API | Integration test suite | Auth flows, database queries, webhook delivery |
| Unity | Play Mode tests | Scene composition, physics, UI layout |
| Mobile | Appium / Detox | Touch interactions, gestures, navigation |
| CLI | bats / shunit2 | Exit codes, stdout/stderr output, interactive behavior |

---

## How This Registry Is Used

### By the SubagentStop Hook
The hook reads the agent's transcript, extracts acceptance criteria text, and matches against the keyword patterns above. If matches are found, it injects a warning into Claude's context listing the empirical criteria.

### By the QA DoD Validator
When reviewing a developer's output, the QA validator checks the "Verification Status" section. If "Requires runtime validation" items exist, the validator returns CODE_COMPLETE instead of DONE, and lists the empirical criteria with their severity.

### By Developer/Godot Skills
When producing the "Verification Status" section of their output, these skills check acceptance criteria against the keyword patterns. Any matching criteria are listed under "Requires runtime validation" rather than "Verified by inspection."

### By the Delivery Pipeline
- Stage 6 (Development): CODE_COMPLETE stories carry forward to Stage 7
- Stage 7 (UAT): Pending empirical validations become mandatory test cases
- Human Checkpoint 4: User sees both automated results AND pending runtime validations
