## Idea Brief — SPIKE: Cross-Skill Shared References

**Project Type**: SPIKE
**Date**: 2026-04-01
**Source Issue**: #47 — Cross-skill shared references mechanism for delivery-team
**Pipeline Routing**: SPIKE (Idea → Refine-light → Design-skip → Architect-light → Plan-light → Dev → UAT-light)

---

### 1. Spike Question

**What is the simplest viable mechanism for sharing reference files across delivery-team skills, and does it work in practice with at least two skills?**

Sub-questions:
- Which reference files are genuine sharing candidates vs. skill-specific?
- Do any of the four proposed approaches fail on cross-platform, context loading, or plugin architecture constraints?
- Is the existing ad-hoc pattern (godot SKILL.md hardcodes a path to developer/clean-code.md) sufficient, or does it need to be formalized?

---

### 2. Background

The delivery-team plugin currently contains 11 skills with 107+ reference files (~25,000 lines). Each skill loads references from its own `references/` directory. There is no formal mechanism for sharing reference content across skills.

**Why this matters now**:

1. **Duplication is already happening**. The godot skill reads `developer/references/clean-code.md` via a hardcoded cross-skill path in its SKILL.md — a working but undocumented pattern. If a second skill (e.g., quality) needs the same file, it would need to discover and replicate this ad-hoc convention.

2. **Maintenance cost scales with skill count**. We have 11 skills today. When content that applies to multiple skills (security patterns, clean code standards, defect prevention checklists) must be updated, there is no single source of truth unless we formalize sharing.

3. **New skills cannot reuse existing material**. A new skill author must either duplicate content or discover the hardcoded cross-reference pattern from godot's SKILL.md.

**Current state evidence** (from repository scan):
- `developer/references/clean-code.md` (104 lines) — already cross-referenced by godot SKILL.md
- `developer/references/clean-code-review-checklist.md` — used by developer, potentially useful for quality
- `architect/references/security-patterns.md` and `quality/references/security-scanning.md` — related but distinct content on security
- `architect/references/quality-attributes.md` and `quality/references/quality-metrics.md` — overlapping quality domain
- `delivery-flow/references/quality-gates.md` — referenced from delivery-flow SKILL.md but conceptually consumed by quality role during DoD validation
- `godot/references/defect-prevention.md` (111 lines) — potentially useful for developer skill on game projects

---

### 3. Approaches to Evaluate

The spike should evaluate these approaches in priority order (simplest first):

| # | Approach | Effort | Description |
|---|----------|--------|-------------|
| 1 | **Shared directory** (`delivery-team/shared/`) | Low | Create a `shared/` directory at the plugin root. Skills reference files via relative path (`../../shared/clean-code.md`). No architecture change needed. |
| 2 | **Formalized cross-skill paths** (current godot pattern) | Low | Document a convention: any SKILL.md may reference `delivery-team/skills/<other-skill>/references/<file>.md`. No new directory. Codify the existing ad-hoc pattern. |
| 3 | **Explicit paths in sub-agent prompts** | Medium | The delivery-flow orchestrator passes shared reference paths when spawning sub-agents. Centralized control, but requires orchestrator changes. |
| 4 | **Reference registry in marketplace.json** | Medium | Declare shared references at the plugin level in `marketplace.json`. Skills declare which shared refs they consume. Requires tooling to resolve. |
| 5 | **Symlinks** | Low | Symlink shared files into each skill's `references/` directory. Known fragile on Windows and potentially confusing for Claude's file resolution. |

**Spike should also answer**: Is there a reason to NOT share? Some "duplication" may actually be intentional divergence — security-patterns.md (architect) and security-scanning.md (quality) serve different roles. The spike must distinguish true duplicates from related-but-distinct content.

---

### 4. Success Criteria

The spike is DONE when:

- [ ] **Inventory complete**: A list of reference files that are candidates for sharing, with justification for each (true duplicate, partial overlap, or intentionally distinct)
- [ ] **At least 2 approaches prototyped**: Working proof that two approaches can load a shared reference from two different skills
- [ ] **Cross-platform validated**: The chosen approach works on Linux, macOS, and Windows (or documents known limitations)
- [ ] **Decision recorded**: An ADR-style decision stating which approach is recommended (or "none viable") with evidence
- [ ] **Dogfooding signal**: The prototype was tested by actually invoking two skills that load the shared reference, not just by reading the file paths
- [ ] **No regressions**: Existing skill loading (especially godot -> clean-code.md) still works after the prototype

---

### 5. Time Box

**1 sprint (single pipeline run)**. This is an architecture exploration, not a committed feature. If the simplest approach (shared directory or formalized paths) works, the spike should stop there. Do not gold-plate.

Deliverables:
- Decision document (ADR format)
- Prototype diff (can be throwaway)
- Sharing candidate inventory
- Recommendation for follow-up feature work (if any)

---

### 6. Constraints

- **No breaking changes**: Existing skill loading must continue to work unchanged. This is additive only.
- **Plugin structure compliance**: Any new directory or convention must be compatible with the plugin structure documented in CLAUDE.md and validated by plugin-dev:plugin-validator.
- **No new dependencies**: No build tools, no package managers, no scripts required to resolve references. Claude must be able to `Read` the file directly from a path.
- **Markdown/YAML only**: The spike produces documentation and prototype config changes. No source code required.
- **Config schema unchanged**: No new keys in `.delivery/config.yml` for this spike. If the recommended approach needs config support, that goes into the follow-up feature brief.
- **Claude's file resolution**: The mechanism must work within how Claude Code resolves file paths — relative paths from the SKILL.md's location, absolute paths from the repo root, or paths specified in sub-agent prompts. The spike must test which of these actually work.

---

*Not all those who wander through reference directories are lost — but some of them are reading the same document in three different places. This spike shall determine whether they need a shared library or merely a better map.*

```
STATUS: DONE
ARTIFACT: .delivery/artifacts/01-idea/po/idea-brief.md
SUMMARY: SPIKE idea brief for #47 — cross-skill shared references. 5 approaches to evaluate, 6 success criteria, 1-sprint timebox.
```
