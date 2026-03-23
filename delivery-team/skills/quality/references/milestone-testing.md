# Milestone Testing Protocols by Project Type

## Overview

Milestone testing validates that sprint deliverables work correctly as integrated
features -- not just as individual stories. Every project type has specific patterns
to test at sprint demos, phase completions, and feature integrations.

This file covers non-game project types. For game-specific milestone protocols,
see `exploratory-testing.md`.

## When to Run

- After each sprint that delivers integrated or user-facing features
- At phase completion (all stories in a phase delivered)
- When a major feature or integration point is first functional end-to-end
- Before any external demo, stakeholder review, or release candidate cut

## Feedback Template (All Project Types)

Use this template for every milestone test session, regardless of project type.

```markdown
## Milestone Test Report: [Sprint N / Phase N / Feature Name]
**Tester**: [role]
**Project Type**: [Web / API / Enterprise / Mobile / CLI]
**Duration**: [time]
**Build**: [commit hash]

### Findings
| # | Category | Severity | Finding | Spec Alignment |
|---|----------|----------|---------|----------------|

Categories: Bug, UX, Performance, Spec Gap, Integration Issue
Severity: CRITICAL / HIGH / MEDIUM / LOW
Spec Alignment: Matches spec / Contradicts spec / Not in spec
```

## Feedback Classification

| Classification | Action | Example |
|----------------|--------|---------|
| Bug | Log to .delivery/defects/ | Crash, broken endpoint, null reference |
| UX issue | Route to UX Designer | Confusing navigation, poor error messages |
| Performance issue | Route to Developer/Architect | Slow response, high memory, large bundle |
| Spec gap | Update PRD | Feature needed but not in spec |
| Integration issue | Route to Architect | Cross-service communication failure |

---

## Web / React Apps

### Milestone Validation

**Trigger**: Sprint delivers a complete user-facing page, workflow, or interactive
component that connects to live data or services.

**Duration**: 60-90 minutes per milestone. Include at least one full walkthrough
of each new workflow on two browser engines.

### Role-Specific Checklists

**Product Owner**
- [ ] Each delivered story is demo-ready and matches acceptance criteria
- [ ] Navigation between new and existing pages is logical and consistent
- [ ] Data displayed on screen matches expected business values
- [ ] Error states show user-friendly messages, not raw exceptions
- [ ] New features are discoverable without documentation

**QA Lead**
- [ ] Form validation rejects invalid input and preserves valid input on error
- [ ] Browser back/forward buttons do not break application state
- [ ] Loading states appear for async operations over 300ms
- [ ] Responsive layout holds at 320px, 768px, 1024px, and 1440px widths
- [ ] No console errors or warnings in the browser developer tools

**Developer**
- [ ] API calls use correct HTTP methods and return expected status codes
- [ ] Client-side state stays consistent after rapid user interactions
- [ ] No stale data after navigation away and back to a page
- [ ] Bundle size delta is within agreed threshold for the sprint

**UX Designer**
- [ ] Visual hierarchy guides the user toward primary actions
- [ ] Interactive elements have visible focus, hover, and active states
- [ ] Color contrast meets WCAG AA for all text and actionable elements
- [ ] Animations and transitions do not cause layout shifts
- [ ] Touch targets are at least 44x44px on mobile viewports

### Critical Path Testing

1. **New user onboarding flow** -- Create a new account (or new session) and walk
   through every step the user encounters before reaching the core feature.
2. **Primary CRUD cycle** -- Create, read, update, and delete the main domain
   object. Verify list views, detail views, and confirmation dialogs.
3. **Cross-page data consistency** -- Change data on one page and confirm the
   change is reflected on every other page that displays the same data.
4. **Authentication boundary** -- Log out mid-workflow, log back in, and verify
   the application recovers to a usable state without data loss.
5. **Error recovery** -- Disconnect the network, attempt an action, reconnect,
   and verify the application surfaces the failure and allows retry.
6. **Concurrent tab behavior** -- Open the same workflow in two tabs, make
   conflicting changes, and observe how the application resolves them.

