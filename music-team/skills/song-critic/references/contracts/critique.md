---
loaded_by: song-critic
level: L2
last_reviewed: 2026-10-26
---

# Output Contract: critique

Artifact: `critiques/<stage>-<n>.md` (`<stage>` is the stage key such as `lyrics`; `<n>` the loop number). Written by a
judge (hook, prosody, music, structure, adaptation-fidelity). Read by the next worker dispatch as
`CRITIQUE TO ADDRESS`. No script validates it; the worker consumes it, so keep it mechanical and short.

## Grammar

```markdown
---
critic_role: prosody-judge
stage: lyrics
loop: 1
artifact: lyrics.md
gate_status: FAIL
---

## Fixes

| rank | location | why | fix | impact |
|------|----------|-----|-----|--------|
| 1 | Verse 2:3 | stress mismatch 0.22 vs limit 0.15 | move the stressed noun to beat 3 | prosody_check verse_2_mismatch_ratio |

## Rubric

| criterion | score | evidence |
|-----------|-------|----------|
| <name from the rubric file> | 4 | Chorus:2 lands on the beat |

## Notes
- FALSE-POSITIVE? <one line, at most one>
```

## Rules

1. **Front-matter.** `critic_role` is the dispatched role; `gate_status` is the status the gate JSON reported (copy it).
2. **Fixes table.** Exactly five columns. One row per gate violation, ranked by expected gate impact (1 first). `fix` is an instruction a worker can apply without asking; it never contains a replacement section. `impact` names the script metric it should move.
3. **Rubric table.** One row per rubric criterion (five), `score` an integer 1-5, `evidence` a location or metric. Scores inform; they never replace the gate.
4. **Notes.** Optional. At most one `FALSE-POSITIVE?` line, and any `ORIGINALITY?` line with its location.
5. **Length.** Under 60 lines. Quote at most six words of any user line. No artist or song names.
6. **Loop 2+.** Add a `## Previous fixes` section: one bullet per earlier fix, `applied` or `not applied`.

## Hand-back

```text
SKILL_LOADED: <paths>
STATUS: DONE | BLOCKED
ARTIFACT: <path of the critique>
SUMMARY: <one sentence, 200 characters or fewer; the top fix>
```

BLOCKED means the artifact or gate JSON was unreadable or provenance was missing; add `FINDINGS:` with the reason.
