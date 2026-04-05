# User Feedback

**Invocation**: `delivery-team:user-feedback`

Simulated end-user feedback agent that spawns persona-based sub-agents to review product artifacts from real user perspectives.

## How It Works

1. **Select personas** based on project type (3-7 personas)
2. **Prepare artifact** — strip implementation details, present as user-facing content
3. **Spawn each persona independently** — each is a separate sub-agent with only its profile
4. **Aggregate results** — synthesize consensus, conflicts, and recommendations

Personas never see each other's feedback. This independence produces diverse perspectives.

## Built-In Personas

### Gamers

| Persona | Profile |
|---------|---------|
| Casual Casey | Plays in short sessions, values accessibility and simplicity |
| Hardcore Hank | Wants depth, challenge, and mastery mechanics |
| Speedrunner Sam | Optimizes for efficiency, finds exploits |
| Completionist Cora | Wants to experience everything, thorough explorer |
| Social Skyler | Plays for social interaction and community |
| Accessible Alex | Uses assistive technology, evaluates accessibility |
| Mobile Morgan | Plays on mobile, values touch-friendly UI |

### Web/App Users

| Persona | Profile |
|---------|---------|
| Power User Pat | Expert user, wants keyboard shortcuts and efficiency |
| Average User Avery | Mainstream user with moderate tech literacy |
| First-Time Fiona | Brand new user, evaluates onboarding |
| Non-Technical Nate | Low tech literacy, needs clear guidance |
| Accessible Ash | Uses screen reader, evaluates accessibility |

### Enterprise/B2B

| Persona | Profile |
|---------|---------|
| Admin Alice | System administrator, evaluates configuration |
| End User Eddie | Day-to-day user, evaluates workflow efficiency |
| Manager Maya | Needs reporting and oversight capabilities |
| IT/Security Ivan | Evaluates security, compliance, and integration |

### Demographic Overlays

Gen Z Zara, Millennial Mia, Gen X Xavier, Boomer Barbara — these modify communication style and expectations without replacing the base persona.

## Selection Rules

- **Minimum**: 3 personas. **Recommended**: 5. **Maximum**: 7.
- At least 1 accessibility persona is always included
- Custom personas can be defined in `.delivery/config.yml` or described in natural language

## Pipeline Integration

Persona feedback runs at configurable stages (default: Refine, Design, Dev, UAT). Each stage provides stage-appropriate artifacts to personas.

## Example Usage

```
User: "Run a focus group on this checkout design"

Personas: Power User Pat, First-Time Fiona, Accessible Ash,
          Average User Avery, Non-Technical Nate

Output: Individual persona feedback + aggregated report with
        consensus findings, conflicts, and recommendations
```
