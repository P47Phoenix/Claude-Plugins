# Gate 2 Evaluation, Round 1 — BACKLOG-108 Opus 4.8 Migration PRD

Evaluator: QA Engineer (evaluator only). Artifact: `.delivery/artifacts/02-refine/po/prd.md`. Stage 2 LIGHT. Binding decisions in `.delivery/memory/topics/opus-4-8-migration.md` treated as authoritative.

**Verdict: REVISE**

## 1. Gate 2 per-criterion results

| # | Criterion | Sev | Result | Note |
|---|-----------|-----|--------|------|
| 1 | Every FR has AC with testable condition | blocking | FAIL | Most FRs have no AC (D-1) |
| 2 | NFRs quantified | blocking | FAIL | No NFR section. $15 / `--cost-cap 3.00` / line budgets only scattered in Constraints (D-2) |
| 3 | Out-of-scope present, non-empty | blocking | PASS | Sec 7, three items |
| 4 | Success metrics numeric + method | blocking | PASS (conditional) | Gates G1-G8 carry counts + commands, but ownership defects D-3, D-4 |
| 5 | No blocking open questions | blocking | FAIL | Two UNVERIFIED claims "Architect to confirm at Stage 4" with no Open Questions section or deferral rationale (D-6) |
| 6 | Personas specific | warning | FAIL | None (D-7) |
| 7 | Dependencies w/ status | warning | FAIL | Story order only, no confirmed/pending/at-risk (D-7) |
| 8 | Risks w/ likelihood/impact/mitigation | warning | FAIL | None in PRD (idea-brief R1-R5 not carried) (D-7) |
| 9 | Assumptions explicit | suggestion | FAIL | None (D-7) |

## 2. Discovery commands: PRD claim vs reality (worktree root)

| Command / claim | PRD says | Actual | Match |
|---|---|---|---|
| `find . -name SKILL.md \| wc -l` | 34 | 34 | YES |
| `grep -rl model_awareness . --include=SKILL.md \| wc -l` | 25 files | 25 | YES |
| Stamp values | 7 x `opus-4-7`, 18 x `opus-4-7-frontmatter-only` | 7 and **19** (26 lines in 25 files; `prompt-engineer/SKILL.md` has 2 stamp lines) | NO (D-11) |
| Unstamped files | 9 (4 personas + 5 research-types) | 9, exactly those | YES |
| 4-7 literals, py/md/SKILL.md excl `.delivery/` | "FIVE sites, 7 hits" | 7 hits in 4 files (agent_registry x1, prompt-engineer x1, conftest x4, smoke-test-architecture x1). Table lists 4 rows. 5th "site" = guard yml (2 more hits, L23/L39), not in table | Hits YES; "FIVE" vs 4-row table inconsistent (D-11) |
| AC-1 first cmd today | target 0 | 7 | n/a (Stage 6); well-formed, runnable |
| AC-1 allowlist grep on guard | >= 1 | 5 today on the OLD 4-7 guard | Runnable but passes pre-migration (D-5) |
| AC-2 cmds | 34 / 0 | 0 / 26 today | Runnable; second cmd weak (D-5) |
| AC-3 `frontmatter-only` | 0 | 19 today | Runnable |
| AC-5 baseline JSON | prints `claude-opus-4-8 5 active True True` | file keys: `schema_version, scenario, sample_status, n_samples, last_captured_utc, last_captured_git_sha, last_captured_cli_version, metrics, deferred_reason`. **No `model` key.** Prints `None 1 partial-1-of-5` | Runnable but asserts field schema lacks (D-8) |
| AC-6 `check_skill_budgets.py` | exit 0 | BUDGET CHECK PASSED (17 files) | YES |
| AC-7 provisional grep | 0 | 2 hits, both `research-agent/SKILL.md` (L207, L400) legit "unverified" rubric prose | false-positive (D-9) |
| `run_smoke.py --effort` | FR-5.3 adds | flag absent; `--cost-cap` present | needs code, no AC (D-1) |
| `validate_constraints.py` on constraints.yml | valid | **INVALID**: missing `entities`, `invariants` | FAIL (D-10) |

Note: `--effort`, `cost-cap` exist/absent as above. Budget script and validator located at `scripts/check_skill_budgets.py` and `delivery-team/skills/delivery-flow/scripts/validate_constraints.py`.

## 3. Binding-decision honor check

Honored: 2.1, 2.2, 2.3, 2.4, 2.5, 3.1-3.3, 4.1-4.3, 4.5, 5.1-5.5. No re-debate found. Gap: BINDING-4.4 (baseline invalidation/re-capture) not referenced by any FR (D-13). BINDING-1.4 exemption only in scope text; AC-1 recursion has no explicit `prd-quality-gate-flow/` handling (none hit today).

## 4. Numbered defects and required fixes

