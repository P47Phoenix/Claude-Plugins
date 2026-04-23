# Idea Brief — Opus 4.7 Plugin-Skill Migration (Execution)

**Engagement:** `run-2026-04-22-4x7e` (FEATURE)
**Upstream design:** `run-2026-04-20-o4v7` (DESIGN, terminus: transformation plan + ADRs)
**Author:** Product Owner (Gandalf speaking)
**Status:** Draft

---

## 1. Problem — One Paragraph

The runtime beneath this marketplace has already stepped into a new age: `CLAUDE.md` names Opus 4.7 as the model that reads these skills, yet the skills themselves still speak the elder tongue of 4.6. Three stale model-ID references (MID-01, MID-02, MID-03) sit in documentation and examples; the prompt-engineer pattern library still frames Pattern-01 around the prior paradigm (PAT-01); and seventeen `SKILL.md` files wear no marker of 4.7-readiness. Authors and agents reading these skills today cannot tell, at a glance, what has been verified against the current model and what has merely been inherited. That is not a broken kingdom — but it is a silent one, and silence in documentation always gets louder with time. The repo must be made to plainly speak the language of its own runtime.

## 2. Scope — One Paragraph

Execute the already-approved transformation plan as a single consolidated FEATURE engagement. Scope is not re-opened here; it is carried. The binding source is `.delivery/artifacts/04-architect/solution/transformation-plan.md` (rev 1, §6 Roadmap), comprising fourteen work items (WI-01 through WI-14) sequenced across four waves — evidence capture, spike resolution, skill-by-skill updates, and the marker/CI-guard closeout. This brief points at that plan; it does not restate it. Any item not in that table is out of scope for this engagement and belongs in the backlog.

## 3. Six Binding Architecture Decisions (ADRs)

These are accepted and frozen for the duration of this engagement. None is re-litigated mid-flight.

- **ADR-001** — Migration paradigm: annotate-in-place (the Galadriel pattern), not rewrite.
- **ADR-002** — Model-ID reference strategy: canonical IDs in a single source, documentation references it rather than hard-coding.
- **ADR-003** — Extended-thinking adoption: scope and guardrails for when skills may invoke it.
- **ADR-004** — Prompt-caching scope: which skill bodies are cache-eligible and which remain dynamic.
- **ADR-005** — Pattern library location: canonical home for the 4.7-era pattern set is `prompt-engineer/SKILL.md`.
- **ADR-006** — Readiness-marker convention: the frontmatter/marker shape that declares a skill 4.7-ready.

Full text under `.delivery/artifacts/04-architect/adrs/ADR-00[1-6]-4-7-*.md`.

## 4. Carry-Items from the DESIGN Retrospective (A1–A6 → ACs, not new work)

Four items travel forward from `.delivery/artifacts/retrospective.md` and are woven into this engagement's acceptance criteria, not added as fresh WIs:

- **MID-04** — a fourth stale model-ID site surfaced late in design; folded into WI-10's sweep scope.
- **Keystone AC unevenness** — ACs across WIs are levelled so the keystone items are not thinner than the leaves.
- **AC-03B.2 hardening** — the NDOC-02 frontmatter-contract AC is tightened so the Wave-2 blocker has a sharp exit test.
- **Label drift** — terminology between `4.7-ready` / `4.7-verified` / `opus-4-7` is reconciled to one term before WI-11 backfill.

## 5. One Deviation from Plan Defaults (User Direction)

WI-13 (NEW-BACKLOG registration) was authored assuming local-file backlog entries only. The user directed a dual-write: for each deferred item, create **both** a local `.delivery/backlog/BACKLOG-47-<topic>.md` file **and** a GitHub issue labeled `backlog-47`. Count and topic set remain as the plan specifies.

## 6. Out-of-Scope, Honoured via WI-13

The following are deliberately deferred and must ship as `backlog-47` entries (file + issue), not touched as code in this engagement:

- Task-budget wiring
- Memory-tool adoption
- SDK / prompt-caching wiring
- Cyber-safeguard integration
- Frontmatter prose-skim upgrade
- Galadriel on-ramp artifact

Scope terminus is held by logging, not by saying no.

## 7. Success — What the End Looks Like

This engagement is done when the six verification commands from the kickoff plan return their expected values: stale-ID grep returns zero; both CI guards (DX-M4 header warn, M-02 stale-ID block) are wired and green on a sample PR; all seventeen `SKILL.md` files carry the reconciled 4.7-readiness marker; six `BACKLOG-47-*.md` files exist locally; and six corresponding GitHub issues exist with the `backlog-47` label. When those six numbers come up right, the kingdom speaks its own tongue again — and we ride on.

---

*"All we have to decide is what to build with the time that is given to us. And I decide we execute the plan before us — no more, no less — and log the rest for the road ahead."*

```
STATUS: DRAFT
ARTIFACT: .delivery/artifacts/08-execute/01-idea/po/idea-brief.md
```
