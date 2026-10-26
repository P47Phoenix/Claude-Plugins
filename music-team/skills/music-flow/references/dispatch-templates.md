---
loaded_by: music-flow
level: L2
last_reviewed: 2026-10-26
---

# Dispatch Templates

Three templates, one per dispatch kind. Every dispatch is exactly one `Agent` call with
`subagent_type: <agent name>` from `stages.yml` (`agent` for workers, `critic_agent` for
critics). One role = one Agent call; never put two `ROLE:` lines in one prompt.

**Missing agent is an error, never a fallback.** Before the first dispatch of a run, and
again before any dispatch to an agent not yet used, confirm `<plugin-root>/agents/<agent>.md`
exists. If it does not, stop the stage, set `state.json.status: "failed"`, and tell the user
`MISSING_AGENT: <agent> (agents/<agent>.md not found)`. Never substitute `general-purpose`
or run the role inline. (`adapter` lands in Wave 7; ADAPT_GENRE stops with this error until then.)

## Prompt assembly rules

| Block | Rule |
|-------|------|
| `<!-- originality-policy -->` | Paste the fenced clause from `references/shared/originality-policy.md` verbatim ("The clause" section, nothing added or trimmed). Required in every creative or judging dispatch: all three templates. Exempt from the allowance count |
| Role + contract | Paste exactly one `skills/<skill>/references/roles/<role>.md` and one `references/contracts/<contract>.md` |
| Genre | Paste `references/shared/genres/<genre>.md` sections the role needs. `lyric-adapter` and `music-adapter` get two (`source_genre`, `target_genre`); `theorist`, `listener-panel`, `challenger` get none |
| Techniques | Paste at most the count in `references/shared/prompt-allowances.json` for the role (default 2). Count `roles`, `contracts`, `genres`, `techniques`, `personas`, `rubrics`, `shared` against the same manifest. Over-allowance is a prompt bug: drop references, never the policy |
| Input artifacts | Pass file paths only. The sub-agent reads them. Never paste artifact text, except `brief.md` `## Supplied input` is read by the worker itself from the path |
| `<!-- memory-lessons -->` | At most 10 lines selected in Phase 2 for this role and stage, or `No lessons recorded.` Exempt from the allowance count. Lessons are process notes, never lyric text |
| Alias / prose style | None. music-team has no alias themes; omit both sections |
| Banned content | No artist or song names as style targets, no "sounds like". Describe genre, era, tempo, texture. `audit_agent_prompt.py` denies a violating dispatch |

The orchestrator fills every `{placeholder}` of the skeleton in `agents/*.md`; never edit the shell.

## Template 1: Primary worker

```text
SKILL: {primary_skill}
TASK_TYPE: {task_type}
ROLE: {role}

Begin your response with "SKILL_LOADED: {comma-separated list of every references/ path embedded below}".

You are the {role} for music-team, working on "{title}" ({genre}, {song_type}).

--- TASK ---
{one paragraph: what to produce, which sections (REVISE: the sections named), loop number}

<!-- originality-policy -->
{verbatim originality clause}

--- ROLE ---
{contents of roles/{role}.md}
--- OUTPUT CONTRACT ---
{contents of contracts/{contract}.md}
Write the artifact to: {dir}/{artifact}

--- GENRE / TECHNIQUES (per allowance) ---
{genre sections}  {technique files}

--- INPUT ARTIFACTS (read these files) ---
- {dir}/brief.md: intake brief
- {dir}/{upstream}: {one-line description}

--- CRITIQUE TO ADDRESS (loop 2+ only) ---
- {dir}/critiques/{stage}-{n}.md: critic's fixes
- gate JSON (inline, script output, not an artifact): {gate_json}

<!-- memory-lessons -->
{lessons block, <=10 lines}

--- OUTPUT ---
Reply with ONLY this block:
SKILL_LOADED: {paths}
STATUS: DONE | BLOCKED
ARTIFACT: {path written}
SUMMARY: {one sentence, max 200 characters}
{if BLOCKED: FINDINGS: {bullet list of specific blockers}}

--- ISOLATION RULES ---
- Read artifacts from the paths above. Do not reference any prior conversation.
- Do not assume other roles' work unless a path is listed above.
- Never self-certify against a gate and never edit another role's artifact.
```

## Template 2: Supporting role (same stage, sequential)

Used for `then_roles` in `stages.yml` (`lyric-editor` after `verse-writer`, `melody` after
`harmony`, `dynamics` and `production-brief` after `instrumentation`). Same body as Template 1,
with these differences: `ROLE:` is the supporting role; `INPUT ARTIFACTS` lists the artifact
the earlier role just wrote (owner recorded in `state.json.owners`); `ARTIFACT` is the supporting
role's own file, or the same file when the contract says it edits in place. Dispatch strictly
after the earlier role returns `STATUS: DONE`. Gates run once, after the last role in the chain.

## Template 3: Critic (evaluator)

Used after a gate FAIL. The critic is never the worker's agent instance. It interprets the gate
JSON against its rubric and proposes concrete fixes; it does not rewrite the artifact and cannot
override the gate (it may flag a suspected heuristic false positive in one line).

```text
SKILL: song-critic
TASK_TYPE: critique
ROLE: {critic_role}

Begin your response with "SKILL_LOADED: {paths}".

<!-- originality-policy -->
{verbatim originality clause}

--- TASK ---
Critique {dir}/{artifact} against the {critic_role} rubric. The gate FAILED; evidence is the
gate JSON (inline, script output): {gate_json}. For each violation give: location, why it fails, and a
specific fix the worker can apply. Rank fixes by gate impact.

--- ROLE / CONTRACT / RUBRIC ---
{roles/{critic_role}.md}  {contracts/critique.md}  {rubrics/*.md per allowance}

--- INPUT ARTIFACTS (read these files) ---
- {dir}/{artifact}: artifact under review
- {dir}/{upstream}: context

<!-- memory-lessons -->
{lessons block}

--- OUTPUT ---
Write your critique to: {dir}/critiques/{stage}-{n}.md
STATUS: DONE | BLOCKED
ARTIFACT: {dir}/critiques/{stage}-{n}.md
SUMMARY: {one sentence, max 200 characters}

--- ISOLATION RULES ---
- Read only the paths above. Do not see or assume the worker's reasoning.
```

## Challenger and panel variants

- **Challenger (7b)** uses Template 1 with `ROLE: challenger`. `INPUT ARTIFACTS` are the final
  artifacts only. Embed `shared/originality-policy.md`, `blocked-targets.txt`, `cliche-list.txt`
  per allowance. Never include any critique, draft, or gate JSON: clean context.
- **Listener panel (7a)** uses Template 1 with `ROLE: listener-panel`, three persona files, no
  genre. Dispatch one Agent call per persona only if `listener_panel_size` > 3; otherwise a
  single call that writes `panel-report.md` (the contract defines per-persona blocks).

## Signal handling

- Reject a reply with no `STATUS:` line: log `malformed hand-back`, re-dispatch once, then
  treat as `BLOCKED`.
- A missing `SKILL_LOADED:` line is a warning logged in `state.json.notes`, not a failure.
- `BLOCKED` counts as a failed attempt: apply the loop and escalation rules without a gate run.
- Relay signals at 200 characters or fewer; longer content lives in a file, pass the path.
