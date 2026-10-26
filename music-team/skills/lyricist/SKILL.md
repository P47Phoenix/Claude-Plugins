---
name: lyricist
description: Lyricist agent for hooks, verses, pre-choruses, bridges, lyric editing, and extending a supplied lyric. Auto-detects the role (hook-writer, verse-writer, lyric-editor, augmenter) and spawns a role-scoped sub-agent carrying one genre section and at most the allowed technique files. Triggers on phrases like "write lyrics", "chorus lyrics", "verse", "hook line", "rhyme this", "rewrite this lyric", "tighten these lyrics", "add a verse", "write a bridge for my song", "extend my lyrics", "more verses in the same voice", "pre-chorus".
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

# Lyricist

## Design Principle: Role Context Isolation

Keep lyric craft knowledge out of the main context. Detect the role, read only the matched role manifest, contract, one genre `## Lyric` section and the allowed technique files, then spawn a sub-agent that does the writing. The main context receives the finished artifact and a hand-back, never the craft references. Follow `references/shared/originality-policy.md` in every prompt: paste its fenced clause verbatim under `<!-- originality-policy -->`.

---

## Phase 1: Role Detection

Detect the role from, in priority order:

1. **Pipeline invocation.** A prompt that begins with `SKILL: lyricist` carries `ROLE:` and `TASK_TYPE:`. Honour them exactly and skip detection.
2. **Explicit role mention.** "as the hook writer", "just edit it".
3. **Task signals.** See the routing table below.
4. **Supplied-text signals.** A supplied lyric plus "fix", "tighten", "polish", "second draft" means `lyric-editor`. A supplied lyric plus "add", "extend", "one more", "more verses", "bridge for my song" means `augmenter`. No supplied lyric and a request for a title, chorus or hook means `hook-writer`; a request for verses or bridges to a concept or structure means `verse-writer`.

**If ambiguous, ask one question before proceeding.** Do not assume.

### Provenance gate (augmenter and lyric-editor on user-supplied text)

These two roles build on text the user supplied, so they REQUIRE provenance in `brief.md`: `user_asserts_original_input: true`, or `public_domain: true` with `public_domain_source`.

- In a pipeline, `music-brief` already checked it. Re-read the brief front-matter; if neither flag is set, return `STATUS: BLOCKED`.
- Standalone, ask once: "Is this lyric your own original work, or public domain (name the source)?" Proceed only on a yes.
- On a no, or any refusal to say, reply with exactly this sentence and write no artifact: *I cannot write a parody of, or a song to the tune of or in the exact style of, a named existing song or artist; I would be glad to write an original song on the same theme and in the same genre instead.*
- If you recognise the supplied text as a well-known existing lyric, stop and report it (originality clause 4). Never edit or extend it.

**Declare before every task:**

> `Role: [ROLE] | Task: [TASK_TYPE] | References: [list of reference files]`

### Role Routing Table

Load only the matched role manifest. Each manifest holds the task-type routing table, instructions and guardrails for that role.

| Role | Manifest | Task type | Stage | Detection cue |
|------|----------|-----------|-------|---------------|
| Hook Writer | `references/roles/hook-writer.md` | `hook-concept` | 2 | title, hook line, chorus idea, central image, arc |
| Verse Writer | `references/roles/verse-writer.md` | `section-lyrics` | 4 | verses, pre-chorus, chorus lines, bridge to a given structure, "rhyme this" |
| Lyric Editor | `references/roles/lyric-editor.md` | `lyric-revision` | 4 | rewrite, tighten, fix meter, polish, remove cliches |
| Augmenter | `references/roles/augmenter.md` | `lyric-augment` | 4 (AUGMENT_LYRICS) | add a verse, bridge, pre-chorus, extend, same voice |

For cross-role chains (verse-writer then lyric-editor) see `references/contracts/cross-role-tasks.md`.

---

## Phase 2: Sub-Agent Invocation

**For every lyric task, follow these steps exactly. Do not skip:**

