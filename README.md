# Claude Plugins

A collection of plugins for [Claude Code](https://code.claude.com) that extend Claude's capabilities with specialized skills and tools.

## What are Claude Code Plugins?

Plugins extend Claude Code's functionality through custom commands, agents, hooks, Skills, and MCP servers. They're discoverable through marketplaces and shareable across teams and projects.

## Plugins in this Repository

### Skill Creator

A plugin that helps you create new Claude skills with specialized knowledge, workflows, and tools.

**Features:**
- Comprehensive skill creation guidance
- Automated skill initialization with templates
- Validation and packaging tools
- Best practices for skill design

**Included Tools:**
- `init_skill.py` - Generate new skill templates with proper structure
- `package_skill.py` - Validate and package skills for distribution
- `quick_validate.py` - Quick validation of skill structure and format

**When to use:** Creating skills for specialized domains, workflows, or bundled resources (scripts, references, assets).

### Plugin Creator

A comprehensive plugin that helps you create complete Claude Code plugins with commands, agents, hooks, skills, and MCP integrations.

**Features:**
- Complete plugin creation guidance
- Support for all plugin components (commands, agents, hooks, skills, MCP)
- Automated plugin scaffolding
- Validation and packaging tools
- Best practices for plugin architecture

**Included Tools:**
- `init_plugin.py` - Generate new plugin templates with selected components
- `package_plugin.py` - Validate and package plugins for distribution

**When to use:** Creating custom slash commands, specialized agents, event hooks, or combining multiple components into a single distributable plugin.

## Installation

### Adding the Marketplace

1. Open Claude Code
2. Run the following command to add this marketplace:
   ```
   /plugin marketplace add https://github.com/P47Phoenix/Claude-Plugins
   ```

### Installing Plugins

Once the marketplace is added, you can install either or both plugins:

**Install Skill Creator:**
```
/plugin install skill-creator
```

**Install Plugin Creator:**
```
/plugin install plugin-creator
```

**Or use the interactive menu:**
```
/plugin
```

Then browse and select the plugins you want from the list.

## Using the Skill Creator

After installation, Claude will automatically use the skill creator when you want to create or modify skills.

**Example usage:**
- "Help me create a new skill for [your use case]"
- "I want to build a skill that [describes functionality]"
- "Update the [skill-name] skill to include [new features]"

The skill creator will guide you through:
1. Understanding your skill requirements with concrete examples
2. Planning the reusable skill contents (scripts, references, assets)
3. Initializing the skill structure
4. Editing and implementing the skill
5. Packaging for distribution
6. Iterating based on testing

## Using the Plugin Creator

After installation, Claude will automatically use the plugin creator when you want to create or modify complete plugins.

**Example usage:**
- "I want to create a plugin that helps me [describes functionality]"
- "Help me build a plugin with custom commands for [use case]"
- "Create a plugin that includes [commands/agents/hooks/skills]"

The plugin creator will guide you through:
1. Defining plugin scope and components
2. Initializing plugin structure with selected components
3. Implementing commands, agents, hooks, skills, or MCP integrations
4. Configuring plugin metadata
5. Documentation and testing
6. Packaging for distribution

## Plugin Structure

This repository follows the Claude Code plugin structure:

```
.
├── .claude-plugin/
│   └── marketplace.json         # Marketplace and plugin metadata
├── skill-creator/               # The skill creator plugin
│   ├── SKILL.md                # Skill definition and instructions
│   ├── LICENSE.txt             # License information
│   └── scripts/                # Helper scripts
│       ├── init_skill.py       # Initialize new skills
│       ├── package_skill.py    # Package skills for distribution
│       └── quick_validate.py   # Validate skill structure
├── plugin-creator/              # The plugin creator plugin
│   ├── SKILL.md                # Skill definition and instructions
│   ├── LICENSE.txt             # License information
│   ├── scripts/                # Helper scripts
│   │   ├── init_plugin.py      # Initialize new plugins
│   │   └── package_plugin.py   # Validate and package plugins
│   └── references/             # Reference documentation (future)
└── README.md                   # This file
```

## Creating Your Own Plugins

To create your own plugin in this marketplace:

1. Use the skill creator to generate a new skill
2. Add the skill directory to this repository
3. Update `.claude-plugin/marketplace.json` to include the new plugin
4. Commit and push your changes

### Marketplace Configuration

The `.claude-plugin/marketplace.json` file defines:
- Marketplace name and owner information
- Available plugins and their metadata
- Skill locations and configurations

## Managing Plugins

**View installed plugins:**
```
/plugin
```

**Enable/disable plugins:**
```
/plugin disable skill-creator
/plugin enable skill-creator
/plugin disable plugin-creator
/plugin enable plugin-creator
```

**Uninstall plugins:**
```
/plugin uninstall skill-creator
/plugin uninstall plugin-creator
```

## Resources

- [Claude Code Documentation](https://code.claude.com/docs)
- [Plugin Documentation](https://code.claude.com/docs/en/plugins)
- [Skills Guide](https://code.claude.com/docs/en/skills)

## License

See individual plugin directories for license information.

## Contributing

Contributions are welcome! To add a new plugin:

1. Create your plugin following the Claude Code plugin structure
2. Test thoroughly using the skill creator validation tools
3. Add proper documentation
4. Submit a pull request

## Support

For issues or questions:
- Check the [Claude Code documentation](https://code.claude.com/docs)
- Review the skill creator guidance
- Open an issue in this repository
