<!-- run: run-2026-05-28-backlog-108 -->
## Architect DoD Review — Idea Stage (Round 2, re-validation)

**Artifact**: `.delivery/artifacts/01-idea/po/idea-brief.md`
**Role**: Architect DoD Validator (Celebrimbor, master craftsman of enduring systems)
**Stage**: 1 — Idea (LIGHT depth), Round 2 after PO revision
**Date**: 2026-05-28
**Initiative**: Opus 4.8 Migration (BACKLOG-108)
**Verdict**: **DONE** — all four Round-1 blockers resolved; every claim re-verified against disk-truth.

> *The boundaries are now true. The work will endure because the allowlist has finally seen every string it must judge.*

---

### Round-1 blocker closure (re-verified, not brief-trusted)

| R1 fix required | Round-2 brief | Disk truth | Closed? |
|-----------------|---------------|------------|---------|
| S1: "new guard" → **rewrite** existing, invert allowlist | S1 (L41) reads "**Rewrite** existing `stale-model-id-guard.yml`"; Scope L84 "**rewrite existing guard** … Not a new file"; Problem L27 "exists today and currently allowlists `claude-opus-4-7`" | Guard exists; header L23 says `claude-opus-4-7 (current)`; regex `[^7]` (L29) deliberately permits 4-7 — confirms it must be inverted, not created | **YES** |
| Scope additions: conftest.py (4), smoke-test-architecture.md (1), prompt-engineer:368 MODEL_ID | Scope L86-88 lists all three with exact line numbers; S2 (L42) flags `prompt-engineer/SKILL.md:368` MODEL_ID as code-literal, not stamp-only; S4 (L44) carries conftest 4 hits + arch-doc 1 hit | grep confirms all 5 live literals: `agent_registry.py:190`, `prompt-engineer/SKILL.md:368`, `conftest.py:105/117/129/151`, `smoke-test-architecture.md:115` | **YES** |
| AC2: assert count of 34, not value filter; 9 are stamp *additions* | AC2 (L71) asserts `wc -l` == **34** AND a zero-count for non-4-8 values; L49-55 names the 9 unstamped as NEW stamp creations | 34 SKILL.md total; 25 carry `model_awareness:` (7 × `opus-4-7`, 19 × `opus-4-7-frontmatter-only`); the exact 9 named files are confirmed unstamped | **YES** |
| Add risk R5 (hidden literals trip guard → pre-squash grep sweep) | R5 (L122): "Hidden 4-7 literals trip the rewritten guard at squash"; mitigation = QA-run pre-squash `grep -rn` sweep before ff-merge | Matches the AC1 gating exposure exactly | **YES** |

---

### Gate criteria results (Round 2)

**1. Technical feasibility — PASS.** Every named surface exists on disk and is editable: the guard, all 5 literal sites, the 34 SKILL.md files, smoke harness, baseline JSON, `cache-prefix-hash.txt`. No missing primitive. Achievable within stated constraints.

**2. Story decomposition S1-S7 dependency-coherent — PASS.** Spine unchanged and correct: guard rewrite (S1) → keystone prose (S2) → full sweep (S3) → code IDs (S4) → smoke harness (S5) → cache re-freeze (S6, after all SKILL.md edits per BINDING-5.3) → memory+changelog+squash (S7). Stamp-after-prose (L57) matches BINDING-2.3. No cycle, no inversion.

**3. Critical files/surfaces identified — PASS (was PARTIAL FAIL).** The guard is now correctly described as a **rewrite** of an existing file that currently allowlists 4.7 — verified against the guard's own `(current)` header and `[^7]` regex. All four live 4.7 literal sites beyond the registry are now enumerated with line numbers and confirmed on disk: `agent_registry.py:190`, `prompt-engineer/SKILL.md:368`, `conftest.py` (105/117/129/151), `smoke-test-architecture.md:115`. Nothing the rewritten guard will gate on is left out of scope.

**4. Risks real, mitigations credible — PASS.** R1 (self-referential dispatch → One-Role-One-Agent, BINDING-5.4) remains the correct top risk. R2 (doc-divergence → adversarial re-fetch, BINDING-3.2), R3 (best-effort WARN-not-FAIL, BINDING-4.2), R4 (fingerprint scope → ADR-4-8-001) all credible. **R5 is now present** and is the right control for the scope-completeness exposure: an independent QA pre-squash `grep -rn "claude-opus-4-7"` sweep before ff-merge, with only the one permitted provenance comment allowed to remain.

**5. No architectural contradiction with binding decisions — PASS (was FAIL).** The Round-1 contradiction (guard framed as "new" vs. BINDING-2.1) is resolved: the brief now describes the rewrite/inversion explicitly and matches the on-disk reality. AC1's clean-tree assertion (one permitted provenance comment in `agent_registry.py`, all 5 sites migrated) is consistent with BINDING-1.3, BINDING-2.1, and BINDING-2.4. No dual-allow window (Constraint 6, BINDING-2.1). Ship pattern (Scope L98) matches BINDING-5.1.

**6. plugin-dev skill routing acknowledged — PASS.** L59-62 and Constraint 1 (L104) state SKILL.md edits route through `plugin-dev:skill-development`, hook edits through `plugin-dev:hook-development`, non-optional, with Developer DoD evidence. S1 edits a workflow YAML (not a hook) — correctly no plugin-dev routing claimed there.

**7. Cache-prefix re-fingerprint sequencing sound — PASS.** S6 (L46) runs after S2/S3 and before S7's squash; ADR-4-8-001 owns the scope-expansion decision (R4, BINDING-5.5). Matches BINDING-5.3.

---

### Independent verification performed

```
find . -name SKILL.md -not -path "./.delivery/*" | wc -l           → 34
grep -rl "model_awareness:" --include=SKILL.md | wc -l (non-.delivery) → 25
model_awareness distribution → 7 opus-4-7, 19 opus-4-7-frontmatter-only
9 named files (4 personas + 5 research-types) → all confirmed unstamped
grep -rn "claude-opus-4-7" (*.py,*.md, non-.delivery) → 5 sites / 8 hits, all named in scope
test -f .github/workflows/stale-model-id-guard.yml → EXISTS; header allowlists "claude-opus-4-7 (current)", regex [^7] permits 4-7
```

Every load-bearing claim in the revised brief matches disk. The stamp accounting (25 updates + 9 creations = 34) is arithmetically and factually correct.

---

### Verdict

All four Round-1 required fixes are landed and independently confirmed. The dependency spine, risk framing (now including R5), plugin-dev routing, and re-fingerprint sequencing were already sound and remain so. The two blocking factual gaps (guard-is-new, AC2-value-vs-count) and the under-scoped literal sites are fully corrected. The Idea gate passes from the Architect's chair.

— Celebrimbor, Architect DoD Validator, run-2026-05-28-backlog-108. *The boundaries are true; all of them are now drawn.*
