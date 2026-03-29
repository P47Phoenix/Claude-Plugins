# Persona Validation: PRD v2.0 — Deterministic Rules Engine Integration

**Date**: 2026-03-28
**Artifact**: Simulated user interview round 2 (concept validation against concrete PRD)
**Interviewer**: User Feedback Agent
**Personas**: 5 (same panel as round 1)

---

## 1. Sarah — Solo Developer

**Profile**: Freelance full-stack dev. Values speed/simplicity. Round 1 priority: 3/5.

### Q1: Reaction to 4-layer system

"Four layers sounds like overkill for someone like me, but honestly? The fact that I can just set `rules.preset: solo` and ignore the rest is exactly what I need. I don't care about layers 1, 3, or 4 — I just want one setting that makes the pipeline predictable and fast. The layered system doesn't hurt me as long as I never have to think about it."

### Q2: Preset fit

"Solo preset, obviously. The spec says: light on everything except Development and UAT, 1 validator per gate, escalation at 2 iterations. That maps directly to how I work. I was worried solo would mean 'stripped down to useless' but it actually matches my workflow — I still get gates, they're just faster. My one concern: does 'light' on Design mean I still get useful feedback, or is it just a rubber stamp?"

### Q3: Hybrid format

"I do not care about JSON internally. I write YAML, YAML is what I see. As long as I never have to touch a JSON file, this is fine. The PRD is clear that I won't — good."

### Q4: Wizard experience

"Three new questions is fine. The conditional display on W-12 is smart — if I pick solo, don't make me configure rules I'll never use. The auto-detection from Q3 is a nice touch. My concern from round 1 was configuration complexity, and the wizard addresses it by hiding what I don't need."

### Q5: Concern resolution

*Round 1 top concern: Unpredictable pipeline duration killing her ability to plan.*

"The PRD addresses this directly. Deterministic routing means I can predict exactly which stages run at what depth for a given project type. The solo preset with FEATURE routing gives me: Idea=light, Refine=light, Design=light, Architect=light, Plan=light, Development=full, UAT=light. That's predictable. I can estimate time now. The Routing Decision Specification (FR-18) is the key — once I see the routing table, I'll know exactly what to expect. **Concern: mostly resolved.** I'd want to see the actual routing table before I'm fully satisfied."

### Q6: Updated priority

**4/5** (up from 3/5). "The solo preset and deterministic routing turn this from 'nice but maybe too heavy' into 'I'd actually use this for everything.' Still not 5/5 because my workflow works without it — but I'd adopt it."

### Q7: Missing anything?

"Two things. First: a dry-run mode where I can see what the rules engine *would* do before committing to a full pipeline run. The PRD mentions `--compare` for migration but not a general preview. Second: I'd love a one-liner status like 'solo preset, estimated 5 stages light + 2 full' at the start of every run so I know what I'm getting into."

---

## 2. Marcus — Engineering Team Lead

**Profile**: 6-person team at SaaS company. Round 1 priority: 5/5.

### Q1: Reaction to 4-layer system

"This is exactly the model I would design. Layer 1 gives me a sane baseline I don't have to maintain. Layer 2 presets let me onboard new team members fast — 'use standard.' Layer 3 per-repo config is where my team lives — we have different quality bars for our core API vs. internal tools. Layer 4 per-run override is the escape valve I need for urgent hotfixes. The merge semantics (last-writer-wins, shallow-merge for maps) are simple and predictable. No complaints."

### Q2: Preset fit

"Standard for most repos. Strict for our payment processing service. The ability to mix presets with per-repo overrides (e.g., standard preset + `rules.pass_threshold.development: 95` for the API repo) is the exact flexibility I need. I would actually use all three presets across different repos."

### Q3: Hybrid format

"I actively appreciate JSON internally. YAML's implicit typing has bitten us before — `3.10` becoming `3.1` is a real bug we've hit. JSON as the evaluation format eliminates a class of subtle config bugs. As long as the YAML surface is clean and well-documented in config-schema v2.4, the internal format is a good engineering decision."

### Q4: Wizard experience

