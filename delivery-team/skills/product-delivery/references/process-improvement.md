# Process Improvement

Frameworks and techniques for continuous improvement of team and organizational
delivery practices. Improvement is a discipline, not an event.

---

## Kaizen: Continuous Small Improvements

Kaizen means "change for better." The philosophy: many small improvements compound
into transformational change. Large reorganizations are disruptive and often fail.

**PDCA Cycle (Deming Cycle):**
1. **Plan:** Identify a problem, analyze root causes, and design an experiment.
   Define what "better" looks like with a measurable target condition.
2. **Do:** Execute the experiment on a small scale. A single team, a single sprint,
   a single workflow. Do not roll out organization-wide before validating.
3. **Check:** Measure results against the target condition. Did the change produce
   the expected effect? Were there unintended consequences?
4. **Act:** If the experiment worked, standardize the new practice. If it failed,
   analyze why and design the next experiment. Either way, start the next cycle.

**Cadence:** Run PDCA continuously. Each sprint retrospective should produce at
least one small experiment. Track experiments on a visible improvement board.

---

## Value Stream Mapping

Visualizing the end-to-end flow of work to identify waste.

**Current state map:** Document every step from request to delivery. For each step:
process time, wait time, percent complete and accurate (%C&A), handoff mechanism.

**Waste categories (TIMWOODS):**
- **T**ransportation: unnecessary handoffs between teams or systems.
- **I**nventory: work sitting in queues (backlog bloat, PR review queues).
- **M**otion: context switching, searching for information, navigating tools.
- **W**aiting: blocked work, approval delays, environment provisioning.
- **O**ver-production: building features nobody uses, gold-plating.
- **O**ver-processing: excessive documentation, redundant reviews, unnecessary
  ceremony.
- **D**efects: bugs, rework, miscommunication requiring clarification.
- **S**kills underutilization: people doing work below their capability.

**Future state map:** Design the improved flow by eliminating or reducing identified
waste. Prioritize the largest wait-time reductions -- they typically dwarf process-
time improvements.

---

## Theory of Constraints (TOC)

A system can only move as fast as its slowest bottleneck.

**Five Focusing Steps:**
1. **Identify** the constraint. Where does work pile up? Where do people wait?
   Use cumulative flow diagrams and WIP visualization to find it.
2. **Exploit** the constraint. Maximize throughput at the bottleneck without adding
   resources. Remove distractions, automate repetitive tasks, ensure the bottleneck
   is never idle.
3. **Subordinate** everything else. Upstream processes should produce only what the
   bottleneck can consume. Flooding a bottleneck with more work increases WIP and
   lead time without increasing throughput.
4. **Elevate** the constraint. Add capacity: hire, train, invest in tooling, or
   restructure work to bypass the bottleneck.
5. **Repeat.** Once the constraint moves, start over. The new bottleneck is
   elsewhere.

**Common software bottlenecks:** Code review, QA, deployment pipeline, product
owner availability, environment provisioning, architecture review boards.

---

## Shu-Ha-Ri Maturity Model

A martial arts concept applied to team and practice maturity.

- **Shu (Follow):** The team follows practices as prescribed. Daily standups at
  9 AM, 15 minutes, three questions. Sprint planning uses planning poker. No
  deviations. This is appropriate for new teams or teams adopting new practices.
- **Ha (Break):** The team understands why practices exist and begins adapting them.
  Standups shift to walking the board. Planning uses right-sizing instead of
  estimation. The team modifies practices based on experience and context.
- **Ri (Transcend):** The team has internalized the principles behind the practices.
  They invent new practices that serve their unique context. Ceremonies may look
  nothing like textbook Scrum, but the underlying values are deeply embedded.

**Scrum Master role at each stage:** In Shu, teach and enforce. In Ha, coach and
question. In Ri, mentor and get out of the way.

---

## Team Topology Patterns

How teams are structured determines what they can deliver.

**Four fundamental team types:**
- **Stream-aligned:** Delivers value to a customer segment. Most teams. Owns a full
  product slice.
- **Enabling:** Helps stream-aligned teams overcome obstacles. Time-boxed, not
  permanent dependencies.
- **Complicated-subsystem:** Owns components requiring deep specialist knowledge.
  Only when specialization is genuinely complex.
- **Platform:** Self-service capabilities for stream-aligned teams. Reduces
  cognitive load.

**Interaction modes:** Collaboration (working together), X-as-a-Service (consuming
via API/tool), Facilitating (coaching). Minimize long-term collaboration; move
toward X-as-a-Service when interfaces stabilize.

---

## Agile Anti-Pattern Catalog

Recognizing dysfunction is the first step to addressing it.

**Zombie Scrum:** All ceremonies performed, nothing improves. Standups are status
reports. Retro actions never completed. Symptom: team cannot say what they learned.

**Waterfall in sprints:** Requirements, design, build, test in sequence within a
sprint. Symptom: testing only on the last day.

**Estimation theater:** Half-day debates over 5 vs 8 points. Symptom: estimation
meetings longer than the work itself.

**Sprint scope creep:** Work added mid-sprint without removing other work. Symptom:
burn-down goes up.

**Retrospective inaction:** Same issues identified sprint after sprint, never
resolved. Symptom: last sprint's retro notes read identically to this sprint's.

---

## Flow Optimization

Principles for improving the smooth movement of work through the system.

**Reduce batch size:** Smaller batches flow faster, provide earlier feedback, and
reduce risk.

**Limit WIP:** Per Little's Law, reducing WIP reduces lead time. Lower the limit
until discomfort, then raise by one. The discomfort reveals systemic issues.

**Manage queues:** Make queues visible. Measure wait times. Use pull signals.

**Reduce handoffs:** Each handoff loses ~50% of information and adds wait time.
Cross-functional teams keep all skills within the team.

---

## Improvement Kata

A structured practice for building improvement as a daily habit.

1. **Understand the direction:** What is the long-term challenge or vision?
2. **Grasp the current condition:** Measure with data, not assumptions. Go to the
   gemba (where work happens) and observe.
3. **Establish the next target condition:** A measurable state to reach in 1-4
   weeks. Not the final goal, just the next step.
4. **Experiment toward the target:** Identify one obstacle, design one experiment,
   predict the outcome, run it, compare actual to predicted, learn.

**Coaching kata:** Five daily questions: What is the target condition? What is the
actual condition? What obstacles exist? What is the next step? When can we learn?

---

## Measuring Improvement

Without measurement, improvement is just opinion.

**Before/after metrics:** Establish a baseline before changing anything. Measure
the same metric after the change. Use the same measurement method both times.

**Trend analysis:** Single data points are noise. Look for trends over 4-6 data
points minimum. Plot metrics on control charts to distinguish signal from noise.

**Statistical significance:** For small teams, formal statistical tests are often
impractical (sample sizes too small). Instead, look for consistent directional
change over multiple sprints and qualitative confirmation from the team.

**Leading indicators of improvement:** Team members volunteer for improvement work.
Action items from retros are completed within one sprint. The team self-identifies
problems before the Scrum Master does. Stakeholders report improved predictability.
