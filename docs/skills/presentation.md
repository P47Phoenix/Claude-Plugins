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

## Narrative Intelligence

Step 4 (Compose) runs four sequential editorial passes that transform slide content. Order is strict: Emphasis > Cutting > Framing > Tension. Each pass can be individually disabled via config.

| Pass | Config Key | Effect |
|------|-----------|--------|
| **Emphasis Selection** | `presentation.narrative.emphasis` | Reorders slides so highest-impact content leads (data-backed results first, user impact over technical achievement) |
| **Information Cutting** | `presentation.narrative.cutting` | Removes or merges slides that do not earn their place (no data + no decision = cut candidate) |
| **Audience-Specific Framing** | `presentation.narrative.framing` | Restructures the argument within each slide based on audience values (investor, executive, technical, client-facing, casual) |
| **Narrative Tension** | `presentation.narrative.tension` | Positions the climax slide at the 60-70% point for maximum impact (requires 6+ slides) |

Step 4 never degrades -- all enabled editorial passes run at full depth regardless of light mode or threshold status.

## Configuration

```yaml
presentation:
  default_format: structured-markdown
  default_audience: technical
  speaker_notes: false
  save_to_artifacts: true
  marp_theme: default
  staleness_warning_days: 7
  vocabulary_overrides: {}
  narrative:
    emphasis: true
    cutting: true
    framing: true
    tension: true
  light_mode: auto
  thresholds: {}
  thresholds_default: 90
  pptx_template: ""
  pptx_font: Calibri
  pptx_accent_color: "#2d5aa0"
```
