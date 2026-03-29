# User Interviews: Rules Engine Integration for Delivery-Flow Pipeline

**Date**: 2026-03-28
**Method**: Simulated persona-based interviews (Jobs-to-be-Done framework)
**Feature**: Deterministic business rules engine for pipeline routing and gating
**Personas**: 5 (Solo Developer, Engineering Team Lead, Enterprise Architect, Game Developer, DevOps Engineer)

---

## Persona 1: Sarah (Solo Developer)

**Profile**: Freelance full-stack developer. Uses Claude Code daily for personal projects. Values speed and simplicity. Has tried delivery-flow but found it heavyweight for solo work.

### Q1 — Context
> "Tell me about the last time you ran a delivery pipeline and something unexpected happened with the routing or gating."

**Sarah**: I was building a small SaaS side project -- a bookmark manager. I kicked off the delivery pipeline for what I thought was a straightforward FEATURE type. The pipeline routed me through a full architecture stage with security review, which is overkill for adding a tag filtering feature to my personal project. Next time I ran it with almost identical inputs, it went lighter on architecture but then got really thorough in the design stage instead. I just wanted to write code. The inconsistency meant I never knew how long the pipeline would take, which killed my ability to plan my evening coding sessions.

### Q2 — Pain
> "What's the most frustrating thing about how pipeline decisions are made today?"

**Sarah**: Unpredictability. When I'm solo, I need to know: "If I start this, will it take 20 minutes or 2 hours?" Right now I genuinely cannot estimate. The AI sometimes decides my tiny feature needs a full security review and sometimes it skips it. I cannot plan around that. I've started just going straight to the developer skill and skipping the pipeline entirely for small stuff, which I know defeats the purpose.

### Q3 — Workaround
> "How do you currently handle inconsistent pipeline behavior?"

**Sarah**: Honestly? I bypass the pipeline for anything I think is small. I only use it for bigger features where I actually want the structure. For the stuff I do run through, I just accept whatever it decides and push through. I've also started putting very explicit instructions in my prompts like "this is a small change, keep stages light" but it does not always listen.

### Q4 — Value
> "If gate decisions were 100% deterministic and configurable, what would that change for you?"

**Sarah**: That would be huge for me. I could set up a "solo light" config that says: features under X complexity skip architecture, design is always light, go straight to dev with just a quick quality check. If I knew those rules were always followed, I'd actually use the pipeline for everything instead of bypassing it. Predictability is worth more to me than AI judgment on routing.

### Q5 — Trade-off
> "What would you give up for more determinism? Would you accept less flexibility in how gates are evaluated?"

**Sarah**: Absolutely. I would give up the AI's ability to "intelligently" route things because its intelligence has been inconsistent for me. I would rather have dumb-but-predictable rules that I configured myself. As long as I can override them when I want to -- like forcing a full pipeline for a bigger feature -- I am completely fine with less flexibility day-to-day.

### Q6 — Priority
> "On a scale of 1-5, how important is this compared to other improvements you'd want?"

**Sarah**: **4 out of 5**. The only thing I'd rank higher is making the pipeline faster overall. But deterministic routing would indirectly help with speed because I could configure lighter paths and know they'd stick.

### Q7 — Concern
> "What worries you about adding a rules engine to the pipeline?"

**Sarah**: Configuration complexity. If I have to write a 200-line YAML file to set up rules, I'll never do it. It needs to have sane defaults that work for solo devs out of the box, with optional customization. Also, if the rules engine makes the pipeline slower because it's doing extra evaluation steps, that would be a dealbreaker.

### Q8 — Magic wand
> "If you could change one thing about how the pipeline makes decisions, what would it be?"

**Sarah**: Let me set a project profile -- "solo", "small team", "enterprise" -- and have the pipeline automatically adjust all its gate thresholds and routing decisions based on that. One setting, predictable behavior. That's the dream.

---

