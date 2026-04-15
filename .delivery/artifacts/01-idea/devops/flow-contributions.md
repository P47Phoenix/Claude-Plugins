# Flow Contributions — DevOps Lens

> *"Well, Mr. Frodo, I can't deploy the feature for you, but I can carry the
> pipeline. Someone's got to mind the hooks, the state file, and the cache —
> and that's a hobbit's job if ever there was one."* — Samwise Gamgee

**Contributor:** operations (DevOps) · **Stage:** 01-idea · **Scope:** operational/lifecycle flow docs to complement Celebrimbor's architectural set.

---

## Proposals

### 1. Hook Firing Timeline (`hook-firing-timeline.md`)
- **Audience:** plugin maintainers, hook authors, debuggers.
- **Why it matters:** The 7 hooks fire across 5 event types, and nobody has a single timeline that says "in a representative FEATURE run, here's the actual firing order." Today you grep `hooks.json` and guess.
- **Diagram:** swimlane — orchestrator vs. sub-agent vs. hooks — across SessionStart → first PreToolUse(Skill) → per-stage PreToolUse(Agent)/PostToolUse(Agent)/SubagentStop → PostToolUse(Write/Edit) on any .gd writes → Stop.
- **Complexity:** M.
- **Overlap risk:** low. Celebrimbor's "hook perimeter" is spatial; this one is temporal.

### 2. State Persistence + Atomic Write Protocol (`state-lifecycle.md`)
- **Audience:** orchestrator contributors, resume-bug hunters, SREs.
- **Why it matters:** `.delivery/state.md` is the resume contract. The atomic write (`state.tmp.md` → rename) is load-bearing but only documented inline in `SKILL.md` L552/901. Failure modes (crash mid-write, divergent config snapshot, missing artifact on resume, abort vs. complete retention) deserve one picture.
- **Diagram:** state machine (idle → in_progress → stage_running ↔ correcting → stage_complete → completed/aborted) overlaid with a file-lifecycle lane (create · tmp-write · rename · update · delete-on-complete · preserve-on-abort).
- **Complexity:** M.
- **Overlap risk:** partial with ARCHITECTURE §5 (which is a state diagram only) — this extends it with write protocol + failure modes. Coordinate so §5 links here instead of duplicating.

### 3. Installed↔Source Cache Sync (`cache-sync.md`)
- **Audience:** anyone dogfooding plugin changes (this is memory `feedback_dogfooding.md` in diagram form).
- **Why it matters:** Source-of-truth is `delivery-team/` in repo; runtime reads `~/.claude/plugins/cache/...`. Divergence silently breaks UAT — lesson learned the hard way. No doc captures the sync trigger, drift detection, or the "validate installed cache reflects source" UAT step.
- **Diagram:** two-node sync flow (repo → marketplace install → cache) with drift detectors (checksum, version tag, last-sync timestamp) and a UAT gate.
- **Complexity:** S.
- **Overlap risk:** none. Pure ops concern; architect won't cover it.

### 4. Retrospective + Memory Write Cycle (`retro-memory-cycle.md`)
- **Audience:** self-learning maintainers, Stop-hook debuggers.
- **Why it matters:** Post-pipeline protocol chains several file writes (retro artifact → chunk routing to `stages/`/`topics/`/`archive/` → `MEMORY.md` index rebuild → archive prune at 20 runs → defect review → optional PR trigger). Today this lives scattered across `memory-protocol.md`, Stop-hook prompt, and defect doc. One sequence diagram would collapse it.
- **Diagram:** sequence — orchestrator · retro-writer · chunker · index builder · pruner · defect gate, with actual file paths on each arrow.
- **Complexity:** M.
- **Overlap risk:** low. Architect may sketch memory tiers; this is the write-cycle, not the read-cycle.

### 5. Notification Channel Routing (`notification-routing.md`)
- **Audience:** config authors, integrators hooking Slack/GitHub Discussions.
- **Why it matters:** `notifications.channels` × `notifications.events` is an N×M matrix with no visual. Users don't know which event fires which channel, or that `console` is the guaranteed-on fallback.
- **Diagram:** routing matrix + flow — event source (complete/abort/escalation/checkpoint/defect-threshold) → filter → channel fan-out (console/file/slack/github-discussion) with failure-to-fallback arrows.
- **Complexity:** S.
- **Overlap risk:** none.

### 6. Config Loading + Migration Lifecycle (`config-lifecycle.md`)
- **Audience:** schema maintainers, anyone adding a v2.8 field.
- **Why it matters:** `.delivery/config.yml` discovery → version check → in-memory upgrade for missing keys → v2.6→v2.7 migration path (DEFECT-003 `project_type` removal) → 30-day staleness warning. The extension protocol lives in `config-schema.md` but the *runtime* lifecycle doesn't have a picture.
- **Diagram:** flowchart — SessionStart hook discovery → parse → version branch → migrate-or-warn → staleness check → hand-off to orchestrator; with an ADR-style "when to bump schema version" sidebar.
- **Complexity:** M.
- **Overlap risk:** minor with architect's config-as-contract framing — theirs is schema; this is runtime behaviour.

---

## Honest Overlap Summary

| Proposal | Likely architect overlap | Resolution |
|---|---|---|
| 1 Hook Timeline | low — they'll do perimeter, not timing | keep both, cross-link |
| 2 State Lifecycle | partial — ARCH §5 is shallow | extend §5, link out |
| 3 Cache Sync | none | DevOps-only |
| 4 Retro/Memory Write | low — they may do memory *read* tiers | complementary |
| 5 Notifications | none | DevOps-only |
| 6 Config Lifecycle | minor — schema vs runtime | complementary |

**Recommendation to PO:** ship all 6. If trimming, drop #5 first (smallest audience), then #6 (partially covered by `config-schema.md` extension protocol). Keep #1–#4 — they plug the most painful knowledge gaps, especially #3 which is a recurring hot lesson in memory.

---

STATUS: DONE
ARTIFACT: .delivery/artifacts/01-idea/devops/flow-contributions.md
SUMMARY: Sam here — proposed 6 ops-lens flow docs (hook timeline, state lifecycle, cache sync, retro/memory cycle, notification routing, config lifecycle). Low overlap with architect.
