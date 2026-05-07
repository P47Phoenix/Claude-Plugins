<!-- run: run-2026-05-05-tk3 | stage: 07-uat | depth: full | author: DevOps (Boromir of Gondor) | sources: story-1-implementation.md, ADR-tk3-001, stories.md -->

# Stage 7 Release Plan — Wave caveman-lite (BACKLOG-102)

> "It is a strange fate that we should suffer so much fear and doubt over so small a thing." — Boromir, Captain of Gondor.

The road is short. Squash-rebase + ff-merge to main, no PR — proven through Waves 0/1/2. Rollback armed at runtime and structural levels.

## 1. Release Scope

**Source-tree (7 files, Story-1 list verified at Stage 6 CODE_COMPLETE):**

| Path | Change |
|---|---|
| `delivery-team/skills/delivery-flow/SKILL.md` | +3 lines (Phase 0 +1; Phase 4 Step 4 pointer +2). 500/500 at ceiling. |
| `delivery-team/skills/delivery-flow/references/config-schema.json` | regenerated; gains `prose_style`; `config_version` default `"2.9"`. |
| `delivery-team/skills/delivery-flow/references/config-schema.md` | v2.8 → v2.9; new `prose_style` row; template gains `prose_style: caveman-lite`; Version History v2.9 row dated 2026-05-05. |
| `delivery-team/skills/delivery-flow/references/pipeline-stages.md` | PROSE STYLE block inserted in 3 dispatch templates (Primary, Supporting, DoD Validator) between `--- ALIAS ---` and `--- OUTPUT ---`. |
| `delivery-team/skills/delivery-flow/references/quality-gates.md` | one instructional line in DoD Validator template directing caveman-lite verdict prose. |
| `delivery-team/skills/delivery-flow/references/prose-style.md` | NEW (40 lines) — verbatim PROSE STYLE block, extracted to keep SKILL.md within ceiling. |
| `governance/cache-prefix-hash.txt` | regenerated. New: `f997ec25...`. Prior: `9d4011d1...`. |

**Run record (`.delivery/artifacts/`, Stages 1..7):** all stage-summaries, dod review files, ADR-tk3-001, architecture-tk3-caveman-lite.md, stories.md, story-1-implementation.md, release-plan.md, go-no-go-input.md — ride in the same commit per Wave 0/1/2 precedent.

Working-tree count at author time: `git status --short | wc -l` = **39**. Orchestrator re-captures pre-commit.

## 2. Pre-merge Verification (orchestrator runs immediately before `git add -A`)

```bash
python3 scripts/check_skill_budgets.py                                # rc=0, "BUDGET CHECK PASSED: 13 file(s) checked, 7 known-debt, 0 exception(s)."
wc -l delivery-team/skills/delivery-flow/SKILL.md                     # 500
python3 -c "import json; d=json.load(open('delivery-team/skills/delivery-flow/references/config-schema.json')); assert d['properties']['prose_style']['default'] == 'caveman-lite'; print('OK')"   # OK
python3 -c "import hashlib; assert hashlib.sha256(open('delivery-team/skills/delivery-flow/SKILL.md','rb').read()).hexdigest() in open('governance/cache-prefix-hash.txt').read(); print('OK')"  # OK
git status --short | wc -l                                            # note count for commit message
```

All five returned expected values during release-plan authoring. Halt on any non-zero or unexpected output.

## 3. Merge Procedure

Branch precondition: HEAD = `feature/caveman-lite-tk3` (already checked out). All Stage 1..7 artifacts in working tree. No separate PR per binding directive.

