# Deploy Plan — Opus 4.7 Plugin-Skill Migration

**Engagement:** `run-2026-04-22-4x7e` (FEATURE, Stage 5 Plan)
**Role:** DevOps — Samwise Gamgee speaking
**Upstream execution-PRD:** `.delivery/artifacts/08-execute/02-refine/po/execution-prd.md`
**Config source of truth:** `.delivery/config.yml` (git + github sections)
**CI template reference:** `.github/workflows/workflow-injection-lint.yml`
**Status:** Draft for Plan-stage DoD

---

> *"I can't deploy the feature for you, Mr. Frodo, but I can carry the pipeline. Fourteen work items, four waves, one branch, one PR at the end. No cloud, no containers — just commits, workflows, and a handful of issues. That I can carry. We walk it together."*
> — Samwise

---

## 1. Deploy Surface

There's no server to push to, Mr. Frodo. The "deploy" for this engagement is what lands in the repo and in GitHub. Here's the whole surface, laid out plain:

**Source code edits (keystone — prose-reviewed):**
- `delivery-team/skills/delivery-flow/SKILL.md` (WI-04)
- `prompt-engineer/SKILL.md` (WI-05)
- `research-agent/SKILL.md` (WI-06)
- `delivery-team/skills/product-delivery/SKILL.md` (WI-07)
- `delivery-team/skills/architect/SKILL.md` (WI-08)
- `mtg-commander/SKILL.md` (WI-09)

**Source code edits (mechanical — frontmatter-only):**
- 11 non-keystone SKILL.md files per WI-11 AC-1 (frontmatter backfill only, no prose)

**Python edits (WI-10 model-ID sweep):**
- `agentic-flow-builder/scripts/agent_registry.py` (lines 148, 172, 187)
- `prd-quality-gate-flow/stage_definitions.py` (lines 47, 83, 115, 150, 181, 216, 243, subject to AS-IS outcome)

**Supporting single-line edit (per WI-05 AC-7):**
- `research-agent/references/prompt-library.md` line 10

**CI workflows (new, under `.github/workflows/`):**
- `skill-md-header-warn.yml` — warning-only (DX-M4)
- `stale-model-id-guard.yml` — blocking (M-02)

**Backlog docs (`.delivery/backlog/`):**
- 6 required `BACKLOG-47-*.md` files
- Up to 3 optional Galadriel on-ramp `BACKLOG-47-*.md` files (time-permitting)

**Pipeline artifacts (documentation trail):**
- All `.delivery/artifacts/08-execute/**` stage outputs (already in-tree as edits land)

**GitHub surface:**
- 6 issues labeled `backlog-47` (dual-write per WI-13; up to 9 with Galadriel on-ramp)
- 1 PR bundling the entire engagement (per `github.create_pr: true`)

No binaries. No containers. No cloud infrastructure. No secrets. Just text edits, YAML, and GitHub API calls. That's the whole ring, Mr. Frodo — and it's not heavy, only awkward.

---

## 2. Branching and Commits

Config pins the rules. We honour them.

- `git.branch_strategy: github-flow` → single feature branch off `main`. No release branches, no develop branch.
- `git.auto_branch: true` → branch created at Plan stage (this stage), not deferred to Development.
- `git.commit_convention: conventional` → `type(scope): subject` form on every commit.
- `git.clean_tree_check: true` → UAT verifies the working tree is clean before the PR opens.

**Proposed branch name:**

```
feature/opus-4-7-migration-run-2026-04-22-4x7e
```

The run-ID suffix keeps it traceable back to this engagement's artifacts folder. Created off latest `main` at the start of Wave 1.

**Commit cadence — the choice:**

| Option | Commit Count | Reverability | Narrative Trail |
|--------|--------------|--------------|-----------------|
| Per-wave | 4 | Coarse — revert rolls back ~3–6 WIs together | Each wave is one story |
| **Per-WI (preferred)** | **14** | **Per-WI `git revert` isolates every change** | **Each WI has its own story, audit-ready** |

**Recommendation: per-WI commits.** ADR-002 (direct strings with provenance comments) and ADR-005 (single-file pattern library) were both designed so that a single WI revert is sufficient to unwind a single change. Fourteen commits costs us nothing — GitHub doesn't charge per commit, and the PR summary renders them cleanly. What it buys us is precision: if WI-09 (mtg-commander adversarial-tone audit) lands and later the impl-run PO decides the tone edit was too heavy, one `git revert <sha>` unwinds it without touching WI-04 or WI-07.

