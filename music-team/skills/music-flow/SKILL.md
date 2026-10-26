---
name: music-flow
description: Song-creation pipeline orchestrator. Coordinates the music team through 7 stages (Brief, Concept, Structure, Lyrics, Music, Arrangement, Release) with song-type auto-detection across 11 types, deterministic script gates, evaluator-optimizer loops, a listener panel, an adversarial challenger, genre adaptation, lyric augmentation, music-theory answers, and self-learning memory. Triggers on phrases like "write me a song", "song pipeline", "music pipeline", "start a song", "run the song flow", "adapt my song to", "add a verse to my song", "explain this progression", "revise the song".
license: Apache License 2.0 - See repository LICENSE file
model_awareness: opus-4-7
last_audited: 2026-10-26
pattern_library_version: 4-7-1
model: sonnet
tier: A
maintainer: music-team-leads
fitness_review_due: 2027-01-24
context_budget: 500
allowed-tools: [Read, Write, Edit, Bash, Agent, Skill]
---

# Music Flow Orchestrator

## Design Principle

This skill is the ORCHESTRATOR. It coordinates the song team through a staged pipeline and NEVER
produces creative content: no title, hook, lyric line, chord cell, ABC note, or texture note. Every
creative artifact is written by a named sub-agent (`lyricist`, `composer`, `arranger`, `adapter`,
`song-critic`) dispatched with the `Agent` tool. Full doctrine, anti-patterns, and guardrails:
`music-team/references/shared/orchestrator-doctrine.md`.

Invariants (one line each, rationale in the doctrine):

1. The orchestrator never writes the song; its only write paths are `.song/active`,
   `.song/<slug>/state.json`, `.song/<slug>/decisions.md`, `.song/memory/**`.
2. One role = one Agent call. Never combine writer and judge, or two roles, in one prompt.
3. Scripts decide pass or fail. Sub-agents never self-certify; only the user overrides a gate, and
   every override is recorded.
4. The challenger sees final artifacts only, never drafts or critiques.
5. Artifacts move by path. Signals stay at 200 characters or fewer.
6. Everything is on disk; `state.json` is rewritten after every stage so any session can resume.

> **Model awareness (Opus 4.7):** under-dispatch is the main regression mode. The number of Agent
> calls at a stage MUST equal the roles listed in `references/stages.yml` for that song type and
> cell. A short-count dispatch, or doing a role's work inline, is a violation.

Plugin root: resolve `<plugin-root>` once in Phase 0 (`${CLAUDE_PLUGIN_ROOT}` when set, else
`music-team/`) and use literal paths afterwards. Shared references live under
`<plugin-root>/references/shared/`; this skill's under `<plugin-root>/skills/music-flow/references/`.

---

## Phase 0: Setup and Resume

Run before anything else.

1. **Config.** Read `.song/config.yml`. If absent, `music-brief` creates it from
   `<plugin-root>/.song.config.yml.example` and announces it. Keys and defaults:
   `references/shared/config-schema.md`. Note `quick`, `routing.force_type`, `loops.*`,
   `escalation.*`, `adaptation.*`, `memory.*`, `quality.*`.
2. **Quick mode.** When `quick: true` or the request says "quick song": every `loops.<stage>` is 1
   (including `release`), `escalation.on_loop_exhaustion` is `accept_best`, the wizard asks at most 2
   questions. Record `quick: true` in `state.json`. Quick mode never changes which stages run.
3. **Agent roster check.** Confirm each agent file `<plugin-root>/agents/<name>.md` exists for the
   agents the routed stages will use. A missing file is a clear error, not a fallback:
   `MISSING_AGENT: <name> (agents/<name>.md not found)`. Stop that stage; never substitute
   `general-purpose` or perform the role inline. `adapter` is delivered in Wave 7; ADAPT_GENRE
   stops with this error until then and the user is told so.
4. **Resume check.** Read `.song/active`.
   - Names a slug whose `.song/<slug>/state.json` has `status: in_progress`: tell the user
     `Resuming <slug> at stage <N> (<name>)`, re-run that stage's gates first, then continue from
     `state.stage`. Never start a second run while one is active; offer `resume`, or `abort` first.
   - Names a slug with `status: complete` and the request is a change: route as `REVISE` (Phase 1).
   - `status: failed`: show the failure, offer `revise <stage>` or `start` for a new song.
   - Absent or empty: proceed to Phase 1.