"Three questions is right. I'd add one nuance: when I'm onboarding a new team member, I want the wizard to show them what the team's standard config looks like, not just the generic options. But that's a 'nice to have' — the current wizard is sufficient."

### Q5: Concern resolution

*Round 1 top concern: Two developers with similar-scoped changes getting different gate results, making it impossible to mandate pipeline usage.*

"The PRD addresses this head-on. G1 guarantees identical structured inputs produce identical routing. FR-03 encodes routing as explicit rules, not AI interpretation. The Determinism Boundary (Section 5) is honest about what is and isn't deterministic — I respect that. DoD gates are hybrid (AI-derived validator outputs, deterministic aggregation), which means two devs will get the same *aggregation* of their validator results, even if the validators themselves give slightly different feedback. That's the right tradeoff — I can't expect AI code reviews to be identical, but I can expect the pass/fail *decision* to be consistent. **Concern: fully resolved.**"

### Q6: Updated priority

**5/5** (unchanged). "This was already my highest priority. The PRD confirms it's the right approach. The audit trail (FR-06) is a bonus — I can show my VP exactly why a gate passed or failed."

### Q7: Missing anything?

"Two things. First: a team-level config inheritance model. I have 6 repos and I want to set a team baseline, then per-repo overrides. Right now I'd have to duplicate config across repos. I know cross-pipeline sharing is out of scope (Section 9, item 3), but at least acknowledge it as a fast-follow. Second: rule change notifications — when a plugin default (Layer 1) changes in an update, I want to know what changed and whether it affects my Layer 3 overrides."

---

## 3. Priya — Enterprise Architect

**Profile**: Regulated financial services. SOC2/ISO compliance. Round 1 priority: 5/5.

### Q1: Reaction to 4-layer system

"The 4-layer model is architecturally sound for enterprise use. Layer 1 (immutable plugin defaults) provides a defensible baseline. Layer 2 (presets) maps to our compliance profiles. Layer 3 (per-repo) maps to our project-specific risk controls. Layer 4 is a concern — natural language overrides in a regulated environment are a non-starter. The PRD addresses this: in strict mode, Layer 4 is disabled. That's the correct decision. I would mandate strict mode for all our repos."

### Q2: Preset fit

"Strict, without question. The strict preset features match our requirements: all stages full, security validator on every gate, warnings promoted to blocking, no AI fallback, full audit trail with determinism tagging. I would additionally need Layer 3 overrides to add our own compliance-specific validators (e.g., data classification check, PII scan gate)."

### Q3: Hybrid format

"The hybrid format is a compliance advantage. JSON internally means the evaluation logic is type-safe and unambiguous — auditors can inspect the exact rule that was evaluated. YAML on the surface means my teams don't need to learn a new config language. The translation layer (FR-10) detecting type coercion and logging warnings is important — we'd want those warnings promoted to errors in strict mode."

### Q4: Wizard experience

"For enterprise onboarding, three questions is too few. But that's acceptable because we would never use the wizard for production setup — we'd template our `.delivery/config.yml` from a centralized compliance baseline and distribute it. The wizard is fine for developer experimentation."

### Q5: Concern resolution

*Round 1 top concern: Non-determinism in flow control is a non-starter for regulated environments; AI-interpreted gates cannot satisfy audit requirements.*

"The PRD addresses my core concern comprehensively. The Determinism Boundary (Section 5) is the most important section — it explicitly classifies every decision point and is honest about hybrid decisions. The strict mode requirement for user-declared project type (eliminating hybrid routing) and the 80% structural DoD check weighting are exactly right. The audit trail (FR-06) with determinism category tagging means I can show an auditor: 'These decisions were category (a) fully deterministic, these were category (b) deterministic aggregation of AI inputs, and the AI inputs are logged separately.' That's auditable. **Concern: fully resolved.** This is the first time I'd consider this tool viable for regulated environments."

### Q6: Updated priority

**5/5** (unchanged). "Still binary. Without this, the tool is not viable. With this, it becomes a candidate for our tooling evaluation."

