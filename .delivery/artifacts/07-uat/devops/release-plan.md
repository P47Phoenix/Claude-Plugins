<!-- run: run-2026-05-09-tk4 | stage: 07-uat | depth: full | author: DevOps (Boromir of Gondor) | sources: stories.md, ADR-tk4-{001,002,003}, story-{1..7}-implementation.md, governance/cache-prefix-hash.txt | wave: 3 — closure -->

# Stage 7 Release Plan — Wave 3 (BACKLOG-104)

> "Give us the chance, and you shall have my respect." — Boromir, Captain of Gondor.

Squash-rebase + ff-merge to `main` (no PR) — the same march proven through Waves 0/1/2 and caveman-lite. Rollback armed runtime (frontmatter revert) + structural (`git revert <merge>`) per ADR-tk4-003.

## 1. Release Scope

**Source-tree (7 stories' surface, post-Stage-6 CODE_COMPLETE):**

| # | Stories / WIs | Surface |
|---|---|---|
| S1 | W3-1 architect Tier-B closure | `delivery-team/skills/architect/SKILL.md` + new `references/{decomposition,roles,contracts,guardrails}/*.md` per ADR-tk4-001 (5 extractions, pointer tables in SKILL.md). |
| S2 | W3-2/3/4 presentation+ui+operations trims | `delivery-team/skills/{presentation,ui,operations}/SKILL.md` + `references/**` (types/flow/formats/roles/contracts). 3 files parallel-safe. |
| S3 | W3-5/6/7 quality+user-feedback+godot trims | `delivery-team/skills/{quality,user-feedback,godot}/SKILL.md` + `references/**`. Godot zero-headroom (=200 exactly post-frontmatter). |
| S4 | W3-8 paradigm sub-skill pattern | `research-agent/skills/research-types/<type>/SKILL.md` ×5 + `delivery-team/skills/user-feedback/skills/personas/<family>/SKILL.md` ×4 (joint with S3) + `.github/workflows/marketplace-discoverability-lint.yml` per ADR-tk4-002. |
| S5 | W3-9 governance frontmatter rollout | All 13 delivery-team SKILL.md +3 keys (`maintainer`, `fitness_review_due`, `context_budget`); `governance/cache-prefix-hash.txt` regenerated (1→13 file scope, current `43067c9e...`); `scripts/lint_skill_frontmatter.py` + `.github/workflows/skill-frontmatter-lint.yml` per ADR-tk4-003. |
| S6 | W3-10/11/12 retro KPI + fitness review + CLAUDE.md | `delivery-flow/references/retrospective-template.md` (KPI); `governance/fitness-review.md` + `.github/workflows/fitness-review.yml` (cron); `CLAUDE.md` 168→**112** with plugin-detail extracted to per-plugin ARCHITECTURE.md. |
| S7 | W3-13..18 admin + carry-forwards | `delivery-flow/references/validator-prompt-template.md`; `scripts/lint_known_debt.py` + `.github/workflows/lint-known-debt.yml` (W3-14); STATUS standardization + Stage 7 entry-step in `delivery-flow/SKILL.md` + `quality-gates.md` (closes DEFECT-006); `governance/git-hooks-install.md` + pre-commit script (W3-16); `delivery-team/hooks/telemetry.py` (W3-18 `placeholder=true`); `governance/skill-budgets.json` re-baselined (`known_debt[]` empty — closes initiative AC-1). |

**Run record (`.delivery/artifacts/`):** all Stage 1..7 stage-summaries, dod reviews, ADR-tk4-{001,002,003}, stories.md, story-{1..7}-implementation.md, release-plan.md, go-no-go-input.md ride in the same commit per Wave 0/1/2/caveman-lite precedent. Working-tree count at author time: `git status --short | wc -l` = **118**. Orchestrator re-captures pre-commit.

## 2. Pre-merge Verification (orchestrator runs immediately before `git add -A`)

```bash
python3 scripts/check_skill_budgets.py
# Verified: "BUDGET CHECK PASSED: 17 file(s) checked, 0 known-debt, 0 exception(s)."  rc=0

python3 scripts/lint_known_debt.py
# Verified: "LINT OK: known_debt JSON↔Python in sync; all SKILL.md frontmatter complete."  rc=0  (W3-14)

wc -l CLAUDE.md
# Verified: 112 (≤150; W3-12 binding satisfied with 38-line headroom)

wc -l delivery-team/skills/godot/SKILL.md
# Verified: 200 (=200 exactly; round-2 zero-headroom binding from ADR-tk4-001)

wc -l delivery-team/skills/delivery-flow/SKILL.md
# Verified: 499 (≤500; Tier-A invariant preserved)

python3 -c "import hashlib; h=hashlib.sha256(open('delivery-team/skills/delivery-flow/SKILL.md','rb').read()).hexdigest(); assert h in open('governance/cache-prefix-hash.txt').read(); print('OK')"
# Verified: OK (cache-prefix hash = 43067c9e07e0b988...; matches per ADR-tk4-003)

git status --short | wc -l
# Verified: 118 (record exact count in commit body)
```

All six commands returned expected values during release-plan authoring. **Halt on any non-zero exit or unexpected output** — do not proceed to merge.

## 3. Merge Procedure

Branch precondition: HEAD = `feature/wave-3-tk4` (already checked out). All Stage 1..7 artifacts in working tree. No separate PR per binding directive.

```bash
git add -A

git commit -m "$(cat <<'EOF'
feat(delivery-team): Wave 3 skill token-economy completion (BACKLOG-104)

Closes Tier-B/C SKILL.md ceilings across delivery-team, ships the
canonical paradigm sub-skill pattern (ADR-tk4-002), and operationalizes
governance frontmatter + quarterly fitness review (ADR-tk4-003).
Discharges all six Wave-3 retro carry-forwards on the same wave.

ADR-tk4-001 ratifies the per-file extraction strategy. ADR-tk4-002
codifies disable-model-invocation: true + marketplace-discoverability
invariant. ADR-tk4-003 mandates the cumulative cache-prefix re-freeze
(scope 1→13 files) and binds Dev to run-the-command at DoD.

Stories shipped (7/7):
  S1 W3-1        architect Tier-B closure
  S2 W3-2/3/4    presentation + ui + operations trims
  S3 W3-5/6/7    quality + user-feedback + godot trims (godot =200)
  S4 W3-8        paradigm sub-skill pattern (research-agent + personas)
  S5 W3-9        governance frontmatter rollout (13 files; hash refreshed)
  S6 W3-10/11/12 retro KPI + fitness review + CLAUDE.md →112
  S7 W3-13..18   validator template + lint-known-debt + STATUS standard
                 + pre-commit hook + Stage-7 entry sweep + telemetry
                 + skill-budgets.json re-baseline (known_debt[] empty)

AC-13 close-out: empirical token-reduction baseline runs NEXT pipeline
(W3-18 placeholder=true ensures KPI excludes missing-measurement rows).

Cache-prefix hash (delivery-flow/SKILL.md whole-file SHA-256):
prior f997ec25... -> current 43067c9e07e0b988... per ADR-tk4-003.

DEFECT-006 closes at merge of W3-17. Initiative AC-1 closes:
known_debt[] empty for delivery-team scope (first since BACKLOG-100).

Refs: ADR-tk4-001, ADR-tk4-002, ADR-tk4-003, BACKLOG-104, run-2026-05-09-tk4
EOF
)"

git checkout main
git rebase feature/wave-3-tk4
git merge --ff-only feature/wave-3-tk4
git push origin main
git branch -d feature/wave-3-tk4
```

Conventional-commit format follows Wave 0/1/2/caveman-lite precedent.

## 4. Post-merge Verification

```bash
git log --oneline -3
# Top line: "feat(delivery-team): Wave 3 skill token-economy completion (BACKLOG-104)"
git diff main..origin/main          # expected: empty
```

W3-14 CI workflow (`.github/workflows/lint-known-debt.yml`) validates on the next PR; W3-16 pre-commit hook is opt-in per `governance/git-hooks-install.md` (absence does not block merges). `skill-line-budget.yml` triggers on `pull_request:` only — the binding ff-push to main does NOT fire CI budget gates; §2 local invocation IS the authoritative budget verification (precedent: Wave caveman-lite).

## 5. Rollback Procedure (per ADR-tk4-003)

**Runtime opt-out — low-cost, preferred (per-file granularity).** Each frontmatter rollout is a 3-line addition to one SKILL.md. Frontmatter keys are advisory at runtime (CI lint enforces; orchestrator does not consume `maintainer` / `fitness_review_due` / `context_budget`). Per-file revert is safe.

```bash
git checkout HEAD~1 -- <skill.md>                          # or hand-edit the 3 lines out
echo "f997ec25...  delivery-team/skills/delivery-flow/SKILL.md" \
  > governance/cache-prefix-hash.txt                       # restore prior hash if affected
sha256sum delivery-team/skills/delivery-flow/SKILL.md      # verify
```

**Structural rollback — high-cost, only if multiple stories regress (e.g., paradigm router fault, frontmatter lint regression):**

```bash
git revert <merge-commit-sha>   # Stories 1–7 are squashed; revert restores all 7 states.
git push origin main
```

## 6. Hazards / Watch Items

1. **Cache re-warm cost (one-time, ~650B × 13 files = ~26KB, accepted).** First post-merge dispatch invalidates the cache-prefix slice across all 13 delivery-team SKILL.md (ADR-tk4-003 §Cumulative cache-prefix impact). Bounded; informational.
2. **W3-18 telemetry chicken-and-egg.** Hardened `placeholder=true` route lands in this merge; first effective baseline for the W3-10 KPI starts NEXT pipeline. Orchestrator captures NEXT-run telemetry as the first authoritative data point.
3. **Pre-commit hook adoption (opt-in).** W3-16 hook installation is voluntary per `governance/git-hooks-install.md`; CI `skill-line-budget.yml` PR gate remains authoritative. Not a blocker.
4. **AC-13 (BACKLOG-102 carry-forward) empirical measurement pending.** First post-merge prose-token telemetry validates AC-13; <15% reduction trips the BACKLOG-102 stop-rule retro. Orchestrator captures on first post-merge dispatch.
5. **Known-debt registry baselines empty for first time since BACKLOG-100.** Any new non-compliant file re-arms the registry; W3-14 JSON↔Python lint (rc=0) is the regression guard.

## 7. Go/No-Go Input (DevOps lens, summary)

```
DevOps Recommendation: GO
Rationale: all six pre-merge verification commands return expected
outputs (check_skill_budgets rc=0 / 0 known_debt; lint_known_debt rc=0;
CLAUDE.md=112≤150; godot=200 exact; delivery-flow=499≤500;
cache-prefix hash matches 43067c9e...); merge strategy proven through
4 prior waves; rollback armed at runtime per-file + structural levels.
Risks: 0 BLOCKING; 1 P1 (AC-13 empirical token-reduction baseline NEXT
       pipeline per BACKLOG-102 stop-rule); 1 P2 (cache re-warm 26KB
       one-time); 1 P3 (pre-commit hook adoption opt-in).
```

Detailed input: `.delivery/artifacts/07-uat/devops/go-no-go-input.md`.

STATUS: DONE
ARTIFACT: .delivery/artifacts/07-uat/devops/release-plan.md
SUMMARY: Wave 3 marches to ff-merge; gates pass clean (0 known_debt, hash 43067c9e, godot=200, CLAUDE=112); rollback armed runtime+structural per ADR-tk4-003.
