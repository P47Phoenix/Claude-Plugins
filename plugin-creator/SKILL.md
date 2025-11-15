---
name: plugin-creator
description: Guide for creating Claude Code plugins. This skill should be used when users want to create a new plugin (or update an existing plugin) that extends Claude Code with custom commands, agents, hooks, skills, or MCP servers.
license: MIT License - See repository LICENSE file
---

# Plugin Creator

This skill provides comprehensive guidance for creating Claude Code plugins that extend Claude's capabilities through custom commands, agents, hooks, skills, and MCP server integrations.

## About Plugins

Plugins are extensions for Claude Code that provide custom functionality through multiple components. Unlike skills (which provide specialized knowledge and workflows), plugins can include:

1. **Custom Commands** - Slash commands that execute specific tasks
2. **Custom Agents** - Specialized agents for particular workflows
3. **Hooks** - Event handlers that trigger on specific actions
4. **Skills** - Reusable capabilities with specialized knowledge
5. **MCP Servers** - Model Context Protocol integrations

### When to Create a Plugin vs a Skill

**Create a Skill when:**
- Providing specialized knowledge or workflows for a specific domain
- Building reusable capabilities that Claude can invoke autonomously
- Bundling scripts, references, and assets for repetitive tasks

**Create a Plugin when:**
- Adding custom slash commands for user-initiated actions
- Building specialized agents with unique tool access
- Implementing hooks to respond to events
- Combining multiple components (commands + skills + hooks)
- Distributing functionality through a marketplace

## Plugin Structure

Every plugin follows this standardized structure:

```
plugin-name/
├── .claude-plugin/
│   └── plugin.json          # Plugin metadata (required)
├── commands/                 # Custom slash commands (optional)
│   └── command-name.md
├── agents/                   # Custom agents (optional)
│   └── agent-definition.json
├── skills/                   # Skills subdirectories (optional)
│   └── skill-name/
│       └── SKILL.md
├── hooks/                    # Event handlers (optional)
│   └── hooks.json
└── .mcp.json                # MCP server config (optional)
```

### Plugin Metadata (.claude-plugin/plugin.json)

The `plugin.json` file contains essential metadata:

```json
{
  "name": "plugin-name",
  "version": "1.0.0",
  "description": "Brief description of what this plugin does",
  "author": {
    "name": "Author Name",
    "email": "author@example.com"
  },
  "commands": ["./commands"],
  "agents": ["./agents"],
  "skills": ["./skills/skill-name"],
  "hooks": "./hooks/hooks.json",
  "mcp": "./.mcp.json"
}
```

**Important:** Use kebab-case for plugin names (e.g., "my-plugin", not "my plugin").

## Plugin Creation Process

Follow this systematic process to create effective plugins:

### Step 1: Define Plugin Scope and Components

Before creating a plugin, clearly identify:

1. **Purpose**: What problem does this plugin solve?
2. **Components needed**: Which components (commands, agents, hooks, skills, MCP) are required?
3. **User workflows**: How will users interact with this plugin?
4. **Distribution**: Will this be shared via marketplace or kept private?

Ask clarifying questions to understand:
- What commands should users be able to run?
- What automated capabilities should Claude have?
- What events should trigger actions?
- What external tools or APIs need integration?

### Step 2: Initialize Plugin Structure

Use the `init_plugin.py` script to create a new plugin with proper structure:

```bash
python scripts/init_plugin.py <plugin-name> --path <output-directory>
```

Options:
- `--commands`: Include commands directory
- `--agents`: Include agents directory
- `--skills`: Include skills directory
- `--hooks`: Include hooks directory
- `--mcp`: Include MCP configuration

The script creates:
- Proper directory structure based on selected components
- `plugin.json` with metadata template
- Example files for each component type
- README.md with basic documentation

### Step 3: Implement Plugin Components

Implement each component based on your plugin's requirements:

#### Creating Custom Commands

Commands are markdown files in the `commands/` directory that define slash commands.

**File naming**: `command-name.md` creates `/command-name` command

**Command structure**:
```markdown
---
description: Brief description shown in command list
---

# Command Instructions

When this command is invoked, perform the following actions:

1. First step
2. Second step
3. Third step

## Parameters

Commands can accept parameters after the command name.

## Output

Describe what the command should output or do.
```

**Best practices**:
- Use clear, actionable descriptions
- Write step-by-step instructions for Claude to follow
- Document any parameters the command accepts
- Keep commands focused on a single task

#### Creating Custom Agents

Agents are defined in JSON files in the `agents/` directory.

**Agent structure**:
```json
{
  "name": "agent-name",
  "description": "What this agent does",
  "tools": ["Read", "Write", "Bash", "Grep"],
  "systemPrompt": "Specialized instructions for this agent"
}
```

**Best practices**:
- Limit tools to only what the agent needs
- Provide clear, specific system prompts
- Define when the agent should be used
- Consider agent autonomy level

#### Creating Skills

Skills are subdirectories within `skills/` containing a `SKILL.md` file.

For comprehensive skill creation guidance, refer to the `skill-creator` skill or use:
```bash
python scripts/init_skill.py <skill-name> --path ./skills
```

Skills can include:
- `SKILL.md` with metadata and instructions
- `scripts/` for executable code
- `references/` for documentation
- `assets/` for templates and resources

#### Configuring Hooks

Hooks respond to events like tool calls or user actions.

**hooks.json structure**:
```json
{
  "onToolCall": {
    "Read": "echo 'File was read'",
    "Write": "echo 'File was written'"
  },
  "onUserPromptSubmit": "echo 'User submitted prompt'"
}
```

