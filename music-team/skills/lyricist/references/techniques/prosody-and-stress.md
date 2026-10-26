---
loaded_by: lyricist
level: L3
last_reviewed: 2026-10-26
---

# Prosody and Stress

Prosody is the fit between where the words stress and where the music stresses. `structure.md` states the target as `meter_spec`: `syllables/stress` per line, for example `9/uSuSuuSuS`. Write to that string.

## Reading a spec

Each character is one syllable. `S` is a strong beat, `u` a weak one. `9/uSuSuuSuS` is nine syllables with strong beats on syllables 2, 4, 7 and 9. Count positions, not words.

## How the gate counts

- **Syllables** follow careful dictionary speech: `every` is 3, silent final e is dropped, `-ed` counts only after t or d, consonant plus `-le` counts one.
- **Stress**: one-syllable function words (the, a, and, of, to, my, is, for) are weak; one-syllable content words (nouns, verbs, adjectives) are strong; longer words stress their dictionary syllable; a line-final preposition is strong.
- **Ratio**: unmet strong positions plus the syllable-count gap, divided by the number of `S` in the spec. It must stay at or under `quality.prosody_tolerance`.

## Writing method

1. Write the spec's `S` slots first: place the line's most important content words there.
2. Fill `u` slots with function words and the unstressed syllables of longer words.
3. Where the spec has two weak slots in a row, use a function word pair (of the, in a, and the) or an unstressed prefix.
4. Where it has two strong slots in a row, use two content words (cold light, long road) or a content word plus a particle.
5. Count syllables aloud, then compare to the spec position by position.

## Common fixes

| Problem | Fix |
|---------|-----|
| One syllable too many | Drop an article, swap a two-syllable word for a one-syllable one, use a contraction |
| One syllable too few | Add an adjective or a weak connective, or choose a longer synonym |
| Content word on a weak slot | Swap its position with a function word, or choose a synonym with the stress elsewhere |
| Function word on a strong slot | Replace with a content word or reorder the clause |
| Stress falls on the wrong syllable of a long word | Pick a different word; do not rely on "sung" stress shifts |

## Natural stress over forced stress

If a line only fits by bending a word's stress, reword. Singers can bend stress, but the gate cannot, and listeners hear the strain. Prefer lines that sound like speech with a beat under them.

## Repeated sections

A Chorus repeated with the same spec gets the same words. If the spec differs on a repeat (a longer last line), adjust only the lines whose spec changed.

## Non-English

For `language` other than `en`, keep the line counts and aim for the spec by ear; the prosody gate SKIPS.
