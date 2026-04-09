# Release Plan — Paired Constraints Primitive v1.0

> "Share and enjoy, Mr. Frodo. I've got the pack, you've got the Ring." — Sam

## 1. Release Name + Version
- **Release:** Paired Constraints Primitive v1.0
- **Target:** `delivery-team` plugin **v2.17.3** (bump from 2.17.2 in `.claude-plugin/marketplace.json`)
- Plugin-internal; no cloud, no services. Source edit + cache sync + dogfood.

## 2. Change Inventory

**NEW files** (from US-1..US-9 developer logs):
- `delivery-team/skills/delivery-flow/references/constraints-schema.json` (US-1)
- `delivery-team/skills/delivery-flow/scripts/validate_constraints.py` (US-1)
- `delivery-team/skills/delivery-flow/scripts/check_dod_constraints.py` (US-8)
- `delivery-team/skills/delivery-flow/references/constraints-model-guide.md` (US-2)
- `delivery-team/skills/delivery-flow/references/templates/constraints-refine.yml` (US-3)
- `delivery-team/skills/delivery-flow/references/templates/constraints-architect.yml` (US-4)
- `delivery-team/skills/delivery-flow/references/templates/README.md` (US-4)
- `delivery-team/skills/delivery-flow/references/fixtures/constraints-valid.yml` (US-1)
- `delivery-team/skills/delivery-flow/references/fixtures/constraints-invalid-missing-entities.yml` (US-1)
- `delivery-team/skills/delivery-flow/references/fixtures/constraints-forward-compat.yml` (US-1)
- `delivery-team/skills/delivery-flow/references/fixtures/constraints-refine-sample.yml` (US-3)
- `delivery-team/skills/delivery-flow/references/fixtures/constraints-dod-sample.yml` (US-8)
- `delivery-team/skills/delivery-flow/references/fixtures/dod-artifact-clean.md` (US-8)
- `delivery-team/skills/delivery-flow/references/fixtures/dod-artifact-contaminated.md` (US-8)
- `.delivery/artifacts/02-refine/po/constraints.yml` — dogfood Exhibit A (US-9)

**MODIFIED files:**
- `delivery-team/skills/architect/references/volatility-decomposition.md` — §0 Golden Rule insert (US-5)
- `delivery-team/skills/architect/references/strategic-ddd.md` — Phase 1–4 Decomposition Hygiene sidebars (US-6)
- `delivery-team/skills/delivery-flow/references/pipeline-stages.md` — Stage 2 Refine PO constraints step (US-3) + Stage 5 Architect-in-Plan step w/ renumber (US-7)

## 3. Release Steps (reversible)
1. **Git status check** — `cd /var/home/meconnelly/Documents/GitHub/Claude-Plugins && git status` — clean, on `main`, all US PRs merged.
2. **Version bump** — edit `.claude-plugin/marketplace.json`: delivery-team `2.17.2` → `2.17.3`.
3. **Commit source** — `git add -A delivery-team/ .claude-plugin/marketplace.json .delivery/artifacts/02-refine/po/constraints.yml && git commit -m "feat(delivery-flow): paired constraints primitive v1.0 (US-1..US-9)"`.
4. **Push branch** — `git push origin main` (or PR branch if gated).
5. **Installed ↔ source sync** — identify active cache hash, rsync source → cache:
   ```
   HASH=$(ls -t ~/.claude/plugins/cache/mec-claude-agent-skills/delivery-team/ | head -1)
   rsync -a --delete \
     /var/home/meconnelly/Documents/GitHub/Claude-Plugins/delivery-team/ \
     ~/.claude/plugins/cache/mec-claude-agent-skills/delivery-team/$HASH/delivery-team/
   diff -rq /var/home/meconnelly/Documents/GitHub/Claude-Plugins/delivery-team/ \
     ~/.claude/plugins/cache/mec-claude-agent-skills/delivery-team/$HASH/delivery-team/
   ```
   Expect zero drift. Restart Claude Code session after.
6. **Smoke test** — run validator on shipped fixtures:
   ```
   python delivery-team/skills/delivery-flow/scripts/validate_constraints.py \
     delivery-team/skills/delivery-flow/references/fixtures/constraints-valid.yml
   ```
   Expect exit 0. Repeat on `constraints-forward-compat.yml` (exit 0) and `constraints-invalid-missing-entities.yml` (exit 1).
7. **Post-release monitoring** — track `.delivery/memory/stages/plan.md` entries tagged `[constraints]` and `.delivery/memory/index.md` Plan stage health across the next 10 pipeline runs. Target: Plan quality 57% → 80%.

## 4. Rollback Plan
- `git revert <release-sha>` on main (content is additive — safe).
- Re-run Step 5 rsync against reverted source; diff-verify zero drift; restart session.
- Fixtures, schema, scripts are pure-additive — no data migration.

## 5. Go/No-Go Criteria
- **GO pending QA DONE** (QA running in parallel on this release).
- All three US-1 validator fixtures exit as expected (0 / 0 / 1).
- US-8 DoD checks green on `dod-artifact-clean.md`, red on `dod-artifact-contaminated.md`.
- `diff -rq` source↔cache returns zero drift post-rsync.
- No regression in delivery-flow dogfood run at Stage 5.

## 6. Operational Observations (watch first 5–10 runs)
- **Stale cache drift** (memory hot lesson #4) — if Stage 5 guidance misses constraints, rsync was skipped.
- **False-positive forbidden-vocab hits** on PRDs discussing banned terms as concepts (US-9 saw 32 hits on its own PRD — by design, US-8 targets Stage-4 decomposition artifacts). Log to `.delivery/memory/defects/` if DoD fires on Refine-scope artifacts.
- **PyYAML fallback** unexercised in CI; watch for parse errors where PyYAML absent.
- **Architect-in-Plan waiver** (US-7) — confirm routing honors waiver on first BUG_FIX/DOCS_ONLY/DESIGN run post-release.
- **Plan stage health metric** — 10-run rolling average must trend toward 80% or raise a defect PR.

## 7. Feature Flag Note
Optional `constraints_enforcement: {off|warn|block}` key (proposed in Stage 5 deploy-plan §4) is **NOT implemented in v2.17.3**. Deferred follow-up, paired with the `config-schema.md` v2.7 → v2.8 bump originally scoped in deploy-plan US-9. Current release ships with **implicit `warn` semantics** baked into US-8 check severities (FAIL/WARN/INFO). Escape hatch for false positives: users delete or blank `constraints.yml` (NFR-4 soft-empty-stub honored). Tracked as follow-up in backlog.

---
```
STATUS: DONE
ARTIFACT: .delivery/artifacts/07-uat/devops/release-plan.md
SUMMARY: Release plan stitched, Mr. Frodo. v2.17.3 — 14 new files, 3 edits, rsync + smoke + dogfood. GO pending QA. Flag deferred. I'll carry it.
```
