# Contract: Song Ideas List

Emitted by `research` task type `song-ideas`. A numbered pick list, modeled on `on-this-day-list.md`: the user chooses what to take elsewhere; the list never recommends, never drafts, and never hands off. The timeline the ideas rest on is included so every idea's event is visible. The gate returns it in the same shape, ending in Verification notes.

## Template

```markdown
# Song Ideas: [ERA NAME(S)] [(batch N of M, when more than three eras were asked for)]

**Eras covered:** [NUMBERS AND NAMES]. **Translation:** [NAME, stated once]. **What this is:** ideas only, labeled as creative inference; no lyrics, no titles, no artists. The events and references were checked; the ideas were not, because they are not fact claims.

## Timeline these ideas rest on
[THE TIMELINE TABLE(S) PER contracts/timeline.md, ERA NOTES INCLUDED. EVENTS NUMBERED CONTINUOUSLY.]

## Ideas

### [Era name]
1. **Event:** [EVENT NAME] (timeline [#]). **Passage:** [BOOK CH:VV].
   **Angle:** [lament | praise | narrative | prayer | testimony | confession | thanksgiving | call to worship | meditation | blessing]. **Register:** [congregational | solo or testimony | children | choir or anthem | meditative | procession or celebration].
   **Theme:** [TWO TO EIGHT NEUTRAL WORDS, NOT A LINE].
   **Source:** S[N], S[N]. [INFERENCE] [CONTESTED or TRADITIONAL, IF THE EVENT CARRIES IT]
2. ...

[REPEAT PER ERA. NUMBER IDEAS CONTINUOUSLY ACROSS ERAS, NEVER RESTARTING AT 1, SO "PICK BY NUMBER" IS UNAMBIGUOUS]

## Method notes
[SOURCE PLAN FOLLOWED, BIAS AUDIT RESULT, ANY PROVISIONAL DISCLOSURE, ANGLE AND REGISTER SPREAD IN ONE LINE.]

## Sources
S1 ([tier]) -- [AUTHOR OR SITE], [TITLE], [YEAR]. Opened: [WHAT].
S2 ...

Which of these would you like to keep? (Pick by number, or none. This list is for you to take to your own songwriting; it does not write the song.)

**Verification notes:**
[SUPPLIED BY THE GATE. MINIMUM ONE LINE.]
```

## Rules

- Items are numbered continuously across eras so the user can pick; **never pre-select, rank or recommend** (shortlist-then-pick)
- Every idea carries `[INFERENCE]` and points at a numbered timeline event with its passage (guardrail 13)
- **No lyrics, lines, hooks, rhymes, song or hymn titles, artist, songwriter or publisher names, and no musical direction** (guardrail 13; `song-ideas.md` section 3). The gate removes any that slip through
- An idea whose event the gate removed is removed with it
- Roughly 15-20 ideas per era; fewer when the era is thin; never padded
- Angle and Register vary within each era (`song-ideas.md` rules 3-4)
- The closing question is fixed and offers no handoff
- Plain language (guardrail 6); never reproduce long text from a source (guardrail 9)
- The internal draft carries "INTERNAL DRAFT - NOT FOR THE USER" as its first line; the gate removes it
- The hook pattern for this contract is the `# Song Ideas:` heading **plus** the `**Eras covered:**` header line; keep both verbatim
