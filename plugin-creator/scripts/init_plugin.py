#!/usr/bin/env python3
"""
Initialize a new Claude Code plugin with proper structure.

Usage:
    python init_plugin.py <plugin-name> --path <output-directory> [options]

Options:
    --commands      Include commands directory
    --agents        Include agents directory
    --skills        Include skills directory
    --hooks         Include hooks directory
    --mcp           Include MCP configuration
    --all           Include all component types
    --author        Author name (default: prompted)
    --email         Author email (default: prompted)
"""

import argparse
import json
import os
import sys
from pathlib import Path


def validate_plugin_name(name):
    """Validate plugin name follows kebab-case convention."""
    if ' ' in name:
        return False, "Plugin name cannot contain spaces. Use kebab-case (e.g., 'my-plugin')"
    if not name.replace('-', '').replace('_', '').isalnum():
        return False, "Plugin name can only contain letters, numbers, hyphens, and underscores"
    if name != name.lower():
        return False, "Plugin name should be lowercase"
    return True, ""


def create_plugin_json(plugin_name, author_name, author_email, components):
    """Generate plugin.json content."""
    plugin_json = {
        "name": plugin_name,
        "version": "1.0.0",
        "description": f"TODO: Add description for {plugin_name}",
        "author": {
            "name": author_name,
            "email": author_email
        }
    }

    if components['commands']:
        plugin_json['commands'] = ['./commands']
    if components['agents']:
        plugin_json['agents'] = ['./agents']
    if components['skills']:
        plugin_json['skills'] = ['./skills/example-skill']
    if components['hooks']:
        plugin_json['hooks'] = './hooks/hooks.json'
    if components['mcp']:
        plugin_json['mcp'] = './.mcp.json'

    return json.dumps(plugin_json, indent=2)


def create_example_command():
    """Generate example command markdown."""
    return """---
description: Example command that demonstrates plugin functionality
---

# Example Command

When this command is invoked, perform the following actions:

1. Greet the user
2. Explain what this command does
3. Provide an example of the functionality

## Usage

This command can be invoked with:
```
/example-command
```

## Parameters

You can extend this command to accept parameters:
```
/example-command <parameter>
```

## Implementation

Replace this content with your actual command implementation.
"""


def create_example_agent():
    """Generate example agent JSON."""
    return json.dumps({
        "name": "example-agent",
        "description": "Example agent for demonstration purposes",
        "tools": ["Read", "Write", "Grep"],
        "systemPrompt": "You are a specialized agent. Replace this with your specific instructions."
    }, indent=2)


def create_example_hooks():
    """Generate example hooks.json."""
    return json.dumps({
        "onToolCall": {
            "Read": "echo 'File read hook triggered'",
            "Write": "echo 'File write hook triggered'"
        }
    }, indent=2)


def create_example_mcp():
    """Generate example .mcp.json."""
    return json.dumps({
        "servers": {
            "example-server": {
                "command": "node",
                "args": ["path/to/server.js"],
                "env": {
                    "API_KEY": "${API_KEY}"
                }
            }
        }
    }, indent=2)


def create_readme(plugin_name, components):
    """Generate README.md content."""
    component_list = []
    if components['commands']:
        component_list.append("- **Custom Commands**: Slash commands for user-initiated actions")
    if components['agents']:
        component_list.append("- **Custom Agents**: Specialized agents for specific workflows")
    if components['skills']:
        component_list.append("- **Skills**: Autonomous capabilities with specialized knowledge")
    if components['hooks']:
        component_list.append("- **Hooks**: Event handlers for automated responses")
    if components['mcp']:
        component_list.append("- **MCP Integration**: External tool and API integrations")

    components_section = "\n".join(component_list) if component_list else "- No components configured yet"

    return f"""# {plugin_name}

TODO: Add a brief description of what this plugin does.

## Features

{components_section}

## Installation

Add this plugin to Claude Code via marketplace:

```
/plugin marketplace add <your-marketplace-url>
/plugin install {plugin_name}
```

## Usage

TODO: Provide examples of how to use this plugin.

### Commands

TODO: List available commands and their usage.

### Skills

TODO: Describe when skills will be automatically triggered.

## Configuration

TODO: Document any required configuration or API keys.

## Examples

TODO: Provide common use cases and example workflows.

## Development

### Structure

```
{plugin_name}/
├── .claude-plugin/
│   └── plugin.json
{('├── commands/' if components['commands'] else '')}
{('├── agents/' if components['agents'] else '')}
{('├── skills/' if components['skills'] else '')}
{('├── hooks/' if components['hooks'] else '')}
{('└── .mcp.json' if components['mcp'] else '')}
```

### Testing

TODO: Describe how to test this plugin.

## License

TODO: Add license information.

## Contributing

TODO: Add contribution guidelines.
"""


