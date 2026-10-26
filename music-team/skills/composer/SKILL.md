---
name: composer
description: Composer agent for chord progressions (Roman numerals plus concert pitch), single-voice melodies in ABC notation, song structure (key, mode, tempo, time signature, form), and music-theory questions. Auto-detects the role (harmony, melody, groove, theorist) and spawns a role-scoped sub-agent with only the relevant references. Triggers on phrases like "write chords", "chord progression", "melody for", "what key", "explain this progression", "what mode is", "reharmonize", "what chords fit", "theory question", "groove", "song structure", "time signature", "tempo for".
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

# Composer Agent

## Design Principle: Role Context Isolation

This skill keeps music-theory and notation knowledge **out of the main context window**. When a composing task arrives, the role is detected, only the matching role manifest, its output contract, the genre sections the role needs, and a few theory or technique files are read, and a sub-agent is spawned with that isolated context. The main context receives only the finished artifact path (or, for theory questions, the finished inline answer).

Four roles share this skill: `harmony` writes `chords.md`, `melody` writes `melody.abc`, `groove` writes `structure.md`, `theorist` answers theory questions inline. They never share a prompt: one role is one `Agent` call.

---

## Phase 1: Role Detection

**Pipeline mode.** When the prompt begins `SKILL: composer`, a `TASK_TYPE:` and a `ROLE:` line are given by the orchestrator (`music-flow`). Honour them. Do not detect. Begin the output with `SKILL_LOADED: <every references/ path embedded>`.

**Standalone mode.** Detect the role from (in priority order):

1. **Explicit role mention** -- "as the harmony writer", "theory question", "just the melody"
2. **Deliverable signals** -- see the role manifests below
3. **Domain signals** -- chord and numeral words route to harmony; ABC, topline, motif, singable words to melody; key, tempo, meter, form, section-length words to groove; "explain", "analyze", "why", "what mode", "what fits" to theorist
4. **Artifact signals** -- a supplied progression to explain or reharmonize routes to theorist; a request to write `chords.md` routes to harmony

**If ambiguous, ask before proceeding.** Do not assume.

Standalone use outside a `.song/` run prints one line first: `Note: no active pipeline (no .song/active); working standalone, nothing is gate-checked by the orchestrator.` Then proceed.

**Declare before every task:**

> `Role: [ROLE] | Task: [TYPE] | References: [list of reference files]`

### Role Routing Table

Load only the matched role manifest. Each manifest holds the task-type routing table, instructions, and guardrails.

| Role | Manifest | Detection Cue | Writes |
|------|----------|---------------|--------|
| Harmony | `references/roles/harmony.md` | chords / progression / Roman numerals / reharmonize a section / key-fit | `chords.md` |
| Melody | `references/roles/melody.md` | melody / topline / ABC / motif / hook line tune / singable | `melody.abc` |
| Groove | `references/roles/groove.md` | structure / key / mode / bpm / time signature / form / bars / meter spec | `structure.md` |
| Theorist | `references/roles/theorist.md` | explain / analyze / what mode / why / what fits / transpose / theory | inline answer |

For cross-role tasks see `references/contracts/cross-role-tasks.md`.

---

## Phase 2: Sub-Agent Invocation

**For every composing task, follow these steps exactly -- do not skip:**

1. Detect the role and task type (Phase 1), or take them from the pipeline prompt
2. Read **only** the matched role manifest, its output contract, the genre sections the role needs (`## Harmony` and `## Rhythm` of `references/shared/genres/<genre>.md`; theorist gets no genre), and the theory or technique files the manifest routes to -- never more than the allowance in `references/shared/prompt-allowances.json` (default 2 techniques; theorist 3, no genre)
3. Spawn a sub-agent using the `Agent` tool with the prompt template below, pasting the full contents of each file you read
4. Return the sub-agent's output directly to the user

**Do not inline music knowledge into the main context.** The sub-agent is the execution boundary for all composing reasoning. Theory files under `references/theory/` and `references/techniques/` both count against the techniques allowance.

### Sub-Agent Prompt Template

```
SKILL: composer
TASK_TYPE: [TASK TYPE]
ROLE: [ROLE]

Begin your response with "SKILL_LOADED: [comma-separated list of every references/ path embedded below]".

You are the [ROLE] for music-team, working on "[TITLE]" ([GENRE], [SONG_TYPE]).

--- TASK ---
[one paragraph: what to produce, which sections, loop number]

<!-- originality-policy -->
[verbatim clause from references/shared/originality-policy.md]

--- ROLE ---
[CONTENTS OF roles/<role>.md]
--- OUTPUT CONTRACT ---
[CONTENTS OF contracts/<role>-output.md]
Write the artifact to: [DIR]/[ARTIFACT]

--- GENRE / TECHNIQUES ---
[genre sections]  [theory or technique files, within the allowance]

--- INPUT ARTIFACTS (read these files) ---
- [paths only; the sub-agent reads them]

--- OUTPUT ---
SKILL_LOADED: [paths]
STATUS: DONE | BLOCKED
ARTIFACT: [path written, or none]
SUMMARY: [one sentence, max 200 characters]
```

