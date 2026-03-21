# Object-Oriented Programming Patterns

Language-agnostic OOP patterns for reference by any language that supports objects. Includes SOLID principles, GoF design patterns, and composition-over-inheritance guidelines.

Languages this guide applies to: **C#, C++, Java, TypeScript, Python (OOP style), Kotlin, Swift**.

---

## SOLID Principles

### S — Single Responsibility Principle (SRP)

A class should have **one reason to change**. Each class owns one concept; if you need to change two different behaviors, they belong in two different classes.

```csharp
// Violates SRP — Order handles persistence AND business logic
class Order {
    public void Save() { /* database */ }
    public decimal CalculateTax() { /* business rule */ }
}

// Correct — split responsibilities
class Order {
    public decimal CalculateTax() { ... }
}
class OrderRepository {
    public void Save(Order order) { ... }
}
```

### O — Open/Closed Principle (OCP)

Classes should be **open for extension, closed for modification**. Add new behavior by extending (subclass, interface implementation, composition), not by editing existing code.

```typescript
// Violates OCP — every new discount type requires modifying this class
class PriceCalculator {
    calculate(type: string, price: number): number {
        if (type === "seasonal") return price * 0.9;
        if (type === "loyalty") return price * 0.85;
        return price;
    }
}

// Correct — each discount is a separate implementation
interface DiscountStrategy {
    apply(price: number): number;
}
class SeasonalDiscount implements DiscountStrategy {
    apply(price: number) { return price * 0.9; }
}
class LoyaltyDiscount implements DiscountStrategy {
    apply(price: number) { return price * 0.85; }
}
```

### L — Liskov Substitution Principle (LSP)

A subclass must be substitutable for its base class without breaking correctness. If `Bird` has `fly()`, `Penguin extends Bird` violates LSP because penguins cannot fly. Fix by redesigning the hierarchy.

**Red flags:** subclass overrides a method to throw `NotImplementedException`, or adds preconditions stricter than the base.

### I — Interface Segregation Principle (ISP)

Clients should not depend on interfaces they don't use. Split fat interfaces into focused, cohesive ones.

```typescript
// Violates ISP — not all workers can eat
interface Worker {
    work(): void;
    eat(): void;  // robots don't eat
}

// Correct — segregated interfaces
interface Workable { work(): void; }
interface Eatable { eat(): void; }
class Human implements Workable, Eatable { ... }
class Robot implements Workable { ... }
```

### D — Dependency Inversion Principle (DIP)

High-level modules should not depend on low-level modules — both should depend on abstractions. Inject dependencies rather than constructing them internally.

```csharp
// Violates DIP — high-level class creates its own low-level dependency
class ReportService {
    private SqlReportRepository _repo = new SqlReportRepository(); // hard dependency
}

// Correct — depend on abstraction; inject the implementation
class ReportService {
    private readonly IReportRepository _repo;
    public ReportService(IReportRepository repo) { _repo = repo; }
}
```

---

## Composition Over Inheritance

Prefer composing behavior from small, focused objects rather than deep inheritance hierarchies. Inheritance creates tight coupling; composition keeps things replaceable.

```typescript
// Inheritance approach — fragile when behavior combinations explode
class FlyingSwimmingDuck extends SwimmingDuck { ... }

// Composition approach — behaviors are interchangeable
interface FlyBehavior { fly(): void; }
interface SwimBehavior { swim(): void; }

class Duck {
    constructor(
        private fly: FlyBehavior,
        private swim: SwimBehavior
    ) {}
}
const mallard = new Duck(new WingFly(), new DuckSwim());
const rubber = new Duck(new NoFly(), new DuckSwim());
```

**Rules:**
- Inherit for **is-a** relationships with shared behavior that is unlikely to vary
- Compose for **has-a** relationships and any behavior that may change at runtime
- Limit inheritance depth to 2–3 levels; beyond that, refactor to composition

---

## GoF Design Patterns

### Creational

#### Factory Method

Define an interface for creating objects; subclasses decide which class to instantiate.

