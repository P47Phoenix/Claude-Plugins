# Contract: On This Day List

Emitted by `on-this-day`. A list the user can choose from, consistent with the shortlist-then-pick pattern used elsewhere in the project. Modeled on the project's two best On This Day outputs (a dated church event, lectionary readings, and a Hebrew date with its year).

## Template

```markdown
# On This Day: [DAY MONTH YEAR]

## Liturgical calendar
1. **[OBSERVANCE]** ([CALENDAR NAME, EDITION OR PROVINCE]; [rank]). [ONE SENTENCE IN PLAIN LANGUAGE]. Readings: [REFERENCES, IF LECTIONARY]. Source: [PAGE OPENED]

## Documented church history
2. **[EVENT]** ([DAY MONTH YEAR]; [Julian | Gregorian]; [documented | traditional | contested]). [ONE SENTENCE]. Source: [AUTHOR, TITLE, YEAR | PRIMARY DOCUMENT]

## Hebrew calendar (only if requested)
3. **[HEBREW DATE, WITH YEAR]** ([daytime | begins at sunset the evening before]). [OBSERVANCE, IF ANY, WITH LEVITICUS 23 OR OTHER BIBLICAL REFERENCE]. Source: [CONVERTER OR CALENDAR]

If nothing is found for a part: "No dated, sourced [liturgical entry | church-history event] found for this date."

Which of these would you like to build a sermon from? (Or none.)

**Verification notes:** [WHAT WAS CHECKED AND AGAINST WHAT; WHAT COULD NOT BE CONFIRMED; WHAT WAS LEFT OUT AND WHY. MINIMUM ONE LINE]
```

## Rules

- Every entry names its specific calendar, source or historical reference (guardrail 12)
- **State the specific year** with every Hebrew-calendar correspondence (guardrail 12)
- Items are numbered, so the user can pick one; never pre-select or recommend (shortlist-then-pick)
- If no dated, sourced event exists for a part, say so rather than manufacturing one (guardrail 1)
- Label events documented, traditional or contested (guardrail 4); do not present loosely dated traditions as fixed to this day
- Jewish sources are cited by tractate and folio or named Midrash (guardrail 3)
- Plain language, short sentences (guardrail 6)
- The Verification notes line is mandatory, minimum one line ("All entries checked against the sources named; none unconfirmed.")
- Do not reproduce long text from a source (guardrail 9)
