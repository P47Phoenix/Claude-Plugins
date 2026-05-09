<!-- run: run-2026-05-09-tk4 | stage: 4 (Architect, light) | DoD round: 1 | reviewer: Developer (RUNS-THE-COMMAND, FRESH dispatch) -->

# Developer DoD Review — Stage 4 Architect, Wave 3

**STATUS**: DONE
**Pipeline**: `run-2026-05-09-tk4`
**Stage**: 4 (Architect, LIGHT) — DoD round 1
**Reviewer**: developer skill (FRESH dispatch, runs-the-command)
**Binding**: per tk3 retro Hot Lesson #1 extension, cache-prefix-impacting ADRs (ADR-tk4-003) require Dev runs-the-command at DoD. This review honors that binding.

Artifacts under review:

- `.delivery/artifacts/04-architect/adrs/ADR-tk4-001-tier-b-closure-approach.md`
- `.delivery/artifacts/04-architect/adrs/ADR-tk4-002-paradigm-sub-skill-pattern.md`
- `.delivery/artifacts/04-architect/adrs/ADR-tk4-003-governance-frontmatter-shape.md`
- `.delivery/artifacts/04-architect/solution/architecture-tk4-wave-3.md`

---

## Commands run

1. `ls -la .delivery/artifacts/04-architect/{adrs,solution,dod}/` — confirmed all four artifact files exist on disk with timestamps from the current run.
2. `ls -la governance/ scripts/` — confirmed `governance/cache-prefix-hash.txt` and `governance/skill-budgets.json` exist; `scripts/check_skill_budgets.py` exists; `scripts/regenerate_cache_prefix_hash.py` does NOT exist.
3. `for f in <7 over-budget files>; do wc -l < "$f"; done` — verified line counts on all 7 SKILL.md files. Results match ADR-tk4-001 `before` column EXACTLY: architect 500, presentation 545, ui 496, operations 420, quality 418, user-feedback 399, godot 236.
4. `head -15` + `head -c 200 | od -c` on architect, presentation, godot SKILL.md — confirmed frontmatter sits at byte 0 (file begins with `---\nname:`).
5. `printf '<3 new keys>\n' | wc -c` and `wc -l` — exact byte cost of 3 frontmatter keys = **83 bytes / 3 lines** (ADR claimed ~50 bytes; ADR underestimates by ~33 bytes/file but conclusion intact).
6. `cat governance/cache-prefix-hash.txt` — current hash file is sha256sum format, scoped to `delivery-team/skills/delivery-flow/SKILL.md` only. Matches ADR-tk4-003 §"this wave expands the hash file's scope" claim.
7. `sha256sum delivery-team/skills/delivery-flow/SKILL.md` — confirmed current hash matches the recorded hash byte-for-byte. Re-freeze procedure is trivially achievable via `sha256sum <files> > governance/cache-prefix-hash.txt`.
8. `find . -maxdepth 4 -name "research-agent" -type d` + `ls research-agent/SKILL.md` — research-agent path resolves at top-level repo (`./research-agent/SKILL.md`), no `skills/` subtree yet (matches ADR-tk4-002).
9. `ls delivery-team/skills/{presentation,user-feedback,architect/paradigms}/` — presentation and user-feedback skill dirs exist; `architect/paradigms/{volatility,ddd}/` precedent exists (matches ADR-tk4-002 grandfathering claim).
10. `grep -m1 '^\*\*Status\*\*' <each ADR>` — all three ADRs report `**Status**: Accepted`. Binary, no parentheticals.
11. `grep -nE -i "(MUST|hard gate|sequenc|after.*W3-1|before.*W3-9|stories 1-4|story 5)" ADR-tk4-003 + architecture-tk4-wave-3.md` — sequencing recorded explicitly in BOTH artifacts (ADR lines 25, 61, 74, 76; architecture lines 25, 44, 47-58).
12. `sed -n` spot-checks on architect and godot — line-range citations in ADR-tk4-001 resolve precisely (`## Architecture Style and Decomposition from Config` at line 132, `## Software Architecture Roles` at line 231, `## Common Task Patterns` at godot line 151, `## Architecture Guardrails` at godot line 190).
13. `grep -nE '^\s*(```|    )?(python3?|sha256sum|grep|find|wc|...)\b' <ADRs>` — audited cited verification commands; all standard CLI tools (python3, grep, find, sha256sum, wc) already in environment.
14. `grep -n "skills/paradigms\|architect/paradigms" CLAUDE.md` — confirmed CLAUDE.md line 49 says `skills/paradigms/` while actual path is `paradigms/`; ADR-tk4-002's stale-doc claim is accurate.