1. Detect the role and task type (Phase 1) and announce the `Role | Task | References` line.
2. Read **only** the matched role manifest, its output contract, one genre's `## Lyric` section from `references/shared/genres/<genre>.md` (the augmenter uses the target genre when one is given, else the source genre), and at most the technique files the manifest's routing row names, within `references/shared/prompt-allowances.json` (default 2 techniques; augmenter 1 genre and 2 techniques). Do NOT read other manifests, other genres, or other techniques.
3. Spawn a sub-agent with the `Agent` tool (`subagent_type: lyricist` in a pipeline) using the prompt template below.
4. Return the sub-agent's output directly. Before handing back, run the self-check below.

**Do not inline craft knowledge into the main context.** The sub-agent is the execution boundary.

### Sub-Agent Prompt Template

```
SKILL: lyricist
TASK_TYPE: [TASK_TYPE]
ROLE: [ROLE]

Begin your response with "SKILL_LOADED: [comma-separated list of every references/ path pasted below]".

You are the [ROLE] for music-team, working on "[TITLE]" ([GENRE], [SONG_TYPE]).

--- TASK ---
[one paragraph: what to produce, which sections, loop number]

<!-- originality-policy -->
[VERBATIM FENCED CLAUSE FROM originality-policy.md]

--- ROLE ---
[FULL CONTENTS OF roles/<role>.md]
--- OUTPUT CONTRACT ---
[FULL CONTENTS OF contracts/<contract>.md]
Write the artifact to: [PATH]

--- GENRE / TECHNIQUES ---
[genres/<genre>.md "## Lyric" section only]
[technique files, separated by ---]

--- INPUT ARTIFACTS (read these files) ---
- [path]: [one-line description]

--- CRITIQUE TO ADDRESS (loop 2+ only) ---
[critique path and gate JSON]

<!-- memory-lessons -->
[<=10 lines, or "No lessons recorded."]

--- OUTPUT ---
SKILL_LOADED: [paths]
STATUS: DONE | BLOCKED
ARTIFACT: [path written]
SUMMARY: [one sentence, max 200 characters]
```

Pass input artifacts as paths for the sub-agent to read; never paste artifact text. No artist or song names as style targets: describe genre, era, tempo and texture.

### Pipeline vs standalone

| Mode | Trigger | Behaviour |
|------|---------|-----------|
| Pipeline | Prompt begins `SKILL: lyricist` with `ROLE:` and `TASK_TYPE:` | Honour them. Begin the response with `SKILL_LOADED:`. Write the artifact to the path given. Do not run gates on the orchestrator's behalf as a verdict; self-check only |
| Standalone | Any other request | Warn once: "No active pipeline (no `.song/active`); I will write to `./lyrics.md` or `./concept.md` and gates run without `structure.md` unless you supply one." Proceed |

Standalone with no `structure.md`: derive a working `meter_spec` from the user's lines (or ask for a target line length) and state it in the artifact notes.

---

## Self-Check Before Hand-Back

Run the gate scripts on the artifact you wrote, with `python3 -I`, from the song directory. Fix and re-run until each prints PASS or SKIPPED, or report the remaining violations in `SUMMARY`. A self-check is advisory; the SubagentStop hook and the orchestrator make the gate decision.

```bash
python3 -I <plugin>/scripts/cliche_scan.py --json concept.md
python3 -I <plugin>/scripts/prosody_check.py --hook --json concept.md
python3 -I <plugin>/scripts/prosody_check.py --json lyrics.md structure.md brief.md
python3 -I <plugin>/scripts/rhyme_check.py --json lyrics.md structure.md
python3 -I <plugin>/scripts/cliche_scan.py --json lyrics.md
```

| Role | Run |
|------|-----|
| hook-writer | `cliche_scan` and `prosody_check --hook` on `concept.md` |
| verse-writer, lyric-editor, augmenter | `prosody_check`, `rhyme_check`, `cliche_scan` on `lyrics.md` |

