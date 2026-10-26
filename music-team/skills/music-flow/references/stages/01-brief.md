---
loaded_by: music-flow
level: L2
last_reviewed: 2026-10-26
---

# Stage 1: Brief

Routing data: `stages.yml` key `01-brief`. Matrix column 1 is `F` for every type except `REVISE` (`-`)
and `PARODY_ADAPT` (refused).

## Purpose

Detect the song type, collect the missing brief keys, record provenance, and write `brief.md`.
Runs inline through the `music-brief` skill (`Skill` tool), not an `Agent` dispatch. The
orchestrator does not infer brief content itself; it passes the user's raw request to the skill.

## Inputs and outputs

| In | Out |
|----|-----|
| user request text; `.song/config.yml` (created by `music-brief` from `.song.config.yml.example` when absent); `.song/active` | `.song/<slug>/brief.md`; `.song/active` (written by the orchestrator after the slug is known); declaration line `Type: <T> | Genre: <g> | Provenance: <p> | Brief: <path>` |

## Sub-flow

1. Invoke `music-brief` with the request. It returns the declaration line, or an inline refusal.
2. On refusal (`PARODY_ADAPT`, or ADAPT_GENRE / AUGMENT_LYRICS without provenance): relay the
   sentence verbatim, create no `.song/<slug>/` directory, do not write `.song/active`, stop.
3. Read the declaration. Apply `routing.force_type` when set: detection still runs and is logged,
   routing uses the pin, announce `FORCED TYPE: <pin> (detected: <T>)` every run. `REVISE` is
   never forced.
4. Create `.song/<slug>/`; write `.song/active` (slug only, one line); write initial `state.json`
   with `stage: 1`, `song_type`, `status: "in_progress"`, `quick`, zeroed `loops_used`, empty
   `gates`, `gate_overrides`, `accepted_best`, `owners: {"brief.md": "music-brief"}`, `started`,
   `updated`, and a new `run_id` (`<UTC timestamp>-<slug>`).
5. Brief validation (no script): `theme` non-empty, `song_type` set, `language` set. Anything
   missing sends the user back to `music-brief` once; a second miss asks the user directly.

## Gates, critic, loops

None. `loops.*` does not apply. The only retry is the single re-ask in step 5.

## Per-type variations

| Type | Cell | Behaviour |
|------|------|-----------|
| FULL_SONG, LYRICS_ONLY, INSTRUMENTAL, JINGLE | F | Standard intake |
| TOPLINE, REWRITE | F | Provenance `user_asserts_original_input: true` required; supplied chords or lyric stored under `## Supplied input` |
| ADAPT_GENRE | F | Also `source_genre`, `target_genre`; provenance `user_asserts_original_input` or `public_domain` + `public_domain_source` |
| AUGMENT_LYRICS | F | Provenance as ADAPT_GENRE; `target_genre` optional |
| THEORY | F | No `brief.md`, no directory, no `.song/active` unless the user asks to save. Dispatch `composer` role `theorist` (Template 1, no genre, up to 3 technique files) and relay the answer; stop. The hand-back is the 4-line block then an `ANSWER:` block (`composer/references/contracts/theory-output.md`): show everything under `ANSWER:` to the user unchanged, written to a file only on request |
| REVISE | - | `music-brief` is skipped. Read `state.json`, apply the re-entry rules in `references/shared/song-types.md`, new `run_id`, continue at the re-entry stage |
| PARODY_ADAPT | refused | Never reaches this stage's file writes |

## state.json after this stage

`stage: 2` (or the first non-skipped stage), `updated`, `owners["brief.md"]`.
