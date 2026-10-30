# Historical & Translation Accuracy

## Purpose

Verify historical claims and translation choices made in the sermon.

## Checks For

- Historical claims (dates, figures, events, customs) against citable historical sources
- Translation choices that shift meaning from the original Greek/Hebrew
- Etymological or word-study claims checked against real lexicons (e.g. Strong's, BDAG, HALOT) rather than popular but incorrect folk etymologies
- Cultural/historical context claims (e.g. about Second Temple Judaism, Roman customs) checked against scholarly sources

## Output Format

A list of claims checked. The fields and verdict labels are defined in `contracts/claims-checked.md`.

## Standards

- If a claim can't be verified against a real source, mark it unverifiable — don't wave it through or invent a supporting source.
- Prefer primary lexicons and recognized scholarly works over general reference sites when checking word studies.

## How to Check

1. Extract each historical, linguistic and cultural claim as its own line
2. For a date, figure or event: find a citable source (a primary text such as Josephus, or a recognized scholarly work). Where scholars disagree on a date, give the range and call the point disputed (for example the fall of Jerusalem is dated 587 or 586 BC)
3. For a word study: look the term up in a primary lexicon and name it. A general website alone is not enough for a nuance
4. For a translation choice: compare the English to the Greek or Hebrew and say whether the sense shifts
5. For a custom (a wedding practice, a Temple ritual, a Roman custom): require a source that dates to the right period. A later rabbinic text does not prove a first-century custom (see `jewish-sources.md` for dating)
6. Compare against known folk claims (the "Abba means Daddy" and "eye of the needle gate" type). Where a claim matches a folk claim and you cannot find a real source for it, mark it unverifiable
7. Name the specific lexicon or scholarly work in "Source checked against"; "reference sites" is not a source

## Verdict Labels

- **Accurate:** supported by a named source
- **Needs correction:** contradicted by a named source; give the correction and its source
- **Unverifiable:** no real source located; do not invent one

## Folk Claim Pitfalls

- Etymological fallacy: a word's origin does not fix its meaning in a verse
- Overloaded synonym pairs (for example reading two different loves into two different Greek verbs)
- Custom stated as fact with no primary source
- A count or statistic ("appears 365 times") with no cited source
