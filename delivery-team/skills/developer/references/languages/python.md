# Python Best Practices

Version baseline: Python 3.10+

## Style & Formatting

- Follow PEP 8; enforce with `ruff` (preferred) or `flake8`
- Format with `black` or `ruff format`; line length 88 (black default)
- Use `snake_case` for functions, variables, modules; `PascalCase` for classes; `UPPER_SNAKE_CASE` for constants
- One import per line; group: stdlib → third-party → local (separated by blank lines)
- Prefer explicit relative imports within packages

## Idioms & Patterns

- Use type hints everywhere: function signatures, class attributes, return types
- Prefer `dataclasses` or `pydantic` models over plain dicts for structured data
- Use context managers (`with`) for resource management — files, DB connections, locks
- Use `pathlib.Path` over `os.path` for all file system operations
- List/dict/set comprehensions over `map`/`filter` when readable; avoid nested comprehensions
- Use `enumerate()` over `range(len(x))`; `zip()` for parallel iteration
- Prefer `f-strings` over `.format()` or `%` formatting
- Use `walrus operator` (`:=`) sparingly — only when it genuinely improves clarity
- For async code: use `async`/`await` with `asyncio`; prefer `anyio` for library code

## Error Handling

- Catch specific exceptions, not bare `except:` or `except Exception:`
- Use custom exception classes that inherit from a domain base exception
- Never silence exceptions without logging: `except SomeError: pass` is almost always wrong
- Use `contextlib.suppress(ExceptionType)` when intentionally ignoring specific errors
- For functions that can fail, consider returning `result | None` or raising — be consistent
- Log exceptions with `logger.exception("message")` to capture traceback automatically

## Testing

- Use `pytest` as the test runner and framework
- Name test files `test_<module>.py`; test functions `test_<behavior>`
- Use `pytest.mark.parametrize` for data-driven tests
- Use fixtures for setup/teardown; prefer function-scoped unless shared state is needed
- Use `unittest.mock.patch` or `pytest-mock` for mocking; mock at the boundary (I/O, external services)
- Assert meaningful things — test behavior, not implementation details
- Target 80%+ coverage on business logic; don't chase coverage on boilerplate

## Security

- Never use `eval()` or `exec()` on untrusted input
- Use `secrets` module (not `random`) for security-sensitive randomness
- Use parameterized queries for all database access — never format SQL strings
- Validate and sanitize all external input at the boundary
- Store secrets in environment variables or secret managers — never in code or config files
- Use `subprocess` with `shell=False` and explicit argument lists; avoid `os.system()`
- Pin dependencies and run `pip-audit` or `safety` in CI

## Performance

- Profile before optimizing: `cProfile`, `line_profiler`
- Prefer generators over building large lists when processing sequences
- Use `__slots__` on data-heavy classes to reduce memory
- Avoid repeated attribute lookups in tight loops: cache as local variable
- Use `functools.lru_cache` or `functools.cache` for pure function memoization
- Prefer `collections.deque` over `list` for queue-like operations (O(1) append/popleft)
- I/O bound: use `asyncio`; CPU bound: use `multiprocessing` (GIL limitation)

## Anti-Patterns to Avoid

- **Mutable default arguments:** `def f(x=[])` — use `def f(x=None): x = x or []`
- **Wildcard imports:** `from module import *` pollutes namespace
- **Global state:** module-level mutable globals make testing and reasoning hard
- **`isinstance` chains:** use polymorphism, `match` statements, or `functools.singledispatch`
- **String accumulation in loops:** use `"".join(parts)` not `s += piece`
- **Catching and re-raising without context:** use `raise NewError(...) from original_error`
- **`os.path` for new code:** use `pathlib.Path`
- **Bare `print()` for logging:** use the `logging` module

## Tooling

| Tool | Purpose | Command |
|------|---------|---------|
| `ruff` | Linter + formatter | `ruff check . && ruff format .` |
| `mypy` | Type checker | `mypy src/` |
| `pytest` | Test runner | `pytest -v` |
| `pip-audit` | Dependency security | `pip-audit` |
| `pyproject.toml` | Project config | Single config file for all tools |