**D-1 (blocking) FR->AC coverage (Sec 2 vs Sec 3).** No AC covers FR-1.2/1.3, FR-2.1-2.4, FR-3.1 (only weak AC-3), FR-4.2/4.3/4.4, FR-5.1-5.4, FR-6.1/6.2, FR-7.1-7.3. Fix: add runnable stdlib ACs, e.g. FR-1.2: temp file containing `claude-opus-4-7` piped through the guard's grep expression yields non-empty; FR-1.3: zero `claude ` CLI invocations in the guard yml; FR-5.3: `--effort` present in `run_smoke.py`; FR-5.1/5.2: named metrics keys present in baseline `metrics`; FR-6.1: recompute fingerprint and compare to `governance/cache-prefix-hash.txt` (name the algorithm/script); FR-6.2: `test -f` on ADR path (name it); FR-7.1/7.2: CHANGELOG contains `BACKLOG-108`, memory file has run-outcome heading. Tag process-only FRs (FR-2.4, FR-4.4, FR-7.3) as inspection-verified with named evidence.

**D-2 (blocking) NFRs (Sec 8).** Add NFR section with numeric targets and measurement command: cost <= $3.00/run, <= $15 total; line-budget breaches = 0; guard false positives on current tree = 0; baseline n_samples = 5; provisional-claim count = 0.

**D-3 (blocking) Gate ownership (Sec 4).** G1 owner S1, but AC-1 (zero 4-7 literals) can only go green after S2 (prompt-engineer:368) and S4 (registry, conftest, architecture doc). S1 cannot close it. G6 "S2+S3" and G8 "all" are shared, contradicting "one story closes one gate". Fix: G1 -> S4; add separate S1 gate (guard rejects 4-7 fixture, allowlist correct); G6 -> S3 with S2 as precondition; G8 -> one named closer (S7 or UAT QA validator).

**D-4 (blocking) AC-DISP not runnable (Sec 3).** "QA validator enumerates" is not a testable command. Fix: name observable artifact (dispatch log path) and stdlib count command: dispatches per stage == `len(dod_validators)`.

**D-5 (blocking) Weak AC commands.** (a) AC-1 allowlist `grep -c ... >= 1` passes on the old guard; require 0 non-comment `claude-opus-4-7` in guard AND three separate greps for each approved ID. (b) AC-2 second cmd `grep -v "opus-4-8"` lets `opus-4-8-frontmatter-only` through; use `grep -v "model_awareness: opus-4-8$"`. (c) FR-7.2 CHANGELOG entry will likely name `claude-opus-4-7` and trip AC-1; specify wording form (`# prior:` or exclusion) or exclude CHANGELOG. (d) Add `--exclude-dir=.claude --exclude-dir=.git` to avoid worktree/dup counts.

**D-6 (blocking) Open questions (Sec 6).** Two UNVERIFIED rows deferred to Stage 4 without a deferral entry. Fix: Open Questions section OQ-1, OQ-2 with owner (Architect), due stage, and rationale why non-blocking (prose anchored to VERIFIED effort behavior; AC-7 catches leakage).

**D-7 (warning) Missing sections.** Add personas (maintainer, downstream plugin consumer, CI reviewer with goals/pain/context), dependencies with status, risks with L/I/mitigation (carry R1-R5 from idea-brief), assumptions.

**D-8 (blocking) AC-5 vs schema.** Baseline JSON has no `model` field; no FR adds it. Fix: add FR extending baseline schema with `model` (and `effort`), or derive model from `metrics.model_usage` keys; state source of truth.

**D-9 (warning) AC-7 false positives.** `UNVERIFIED` pattern matches legit research-agent rubric prose. Fix: scope pattern to the two hedge phrases from Sec 6, or exclude `research-agent/`.

**D-10 (blocking, Stage 2 DoD) constraints.yml invalid.** Validator: missing `entities`, `invariants`. Fix: add non-empty string lists (entities: SKILL.md stamp, model-ID literal, CI guard, baseline JSON, cache fingerprint; invariants: one-role-one-agent, no 4-7 literal outside the provenance comment, stamps after prose DoD, no claude CLI in CI); re-run validator to pass.

**D-11 (blocking) Discovery-number accuracy (Sec 1).** "18 x frontmatter-only" wrong: actual 19 lines (prompt-engineer has 2 stamp lines). Affects G2 "25 updated + 9 created" and AC-2/AC-3. Fix: state 26 lines in 25 files; add AC `grep -c "model_awareness:" prompt-engineer/SKILL.md` == 1 and total stamp lines == 34. Reconcile "FIVE sites" with the 4-row table (name guard yml as the 5th, or say four files).

**D-12 (warning) AC-3 body-delta check.** "spot-check >= 5" contradicts BINDING-2.2 (all 34) and is not machine-runnable. Fix: stdlib check that every SKILL.md has >= 1 changed line outside frontmatter, 34/34.

**D-13 (warning) BINDING-4.4.** Add FR for baseline invalidation/re-capture or cite S5 as subsuming it.

## 5. Summary

Blocking fails: criteria 1, 2, 5; plus D-3, D-4, D-5, D-8, D-10, D-11. Verified live and correct: 34 SKILL.md, 25 stamped, 9 unstamped, 7 literal hits, budgets pass.
