# User Guides

## Diataxis Framework

### Four Content Types

The Diataxis framework organizes documentation into four types based on two axes: learning vs working, and practical vs theoretical.

| Type | Orientation | Purpose | User Need |
|------|------------|---------|-----------|
| **Tutorial** | Learning-oriented | Teach by doing | "I want to learn" |
| **How-To Guide** | Task-oriented | Solve a specific problem | "I want to accomplish X" |
| **Reference** | Information-oriented | Provide technical facts | "I need to look up Y" |
| **Explanation** | Understanding-oriented | Clarify concepts | "I want to understand why" |

### Tutorials (Learning-Oriented)

- Designed for beginners encountering the topic for the first time
- Lead the reader through a series of steps to complete a meaningful project
- Every step must work -- test the tutorial from start to finish before publishing
- Focus on learning, not on building something useful -- the tutorial is the point, not the product
- Do not explain concepts in depth -- link to explanation docs for deeper understanding
- Keep decisions minimal -- tell the reader exactly what to do at each step

### How-To Guides (Task-Oriented)

- Written for users who already understand the basics and need to accomplish a specific task
- Start with the goal: "How to configure email notifications"
- Assume the reader knows the system but may not know this specific procedure
- Include prerequisites: what must be true before starting
- Steps are numbered, specific, and actionable
- Include verification: how to confirm the task was completed successfully

### Reference (Information-Oriented)

- Structured for lookup, not reading -- users scan for specific information
- Organized by the structure of the system (API endpoints, configuration options, CLI commands)
- Complete and accurate -- reference docs must cover every option, parameter, and field
- Austere -- minimal explanation, maximum precision. Describe what something is, not how to use it.
- Consistent format -- every entry follows the same structure

### Explanation (Understanding-Oriented)

- Provides context, background, and reasoning
- Answers "why" questions: why the system works this way, why this approach was chosen
- Can discuss alternatives, trade-offs, and history
- Not tied to specific tasks -- readers come to understand, not to do
- Links to relevant how-to guides and reference docs for practical follow-up

---

## Audience Analysis

### Levels

| Level | Characteristics | Documentation Approach |
|-------|----------------|----------------------|
| **Beginner** | New to the product and possibly the domain. Needs hand-holding. | Start with concepts, use simple language, explain every step, provide screenshots or diagrams. |
| **Intermediate** | Familiar with basics, can navigate the product. Needs help with specific tasks. | Task-focused how-to guides, assume basic knowledge, focus on the procedure not the concepts. |
| **Advanced** | Expert user or developer. Needs reference material and edge case documentation. | Concise reference docs, advanced configuration, API details, performance tuning. |

### Identifying the Audience

Before writing any document, answer:

1. Who will read this? (Role: developer, operator, end-user, manager)
2. What do they already know? (Prerequisites: technologies, concepts, prior experience)
3. What do they need to accomplish? (Goal: set up, configure, troubleshoot, understand)
4. What is their context? (Environment: production, development, evaluation)

### Adjusting Depth

- For beginners: explain terms, provide context, include examples of expected output
- For intermediate users: skip concept introductions, link to them instead
- For advanced users: provide configuration reference, omit basic steps, include edge cases and caveats

---

## Progressive Complexity

### Start Simple

- Begin every guide with the simplest possible example that works
- The reader's first experience should be success -- complexity comes after confidence
- Example: "Hello World" before authentication, single-resource CRUD before relationships

### Layer on Complexity

- After the simple case works, introduce one new concept at a time
- Each layer builds on the previous: simple --> parameters --> error handling --> advanced configuration
- Mark advanced sections clearly so beginners can skip them without confusion

### Do Not Front-Load Edge Cases

- Edge cases and caveats belong at the end of a section or in a dedicated "Advanced" subsection
- If an edge case is critical (data loss, security), place a warning at the relevant step -- but keep it brief
- Link to detailed edge case documentation rather than embedding it in the flow

---

## Getting Started Guide Pattern

### Structure

