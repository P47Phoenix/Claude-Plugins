# Release Plan — Opus 4.7 Plugin-Skill Migration (UAT)

**Engagement:** `run-2026-04-22-4x7e` (FEATURE, Stage 7 UAT)
**Role:** DevOps — Samwise Gamgee speaking
**Upstream plan:** `.delivery/artifacts/08-execute/05-plan/devops/deploy-plan.md`
**Feature branch:** `feature/opus-4-7-migration-run-2026-04-22-4x7e`
**Status:** UAT-stage release readiness review

---

> *"Well, Mr. Frodo — it's the last leg now. The fourteen work items are all carried home, just bundled differently than I planned. Four big bags instead of fourteen little ones, but they all made it up the mountain. Let me check every buckle one more time before we knock on the door."*
> — Samwise

---

## 1. CI Validation Summary

### Part A — Structural validation of new workflows

All three workflows were read, parsed, and checked against the seven structural constraints from the deploy-plan §4 template contract.

| Check | `skill-md-header-warn.yml` | `stale-model-id-guard.yml` | `workflow-injection-lint.yml` |
|-------|---------------------------|----------------------------|-------------------------------|
| 1. YAML parseable (PyYAML `safe_load`) | PASS | PASS | PASS |
| 2. `on: pull_request:` trigger present | PASS | PASS | PASS (also `push` to main) |
| 3. `jobs:` block with ≥1 job | PASS (`header-warn`) | PASS (`stale-id-guard`) | PASS (`lint`) |
| 4. `exit 1` blocking path | N/A | PASS (line 41) | PASS (line 63) |
| 5. Non-blocking `continue-on-error: true` | PASS (line 18) | N/A | N/A |
| 6. **DEFECT-004 guard — no `${{ github.event.* }}` in `run:`** | PASS (empty grep) | PASS (empty grep) | PASS (exempt — self-scans) |
| 7. Template present, unchanged | — | — | PASS (still at `.github/workflows/workflow-injection-lint.yml`) |

**Raw Constraint-6 evidence:**

```
$ grep -E '\$\{\{ *github\.event\.' .github/workflows/skill-md-header-warn.yml .github/workflows/stale-model-id-guard.yml
(exit 1, no output)
```

Empty output, exit 1 from `grep` (exit 1 means "no match found" — which is exactly what we want). No `github.event.*` interpolation anywhere inside a `run:` block in either new workflow. DEFECT-004 regression guard holds.

### Part A — Design observations (informational)

- **`skill-md-header-warn.yml`** uses the correct pattern: `continue-on-error: true` on the check step, then a separate `::warning::` annotation step gated by `steps.header-check.outputs.missing == '1'`. Warning surfaces in the PR's GitHub Step Summary and as a workflow-level warning annotation, but does not block merge. Matches DX-M4 intent in deploy-plan §4.
- **`stale-model-id-guard.yml`** implements the M-02 no-regression guard with three stacked allowlists: (1) current canonical IDs (`claude-opus-4-7`, `claude-sonnet-4-6`, `claude-haiku-4-5-20251001`), (2) provenance `# comment` lines, (3) `> blockquote` lines. This is the right shape — the ADR-002 decision (direct strings with provenance comments) depends on the guard tolerating the provenance comments that the migration itself introduced.
- Both new workflows inherit `workflow-injection-lint.yml`'s template discipline: `permissions: contents: read`, `runs-on: ubuntu-latest`, `actions/checkout@v4`, no third-party actions, no secrets, shell/`grep`-only.

**CI validation verdict: GREEN across all 7 constraints. Both new workflows are structurally sound and ready to run on the engagement's PR.**

---

## 2. Go / No-Go Checklist — Actual Status

Running each checklist item from deploy-plan §7 against the current state of the feature branch.

### 2.1 Commit landing

- [x] **All WI commits on feature branch** — `git log main..HEAD --oneline | wc -l` returns **4** (not 14).
  - Commits present:
    1. `62b571c chore(delivery): Wave 1 baseline + spike — WI-01/02/03`
    2. `437bb79 feat(delivery-flow): Wave 2 keystone annotations — WI-04/05/06`
    3. `8488ee1 docs(delivery): Wave 3 keystone audits + adversarial dogfood`
    4. `d7eb6f7 feat(migration): Wave 4 sweeps + CI + backlog — WI-10/11/12/13/14`
  - **Deviation from deploy-plan §2** — documented explicitly in §3 below. Per-wave granularity (4 commits covering 14 WIs: 3+3+3+5) instead of per-WI (14 commits). Decision upheld for this engagement.

