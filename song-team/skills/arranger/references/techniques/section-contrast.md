---
loaded_by: instrumentation, dynamics
level: L3
last_reviewed: 2026-10-26
---

# Technique: Section Contrast (making the form audible)

A listener who cannot hear the lyric should still know when the chorus arrives. Contrast is the arranger's only tool for that, and it is spent in four currencies: density, register, rhythm, and space. Every consecutive pair of sections should differ in at least two of them. This file is the checklist for `instruments_in`, `instruments_out`, and `texture_note`.

## The four currencies

| Currency | Low setting | High setting | Cheapest move |
|----------|-------------|--------------|---------------|
| Density | 2-3 parts, one note per beat or less | 6+ parts, pads and doubles | add or remove one part |
| Register | lead and accompaniment in the middle octave | top harmony an octave up, sub bass below | double the lead an octave up in the chorus |
| Rhythm | half-time kit, long notes, no hi-hat | straight eighths, open hi-hat, syncopated bass | change the hi-hat pattern |
| Space | dry, mono, close | wide stereo, reverb tail, delay | widen the doubles, open the reverb |

A chorus that only gets louder changes one currency. A chorus that adds a part, lifts the harmony an octave, opens the hi-hat, and widens the vocal changes four and will feel twice as big at the same level.

## Entry and exit grammar

- **Hold back.** The opening section uses at most half the final palette. Every section until the first chorus adds something; nothing leaves before the first chorus.
- **Subtract to return.** A verse after a chorus loses at least one part (the pad, the doubles, the open hi-hat) so the next chorus can add it back. Listeners hear a re-entry more clearly than a first entry.
- **One new thing per chorus.** Chorus 2 adds a part Chorus 1 did not have; the final chorus adds one more (a high harmony, a group vocal, a counter-line). This is what makes the rising energy numbers true.
- **Change the floor in the bridge.** Remove the kit, the main chordal instrument, or the bass, or hand the lead to a different instrument. A bridge with the chorus palette at lower volume is a quieter chorus, not a bridge.
- **Mid-section entries get a bar number.** `bass enters bar 5`, `hi-hat from bar 3`, `drum break on bar 8`. The producer needs the bar, and the `dynamics` role needs to know the section is not static.
- **Nothing enters twice without leaving.** If the pad is in `instruments_in` for Chorus and again for the final Chorus, it must appear in an `instruments_out` cell in between.

## Textures by section role (starting points, not rules)

| Section | Density | Register | Rhythm | Space |
|---------|---------|----------|--------|-------|
| Intro | 1-3 parts, a motif or the chord loop | middle | sparse, often no kit | dry or one long reverb |
| Verse | 3-4 parts | middle; nothing above the lead | kit light or half-time; hi-hat closed | dry lead, narrow |
| Pre-Chorus | verse plus one or two | bass walks up; harmony rises | subdivision doubles; snare build or tom fill | doubles begin |
| Chorus | full palette minus the last reveal | lead doubled; top harmony up | straight eighths or four-on-the-floor; hi-hat open | wide, reverb and delay on |
| Bridge | subtract two parts or swap the lead | often lower or a new instrument's range | feel change (half-time, stop-time, or rubato) | either very dry or very wet, not chorus-wide |
| Final Chorus | everything | highest harmony, group vocal | busiest | widest |
| Outro | fragments of the intro palette | falling | thinning | tail or hard stop |

## Writing the `texture_note`

One phrase, under 90 characters, naming the currencies that moved: `half-time feel, pad filtered, single vocal` says rhythm, space, and density in nine words. Avoid adjectives that name a feeling (`hopeful`, `anxious`) or a comparison (`like a stadium`); write what a producer would set (`wide stereo doubles`, `open hi-hat`, `bass on the root only`).

## Quick audit before writing

1. Do any two adjacent rows share the same `instruments_in`, `instruments_out`, and the same first three words of `texture_note`? Change one.
2. Does each chorus row add at least one part the previous chorus row did not? If not, move an entry.
3. Does the bridge row have a non-empty `instruments_out`? If not, strip it.
4. Does the final chorus row contain the last reveal? If the reveal happened earlier, move it.
5. Does any verse row have the lead doubled? Undouble it; save doubles for the chorus.
