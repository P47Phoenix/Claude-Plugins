# Frontend State Management

Cross-framework reference for state architecture, reactive patterns, server state, URL state, form state, optimistic updates, normalization, derived state, persistence, and anti-patterns.

---

## Local vs Global State

### When to Use Each

| State type | Scope | Examples |
|---|---|---|
| Local | Single component | Toggle open/closed, input value, hover state, animation state |
| Shared | Parent + few children | Selected item in a list, accordion expansion state |
| Global | App-wide | Authenticated user, theme preference, feature flags, notification queue |

### Colocation Principle

Keep state as close as possible to where it is used. Start with local state; lift it up only when a sibling or distant component needs it. Moving state to a global store prematurely creates coupling and makes components harder to reuse.

### Lifting State Up

When two sibling components need the same state, move it to their nearest common ancestor. Pass the value down as a prop and the updater function as a callback. This is the simplest form of state sharing and should be the first approach before reaching for context or stores.

---

## State Machines for UI

Model complex UI flows as explicit state machines using XState, statecharts, or a simple reducer with named states.

### When to Use

- Modals with multiple stages (confirm, loading, success, error)
- Multi-step forms / wizards
- Async operations with loading, success, error, and retry states
- Any flow where certain actions are only valid in certain states

### Benefits

- Impossible states are truly impossible: the machine defines exactly which transitions are valid
- Self-documenting: the state chart is a visual specification of the flow
- Testable: enumerate states and transitions; verify guards and side effects
- Avoids boolean flag combinatorics (`isLoading && !isError && hasData` becomes a single named state)

### Implementation Pattern

```
States: idle, loading, success, error
Events: FETCH, RESOLVE, REJECT, RETRY, RESET
Transitions:
  idle -> loading (on FETCH)
  loading -> success (on RESOLVE)
  loading -> error (on REJECT)
  error -> loading (on RETRY)
  success -> idle (on RESET)
```

Define side effects (data fetching, analytics) as actions on transitions, not inside render logic.

---

## Reactive Stores

### Signals Pattern

Fine-grained reactivity where individual values are observable and only the consumers of a changed value re-render.

- Solid.js: `createSignal`, `createEffect`, `createMemo`
- Preact Signals, Angular Signals, Vue `ref` / `reactive`
- Only the specific DOM nodes or computations that depend on a signal update when it changes
- No need for memoization wrappers; reactivity is automatic and granular

### Observables

Stream-based reactivity (RxJS) for complex async flows: debounce, merge, switchMap, retry.

- Best for: real-time data streams, complex event coordination, race condition management
- Subscription management is critical: unsubscribe on component unmount to prevent memory leaks
- Use `takeUntil`, `take`, or framework-provided auto-cleanup (Angular `AsyncPipe`, RxJS interop hooks)

### Subscription Management

- Always clean up subscriptions when a component unmounts
- React: return a cleanup function from `useEffect`
- Vue: `onUnmounted` or `watchEffect` auto-cleanup
- Svelte: use the `$` auto-subscription syntax or `onDestroy`
- Framework store adapters (Zustand, Pinia, NgRx) handle subscription lifecycle automatically

---

## Server State Management

Server state is fundamentally different from client state: it is asynchronous, shared, and can become stale. Treat it with dedicated tools.

### Fetch, Cache, Invalidate Pattern

Libraries: TanStack Query (React Query), SWR, Apollo Client, Vue Query, URQL.

- **Fetch**: declare a query key and a fetch function; the library handles deduplication, caching, and refetching
- **Cache**: responses are cached by key; subsequent renders use the cache while revalidating in the background
- **Invalidate**: after a mutation, invalidate related query keys to trigger a refetch
- Stale time: how long cached data is considered fresh before background refetch
- Cache time: how long unused cached data stays in memory before garbage collection

### Optimistic Updates with Server State

- Update the cache immediately before the mutation request completes
- Roll back the cache to the previous value if the mutation fails
- TanStack Query: `onMutate` returns a context with the previous value; `onError` uses it to roll back

### Pagination and Infinite Queries

- **Pagination**: pass page number as part of the query key; prefetch the next page for instant navigation
- **Infinite queries**: append new pages to an accumulated list; track `hasNextPage` and `fetchNextPage`
- Use cursor-based pagination when the dataset changes frequently (offset-based can skip or duplicate items)

---

## URL State

Use URL search parameters as state for values that should be shareable, bookmarkable, or survive page refresh.

### When to Use URL State

- Filter and sort settings on a list page
- Active tab or panel selection
- Search query text
- Pagination page number
- Any state where a user expects to share or bookmark the current view

### Implementation

- Read from `URLSearchParams` or framework router query params
- Write by updating the URL via `pushState` / `replaceState` or the router's navigation API
- Use `replaceState` for high-frequency updates (typing in a search box) to avoid polluting history
- Serialize complex values to JSON; keep URL-encoded values human-readable when possible

### Deep Linking

- On initial load, parse the URL and initialize component state from query params
- Ensure the UI and URL stay in sync: URL changes update the UI, and UI changes update the URL
- Test that shared URLs reproduce the expected view for another user

---

## Form State

### Library Patterns

| Library | Framework | Key concept |
|---|---|---|
| React Hook Form | React | Uncontrolled inputs with `register`; minimal re-renders; `useForm` hook |
| Formik | React | Controlled form state; `<Field>`, `<Form>`, `useFormik` |
| VeeValidate | Vue | Composition API `useForm`, `useField`; schema-based validation |
| Svelte Superforms | Svelte | Server-validated forms with progressive enhancement |

