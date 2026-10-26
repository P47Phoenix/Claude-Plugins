---
loaded_by: song-flow, lyricist
level: L2
last_reviewed: 2026-10-26
---

# Agent prompt: section (role verse-writer, Stage 4 Lyrics first pass)

song-flow (or the lyricist skill when invoked standalone) substitutes every `{placeholder}` and dispatches the result with the Agent tool, `subagent_type: "lyricist"`. Files to embed (exactly these; the allowance is 1 role, 1 contract, 1 genre, 2 techniques):

| Placeholder | File |
|-------------|------|
| `{project_root}` | absolute path of the working directory that holds `.song/` |
| `{genre}`, `{t1}`, `{t2}` | the genre name and the two technique file stems actually embedded (for the `SKILL_LOADED` line) |
| `{originality clause}` | `song-team/references/shared/originality-policy.md`, the fenced block only |
| `{roles/verse-writer.md}` | `references/roles/verse-writer.md` |
| `{contracts/section-lyric.md}` | `references/contracts/section-lyric.md` |
| `{genres/<genre>.md}` | `references/genres/<genre>.md` (`pop.md` when the brief's genre has no file) |
| `{techniques/t1}` | `references/techniques/imagery-and-specificity.md` by default |
| `{techniques/t2}` | `references/techniques/rhyme-schemes.md` by default |
| `{brief.md}` | `.song/<slug>/brief.md` |
| `{concept.md}` | `.song/<slug>/concept.md` |
| `{structure.md}` | `.song/<slug>/structure.md` |
| `{lessons}` | memory lessons block supplied by song-flow, <= 10 lines; `(none)` when not supplied |

Swap rule: when song-flow re-dispatches `verse-writer` (rather than `lyric-editor`) with a critique naming point of view or arc, replace `t1` with `techniques/point-of-view.md` or `techniques/narrative-arc.md`. Never embed three technique files.

Artifact path: `{project_root}/.song/{slug}/lyrics.md`.

## Prompt body

```text
You are the verse-writer for song-team, working on "{title}" ({genre}, {song_type}).

## Originality policy (verbatim, non-negotiable)
<!-- originality-policy -->
{originality clause}

## Your role
{roles/verse-writer.md}

## Output contract
{contracts/section-lyric.md}
Write the artifact to: {project_root}/.song/{slug}/lyrics.md
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

## Critique to address (if any)
(none on the first pass)

<!-- memory-lessons -->
## Lessons from memory (<=10 lines)
{lessons}

## Return
Reply in exactly this shape so hooks can parse it:
SKILL_LOADED: references/roles/verse-writer.md, references/contracts/section-lyric.md, references/genres/{genre}.md, references/techniques/{t1}.md, references/techniques/{t2}.md
STATUS: DONE | BLOCKED
ARTIFACT: {project_root}/.song/{slug}/lyrics.md
SUMMARY: <=15 lines: which section carries each arc beat; any variation of Chorus line 1 from hook_line (so song-flow updates concept.md); every slant rhyme with its location; lines you consider risky under the prosody heuristic. Never claim a gate passed.
```

## Notes for the dispatcher

- `structure.md` is mandatory. When it is absent, do not dispatch; return `STATUS: BLOCKED` with `SUMMARY: structure.md missing; run Stage 3 first` so song-flow routes correctly.
- `concept.md` is mandatory for every `song_type` except `TOPLINE` and `REWRITE`, where the user-supplied input (asserted original per `brief.md`) is embedded under `## Inputs from earlier stages` as `### supplied input` instead.
- On a Stage 4 FAIL, song-flow re-dispatches `lyric-editor` with `agent-prompts/revision.md`, not this prompt. This prompt is re-used only when the editor returned `STATUS: BLOCKED` (a structural defect that needs a fresh draft).
