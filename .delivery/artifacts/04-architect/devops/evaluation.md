# DevOps Evaluation — Transformation Plan (Opus 4.6 → 4.7)

**Artifact:** Evaluator-Optimizer review (DevOps lens)
**Stage:** 4 / Architect — evaluator pass on `solution/transformation-plan.md`
**Date:** 2026-04-20
**Evaluator:** Samwise — *"I can't deploy the feature for you, Mr. Frodo, but I can carry the pipeline."*
**Input artifacts read:**
- `.delivery/artifacts/04-architect/solution/transformation-plan.md` (528 lines)
- `.delivery/artifacts/04-architect/adrs/` (26 ADR files; ADR-001..006 for 4-7 engagement read in full)
- `.delivery/artifacts/02-refine/po/prd.md` (spot-read via grep against CI / release / hook / branch keywords)
- `CLAUDE.md` (repo conventions, hook inventory, config v2.7)
- `.delivery/config.yml` lines 81–89 (git + github config)
- `.github/workflows/` contents (`docs.yml`, `release.yml`, `version.yml`, `workflow-injection-lint.yml`)
- `delivery-team/hooks/` (`hooks.json`, `verify_skill_load.py`, `audit_agent_prompt.py`, and listing of all 7 hook scripts)

---

## VERDICT: **ACCEPT**

The plan is deployable, reversible, and CI-aligned. Eight observations below are **Advisory (non-blocking)** — small hardening notes for the implementation-run PO to absorb opportunistically. None of them rise to REVISE severity; each has an identified owner-on-impl-run and a proposed disposition.

---

## 1. Deployability — PASS

**Finding:** Every wave / work item is shippable from within this repo alone. Zero cross-repo coordination, zero external registry updates, zero marketplace re-publishing, zero SDK credential rotation. `marketplace.json` is explicitly frozen per PRD Constraint 2 + ADR-005 Consequences. The plugin-manifest discovery contract is untouched (ADR-006 Option A lands inside the existing frontmatter YAML surface).

**Evidence:**
- Plan §3.2 "Untouched" row lists `marketplace.json`, `hooks.json`, all hook scripts, all `scripts/` utilities.
- Plan §3.3 change-type breakdown is (a) 2 Python files, (b) 6 prose-edited SKILL.md files + 11 frontmatter-backfilled SKILL.md files, (c) 13 alias YAMLs conditional-only, (d) backlog markdown file creation. All repo-local.
- No Wave requires a PyPI release, Docker image rebuild, container registry push, infrastructure change, or external API credential.

**Hidden deploy-time coupling checked:** None found. `prd-quality-gate-flow` has a SQLite DB (`prd_flows.db`) that *could* be a deploy-time coupling if MID-04 labels are routing keys. Plan §6.1 WI-10 and §8 ARCH-R6 both require the AC-01.5 structural gate on `flow_orchestrator.py` before MID-04 edits land. Coupling acknowledged and gated.

**DevOps disposition:** Accept as-is.

---

## 2. Rollback — PASS with one advisory

**Finding:** Plan §7.4 provides wave-level rollback via `git revert` and correctly observes that Wave 3 WIs cite only INTO `prompt-engineer/SKILL.md` (WI-05), preventing an intra-Wave-3 citation-web orphan on partial revert. Wave 4 items are per-WI revertable. No step in the plan performs irreversible state mutation (no file deletion of widely-referenced content; no DB schema migration; no tag deletion; no branch pruning).

**Irreversibility audit — each WI:**

| WI | Irreversible op? | Notes |
|---|---|---|
| WI-01 | None | Read-only log analysis, markdown output. |
| WI-02 | None | Baseline capture — write-only of new artifact. |
| WI-03 | None | WebFetch research + markdown finding. |
| WI-04 | None | Additive prose + frontmatter add. `git revert` clean. |
| WI-05 | None | Additive pattern-library section + PAT-01 reframe. `git revert` clean; reframe reverts cleanly. |
| WI-06 | None | Dogfood transcript + optional prose add. |
| WI-07 | None | Audit output file; optional prose add. |
| WI-08 | None | Audit output file; optional prose add. |
| WI-09 | None | Persona-review artifact; optional prose add. |
| WI-10 | **Low-risk mutation** | String substitution in 2 `.py` files. `git revert` re-introduces stale IDs (drift hygiene only — §3.1.1 zero SDK imports). |
| WI-11 | None | Additive frontmatter fields. |
| WI-12 | None | Conditional YAML edit; revert restores prior voice markers. |
| WI-13 | None | Backlog file creation. Revert removes files. |