### Q7: Missing anything?

"Three items. First: the audit log format needs a schema definition (JSON Schema) so we can validate log entries programmatically. The PRD describes the fields but doesn't provide a formal schema. Second: log retention and rotation policy — `.delivery/audit/` will grow. We need a documented retention strategy. Third: the YAML type coercion warnings (US-13 AC-4) must be errors in strict mode, not just warnings. A coerced value in a gate rule is a compliance incident."

---

## 4. Jake — Game Developer

**Profile**: Indie Godot dev. Cares about iteration speed. Round 1 priority: 3/5.

### Q1: Reaction to 4-layer system

"Honestly? I glazed over at '4-layer resolution system.' I don't think in layers — I think in 'make this fast' and 'make this thorough.' But when I read the actual presets, the solo profile is basically what I want: light on everything, full on Dev and UAT. So the layers exist but I'd only ever interact with the top one (preset selection). That's fine."

### Q2: Preset fit

"Solo preset + GAME_DEV project type. The PRD specifically addresses my use case (US-06 AC-4): physics/animation parameter changes get Design=light (visual/gameplay impact only) and Architect=light (performance validation only). That's the fast path I asked for. My concern: the PRD says 'no stages are executed at depth less than light.' I need to validate that 'light' for game iteration work actually feels light — like 2-3 minutes, not 15. The PRD doesn't give me time estimates."

### Q3: Hybrid format

"Don't care. I write YAML, it works, that's all I need to know."

### Q4: Wizard experience

"Three questions is fine. The auto-detection from Q3 ('minimal' maps to solo) means I'd barely notice the new questions. W-12 being conditional and hidden for solo users is correct — don't show me stuff I don't need."

### Q5: Concern resolution

*Round 1 top concern: Pipeline classified physics value tweaks as FEATURE and routed through full architecture — game dev iteration doesn't fit standard software buckets.*

"Partially resolved. The GAME_DEV project type with explicit routing rules (FR-03) means physics tweaks won't get misclassified as FEATURE anymore. The routing table will have a specific GAME_DEV row. But there's a gap: the PRD doesn't define what GAME_DEV routing actually looks like for all 7 stages x 3 risk tolerances. That's deferred to the Routing Decision Specification (FR-18). I need to see that spec before I'm confident. Also, the PRD says game-dev is not a separate preset (Section 9, item 8) — it's handled by project type + solo preset. I hope the combination is enough. **Concern: partially resolved.** Needs the routing spec to be fully resolved."

### Q6: Updated priority

**4/5** (up from 3/5). "The explicit GAME_DEV routing type and solo preset combination moved this from 'maybe useful' to 'I'd try it.' If the routing spec gives me genuinely fast paths for iteration work, this becomes a 5. But I need to see the spec first."

### Q7: Missing anything?

"One big thing: an 'iteration mode' toggle. Not a full preset — more like a per-run flag that says 'I'm doing game-feel tuning, make everything as light as possible.' The PRD has Layer 4 (per-run overrides) but it's natural language parsing, which feels unreliable. I'd want a concrete flag like `--iteration` that deterministically applies the lightest possible routing. Also: performance. The PRD says sub-500ms per decision point (NFR-01). For tight iteration loops where I might trigger 10+ decision points, that's up to 5 seconds of overhead. That's noticeable. Sub-200ms routing (mentioned in the risks section) should be the target, not sub-500ms."

---

## 5. Chen — DevOps Engineer

**Profile**: Platform engineer. Wants CI/CD integration. Round 1 priority: 5/5.

### Q1: Reaction to 4-layer system

"The 4-layer model maps cleanly to infrastructure patterns I already use. Layer 1 = base image defaults. Layer 2 = environment profiles (dev/staging/prod). Layer 3 = per-service overrides. Layer 4 = runtime flags. The merge semantics (scalars replace, lists replace with opt-in extend, maps shallow-merge) are simple and predictable. I can reason about what the final resolved config will be, which is essential for CI/CD. The `_merge: extend` opt-in for lists is a nice touch — prevents accidental list replacement."

### Q2: Preset fit

