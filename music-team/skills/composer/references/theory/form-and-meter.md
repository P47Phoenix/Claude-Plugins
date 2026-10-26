---
loaded_by: composer
level: L3
last_reviewed: 2026-10-26
---

# Form and Meter

## Section roles

| Section | Job | Typical bars | Energy |
|---------|-----|--------------|--------|
| Intro | set key, tempo, texture | 2-8 | low to mid |
| Verse | tell the story; the melody stays low and conversational | 8 (or 16) | low |
| Pre-Chorus | build tension toward the chorus; ends on V or IV | 4 | rising |
| Chorus | state the hook; highest, most repeated, most singable | 8 | high |
| Post-Chorus | extra hook or chant after the chorus | 2-4 | high |
| Bridge | contrast: new chords, new melody, new angle | 4-8 | varied |
| Instrumental / Breakdown | space for a solo or a dropout | 4-8 | varied |
| Outro / Tag | wind down or repeat the hook | 2-8 | falling |

## Form templates

Names come from `scripts/data/form-templates.json`; the letter string reads left to right.

| Template | Reads as | Fit |
|----------|----------|-----|
| `VCVCBC` | Verse, Chorus, Verse, Chorus, Bridge, Chorus | default pop, rock, country |
| `AABA` | A1 A2 B A3 (32 bars) | jazz standards, ballads |
| `verse-refrain` | verses ending in a repeated refrain line | folk, blues, hymn |
| `jingle` | short hook plus tag with a hard length cap | ads, themes |
| `edm-build-drop` | build, drop, breakdown cycles | electronic |
| `through-composed` | no repeated sections | story songs, theatre |

Use `structure_check.py` as the arbiter of which label sequences and bar ranges a template accepts.

## Choosing length

Duration in seconds is bars x beats per bar x 60 / bpm. At 4/4 and 118 bpm, 1 bar is about 2.03 seconds, so a 56-bar song runs near 114 seconds and a 90-bar song near 183 seconds. Work backwards from `target_length_sec`: choose the template, set verse and chorus bars to 8, then add or remove a bridge, intro, or outro.

## Meter and time signature

| Signature | Feel | Count | Genres |
|-----------|------|-------|--------|
| 4/4 | steady, square | 1 2 3 4 | nearly everything |
| 3/4 | waltz, lilt | 1 2 3 | folk, ballad, some country |
| 6/8 | rolling two-groups-of-three | 1 2 3 4 5 6 (accents on 1 and 4) | ballad, gospel, blues shuffle |
| 12/8 | slow rolling four-groups-of-three | accents on 1 4 7 10 | slow blues, soul |
| 2/4 or cut time | march, polka | 1 2 | folk dance, bluegrass |

## Tempo

| Range (bpm) | Feel | Use |
|-------------|------|-----|
| 56-76 | slow | ballad, hymn |
| 76-100 | easy | folk, soul ballad, laid back groove |
| 100-125 | moderate | pop, rock, country |
| 125-145 | brisk | dance pop, up-tempo rock |
| 145 and up | fast | punk, bluegrass, uptempo electronic |

Use the genre profile `## Rhythm` section for the exact band; ballads sit near the low end.

## Singable lines

One syllable per note is the default; a melisma spreads one syllable over several notes. A comfortable line holds 6-10 syllables per two 4/4 bars at 100-120 bpm; faster tempos hold more syllables per bar only if the words are short.

## Meter spec (`structure.md` column)

`syllables/stress` per line with `S` and `u`: `8/uSuSuSuS` is an eight-syllable iambic line. Dictionary stress rules: content words take stress on their primary syllable; function words are unstressed. Write the spec from the real lyric, not from an ideal pattern.

## Rhyme scheme letters

`ABAB` alternating, `AABB` couplets, `ABCB` second and fourth, `AxAx` unconstrained alternate lines. Letters reset in each section.

## Checks worth running

`structure_check.py structure.md`, then after all artifacts exist `structure_check.py --consistency structure.md lyrics.md chords.md melody.abc`.