Add `--genre <genre>` for genre threshold overrides. Exit codes: 0 PASS, 1 FAIL, 2 SKIPPED (non-English), 3 ERROR. An augmentation file keeps `#`-prefixed marker and `## Augmentation` lines so every gate ignores them.

---

## Output Contracts

| Role | Contract |
|------|----------|
| Hook Writer | `references/contracts/concept-output.md` |
| Verse Writer | `references/contracts/lyrics-output.md` |
| Lyric Editor | `references/contracts/revision-output.md` |
| Augmenter | `references/contracts/augment-output.md` |

---

## Sub-Agent Interface (Agentic Flow Integration)

### Input Contract

```json
{
  "task_type": "hook-concept | section-lyrics | lyric-revision | lyric-augment",
  "role": "hook-writer | verse-writer | lyric-editor | augmenter",
  "context": {
    "title": "string (optional)",
    "genre": "string -- genre label, never an artist",
    "song_type": "FULL_SONG | LYRICS_ONLY | TOPLINE | JINGLE | REWRITE | AUGMENT_LYRICS | REVISE",
    "brief_path": "string -- path to brief.md",
    "structure_path": "string (optional) -- path to structure.md",
    "concept_path": "string (optional) -- path to concept.md",
    "source_path": "string (optional) -- user-supplied lyric (rewrite, augment)",
    "sections": ["array (optional) -- section labels to write, edit or add"],
    "target_genre": "string (optional, augmenter) -- differs from genre only on request",
    "critique_path": "string (optional) -- loop 2+ critique",
    "provenance": "user_asserts_original_input | public_domain | none"
  },
  "input": "string -- the raw request"
}
```

### Output Contract

```json
{
  "task_type": "string",
  "role": "string",
  "artifact_path": "string",
  "status": "DONE | BLOCKED",
  "sections_written": ["array of section labels"],
  "self_check": { "prosody_check": "PASS|FAIL|SKIPPED", "rhyme_check": "PASS|FAIL|SKIPPED", "cliche_scan": "PASS|FAIL" },
  "assumptions": ["array"],
  "open_questions": ["array"],
  "downstream_ready": true,
  "downstream_notes": "string -- what the next role or stage needs to know"
}
```

---

## User Commands

| Command | Action |
|---|---|
| `role <name>` | Override the detected role (`hook-writer`, `verse-writer`, `lyric-editor`, `augmenter`) |
| `hook` | Write a title, hook line, central image and arc |
| `verse` | Write verses, choruses or pre-choruses to a structure |
| `edit` | Tighten, fix meter or rhyme, remove cliches in a supplied lyric |
| `augment` | Add a verse, bridge or pre-chorus to a supplied lyric |
| `check` | Run the self-check gates on the current artifact |
| `accept` | Finalize the current artifact |

---

## References

### Role Manifests

- `references/roles/hook-writer.md` -- Stage 2 concept: title, hook, image, arc
- `references/roles/verse-writer.md` -- Stage 4 section lyrics to a meter and rhyme spec
- `references/roles/lyric-editor.md` -- Stage 4 revision pass and REWRITE
- `references/roles/augmenter.md` -- AUGMENT_LYRICS: new sections that match a supplied lyric

### Contracts

- `references/contracts/concept-output.md`, `lyrics-output.md`, `revision-output.md`, `augment-output.md`
- `references/contracts/cross-role-tasks.md` -- verse-writer then lyric-editor chain, REVISE scoping

### Techniques (loaded per matched task type, within the allowance)

- `references/techniques/hook-craft.md` -- hook shape, placement, syllable budget
- `references/techniques/prosody-and-stress.md` -- fitting words to a meter_spec
- `references/techniques/rhyme-schemes.md` -- full and slant rhyme, scheme letters
- `references/techniques/imagery-and-specificity.md` -- concrete images, cliche replacement
- `references/techniques/section-roles.md` -- what each section does
- `references/techniques/editing-passes.md` -- ordered revision passes
