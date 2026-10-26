---
loaded_by: music-judge
level: L3
last_reviewed: 2026-10-26
---

# Melody Rubric (Stage 5)

Five criteria, each scored 1-5. Anchors are given for 1, 3, and 5; score 2 and 4 when the music sits between anchors. The rubric informs the critique and sets revision priority. `chord_tools.py` and `abc_validate.py` decide the gate; scores never alter `gate_status`. Metrics referenced: `abc_validate` `min_pitch`, `max_pitch`, `max_leap`, `aligned_bars`, `notes`; `chord_tools` `diatonic_ratio`, `warnings`.

## 1. Contour and climax

- **1**: the melody wanders with no shape; the highest note falls in a verse, or every phrase starts and ends on the same pitch.
- **3**: each phrase has a direction (rise, fall, arch), but the chorus peak arrives on an unstressed syllable or in the first bar.
- **5**: verse phrases arch low and return; the chorus peak (`max_pitch`) lands on a stressed syllable of the hook line, in the second half of the chorus, and is approached by step or one prepared leap.

## 2. Range and tessitura

- **1**: `max_pitch - min_pitch` exceeds the `vocal_range` span, or the chorus sits in the top three semitones for more than half its notes.
- **3**: inside `vocal_range`; the verse and chorus share a tessitura, so the lift comes only from the arrangement.
- **5**: verse tessitura in the lower-middle of the range, chorus a fourth or fifth higher, the top note touched no more than twice per chorus; no leap above `max_melodic_leap` and no leap over a sixth onto a weak syllable.

## 3. Rhythm and word stress

- **1**: stressed syllables fall on weak beats in the hook line, or a long note sits on a closed vowel or an article.
- **3**: strong beats carry stressed syllables in the chorus; verse lines have two or three collisions the singer must swallow.
- **5**: every `w:` bar aligns (`aligned_bars` equals `bars`); stressed syllables land on beats 1 and 3 or the agogic accent; long notes sit on open vowels; the rhythm of the hook line differs from the verse rhythm.

## 4. Hook identity

- **1**: the chorus melody is the verse melody with new words; no interval, rhythm, or repeated cell marks the hook line.
- **3**: the chorus has a distinct rhythm or opening interval, but the hook line's melody does not repeat anywhere else in the chorus.
- **5**: the hook line owns a melodic cell (a two- or three-note figure or a signature leap) that returns at least twice in the chorus and nowhere in the verse; a listener could hum it after the first chorus.

## 5. Harmonic fit

- **1**: `diatonic_ratio` below the limit with no expressive purpose; downbeat melody notes clash with the chord beneath; sections end on no cadence.
- **3**: diatonic and consonant; the melody sits on chord tones so completely that the verse and chorus both lack tension; `warnings` list a chorus without a cadence.
- **5**: downbeats on chord tones, passing tones on weak beats, one deliberate non-chord tone at the chorus peak; every section's last two cells cadence; any borrowed chord is placed under a lyric turn.

## Scoring notes

- Score the music as written in the two artifacts, not as it could be arranged.
- Criteria 2 and 5 reflect the gate; a 4 or 5 on a FAIL is a `## Suspected false positives` candidate (name the cell or bar).
- Total 10 or below on a PASS gate: recommend one optional quality loop before Stage 6; the orchestrator decides.
- Criterion 4 at 1 or 2 on a PASS gate produces a `rubric:notes` advisory row naming the chorus bars to vary.
