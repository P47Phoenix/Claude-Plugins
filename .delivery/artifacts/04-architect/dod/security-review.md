# Security Re-Validation Review: hardware-team Plugin Architecture v1.4

**Role:** Security Architect | **Task:** dod-validation (re-validation) | **Gate 4 Criterion:** Security addressed (authentication, authorization, data protection, input validation)
**Date:** 2026-04-12
**Artifact Reviewed:** `.delivery/artifacts/04-architect/solution/architecture.md` v1.4
**Prior Review:** Security review of v1.3, findings SEC-01 through SEC-06

---

## Re-Validation Scope

This review verifies that the architect's v1.4 revisions adequately address all six findings from the prior security review. It also checks for new security issues introduced by the revisions.

---

## Finding Re-Validation

### SEC-01: File path traversal in artifact and state paths (was BLOCKING)

**Status: RESOLVED**

The v1.4 revision adds Section 7.2 ("Path Sanitization") with:

1. **Whitelist validation** via `sanitize_path_component()` using pattern `^[a-zA-Z0-9._-]+$` -- rejects `/`, `\`, `..`, null bytes, and all characters outside the whitelist. This directly addresses the threat of crafted `pipeline_id` or `project_name` values.
2. **Path canonicalization** via `safe_join()` using `os.path.realpath()` with verification that the resolved path starts with the `.hardware/` base directory. This is the defense-in-depth check that catches edge cases the whitelist might miss (e.g., symlink traversal).
3. **Error code `HW-STA-005`** added to the error taxonomy (Section 13.2) for path traversal detection, with Critical severity and a clear response behavior.
4. **Application scope documented**: Section 7.3 (State Operations, Create operation) explicitly calls out `sanitize_path_component()` for `pipeline_id` and `safe_join()` for config snapshot paths. Section 14.1 (Coding Standards) mandates `safe_join()` for all path construction from user-controlled values.
5. **Security invariant language**: The sanitization is called out as a "security invariant -- violation is a blocking defect" in Section 7.2.
6. **Testability**: Section 12.1 includes explicit unit test cases for both safe and unsafe path components, including `../../etc/passwd`, `foo/bar`, `foo\bar`, and `foo\x00bar`.

The mitigation is comprehensive and correctly layered (whitelist + canonicalization). The API design (`safe_join()` returning the un-resolved path for use, while validating the resolved path internally) is appropriate -- it avoids symlink confusion in normal operation while catching traversal attempts.

**Assessment: Adequately fixed. No residual concern.**

---

### SEC-02: Sensitive data exposure in BOM artifacts and kicad-happy output (was BLOCKING)

**Status: RESOLVED**

The v1.4 revision adds Section 14.2 ("Data Classification") with:

1. **Three-tier classification**: SENSITIVE (unit prices, total costs, supplier account IDs, negotiated rates), INTERNAL (supplier names, MPNs, datasheet URLs, stock levels), PUBLIC (descriptions, package types, quantities). The classification is well-scoped and covers the fields identified in the original finding.
2. **Artifact-level classification table**: Maps specific artifact files to their classification level. The two BOM artifacts (`bom-validation.md`, `final-bom.md`) are correctly classified as SENSITIVE.
3. **`.gitignore` integration**: The setup wizard offers to add SENSITIVE artifacts to `.gitignore` with an explicit user-facing note about public repositories. The entries are specific (not overly broad) and include the memory directory and config snapshots.
4. **Memory no-pricing filter**: Section 8.3, step 5 adds the primary defense (sub-agent prompt instruction to exclude pricing). Section 14.2 adds a secondary pattern-matching filter with `HW-SEC-001` error code for detected pricing. The two-layer approach (prompt instruction + pattern filter) is the correct design -- the prompt instruction prevents most pricing from entering the memory pipeline, and the filter catches what slips through.
5. **Testability**: Section 12.1 includes unit tests for the no-pricing filter with currency patterns and clean entries.
6. **Honest limitation acknowledged**: The pattern matching is described as "best-effort" and may miss obfuscated pricing. This is an appropriate acknowledgment rather than overclaiming.

**Assessment: Adequately fixed. No residual concern.**

---

### SEC-03: YAML injection in config and state files (was ADVISORY)

**Status: RESOLVED**

The v1.4 revision addresses this in two locations:

1. **Section 7.1**: Adds a "Security invariant (SEC-01)" callout (note: the document labels it SEC-01 in the callout but it addresses SEC-03 -- the YAML safe loading concern is correctly specified regardless of label). The mandate is clear: `yaml.safe_load()` only, never `yaml.load()` or `yaml.FullLoader`, with the deserialization attack vector explicitly named (`!!python/object/apply:os.system`).
2. **Section 14.1** (Coding Standards): Consolidates the requirement in a table with rationale. Lists `yaml.load()`, `yaml.FullLoader`, and `yaml.UnsafeLoader` as prohibited.
3. **Testability**: Section 12.1 includes a unit test that feeds `!!python/object/apply:os.system` tags to the parsers and verifies `ConstructorError` is raised.

**Assessment: Adequately addressed. The coding standard is precise and testable.**

---

### SEC-04: Cross-plugin invocation trust boundary (was ADVISORY)

**Status: RESOLVED**

The v1.4 revision adds a "Cross-Plugin Trust Boundary" subsection under Section 5.1 with:

1. **Explicit trust assumption**: "hardware-team trusts that the Claude Code plugin harness ensures plugin authenticity and integrity." This is the exact documentation recommended in the original finding.
2. **Threat acknowledged**: Plugin cache tampering is explicitly named as outside the plugin's threat model and assigned to the platform.
3. **Limitation acknowledged**: Semantic malicious data (e.g., manipulated BOM with inflated prices) would not be caught by contract validation. This is correctly classified as an accepted platform-level risk.
4. **Trust boundaries table**: Section 14.3 includes a row for the plugin harness trust boundary with a cross-reference to Section 5.1.
5. **Accepted risks table**: Section 14.4 includes plugin cache compromise with mitigating controls noted.

**Assessment: Adequately addressed. The trust boundary is now visible and well-documented.**

---

### SEC-05: State file tampering (was ADVISORY)

**Status: RESOLVED**

The v1.4 revision adds Section 7.2.1 ("State Tampering Accepted Risk") with:

1. **Accepted risk documentation**: Explicitly states the risk is accepted for a local development tool, with the rationale that users have legitimate override needs.
2. **Lightweight integrity hash**: SHA-256 hash over `stages_completed` and `gates` arrays, stored as `_integrity_hash` in the YAML frontmatter. On resume, a mismatch produces a warning.
3. **Non-blocking by design**: The warning does not block pipeline progression -- this is the correct choice for a local tool where the user is trusted.
4. **Trust boundary documented**: Section 14.3 includes `.hardware/state.md` with the note "User-editable; semantic tampering is an accepted risk."

**Assessment: Adequately addressed. The advisory integrity hash is proportionate to the risk level.**

---

### SEC-06: Hook script injection via environment variables (was ADVISORY)

**Status: RESOLVED**

The v1.4 revision adds Section 9.6 ("Hook Script Security Standards") with:

1. **Five coding standards** documented in a clear list: JSON parsing via `json.loads()` only, no shell execution of input data (`subprocess.run(shell=False)` with argument lists), path validation for extracted paths, fail-safe exit behavior.
2. **Code template**: A safe hook input parsing template is provided, demonstrating the correct pattern with `json.loads()`, `JSONDecodeError` handling, and `sys.exit(0)` on failure.
3. **Section 14.1 consolidation**: The coding standards table includes environment variable handling as untrusted input.
4. **Testability**: Section 12.1 includes unit tests for hook input sanitization with malformed JSON, shell metacharacters, and path traversal sequences.

**Assessment: Adequately addressed. The template provides a copy-paste-safe starting point for implementers.**

---

## New Issues Introduced by v1.4 Revisions

### Check 1: Does the path sanitization introduce any denial-of-service?

The `sanitize_path_component()` function raises `ValueError` on unsafe input, and the error taxonomy assigns `HW-STA-005` with Critical severity. This means a user who accidentally sets `project_name` to something containing a space (e.g., `"sensor board v2"`) would be blocked because spaces are not in the whitelist `^[a-zA-Z0-9._-]+$`.

**Assessment: Acceptable.** The config validation (Section 6.2) validates `project_name` as a non-empty string but does not restrict characters. However, the path sanitization will reject names with spaces at path construction time. This is a minor usability gap (the user gets a cryptic `HW-STA-005` error rather than a config validation warning), but it is not a security issue -- it fails closed, which is correct. The implementation should consider adding a config validation rule that checks `project_name` against the same whitelist pattern so the user gets an early, clear error during config validation rather than a late error during path construction. This is a **usability improvement, not a security finding**.

### Check 2: Does the integrity hash create a false sense of security?

The lightweight integrity hash in Section 7.2.1 is advisory only. A user who edits `state.md` could also update the `_integrity_hash` to match. The document correctly frames this as "for awareness, not enforcement" and the pipeline proceeds regardless.

**Assessment: No issue.** The design is honest about its limitations. The hash catches accidental edits, not adversarial tampering. This is appropriate for the threat model.

### Check 3: Does the no-pricing filter introduce information loss?

The pricing redaction in memory entries replaces values with `[PRICE REDACTED]`. If a future memory reader expects numeric values, the redacted string could cause a parse error.

**Assessment: No issue.** Memory entries are free-text lessons (string field), not structured data. The `[PRICE REDACTED]` marker is appropriate for text fields.

### Check 4: Does Section 14 consolidation miss any trust boundary?

Reviewed all trust boundaries in Section 14.3 against the architecture:
- Claude Code plugin harness: documented
- kicad-happy output: documented
- State file: documented
- User config: documented
- Hook environment variables: documented

No missing boundaries identified.

### Check 5: Are there any paths that bypass `safe_join()`?

Section 7.2 mandates `safe_join()` for all path construction from user-controlled values. The following path construction points exist in the architecture:
- Config snapshot path (`config-snapshot-<pipeline_id>.yml`): Section 7.3 documents `safe_join()` usage.
- Archived artifact paths (`archived/run-N/`): Section 3.4 describes archival but relies on `safe_join()` per Section 7.2 mandate.
- Artifact registry paths: Section 7.1 stores paths in the YAML registry. These are read-back for existence checks during resume (Section 7.4). The paths in the registry are written by the orchestrator using `safe_join()`, so they are validated at write time.

**Assessment: No bypass identified.** The mandate is comprehensive and covers all path construction points enumerated in the architecture.

---

## Quality Attribute Assessment (Updated)

| Attribute | Prior State | Current State (v1.4) | Risk Level |
|-----------|------------|---------------------|------------|
| Authentication | N/A (correct) | N/A (correct) | Low |
| Authorization | Partial (advisory bypass warning) | Partial (unchanged, acceptable for P1) | Low |
| Data Protection | **Gap** (BOM data unclassified) | **Resolved** (three-tier classification, `.gitignore`, no-pricing filter) | Low |
| Input Validation | **Gap** (path sanitization missing) | **Resolved** (whitelist + canonicalization + `safe_join()` API) | Low |
| Audit Trail | Strong | Strong (unchanged) | Low |
| Integrity | Partial | Improved (integrity hash + accepted risk documentation) | Low |

---

## Conclusion

All six findings from the prior security review (SEC-01 through SEC-06) have been adequately addressed in architecture v1.4. The two blocking findings (SEC-01 path traversal, SEC-02 BOM data exposure) are resolved with comprehensive, testable mitigations. The four advisory findings (SEC-03 through SEC-06) are resolved with appropriate coding standards, trust boundary documentation, and accepted risk rationale. No new security issues were introduced by the revisions.

The Gate 4 security criterion -- "Security addressed: authentication, authorization, data protection, input validation" -- is satisfied.
