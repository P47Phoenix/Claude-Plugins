# Versioning Patterns

## Semantic Versioning (SemVer 2.0)

### Format: MAJOR.MINOR.PATCH

- **MAJOR** -- Incremented when making incompatible API changes. Consumers of your API/library must update their code.
- **MINOR** -- Incremented when adding functionality in a backward-compatible manner. Existing consumers are unaffected.
- **PATCH** -- Incremented when making backward-compatible bug fixes. No new functionality, just corrections.

### When to Bump Each

| Change Type | Version Bump | Example |
|-------------|-------------|---------|
| Breaking API change (removed endpoint, changed response structure) | MAJOR | 1.4.2 --> 2.0.0 |
| New feature, backward-compatible | MINOR | 1.4.2 --> 1.5.0 |
| Bug fix, no behavior change for correct usage | PATCH | 1.4.2 --> 1.4.3 |
| Security fix (backward-compatible) | PATCH | 1.4.2 --> 1.4.3 |
| Dependency update (no API change) | PATCH | 1.4.2 --> 1.4.3 |
| Performance improvement (no API change) | PATCH | 1.4.2 --> 1.4.3 |
| New optional parameter added | MINOR | 1.4.2 --> 1.5.0 |
| Required parameter added | MAJOR | 1.4.2 --> 2.0.0 |

### Rules

- MAJOR version zero (0.y.z) is for initial development. Anything may change. The API is not considered stable.
- Version 1.0.0 defines the public API. All subsequent version bumps are relative to this API.
- When MAJOR increments, MINOR and PATCH reset to 0 (1.4.2 --> 2.0.0)
- When MINOR increments, PATCH resets to 0 (1.4.2 --> 1.5.0)

---

## Calendar Versioning (CalVer)

### Common Formats

| Format | Example | Best For |
|--------|---------|----------|
| YYYY.MM.DD | 2025.03.15 | Products with date-significant releases |
| YYYY.MM.MICRO | 2025.03.1 | Monthly releases with patch numbering |
| YYYY.0M.MICRO | 2025.03.2 | Same as above with zero-padded month |
| YY.MM | 25.03 | Short form for frequent releases |

### When to Use CalVer Over SemVer

- The product does not have a meaningful public API (end-user applications, mobile apps)
- Releases are time-based rather than feature-based (monthly release trains)
- Users care more about "how recent" than "what changed" (OS distributions, data packages)
- The project follows a continuous delivery model where version semantics are less meaningful
- SemVer MAJOR bumps would happen so frequently they lose meaning

### When SemVer Is Better

- Libraries consumed by other developers (npm packages, Python packages, Go modules)
- APIs with contractual stability guarantees
- Systems where consumers need to know if an upgrade is safe without reading changelogs

---

## Pre-Release Conventions

### Standard Pre-Release Tags (SemVer)

- **alpha** -- Early development, unstable, API may change significantly. `2.0.0-alpha.1`
- **beta** -- Feature-complete for the release, but may contain bugs. API mostly stable. `2.0.0-beta.1`
- **rc (release candidate)** -- Believed to be ready for release. Only critical bug fixes between rc and final. `2.0.0-rc.1`

### Ordering

Pre-release versions have lower precedence than the release version:
`1.0.0-alpha.1 < 1.0.0-alpha.2 < 1.0.0-beta.1 < 1.0.0-rc.1 < 1.0.0`

### Build Metadata

- Appended with `+`: `1.0.0+build.123`, `1.0.0+20250315`
- Build metadata is ignored for version precedence -- `1.0.0+build.1` and `1.0.0+build.2` are equivalent for ordering
- Use for traceability: include CI build number, commit SHA, or build timestamp

---

## API Versioning

### URL Path Versioning

`/api/v1/users`, `/api/v2/users`

- **Pros:** Explicit, easy to understand, easy to route, easy to cache
- **Cons:** URL changes between versions, harder to support gradual migration
- **Best for:** Public APIs, APIs where version visibility is important

### Header Versioning

`Accept: application/vnd.myapp.v2+json` or `X-API-Version: 2`

- **Pros:** Clean URLs, supports content negotiation
- **Cons:** Version is hidden, harder to test in browser, harder to cache
- **Best for:** Internal APIs, APIs where URL stability is valued

