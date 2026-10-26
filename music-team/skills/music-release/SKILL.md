---
name: music-release
description: Song release skill that assembles the final package (lyric sheet, lead sheet, MIDI export, one-pager, release notes) from the .song/<slug>/ artifacts after the challenger passes. Runs inline at Stage 7c through the Skill tool. Triggers on phrases like "export the song", "finalize the song", "song package", "lead sheet", "release notes", "export MIDI", "package my song".
license: Apache License 2.0 - See repository LICENSE file
model_awareness: opus-4-7
last_audited: 2026-10-26
pattern_library_version: 4-7-1
model: sonnet
tier: C
maintainer: music-team-leads
fitness_review_due: 2027-01-24
context_budget: 200
allowed-tools: [Read, Write, Edit, Bash, Agent, Skill]
---

# Music Release

Stage 7c. Inline skill (no sub-agent): it copies, formats and summarises artifacts that already passed their gates. It
writes no new lyric, chord or note, and edits no source artifact. Layout and grammar live in
`references/contracts/package-output.md`; the type matrix and loop rules are in `music-flow/references/stages/07-release.md`.

## Phase 1: Preconditions

1. Resolve the song directory: `.song/active` names the slug; the directory is `.song/<slug>/`. Standalone with no `.song/active`, ask which directory holds the artifacts, or use the current one.
2. Read `state.json` for `song_type`, `run_id`, `loops_used`, `gates`, `gate_overrides`, `accepted_best`. Missing `state.json` (standalone): note "no gate history" in `release-notes.md` and continue.
3. Release starts only after 7b passed: `gates.release` is PASS or SKIPPED, or `challenge-report.md` has no BLOCKER row. Otherwise stop and say `NOT RELEASABLE: BLOCKER rows remain`; package nothing.
4. Read `brief.md` front-matter for title, genre and language.

## Phase 2: Package by type

| Type | Files written to `package/` |
|------|-----------------------------|
| FULL_SONG, JINGLE, REVISE | `lyric-sheet.md`, `lead-sheet.abc`, `song.mid`, `one-pager.md`, `release-notes.md` |
| INSTRUMENTAL | `lead-sheet.abc`, `song.mid`, `one-pager.md`, `release-notes.md` (no lyric sheet) |
| ADAPT_GENRE | the full set plus a copy of `adaptation-report.md` |
| TOPLINE | `lyric-sheet.md`, `lead-sheet.abc`, `song.mid`, `release-notes.md` |
| LYRICS_ONLY, REWRITE | `lyric-sheet.md`, `release-notes.md` |
| AUGMENT_LYRICS | `lyric-sheet.md` (the whole augmented lyric), `new-sections.md` (only the added sections), `release-notes.md` |
| THEORY, PARODY_ADAPT | nothing (not released) |

Write each file per `references/contracts/package-output.md`. Create `package/` first (`mkdir -p`). Never write outside it.

### MIDI export

For every type with `chords.md` or `melody.abc`, run from the song directory:

```bash
python3 -I <plugin>/scripts/midi_export.py --out package/song.mid --chords chords.md --melody melody.abc --structure structure.md
python3 -I <plugin>/scripts/midi_export.py --check --chords chords.md --melody melody.abc --structure structure.md
```

Omit `--chords` or `--melody` when that file is absent. Exit 0 means written; the second command is the round-trip check on the same inputs (exit 0 PASS, 1 FAIL). Exit 3 (unreadable input) means omit `song.mid` and record `midi: omitted (unreadable input)` in `release-notes.md`. Non-zero `metrics.warnings` is noted, not fatal.

## Phase 3: Hand-back

Run the listing below and fix any missing expected file, then reply.

```bash
ls -1 package/
```

```text
SKILL_LOADED: <paths of references/ files read>
STATUS: DONE | BLOCKED
ARTIFACT: <dir>/package/
SUMMARY: <one sentence, max 200 characters; files written and panel majority>
```

BLOCKED lists the reason after `FINDINGS:`. Set no `state.json` field: `music-flow` sets `status: "complete"` after Stage 7d.

## Guardrails

- **Copy, do not compose.** The lyric sheet is `lyrics.md` text reformatted, byte-for-byte per line. No new lines, no edits.
- **No artist or song names**, no "sounds like", in any file, including `one-pager.md`.
- **Overrides and accepted-best are disclosed** in `release-notes.md`; never hide them.
- **The panel is advisory.** Report its majority and top notes; never present it as a gate.
- **Language and encoding**: UTF-8, LF line endings.

## User Commands

| Command | Action |
|---|---|
| `package` | Assemble the full package for the current song |
| `lead sheet` | Write only `lead-sheet.abc` |
| `midi` | Run only the MIDI export and check |
| `notes` | Rewrite `release-notes.md` from current `state.json` |

## References

- `references/contracts/package-output.md` -- file layout, lead-sheet chord rule, one-pager and release-notes grammar
