---
loaded_by: music-memory
level: L2
last_reviewed: 2026-10-26
---

# Output Contract: retrospective.md and memory lessons

Artifact: `.song/<slug>/retrospective.md`, written by `music-memory` at Stage 7d. Grammar source of truth for the
front-matter: `references/shared/artifact-formats.md`, section `retrospective.md`. Never contains lyric text.

## Grammar

```markdown
---
run_id: 2026-10-26T14-02-11Z-nobody-knows
slug: nobody-knows-my-name-here
genre: pop
song_type: FULL_SONG
date: 2026-10-26
---

# Retrospective

## Loops
- concept 1, structure 0, lyrics 2, music 0, arrangement 0, release 1

## Most-failed gate
- prosody_check (lyrics): 2 FAILs; worst metric verse_2_mismatch_ratio 0.22

## Recurring critique
- stress alignment on Verse 2 line endings (rubric: stress alignment), seen in 2 critiques

## Overrides
- none

## Next time
- Give the verse-writer the syllable budget per line before drafting.
- Run the cliche scan on the concept before Stage 4.
- Keep bridge energy one step above the last chorus.
```

## Rules

1. **Front-matter.** `run_id` copied exactly from `state.json.run_id`; `slug` equals the directory name; `genre`, `song_type` from the brief; `date` is the run date, ISO.
2. **Loops.** One bullet, the six `loops_used` counters in that order.
3. **Most-failed gate.** The gate with the most FAIL events across `decisions.md` and critiques; `none` when every gate passed first time. Name script, stage, and the worst metric with its value.
4. **Recurring critique.** At most three bullets, each naming a rubric criterion and a section label, with the count of critiques that raised it. No quoted words from the song.
5. **Overrides.** One bullet per `gate_overrides` entry (stage and reason in six words or fewer), or `none`. Include `accepted_best` stages.
6. **Next time.** Exactly three bullets, imperative, reusable on another song.
7. **Whole file under 60 lines.** No artist or song names; no phrase from any lyric.

## Lesson lines (`<memory.path>/index.md`)

```text
lyrics | pop | Give the verse-writer a syllable budget per line before drafting.
* | * | Rank fixes by gate impact so loop 2 changes the failing metric first.
```

| Rule | Detail |
|------|--------|
| Shape | `stage-or-role | genre | lesson`, pipes with single spaces, one line each |
| `stage-or-role` | `concept`, `structure`, `lyrics`, `music`, `arrangement`, `release`, or a role name |
| `genre` | A genre label from `references/shared/genres/`, or `*` |
| `lesson` | One imperative sentence, 160 characters or fewer, no pipe character, no lyric text |
| Per run | At most three lines appended |
| Dedupe | Compare lower-cased, whitespace-collapsed lines; skip exact repeats and same-meaning repeats for the same key |
| Cap | 200 lines; trim from the top |

## Hand-back

`ARTIFACT:` the path of `retrospective.md`. `SUMMARY:` one sentence, 200 characters or fewer, giving the count of lessons
appended and skipped. Report BLOCKED with `FINDINGS:` only when `state.json` is unreadable.
