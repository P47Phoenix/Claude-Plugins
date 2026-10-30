# Scripture-Citation Verification

## Purpose

Verify every scripture citation in the sermon actually supports the claim made against it.

## Checks For

- Correct book/chapter/verse for every reference cited
- Whether the cited verse, in its actual wording and context, supports the specific claim attached to it (not just topically related)
- Cases where a verse is quoted out of its surrounding context in a way that changes its meaning
- Consistency of translation used throughout (or clear notation when switching translations)

## Output Format

A verse-by-verse checklist. The fields and verdict labels are defined in `contracts/citation-checklist.md`.

## Standards

- Check against the original language text where the claim hinges on a specific word or phrase, not just the English translation in use.
- No invention: if a verse reference can't be located or confirmed, flag it as unverifiable rather than assuming it's correct.

## How to Check

1. List every citation, including ranges and cross-references, in the order they appear
2. Fetch or read the verse (and its surrounding paragraph) from a real source; name the translation checked
3. Compare the verse's wording to the claim attached to it. "Topically related" is not support
4. Read the surrounding context; ask whether the verse changes meaning when restored to it
5. For a claim that hinges on a word, check the Greek or Hebrew word in a lexicon (BDAG, HALOT, Strong's) and name it
6. Check that quotations match the stated translation; mark any switch
7. Distinguish **quotation**, **allusion** and **echo** (guardrail 8); a claim that something is "quoted" when it is not is "partially supported"
8. Verse numbering differs between Hebrew and English Bibles in some places (for example Psalm titles). Note which numbering is used

## Verdict Labels

- **Supported:** the verse, in its wording and context, supports the claim
- **Partially supported:** related, but overstated, narrower or broader than the claim, or the claim fits only one reading
- **Not supported:** the verse does not say or imply the claim, or the reference is wrong
- **Unverifiable:** the reference could not be located or confirmed (never assumed correct)
