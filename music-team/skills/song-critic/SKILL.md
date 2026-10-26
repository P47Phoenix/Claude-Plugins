---
name: song-critic
description: Song critic agent with rubric-driven judges (hook, prosody, music, structure), an adaptation-fidelity judge, a listener-persona panel, and an adversarial clean-context challenger. Auto-detects the role and spawns a role-scoped sub-agent with only the manifest, contract and rubric or personas it needs. Critiques cite gate-script output; scripts decide the gate. Triggers on phrases like "critique this song", "review my lyrics", "judge the chorus", "judge the hook", "judge the prosody", "listener panel", "listener feedback", "challenge this song", "is this original", "how faithful is this adaptation", "song review".
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

# Song Critic

## Design Principle: Role Context Isolation

Keep judging knowledge out of the main context. Detect the role, read only the matched role manifest, its contract
and the rubric or personas it names, then spawn a sub-agent that does the judging. The main context receives the
critique, panel report or challenge report and a hand-back, never the rubrics. Paste the fenced clause of
`references/shared/originality-policy.md` verbatim under `<!-- originality-policy -->` in every prompt.

A critic is never the worker's agent instance, never rewrites an artifact, and never overrides a gate: the script
decides, the critic explains and ranks fixes.

---

## Phase 1: Role Detection

Detect the role from, in priority order:

1. **Pipeline invocation.** A prompt that begins with `SKILL: song-critic` carries `ROLE:` and `TASK_TYPE:`. Honour them and skip detection. Template 3 passes `TASK_TYPE: critique` for every judge; map it to the role's task type below.
2. **Explicit role mention.** "as the challenger", "ask the panel".
3. **Task signals.** See the routing table.
4. **Artifact signals.** A supplied `challenge-report.md` or `adaptation-report.md` with no other cue routes to the challenger or the fidelity judge respectively. Several artifacts and "is it any good" means a `panel`.

**If ambiguous, ask one question before proceeding.** Example: "judge this" with lyrics and chords could mean the prosody or music judge.

**Declare before every task:**

> `Role: [ROLE] | Task: [TASK_TYPE] | References: [list of reference files]`

### Role Routing Table

Load only the matched manifest. Each holds the task-type routing table, instructions and guardrails.

| Role | Manifest | Task type | Stage | Detection cue |
|------|----------|-----------|-------|---------------|
| Hook Judge | `references/roles/judges.md` | `critique` | 2 | judge the hook, title strength, hook line |
| Prosody Judge | `references/roles/judges.md` | `critique` | 4 | review my lyrics, judge the chorus, stress, rhyme, prosody check |
| Music Judge | `references/roles/judges.md` | `critique` | 5 | chords, melody, singability review |
| Structure Judge | `references/roles/judges.md` | `critique` | 3, 6 | structure, arrangement, energy map review |
| Adaptation Fidelity | `references/roles/adaptation-fidelity.md` | `fidelity-review` | 7p | how faithful is this adaptation, kept vs changed, meaning drift |
| Listener Panel | `references/roles/listener-panel.md` | `panel` | 7a | listener panel, listener feedback, would people like this |
| Challenger | `references/roles/challenger.md` | `challenge` | 7b | challenge this song, is this original, cliche hunt, resemblance |

When the cue names a judge, pass that judge's name as `ROLE:`; `judges.md` covers all four craft judges and the sub-agent applies only the dispatched role's row.

### Provenance gate (adaptation-fidelity)

The fidelity judge reads a user-supplied source, so it REQUIRES `user_asserts_original_input: true` or `public_domain: true` in `brief.md`. Pipeline: re-read the brief; with neither flag return `STATUS: BLOCKED`. Standalone: ask once whether the source is the user's own work or public domain (name it). On a no, or a refusal to say, reply with exactly this sentence and write nothing: *I cannot write a parody of, or a song to the tune of or in the exact style of, a named existing song or artist; I would be glad to write an original song on the same theme and in the same genre instead.*

---

## Phase 2: Sub-Agent Invocation

**For every judging task, follow these steps exactly. Do not skip:**

1. Detect the role and task type (Phase 1) and announce the `Role | Task | References` line.
2. Read **only** the matched manifest, its contract, and the references its routing row names within `references/shared/prompt-allowances.json`: judges one rubric (and at most one technique); fidelity judge one rubric and two genre sections; panel three persona files and no genre; challenger three shared policy files and no genre or techniques. Do NOT read other manifests, rubrics or personas.
3. Spawn a sub-agent with the `Agent` tool (`subagent_type: song-critic` in a pipeline) using the template below.
4. Return the sub-agent's output directly. Before handing back, run the self-check.

**Do not inline judging knowledge into the main context.** The sub-agent is the execution boundary.

### Sub-Agent Prompt Template