5. **Command parse.** If the request is a User Command (below), execute that command and stop.

## Phase 1: Brief and Song-Type Detection

Invoke `music-brief` (Skill tool) with the JSON request from its I/O contract, unless the type is
`REVISE` (no new brief; read the existing one).

- It returns `status: OK` plus `song_type`, `genre`, `provenance`, `slug`, `brief_path`; or
  `REFUSED` (relay the refusal sentence verbatim, create nothing, stop); or `NEEDS_INPUT` (relay its
  questions, 3 maximum, then re-invoke with the answers).
- `THEORY` returns `brief_path: null`: skip to the Stage 1 THEORY variation
  (`references/stages/01-brief.md`).
- Announce: `Type: <T> | Genre: <g> | Provenance: <p> | Brief: <path>`. If `routing.force_type` is
  set, also announce `FORCED TYPE: <pin> (detected: <T>)` on every run. `REVISE` cannot be forced.
- Create `.song/<slug>/` and `.song/active`; write the initial `state.json` (grammar in
  `references/shared/artifact-formats.md`) with a fresh `run_id`.
- Ask nothing the brief already answers.

**REVISE re-entry** (`references/shared/song-types.md`, "REVISE re-entry rules"): new `run_id`,
`state.stage` set to the earliest stage the request touches (`concept.md` 2, `structure.md` 3,
`lyrics.md` 4, `chords.md`/`melody.abc` 5, `arrangement.md`/`production-brief.md` 6, packaging 7),
`loops_used` reset for that stage and all downstream, `.song/active` rewritten. The re-entered stage
runs as F scoped to the sections named; after it passes run
`structure_check.py --consistency {present}`; downstream stages whose artifact appears in a violation
run as F, all others as L; Stage 7 always F.

## Phase 2: Memory Retrieval

Skip when `memory.enabled: false`. The memory directory is `memory.path` from config (default
`.song/memory/`, per `config-schema.md`). Minimal protocol:

1. If `<memory.path>/index.md` exists, read it. It holds one line per lesson:
   `<stage-or-role> | <genre or *> | <lesson>`.
2. Select the lessons that match the current genre and the stage being dispatched, at most 10 lines
   per dispatch. Never include lyric text; lessons are process notes only.
3. Paste the selection under `<!-- memory-lessons -->` in each prompt. With no file or no match,
   write `No lessons recorded.`
4. Writing lessons is `music-memory`'s job (Stage 7d). The orchestrator only reads.

## Phase 3: Stage Routing

Routing is machine data: `references/stages.yml` (validated by `scripts/validate_stages.py` against
`references/stages-schema.json`). Never copy it into this file and never invent a second table.

For the detected type read `matrix.<TYPE>` (7 cells, one per stage column) and the stage entries.
Legend: **F** full stage with critic loop · **L** light (one dispatch, gate runs, no critic loop; FAIL
applies escalation immediately) · **I** input (artifact comes from the user's supplied material:
validated, not invented; any dispatch listed under the stage's variation is a transcription run as L) ·
**-** skipped · `per request` (REVISE) · `refused` (PARODY_ADAPT, never reaches routing).

Rules that apply to every type:

- An **L stage is never skipped.** Light means reduced depth, not absent.
- For each stage use the entry's `type_variants.<TYPE>` when present (it overrides `agent`, `role`,
  `then_roles`, `task_type`, `primary_skill`); else the base entry.
- Stage 7 expands into the keys `07p`, `07a`, `07b`, `07c`, `07d`, filtered by `only_types` and
  `runs_on_cells` against the type's Stage 7 cell.
- Per-stage prose (sub-flow, inputs, outputs, gates, critic, loop and type variations):
  `references/stages/0N-<stage>.md`. Read only the file for the stage about to run.

Summary of the shape (the matrix block in `stages.yml` is authoritative):

