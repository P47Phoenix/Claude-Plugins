# Contract: Research Findings

Emitted by `research` for `word-study`, `person`, `theme-trace`, `passages` and `church-history`. The gate returns it in the same shape, ending in Verification notes.

## Template

```markdown
# Research Findings: [TERM, PERSON, THEME, TOPIC OR QUESTION]

**Question shape:** [descriptive | explanatory | comparative | exploratory]. **Translation:** [NAME, stated once].

## Summary
[THREE TO SIX SENTENCES IN PLAIN LANGUAGE. WHAT THE SOURCES SUPPORT, WHAT IS CONTESTED, WHAT COULD NOT BE CONFIRMED.]

## Findings
1. **[FINDING]** -- [ONE OR TWO SENTENCES]. ([REFERENCE], S[N]; [SOURCE], S[N]) [TAGS, IF ANY]
2. ...

## Original language (if any term was studied)
- **[transliterated term]** ([Hebrew | Aramaic | Greek]) -- sense: [LEXICON GLOSS, LEXICON NAMED, S[N]]. Range: [OTHER SENSES]. In this passage: [WHICH SENSE AND WHY].

## Context
[HISTORICAL, LITERARY OR CANONICAL SETTING THE FINDINGS NEED. JEWISH SOURCES BY TRACTATE AND FOLIO OR NAMED MIDRASH, TAGGED [TRADITIONAL].]

## Positions (if contested)
- **[POSITION A]** -- held by [NAME, WORK, S[N]]. Grounds: [ONE SENTENCE].
- **[POSITION B]** -- held by [NAME, WORK, S[N]]. Grounds: [ONE SENTENCE].

## Passages (ordered as the canon orders them)
| Reference | What it says (paraphrase) | Note |
|---|---|---|

## Method notes
[QUESTION SHAPE, SOURCE PLAN FOLLOWED, BIAS AUDIT RESULT, ANY PROVISIONAL DISCLOSURE.]

## Sources
S1 ([tier]) -- [AUTHOR OR SITE], [TITLE], [YEAR]. Opened: [WHAT].
S2 ...

**Verification notes:**
[SUPPLIED BY THE GATE. MINIMUM ONE LINE.]
```

## Rules

- Every finding cites a reference or a source ID; a finding with neither is removed (guardrail 1)
- `[UNVERIFIED]`, `[INFERENCE]`, `[CONTESTED]`, `[Single-source]` and `[TRADITIONAL]` tags stay inline (guardrails 4, 5, 14)
- Original-language entries name the lexicon (guardrail 2); Jewish sources give tractate and folio or the named Midrash (guardrail 3)
- Omit an empty section except Summary, Findings, Sources and Verification notes
- Plain language, short sentences, technical terms glossed once (guardrail 6)
- Never reproduce long text from a source (guardrail 9)
- The internal draft carries "INTERNAL DRAFT - NOT FOR THE USER" as its first line; the gate removes it
