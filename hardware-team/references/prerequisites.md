# Prerequisites: kicad-happy Dependency

The hardware-team plugin requires the **kicad-happy** plugin as an external dependency. Hardware-team role skills invoke kicad-happy skills via the Skill tool to perform schematic analysis, PCB review, component sourcing, fabrication validation, EMC analysis, and documentation generation.

---

## Dependency Summary

| Property | Value |
|----------|-------|
| Plugin name | `kicad-happy` |
| Minimum version | `>=1.2.0` |
| Skills consumed | 11 (kicad, spice, digikey, mouser, lcsc, element14, jlcpcb, pcbway, bom, emc, kidoc) |
| Required? | Yes (pipeline operates with degraded capability without it) |
| Config key | `dependencies.kicad_happy_version` in `.hardware/config.yml` |

---

## Installation

### Step 1: Install via Claude Code Plugin System

The kicad-happy plugin is installed through the Claude Code plugin system. It is hosted at the same repository or marketplace as hardware-team.

```
# In Claude Code, install the plugin:
install plugin kicad-happy
```

Or if installing from a GitHub repository:

```
install plugin from github P47Phoenix/Claude-Plugins/kicad-happy
```

### Step 2: Verify Installation

After installation, the plugin cache should contain kicad-happy at:

```
~/.claude/plugins/cache/kicad-happy/kicad-happy/<version>/
```

Each skill directory should contain a `SKILL.md` file:

```
<version>/
+-- kicad/SKILL.md
+-- spice/SKILL.md
+-- digikey/SKILL.md
+-- mouser/SKILL.md
+-- lcsc/SKILL.md
+-- element14/SKILL.md
+-- jlcpcb/SKILL.md
+-- pcbway/SKILL.md
+-- bom/SKILL.md
+-- emc/SKILL.md
+-- kidoc/SKILL.md
```

Or under a `skills/` subdirectory (both layouts are supported).

### Step 3: Configure Version Requirement

In your project's `.hardware/config.yml`, set the minimum required version:

```yaml
dependencies:
  kicad_happy_version: ">=1.2.0"
```

---

## Automatic Verification

The hardware-team plugin includes a **SessionStart hook** (`hooks/check_kicad_happy.py`) that automatically verifies kicad-happy availability every time a Claude Code session starts.

### What the Hook Checks

1. **Installation presence**: Is kicad-happy installed in the plugin cache?
2. **Skill availability**: For each of the 11 required skills, does the SKILL.md file exist?
3. **Version compatibility**: Does the installed version meet the `dependencies.kicad_happy_version` requirement from config?

### Hook Output Messages

| Condition | Message |
|-----------|---------|
| All 11 skills available | `kicad-happy: 11/11 skills available` |
| Some skills missing | `kicad-happy: N/11 skills available. Missing: [list]. Install kicad-happy via Claude Code plugin system.` |
| Not installed | `WARNING: Required dependency kicad-happy is not installed.` |
| Version mismatch | `kicad-happy version X.Y.Z installed; hardware-team requires >=A.B.C.` |
| Corrupted install | `WARNING: kicad-happy is installed but no skills found at <path>.` |

---

## Version Compatibility

| hardware-team Version | Minimum kicad-happy Version | Notes |
|----------------------|---------------------------|-------|
| 1.0.x | >=1.2.0 | Initial release. All 11 skill contracts at version 1.0. |

### Contract Versioning

Each kicad-happy skill has an output contract defined in `hardware-flow/references/kicad-integration.md`. When kicad-happy releases a new version:

1. Run the reference test fixture against the new version
2. If any output contract mismatch (`HW-KCH-004`) fires, the new version has a breaking change
3. Update contracts in `kicad-integration.md` to match
4. Increment the contract version
5. Update the compatibility table above

---

## Degraded Operation

If kicad-happy is not installed or partially installed, the hardware pipeline does NOT crash. Instead:

- Role skills that depend on unavailable kicad-happy skills report `SKILL_UNAVAILABLE`
- The pipeline continues with degraded capability
- Gates evaluate on available data only
- Artifacts document what could not be produced and why

This means you can explore the hardware-team pipeline structure and non-kicad-happy functionality without kicad-happy installed. However, for a complete pipeline run, all 11 kicad-happy skills should be available.

---

## Troubleshooting

### kicad-happy Not Found

```
WARNING: Required dependency kicad-happy is not installed.
```

**Fix**: Install kicad-happy via the Claude Code plugin system.

### Skills Missing

```
kicad-happy: 8/11 skills available. Missing: [emc, kidoc, spice].
```

**Fix**: The kicad-happy installation may be incomplete or an older version. Reinstall or update to the latest version.

### Version Mismatch

```
kicad-happy version 1.1.0 installed; hardware-team requires >=1.2.0.
```

**Fix**: Update kicad-happy to version 1.2.0 or later. Output contract mismatches are more likely with older versions.

### Contract Mismatch at Runtime

```
HW-KCH-004: CONTRACT_MISMATCH for kicad-happy:bom
```

**Fix**: This usually means the kicad-happy version has changed its output format. Check `kicad-integration.md` for the expected contract and compare with the actual output. Either update kicad-happy or update the contract definitions.
