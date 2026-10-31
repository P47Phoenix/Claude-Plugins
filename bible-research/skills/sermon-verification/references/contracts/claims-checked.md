# Contract: Claims Checked

Emitted by `sermon-verification` task type `history`. A list of historical, linguistic and cultural claims checked.

## Template

```markdown
# Claims Checked: Historical and Translation Accuracy

**Claims checked:** [COUNT]  |  Accurate: [N]  Needs correction: [N]  Unverifiable: [N]

## [N]. [SHORT LABEL]
- **Claim:** [THE HISTORICAL OR LINGUISTIC STATEMENT MADE]
- **Source checked against:** [THE SPECIFIC LEXICON, SCHOLARLY WORK, OR HISTORICAL REFERENCE USED; HEADWORD OR PAGE/SECTION WHERE KNOWN]
- **Verdict:** [accurate / needs correction / unverifiable]
- **Correction:** [IF NEEDED, WITH ITS SOURCE; "None needed" IF ACCURATE]

## Summary
[ONE PARAGRAPH, PLAIN LANGUAGE]
```

## Rules

- Verdict is one of three labels: accurate, needs correction, unverifiable
- "Source checked against" names a specific work. "Reference sites" or "common knowledge" is not a source (guardrail 1)
- For word studies, name the lexicon (BDAG, HALOT, Strong's) and the headword (guardrail 2)
- A claim that cannot be verified is marked unverifiable. It is not waved through and no supporting source is invented (guardrail 5)
- Where scholars disagree on a date or reading, say the point is disputed and give the range (guardrail 4)
- Jewish sources are cited by tractate and folio or named Midrash, with their date relative to the New Testament (guardrail 3)
- Prefer primary lexicons and recognized scholarly works over general reference sites
