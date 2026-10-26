---
loaded_by: song-flow
level: L2
last_reviewed: 2026-10-26
---

# Package formats, thin slice (Stage 7-light, LYRICS_ONLY)

Until `song-release` lands (W4-3), `song-flow` assembles `package/` itself. Assembling a
package copies finished artifacts; it writes no new lyric, hook, or chord, so principle 1
holds. W4-3 moves this work into `song-release` and this file is then deleted.

## `package/lyric-sheet.md`

Line 1: `# <title>` where `<title>` is the `title` value from `concept.md` front-matter.
Line 2: blank. Then the body of `lyrics.md` copied byte-for-byte, including `[Label]` tags
and blank lines between sections, with every `# ` comment line removed. No front-matter,
no credits, no hook line restated (it is already in the chorus).

Example: `# Half the Island Looks Away` / blank / `[Verse 1]` / `The ferry leaves at half past four` / ...

## `package/release-notes.md`

```markdown
---
run_id: <state.json.run_id>
slug: <slug>
song_type: LYRICS_ONLY
quick: <true|false>
---

# Release notes

## Gates
| stage | script | status | skipped | key metric |
|-------|--------|--------|---------|------------|
| 2 | cliche_scan | PASS | false | per_100_words 0.0 |
| 2 | prosody_check --hook | PASS | false | hook_syllables 7 |
| 3 | structure_check | PASS | false | sections 6 |
| 4 | prosody_check | PASS | false | worst ratio 0.125 |
| 4 | rhyme_check | PASS | false | pairs_checked 12 |
| 4 | cliche_scan | PASS | false | per_100_words 0.0 |
| 4 | structure_check | PASS | false | sections 6 |
| 7 | challenge_gate | not run (W3-4) | - | - |

## Loops used
| stage | used | cap |
|-------|------|-----|
| concept | 0 | 3 |
| structure | 0 | 2 |
| lyrics | 1 | 4 |

## Overrides and accept_best
(none)   <- or one line per `gate_overrides[]` entry and per `accepted_best` key
```

Gate rows: one per key of `state.json.gates[<stage>].results`, the `script` cell being the
invocation string from `scripts` (`prosody_check --hook` at Stage 2); `status` and
`skipped` come from that script's own result. The `challenge_gate` row is fixed text in
Wave 2: no `gates.release` entry exists, so nothing is read for it. Loop rows: one per key
of `loops_used` in file order; `cap` is the effective cap (`loops.<stage>` from config, or
1 in quick mode), never a hard-coded number. `key metric` is the one `metrics` value that
best explains the result; the full JSON stays in `state.json.gates`. Every row comes from
`state.json`; nothing is recomputed.
