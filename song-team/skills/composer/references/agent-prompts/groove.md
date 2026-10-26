---
loaded_by: song-flow, composer
level: L2
last_reviewed: 2026-10-26
---

# Agent prompt: groove (role groove, Stage 3 Structure)

song-flow (or the composer skill when invoked standalone) substitutes every `{placeholder}` and dispatches the result with the Agent tool, `subagent_type: "composer"`. Files to embed (exactly these; the allowance is 1 role, 1 contract, 1 genre, 2 techniques):

| Placeholder | File |
|-------------|------|
| `{project_root}` | absolute path of the working directory that holds `.song/` |
| `{genre}`, `{t1}`, `{t2}` | the genre name and the two technique file stems actually embedded (for the `SKILL_LOADED` line) |
| `{originality clause}` | `song-team/references/shared/originality-policy.md`, the fenced block only |
| `{roles/groove.md}` | `references/roles/groove.md` |
| `{contracts/structure.md}` | `references/contracts/structure.md` |
| `{genres/<genre>.md}` | `references/genres/<genre>.md` (`pop.md` when the brief's genre has no file) |
| `{techniques/t1}` | `references/techniques/rhythmic-feel.md` |
| `{techniques/t2}` | `references/techniques/form-templates.md` |
| `{brief.md}` | `.song/<slug>/brief.md` (includes `## Supplied input` for REWRITE and TOPLINE) |
| `{concept.md}` | `.song/<slug>/concept.md`; `(none: REWRITE)` when Stage 2 did not run |
| `{critique}` | `(none on the first pass)`, or the song-flow critique block (gate line, verbatim gate JSON, critique-3.md findings) |
| `{lessons}` | memory lessons block supplied by song-flow, <= 10 lines; `(none)` when not supplied |

No swap rule: the groove role always embeds `rhythmic-feel.md` and `form-templates.md`.

Artifact path: `{project_root}/.song/{slug}/structure.md`.

## Prompt body

```text
You are the groove for song-team, working on "{title}" ({genre}, {song_type}).

## Originality policy (verbatim, non-negotiable)
<!-- originality-policy -->
{originality clause}

## Your role
{roles/groove.md}

## Output contract
{contracts/structure.md}
Write the artifact to: {project_root}/.song/{slug}/structure.md
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

## Critique to address (if any)
{critique}

<!-- memory-lessons -->
## Lessons from memory (<=10 lines)
{lessons}

## Return
Reply in exactly this shape so hooks can parse it:
SKILL_LOADED: references/roles/groove.md, references/contracts/structure.md, references/genres/{genre}.md, references/techniques/{t1}.md, references/techniques/{t2}.md
STATUS: DONE | BLOCKED
ARTIFACT: {project_root}/.song/{slug}/structure.md
SUMMARY: <=15 lines: template and why; the hook line's syllable count and stress pattern as counted by hand; running time against target_length_sec; key, mode, tempo, and feel word with one line of rationale each. Never claim a gate passed.
```

## Notes for the dispatcher

- `concept.md` is mandatory for every `song_type` except `REWRITE` (no Stage 2) and `INSTRUMENTAL` when the concept carries `motif` instead of `hook_line` (the chorus meter rule then does not apply and every `meter_spec` is empty). When it is missing for any other type, do not dispatch; return `STATUS: BLOCKED` with `SUMMARY: concept.md missing; run Stage 2 first`.
- `REWRITE` and `TOPLINE` embed the user's supplied input inside `brief.md`; the role reads the meter spec (REWRITE) or the section list and bars (TOPLINE) from it. `brief.md` must carry `user_asserts_original_input: true` for either; otherwise do not dispatch.
- On a Stage 3 FAIL at an F stage, song-flow dispatches `song-critic:structure-judge`, then re-dispatches this same prompt with `{critique}` filled. There is no separate revision prompt for the groove role; the role rewrites `structure.md` whole.
- `{title}` is `concept.md.title` once Stage 2 has passed, else `brief.md.theme`.
