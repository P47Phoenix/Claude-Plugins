# Developer DoD Review — Stage 4 Architect (LIGHT), Round 1

**Pipeline**: run-2026-05-05-tk3
**Role**: developer (DoD reviewer — RUNS-THE-COMMAND)
**Stage**: 4 (Architect, light)
**Reviewer dispatch**: FRESH (no prior-loop context)
**Artifacts under review**:
- `.delivery/artifacts/04-architect/adrs/ADR-tk3-001-prose-style-config.md`
- `.delivery/artifacts/04-architect/solution/architecture-tk3-caveman-lite.md`
**Lens**: developer, light, blocking-only
**Prose style**: standard

---

## STATUS

**STATUS: NOT_DONE**

Two blocking developer-lens findings: (1) ADR Element 5's Phase 0 byte-offset claim is factually wrong by ~1794 bytes and the resulting reconciliation conclusion ("Phase 0 sits outside the 2KB prefix region; cache-warmup unaffected") is the inverse of reality; (2) ADR repeatedly mislocates Phase 0 as "L56-110" when the section header is at L31 and the section spans L31-125. Both contaminate the central architectural justification.

---

## Commands run (with stdout summary)

| # | Command | Stdout (summary) |
|---|---|---|
| 1 | `wc -l delivery-team/skills/delivery-flow/SKILL.md` | `497` (matches ADR's "497 of 500" Tier-A claim) |
| 2 | `wc -l delivery-team/skills/delivery-flow/references/{pipeline-stages,quality-gates,config-schema}.md` | `682, 288, 369` |
| 3 | `python3 -c "data=open('SKILL.md','rb').read(); print(data.find(b'## Phase 0'))"` | `1809` — `## Phase 0` heading lives at byte **1809**, NOT byte 3603 as ADR cites |
| 4 | `python3 -c "lines=...; offset of L56"` | `3529` — ADR's "byte 3603" appears to be a mis-derived offset for L56 (mid-Phase-0 body), NOT for Phase 0 start |
| 5 | `grep -n -E "(Primary\|Supporting\|DoD Validator) Dispatch Template" pipeline-stages.md` | L44, L87, L130 — all three anchors present at the exact lines cited in ADR Element 2 |
| 6 | `grep -n "ALIAS\|OUTPUT" pipeline-stages.md` (template insertion points) | ALIAS ends at L70/L113/L161; OUTPUT starts at L72/L115/L163 — matches ADR table exactly |
| 7 | `grep -nE "Current Version\|config_version\|Version History" config-schema.md` | L5 `## Current Version: 2.8`; L15 `Default: "2.8"`; L347 `### Version History`; v2.8 row present at L365; v2.9 absent — confirms ADR's v2.8-taken / v2.9-free claim |
| 8 | `python3 scripts/check_skill_budgets.py 2>&1; echo $?` | exit `0`; `BUDGET CHECK PASSED: 13 file(s) checked, 7 known-debt, 0 exception(s)` — current state has no overage; SKILL.md at 497/500 |
| 9 | `cat governance/cache-prefix-hash.txt` | `9d4011d11e5b83321526c41ff79dd25c9186f4c659a745feb0c13f686205926f` — ADR cites this exact hex prefix in Element 5; whole-file SHA-256 |
| 10 | `sha256sum delivery-team/skills/delivery-flow/SKILL.md` | `709808547fe9c28963355c7ce5c39a00eb59ccf4520399cec1bab2c3ad7a0d00` — does NOT match stored hash; pre-existing drift, NOT introduced by this ADR (out of this gate's scope per memory binary-status rule + TARGET vs CURRENT framing) |
| 11 | `python3` cumulative-byte math: L1-110 sum | `8360` bytes — exactly matches ADR Element 5 table cell "L1-110 cumulative: 8360" |
| 12 | `python3` L56-110 byte sum | `4831` bytes — exactly matches ADR Element 5 table cell "Phase 0 section L56-110: 4831" (sub-range math holds, but the SECTION LABEL is wrong — see Finding 2) |
| 13 | `grep -nE "^# \|^## " SKILL.md` | Phase 0 heading at L31, Phase 1 at L126; **Phase 0 actually spans L31-125**, not L56-110 |
| 14 | `grep -n "Volatile\|prefix\|2048" SKILL.md` | L478: "the prefix boundary sits at the end of Phase 3 (Stage Routing)" — semantic boundary is "end of Phase 3", not just bytes 0..2048. Phase 0 is *inside* this region by both interpretations |
| 15 | `python3 -c "print(1809 < 2048)"` | `True` — Phase 0 heading byte 1809 is **INSIDE** the documented 2KB prefix region |
| 16 | Math closure `497 + 3 = 500 ≤ 500` | True — Tier-A budget closes at TARGET state |
| 17 | `cat .claude/settings.local.json` for CLI deps | Only `WebSearch`, `flatpak list`, `git add` allowed; no `yq`/`xq`. ADR cites only `sha256sum`, `wc`, `grep`, `python3`, `awk` — all stdlib/coreutils. PASS |
| 18 | `grep` ADR Status line | `**Status**: Accepted` — exactly the binary token, no parenthetical |
| 19 | Cross-check `.delivery/memory/stages/architect.md` lesson on binary status | "ADR status must be binary (Proposed \| Accepted \| Deprecated)..." — memory rule honored by Status line |
| 20 | `grep -n "v2.8\|v2.9" config-schema.md Version History` | v2.8 row at L365 (DESIGN routing, dated 2026-04-05); v2.9 not yet present — ADR's "v2.8 taken; bump to v2.9" is correct |

---

## Findings (8 gate criteria)

### G1 — Phase 0 byte-offset claim verifiable — **NOT_PASS** (BLOCKING)

ADR Element 5 row 1 of byte-impact table: *"Phase 0 starts at byte 3603, after the prefix boundary"*. Architecture summary §4 repeats: *"Phase 0 (L56-110, bytes 3603-7625) sits outside the 2KB prefix region"*.

**Measured**: `## Phase 0: Setup Wizard` heading is at byte **1809** (L31). Delta from cited 3603 is **1794 bytes** — far outside ±100 tolerance. The mis-attribution appears to come from measuring L56 (the start of the *config-read implementation block*, byte 3529) and labeling it as "Phase 0 start". The downstream conclusion is inverted: byte 1809 IS inside the documented 0..2048 prefix region.

**Why blocking, not stylistic**: this isn't a typo — the byte number is the load-bearing premise of Element 5's reconciliation. Once corrected, the ADR's central conclusion ("cache-warmup behavior is preserved... mechanically satisfied without further action") flips. Either (a) the ADR must reframe Phase 0 as INSIDE the prefix region and treat the edit as a real cache-cost event with corresponding mitigation, or (b) the ADR must redefine the prefix region using the L478 SKILL.md comment's *semantic* anchor ("the end of Phase 3") and acknowledge bytes 0..2048 is documentation drift inside SKILL.md itself.

### G2 — SKILL.md line count claim accurate — **PASS**

`wc -l` returns 497. ADR cites "497 of 500 lines". Δ = 0, within ±2. PASS.

### G3 — 3 dispatch templates exist at cited line numbers — **PASS**

`grep -n` finds:
- `### Primary Agent Dispatch Template` at L44 (ADR cites L44; Δ=0)
- `### Supporting Agent Dispatch Template` at L87 (ADR cites L87; Δ=0)
- `### DoD Validator Dispatch Template` at L130 (ADR cites L130; Δ=0)

ALIAS/OUTPUT delimiter pairs at L70/L72, L113/L115, L161/L163 also match the ADR Element 2 insertion-point table exactly. PASS.

### G4 — Schema version-history confirms v2.8 taken; v2.9 free — **PASS**

`config-schema.md` L5 currently reads `## Current Version: 2.8`. L15 row defaults `config_version` to `"2.8"`. The Version History at L347 contains a v2.8 entry (DESIGN routing, dated 2026-04-05) and no v2.9 entry. ADR's W2-3 ratification ("schema MUST bump to v2.9, not v2.8") is exactly consistent with the file's current state. PASS.

### G5 — Phase 0 edit size (≤3 lines) preserves Tier-A budget — **PASS**

`python3 scripts/check_skill_budgets.py` exits 0 at HEAD (no current overage; SKILL.md at 497/500). TARGET-state math: 497 + ≤3 = ≤500, equality `497 + 3 = 500` closes. Budget ceiling met at the worst case. PASS. (Note: this is "is the math correct?" — pre-validating the actual edit is Stage 6's gate per the dispatch contract.)

### G6 — ADR status is BINARY — **PASS**

Status line at ADR L3 reads exactly `**Status**: Accepted` with no parenthetical, no "contingent on...", no qualifier. Memory `architect.md` lesson ("status must be binary; readers grepping for `Status: Accepted` will stop reading") is honored. PASS.

### G7 — Architecture batching math discipline — **PARTIAL FAIL** (BLOCKING)

Sub-range math closes:
- L1-110 cumulative: ADR says 8360, measured 8360. PASS.
- L56-110: ADR says 4831, measured 4831. PASS.
- Tier-A budget: 497 + 3 = 500. PASS.

But the **labels** for those sub-ranges are wrong. The ADR Element 5 table row labels L56-110 as "Phase 0 section" — but Phase 0 is L31-125. The arithmetic is correct on the cited line numbers; the **section identity** mapped to those line numbers is wrong. This propagates to architecture.md §4 ("Phase 0 (L56-110, bytes 3603-7625)") where both the line range and the byte range are mis-labeled.

**Per Wave 1 retro batching discipline**: math discipline isn't only equality closure — it's also that the labels on the table cells match what the prose claims. NOT_DONE.

### G8 — No new CLI deps — **PASS**

Verification commands cited in ADR (`sha256sum`, `wc -c`, `python3 delivery-team/scripts/generate-schema.py`) and architecture.md (`sha256sum > governance/cache-prefix-hash.txt`) all run with bash + coreutils + python3 stdlib. No `yq`, no `xq`, no fresh `jq`. `.claude/settings.local.json` allow-list confirmed: no MCP-only or unfamiliar binaries introduced. PASS.

---

## Verdict (≤3 sentences)

The ADR's contract surface is structurally sound — six elements are well-bounded, the dispatch templates exist where claimed, schema bump aligns with file state, status is binary, line-count and budget math close, and no new CLI deps are smuggled in. But Element 5's Phase 0 byte-offset claim (3603) is wrong by ~1794 bytes, which inverts the central reconciliation conclusion (Phase 0 is *inside* the documented 2KB prefix region, not outside), and the Phase-0-as-L56-110 mis-labeling propagates into the architecture summary. Stage 4 round 1 is **NOT_DONE**: ADR Element 5 needs a rewrite that either accepts Phase 0 IS in the prefix region (and adds explicit cache-cost mitigation) or redefines the prefix boundary using the SKILL.md L478 semantic anchor; architecture.md §4 needs the corresponding correction.

---

## STATUS

```
STATUS: NOT_DONE
ARTIFACT: .delivery/artifacts/04-architect/dod/developer-review.md
SUMMARY: Element 5 Phase 0 byte offset wrong (3603→actual 1809); Phase 0 is INSIDE the 2KB prefix region, inverting Element 5's reconciliation. Other 7 criteria mostly pass; section labels mislocate Phase 0 as L56-110.
```
