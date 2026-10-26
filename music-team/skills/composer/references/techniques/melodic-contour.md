---
loaded_by: composer
level: L3
last_reviewed: 2026-10-26
---

# Melodic Contour

Contour is the shape a melody draws over time. A singable tune has a clear shape, a small number of ideas, and a high point that is reached once and earned.

## Shapes

| Shape | Description | Use |
|-------|-------------|-----|
| Arch | rises to a peak, then falls | the most common phrase shape; verse lines |
| Inverted arch | dips, then returns | reflective lines, questions |
| Ascending | steady climb | pre-chorus, building tension |
| Descending | steady fall | resolution, ends of sections |
| Wave | rise and fall repeated | folk, lullaby |
| Plateau | repeats around one note | recitative, rap-adjacent verses, tension |

## Range plan by section

| Section | Register | Notes |
|---------|----------|-------|
| Verse | low to middle of the vocal range | conversational, narrow (a sixth to an octave) |
| Pre-Chorus | climbs through the middle | ends on a note that wants to move |
| Chorus | sits high, includes the song's peak note once or twice | widest range, longest notes |
| Bridge | new area: lower or higher than the chorus | contrast of register |
| Outro | falls or repeats the hook | settle |

The chorus peak is usually a third to a fifth above the verse's top note. Keep every pitch inside the vocal range (default G3-G5; check the brief).

## Intervals

- Steps (1-2 semitones) carry most of a melody.
- Skips of a third or fourth add shape; chord tones make them sound inevitable.
- Leaps of a fifth or more are events: approach from below or above by step, and return in the opposite direction within a note or two.
- The gate limit is `max_melodic_leap` (default 12 semitones); aim for far fewer than that.

## Chord tones and strong beats

Put a chord tone of the bar's chord on strong beats and on the last note of each phrase. Weak beats carry passing and neighbor tones. The last note of a section lands on the root or third of the tonic chord for finality, on the fifth or second for continuation.

## Motif and development

1. State a short motif (2-5 notes) in the hook.
2. Repeat it with a changed ending (variation), then transposed within the key (sequence).
3. Contrast with a new motif in the bridge, then return to the hook.
4. Repeat every phrase at least once; a melody with no repetition reads as noise.

## Syllable and contour

Stressed syllables take the highest note of a small group or a longer note; unstressed syllables fall away. Match emotion: rising contour on questions, falling on statements. Long notes belong to key words and the hook's last word.

## Hooks

A hook melody is short, rhythmically distinct, and repeated. Keep it inside an octave, built from two or three scale degrees plus one skip; place its peak on the stressed syllable of the hook line.

## Checklist

| Check | Pass when |
|-------|-----------|
| One peak per phrase | no flat plateau of random highs |
| Chorus higher than verse | by a third or more |
| Leaps recover | after a leap, stepwise motion in the opposite direction |
| Phrase ends | on chord tones |
| Range | inside the vocal range, no unsingable extremes |

Use `abc_validate.py` for the range, leap, and bar-sum checks.