## Persona 2: Marcus (Engineering Team Lead)

**Profile**: Leads a 6-person team at a mid-size SaaS company. Uses delivery-flow for feature work. Frustrated by inconsistent gate results across runs. Needs to justify tooling decisions to VP of Engineering.

### Q1 — Context
> "Tell me about the last time you ran a delivery pipeline and something unexpected happened with the routing or gating."

**Marcus**: Two weeks ago, two of my developers were working on similar-scoped features -- both adding new API endpoints with database migrations. Dev A's pipeline flagged a gate failure at the architecture stage saying the database schema needed review. Dev B's pipeline passed the same stage with a nearly identical change. When I asked Dev B to re-run to double-check, it failed this time. Same inputs, different result. I had to explain to my VP why our "quality pipeline" was giving different answers to the same question. That was not a fun conversation.

### Q2 — Pain
> "What's the most frustrating thing about how pipeline decisions are made today?"

**Marcus**: Lack of reproducibility. I cannot tell my team "here are the standards, and the pipeline enforces them" because the pipeline's interpretation of those standards changes between runs. It undermines trust in the tool. My senior devs have started treating gate results as suggestions rather than requirements, which is exactly the opposite of what I want. I need gates that are respected, and for that they need to be consistent.

### Q3 — Workaround
> "How do you currently handle inconsistent pipeline behavior?"

**Marcus**: I've created an internal checklist document that parallels what the pipeline is supposed to check. When a gate passes, the developer still has to go through the manual checklist. When a gate fails, they review the checklist to see if it's a "real" failure or the AI being overzealous. So essentially we're running two quality systems in parallel, which is absurd.

### Q4 — Value
> "If gate decisions were 100% deterministic and configurable, what would that change for you?"

**Marcus**: I could throw away my manual checklist. I could tell my VP: "Here are the rules. They are version-controlled. They produce the same result every time. Here is the audit log." That is the kind of tooling story that gets budget approval. It would also mean I can onboard new team members by pointing them at the config instead of explaining tribal knowledge about "when to trust the pipeline and when not to."

### Q5 — Trade-off
> "What would you give up for more determinism? Would you accept less flexibility in how gates are evaluated?"

**Marcus**: Yes, with a caveat. I want deterministic defaults with the ability to add AI-evaluated criteria for subjective things like code readability or design quality. Those can be advisory. But the pass/fail decision on a gate -- whether you can proceed -- that must be rule-based. Split the evaluation: rules decide go/no-go, AI provides commentary.

### Q6 — Priority
> "On a scale of 1-5, how important is this compared to other improvements you'd want?"

**Marcus**: **5 out of 5**. This is the single biggest blocker to me recommending the pipeline for all team work instead of just feature work. Without deterministic gates, I cannot mandate pipeline usage because I cannot defend inconsistent results to leadership.

### Q7 — Concern
> "What worries you about adding a rules engine to the pipeline?"

**Marcus**: Two things. First, rule maintenance -- who owns the rules? If they're in YAML config, they need to be code-reviewed like any other config. I need to make sure my team treats rule changes as seriously as code changes. Second, will the rules be expressive enough? If I want a rule like "any PR touching the payments module requires architecture review," can the engine handle conditional logic based on file paths or module boundaries?

### Q8 — Magic wand
> "If you could change one thing about how the pipeline makes decisions, what would it be?"

**Marcus**: Give me a rule definition language that is powerful enough for real conditions but simple enough that any developer on my team can read and modify it. And make every rule evaluation produce a log entry that I can show in a report. Auditability is not optional -- it's the whole point.

---

## Persona 3: Priya (Enterprise Architect)

**Profile**: Works at a regulated financial services firm. Evaluating Claude Code plugins for enterprise adoption. SOC2 and ISO 27001 compliance are non-negotiable. Concerned about auditability.

### Q1 — Context
> "Tell me about the last time you ran a delivery pipeline and something unexpected happened with the routing or gating."