```
# Getting Started with [Product]

## Prerequisites
- [Software requirement with version]
- [Account or access requirement]
- [Knowledge prerequisite with link to learning resource]

## Installation
[Step-by-step installation with commands to copy/paste]

## Configuration
[Minimal configuration to get running -- do not cover all options here]

## Your First [Task]
[Walk through the most common initial task with expected output shown]

## Verification
[How to confirm everything is working correctly]

## Next Steps
- [Link to first how-to guide]
- [Link to core concepts explanation]
- [Link to full configuration reference]
```

### Rules

- Getting started must be completable in under 15 minutes
- Every command must be copy-paste ready
- Show expected output after every significant step
- Test on a clean environment before publishing -- no hidden dependencies
- Link to troubleshooting for common installation issues

---

## Screenshot and Diagram Conventions

### When to Include Screenshots

- UI that cannot be described adequately in text (complex layouts, visual configurations)
- Confirmation of expected state ("you should see a screen like this")
- Infrequently -- screenshots go stale faster than text

### When NOT to Include Screenshots

- Simple form fields that can be described in text
- Terminal output (use code blocks instead)
- Content that changes frequently (dashboard layouts, menu structures)

### Annotation Standards

- Use numbered callouts or arrows to draw attention to specific areas
- Include alt text for accessibility
- Crop screenshots to show only the relevant area -- full-screen screenshots are overwhelming
- Use consistent screenshot dimensions and styling across the documentation

### Diagram Guidelines

- Use text-based diagram tools (Mermaid, PlantUML) for version-controllable diagrams
- Keep diagrams simple: 5-7 elements maximum per diagram
- Label every element and connection
- Include a caption explaining what the diagram shows
- Use consistent visual language: boxes for services, arrows for data flow, cylinders for databases

### Maintainability

- Record how screenshots were captured (browser, resolution, test data) so they can be recreated
- Tag screenshots with the product version they depict
- Review screenshots when the product UI changes -- schedule review with each major release

---

## Voice and Tone

### Core Principles

- **Second person** -- Address the reader as "you": "You configure the pipeline by editing..."
- **Active voice** -- "The system sends a notification" not "A notification is sent by the system"
- **Present tense** -- "The command creates a new directory" not "The command will create a new directory"
- **Concise** -- Remove words that do not add meaning. "In order to" becomes "To". "It is necessary to" becomes "You must".

### What to Avoid

- Jargon without definition -- define technical terms on first use or link to a glossary
- Hedging language -- "You might want to consider" becomes "Consider" or "We recommend"
- Humor and colloquialisms -- they do not translate across cultures and become stale
- Marketing language -- documentation is not a sales pitch; state facts, not superlatives

### Addressing the Reader

- "You" for the reader: "You can configure this in the settings panel"
- "We" sparingly, for the product team: "We recommend using environment variables for secrets"
- Avoid "I" -- documentation is not personal narrative
- Avoid passive voice that obscures who performs the action

---

## Troubleshooting Guide Pattern

### Structure: Symptom, Cause, Solution

```
## Troubleshooting: [Feature/Area]

### [Symptom: what the user observes]

**Cause:** [Why this happens]

**Solution:**
1. [Step to diagnose or confirm]
2. [Step to resolve]
3. [Step to verify the fix]

**If this does not resolve the issue:** [Escalation path or next troubleshooting step]
```

### Guidelines

- Organize by symptom, not by cause -- users know what they see, not why it happens
- Include exact error messages -- users search for the error message they received
- Provide the diagnostic step first -- confirm the cause before applying the fix
- End with verification -- how does the user know the problem is solved?
- Include an escalation path -- what to do if the documented solution does not work

---

## Content Organization

### Table of Contents

- Include a table of contents for any document longer than 3 sections
- Use descriptive heading text -- "Configuring Database Connections" not "Configuration"
- Nest headings logically: H2 for major sections, H3 for subsections, H4 only when necessary
- Do not skip heading levels (H2 directly to H4)

### Cross-References

- Link to related documents inline where they are relevant: "For authentication details, see [Authentication Guide](link)"
- Do not force the reader to leave the page for critical information -- include what they need, link for depth
- Use relative links within the documentation set for portability
- Check links regularly -- broken links undermine trust

### Search Optimization

- Use descriptive, keyword-rich headings that match what users search for
- Include common synonyms and alternate phrasings in the text
- Place the most important information at the top of the page
- Use front matter or metadata tags if the documentation platform supports search indexing
