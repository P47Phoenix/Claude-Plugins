---
loaded_by: composer
level: L3
last_reviewed: 2026-10-26
---

# Reharmonization

Replace or enrich chords while keeping the melody and the phrase function. Every substitution should either share the original chord's function or add a stronger lead-in.

## Substitution families

| Family | Replace | With | Why it works |
|--------|---------|------|--------------|
| Relative | I | vi or iii | share two notes with I |
| Predominant swap | IV | ii (or ii7) | both are predominant; ii leads into V by a fifth |
| Extension | triad | 7th, 9th, 13th | same function, richer color |
| Dominant extension | V | V7, V9, V13, V7sus4 | more tension, same resolution |
| Tritone substitution | V7 | bII7 | shares the 3rd and 7th (tritone) with V7; bass slides down by half step |
| Secondary dominant | any chord X | V7/X before X | leads in by a fifth |
| Related ii-V | V7/X | ii7-V7 of X | stretches a lead-in over two chords |
| Diminished passing | between I and ii | #i°7 | chromatic bass line |
| Borrowed | IV | iv, bVI, bVII | color from the parallel minor |
| Slash/pedal | any | same chord over a held bass | stills the harmony |

## Style palettes (what `chord_tools.py reharmonize --style ...` applies)

| Style | Moves |
|-------|-------|
| jazz | add 7ths to every chord (maj7, m7, 7, ø7), swap IV for ii when it leads to V, insert ii before V, close an open V with I; optional tritone substitute for V7 before I |
| blues | dominant 7ths on I, IV, V (minor blues: m7 on i and iv); 12-bar sketch printed alongside |
| gospel | secondary dominants into ii, vi, V; passing diminished 7ths I to ii and IV to V; IV over a V bass (`IV/V`) before I; maj7 and m7 colors |
| bossa-nova | maj9 on I, m9 on ii and vi, dominant 13ths, III7b9 leading into vi, minor iv with a sixth |
| pop | strip to diatonic triads, replace ii with IV and iii with vi, vii° with V; suggests the vi IV I V loop shape |

## Gentle, medium, bold

| Level | Changes | Example in C: C Am F G |
|-------|---------|------------------------|
| Gentle | add 7ths, keep roots | Cmaj7 Am7 Fmaj7 G7 |
| Medium | swap one predominant, add a lead-in | Cmaj7 Am7 Dm7 G7 |
| Bold | secondary dominants and a tritone substitute | Cmaj7 E7 Am7 Db7 |

Offer 2-3 levels; keep the melody's strong-beat notes as chord tones or recognised extensions of the new chords.

## Rules of thumb

1. **Change function sparingly.** One new chord per phrase is a reharmonization; four is a different song.
2. **Keep the cadence.** Do not remove the arrival chord the melody ends on.
3. **Check melody notes.** A melody note that is the root of the old chord can be a 9th or 7th of the new one; one that clashes (a half step above a chord tone on a strong beat) needs a different chord.
4. **Match harmonic rhythm.** Add chords by splitting a bar, never by adding bars unless the structure is updated.
5. **Genre first.** A pop chorus wants triads and a loop; do not convert it to altered dominants unless asked.
6. **Respell with the tool.** Run `chord_tools.py reharmonize <key> <chords...> --style <style>` and use its table (source, target, reason) as the starting point; always re-check spellings.

## Minor keys

Use iiø7 to V7(b9) to i7 for the jazz cadence; bVII and bVI are diatonic, so most substitutions are extensions; the raised seventh makes V major, the fastest way to a firm close.

## Process

1. Analyze the original into numerals and functions.
2. Mark the arrival chords the melody depends on.
3. Choose a family and a level for each weak spot.
4. Generate with the tool, edit for taste, re-spell.
5. Explain each change in one line: function kept or replaced, effect on the ear.
