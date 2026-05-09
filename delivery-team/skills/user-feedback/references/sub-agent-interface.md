# Sub-Agent Interface (Agentic Flow Integration)

For orchestration with other delivery-team skills, the user-feedback skill accepts and produces structured contracts. Load this reference when the user-feedback skill is invoked from an orchestrator (delivery-flow, agentic-flow-builder) rather than directly from the user.

---

## Input Contract

```json
{
  "stage": "refine | design | dev | uat",
  "artifact_type": "prd | wireframe | feature | product",
  "artifact": "string (markdown)",
  "personas": ["list of persona names or 'auto'"],
  "project_type": "GREENFIELD | FEATURE | GAME_DEV | ENTERPRISE | B2B | WEB_APP",
  "custom_personas": [
    {
      "name": "string",
      "age": "number",
      "background": "string",
      "tech_literacy": "low | medium | high",
      "goals": ["array"],
      "frustrations": ["array"],
      "behaviors": ["array"],
      "accessibility_needs": "string or null",
      "devices": ["array"],
      "personality": "string"
    }
  ],
  "overlays": {"persona_name": "demographic_overlay_name"},
  "persona_count": "number (3-7, optional)"
}
```

---

## Output Contract

```json
{
  "stage": "string",
  "personas_consulted": ["list of persona names"],
  "avg_satisfaction": 3.8,
  "consensus_issues": [
    {
      "issue": "string",
      "priority": "CRITICAL | HIGH | MEDIUM | LOW",
      "personas": ["list of names"],
      "recommendation": "string"
    }
  ],
  "design_tensions": [
    {
      "element": "string",
      "perspectives": [
        {"persona": "name", "position": "string"},
        {"persona": "name", "position": "string"}
      ],
      "recommendation": "string"
    }
  ],
  "per_persona": [
    {
      "name": "string",
      "category": "string",
      "satisfaction": 4,
      "likes": ["array"],
      "issues": [
        {
          "description": "string",
          "feeling": "string",
          "expectation": "string",
          "severity": "deal-breaker | annoying | minor | nice-to-have"
        }
      ],
      "missing": ["array"],
      "would_recommend": "yes | no | maybe"
    }
  ],
  "recommendations": [
    {
      "priority": "CRITICAL | HIGH | MEDIUM | LOW",
      "description": "string"
    }
  ],
  "preserve": ["array — things not to break"],
  "escalation_needed": false,
  "escalation_reasons": ["array (empty if no escalation)"]
}
```