| Stage | Worker (agent: role) | Critic (song-critic) | Gate scripts | Loop key |
|-------|----------------------|----------------------|--------------|----------|
| 1 Brief | inline `music-brief` | - | brief validation | - |
| 2 Concept | lyricist: hook-writer | hook-judge | cliche_scan, prosody_check --hook | `concept` |
| 3 Structure | composer: groove | structure-judge | structure_check | `structure` |
| 4 Lyrics | lyricist: verse-writer, lyric-editor | prosody-judge | prosody_check, rhyme_check, cliche_scan | `lyrics` |
| 5 Music | composer: harmony, melody | music-judge | chord_tools, abc_validate | `music` |
| 6 Arrangement | arranger: instrumentation, dynamics, production-brief | structure-judge | arrangement_check, structure_check --consistency | `arrangement` |
| 7 Release | 7p adapter, 7a listener-panel, 7b challenger, 7c music-release, 7d music-memory | - | challenge_gate, resemblance_check, midi_export, adapt_check | `release` |

Type variations that change *who* runs (all in `stages.yml` `type_variants`): `THEORY` dispatches
`composer:theorist` at Stage 1 and ends; `ADAPT_GENRE` runs Stages 4-6 and 7p through `adapter`
(`lyric-adapter`, `music-adapter`); `AUGMENT_LYRICS` runs only `lyricist:augmenter` at Stage 4;
`REWRITE` runs only `lyric-editor`; `TOPLINE` runs only `melody` at Stage 5.

## Phase 4: Pipeline Execution Protocol

### One Role = One Sub-Agent

Each worker, supporting role, critic, challenger, and panel is a separate `Agent` call with
`subagent_type: <agent name>`. Parallel only where independent (7a and 7b). Violations: a prompt with
two `ROLE:` lines; asking one agent to write and judge; pasting a prior critique into the challenger;
dispatching `general-purpose` when a named agent file is missing.

### Two-Channel Communication

- **Signal channel**: `STATUS`, paths, one-sentence summaries of 200 characters or fewer flow through
  the orchestrator.
- **Artifact channel**: artifact content never flows through the orchestrator. Sub-agents write to
  `.song/<slug>/`; downstream agents read by path. Gate JSON is the one allowed inline evidence
  (script output, passed to the critic).

### Stage loop (steps 1 to 10)

Repeat for each stage whose matrix cell is not `-`, in order. Templates and prompt assembly rules:
`references/dispatch-templates.md`. Gate semantics: `references/shared/stage-gates.md`.

**Step 1: Announce.** `Stage <N>: <name> (<F|L|I>) - <one-line purpose>`.

**Step 2: Load stage memory.** Select lessons per Phase 2 for the role and genre.

**Step 3: Load stage definition.** Read the stage's `stages.yml` entry and `references/stages/0N-*.md`.
Apply `type_variants.<TYPE>`. For `I` cells follow the stage file (usually no dispatch, or one
transcription run).

**Step 4: Dispatch the worker.** Build Template 1 for the role. Embed the originality clause
verbatim under `<!-- originality-policy -->`. Count embedded references against
`references/shared/prompt-allowances.json` for the role; trim references, never the clause. Pass
artifact paths, not text. Send one Agent call with `subagent_type` = `agent`. Chained roles
(`then_roles`) follow sequentially (Template 2), each after the previous returns `STATUS: DONE`.

**Step 4.5: Delegation self-check.** Before any Write or Edit under `.song/<slug>/`, stop and ask:
"Am I writing song content (a title, hook, lyric, chord, note, arrangement text, critique)?"
- YES: do not write. Dispatch the owning role.
- NO (`state.json`, `decisions.md`, `.song/active`, memory index reads): proceed.
No justification bypasses this. "It is only one line", "I know the chord", "no agent exists" all mean
dispatch or stop with `MISSING_AGENT`. Constructing such a justification is itself the violation.

**Step 5: Verify the hand-back.** Reply must begin `SKILL_LOADED:` then `STATUS: DONE | BLOCKED`,
`ARTIFACT:`, `SUMMARY:` (<= 200 characters). Confirm the artifact exists on disk. `BLOCKED` or a
missing artifact is a failed attempt: skip to step 8 without a gate run.

**Step 6: Run the gate (single runner).** Read `state.gates.<stage>`. If a `SubagentStop` hook
populated it in this dispatch and its `artifact_sha256` equals the sha256 of the artifact on disk,
reuse it. Otherwise run every script in the entry's `gates[]` via Bash:

```bash
python3 -I <plugin-root>/scripts/<script> <flags and paths from stages.yml, {dir} = .song/<slug>> \
  --config .song/config.yml --json --genre <genre>
```

