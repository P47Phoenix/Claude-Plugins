---
loaded_by: melody
level: L3
last_reviewed: 2026-10-26
---

# Technique: Melodic Contour, Range, and Tessitura

`abc_validate.py` measures three things about pitch: the lowest and highest note against `vocal_range`, the largest interval between consecutive heads against `max_melodic_leap`, and nothing else. Everything below the gate (contour, peak, tessitura) is what the music-judge reads. Write for the voice, then check the three numbers.

## Range and tessitura

- `vocal_range` default is MIDI 55-79: `G,` (G3) to `g` (G5) in ABC with `L:1/8` and no transposition. A config or genre override widens or narrows it; the prompt's gate JSON on re-dispatch states the resolved value.
- **Tessitura** is where the voice lives, not where it is allowed. Keep 80 percent of the heads inside the **middle third** of the range: for 55-79 that is MIDI 63-71, `_E` to `B` in ABC (`E` to `B` with the key's accidentals). Verses sit in the lower half of the tessitura, choruses in the upper half.
- The range extremes are spent on purpose: the top note once per chorus on the hook's stressed syllable, the bottom note once in a verse or the bridge's first bar. A melody that touches `g` four times in a verse has no chorus left.
- MIDI quick table (no accidentals): `G,`=55 `A,`=57 `B,`=59 `C`=60 `D`=62 `E`=64 `F`=65 `G`=67 `A`=69 `B`=71 `c`=72 `d`=74 `e`=76 `f`=77 `g`=79. Key-signature sharps and flats shift the letter by one (in D major, `F` is 66 and `C` is 61).

## Leaps

- `max_melodic_leap` default 12 semitones (an octave). The gate checks every pair of consecutive heads, across bar lines and section boundaries too; a tied note is not a new head. A rest between two notes does not reset the pair.
- Craft limit is tighter than the gate: a leap larger than a fifth (7 semitones) is followed by a step in the opposite direction; two leaps in the same direction in a row stay inside an octave combined.
- The biggest leap of the song belongs to the chorus entry (verse-end note up to the hook's first stressed note) or to the bridge's first phrase. Verses move by step and third.

## Contour shapes per section

| Section | Shape | Peak | Start and end |
|---------|-------|------|---------------|
| Verse | arch or gentle descent; narrow (a fifth or sixth) | mid-phrase, below the chorus peak | starts and ends on a chord tone of `I` or its substitute |
| Pre-Chorus | rising; each line starts higher than the last | last note before the chorus, unresolved (`2` or `7` of the key) | ends on a non-tonic so the chorus feels like arrival |
| Chorus | arch with an early peak; widest range (an octave at most) | line 1 or line 2, on the hook's main stressed syllable | starts on `1`, `3`, or `5`; ends on `1` in the final chorus |
| Bridge | starts on the note the chorus never started on; contrasts in direction | its own smaller peak, never above the chorus peak | ends on `5` or `2` so the last chorus resolves it |
| Tag/Outro | fragment of the chorus's first phrase, lower | none | ends on `1` |

## Stress and placement

The `meter_spec` entry for each lyric line marks `S` and `u`. Put every `S` on a strong beat (beats 1 and 3 in 4/4; beat 1 in 3/4) or on a note longer than its neighbours; put `u` syllables on weak beats or short notes. A stressed syllable on a weak eighth is the first thing the judge hears. When the chart has one chord per bar, the downbeat note is a chord tone (root, third, fifth) in at least three bars of four; passing tones fall on the offbeats.

## Repetition and variation

- The chorus melody is identical in every chorus. The final chorus is allowed one variation in its last line (a higher ending note, or a held hook note with `_`).
- Verse 2 reuses Verse 1's melody with at most two notes changed to fit the new lyric's stresses.
- A motif (two to four notes with a rhythm) stated in Verse 1 returns in the chorus transposed up; this is what makes a melody feel composed rather than generated.

## Worked example (original; Chorus line 1, spec `8/SuuSuSSS`, D major, hook on the peak)

```abc
%%section Chorus
d2 c2 B2 A2 | B2 A2 F2 ED |
w: No-bo-dy knows | my name here yet_ |
```

Peak `d` (74) on `No-`, the first `S`; `knows` (`S`) on a quarter; `name`, `here`, `yet` on the three closing stresses; the melisma `_` on `yet` makes bar 2's 6 heads match 5 syllables + 1 extension. Range used: 62-74, tessitura centre 67.

## Reading an `abc_validate.py` result

- `pitch outside vocal_range`, `location: Chorus:3`, `observed: 81`: lower that bar's peak by a third, or move the whole chorus down a step and tell the harmony role in `SUMMARY` (a key change is a debate, not a unilateral edit).
- `melodic leap exceeds max_melodic_leap`, `observed: 14`: insert a passing note or shrink the leap; the pair is the last head of one bar and the first of the next when `location` names a bar's first note.
- `metrics.min_pitch`/`max_pitch` in a PASS: when the span is under a sixth, the chorus has no lift; when it is over a twelfth, the verse is too high or the chorus too low.
