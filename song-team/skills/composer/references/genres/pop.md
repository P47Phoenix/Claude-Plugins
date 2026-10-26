---
loaded_by: harmony, melody, groove
level: L3
last_reviewed: 2026-10-26
---

# Genre: Pop

## Common progressions (Roman numerals, one cell per bar)

- Verse: `| I | V | vi | IV |`, `| vi | IV | I | V |`, `| I | iii | IV | I |`
- Pre-chorus: `| ii | IV | V | V |` (half cadence into the chorus), `| IV | V | vi | V |`
- Chorus: `| IV | I | V | vi |` then `| IV | I | V | I |`; or `| I | IV | vi | V |` twice with the second ending `| V | I |`
- Bridge: `| vi | IV | I | V |`, or one borrowed colour: `| bVI | bVII | I | I |`
- Four chords per section is the norm; the chorus opens on a different degree from the verse.

## Tempo bands

| Mood | bpm |
|------|-----|
| ballad | 68-84 |
| mid-tempo | 92-108 |
| upbeat (default) | 112-126 |
| dance-leaning | 124-132 |

`4/4` always; `6/8` only for a ballad the brief calls "swaying".

## Feel

Straight eighths; backbeat on 2 and 4; the chorus adds a four-on-the-floor kick. Sections are 8 bars (verse, chorus), 4 bars (pre-chorus, post-chorus); an intro of 4; a final chorus repeat is expected when `target_length_sec` >= 180.

## Typical keys

Major: `C`, `D`, `G`, `A`, `F`; minor: `A`, `E`, `D`. Keep within four sharps or flats. A key change for the final chorus is a critique risk, not a feature; raise the melody instead.

## Melodic idioms

- Chorus peaks in line 1 on the hook's main stress, then repeats the shape in line 3.
- Verses narrow (a fifth), rhythmic, lots of repeated notes on one pitch; the chorus widens to an octave at most.
- Pre-chorus rises by step each line and ends on `2` or `7`, unresolved.
- Syncopation: anticipate the downbeat by an eighth on the hook's first syllable (`z A2 ...` or a tied pickup) in the chorus only.
- Post-chorus or tag: the hook's last three syllables on three notes, repeated.

## Section conventions for the groove role

| Section | Bars | Lines | Syllables per line |
|---------|------|-------|--------------------|
| Verse | 8 | 4 | 7-9 |
| Pre-Chorus | 4 | 2 | 8-10 |
| Chorus | 8 | 4 | 7-9, hook line shortest |
| Bridge | 8 | 4 | 8-9 |

## Threshold overrides

`diatonic_min_ratio`: no override (default 0.6). Pop charts that pass sit at 0.85 or above; spend the budget on the bridge.
