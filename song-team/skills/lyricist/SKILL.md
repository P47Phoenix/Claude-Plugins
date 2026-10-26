---
name: lyricist
description: Lyricist agent for hooks, verses, pre-choruses, bridges, and lyric editing passes. Auto-detects the role (hook-writer, verse-writer, lyric-editor) and dispatches a role-scoped sub-agent carrying one genre file and at most two technique files. Triggers on phrases like "write lyrics", "chorus lyrics", "verse", "rewrite this lyric", "hook line", "rhyme this".
license: Apache License 2.0 - See repository LICENSE file
tier: B
maintainer: song-team-leads
fitness_review_due: 2027-01-24
context_budget: 300
allowed-tools: [Read, Write, Edit, Bash, Agent, Skill]
---

# Lyricist

## Design Principle

This skill keeps craft knowledge **out of the main context window**. Every lyric line is written by a sub-agent that carries exactly one role file, one output contract, one genre file, and at most two technique files. Nothing else from `references/` is loaded, ever.

- A hook task for a country brief loads `genres/country.md` and nothing about pop or folk.
- A verse task loads `techniques/imagery-and-specificity.md` and `techniques/rhyme-schemes.md`; it never sees `hook-craft.md`.
- An editing task loads only the sections the gate report cites.

Three rules hold across every dispatch:

1. **Role and genre isolation.** One role, one genre, per sub-agent. Mixed-genre briefs resolve to the first genre listed in `brief.md`.
2. **The lyricist never judges itself.** The sub-agent writes the artifact and returns. It never claims a gate passed. `song-critic` judges; `song-flow` decides.
3. **Gates are scripts.** `prosody_check.py`, `rhyme_check.py`, and `cliche_scan.py` decide pass/fail on measurable properties. The technique files teach what the scripts measure so the first attempt passes; they never replace the scripts.

The main context receives only the hand-back block and the artifact path.

---

## Pipeline Context Check

Before any dispatch, check for `.song/config.yml` in the current working directory.

1. Present: proceed. `song-flow` owns the gate loop and thresholds.
2. Absent: print this warning, then proceed:

> WARNING: No song pipeline config found. This lyric task is not running inside song-flow. Gate scripts (prosody_check, rhyme_check, cliche_scan), the critic loop, and memory lessons will NOT run. Start the pipeline with `song-team:song-flow`, or say "skip pipeline" to continue without gates.

The check warns; it never denies. "skip pipeline" bypasses the warning for the rest of the session. Standalone output still follows the output contract so a later pipeline run accepts it.

---

## Role Detection

Detect the role from the task wording and the pipeline stage, in that order of priority.

| Role | Detect when | Loads (L2) | Loads (L3) |
|------|-------------|-----------|-----------|
| `hook-writer` | task is chorus / hook / title line; song-flow Stage 2 (Concept) | `roles/hook-writer.md`, `contracts/hook.md` | `genres/<g>.md`, `techniques/hook-craft.md`, `techniques/prosody.md` |
| `verse-writer` | task is verse / pre-chorus / bridge / "write the lyrics"; song-flow Stage 4 first pass | `roles/verse-writer.md`, `contracts/section-lyric.md` | `genres/<g>.md`, `techniques/imagery-and-specificity.md`, `techniques/rhyme-schemes.md` |
| `lyric-editor` | task is revise / tighten / fix prosody / fix rhyme / a gate FAIL report is supplied; song-flow Stage 4 re-dispatch | `roles/lyric-editor.md`, `contracts/revision.md` | `genres/<g>.md`, `techniques/prosody.md`, `techniques/cliche-avoidance.md` |

Trigger words per role:

- `hook-writer`: "hook", "hook line", "chorus line", "title", "concept", "what is the song called"
- `verse-writer`: "verse", "pre-chorus", "bridge", "lyrics", "fill the structure", "rhyme this"
- `lyric-editor`: "rewrite", "revise", "tighten", "fix the stress", "fix the rhyme", "too many clichés", or any prompt that includes a gate JSON with `"status": "FAIL"`

