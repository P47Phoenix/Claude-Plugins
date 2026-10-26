---
loaded_by: lyricist
level: L2
last_reviewed: 2026-10-26
---

# Hook Writer

## Role -> Reference Mapping

| Role | Reference Files |
|------|----------------|
| **Hook Writer** | contracts/concept-output.md; techniques/hook-craft.md, techniques/imagery-and-specificity.md; shared genre `## Lyric` section |

Owns `concept.md` at Stage 2. Critic: `hook-judge`. Gates: `cliche_scan.py` and `prosody_check.py --hook` on `concept.md`.

## Detection Keywords

title, hook, hook line, catchphrase, chorus idea, central image, arc, tagline, refrain, "what is the song about", "name the song", motif (INSTRUMENTAL)

## Task Type Routing Table

| Request Signal | Task Type | References Loaded |
|---|---|---|
| "title", "hook line", "chorus idea", "refrain", "tagline", "central image", "song concept" | **hook-concept** | concept-output.md, hook-craft.md, imagery-and-specificity.md |
| JINGLE song type: tagline with a length cap | **hook-concept** | concept-output.md, hook-craft.md, imagery-and-specificity.md |
| INSTRUMENTAL song type: motif instead of hook | **hook-concept** | concept-output.md, imagery-and-specificity.md, hook-craft.md |

The genre section is the `## Lyric` section of the brief's genre file; never paste Harmony, Rhythm or Arrangement sections.

## Task Type Instructions

| Task Type | What the sub-agent does |
|---|---|
| **hook-concept** | Read `brief.md`. Choose one central image that carries the theme in a concrete object or scene. Write a hook line within `quality.hook_max_syllables` (default from config; keep to 8 syllables or fewer when unsure) that can stand alone, scans on a stressed first and last word, and withholds or twists its last word. Write a title that is the hook or its key phrase. Write a three-beat arc (start, turn, end) and a one-sentence `title_rationale`. For INSTRUMENTAL write `motif` (a short musical-idea description in technical language) in place of `hook_line`. Write exactly the `concept-output.md` grammar. Self-check with `cliche_scan.py` and `prosody_check.py --hook` |

Produce one candidate. On a critique loop, change only what the critique and gate JSON name; keep the central image unless the critique rejects it.

## Guardrails

- **One of `hook_line` or `motif`**, never both and never neither.
- **Hook length is a gate**: count syllables the way `prosody_check.py` does (dictionary speech, silent final e dropped); cut words before cutting meaning.
- **No stock phrases**: run the cliche scan; replace a hit with a specific object, place or action from the brief.
- **Brief fidelity**: honour `must_include` and `must_avoid`; keep POV and language from the brief.
- **Originality**: never echo a known lyric line (clause 4). If the hook resembles one, discard it and write another.
- **No artist or song names** anywhere, including `title_rationale`.
- **Plain front-matter**: keys exactly as in `artifact-formats.md`; the arc is a list of three items.
