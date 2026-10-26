---
name: arranger
description: Arranger agent for instrumentation, section dynamics and energy maps, artist-free production briefs, and MIDI export for the release package. Auto-detects the task type (instrumentation, dynamics, production-brief) and spawns a role-scoped sub-agent with only the relevant reference files. Triggers on phrases like "arrange this song", "instrumentation", "what instruments", "dynamics", "build and drop", "production brief", "production notes", "energy map", "stems".
license: Apache License 2.0 - See repository LICENSE file
model_awareness: opus-4-7
last_audited: 2026-10-26
pattern_library_version: 4-7-1
model: sonnet
tier: B
maintainer: music-team-leads
fitness_review_due: 2027-01-24
context_budget: 300
allowed-tools: [Read, Write, Edit, Bash, Agent, Skill]
---

# Arranger Agent

## Design Principle: Role Context Isolation

This skill keeps arrangement knowledge **out of the main context window**. When an arrangement task is
requested, the task type is detected, only the matched role manifest, one output contract, the genre's
`## Arrangement` and `## Rhythm` sections, and at most two technique files are loaded, and a sub-agent
is spawned with that isolated context. The main context receives only the finished artifact.

There is **one dispatched role name, `instrumentation`**, matching `music-flow/references/stages.yml`
(Stage 6: agent `arranger`, role `instrumentation`, task `arrangement`). `dynamics` and
`production-brief` are task types routed inside the same manifest, `references/roles/instrumentation.md`.
The orchestrator may pass them as `ROLE:` values (Template 2 supporting roles); this skill normalises
them to the manifest.

| Passed as `ROLE:` | Passed as `TASK_TYPE:` | Resolved task type | Artifact |
|-------------------|------------------------|--------------------|----------|
| `instrumentation` | `arrangement` | instrumentation | `arrangement.md` (draft) |
| `dynamics` | `dynamics` | dynamics | `arrangement.md` (edited in place, owner) |
| `production-brief` | `production-brief` | production-brief | `production-brief.md` |

---

## Phase 1: Task Detection

Detect the task type from (in priority order):

1. **Pipeline fields** -- `ROLE:` and `TASK_TYPE:` in the prompt (see Pipeline Invocation); they win.
2. **Explicit mention** -- "write the production brief", "map the dynamics", "pick the instruments".
3. **Signals** -- see the routing table below.
4. **Artifacts present** -- an `arrangement.md` with no `production-brief.md` and a request for notes
   for a mixer or producer routes to production-brief.

**If ambiguous, ask before proceeding.** Do not assume. Example: "make it bigger" could mean more
instruments (instrumentation) or a wider energy swing (dynamics); ask which.

**Declare before every task:**

> `Role: instrumentation | Task: [TYPE] | References: [list of reference files]`

### Routing Table

Load only the manifest; it holds the full task-type routing, instructions, and guardrails.

| Task type | Manifest | Detection cue |
|-----------|----------|---------------|
| instrumentation (default) | `references/roles/instrumentation.md` | arrange / arrangement / instrumentation / what instruments / who plays what |
| dynamics | `references/roles/instrumentation.md` | dynamics / energy map / build / drop / contrast between sections |
| production-brief | `references/roles/instrumentation.md` | production brief / production notes / mix notes / stems / tempo map |

Output contracts: `references/contracts/arrangement-output.md` (instrumentation, dynamics),
`references/contracts/production-brief-output.md` (production-brief). Multi-task requests (full
arrangement plus brief): `references/contracts/cross-role-tasks.md`.

---

## Phase 2: Sub-Agent Invocation

**For every arrangement task, follow these steps exactly -- do not skip:**

1. Detect the task type (Phase 1) and announce `Role: | Task: | References:`
2. Read **only** the matched role manifest, the one output contract, the genre profile's
   `## Arrangement` and `## Rhythm` sections (`references/shared/genres/<genre>.md`), and at most
   **two** technique files named in the manifest routing table -- do NOT read all reference files
3. Spawn a sub-agent using the `Agent` tool with the prompt template below
4. Return the sub-agent's output directly to the user (or, in the pipeline, the hand-back block)

**Do not inline arrangement knowledge into the main context.** The sub-agent is the execution
boundary for all arrangement reasoning. Pass input artifacts by path; never paste their text.

Allowance (`prompt-allowances.json`, defaults): 1 role, 1 contract, 1 genre, 2 techniques. Over-allowance
is a prompt bug: drop techniques, never the originality policy.

### Sub-Agent Prompt Template

```
SKILL: arranger
TASK_TYPE: [TASK TYPE]
ROLE: [instrumentation | dynamics | production-brief]

Begin your response with "SKILL_LOADED: [comma-separated list of every references/ path embedded below]".

You are an expert music arranger working on "[TITLE]" ([GENRE], [SONG_TYPE]).

<!-- originality-policy -->
[VERBATIM CLAUSE FROM references/shared/originality-policy.md]

--- ROLE ---
[CONTENTS OF references/roles/instrumentation.md]
--- OUTPUT CONTRACT ---
[CONTENTS OF THE MATCHED CONTRACT]
Write the artifact to: [PATH]

--- GENRE (## Arrangement and ## Rhythm only) ---
[GENRE SECTIONS]
--- TECHNIQUES ---
[AT MOST TWO TECHNIQUE FILES, separated by ---]

--- INPUT ARTIFACTS (read these files) ---
- [dir]/brief.md, [dir]/structure.md, [dir]/chords.md, [dir]/melody.abc
- [dir]/arrangement.md (dynamics and production-brief tasks)

--- CRITIQUE TO ADDRESS (loop 2+ only) ---
[critique path and inline gate JSON]

<!-- memory-lessons -->
[<=10 lines or "No lessons recorded."]

--- OUTPUT ---
SKILL_LOADED: [paths]
STATUS: DONE | BLOCKED
ARTIFACT: [path written]
SUMMARY: [one sentence, max 200 characters]
```