```typescript
interface Logger { log(msg: string): void; }
class ConsoleLogger implements Logger { log(msg: string) { console.log(msg); } }
class FileLogger implements Logger { log(msg: string) { /* write to file */ } }

function createLogger(env: string): Logger {
    return env === "production" ? new FileLogger() : new ConsoleLogger();
}
```

Use when: the exact type to create is determined at runtime; callers should not know the concrete class.

#### Builder

Construct complex objects step-by-step. Avoids constructors with many parameters.

```csharp
var query = new QueryBuilder()
    .From("orders")
    .Where("status", "active")
    .OrderBy("created_at", descending: true)
    .Limit(50)
    .Build();
```

Use when: an object requires many optional parameters or must be assembled in steps.

#### Singleton

Ensure only one instance exists. Use sparingly — singletons make testing difficult.

```typescript
class AppConfig {
    private static _instance: AppConfig;
    private constructor() {}
    static get instance(): AppConfig {
        if (!AppConfig._instance) AppConfig._instance = new AppConfig();
        return AppConfig._instance;
    }
}
```

**Prefer dependency injection over singleton** for testability. Use singleton only for true global resources (logging, config).

---

### Structural

#### Adapter

Convert an interface into another interface that clients expect. Wraps an incompatible object.

```csharp
// Existing interface your code depends on
interface IPaymentGateway { void Charge(decimal amount); }

// Third-party library with incompatible interface
class StripeClient { public void ProcessPayment(int cents) { ... } }

// Adapter bridges the gap
class StripeAdapter : IPaymentGateway {
    private readonly StripeClient _stripe;
    public StripeAdapter(StripeClient stripe) { _stripe = stripe; }
    public void Charge(decimal amount) { _stripe.ProcessPayment((int)(amount * 100)); }
}
```

#### Decorator

Add behavior to objects dynamically by wrapping them. Avoids subclassing for every combination.

```typescript
interface TextFormatter { format(text: string): string; }

class PlainText implements TextFormatter {
    format(text: string) { return text; }
}
class BoldDecorator implements TextFormatter {
    constructor(private inner: TextFormatter) {}
    format(text: string) { return `<b>${this.inner.format(text)}</b>`; }
}
class ItalicDecorator implements TextFormatter {
    constructor(private inner: TextFormatter) {}
    format(text: string) { return `<i>${this.inner.format(text)}</i>`; }
}

const formatter = new ItalicDecorator(new BoldDecorator(new PlainText()));
formatter.format("Hello"); // <i><b>Hello</b></i>
```

#### Facade

Provide a simplified interface to a complex subsystem. Hides complexity behind a clean API.

```csharp
// Facade — callers don't need to know about the three subsystems
class OrderFacade {
    public void PlaceOrder(Cart cart) {
        _inventory.Reserve(cart.Items);
        _payment.Charge(cart.Total);
        _shipping.Schedule(cart.Address);
    }
}
```

---

### Behavioral

#### Strategy

Define a family of algorithms, encapsulate each, and make them interchangeable at runtime.

```typescript
interface SortStrategy<T> { sort(data: T[]): T[]; }
class QuickSort<T> implements SortStrategy<T> { sort(data: T[]) { ... } }
class MergeSort<T> implements SortStrategy<T> { sort(data: T[]) { ... } }

class DataProcessor<T> {
    constructor(private strategy: SortStrategy<T>) {}
    process(data: T[]) { return this.strategy.sort(data); }
}
```

Use when: you need to switch algorithms at runtime, or eliminate conditional branches for algorithm selection.

#### Observer

Define a one-to-many dependency so that when one object changes state, all dependents are notified automatically.

```csharp
interface IObserver { void Update(string eventName, object data); }

class EventBus {
    private Dictionary<string, List<IObserver>> _listeners = new();
    public void Subscribe(string evt, IObserver obs) { ... }
    public void Publish(string evt, object data) {
        if (_listeners.TryGetValue(evt, out var list))
            foreach (var obs in list) obs.Update(evt, data);
    }
}
```

