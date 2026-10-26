---
loaded_by: song-critic
level: L3
last_reviewed: 2026-10-26
---

# Rubric: music (music-judge)

Five criteria, 1-5 each. `chord_tools.py` and `abc_validate.py` decide the gate.

| Criterion | 5 means | 1 means | Gate link |
|-----------|---------|---------|-----------|
| Harmonic coherence | Chords fit the key and mode; non-diatonic chords have a stated job | Clashing or unexplained chords | `diatonic_min_ratio`, spelling violations |
| Singability | Range inside `vocal_range`, tessitura in the middle third, small leaps | Wide leaps, extreme notes | `max_melodic_leap`, range violations |
| Lyric fit | One syllable per note, stressed syllables on strong beats | Syllable count or stress mismatches | lyric alignment violations (`w:` lines) |
| Hook contour | The chorus melody rises or peaks where the hook lands | Flat or buried hook | none |
| Cadence and pacing | Phrases end on stable chords at section ends; harmonic rhythm suits the genre | Sections end without arrival | none |

## Reading the gate JSON

- Spelling or key violations: name the bar and the chord, say the correct spelling in the key (do not re-voice the song).
- Diatonic ratio under the limit: list the offending chords and say which to keep as deliberate colour and which to replace.
- Leap or range rows: give the bar, the interval or pitch, and a smaller or transposed alternative.
- Alignment rows (`<section>:<bar>`): state the note count versus the syllable count and which syllable to merge, split or tie.
- Section label or `K:`/`M:` mismatches against `structure.md`: the fix is in the music file, never in `structure.md`.
