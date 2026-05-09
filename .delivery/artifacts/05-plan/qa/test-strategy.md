<!-- run: run-2026-05-09-tk4 | stage: 05-plan | depth: light | author: QA Engineer (Pippin Took) | sources: stories.md, prd.md, ADR-tk4-{001,002,003}, BACKLOG-104, architecture-tk4-wave-3.md | wave: 3 — closure -->

# Test Strategy — Wave 3 (run-2026-05-09-tk4, BACKLOG-104 closure)

> "But what about second breakfast? And the stop-rule? And the godot ceiling? Has anyone counted the bytes after the frontmatter goes on?"
> — Pippin, asking the questions the others were too tall to notice. Round 2: I miscounted to seven and the tall folk were right to send me back. Ten init ACs, not seven.

Sixteen test cases. Seven stories. Fifty-two acceptance lines (7 PRD FRs + 10 initiative ACs + 35 story ACs). Zero gaps in the coverage map. The road is mapped; the gates are sharp; the small folk verify everything that the tall folk took on faith.

## Scope

**In**: per-file extraction verifications (Stories 1–3); paradigm sub-skill structural verification (Story 4); frontmatter rollout + cache-prefix re-freeze + post-rollout budget verification (Story 5); CLAUDE.md ≤150 + retro KPI integration (Story 6); validator template + STATUS standardization + JSON↔Python lint + Stage-7 stale-sweep + telemetry hardening (Story 7); cumulative ≥50% reduction telemetry close-out (NFR-4 / AC-7 / AC-13 caveman-lite carry-forward); tripwire activation verification.

**Out**: language-level unit tests for refactored markdown (no behavior change in Python beyond the new lint scripts; those are tested in TC-5/TC-6/TC-12); other-plugin Tier-B/C debt (deferred to BACKLOG-105+); presentation paradigm if Stage 6 selects references-only (covered by TC-4 conditional path); developer + architect 11-role paradigm (BACKLOG-106+).

## Coverage Map (FR/AC ↔ TC traceability — zero gaps)

| Source | ID | Topic | TC IDs |
|---|---|---|---|
| PRD FR-1 | Story 1 architect Tier-B closure | extraction + router | TC-1 |
| PRD FR-2 | Story 2 presentation/ui/operations trims | parallel extractions + router | TC-2 |
| PRD FR-3 | Story 3 quality/user-feedback/godot trims | extraction + godot ≤197 | TC-3 |
| PRD FR-4 | Story 4 paradigm sub-skill pattern | sub-skill structure + lint | TC-4 |
| PRD FR-5 | Story 5 governance frontmatter rollout | frontmatter + budget + cache | TC-5, TC-6, TC-7 |
| PRD FR-6 | Story 6 retro KPI + fitness + CLAUDE.md | KPI + line-count + governance doc + workflow | TC-8, TC-9, TC-15, TC-16 |
| PRD FR-7 | Story 7 admin carry-forwards | validator + STATUS + JSON↔Py + sweep + telemetry | TC-10, TC-11, TC-12, TC-13, TC-14 |
| BACKLOG-104 init AC-1 | empty `known_debt[]` post-Wave-3 | TC-6 |
| BACKLOG-104 init AC-2 | CLAUDE.md ≤150 | TC-8 |
| BACKLOG-104 init AC-3 | governance frontmatter on every SKILL.md | TC-5 |
| BACKLOG-104 init AC-4 | 4 Wave-2 carry-forwards discharged | TC-10, TC-11, TC-12 |
| BACKLOG-104 init AC-5 | 2 caveman-lite carry-forwards + DEFECT-006 close | TC-13, TC-14 |
| BACKLOG-104 init AC-6 | paradigm pattern ≥3 axes | TC-4 |
| BACKLOG-104 init AC-7 / NFR-4 | ≥50% cumulative reduction | Empirical Measurement Protocol |
| BACKLOG-104 init AC-8 | no DoD pass-rate regression (NFR-5) | DoD Pass-Rate Regression Protocol (Stage 7 dogfood; runnable from `.delivery/memory/archive/*.md`) |
| BACKLOG-104 init AC-9 | defects/story rolling 3-PR window ≤0.4 (NFR-6 / stop-rule) | Defects-Per-Story Rolling Window Protocol (Stage 7 dogfood; runnable PR-history query) |
| BACKLOG-104 init AC-10 | quarterly fitness review process operational (governance doc + scheduled GH Action live) | TC-15, TC-16 |
| Story 1 ACs (5) | W3-1 budget/exception, router 11/11, cache, refs present | TC-1, TC-7 |
| Story 2 ACs (5) | W3-2/3/4 wc + 16 router inputs + budget exit-0 | TC-2 |
| Story 3 ACs (5) | W3-5/6/7 wc, godot ≤197 (zero-headroom), router 15 | TC-3 |
| Story 4 ACs (5) | sub-skill find + frontmatter + lint + cache + conditional | TC-4 |
| Story 5 ACs (5) | lint + budget + cache regen + sequencing + tripwire | TC-5, TC-6, TC-7, Tripwire Activation Protocol |
| Story 6 ACs (5) | AC-1 KPI → TC-9; AC-2 governance doc → TC-15; AC-3 workflow + cron + injection-lint → TC-16; AC-4 CLAUDE.md ≤150 → TC-8; AC-5 stale-path side-fix → TC-8 | TC-8, TC-9, TC-15, TC-16 |
| Story 7 ACs (5) | validator template + CI + STATUS-grep + hook + DEFECT-006 + telemetry | TC-10, TC-11, TC-12, TC-13, TC-14 |

