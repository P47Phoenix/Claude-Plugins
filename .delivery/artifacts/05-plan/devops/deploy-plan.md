# Deploy Plan — Constraints Model Feature

> "I can't deploy the feature for you, Mr. Frodo, but I can carry the pipeline." — Sam

Plugin-internal feature. No cloud, no services. Deploy = source edit + cache sync + dogfood.

## 1. Deploy Target Surface
**New files** (source: `delivery-team/references/`):
- `constraints-model-guide.md`, `templates/constraints.yml.template`, `templates/constraint-adr.md.template`
- `delivery-team/schemas/constraints.schema.json` (US-1)
- `delivery-team/scripts/validate_constraints.py` (stdlib only, PyYAML fallback)

**Edited files**:
- `delivery-team/references/volatility-decomposition.md` (§0 preface)
- `delivery-team/references/strategic-ddd.md` (sidebar)
- `delivery-team/references/pipeline-stages.md` (Stage 5 hook)
- `delivery-team/SKILL.md` (constraints reference)
- `delivery-team/references/config-schema.md` (v2.7 → v2.8 bump, optional `constraints_enforcement`)

## 2. Installed ↔ Source Sync Checklist
Source of truth: `/var/home/meconnelly/Documents/GitHub/Claude-Plugins/delivery-team/`
Cache root: `~/.claude/plugins/cache/mec-claude-agent-skills/delivery-team/<hash>/delivery-team/`

1. `git status` clean on main, all US PRs merged
2. Active cache hash: `ls -t ~/.claude/plugins/cache/mec-claude-agent-skills/delivery-team/ | head -1`
3. `rsync -a --delete /var/home/meconnelly/Documents/GitHub/Claude-Plugins/delivery-team/ ~/.claude/plugins/cache/mec-claude-agent-skills/delivery-team/<hash>/delivery-team/`
4. Diff-verify: `diff -rq` source vs cache — expect zero drift
5. Restart Claude Code session (cache read at session start)

## 3. Release Steps (reversible)
1. **Merge order**: US-1 (schema) → US-2/3 (templates/guide) → US-4..7 (ref edits) → US-8 (DoD check) → US-9 (config-schema bump). Each its own PR, squash-merge.
2. **Validator smoke**: `python delivery-team/scripts/validate_constraints.py delivery-team/references/templates/constraints.yml.template` — exit 0.
3. **Version bump**: `.claude-plugin/marketplace.json` delivery-team → 2.18.0. Commit `chore: bump delivery-team to 2.18.0 (constraints model)`.
4. **Cache sync**: run §2 steps 2–5.
5. **Post-deploy verify**: dogfood `delivery-team:delivery-flow` on a trivial FEATURE run; confirm Stage 5 surfaces constraints guidance and DoD check fires.

## 4. Rollback Plan
- **Git revert** squash commits in reverse order. Content is pure-additive — revert is safe.
- **Feature flag** (escape hatch): optional `constraints_enforcement: off|warn|block` (default `warn`). NFR-4 honored — key is **optional**, v2.7 configs work unchanged. False-positive DoD hits → users set `off` without revert. `block` opt-in only.
- **Cache rollback**: revert source, re-run rsync, restart session.

## 5. Observability
No external telemetry. Evidence in-repo:
- `.delivery/memory/stages/plan.md` — lesson entries tagged `[constraints]`
- `.delivery/memory/index.md` — stage health stats (Plan quality %)
- `.delivery/memory/defects/` — false-positive DoD hits → self-improvement PRs
- Metric target: Plan stage 57% → 80% across 10 post-deploy runs before declaring success.

## 6. Known Operational Risks
- **Stale cache** (memory hot lesson #4): mitigated by mandatory §2 rsync + diff-verify. Skip it and source edits are invisible.
- **Python deps**: validator stdlib-only; PyYAML fallback documented in US-1. No pip install.
- **Legacy config**: v2.7 untouched. Missing `constraints_enforcement` → defaults `warn`. ADR-001 soft-empty-stub honored.

## 7. Effort Estimate
**2 points** (~2–3 hrs): rsync + diff + version bump + smoke + dogfood kickoff. Pure content + one validator. Sam-tier reliable.

---
```
STATUS: DONE
ARTIFACT: .delivery/artifacts/05-plan/devops/deploy-plan.md
SUMMARY: Deploy plan ready, Mr. Frodo. Rsync source to cache, diff-verify, smoke the validator, dogfood a run. Optional constraints_enforcement flag for safe rollback. I'll carry it.
```