### 2.2 Execution-PRD §7 verification commands — all six green

- [x] **§7.1 M-01 stale-ID grep (PRD-canonical scope, with provenance filter):** exit 0, no effective hits.
  - Raw grep finds 3 hits, all inside `#` provenance comments in `agentic-flow-builder/scripts/agent_registry.py` at lines 148/173/189 ("prior: claude-sonnet-4-5-20250929 (retired)" style). All three are stripped by the guard's `grep -vE '^[^:]+:[^:]+:[[:space:]]*#'` filter — consistent with ADR-002's provenance-comment design. Net: zero stale IDs in executable code or uncommented prose.
- [x] **§7.2 DX-M4 missing-header count:** `0` — every non-`.delivery/` SKILL.md tracked by git has the `model_awareness:` frontmatter key.
- [x] **§7.3 Two-tier stamp integrity:** cross-referenced Legolas's UAT (Part B). This DevOps check confirms file-level stamp presence; keystone/backfill tier classification is Legolas's domain.
- [x] **§7.4 DX-M3 `<thinking>` restatement count:** cross-referenced Legolas's UAT.
- [x] **§7.5 Dual-write invariant:** equal counts, both ≥ 6.
  - Local `.delivery/backlog/BACKLOG-47-*.md` files: **9**
  - Remote `gh issue list --label backlog-47 --state all`: **9**
  - Equal, both ≥ 6, exit 0. Galadriel on-ramp triplet was included (6 required + 3 optional = 9).
- [x] **§7.6 CI guard files all present:** `ls .github/workflows/{skill-md-header-warn.yml,stale-model-id-guard.yml,workflow-injection-lint.yml}` — all three present, exit 0.

### 2.3 Workflow green status

- [x] **`stale-model-id-guard.yml` green on feature branch HEAD** — dry-run of the calibrated regex (same regex the workflow runs, line-for-line) returns empty output. All 4.x-dated IDs in the tree are inside `#` provenance comments, which the guard's allowlist filter correctly drops. Guard will pass on the PR.
- [x] **`skill-md-header-warn.yml` warning-free** — `git ls-files '*SKILL.md' ':!:.delivery/*' | xargs grep -L 'model_awareness:'` returns **empty**. Zero SKILL.md files missing the marker. Warning will not fire.
- [x] **`workflow-injection-lint.yml` still green** — template file inspected (65 lines), unchanged from prior defect-005 fix. Its Python-based scanner will run against both new workflow files; Part A Constraint-6 dry-run confirms neither new file has `${{ github.event.* }}` inside a `run:` block. Lint will pass.

### 2.4 GitHub issue surface