Note: In languages with built-in event systems (C# events/delegates, TypeScript EventEmitter), prefer those over manual observer implementations.

#### Command

Encapsulate a request as an object, allowing undo, queuing, and logging of requests.

```typescript
interface Command { execute(): void; undo(): void; }

class MoveCommand implements Command {
    constructor(
        private entity: Entity,
        private from: Vector2,
        private to: Vector2
    ) {}
    execute() { this.entity.position = this.to; }
    undo() { this.entity.position = this.from; }
}
```

Use when: you need undo/redo, command queuing, macro recording, or transactional operations.

#### Template Method

Define the skeleton of an algorithm in a base class; let subclasses fill in specific steps.

```csharp
abstract class DataExporter {
    // Template method — defines the algorithm
    public void Export(DataSet data) {
        var formatted = Format(data);  // abstract — subclass decides
        Validate(formatted);           // concrete — shared by all
        WriteOutput(formatted);        // abstract — subclass decides
    }
    protected abstract string Format(DataSet data);
    protected abstract void WriteOutput(string data);
    private void Validate(string data) { /* shared validation */ }
}
```

#### Repository

Abstract data access behind an interface. Callers work with domain objects; the repository handles persistence.

```typescript
interface UserRepository {
    findById(id: string): Promise<User | null>;
    save(user: User): Promise<void>;
    delete(id: string): Promise<void>;
}

class SqlUserRepository implements UserRepository { ... }
class InMemoryUserRepository implements UserRepository { ... } // for tests
```

---

## Anti-Patterns to Avoid

| Anti-Pattern | Description | Fix |
|---|---|---|
| **God Class** | One class knows and does everything | Split by responsibility (SRP) |
| **Anemic Domain Model** | Classes are just data bags with no behavior | Move business logic into the domain class |
| **Primitive Obsession** | Using primitives (string, int) for domain concepts (Email, Money) | Create value objects |
| **Deep Inheritance** | 4+ levels of inheritance | Flatten with composition or interfaces |
| **Shotgun Surgery** | One change requires edits across many classes | Consolidate related responsibilities |
| **Feature Envy** | A method uses another class's data more than its own | Move the method to the class it envies |
| **Inappropriate Intimacy** | Two classes reach into each other's internals | Introduce abstractions / reduce coupling |
| **Magic Numbers** | Unexplained numeric literals in logic | Named constants or enums |

---

## Value Objects

For domain concepts that are defined by their value rather than identity, use value objects:

```csharp
// Primitive obsession
void Transfer(string fromAccount, string toAccount, decimal amount) { ... }

// Value objects — compile-time safety, no invalid state
record AccountId(string Value) {
    public static AccountId Parse(string raw) {
        if (string.IsNullOrWhiteSpace(raw)) throw new ArgumentException("Invalid account ID");
        return new(raw);
    }
}
record Money(decimal Amount, string Currency);
void Transfer(AccountId from, AccountId to, Money amount) { ... }
```

Value object rules:
- Immutable — no setters
- Equality by value, not reference
- Self-validating constructor — invalid state cannot be constructed
- Rich behavior — put domain logic on the value object, not on the caller

---

## Dependency Injection (DI)

Constructor injection is the preferred pattern. Avoid service locator — it hides dependencies.

```typescript
// Service locator — hidden dependencies, hard to test
class OrderService {
    process(order: Order) {
        const repo = ServiceLocator.get<OrderRepository>("OrderRepository"); // hidden
    }
}

// Constructor injection — explicit dependencies, easy to mock in tests
class OrderService {
    constructor(
        private readonly repo: OrderRepository,
        private readonly mailer: Mailer
    ) {}
    process(order: Order) { this.repo.save(order); this.mailer.sendConfirmation(order); }
}
```

**DI rules:**
- Depend on interfaces, not concrete classes (DIP)
- Inject via constructor, not via property or method injection (constructor injection enforces required dependencies)
- Wire the object graph in a composition root (startup / main), not inside classes
- Use a DI container for large applications; avoid for small scripts
