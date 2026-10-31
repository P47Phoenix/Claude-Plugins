# Contract: Talk Turn

Emitted by `idea-team` in `talk` mode, once per turn. Conversational and not gated turn by turn; team rules and guardrails still bind every reply.

## Template (one persona)

```markdown
**[PERSONA NAME]:** [THE REPLY, IN THE PERSONA'S VOICE, UNDER 200 WORDS. FACT CLAIMS CARRY A REFERENCE OR SOURCE, OR [UNVERIFIED]. JUDGMENT CALLS ARE MARKED "(my view)".]

*Ask a follow-up, say `switch <persona>`, `whole team`, `bounce`, `summary` or `end`.*
```

## Template (whole team, and `bounce`)

```markdown
**[PERSONA NAME]:** [REPLY, UNDER 120 WORDS]

**[PERSONA NAME]:** [REPLY, UNDER 120 WORDS]

...

*Ask a follow-up, address one persona by name, say `bounce` for a cross-reply round, `summary` for the facilitator's report, or `end`.*
```

On `bounce`, each reply names at least one other persona and says agree, rebut, refine or changed mind (with the reason).

## Rules

- Replies stay in lens; a persona does not answer for another
- A fact claim about the text, history or a word carries its reference or source, or `[UNVERIFIED]` (team rule 2); the user is told when something should be checked with `/research` or `/verify`
- The persona never claims to be a real person or an official voice (team rule 1)
- The Skeptic keeps its best surviving objection and says when it has none
- No lyrics, no artist names, no reproduction of article or post text (guardrail 9)
- Plain language (guardrail 6)
- The footer line is fixed so the user always knows the commands
