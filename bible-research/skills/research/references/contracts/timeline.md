# Contract: Timeline

Emitted by `research` task type `timeline`, and as the first part of `song-ideas`. One table per era, in canonical order. The gate returns it in the same shape, ending in Verification notes.

## Template

```markdown
# Timeline: [ERA NAME(S) OR "The whole Bible"]

**Eras covered:** [NUMBERS AND NAMES FROM THE PICK LIST]. **Translation:** [NAME, stated once]. **Chronologies used:** [WORKS, WITH S[N] IDs].

## [N]. [Era name] ([BOOKS])

| # | Event | Passage | Sequence | Date | Witness | Why it matters |
|---|---|---|---|---|---|---|
| 1 | [EVENT] | [BOOK CH:VV] | [after X, before Y; or "sequence only"] | [RANGE, e.g. 597 BC (S3)] or **contested:** [A (S3) / B (S4)] or -- | [EXTERNAL WITNESS, IF ANY, WITH S[N]] | [ONE PLAIN SENTENCE] |

**Era notes:** [THE DATING SPLITS THAT SHAPE THIS ERA, IN TWO OR THREE SENTENCES. WHAT WAS LEFT OUT FOR LACK OF A SOURCE.]

[REPEAT PER ERA]

## Method notes
[SOURCE PLAN FOLLOWED, BIAS AUDIT RESULT, ANY PROVISIONAL DISCLOSURE.]

## Sources
S1 ([tier]) -- [AUTHOR OR SITE], [TITLE], [YEAR]. Opened: [WHAT].
S2 ...

**Verification notes:**
[SUPPLIED BY THE GATE. MINIMUM ONE LINE.]
```

## Rules

- **Every date is a range or marked contested, with a source ID** (guardrail 12). A cell never holds a single bare year. Eras 1-2 carry no absolute dates; their Date cell reads "--" or names the contested positions
- Events are numbered continuously across eras so song ideas can point at them
- The Sequence column comes from the text; "sequence only" is a valid entry where no date survives
- An event that could not be opened in the text, or whose date has no source, is **left out** and named in Era notes (guardrail 5)
- External witnesses (an inscription, a chronicle, Josephus) are named with their source ID; they are evidence for the date, not for the theology
- Jewish or patristic traditions about an event are tagged `[TRADITIONAL]` with tractate and folio or the work named (guardrail 3)
- Plain language in "Why it matters" (guardrail 6); never reproduce long text from a source (guardrail 9)
- The internal draft carries "INTERNAL DRAFT - NOT FOR THE USER" as its first line; the gate removes it
- The hook pattern for this contract is the `# Timeline` heading; keep the heading
