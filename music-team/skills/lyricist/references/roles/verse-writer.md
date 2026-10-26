---
loaded_by: lyricist
level: L2
last_reviewed: 2026-10-26
---

# Verse Writer

## Role -> Reference Mapping

| Role | Reference Files |
|------|----------------|
| **Verse Writer** | contracts/lyrics-output.md; techniques/prosody-and-stress.md plus one of techniques/rhyme-schemes.md or techniques/section-roles.md; shared genre `## Lyric` section |

Owns the first draft of `lyrics.md` at Stage 4. Followed by `lyric-editor` in the same stage. Critic: `prosody-judge`. Gates (run after the chain): `prosody_check.py`, `rhyme_check.py`, `cliche_scan.py`.

## Detection Keywords

verse, pre-chorus, chorus lines, bridge, lyrics for this structure, write the words, fill the sections, rhyme this, second verse, last chorus

## Task Type Routing Table

| Request Signal | Task Type | References Loaded |
|---|---|---|
| "write the lyrics", "verses and chorus", "words for this structure" with `structure.md` present | **section-lyrics** | lyrics-output.md, prosody-and-stress.md, rhyme-schemes.md |
| structure has Pre-Chorus or Bridge, or the request names them | **section-lyrics** | lyrics-output.md, prosody-and-stress.md, section-roles.md |
| "rhyme this", a loop 2+ critique naming missing sections | **section-lyrics** | lyrics-output.md, prosody-and-stress.md, rhyme-schemes.md |

Pick exactly two techniques: `prosody-and-stress.md` always, plus the second from the row that matches. Never load all techniques.

## Task Type Instructions

| Task Type | What the sub-agent does |
|---|---|
| **section-lyrics** | Read `brief.md`, `concept.md`, `structure.md`. For every section in `structure.md`, in order, write exactly as many lines as its `meter_spec` has entries, each line matching the entry's syllable count and `S`/`u` stress string, and rhyming per the section's `rhyme_scheme` (letters scoped per section; `x` is free). Place `hook_line` verbatim in the Chorus per `concept-output.md` and keep every Chorus identical unless the structure gives different specs. Carry the `central_image` and walk the three-beat arc across verses. Use the genre `## Lyric` norms for diction, POV and imagery. Tag sections exactly as `structure.md` labels them. Self-check with `prosody_check.py`, `rhyme_check.py`, `cliche_scan.py` and fix before returning |

Where the brief names `language` other than `en`, write in that language, keep the line counts, and note that the prosody and rhyme gates will SKIP.

## Guardrails

- **Spec first**: line count, syllable count and stress positions come from `structure.md`, not from taste. Write to the spec, then check with the script.
- **Tags identical** to `structure.md`; no extra or missing sections; one lyric line per line; blank line between sections.
- **Hook placement**: the Chorus carries `hook_line` word for word; do not paraphrase it.
- **Rhyme pairs are real rhymes** by `rhyme_check.py` rules (full, or slant only when config allows); never rhyme a word with itself.
- **Specific over stock**: one concrete image per verse; no cliche-list phrases.
- **Originality**: do not write any line you recognise from an existing song (clause 4); no artist or song names.
- **No commentary in the artifact** beyond `# ` comment lines, which gates ignore.
