# Frontend Component Patterns

Cross-framework reference for component architecture, composition, forms, routing, error handling, lazy loading, accessibility, API design, and testing.

---

## Component Composition Patterns

### Render Props / Scoped Slots

Pass a function (or scoped slot) as a child that receives data and returns UI. The component owns the logic; the consumer owns the rendering.

- React: `<DataFetcher render={(data) => <List items={data} />} />`
- Vue: `<DataFetcher v-slot="{ data }"><List :items="data" /></DataFetcher>`
- Use when multiple consumers need the same behavior with different UIs
- Prefer hooks/composables when the pattern results in deeply nested render props ("render prop hell")

### Children / Slot Projection

Project arbitrary content into a component's layout regions.

- React: `props.children` for default slot; named slots via explicit props
- Vue: `<slot>` for default, `<slot name="header">` for named slots
- Svelte: `<slot>` and `<slot name="footer">`
- Angular: `<ng-content>` and `<ng-content select="[header]">`

### Compound Components

A set of components that share implicit state and work together as a unit (e.g., `<Tabs>`, `<TabList>`, `<Tab>`, `<TabPanel>`).

- Parent manages state; children register and consume via context or injection
- Enforces correct usage structure while keeping each piece composable
- Validate that required children are present; warn if misused

### Provider Pattern

A wrapper component that supplies data to an entire subtree without prop drilling.

- React: `React.createContext` + `useContext`
- Vue: `provide` / `inject`
- Scope providers narrowly; avoid a single global provider for unrelated concerns
- Nest providers in a defined order when multiple are needed

---

## Headless Components

Separate logic from presentation entirely. The component manages state, keyboard interaction, and ARIA attributes; the consumer supplies all markup and styling.

- Hook-based (React): `useCombobox()`, `useDialog()` -- return state + prop getters
- Renderless (Vue): component with only a scoped slot, no template of its own
- Libraries: Headless UI, Radix Primitives, React Aria, Downshift
- Benefits: full styling freedom, consistent behavior, testable logic in isolation
- The headless layer must handle accessibility; consumers should not need to add ARIA manually

---

## Form Patterns

### Controlled vs Uncontrolled

| Approach | How it works | When to use |
|---|---|---|
| Controlled | Component state drives the input value; every change triggers a state update | Validation on change, conditional logic, derived values |
| Uncontrolled | DOM holds the value; read via ref on submit | Simple forms, performance-sensitive large forms |

### Validation Strategies

- **Field-level**: validate as the user types or on blur; immediate feedback
- **Form-level**: validate all fields on submit; fewer interruptions
- **Schema-based**: define validation with Zod, Yup, or Valibot; share schemas between client and server
- Show errors after the first blur or submit attempt, not before the user has interacted
- Debounce async validation (e.g., username availability) to avoid excessive requests

### Multi-Step Forms (Wizards)

- Maintain a single form state object across steps; validate per-step on "Next"
- Allow backward navigation without losing data
- Model steps as a finite state machine: each step has allowed transitions
- Show a progress indicator; persist draft state to avoid data loss on refresh

### Form State Management

- Track: values, touched fields, dirty fields, errors, submission status, validation state
- Reset to initial values on cancel; confirm before discarding unsaved changes
- Disable submit button during async submission; show loading state

---

## Routing Patterns

### File-Based vs Code-Based

- File-based (Next.js, Nuxt, SvelteKit): filesystem structure defines routes; convention over configuration
- Code-based (React Router, Vue Router): explicit route definitions in a config file; more flexible
- Hybrid: file-based with escape hatches for programmatic route manipulation

### Nested and Dynamic Routes

- Nested routes render child views inside parent layouts (outlet / router-view / slot)
- Dynamic segments: `/users/:id`, `/posts/[slug]` -- extract params in the route handler
- Catch-all routes for 404 handling: `*`, `[...slug]`, `_`

### Route Guards and Middleware

- Authentication guards: redirect unauthenticated users before rendering the page
- Authorization guards: check permissions, show forbidden page if insufficient
- Data loading: fetch required data before route transition (loader pattern)
- Navigation guards: confirm before leaving a page with unsaved changes

### Lazy Route Loading

- Load route components on demand using dynamic imports
- Prefetch on hover or viewport intersection for perceived performance
- Show a loading indicator during chunk download; handle chunk load failures gracefully

---

## Error Boundaries

