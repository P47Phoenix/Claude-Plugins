# Strategic Domain-Driven Design

Strategic DDD for system decomposition following Eric Evans' and Martin Fowler's process. DDD is iterative and model-driven — understanding the domain deeply BEFORE making architectural decisions.

This reference covers: knowledge crunching, model exploration, ubiquitous language, bounded context discovery, subdomain classification, and context mapping. For tactical patterns within a bounded context (aggregates, entities, value objects, repositories), see architecture-patterns.md.

## The DDD Process (Evans/Fowler)

DDD is NOT a classification exercise. It is an iterative modeling process where deep domain understanding drives architectural decisions. The sequence matters:

1. **Knowledge Crunching** — understand the domain deeply through collaboration
2. **Model Exploration** — sketch, challenge, and refine domain models iteratively
3. **Ubiquitous Language** — discover the precise language of the domain
4. **Bounded Context Identification** — find where the language and model change
5. **Subdomain Classification** — classify AFTER understanding (not before)
6. **Context Mapping** — map relationships between contexts

Jumping to step 5 or 6 without doing 1-4 produces shallow architectures that don't survive contact with the real domain.

---

## Phase 1: Knowledge Crunching

The foundation of DDD. Domain experts and developers collaborate to build shared understanding.

### What Knowledge Crunching Is

- Domain experts explain the business in their own words
- Developers listen, ask questions, and build mental models
- Both sides iterate until they share a common understanding
- The goal is NOT documentation — it's shared understanding

### How to Crunch Knowledge

1. **Start with stories**: "Tell me about how [process] works. What happens?"
2. **Follow the chain**: "And then what happens? Who does that? What do they need to know?"
3. **Ask for exceptions**: "What goes wrong? What's the weird case?"
4. **Challenge assumptions**: "Why is it done that way? Has it always been that way?"
5. **Sketch as you go**: draw rough models on paper/whiteboard — entities, relationships, flows
6. **Check understanding**: "So if I understand correctly, [restate in your own words]..."

### Output

- Rough domain model sketches (NOT final architecture — these will change)
- List of key domain concepts with expert-validated definitions
- Identified areas of complexity ("this is where the real business logic lives")
- Areas of confusion ("we don't fully understand this yet" — flag for deeper exploration)

### Key Principle

> "The model is not the diagram. The model is the shared understanding in people's heads. The diagram is just a communication tool." — Eric Evans

---

## Phase 2: Model Exploration Whirlpool

Evans' Model Exploration Whirlpool — rapid iterative cycles of modeling and validation.

### The Whirlpool Process

Each cycle (15-30 minutes):

1. **Scenario**: Pick a concrete business scenario ("Customer places an order with a discount code")
2. **Sketch**: Draw the domain model that handles this scenario (entities, value objects, relationships)
3. **Walkthrough**: Trace the scenario through the model step by step
4. **Challenge**: "What happens if [edge case]? Does the model handle it?"
5. **Refine or restart**: If the model handles it — refine. If not — discard and try a different model.

### Multiple Passes

- **Pass 1**: Core happy path — does the basic model work?
- **Pass 2**: Edge cases — does the model survive exceptions?
- **Pass 3**: Scale — does the model work with 10x the data/users?
- **Pass 4**: Cross-domain — does the model work when other parts of the business interact?

### Signals the Model Is Right

- Domain experts say "yes, that's exactly how it works"
- The model handles edge cases without special-case code
- The model makes predictions about the domain that turn out to be true
- New scenarios fit naturally without restructuring

### Signals the Model Is Wrong

