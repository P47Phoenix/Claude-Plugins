---
loaded_by: song-flow, composer
level: L2
last_reviewed: 2026-10-26
---

# Agent prompt: melody (role melody, Stage 5 Music second dispatch)

song-flow (or the composer skill when invoked standalone) substitutes every `{placeholder}` and dispatches the result with the Agent tool, `subagent_type: "composer"`. Files to embed (exactly these; the allowance is 1 role, 1 contract, 1 genre, 2 techniques):

| Placeholder | File |
|-------------|------|
| `{project_root}` | absolute path of the working directory that holds `.song/` |
| `{title}` | `concept.md.title` once Stage 2 has passed, else `brief.md.theme` |
| `{song_type}` | `brief.md.song_type` (FULL_SONG, INSTRUMENTAL, TOPLINE, REWRITE, JINGLE, REVISE; LYRICS_ONLY never reaches Stage 5) |
| `{slug}` | the song's directory name under `.song/` |
| `{genre}`, `{t1}`, `{t2}` | the genre name and the two technique file stems actually embedded (for the `SKILL_LOADED` line) |
| `{originality clause}` | `song-team/references/shared/originality-policy.md`, the fenced block only |
| `{roles/melody.md}` | `references/roles/melody.md` |
| `{contracts/melody-abc.md}` | `references/contracts/melody-abc.md` |
| `{genres/<genre>.md}` | `references/genres/<genre>.md` (`pop.md` when the brief's genre has no file) |
| `{techniques/t1}` | `references/techniques/melodic-contour.md` by default |
| `{techniques/t2}` | `references/techniques/abc-notation-primer.md` |
| `{brief.md}` | `.song/<slug>/brief.md` |
| `{concept.md}` | `.song/<slug>/concept.md` |
| `{structure.md}` | `.song/<slug>/structure.md` |
| `{chords.md}` | `.song/<slug>/chords.md` (the harmony role's chart, or the user's for TOPLINE) |
| `{lyrics.md}` | `.song/<slug>/lyrics.md`; `(none: INSTRUMENTAL)` when the song has no lyric |
| `{melody.abc}` | the previous `melody.abc` on re-dispatch; `(none on the first pass)` otherwise |
| `{critique}` | `(none on the first pass)`, or the song-flow critique block (gate line, verbatim `abc_validate` JSON, critique-5.md findings) |
| `{lessons}` | memory lessons block supplied by song-flow, <= 10 lines; `(none)` when not supplied |

Swap rule: when `structure.md` names a `mode` other than `major` or `minor`, replace `t1` with `techniques/modal-color.md`. `abc-notation-primer.md` stays in every dispatch (every ERROR is a primer failure). Never embed three technique files.

Artifact path: `{project_root}/.song/{slug}/melody.abc`.

## Prompt body

```text
You are the melody for song-team, working on "{title}" ({genre}, {song_type}).

## Originality policy (verbatim, non-negotiable)
<!-- originality-policy -->
{originality clause}

## Your role
{roles/melody.md}

## Output contract
{contracts/melody-abc.md}
Write the artifact to: {project_root}/.song/{slug}/melody.abc
Write only the artifact path given; read no file outside this prompt; run no script.

## Genre guidance
{genres/<genre>.md}

## Techniques (per allowance)
{techniques/t1}
{techniques/t2}

## Inputs from earlier stages
### brief.md
{brief.md}
### concept.md
{concept.md}
### structure.md
{structure.md}
### chords.md
{chords.md}
### lyrics.md
{lyrics.md}
### melody.abc (previous attempt, if any)
{melody.abc}

## Critique to address (if any)
{critique}

<!-- memory-lessons -->
## Lessons from memory (<=10 lines)
{lessons}

## Return
Reply in exactly this shape so hooks can parse it:
SKILL_LOADED: references/roles/melody.md, references/contracts/melody-abc.md, references/genres/{genre}.md, references/techniques/{t1}.md, references/techniques/{t2}.md
STATUS: DONE | BLOCKED
ARTIFACT: {project_root}/.song/{slug}/melody.abc
SUMMARY: <=15 lines: lowest and highest pitch (MIDI); largest leap and its bar; chorus peak note and the syllable it carries; bars where you used _ or *; any key or tempo concern for the harmony role. Never claim a gate passed. End with exactly one line `PROPOSE key: <key> <mode>; bpm: <n>` (the values the melody is written in; copy structure.md when you have no concern).
```

## Notes for the dispatcher

- `structure.md` and `chords.md` are mandatory. When either is absent, do not dispatch; return `STATUS: BLOCKED` naming the missing file and the stage that owns it (Stage 3 or the harmony dispatch).
- `lyrics.md` is mandatory for every `song_type` except `INSTRUMENTAL`. For `INSTRUMENTAL` the gate runs without alignment (`alignment_skipped: 1`) and the role writes no `w:` lines; `concept.md` then carries `motif` instead of `hook_line`.
- `TOPLINE` runs this prompt as the only Stage 5 dispatch (L: one pass, gate, no critic loop); `{chords.md}` is the user's chart, asserted original in `brief.md`.
- On an `abc_validate` FAIL, song-flow dispatches `song-critic:music-judge`, then re-dispatches this prompt with `{critique}` and `{melody.abc}` filled. A `chord_tools` FAIL re-dispatches the harmony prompt first and this prompt afterwards with the new chart; the pair counts one music loop.
- The `PROPOSE` line is parsed: when it differs from `structure.md` the orchestrator opens the debate (`stage-gates.md` section 6). `TOPLINE` never debates; the chart is input.