**Available hooks**:
- `onToolCall`: Triggers when specific tools are used
- `onUserPromptSubmit`: Triggers when user submits a prompt
- `onSessionStart`: Triggers at session start
- `onSessionEnd`: Triggers at session end

#### Integrating MCP Servers

MCP (Model Context Protocol) servers provide external tool integrations.

**.mcp.json structure**:
```json
{
  "servers": {
    "server-name": {
      "command": "node",
      "args": ["path/to/server.js"],
      "env": {
        "API_KEY": "${API_KEY}"
      }
    }
  }
}
```

### Step 4: Configure Plugin Metadata

Update `plugin.json` with accurate metadata:

1. **name**: Use kebab-case (e.g., "my-plugin")
2. **version**: Follow semantic versioning (1.0.0)
3. **description**: Clear, concise description of functionality
4. **author**: Your name and contact information
5. **components**: List paths to commands, agents, skills, hooks, MCP

Ensure all component paths in `plugin.json` match actual directory structure.

### Step 5: Document the Plugin

Create or update `README.md` to include:

1. **Overview**: What the plugin does
2. **Installation**: How to install from marketplace
3. **Usage**: Examples of commands and features
4. **Components**: List of included commands, agents, skills
5. **Configuration**: Any required setup or API keys
6. **Examples**: Common use cases and workflows

### Step 6: Validate and Package

Use the `package_plugin.py` script to validate and package your plugin:

```bash
python scripts/package_plugin.py <path/to/plugin-directory>
```

The script:
1. **Validates** plugin structure and metadata
2. **Checks** all component references are valid
3. **Verifies** naming conventions (kebab-case)
4. **Packages** into a distributable zip file

Fix any validation errors before distribution.

### Step 7: Test the Plugin

Test your plugin thoroughly:

1. **Install locally**: Add plugin to local marketplace
2. **Test commands**: Run each slash command
3. **Verify skills**: Ensure skills trigger appropriately
4. **Check hooks**: Confirm hooks respond to events
5. **Test integrations**: Verify MCP servers connect properly

Iterate based on testing results.

### Step 8: Distribute via Marketplace

To share via marketplace:

1. **Create marketplace.json** in `.claude-plugin/` directory:
```json
{
  "name": "marketplace-name",
  "owner": {
    "name": "Your Name",
    "email": "your@email.com"
  },
  "metadata": {
    "description": "Marketplace description",
    "version": "1.0.0"
  },
  "plugins": [
    {
      "name": "plugin-name",
      "description": "Plugin description",
      "source": "./",
      "strict": false,
      "commands": ["./commands"],
      "skills": ["./skills/skill-name"]
    }
  ]
}
```

2. **Publish to repository**: Push to GitHub or other Git hosting
3. **Share URL**: Users can add with `/plugin marketplace add <url>`

## Best Practices

### Naming Conventions
- **Plugins**: Use kebab-case (e.g., "api-helper")
- **Commands**: Use kebab-case (e.g., "deploy-app")
- **Skills**: Use kebab-case (e.g., "data-analyzer")
- **Files**: Follow component conventions

### Component Organization
- Keep related functionality together
- Separate concerns (commands vs skills vs hooks)
- Use skills for autonomous capabilities
- Use commands for user-initiated actions

### Documentation
- Write clear descriptions for all components
- Provide usage examples
- Document configuration requirements
- Include troubleshooting guidance

### Versioning
- Follow semantic versioning (MAJOR.MINOR.PATCH)
- Document breaking changes
- Maintain backward compatibility when possible
- Update version in plugin.json

### Testing
- Test all commands with various inputs
- Verify skill triggering logic
- Check hook event handling
- Validate MCP integrations
- Test on fresh installations

## Using Plugin Creation Scripts

### Initialize New Plugin

```bash
python scripts/init_plugin.py my-plugin --path ./plugins --commands --skills
```

Creates a new plugin with commands and skills directories.

### Initialize New Skill (within plugin)

```bash
python scripts/init_skill.py my-skill --path ./my-plugin/skills
```

Creates a new skill within an existing plugin.

### Package Plugin

```bash
python scripts/package_plugin.py ./my-plugin
```

Validates and packages the plugin for distribution.

### Validate Plugin Only

```bash
python scripts/package_plugin.py ./my-plugin --validate-only
```

Validates plugin structure without creating package.

## Common Patterns

### Command + Skill Combination

Create a command that users invoke, backed by a skill that provides the knowledge:

- **Command**: `/analyze-code` - User-facing command
- **Skill**: `code-analyzer` - Provides analysis methodology and tools

### Multi-Component Plugin

Combine multiple components for comprehensive functionality:

- **Commands**: User-initiated actions
- **Skills**: Autonomous capabilities
- **Hooks**: Automated responses
- **MCP**: External tool integrations

### Marketplace Plugin Collection

Create a marketplace with multiple related plugins:

```
marketplace-name/
├── .claude-plugin/
│   └── marketplace.json
├── plugin-one/
├── plugin-two/
└── plugin-three/
```

## Troubleshooting

### "Plugin name cannot contain spaces"
- Use kebab-case for all plugin names in marketplace.json
- Example: "my-plugin" not "my plugin"

### "Invalid plugin structure"
- Ensure plugin.json exists in .claude-plugin/ directory
- Verify all referenced components exist
- Check JSON syntax validity

### "Skill not triggering"
- Review skill description in YAML frontmatter
- Ensure description clearly indicates when to use
- Check skill is listed in plugin.json

### "Command not found"
- Verify command file is in commands/ directory
- Check plugin.json lists commands directory
- Ensure .md file name matches command name

## References

For more detailed information, refer to:
- `references/plugin-schema.md` - Complete plugin.json schema
- `references/command-format.md` - Command file format specification
- `references/marketplace-config.md` - Marketplace configuration guide