**Tally**: 7 PRD FRs + 10 initiative ACs + 35 story ACs = **52 source lines** mapped to 16 TCs + 4 Protocols (Empirical Measurement, Tripwire Activation, DoD Pass-Rate Regression, Defects-Per-Story Rolling Window). **Zero unmapped lines**; PO Plan-memory-lesson-2 satisfied (round-2 corrected denominator: 10 init ACs verified at BACKLOG-104 lines 280-289, not 7).

## Test Cases (16)

| ID | Title | Trigger | Command / Procedure | Expected Result |
|---|---|---|---|---|
| TC-1 | Per-file extraction verification (architect) | post-Story-1 | `wc -l delivery-team/skills/architect/SKILL.md`; `grep -c "references/roles" SKILL.md`; spot-check 11/11 router | wc returns ≤297 (canonical) OR ≤308 with `Budget-Exception: ADR-tk4-001` AND `known_debt[].W3-1-residual` present; refs grep ≥11; routing tables resolve correct role manifest |
| TC-2 | Triple-trim parallel verification (Story 2) | post-Story-2 | `wc -l` on presentation/ui/operations SKILL.md; replay 9+4 + 3 + 3 = 19 dogfood router inputs | All three ≤297; presentation type 9/9 + format 4/4; ui designer 3/3; ops 3/3; sub-agent loads ONLY matched references |
| TC-3 | Triple-trim verification (Story 3; godot critical) | post-Story-3 | `wc -l delivery-team/skills/{quality,user-feedback,godot}/SKILL.md`; verify godot exactly ≤197 | quality ≤276, user-feedback ≤250, **godot ≤197 (binding; round-2 zero-headroom)**; `git diff --name-only` shows Wave-2 godot refs untouched; quality 7/7 + user-feedback 4/4 + godot 4/4 router inputs route correctly |
| TC-4 | Paradigm sub-skill structure verification | post-Story-4 | `find research-agent -path "*/skills/research-types/*/SKILL.md" \| wc -l` (≥5); `find delivery-team/skills/user-feedback -path "*/skills/personas/*/SKILL.md" \| wc -l` (=4); `grep -L "disable-model-invocation: true"` on each | research-agent ≥5 + user-feedback =4 sub-skills; ALL contain `disable-model-invocation: true`; presentation conditional path: telemetry decision recorded (a) 9 sub-skills present + 9/9 router OR (b) defer cite recorded in PR body; marketplace lint excludes top-level SKILL.md |
| TC-5 | Frontmatter add verification (Story 5) | post-Story-5 | `grep -L "^maintainer:" $(find delivery-team -name SKILL.md)` returns empty; `python3 scripts/lint_skill_frontmatter.py` exits 0 | All 13+ delivery-team SKILL.md have `maintainer:` + `fitness_review_due:` (ISO-8601) + `context_budget:` (matches tier A=500/B=300/C=200); deliberately-omitted-key fault-injection FAILS lint |
| TC-6 | Post-Story-5 budget verification | post-Story-5 (gate before PR merge) | `python3 scripts/check_skill_budgets.py`; `wc -l delivery-team/skills/godot/SKILL.md` | Exit code 0 with `known_debt[]` empty (delivery-team scope); EVERY file at-or-under tier ceiling INCLUDING +3 frontmatter; **godot returns exactly 200** (197 + 3); tightest binding gate of the wave |
| TC-7 | Cache-prefix hash regeneration | post-Story-5 | Diff `governance/cache-prefix-hash.txt` pre/post; verify header comment expanded scope (13 files, was 1) | New hash value differs from pre-Story-5; header records 13-file scope; PR body cites ACTUAL byte counts (NOT +650B projection); Dev runs-the-command at DoD per ADR-tk4-003 binding |
| TC-8 | CLAUDE.md ≤150 | post-Story-6 | `wc -l CLAUDE.md`; `grep -E "ARCHITECTURE.md\|plugin-catalog.md" CLAUDE.md` | wc returns ≤150; ≥1 one-hop discoverability link present; `grep "architect/skills/paradigms/" CLAUDE.md` returns 0 (stale path side-fix) |
| TC-9 | Retro template KPI integration | post-Story-6 | Inspect retro template for `context_tokens_per_pipeline_run` section; synthesize 5-prior-run dataset and run KPI compute | KPI section contains formula + source-data ref + Δ-vs-prior-5-window annotation; rolling mean compute matches expected from synthetic input |
| TC-10 | Validator template standardization | post-Story-7 | Read `delivery-team/skills/delivery-flow/references/validator-prompt-template.md`; grep all Stage 6 + Stage 7 validator dispatches in `SKILL.md` for reference | Template exists with spec-vs-impl framing block + canonical-path block; ALL current validator dispatches reference the template (W3-13 + W3-15 joint-AC) |
| TC-11 | STATUS-format standardization | post-Story-7 | Run `grep -E "^STATUS: (DONE\|NOT_DONE\|CODE_COMPLETE\|PASS_WITH_NOTES)$"` against 5 sample DoD reviews from this run | 5/5 DoD reviews match the standardized single-line format; STATUS values stay verbatim per FR-7.3 |
| TC-12 | JSON↔Python KNOWN_DEBT lint workflow | post-Story-7 | Trigger `.github/workflows/skill-budget-consistency.yml`; introduce a deliberate JSON↔Python drift on a fault-injection branch | Workflow PASSES on clean tree; FAILS on fault-injection (exit non-zero); `workflow-injection-lint.yml` gate PASSES (no `${{ github.event.* }}` in `run:` blocks per DEFECT-004 regression guard); pre-commit hook fails commit when SKILL.md exceeds budget without `Budget-Exception:` |
| TC-13 | Stage-7 stale-sweep (DEFECT-006 close) | post-Story-7 (Stage 7 dogfood) | Plant a synthetic stale Wave-N-1 file at `.delivery/artifacts/07-uat/dod/`; run Stage 7 entry-step; verify dogfood against THIS run's PRD-§3 stale-PRD instance | Stage 7 emits Option-A banner per stale file (per Architect §Open questions #3 ruling); synthetic case banners; live dogfood case banners on tk3-stale PRD; **DEFECT-006 closes upon merge** |
| TC-14 | Telemetry hardening (zero-token capture) | post-Story-7 | Synthesize a missing-measurement scenario; verify `.delivery/telemetry/skill-loads.jsonl` row behavior; verify W3-10 KPI compute excludes those rows | Telemetry hook either fails-loud OR marks zero-token rows `placeholder=true` per FR-7.6; W3-10 KPI compute correctly EXCLUDES placeholder rows; if `compute_token_reduction.py` lacks `--baseline pre-caveman-lite` support today, that flag landed via W3-18 BEFORE Story 5 PR opens (per architecture-tk4-wave-3.md §Stop-Rule Tripwire Mechanics tail) |
| TC-15 | Fitness-review governance doc (Story 6 AC-2 + init AC-10 part 1) | post-Story-6 | `test -f governance/fitness-review.md`; `grep -E "^(##\|###) (Cadence\|Owner\|Inputs\|Outputs\|Kill[- ]criteria)" governance/fitness-review.md` | File exists (exit 0); ≥5 required-section-header matches (Cadence + Owner + Inputs + Outputs + Kill-criteria); kill-criteria section explicitly cites "skills failing fitness 2 quarters in a row" threshold per BACKLOG-104 W3-11 |
| TC-16 | Fitness-review workflow operational (Story 6 AC-3 + init AC-10 part 2) | post-Story-6 | `test -f .github/workflows/fitness-review-reminder.yml`; `grep -E "schedule:\|cron:" .github/workflows/fitness-review-reminder.yml`; `grep -E '\$\{\{[[:space:]]*github\.event\.' .github/workflows/fitness-review-reminder.yml`; synthetic dry-run with planted `fitness_review_due:` date 7 days out | File exists (exit 0); ≥1 cron/schedule match (weekly cadence per W3-11); ZERO `${{ github.event.* }}` matches inside `run:` blocks (DEFECT-004 regression guard via `workflow-injection-lint.yml`); synthetic dry-run opens an issue for the planted earliest-due date |

