# Simulated User Interviews: Presentation Skill

**Interviewer**: User Feedback Agent
**Date**: 2026-03-25
**Input**: Idea Brief (`01-idea-brief.md`), Brainstorm (`01a-brainstorm-ownership.md`)
**Method**: Simulated persona-based interviews (5 personas, 4 questions each)

---

## Persona 1: Sarah — Solo Indie Dev

**Background**: Bootcamp grad, working on side projects alone. Uses Claude-Plugins to stay organized. Reports monthly to a mentor/advisor. Has never heard of Marp.

---

**Q1: How do you currently create presentations from your delivery work?**

> Honestly? I don't. When I meet with my mentor I just screen-share my terminal or pull up the PRD in a browser tab and walk through it. Sometimes I'll make a quick Google Slides deck the night before, but it's basically me copying and pasting bullet points from my notes. It takes like two hours and the result is ugly. Most months I just skip the deck and talk through things off the cuff, which my mentor has told me is not great for my communication skills.

**Q2: What types of presentations do you need most often?**

> Progress updates, for sure. "Here's what I built this month, here's what's next, here's where I'm stuck." It's not a sprint review in the formal sense — more like a show-and-tell. Sometimes my mentor asks me to present my architecture decisions so she can poke holes in them. That's closer to a technical deep-dive but way less formal than what an enterprise team would need.

**Q3: What would make you actually use an AI-generated presentation skill vs doing it yourself?**

> If it just worked without me installing stuff. I barely got Claude-Plugins set up in the first place. If the skill tells me "install marp-cli" as a first step, I'm going to close the terminal and go back to Google Slides. The fallback markdown option sounds fine to me — if it gives me a clean outline with slide breaks that I can paste into Google Slides or Canva, that's already 10x better than what I do now. Also, I'd want it to use simple language. I'm not presenting to a board of directors. If the generated slides are full of enterprise jargon I'll have to rewrite every slide anyway.

**Q4: What's the minimum output quality that would make this useful to you?**

> If it pulls the right content from my delivery artifacts and organizes it into a logical flow — intro, what I did, what I learned, what's next — that's enough. I don't need animations or fancy themes. I need it to save me the two hours of copy-pasting and reorganizing. Even structured markdown with clear sections would be useful. The bar is "better than what I'd make in two hours on my own," which is low.

---

## Persona 2: Marcus — Enterprise Tech Lead

**Background**: Manages a team of 8 developers. Uses delivery-team for sprint planning. Presents sprint reviews to VP of Engineering biweekly. Corporate environment with strict branding guidelines and a mandatory company .pptx template.

---

**Q1: How do you currently create presentations from your delivery work?**

> We have a company PowerPoint template that every team is required to use. It has the logo, the color scheme, specific fonts — if you show up to a VP meeting without the branded template, you'll hear about it. So every two weeks I open the template, duplicate the slides from last sprint, update the numbers, swap out the feature descriptions, and add new screenshots. It takes about 90 minutes, and the worst part is pulling metrics from three different places — JIRA, our dashboards, and the delivery artifacts. The content is the hard part, not the formatting.

**Q2: What types of presentations do you need most often?**

> Sprint reviews, hands down. Every two weeks, non-negotiable. Beyond that, quarterly roadmap presentations for the VP and occasional technical deep-dives when we're proposing a major architectural change. The sprint reviews follow the same structure every time — sprint goal, what we committed, what we delivered, velocity trend, risks, next sprint. It's formulaic, which is exactly why it should be automated.

**Q3: What would make you actually use an AI-generated presentation skill vs doing it yourself?**

> Two things. First, it has to produce output that I can get into our corporate .pptx template. Marp markdown is fine as an intermediate step, but if the final deliverable isn't a .pptx that uses our template — or at least structured content I can paste into our template quickly — it doesn't solve my actual problem. The idea brief mentions python-pptx as a secondary path but seems to punt it to v2. That's a mistake for enterprise users. Second, the metrics need to be accurate. If the skill pulls sprint velocity from pipeline analytics, it has to match what I'd report manually. One wrong number in front of the VP and I'll never trust the tool again.