def init_plugin(plugin_name, output_path, components, author_name, author_email):
    """Initialize a new plugin with specified components."""

    # Validate plugin name
    valid, error_msg = validate_plugin_name(plugin_name)
    if not valid:
        print(f"Error: {error_msg}")
        return False

    # Create plugin directory
    plugin_dir = Path(output_path) / plugin_name
    if plugin_dir.exists():
        print(f"Error: Directory {plugin_dir} already exists")
        return False

    try:
        # Create base structure
        plugin_dir.mkdir(parents=True)
        claude_plugin_dir = plugin_dir / '.claude-plugin'
        claude_plugin_dir.mkdir()

        # Create plugin.json
        plugin_json_path = claude_plugin_dir / 'plugin.json'
        plugin_json_path.write_text(
            create_plugin_json(plugin_name, author_name, author_email, components)
        )
        print(f"✓ Created {plugin_json_path}")

        # Create component directories and examples
        if components['commands']:
            commands_dir = plugin_dir / 'commands'
            commands_dir.mkdir()
            example_cmd = commands_dir / 'example-command.md'
            example_cmd.write_text(create_example_command())
            print(f"✓ Created {commands_dir}/ with example command")

        if components['agents']:
            agents_dir = plugin_dir / 'agents'
            agents_dir.mkdir()
            example_agent = agents_dir / 'example-agent.json'
            example_agent.write_text(create_example_agent())
            print(f"✓ Created {agents_dir}/ with example agent")

        if components['skills']:
            skills_dir = plugin_dir / 'skills' / 'example-skill'
            skills_dir.mkdir(parents=True)
            skill_md = skills_dir / 'SKILL.md'
            skill_md.write_text("""---
name: example-skill
description: TODO: Add description of when this skill should be used
---

# Example Skill

TODO: Add skill implementation here.

## Usage

This skill will be triggered when...

## Resources

- scripts/ - Executable code
- references/ - Documentation
- assets/ - Templates and resources
""")
            print(f"✓ Created {skills_dir}/ with example skill")

        if components['hooks']:
            hooks_dir = plugin_dir / 'hooks'
            hooks_dir.mkdir()
            hooks_json = hooks_dir / 'hooks.json'
            hooks_json.write_text(create_example_hooks())
            print(f"✓ Created {hooks_dir}/ with example hooks")

        if components['mcp']:
            mcp_json = plugin_dir / '.mcp.json'
            mcp_json.write_text(create_example_mcp())
            print(f"✓ Created {mcp_json}")

        # Create README
        readme_path = plugin_dir / 'README.md'
        readme_path.write_text(create_readme(plugin_name, components))
        print(f"✓ Created {readme_path}")

        print(f"\n✓ Successfully initialized plugin: {plugin_name}")
        print(f"  Location: {plugin_dir}")
        print(f"\nNext steps:")
        print(f"  1. Edit {plugin_json_path} to update description and metadata")
        print(f"  2. Implement your plugin components")
        print(f"  3. Update README.md with documentation")
        print(f"  4. Run package_plugin.py to validate and package")

        return True

    except Exception as e:
        print(f"Error creating plugin: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description='Initialize a new Claude Code plugin',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Create plugin with commands and skills
  python init_plugin.py my-plugin --path ./plugins --commands --skills

  # Create plugin with all components
  python init_plugin.py my-plugin --path ./plugins --all

  # Create minimal plugin
  python init_plugin.py my-plugin --path ./plugins --skills
"""
    )

    parser.add_argument('plugin_name', help='Name of the plugin (use kebab-case)')
    parser.add_argument('--path', default='.', help='Output directory (default: current directory)')
    parser.add_argument('--commands', action='store_true', help='Include commands directory')
    parser.add_argument('--agents', action='store_true', help='Include agents directory')
    parser.add_argument('--skills', action='store_true', help='Include skills directory')
    parser.add_argument('--hooks', action='store_true', help='Include hooks directory')
    parser.add_argument('--mcp', action='store_true', help='Include MCP configuration')
    parser.add_argument('--all', action='store_true', help='Include all component types')
    parser.add_argument('--author', help='Author name')
    parser.add_argument('--email', help='Author email')

    args = parser.parse_args()

    # If --all specified, enable all components
    if args.all:
        components = {
            'commands': True,
            'agents': True,
            'skills': True,
            'hooks': True,
            'mcp': True
        }
    else:
        components = {
            'commands': args.commands,
            'agents': args.agents,
            'skills': args.skills,
            'hooks': args.hooks,
            'mcp': args.mcp
        }

    # Ensure at least one component is selected
    if not any(components.values()):
        print("Error: At least one component type must be specified")
        print("Use --commands, --agents, --skills, --hooks, --mcp, or --all")
        sys.exit(1)

    # Get author info
    author_name = args.author or input("Author name: ").strip()
    author_email = args.email or input("Author email: ").strip()

    if not author_name or not author_email:
        print("Error: Author name and email are required")
        sys.exit(1)

    # Initialize plugin
    success = init_plugin(args.plugin_name, args.path, components, author_name, author_email)
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