**Commit message shape (per-WI):**

```
<type>(scope): <one-line subject, imperative mood>

WI-NN — <story title from execution-PRD §2>
Refs: <REQ anchors>, <ADR anchors>
Dogfood: <one-line dogfood command outcome>
```

**Type mapping per WI class** (Samwise advisory #4 — impl-run PO has autonomy here, this is my recommended default):

| WI Class | Type | Example |
|----------|------|---------|
| WI-01, WI-02 (observability capture) | `chore` | `chore(observability): capture 4.7 AS-IS dispatch counts` |
| WI-03 (research spike) | `docs` | `docs(research): NDOC-02 frontmatter-contract verdict` |
| WI-04, WI-05, WI-06, WI-07, WI-08, WI-09 (keystone SKILL.md) | `docs` | `docs(delivery-flow): annotate 4.7 dispatch contract` |
| WI-10 (Python model-ID sweep) | `fix` | `fix(model-ids): sweep stale dated IDs per ADR-002` |
| WI-11 (frontmatter backfill) | `docs` | `docs(skills): backfill ADR-006 frontmatter on 11 files` |
| WI-12 (alias-theme dogfood) | `chore` or `fix` | depends on pass/fail |
| WI-13 (backlog dual-write) | `chore` | `chore(backlog): register 6 BACKLOG-47-* deferrals` |
| WI-14 (CI guards) | `ci` | `ci(workflows): add header-warn and stale-ID guards` |

`github.link_commits: true` is on — each commit body references the matching `backlog-47` issue number where applicable (WI-13 commits reference their own issues).

---

## 3. Rollback Plan

Three tiers, matched to the three ADRs that shaped this scope:

**Tier 1 — Per-WI rollback (ADR-002, ADR-005):**

Any individual WI commit can be reverted with `git revert <sha>` on the feature branch. ADR-002 put direct model-ID strings with provenance comments (no central alias module), so a WI-10 revert only touches the files WI-10 edited — no multi-file unwind. ADR-005 put the pattern library in one file (`prompt-engineer/SKILL.md`), so WI-05 revert is a single-file unwind; Wave 3 citations (WI-07, WI-08) cite **into** WI-05 and not between themselves, so no citation web breaks.

**Tier 2 — ADR-006 mechanical rollback (within-engagement):**

If WI-03's NDOC-02 spike returns `strict`, ADR-006 fires automatically: WI-04, WI-05, WI-06, and WI-11's frontmatter edits flip from YAML fields to HTML-comment form (`<!-- model_awareness: opus-4-7 -->` below the closing `---` of each file). Same three fields, same semantics, different placement. This is a **within-engagement branch**, not a post-deploy rollback — it fires at the Wave 1 → Wave 2 gate before any frontmatter edit has landed.

**Tier 3 — Full-engagement rollback (PR withdrawal):**

If the engagement is pulled entirely at UAT, `git revert <first-commit>..<last-commit>` on the feature branch, then close the PR. Because everything lives on a feature branch and `main` is never touched until merge, there's no `main`-history damage to repair. Nothing to clean up on the server — there is no server.

**Wave-4 revert order discipline** (carried from transformation-plan §7.4):

If a Wave-4 rollback is ever needed after partial merge, revert **WI-14 before WI-10 or WI-11**. Otherwise `stale-model-id-guard.yml` blocks the revert PR that re-introduces the stale IDs we're removing. The guard doesn't know it's a rollback — it sees stale IDs and fails. Revert the guard first, then the sweep.

---

## 4. CI Pipeline Changes

WI-14 adds two new workflows under `.github/workflows/`. Both use `workflow-injection-lint.yml` as their structural template — same YAML shape, same permissions posture, same failure-mode contract. No new secrets, no new runners, no third-party actions.

**Workflow 1 — `skill-md-header-warn.yml` (warning-only, DX-M4 guard):**

- **Trigger:** `pull_request` on paths `**/SKILL.md`
- **Runs:** `git ls-files '*SKILL.md' ':!:.delivery/*' | xargs grep -L 'model_awareness:'`
- **Mode:** warning — job reports missing-header files in step summary or PR comment; does not block merge (`continue-on-error: true` on the check step, or emit a warning-level annotation)
- **Purpose:** if a future PR adds a new SKILL.md without the ADR-006 frontmatter, CI surfaces it — but doesn't block, because this is DX hygiene, not correctness

**Workflow 2 — `stale-model-id-guard.yml` (blocking, M-02 guard):**

- **Trigger:** `pull_request` on paths `**/*.py`, `**/*.md` (excluding `.delivery/` and `prd_flows.db`)
- **Runs:** the PRD-canonical M-01/M-02 regex across tracked `.py` and `.md` files
  - `grep -rEn 'claude-(opus-4-20250514|sonnet-4-5-20250929|haiku-4-20250514)' <scope>`
- **Mode:** blocking — any hit fails the check, PR cannot merge until resolved
- **Purpose:** prevents a future PR from re-introducing a stale dated ID; M-02 no-regression guarantee

**Both workflows share the template pattern:**

- `permissions: contents: read` (minimal)
- `runs-on: ubuntu-latest`
- `actions/checkout@v4` for source access
- No `${{ github.event.* }}` inside `run:` blocks (DEFECT-004 regression guard still applies — the existing `workflow-injection-lint.yml` will check these two new files on the same PR)
- Pinned to the shell-only, Python-only patterns already in `workflow-injection-lint.yml` — no new dependencies

**Synthetic-test validation (WI-14 AC-5):** after merge, a throwaway test PR re-introducing `claude-opus-4-20250514` should fail the stale-ID guard; a throwaway test PR adding a SKILL.md without `model_awareness:` should produce a warning but merge cleanly. These are one-off validations, not ongoing gates.

---

## 5. GitHub Integration

Config already has the three GitHub switches we need:

| Key | Value | Consequence |
|-----|-------|-------------|
| `github.create_issues` | `true` | PO/SM uses `gh issue create --label backlog-47` for each BACKLOG-47 topic during WI-13 |
| `github.create_pr` | `true` | Single PR at UAT stage bundles the engagement |
| `github.link_commits` | `true` | Each commit body references the issue number where applicable |

**Issue creation (WI-13):**

Six `gh issue create --label backlog-47` invocations (plus up to 3 optional Galadriel on-ramp), one per topic:

1. `BACKLOG-47-task-budget-eval`
2. `BACKLOG-47-memory-tool-eval`
3. `BACKLOG-47-sdk-wiring-routing-via-claude-api`
4. `BACKLOG-47-r-06-cyber-safeguard-prose-spot-read`
5. `BACKLOG-47-frontmatter-only-prose-skim`
6. `BACKLOG-47-overpressure-audit`

Title format: `[BACKLOG-47] <topic>` — body references the matching `.delivery/backlog/BACKLOG-47-<topic>.md` file and a link back to the transformation-plan. Label `backlog-47` is the load-bearing join key — the §7.5 verification command counts issues with this label and matches them to local files.

If the label doesn't exist yet in the repo: first `gh label create backlog-47 --color <hex>` once, then the six issue creates. Impl-run autonomy on color choice.

**PR creation (UAT stage):**

Single `gh pr create` at UAT. Proposed title:

```
feat(delivery): execute Opus 4.7 migration plan (run-2026-04-22-4x7e)
```

PR body includes:
- Link to the execution-PRD
- Link to the transformation-plan
- List of all 14 WIs with their dogfood-pass status
- All six §7 verification command outputs
- Closes-reference for any BACKLOG-47 issues that are being closed by this engagement (most will stay open as deferrals)

---

## 6. Monitoring During the Run

There is no production to watch. The run monitors itself through the dogfood gates:

- **Per-WI:** Developer DoD runs the WI's dogfood command. Each WI in the execution-PRD §2 carries one. Pass/fail is mechanical — exit code tells the truth.
- **Per-wave:** Wave-exit gate is a single command or file-existence check (execution-PRD §5). Wave 1 → 2 checks the NDOC-02 verdict. Wave 2 → 3 checks the six `### Pattern 4.N —` headings. Wave 3 → 4 checks the WI-06 and WI-09 JSON verdicts. Wave 4 → UAT runs the three-command check from §5.
- **Sprint-exit (pre-PR):** the six §7 verification commands from the execution-PRD. All six must return their expected values. This is the final go/no-go gate before PR opens.

No alerting, no dashboards, no SLOs. The dogfood commands themselves are the alert system. If a dogfood exits non-zero, the WI doesn't merge its commit — the impl-run PO decides whether to fix-and-re-run or re-plan within the same wave.

---

## 7. Go / No-Go Checklist (pre-PR at UAT)

Samwise's pre-flight check. All boxes must be ticked before `gh pr create` runs.

- [ ] All 14 WI commits land on `feature/opus-4-7-migration-run-2026-04-22-4x7e`
- [ ] All 6 execution-PRD §7 verification commands return expected values locally
  - [ ] §7.1 M-01 stale-ID grep: exit 0, no hits
  - [ ] §7.2 DX-M4 missing-header count: `0`
  - [ ] §7.3 Two-tier stamp integrity: 6 keystones + 11 backfill, exit 0
  - [ ] §7.4 DX-M3 `<thinking>` restatement count: `0`
  - [ ] §7.5 Dual-write invariant: equal counts, both ≥ 6, exit 0
  - [ ] §7.6 CI guard files all present: exit 0
- [ ] `stale-model-id-guard.yml` green on feature branch HEAD
- [ ] `skill-md-header-warn.yml` warning-free (0 SKILL.md files missing marker)
- [ ] `workflow-injection-lint.yml` still green on the two new workflow files (Constraint 6 / DEFECT-004 regression guard)
- [ ] At least 6 GitHub issues labeled `backlog-47` open (optionally 9 if Galadriel on-ramp time permitted)
- [ ] Every `BACKLOG-47-*.md` file has a matching `backlog-47` issue; every issue has a matching file (WI-13 dual-write invariant)
- [ ] `git status` clean on feature branch (per `git.clean_tree_check: true`)
- [ ] Release notes drafted by Technical Writer (Bilbo) — summarising the 14 WIs, the ADRs bound, and the end-state gates

When every box is ticked, the PR opens. Not before. That's how we carry it all the way to Mount Doom — one step, one check, one careful foot after another.

---

## 8. Assumptions

- `gh` CLI is installed and authenticated for the impl-run PO's environment. Config doesn't specify the auth token; assume standard `gh auth login` has been completed.
- The `backlog-47` GitHub label either exists or will be created once as a one-off before the first issue-create runs.
- No branch protection rules currently block direct pushes to the feature branch — github-flow assumes PR-based merges to main but allows feature-branch freedom.
- The two new CI workflows will run on the feature branch PR before merge — GitHub Actions `pull_request` trigger defaults handle this.
- Feature branch lives for the duration of the engagement (Wave 1 through UAT); no long-running branch concerns.

---

## 9. Risks and Mitigations

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| `stale-model-id-guard.yml` blocks the WI-10 PR because WI-10 commits arrive before the guard is active | Med | Low | WI-14 AC-6 sequences WI-14 AFTER WI-10 and WI-11 land; guard activates on a green tree |
| Per-WI revert on Wave 4 hits the stale-ID guard | Med | Low | §3 Tier-3 discipline: revert WI-14 before WI-10/11 in a rollback scenario |
| `backlog-47` label doesn't exist and first `gh issue create` fails | Low | Med | Pre-create the label once; impl-run PO autonomy on color |
| ADR-006 `strict` verdict from WI-03 flips frontmatter placement mid-flight | Low | Low | ADR-006 is mechanical — no re-litigation; WI-04/05/06/11 simply use HTML-comment form. Semantics identical. |
| Synthetic-test PR (WI-14 AC-5) pollutes main branch or issue list | Low | Low | Use throwaway branches, close without merge, delete after validation |

---

## 10. Follow-Up

- **For the Developer (Gimli):** each WI's dogfood command is the Definition-of-Done signal — run it, record exit code, only then request commit.
- **For the SM (Théoden):** wave gates are mechanical per execution-PRD §5 — don't advance the wave until the gate command passes.
- **For the Technical Writer (Bilbo):** release notes are drafted at UAT stage, not Plan stage — this plan does not author them, only earmarks the task.
- **For the impl-run PO (Gandalf):** autonomy on shipping cadence (rolling vs batched commits — Samwise advisory #8), commit-type mapping adjustments, and Galadriel on-ramp triplet inclusion.

---

*"There and back again, Mr. Frodo. Fourteen commits, two workflows, six issues, one PR. No fire, no cloud — just text and discipline. I'll carry the pipeline. You carry the scope."*
— Samwise

---

```
STATUS: DONE
ARTIFACT: .delivery/artifacts/08-execute/05-plan/devops/deploy-plan.md
SUMMARY: One feature branch, fourteen per-WI commits, two new CI guards, six backlog issues, one PR at UAT — I'll carry the pipeline, Mr. Frodo.
```
