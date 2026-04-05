# Presentation

**Invocation**: `delivery-team:presentation`

Presentation Composer that assembles team contributions into cohesive presentations through a 6-step collaboration flow.

## Design Principle

The Composer is a **mini-orchestrator**, not a content creator. It assembles contributions from delivery team roles (PO, Data Analyst, Developer, Architect, QA) into a cohesive presentation. Each contributing role loads its own skill. The Composer shapes tone, flow, density, and format.

## How to Trigger

- "create presentation", "sprint review", "sprint demo"
- "pitch", "propose", "sell this feature"
- "status update", "executive update"
- "technical presentation", "deep dive"
- "investor pitch", "roadmap", "product demo"
- "onboarding", "retro summary"

## Presentation Types

| Type | When to Use |
|------|-------------|
| Sprint Review | End of sprint — what was delivered |
| Feature Pitch | Proposing a new feature |
| Stakeholder Update | Progress report for executives |
| Technical Deep-Dive | Architecture or implementation overview |
| Investor Pitch | Fundraising or investment presentation |
| Roadmap | Quarterly plan or what is coming next |
| Product Demo | Showcase completed features |
| Onboarding | Project handoff or team orientation |
| Retrospective Summary | What the team learned |

## 6-Step Flow

1. **Assemble** — Identify type, contributing roles, and source artifacts
2. **Content Gate** — Verify source artifacts exist and are sufficient
3. **Draft** — Contributing roles produce domain-specific content sections
4. **Compose** — Editorial passes: emphasis, cutting, audience framing, narrative tension
5. **Review Gate** — Technical Writer (and optionally UX) review for quality
6. **User Review** — User reviews and approves the final presentation

## Output Formats

- **Structured Markdown** (default)
- **Marp** — Markdown-based slide decks
- **Paste-Ready** — Formatted for copy-paste into slide tools
- **PPTX** — PowerPoint output with configurable template and branding

## Light Mode

Reduces sub-agent dispatch for simpler presentation types:

| Config Value | Behavior |
|-------------|----------|
| `auto` (default) | Light mode when 3 or fewer contributing roles |
| `always` | Light mode for all types |
| `never` | Full mode always |

Override per-request: `present --full` or `present --light`

## Example Usage

```
User: "Create a sprint review for what we delivered"

Type: Sprint Review (auto-detected)
Contributing roles: PO (what was delivered), Developer (technical details),
                    QA (test results), Data Analyst (metrics)

Output: Structured presentation with slides covering deliverables,
        technical highlights, quality metrics, and next steps
```

## Configuration

```yaml
presentation:
  default_format: structured-markdown
  default_audience: technical
  speaker_notes: false
  light_mode: auto
  thresholds_default: 90
```
