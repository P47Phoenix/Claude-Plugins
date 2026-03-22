# CI/CD Pipeline Patterns

## Pipeline Stages

A well-structured CI/CD pipeline follows a progression from fast, cheap checks to slow, expensive validations. Fail fast -- the earliest stages should catch the most common errors.

### Standard Stage Progression

1. **Checkout & Setup** -- Clone repository, restore caches, install dependencies
2. **Lint & Static Analysis** -- Code style, type checking, security linting (seconds)
3. **Unit Tests** -- Fast, isolated tests with high coverage (seconds to low minutes)
4. **Build** -- Compile, bundle, containerize (minutes)
5. **Integration Tests** -- Tests requiring external dependencies, databases, services (minutes)
6. **Security Scan** -- Dependency vulnerability scanning, SAST, container image scanning (minutes)
7. **Package** -- Create versioned artifacts, push to registry (seconds)
8. **Deploy to Staging** -- Automated deployment to pre-production environment
9. **Acceptance Tests** -- End-to-end tests, smoke tests, performance baseline (minutes)
10. **Deploy to Production** -- Automated or gated deployment to production

### Stage Design Principles

- Each stage has a single clear purpose and a pass/fail outcome
- Stages run in parallel where dependencies allow (e.g., lint and unit tests in parallel)
- Failed stages halt the pipeline -- no skipping past failures
- Every stage produces artifacts or reports consumable by later stages
- Stage output is deterministic: same inputs produce same outputs

---

## Branching Strategies

### Trunk-Based Development

All developers commit to `main` (or `trunk`) frequently -- at least daily. Short-lived feature branches (1-2 days maximum) are acceptable. Release branches are cut from main when needed.

**When to use:** Teams with strong CI discipline, continuous deployment, feature flags for incomplete work. Preferred for most modern projects.

**Requirements:** Fast CI pipeline (under 10 minutes), comprehensive automated tests, feature flags, and a culture of small incremental changes.

### GitFlow

Long-lived `develop` and `main` branches with feature branches, release branches, and hotfix branches. Formal merge process between branches.

**When to use:** Projects with scheduled releases, multiple supported versions, strict release processes, or regulatory requirements that mandate release branches.

**Drawbacks:** Merge conflicts from long-lived branches, complex branch management, slower integration feedback.

### GitHub Flow

Single `main` branch with short-lived feature branches. Pull requests for code review. Merge to main triggers deployment.

**When to use:** Web applications with continuous deployment, small to medium teams, projects where every merge should be deployable.

**Distinction from trunk-based:** GitHub Flow encourages pull requests as a review gate; trunk-based emphasizes direct commits to main with post-commit review.

### Choosing a Strategy

| Factor | Trunk-Based | GitHub Flow | GitFlow |
|--------|-------------|-------------|---------|
| Release cadence | Continuous | Continuous | Scheduled |
| Team size | Any | Small-medium | Any |
| CI maturity required | High | Medium | Low |
| Merge conflict risk | Low | Low | High |
| Parallel version support | No | No | Yes |
| Regulatory compliance | Feature flags | PR approval logs | Branch-based audit trail |

---

## Artifact Management

### Versioned Artifacts

- Every build produces an immutable, versioned artifact (container image, binary, package)
- Artifact version ties back to a specific commit SHA -- traceability is non-negotiable
- Artifacts are built once and promoted through environments -- never rebuild for production
- Artifact metadata includes: commit SHA, build timestamp, pipeline run ID, dependency versions

### Container Registries

- Use a private registry for production images (ECR, GCR, ACR, Harbor)
- Tag images with both semantic version and commit SHA: `app:1.2.3` and `app:abc123f`
- Never use `latest` tag in production -- it is ambiguous and non-reproducible
- Implement image scanning on push -- block deployment of images with critical vulnerabilities
- Set retention policies to prevent unbounded storage growth

### Artifact Promotion

- Artifacts promoted from dev --> staging --> production without rebuilding
- Promotion is gated by test results and approvals at each stage
- Promoted artifacts are re-tagged or copied (not rebuilt) in the target registry
- Promotion audit trail records who approved, when, and what test results backed the decision

---

## Secrets Management

### Vault Patterns

- Secrets stored in a dedicated secrets manager (HashiCorp Vault, AWS Secrets Manager, Azure Key Vault)
- Applications retrieve secrets at startup or via sidecar injection -- never baked into images
- Secrets have explicit access policies -- principle of least privilege per service
- Secret references (paths/ARNs) are in config; actual values are never in version control