## Test Data

- **Synthetic dispatches**: 11 architect + 16 (presentation 9 + 4, ui 3, ops 3) + 15 (quality 7, user-feedback 4, godot 4) + 5 research-agent + 4 persona-family = **51 router-regression dogfood inputs**, all dispatched via the existing `lotr` theme to preserve theme continuity (BACKLOG-104 §Pipeline preferences).
- **Baselines**: Wave 2 prose-token snapshot at `.delivery/memory/archive/run-2026-05-05-tk2.md` (pre-caveman-lite reference, per architecture §Stop-Rule Tripwire Mechanics line 78); Wave 0 archive for the pre-Wave-0 cumulative-reduction baseline (NFR-4 / AC-7).
- **Synthetic 5-prior-run dataset** (TC-9): hand-crafted JSONL rows with known prose-token totals so the rolling-mean Δ annotation can be verified against an arithmetic answer-key.
- **Fault-injection fixtures**: (a) one delivery-team SKILL.md with `maintainer:` deleted (TC-5); (b) JSON↔Python drift branch — add `W4-fake` to `governance/skill-budgets.json known_debt[]` without updating `scripts/check_skill_budgets.py` (TC-12); (c) plant `tk3-residual.md` at `.delivery/artifacts/07-uat/dod/` for stale-sweep (TC-13); (d) crafted JSONL row with `prose_tokens: 0` for placeholder-route (TC-14).