### Cross-Feature Interaction Questions

- Does the new feature degrade the performance of existing pages that share the
  same API endpoints?
- Do global UI elements (header, sidebar, notifications) still function correctly
  when the new feature is active?
- If the feature introduces new roles or permissions, are unauthorized users
  properly blocked from accessing it?
- Does the feature interact correctly with existing browser extensions or ad
  blockers that users commonly run?

---

## API / Backend

### Milestone Validation

**Trigger**: Sprint delivers a new endpoint group, a data migration, or a service
integration that consumers can call end-to-end.

**Duration**: 45-75 minutes per milestone. Focus on contract compliance and
failure modes rather than visual output.

### Role-Specific Checklists

**Product Owner**
- [ ] API responses contain the fields and values specified in the contract
- [ ] Business rules produce correct outcomes for representative test data
- [ ] Rate limits and quotas match the documented SLA
- [ ] Changelog or versioning reflects the new capabilities accurately

**QA Lead**
- [ ] Every new endpoint returns correct status codes for success and each
      documented error condition
- [ ] Input validation rejects payloads that violate the schema
- [ ] Pagination, sorting, and filtering work on list endpoints
- [ ] Idempotency keys prevent duplicate side effects on retry
- [ ] Response times are within the agreed performance budget

**Developer**
- [ ] Database queries use indexes and avoid N+1 patterns
- [ ] Transactions roll back cleanly on partial failure
- [ ] Logging captures request IDs, durations, and error details without
      exposing secrets
- [ ] New migrations are reversible and tested in both directions

**Architect**
- [ ] Service-to-service authentication tokens rotate without downtime
- [ ] New endpoints follow the existing URL and naming conventions
- [ ] Breaking changes are versioned and old consumers are unaffected
- [ ] Circuit breakers and timeouts are configured for external dependencies
- [ ] Health check endpoint reflects the status of new dependencies

### Critical Path Testing

1. **Full auth flow** -- Obtain a token, call a protected endpoint, refresh the
   token, and call again. Verify rejection after token revocation.
2. **CRUD cycle with validation** -- Create an entity with valid data, read it
   back, update with partial data, and delete. Confirm 404 on subsequent read.
3. **Bulk operation** -- Submit a batch of 100+ items. Verify all succeed, or
   that partial failure returns clear per-item error detail.
4. **Concurrent writes** -- Send two conflicting updates at the same time.
   Verify optimistic locking or last-write-wins behavior matches the spec.
5. **Downstream dependency failure** -- Simulate a timeout or 500 from an
   external service. Verify the API returns a meaningful error and does not
   leave data in an inconsistent state.
6. **Schema evolution** -- Send a request with an extra unknown field. Confirm
   the API either ignores it or rejects it, per the documented contract.
7. **Large payload** -- Submit a request at or above the documented size limit.
   Verify the API enforces the limit with an appropriate error.

### Cross-Feature Interaction Questions

- Do new endpoints share database tables with existing endpoints, and if so,
  do new indexes or constraints affect existing query performance?
- Does the new service emit events that existing consumers need to handle?
- If the new feature introduces asynchronous processing, is there a way to
  verify job completion and handle job failure?

---

## Enterprise / B2B

### Milestone Validation

**Trigger**: Sprint delivers a tenant-facing capability, an admin configuration
surface, a compliance control, or an integration with a corporate identity provider.

**Duration**: 75-120 minutes per milestone. Must include at least two tenant
configurations to verify isolation.

### Role-Specific Checklists

**Product Owner**
- [ ] Feature behavior is correct for each license tier (free, standard, premium)
- [ ] Admin configuration changes take effect without requiring a restart
- [ ] Audit log entries are created for every state-changing action
- [ ] Branding and white-label settings apply consistently across the feature

**QA Lead**
- [ ] Tenant A cannot view, modify, or infer data belonging to Tenant B
- [ ] Role-based access control enforces the permission matrix for every action
- [ ] Session timeout and re-authentication work per the security policy
- [ ] Data export produces correct output in all supported formats (CSV, PDF, JSON)
- [ ] Bulk operations complete within SLA and report progress to the user

