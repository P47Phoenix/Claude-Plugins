---
name: adapter
description: Cross-genre adaptation worker for a song the user owns or that is in the public domain. Detects whether the lyric, the music, or both need adapting, resolves the source and target genres, checks provenance, loads both genre profiles, and spawns a role-scoped sub-agent (lyric-adapter or music-adapter) that keeps the identity of the song, remaps its style, and records kept versus changed in an adaptation report. Triggers on phrases like "just adapt the chords to", "turn my ballad into", "convert this to <genre>", "make it bossa nova", "cross-genre", "reharmonize for <genre>", "re-fit these lyrics to", "genre adaptation", "what would change if this were <genre>".
license: Apache License 2.0 - See repository LICENSE file
model_awareness: opus-4-7
last_audited: 2026-10-26
pattern_library_version: 4-7-1
model: sonnet
phase_1_detector_model: haiku
tier: B
maintainer: music-team-leads
fitness_review_due: 2027-01-24
context_budget: 300
allowed-tools: [Read, Write, Edit, Bash, Agent, Skill]
---

# adapter

## Design Principle: Two Genres, One Role

Adapting a song needs the source genre and the target genre in context at the same time, which no
other music-team role needs. This skill keeps adaptation craft out of the main context: it detects
the role, reads only the matched manifest, one output contract, both genre profiles and at most two
techniques, then spawns one sub-agent per role. The main context receives the finished artifact and a
one-sentence summary. Craft lives in `references/`, never here.

The adapter keeps what makes the song itself (hook, title, melody contour, lyric meaning, point of
view, key images) and remaps what makes it sound like a genre (feel, tempo band, harmony, form,
instrumentation, diction register). It never adds new meaning and never imports a line from any
existing song. Originality policy clauses 1, 2, 4 and 5 apply
(`music-team/references/shared/originality-policy.md`).

---

## Phase 1: Detection

Detection is cheap pattern work; run it on `phase_1_detector_model` (haiku) when delegated.

### 1. Roles from what the user supplied

| Supplied input | Role(s) | Order |
|----------------|---------|-------|
| Lyric only | `lyric-adapter` | single call |
| Chords and/or melody only (no lyric) | `music-adapter` | single call |
| Lyric and chords/melody | `lyric-adapter`, then `music-adapter` | two sequential `Agent` calls, one role each |
| Arrangement or production notes only | `music-adapter` (task `arrangement-adapt`) | single call |
| "what would change if this were <genre>" | the role the input matches, task `adaptation-report` only; write nothing else | single call |

One role is one `Agent` call; never put two `ROLE:` lines in one prompt. When ambiguous, ask once.

### 2. Genres

- `source_genre`: from the brief, the request, or the input itself. If absent or unclear, ask. Do not guess.
- `target_genre`: must resolve to a profile in `music-team/references/shared/genres/<slug>.md` through its
  `genre:` or `aliases:` front-matter (for example "bossa" and "bossa nova" resolve to `bossa-nova`).
- A target that is a named artist, band or song, "in the style of <name>", "to the tune of", or an entry in
  `blocked-targets.txt`: refuse with exactly the sentence under "PARODY_ADAPT refusal" in
  `music-team/references/shared/song-types.md`. Create nothing.
- A genre with no profile: say which profiles exist and ask the user to pick the nearest one. Do not improvise a profile.

### 3. Provenance (check once, before any dispatch)

