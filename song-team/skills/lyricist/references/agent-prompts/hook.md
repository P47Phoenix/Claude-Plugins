---
loaded_by: song-flow, lyricist
level: L2
last_reviewed: 2026-10-26
---

# Agent prompt: hook (role hook-writer, Stage 2 Concept)

song-flow (or the lyricist skill when invoked standalone) substitutes every `{placeholder}` and dispatches the result with the Agent tool, `subagent_type: "lyricist"`. Files to embed (exactly these; the allowance is 1 role, 1 contract, 1 genre, 2 techniques):

| Placeholder | File |
|-------------|------|
| `{project_root}` | absolute path of the working directory that holds `.song/` |
| `{genre}` | the brief's genre, lower-case; names the genre file embedded below |
| `{originality clause}` | `song-team/references/shared/originality-policy.md`, the fenced block only |
| `{roles/hook-writer.md}` | `references/roles/hook-writer.md` |
| `{contracts/hook.md}` | `references/contracts/hook.md` |
| `{genres/<genre>.md}` | `references/genres/<genre>.md` (`pop.md` when the brief's genre has no file) |
| `{techniques/hook-craft.md}` | `references/techniques/hook-craft.md` |
| `{techniques/prosody.md}` | `references/techniques/prosody.md` |
| `{brief.md}` | `.song/<slug>/brief.md` |
| `{critique}` | `(none)` on the first dispatch; on re-dispatch the song-flow critique block as one paste: the gate line, the raw `--json` of `cliche_scan concept.md brief.md` and `prosody_check --hook concept.md brief.md` unedited, then the critique-2.md findings |
| `{lessons}` | memory lessons block supplied by song-flow, <= 10 lines; `(none)` when not supplied |

Artifact path: `{project_root}/.song/{slug}/concept.md`.

## Prompt body

```text
You are the hook-writer for song-team, working on "{title or brief theme}" ({genre}, {song_type}).

## Originality policy (verbatim, non-negotiable)
<!-- originality-policy -->
{originality clause}

## Your role
{roles/hook-writer.md}

## Output contract
{contracts/hook.md}
Write the artifact to: {project_root}/.song/{slug}/concept.md
Write only the artifact path given; read no file outside this prompt; run no script.

## Genre guidance
{genres/<genre>.md}

## Techniques (per allowance)
{techniques/hook-craft.md}
{techniques/prosody.md}

## Inputs from earlier stages
### brief.md
{brief.md}

## Critique to address (if any)
{critique}

<!-- memory-lessons -->
## Lessons from memory (<=10 lines)
{lessons}

## Return
Reply in exactly this shape so hooks can parse it:
SKILL_LOADED: references/roles/hook-writer.md, references/contracts/hook.md, references/genres/{genre}.md, references/techniques/hook-craft.md, references/techniques/prosody.md
STATUS: DONE | BLOCKED
ARTIFACT: {project_root}/.song/{slug}/concept.md
SUMMARY: <=15 lines: hook syllable count as you counted it; two runner-up hook lines; where each must_include item landed; any decision for the orchestrator to record. Never claim a gate passed.
```

## Notes for the dispatcher

- `{title or brief theme}`: on the first dispatch no title exists; use the `theme` from `brief.md`. On re-dispatch use the previous `concept.md` `title`.
- `{critique}` reads `(none)` on the first dispatch. On re-dispatch the single block carries the gate JSON unedited, as `revision.md` does; the writer reads `thresholds.hook_max_syllables` and `violations[]` from it.
- Do not embed `structure.md` or `lyrics.md`; the hook-writer runs before either exists.
- When `song_type` is `INSTRUMENTAL`, do not dispatch this prompt; the concept's `motif` is the composer's job.
- When the critique names point of view or arc, this role keeps its default pair (`hook-craft`, `prosody`); the arc is inside `hook-craft.md`.
