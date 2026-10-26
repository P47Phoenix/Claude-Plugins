---
loaded_by: adapter
level: L2
last_reviewed: 2026-10-26
---

# Lyric Adapter

## Role -> Reference Mapping

| Role | Reference Files |
|------|----------------|
| **Lyric adapter** | contracts/lyric-adapt-output.md (and contracts/adaptation-report.md for task `adaptation-report`), techniques/lyric-refit.md, techniques/feel-conversion.md |

Genre files are not listed here: the orchestrator pastes `source_genre` (Identity, Lyric) and
`target_genre` (Identity, Lyric, Adaptation notes). Two genre files, at most two techniques.

## Detection Keywords

lyric, lyrics, words, verse, chorus, bridge, refrain, line, syllable, stress, meter, rhyme, scheme, diction, register, imagery, point of view, re-fit, fit to the melody, shorten, singable, phrasing

## Task Type Routing Table

| Request Signal | Task Type | References Loaded |
|---|---|---|
| Stage 4 dispatch; "adapt my lyric to <genre>", "re-fit these lyrics to", "make the words fit a <genre> groove" | **lyric-adapt** | contracts/lyric-adapt-output.md, techniques/lyric-refit.md, techniques/feel-conversion.md |
| Stage 7p dispatch or "what would change if this were <genre>" with only a lyric supplied | **adaptation-report** | contracts/adaptation-report.md, techniques/lyric-refit.md |

## Task Type Instructions

| Task Type | What the sub-agent does |
|---|---|
| **lyric-adapt** | Adapt the supplied lyric to the meter and rhyme already set in `structure.md`, and to the diction of `target_genre`; write `lyrics.md` with a trailing `## Adaptation notes` block |
| **adaptation-report** | Consolidate the notes blocks of the supplied artifacts into `adaptation-report.md` per the contract; only used when no music-adapter run exists |

### Procedure for lyric-adapt

1. **Analyze the source.** Read `## Supplied input` in `brief.md`. Record per section: line count, syllables per line,
   stress shape, rhyme scheme, point of view, tense, the 3-5 key images, and the hook line (usually the refrain or title).
2. **Keep identity.** Mark as untouchable: the hook idea and title, the meaning of every line, the point of view, the key
   images, and section order. A refrain line stays verbatim unless its syllable count makes the target meter impossible;
   then change the fewest words and log it.
3. **Remap style.** Using the target `## Adaptation notes` and `## Lyric`: line length band, stress shape, rhyme habit,
   diction register (plain, colloquial, poetic), and how the hook is placed. Concrete images may be swapped for a
   near-synonym; they may not be swapped for a different image.
4. **Re-fit to the meter.** Fit each line to the `meter_spec` of its section in `structure.md` (techniques/lyric-refit.md):
   cut or add function words and adjectives first, then re-order, and only then substitute words. Never add a fact, a
   person, a place or a feeling that the source line lacks.
5. **Check the rhyme.** Keep the source scheme when the target profile allows it; otherwise move to the profile's
   scheme and log it. Slant rhyme is allowed where `slant_rhyme_allowed` is true.
6. **Write the notes block.** Append `## Adaptation notes` (Kept / Changed / Risks) as the contract specifies.
7. **Count.** Stay within `adaptation.max_changed_elements`: group related line edits into one Changed entry per section.

## Guardrails

- **Provenance first** -- build only on input that `brief.md` marks `user_asserts_original_input: true` or `public_domain: true`
- **Meaning is frozen** -- re-fit changes syllables and stress, never ideas; if a line cannot fit without new meaning, return `BLOCKED` with the line in `FINDINGS`
- **Never introduce a line from any existing song** -- if a candidate line feels familiar, discard it (clause 4)
- **No artist, band or song names** anywhere in the artifact or notes; describe genre, era, tempo and texture only
- **Do not edit `structure.md`** -- meter conflicts are reported, not fixed here
- **Quote only the user's supplied lines** in the notes block, and only what is needed to identify the change
- **One hook** -- the adapted lyric keeps exactly the source hook idea; do not invent a second
