# Getting Started with the Delivery Team

This guide gets you from zero to a running delivery pipeline in under 5 minutes. It covers the quick-start wizard, a skill map, your first pipeline walkthrough, and a command cheat sheet.

> **Stuck?** Jump to [`troubleshooting.md`](troubleshooting.md) for the SYMPTOM → CAUSE → FIX quick reference.

---

## Quick Start (3 Questions)

The full setup wizard asks 9+ questions about your project type, tech stack, team size, deployment, risk tolerance, compliance, checkpoints, collaboration patterns, personas, and enforcement. That is thorough but slow for someone who just wants to get going.

**Quick-start mode** collapses all of that into 3 questions. Say "quick start", "quick setup", or "just get started" when the wizard launches.

### Question 1: What are you building?

Describe your project in one sentence. The wizard auto-detects the project type from your answer:

| You Say | Detected Type |
|---------|--------------|
| "New web app from scratch" | GREENFIELD |
| "Adding search to our API" | FEATURE |
| "Fix the login crash" | BUG_FIX |
| "New roguelike in Godot" | GAME_DEV+GREENFIELD |
| "Investigate whether Redis fits" | SPIKE |
| "Write API docs" | DOCS_ONLY |

### Question 2: What language/framework?

The wizard scans your codebase for languages and frameworks. It presents what it found and asks you to confirm or correct. If this is a greenfield project with no codebase yet, just tell it what you plan to use.

### Question 3: How strict?

Pick a strictness level. This sets checkpoints, collaboration patterns, enforcement, and ceremony in one shot.

| Level | What It Means |
|-------|--------------|
| **Prototype** | Minimal gates. Fast. Evaluator-optimizer only. No human checkpoints except UAT. Source code hook off. |
| **Standard** | Balanced. Evaluator-optimizer + adversarial review + decision routing. Checkpoints at Refine and UAT. Source code hook on. |
| **Strict** | Full ceremony. All 6 collaboration patterns. All 4 checkpoints. All enforcement on. |

Everything else -- team size, deployment, compliance, personas, git strategy -- uses smart defaults derived from your project type and strictness level. You can always re-run `setup` later to fine-tune individual settings.

---

## Skill Map

The delivery team has 10 skills. Here is what each one does and when to use it.

```
delivery-team:delivery-flow    Start here. Orchestrates everything.
delivery-team:developer        Write code in any of 14 languages
delivery-team:architect        Design systems, decompose, ADRs
delivery-team:quality          Test strategy, test cases, QA
delivery-team:operations       CI/CD, deployment, releases, docs
delivery-team:product-delivery Stories, PRDs, retros, metrics
delivery-team:ui               UX flows, wireframes, design systems
delivery-team:godot            Godot 4.x game development
delivery-team:user-feedback    Simulated persona testing
delivery-team:alias-creator    Create custom character themes
```

### When to Use Each Skill Directly (vs Through the Pipeline)

**Use `delivery-flow` for**: new features, greenfield projects, game development, any multi-stage work where you want structured requirements, architecture, planning, development, and QA.

**Use `developer` directly for**: quick one-off code tasks, small bug fixes you do not need the full pipeline for, code refactoring within an already-designed system.

**Use `architect` directly for**: writing ADRs, technology evaluation, architecture review of an existing system, decomposition analysis without a full pipeline run.

**Use `quality` directly for**: test case design for existing code, test strategy documents, quality metrics analysis, exploratory testing plans.

**Use `operations` directly for**: writing technical documentation, release planning, CI/CD pipeline design, runbook creation.

**Use `product-delivery` directly for**: writing user stories from scratch, sprint retrospectives, product metrics analysis, A/B test design.

**Use `ui` directly for**: UX flow design, wireframe creation, design system documentation, accessibility review.

**Use `godot` directly for**: quick Godot scripting tasks, scene setup, signal wiring -- when you already know what to build and just need implementation.

**Use `user-feedback` directly for**: running a simulated focus group on a design, getting persona-based feedback on a feature concept, usability testing outside the pipeline.

**Use `alias-creator` directly for**: creating custom character themes (Lord of the Rings, Star Wars, etc.) that change how the delivery team members present themselves.

---

## Your First Pipeline Run

Here is a step-by-step walkthrough of a minimal pipeline run using quick-start mode.

### Step 1: Start the Pipeline

Say: "start a new feature"

This triggers `delivery-team:delivery-flow`. The orchestrator activates and checks for existing configuration.

