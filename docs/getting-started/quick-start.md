# Quick Start

Get from zero to a running delivery pipeline in under 5 minutes.

## Quick-Start Wizard (3 Questions)

The full setup wizard asks 9+ questions about your project. Quick-start mode collapses everything into 3 questions. Say **"quick start"**, **"quick setup"**, or **"just get started"** when the wizard launches.

### Question 1: What are you building?

Describe your project in one sentence. The wizard auto-detects the project type:

| You Say | Detected Type |
|---------|--------------|
| "New web app from scratch" | GREENFIELD |
| "Adding search to our API" | FEATURE |
| "Fix the login crash" | BUG_FIX |
| "New roguelike in Godot" | GAME_DEV+GREENFIELD |
| "Investigate whether Redis fits" | SPIKE |
| "Write API docs" | DOCS_ONLY |

### Question 2: What language/framework?

The wizard scans your codebase for languages and frameworks. Confirm or correct what it finds. For greenfield projects with no codebase yet, just tell it what you plan to use.

### Question 3: How strict?

| Level | What It Means |
|-------|--------------|
| **Prototype** | Minimal gates. Fast. Evaluator-optimizer only. No human checkpoints except UAT. |
| **Standard** | Balanced. Evaluator-optimizer + adversarial review + decision routing. Checkpoints at Refine and UAT. |
| **Strict** | Full ceremony. All 6 collaboration patterns. All 4 checkpoints. All enforcement on. |

Everything else uses smart defaults based on your project type and strictness level. You can re-run `setup` later to fine-tune.

---

## Your First Pipeline Run

### Step 1: Start the Pipeline

Say: **"start a new feature"**

This triggers `delivery-team:delivery-flow`. The orchestrator checks for existing configuration.

### Step 2: Quick-Start Wizard

If no `.delivery/config.yml` exists, the wizard launches. Say "quick start" and answer the 3 questions. The wizard generates your config and initializes the `.delivery/` directory.

### Step 3: Idea (Stage 1)

Describe your idea in detail. The Product Owner captures it as an idea brief and validates it meets entry criteria.

### Step 4: Refine (Stage 2)

The Product Owner writes a PRD with user stories, acceptance criteria, and scope. If checkpoints are enabled, you review and approve before moving on.

### Step 5: Design (Stage 3)

The UX Designer creates user flows and wireframes. The team reviews for completeness and usability.

### Step 6: Architect (Stage 4)

The Architect designs system architecture — components, data models, API contracts, technology decisions. If checkpoints are enabled, you approve the architecture.

### Step 7: Plan (Stage 5)

The Scrum Master creates a sprint plan with implementable tasks and test cases. If checkpoints are enabled, you approve the plan.

### Step 8: Development (Stage 6)

The Developer implements each story. The QA Engineer reviews against acceptance criteria. Self-correction loops handle issues automatically.

### Step 9: UAT (Stage 7)

User Acceptance Testing runs. Simulated personas test the deliverables. You review the final output and accept or reject. On acceptance, the pipeline completes and writes lessons to memory.

---

## Skill Map

Use skills directly for standalone tasks, or through the pipeline for full delivery:

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
delivery-team:presentation     Team-collaborative presentations
```

### When to Use Skills Directly

- **`developer`** — Quick one-off code tasks, small bug fixes, refactoring
- **`architect`** — ADRs, tech evaluation, architecture review without full pipeline
- **`quality`** — Test case design, test strategy, quality metrics for existing code
- **`operations`** — Technical docs, release planning, CI/CD pipeline design
- **`product-delivery`** — User stories, retrospectives, product metrics
- **`ui`** — UX flows, wireframes, design system documentation
- **`godot`** — Quick Godot scripting, scene setup, signal wiring
- **`user-feedback`** — Simulated focus group outside the pipeline
- **`alias-creator`** — Create or edit character themes