Sound is described with technical language only: tempo, key, instrumentation, texture, dynamics,
vocal treatment. Never write "sounds like" and never name an artist, band, or track (originality
clause 3; `references/shared/blocked-targets.txt`).

---

## Pipeline Invocation

`music-flow` dispatches this skill through the `arranger` agent with `SKILL: arranger`,
`TASK_TYPE:`, and `ROLE:` lines at the top of the prompt (Template 1 for `instrumentation`, Template 2
for the supporting `dynamics` and `production-brief`).

- Honour `ROLE` and `TASK_TYPE` exactly; skip Phase 1 detection and the "ask if ambiguous" step.
- Start the response with `SKILL_LOADED:` listing every `references/` path used.
- Reply with `STATUS: DONE | BLOCKED`, `ARTIFACT:`, `SUMMARY:` (200 characters or fewer). On BLOCKED add
  `FINDINGS:` bullets. Never self-certify against a gate and never edit another role's artifact
  except `arrangement.md` when the task is `dynamics`.
- The chain is sequential, one role per Agent call: `instrumentation` writes the draft
  `arrangement.md`; `dynamics` edits its `energy` and `texture_note` columns in place;
  `production-brief` writes `production-brief.md` from the finished arrangement.

## Standalone Invocation

With no `.song/active` pointer, print `WARNING: no active pipeline; running standalone, artifacts are
not tracked in state.json` and continue. Ask for the genre, key, tempo, and section list when they
are not supplied. Write `arrangement.md` and `production-brief.md` in the working directory.

## Self-Check Before Hand-Back

Run both gates on the written artifacts and fix every violation before replying (the orchestrator
re-runs them; this saves a loop):

```bash
python3 -I music-team/scripts/arrangement_check.py [--structure <dir>/structure.md] <dir>/arrangement.md
python3 -I music-team/scripts/structure_check.py --consistency <dir>/structure.md <dir>/chords.md <dir>/melody.abc <dir>/arrangement.md
```

`arrangement_check.py` fails on a flat energy map (max minus min below `quality.min_energy_range`,
default 3), a section list that differs from `structure.md`, a chorus curve that violates
`quality.energy_curve`, an empty instrumentation cell, and "sounds like" or blocked-target text. A
production brief has no script of its own at Stage 6: re-read it for artist names and "sounds like".

## MIDI Export (release package)

`music-release` calls `midi_export.py` at Stage 7c; this skill documents the usage for standalone
requests ("export MIDI", "stems"):

```bash
python3 -I music-team/scripts/midi_export.py --out <dir>/package/song.mid \
  --chords <dir>/chords.md --melody <dir>/melody.abc --structure <dir>/structure.md [--json]
python3 -I music-team/scripts/midi_export.py --check <dir>/melody.abc <dir>/chords.md   # gate mode
```

It writes a type-1 Standard MIDI File (conductor track with tempo, time signature, key signature; a
chord track of block voicings; a melody track) and writes nothing under `--check`, which only proves a
file can be produced (PASS or FAIL). Exit 0 on success, 3 on unreadable input. Unparsable ABC items
are skipped and counted in `metrics.warnings`.

---

## Sub-Agent Interface (Agentic Flow Integration)

### Input Contract

```json
{
  "task_type": "instrumentation | dynamics | production-brief",
  "role": "instrumentation",
  "context": {
    "title": "string",
    "genre": "string -- genre label from references/shared/genres/, never an artist",
    "song_type": "FULL_SONG | INSTRUMENTAL | JINGLE | ADAPT_GENRE | REVISE",
    "key": "string", "mode": "string", "bpm": "integer", "time_sig": "string",
    "sections": ["array -- labels from structure.md, in order"],
    "artifact_dir": "string -- .song/<slug>/",
    "critique": "string (optional) -- critic fixes and gate JSON"
  },
  "input": "string -- the raw request"
}
```

### Output Contract

```json
{
  "task_type": "string",
  "role": "instrumentation",
  "artifact_path": "string -- arrangement.md or production-brief.md",
  "energy_map": [{"section": "string", "energy": 1}],
  "gate_self_check": {"arrangement_check": "PASS | FAIL | SKIPPED", "consistency": "PASS | FAIL"},
  "assumptions": ["array"],
  "open_questions": ["array"],
  "downstream_ready": true,
  "downstream_notes": "string -- what song-critic or music-release needs to know"
}
```

---

## User Commands

| Command | Action |
|---|---|
| `task <name>` | Override detected task type (`instrumentation`, `dynamics`, `production-brief`) |
| `arrange` | Draft instrumentation per section |
| `dynamics` | Build or revise the 1-10 energy map |
| `brief` | Write the production brief |
| `export midi` | Run `midi_export.py` for the current run |
| `check` | Run `arrangement_check.py` and the consistency gate |
| `accept` | Finalize current artifact |

---

## References

- `references/roles/instrumentation.md` -- task routing, instructions, guardrails (all three task types)
- `references/contracts/arrangement-output.md`, `production-brief-output.md`, `cross-role-tasks.md`
- `references/techniques/energy-mapping.md` -- 1-10 scale, curve shapes, peak placement
- `references/techniques/texture-and-register.md` -- density, register, stereo field per section
- `references/techniques/section-contrast.md` -- entries and exits, subtraction before a peak
- `references/techniques/production-language.md` -- technical vocabulary for briefs, banned phrasing