## Empirical Measurement Protocol — AC-13 close-out + cumulative reduction

Closes the deferred caveman-lite AC-13 (telemetry-measurable cumulative token reduction) AND BACKLOG-104 init AC-7 / PRD NFR-4. Wave 3 IS the first post-merge run for caveman-lite, so its first 5 dispatches are the empirical close-out artifact.

1. **Source**: `.delivery/telemetry/skill-loads.jsonl` (post W3-18 hardening; per architecture §Stop-Rule Tripwire Mechanics line 76 the `prose_tokens` field is reliable per dispatch only after W3-18 ships).
2. **Pre-Wave-0 baseline**: cite Wave 0 archive (`memory/archive/run-2026-04-…-tk0e.md` snapshot of pre-Wave-0 mean prose-tokens per delivery-flow invocation; the same archive that originally registered AC-13 as deferred).
3. **Window**: first 5 Wave-3 `delivery-team:delivery-flow` dispatches post-Wave-3-merge.
4. **Cumulative reduction calculation**: `reduction% = (baseline_mean - W3_mean) / baseline_mean × 100`, where `W3_mean = mean(prose_tokens)` over the 5-dispatch window EXCLUDING any rows with `placeholder=true` per FR-7.6 + TC-14.
5. **Command**: `python3 scripts/compute_token_reduction.py --baseline pre-W0 --window 5 --output .delivery/telemetry/cumulative-reduction-tk4.txt` (mirrors the tripwire command shape from architecture §Stop-Rule Tripwire Mechanics; if `--baseline pre-W0` flag does not yet exist today, fold into W3-18 alongside `--baseline pre-caveman-lite`).
6. **Pass criterion**: cumulative reduction **≥50%** compounding W0+W1+W2+caveman-lite+W3 (PRD NFR-4; BACKLOG-104 init AC-7).
7. **Citation artifact**: `.delivery/telemetry/cumulative-reduction-tk4.txt` is the binding DoD artifact for AC-7 / AC-13 — narrative claims rejected (caveman-lite Hot Lesson #1 binding).

## Tripwire Activation Protocol — QA Stage 7 verification

Verifies whether the BACKLOG-104 §Stop-rule trigger #2 (caveman-lite carry-forward) fired during Stage 6, per architecture §Stop-Rule Tripwire Mechanics + ADR-tk4-003 §DoD validator binding. Run at Stage 7 entry by QA before UAT acceptance.

1. **Existence check**: `test -f .delivery/telemetry/stop-rule-tk4.txt` MUST return 0. Absence = Stage 6 failed to honor binding artifact contract → Stage 7 BLOCKS UAT pending Stage-6 re-dispatch.
2. **Parse**: read first-3-dispatch mean from the file (produced by `python3 scripts/compute_token_reduction.py --baseline pre-caveman-lite --window 3 --output .delivery/telemetry/stop-rule-tk4.txt`).
3. **Threshold compare**: if reduction `<15%` → tripwire **DID FIRE** during Stage 6 → verify Stories 1–4 + Story 7 landed but Stories 5 + 6 (W3-9..W3-12) HELD pending caveman-lite root-cause retro per architecture line 79–80; UAT validates only the landed scope.
4. **Sequencing audit (tripwire NOT fired path)**: `git log --merges --oneline main..HEAD` MUST show Stories 1–4 merge commits BEFORE Story 5 commit timestamp (Story 5 AC-4 from `stories.md`); if Story 5 PR opened with no `stop-rule-tk4.txt` cite, escalate as DoD-validator bypass.
5. **Recovery-path verification (tripwire DID fire path)**: confirm `.delivery/memory/` has a caveman-lite root-cause retro entry post-tripwire; confirm BACKLOG-102 follow-up issue opened; confirm Stage 4 round-3 (or Wave 4 deferral) decision recorded.
6. **Output**: QA writes Stage-7 finding to `.delivery/artifacts/07-uat/qa/tripwire-verification.md` citing which path (FIRED / NOT FIRED) was taken and the artifact lines that prove it.

## DoD Pass-Rate Regression Protocol — BACKLOG-104 init AC-8 (NFR-5 cross-check)

Closes init AC-8 ("no regression in delivery-flow first-try DoD pass rate") with a runnable Stage-7 dogfood activity. Round-2 fix: bare "cross-checked at retro" was not runnable per Gate 4 standard.

1. **Source**: `.delivery/memory/archive/*.md` retro entries (each archived run records per-stage first-try DoD outcomes).
2. **Window**: last 5 archived pipeline runs INCLUDING tk4 (rolling baseline = mean across the 5; per-run = tk4 alone).
3. **Command**: `python3 scripts/dod_pass_rate.py --archive-glob '.delivery/memory/archive/*.md' --window 5 --include-current tk4 --output .delivery/telemetry/dod-pass-rate-tk4.txt` (script extracts STATUS lines per Gate 4 / TC-11 standardized format; if script does not yet exist, falls back to hand-tally with `grep -c "^STATUS: DONE" .delivery/artifacts/*/dod/*.md` against the same 5-run window).
4. **Pass criterion**: tk4 first-try DoD pass rate ≥ baseline_mean (NOT a hard percentage — relative to the 60-90% range from `memory/index.md` per BACKLOG-104 AC-8 wording). Regression = strictly less than baseline_mean by >5 percentage points.
5. **Output artifact**: `.delivery/telemetry/dod-pass-rate-tk4.txt` is the binding evidence; QA cites it in the Stage-7 retro section.

## Defects-Per-Story Rolling Window Protocol — BACKLOG-104 init AC-9 (stop-rule trigger #1)

Closes init AC-9 ("defects/story rate ≤0.4 rolling 3-PR window") with a runnable Stage-7 dogfood activity. Round-2 fix: bare "measured at retro" was not runnable.

1. **Source**: GitHub PR history for the last 3 merged PRs on `main` (current rolling window per BACKLOG-104 §Stop-rule line 312 = tk2 + tk3 + tk4).
2. **Defect definition**: any issue with label `defect` opened within 7 days of PR merge AND citing the merged PR in body (per BACKLOG-100 stop-rule origin convention).
3. **Command**: `python3 scripts/defects_per_story.py --pr-window 3 --story-source .delivery/artifacts/05-plan/po/stories.md --output .delivery/telemetry/defects-per-story-tk4.txt` (script: count defect-labeled issues opened in 7-day post-merge window for each of last 3 PRs ÷ total story count across same 3 PRs; if script does not yet exist, fallback hand-query `gh issue list --label defect --search "merged:>$(date -d '21 days ago' --iso) PR-XXX"` per PR).
4. **Pass criterion**: rolling 3-PR mean defects/story **≤0.4** (current at run start: tk2=0 + tk3=1/7 = 0.14 + tk4 TBD; tk4 may add up to 1.66 defects total before triggering — practically ≤2 defects this wave).
5. **Output artifact**: `.delivery/telemetry/defects-per-story-tk4.txt` is the binding evidence; if computed value >0.4, stop-rule trigger #1 fires per BACKLOG-100 carry-forward and Wave 4 holds pending root-cause retro.

## Risk Areas (3)

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| **Godot ceiling tightness** (236 → 197 → 200 post-frontmatter; ZERO headroom) | High | High — single line over breaks Tier-C, blocks Story-5 PR merge, cascades to ADR-tk4-001 partial-compliance escape hatch | TC-3 binds godot to ≤197 BEFORE Story 5; TC-6 verifies exactly 200 AFTER frontmatter; ADR-tk4-001 round-2 escape hatch (5-line guardrails fold) demoted to Stage-6 reserve and remains usable if measured `wc -l` exceeds projection by 1–2 lines |
| **Frontmatter byte-impact estimate variance** (+650B projection across 13 files; one-time ~26KB cold-cache re-warm) | Medium | Medium — wrong projection breaks tripwire baseline math, distorts Empirical Measurement Protocol output | TC-7 cites ACTUAL byte counts from regenerated hash file (NOT projection); ADR-tk4-003 §Cumulative cache-prefix re-freeze procedure mandates Dev runs-the-command at DoD; tripwire artifact `stop-rule-tk4.txt` is binding evidence not narrative claim |
| **Paradigm sub-skill discoverability** (Ruling 2: top-level discoverable, sub-skills router-only via `disable-model-invocation: true`) | Medium | High — silent breakage of marketplace auto-discovery would not surface until user reports missing skills | TC-4 lint runs the deliberate-violation path (introduce `disable-model-invocation: true` on a top-level SKILL.md → MUST fail); existing `architect/paradigms/{volatility,ddd}` grandfathered shape is the canonical reference; `plugin-dev:plugin-validator` mandatory pre-PR per Story-4 routing |

## Entry Criteria

- All 7 stories in `.delivery/artifacts/05-plan/po/stories.md` accepted by PO; story-AC count = 35 (verified at QA load).
- ADRs tk4-001 / tk4-002 / tk4-003 in `Accepted` state; architecture-tk4-wave-3.md §Stop-Rule Tripwire Mechanics present (lines 72–81).
- `governance/cache-prefix-hash.txt` baseline captured pre-Story-5 (for TC-7 diff).
- `.delivery/telemetry/skill-loads.jsonl` reachable; pre-Wave-0 baseline mean recorded from Wave 0 archive (for Empirical Measurement Protocol).
- Wave 2 + caveman-lite both merged on main (BACKLOG-104 §Pre-flight gate; status: SATISFIED at run start).

## Exit Criteria

- All 16 TCs PASS (TC-3 godot ≤197 + TC-6 godot exactly 200 + TC-12 fault-injection FAIL-path + TC-5 fault-injection FAIL-path are the four binding fail-path verifications; TC-15 + TC-16 close fitness-review process for init AC-10).
- Empirical Measurement Protocol output `.delivery/telemetry/cumulative-reduction-tk4.txt` shows ≥50% cumulative reduction (init AC-7 / NFR-4).
- Tripwire Activation Protocol output `.delivery/artifacts/07-uat/qa/tripwire-verification.md` records FIRED-or-NOT-FIRED path with artifact citations.
- DoD Pass-Rate Regression Protocol output `.delivery/telemetry/dod-pass-rate-tk4.txt` shows tk4 ≥ baseline_mean (init AC-8 / NFR-5).
- Defects-Per-Story Rolling Window Protocol output `.delivery/telemetry/defects-per-story-tk4.txt` shows rolling 3-PR mean ≤0.4 (init AC-9 / NFR-6 / Stop-rule trigger #1).
- BACKLOG-104 init AC-1 (`known_debt[]` empty), AC-3 (frontmatter on all SKILL.md), AC-5 (DEFECT-006 closes), AC-6 (paradigm ≥3 axes), AC-10 (fitness review operational via TC-15+TC-16) all satisfied per their TC/Protocol mappings above.

## Approach

Risk drives prioritization. The single tightest gate (godot 197 → 200 with zero headroom) is verified twice — once before frontmatter (TC-3), once after (TC-6). The cache-prefix re-freeze is binding-empirical-only (TC-7); narrative claims are explicitly rejected per ADR-tk4-003 + caveman-lite Hot Lesson #1. Fault-injection fixtures exercise the fail-paths of every CI/lint/hook artifact this wave introduces (TC-5, TC-12, TC-13, TC-14, TC-16 injection-lint guard). Round-2 fix: TC-15 + TC-16 split the fitness-review process into doc-existence + workflow-operational verifications (Story 6 AC-2 and AC-3 were previously mis-mapped to TC-8/TC-9 which cover CLAUDE.md and retro KPI respectively — different content). The four protocols (Empirical Measurement, Tripwire Activation, DoD Pass-Rate Regression, Defects-Per-Story Rolling Window) are deliberately separated from the 16 TCs because they consume Stage-6 + post-merge telemetry that does not exist at Plan time; QA at Stage 7 runs them against live data and writes the binding citation artifacts. Bare "cross-checked at retro" / "measured at retro" lines were not runnable per Gate 4 standard and have been replaced with named protocols citing concrete script invocations + fallback hand-query commands + binding output artifacts.

— Pippin Took, QA Engineer, run-2026-05-09-tk4 (round 2). Sixteen cases. Fifty-two source lines. Zero gaps. The hobbits counted to ten this time, not seven; the road is plain again.