### Step 2: Quick-Start Wizard

If no `.delivery/config.yml` exists, the wizard launches. Say "quick start" to use the 3-question mode:

1. Describe what you are building.
2. Confirm the detected tech stack (or specify it).
3. Pick prototype / standard / strict.

The wizard generates `.delivery/config.yml` and initializes the `.delivery/` directory.

### Step 3: Idea (Stage 1)

Describe your idea in detail. The Product Owner captures it as an idea brief, and the team validates it meets the entry criteria for refinement.

### Step 4: Refine (Stage 2)

The Product Owner writes a PRD (Product Requirements Document) with user stories, acceptance criteria, and scope. If checkpoints are enabled, you review and approve the PRD before moving on.

### Step 5: Design (Stage 3)

The UX Designer creates user flows and wireframes. The team reviews the design for completeness and usability.

### Step 6: Architect (Stage 4)

The Architect designs the system architecture -- component decomposition, data models, API contracts, technology decisions. If checkpoints are enabled, you approve the architecture.

### Step 7: Plan (Stage 5)

The Scrum Bag creates a sprint plan with stories broken into implementable tasks, each with test cases. If checkpoints are enabled, you approve the plan.

### Step 8: Development (Stage 6)

The Developer implements each story. The QA Engineer reviews each implementation against acceptance criteria. Self-correction loops handle issues automatically (up to the configured limit).

### Step 9: UAT (Stage 7)

User Acceptance Testing runs. Simulated personas test the deliverables. You review the final output and accept or reject. Once accepted, the pipeline completes and writes a memory file with lessons learned.

---

## Common Commands Cheat Sheet

| What You Want | Say This |
|--------------|---------|
| Start a project | "start a new feature" |
| Start fast | "quick start" |
| Write code | "implement this story" |
| Get architecture | "design the architecture for..." |
| Run tests | "create test cases for..." |
| Get user feedback | "run a focus group on this design" |
| Change theme | Edit `.delivery/config.yml` and set `aliases.theme: lotr` |
| See pipeline status | "status" |
| Re-run setup | "setup" |
| Change one setting | "change risk tolerance to strict" |
| Skip a stage | The pipeline handles stage skipping based on project type |
| Resume a pipeline | "resume" (if a previous run was interrupted) |

---

## Smart Defaults Reference

When quick-start mode runs, it derives all other settings from your project type and strictness level. Here is what you get by default.

### By Project Type

| Setting | GREENFIELD | FEATURE | BUG_FIX | GAME_DEV+ | SPIKE | DOCS_ONLY |
|---------|-----------|---------|---------|-----------|-------|-----------|
| Checkpoints | all 4 | refine, uat | uat | all 4 | none | uat |
| Persona categories | web-users | web-users | none | gamers | none | none |
| Collaboration depth | all 6 | all 6 | eval + routing | all 6 | eval only | eval only |

### By Strictness Level

| Setting | Prototype | Standard | Strict |
|---------|-----------|----------|--------|
| Collaboration patterns | evaluator-optimizer | eval + adversarial + routing | all 6 |
| Source code hook | off | on | on |
| Retro frequency | manual | every-run | every-run |
| Retro skip allowed | yes | yes | no |

### Overriding Defaults

Quick-start gets you going fast, but you can always fine-tune later:

- **Re-run the full wizard**: say "setup" to answer all 9+ questions
- **Change one setting**: say "change [setting] to [value]" and the wizard updates just that key
- **Edit directly**: open `.delivery/config.yml` and modify the YAML frontmatter

See `config-schema.md` for the complete list of all configuration keys, their types, defaults, and valid values.

---

## Troubleshooting

**"Pipeline bypass detected" warning**: You invoked a skill (like `developer` or `godot`) outside the delivery pipeline. This is the enforcement hook doing its job. If you want to use the skill directly without the pipeline, that is fine -- the warning is informational, not blocking.

**"Config is stale" message**: Your `.delivery/config.yml` is more than 30 days old. Run "setup" to refresh it, or ignore the message if your settings are still correct.

**Pipeline seems stuck**: Check "status" to see where the pipeline is. If a self-correction loop hit its limit, the pipeline escalates to you for a decision.

**Too much ceremony**: Re-run "setup" and pick "prototype" strictness, or say "change risk tolerance to prototype" to reduce gates and collaboration patterns.

**Not enough review**: Re-run "setup" and pick "strict" strictness, or enable specific checkpoints and patterns individually.
