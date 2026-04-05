# Commands Reference

Commands available within the delivery pipeline and individual skills.

## Pipeline Commands

These commands are available when the delivery-flow orchestrator is active:

| Command | Action |
|---------|--------|
| `setup` | Run or re-run the setup wizard |
| `quick start` | Run the 3-question quick-start wizard |
| `status` | Show current pipeline state |
| `resume` | Resume an interrupted pipeline run |
| `skip pipeline` | Proceed without quality gates (when warned) |

## Product Owner Commands

Available in the `product-delivery` skill (Product Owner role):

| Command | Action |
|---------|--------|
| `split` | Split the current story (failed the Small criterion) |
| `detail <story #>` | Expand a story title into full story + ACs |
| `score` | Apply RICE or WSJF scoring to the current backlog |
| `moscow` | Reformat backlog using MoSCoW categories |
| `refine` | Tighten acceptance criteria |
| `persona <name>` | Switch the user persona for story writing |
| `prd` | Expand current stories/epic into a full PRD |
| `sprint` | Produce a sprint plan from current backlog |
| `accept` | Finalize and deliver the current artifact |

## Scrum Master Commands

Available in the `product-delivery` skill (Scrum Master role):

| Command | Action |
|---------|--------|
| `retro` | Start a retrospective |
| `facilitate` | Produce a facilitation guide for a ceremony |
| `metrics` | Analyze velocity or agile metrics |
| `assess` | Run an agile maturity assessment |

## Data Analyst Commands

Available in the `product-delivery` skill (Data Analyst role):

| Command | Action |
|---------|--------|
| `dashboard` | Design a dashboard specification |
| `experiment` | Create an A/B test plan |

## Developer Commands

Available in the `developer` skill:

| Command | Action |
|---------|--------|
| `lang <name>` | Override detected language |
| `review` | Switch to code review mode |
| `test` | Generate tests for current code |
| `refactor` | Improve structure without behavior change |
| `explain` | Annotate and explain the code |
| `accept` | Finalize and write pending files to disk |

## Architect Commands

Available in the `architect` skill:

| Command | Action |
|---------|--------|
| `role <name>` | Override detected role |
| `adr` | Write an ADR for the current decision |
| `c4` | Produce C4 diagram descriptions |
| `review` | Switch to architecture review mode |
| `evaluate` | Compare technologies or approaches |
| `decompose` | Break system into services/components |
| `threats` | Run threat modeling |
| `quality` | Analyze quality attributes |
| `budget` | Analyze performance budget (game roles) |
| `accept` | Finalize current artifact |
| `adr review` | Review all ADRs for staleness |

## Presentation Commands

Available in the `presentation` skill:

| Command | Action |
|---------|--------|
| `present --full` | Force full mode (all contributors) |
| `present --light` | Force light mode (reduced contributors) |
