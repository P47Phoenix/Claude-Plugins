# Contract: Idea Review Report

Emitted by the `idea-facilitator` at the end of `review` mode, and on `summary` in `talk` mode. Passes through the gate when it carries scripture references or historical claims, and then ends in Verification notes.

## Template

```markdown
# Idea Review: [IDEA IN ONE LINE]

**Personas:** [NAMES]. **Rounds:** [N] ([stopped: no movement | stopped: cap reached]). **Aim and audience:** [FROM THE FRAME]. **Translation:** [NAME, if scripture was cited].

*The reviewers are simulated viewpoints, not real people or official positions of any church or institution. Disagreement is reported as found.*

## Consensus
- **[POINT]** -- consensus. [ONE SENTENCE ON WHY THE TEAM AGREES]
- **[POINT]** -- majority ([N] of [M]; dissent: [NAME], because [REASON]).

## Remaining tensions
- **[POINT]** -- split: [NAMES] hold [A]; [NAMES] hold [B]. What would settle it: [A SOURCE | THE USER'S DECISION | A TRIAL].

## Who changed their mind, and why
- Round [N]: [NAME], from [X] to [Y], because [REASON NAMING THE ARGUMENT].
- (or) No persona changed position.

## Ranked concerns
| # | Concern | Held by (final round) | Severity | Rests on |
|---|---|---|---|---|
| 1 | [CONCERN] | [NAMES] | critical / high / medium / low | [REFERENCE, SOURCE, OR "opinion" / "unverified claim"] |

The Skeptic's surviving objection: [THE OBJECTION, OR "none survived"].

## The strongest revised version
[THE IDEA, REWRITTEN TO TAKE IN THE CONSENSUS AND ADDRESS THE CRITICAL AND HIGH CONCERNS. MARKED AS A PROPOSAL. WHERE A SPLIT CHANGES IT, TWO FORMS IN A SENTENCE EACH.]

## Open questions for you
1. [WHAT ONLY THE USER CAN DECIDE]
2. [WHAT A SOURCE COULD SETTLE, AND WHICH]

## Scripture and sources cited
[REFERENCES AND SOURCES THE PERSONAS USED, WITH ANY [CONTESTED] OR [TRADITIONAL] TAGS]

**Verification notes:**
[SUPPLIED BY THE GATE. MINIMUM ONE LINE.]
```

## Rules

- Consensus levels are counted from what personas said in the digests; silence is not agreement, and the facilitator never breaks a tie (team rule 4)
- Severity follows the thresholds in `facilitation.md` section 4; a concern resting on an `[UNVERIFIED]` claim does not rise above medium until sourced; low concerns are named, never dropped
- Every "changed mind" line carries the reason; an unsupported change is reported as such (team rule 3)
- Opinion stays labeled opinion; fact claims carry references or sources; the gate removes fact claims no source supports and the notes say which persona made them (guardrails 1, 5; team rule 2)
- The honesty line is mandatory (team rule 1)
- The revised version is a proposal in the user's terms; it never grows past the original plus a third
- Plain language (guardrail 6); never reproduce song lyrics, article paragraphs or post text (guardrail 9)
- The internal draft carries "INTERNAL DRAFT - NOT FOR THE USER" as its first line when it goes to the gate; the gate removes it
- The hook pattern for this contract is the `# Idea Review` heading; keep the heading