**Advisory #1 (non-blocking):** Plan §7.4 does not explicitly address **`last_audited` date regression under Wave 3 revert.** If WI-04 (say) is reverted after WI-11 backfill has landed, the keystone loses its reviewed-state frontmatter while the 11 non-keystone files keep theirs — a state that technically violates ADR-006 semantics ("date reflects review state"). Cosmetic only; no runtime impact. Proposed disposition: impl-run adds a one-line convention in the WI-11 commit message — "if a keystone is reverted, its `last_audited` is reset by the revert itself; no backfill action needed." Document and move on.

**DevOps disposition:** Accept. Advisory #1 logged.

---

## 3. CI/CD alignment — PASS with one advisory

**Finding:** Plan explicitly names CI surface in two places:

- §3.1 "CI regression guards under `.github/workflows/` (`workflow-injection-lint.yml` — DEFECT-004 guard, must not regress per Constraint 6)" — ✓ acknowledged.
- §4.4 "CI warns (not blocks) on missing `model_awareness` field" — new CI check proposed.
- ADR-006 line 49: `grep -L "model_awareness:" **/SKILL.md` CI warning, "Lives alongside the existing `workflow-injection-lint.yml` regression guard pattern."
- §9 Table M-02: "Run M-02 regex (widened per challenger loop2 Finding #1 …) as part of CI."

**Evidence of CI alignment with repo reality:**
- Confirmed present: `.github/workflows/docs.yml`, `release.yml`, `version.yml`, `workflow-injection-lint.yml`.
- `release.yml` auto-generates GitHub Release notes from conventional commits (feat/fix/docs/chore) on `v*` tag push.
- `version.yml` auto-bumps semver in `marketplace.json` on main-push based on conventional commit prefix (`feat!:` → major, `feat:` → minor, `fix:` → patch).
- Existing CI thus **picks up migration commits automatically** with zero new pipeline wiring — implementation just needs to use conventional prefixes (see §5 below).

**Advisory #2 (non-blocking):** Plan mentions two new CI checks (DX-M4 `grep -L model_awareness` warning; M-02 stale-ID regex guard) but does not say **which workflow file they live in, who owns writing them, or which WI pays their cost.** Both are small bash one-liners, but neither has a WI anchor. Proposed disposition: impl-run PO to add a micro-WI "WI-14: CI guard wiring (DX-M4 header warn + M-02 stale-ID block) — XS" in Wave 4, or fold them into WI-13 as a sub-scope line. Non-blocking because both are plan-era-documented and have clear pattern (existing `workflow-injection-lint.yml` as reference template).

**DevOps disposition:** Accept. Advisory #2 logged against impl-run PO backlog.

---

## 4. Hooks impact — PASS

**Finding:** Plan is correct and definitive that **no hook edits are required.** Evidence converges from three independent places:

- Plan §3.2 "Untouched": all hook scripts under `delivery-team/hooks/` and `hooks.json` frozen per Constraint 2.
- Plan §3.3(e): "**No hook edits.** HK-01..07 are deterministic Python / SKILL_LOADED-detection only; zero LLM-facing prompt text. Confirmed by PRD §3.5 grep and round 2 DoD."
- Direct verification of `verify_skill_load.py` (34 lines) and `audit_agent_prompt.py` (regex-based) confirms these are pure Python text-pattern matchers — they do not issue prompts to Claude, they parse tool-call output.

**4.7 behaviour impact audit of each hook:**

