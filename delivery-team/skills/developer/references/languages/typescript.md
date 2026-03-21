# TypeScript Best Practices

Version baseline: TypeScript 5.x with strict mode

## Style & Formatting

- Enable `"strict": true` in `tsconfig.json` — this is non-negotiable
- Use ESLint with `@typescript-eslint` rules; format with Prettier
- Use `camelCase` for variables and functions; `PascalCase` for types, interfaces, classes, enums; `UPPER_SNAKE_CASE` for constants
- Prefer `interface` for object shapes that may be extended; `type` for unions, intersections, and aliases
- Export types alongside their implementations; use `export type { Foo }` for type-only exports

## Idioms & Patterns

- Always annotate public function return types explicitly — let TypeScript infer internal variables
- Use `unknown` instead of `any` when type is genuinely unknown; always narrow before use
- Use discriminated unions for modeling state: `{ status: 'loading' } | { status: 'success'; data: T } | { status: 'error'; error: Error }`
- Use `as const` for literal type narrowing on objects and arrays
- Use `satisfies` operator to validate a value against a type without widening
- Use `Readonly<T>` and `ReadonlyArray<T>` for immutable data structures
- Use template literal types for string constraints: `type EventName = `on${string}``
- Prefer `Map<K, V>` over `Record<string, V>` when keys are dynamic
- Use `Zod` or `io-ts` for runtime validation of external data (API responses, env vars, user input)

## Error Handling

- Use result types or discriminated unions for expected failures rather than throwing
- When throwing, always throw `Error` instances — not strings or plain objects
- Use `instanceof` to narrow error types in catch blocks
- For async code, always handle rejections — attach `.catch()` or use `try/catch` with `await`
- Avoid `as unknown as TargetType` casts — they bypass type safety; use type guards instead
- Write user-defined type guards (`function isUser(x: unknown): x is User`) for runtime narrowing

## Testing

- Use `Vitest` (preferred for modern projects) or `Jest` with `ts-jest`
- Write tests in `.test.ts` or `.spec.ts` files co-located with source
- Type your test data — avoid `any` in test fixtures
- Use `vi.mock()` / `jest.mock()` with typed mocks; use `vi.fn<Args, Return>()` for typed mock functions
- Use `@testing-library` for React/DOM components
- Test edge cases explicitly — TypeScript catches type errors at compile time, but tests catch runtime logic errors

## Security

- Do not use `as any` on data coming from external sources — always validate with Zod or similar
- Never trust `JSON.parse()` output without type narrowing
- Use `readonly` to prevent accidental mutation of shared data
- Avoid `Function` type — use specific function signatures
- Keep type assertions (`as Type`) confined to well-tested boundary code

## Performance

- Avoid excessive use of `Object.keys()` / `Object.entries()` in hot paths — they create new arrays
- Be cautious with complex mapped/conditional types — they increase compilation time
- Use `const enum` for compile-time constant folding (but avoid in library code for compatibility)
- Profile with `--diagnostics` flag in `tsc` to find slow type operations
- Split large type files; TypeScript incremental compilation is faster with proper project references

## Anti-Patterns to Avoid

- **`any`:** use `unknown` and narrow; `any` turns off type checking entirely
- **Non-null assertions everywhere (`!`):** indicates type model is wrong; fix the model
- **Double assertion (`x as unknown as Y`):** almost always a sign of a type error being hidden
- **`// @ts-ignore` without explanation:** leave a comment explaining why and when it can be removed
- **`enum` with string values:** prefer `as const` objects — they work better with exhaustiveness checking
- **Optional properties everywhere:** prefer discriminated unions over `Partial<T>` for state modeling
- **Implicit `any` in catch blocks:** `catch (e: unknown)` and narrow with `instanceof`

## Tooling

| Tool | Purpose | Command |
|------|---------|---------|
| `tsc` | Type checking | `tsc --noEmit` |
| `@typescript-eslint` | TS-aware linting | `eslint src/ --ext .ts,.tsx` |
| `prettier` | Formatting | `prettier --write .` |
| `vitest` | Test runner | `vitest run` |
| `zod` | Runtime validation | — |
| `tsx` | TS script runner | `tsx script.ts` |
