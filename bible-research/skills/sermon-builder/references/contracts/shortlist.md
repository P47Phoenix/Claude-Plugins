# Contract: Shortlist

Emitted by `sermon-builder` task type `shortlist`. Modeled on the project's best shortlist output (a sample kept in the repository's `source/` folder, which is not shipped with the plugin). The sub-agent fills every `[BRACKETED]` placeholder. The gate adds the closing "Verification notes".

## Template

```markdown
Here are [3-5] candidates for [USER'S REQUEST IN A PHRASE]. Pick one and I'll break it down in full.

## 1. [CANDIDATE TITLE]: [PASSAGE REFERENCE]

**Why it fits:** [ONE TO TWO SENTENCES, PLAIN LANGUAGE, WITH SCRIPTURE REFERENCES FOR ANY CLAIM]
**Textual note:** [ONE RELEVANT TEXTUAL, ORIGINAL-LANGUAGE OR HISTORICAL NOTE; TRANSLITERATE ANY GREEK OR HEBREW TERM AND GIVE ITS SENSE; NO DEEP DIVE]

## 2. [CANDIDATE TITLE]: [PASSAGE REFERENCE]
[same two fields]

...

Which one would you like to develop?

**Verification notes:** [ADDED BY THE GATE, SEE verification-notes.md]
```

## Rules

- 3 to 5 candidates. Fewer than 3 or more than 5 is a contract violation
- Candidates must differ in genre, book or angle
- Each candidate has a passage reference, a "Why it fits" of one or two sentences, and one note labeled **Textual note** (or **Historical note** if the note is historical)
- Jewish sources in a note are cited by tractate and folio or by named Midrash (guardrail 3)
- Echoes and parallels are labeled as such (guardrail 8)
- No ranking, no recommendation, no marked favorite, no "my pick" (guardrail 12)
- **Stop after the closing question.** Do not begin a breakdown
- A shortlist is in scope for the gate: it must end with "Verification notes" (minimum one line)
- The translation used is stated once if any quotation appears
