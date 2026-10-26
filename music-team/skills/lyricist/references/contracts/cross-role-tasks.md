---
loaded_by: lyricist
level: L2
last_reviewed: 2026-10-26
---

# Cross-Role Tasks

Lyricist roles run as separate sub-agents, one `Agent` call per role. Never put two `ROLE:` lines in one prompt. This file defines the chains and hand-offs the orchestrator (or a standalone user) follows.

## Chains

| Chain | Roles in order | Artifacts | Gate run |
|-------|----------------|-----------|----------|
| Stage 2 concept | `hook-writer` | `concept.md` | `cliche_scan.py`, `prosody_check.py --hook` after the role |
| Stage 4 lyrics (FULL_SONG, LYRICS_ONLY, TOPLINE, JINGLE) | `verse-writer` then `lyric-editor` | `lyrics.md` (edited in place) | Once, after the last role |
| Stage 4 REWRITE | `lyric-editor` only | `lyrics.md` from the supplied input | Once |
| Stage 4 AUGMENT_LYRICS | `augmenter` only | `lyrics.md` with `# <!-- new -->` markers | Scoped to new sections, plus `cliche_scan.py` |
| REVISE (lyrics) | `lyric-editor` scoped to named sections | `lyrics.md` | Once, then `structure_check.py --consistency` |
| Gate FAIL loop | critic (`prosody-judge`), then `lyric-editor` (`verse-writer` only if sections are missing) | `lyrics.md` | After each loop |

## Hand-off rules

- The second role reads the first role's artifact by path; the first role's reasoning is not passed.
- `verse-writer` leaves `lyrics.md` complete and gate-attempted; `lyric-editor` improves it and may not drop a section or change a tag.
- The last writer is recorded as the artifact owner (`state.json.owners["lyrics.md"]`).
- The `hook_line` from `concept.md` is read-only for every Stage 4 role.
- Standalone (no pipeline): the user plays orchestrator. Run the roles in the order above, one at a time, passing the earlier file path.

## Scoping a REVISE

The prompt lists the section labels to change. The editor copies every other section byte for byte and lists them under `# Unchanged:`. If a requested change breaks a `structure.md` constraint, report it; do not edit `structure.md`.

## Provenance

`augmenter` and `lyric-editor` on user-supplied text need `user_asserts_original_input: true` or `public_domain: true` with `public_domain_source`. The first role to find it missing returns `BLOCKED` with that reason; the chain stops.

## Failure handling

| Event | Action |
|-------|--------|
| Role returns `BLOCKED` | Chain stops; the orchestrator counts a failed attempt |
| Reply lacks `STATUS:` | Re-dispatch once, then treat as `BLOCKED` |
| Reply lacks `SKILL_LOADED:` | Warning only |
