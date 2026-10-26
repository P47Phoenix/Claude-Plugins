---
loaded_by: adapter
level: L3
last_reviewed: 2026-10-26
---

# Technique: Reharmonization Moves

Change the colour of the harmony to suit `target_genre` while the key, the section cadences and the melody's
strong-beat notes stay put. Work in roman numerals (uppercase major, lowercase minor, `b` for flat, `7`
dominant seventh, `maj7`, `m7`, `7b5`, `sus4`, `add9`); concert chords go on the `>` line. The target's
`## Harmony` lists the chords and progressions that are idiomatic; use those first.

## Rules of the road

1. Keep the **tonic** and the **final cadence** of each section (V to I, IV to I, or the open dominant) unless the
   target profile explicitly drops it; log any drop under Risks.
2. Keep every **melody note on a strong beat** inside the new chord (root, third, fifth, seventh, or the
   chord's stated extension). If it clashes, change the chord, not the note.
3. Change **one dimension at a time** per section: colour, then substitution, then insertion. Layering all
   three in one bar makes the progression unreadable.
4. Stay inside `quality.diatonic_min_ratio`: at least 60 percent of the chords in a section diatonic to the key,
   and at most 40 percent chromatic or borrowed.
5. Move bass notes by step where possible; the bass line is what listeners hear as the "progression".

## Moves toward richer genres (jazz-influenced, bossa, R&B, gospel)

| Move | Example | Use when |
|---|---|---|
| Add a seventh or extension | I to Imaj7; IV to IV9; V to V7 | any triad that is held for a bar or more |
| Passing ii-V | insert ii7 - V7 before a target chord one bar long | the source holds a chord for two bars |
| Secondary dominant | V7/V before V; V7/vi before vi | a stepwise bass approach is wanted |
| Tritone substitution | V7 to bII7 | the bass can descend by semitone to the tonic |
| Modal interchange | borrow iv, bVII, bVI from the parallel minor | a bright major phrase needs shade |
| Chromatic passing chord | diminished seventh between I and ii | a quick bar of motion between two stable chords |
| Pedal tone | keep the tonic in the bass under moving upper chords | a lyric line needs to feel suspended |

## Moves toward plainer genres (folk, country, rock, pop)

| Move | Example | Use when |
|---|---|---|
| Strip extensions | Imaj7 to I; V7 to V | the target wants open triads |
| Collapse a ii-V | ii7 - V7 to a single V | the passing pair was decoration |
| Replace a substitute with the original | bII7 to V7 | a tritone substitution has no place in the target |
| Prefer a plain loop | I - IV - V - I; I - V - vi - IV | a lyric is the focus and the harmony must stay out of the way |
| Add a sus resolution | V to Vsus4 to V | the source chord needs motion but not colour |
| Widen the spacing | root and fifth only | the arrangement is acoustic and sparse |

## Minor-key notes

- The raised leading tone gives V7 in minor; keep it when the source cadence used it.
- The half-diminished ii (written `ii7b5`) is the natural approach to V7 in minor.
- Modal minors (Dorian, Mixolydian-flavoured) suit the folk, country and gospel profiles; keep the mode named in `structure.md`.

## Process

1. Write the source progression per section as roman numerals.
2. Mark the anchors: first and last chord of each section, any chord under a held melody note.
3. Choose moves from the matching table until the section matches the target's idiomatic progressions.
4. Re-voice for the target's instruments (open triads for acoustic, close voicings for keys and guitar).
5. Write one Changed entry per move family ("chord colour", "chorus harmony"), not one per bar.
6. Run the check: key, cadence, strong-beat notes, diatonic ratio.