**Q4: What's the minimum output quality that would make this useful to you?**

> For me, structured content that maps 1:1 to my existing slide structure. If the skill gives me: slide 1 = sprint goal (text), slide 2 = committed vs delivered (table), slide 3 = feature highlights (bullets + descriptions), slide 4 = velocity chart data, slide 5 = risks and blockers, slide 6 = next sprint preview — and the content is accurate — I can paste that into the corporate template in 15 minutes instead of spending 90 minutes assembling it from scratch. That's the value. I don't need it to produce a beautiful finished deck. I need it to produce accurate, well-structured content in the right order.

---

## Persona 3: Priya — Startup CTO

**Background**: 3-person founding team. Uses delivery-flow for rapid feature delivery. Needs pitch decks for investors and product demos for early customers. Speed matters more than polish.

---

**Q1: How do you currently create presentations from your delivery work?**

> We use a shared Notion doc as our "deck" for most things. When we need a real pitch deck for investors, my co-founder who has a design background makes one in Figma. But that takes her 2-3 days because she's also doing product design work. For customer demos, we just do live walkthroughs — no slides at all. The problem is investor meetings come up on short notice. We got a warm intro last month and had 48 hours to prepare a deck. We ended up pulling an all-nighter because we had to extract product progress from our delivery artifacts, write the narrative, and design the slides all at once.

**Q2: What types of presentations do you need most often?**

> Investor pitch decks and product demos, in that order. The pitch deck needs to tell a story: problem, solution, traction, team, ask. The product demo needs to show what the product actually does, with screenshots or user flow descriptions. We also need occasional customer-facing "what's coming next" roadmap slides. We don't do sprint reviews — with 3 people, we just talk to each other.

**Q3: What would make you actually use an AI-generated presentation skill vs doing it yourself?**

> Speed. If I can go from "we have an investor meeting Thursday" to "here's a first draft pitch deck" in 10 minutes by pointing the skill at our delivery artifacts, that's game-changing. I don't need it to be investor-ready out of the box — I need a solid first draft that captures our actual product progress and frames it in investor language. My co-founder can polish the design. What I can't afford is the 4 hours of content assembly. Also — the skill needs to handle the fact that startups iterate fast. Our PRD from two weeks ago might be half-obsolete. The skill should pull from the latest pipeline state, not stale artifacts.

**Q4: What's the minimum output quality that would make this useful to you?**

> A coherent narrative arc with accurate product information. If the pitch deck correctly describes what we've built, what our metrics look like, and what we're building next — even in plain markdown with no design — that's a 4-hour time savings. I can make it pretty later. What I can't have is the skill hallucinating features we haven't built or metrics we haven't hit. Accuracy of claims is everything when you're talking to investors. If it says "launched feature X to 500 users" and we only have 200, that's a credibility disaster.

---

## Persona 4: Jake — Game Dev Studio Lead

**Background**: Uses GAME_DEV pipeline for Godot projects. Presents game design docs and technical deep-dives to a publisher. Runs weekly sprint reviews with a small team. Wants visual-heavy presentations with screenshots and GIFs.

---

**Q1: How do you currently create presentations from your delivery work?**

> Publisher meetings are a pain. I take screenshots from the Godot editor, screen-record GIF clips of gameplay, dump them into Google Slides, and write bullet points around them. For design doc presentations, I basically read the GDD out loud with slides that have key diagrams. The visual stuff is critical — publishers want to SEE the game, not read about it. Sprint reviews for the team are more casual; I just share my screen and walk through the Trello board and the latest build. No slides needed there.

**Q2: What types of presentations do you need most often?**

