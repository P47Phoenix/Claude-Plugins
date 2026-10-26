---
loaded_by: groove
level: L3
last_reviewed: 2026-10-26
---

# Technique: Rhythmic Feel, Tempo, Key, and the Hook's Meter

The groove role fixes four numbers (`bpm`, `time_sig`, `key`, `mode`) and one pattern per lyric line. The numbers come from the brief; the pattern for Chorus line 1 comes from the hook line itself, counted the way `prosody_check.py` counts.

## Tempo

| Mood word in `brief.md` | Band (bpm, 4/4) | Feel |
|-------------------------|-----------------|------|
| still, tender, grief, lullaby | 60-76 | ballad; one chord per bar, long notes |
| reflective, warm, nostalgic | 76-92 | mid-slow; half-time backbeat |
| hopeful, steady, road, story | 92-110 | walking; the default for folk and country |
| upbeat, bright, confident | 110-126 | pop drive; eighth-note pulse |
| urgent, joyful, dance, anthem | 126-140 | push; four-on-the-floor or driving eighths |
| frantic, party, jingle | 140-160 | fast; short sections, short lines |

Clamp to the form template's band (`VCVCBC` 84-140, `AABA` 60-120, `verse-refrain` 70-130, `jingle` 100-160, `edm-build-drop` 120-150, `through-composed` 60-140) and then to the genre file's band. Pick an integer. Compute running time before writing: `bars x beats_per_bar x 60 / bpm`; adjust bars (inside each group's range) rather than tempo when the result misses `target_length_sec` by more than 15 percent.

## Time signature

`4/4` unless the genre file or the brief says otherwise. `3/4` for a waltz or a lilting folk ballad; `6/8` for a rolling, compound feel (count two dotted-quarter beats per bar; `bpm` then names the quarter note, which is what `Q:1/4=` in ABC means, so a 6/8 song at 120 feels like 40 slow pulses). `5/4` and `7/8` are outside the Stage 5 scripts' defaults; avoid them unless the brief insists, and say so in `SUMMARY`.

## Key and mode from mood

| Mood | Mode | Keys that sit well for a mid voice (range 55-79) |
|------|------|--------------------------------------------------|
| bright, open, hopeful | major | `C`, `D`, `G`, `A` |
| warm, wistful | major with `vi` emphasis, or mixolydian | `F`, `Bb`, `G mixolydian` |
| dark, driving, tense | minor | `A`, `E`, `D`, `B` |
| floating, ambiguous | dorian | `D dorian`, `A dorian` |
| grand, hymn-like | major, plagal motion | `Eb`, `Ab` |

Write `key` as the tonic only (`D`) and `mode` as the word (`major`, `minor`, `dorian`, `mixolydian`); `chords.md` and `melody.abc` restate them in their own spellings. Keys with more than four sharps or flats are legal but every downstream role pays for them; prefer the table.

## Feel words for the arranger

The structure does not record feel, but `SUMMARY` does, in these terms so the arranger inherits them: `straight eighths`, `swung eighths`, `half-time`, `four-on-the-floor`, `backbeat on 2 and 4`, `waltz`, `shuffle`, `train beat`. One term per song.

## Counting the hook line (Chorus line 1)

`concept.md.hook_line` becomes the first `meter_spec` entry of every Chorus row, as `<n>/<pattern>`. Count it by hand with these rules; they are the ones `prosody_check.py` applies at Stage 4, so a correct count here is what lets the lyricist pass.

**Syllables.** Performance counts from the exception table first (`every` 3, `everything` 3, `fire` 1, `hour` 1, `our` 1, `tired` 1, `real` 1, `poem` 2, `flower` 2, `heaven` 2, `evening` 2, `family` 3, `camera` 3, `idea` 3, `piano` 3). Otherwise count vowel groups (`a e i o u y` runs; `y` is a vowel only between a consonant and a non-vowel). A trailing silent `e` after a consonant does not count (`name` 1, `candle` 2 with `-le` counting one). `-ed` after a consonant other than `t`/`d` is silent (`walked` 1, `wanted` 2). `-es` counts only after `s x z c g ch sh`. Hiatus pairs `ia io iu eo ua uo` split (`radio` 3). Minimum one. Contractions count as written (`I'm` 1).

**Stress.** Monosyllables are `u` when they are function words (articles, prepositions, pronouns, auxiliaries, conjunctions, and `like still yours not am is are did no so just oh yeah`), else `S` (`here yet down now one well` are content words). A line-final stranded preposition (`on in at by for with through off`) is `S`. Polysyllables: exception pattern first (`every` Suu, `idea` uSu); then a stress-fixing suffix (`-tion -sion -cian -ic -ity -ical -logy -ette -eer -self`: `nation` Su, `electric` uSu, `myself` uS); then strip a neutral inflection (`-s -ed -ing -er -ly -ness -ful -less -ment`) and re-evaluate the base (`morning` Su, `forgets` uS); then an unstressed Latin prefix (`un- re- de- be- ex- com- con- pre- pro- dis- trans- a-`) before an open syllable (`before` uS, `again` uS, `remember` uSu, `about` uS); else first-syllable stress (`window` Su, `nobody` Suu).

**Worked examples (original hook lines).**

| Hook line | Count | Pattern | Entry |
|-----------|-------|---------|-------|
| Nobody knows my name here yet | 8 | `Suu S u S S S` | `8/SuuSuSSS` |
| Stay awake for the falling light | 8 | `S uS u u Su S` | `8/SuSuuSuS` |
| Half the island looks away | 7 | `S u Su S uS` | `7/SuSuSuS` |
| Leave the porch light on | 5 | `S u S S S` | `5/SuSSS` |

Write the entry exactly as counted; do not round it to a template default. If the count exceeds the genre's chorus syllable band, say so in `SUMMARY` (the hook was gated at Stage 2 against `hook_max_syllables`, so it is the structure that bends, not the hook).

## Other meter lines

Verse lines in the genre's band, iambic (`uSuSuSuS`) for narrative, trochaic (`SuSuSuS`) for declarative or chorus lines. Line counts per section: verse 4, pre-chorus 2, chorus 4 (line 1 is the hook), bridge 2 or 4, tag 1, post-chorus 2. Keep every repeated section's spec identical. Rhyme scheme letters: `ABAB` verses, `AABB` choruses, `AA`/`AABB` bridges, `x` for a line you want free.
