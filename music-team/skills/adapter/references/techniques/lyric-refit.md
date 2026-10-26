---
loaded_by: adapter
level: L3
last_reviewed: 2026-10-26
---

# Technique: Lyric Re-fit

Fit an existing lyric to a new meter and register without changing what it says. The target meter is the
`meter_spec` already written in `structure.md`; the target diction and line habits are in the target
profile's `## Lyric` and `## Adaptation notes`.

## 1. Map the source

For each section write: line count, syllables per line, stress shape (`S` stressed, `u` unstressed), rhyme
letters, point of view, tense, the key images, and the hook line. This is the meaning inventory; nothing on it
may be lost or added.

## 2. Compare to the target meter

For each line compute `delta = target syllables - source syllables`:

| Delta | Meaning | First move |
|---|---|---|
| 0 | same count | check only the stress shape |
| -1 to -3 | shorten | cut function words and adjectives |
| -4 or less | shorten a lot | merge two images into one line only if the images stay recognisable; otherwise return `BLOCKED` |
| +1 to +3 | lengthen | restore a dropped article, use a two-syllable synonym, or hold a word across a beat |
| +4 or more | lengthen a lot | split the idea across two lines only if `structure.md` allows more lines; otherwise return `BLOCKED` |

## 3. Re-fit order (least to most invasive)

1. **Elide or restore function words** (a, the, and, my, that); contractions count one syllable.
2. **Drop or add a modifier** that carries no image.
3. **Swap word order** to move a stressed word onto a target stress position.
4. **Substitute a near-synonym** with the right syllable count and stress (for example three syllables
   with stress on the first in place of two with stress on the last).
5. **Restructure the line** keeping the same words where possible.
6. **Last resort:** change the refrain wording by the fewest possible words and log it.

Never use a move that adds a fact, a person, a place, a feeling or a tense change.

## 4. Stress and breath

- A stressed syllable falls on a strong position of the target shape; unstressed syllables fill the weak ones.
- Two stressed syllables in a row are acceptable for emphasis once per section; mark it under Risks.
- Put the most important word of the line (usually a noun or the verb) on the last stressed position.
- Leave a breath at the section's line ends and mid-line commas; a line longer than the singer's phrase length
  from the target profile needs a cut.
- Hard consonant clusters slow soft, legato genres; prefer open vowels there, and the reverse for percussive genres.

## 5. Rhyme

- Keep the source scheme if the target profile allows it. Otherwise move to the profile's scheme and log it.
- Keep rhyme words that are image words; change the non-image end first.
- A slant rhyme is acceptable where the config allows it; do not force a perfect rhyme by adding meaning.
- The refrain's rhyme word stays the same at every repeat.

## 6. Diction register

Match the target `## Lyric` diction rule: concrete and plain, colloquial, or poetic. Swap words, not
subjects. Avoid every phrase on `cliche-list.txt` that the swap might introduce.

## 7. Verify

- Every line meets its syllable count and stress shape within tolerance.
- The meaning inventory from step 1 is intact: same images, same POV, same hook idea.
- No line is borrowed from an existing song; if any line feels familiar, discard it.
- One `Changed` entry per section or per move family in the notes block, not one per line.
