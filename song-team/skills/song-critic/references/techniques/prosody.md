---
loaded_by: hook-writer, lyric-editor
level: L3
last_reviewed: 2026-10-26
---

# Technique: Prosody (counting the way the gate counts)

`prosody_check.py` is a heuristic, not an ear. Write for the ear, then verify with the heuristic. This file teaches the heuristic so the first draft passes.

## Reading a meter entry

`8/uSuSuSuS` means: eight syllables; positions 2, 4, 6, 8 are stressed (`S`), the rest unstressed (`u`). Entries are separated by `;`, one per lyric line, in order. A section with an empty `meter_spec` is unconstrained.

Only `S` positions are checked. A stressed syllable sitting on a `u` slot costs nothing. An unstressed syllable on an `S` slot costs one. A syllable-count difference costs one per syllable. The section's ratio is total cost divided by the number of `S` in its spec; FAIL above `prosody_tolerance` (default 0.15, equal passes).

Budget in practice: a four-line section of `uSuSuSuS` has 16 `S`; two missed beats = 0.125 (pass), three = 0.1875 (fail). A two-line `AA` pre-chorus of `uSuSuSuS` has 8 `S`; one miss passes, two fail. Syllable drift is the expensive error: one extra syllable plus one missed beat in a four-line section is already 0.125.

## Counting syllables

1. Look the word up in `scripts/data/syllable-exceptions.txt` first. These are performance counts: `every` 3, `everything` 3, `fire` 1, `hour` 1, `our` 1, `tired` 1, `real` 1, `poem` 2, `flower` 2, `heaven` 2, `evening` 2, `family` 3, `camera` 3, `idea` 3, `piano` 3.
2. Otherwise count vowel groups (`a e i o u y` runs). `y` is a vowel only between a consonant and a non-vowel (`rhythm`, `lonely`), not at a word start (`yet`).
3. A trailing silent `e` after a consonant does not count: `name` 1, `inside` 2, `candle` 2 (the `-le` after a consonant counts one).
4. `-ed` after a consonant other than `t`/`d` is silent: `walked` 1, `jumped` 1, `wanted` 2, `loaded` 2.
5. `-es` counts only after `s x z c g ch sh`: `boxes` 2, `wishes` 2, `makes` 1.
6. Hiatus pairs `ia io iu eo ua uo` split: `radio` 3.
7. Minimum one syllable per word. Contractions count as written: `I'm` 1, `I've` 1, `they're` 1.

## Marking stress

- **Monosyllables:** `u` when the word is in `scripts/data/function-words.txt`, else `S`. Function words include articles, prepositions, pronouns, auxiliaries, conjunctions, and some words that feel heavy: `like`, `still`, `yours`, `not`, `am`, `is`, `are`, `did`, `no`, `so`, `just`, `oh`, `yeah`. Words such as `here`, `yet`, `down`, `now`, `one`, `well` are content words (`S`). When in doubt, treat a word as function if it is grammatical glue.
- **A stranded line-final preposition** (`on`, `in`, `at`, `by`, `for`, `with`, `through`, `off`) is `S`: "the light I leave on" ends on a beat.
- **Polysyllables**, in order of precedence:
  1. Exception-table pattern (`every` Suu, `idea` uSu, `piano` uSu).
  2. Stress-fixing suffix: `-tion -sion -cian -ic -ity -ical -logy -ette -eer -self` put stress on the syllable before (or on) the suffix: `nation` Su, `electric` uSu, `city` Su, `cigarette` uuS, `engineer` uuS, `myself` uS.
  3. Neutral inflection (`-s -ed -ing -er -ly -ness -ful -less -ment`) is stripped and the base is re-evaluated: `morning` Su, `lonely` Su, `forgets` uS.
  4. Unstressed Latin prefix (`un- re- de- be- ex- com- con- pre- pro- dis- trans- a-`) before an open syllable: `before` uS, `again` uS, `inside` uS, `unfold` uS, `belong` uS, `decide` uS, `remember` uSu, `about` uS, `between` uS.
  5. Else first-syllable stress: `window` Su, `river` Su, `summer` Su, `vendor` Su, `borrowed` Su, `nobody` Suu.

## Worked examples (original lines)

| Line | Heuristic | Against `8/uSuSuSuS` |
|------|-----------|----------------------|
| The kettle hums before the light | `8/uSuSuSuS` | 0 cost |
| A borrowed coat that fits me wrong | `8/uSuSuSuS` | 0 cost |
| The vendor asks my name again | `8/uSuSuSuS` | 0 cost |
| Remember how the river bent | `8/uSuuuSuS` | 1 (position 4 `how` is `u`) |
| I count the numbers on the street | `8/uSuSuuuS` | 1 (position 6 `on` is `u`); passes a spec of `uSuSuuuS` with 0 |
| The vendor asked me for my name again | `9/uSuSuuuSuS` | 1 syllable + 1 beat = 2 |

The last row shows the typical failure: one filler word (`me for`) adds a syllable and pushes a function word onto a beat. Cut the filler and the line passes.

## Fixing a line without rewriting it

1. **Count first.** Syllable drift costs the most and is the easiest to see.
2. **Swap a function word off the beat.** `I count the numbers on the street` is `uSuSuuuS`; against `uSuSuSuS` the `on` at position 6 misses. `I count the numbers down the street` is `uSuSuSuS` (`down` is a content word) and costs nothing.
3. **Trade a two-syllable word for one.** `Remember how the river bent` puts `how` (u) on beat 4. `I recall the river bent` moves the beat onto `-call`; recount, since the line is now 7 syllables and needs one more.
4. **Move the content word.** `on the floor I set my case` opens `u u S`; `I set my case upon the floor` is `uSuSuSuS` exactly.
5. **Use the exception table as a tool.** `every` (Suu) fills three slots when a dactyl is needed; `fire` and `hour` fill one.
6. **Never pad with `oh`, `yeah`, `so`, `just`.** They are function words to the script and land `u` on a beat.

## What the ear hears versus what the script counts

The script never hears contrastive stress, melisma, or a singer leaning on an article. When a line sings right but the heuristic disagrees, prefer the rewrite that satisfies both; a `u` slot carrying a stressed syllable is free, so a line with more content words than the spec asks for is safer than one with fewer.
