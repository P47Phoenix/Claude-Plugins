---
name: music-memory
description: Song retrospective and lesson writer. After every pipeline run it records loops used per stage, the most-failed gate, recurring critiques, overrides and next-time notes to retrospective.md, and appends deduplicated lessons to .song/memory/index.md. Runs inline at Stage 7d. Triggers on phrases like "song retrospective", "what did we learn", "record lessons", "retro for this song", "save lessons".
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

# Music memory

Runs inline via the Skill tool (`dispatch: skill`), not as an Agent dispatch.

Stage 7d. Inline skill (no sub-agent). It turns one finished run into a process record and a few reusable lessons.
It writes **process observations only, never lyric text** (originality policy, "How it is enforced" item 5): no
line, no phrase of more than three words from any lyric, no artist or song name. Grammar and examples are in
`references/contracts/retrospective-output.md`.

## Phase 1: Gather

1. Resolve `.song/active` to `.song/<slug>/`. Standalone with no active run, ask for the directory; with no `state.json`, write a short retrospective from what the user says and omit `run_id`-dependent lines.
2. Read `state.json` (`run_id`, `song_type`, `loops_used`, `gates`, `gate_overrides`, `accepted_best`), `decisions.md`, and every `critiques/*.md` front-matter and Fixes table.
3. Read `brief.md` front-matter for `genre`. Read `memory.path` from `.song/config.yml` (default `.song/memory/`); stop with `memory disabled` when `memory.enabled: false`, but still write `retrospective.md`.

## Phase 2: Write `retrospective.md`

Write `.song/<slug>/retrospective.md` per the contract. Front-matter `run_id` MUST equal `state.json.run_id`: the Stop
hook compares them. Body sections: `## Loops`, `## Most-failed gate`, `## Recurring critique`, `## Overrides`,
`## Next time`. Describe recurring critiques by rubric criterion and gate metric ("stress alignment, Verse 2"), never
by quoting words from the song.

## Phase 3: Append lessons

Distil at most three lessons, each reusable on a different song. Write each as one line in
`<memory.path>/index.md`:

```text
stage-or-role | genre | lesson
```

| Field | Rule |
|-------|------|
| `stage-or-role` | A stage key (`concept`, `lyrics`, `music`, `arrangement`, `release`) or a role (`verse-writer`, `harmony`, `challenger`, ...) |
| `genre` | The genre label, or `*` when the lesson holds for every genre |
| `lesson` | One imperative sentence, 160 characters or fewer, technical language only |

**Dedupe before appending**: lower-case and collapse whitespace on `stage-or-role | genre | lesson`; skip a line whose
normalised text already exists, and skip a lesson whose meaning an existing line for the same `stage-or-role` and
`genre` already states. Create `<memory.path>` and `index.md` if absent (`mkdir -p`). Keep the file at 200 lines at most:
when over, drop the oldest lines first. Never rewrite or reorder existing lines.

## How `music-flow` reads lessons

`music-flow` Phase 2 reads `index.md`, selects lines whose `stage-or-role` matches the stage or role being dispatched
and whose `genre` matches the song's genre or is `*`, takes at most 10 lines, and pastes them under
`<!-- memory-lessons -->` in each sub-agent prompt (`No lessons recorded.` when none match). Write lessons so a line
makes sense to a worker with no other context.

## Phase 4: Hand-back

```text
SKILL_LOADED: <paths of references/ files read>
STATUS: DONE | BLOCKED
ARTIFACT: <dir>/retrospective.md
SUMMARY: <one sentence, max 200 characters; lessons appended and skipped as duplicates>
```

## Guardrails

- **No lyric text**, no artist or song names, anywhere, including lesson lines.
- **Append-only** for `index.md`; the only deletion is the oldest-line trim above.
- **Facts from files**: loop counts and gate names come from `state.json`; do not estimate.
- **Do not set** `state.json.status`; `music-flow` does after this stage.

## User Commands

| Command | Action |
|---|---|
| `retro` | Write `retrospective.md` and append lessons for the current run |
| `lessons` | Show the lines of `index.md` that match a stage and genre |
| `forget <line>` | Remove one named line from `index.md` (ask first) |

## References

- `references/contracts/retrospective-output.md` -- front-matter, sections, lesson-line grammar
