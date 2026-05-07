<!-- run: run-2026-05-05-tk3 | stage: 05-plan | depth: light | author: QA Engineer (Peregrin "Pippin" Took) | role: qa-engineer | task: test-strategy -->

# Test Strategy — Caveman-Lite Prose Discipline (run-2026-05-05-tk3)

> "But what about second breakfast? Elevenses? Luncheon? Afternoon tea?"
> — Pippin, refusing to leave a meal — or an AC — uncovered.

Light depth. TARGET-state framing — what Stage 6 Dev DoD will run to verify Story 1, not what passes today on `main`.

## Scope

**In**: 13 Story-1 ACs, 6 BACKLOG-102 initiative ACs, 3 PRD FRs (FR-1 PROSE STYLE block, FR-2 verdict-prose, FR-3 schema bump), 6 ADR-tk3-001 contract elements. **Out**: Tier 2/3 surfaces (PRD/ADR/release-notes/CLAUDE.md prose); per-role overrides; full/ultra caveman ladder.

## Coverage Map (FR / WI / AC traceability — ZERO gaps)

| FR | WI | Story-1 AC(s) | Initiative AC | Test Case | Verification (canonical paths) |
|---|---|---|---|---|---|
| FR-1 | W2-1 | S1, S2, S3 | AC-1, AC-5 | TC-2, TC-4 | `grep -c "^PROSE STYLE: caveman-lite for narrative-framing prose ONLY" delivery-team/skills/delivery-flow/references/pipeline-stages.md` → `3`; `grep -c "Auto-clarity exemptions apply" …pipeline-stages.md` → `3`; `grep -nE "PROSE STYLE\|prose_style" delivery-team/skills/delivery-flow/SKILL.md` ≥1 in L329-345 |
| FR-2 | W2-2 | S1, S2, S3 | AC-2, AC-3 | TC-3 | `grep -nE "STATUS:.*(DONE\|NOT_DONE\|CODE_COMPLETE)" delivery-team/skills/delivery-flow/references/quality-gates.md` matches L21-38 verbatim; `grep -c "caveman-lite" …quality-gates.md` ≥1; `grep -nE "file/line/criterion\|name file" …quality-gates.md` preserved |
| FR-3 | W2-3 | S1, S2, S3, S4 + Phase 0 wiring | AC-6 | TC-1, TC-5, TC-6 | `grep -n "^## Current Version: 2.9" …config-schema.md` on L5; `grep -nE '^\| `prose_style`' …config-schema.md` returns one row; `grep -n '^\| 2.9 ' …config-schema.md` returns one Version History row dated 2026-05-05; `python3 -c "import json; d=json.load(open('…/config-schema.json')); assert 'prose_style' in d['properties']; assert d['properties']['config_version']['default']=='2.9'"` exits 0; `grep -nE "prose_style" …/SKILL.md` ≥1 in L56-89 |
| cross | — | AC-CACHE-PREFIX | (NFR-1) | TC-7 | `sha256sum delivery-team/skills/delivery-flow/SKILL.md` = `governance/cache-prefix-hash.txt` line 1; same PR |
| cross | — | AC-TIER-A-BUDGET | (Ruling 3) | TC-8 | `python3 delivery-team/scripts/check_skill_budgets.py` exits 0; `wc -l SKILL.md` ≤500 |
| cross | — | AC-INITIATIVE-GATES | AC-1, AC-2, AC-3, AC-4 | Empirical Protocol §below | telemetry-driven post-merge |

**Gap audit**: every Story-1 AC, every initiative AC, every PRD FR maps to ≥1 TC. **Zero gaps**. Pippin satisfied.

## Test Cases (8, light depth)

- **TC-1 — Phase 0 reads `prose_style` at startup** (W2-3 / FR-3 / ADR Element 1): `grep -nE "prose_style" delivery-team/skills/delivery-flow/SKILL.md | awk -F: '$2>=56 && $2<=89'` → ≥1 line referencing `config.prose_style` load; default applied when key absent.

