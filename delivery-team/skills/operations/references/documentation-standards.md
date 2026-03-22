# Documentation Standards

## Style Guide

### Voice and Tone

- **Active voice** -- "The system processes the request" not "The request is processed by the system"
- **Present tense** -- "This command creates a file" not "This command will create a file"
- **Second person** -- "You configure the setting by..." not "The user configures the setting by..."
- **Direct and concise** -- Remove filler words. "In order to configure" becomes "To configure". "It is important to note that" becomes a direct statement.
- **Imperative mood for instructions** -- "Run the command" not "You should run the command"

### Sentence and Paragraph Structure

- **Short sentences** -- Aim for 15-20 words per sentence. Break long sentences into two.
- **One idea per paragraph** -- If a paragraph covers two topics, split it.
- **Front-load important information** -- The first sentence of a paragraph should state the main point. Details follow.
- **Use lists for three or more items** -- Inline lists ("A, B, and C") are harder to scan than bulleted lists.

### Terminology

- Use consistent terminology throughout all documentation -- do not alternate between synonyms (e.g., pick "user" or "customer" and use it everywhere)
- Define technical terms on first use or link to a glossary
- Prefer industry-standard terms over invented vocabulary
- Maintain a terminology reference listing preferred terms and their definitions

### Capitalization and Formatting

- Use sentence case for headings: "Configure the database connection" not "Configure the Database Connection"
- Capitalize proper nouns and product names exactly as the product does
- Use code formatting for: commands, file paths, variable names, configuration keys, error codes
- Use bold for UI element names: "Click **Save**"
- Use italics sparingly -- for emphasis or for introducing a term being defined

---

## Markdown Conventions

### Heading Hierarchy

- H1 (`#`) -- Document title only, one per document
- H2 (`##`) -- Major sections
- H3 (`###`) -- Subsections within a major section
- H4 (`####`) -- Use sparingly, only when H3 subsections need further division
- Never skip levels (H2 directly to H4)
- Headings should be descriptive: "Configure email notifications" not "Configuration"

### Code Blocks

- Use fenced code blocks with language identifiers for syntax highlighting
- Include the command prompt (`$`) for shell commands to distinguish input from output
- Show expected output after commands when it aids understanding
- For configuration files, include enough context to locate the section being modified
- Indicate placeholder values clearly: `YOUR_API_KEY`, `<project-name>`, `${VARIABLE}`

### Tables

- Use tables for structured data with consistent columns
- Include a header row with descriptive column names
- Align columns for readability in the source (not required, but helpful for reviewers)
- If a table has more than 6 columns, consider restructuring as a list or separate sections
- Keep cell content concise -- if a cell needs a paragraph, the data does not belong in a table

### Links

- Use descriptive link text: "[Authentication Guide](link)" not "[click here](link)"
- Use relative links within the documentation set for portability
- External links open in a new tab when the platform supports it
- Check all links before publishing and schedule regular link validation

### Admonitions

Use admonitions (notes, warnings, tips) to highlight important information:

- **Note** -- Additional context that is helpful but not critical
- **Warning** -- Information about potential data loss, security risks, or breaking changes
- **Tip** -- Suggestions for better practices or shortcuts
- Do not overuse admonitions -- if everything is highlighted, nothing stands out

---

## Information Architecture

### Content Types

| Type | Purpose | Structure | Example |
|------|---------|-----------|---------|
| **Tutorial** | Learning-oriented, hands-on | Step-by-step, progressive | "Getting Started with Widgets" |
| **How-To** | Task-oriented, solve a problem | Prerequisites, steps, verification | "How to configure email alerts" |
| **Reference** | Information-oriented, lookup | Tables, lists, schemas | "API endpoint reference" |
| **Explanation** | Understanding-oriented, concepts | Prose, diagrams, examples | "How authentication works" |
| **FAQ** | Common questions and answers | Q&A format | "Frequently asked questions" |
| **Changelog** | Record of changes | Version, date, categorized changes | "Changelog" |
| **ADR** | Architecture decisions | Context, decision, consequences | "ADR-001: Use PostgreSQL" |

### Navigation

- Top-level navigation reflects the primary user journeys: Getting Started, Guides, API Reference, Troubleshooting
- Sidebar navigation shows the full content hierarchy within each section
- Breadcrumbs show the reader where they are in the hierarchy
- Search is available on every page
- "Next" and "Previous" links at the bottom of sequential content (tutorials, guides)

### Search

- Ensure all content is indexed by the documentation platform's search
- Use front matter or metadata for improved search ranking
- Include common search terms and synonyms in the content
- Test search regularly by searching for terms you expect users to use

### Cross-References

- Link related content inline: "For more details, see [Authentication](link)"
- Include a "Related" or "See Also" section at the end of documents when there are multiple related pages
- Do not force the reader to leave the current page for critical information -- include the essential point and link for depth
- Maintain a dependency map: know which documents reference each other so updates can be propagated

---

## Content Types Taxonomy

### Tutorial

