# JavaScript Best Practices

Version baseline: ES2022+ (Node.js 20 LTS / modern browsers)

## Style & Formatting

- Use ESLint with a consistent ruleset (`eslint:recommended` + `plugin:prettier/recommended`)
- Format with Prettier; default config is fine for most projects
- Use `camelCase` for variables and functions; `PascalCase` for classes and components; `UPPER_SNAKE_CASE` for constants
- Use `const` by default; `let` only when reassignment is needed; never `var`
- Prefer named exports over default exports for better refactoring support
- Keep files focused: one primary concern per file

## Idioms & Patterns

- Use `async`/`await` over raw Promises or callbacks
- Use optional chaining (`?.`) and nullish coalescing (`??`) to handle null/undefined safely
- Prefer `Array` methods (`map`, `filter`, `reduce`, `find`, `some`, `every`) over `for` loops for transformations
- Use destructuring for objects and arrays to improve readability
- Use spread (`...`) for shallow copies and merging — be aware it is not a deep clone
- Use `structuredClone()` for deep cloning (Node 17+, modern browsers)
- Use `Promise.all()` for concurrent async operations; `Promise.allSettled()` when you need all results regardless of failure
- Use `Map` and `Set` over plain objects when keys are dynamic or non-string
- Avoid `arguments` object — use rest parameters (`...args`) instead

## Error Handling

- Always `try/catch` async operations or attach `.catch()` — never leave unhandled promise rejections
- Create custom error classes extending `Error`: set `this.name` in the constructor
- Use `instanceof` to check error type in catch blocks
- Log errors with sufficient context before rethrowing or handling
- Distinguish operational errors (expected, recoverable) from programmer errors (bugs)
- Set `process.on('unhandledRejection', ...)` in Node.js applications to catch missed rejections

## Testing

- Use `Jest` (general-purpose) or `Vitest` (Vite projects) as the test runner
- Name test files `<module>.test.js` or `<module>.spec.js`
- Use `describe` blocks to group related tests; `it`/`test` for individual cases
- Use `jest.mock()` to mock modules at the boundary (HTTP, DB, filesystem)
- Avoid testing implementation details — test observable behavior
- Use `@testing-library` for DOM/component testing; avoid direct DOM manipulation in tests

## Security

- Never use `eval()`, `new Function()`, or `innerHTML = userInput`
- Sanitize user input before rendering in the DOM — use `textContent` over `innerHTML`
- Use `===` (strict equality) — `==` causes type coercion that leads to subtle bugs
- Avoid `JSON.parse()` on untrusted input without a try/catch
- Do not log sensitive data (tokens, passwords, PII)
- Use `crypto.randomUUID()` or `crypto.randomBytes()` for security-sensitive randomness
- In Node.js: validate and sanitize all inputs; never pass user data to `exec()`, `spawn()` with `shell: true`, or `eval()`

## Performance

- Avoid synchronous operations in Node.js that block the event loop (`fs.readFileSync`, `crypto.pbkdf2Sync` in request handlers)
- Use `WeakMap`/`WeakRef` for caches keyed on objects to allow garbage collection
- Debounce or throttle event handlers that fire frequently (scroll, resize, input)
- Use `AbortController` to cancel fetch requests and avoid memory leaks
- Profile with Chrome DevTools or `node --inspect` before optimizing

## Anti-Patterns to Avoid

- **`var` declarations:** use `const`/`let`
- **Callback hell:** use async/await or Promise chaining
- **`== null` checks:** use `=== null` or `=== undefined` explicitly, or `??`
- **Mutating function arguments:** treat parameters as immutable; return new values
- **`for...in` on arrays:** use `for...of` or array methods
- **Floating Promises:** `asyncFn()` without `await` or `.catch()` silently drops errors
- **`__proto__` mutation:** use `Object.create()` or class syntax

## Tooling

| Tool | Purpose | Command |
|------|---------|---------|
| `eslint` | Linter | `eslint src/` |
| `prettier` | Formatter | `prettier --write .` |
| `jest` / `vitest` | Test runner | `jest` / `vitest run` |
| `npm audit` | Dependency security | `npm audit` |
| `.nvmrc` | Node version pinning | `nvm use` |