- **TC-2 — PROSE STYLE block injected post-ALIAS pre-OUTPUT in all 3 dispatch templates** (W2-1 / FR-1 / ADR Element 2): three `grep -c` commands above return `3`; plus `grep -nE "^--- (ALIAS\|PROSE STYLE\|OUTPUT) ---" …/pipeline-stages.md` → 9 lines, ordered ALIAS→PROSE STYLE→OUTPUT in three template blocks (L44, L87, L130 anchors).

- **TC-3 — DoD validator template directs caveman-lite verdict prose; STATUS verbatim; FINDINGS preserved** (W2-2 / FR-2 / ADR Element 4): three FR-2 grep commands above; plus synthetic dispatch on a fixture review with `prose_style: caveman-lite` → transcript at `.delivery/artifacts/06-development/dogfood/dod-validator-caveman-lite.md` shows verdict prose ≤3 sentences, STATUS line literal, FINDINGS bullets each name file/line/criterion.

- **TC-4 — Auto-clarity exemption: destructive-op dispatch produces standard prose** (W2-1 / BACKLOG-102 AC-5 / ADR Element 3): with `prose_style: caveman-lite`, run 3 synthetic dispatches — security warning, `git revert` confirmation, 4-step migration sequence. Capture: `.delivery/artifacts/06-development/dogfood/auto-clarity-{1,2,3}.md`. Expect: PROSE STYLE block present in dispatch prompt; narrative output is standard prose for all 3/3. Any fragment-prose in security/destructive/multi-step narrative → BACKLOG-102 stop-rule fires.

- **TC-5 — Opt-out: `prose_style: standard` reverts behavior** (W2-3 / BACKLOG-102 AC-6 / ADR Element 1): edit `.delivery/config.yml` → `prose_style: standard`; restart pipeline; run 3 dispatches → `.delivery/artifacts/06-development/dogfood/optout-{1,2,3}.md`. Expect: PROSE STYLE block ABSENT from prompt (no `--- PROSE STYLE ---` delimiter); narrative prose matches pre-merge baseline (no compression artifacts). Restore `prose_style: caveman-lite` after.

- **TC-6 — Schema bump v2.8 → v2.9; v2.7 configs auto-default** (W2-3 / FR-3 / ADR Element 6): four FR-3 commands above, plus a synthetic v2.7 config (no `prose_style` key) loads cleanly and the orchestrator emits banner `Config upgraded from v2.7 to v2.9. New settings applied with defaults: prose_style=caveman-lite`.

- **TC-7 — Cache-prefix hash regenerated alongside Phase 0 edit** (cross-cutting / ADR Element 5 / NFR-1): `sha256sum delivery-team/skills/delivery-flow/SKILL.md | awk '{print $1}'` matches line 1 of `governance/cache-prefix-hash.txt`; `git log -1 --name-only --pretty=format: -- governance/cache-prefix-hash.txt delivery-team/skills/delivery-flow/SKILL.md` shows BOTH files in the same commit; hash differs from pre-edit value `9d4011d11e5b83321526c41ff79dd25c9186f4c659a745feb0c13f686205926f`.

- **TC-8 — Tier-A budget preserved post-edit** (cross-cutting / Ruling 3): `python3 delivery-team/scripts/check_skill_budgets.py` exits `0`; `wc -l delivery-team/skills/delivery-flow/SKILL.md | awk '{print $1}'` ≤ `500`. Pre-edit baseline 497 lines; ADR caps Phase 0 edit at +3 max.

## Test Data

- **Theme alias**: existing `lotr` — no new alias bundles.
- **Synthetic dispatch fixtures**: fresh sub-skill agent context per dispatch; rotate role across primary / supporting / DoD-validator templates to exercise all three insertion points.
- **Pre-merge baseline telemetry**: last 5 dispatches in `.delivery/telemetry/skill-loads.jsonl` from Wave 2 archive `.delivery/memory/archive/run-2026-05-05-tk2.md` (predecessor commit c2e7d5a). Dispatch IDs entering the baseline get recorded in `w2-1-implementation.md` per PRD §8.1.
- **DoD review baseline**: byte-length sample over `.delivery/artifacts/*/dod/*-review.md` from the same 5 pre-merge runs.
- **v2.7 fixture config**: synthetic `.delivery/config.yml.v2.7` (no `prose_style` key) — used in TC-6 migration check.
- **Destructive-op fixture prompts**: `.delivery/artifacts/05-plan/qa/fixtures/{security-warning,git-revert,four-step-migration}.md` — Stage 6 Dev creates these alongside dogfood transcripts.