**Security**
- [ ] All inputs are sanitized against injection (SQL, XSS, command injection)
- [ ] Sensitive fields are encrypted at rest and masked in API responses
- [ ] API keys and tokens are not logged or exposed in error messages
- [ ] Failed login attempts trigger lockout after the configured threshold
- [ ] Data retention and deletion comply with the stated policy

**Architect**
- [ ] Multi-tenant data isolation uses the agreed strategy (schema, row, database)
- [ ] Background jobs are tenant-scoped and do not starve other tenants
- [ ] SSO and SAML/OIDC flows complete correctly for each identity provider
- [ ] Feature flags disable the new capability per-tenant without side effects

### Critical Path Testing

1. **Multi-tenant isolation** -- Log in as Tenant A, create data. Log in as
   Tenant B and confirm no visibility into Tenant A data via UI, API, or
   exported reports.
2. **Role escalation attempt** -- Authenticate as a low-privilege user and
   attempt to call admin-only endpoints or access admin UI routes directly.
3. **SSO round-trip** -- Initiate login via SAML/OIDC, complete authentication
   at the identity provider, and verify correct tenant and role assignment on
   return.
4. **Compliance audit trail** -- Perform create, update, and delete operations.
   Query the audit log and verify every action is recorded with actor, timestamp,
   and before/after values.
5. **License enforcement** -- Attempt to use a premium feature from a standard
   tier account. Verify the system blocks the action with a clear upgrade prompt.
6. **Data residency** -- If the system supports regional data storage, confirm
   that tenant data is written to and read from the designated region only.

### Cross-Feature Interaction Questions

- Does the new feature respect existing tenant-level feature flags and license
  restrictions?
- Are background jobs and scheduled tasks scoped to the correct tenant context,
  especially when running in a shared worker pool?
- Does the feature generate notifications or emails, and if so, do they use the
  tenant's branding and sender domain?
- If the feature touches personally identifiable information, does it integrate
  with the existing data subject access request (DSAR) workflow?

---

## Mobile Apps

### Milestone Validation

**Trigger**: Sprint delivers a new screen, a native integration (camera, GPS,
push notifications), or an offline-capable workflow.

**Duration**: 60-90 minutes per milestone. Test on at least one iOS and one
Android device (physical preferred over emulator for hardware integration).

### Role-Specific Checklists

**Product Owner**
- [ ] Each delivered feature is reachable from the main navigation
- [ ] Push notifications display correct content and deep-link to the right screen
- [ ] Onboarding and first-run experience matches the approved design
- [ ] In-app purchase or subscription flow completes without error

**QA Lead**
- [ ] App does not crash on launch, backgrounding, or foregrounding
- [ ] Screen transitions are smooth with no visible frame drops
- [ ] Text does not overflow or truncate on smallest supported screen size
- [ ] Accessibility labels are present on all interactive elements
- [ ] App handles permission denial gracefully (camera, location, notifications)

**Developer**
- [ ] Network requests use certificate pinning where required
- [ ] Local database migrations run without data loss on upgrade
- [ ] Memory usage stays within acceptable bounds during extended use
- [ ] Background tasks complete within OS-imposed time limits
- [ ] Deep links resolve to the correct screen with correct parameters

**UX Designer**
- [ ] Gesture interactions (swipe, long press, pinch) are discoverable
- [ ] Haptic feedback is used consistently for destructive or confirming actions
- [ ] Dark mode and light mode both render correctly
- [ ] Keyboard does not obscure input fields on any screen
- [ ] Loading skeletons or placeholders appear before content loads

### Critical Path Testing

1. **Offline workflow** -- Enable airplane mode, perform the core user action,
   re-enable connectivity, and verify data syncs correctly without duplicates.
2. **Interruption recovery** -- Receive a phone call mid-workflow, return to the
   app, and verify state is preserved and the workflow can continue.