When the wording is ambiguous and no stage is supplied, ask one question: "Hook, full lyric, or revision?" Never load two roles to hedge.

The technique files `point-of-view.md` and `narrative-arc.md` are swap-ins, never additions: a role embeds at most two technique files. Swap one in only when the critique names point of view or arc as the failure and the role's default pair does not address it.

Declare before every dispatch:

> `Role: [hook-writer | verse-writer | lyric-editor] | Genre: <g> | Artifact: .song/<slug>/<file> | Refs: roles/<r>.md, contracts/<c>.md, genres/<g>.md, techniques/<t1>.md, techniques/<t2>.md`

---

## Dispatch Protocol

Follow these steps in order for every task. Skip none.

1. **Detect the role** per the table above. Record it in the declaration line.
2. **Resolve the genre.** Read `genre:` from `.song/<slug>/brief.md`. Lower-case it and hyphenate spaces (`hip hop` becomes `hip-hop`). When `brief.md` is absent or `genre` is empty, use `pop`. When `genres/<g>.md` does not exist, use `genres/pop.md` and say so in the declaration line.
3. **Read only the allowed files.** Exactly one role file, one contract, one genre file, and at most two technique files, as the Role Detection table lists for the detected role. This matches `defaults` in `references/shared/prompt-allowances.json` (`roles: 1, contracts: 1, genres: 1, techniques: 2`). Reading a fourth technique file, a second genre, or any rubric or persona is a protocol violation; `audit_agent_prompt.py` denies the dispatch when it lands.
4. **Build the prompt** from `references/agent-prompts/<task>.md`, where `<task>` is `hook`, `section`, or `revision`. Substitute every `{placeholder}` with file contents or values. Leave no bracket unfilled.
5. **Embed the originality clause.** Paste the fenced block from `references/shared/originality-policy.md` verbatim directly under the `<!-- originality-policy -->` marker. This block is exempt from the allowance count and is never summarised.
6. **Embed memory lessons** when `song-flow` supplies them: paste the lessons block (at most 10 lines) under the `<!-- memory-lessons -->` marker. When none are supplied, write `(none)` under the marker. Never read `.song/memory/` directly.
7. **Embed inputs.** `brief.md` always; `structure.md` for `verse-writer` and `lyric-editor`; `concept.md` for `verse-writer` and `lyric-editor`; the previous `lyrics.md` plus the critique and gate JSON for `lyric-editor`.
8. **Dispatch** with the Agent tool, `subagent_type: "lyricist"`, and the built prompt. The named agent exists so the `SubagentStop` gate hook matcher fires. Dispatch exactly one sub-agent per task; never dispatch two roles in parallel for the same artifact.
9. **Return the hand-back verbatim.** Relay the `SKILL_LOADED`, `STATUS`, `ARTIFACT`, and `SUMMARY` lines exactly as the sub-agent wrote them. Add nothing, reorder nothing, and run no gate script yourself; `song-flow` step 4 is the only gate runner.

Artifact path per role:

| Role | Writes | Overwrites |
|------|--------|------------|
| `hook-writer` | `.song/<slug>/concept.md` | yes, on re-dispatch after a hook-judge critique |
| `verse-writer` | `.song/<slug>/lyrics.md` | yes, on the first Stage 4 pass only |
| `lyric-editor` | `.song/<slug>/lyrics.md` | yes; cited sections only, passing lines preserved byte-for-byte |

Outside the pipeline (no `.song/config.yml`), write to the path the user names, else `./lyrics.md` or `./concept.md` in the working directory.

---

## Output Contract

Each role has exactly one contract. The contract is the only description of the artifact the sub-agent sees, so it is complete on its own.