Parse stdout JSON (`script`, `status`, `thresholds`, `metrics`, `violations`) and the exit code:
`0` PASS, `1` FAIL, `2` SKIPPED, `3` ERROR. The stage passes only when every script is PASS or
SKIPPED. Rules:
- **SKIPPED** (gate not applicable, e.g. non-English lyrics): proceed as PASS; set `skipped: true`.
- **Script file absent** (listed as not-yet-built in `stage-gates.md` section 7, e.g.
  `adapt_check.py` in Wave 7): record `SKIPPED (script absent)`, proceed as PASS, and tell the user
  the gate did not run. Never FAIL on an absent script. An absent script that is *not* on that list
  is an error: stop and report.
- **ERROR** (unparseable input): not a loop trigger. Report the first `violations[].reason`, ask the
  user, do not count it as a loop.
- Write the merged result to `state.gates.<stage>`: worst status wins, `metrics` and `violations`
  concatenated, plus `artifact_sha256` and `skipped`.

**Step 7: Critic loop on FAIL (F stages only).** Dispatch the stage's `critic_role` through
`critic_agent` (Template 3) with the gate JSON inline as evidence. Then re-dispatch the worker
(from the role the critique names, else the first role) with the critique path.
`state.loops_used.<max_loops_key> += 1`. Go back to step 6. The critic never rewrites the artifact and
cannot override a gate. L stages skip this step: a FAIL goes straight to step 8.

**Step 8: Loop exhaustion and escalation.** When `loops_used.<key>` reaches `loops.<key>` (config,
or 1 in quick mode) and the gate still FAILs, apply `escalation.on_loop_exhaustion`:
- `ask_user`: show the last three attempt summaries and the gate violation diff. The user chooses
  **accept** (continue), **override** (record in `state.gate_overrides[]` as
  `{stage, run_id, reason, timestamp}` and append an `override` entry to `decisions.md`), or
  **guidance** (user text becomes the next critique; reset the counter to 0 once).
- `accept_best`: keep the attempt with the fewest violations, then the lowest worst ratio. Set
  `state.accepted_best.<stage> = true`, append an `accept_best` entry to `decisions.md`, continue.
- `fail`: set `state.status = "failed"`, write `state.json`, report the stage and last violations, stop.
A `loops.<key>` of 0 means no retry: escalate on the first FAIL.

**Step 8.5: Debate.** When `harmony` and `melody` disagree on key or tempo, or two hook candidates
tie, score both options on the rubric in `references/shared/stage-gates.md` section 6 (each advocate
<= 10 lines), pick the winner, and append a `debate` entry to `decisions.md`. The decision is final
for the run unless the user overrides.

**Step 9: Update state.** Rewrite `.song/<slug>/state.json`: `stage` (the next stage to run),
`updated`, `loops_used`, `gates`, `owners[<artifact>] = <role>`, `gate_overrides`, `accepted_best`.
Write it after every stage, including skipped and failed ones. Use a temp file and rename.

**Step 10: Advance.** Report one line to the user: `Stage <N> <name>: <PASS|SKIPPED|ACCEPTED_BEST|OVERRIDDEN>
(loops <used>/<cap>) -> <artifact path>`. Continue to the next non-`-` stage.

### Stage 7: Release and the release loop

Follow `references/stages/07-release.md`. Order: 7p (ADAPT_GENRE only) then 7a and 7b in parallel
(two Agent calls in one message; 7a only for cell F), then 7c, then 7d.

- **7b challenger BLOCKER** returns to Stage 4, or to Stage 5 when the BLOCKER row's `location` names
  `chords.md` or `melody.abc`. `loops_used.release += 1`; reset the re-entered stage's counter to 0;
  pass the BLOCKER rows (not the report) as the critique; downstream stages re-run as L unless
  `structure_check.py --consistency` invalidates their artifact (then F). A `resemblance_check.py`
  FAIL counts as a BLOCKER on `lyrics.md`. At `loops.release` apply `escalation.on_blocker`
  (`ask_user | accept_best | fail`, same three policies as step 8). `accept_best` is not allowed
  when a BLOCKER cites a recognised existing lyric; fall back to `ask_user`.
- **ADAPT_GENRE** requires `adaptation-report.md` when `adaptation.require_report` is true (7p). Run
  `adapt_check.py`; the script lands in Wave 7. While `<plugin-root>/scripts/adapt_check.py` is
  absent the gate is SKIPPED (script absent), not FAIL: state that plainly and note the report was not
  machine-checked.