Proceed only when `brief.md` (or the user's message in standalone use) records
`user_asserts_original_input: true`, or `public_domain: true` with a `public_domain_source`. Otherwise reply
with the refusal sentence above and stop. A supplied lyric recognised as an existing well-known song is
refused under clause 4 even when the flag is set.

### 4. Announce

> `Roles: [lyric-adapter | music-adapter | both] | Source: [genre] | Target: [genre] | References: [list of reference files]`

---

## Phase 2: Sub-Agent Invocation

**For every adaptation task, follow these steps exactly -- do not skip:**

1. Detect the role(s), task type, `source_genre` and `target_genre` (Phase 1)
2. Read **only** the matched role manifest, its output contract, **both** genre profiles and at most two
   techniques from the manifest's routing table -- do NOT read other roles' manifests or other genre files
3. Spawn a sub-agent using the `Agent` tool (`subagent_type: adapter` in pipeline use) with the prompt template below
4. Return the sub-agent's output directly to the user

**Do not inline adaptation knowledge into the main context.** The sub-agent is the execution boundary.

### Role Routing Table

| Role | Manifest | Detection Cue |
|------|----------|---------------|
| Lyric adapter | `references/roles/lyric-adapter.md` | lyric / words / verses / re-fit / syllables / diction / rhyme |
| Music adapter | `references/roles/music-adapter.md` | chords / melody / harmony / reharmonize / tempo / feel / arrangement / instrumentation |

For multi-role sequences and report hand-offs, see `references/contracts/cross-role-tasks.md`.

### Genre sections to paste (per role)

| Genre | Lyric-adapter | Music-adapter |
|-------|---------------|---------------|
| `source_genre` | `## Identity`, `## Lyric` | `## Identity`, `## Harmony`, `## Rhythm`, `## Arrangement` |
| `target_genre` | `## Identity`, `## Lyric`, `## Adaptation notes` | `## Identity`, `## Harmony`, `## Rhythm`, `## Arrangement`, `## Adaptation notes` |

Two genre files is the allowance for both roles (`prompt-allowances.json`); never paste a third.

### Sub-Agent Prompt Template

```
SKILL: adapter
TASK_TYPE: [TASK_TYPE]
ROLE: [ROLE]

Begin your response with "SKILL_LOADED: [comma-separated list of every references/ path pasted below]".

You are the [ROLE] for music-team, working on "[TITLE]" ([SOURCE_GENRE] -> [TARGET_GENRE], ADAPT_GENRE).

<!-- originality-policy -->
[PASTE THE FENCED CLAUSE FROM references/shared/originality-policy.md, VERBATIM]

--- ROLE ---
[PASTE FULL CONTENTS OF THE MATCHED references/roles/<role>.md]
--- OUTPUT CONTRACT ---
[PASTE FULL CONTENTS OF THE MATCHED references/contracts/<contract>.md]
Write the artifact to: [ARTIFACT PATH]
--- GENRE: SOURCE ([SOURCE_GENRE]) ---
[SECTIONS FROM THE TABLE ABOVE]
--- GENRE: TARGET ([TARGET_GENRE]) ---
[SECTIONS FROM THE TABLE ABOVE, INCLUDING ## Adaptation notes]
--- TECHNIQUES (at most 2) ---
[PASTE techniques/<t1>.md AND techniques/<t2>.md]

--- TASK ---
[TASK TYPE]: [WHAT TO ADAPT, WHICH SECTIONS, LOOP NUMBER]

--- INPUT ARTIFACTS (read these files) ---
- [PATH]/brief.md: the supplied source is under "## Supplied input"
- [PATH]/structure.md: meter, rhyme scheme, form already set for the target
- [upstream artifacts adapted earlier in this run]

--- CRITIQUE TO ADDRESS (loop 2+ only) ---
[critique path and gate JSON]

<!-- memory-lessons -->
[AT MOST 10 LINES, OR "No lessons recorded."]

--- OUTPUT ---
Reply with ONLY:
SKILL_LOADED: [every references/ path pasted above]
STATUS: DONE | BLOCKED
ARTIFACT: [path written]
SUMMARY: one sentence, max 200 characters
```

Pass artifact **paths**, never artifact text. Exception: the worker reads `## Supplied input` itself.

### Pipeline Invocation (`SKILL: adapter`)

When the prompt that invoked this skill starts with `SKILL: adapter`, `music-flow` has already detected
the type, checked provenance and set the genres:

- Honour the given `ROLE:` and `TASK_TYPE:` exactly; skip role detection and the announce line.
- Run steps 2-4 of Phase 2 for that one role. Do not chain roles yourself; the orchestrator dispatches each.
- Begin the reply with `SKILL_LOADED: <comma-separated list of every references/ path you embedded>`,
  then the hand-back block above.
- Run the self-check below (advisory); the SubagentStop hook and orchestrator decide the gate.
  Before handing back `adaptation-report.md`, run
  `python3 -I music-team/scripts/adapt_check.py <dir>/adaptation-report.md <dir>/structure.md <dir>/lyrics.md`
  once and fix any FAIL it reports. Report the status in `SUMMARY`; it does not replace the gate.

### Standalone Invocation

With no `SKILL: adapter` header there is no pipeline. Say once: "No active pipeline: running adapter
standalone; no gates, state or memory." Then run Phase 1, ask for any missing genre or provenance, run
Phase 2, write artifacts to the working directory the user names (default `./adapted/`), and finish
with the report check described above.

---

## Task Types

| Task | Role | Output | Stage |
|------|------|--------|-------|
| `lyric-adapt` | lyric-adapter | `lyrics.md` | 4 |
| `music-adapt` | music-adapter | `chords.md` (+ `melody.abc` when a melody is supplied) | 5 |
| `arrangement-adapt` | music-adapter | `arrangement.md` | 6 |
| `adaptation-report` | music-adapter (either role standalone) | `adaptation-report.md` | 7p |

### The adaptation report

Each role appends an `## Adaptation notes` block (Kept / Changed / Risks) to its artifact. Task
`adaptation-report` reads those blocks and consolidates them into `adaptation-report.md` (grammar in
`music-team/references/shared/artifact-formats.md`; rules in `references/contracts/adaptation-report.md`).
The `## Changed` table holds at most `adaptation.max_changed_elements` rows (default 12). The report is
mandatory when `adaptation.require_report` is true. Self-check before hand-back:

```bash
python -I music-team/scripts/adapt_check.py [--max-changed N] <dir>/adaptation-report.md <dir>/structure.md
```

---

## JSON I/O Contract (Agentic Flow Integration)

### Input

```json
{
  "task_type": "lyric-adapt | music-adapt | arrangement-adapt | adaptation-report",
  "role": "lyric-adapter | music-adapter",
  "source_genre": "string -- genre label with a profile in references/shared/genres/",
  "target_genre": "string -- genre label with a profile; never an artist or song",
  "provenance": {
    "user_asserts_original_input": "boolean",
    "public_domain": "boolean (optional)",
    "public_domain_source": "string (required when public_domain is true)"
  },
  "paths": {
    "brief": "string -- brief.md path (## Supplied input holds the source)",
    "structure": "string (optional) -- structure.md path",
    "upstream": ["array (optional) -- lyrics.md, chords.md, melody.abc, arrangement.md"]
  },
  "max_changed_elements": "integer (optional, default 12)"
}
```

### Output

```json
{
  "task_type": "string",
  "role": "string",
  "status": "DONE | BLOCKED",
  "artifact": "string -- path written",
  "kept": ["array -- preserved elements"],
  "changed": [{"element": "string", "source": "string", "target": "string", "why": "string"}],
  "risks": ["array"],
  "findings": ["array (BLOCKED only) -- specific blockers"],
  "summary": "string -- one sentence, max 200 characters"
}
```

---

## User Commands

| Command | Action |
|---|---|
| `adapt <genre>` | Adapt the supplied song to `<genre>` (detect roles, run Phase 2) |
| `role <name>` | Override the detected role (`role lyric-adapter`, `role music-adapter`) |
| `report` | Produce `adaptation-report.md` from the notes already in the artifacts |
| `diff` | Show Kept vs Changed in the conversation; write no file |
| `accept` | Finalize the current artifact |

---

## References

### Role Manifests

- `references/roles/lyric-adapter.md` -- lyric re-fit routing, instructions, guardrails
- `references/roles/music-adapter.md` -- harmony, melody, feel and arrangement routing, instructions, guardrails

### Output Contracts

- `references/contracts/lyric-adapt-output.md`, `music-adapt-output.md`, `arrangement-adapt-output.md`
- `references/contracts/adaptation-report.md` -- consolidated kept-versus-changed report
- `references/contracts/cross-role-tasks.md` -- sequencing and hand-offs

### Techniques (L3, at most two per dispatch)

- `references/techniques/feel-conversion.md` -- meter, tempo band and groove conversion
- `references/techniques/reharmonization-moves.md` -- roman-numeral harmony moves in both directions
- `references/techniques/lyric-refit.md` -- syllable and stress re-fit without new meaning

### Shared (read by the orchestrator, pasted per template)

- `music-team/references/shared/genres/<slug>.md`, `originality-policy.md`, `artifact-formats.md`, `song-types.md`
