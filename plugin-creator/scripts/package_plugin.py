#!/usr/bin/env python3
"""
Validate and package Claude Code plugins for distribution.

Usage:
    python package_plugin.py <plugin-directory> [output-directory]
    python package_plugin.py <plugin-directory> --validate-only

Examples:
    python package_plugin.py ./my-plugin
    python package_plugin.py ./my-plugin ./dist
    python package_plugin.py ./my-plugin --validate-only
"""

import argparse
import json
import sys
import zipfile
from pathlib import Path


class PluginValidator:
    """Validates Claude Code plugin structure and metadata."""

    def __init__(self, plugin_path):
        self.plugin_path = Path(plugin_path)
        self.errors = []
        self.warnings = []

    def validate(self):
        """Run all validation checks."""
        self.check_plugin_directory()
        self.check_plugin_json()
        self.check_components()
        return len(self.errors) == 0

    def check_plugin_directory(self):
        """Validate plugin directory structure."""
        if not self.plugin_path.exists():
            self.errors.append(f"Plugin directory does not exist: {self.plugin_path}")
            return

        if not self.plugin_path.is_dir():
            self.errors.append(f"Plugin path is not a directory: {self.plugin_path}")
            return

        # Check for .claude-plugin directory
        claude_plugin_dir = self.plugin_path / '.claude-plugin'
        if not claude_plugin_dir.exists():
            self.errors.append("Missing .claude-plugin/ directory")
            return

        if not claude_plugin_dir.is_dir():
            self.errors.append(".claude-plugin exists but is not a directory")

    def check_plugin_json(self):
        """Validate plugin.json file."""
        plugin_json_path = self.plugin_path / '.claude-plugin' / 'plugin.json'

        if not plugin_json_path.exists():
            self.errors.append("Missing .claude-plugin/plugin.json file")
            return

        try:
            with open(plugin_json_path, 'r', encoding='utf-8') as f:
                plugin_json = json.load(f)
        except json.JSONDecodeError as e:
            self.errors.append(f"Invalid JSON in plugin.json: {e}")
            return
        except Exception as e:
            self.errors.append(f"Error reading plugin.json: {e}")
            return

        # Validate required fields
        required_fields = ['name', 'version', 'description']
        for field in required_fields:
            if field not in plugin_json:
                self.errors.append(f"Missing required field in plugin.json: {field}")

        # Validate name format (kebab-case)
        if 'name' in plugin_json:
            name = plugin_json['name']
            if ' ' in name:
                self.errors.append(
                    f"Plugin name cannot contain spaces: '{name}'. Use kebab-case (e.g., 'my-plugin')"
                )
            if name != name.lower():
                self.warnings.append(f"Plugin name should be lowercase: '{name}'")

        # Validate version format
        if 'version' in plugin_json:
            version = plugin_json['version']
            parts = version.split('.')
            if len(parts) != 3 or not all(p.isdigit() for p in parts):
                self.warnings.append(
                    f"Version should follow semantic versioning (e.g., '1.0.0'): '{version}'"
                )

        # Validate description
        if 'description' in plugin_json:
            desc = plugin_json['description']
            if desc.startswith('TODO:') or len(desc) < 10:
                self.warnings.append("Plugin description should be updated with meaningful content")

        # Validate author info
        if 'author' in plugin_json:
            author = plugin_json['author']
            if not isinstance(author, dict):
                self.warnings.append("Author should be an object with 'name' and 'email' fields")
            elif 'name' not in author or 'email' not in author:
                self.warnings.append("Author object should include both 'name' and 'email'")

        self.plugin_json = plugin_json

    def check_components(self):
        """Validate referenced components exist."""
        if not hasattr(self, 'plugin_json'):
            return  # Skip if plugin.json validation failed

        plugin_json = self.plugin_json

        # Check commands
        if 'commands' in plugin_json:
            for cmd_path in plugin_json['commands']:
                full_path = self.plugin_path / cmd_path
                if not full_path.exists():
                    self.errors.append(f"Commands directory does not exist: {cmd_path}")
                elif full_path.is_dir():
                    # Check if directory contains .md files
                    md_files = list(full_path.glob('*.md'))
                    if not md_files:
                        self.warnings.append(f"Commands directory is empty: {cmd_path}")

        # Check agents
        if 'agents' in plugin_json:
            for agent_path in plugin_json['agents']:
                full_path = self.plugin_path / agent_path
                if not full_path.exists():
                    self.errors.append(f"Agents directory does not exist: {agent_path}")
                elif full_path.is_dir():
                    # Check if directory contains .json files
                    json_files = list(full_path.glob('*.json'))
                    if not json_files:
                        self.warnings.append(f"Agents directory is empty: {agent_path}")

        # Check skills
        if 'skills' in plugin_json:
            for skill_path in plugin_json['skills']:
                full_path = self.plugin_path / skill_path
                if not full_path.exists():
                    self.errors.append(f"Skill directory does not exist: {skill_path}")
                else:
                    # Check for SKILL.md
                    skill_md = full_path / 'SKILL.md'
                    if not skill_md.exists():
                        self.errors.append(f"Skill missing SKILL.md file: {skill_path}")
                    else:
                        self.validate_skill_md(skill_md, skill_path)

        # Check hooks
        if 'hooks' in plugin_json:
            hooks_path = self.plugin_path / plugin_json['hooks']
            if not hooks_path.exists():
                self.errors.append(f"Hooks file does not exist: {plugin_json['hooks']}")
            else:
                try:
                    with open(hooks_path, 'r', encoding='utf-8') as f:
                        json.load(f)
                except json.JSONDecodeError as e:
                    self.errors.append(f"Invalid JSON in hooks file: {e}")

        # Check MCP config
        if 'mcp' in plugin_json:
            mcp_path = self.plugin_path / plugin_json['mcp']
            if not mcp_path.exists():
                self.errors.append(f"MCP config file does not exist: {plugin_json['mcp']}")
            else:
                try:
                    with open(mcp_path, 'r', encoding='utf-8') as f:
                        json.load(f)
                except json.JSONDecodeError as e:
                    self.errors.append(f"Invalid JSON in MCP config: {e}")

    def validate_skill_md(self, skill_md_path, skill_path):
        """Validate SKILL.md file format."""
        try:
            with open(skill_md_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Check for YAML frontmatter
            if not content.startswith('---'):
                self.errors.append(f"Skill missing YAML frontmatter: {skill_path}")
                return

            # Extract frontmatter
            parts = content.split('---', 2)
            if len(parts) < 3:
                self.errors.append(f"Invalid YAML frontmatter format: {skill_path}")
                return

            # Simple check for required fields
            frontmatter = parts[1]
            if 'name:' not in frontmatter:
                self.errors.append(f"Skill frontmatter missing 'name' field: {skill_path}")
            if 'description:' not in frontmatter:
                self.errors.append(f"Skill frontmatter missing 'description' field: {skill_path}")

            # Check body is not empty
            body = parts[2].strip()
            if not body or len(body) < 50:
                self.warnings.append(f"Skill body is very short: {skill_path}")

        except Exception as e:
            self.errors.append(f"Error reading SKILL.md in {skill_path}: {e}")

    def print_results(self):
        """Print validation results."""
        if self.errors:
            print("\n❌ Validation failed with errors:\n")
            for error in self.errors:
                print(f"  ❌ {error}")

        if self.warnings:
            print("\n⚠️  Warnings:\n")
            for warning in self.warnings:
                print(f"  ⚠️  {warning}")

        if not self.errors and not self.warnings:
            print("\n✓ Plugin validation passed!")

        return len(self.errors) == 0


def package_plugin(plugin_path, output_dir=None):
    """Package plugin into a zip file."""
    plugin_path = Path(plugin_path)
    plugin_name = plugin_path.name

    # Determine output path
    if output_dir:
        output_path = Path(output_dir) / f"{plugin_name}.zip"
        Path(output_dir).mkdir(parents=True, exist_ok=True)
    else:
        output_path = plugin_path.parent / f"{plugin_name}.zip"

    # Create zip file
    try:
        with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # Add all files in plugin directory
            for file_path in plugin_path.rglob('*'):
                if file_path.is_file():
                    # Skip common non-essential files
                    if file_path.name in ['.DS_Store', 'Thumbs.db', '.gitignore']:
                        continue
                    # Skip __pycache__ and .pyc files
                    if '__pycache__' in file_path.parts or file_path.suffix == '.pyc':
                        continue

                    # Calculate archive path
                    arcname = file_path.relative_to(plugin_path.parent)
                    zipf.write(file_path, arcname)

        print(f"\n✓ Plugin packaged successfully!")
        print(f"  Output: {output_path}")
        print(f"  Size: {output_path.stat().st_size / 1024:.1f} KB")
        return True

    except Exception as e:
        print(f"\n❌ Error packaging plugin: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description='Validate and package Claude Code plugins',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Validate and package plugin
  python package_plugin.py ./my-plugin

  # Package to specific directory
  python package_plugin.py ./my-plugin ./dist

  # Validate only (no packaging)
  python package_plugin.py ./my-plugin --validate-only
"""
    )

    parser.add_argument('plugin_path', help='Path to plugin directory')
    parser.add_argument('output_dir', nargs='?', help='Output directory for package (optional)')
    parser.add_argument('--validate-only', action='store_true',
                        help='Only validate, do not create package')

    args = parser.parse_args()

    # Validate plugin
    print(f"Validating plugin: {args.plugin_path}\n")
    validator = PluginValidator(args.plugin_path)
    is_valid = validator.validate()
    validator.print_results()

    if not is_valid:
        print("\n❌ Fix validation errors before packaging")
        sys.exit(1)

    # Package if requested
    if not args.validate_only:
        if not package_plugin(args.plugin_path, args.output_dir):
            sys.exit(1)
    else:
        print("\n✓ Validation complete (no package created)")

    sys.exit(0)


if __name__ == '__main__':
    main()