| Hook | 4.7 behaviour risk | Finding |
|---|---|---|
| `check_config.py` (SessionStart) | None | Reads `.delivery/config.yml`; no LLM involvement. |
| Retrospective enforcement (Stop) | None | File-state check; no LLM involvement. |
| `enforce_pipeline_scope.py` (PreToolUse Skill) | None | Skill-name matching; no LLM involvement. |
| `audit_agent_prompt.py` (PreToolUse Agent) | **Possible over-match** | Regex-based compound-role detection. On 4.7, F-25 (literal instruction following) may cause dispatch prompts to be phrased more bluntly, triggering `_YOU_ARE_MULTI_RE` false positives if someone writes "You are the architect. You are also the evaluator." Low likelihood; warning-only (non-blocking); detectable in dogfood via spurious warnings in run logs. |
| `validate_gdscript.py` (PostToolUse Write/Edit) | None | Headless Godot parse; no LLM involvement. |
| `verify_skill_load.py` (PostToolUse Agent) | **Positive coupling** | Checks first 5 lines of agent output for `SKILL_LOADED:` marker. 4.7's F-25 literal-following tightens compliance with the "AFTER writing, respond with EXACTLY" contract — hit rate should go *up*, not down. Plan §9 M-07 already measures this. |
| `flag_empirical_validation.py` (SubagentStop) | None | Regex over stop reasons; no LLM involvement. |

**Advisory #3 (non-blocking):** The `audit_agent_prompt.py` false-positive risk under F-25 is worth a baseline-capture data point. Plan WI-02 captures SKILL_LOADED first-attempt rate but does not capture **audit-hook warning count per run.** Proposed disposition: impl-run PO adds one line to WI-02 acceptance — "capture count of `audit_agent_prompt.py` warnings emitted per dogfood run; establish baseline and monitor for regression in Waves 2–4." Non-blocking; the warnings are non-blocking already, so no deployment risk — this is observability hardening.

**DevOps disposition:** Accept. Advisory #3 logged. Plan's "no hook edits" conclusion stands firm.

---

## 5. Branching / commit strategy — PASS

**Finding:** Plan does not discuss branching and commit conventions explicitly, but nothing in the plan conflicts with the repo's configured strategy (`github-flow` + `auto_branch` + `conventional` + `clean_tree_check`).

**Verified repo config (`.delivery/config.yml` lines 81–89):**
```yaml
git:
  branch_strategy: github-flow
  auto_branch: true
  commit_convention: conventional
  clean_tree_check: true
github:
  create_issues: true
  create_pr: true
  link_commits: true
```

**Compatibility with plan:**
- Wave-based rollout (4 waves) + independent per-WI reverts fit github-flow's short-lived feature-branch-per-change pattern.
- Conventional commits align with `version.yml` auto-bump logic — the migration will ship as a `feat:` or `chore:` series, producing release notes automatically.
- `clean_tree_check: true` means each WI should land on its own branch via `auto_branch` — consistent with the plan's "per-WI revert" guarantee.

**Advisory #4 (non-blocking):** Plan does not specify **which conventional commit type each wave produces.** My recommendation for the impl-run PO:

| Wave | Proposed type(s) | Rationale |
|---|---|---|
| 1 | `chore:` (observability scaffolding, non-runtime) | Triggers no version bump — baseline capture is pre-work. |
| 2 | `docs:` (WI-04, WI-05 annotations) + `test:` (WI-06 dogfood) | Docs trigger no bump; preserves version stability during prose changes. |
| 3 | `docs:` (audits) or `feat:` if net-new pattern language ships | Minor bump iff WI-05's pattern library is treated as net-new capability. |
| 4 | `fix:` (WI-10 model-ID sweep — hygiene fix) + `chore:` (frontmatter backfill, backlog registration) | Patch bump on WI-10 feels right. |

None of this is blocking; the impl-run PO has autonomy to pick labels per `feedback_team_autonomy.md`.

**DevOps disposition:** Accept. Advisory #4 is guidance, not requirement.

---

## 6. Observability — PASS with one advisory

**Finding:** Baseline-capture mechanism (REQ-10 / WI-02) is operable and durable. Plan §6.1 WI-02 defines a concrete file path (`.delivery/artifacts/<impl-run>/observability/4-7-baseline.json`), a concrete content checklist (five items a–e), and a concrete measurement source (`verify_skill_load.py` telemetry + run logs). Galadriel §7 Q5 (absorbed into plan as row 5 of §6.3 table) specifies "lightweight shell + hook piggyback on `verify_skill_load.py`" — no new hook required, no new dependency.

