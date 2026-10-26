---
loaded_by: composer
level: L2
last_reviewed: 2026-10-26
---

# Harmony

## Role -> Reference Mapping

| Role | Contract | Genre section | Theory / technique files (max 2 total) |
|------|----------|---------------|----------------------------------------|
| **Harmony** | `contracts/harmony-output.md` | `genres/<genre>.md` `## Harmony` (and `## Rhythm` for harmonic rhythm) | `theory/functional-harmony.md`, `theory/voice-leading.md`, `theory/reharmonization.md`, `theory/modes-scales.md`, `techniques/borrowed-chords.md`, `techniques/modal-color.md` |

## Detection Keywords

chords, chord progression, Roman numerals, harmonize, harmony, changes, key fit, cadence, turnaround, reharmonize a section, borrowed chord, modal progression, chords.md, concert pitch, what chords fit this melody

## Task Type Routing Table

| Request Signal | Task Type | References Loaded |
|---|---|---|
| Pipeline Stage 5 (`TASK_TYPE: chords-melody`), "write chords for the song", "chords for each section" | **chords-melody** | functional-harmony.md, borrowed-chords.md |
| "change the chorus chords", "fix the diatonic ratio", "the bridge feels flat" (a revision loop or REVISE) | **reharmonize-revise** | reharmonization.md, functional-harmony.md |
| "modal", "dorian", "mixolydian", "vamp", "one-chord groove" | **modal-progression** | modes-scales.md, modal-color.md |
| "smoother", "bass line", "voice leading", "parallel fifths warning" | **voice-leading-pass** | voice-leading.md, functional-harmony.md |
| Supplied chords in `brief.md` `## Supplied input` (TOPLINE), "use my chords" | **topline-transcribe** | functional-harmony.md |

## Task Type Instructions

| Task Type | What the sub-agent does |
|---|---|
| **chords-melody** | Read `structure.md` (key, mode, bpm, time_sig, section labels, bars) and `brief.md`. Write one `[Label]` block per structure section, in order, with one bar per cell, so that a section's cell count equals its `bars` (4/4: 4 chords per 4 bars at one chord per bar, or fewer cells with `%`). Choose a progression per section family: verses settle, pre-choruses lean forward, choruses land and resolve, bridges contrast. Use the genre `## Harmony` progressions as a starting palette, not a script. Keep the diatonic ratio at or above the gate threshold (0.6 default) and end every section on a V-I, IV-I, V-vi, or bVII-I motion. Derive the concert line with `chord_tools.py roman` and `diatonic`, never from memory |
| **reharmonize-revise** | Read the named sections and the critique or gate JSON. Change only the named sections, keep labels and cell counts, keep the key. Use `chord_tools.py reharmonize <key> <chords...> --style <style>` as a source of idiomatic substitutions, then adapt. State each change in the artifact notes |
| **modal-progression** | Build the progression from the modal characteristic chord and a tonic anchor (see modal-color.md). Numerals stay major-scale-relative: a dorian chart reads `i`, `IV`, `bVII`. Keep the structure.md `mode` field truthful |
| **voice-leading-pass** | Re-order inversions only through slash-bass numerals (`I/3`), keep the bass moving by step where the line allows, avoid the parallel-fifth warnings the gate lists. Never change the chord roots unless asked |
| **topline-transcribe** | Copy the supplied progression into `chords.md` unchanged (numerals derived from the stated key, concert line verified), one block per structure section. Do not improve, simplify, or substitute. Record any chord that fails to parse in `FINDINGS` and return BLOCKED |

## Guardrails

- **Gate-visible grammar only.** Header `key: <key> <mode>`, then `[Label]` blocks, `| I | V |` cells, `%` repeats, `> | D | A |` concert lines. See the harmony contract; do not invent columns
- **Numerals are major-scale-relative** with accidentals: minor key reads `i`, `bIII`, `iv`, `v` or `V`, `bVI`, `bVII`. Uppercase major, lowercase minor, `°` diminished, `ø7` half-diminished, `7`, `maj7`, `m7`, `add9`, `sus2`, `sus4`
- **Concert pitch comes from the tool.** Spell every `>` cell from `chord_tools.py`; flats and sharps follow the key (F major has Bb, never A#)
- **Section labels match structure.md exactly**, same order and repeats; every chorus repeat gets its own block
- **Chords are sung under a melody.** Keep harmonic rhythm at one or two chords per bar unless the genre profile says otherwise; a chord change needs a reason (new lyric image, section lift, cadence)
- **Borrowed chords are seasoning.** A few non-diatonic chords per song are fine; the ratio must stay at or above `diatonic_min_ratio`
- **Originality.** No named songs or artists as progression targets; describe the function ("rising pre-chorus into a plagal landing"), not a source
- **Never certify.** Run `chord_tools.py` for early errors; the orchestrator's gate decides
