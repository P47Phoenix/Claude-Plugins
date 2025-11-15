#!/usr/bin/env python3
"""
Agent Registry - Dynamic agent discovery and assignment based on task requirements.

This module provides:
- Agent registration with capability tagging
- Dynamic agent selection based on task similarity
- Agent pool management
- Load balancing and availability tracking
- Hot-reload of new agents without system restart
"""

import json
import sqlite3
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum
from pathlib import Path


class AgentType(Enum):
    """Types of agents available."""
    TASK = "task"  # Task-specific agent from Claude Code
    GENERAL = "general"  # General-purpose Claude agent
    SPECIALIZED = "specialized"  # Custom specialized agent
    EXTERNAL = "external"  # External API/service


class AgentStatus(Enum):
    """Agent availability status."""
    AVAILABLE = "available"
    BUSY = "busy"
    OFFLINE = "offline"
    DISABLED = "disabled"


@dataclass
class AgentCapability:
    """Represents an agent's capability."""
    name: str
    description: str
    tags: List[str]
    confidence: float  # 0.0 to 1.0


@dataclass
class AgentDescriptor:
    """Complete agent description."""
    agent_id: str
    agent_type: AgentType
    name: str
    description: str
    capabilities: List[AgentCapability]
    status: AgentStatus
    config: Dict[str, Any]
    metadata: Dict[str, Any]