- Purpose: Teach the reader a new skill through a complete, working project
- Audience: Beginners to the topic
- Length: 15-45 minutes to complete
- Structure: Introduction, prerequisites, numbered steps, conclusion, next steps
- Maintenance: Update with every major version change

### How-To Guide

- Purpose: Help the reader accomplish a specific task
- Audience: Users who already know the basics
- Length: 5-15 minutes to complete
- Structure: Goal statement, prerequisites, numbered steps, verification
- Maintenance: Update when the procedure changes

### Reference

- Purpose: Provide complete, accurate technical information for lookup
- Audience: Users who know what they are looking for
- Length: Varies -- must be complete
- Structure: Consistent format per entry (parameters table, return values, examples)
- Maintenance: Update with every API or configuration change

### Explanation

- Purpose: Provide understanding and context
- Audience: Users who want to understand concepts
- Length: 5-15 minutes to read
- Structure: Prose with diagrams, can be conversational
- Maintenance: Update when the underlying design changes

### FAQ

- Purpose: Answer common questions quickly
- Audience: All users
- Length: 2-3 sentences per answer, with links to detailed docs
- Structure: Q&A pairs, grouped by topic
- Maintenance: Review quarterly, add questions from support channels

### Changelog

- Purpose: Record what changed in each release
- Audience: Existing users upgrading between versions
- Structure: Version heading, date, categorized entries (Added, Changed, Fixed, Removed, Security)
- Format: Follow the Keep a Changelog convention (keepachangelog.com)
- Maintenance: Updated with every release

### ADR (Architecture Decision Record)

- Purpose: Capture the context and rationale for significant technical decisions
- Audience: Current and future team members
- Structure: Status, context, decision, consequences, alternatives
- Maintenance: Status updated when decisions are superseded; content is immutable

---

## Review Checklist

### Before Publishing

- [ ] **Accuracy** -- Technical content verified against the actual implementation
- [ ] **Completeness** -- All necessary steps, parameters, and options are documented
- [ ] **Clarity** -- A person unfamiliar with the topic can follow the document
- [ ] **Consistency** -- Terminology, formatting, and style match the style guide
- [ ] **Code examples tested** -- Every code snippet and command has been executed and verified
- [ ] **Links validated** -- All internal and external links resolve correctly
- [ ] **Formatting correct** -- Headings, lists, tables, and code blocks render properly
- [ ] **Audience appropriate** -- Content depth matches the stated audience level
- [ ] **No sensitive information** -- No API keys, passwords, internal URLs, or PII in examples
- [ ] **Spelling and grammar** -- Proofread for errors

### Review Process

1. Author writes the document following this style guide
2. Technical reviewer verifies accuracy against the implementation
3. Peer reviewer checks clarity, consistency, and style compliance
4. Final review by the documentation owner or lead
5. Publish and announce to the relevant audience

---

## Documentation-as-Code

### Docs in Repository

- Documentation lives in the same repository as the code it describes (or in a dedicated docs repository)
- Documentation changes go through the same pull request and review process as code changes
- Documentation is versioned alongside the code -- each release tag includes the matching documentation

### CI Checks

- Linting: check markdown formatting (markdownlint or equivalent)
- Link validation: check all links resolve (broken link checker in CI)
- Spell checking: automated spell check with custom dictionary for technical terms
- Build check: documentation builds without errors (for static site generators)
- Screenshot freshness: warn if screenshots are older than the latest UI change

### Preview Environments

- Pull requests that include documentation changes should deploy a preview
- Reviewers can see the rendered documentation before merging
- Preview environments use the same build process as production documentation
- Preview URLs are posted as PR comments for easy access

---

## Versioned Documentation

### Matching Docs to Product Versions

- Each major/minor version of the product has a corresponding documentation version
- Users can select their product version to see the matching documentation
- The default version shown is the latest stable release (not a pre-release)
- Archive older versions but keep them accessible -- users on older versions still need documentation

### Deprecation Notices

- When a feature is deprecated, add a deprecation notice at the top of its documentation
- Include: what is deprecated, what replaces it, when it will be removed, link to migration guide
- Remove deprecated documentation only after the feature is removed from the product
- Update all cross-references to deprecated content to point to the replacement

### Version Selector

- Documentation platform should provide a version selector visible on every page
- Clearly indicate which version the reader is currently viewing
- Link to the same page in other versions when possible
- Show a banner when the reader is viewing documentation for an older version

---

## Template Library

### Standard Templates

Maintain a template for each content type so authors start from a consistent structure:

- Tutorial template: title, introduction, prerequisites, steps, conclusion, next steps
- How-to template: title, goal, prerequisites, steps, verification, troubleshooting
- Reference template: title, description, parameters table, examples, related endpoints
- FAQ template: question, answer, related links
- Changelog template: version, date, categorized entries
- ADR template: status, date, context, decision, consequences, alternatives

### Template Usage Rules

- Authors start from the template -- do not create documents from scratch
- Templates define required sections -- authors may add sections but must not remove required ones
- Templates are maintained by the documentation lead and updated based on team feedback
- Template changes go through review to ensure consistency across existing and future documents