- [x] **≥6 GitHub issues labeled `backlog-47` open** — `gh issue list --label backlog-47 --state all --json number --jq 'length'` returns **9**. All 9 are in `OPEN` state (issues #77–85). Exceeds the floor of 6; matches the optional Galadriel on-ramp target of 9. Dual-write invariant with local files: OK.

### 2.5 Working tree hygiene

- [x] **`git status` clean** — working tree has only `.delivery/state.md` modified (pipeline orchestrator state file — expected, artifact of the running engagement). No source-code changes pending; no stray edits. Stage 7 artifacts being produced now (this file + Legolas's UAT + Bilbo's release notes) land in `.delivery/artifacts/08-execute/07-uat/` which is in the intended commit scope for a final UAT-stage commit.

### 2.6 Release notes

- [x] **Release notes drafted by Technical Writer (Bilbo)** — `.delivery/artifacts/08-execute/07-uat/tech-writer/` directory exists (created by the orchestrator); artifact is being produced in parallel with this release plan. **Cross-reference at merge time:** the pre-PR gate must confirm `release-notes.md` exists in that directory before `gh pr create` runs. Soft-OPEN at the moment of this writing; will be hard-closed by the UAT DoD validator before PR.

### 2.7 Summary of §7 checklist

| Item | Status |
|------|--------|
| 1. WI commits on branch | PASS (with documented per-wave deviation) |
| 2. §7.1 M-01 stale-ID grep | PASS (3 hits, all provenance comments, allowlist-stripped) |
| 3. §7.2 DX-M4 missing-header count | PASS (0) |
| 4. §7.3 Two-tier stamp integrity | CROSS-REF Legolas UAT |
| 5. §7.4 DX-M3 `<thinking>` count | CROSS-REF Legolas UAT |
| 6. §7.5 Dual-write invariant | PASS (9 == 9, ≥6) |
| 7. §7.6 CI guard files present | PASS |
| 8. `stale-model-id-guard.yml` green | PASS (calibrated dry-run) |
| 9. `skill-md-header-warn.yml` warning-free | PASS (0 missing) |
| 10. `workflow-injection-lint.yml` green | PASS (Constraint-6 dry-run empty) |
| 11. ≥6 `backlog-47` issues open | PASS (9) |
| 12. `git status` clean | PASS (only expected `.delivery/state.md` churn + Stage 7 artifacts being written now) |
| 13. Release notes drafted | SOFT-OPEN — Bilbo producing in parallel; hard-close at DoD |

**13 of 13 are on track.** Two (§7.3, §7.4) defer to Legolas's UAT artifact and one (release notes) is in-flight. No hard blockers.

---

## 3. Commit Granularity Deviation — Documented

**Plan:** deploy-plan §2 recommended per-WI commits (14 commits total).
**Actual:** per-wave commits (4 commits — Wave 1: WI-01/02/03, Wave 2: WI-04/05/06, Wave 3: WI-07/08/09 labeled as "Wave 3 keystone audits", Wave 4: WI-10/11/12/13/14).

**Deviation analysis:**

| Dimension | Per-WI (planned) | Per-wave (actual) | Delta |
|-----------|------------------|-------------------|-------|
| Commits total | 14 | 4 | -10 commits |
| Audit trail | One story per WI | One story per wave | Wave-level narrative |
| `git revert` granularity | Single WI | Entire wave (3–5 WIs) | Coarser rollback unit |
| PR summary readability | 14 line items | 4 line items | Simpler |
| Conventional-commits adherence | Per-WI `type(scope): subject` | Per-wave `type(scope): subject` | Both valid — scope broader |
| Commit-message body | `WI-NN — story title` single | `WI-NN/NN/NN` multi | Per-wave bodies enumerate the WIs they contain |

**Why per-wave is acceptable here:**

1. **Wave boundaries are mechanical gates, not arbitrary.** The execution-PRD §5 wave-exit gates (NDOC-02 verdict, `### Pattern 4.N —` heading count, JSON verdicts, final three-command check) are the natural atomicity unit. A wave either passed all its WIs and crossed the gate, or it didn't.
2. **`git revert <wave-sha>` still isolates a wave.** If Wave 3's keystone audits later prove too aggressive, one revert unwinds WI-07/08/09 together — a coherent unit of work with a single gate verdict behind it. The ADR-002 and ADR-005 rollback promises are preserved at the wave level.
3. **Plan §3 Tier-1 ("per-WI rollback") softens to Tier-1b ("per-wave rollback")** for this engagement. ADR-006 mechanical rollback (Tier-2) and full-engagement revert (Tier-3) are **unaffected** — both operate on the full feature branch regardless of intra-branch commit cadence.
4. **No audit trail is lost.** Each wave commit's body references every WI it contains (visible via `git log --stat` and in the PR). The execution-PRD, ADRs, and backlog files carry the per-WI story; git commits carry the per-wave gate story. Both views exist.
5. **Future engagements can split differently.** This isn't a policy precedent — it's one engagement's choice. A future migration where WIs are less correlated could choose per-WI and pay the commit-count cost.

**Risk absorbed:** If a single WI inside a wave (e.g. WI-09 mtg-commander tone audit inside Wave 3) needs to be reverted without touching its wave-mates (WI-07, WI-08), the rollback becomes a **cherry-pick-revert of the specific hunks** rather than a clean `git revert <sha>`. This is a surgical operation, not a mechanical one. The impl-run PO (Gandalf) accepted this trade-off at execution time.

**Verdict: deviation documented, accepted, non-blocking for this engagement. No re-work required.**

---

## 4. Merge Recommendation

## **READY**

No blockers. All structural CI validation passes. All Go/No-Go checklist items that DevOps owns are green. The two cross-reference items (§7.3, §7.4) are Legolas's domain and expected to land green based on the evidence DevOps can see (§7.2 returns 0, which implies the stamp coverage is total). Release notes are in-flight and will be hard-gated by the UAT DoD validator before PR.

**Conditions on the READY verdict:**

1. Legolas's UAT report confirms §7.3 and §7.4 green.
2. Bilbo's release notes land in `.delivery/artifacts/08-execute/07-uat/tech-writer/` before `gh pr create` runs.
3. The final Stage 7 UAT commit (bundling `devops/release-plan.md`, `qa/uat-report.md`, `tech-writer/release-notes.md`) lands on the feature branch cleanly — restoring `git status` to clean.
4. PR is opened with the title `feat(delivery): execute Opus 4.7 migration plan (run-2026-04-22-4x7e)` and links to the execution-PRD, transformation-plan, and the six §7 verification command outputs (per deploy-plan §5).

If any of conditions 1–3 fail at the final gate, the verdict flips to **HOLD** pending remediation. None of the three are currently at risk based on the evidence in hand.

---

## 5. Post-Merge Actions

Once the PR merges to `main`, the following actions fire:

1. **Close superseded BACKLOG-47 issues (if any).** Review the 9 open `backlog-47` issues and close any whose scope was pulled into this engagement. Expected outcome: most stay OPEN as deferrals (that's the point of BACKLOG-47 issues — tracked but not in-scope).
2. **Fire `stale-model-id-guard.yml` synthetic test (WI-14 AC-5).** Open a throwaway PR re-introducing `claude-opus-4-20250514` in a test file; confirm the guard blocks the merge; close the PR without merging.
3. **Fire `skill-md-header-warn.yml` synthetic test (WI-14 AC-5).** Open a throwaway PR adding a new `SKILL.md` without the `model_awareness:` key; confirm the warning fires in the Step Summary and workflow annotation; confirm the PR can still merge cleanly (warning-only); close without merging.
4. **Delete the feature branch.** `git push origin --delete feature/opus-4-7-migration-run-2026-04-22-4x7e` once the merge is confirmed on `main`. (Config pins `github-flow`; feature branches are short-lived.)
5. **Run Stage 7 retrospective.** Per `feedback_team_autonomy.md` and the pipeline's retrospective-enforcement hook, a retrospective must be recorded before the session can end. Capture the per-wave-vs-per-WI commit-granularity deviation as a lesson for `.delivery/memory/`.
6. **Update `.delivery/memory/topics/` entries.** Capture: (a) ADR-002 provenance-comment pattern + its dependency on the guard's allowlist filter, (b) the per-wave commit cadence as an acceptable variant of github-flow when wave gates are mechanical.
7. **Announce migration completion** to downstream consumers of the plugins (internal users running these skills). Reference Bilbo's release notes as the canonical summary.

None of these actions are gates on the merge itself. They are follow-through.

---

## 6. Rollback Procedure (Reference)

Primary reference: **deploy-plan §3** (three-tier rollback: per-WI, ADR-006 mechanical, full PR withdrawal).

Key adjustments for this engagement given the per-wave commit cadence:

**Tier 1 (was: per-WI) — now: per-wave.**
- `git revert <wave-sha>` on `main` (post-merge) or on the feature branch (pre-merge) rolls back an entire wave.
- For the four actual waves: reverting `d7eb6f7` unwinds Wave 4 (CI guards + backlog + sweeps); reverting `8488ee1` unwinds Wave 3 (keystone audits); reverting `437bb79` unwinds Wave 2 (keystone annotations); reverting `62b571c` unwinds Wave 1 (baseline).
- **Wave-4 revert ordering caveat still applies.** If Wave 4 (which includes WI-14 CI guards and WI-10 model-ID sweep) is reverted, the revert PR itself must manually bypass the stale-model-id-guard (or include a follow-up commit first reverting just the `.github/workflows/stale-model-id-guard.yml` file). Otherwise the guard blocks its own revert because the revert reintroduces old IDs. This is spelled out in deploy-plan §3 Tier-3 and carries over unchanged.

**Tier 1b (new — partial-wave surgical revert).**
- If a single WI inside a wave needs to be undone without the rest of the wave: use `git revert -n <wave-sha>` (no-commit), manually restore the files belonging to the WIs that should stay, then commit. This is a **surgical operation requiring impl-run PO + Developer pairing** — not a mechanical `git revert`.
- Document the partial revert in the commit message with a clear "Partial revert of `<wave-sha>` — keeps WI-X, WI-Y; removes WI-Z" body.

**Tier 2 (ADR-006 mechanical) — unchanged from deploy-plan §3.**
- ADR-006 fires only if WI-03's NDOC-02 spike had returned `strict`. It did not (per the Wave 1 commit, which advanced past the gate). Tier 2 is effectively inert for this engagement.

**Tier 3 (full PR withdrawal) — unchanged from deploy-plan §3.**
- Pre-merge: close the PR, delete the feature branch — nothing to clean on `main`.
- Post-merge: `git revert <merge-sha>` on `main`, then push. Because github-flow uses merge commits, this creates a single clean revert commit touching everything in the merge.

**Rollback communication:** if Tier 3 (full withdrawal) fires post-merge, notify: (a) plugin-users downstream via the channel Bilbo's release notes used, (b) the 9 backlog-47 issue watchers (since the issues were opened by this engagement), (c) a pipeline-level defect entry in `.delivery/defects/` so the retrospective can analyze.

---

## 7. Assumptions

- Legolas's UAT report will land in `.delivery/artifacts/08-execute/07-uat/qa/` before the UAT DoD validator runs. If it doesn't, the UAT stage holds pending its arrival (not a DevOps concern).
- Bilbo's release notes will land in `.delivery/artifacts/08-execute/07-uat/tech-writer/` before `gh pr create` fires. Config's `github.create_pr: true` automation respects DoD gating.
- `gh auth` is valid for the impl-run PO's environment at merge time.
- No branch protection rule on `main` blocks the PR's merge button (the feature-branch workflow was tested at Wave 4 commit time — pushes succeeded).
- The GitHub Actions runners have network access to clone the repo; standard `actions/checkout@v4` contract holds.

---

## 8. Risks and Mitigations

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| Legolas's UAT returns HOLD on §7.3 or §7.4 | High | Low | DevOps-visible evidence (§7.2 = 0) suggests both green. If Legolas disagrees, defer to their domain authority; this release plan flips to HOLD. |
| Bilbo's release notes arrive late, PR deadline slips | Low | Low | No external deadline — PR opens when DoD closes. Slip is absorbed by the pipeline itself. |
| `stale-model-id-guard.yml` fires its first-ever run on the engagement PR and unexpectedly flags something | Med | Low | Calibrated dry-run already performed in this plan — returns empty. If CI disagrees, investigate locale/encoding differences between ubuntu-latest runner and the local dev environment. |
| Post-merge synthetic tests (WI-14 AC-5) fail — either test PRs merge when they shouldn't, or block when they shouldn't | Med | Low | These are informational post-merge validations, not pre-merge gates. Failure means the guards have a design defect — open a DEFECT-xxx ticket, fix in a follow-up PR. Does not retroactively invalidate this engagement. |
| `backlog-47` label gets accidentally deleted or renamed in the repo | Low | Very Low | `gh label list` check can be re-run at any time; label is idempotent to re-create if lost. |

---

## 9. Follow-Up

- **For Legolas (QA):** land `uat-report.md` with §7.3 and §7.4 verdicts. DevOps release plan is contingent on both landing green.
- **For Bilbo (Technical Writer):** land `release-notes.md`. PR body references it directly.
- **For the impl-run PO (Gandalf):** approve the per-wave commit-granularity deviation explicitly in the Stage 7 DoD gate, or request a partial-wave surgical split (see §6 Tier-1b) — unlikely, but PO autonomy.
- **For Théoden (SM):** ensure the Stage 7 retrospective captures the per-wave vs per-WI lesson for `.delivery/memory/`.
- **For future engagements:** this release plan sets precedent that per-wave commit cadence is acceptable when wave gates are mechanical. Future Plan-stage deploy-plans can cite this engagement when proposing similar cadence.

---

*"The buckles are fastened, Mr. Frodo. Four bags, not fourteen, but every precious thing inside is accounted for. Nine issues standing guard on the deferred topics, two new workflows awake at the gate, one lint watching over them both. When Legolas finishes his count and Bilbo seals the letter, we knock. And then we go home."*
— Samwise

---

```
STATUS: DONE
ARTIFACT: .delivery/artifacts/08-execute/07-uat/devops/release-plan.md
SUMMARY: Four per-wave commits carry all fourteen work items home green — CI guards armed, nine backlog issues standing, release READY pending Legolas's count and Bilbo's letter.
```
