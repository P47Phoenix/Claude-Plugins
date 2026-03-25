# Custom Persona Definition

How to create project-specific personas that supplement or replace the built-in library.

---

## Defining Custom Personas

### In `.delivery/config.yml` (persisted across pipeline runs)

Add a `personas` section to the config YAML frontmatter:

```yaml
personas:
  # Override which built-in categories to use
  categories: [gamers, web-users]  # omit categories you don't need

  # Select specific built-ins by name
  selected:
    - Casual Casey
    - Hardcore Hank
    - Accessible Alex
    - Power User Pat

  # Define fully custom personas
  custom:
    - name: "Tournament Tina"
      category: gamer
      demographics: "25, esports competitor, streams on Twitch, based in Seoul"
      tech_literacy: expert
      goals:
        - Win regional tournaments
        - Build Twitch community
        - Optimize loadouts and find meta builds
        - Stream-friendly UI (visible to viewers)
      frustrations:
        - Input lag above 16ms
        - Unbalanced meta with no counterplay
        - Poor spectator mode
        - No replay system
        - UI elements that block gameplay during streams
      behaviors:
        - Plays 6+ hrs/day
        - Watches patch notes within hours of release
        - Active in competitive Discord servers
        - Tests frame data in training mode
        - Provides detailed bug reports with video clips
      accessibility: none
      devices: [PC (240Hz monitor), Stream Deck, Dual monitor]
      personality: "Competitive and precise. Notices 1-frame differences. Feedback includes frame data and exact reproduction steps."

    - name: "Budget Ben"
      category: web-user
      demographics: "35, freelance designer, cost-conscious, based in rural US"
      tech_literacy: moderate
      goals:
        - Get work done without paid subscriptions
        - Export data in open formats
        - Offline capability for spotty internet
      frustrations:
        - Paywalls on basic features
        - Feature gates that feel artificial
        - No offline mode
        - Forced cloud storage
      behaviors:
        - Uses free tiers of everything
        - Exports data immediately (doesn't trust cloud)
        - Compares alternatives weekly
        - Cancels trials before they convert
      accessibility: none
      devices: [Older Windows laptop, Android phone]
      personality: "Evaluates everything by cost-to-value. Will find the free alternative and compare it unfavorably."
```

### Inline (conversational, per-request)

Users can describe a persona conversationally:

> "Get feedback from a 60-year-old retired teacher who's never played a video game but wants to try, and a 12-year-old who plays Fortnite 4 hours a day"

The skill constructs persona profiles from the description:
1. Extract demographics, tech literacy, goals, frustrations from the description
2. Infer missing fields from context (age implies likely devices, stated hobby implies likely behaviors)
3. Present the constructed profile for user confirmation before using it
4. Store in working memory for the duration of the pipeline run (not persisted unless user says so)

### Demographic Overlays (composable)

Overlay a demographic lens on any persona:

> "Use Hardcore Hank but as a Gen Z player" -> combines Hank's gaming traits with Zara's generational traits

Overlays modify:
- Communication style (Gen Z: emoji, short reactions | Boomer: formal, detailed)
- Device expectations (Gen Z: mobile-first | Gen X: desktop-first)
- Feature expectations (Gen Z: AI features, social sharing | Boomer: phone support, print)
- Trust factors (Gen Z: peer reviews | Boomer: brand reputation)

---

## Persona Profile Requirements

Every persona (built-in or custom) MUST have:

| Field | Required | Notes |
|-------|----------|-------|
| name | Yes | Memorable, used in feedback reports |
| category | Yes | gamer / web-user / enterprise / demographic |
| demographics | Yes | Age, role, relevant context |
| tech_literacy | Yes | novice / moderate / proficient / expert |
| goals | Yes | 3-5 items |
| frustrations | Yes | 3-5 items |
| behaviors | Yes | 3-5 items |
| accessibility | Yes | "none" or specific needs |
| devices | Yes | Primary devices used |
| personality | Recommended | Shapes feedback style |

Incomplete personas will be flagged: "Persona [name] is missing [fields]. Feedback quality may be reduced."

---

## Managing Personas

| Command | Action |
|---------|--------|
| `personas` | List currently loaded personas |
| `add-persona` | Define a new custom persona (interactive) |
| `remove-persona [name]` | Remove a persona from the current session |
| `focus-group [names]` | Run feedback with specific personas only |
