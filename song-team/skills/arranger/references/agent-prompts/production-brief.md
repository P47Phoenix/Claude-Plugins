---
loaded_by: song-flow, arranger
level: L2
last_reviewed: 2026-10-26
---

# Agent prompt: production-brief (role production-brief, Stage 6 Arrangement, dispatch 3)

song-flow (or the arranger skill when invoked standalone) substitutes every `{placeholder}` and dispatches the result with the Agent tool, `subagent_type: "arranger"`. Files to embed (exactly these; the allowance is 1 role, 1 contract, 1 genre, 2 techniques; one technique by default):

| Placeholder | File |
|-------------|------|
| `{project_root}` | absolute path of the working directory that holds `.song/` |
| `{title}` | `concept.md.title` once Stage 2 has passed, else `brief.md.theme` |
| `{song_type}` | `brief.md.song_type` (FULL_SONG, LYRICS_ONLY, INSTRUMENTAL, TOPLINE, REWRITE, JINGLE, REVISE) |
| `{slug}` | the song's directory name under `.song/` |
| `{genre}`, `{t1}` | the genre name and the technique file stem actually embedded (for the `SKILL_LOADED` line) |
| `{originality clause}` | `song-team/references/shared/originality-policy.md`, the fenced block only |
| `{roles/production-brief.md}` | `references/roles/production-brief.md` |
| `{contracts/production-brief.md}` | `references/contracts/production-brief.md` |
| `{genres/<genre>.md}` | `references/genres/<genre>.md` (`pop.md` when the brief's genre has no file) |
| `{techniques/t1}` | `references/techniques/reference-track-language.md` by default |
| `{brief.md}` | `.song/<slug>/brief.md` |
| `{concept.md}` | `.song/<slug>/concept.md` (for the title line); `(none)` when absent |
| `{structure.md}` | `.song/<slug>/structure.md` |
| `{arrangement.md}` | `.song/<slug>/arrangement.md`, the finalised table after the `dynamics` dispatch |
| `{lyrics.md}` | `.song/<slug>/lyrics.md` when it exists; `(instrumental; no lyrics)` otherwise |
| `{critique}` | `(none on the first pass)`, or the `validate_artifacts` finding, or the Stage 7b challenger's BLOCKER rows whose `location` names `production-brief.md` (an L re-dispatch counted against `loops.release`) |
| `{lessons}` | memory lessons block supplied by song-flow, <= 10 lines; `(none)` when not supplied |

Swap rule: when a re-dispatch critique names vocal layering or the vocal chain as the weakness, add `techniques/vocal-production.md` as `t2` (the allowance permits two). Never embed three technique files.

Artifact path: `{project_root}/.song/{slug}/production-brief.md`.

## Prompt body

```text
You are the production-brief for song-team, working on "{title}" ({genre}, {song_type}).

## Originality policy (verbatim, non-negotiable)
<!-- originality-policy -->
{originality clause}

## Your role
{roles/production-brief.md}

## Output contract
{contracts/production-brief.md}
Write the artifact to: {project_root}/.song/{slug}/production-brief.md
Write only the artifact path given; read no file outside this prompt; run no script.

## Genre guidance
{genres/<genre>.md}

## Techniques (per allowance)
{techniques/t1}

## Inputs from earlier stages
### brief.md
{brief.md}
### concept.md
{concept.md}
### structure.md
{structure.md}
### arrangement.md
{arrangement.md}
### lyrics.md
{lyrics.md}

## Critique to address (if any)
{critique}

<!-- memory-lessons -->
## Lessons from memory (<=10 lines)
{lessons}

## Return
Reply in exactly this shape so hooks can parse it:
SKILL_LOADED: references/roles/production-brief.md, references/contracts/production-brief.md, references/genres/{genre}.md, references/techniques/{t1}.md
STATUS: DONE | BLOCKED
ARTIFACT: {project_root}/.song/{slug}/production-brief.md
SUMMARY: <=15 lines: tempo and bar total; the vocal chain in one line; the mix priority most likely to be contested; confirmation that you scanned for names, "sounds like", and "reference track" and what you removed. Never claim a lint passed.
```

## Notes for the dispatcher

- `arrangement.md` is mandatory and must be the finalised table (no `# energy: provisional` comment). When it is absent or still provisional, do not dispatch; return `STATUS: BLOCKED` with `SUMMARY: arrangement.md missing or provisional; run the dynamics dispatch first`.
- No gate script runs on this artifact. `validate_artifacts.py` (W4-2) lints it on write as an advisory hook; the challenger reads it at Stage 7b. A finding from either re-enters here with `{critique}` filled.
- For `INSTRUMENTAL` the `## Vocal treatment` section begins `None.` and treats the lead instrument as the voice; the dispatcher passes `(instrumental; no lyrics)` for `{lyrics.md}`.
