---
loaded_by: composer
level: L2
last_reviewed: 2026-10-26
---

# Groove

## Role -> Reference Mapping

| Role | Contract | Genre section | Theory / technique files (max 2 total) |
|------|----------|---------------|----------------------------------------|
| **Groove** | `contracts/structure-output.md` | `genres/<genre>.md` `## Rhythm` (tempo, meter, feel) and `## Lyric` form lines | `theory/form-and-meter.md`, `techniques/rhythmic-feel.md`, `theory/modes-scales.md` |

## Detection Keywords

structure, song structure, form, key, mode, tempo, bpm, time signature, meter, bars, section lengths, verse chorus layout, groove, pulse, feel, meter spec, rhyme scheme layout, structure.md

## Task Type Routing Table

| Request Signal | Task Type | References Loaded |
|---|---|---|
| Pipeline Stage 3 (`TASK_TYPE: structure`), "set up the song structure", "form for a <genre> song" | **structure** | form-and-meter.md, rhythmic-feel.md |
| "what key", "which key suits a <range> voice", "mode for this mood", "tempo for", "what bpm" | **tempo-key** | form-and-meter.md, modes-scales.md |
| REWRITE or LYRICS_ONLY with supplied lyric, "work out the meter of my lyric" | **meter-infer** | form-and-meter.md, rhythmic-feel.md |
| TOPLINE or ADAPT_GENRE with supplied chords or source, "derive the form from my chords" | **structure** | form-and-meter.md |

## Task Type Instructions

| Task Type | What the sub-agent does |
|---|---|
| **structure** | Read `brief.md` and `concept.md`. Pick `form_template` from `scripts/data/form-templates.json` names (for example `VCVCBC`) that fits genre, mood, and `target_length_sec`; choose `key`, `mode`, `bpm`, `time_sig` from the genre `## Rhythm` ranges and the brief's mood. Write the header and the table. Section labels must satisfy the template's label patterns, bars must sit inside the template's ranges, and total bars must respect the cap. For each lyric section write a `meter_spec` (`syllables/stress` per line, lines separated by `;`, stress `S`/`u`) that a singer can deliver at the chosen bpm and a `rhyme_scheme` letter string per section; use `x` for unconstrained lines |
| **tempo-key** | Answer or set key and bpm from the vocal range, mood, and genre. Report the reasoning in two sentences (tempo band, key comfort). Prefer keys where the melody sits inside the vocal range with no strain notes. If run standalone, give the options as a short list and name the one you chose |
| **meter-infer** | Count the supplied lyric's syllables and stress per line (dictionary stress), group lines into sections, and write the `meter_spec` strings that reproduce it exactly; infer the `rhyme_scheme` from line endings. Transcribe, never rewrite the user's lyric. Pick bars so each line fits two bars in 4/4 unless the lyric demands otherwise |

## Guardrails

- **Header keys are exact:** `key`, `mode`, `bpm`, `time_sig`, `form_template`, then one table with columns `section | label | bars | meter_spec | rhyme_scheme`
- **Labels come from the allowed set** (`Intro`, `Verse N`, `Pre-Chorus N`, `Chorus`, `Post-Chorus`, `Bridge`, `Instrumental`, `Breakdown`, `Build`, `Drop`, `Tag`, `Outro`, and AABA `A1 A2 B A3`)
- **Downstream roles obey this file.** `harmony` and `melody` copy key, mode, bpm, and time signature from it; a change here invalidates `chords.md`, `melody.abc`, and `arrangement.md`
- **Singable meter.** A line of 7-10 syllables per two 4/4 bars is comfortable; 12 or more per two bars at 130 bpm or faster needs a wider section. The hook line stays within the hook syllable limit (default 12)
- **INSTRUMENTAL** leaves `meter_spec` and `rhyme_scheme` columns empty; **JINGLE** uses the `jingle` template and a hard length cap
- **Mode names are spelled in full** (`major`, `minor`, `dorian`, `mixolydian`, ...); `key` is a tonic with accidental (`Bb`, `F#`), never a mode word
- **Originality.** Choose form and tempo from genre, era, and mood language, never "like <named song>"
- **Never certify.** Run `structure_check.py` for early errors; the orchestrator's gate decides
