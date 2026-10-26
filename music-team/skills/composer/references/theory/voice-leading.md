---
loaded_by: composer
level: L3
last_reviewed: 2026-10-26
---

# Voice Leading

Voice leading is how each note of one chord moves to the next. Good voice leading makes a progression feel inevitable even when the chords are plain.

## Principles

1. **Keep common tones.** If two chords share a note, hold it. C to Am share C and E; only G moves (to A).
2. **Move the rest by step.** Prefer a second (1-2 semitones) to a leap. Total motion across all voices stays small.
3. **Contrary motion against the bass.** When the bass goes up, upper voices tend down, and the reverse.
4. **Resolve tendency tones.** The leading tone (7) rises to 1; the chord seventh falls by step; a suspension resolves down.
5. **Avoid parallel perfect fifths and octaves** between the same two voices in adjacent chords.

## Parallel fifths

Two voices a perfect fifth apart that both move by the same interval to another perfect fifth. In root-position triads that move by step (C to D, Am to Bm), the roots and fifths run in parallel if every voice shifts the same way. Fixes: invert one chord, keep a common tone, or move one voice contrary. `chord_tools.py` warns about adjacent root-position triads whose roots are a step apart; the warning does not fail the gate.

## Inversions and slash chords

| Chart | Bass note | Use |
|-------|-----------|-----|
| `I/3` | third of I | smooth step from the previous bass note to IV |
| `V/7` (in numerals `V/b7`) | seventh of V | descending bass line |
| `IV/1` | tonic under IV | pedal; keeps the bass still |

Write inversions as slash numerals in `chords.md`; the concert line shows the bass note (`C/E`).

## Bass lines

- **Stepwise descent:** I, V/7, vi, I/3 (C, G/B, Am, C/E) walks the bass 1 7 6 3 with one move per bar.
- **Pedal:** the tonic or the dominant held while chords above change; builds tension at section ends.
- **Walking:** one note per beat, chord tones on strong beats and passing tones between (jazz, blues).
- **Root-fifth alternation:** the baseline for folk, country, and gospel feels.

## Spacing

Keep the upper three voices within an octave of each other when they are close together (the common vocal and piano spacing); open the lowest interval up when the bass is low. Avoid doubling the leading tone and the chord seventh.

## Melody against harmony

On strong beats, put a chord tone in the melody; use passing and neighbor tones on weak beats. A sustained non-chord tone is a suspension: prepare it (same note in the previous chord), sound it on the beat, resolve down by step. Leave an unresolved color tone (add9, 6) only on long notes.

## Quick checklist for a progression

| Check | Pass when |
|-------|-----------|
| Bass line | moves by step or a fifth in most bars, no random leaps |
| Common tones | at least one shared note between neighbors in most chord pairs |
| Tendency tones | leading tone and chord sevenths resolve |
| Section ends | land on a cadence with the bass on the root |
| Parallels | no adjacent root-position triads a step apart in the same voicing |

## Where the scripts help

`chord_tools.py chord <symbol>` shows the chord's spelling so common tones are visible; `chord_tools.py transpose` keeps the voice-leading shape in a new key.
