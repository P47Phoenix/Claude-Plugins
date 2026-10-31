---
description: Run an idea past a team of simulated personas - a facilitated multi-round review, or an interactive talk-through
argument-hint: <idea or topic> [review|talk] [rounds: N] [personas: A, B, C]
allowed-tools: Skill, Read, Write, Agent, WebFetch, WebSearch
---

Invoke the `bible-research:idea-team` skill with this request: $ARGUMENTS

Follow the skill's workflow exactly:

- Default mode is `review` for an idea stated as a thing to judge, `talk` for a question addressed to a persona or the team
- Select 3-7 personas (default 5); the Skeptic and the Lay Listener are always in. Load `.bible-research/personas.yml` if it exists
- Each persona runs in its own agent and never shares a context with another; rounds bounce through the attributed digest. At least 2 rounds; more only while positions move, up to the cap (default 3, maximum 4)
- A pasted draft to attack is `sermon-verification` `redteam`, not this skill; this skill reviews ideas, plans and concepts
- Personas are simulated viewpoints, never real people or official positions. Opinion is labeled opinion; fact claims need a source
- Every `review` or `summary` report passes the verification gate and ends with "Verification notes"