### Validation Schemas

- Define validation separately from the form component using Zod, Yup, or Valibot
- Share schemas between client and server for consistent validation
- Schema-first approach: derive TypeScript types from the schema to keep types and validation in sync

### Dirty Tracking and Submit Handling

- Track `isDirty` (any field changed from initial value) and `touchedFields` (fields the user has interacted with)
- Show a confirmation dialog if the user navigates away with unsaved changes
- Disable the submit button during submission; show a loading indicator
- Handle submission errors: display server-side validation errors next to the relevant fields
- Reset form state after successful submission or provide a clear action

---

## Optimistic Updates

Update the UI immediately as if the operation succeeded, then reconcile with the server response.

### Pattern

1. Save the current state as a rollback snapshot
2. Apply the expected change to local state / cache
3. Send the mutation request to the server
4. On success: optionally replace the optimistic value with the server's canonical response
5. On failure: revert to the rollback snapshot; show an error message

### Conflict Resolution

- If the server returns a different value than expected, use the server value (server is source of truth)
- For collaborative editing, consider operational transforms or CRDTs instead of simple optimistic updates
- Queue mutations when offline; replay and reconcile when connectivity returns

### When to Use

- Actions where latency is noticeable and the success rate is high (adding to cart, toggling a favorite, sending a message)
- Avoid for destructive actions where failure has significant consequences (payments, deletions without undo)

---

## State Normalization

### Flat Structures

Store entities in a flat map keyed by ID instead of deeply nested objects.

```js
// Instead of nested:
{ posts: [{ id: 1, author: { id: 5, name: "Alice" }, comments: [...] }] }

// Normalized:
{
  posts: { byId: { 1: { id: 1, authorId: 5, commentIds: [10, 11] } }, allIds: [1] },
  users: { byId: { 5: { id: 5, name: "Alice" } } },
  comments: { byId: { 10: {...}, 11: {...} } }
}
```

### Benefits

- Single source of truth for each entity; updating a user name propagates everywhere
- Eliminates data duplication and the bugs that come with inconsistent copies
- Efficient lookups by ID; selectors compose flat data into the shape components need

### Selector Patterns

- Write selectors that derive component-specific views from normalized state
- Memoize selectors (reselect, computed properties) to avoid recomputation on unrelated state changes
- Selectors are the API between store shape and component needs; changing the store shape only requires updating selectors

---

## Derived State and Computed Values

State that can be calculated from other state should not be stored separately -- compute it.

### Principles

- If a value can be derived from existing state, derive it; do not store it
- Storing derived values creates synchronization bugs (the derived value gets out of sync with its source)
- Use memoization to avoid expensive recomputation: `useMemo`, `computed`, `createMemo`, reselect

### Framework Patterns

| Framework | Mechanism |
|---|---|
| React | `useMemo(() => derive(state), [state])` |
| Vue | `computed(() => derive(state.value))` |
| Svelte | `$: derived = compute(state)` |
| Solid | `createMemo(() => derive(signal()))` |
| Angular | `computed(() => derive(signal()))` |

### Common Derived Values

- Filtered / sorted lists from a base collection
- Totals, counts, aggregates
- Formatted display values (currency, dates, full names)
- Validation state derived from form values

---

## State Persistence

### Storage Options

| Storage | Capacity | Lifetime | Scope |
|---|---|---|---|
| `localStorage` | ~5-10 MB | Permanent until cleared | Same origin |
| `sessionStorage` | ~5-10 MB | Until tab closes | Same origin, same tab |
| `IndexedDB` | Large (hundreds of MB) | Permanent until cleared | Same origin |
| Cookies | ~4 KB | Configurable expiry | Same origin, sent to server |

### Sync Across Tabs

- `localStorage` fires a `storage` event in other tabs when a value changes
- Use `BroadcastChannel` for more complex cross-tab communication
- Keep a single source of truth; other tabs react to changes rather than independently writing

### Implementation

- Serialize state to JSON before storing; deserialize on load
- Handle missing or corrupted stored data gracefully: validate on load, fall back to defaults
- Version stored data with a schema version key; migrate or discard stale data on load
- Be mindful of storage limits; do not store large datasets in `localStorage`

---

## Common Anti-Patterns

### Prop Drilling Too Deep

Passing props through many intermediate components that do not use them. Solution: use context, provide/inject, or a store for deeply shared state.

### Global State Overuse

Putting everything in a global store (form input values, toggle states, hover states). Solution: default to local state; promote to global only when multiple unrelated components need it.

### Redundant State

Storing a value that can be derived from other state (e.g., storing both `items` and `itemCount`). Solution: compute derived values; do not store them.

### State Synchronization Bugs

Keeping the same data in two places and manually syncing them. One inevitably becomes stale. Solution: single source of truth, derive everything else.

### Stale Closure Bugs

Referencing outdated state inside closures (common in React `useEffect` and event handlers). Solution: include all dependencies in dependency arrays; use refs for values that should not trigger re-effects.

### Overfetching and Underfetching

Fetching too much data (loading all users when you need one) or too little (N+1 queries on the client). Solution: design API queries to match UI needs; use GraphQL or backend-for-frontend patterns when REST endpoints do not align.