**Priya**: We did a proof-of-concept evaluation last quarter. We ran the same feature through the pipeline three times with identical inputs as part of our tool assessment. We got three different routing decisions. The compliance team flagged this immediately -- in our environment, a quality gate that produces non-deterministic results is, by definition, not a control. It cannot be cited in a SOC2 audit. We shelved the evaluation at that point. The technology is impressive, but non-determinism in flow control is a non-starter for regulated environments.

### Q2 — Pain
> "What's the most frustrating thing about how pipeline decisions are made today?"

**Priya**: That the pipeline conflates creative assistance with control execution. AI is excellent for generating design options, reviewing code quality, suggesting improvements. But when you use the same AI to decide whether a gate passes or fails, you have introduced variance into your control framework. Our auditors will ask: "How do you ensure this control produces consistent results?" And the honest answer today is: "We cannot." That kills enterprise adoption.

### Q3 — Workaround
> "How do you currently handle inconsistent pipeline behavior?"

**Priya**: We did not adopt it. We are still using our existing SDLC toolchain with manually configured gates in Jira and Jenkins. It's slower, it's clunkier, but it's deterministic and auditable. We have been watching Claude Code plugins for the AI-assisted parts -- code generation, design review, documentation -- but we cannot use the pipeline orchestration until the control problem is solved.

### Q4 — Value
> "If gate decisions were 100% deterministic and configurable, what would that change for you?"

**Priya**: It would reopen our evaluation. Specifically, if I could show my compliance team: (1) gate rules are defined in version-controlled configuration, (2) the same inputs always produce the same gate decision, (3) every evaluation is logged with timestamp, inputs, rule evaluated, and result -- then we could potentially cite delivery-flow gates as automated controls in our SOC2 Type II report. That would be transformative. It would reduce our manual control burden significantly.

### Q5 — Trade-off
> "What would you give up for more determinism? Would you accept less flexibility in how gates are evaluated?"

**Priya**: In a regulated environment, we actively want less flexibility in control execution. Flexibility in controls is a risk, not a feature. We want rigid, predictable, auditable gate decisions. The AI flexibility should be confined to the creative stages -- ideation, design generation, code review commentary. The gates themselves must be deterministic. This is not a trade-off for us; it's an alignment of the tool with how regulated enterprises actually work.

### Q6 — Priority
> "On a scale of 1-5, how important is this compared to other improvements you'd want?"

**Priya**: **5 out of 5**. Without this, the pipeline is not viable for our use case. With this, it becomes a strong candidate to replace significant portions of our current SDLC toolchain. It is binary -- this is the gating feature for enterprise adoption.

### Q7 — Concern
> "What worries you about adding a rules engine to the pipeline?"

**Priya**: Implementation completeness. A rules engine that covers 80% of cases but falls back to AI judgment for the other 20% is not sufficient. Every gate decision path must be rule-based, with no AI fallback for the pass/fail determination. I also need assurance that the audit log is tamper-evident and includes enough context to reconstruct why any decision was made. And the rule configuration schema must be documented well enough for our security team to review and approve.

### Q8 — Magic wand
> "If you could change one thing about how the pipeline makes decisions, what would it be?"

**Priya**: Complete separation of concerns. AI handles content generation and advisory feedback. A deterministic rules engine handles all flow control, gating, and routing decisions. The two never cross. The rules engine produces a complete, queryable audit trail. That architecture would make this tool enterprise-ready overnight.

---

## Persona 4: Jake (Game Developer)

**Profile**: Indie game dev using Godot. Uses the godot skill within delivery-flow. Cares most about game feel and iteration speed. Skeptical of "process overhead."

### Q1 — Context
> "Tell me about the last time you ran a delivery pipeline and something unexpected happened with the routing or gating."