3. **Permission request sequence** -- Install the app fresh, walk through the
   first-run flow, deny each permission when prompted, and verify the app
   degrades gracefully with clear explanations of what is unavailable.
4. **Background to foreground** -- Leave the app in the background for 10+
   minutes, return, and verify data is fresh and the session is still valid.
5. **Low storage and low battery** -- Simulate constrained conditions and verify
   the app does not crash or corrupt data.
6. **Push notification tap** -- Send a push notification while the app is closed,
   tap it, and verify the app opens to the correct screen with correct context.
7. **Upgrade path** -- Install the previous version, create data, then upgrade
   to the current build. Verify all data migrates and features work.

### Cross-Feature Interaction Questions

- Does the new screen interfere with existing navigation gestures (swipe-back,
  tab switching)?
- If the feature uses the camera or microphone, does it release the hardware
  resource when the user navigates away?
- Does the feature's network usage affect the app's overall data consumption in
  a way that matters for metered connections?

---

## CLI Tools

### Milestone Validation

**Trigger**: Sprint delivers a new command, a new output format, a configuration
system change, or a scripting integration point.

**Duration**: 30-60 minutes per milestone. Test in at least two shell environments
(bash and one other -- zsh, fish, or PowerShell).

### Role-Specific Checklists

**Product Owner**
- [ ] Command names and flag names match the documented interface
- [ ] Help text for each new command is accurate and includes examples
- [ ] Default behavior without flags matches the documented convention
- [ ] Error messages tell the user what went wrong and how to fix it

**QA Lead**
- [ ] Exit codes follow the documented convention (0 for success, non-zero for
      specific error categories)
- [ ] Output formats (plain text, JSON, table) are selectable and well-formed
- [ ] Commands that modify state prompt for confirmation unless --yes is passed
- [ ] Long-running commands show progress indicators
- [ ] Ctrl+C interrupts cleanly without leaving temp files or locks

**Developer**
- [ ] Stdin, stdout, and stderr are used correctly (data to stdout, messages
      to stderr)
- [ ] File paths handle spaces, unicode, and symlinks
- [ ] Environment variable overrides work as documented
- [ ] Commands are safe to retry without unintended side effects

**Architect**
- [ ] Configuration precedence follows the documented order: flags > env vars >
      project config > user config > defaults
- [ ] Plugin or extension points load third-party code without compromising the
      main process
- [ ] Shell completion scripts are generated correctly for bash, zsh, and fish
- [ ] Subcommand structure is consistent and does not conflict with common
      system commands

### Critical Path Testing

1. **Pipe chain** -- Pipe the output of the new command into grep, awk, or jq
   and verify the output is machine-parseable and free of decoration.
2. **Exit code contract** -- Run the command with valid input (expect 0), invalid
   input (expect specific non-zero), and missing dependencies (expect distinct
   non-zero). Verify each exit code.
3. **Configuration cascade** -- Set a value at each precedence level (default,
   user config, project config, env var, flag) and verify the highest-priority
   source wins at each step.
4. **Large input** -- Feed a file with 100,000+ lines into the command. Verify
   it completes in reasonable time without excessive memory use.
5. **Globbing and quoting** -- Pass arguments with spaces, wildcards, and special
   characters. Verify the command handles them without shell expansion issues.
6. **Concurrent execution** -- Run two instances of the command targeting the
   same resource. Verify file locking or conflict detection prevents corruption.
7. **Verbose and quiet modes** -- Run with --verbose and --quiet flags. Verify
   verbose adds diagnostic detail to stderr and quiet suppresses non-error output.

### Cross-Feature Interaction Questions

- Does the new command respect global flags (--config, --no-color, --format)
  that existing commands already support?
- If the command writes to a shared config or state file, does it lock correctly
  to prevent corruption from parallel runs?
- Does the command's output format remain stable enough for existing scripts and
  CI pipelines that may consume it?
- If the command introduces new dependencies, does the installation or setup
  documentation account for them?