"Standard for most services. Strict for anything touching production data. I'd use Layer 3 heavily to customize per-service. For CI/CD, I'd want to lock Layer 4 (disable per-run overrides) so that pipeline behavior is 100% determined by committed config. The PRD supports this via strict mode disabling Layer 4 — good."

### Q3: Hybrid format

"I actively prefer JSON internally. JSON is machine-parseable, unambiguous, and every CI/CD tool speaks it. The audit logs being JSON Lines (FR-06) means I can pipe them into any log aggregation system (ELK, Datadog, Splunk) without transformation. YAML on the surface is fine for humans. This is the right architectural split."

### Q4: Wizard experience

"For CI/CD integration, the wizard is irrelevant — I'd generate configs programmatically. But for developer onboarding, 3 questions is appropriate. The auto-detection from Q3 reduces friction. No complaints."

### Q5: Concern resolution

*Round 1 top concern: Non-determinism violates the fundamental CI/CD contract (same commit + same environment = same result).*

"The PRD addresses this directly and thoroughly. G1 guarantees deterministic routing for identical structured inputs. NFR-02 requires byte-identical JSON outputs. The Determinism Boundary (Section 5) is the best part of the PRD — it's honest about what's deterministic and what's not. For CI/CD, I'd use strict mode (user-declared project type, no Layer 4, no AI fallback) to get full category (a) determinism on routing. The evaluation script (FR-11) with JSON stdin/stdout and exit codes (0/1/2) is exactly the interface I need for CI/CD integration. **Concern: fully resolved.** This is the foundation I need to build CI/CD integration on top of."

### Q6: Updated priority

**5/5** (unchanged). "Still the prerequisite for everything I want to build. The PRD delivers the deterministic evaluation foundation. CI/CD integration (out of scope, Section 9 item 6) is the obvious fast-follow, and the PRD explicitly enables it."

### Q7: Missing anything?

"Three things. First: a `--dry-run` mode for the evaluation script that outputs what decisions *would* be made without executing the pipeline. Essential for CI/CD validation (`python evaluate_rules.py --dry-run --context ...` in a pre-merge check). Second: a machine-readable rule manifest that I can export and version-lock. If Layer 1 defaults change in a plugin update, I want my CI/CD pipeline to detect the change and alert. Third: the evaluation script should support `--format` flag for output (json, jsonl, summary) so I can adapt output to different CI/CD contexts."

---

## Synthesis

### Priority Consensus

| Persona | Round 1 | Round 2 | Delta | Rationale |
|---------|---------|---------|-------|-----------|
| Sarah (Solo Dev) | 3/5 | 4/5 | +1 | Solo preset and deterministic routing converted skepticism to adoption intent |
| Marcus (Team Lead) | 5/5 | 5/5 | 0 | Already highest priority; PRD confirmed the right approach |
| Priya (Enterprise) | 5/5 | 5/5 | 0 | Binary requirement unchanged; PRD met the bar for viability |
| Jake (Game Dev) | 3/5 | 4/5 | +1 | GAME_DEV project type + solo preset addressed core concern; routing spec needed for full confidence |
| Chen (DevOps) | 5/5 | 5/5 | 0 | Deterministic evaluation foundation is exactly what CI/CD integration requires |

**Updated average: 4.6/5** (up from 4.4/5 in round 1)

### Concern Resolution Status

| Persona | Round 1 Top Concern | Resolution Status | Notes |
|---------|-------------------|-------------------|-------|
| Sarah | Unpredictable pipeline duration | **Mostly resolved** | Solo preset + deterministic routing. Needs to see Routing Decision Spec for full confidence. |
| Marcus | Different gate results for similar-scoped changes | **Fully resolved** | Deterministic aggregation of validator outputs. Honest about hybrid boundary. |
| Priya | Non-deterministic gates fail audit requirements | **Fully resolved** | Strict mode + determinism category tagging + category (a)/(b) separation in audit trail. |
| Jake | Game iteration misclassified as FEATURE | **Partially resolved** | GAME_DEV project type exists; actual routing table deferred to FR-18 spec. |
| Chen | Non-determinism violates CI/CD contract | **Fully resolved** | Byte-identical outputs, strict mode, JSON interface with exit codes. |