**Jake**: I was iterating on a player movement system -- trying to get the jump arc to feel right. I ran it through the pipeline thinking it would be a quick BUG_FIX type since I was just tweaking physics values. The pipeline decided it was a FEATURE and routed me through design and architecture stages. For changing three float values. I killed the pipeline and just edited the code directly. Game dev is all about rapid iteration -- tweak, test, feel, repeat. You cannot put a gate between each iteration cycle.

### Q2 — Pain
> "What's the most frustrating thing about how pipeline decisions are made today?"

**Jake**: The pipeline does not understand game dev workflows. Game feel tuning is not a "feature" or a "bug fix" -- it's its own thing. But the AI keeps trying to categorize it into software development buckets that do not fit. I end up fighting the pipeline's classification more than I fight the actual code. And sometimes the same tuning change gets classified differently, so I never know what I'm in for.

### Q3 — Workaround
> "How do you currently handle inconsistent pipeline behavior?"

**Jake**: I use the godot skill directly for most things and only use the full pipeline for big features like adding a new game system or a new level. For iteration work -- which is 70% of game dev -- I bypass the pipeline entirely. I know that's not ideal, but the pipeline's overhead does not justify itself for "make the jump feel better."

### Q4 — Value
> "If gate decisions were 100% deterministic and configurable, what would that change for you?"

**Jake**: If I could configure a rule like "changes to physics parameters or animation curves skip design and architecture stages" -- that would get me back into the pipeline for iteration work. I want the pipeline's quality checks, just not its routing overhead for the types of changes I make most frequently. Deterministic rules would let me carve out fast paths for game-dev-specific workflows.

### Q5 — Trade-off
> "What would you give up for more determinism? Would you accept less flexibility in how gates are evaluated?"

**Jake**: For game dev? Yes, easily. I would rather have fast, predictable paths that I defined than smart, slow paths that the AI chose. The AI does not know what "game feel" means. I do. Let me define the rules for when things need full review versus when they can fast-track, and I'll be happy. The only flexibility I want is the AI's creativity in the actual code generation and design suggestion parts.

### Q6 — Priority
> "On a scale of 1-5, how important is this compared to other improvements you'd want?"

**Jake**: **3 out of 5**. It is important, but for me the bigger win would be better game-dev-aware routing in general. The rules engine is a means to an end -- the end being "stop making me do architecture review for tweaking jump height." If the rules engine enables that, great. If there's another way to get there, I'm open to it.

### Q7 — Concern
> "What worries you about adding a rules engine to the pipeline?"

**Jake**: More config to manage. I'm a solo indie dev -- I want to make games, not write YAML. If this means I need to become a rules engine expert before I can use the pipeline comfortably, that's a net negative. It needs to ship with game-dev presets that work out of the box. Also, don't make the rules engine itself slow. If evaluating rules adds even 5 seconds to each pipeline step, that's 5 seconds too many when I'm in a tight iteration loop.

### Q8 — Magic wand
> "If you could change one thing about how the pipeline makes decisions, what would it be?"

**Jake**: Add a "game feel iteration" mode. One command that says "I'm tuning, not building." Minimal gates, fast path, just quality checks on the code itself. Whether that's implemented as rules engine presets or a dedicated mode, I do not care, as long as it's fast.

---

## Persona 5: Chen (DevOps Engineer)

**Profile**: Platform engineer at a startup. Interested in CI/CD integration with delivery-flow. Wants deterministic pipeline behavior that mirrors their existing CI/CD philosophy.

### Q1 — Context
> "Tell me about the last time you ran a delivery pipeline and something unexpected happened with the routing or gating."

**Chen**: I was evaluating delivery-flow as a pre-CI step -- the idea being that developers run through the pipeline before pushing to our GitHub Actions workflow. I set up a test where I ran the same feature through the pipeline twice from a clean state. The first run required architecture review, the second didn't. In CI/CD, that's a cardinal sin. If your pipeline produces different results for the same input, your pipeline is broken. I flagged it as a blocker for adoption and moved on to evaluating other options.