class AgentRegistry:
    """
    Registry for managing available agents and dynamic assignment.

    Automatically discovers agents from:
    - Claude Code Task agents
    - Custom plugin agents
    - External services
    - Local agent definitions
    """

    def __init__(self, db_path: str = "agentic_flows.db"):
        """Initialize agent registry with database connection."""
        self.db_path = Path(db_path)
        self.conn = sqlite3.connect(str(self.db_path))
        self.conn.row_factory = sqlite3.Row
        self._create_schema()
        self._load_default_agents()

    def _create_schema(self):
        """Create agent registry schema."""
        cursor = self.conn.cursor()

        # Agents table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS agents (
                agent_id TEXT PRIMARY KEY,
                agent_type TEXT NOT NULL,
                name TEXT NOT NULL,
                description TEXT,
                status TEXT DEFAULT 'available',
                config JSON,
                metadata JSON,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Agent capabilities table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS agent_capabilities (
                capability_id TEXT PRIMARY KEY,
                agent_id TEXT NOT NULL,
                name TEXT NOT NULL,
                description TEXT,
                tags JSON,  -- Array of capability tags
                confidence REAL DEFAULT 1.0,
                FOREIGN KEY (agent_id) REFERENCES agents(agent_id) ON DELETE CASCADE
            )
        """)
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_agent_caps ON agent_capabilities(agent_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_cap_tags ON agent_capabilities(tags)")

        # Agent assignments - track which agent is assigned to which node execution
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS agent_assignments (
                assignment_id TEXT PRIMARY KEY,
                execution_id TEXT NOT NULL,
                node_id TEXT NOT NULL,
                agent_id TEXT NOT NULL,
                assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                completed_at TIMESTAMP,
                success BOOLEAN,
                performance_score REAL,
                FOREIGN KEY (agent_id) REFERENCES agents(agent_id) ON DELETE CASCADE
            )
        """)
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_assignments_exec ON agent_assignments(execution_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_assignments_agent ON agent_assignments(agent_id)")

        self.conn.commit()

    def _load_default_agents(self):
        """Load default Claude agents."""
        import uuid

        # Check if default agents already loaded
        cursor = self.conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM agents WHERE agent_type = 'general'")
        if cursor.fetchone()[0] > 0:
            return  # Already loaded

        # Add default Claude models as agents
        default_agents = [
            {
                "agent_id": str(uuid.uuid4()),
                "agent_type": "general",
                "name": "claude-sonnet",
                "description": "Claude Sonnet - Fast, balanced model for most tasks",
                "config": {"model": "claude-sonnet-4-5-20250929"},
                "capabilities": [
                    {
                        "name": "general_reasoning",
                        "description": "General-purpose reasoning and problem solving",
                        "tags": ["reasoning", "analysis", "planning", "writing"]
                    },
                    {
                        "name": "code_generation",
                        "description": "Writing and reviewing code",
                        "tags": ["coding", "programming", "debugging"]
                    },
                    {
                        "name": "data_analysis",
                        "description": "Analyzing and interpreting data",
                        "tags": ["analysis", "data", "statistics"]
                    }
                ]
            },
            {
                "agent_id": str(uuid.uuid4()),
                "agent_type": "general",
                "name": "claude-haiku",
                "description": "Claude Haiku - Fast, cost-effective for simple tasks",
                "config": {"model": "claude-haiku-4-20250514"},
                "capabilities": [
                    {
                        "name": "quick_tasks",
                        "description": "Fast completion of straightforward tasks",
                        "tags": ["simple", "quick", "classification", "extraction"],
                        "confidence": 0.8
                    }
                ]
            },
            {
                "agent_id": str(uuid.uuid4()),
                "agent_type": "general",
                "name": "claude-opus",
                "description": "Claude Opus - Most capable for complex tasks",
                "config": {"model": "claude-opus-4-20250514"},
                "capabilities": [
                    {
                        "name": "complex_reasoning",
                        "description": "Advanced reasoning and problem solving",
                        "tags": ["complex", "reasoning", "research", "analysis"],
                        "confidence": 1.0
                    },
                    {
                        "name": "creative_tasks",
                        "description": "Creative writing and content generation",
                        "tags": ["creative", "writing", "storytelling"],
                        "confidence": 1.0
                    }
                ]
            }
        ]

        for agent_def in default_agents:
            self.register_agent(
                agent_type=AgentType(agent_def["agent_type"]),
                name=agent_def["name"],
                description=agent_def["description"],
                config=agent_def["config"],
                capabilities=agent_def["capabilities"],
                agent_id=agent_def["agent_id"]
            )

    def register_agent(self, agent_type: AgentType, name: str, description: str,
                      capabilities: List[Dict], config: Dict = None,
                      metadata: Dict = None, agent_id: str = None) -> str:
        """
        Register a new agent in the registry.

        Args:
            agent_type: Type of agent
            name: Agent name
            description: Agent description
            capabilities: List of capability dicts with name, description, tags
            config: Agent configuration
            metadata: Additional metadata
            agent_id: Optional custom agent ID

        Returns:
            agent_id
        """
        import uuid

        agent_id = agent_id or str(uuid.uuid4())
        cursor = self.conn.cursor()

        # Insert agent
        cursor.execute("""
            INSERT OR REPLACE INTO agents (agent_id, agent_type, name, description, config, metadata)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (agent_id, agent_type.value, name, description,
              json.dumps(config or {}), json.dumps(metadata or {})))

        # Insert capabilities
        for cap in capabilities:
            cap_id = str(uuid.uuid4())
            cursor.execute("""
                INSERT INTO agent_capabilities (capability_id, agent_id, name, description, tags, confidence)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (cap_id, agent_id, cap['name'], cap.get('description', ''),
                  json.dumps(cap.get('tags', [])), cap.get('confidence', 1.0)))

        self.conn.commit()
        return agent_id

    def discover_task_agents(self) -> List[str]:
        """
        Discover available Task agents from Claude Code.

        Returns:
            List of newly registered agent IDs
        """
        import subprocess
        import uuid

        # In a real implementation, this would query Claude Code's agent registry
        # For now, we'll simulate discovering some task agents

        # Example: Query for available agents (would use actual Claude Code API)
        # result = subprocess.run(['claude', 'agent', 'list'], capture_output=True)

        # Simulated discovered agents
        discovered_agents = []

        # Check if we already have task agents
        cursor = self.conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM agents WHERE agent_type = 'task'")
        if cursor.fetchone()[0] > 0:
            return []  # Already discovered

        # Simulated task agents that might be available
        task_agents = [
            {
                "name": "code-reviewer",
                "description": "Reviews code for quality, security, and best practices",
                "capabilities": [
                    {
                        "name": "code_review",
                        "description": "Code quality and security review",
                        "tags": ["code", "review", "security", "quality"]
                    }
                ]
            },
            {
                "name": "test-runner",
                "description": "Runs and analyzes test suites",
                "capabilities": [
                    {
                        "name": "test_execution",
                        "description": "Execute and analyze tests",
                        "tags": ["testing", "qa", "validation"]
                    }
                ]
            }
        ]

        for task_agent in task_agents:
            agent_id = self.register_agent(
                agent_type=AgentType.TASK,
                name=task_agent["name"],
                description=task_agent["description"],
                capabilities=task_agent["capabilities"],
                config={"source": "claude_code_task"}
            )
            discovered_agents.append(agent_id)

        return discovered_agents

    def find_best_agent(self, task_description: str, required_tags: List[str] = None,
                       prefer_agent_type: AgentType = None) -> Optional[AgentDescriptor]:
        """
        Find the best agent for a given task based on capability matching.

        Args:
            task_description: Description of the task
            required_tags: Optional list of required capability tags
            prefer_agent_type: Optional preference for agent type

        Returns:
            AgentDescriptor for best match or None
        """
        cursor = self.conn.cursor()

        # Get all available agents with their capabilities
        cursor.execute("""
            SELECT
                a.*,
                json_group_array(
                    json_object(
                        'capability_id', ac.capability_id,
                        'name', ac.name,
                        'description', ac.description,
                        'tags', ac.tags,
                        'confidence', ac.confidence
                    )
                ) as capabilities_json
            FROM agents a
            LEFT JOIN agent_capabilities ac ON a.agent_id = ac.agent_id
            WHERE a.status = 'available'
            GROUP BY a.agent_id
        """)

        agents = cursor.fetchall()
        scored_agents = []

        for agent_row in agents:
            agent = dict(agent_row)
            capabilities = json.loads(agent['capabilities_json'])

            # Skip if wrong type preference
            if prefer_agent_type and agent['agent_type'] != prefer_agent_type.value:
                continue

            # Calculate match score
            score = self._calculate_agent_score(
                task_description, required_tags, capabilities
            )

            if score > 0:
                scored_agents.append((score, agent, capabilities))

        if not scored_agents:
            return None

        # Sort by score (descending)
        scored_agents.sort(key=lambda x: x[0], reverse=True)

        # Return best match
        best_score, best_agent, best_caps = scored_agents[0]

        return AgentDescriptor(
            agent_id=best_agent['agent_id'],
            agent_type=AgentType(best_agent['agent_type']),
            name=best_agent['name'],
            description=best_agent['description'],
            capabilities=[
                AgentCapability(
                    name=cap['name'],
                    description=cap['description'],
                    tags=json.loads(cap['tags']),
                    confidence=cap['confidence']
                ) for cap in best_caps if cap['capability_id']
            ],
            status=AgentStatus(best_agent['status']),
            config=json.loads(best_agent['config']),
            metadata=json.loads(best_agent['metadata'])
        )

    def _calculate_agent_score(self, task_description: str,
                              required_tags: List[str],
                              capabilities: List[Dict]) -> float:
        """
        Calculate how well an agent matches a task.

        Scoring:
        - Required tag match: +1.0 per tag
        - Task description keyword match: +0.5 per keyword
        - Confidence multiplier: capabilities' confidence values
        """
        score = 0.0
        task_lower = task_description.lower()

        for cap in capabilities:
            if not cap.get('capability_id'):  # Skip null capabilities
                continue

            cap_tags = json.loads(cap['tags'])
            confidence = cap['confidence']

            # Check required tags
            if required_tags:
                matching_tags = set(required_tags) & set(cap_tags)
                score += len(matching_tags) * confidence

            # Check task description keywords
            cap_desc = (cap['description'] or '').lower()
            cap_name = cap['name'].lower()

            # Simple keyword matching
            keywords = task_lower.split()
            for keyword in keywords:
                if len(keyword) > 3:  # Skip short words
                    if keyword in cap_desc or keyword in cap_name:
                        score += 0.5 * confidence

            # Tag presence in task description
            for tag in cap_tags:
                if tag.lower() in task_lower:
                    score += 0.3 * confidence

        return score

    def assign_agent(self, execution_id: str, node_id: str, agent_id: str) -> str:
        """
        Record an agent assignment to a node execution.

        Args:
            execution_id: Execution ID
            node_id: Node ID
            agent_id: Agent ID to assign

        Returns:
            assignment_id
        """
        import uuid

        assignment_id = str(uuid.uuid4())
        cursor = self.conn.cursor()

        cursor.execute("""
            INSERT INTO agent_assignments (assignment_id, execution_id, node_id, agent_id)
            VALUES (?, ?, ?, ?)
        """, (assignment_id, execution_id, node_id, agent_id))

        # Update agent status to busy
        cursor.execute("""
            UPDATE agents SET status = 'busy' WHERE agent_id = ?
        """, (agent_id,))

        self.conn.commit()
        return assignment_id

    def complete_assignment(self, assignment_id: str, success: bool,
                           performance_score: float = None):
        """
        Mark an assignment as completed and update agent status.

        Args:
            assignment_id: Assignment ID
            success: Whether assignment was successful
            performance_score: Optional performance score (0.0-1.0)
        """
        cursor = self.conn.cursor()

        # Update assignment
        cursor.execute("""
            UPDATE agent_assignments
            SET completed_at = CURRENT_TIMESTAMP, success = ?, performance_score = ?
            WHERE assignment_id = ?
        """, (success, performance_score, assignment_id))

        # Get agent_id
        cursor.execute("""
            SELECT agent_id FROM agent_assignments WHERE assignment_id = ?
        """, (assignment_id,))
        result = cursor.fetchone()

        if result:
            agent_id = result['agent_id']
            # Set agent back to available
            cursor.execute("""
                UPDATE agents SET status = 'available' WHERE agent_id = ?
            """, (agent_id,))

        self.conn.commit()

    def get_agent_performance(self, agent_id: str) -> Dict:
        """
        Get performance statistics for an agent.

        Returns:
            Dict with performance metrics
        """
        cursor = self.conn.cursor()

        cursor.execute("""
            SELECT
                COUNT(*) as total_assignments,
                SUM(CASE WHEN success = 1 THEN 1 ELSE 0 END) as successful,
                AVG(performance_score) as avg_score,
                AVG(CAST((julianday(completed_at) - julianday(assigned_at)) * 24 * 60 AS REAL)) as avg_duration_minutes
            FROM agent_assignments
            WHERE agent_id = ? AND completed_at IS NOT NULL
        """, (agent_id,))

        result = dict(cursor.fetchone())
        result['success_rate'] = (result['successful'] / result['total_assignments']
                                 if result['total_assignments'] > 0 else 0.0)

        return result

    def list_agents(self, agent_type: AgentType = None,
                   status: AgentStatus = None) -> List[AgentDescriptor]:
        """
        List all registered agents with optional filtering.

        Args:
            agent_type: Optional filter by agent type
            status: Optional filter by status

        Returns:
            List of AgentDescriptor
        """
        cursor = self.conn.cursor()

        query = "SELECT * FROM agents WHERE 1=1"
        params = []

        if agent_type:
            query += " AND agent_type = ?"
            params.append(agent_type.value)

        if status:
            query += " AND status = ?"
            params.append(status.value)

        cursor.execute(query, params)
        agents = []

        for row in cursor.fetchall():
            agent = dict(row)

            # Get capabilities
            cursor.execute("""
                SELECT * FROM agent_capabilities WHERE agent_id = ?
            """, (agent['agent_id'],))
            caps = cursor.fetchall()

            agents.append(AgentDescriptor(
                agent_id=agent['agent_id'],
                agent_type=AgentType(agent['agent_type']),
                name=agent['name'],
                description=agent['description'],
                capabilities=[
                    AgentCapability(
                        name=cap['name'],
                        description=cap['description'],
                        tags=json.loads(cap['tags']),
                        confidence=cap['confidence']
                    ) for cap in caps
                ],
                status=AgentStatus(agent['status']),
                config=json.loads(agent['config']),
                metadata=json.loads(agent['metadata'])
            ))

        return agents

    def reload_agents(self):
        """
        Reload/rediscover all agents. Useful for hot-reloading new agents.
        """
        # Discover new task agents
        new_task_agents = self.discover_task_agents()

        # Could also scan for plugin-provided agents, etc.

        return {
            "new_task_agents": len(new_task_agents),
            "total_agents": len(self.list_agents())
        }

    def close(self):
        """Close database connection."""
        self.conn.close()


# Example usage
if __name__ == "__main__":
    registry = AgentRegistry("test_flows.db")

    # Discover available agents
    registry.discover_task_agents()

    # Find best agent for a task
    agent = registry.find_best_agent(
        task_description="Review this code for security vulnerabilities",
        required_tags=["code", "security"]
    )

    if agent:
        print(f"Selected agent: {agent.name}")
        print(f"Description: {agent.description}")
        print(f"Capabilities: {[cap.name for cap in agent.capabilities]}")

    # List all agents
    print("\nAll available agents:")
    for agent in registry.list_agents(status=AgentStatus.AVAILABLE):
        print(f"- {agent.name} ({agent.agent_type.value})")

    registry.close()