**Operability check — can a human run this?**
- ✅ Path is pre-existing (`.delivery/artifacts/<impl-run>/observability/` follows the delivery-flow artifact convention).
- ✅ Measurement mechanism exists (`verify_skill_load.py` emits telemetry today).
- ✅ No new tooling required; `yq` and `grep` are already implied by existing metric definitions.
- ✅ Durable: file lives under `.delivery/` which is git-tracked (per the repo's convention of committing delivery artifacts — confirmed by the `.delivery/artifacts/` tree already being in `main`).

**Advisory #5 (non-blocking):** Plan WI-02 acceptance criteria says "JSON (or markdown) artifact … format is Architect's call; content is fixed." From a DevOps perspective, a strong preference for **JSON** is warranted because:
1. Downstream metrics (M-03, M-04, M-05, M-07) are numerical comparisons against the baseline — machine-readable wins over prose.
2. The baseline will be diffed across 2026-2027 runs — JSON Schema-able format protects against format drift.
3. `jq` queries are cheaper than regex-over-markdown in future CI wiring.

Proposed disposition: impl-run Architect picks JSON. If markdown wins, ensure at minimum a JSON-embedded code-fence block carries the numeric fields. Non-blocking.

**DevOps disposition:** Accept. Advisory #5 logged.

---

## 7. Release notes — PASS

**Finding:** Plan does not explicitly name release-note / CHANGELOG content — but this is correct, because the repo's `release.yml` **auto-generates release notes from conventional commits** on tag push. There is no hand-maintained `CHANGELOG.md`. The existing auto-release mechanism will surface the migration commits appropriately provided Advisory #4 (commit-type discipline) is honoured.

**Evidence:**
- `.github/workflows/release.yml` lines 32–88 build release notes by categorising `feat:/fix:/docs:/chore:` commits between tags.
- `.github/workflows/version.yml` auto-bumps `marketplace.json` version on `feat/fix/!` commits.
- No `CHANGELOG.md` file exists at repo root (verified via Glob convention — plan §3 does not reference one either).

**User-visible impact of the migration:**
- 6 SKILL.md files get additive prose (Waves 2–3) — low user-visible impact per invocation.
- 17 SKILL.md frontmatter fields added — invisible to skill invocation.
- 2 Python files get model-ID updates — zero runtime impact per §3.1.1.
- 13 alias theme YAMLs *possibly* edited conditionally — user-visible if regression fires.

**Advisory #6 (non-blocking):** The user-visible impact of Wave 3 audits is the *documentation* itself (patterns 4.1–4.6 arrive in `prompt-engineer/SKILL.md`). That IS a feature ship from a skill-author's perspective. Proposed disposition: impl-run PO ensures WI-05's commit uses `feat:` prefix so it auto-bumps minor version and lands in release notes under "Features." This is the one WI where commit-type matters load-bearingly.

**DevOps disposition:** Accept. Advisory #6 logged.

---

## 8. Risk during rollout (partial-migration windows) — PASS with caveat

**Finding:** Plan §4.4 "Fail-soft behavior" invariant explicitly addresses this: SKILL.md files stay model-agnostic in core instructions; 4.7-only guidance lives in `## Model-specific optimisation — Claude Opus 4.7` sub-sections. A skill called from a non-4.7 model still works; the 4.7 sub-section is additive.

**Windows of partial-migrated state — each risk:**

| Window | Broken state? | Why |
|---|---|---|
| Wave 1 ships, Wave 2 not yet | No | Wave 1 produces only observability artifacts — zero code behaviour change. |
| Wave 2 WI-05 ships, WI-04 not yet | No | Pattern library (WI-05) adds stable anchors; citations from WI-04 arrive later. Orphan-anchor risk is zero — anchors pre-exist before citations. |
| Wave 2 WI-04 ships, WI-05 not yet | **Minor issue** | WI-04 should cite Pattern 4.2 by name (per plan §6.1). If Pattern 4.2 doesn't exist yet, the citation orphans. Plan §3.4 dependency "ADR-005 pattern library expansion (WI-05) precedes the citation edits" correctly mitigates. |
| Wave 2 partial, Wave 3 starts | No | Wave 3 depends on WI-05 (plan §6.1 explicit "WI-05 must exist before citations land" — WI-07, WI-08 gated). |
| Wave 3 partial ship (e.g., WI-07 but not WI-08) | No | Wave 3 WIs cite only INTO `prompt-engineer/SKILL.md`, not between themselves. |
| WI-10 partial (e.g., MID-01 but not MID-04) | Low risk | §3.1.1 confirms zero SDK imports in affected files — stale IDs are drift hygiene, not runtime. Half-done sweep is ugly but not broken. |
| WI-11 partial (some SKILL.md files have frontmatter, others don't) | Grey zone | Functional: skill invocation still works (ADR-006 Consequences — YAML frontmatter accepts unknown fields per NDOC-02 spike assumption). Cosmetic: DX-M4 coverage < 100% until complete. |
| User has some plugins updated, others not (cross-plugin state) | **Not applicable** | All six plugins live in this repo and ship as one release. A user can't partially update them — they clone / install the marketplace and get the state of main. |

**Advisory #7 (non-blocking):** Plan §7.4 Wave 3 note about "Citations that pointed into Wave 3 content would orphan — mitigation: Wave 3 WIs cite only INTO `prompt-engineer/SKILL.md`" is correct but **puts the load-bearing rule in the rollback-strategy section**, not in the authoring-contract section. Proposed disposition: impl-run should restate this as an explicit rule in each WI-07/08/09's WI body — "This audit cites Pattern 4.N by name (resolving to `prompt-engineer/SKILL.md#pattern-4-N`) and does NOT cite prose in sibling Wave 3 files." Non-blocking; the plan's intent is already correct.

**Advisory #8 (non-blocking):** Plan does not discuss the scenario where **an implementation PR is merged to main but the release tag is delayed.** In this repo, `version.yml` auto-bumps on every push to main matching `feat:/fix:/!` — so a merged `feat:` WI immediately bumps the marketplace.json minor version and tags. Consumers who `git pull` between WI merges get intermediate states — which is fine because of the fail-soft invariant (§4.4), but worth calling out for the impl-run PO. Proposed disposition: impl-run PO batches Wave 2 and Wave 3 merges on a feature branch if strict transactional "all-waves-or-none" shipping is wanted; otherwise accept rolling ship. `feedback_team_autonomy.md` says the team decides — Samwise's recommendation is **rolling ship is fine** because of the fail-soft invariant.

**DevOps disposition:** Accept. Advisories #7 and #8 logged.

---

## Advisory Register (consolidated)

| # | Area | Severity | Proposed disposition | Owner on impl-run |
|---|---|---|---|---|
| 1 | Rollback + `last_audited` date hygiene | Cosmetic | One-line convention in WI-11 commit message | Impl-run PO |
| 2 | CI guards for DX-M4 + M-02 have no WI anchor | Low | Add "WI-14: CI guard wiring (XS)" in Wave 4 OR fold into WI-13 | Impl-run PO |
| 3 | `audit_agent_prompt.py` F-25 false-positive baseline | Low | Capture warning-count in WI-02 baseline | Impl-run PO |
| 4 | Commit-type mapping per wave | Guidance | Use the wave-to-type table above; impl-run PO has autonomy | Impl-run PO |
| 5 | Prefer JSON for baseline file (vs markdown) | Guidance | Architect pick JSON in WI-02 format call | Impl-run Architect |
| 6 | WI-05 should use `feat:` prefix for release-note visibility | Guidance | Impl-run commit discipline | Impl-run Developer |
| 7 | Wave-3 citation-into-WI-05-only rule should be in WI bodies, not only §7.4 | Cosmetic | Restate rule in WI-07/08/09 bodies | Impl-run Architect |
| 8 | Rolling-ship vs batched-ship decision for Waves 2–3 | Decision | Accept rolling ship (fail-soft invariant holds); document choice | Impl-run PO |

**None of the eight advisories is blocking.** All eight can be absorbed opportunistically by the implementation run without re-architecture.

---

## Samwise's Closing

*"The pipeline carries. The waves march. The fail-soft invariant keeps the lantern lit between stops. The release notes write themselves on the way home. Eight pebbles in my pocket for the road — none big enough to trip over, all small enough to hand to Mr. Frodo with a nod."*

*"I can't deploy the feature for you, Mr. Frodo, but I can carry the pipeline."*

— **Samwise**, DevOps

---

**End of DevOps Evaluation.**
