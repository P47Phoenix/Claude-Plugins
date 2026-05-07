# Architecture — Caveman-Lite Prose Discipline (run-2026-05-05-tk3)

**Stage**: 4 (Architect, light)
**Pipeline**: run-2026-05-05-tk3
**Author**: Solution Architect (Saruman of Many Colours)
**Depth**: light, single ADR
**Date**: 2026-05-05

> Filename note: this file is the canonical `architecture.md` for run-2026-05-05-tk3. It is namespaced (`architecture-tk3-caveman-lite.md`) to coexist with prior runs' artifacts in `.delivery/artifacts/04-architect/solution/` per the established convention (`architecture-tk0e-wave0.md`, `architecture-tk1-wave1.md`, `architecture-tk2-wave2.md`).

---

## 1. Engagement

This architecture summary covers run-2026-05-05-tk3, executing BACKLOG-102 (caveman-lite prose discipline). The PRD at `.delivery/artifacts/02-refine/po/prd.md` consolidates W2-1, W2-2, W2-3 into one Story; the architectural surface is small enough for a single ADR. ADR-tk3-001 ratifies six contract elements: the `prose_style` config key, the PROSE STYLE dispatch block (insertion point in three templates), auto-clarity exemptions (in-prompt directive mechanism), DoD validator verdict-prose treatment, the cache-prefix re-freeze procedure, and the schema bump v2.8 → v2.9.

## 2. System Boundary Diagram (text-based)

```
+--------------------------------------------------------------------+
|  .delivery/config.yml                                              |
|     prose_style: caveman-lite | standard   <-- Element 1, Element 6|
+----------------------------|---------------------------------------+
                             | (read once per pipeline invocation)
                             v
+--------------------------------------------------------------------+
|  delivery-flow/SKILL.md  Phase 0  (L31-125; W2-3 edit at L56-110)  |
|     load config -> store config.prose_style                        |
|     [Phase 0 heading byte 1803, INSIDE 0..2048 prefix slice;       |
|      one-time re-warm cost documented in ADR-tk3-001 Element 5]    |
+----------------------------|---------------------------------------+
                             | (in-memory loaded-config struct)
                             v
+--------------------------------------------------------------------+
|  delivery-flow/SKILL.md  Phase 4 Step 4  (L329-345)                |
|     prompt construction; if config.prose_style == caveman-lite     |
|     inject PROSE STYLE block; else omit section entirely           |
+----------------------------|---------------------------------------+
                             | (prompt rendered from template)
                             v
+--------------------------------------------------------------------+
|  references/pipeline-stages.md  dispatch templates                 |
|     Primary (L44)  | Supporting (L87)  | DoD Validator (L130)      |
|     PROSE STYLE block inserted between --- ALIAS --- and           |
|     --- OUTPUT --- in all three                                    |
+----------------------------|---------------------------------------+
                             | (Agent tool call)
                             v
+--------------------------------------------------------------------+
|  Sub-agent dispatch                                                |
|     - narrative-framing prose: caveman-lite                        |
|     - SUMMARY (<=200 char): caveman-lite                           |
|     - artifact body: standard prose                                |
|     - auto-clarity exempt contexts: standard prose (Element 3)     |
|        [security warnings | irreversible-op confirmations |        |
|         multi-step sequences | user clarifications]                |
+----------------------------|---------------------------------------+
                             | (response: signal block + prose)
                             v
+--------------------------------------------------------------------+
|  DoD validator review file (Element 4)                             |
|     STATUS: verbatim       | FINDINGS: standard prose              |
|     SUMMARY: caveman-lite  | gate-result tables: verbatim          |
|     verdict prose (<=3 sentences): caveman-lite                    |
+--------------------------------------------------------------------+
```

## 3. ADR Index

| ID | Title | Status | Path |
|---|---|---|---|
| ADR-tk3-001 | `prose_style` config key, PROSE STYLE dispatch contract, and cache-prefix re-freeze procedure | Accepted | `.delivery/artifacts/04-architect/adrs/ADR-tk3-001-prose-style-config.md` |

## 4. Cache-prefix impact summary

The repo carries two interpretations of the Ruling 1 cache-prefix freeze, and the Phase 0 edit invalidates both. Phase 0 spans L31-125 with its heading at byte 1803 — **inside** the documented 0..2048 prefix slice (SKILL.md L478). The W2-3 edit lands in the L56-110 config-read sub-block (the PRD §3 "L56-110" citation referred to that sub-range; the broader Phase 0 spans L31-125 — both readings are true at different scopes). Cache-warmup mechanics see a one-time ~2KB prefix re-read on the first post-merge dispatch, then re-warm normally; Ruling 1's "ADR citing cache-cost impact" requirement is discharged by ADR-tk3-001 Element 5, and the recurring AC-1/AC-2 token savings dwarf the bounded one-time cost. The operational guard in `governance/cache-prefix-hash.txt` is a **whole-file SHA-256** (current value `9d4011d…`); Stage 5 Plan stage MUST list `sha256sum delivery-team/skills/delivery-flow/SKILL.md > governance/cache-prefix-hash.txt` as an explicit Story DoD task, committed alongside the SKILL.md edit. Edits to `pipeline-stages.md`, `quality-gates.md`, `config-schema.md`, and `config-schema.json` do NOT trigger any separate re-freeze — they are different files, not under the SKILL.md hash guard. The Phase 0 edit is constrained to ≤3 lines because SKILL.md sits at 497 of 500 Tier-A budget; if more is needed, batch a same-wave reduction elsewhere per Architect batching math discipline (`.delivery/memory/stages/architect.md` lesson 5).
