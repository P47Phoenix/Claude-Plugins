---
loaded_by: composer
level: L3
last_reviewed: 2026-10-26
---

# Modal Color

A mode is a scale with its own home. To make a progression sound modal, emphasize the one note that distinguishes the mode and avoid the chords that pull it back to major or minor.

## Characteristic chords

| Mode | Tonic chord | Characteristic note | Characteristic chord(s) | Avoid |
|------|-------------|---------------------|-------------------------|-------|
| mixolydian | I (major) | b7 | bVII, v (minor five) | V7 (a leading tone undoes the b7) |
| dorian | i (minor) | natural 6 | IV (major four) | bVI (that is aeolian) |
| lydian | I (major) | #4 | II (major two) | IV (cancels the #4) |
| phrygian | i (minor) | b2 | bII (major flat two) | V (not in the mode) |
| aeolian (minor) | i | b6 | bVI, bVII, iv | V (adds the leading tone) unless a close is wanted |
| locrian | i° | b5 | rare; usually a passing color | stable triads on the tonic |

Numerals stay major-scale-relative (see `theory/functional-harmony.md`): D dorian reads `i`, `IV`, `bVII`; D mixolydian reads `I`, `bVII`, `IV`.

## Progression recipes

| Mode | Recipe | Example in D |
|------|--------|--------------|
| mixolydian | I bVII IV I | D C G D |
| mixolydian | I bVII | D C (vamp) |
| dorian | i IV | Dm G (vamp) |
| dorian | i bVII IV i | Dm C G Dm |
| lydian | I II | D E (float) |
| phrygian | i bII i | Dm Eb Dm |

Tonic first, characteristic chord second, return to the tonic. Two-chord vamps are legitimate; mode is conveyed by the pair.

## Writing modal melodies

1. Build the tune on the mode's scale; lean on the characteristic note over the tonic or the chord that carries it.
2. Start and end phrases on the tonic or a pedal-adjacent chord tone.
3. Keep the harmonic rhythm slow (one chord per bar or per two bars).
4. A drone or pedal (tonic held in the bass) cements the center.
5. Use the characteristic note on long notes; use common notes for motion.

## Declaring the mode

In `structure.md` write `mode: mixolydian` (full name). In `melody.abc` write `K:Dmix` or `K:D mixolydian`; in `chords.md` write `key: D mixolydian`. The key signature handles the lowered seventh, so do not add accidentals.

## Diagnosing a mode in a supplied progression

D, C, G, D: the note C (b7 of D) is present and there is no C#. Home chord is D major. That points to D mixolydian. Confirm with `chord_tools.py scale D mixolydian` (D E F# G A B C) and `roman D D C G D --mode mixolydian` (all diatonic).

## Mixing modes within a song

Verse in the minor mode, chorus in its parallel major, is a familiar lift: same tonic, new third. Use a pivot (a shared chord, or a bVII that points up) for the move. Do not change the declared `mode` mid-song; use borrowed chords (`borrowed-chords.md`) for temporary color.

## When not to go modal

If the lyric needs strong resolution (a promise kept, a decision made), use V to I. Reserve modal vamps for open-ended or atmospheric lines.
