---
loaded_by: lyricist
level: L2
last_reviewed: 2026-10-26
---

# Augmenter

## Role -> Reference Mapping

| Role | Reference Files |
|------|----------------|
| **Augmenter** | contracts/augment-output.md; techniques/section-roles.md, techniques/prosody-and-stress.md (or rhyme-schemes.md); ONE genre `## Lyric` section |

Allowance (`prompt-allowances.json`): 1 genre, 2 techniques. Single dispatch at Stage 4 for AUGMENT_LYRICS; no critic loop. Gates: `prosody_check.py` and `rhyme_check.py` scoped to the new sections, plus `cliche_scan.py`.

## Detection Keywords

add a verse, write a bridge for my song, extend, one more chorus, more verses in the same voice, pre-chorus for this, continue my lyric, another verse

## Task Type Routing Table

| Request Signal | Task Type | References Loaded |
|---|---|---|
| "add a verse", "more verses in the same voice", "extend" with a supplied lyric | **lyric-augment** | augment-output.md, section-roles.md, prosody-and-stress.md |
| "write a bridge", "pre-chorus for this", "one more chorus" | **lyric-augment** | augment-output.md, section-roles.md, prosody-and-stress.md |
| the source rhymes in a scheme the new section must copy, or a rhyme gate FAIL | **lyric-augment** | augment-output.md, section-roles.md, rhyme-schemes.md |

Genre: use `target_genre` if the brief gives one, else the source genre. Paste only its `## Lyric` section.

## Task Type Instructions

| Task Type | What the sub-agent does |
|---|---|
| **lyric-augment** | 1. Check provenance in `brief.md` (`user_asserts_original_input` or `public_domain` with source). If missing, return `BLOCKED`. If you recognise the supplied text as a well-known lyric, stop and report it (clause 4); write nothing. 2. Read the supplied lyric and `structure.md`. Record its section order, per-section `meter_spec`, rhyme scheme, POV, tense, recurring images and diction register. 3. Decide which new sections are requested (verse N, pre-chorus, bridge, extra chorus); the task paragraph lists them. 4. Write ONLY the new sections. Each new section copies the meter and rhyme of the matching source section (a new verse copies the nearest verse; a bridge or pre-chorus copies the modal line pattern of the verses unless `structure.md` gives its own spec). Use the genre's `## Lyric` norms; if the target genre differs from the source, shift diction, imagery and line length toward it and note each shift in `Added:`, but keep POV, tense and voice. 5. Preserve every original line verbatim, in order, unless the user asked for edits. 6. Output per `augment-output.md`: full lyrics, new sections marked `# <!-- new -->` under their tag, and the trailing `## Augmentation` block with `Kept:`, `Added:`, `Meter check:`, `Rhyme check:`. 7. Self-check with `prosody_check.py`, `rhyme_check.py`, `cliche_scan.py` |

Echo a recurring image from the source in the new section, then move it forward; do not restate source lines.

## Guardrails

- **Verbatim source**: never alter, reorder, or re-punctuate an original line unless the user asked; the output is checked for the source lines in order.
- **Only new material is yours**: do not edit the source sections, even to fix a gate violation in them; report it.
- **Match, do not improve**: copy the source's meter and rhyme scheme even when you would choose another.
- **Provenance and clause 4**: refuse unprovenanced text; never continue a recognised well-known lyric; the refusal sentence is in SKILL.md.
- **Allowance**: one genre section, two techniques; no extra files.
- **No artist or song names**, and no quoted existing lyrics in `Added:` notes.
- **Markers stay gate-safe**: marker and `## Augmentation` lines start with `#`.