- **7a panel** is advisory: never gates, never loops. Surface the majority and top notes.
- **7d** runs `music-memory` so `retrospective.md` exists with `run_id` equal to `state.json.run_id`
  (the Stop hook compares them). Only then set `status: "complete"`.

## Delegation Self-Check Summary

Before every tool call that writes: Write/Edit allowed only on `.song/active`,
`.song/<slug>/state.json`, `.song/<slug>/decisions.md`, `.song/memory/**` (and `mkdir`). Anything else
under `.song/<slug>/` is a sub-agent's. If a sub-agent returns a bad artifact, re-dispatch; never
patch it. If tempted to "just fix the rhyme", dispatch `lyric-editor` with the gate JSON.

## User Commands

| Command | Action |
|---------|--------|
| `start [request]` | Run Phase 0 to Phase 4 for a new song; refuses if a run is `in_progress` (use `resume` or `abort`) |
| `resume` | Resume the run named by `.song/active` at `state.stage`, re-running that stage's gate first |
| `status` | Print slug, `song_type`, genre, current stage, `loops_used`/caps, last gate status per stage, overrides, `accepted_best`, artifact paths. Signal-length lines only |
| `revise <stage>` | Start a `REVISE` run on the finished song, re-entering at `<stage>` (1-7 or name); new `run_id`; scope from the user's change request |
| `abort` | Set `status: "failed"` with reason `aborted by user`; keep all artifacts; clear nothing else; confirm first |
| `type <TYPE>` | Pin the type for this run only, passed to `music-brief` (cannot pin `REVISE` or `PARODY_ADAPT`) |
| `quick` | Treat this run as quick mode |

## JSON I/O Contract

Machine-facing replies from this skill (for callers, hooks, tests) end with one JSON line:

```json
{ "status": "OK|NEEDS_INPUT|REFUSED|FAILED|COMPLETE", "run_id": "<id>", "slug": "<slug|null>",
  "song_type": "FULL_SONG", "stage": 4, "stage_name": "Lyrics", "cell": "F",
  "gate": { "script": "prosody_check", "status": "PASS|FAIL|SKIPPED|ERROR", "skipped": false },
  "loops_used": { "lyrics": 1 }, "artifacts": ["lyrics.md"], "message": "<=200 chars" }
```

Sub-agent hand-back (all workers and critics), parsed by hooks:

```text
SKILL_LOADED: <comma-separated references/ paths embedded>
STATUS: DONE | BLOCKED
ARTIFACT: <path written>
SUMMARY: <one sentence, <=200 characters>
```

Gate scripts emit `{ "script", "status", "thresholds", "metrics", "violations": [{ "location",
"reason", "observed", "limit" }] }` (`references/shared/stage-gates.md` section 2).

## Guardrails

- **PARODY_ADAPT is refused** before any `.song/<slug>/` exists; no stage runs.
- **Originality clause** appears verbatim in every creative or judging dispatch.
- **Provenance**: ADAPT_GENRE and AUGMENT_LYRICS proceed only with `user_asserts_original_input` or
  `public_domain` (+ `public_domain_source`) in `brief.md`. A missing flag is a refusal, not a prompt
  to build on the input anyway.
- **Standalone workers**: a worker skill invoked outside this flow is warned that gates will not run;
  never deny it.
- **Stage artifacts are never edited by the orchestrator**, including to correct a gate violation.
- **Memory never holds lyric text.**

## References

| File | Purpose |
|------|---------|
| `references/stages.yml`, `references/stages-schema.json` | Machine routing and its schema (`scripts/validate_stages.py`) |
| `references/dispatch-templates.md` | Primary, supporting, critic templates; assembly rules |
| `references/stages/01-brief.md` ... `07-release.md` | Per-stage sub-flows, gates, loops, type variations |
| `references/shared/song-types.md` | Detection order and routing matrix (single source) |
| `references/shared/stage-gates.md` | Gate rules, protocol, release loop, debate rubric |
| `references/shared/config-schema.md` | `.song/config.yml` keys |
| `references/shared/artifact-formats.md` | Artifact paths and grammars, `state.json` |
| `references/shared/originality-policy.md` | The clause embedded in every creative prompt |
| `references/shared/prompt-allowances.json` | Per-role reference counts |
| `references/shared/orchestrator-doctrine.md` | Principles, anti-patterns, resume protocol |