## Empirical Measurement Protocol (post-merge dogfood)

Telemetry-grade evidence for AC-1 (≥20% prose-token reduction) and AC-2 (≥25% DoD review reduction). Bash + python3 stdlib only — no `jq`/`xq`/`yq` (NFR-5).

**AC-1 — response-prose token reduction ≥20%**:

1. Pre-merge baseline (last 5 rows from predecessor runs):
   ```
   python3 -c "import json; rows=[json.loads(l) for l in open('.delivery/telemetry/skill-loads.jsonl')]; pre=[r['response_prose_tokens'] for r in rows if r.get('run_id','').startswith(('run-2026-05-05-tk2','run-2026-05-04-tk1'))][-5:]; print('pre_mean=',sum(pre)/len(pre))"
   ```
2. Post-merge sample: same one-liner with `run_id` prefix `run-2026-05-05-tk3` after Story 1 lands; trigger 5 dispatches against routine pipeline work.
3. Compute: `reduction = (pre_mean - post_mean) / pre_mean ≥ 0.20`. If `< 0.15` → BACKLOG-102 stop-rule fires; pause Tier-2; root-cause retro.

**AC-2 — DoD review file size reduction ≥25%**: `find .delivery/artifacts -path '*dod/*-review.md' -print0 | xargs -0 wc -c` over 5 pre-merge vs 5 post-merge reviews; mean-byte reduction ≥0.25; same stop-rule on <0.20.

**AC-3 — DoD pass-rate preserved**: `grep -h '^STATUS: DONE' .delivery/artifacts/*/dod/*-review.md | wc -l` divided by total validator dispatches (7 per run); threshold ≥`4/7` first-try (matches `memory/index.md` baseline). Any post-merge review missing a finding that Wave 2 flagged → over-compression failure → stop-rule fires.

**AC-4 — downstream artifact quality**: next pipeline run's PRD/ADR/release-notes reads complete without re-reads or clarification dispatches; UAT spot-checks transcript bytes.

**AC-5 / AC-6**: covered by TC-4 / TC-5 transcripts; binary pass/fail.

## Risk Areas (3, ranked by likelihood × impact)

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| **Cache-prefix hash forgotten** — Phase 0 edit lands without `governance/cache-prefix-hash.txt` regen; CI hash-check fails | medium | high (blocks merge) | TC-7 enforces same-PR commit; Story 1 DoD lists `sha256sum > governance/cache-prefix-hash.txt` explicitly. |
| **Schema-JSON drift** — `config-schema.md` edited but `config-schema.json` not regenerated via `generate-schema.py` | medium | medium (Phase 0 config-load fails next run) | TC-6 python `json.load` assertion catches drift; Story 1 DoD lists `python3 delivery-team/scripts/generate-schema.py` explicitly. |
| **Auto-clarity false-positive** — agent over-applies caveman-lite to security/destructive/multi-step prose; finding masked or warning compressed | low-medium | high (NFR-7 regression; user safety) | TC-4 covers all 3 exempt contexts; ADR Element 3 in-prompt directive names exemptions verbatim; BACKLOG-102 stop-rule armed on any 1/3 failure. |

## Entry / Exit Criteria

**Entry**: ADR-tk3-001 accepted; Stage 5 stories.md emitted; baseline telemetry rows present in `.delivery/telemetry/skill-loads.jsonl`.

**Exit (Stage 6 Dev DoD)**: TC-1..8 all pass; AC-1 / AC-2 thresholds met on post-merge dogfood; AC-3 no regression; AC-4 deferred to UAT next-run read; AC-5 / AC-6 transcripts captured and clean.

---

STATUS: DONE
