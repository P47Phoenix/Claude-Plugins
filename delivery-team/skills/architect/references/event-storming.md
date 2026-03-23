# Event Storming

Event-driven system decomposition through collaborative workshops. Discover domain events, derive bounded contexts, and design event-driven service topologies.

## Three Levels of Event Storming

### Big Picture Event Storming

- **Goal**: Discover all domain events across the entire business process
- **Participants**: Domain experts, developers, product owners, architects
- **Duration**: 2-4 hours
- **Output**: Timeline of domain events covering the full business workflow
- **Key rule**: No discussions about solutions -- only discover what happens in the domain

### Process-Level Event Storming

- **Goal**: Detail one bounded context's event flow
- **Participants**: Domain expert for that context + developers who'll build it
- **Duration**: 1-2 hours
- **Output**: Commands, events, policies, read models for one bounded context
- **Key rule**: Be precise about triggers, conditions, and outcomes

### Design-Level Event Storming

- **Goal**: Translate events into aggregates, commands, and policies for implementation
- **Participants**: Developers and architect
- **Duration**: 1-2 hours
- **Output**: Aggregate boundaries, command handlers, event handlers, read models
- **Key rule**: This is the bridge to code -- every element maps to an implementation artifact

## Notation (Sticky Note Colors)

| Color | Element | Definition | Example |
|-------|---------|-----------|---------|
| **Orange** | Domain Event | Something that happened (past tense) | OrderPlaced, PaymentReceived, ShipmentDispatched |
| **Blue** | Command | An action triggered by a user or system | PlaceOrder, ProcessPayment, DispatchShipment |
| **Yellow** | Actor / User | Who triggers the command | Customer, Admin, System (automated) |
| **Pink/Red** | Policy / Reaction | "When X happens, do Y" (automation rule) | "When PaymentReceived, then UpdateInventory" |
| **Lilac/Purple** | Read Model | Data view needed to make a decision | OrderSummary, InventoryLevel, CustomerProfile |
| **Red (large)** | Hot Spot | Problem, question, or disagreement | "What happens if payment fails mid-checkout?" |
| **Green** | Aggregate | Consistency boundary that handles commands and emits events | Order, Payment, Shipment |

## Event Storming Process

### Step 1: Chaotic Exploration (15 min)

- Everyone writes domain events on orange stickies
- No ordering, no filtering, no discussion
- Duplicate events are fine (shows importance)

### Step 2: Timeline Ordering (20 min)

- Arrange events on a timeline (left to right)
- Identify parallel flows
- Mark pivotal events (events that change the direction of the process)

### Step 3: Commands and Actors (20 min)

- For each event, identify: what command caused it? Who triggered the command?
- Blue stickies for commands, yellow for actors

### Step 4: Policies and Reactions (15 min)

- Identify automation: "When [event], then [command]"
- Pink stickies for policies
- These often reveal hidden business rules

### Step 5: Read Models (10 min)

- What data does the actor need to make the decision to trigger the command?
- Lilac stickies for read models

### Step 6: Bounded Context Discovery (15 min)

- Draw boundaries around clusters of events that share language and concepts
- Where the language changes -> bounded context boundary
- Events that cross boundaries -> integration events

### Step 7: Hot Spots (throughout)

- Red stickies for problems, questions, disagreements
- Don't resolve during the workshop -- capture for follow-up

## From Events to Service Boundaries

Events that cluster together by language and lifecycle form bounded contexts:

- Same ubiquitous language -> same context
- Same lifecycle (deploy together, change together) -> same context
- Different actors/teams -> different context
- Events at the boundary between clusters -> integration events (published via event bus)

## CQRS / Event Sourcing Topology

### Command Side (Write Model)

- Receives commands
- Validates against aggregate state
- Emits domain events
- Persists events (event store) not current state

### Query Side (Read Model)

- Subscribes to domain events
- Projects events into read-optimized views (denormalized)
- Serves queries without touching the write model
- Multiple read models for different query patterns

### When to Use CQRS

- Different read and write patterns (many reads, few writes or vice versa)
- Complex domain with rich business rules (write side) but simple displays (read side)
- Need for audit trail (event sourcing provides complete history)

### When NOT to Use

- Simple CRUD (massive overhead for no benefit)
- Small team (complexity cost > benefit)
- Synchronous consistency requirements (eventual consistency is inherent)

## Saga / Process Manager Patterns

For multi-service transactions (no distributed transactions):

### Choreography (event-driven)

- Each service listens for events and reacts
- No central coordinator
- Simple but hard to debug complex flows
- Best for: 2-3 services, simple flows

### Orchestration (command-driven)

- Central Process Manager sends commands to each service
- Knows the full workflow
- Easier to debug but single point of coordination
- Best for: 4+ services, complex flows with compensating transactions

### Compensating Transactions

- When a step fails, undo previous steps via compensating commands
- Example: PaymentFailed -> CancelOrder -> RestoreInventory
- Design every action with its compensation from the start

## Event-Driven Service Topology

| Pattern | Communication | Best For |
|---------|--------------|---------|
| **Pub/Sub** | Events broadcast to all subscribers | Decoupled services, multiple consumers |
| **Event Mesh** | Intelligent routing based on event type | Large systems with many event types |
| **Event Sourcing** | Events as source of truth, replay for state | Audit requirements, temporal queries |
| **Point-to-Point** | Direct event delivery to one consumer | Simple 1:1 integrations |

## When to Use Event Storming

- Complex workflows spanning multiple teams
- Systems with many integration points
- When the domain is poorly understood (discovery tool)
- When moving from monolith to services (identify boundaries)
- At project kickoff (align team understanding)

## Anti-Patterns

- **Events as commands**: "PleaseProcessPayment" is a command, not an event -- events are past tense facts
- **God aggregate**: one aggregate handling too many events (split it)
- **Missing compensating transactions**: happy path only, no failure handling
- **Over-eventing**: creating events for everything including trivial state changes
- **Synchronous event handling**: defeats the purpose of event-driven architecture
- **Skipping domain experts**: developers alone will model the solution, not the domain