> Publisher milestone presentations — "here's what we built this milestone, here's a gameplay video, here's the next milestone plan." Those happen monthly. Also, technical deep-dives when we're proposing a risky architecture change (like switching from GDScript to C# for performance-critical systems). And game design doc walkthroughs when onboarding a new team member or pitching a new game concept.

**Q3: What would make you actually use an AI-generated presentation skill vs doing it yourself?**

> Image and media support is non-negotiable. If the skill can't reference screenshots, embed image paths, or leave placeholders where I should insert GIFs, it's useless for game dev presentations. Text-only slides don't work in our world. Beyond that, I'd want it to understand game dev vocabulary — "sprint" in game dev is often "milestone," "features" are often "mechanics" or "systems," UAT is "playtesting." If it generates slides that sound like enterprise software reviews, the publisher will think we don't know what we're doing. Also, Mermaid diagrams for system architecture would be huge — we draw a lot of node graphs, signal flow diagrams, scene trees. If those can be auto-generated from our architecture docs, that alone would sell me.

**Q4: What's the minimum output quality that would make this useful to you?**

> A slide outline with the right structure for a publisher meeting — milestone recap, visual showcase section with image placeholders, technical highlights, next milestone roadmap — plus accurate content pulled from our delivery artifacts. If it gives me that structure with `![screenshot](path/to/screenshot.png)` placeholders in the right places and I just have to drop in the actual images, that saves me an hour per presentation. The Mermaid diagram integration for architecture slides would be a major bonus but not a blocker for v1.

---

## Persona 5: Chen — Consultant / Freelancer

**Background**: Uses delivery-team across 4-5 client repos simultaneously. Needs client-facing status reports and project handoff presentations. Every client has different branding, terminology, and reporting expectations.

---

**Q1: How do you currently create presentations from your delivery work?**

> Each client gets a different treatment. Client A wants a weekly email with bullet points — no slides. Client B wants a formal PowerPoint with their branded template every two weeks. Client C wants a Loom video walkthrough. Client D wants a PDF report. So I end up reformatting the same delivery information four different ways. The content assembly is the same — pull from artifacts, summarize progress, flag risks — but the output format varies wildly. Right now I spend about 5-6 hours per week just on client reporting across all engagements.

**Q2: What types of presentations do you need most often?**

> Status updates and project handoffs. Status updates are the bread and butter — every client wants to know what happened this week and what's next. Project handoffs are less frequent but much higher stakes — when I'm wrapping up an engagement, I need to leave the client's internal team with a comprehensive "here's the system, here's the architecture, here's what to watch out for" presentation. That's basically an onboarding deck from the idea brief. I also occasionally need a "project proposal" deck when pitching a new engagement to a prospective client, which is similar to the Feature Pitch type.

**Q3: What would make you actually use an AI-generated presentation skill vs doing it yourself?**

> Multi-project support is the big one. I work across 4-5 repos. The skill needs to generate a presentation from the artifacts in THIS repo, not mix in context from other projects. If it pulls the right artifacts from the right `.delivery/` directory, that's already a win. Beyond that, I need output format flexibility. Marp-to-PDF for one client, structured markdown I can email for another, content I can paste into a client's branded template for a third. The idea brief mentions Marp as primary and structured markdown as fallback, but for me these aren't fallback scenarios — they're both primary depending on the client. I'd also need to set a client-facing tone. My delivery artifacts use internal team language ("blocker," "spike," "DoD"), but client presentations need translated language ("delay," "investigation," "acceptance criteria met").

**Q4: What's the minimum output quality that would make this useful to you?**

> Accurate content in a clean structure, with enough flexibility that I can adapt it to each client's expectations in under 15 minutes. If the skill generates a status update that correctly summarizes this sprint's delivery work, flags the right risks, and presents next steps — and I can get that into whatever format the client needs quickly — it would cut my weekly reporting time from 5-6 hours to maybe 2. The key word is "accurate." I bill by the hour. If a status report has wrong information and the client catches it, that's a trust problem that costs me the engagement.

