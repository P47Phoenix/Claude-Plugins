---
loaded_by: adapter
level: L2
last_reviewed: 2026-10-26
---

# Music Adapter

## Role -> Reference Mapping

| Role | Reference Files |
|------|----------------|
| **Music adapter** | contracts/music-adapt-output.md, contracts/arrangement-adapt-output.md, contracts/adaptation-report.md, techniques/feel-conversion.md, techniques/reharmonization-moves.md |

Genre files are not listed here: the orchestrator pastes `source_genre` and `target_genre`
(Identity, Harmony, Rhythm, Arrangement; the target also Adaptation notes). Two genre files, at most two techniques.

## Detection Keywords

chords, chord chart, progression, harmony, reharmonize, key, mode, melody, contour, tempo, bpm, feel, groove, time signature, meter, arrangement, instrumentation, texture, energy, form, section order, production

## Task Type Routing Table

| Request Signal | Task Type | References Loaded |
|---|---|---|
| Stage 5 dispatch; "reharmonize for <genre>", "convert these chords to <genre>", chords or melody supplied | **music-adapt** | contracts/music-adapt-output.md, techniques/reharmonization-moves.md, techniques/feel-conversion.md |
| Stage 6 dispatch; "re-instrument", "change the arrangement to <genre>", arrangement notes supplied | **arrangement-adapt** | contracts/arrangement-adapt-output.md, techniques/feel-conversion.md |
| Stage 7p dispatch; "what would change if this were <genre>" | **adaptation-report** | contracts/adaptation-report.md |

## Task Type Instructions

| Task Type | What the sub-agent does |
|---|---|
| **music-adapt** | Re-voice the supplied chords (and re-contour the melody only if one is supplied) for `target_genre`; write `chords.md` (and `melody.abc`) with a notes block in `chords.md` |
| **arrangement-adapt** | Re-target instrumentation, texture and the energy curve for `target_genre`; write `arrangement.md` with a notes block |
| **adaptation-report** | Read the notes blocks of `lyrics.md`, `chords.md`, `arrangement.md`, then write `adaptation-report.md` per the contract |

### Procedure for music-adapt and arrangement-adapt

1. **Analyze the source.** Per section: key and mode, time signature, bpm, chord functions as roman numerals, cadence,
   rhythmic feel, melody contour (rising, arching, stepwise, leaping), and phrase length in bars.
2. **Keep identity.** Mark as untouchable: the key centre and mode (unless the target profile makes it impossible),
   the cadence at each section end, the hook's melodic contour, section order, and the energy shape (which
   section is quietest, which loudest).
3. **Remap style.** Using the target `## Adaptation notes`, `## Harmony`, `## Rhythm`, `## Arrangement`:
   - time signature and tempo into the target band (techniques/feel-conversion.md);
   - harmony by roman-numeral moves, never by new keys (techniques/reharmonization-moves.md);
   - instrumentation, texture and per-section energy to the target profile's arrangement arc.
4. **Protect the melody.** If a melody is supplied, keep its pitch contour and rhythmic anchors; shift rhythm onto the
   target feel by re-timing, not re-composing. Every melody note on a strong beat must still belong to its chord.
5. **Stay in range.** Keep `chords.md` diatonic ratio and melody leaps inside the config thresholds; use at most
   40 percent chromatic or borrowed chords per section.
6. **Write the notes block.** Append `## Adaptation notes` to the artifact as the contract specifies. Record melody
   changes in the `chords.md` block (`melody.abc` carries no notes block).
7. **Count.** Stay within `adaptation.max_changed_elements`: one Changed entry per element family (for example "chord
   colour", not one per bar).

## Guardrails

- **Provenance first** -- build only on input that `brief.md` marks `user_asserts_original_input: true` or `public_domain: true`
- **Identity before style** -- if a requested style change would break the hook contour or the section cadence, keep identity and log the style change as not applied under Risks
- **Never reproduce a progression-plus-melody pair you recognise from an existing song** (clause 4); generic progressions are fine
- **No artist, band or song names** in any artifact, note or production field; describe sound with tempo, key, texture, dynamics
- **Match the header** -- `key`, `mode`, `bpm`, `time_sig` in `chords.md`/`arrangement.md`/`melody.abc` equal `structure.md`; if the adaptation requires a different value, return `BLOCKED` with `FINDINGS` so the orchestrator updates Stage 3
- **No new sections** -- adapt the sections that exist; extensions belong to the AUGMENT_LYRICS path
- **Do not edit `lyrics.md`** -- lyric changes belong to the lyric-adapter