```bash
git add -A
git commit -m "$(cat <<'EOF'
feat(delivery-team): Wave caveman-lite prose discipline (BACKLOG-102)

Activates caveman-lite prose discipline across the delivery-flow dispatch
surface. ADR-tk3-001 ratifies the six-surface contract (Phase 0 config-read,
Phase 4 Step 4 injection, 3 dispatch templates, DoD Validator template,
schema v2.8 -> v2.9) and names the cache-prefix re-freeze procedure
satisfying skill-token-economy Ruling 1.

Story 1 (W2-1 + W2-2 + W2-3 consolidated): 12/13 structural ACs verified at
Stage 6 CODE_COMPLETE. AC-13 (initiative-level deltas: >=20% prose / >=25%
DoD reduction, no 4/7 DoD pass-rate regression, opt-out verified) is
empirically pending the next post-merge dispatch by Story-1 design and arms
the BACKLOG-102 stop-rule on <15% prose-token reduction.

Cache-prefix hash flipped (whole-file SHA-256 of delivery-flow/SKILL.md):
9d4011d... -> f997ec2... per ADR-tk3-001 Element 5.
Tier-A budget preserved: SKILL.md 500/500 lines.
Files: 6 edits + 1 new (references/prose-style.md) + .delivery/artifacts/
run record for run-2026-05-05-tk3.

Refs: ADR-tk3-001, BACKLOG-102, run-2026-05-05-tk3
EOF
)"

git checkout main
git rebase feature/caveman-lite-tk3        # squash-rebase; ff inline if no divergence
git merge --ff-only feature/caveman-lite-tk3
git push origin main
git branch -d feature/caveman-lite-tk3
```

Conventional-commit format follows Wave 0/1/2 precedent: `feat(delivery-team): Wave <name> <subject> (BACKLOG-NNN)`.

## 4. Post-merge Verification

```bash
git log --oneline -3                # top line: "feat(delivery-team): Wave caveman-lite prose discipline (BACKLOG-102)"
git diff main..origin/main          # expected: empty
ls .github/workflows/skill-line-budget.yml
```

`skill-line-budget.yml` triggers on `pull_request:` only — the binding ff-push to main does NOT fire the budget gate via CI. The §2 local invocation IS the authoritative budget verification for this run. Documented, not a defect.

## 5. Rollback Procedure (per ADR-tk3-001 Element 5)

**Runtime opt-out — low-cost, preferred.** Edit `.delivery/config.yml`; set top-level key `prose_style: standard`. Entire reversal. No source revert. No hash regeneration. Pipeline restart picks up the new value at Phase 0; PROSE STYLE block omitted from every dispatch. AC-6 satisfied by construction.

**Structural rollback — high-cost, only if a downstream regression manifests:**

```bash
git revert <merge-commit-sha>
# cache-prefix-hash.txt is content-derived; the revert restores it. If it
# diverges for any reason, restore explicitly:
echo "9d4011d11e5b83321526c41ff79dd25c9186f4c659a745feb0c13f686205926f  delivery-team/skills/delivery-flow/SKILL.md" \
  > governance/cache-prefix-hash.txt
sha256sum delivery-team/skills/delivery-flow/SKILL.md   # verify match
git push origin main
```

Preference: runtime opt-out first; structural rollback only if opt-out insufficient (e.g., bug in Phase 0 config-read, schema-load regression).

## 6. Hazards / Watch Items

1. **Cache re-warm cost (one-time, accepted).** First post-merge dispatch invalidates the cache-warmup prefix slice for `delivery-flow/SKILL.md` (~2KB re-read). ADR-tk3-001 Element 5 bounds this. Informational watch only.
2. **First post-merge dispatch token-reduction outcome (live failure mode).** AC-13 measurement runs on the next pipeline. **<15% prose-token reduction trips the BACKLOG-102 stop-rule retro** and pauses Tier-2 A/B work. Orchestrator MUST capture telemetry on the first post-merge dispatch and compare to W0-1 baseline before any caveman-lite-dependent follow-on.
3. **v2.7-config auto-load surprise check.** Confirmed `.delivery/config.yml` does NOT pin `prose_style: standard` (current contents: `config_version: "2.7"` only). Migration default `caveman-lite` IS in effect on next run; Phase 0 upgrade banner surfaces it.

## 7. Go/No-Go Input (DevOps lens, summary)

```
DevOps Recommendation: GO
Rationale: pre-merge verification commands all return expected outputs;
merge strategy proven through 3 prior waves; rollback paths armed at
runtime + structural levels.
Risks: 0 BLOCKING; 1 P1 (first-post-merge token reduction below threshold
       -> stop-rule retro per BACKLOG-102).
```

Detailed input: `.delivery/artifacts/07-uat/devops/go-no-go-input.md`.

---

STATUS: DONE
ARTIFACT: .delivery/artifacts/07-uat/devops/release-plan.md
SUMMARY: Squash-rebase + ff-merge to main (no PR, Wave 0/1/2 precedent); commit "feat(delivery-team): Wave caveman-lite prose discipline (BACKLOG-102)"; rollback armed runtime + structural.