---

## Synthesis

### Common Themes Across All 5 Personas

1. **Accuracy is the top concern, universally.** Every persona — from Sarah's mentor meetings to Chen's client reports — said the same thing: if the content is wrong, the tool is worse than useless. Marcus won't trust it after one bad number. Priya can't risk hallucinated metrics with investors. Chen could lose a client. Accuracy of extracted information is the single most important quality attribute.

2. **Content assembly is the real pain point, not slide design.** Nobody is asking for beautiful slides. They all spend the bulk of their time pulling information from multiple sources and organizing it into a coherent flow. The skill's value proposition is "accurate content extraction + logical structure," not "pretty output."

3. **Structured markdown is not a fallback — it is a primary output for most users.** Sarah doesn't know Marp. Marcus needs content for a corporate template. Chen needs content he can paste into multiple formats. Jake needs image placeholders. Only Priya (who'd take any format for speed) and Jake (who'd benefit from Marp + Mermaid) would use Marp natively. The idea brief positions structured markdown as a degraded fallback. For most users, it is the primary useful output.

4. **Tone and vocabulary adaptation matters.** Jake needs game dev language, not enterprise jargon. Chen needs client-facing language, not internal team language. Sarah needs simple language. Marcus needs executive-appropriate language. The presentation type determines structure, but the audience determines language. The idea brief does not address tone/vocabulary adaptation.

5. **Speed of generation matters more than output polish.** Priya needs a draft in 10 minutes. Marcus wants to cut 90 minutes to 15. Chen wants to cut 5-6 hours/week to 2. Sarah wants to save 2 hours. The value is measured in time saved on content assembly, not in output beauty.

### Surprising Insights

1. **The "Marp as primary" decision may be inverted.** The idea brief treats Marp as the primary format and structured markdown as the fallback. But 4 of 5 personas would use structured markdown as their primary output — either because they don't know Marp (Sarah), need corporate templates (Marcus), need format flexibility (Chen), or need image-heavy slides that require manual assembly anyway (Jake). Marp is a power-user format, not a default format.

2. **Project handoff / onboarding presentations are higher-value than expected.** Chen described handoff decks as "high stakes" — they are the lasting artifact of an entire engagement. The idea brief lists Onboarding as one of 8 types but does not call out its importance. For consultants and freelancers, the handoff deck may be the single most valuable presentation type.

3. **Multi-project isolation is a real concern.** Chen's scenario (4-5 client repos) reveals a requirement the idea brief does not address: the skill must be scoped to the current repo's `.delivery/` directory and must not leak context across projects. This is architecturally straightforward but needs an explicit guardrail.

4. **Game dev vocabulary divergence is significant.** Jake's point about "sprint vs milestone," "features vs mechanics," "UAT vs playtesting" suggests the skill needs a vocabulary layer, not just template variations. The GAME_DEV project type already exists in the pipeline — the presentation skill should detect it and adapt terminology.

5. **No one mentioned speaker notes unprompted.** The idea brief lists speaker notes as an open question. None of the 5 personas mentioned them. This suggests speaker notes are a nice-to-have, not a priority for v1. Sarah and Priya would likely ignore them. Marcus and Chen might use them. Jake would benefit most (publisher meeting talking points).

### Requirements the Idea Brief Missed

| # | Requirement | Source Persona | Priority |
|---|-------------|---------------|----------|
| 1 | **Tone/vocabulary adaptation by audience type** (executive, technical, investor, client-facing, casual) | All 5, especially Jake and Chen | High |
| 2 | **Structured markdown as a co-primary format**, not a fallback | Sarah, Marcus, Chen | High |
| 3 | **Image/media placeholder support** (`![](path)` syntax with instructions for manual insertion) | Jake | Medium |
| 4 | **Client-facing language translation** (internal team jargon to external-appropriate language) | Chen | Medium |
| 5 | **GAME_DEV vocabulary adaptation** (milestone, mechanics, playtesting, etc.) | Jake | Medium |
| 6 | **Multi-project isolation guardrail** (never pull artifacts from outside current repo) | Chen | Medium |
| 7 | **Explicit "content for pasting into existing template" output mode** (no Marp frontmatter, just structured content with clear slide boundaries) | Marcus, Chen | High |
| 8 | **Staleness warning** (flag when source artifacts are older than N days) | Priya | Low |
| 9 | **Project proposal / pitch type** (distinct from Feature Pitch — oriented toward selling services, not features) | Chen | Low |

### Priority Adjustments

**Increase priority:**
- **Structured markdown output quality.** The idea brief invests heavily in Marp templates and treats markdown as a fallback. The interviews suggest the reverse: invest in making structured markdown output excellent (clear slide boundaries, content-paste-ready, no tooling dependency), and treat Marp as an enhancement for users who have it installed.
- **Content accuracy validation.** Add a "source citation" mechanism — every slide should reference which artifact(s) it drew from, so users can verify claims before presenting. This was the number one concern across all personas.
- **Tone adaptation.** Add an `audience` parameter (or auto-detect from presentation type) that adjusts vocabulary and formality level. This is not cosmetic — wrong tone actively undermines the presentation for Jake (publisher meetings) and Chen (client reports).

**Decrease priority:**
- **Speaker notes.** Defer to v1.1 or make opt-in. No persona requested them.
- **Mermaid diagram deep integration.** Jake mentioned it as a bonus, not a requirement. Worth including if easy, but not a v1 blocker.
- **python-pptx generation.** Marcus needs corporate template compliance, but he'd be satisfied with paste-ready structured content as a v1 solution. Full python-pptx scripting can remain a v2 item.

**Keep as-is:**
- **8 presentation types.** All 8 mapped to at least one persona's needs. No type was unused.
- **Standalone skill (Model A).** No interview revealed a reason to reconsider the ownership decision.
- **Pipeline integration points.** The opt-in invocation at checkpoints matches how all personas would use it (on-demand, not automatic).

### Risks Confirmed or Newly Discovered

| Risk | Status | Evidence |
|------|--------|----------|
| Marp not installed on user system | **Confirmed and amplified** — most users would not install it | Sarah doesn't know what it is; Marcus needs .pptx; Chen needs format flexibility |
| Stale artifact content | **Confirmed** | Priya explicitly flagged fast iteration invalidating PRDs |
| Corporate template compliance | **Confirmed but deprioritized for v1** | Marcus would accept paste-ready content as interim solution |
| Scope creep into visual design | **Confirmed as non-risk** — no persona wants visual design | Every persona said content and structure matter, not aesthetics |
| **NEW: Accuracy/hallucination risk** | **Critical** — not in idea brief risk table | All 5 personas flagged wrong information as a trust-destroying event |
| **NEW: Vocabulary mismatch risk** | **Medium** — enterprise jargon in game dev or casual contexts | Jake and Sarah both flagged language mismatch as a usability problem |
| **NEW: Cross-project context leakage** | **Medium** — multi-repo users could get mixed content | Chen's multi-client scenario requires strict repo-scoping |

---

## Recommendation for PRD

The interviews confirm the core value proposition: extracting and structuring delivery artifacts into presentation-ready content. The biggest adjustment is **reframing structured markdown from fallback to co-primary output format** and adding **tone/vocabulary adaptation** as a first-class feature. The accuracy concern should drive a **source citation mechanism** (every slide cites its source artifact) that was not in the original idea brief.

The skill should ship with these priorities:
1. Accurate content extraction from pipeline artifacts (table stakes)
2. Logical narrative structure per presentation type (core value)
3. Structured markdown output that is paste-ready for any slide tool (primary format)
4. Tone adaptation by audience type (differentiator)
5. Marp-enhanced output when tooling is available (power-user enhancement)
6. Source citations on every slide for verification (trust mechanism)