Catch rendering errors in a subtree and display a fallback UI instead of crashing the entire app.

- React: class component with `componentDidCatch` / `getDerivedStateFromError`, or libraries like `react-error-boundary`
- Vue: `onErrorCaptured` lifecycle hook
- Place boundaries at meaningful UI seams: around routes, around independent widgets, around third-party components
- Fallback UI should offer a retry action, not just an error message
- Log captured errors to a monitoring service (Sentry, DataDog, etc.)
- Do not catch errors from event handlers or async code -- those need separate try/catch

---

## Lazy Loading and Code Splitting

### Dynamic Imports

- `import('./module')` returns a promise; bundlers create a separate chunk automatically
- React: `React.lazy(() => import('./Component'))` wrapped in `<Suspense>`
- Vue: `defineAsyncComponent(() => import('./Component.vue'))`

### Splitting Strategies

- **Route-based**: each route is a separate chunk; most impactful for initial load
- **Component-based**: heavy components (charts, editors, maps) loaded on demand
- **Library-based**: isolate large dependencies into their own chunk via manual chunk configuration

### Loading States

- Always provide a visible loading indicator (skeleton, spinner, or placeholder)
- Set a minimum display time for loading states to prevent flash of loading content
- Handle chunk load failures: retry the import, or show an error with a reload option

---

## Accessibility Implementation

### ARIA Roles and Properties

- Use semantic HTML first (`<button>`, `<nav>`, `<dialog>`); add ARIA only when semantics are insufficient
- `role`, `aria-label`, `aria-labelledby`, `aria-describedby`, `aria-expanded`, `aria-selected`, `aria-live`
- Do not use ARIA to contradict native semantics (e.g., `role="button"` on a `<div>` when a `<button>` would work)

### Keyboard Handling

- All interactive elements must be reachable via Tab
- Custom widgets: implement arrow key navigation, Enter/Space activation, Escape to close
- Roving tabindex: only one item in a group is tabbable; arrow keys move focus within the group
- Document keyboard shortcuts; avoid overriding browser or OS shortcuts

### Focus Management

- Focus traps for modals and dialogs: Tab cycles within the modal; Escape closes it
- Return focus to the trigger element when a modal closes
- Skip links: a hidden link at the top of the page that jumps to main content on focus
- Manage focus on route transitions: move focus to the new page heading or main content

### Live Regions

- `aria-live="polite"` for non-urgent updates (search results count, form validation messages)
- `aria-live="assertive"` for urgent updates (error alerts, session timeout warnings)
- Keep live region content concise; screen readers will read the entire region content on change

---

## Component API Design

### Props Interface

- Define a clear TypeScript interface or PropTypes definition for every component
- Mark required props explicitly; provide sensible defaults for optional props
- Use union types for constrained values: `size: 'sm' | 'md' | 'lg'` not `size: string`
- Avoid boolean props that invert meaning (`isNotVisible`); prefer positive naming (`isVisible`)

### Event and Callback Naming

- React: `onEventName` (e.g., `onChange`, `onSubmit`, `onItemSelect`)
- Vue: `@event-name` (kebab-case in templates)
- Pass relevant data in the callback argument, not just the raw DOM event
- Document the callback signature in the props interface

### Slot and Render Customization

- Provide default rendering that works without customization
- Allow override via slots, render props, or component injection
- Pass context data to customization points so consumers can make informed rendering decisions

---

## Testing Patterns for Components

### Render Testing

- Render the component with representative props; assert expected output exists in the DOM
- Use `screen.getByRole`, `getByText`, `getByLabelText` -- prefer accessible queries over test IDs
- Test conditional rendering: verify elements appear and disappear based on state/props

### Interaction Testing

- Simulate user actions: click, type, keyboard navigation, focus
- Use `userEvent` (or equivalent) over `fireEvent` for realistic interaction simulation
- Assert side effects: callbacks called with expected arguments, state updates reflected in UI
- Test async interactions: loading states, error states, successful completion

### Snapshot Testing

- Use sparingly; snapshots are brittle and hard to review in code review
- Best for small, stable components (icons, badges) where exact output matters
- Review snapshot diffs carefully; do not blindly update snapshots

### Accessibility Testing

- Run axe or similar automated checks on rendered components
- Test keyboard navigation flows manually or with integration tests
- Verify ARIA attributes are set correctly based on component state
- Test with screen reader announcements for dynamic content changes
