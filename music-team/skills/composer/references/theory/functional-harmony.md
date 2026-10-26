---
loaded_by: composer
level: L3
last_reviewed: 2026-10-26
---

# Functional Harmony

## Numeral conventions (used by every composer artifact)

Numerals are major-scale-relative with accidentals. Uppercase is a major triad, lowercase minor, `°` diminished, `ø7` half-diminished, `+` augmented; qualities `7`, `maj7`, `m7`, `add9`, `sus2`, `sus4` follow the numeral. In a minor key the diatonic set reads `i ii° bIII iv v bVI bVII`, with `V` and `vii°` available from the raised seventh.

## Diatonic chords in a major key

| Degree | Triad | Seventh | Function |
|--------|-------|---------|----------|
| I | major | maj7 | tonic: rest, arrival |
| ii | minor | m7 | predominant: leaves home, leads to V |
| iii | minor | m7 | tonic substitute (weak); links I and IV or vi |
| IV | major | maj7 | predominant: opens up, or plagal landing |
| V | major | 7 | dominant: tension, wants I |
| vi | minor | m7 | tonic substitute: the relative minor, softer than I |
| vii° | diminished | ø7 | dominant substitute: V without its root |

In C: C Dm Em F G Am B°; with sevenths Cmaj7 Dm7 Em7 Fmaj7 G7 Am7 Bm7b5. Use `chord_tools.py diatonic <key>` for any key.

## The three functions

- **Tonic (T):** I, vi, iii. Stability; sections begin and end here.
- **Predominant (PD):** ii, IV. Motion away from tonic that prepares the dominant.
- **Dominant (D):** V, vii°. Tension that resolves to T.

The default flow is T to PD to D to T. Skipping a step is fine (T to D, PD to T); retrograde motion (D to PD) sounds like a pop-style loop rather than a sentence, which is a feature in loop-based genres.

## Cadences

| Cadence | Motion | Effect |
|---------|--------|--------|
| Authentic | V(7) to I | full close |
| Plagal | IV to I | soft, "amen" close |
| Half | any to V | open, a question |
| Deceptive | V to vi | surprise, extends the phrase |
| Modal | bVII to I | rock/folk close, no leading tone |

Every section should end on one of these. The gate warns when a section's last two chords form none of V-I, IV-I, V-vi, bVII-I.

## Common progressions by role

| Role | Shape | Use |
|------|-------|-----|
| Loop | I V vi IV | verse or chorus, open and circular |
| Loop, minor start | vi IV I V | verse that leans into a chorus |
| Sentence | I IV V I | grounded, classic close |
| Pre-chorus lift | IV vi V (or ii IV V) | rises without landing; end on V |
| Bridge contrast | vi IV V (start off tonic) | shifts the center |
| Circle | I vi ii V | steady fifth-based motion |
| Minor loop | i bVI bIII bVII | brooding, cyclical |

## Secondary dominants and borrowing

A secondary dominant is the V or V7 of a degree other than I: `V7/vi` in C is E7 going to Am. It adds one non-diatonic chord with a strong reason. Modal mixture borrows a chord from the parallel mode (see `techniques/borrowed-chords.md`).

## Slash chords

`I/3` puts the third in the bass (first inversion) for a smoother bass line; `V/b7`-style bass choices are voice-leading tools, not new harmonies. A pedal is a repeated bass note under changing chords.

## Harmonic rhythm

How often chords change. One chord per bar is the pop default; two per bar speeds a bridge or turnaround; one per two bars suits ballads and modal vamps. Keep the rate constant within a phrase, change it at section boundaries.

## Checking a chart

Run `chord_tools.py roman <key> <chords...>` to read a chord list as numerals and see which chords are non-diatonic.
