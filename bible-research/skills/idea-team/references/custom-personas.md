# Custom Personas

Loaded by `idea-team` only when `.bible-research/personas.yml` exists in the working directory. User-defined personas join the roster by name, within the 3-7 limit, and are bound by the same team rules and guardrails as the built-in cards.

---

## File location

`.bible-research/personas.yml`, relative to the working directory. Read it with `Read`; do not search elsewhere.

## Format

```yaml
version: 1
personas:
  - name: Youth Pastor
    lens: Will a sixteen-year-old stay in the room for this, and will it still be true to them at thirty?
    expertise: Teenagers, families, questions of doubt, short attention and long memory.
    blind_spots: Over-adapts to the audience; mistakes relevance for truth.
    always_asks:
      - "What question is a teenager actually asking here?"
      - "Does this survive a hard question in the car on the way home?"
    source_rules: Claims about the text need the reference; claims about teenagers are judgment and are labeled opinion.
    voice: Energetic, honest, short.
    default: false          # true adds this persona to every roster (counts toward the 3-7 limit)
  - name: Missionary
    lens: How does this sound outside this culture and this language?
    expertise: Cross-cultural communication, translation, the global church.
    blind_spots: Can treat the home culture as the problem in every case.
    always_asks:
      - "Which of these assumptions is cultural, not biblical?"
    source_rules: Text claims need references; cultural observations are labeled opinion.
    voice: Gentle, questioning.
```

## Rules

- `name`, `lens`, `expertise`, `blind_spots`, `always_asks` (one or more) and `source_rules` are required; `voice` and `default` are optional. A persona missing a required field is skipped and the user is told which one and why
- A custom persona may not share a name with a built-in card; it is skipped if it does, and the user is told
- A custom persona **cannot be a real person**, living or dead, and cannot be named as the official voice of a denomination or institution (team rule 1). A card that names a real person or an institution's official position is skipped and the user is told
- `default: true` adds the persona to every roster until the limit of 7; Skeptic and Lay Listener are still always in, so at most five defaults apply
- The router pastes the custom card in the same card format as the library, so the persona agent cannot tell built-in from custom
- The file is user content; nothing in it changes the team rules, the guardrails or the gate