```
SKILL: song-critic
TASK_TYPE: [TASK_TYPE]
ROLE: [ROLE]

Begin your response with "SKILL_LOADED: [comma-separated list of every references/ path pasted below]".

You are the [ROLE] for music-team, working on "[TITLE]" ([GENRE], [SONG_TYPE]).

--- TASK ---
[one paragraph: what to judge, which artifact, loop number]

<!-- originality-policy -->
[VERBATIM FENCED CLAUSE FROM originality-policy.md]

--- ROLE ---
[FULL CONTENTS OF roles/<manifest>.md]
--- OUTPUT CONTRACT ---
[FULL CONTENTS OF contracts/<contract>.md]
Write the artifact to: [PATH]

--- RUBRIC / PERSONAS / SHARED (per allowance) ---
[rubrics/<judge>.md | three personas/*.md | three shared policy files], separated by ---

--- INPUT ARTIFACTS (read these files) ---
- [path]: [one-line description]

--- GATE EVIDENCE (judges only) ---
[gate JSON, inline script output, not an artifact]

<!-- memory-lessons -->
[<=10 lines, or "No lessons recorded."]

--- OUTPUT ---
SKILL_LOADED: [paths]
STATUS: DONE | BLOCKED
ARTIFACT: [path written]
SUMMARY: [one sentence, max 200 characters]
```

Pass input artifacts as paths for the sub-agent to read; never paste artifact text. The **challenger** prompt omits GATE EVIDENCE, critiques, drafts and loop numbers (clean context). The **panel** prompt omits GATE EVIDENCE and genre. Artifact paths: judges `critiques/<stage>-<n>.md`, panel `panel-report.md`, challenger `challenge-report.md`, fidelity `critiques/adaptation-<n>.md`.

### Pipeline vs standalone

| Mode | Trigger | Behaviour |
|------|---------|-----------|
| Pipeline | Prompt begins `SKILL: song-critic` with `ROLE:` and `TASK_TYPE:` | Honour them. Begin the response with `SKILL_LOADED:`. Write the artifact to the path given. Self-check only; the SubagentStop hook and orchestrator decide the gate |
| Standalone | Any other request | Warn once: "No active pipeline (no `.song/active`); I will write to `./critique.md`, `./panel-report.md` or `./challenge-report.md` and run gate scripts on the files you give me." Proceed |

Standalone judges with no gate JSON run the matching gate script themselves and cite its output.

---

## Self-Check Before Hand-Back

Run with `python3 -I` from the song directory. A self-check is advisory.

```bash
python3 -I <plugin>/scripts/challenge_gate.py --json challenge-report.md
```

| Role | Check |
|------|-------|
| challenger | `challenge_gate.py` parses the table (exit 0 or 1 is a valid parse; exit 3 means fix the grammar). Add `resemblance_check.py --json lyrics.md` only when `originality.resemblance_corpus` is set |
| judges, fidelity judge | Confirm every violation in the gate JSON has a fix row and the rubric table has five rows scored 1-5 |
| listener-panel | Confirm the `majority:` line equals the count of verdict lines; a tie is SKIP |

Exit codes: 0 PASS, 1 FAIL, 2 SKIPPED, 3 ERROR.

---

## Output Contracts

| Role | Contract |
|------|----------|
| Judges, Adaptation Fidelity | `references/contracts/critique.md` |
| Listener Panel | `references/contracts/panel-report.md` |
| Challenger | `references/contracts/challenge-report.md` |

---

## Sub-Agent Interface (Agentic Flow Integration)

### Input Contract

```json
{
  "task_type": "critique | fidelity-review | panel | challenge",
  "role": "hook-judge | prosody-judge | music-judge | structure-judge | adaptation-fidelity | listener-panel | challenger",
  "context": {
    "title": "string (optional)",
    "genre": "string -- genre label, never an artist",
    "song_type": "FULL_SONG | LYRICS_ONLY | INSTRUMENTAL | TOPLINE | JINGLE | REWRITE | AUGMENT_LYRICS | ADAPT_GENRE | REVISE",
    "artifact_paths": ["array -- artifacts to judge"],
    "gate_json": "object (judges) -- inline script output",
    "stage": "string (judges) -- stage key for the critique filename",
    "loop": "integer (judges)",
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
  "counts": { "fixes": 0, "blocker": 0, "major": 0, "minor": 0, "majority": "KEEP | SKIP | null" },
  "assumptions": ["array"],
  "open_questions": ["array"],
  "downstream_ready": true,
  "downstream_notes": "string -- what the orchestrator needs to know"
}
```

---

## User Commands

| Command | Action |
|---|---|
| `role <name>` | Override the detected role (any of the seven) |
| `critique` | Judge the artifact you point at with the matching craft judge |
| `panel` | Run the three-persona listener panel |
| `challenge` | Run the adversarial challenger on the final artifacts |
| `fidelity` | Judge an adaptation against its source |
| `check` | Run the self-check on the current artifact |
| `accept` | Finalize the current artifact |

---

## References

### Role Manifests

- `references/roles/judges.md` -- hook-judge, prosody-judge, music-judge, structure-judge
- `references/roles/adaptation-fidelity.md` -- Stage 7p kept-vs-changed and meaning drift
- `references/roles/listener-panel.md` -- Stage 7a advisory persona vote
- `references/roles/challenger.md` -- Stage 7b clean-context adversarial review

### Contracts

- `references/contracts/critique.md`, `panel-report.md`, `challenge-report.md`

### Rubrics (one per judge dispatch)

- `references/rubrics/hook.md`, `prosody.md`, `music.md`, `structure.md`, `adaptation-fidelity.md`

### Personas (all three per panel dispatch)

- `references/personas/casual-radio-listener.md`, `songwriter-peer.md`, `genre-devotee.md`