---

## Gate evaluations

### Gate 1 — Per-file batching math closes for ALL 7 files: **PASS**

Verified `before` against ADR §3 table:

| File | ADR before | wc -l | match | ADR after | tier ceiling | within? |
|---|---:|---:|:-:|---:|---:|:-:|
| architect | 500 | 500 | YES | 288 | 300 (B) | YES |
| presentation | 545 | 545 | YES | ≈160 | 300 (B) | YES (broad margin) |
| ui | 496 | 496 | YES | 273 | 300 (B) | YES |
| operations | 420 | 420 | YES | 255 | 300 (B) | YES |
| quality | 418 | 418 | YES | 276 | 300 (B) | YES |
| user-feedback | 399 | 399 | YES | 250 | 300 (B) | YES |
| godot | 236 | 236 | YES | 198 | 200 (C) | YES (margin = 2) |

Per-file Δ arithmetic in ADR-tk4-001 §W3-1..W3-7 sums correctly in every case (e.g., architect: -76 -56 -30 -23 -27 = -212; 500-212 = 288). Godot's tight 2-line margin is acknowledged with a stated fallback (additional 5-line trim from `## Architecture Guardrails`).

### Gate 2 — All cited file paths resolve for 7 over-budget files: **PASS**

All 7 paths exist on disk with current line counts matching ADR claims (Gate 1 table). No path drift.

### Gate 3 — Frontmatter byte-impact math (ADR-tk4-003): **PASS WITH NOTE**

Sampled 3 SKILL.md files (architect, presentation, godot):

- All begin with `---\nname:` at byte 0; frontmatter is unambiguously at the cache-prefix region.
- Existing frontmatter blocks span ~10 lines; adding 3 keys is a clean append.
- **Exact** byte cost of the 3 cited keys (`maintainer: delivery-team-leads\nfitness_review_due: 2026-08-09\ncontext_budget: 300\n`) = **83 bytes**, not the ADR's stated ~50 bytes. ADR uses ~17 bytes/line average; actual is closer to ~28 bytes/line for these specific keys.
- Cumulative impact at 13 files: actual ≈ **1,080 bytes**, not 650 bytes. Still well within the 2,048-byte cache-prefix region; conclusion (one-time re-warm, scoped, justified) is intact.

NOTE: Stage 6 DoD must cite ACTUAL byte counts after rollout (the ADR itself mandates this in §"Procedure" item 3 — "MUST cite the regenerated hash file's actual byte counts, NOT the +650-byte projection"). The architect's projection is OPTIMISTIC but the binding is correct.

### Gate 4 — Cache-prefix re-freeze procedure inspectable: **PASS WITH NOTE**