### Environment Injection

- CI pipelines inject secrets as masked environment variables -- never echo or log them
- Use CI platform's native secret storage (GitHub Actions secrets, GitLab CI variables) for pipeline secrets
- Rotate secrets on a defined schedule -- automate rotation where the platform supports it
- Separate secret scopes: CI pipeline secrets, application runtime secrets, infrastructure provisioning secrets

### Rotation Strategy

- Define rotation cadence per secret type (API keys: 90 days, database passwords: 30 days, signing keys: annually)
- Automate rotation -- manual rotation does not scale and is error-prone
- Dual-key/overlap period during rotation to prevent downtime
- Alert on secrets approaching expiration

---

## Build Caching

### Layer Caching (Containers)

- Order Dockerfile instructions from least-changing to most-changing
- Copy dependency manifests (package.json, go.mod, requirements.txt) before source code
- Use multi-stage builds to separate build dependencies from runtime image
- Cache layers in the CI platform's cache or a remote cache (BuildKit remote cache, registry cache)

### Dependency Caching

- Cache package manager directories (node_modules, .gradle, .m2, pip cache) between pipeline runs
- Key caches on the lockfile hash -- when dependencies change, the cache invalidates automatically
- Separate caches per platform/architecture in matrix builds
- Monitor cache hit rates -- low hit rates indicate a keying problem

### Incremental Builds

- Use build tools that support incremental compilation (Gradle, Bazel, Turborepo, Nx)
- Cache build outputs keyed on source file hashes
- For monorepos, detect which packages changed and only build/test affected packages
- Trade-off: incremental builds add complexity; only adopt when full builds are genuinely slow

---

## Matrix Builds

### Multi-Platform

- Build and test across target platforms (Linux, macOS, Windows) in parallel
- Container builds for multiple architectures (amd64, arm64) using buildx or equivalent
- Platform-specific test suites run on their respective platforms -- do not assume cross-platform compatibility

### Multi-Version

- Test against all supported language/runtime versions (e.g., Node 18, 20, 22)
- Test against all supported database versions if applicable
- Use matrix configuration to generate combinations automatically
- Allow failure on pre-release versions (e.g., nightly builds) without blocking the pipeline

---

## Pipeline-as-Code

### Declarative vs Scripted

- **Declarative** (GitHub Actions YAML, GitLab CI YAML, Tekton): Preferred for standard workflows. Easier to read, validate, and enforce structure. Use when the pipeline follows well-known patterns.
- **Scripted** (Jenkinsfile Groovy, custom bash): Use when pipeline logic requires complex conditionals, loops, or dynamic stage generation that declarative syntax cannot express.
- Hybrid approach: declarative pipeline structure calling scripted steps for complex logic.

### Reusable Workflows

- Extract common pipeline patterns into reusable templates (GitHub composite actions, GitLab CI includes, Jenkins shared libraries)
- Version templates independently -- consuming pipelines pin to a specific template version
- Template changes go through code review -- a broken template breaks all consuming pipelines
- Document template inputs, outputs, and side effects

### Template Design

- Templates accept parameters for customization -- do not hardcode project-specific values
- Provide sensible defaults -- a template should work with zero configuration for the common case
- Templates output structured results (test counts, coverage, artifact URLs) for downstream consumption
- Include validation: templates should fail clearly when required inputs are missing

---

## Pipeline Anti-Patterns

- **Manual gates everywhere** -- Excessive manual approvals slow delivery without adding proportional safety. Reserve manual gates for production deployment and regulated processes.
- **No parallelism** -- Running all stages sequentially when many could run in parallel. Lint, unit tests, and security scans are typically independent.
- **Coupling to a specific CI tool** -- Pipeline logic embedded in CI-vendor-specific syntax with no abstraction. Extracting logic into scripts (bash, Python, Makefile) improves portability.
- **Flaky test tolerance** -- Allowing intermittently failing tests to remain in the pipeline. Flaky tests erode confidence and train teams to ignore failures. Quarantine or fix immediately.
- **Monolithic pipeline** -- One massive pipeline file with hundreds of lines. Split into composable stages, reusable templates, and shared libraries.
- **No timeout configuration** -- Pipelines that hang indefinitely on a stuck step. Every stage should have a timeout.
- **Building in production** -- Compiling or building artifacts on production servers. Artifacts must be pre-built and promoted.
- **Ignoring pipeline performance** -- Never measuring pipeline execution time. Slow pipelines reduce developer productivity and delay feedback. Track and optimize.
