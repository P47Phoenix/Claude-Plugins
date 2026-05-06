<!-- run: run-2026-05-05-tk2 | wave: 2 | predecessor: run-2026-05-04-tk1 b412a40 -->

# Idea Brief — Skill Token-Economy Wave 2

## 1. Scope

BACKLOG-103 W2-0 through W2-7 (8 WIs, 5 file-scope stories). Wave 1 merged clean as
b412a40 (GO, run-2026-05-04-tk1). Wave 2 brings delivery-flow, architect,
product-delivery, and developer into full tier compliance; all other files are Wave 3+.

## 2. In-Scope Work Items

| WI    | Description                                              | Effort | Risk     |
|-------|----------------------------------------------------------|--------|----------|
| W2-0  | Re-baseline `governance/skill-budgets.json`              | S      | Low      |
| W2-1  | Externalize shared orchestrator doctrine + ADR-tk2-001   | L      | **High** |
| W2-2  | Extract architect output contracts (×5)                  | M      | Low      |
| W2-3  | Extract developer coding-standards template (×2 refs)    | M      | Low      |
| W2-4  | Move config/commands/manifest tables from delivery-flow  | M      | Low      |
| W2-5  | product-delivery 12 patterns split                       | M      | Low      |
| W2-6  | Architect model split (Sonnet classification/Opus synthesis) | M  | Med      |
| W2-7  | Wave 1 retro backports — math correction + filename      | S      | Low      |

*BACKLOG-103 §§W2-0 – W2-7 are the authoritative spec per row.*

## 3. Out of Scope

Wave 3+: presentation/ui/operations/quality/user-feedback/godot Tier-B extractions
(BACKLOG-104+); CLAUDE.md refactor 169→≤150; BACKLOG-102; governance frontmatter;
paradigm sub-skill pattern; all other plugins.

## 4. Wave 1 Retro Carry-Forward

| # | Action                                                          | Wave 2 status         |
|---|-----------------------------------------------------------------|-----------------------|
| 1 | Backport ADR-tk1-002 + BACKLOG-101 W1-7 line target −1 → −2    | **CLOSED by W2-7**    |
| 2 | Backport BACKLOG-101 W1-3/W1-5 filename → `audit_agent_prompt.py` | **CLOSED by W2-7** |
| 3 | Author BACKLOG-103                                              | DONE                  |
| 4 | File issue: plugin-dev:skill-development invocation pattern     | Carryover post-pipeline |

## 5. Plugin-Dev Skill Routing (binding)

Per `stages/idea.md` (validated run-2026-05-03-tk0e) and `topics/claude-plugins-repo.md`
— pre-loaded to prevent Architect DoD bounce:

- **W2-1, W2-2, W2-3, W2-4, W2-5, W2-6**: create/modify SKILL.md and/or references files
  → `plugin-dev:skill-development` MUST be pre-loaded at each dispatch.
- **W2-0, W2-7**: admin JSON/doc edits only; no SKILL.md or hook code changed → no
  plugin-dev dispatch required.
- Post-completion: `plugin-dev:skill-reviewer` on all modified SKILL.md;
  `plugin-dev:plugin-validator` before PR.

## 6. Known-Debt Status

**Discovery-verified counts (wc -l 2026-05-05)** — note registry stale at delivery-flow 1089; W2-0 corrects to 999:

| File (delivery-team/skills/…)   | Actual | Budget | Delta   | Wave 2 outcome        |
|---------------------------------|--------|--------|---------|-----------------------|
| delivery-flow/SKILL.md          | 999    | 500    | −499    | **CLEARED** → ≤500    |
| architect/SKILL.md              | 673    | 300    | −373    | **CLEARED** → ≤300    |
| product-delivery/SKILL.md       | 691    | 300    | −391    | **CLEARED** → ≤300    |
| developer/SKILL.md              | 495    | 300    | −195    | **CLEARED** → ≤300    |
| presentation, ui, operations, quality, user-feedback, godot | 234–543 | 200–300 | — | **REMAINS Wave 3** |

**CLAUDE.md**: 169/150. Wave 3.

## 7. W2-1 Risk — F-08 Dispatch Fusion Regression (Opus 4.7)

**Risk (High)**: Extracting orchestrator doctrine may lose the semantic anchors that
delivery-flow Phase 3 route fusion requires. On Opus 4.7, absent anchors collapse
sub-agent role boundaries — the F-08 failure mode (session 0876a59e analogue).

**Binding anchors that MUST stay inline**: Phase 0/1/2/3 routing skeleton, Stage Routing
Matrix, One Role = One Sub-Agent invariant, Two-Channel Communication constraint.
All other doctrine (anti-patterns, per-stage detail blocks, memory self-learning detail,
Theme-Gated Reporting protocol) MAY move to `references/shared/orchestrator-doctrine.md`.

**Mitigation — all required for merge**:
1. ADR-tk2-001 (cache-prefix re-freeze) enumerates inline anchors vs extracted content;
   `governance/cache-prefix-hash.txt` MUST be updated; CI hash-check MUST pass.
2. Architect batching math simulation (Wave 1 lesson applied at Stage 4): ADR-tk2-001
   shows before (999) → −Δ → after (≤500) with explicit anchor retention list.
3. Architect dogfood-validates skeleton against synthetic multi-stage pipeline run
   (Idea + Architect + Dev dispatch minimum) BEFORE merge. Routing misfire → restore
   anchors inline; doctrine file grows to compensate — correctness beats line count.

## 8. Success Criteria (runnable)

```bash
python3 scripts/check_skill_budgets.py                                    # exit 0
wc -l delivery-team/skills/delivery-flow/SKILL.md                        # ≤ 500
wc -l delivery-team/skills/architect/SKILL.md                            # ≤ 300
wc -l delivery-team/skills/product-delivery/SKILL.md                     # ≤ 300
wc -l delivery-team/skills/developer/SKILL.md                            # ≤ 300
ls delivery-team/references/shared/orchestrator-doctrine.md
ls delivery-team/skills/architect/references/output-contracts/           # 5 files
ls delivery-team/skills/product-delivery/references/patterns/            # 12 files
ls delivery-team/skills/delivery-flow/references/{config-keys,commands,manifest}.{md,yml}
python3 scripts/check_skill_budgets.py --known-debt-report               # delivery-flow current=999
grep -c "Edit-history" .delivery/backlog/BACKLOG-101-skill-token-economy-delivery-team-wave-1.md
grep -c "Edit-history" .delivery/artifacts/04-architect/adrs/ADR-tk1-002-model-tools-rollout.md
```

Reference: BACKLOG-103 §Acceptance Criteria and §Stop-rule (defects/story ≤ 0.4).

## 9. References

- BACKLOG-103: `.delivery/backlog/BACKLOG-103-skill-token-economy-delivery-team-wave-2.md`
- Wave 1 retro: `.delivery/memory/archive/run-2026-05-04-tk1.md`
- Binding decisions: `.delivery/memory/topics/skill-token-economy.md`
- Stage 1 lesson: `.delivery/memory/stages/idea.md`
- Known-debt registry (stale; W2-0 fixes): `governance/skill-budgets.json`
- Cache-prefix hash: `governance/cache-prefix-hash.txt`