- `governance/cache-prefix-hash.txt` exists, contents inspectable, currently 1 line covering `delivery-team/skills/delivery-flow/SKILL.md` only — matches ADR's "expands the hash file's scope" claim.
- Hash format = sha256sum (verified by `sha256sum delivery-team/skills/delivery-flow/SKILL.md` matching the file's recorded hash byte-for-byte).
- Regeneration is trivially achievable: `sha256sum delivery-team/skills/*/SKILL.md delivery-team/skills/architect/paradigms/*/SKILL.md > governance/cache-prefix-hash.txt`.

NOTE: ADR-tk4-003 §Procedure cites `python3 scripts/regenerate_cache_prefix_hash.py --target ... --files ...` but this script does **NOT** exist in `scripts/` (only `check_skill_budgets.py` is present). The ADR's parenthetical fallback ("Or the equivalent enumeration of all 13 SKILL.md files") covers this — Stage 6 must either create the script OR record the actual `sha256sum` invocation used. Procedure is recoverable without architectural change. Not a blocker for Architect DoD because the procedure intent and target file are both well-specified; the script reference is a forward-looking placeholder.

### Gate 5 — ADR-tk4-002 paradigm pattern locations correct: **PASS**

- `research-agent/SKILL.md` resolves at top-level repo (`./research-agent/SKILL.md`, 17,746 bytes); no `skills/` subtree yet — matches ADR's "verified path: top-level repo `/research-agent/SKILL.md`, no `skills/` subtree yet".
- `delivery-team/skills/presentation/` resolves; SKILL.md present.
- `delivery-team/skills/user-feedback/` resolves; SKILL.md present.
- `delivery-team/skills/architect/paradigms/{volatility,ddd}/` resolve as the grandfathered precedent.
- CLAUDE.md line 49 says `skills/paradigms/` (stale per ADR's claim); actual path is `paradigms/`. ADR's stale-doc note is accurate; W3-12 fix scope correctly cited.

### Gate 6 — All 3 ADR Statuses BINARY: **PASS**

| ADR | Status |
|---|---|
| ADR-tk4-001 | Accepted |
| ADR-tk4-002 | Accepted |
| ADR-tk4-003 | Accepted |

No parentheticals. No "Accepted (pending …)" anti-pattern. Binary in all three.

### Gate 7 — No new CLI deps in cited verification commands: **PASS**

All cited tools (`python3`, `grep`, `find`, `wc`, `sha256sum`) are standard and present in the environment. The single non-standard reference (`scripts/regenerate_cache_prefix_hash.py`) is a procedure forward-reference and does not introduce a new CLI dependency — it relies on `python3` plus a script that does not yet exist (see Gate 4 NOTE).

### Gate 8 — Mandatory-rollout sequencing recorded: **PASS**

Sequencing is recorded EXPLICITLY in both required artifacts:

- ADR-tk4-003 line 25: "W3-9 MUST run AFTER W3-1..W3-7 content trims, because adding ~3 lines to a file already AT-budget pushes it over."
- ADR-tk4-003 line 76: "W3-9 MUST NOT begin until W3-1..W3-8 have landed in the working tree. … This sequencing is a **hard gate** — NOT a soft preference."
- ADR-tk4-003 §"Mandatory-rollout sequencing (binding Wave 0 lesson)" is a dedicated subsection.
- architecture-tk4-wave-3.md line 44: ASCII boundary diagram explicitly labels "HARD GATE — Stories 1-4 must land in working tree first" between content trims and Story 5 (W3-9).
- ADR-tk4-001 §"Sequencing with ADR-tk4-003" reciprocates the gate from the trim-side.

Sequencing is recorded in three places, with consistent language ("hard gate"), and traces back to the Wave 0 mandatory-rollout-side-effect lesson.

---

## Summary scorecard

| Gate | Result |
|---|---|
| 1. Per-file batching math closes for all 7 files | PASS |
| 2. All cited file paths resolve | PASS |
| 3. Frontmatter byte-impact math | PASS WITH NOTE (ADR projection optimistic by ~430 bytes total; conclusion intact) |
| 4. Cache-prefix re-freeze procedure inspectable | PASS WITH NOTE (cited python script doesn't exist; sha256sum fallback is trivial) |
| 5. ADR-tk4-002 paradigm path claims correct | PASS |
| 6. All 3 ADR Statuses BINARY | PASS |
| 7. No new CLI deps | PASS |
| 8. Mandatory-rollout sequencing recorded | PASS |

---

## Verdict

All eight gates pass; two carry forward-looking notes that Stage 6 must honor (cite actual byte counts after rollout, and either create or substitute the `regenerate_cache_prefix_hash.py` script with an equivalent `sha256sum` enumeration). The contracts in all three ADRs and the architecture summary are well-formed and runs-the-command verifiable, with line counts, paths, and sequencing all confirmed empirically against the working tree.

**STATUS: DONE.**

— developer (FRESH dispatch, runs-the-command), DoD round 1, run-2026-05-09-tk4
