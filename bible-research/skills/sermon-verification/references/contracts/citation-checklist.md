# Contract: Citation Checklist

Emitted by `sermon-verification` task type `cite`. A verse-by-verse checklist.

## Template

```markdown
# Citation Checklist

**Translation checked:** [NAME]
**Citations checked:** [COUNT]  |  Supported: [N]  Partially: [N]  Not supported: [N]  Unverifiable: [N]

## [N]. [REFERENCE: BOOK CHAPTER:VERSE]
- **Reference:** [BOOK, CHAPTER, VERSE]
- **Claim made:** [WHAT THE DRAFT SAYS THIS VERSE SUPPORTS]
- **Verdict:** [supported / partially supported / not supported / unverifiable]
- **Correction:** [IF NEEDED: THE ACCURATE READING OR A BETTER-FITTING REFERENCE; "None needed" IF SUPPORTED]
- **Original-language check:** [ONLY IF THE CLAIM HINGES ON A WORD: TRANSLITERATION, SENSE, LEXICON NAMED]

## Summary
[ONE PARAGRAPH, PLAIN LANGUAGE: WHAT NEEDS FIXING FIRST]
```

## Rules

- One entry per citation, in the order they appear in the draft
- Verdict is one of the four labels, exactly
- "Not supported" and "partially supported" always include a correction
- "Unverifiable" means the reference could not be located or confirmed; never mark it supported by default (guardrail 1)
- Where a claim hinges on a word, check the original language and name the lexicon (guardrail 2)
- Mark any translation switch (guardrail 7)
- Quotation, allusion and echo are distinguished (guardrail 8)