- Domain experts say "well, sort of, but..." (model doesn't match reality)
- Edge cases require ugly workarounds or special cases
- The model can't explain why a business rule exists
- Developers struggle to name things clearly (naming difficulty = model confusion)

---

## Phase 3: Ubiquitous Language Discovery

The shared vocabulary between domain experts and developers within a bounded context. Language emerges from modeling — it is not a pre-defined glossary.

### How Language Emerges

- During knowledge crunching, domain experts use specific words
- Pay attention to: which words are precise, which are vague, which mean different things to different people
- When modeling, try using domain words for class names, method names, variable names
- If a name feels awkward in code → the model doesn't match the domain language → refine

### Language Boundary Detection

Watch for these signals that indicate a bounded context boundary:

- **Same word, different meaning**: "Account" means something different in billing vs authentication
- **Different words, same concept**: Sales says "deal", Support says "ticket", both mean a customer interaction
- **Awkward compound names**: "ShippingCustomer" vs "BillingCustomer" — if you need a prefix, you're crossing a boundary

### Language Rules

- Each bounded context has its OWN ubiquitous language
- Code MUST use domain language (no developer-invented names for domain concepts)
- When the language is ambiguous, the model is wrong — refine until precise
- Language is a living document — it evolves as understanding deepens

---

## Phase 4: Bounded Context Identification

Boundaries appear where the language and model change. This is discovered through Phases 1-3, not designed up-front.

### What Bounded Contexts ARE

- Areas where a particular model and language are internally consistent
- Inside a context: one model, one language, full consistency
- Across contexts: different models, different language, eventual consistency

### What Bounded Contexts ARE NOT

- NOT one per entity (Order context, Customer context — too granular)
- NOT one per database table (that's data decomposition, not domain decomposition)
- NOT one per team (teams may align with contexts, but the domain drives the boundary, not the org chart)
- NOT one per microservice (a microservice might implement one context, or a context might span multiple services initially)

### Discovery Process

1. Review the ubiquitous language from Phase 3
2. Identify where language meanings diverge
3. Identify where the model breaks (one model can't serve two interpretations)
4. Draw boundaries where language and model naturally separate
5. **Start broad**: fewer, larger contexts. Split only when complexity demands it.

### Boundary Heuristics

- If two concepts MUST be consistent in the same transaction → same context
- If they can be eventually consistent → candidate for different contexts
- If the same word means different things → definitely different contexts
- If teams work on different cadences → likely different contexts

---

## Phase 5: Subdomain Classification

NOW classify — after understanding the domain deeply through Phases 1-4.

| Subdomain | Definition | Investment Strategy | Build vs Buy |
|-----------|-----------|-------------------|--------------|
| **Core** | Competitive advantage — what makes the business unique | Invest heavily, best developers, deep modeling, custom build | Always build |
| **Supporting** | Necessary but not differentiating | Moderate investment, could outsource | Build or configurable platform |
| **Generic** | Commodity — everyone does it the same | Minimize investment | Buy, SaaS, open source |

### Classification Informs Investment

- **Core subdomains** deserve deep DDD modeling (full tactical patterns: aggregates, domain events, repositories)
- **Supporting subdomains** need adequate modeling (transaction scripts or simple CRUD may suffice)
- **Generic subdomains** need NO modeling — use off-the-shelf solutions

### Common Classification Mistakes

- Treating everything as core (over-investment in commodity capabilities)
- Treating core as generic (using off-the-shelf for your competitive advantage)
- Classification changing over time without updating investment (what was core 5 years ago may be generic now)

---

## Phase 6: Context Mapping

Map relationships between bounded contexts. The map reflects organizational and technical reality.

### Context Mapping Patterns

| Pattern | Relationship | When to Use |
|---------|-------------|-------------|
| **Shared Kernel** | Two contexts share a small subset of the model | Close collaboration, small well-defined overlap |
| **Customer-Supplier** | Upstream supplies to downstream | Clear dependency, upstream prioritizes downstream's needs |
| **Conformist** | Downstream adopts upstream's model as-is | No leverage over upstream (e.g., external API) |
| **Anti-Corruption Layer** | Downstream translates upstream's model | Incompatible models, need isolation from changes |
| **Open Host Service** | Upstream provides well-defined protocol | Multiple consumers, stable versioned API |
| **Published Language** | Shared standard for integration | Industry standards (EDI, HL7, FHIR, OpenAPI) |
| **Partnership** | Two contexts evolve together | Mutual dependency, coordinated releases |
| **Separate Ways** | No integration | Integration cost > benefit |

### Choosing a Pattern

- Same team, same release cycle → Shared Kernel or Partnership
- Different teams, cooperative → Customer-Supplier
- Different teams, external dependency → Conformist or Anti-Corruption Layer
- Many consumers → Open Host Service + Published Language
- No real dependency → Separate Ways

---

## Aggregate Boundary Design

Within a bounded context, aggregates define consistency boundaries:

- **Rule 1**: Aggregates are transactional boundaries — everything inside is strongly consistent
- **Rule 2**: Between aggregates, use eventual consistency (domain events)
- **Rule 3**: Reference other aggregates by ID, not by object reference
- **Rule 4**: Keep aggregates small — large aggregates create contention and merge conflicts
- **Rule 5**: One aggregate = one repository = one transaction

### Sizing Heuristic

- If two entities MUST be consistent in the same transaction → same aggregate
- If they can be eventually consistent → different aggregates
- If in doubt → separate (easier to merge later than to split)

---

## Domain Events as Integration

Between bounded contexts:

- Publish domain events when significant state changes occur
- Events are facts that happened — immutable, past tense ("OrderPlaced", "PaymentReceived")
- Other contexts subscribe and update their own models
- Anti-corruption layer translates incoming events into local domain language
- Eventual consistency is the norm between bounded contexts

### Event Schema Guidelines

- Include the aggregate ID that emitted the event
- Include a timestamp and correlation ID
- Include only data relevant to the event (not entire aggregate state)
- Version event schemas — consumers must handle old versions
- Events are contracts — treat schema changes as breaking changes

---

## When to Use Strategic DDD

- Complex domains with rich business logic
- Multiple teams working on the same system
- Enterprise systems with many integration points
- Evolving business models where understanding is still forming
- Systems where "the same word means different things to different people"

## When NOT to Use

- Simple CRUD applications (massive overhead for no benefit)
- Technical infrastructure (use volatility-based decomposition instead)
- Domains that are well-understood and stable (no modeling needed)
- Very small teams (1-2 people — overhead isn't justified)

---

## Common Mistakes

- **Skipping knowledge crunching**: jumping to context maps without understanding the domain
- **One context per entity**: bounded contexts are NOT database tables
- **Shared database across contexts**: creates hidden coupling, defeats encapsulation
- **Classification before understanding**: labeling subdomains without deep domain knowledge
- **Static context maps**: relationships evolve — revisit when integration pain appears
- **Developer-invented language**: code should use the domain experts' words, not developer jargon
- **Big-bang modeling**: trying to model the entire domain at once instead of iterating

---

## References

- Eric Evans, "Domain-Driven Design: Tackling Complexity in the Heart of Software" (Addison-Wesley, 2003)
- Martin Fowler, "BoundedContext" (martinfowler.com/bliki/BoundedContext.html)
- Martin Fowler, "UbiquitousLanguage" (martinfowler.com/bliki/UbiquitousLanguage.html)
- Vaughn Vernon, "Implementing Domain-Driven Design" (Addison-Wesley, 2013)
- Eric Evans, "Domain-Driven Design Reference" (free PDF, domainlanguage.com)
