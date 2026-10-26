---
loaded_by: song-critic
level: L2
last_reviewed: 2026-10-26
---

# Listener Panel

Stage 7a (cell F only). Advisory: it never gates and never loops. Three persona lenses read the final artifacts
and each votes KEEP or SKIP.

## Role -> Reference Mapping

| Role | Stage | Artifacts read | References (paste exactly three personas) |
|------|-------|----------------|--------------------------------------------|
| **listener-panel** | 7a | `concept.md`, `lyrics.md`, `arrangement.md` | `contracts/panel-report.md`; `personas/casual-radio-listener.md`, `personas/songwriter-peer.md`, `personas/genre-devotee.md` |

No genre section, no technique files. `quality.listener_panel_size` above 3 means one Agent call per persona.

## Detection Keywords

listener panel, panel, listener feedback, would people like this, first listen, audience reaction, focus group,
would you keep or skip

## Task Type Routing Table

| Request Signal | Task Type | References Loaded |
|---|---|---|
| `ROLE: listener-panel`; "listener panel", "listener feedback" | **panel** | panel-report.md, three persona files |

## Task Type Instructions

| Task Type | What the sub-agent does |
|---|---|
| **panel** | Read the artifacts. Take each persona in turn and answer only from that persona's lens (what it notices, what makes it skip). Write one `## <persona-name>` block with `verdict: KEEP` or `verdict: SKIP`, `top_note:` (one sentence, 200 characters or fewer, the single most useful observation) and `question:` (one open question for the writer). End with `majority: KEEP | SKIP (n of m)`. Write to `panel-report.md` |

## Guardrails

- **Advisory only.** Never say a gate passed or failed; never request a loop.
- **Personas stay distinct.** Do not copy a note from one block into another; if two personas agree, say why for each.
- **Evidence.** Each `top_note` names a section or a concrete moment, not "feels good".
- **Majority arithmetic.** Count the verdict lines; a tie goes to SKIP.
- **No lyric reproduction.** Quote at most six words per block. Name no artist or song.
- **Isolation.** Read only the paths given.