### Q2 — Pain
> "What's the most frustrating thing about how pipeline decisions are made today?"

**Chen**: Non-determinism in a pipeline context is not a feature, it's a bug. My entire CI/CD philosophy is: same commit, same environment, same result. Every time. The delivery-flow pipeline violates this principle at a fundamental level. I understand why -- AI brings creativity and judgment -- but those qualities belong in the development phase, not in the pipeline control plane. The pipeline should be infrastructure, and infrastructure must be deterministic.

### Q3 — Workaround
> "How do you currently handle inconsistent pipeline behavior?"

**Chen**: I didn't adopt it. I built a lightweight pre-push hook using shell scripts that does basic checks: test coverage threshold, linting, commit message format, changelog entry. It's primitive compared to what delivery-flow offers, but it's deterministic. I can write a GitHub Actions workflow that gates on these checks and know exactly what will happen. I keep watching the delivery-flow project because the concept is excellent, but the execution needs deterministic foundations.

### Q4 — Value
> "If gate decisions were 100% deterministic and configurable, what would that change for you?"

**Chen**: Everything. I could integrate delivery-flow gates into our CI/CD pipeline as actual pipeline stages. I could write a GitHub Action that runs rule evaluations and gates the PR merge on the results. I could version the rule configuration alongside the application code so that rule changes go through the same PR review process. I could even generate pipeline dashboards from the audit logs. Deterministic + configurable + auditable = infrastructure-grade tooling. That's what I need.

### Q5 — Trade-off
> "What would you give up for more determinism? Would you accept less flexibility in how gates are evaluated?"

**Chen**: I would actively prefer less flexibility in gate evaluation. In fact, I would advocate for a strict mode where AI is completely excluded from gate decisions -- rules only, no fallback. AI advisory commentary is fine as a separate output, but the gate signal (pass/fail/warn) must come exclusively from the rules engine. If you give teams the option to let AI influence gate results, some team will enable it and then wonder why their pipeline is flaky.

### Q6 — Priority
> "On a scale of 1-5, how important is this compared to other improvements you'd want?"

**Chen**: **5 out of 5**. This is the prerequisite for everything else I'd want. CI/CD integration, pipeline-as-code, audit dashboards -- none of that is possible without deterministic gates. It's the foundation.

### Q7 — Concern
> "What worries you about adding a rules engine to the pipeline?"

**Chen**: Scope creep. Rules engines have a tendency to grow into their own DSL with complex conditional logic, and before you know it you're maintaining a programming language. Keep it simple: conditions evaluate to true/false, gates aggregate conditions with AND/OR logic, rules are evaluated in defined order. Also, the rule evaluation itself must be fast and side-effect-free -- no network calls, no file system mutations during evaluation. And please make the audit log structured (JSON), not just human-readable text.

### Q8 — Magic wand
> "If you could change one thing about how the pipeline makes decisions, what would it be?"

**Chen**: Make the pipeline export a declarative rule manifest -- a single file that describes every decision point, every condition, every threshold. Something I can diff between versions, validate in CI, and use to generate documentation. Pipeline-as-code, but for the decision layer, not just the execution layer.

---

## Synthesis

### Common Themes

1. **Non-determinism is universally recognized as a problem.** All 5 personas identified inconsistent gate results as a significant issue, though the severity ranged from "annoying" (Sarah, Jake) to "adoption blocker" (Marcus, Priya, Chen).

2. **Clear demand for separation of AI creativity from flow control.** Every persona independently articulated the same architectural principle: AI should handle creative/advisory work; rules should handle routing and gating. This was the strongest consensus point.

3. **Configuration simplicity is critical.** 4 of 5 personas raised concerns about configuration complexity. They want powerful rules but not a complex DSL. Presets, profiles, and sane defaults were requested repeatedly.

