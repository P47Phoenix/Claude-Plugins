# Team Topology Decomposition

Decompose systems by team cognitive load and communication patterns. Based on Team Topologies by Matthew Skelton and Manuel Pais.

## Core Principle: Inverse Conway's Law

Conway's Law: "Organizations produce system designs that mirror their communication structures."

Inverse Conway: DESIGN your team structure to produce the system architecture you want. If you want independent microservices, create independent teams.

## Four Team Types

### Stream-Aligned Team

- **Purpose**: Deliver value directly to a user or business capability
- **Owns**: One or more bounded contexts end-to-end (design -> build -> deploy -> operate)
- **Size**: 5-9 people (two-pizza team)
- **Examples**: Shopping Cart team, Checkout team, Player Experience team
- **Goal**: Fast flow of change from idea to production
- **Key metric**: Lead time (how fast do changes reach users?)

### Enabling Team

- **Purpose**: Help stream-aligned teams adopt new capabilities
- **Owns**: Nothing permanently -- enables then moves on
- **Examples**: DevOps enablement, accessibility team, cloud migration team
- **Interaction**: Facilitating (temporary, time-boxed)
- **Goal**: Increase stream-aligned team capability, then dissolve or move to next team
- **Anti-pattern**: Becoming a permanent dependency (ticket-based service)

### Complicated-Subsystem Team

- **Purpose**: Own a technically complex component that requires specialist knowledge
- **Owns**: One component with high cognitive load (ML model, video processing, custom database)
- **Examples**: Search algorithm team, rendering engine team, compliance engine team
- **Interaction**: X-as-a-Service (provide API, hide complexity)
- **Goal**: Reduce cognitive load on stream-aligned teams
- **When to create**: Multiple stream-aligned teams need the same complex capability

### Platform Team

- **Purpose**: Provide internal self-service capabilities to stream-aligned teams
- **Owns**: Internal platform (CI/CD, infrastructure, observability, common services)
- **Examples**: Cloud platform team, developer experience team, data platform team
- **Interaction**: X-as-a-Service (self-service, API-driven, documentation)
- **Goal**: Thinnest viable platform -- provide just enough to enable stream-aligned teams
- **Anti-pattern**: Building more platform than teams need

## Three Interaction Modes

| Mode | Description | Duration | Example |
|------|------------|----------|---------|
| **Collaboration** | Two teams work closely together on a shared goal | Temporary (weeks-months) | Stream-aligned + Enabling during adoption |
| **X-as-a-Service** | One team provides a service, the other consumes it via API | Ongoing | Platform provides CI/CD to stream-aligned teams |
| **Facilitating** | One team coaches another to build new capability | Temporary (weeks) | Enabling team teaches testing practices |

### Rules

- Stream-aligned teams should NOT collaborate with more than one other team at a time
- Collaboration mode is expensive -- use sparingly, time-box it
- X-as-a-Service should require no coordination -- self-service with good docs

## Cognitive Load as Design Constraint

### Three Types of Cognitive Load

1. **Intrinsic**: the inherent complexity of the domain (can't reduce, must manage)
2. **Extraneous**: accidental complexity from tooling, process, bad APIs (reduce aggressively)
3. **Germane**: learning and creative problem-solving (maximize this)

### Team Capacity Heuristic

- A team can handle approximately 2-3 bounded contexts
- If a team owns more -> split the team or merge contexts
- If a team struggles with their scope -> reduce extraneous load first (better tooling, simpler processes)

### Cognitive Load Assessment

For each team, evaluate:

| Load Source | Rating (1-5) | Mitigation |
|-------------|-------------|-----------|
| Number of services owned | | Reduce scope or split team |
| Cross-team dependencies | | Move to X-as-a-Service |
| Manual operational toil | | Automate via platform team |
| Technology diversity | | Standardize where possible |
| Domain complexity | | Invest in domain knowledge |

If total exceeds team capacity, something must give. The answer is never "work harder."

## When to Split a Team/Service

- Team owns too many bounded contexts (cognitive load too high)
- Team has too many communication channels with other teams
- Different parts of the team's scope change at different rates
- Different parts require different deployment cadences

## When to Merge

- Two teams have tight coupling (constant collaboration mode)
- One team's service is too thin (overhead > value)
- Communication overhead between teams exceeds benefit of independence

## Thinnest Viable Platform

- Don't build a platform until 3+ stream-aligned teams need the same thing
- Platform should be self-service: no tickets, no waiting, just APIs and docs
- Measure platform value by: how much faster are stream-aligned teams?
- Kill platform features that aren't used
- Start with documentation and scripts before building tooling

## Team-Service Mapping

- One stream-aligned team = one or more services that team owns completely
- Services should match team cognitive capacity (not arbitrary technical boundaries)
- If two services are always deployed together -> consider merging
- If one service has two independent release cycles -> consider splitting

### Ownership Principles

- Every service has exactly one owning team
- The owning team decides the API, release cadence, and technology
- Other teams consume via published API -- they do not modify the service
- If no team wants to own a service, it belongs on the platform or should be retired

## Comparison with Other Strategies

| Aspect | Team Topology | DDD | Volatility |
|--------|--------------|-----|-----------|
| Decompose by | Team cognitive load | Domain boundaries | Axes of change |
| Key constraint | Team size (5-9) | Ubiquitous language | Interface stability |
| Best for | Scaling organizations | Complex domains | High change rate |

## Anti-Patterns

- **Siloed platform team** that creates bottlenecks instead of enabling self-service
- **Permanent enabling team** that becomes a dependency rather than building capability
- **Too many team types** -- most teams should be stream-aligned (aim for 6:1 ratio or higher)
- **Ignoring cognitive load** -- piling more services on a team until they can't cope
- **Tooling-first platform** -- building what's fun, not what teams need
- **Matrix ownership** -- a service owned by "everyone" is owned by no one
- **Reorg without architecture change** -- moving people around without changing the system produces the same system with different names
