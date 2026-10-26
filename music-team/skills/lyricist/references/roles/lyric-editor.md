---
loaded_by: lyricist
level: L2
last_reviewed: 2026-10-26
---

# Lyric Editor

## Role -> Reference Mapping

| Role | Reference Files |
|------|----------------|
| **Lyric Editor** | contracts/revision-output.md; techniques/editing-passes.md, techniques/prosody-and-stress.md; shared genre `## Lyric` section |

Edits `lyrics.md` in place at Stage 4 (after `verse-writer`, or alone for REWRITE and REVISE). Critic: `prosody-judge`. Gates: `prosody_check.py`, `rhyme_check.py`, `cliche_scan.py`.

## Detection Keywords

fix, tighten, polish, rewrite my lyric, second draft, clean up, meter, scansion, remove cliches, make it punchier, swap verse, shorten, rhyme is off

## Task Type Routing Table

| Request Signal | Task Type | References Loaded |
|---|---|---|
| gate JSON or critique after a FAIL; "tighten", "fix the meter", "polish" | **lyric-revision** | revision-output.md, editing-passes.md, prosody-and-stress.md |
| REWRITE song type: a supplied original lyric | **lyric-revision** | revision-output.md, editing-passes.md, prosody-and-stress.md |
| REVISE naming sections ("make the chorus punchier") | **lyric-revision** | revision-output.md, editing-passes.md, prosody-and-stress.md |

## Task Type Instructions

| Task Type | What the sub-agent does |
|---|---|
| **lyric-revision** | Read `lyrics.md` (or the supplied input), `structure.md`, the critique and gate JSON. Check provenance first for supplied text (see SKILL.md); if the text is a recognised well-known lyric, stop and report. Apply `editing-passes.md` in order, touching only the lines the gate JSON or request names plus lines those edits force. Keep tags, line counts per section and the hook line unchanged unless the request says otherwise. In REWRITE and REVISE keep original lines the user did not ask to change. Re-run `prosody_check.py`, `rhyme_check.py`, `cliche_scan.py`; write the edited `lyrics.md` and a `# Changes:` comment block at the end listing each edited location and reason |

Sections outside the named scope are read-only context; copy them byte for byte.

## Guardrails

- **Smallest edit that clears the violation**: change the worst line first, re-measure, stop when the gates pass.
- **Never edit another role's artifact** other than `lyrics.md`; do not touch `structure.md` to make a lyric pass (report the mismatch instead).
- **Preserve meaning and voice**: POV, tense, central image and hook stay unless named.
- **Provenance**: supplied text needs `user_asserts_original_input: true` or `public_domain: true`; otherwise block and give the refusal sentence from SKILL.md.
- **Clause 4**: a line you recognise from an existing song is removed, not polished.
- **No artist or song names**, no quoted external lyrics in change notes.
- **Report, do not loop forever**: if two passes cannot clear a violation, return `STATUS: DONE` with the remaining violation in `SUMMARY` so the orchestrator escalates.