| Role | Contract | Artifact spec it restates | Gate scripts named in it |
|------|----------|---------------------------|--------------------------|
| `hook-writer` | `references/contracts/hook.md` | `concept.md` front-matter: `title`, `hook_line`, `central_image`, `arc`, `title_rationale` | `cliche_scan.py`, `prosody_check.py --hook` |
| `verse-writer` | `references/contracts/section-lyric.md` | `lyrics.md`: `[Label]` tags identical to `structure.md`, one lyric line per `meter_spec` line, rhyme scheme honoured | `prosody_check.py`, `rhyme_check.py`, `cliche_scan.py` |
| `lyric-editor` | `references/contracts/revision.md` | `lyrics.md` revised in place; before/after table in `SUMMARY` | `prosody_check.py`, `rhyme_check.py`, `cliche_scan.py` |

The normative artifact grammar is `references/shared/artifact-formats.md`; the normative gate rules are `references/shared/stage-gates.md`. A contract restates them for one role and never contradicts them. When a contract and `stage-gates.md` disagree, `stage-gates.md` wins and the contract is a defect.

Every contract forbids: real artist names, real song titles, quoted or closely paraphrased existing lyrics, "sounds like" comparisons, and any phrase on `references/shared/cliche-list.txt` beyond the configured density.

---

## Hand-off

The sub-agent's hand-back goes to `song-flow`, which runs the stage protocol (`stage-gates.md` section 4). What happens next, per role:

| After | song-flow runs | On FAIL, critic | Re-dispatch role |
|-------|----------------|-----------------|------------------|
| `hook-writer` (Stage 2) | `cliche_scan.py concept.md`; `prosody_check.py --hook concept.md brief.md` | `song-critic:hook-judge` | `hook-writer` with the critique |
| `verse-writer` (Stage 4) | `prosody_check.py lyrics.md structure.md brief.md`; `rhyme_check.py lyrics.md structure.md`; `cliche_scan.py lyrics.md` | `song-critic:prosody-judge` | `lyric-editor` with the critique |
| `lyric-editor` (Stage 4 loop) | the same three scripts | `song-critic:prosody-judge` | `lyric-editor` again until `loops.lyrics` is exhausted |

A stage passes only when every script returns PASS or SKIPPED. SKIPPED (non-English `language`) proceeds as PASS and is logged.

**What a critique looks like on re-dispatch.** `song-flow` pastes two things under `## Critique to address`: the critic's prose (every item cites a `violations[].location` such as `Verse 2:3`) and the raw gate JSON:

```json
{ "script": "prosody_check", "status": "FAIL",
  "thresholds": { "prosody_tolerance": 0.15 },
  "metrics": { "verse_2_mismatch_ratio": 0.22, "syllable_mismatch_lines": 1 },
  "violations": [ { "location": "Verse 2:3", "reason": "stress mismatch", "observed": 0.22, "limit": 0.15 } ] }
```

The `lyric-editor` revises only the sections named in `violations[].location`, keeps every other line byte-identical, and reports a before/after table so the critic reads the diff rather than the whole lyric.

**Loop exhaustion.** When `loops_used.lyrics` reaches `loops.lyrics`, `song-flow` applies `escalation.on_loop_exhaustion` (`ask_user`, `accept_best`, or `fail`). The lyricist takes no part in that decision and never argues for an override.

**Downstream consumers.** `composer:melody` reads `lyrics.md` to write `w:` lines in `melody.abc`; `song-release` copies it into `package/lyric-sheet.md`; `song-critic:challenger` scans it at Stage 7b. Every one of them depends on the `[Label]` tags matching `structure.md` exactly, which is why the contracts treat a tag mismatch as a hard error rather than a style note.

---

## References

- `references/roles/` — hook-writer, verse-writer, lyric-editor (L2)
- `references/contracts/` — hook, section-lyric, revision (L2)
- `references/genres/` — pop, country, folk (L3; more land in Wave 5)
- `references/techniques/` — prosody, rhyme-schemes, hook-craft, imagery-and-specificity, cliche-avoidance, point-of-view, narrative-arc (L3)
- `references/agent-prompts/` — hook, section, revision (prompt skeletons per Appendix B of the plan)
- `song-team/references/shared/` — originality policy, stage gates, artifact formats, cliché list (read by song-flow; embedded, never loaded here)