In pipeline mode the orchestrator already assembled this prompt; do not rebuild it. Reply only in the shape it asks for. Theorist replies add the inline answer after the four lines under a line `ANSWER:`.

---

## Self-Checks Before Hand-Back

Run the matching script on the artifact just written. Fix what it reports, then hand back. A self-check is an early warning, never a certification: the orchestrator's gate run is authoritative.

| Role | Command | Fix before hand-back |
|------|---------|----------------------|
| harmony | `python3 -I scripts/chord_tools.py <dir>/chords.md <dir>/structure.md` | any FAIL or ERROR; read `metrics.diatonic_ratio` and the `warnings` list |
| melody | `python3 -I scripts/abc_validate.py <dir>/melody.abc <dir>/structure.md <dir>/lyrics.md` | any FAIL or ERROR (bar sums, range, leaps, `w:` alignment) |
| groove | `python3 -I scripts/structure_check.py <dir>/structure.md` | any FAIL or ERROR (form template, bars) |
| theorist | `python3 -I scripts/chord_tools.py scale\|chord\|roman\|diatonic\|transpose\|reharmonize ...` | every spelling in the answer comes from this tool, never from memory |

Paths are relative to the plugin root `music-team/`. Omit `lyrics.md` for INSTRUMENTAL.

---

## Output Contracts

| Role | Contract |
|------|----------|
| Harmony | `references/contracts/harmony-output.md` (`chords.md`) |
| Melody | `references/contracts/melody-output.md` (`melody.abc`) |
| Groove | `references/contracts/structure-output.md` (`structure.md`) |
| Theorist | `references/contracts/theory-output.md` (inline layout) |

---

## Sub-Agent Interface (Agentic Flow Integration)

### Input Contract

```json
{
  "task_type": "chords-melody | reharmonize-revise | modal-progression | voice-leading-pass | topline-transcribe | melody | motif-develop | rhythm-fit | structure | tempo-key | meter-infer | theory-answer | reharmonize-answer | mode-explain | what-fits | transpose | form-meter-answer",
  "role": "harmony | melody | groove | theorist",
  "context": {
    "title": "string (optional)",
    "genre": "string (optional) -- one genre label, never an artist",
    "song_type": "string (optional) -- FULL_SONG | INSTRUMENTAL | TOPLINE | THEORY | ...",
    "artifact_dir": "string (optional) -- .song/<slug>",
    "key": "string (optional) -- e.g. D major",
    "bpm": "integer (optional)",
    "time_sig": "string (optional) -- e.g. 4/4",
    "vocal_range": "string (optional) -- e.g. A3-E5",
    "user_level": "string (optional, theorist) -- beginner | intermediate | advanced",
    "loop": "integer (optional) -- revision loop number",
    "critique_path": "string (optional)"
  },
  "input": "string -- the raw request, or paths to supplied artifacts"
}
```

### Output Contract

```json
{
  "task_type": "string",
  "role": "string",
  "artifact_path": "string | null -- null for theorist inline answers",
  "summary": "string -- max 200 characters",
  "checks": { "chord_tools": "PASS | FAIL | ERROR | not-run", "abc_validate": "...", "structure_check": "..." },
  "assumptions": ["array"],
  "open_questions": ["array"],
  "downstream_ready": true,
  "downstream_notes": "string -- key, mode, bpm, time signature the next role must keep"
}
```

---

## User Commands

| Command | Action |
|---|---|
| `role <name>` | Override detected role (`role harmony`, `role melody`, `role groove`, `role theorist`) |
| `chords` | Write or revise a chord progression |
| `melody` | Write or revise a melody in ABC |
| `structure` | Set key, mode, bpm, time signature, and form |
| `explain` | Analyze or explain a progression, mode, or form |
| `reharmonize` | Propose substitutions in a named style |
| `transpose` | Move chords to another key or by an interval |
| `fits` | List chords or scales that fit a melody or key |
| `check` | Run the matching self-check script on the current artifact |
| `accept` | Finalize the current artifact |

---

## References

### Role Manifests

- `references/roles/harmony.md`, `melody.md`, `groove.md`, `theorist.md` -- task routing, instructions, guardrails

### Output Contracts

- `references/contracts/harmony-output.md`, `melody-output.md`, `structure-output.md`, `theory-output.md`
- `references/contracts/cross-role-tasks.md` -- multi-role combination patterns

### Theory (loaded per matched task type; count against the techniques allowance)

- `references/theory/modes-scales.md` -- modes, key signatures, enharmonic spelling
- `references/theory/functional-harmony.md` -- diatonic functions, cadences, Roman numerals
- `references/theory/voice-leading.md` -- common tones, smooth motion, bass lines
- `references/theory/reharmonization.md` -- substitution families by style
- `references/theory/form-and-meter.md` -- form templates, bar counts, meter and tempo

### Techniques

- `references/techniques/borrowed-chords.md`, `melodic-contour.md`, `rhythmic-feel.md`, `modal-color.md`, `abc-notation-primer.md`

### Shared (read by the dispatcher, not by this skill)

- `music-team/references/shared/artifact-formats.md`, `stage-gates.md`, `genres/<genre>.md`, `originality-policy.md`
