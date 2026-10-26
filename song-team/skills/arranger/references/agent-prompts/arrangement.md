---
loaded_by: song-flow, arranger
level: L2
last_reviewed: 2026-10-26
---

# Agent prompt: arrangement (roles instrumentation and dynamics, Stage 6 Arrangement)

song-flow (or the arranger skill when invoked standalone) substitutes every `{placeholder}` and dispatches the result with the Agent tool, `subagent_type: "arranger"`. The same skeleton serves both roles that write `arrangement.md`; `{role}` selects the role file and the technique. Files to embed (exactly these; the allowance is 1 role, 1 contract, 1 genre, 2 techniques, and both roles use only one technique by default):

| Placeholder | File |
|-------------|------|
| `{project_root}` | absolute path of the working directory that holds `.song/` |
| `{role}` | `instrumentation` (Stage 6 dispatch 1) or `dynamics` (Stage 6 dispatch 2, any `arrangement_check` re-dispatch, and the single dispatch of an L stage) |
| `{genre}`, `{t1}` | the genre name and the technique file stem actually embedded (for the `SKILL_LOADED` line) |
| `{originality clause}` | `song-team/references/shared/originality-policy.md`, the fenced block only |
| `{roles/<role>.md}` | `references/roles/instrumentation.md` or `references/roles/dynamics.md` |
| `{contracts/arrangement-map.md}` | `references/contracts/arrangement-map.md` |
| `{genres/<genre>.md}` | `references/genres/<genre>.md` (`pop.md` when the brief's genre has no file) |
| `{techniques/t1}` | `references/techniques/section-contrast.md` for `instrumentation`; `references/techniques/energy-curve.md` for `dynamics` |
| `{brief.md}` | `.song/<slug>/brief.md` |
| `{structure.md}` | `.song/<slug>/structure.md` |
| `{chords.md}`, `{melody.abc}` | `.song/<slug>/chords.md` and `.song/<slug>/melody.abc` for `instrumentation`; `(not embedded)` for `dynamics` |
| `{arrangement.md}` | the current `.song/<slug>/arrangement.md` for `dynamics` (with the provisional energy); `(none yet)` for `instrumentation` or when no file exists |
| `{critique}`, `{gate_json}` | structure-judge critique and the raw `--json` of `arrangement_check` and `structure_check --consistency` on a re-dispatch; `(none on the first pass)` otherwise |
| `{lessons}` | memory lessons block supplied by song-flow, <= 10 lines; `(none)` when not supplied |

Swap rule: when a `dynamics` re-dispatch critique names section sameness or palette rather than the curve, add `techniques/section-contrast.md` as `t2` (the allowance permits two). Never embed three technique files.

Artifact path: `{project_root}/.song/{slug}/arrangement.md`.

## Prompt body

```text
You are the {role} for song-team, working on "{title}" ({genre}, {song_type}).

## Originality policy (verbatim, non-negotiable)
<!-- originality-policy -->
{originality clause}

## Your role
{roles/<role>.md}

## Output contract
{contracts/arrangement-map.md}
Write the artifact to: {project_root}/.song/{slug}/arrangement.md
Write only the artifact path given; read no file outside this prompt; run no script.

## Genre guidance
{genres/<genre>.md}

## Techniques (per allowance)
{techniques/t1}

## Inputs from earlier stages
### brief.md
{brief.md}
### structure.md
{structure.md}
### chords.md
{chords.md}
### melody.abc
{melody.abc}
### arrangement.md (current)
{arrangement.md}

## Critique to address (if any)
{critique}
{gate_json}

<!-- memory-lessons -->
## Lessons from memory (<=10 lines)
{lessons}

## Return
Reply in exactly this shape so hooks can parse it:
SKILL_LOADED: references/roles/{role}.md, references/contracts/arrangement-map.md, references/genres/{genre}.md, references/techniques/{t1}.md
STATUS: DONE | BLOCKED
ARTIFACT: {project_root}/.song/{slug}/arrangement.md
SUMMARY: <=15 lines: instrumentation: opening and peak palettes, the bridge contrast, the provisional energy list; dynamics: the final energy list in order, every before -> after change, the peak section and why. Never claim a gate passed.
```

## Notes for the dispatcher

- `structure.md` is mandatory. When it is absent, do not dispatch; return `STATUS: BLOCKED` with `SUMMARY: structure.md missing; run Stage 3 first` so song-flow routes correctly.
- Stage 6 order is `instrumentation` -> `dynamics` -> `production-brief`. Dispatch 1 writes every column with a provisional `energy`; dispatch 2 finalises `energy` only. The gates run after dispatch 2.
- In a light (L) stage (JINGLE, REVISE re-runs) dispatch this prompt once with `{role}` = `dynamics` and `{arrangement.md}` = `(none yet)`; the role writes the complete table. Then dispatch `agent-prompts/production-brief.md`.
- On a Stage 6 FAIL, re-dispatch with `{role}` = `dynamics` and the critique; use `instrumentation` only when the critique names the palette or `structure_check` reports a section-list diff.
- `chords.md` and `melody.abc` are embedded for `instrumentation` only; write `(not embedded)` under their headings for `dynamics` so no bracket is left unfilled.