### Feature Gaps Identified

| Gap | Raised By | Severity | PRD Coverage |
|-----|-----------|----------|-------------|
| **Dry-run / preview mode** | Sarah, Chen | High | `--compare` mentioned for migration only; no general dry-run mode. Should be added to FR-11. |
| **Iteration mode toggle** (deterministic `--iteration` flag) | Jake | Medium | Layer 4 is natural-language only. A concrete `--iteration` flag would be more reliable for game devs. |
| **Audit log JSON Schema definition** | Priya | Medium | PRD describes fields but no formal schema. Add to FR-06 deliverables. |
| **YAML coercion warnings promoted to errors in strict mode** | Priya | Medium | PRD warns only (US-13 AC-4). Strict mode should escalate to error. Add to FR-10/FR-14. |
| **Team-level config inheritance** (cross-repo baseline) | Marcus | Low (out of scope acknowledged) | Section 9 item 3 defers this. Marcus accepts deferral but wants it as fast-follow. |
| **Rule change detection on plugin update** | Marcus, Chen | Medium | No mechanism to diff Layer 1 changes between plugin versions. Should be a fast-follow. |
| **Run-start routing summary** | Sarah | Low | No explicit "here's what will happen" summary at pipeline start. Nice UX improvement. |
| **Log retention / rotation policy** | Priya | Low | Not addressed. Add to NFR-03 or as operational guidance. |
| **Performance target: sub-200ms for routing** | Jake | Medium | NFR-01 says sub-500ms. Routing-specific sub-200ms target mentioned only in risks section. Should be promoted to NFR. |
| **Output format flag for evaluation script** | Chen | Low | FR-11 outputs JSON only. `--format` flag is a minor enhancement. |

### Segment Enthusiasm Ranking

1. **Marcus (Team Lead)** — 5/5. Most enthusiastic. This solves his single biggest blocker to mandating pipeline usage. Audit trail is a bonus for leadership reporting.
2. **Chen (DevOps)** — 5/5. Equally enthusiastic. The deterministic evaluation foundation is the prerequisite for all CI/CD integration work he wants to build.
3. **Priya (Enterprise)** — 5/5. Equally enthusiastic, but with the caveat that strict mode must be bulletproof. First time she'd consider the tool viable for regulated environments.
4. **Sarah (Solo Dev)** — 4/5. Converted from skeptic to adopter. Solo preset addressed her core concern. Dry-run mode would push her to 5/5.
5. **Jake (Game Dev)** — 4/5. Cautiously optimistic. GAME_DEV routing type is the right idea, but needs to see the Routing Decision Spec to confirm fast paths are genuinely fast. Performance target (sub-200ms routing) is important to him.

### Key Takeaways

1. **PRD v2.0 validates well across all segments.** Average priority increased from 4.4 to 4.6. No persona decreased priority. Both previously skeptical personas (Sarah, Jake) increased by 1 point.

2. **The Determinism Boundary (Section 5) is the PRD's strongest section.** Marcus, Priya, and Chen all called it out as honest, well-reasoned, and confidence-building. The explicit classification of decision points into categories (a)/(b)/(c) is what convinced Priya the tool could be viable for regulated environments.

3. **The highest-severity gap is dry-run mode.** Both Sarah (preview before committing) and Chen (CI/CD validation) independently requested it. This should be added to FR-11 as a `--dry-run` flag before Phase 1 implementation.

4. **The Routing Decision Specification (FR-18) is the critical next artifact.** Sarah and Jake both said their confidence depends on seeing the actual routing table. FR-18 is correctly positioned as a Phase 0 deliverable — it must ship before routing rules are implemented.

5. **Strict mode needs three hardening items from Priya's feedback**: (a) YAML coercion warnings promoted to errors, (b) audit log JSON Schema for programmatic validation, (c) log retention policy. These are low-effort additions that would close the enterprise gap completely.