4. **Auditability is not optional.** Marcus, Priya, and Chen all explicitly need audit trails. Even Sarah and Jake implicitly benefit from predictable, explainable decisions. Structured audit logs enable reporting, compliance, and CI/CD integration.

5. **Speed must not regress.** Sarah and Jake explicitly flagged performance concerns. The rules engine must evaluate fast -- adding latency to pipeline steps is unacceptable, especially for iteration-heavy workflows.

### Priority Consensus

| Persona | Score | Rationale |
|---------|-------|-----------|
| Sarah (Solo Dev) | 4 | High value but ranks speed improvement slightly higher |
| Marcus (Team Lead) | 5 | Blocker for team-wide pipeline adoption |
| Priya (Enterprise Architect) | 5 | Binary: without this, tool is not viable for regulated environments |
| Jake (Game Dev) | 3 | Values the outcome but sees rules engine as means to an end |
| Chen (DevOps Engineer) | 5 | Prerequisite for all desired CI/CD integrations |

- **Average**: 4.4 / 5
- **Range**: 3 to 5
- **Mode**: 5 (3 of 5 personas)

### Top Concerns to Address

1. **Configuration complexity** -- Must ship with presets/profiles (solo, team, enterprise, game-dev). Advanced configuration optional, not required.
2. **Rule expressiveness vs simplicity** -- Need conditional logic (e.g., "if file path matches X, require Y") without becoming a full DSL. AND/OR/NOT with condition predicates.
3. **Performance overhead** -- Rule evaluation must add negligible latency. No network calls or I/O during evaluation.
4. **Completeness** -- Enterprise users need 100% rule-based gate decisions. No AI fallback on the pass/fail determination.
5. **Audit log format** -- Must be structured (JSON), queryable, and include: timestamp, rule ID, inputs, result, and reasoning.
6. **Scope control** -- Keep the rules engine focused. Resist the temptation to build a Turing-complete DSL.

### Feature Requirements Derived from Interviews

| Requirement | Source Personas | Priority |
|-------------|----------------|----------|
| Deterministic gate evaluation (same input = same result) | All 5 | Must-have |
| YAML-based rule configuration in version control | Marcus, Priya, Chen | Must-have |
| Structured audit log (JSON) for every rule evaluation | Marcus, Priya, Chen | Must-have |
| Preset profiles (solo, team, enterprise, game-dev) | Sarah, Jake | Must-have |
| Separation of AI advisory from gate pass/fail | All 5 | Must-have |
| Conditional routing rules (file paths, modules, change scope) | Marcus, Jake | Should-have |
| Strict mode (no AI influence on gate decisions) | Chen, Priya | Should-have |
| CI/CD integration hooks (exportable rule manifest) | Chen | Should-have |
| Custom fast-path definitions (e.g., "iteration mode") | Jake, Sarah | Should-have |
| Rule evaluation performance SLA (sub-100ms) | Sarah, Jake | Should-have |
| Rule change review workflow (treat as code) | Marcus, Chen | Nice-to-have |
| Dashboard/reporting from audit logs | Marcus, Chen | Nice-to-have |

### Segments Most/Least Enthusiastic

**Most enthusiastic**: Enterprise (Priya) and DevOps (Chen) segments. For both, deterministic rules are the difference between "cannot adopt" and "strong candidate to replace existing tooling." Marcus (Team Lead) is close behind -- his pain is acute and daily.

**Least enthusiastic**: Game Dev (Jake). Not opposed, but views it as indirect value. His core need is faster iteration, and a rules engine is one possible solution. If the rules engine ships with game-dev presets that create fast iteration paths, his enthusiasm would likely increase.

**Swing segment**: Solo Dev (Sarah). Currently bypasses the pipeline for speed. Deterministic rules with lightweight presets could bring her back into the pipeline for all work, but only if configuration is genuinely simple. High risk of losing this segment to complexity.
