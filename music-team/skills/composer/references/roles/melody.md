---
loaded_by: composer
level: L2
last_reviewed: 2026-10-26
---

# Melody

## Role -> Reference Mapping

| Role | Contract | Genre section | Technique files (max 2) |
|------|----------|---------------|-------------------------|
| **Melody** | `contracts/melody-output.md` | `genres/<genre>.md` `## Rhythm` (and `## Harmony` for characteristic tones) | `techniques/melodic-contour.md`, `techniques/rhythmic-feel.md`, `techniques/abc-notation-primer.md`, `techniques/modal-color.md` |

## Detection Keywords

melody, topline, tune, hook melody, ABC, ABC notation, motif, singable, vocal line, range, contour, leap, melodic line, melody.abc, instrumental theme

## Task Type Routing Table

| Request Signal | Task Type | References Loaded |
|---|---|---|
| Pipeline Stage 5 after harmony (`TASK_TYPE: chords-melody`, `ROLE: melody`), "write the melody", "melody for these lyrics" | **melody** | melodic-contour.md, abc-notation-primer.md |
| TOPLINE with supplied chords ("a melody over my chords") | **melody** | melodic-contour.md, abc-notation-primer.md |
| "develop the motif", "variation for the second verse", "answer phrase" | **motif-develop** | melodic-contour.md, rhythmic-feel.md |
| "fit the words to the rhythm", "syllables land on the beat", "w: lines are off" | **rhythm-fit** | rhythmic-feel.md, abc-notation-primer.md |
| INSTRUMENTAL / JINGLE motif line (no lyrics) | **melody** | melodic-contour.md, rhythmic-feel.md |

## Task Type Instructions

| Task Type | What the sub-agent does |
|---|---|
| **melody** | Read `structure.md` (key, mode, bpm, time_sig, labels, bars), `chords.md`, `lyrics.md` (absent for INSTRUMENTAL), and the vocal range from the brief or config. Write ABC with headers `X T M L Q K` in that order, `M` equal to `time_sig`, `K` equal to key and mode, `Q:1/4=<bpm>`. One `%%section <Label>` line per structure section, same order. One music line per lyric line, a `w:` line after each music line when `lyrics.md` exists. Place chord tones on strong beats and stressed syllables; keep the whole line inside the vocal range and every leap within the gate limit (default 12 semitones) |
| **motif-develop** | Keep the hook motif's rhythm and contour recognisable; vary pitch level, ending, or length per section. Repeat verses with a changed cadence, not a new tune. The chorus sits higher than the verse and its hook gets the most repetition |
| **rhythm-fit** | Re-time notes so stressed syllables take downbeats or long notes and unstressed ones take short or off-beat notes. Use `_` melisma and `*` skips instead of inventing syllables. Re-count each bar: syllables plus extensions plus skips equal note heads |

## Guardrails

- **Bar sums are exact.** Every bar totals the meter (4/4 with `L:1/8` is 8 eighths per bar). A short pickup first bar or short final bar is tolerated by the gate; mid-tune short bars are not
- **`w:` alignment is arithmetic.** Per bar, tokens plus `_` extensions plus `*` skips equal the note heads (rests and tied continuations take no syllable). `-` splits a word, `~` joins two words, `|` advances the bar. De-hyphenated `w:` text per section equals the `lyrics.md` section ignoring case and punctuation
- **Single voice.** At most one `V:` line; chord symbols in quotes are annotations only, never extra voices
- **Range and leaps.** Stay inside `vocal_range` (default MIDI 55-79, G3-G5); prefer steps and small skips, answer a leap with a step back
- **Key signature handles accidentals.** Write notes of the key plainly; add `^`, `_`, `=` only for real chromatic notes (they last to the bar line)
- **Section markers.** `%%section` labels equal `structure.md` labels, including repeats of Chorus
- **Originality.** The tune is new: do not echo a known melody's contour or interval pattern; no artist or song names in titles or comments
- **Never certify.** Run `abc_validate.py` for early errors; the orchestrator's gate decides
