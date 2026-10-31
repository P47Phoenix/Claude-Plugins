# Contract: Round Digest

Two parts. The **persona entry** is what each persona agent returns. The **round digest** is what the router assembles from the entries and pastes, attributed, into every persona's next fresh agent. The digest is internal; the user sees it only if they ask.

## Persona entry (returned by each persona agent)

```markdown
### [PERSONA NAME] -- round [N]
**Stance:** [for | against | conditional | undecided]
**Position:** [TWO TO FOUR SENTENCES, IN THE PERSONA'S VOICE AND LENS]
**Strongest point for the idea:** [ONE SENTENCE]
**Strongest concern:** [ONE SENTENCE, WITH WHAT IT RESTS ON: a reference, a source, a logical gap, or "instinct"]
**Fact claims made:** [EACH CLAIM WITH ITS REFERENCE OR SOURCE, OR [UNVERIFIED]; "none" if none]
**Opinion, labeled:** [THE JUDGMENT CALLS IN THIS ENTRY, IN A LINE]
**Questions for the team or the user:** [ZERO TO THREE]
**Round 2 and later -- responses:** [AT LEAST TWO, EACH: "To [NAME]: agree | rebut | refine | changed mind -- [REASON THAT NAMES THE ARGUMENT]"]
**Changed position this round?** [no | yes -- from [X] to [Y] because [REASON]]
```

## Round digest (assembled by the router)

```markdown
# Round [N] digest -- [IDEA IN ONE LINE]

[EVERY PERSONA ENTRY, IN ROSTER ORDER, UNEDITED]

## Positions this round
| Persona | Stance |
|---|---|

## Movement (round 2 and later)
- [NAME]: [no change | changed from X to Y -- reason | unsupported change (no reason given)]

## Fact claims awaiting a source
- [CLAIM] -- made by [NAME], [UNVERIFIED]
```

## Rules

- Entries are copied unedited and attributed; the router adds nothing but the two tables (team rule 4)
- A "changed mind" without a reason that names the argument is recorded as "unsupported change" and does not count as movement for the stop rule (team rule 3)
- Fact claims keep their references or `[UNVERIFIED]` tags; a persona may not cite another persona as a source
- The Skeptic's entry must carry a surviving objection or the words "no surviving objection"
- Plain language (guardrail 6); never reproduce song lyrics, article paragraphs or post text (guardrail 9)
