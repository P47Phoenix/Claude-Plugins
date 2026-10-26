---
loaded_by: harmony, melody, groove
level: L3
last_reviewed: 2026-10-26
---

# Genre: Folk

## Common progressions (Roman numerals, one cell per bar)

- Verse (major): `| I | IV | I | V |` then `| I | IV | V | I |`; or the modal frame `| I | bVII | IV | I |`
- Verse (minor or dorian): `| i | VII | i | v |` then `| i | III | VII | i |`; dorian: `| i | IV | i | VII |`
- Refrain line (last bars of a verse-refrain verse): `| IV | V | I | I |` or `| VII | I | I | I |`
- Bridge or instrumental: `| vi | IV | I | V |`, or a drone: `| I | I | I | I |` with the melody carrying the change
- Long stretches on one chord are idiomatic; a chart line of `| I | % | % | % |` is correct folk harmony.

## Tempo bands

| Mood | bpm |
|------|-----|
| lament, lullaby | 60-76 |
| ballad, story (default) | 80-100 |
| travelling, hopeful | 100-118 |
| reel, dance | 118-132 |

`4/4` default; `3/4` and `6/8` are as common as in any genre and the brief's "lilting" or "rolling" chooses `6/8`.

## Feel

Fingerpicked or strummed pulse; little or no backbeat; the bass moves on 1 and 3. Verses are 8 to 16 bars and carry the song (`verse-refrain` is the default template for a story brief); choruses, when present, are short refrains. An instrumental verse between verses 2 and 3 is expected on a `verse-refrain` form with four or more verses.

## Typical keys

Major: `G`, `D`, `C`, `A`; modal: `D dorian`, `A dorian`, `G mixolydian`, `E minor`. A drone key (`D` or `G`) suits an open-string instrument; keep to two sharps or fewer.

## Melodic idioms

- Stepwise, narrow (a sixth to an octave), mostly in the lower two thirds of the range; the refrain line is the only reach upward.
- Modal colour on a long note: the `b7` in mixolydian or the raised `6` in dorian held on a half note in the verse's third line.
- Melismas are short (`_` over one extra note) and land on the refrain's last word.
- Each verse repeats the melody exactly; variation comes from the lyric, not the tune. Verse 1's melody is the song.
- Avoid syncopated pickups; the first syllable of a line lands on beat 1 or the eighth before it.

## Section conventions for the groove role

| Section | Bars | Lines | Syllables per line |
|---------|------|-------|--------------------|
| Verse (verse-refrain) | 8-16 | 4 + 1 refrain line | 7-9, refrain 6-8 |
| Verse (VCVCBC) | 8 | 4 | 7-9 |
| Chorus | 8 | 2-4 | 6-8 |
| Bridge | 4-8 | 2 | 8-9 |
| Instrumental | 8 | 0 | (empty meter) |

## Threshold overrides

`diatonic_min_ratio`: no override (default 0.6), but a modal `structure.md` (`mode: dorian` or `mixolydian`) makes the characteristic chord diatonic for free, so a folk chart passes at 0.9 or above. Embed `techniques/modal-color.md` in place of `borrowed-chords.md` when the mode is named.