### Query Parameter Versioning

`/api/users?version=2`

- **Pros:** Easy to add, optional (can default to latest)
- **Cons:** Easy to forget, can be stripped by proxies, mixing concerns
- **Best for:** Quick prototyping, not recommended for production APIs

### Choosing a Strategy

- For public APIs: URL path versioning is the industry standard
- For internal APIs: header versioning if the team is disciplined; URL path otherwise
- Avoid mixing strategies within the same API -- pick one and be consistent
- Version the API, not individual endpoints -- all endpoints move to v2 together

---

## Database Migration Versioning

### Sequential Numbering

Migrations numbered sequentially: `001_create_users.sql`, `002_add_email_column.sql`, `003_create_orders.sql`

- Simple and predictable ordering
- Conflict risk in teams: two developers may create migration 004 simultaneously
- Suitable for small teams with linear development

### Timestamp-Based

Migrations named with timestamps: `20250315120000_create_users.sql`, `20250315143000_add_email.sql`

- Avoids numbering conflicts in parallel development
- Ordering is clear from the timestamp
- Preferred for teams with multiple developers working on migrations simultaneously

### Idempotency

- Migrations should be safe to run multiple times -- use `IF NOT EXISTS`, `IF EXISTS` guards
- Track which migrations have run in a migrations table in the database
- Never edit a migration that has been applied to any environment -- create a new migration instead
- Test migrations in both directions: up (apply) and down (revert) where reversible

---

## Monorepo Versioning Strategies

### Independent Versioning

Each package in the monorepo has its own version number, incremented independently.

- Package A at 3.2.1, Package B at 1.0.4 -- no relationship between version numbers
- Each package's version reflects its own changes
- Consumers depend on specific package versions
- Tools: Lerna (independent mode), Nx, Changesets

### Synchronized Versioning

All packages in the monorepo share the same version number, incremented together.

- All packages release as 2.5.0, even if some packages had no changes
- Simpler to reason about compatibility -- "everything at version 2.5.0 works together"
- Version numbers increase faster for stable packages
- Tools: Lerna (fixed mode)

### Changesets

- Developers describe their changes in a changeset file during development
- Changesets specify which packages are affected and whether the change is major, minor, or patch
- At release time, changesets are consumed to automatically determine version bumps and generate changelogs
- Changeset files are committed to the repository and deleted when consumed

### Choosing a Strategy

| Factor | Independent | Synchronized |
|--------|-------------|-------------|
| Package coupling | Low -- packages are loosely related | High -- packages are tightly coupled |
| Release frequency | Packages release on different schedules | All packages release together |
| Consumer clarity | Consumers track individual package versions | Consumers use one version for all packages |
| Version churn | Low for stable packages | High for stable packages |

---

## Breaking Change Management

### Deprecation Policy

1. **Announce deprecation** -- Mark the feature/endpoint as deprecated in documentation, API responses, and changelogs
2. **Provide alternative** -- Document the replacement and migration path before deprecating the old way
3. **Set sunset date** -- Give a concrete date when the deprecated feature will be removed
4. **Warn at runtime** -- Emit deprecation warnings (HTTP headers, log messages, SDK warnings) when deprecated features are used
5. **Track usage** -- Monitor usage of deprecated features to gauge migration progress
6. **Remove after sunset** -- Remove the deprecated feature on or after the sunset date

### Migration Guides

- Every breaking change must have a migration guide published before the breaking version is released
- Migration guides include: what changed, why it changed, step-by-step migration instructions, before/after code examples
- Provide automated migration tools or codemods where feasible
- Test migration guides against real consumer codebases -- do not publish untested migration paths

### Sunset Timelines

| Change Severity | Minimum Deprecation Period |
|----------------|---------------------------|
| Major API restructuring | 6-12 months |
| Endpoint removal | 3-6 months |
| Parameter change | 1-3 months |
| Internal-only change | 1 sprint (with team notification) |

- Timelines are minimums -- extend for changes affecting many consumers
- Communicate timelines in the deprecation announcement, changelogs, and API documentation
- Send reminders at 50% and 25% of remaining deprecation period
