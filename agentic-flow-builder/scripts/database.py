#!/usr/bin/env python3
"""
SQLite database schema and data access layer for agentic flow management.

This module provides persistent storage for:
- Agent tree nodes and hierarchical relationships
- Task states and execution history
- Business rules and gate conditions
- Dual memory systems (episodic + working)
- Comprehensive audit logs
"""

import sqlite3
import json
import uuid
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
from enum import Enum


class NodeType(Enum):
    """Types of nodes in the agent tree."""
    ROOT = "root"
    AGENT = "agent"  # LLM-capable reasoning node
    CONTROL_FLOW = "control_flow"  # Orchestration node
    GATE = "gate"  # Business rule decision point


class NodeStatus(Enum):
    """Execution status of a node."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    BLOCKED = "blocked"  # Waiting on gate evaluation
    SKIPPED = "skipped"  # Skipped due to gate condition


class GateStatus(Enum):
    """Status of gate evaluation."""
    PASS = "pass"
    FAIL = "fail"
    PENDING = "pending"


class FlowDatabase:
    """Database manager for agentic flow storage."""

    def __init__(self, db_path: str = "agentic_flows.db"):
        """Initialize database connection and create schema if needed."""
        self.db_path = Path(db_path)
        self.conn = sqlite3.connect(str(self.db_path))
        self.conn.row_factory = sqlite3.Row  # Enable column access by name
        self._create_schema()

    def _create_schema(self):
        """Create database schema for agentic flows."""
        cursor = self.conn.cursor()

        # Flows table - top-level flow definitions
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS flows (
                flow_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                metadata JSON
            )
        """)

        # Nodes table - hierarchical agent tree structure
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS nodes (
                node_id TEXT PRIMARY KEY,
                flow_id TEXT NOT NULL,
                parent_id TEXT,  -- NULL for root nodes
                node_type TEXT NOT NULL,  -- root, agent, control_flow, gate
                name TEXT NOT NULL,
                description TEXT,
                position INTEGER,  -- Order among siblings
                config JSON,  -- Node-specific configuration
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (flow_id) REFERENCES flows(flow_id) ON DELETE CASCADE,
                FOREIGN KEY (parent_id) REFERENCES nodes(node_id) ON DELETE CASCADE
            )
        """)
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_nodes_flow ON nodes(flow_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_nodes_parent ON nodes(parent_id)")

        # Executions table - flow execution instances
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS executions (
                execution_id TEXT PRIMARY KEY,
                flow_id TEXT NOT NULL,
                status TEXT NOT NULL,  -- pending, in_progress, completed, failed
                started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                completed_at TIMESTAMP,
                error TEXT,
                context JSON,  -- Initial execution context
                FOREIGN KEY (flow_id) REFERENCES flows(flow_id) ON DELETE CASCADE
            )
        """)
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_executions_flow ON executions(flow_id)")

        # Node executions - individual node execution tracking
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS node_executions (
                node_exec_id TEXT PRIMARY KEY,
                execution_id TEXT NOT NULL,
                node_id TEXT NOT NULL,
                status TEXT NOT NULL,
                started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                completed_at TIMESTAMP,
                input_data JSON,
                output_data JSON,
                error TEXT,
                attempts INTEGER DEFAULT 1,
                FOREIGN KEY (execution_id) REFERENCES executions(execution_id) ON DELETE CASCADE,
                FOREIGN KEY (node_id) REFERENCES nodes(node_id) ON DELETE CASCADE
            )
        """)
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_node_exec_execution ON node_executions(execution_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_node_exec_node ON node_executions(node_id)")

        # Business rules table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS business_rules (
                rule_id TEXT PRIMARY KEY,
                flow_id TEXT NOT NULL,
                name TEXT NOT NULL,
                description TEXT,
                rule_type TEXT NOT NULL,  -- gate, validation, transformation
                condition JSON NOT NULL,  -- Rule condition expression
                action JSON,  -- Action to take when rule fires
                priority INTEGER DEFAULT 0,
                active BOOLEAN DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (flow_id) REFERENCES flows(flow_id) ON DELETE CASCADE
            )
        """)
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_rules_flow ON business_rules(flow_id)")

        # Gate evaluations - audit trail for gate decisions
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS gate_evaluations (
                eval_id TEXT PRIMARY KEY,
                execution_id TEXT NOT NULL,
                node_id TEXT NOT NULL,
                rule_id TEXT NOT NULL,
                status TEXT NOT NULL,  -- pass, fail, pending
                evaluated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                input_context JSON,
                evaluation_result JSON,
                reason TEXT,  -- Explanation of decision
                FOREIGN KEY (execution_id) REFERENCES executions(execution_id) ON DELETE CASCADE,
                FOREIGN KEY (node_id) REFERENCES nodes(node_id) ON DELETE CASCADE,
                FOREIGN KEY (rule_id) REFERENCES business_rules(rule_id) ON DELETE CASCADE
            )
        """)
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_gate_eval_execution ON gate_evaluations(execution_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_gate_eval_node ON gate_evaluations(node_id)")

        # Episodic memory - goal-specific examples for context retrieval
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS episodic_memory (
                memory_id TEXT PRIMARY KEY,
                flow_id TEXT NOT NULL,
                node_id TEXT,  -- NULL for flow-level memories
                goal_signature TEXT NOT NULL,  -- Hash/signature of goal type
                example_data JSON NOT NULL,
                success BOOLEAN,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                access_count INTEGER DEFAULT 0,
                last_accessed TIMESTAMP,
                metadata JSON,
                FOREIGN KEY (flow_id) REFERENCES flows(flow_id) ON DELETE CASCADE,
                FOREIGN KEY (node_id) REFERENCES nodes(node_id) ON DELETE SET NULL
            )
        """)
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_episodic_flow ON episodic_memory(flow_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_episodic_signature ON episodic_memory(goal_signature)")

        # Working memory - shared observations across nodes during execution
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS working_memory (
                memory_id TEXT PRIMARY KEY,
                execution_id TEXT NOT NULL,
                node_id TEXT NOT NULL,
                key TEXT NOT NULL,
                value JSON NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                expires_at TIMESTAMP,  -- NULL for persistent within execution
                FOREIGN KEY (execution_id) REFERENCES executions(execution_id) ON DELETE CASCADE,
                FOREIGN KEY (node_id) REFERENCES nodes(node_id) ON DELETE CASCADE,
                UNIQUE(execution_id, key)
            )
        """)
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_working_exec ON working_memory(execution_id)")

        # Audit log - comprehensive logging of all operations
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS audit_log (
                log_id TEXT PRIMARY KEY,
                execution_id TEXT,
                node_id TEXT,
                event_type TEXT NOT NULL,  -- execution_start, node_start, gate_eval, etc.
                event_data JSON NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                user_id TEXT,
                metadata JSON
            )
        """)
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_audit_execution ON audit_log(execution_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_audit_timestamp ON audit_log(timestamp)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_audit_event_type ON audit_log(event_type)")

        self.conn.commit()

    # ==================== Flow Operations ====================

    def create_flow(self, name: str, description: str = "", metadata: Dict = None) -> str:
        """Create a new flow."""
        flow_id = str(uuid.uuid4())
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO flows (flow_id, name, description, metadata)
            VALUES (?, ?, ?, ?)
        """, (flow_id, name, description, json.dumps(metadata or {})))
        self.conn.commit()
        return flow_id

    def get_flow(self, flow_id: str) -> Optional[Dict]:
        """Retrieve flow by ID."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM flows WHERE flow_id = ?", (flow_id,))
        row = cursor.fetchone()
        if row:
            return dict(row)
        return None

    def list_flows(self) -> List[Dict]:
        """List all flows."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM flows ORDER BY created_at DESC")
        return [dict(row) for row in cursor.fetchall()]

    # ==================== Node Operations ====================

    def create_node(self, flow_id: str, node_type: NodeType, name: str,
                    parent_id: Optional[str] = None, description: str = "",
                    position: int = 0, config: Dict = None) -> str:
        """Create a new node in the agent tree."""
        node_id = str(uuid.uuid4())
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO nodes (node_id, flow_id, parent_id, node_type, name, description, position, config)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (node_id, flow_id, parent_id, node_type.value, name, description, position, json.dumps(config or {})))
        self.conn.commit()
        return node_id

    def get_node(self, node_id: str) -> Optional[Dict]:
        """Retrieve node by ID."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM nodes WHERE node_id = ?", (node_id,))
        row = cursor.fetchone()
        if row:
            return dict(row)
        return None

    def get_child_nodes(self, parent_id: str) -> List[Dict]:
        """Get all child nodes of a parent."""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT * FROM nodes
            WHERE parent_id = ?
            ORDER BY position ASC
        """, (parent_id,))
        return [dict(row) for row in cursor.fetchall()]

    def get_flow_tree(self, flow_id: str) -> List[Dict]:
        """Get entire tree structure for a flow."""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT * FROM nodes
            WHERE flow_id = ?
            ORDER BY parent_id, position
        """, (flow_id,))
        return [dict(row) for row in cursor.fetchall()]

    # ==================== Execution Operations ====================

    def create_execution(self, flow_id: str, context: Dict = None) -> str:
        """Start a new execution of a flow."""
        execution_id = str(uuid.uuid4())
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO executions (execution_id, flow_id, status, context)
            VALUES (?, ?, ?, ?)
        """, (execution_id, flow_id, "pending", json.dumps(context or {})))
        self.conn.commit()

        # Log execution start
        self.audit_log(execution_id, None, "execution_start", {
            "flow_id": flow_id,
            "context": context
        })

        return execution_id

    def update_execution_status(self, execution_id: str, status: str, error: str = None):
        """Update execution status."""
        cursor = self.conn.cursor()
        if status in ["completed", "failed"]:
            cursor.execute("""
                UPDATE executions
                SET status = ?, completed_at = CURRENT_TIMESTAMP, error = ?
                WHERE execution_id = ?
            """, (status, error, execution_id))
        else:
            cursor.execute("""
                UPDATE executions
                SET status = ?
                WHERE execution_id = ?
            """, (status, execution_id))
        self.conn.commit()

        # Log status change
        self.audit_log(execution_id, None, "execution_status_change", {
            "new_status": status,
            "error": error
        })

    def create_node_execution(self, execution_id: str, node_id: str, input_data: Dict = None) -> str:
        """Create a node execution record."""
        node_exec_id = str(uuid.uuid4())
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO node_executions (node_exec_id, execution_id, node_id, status, input_data)
            VALUES (?, ?, ?, ?, ?)
        """, (node_exec_id, execution_id, node_id, "in_progress", json.dumps(input_data or {})))
        self.conn.commit()

        # Log node execution start
        self.audit_log(execution_id, node_id, "node_execution_start", {
            "node_exec_id": node_exec_id,
            "input_data": input_data
        })

        return node_exec_id

    def update_node_execution(self, node_exec_id: str, status: str,
                            output_data: Dict = None, error: str = None):
        """Update node execution status and results."""
        cursor = self.conn.cursor()
        cursor.execute("""
            UPDATE node_executions
            SET status = ?, completed_at = CURRENT_TIMESTAMP, output_data = ?, error = ?
            WHERE node_exec_id = ?
        """, (status, json.dumps(output_data or {}), error, node_exec_id))
        self.conn.commit()

    # ==================== Business Rules Operations ====================

    def create_rule(self, flow_id: str, name: str, rule_type: str,
                   condition: Dict, action: Dict = None, description: str = "",
                   priority: int = 0) -> str:
        """Create a business rule."""
        rule_id = str(uuid.uuid4())
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO business_rules (rule_id, flow_id, name, description, rule_type, condition, action, priority)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (rule_id, flow_id, name, description, rule_type,
              json.dumps(condition), json.dumps(action or {}), priority))
        self.conn.commit()
        return rule_id

    def get_rules_for_flow(self, flow_id: str, rule_type: str = None) -> List[Dict]:
        """Get all rules for a flow, optionally filtered by type."""
        cursor = self.conn.cursor()
        if rule_type:
            cursor.execute("""
                SELECT * FROM business_rules
                WHERE flow_id = ? AND rule_type = ? AND active = 1
                ORDER BY priority DESC
            """, (flow_id, rule_type))
        else:
            cursor.execute("""
                SELECT * FROM business_rules
                WHERE flow_id = ? AND active = 1
                ORDER BY priority DESC
            """, (flow_id,))
        return [dict(row) for row in cursor.fetchall()]

    def record_gate_evaluation(self, execution_id: str, node_id: str, rule_id: str,
                              status: GateStatus, input_context: Dict,
                              evaluation_result: Dict, reason: str = "") -> str:
        """Record a gate evaluation for audit trail."""
        eval_id = str(uuid.uuid4())
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO gate_evaluations (eval_id, execution_id, node_id, rule_id, status, input_context, evaluation_result, reason)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (eval_id, execution_id, node_id, rule_id, status.value,
              json.dumps(input_context), json.dumps(evaluation_result), reason))
        self.conn.commit()

        # Log gate evaluation
        self.audit_log(execution_id, node_id, "gate_evaluation", {
            "eval_id": eval_id,
            "rule_id": rule_id,
            "status": status.value,
            "reason": reason
        })

        return eval_id

    # ==================== Memory Operations ====================

    def store_episodic_memory(self, flow_id: str, goal_signature: str,
                            example_data: Dict, node_id: str = None,
                            success: bool = True, metadata: Dict = None) -> str:
        """Store an episodic memory (goal-specific example)."""
        memory_id = str(uuid.uuid4())
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO episodic_memory (memory_id, flow_id, node_id, goal_signature, example_data, success, metadata)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (memory_id, flow_id, node_id, goal_signature, json.dumps(example_data), success, json.dumps(metadata or {})))
        self.conn.commit()
        return memory_id

    def retrieve_episodic_memory(self, flow_id: str, goal_signature: str,
                                limit: int = 5, success_only: bool = True) -> List[Dict]:
        """Retrieve episodic memories for a goal signature."""
        cursor = self.conn.cursor()
        if success_only:
            cursor.execute("""
                SELECT * FROM episodic_memory
                WHERE flow_id = ? AND goal_signature = ? AND success = 1
                ORDER BY access_count DESC, created_at DESC
                LIMIT ?
            """, (flow_id, goal_signature, limit))
        else:
            cursor.execute("""
                SELECT * FROM episodic_memory
                WHERE flow_id = ? AND goal_signature = ?
                ORDER BY access_count DESC, created_at DESC
                LIMIT ?
            """, (flow_id, goal_signature, limit))

        memories = [dict(row) for row in cursor.fetchall()]

        # Update access counts
        for memory in memories:
            cursor.execute("""
                UPDATE episodic_memory
                SET access_count = access_count + 1, last_accessed = CURRENT_TIMESTAMP
                WHERE memory_id = ?
            """, (memory['memory_id'],))
        self.conn.commit()

        return memories

    def store_working_memory(self, execution_id: str, node_id: str,
                           key: str, value: Any, expires_at: str = None) -> str:
        """Store working memory (shared observations)."""
        memory_id = str(uuid.uuid4())
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO working_memory (memory_id, execution_id, node_id, key, value, expires_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (memory_id, execution_id, node_id, key, json.dumps(value), expires_at))
        self.conn.commit()
        return memory_id

    def retrieve_working_memory(self, execution_id: str, key: str = None) -> Dict:
        """Retrieve working memory for an execution."""
        cursor = self.conn.cursor()
        if key:
            cursor.execute("""
                SELECT * FROM working_memory
                WHERE execution_id = ? AND key = ?
                AND (expires_at IS NULL OR expires_at > CURRENT_TIMESTAMP)
            """, (execution_id, key))
            row = cursor.fetchone()
            return dict(row) if row else None
        else:
            cursor.execute("""
                SELECT * FROM working_memory
                WHERE execution_id = ?
                AND (expires_at IS NULL OR expires_at > CURRENT_TIMESTAMP)
            """, (execution_id,))
            return [dict(row) for row in cursor.fetchall()]

    # ==================== Audit Operations ====================

    def audit_log(self, execution_id: str, node_id: str, event_type: str,
                 event_data: Dict, user_id: str = None, metadata: Dict = None):
        """Create an audit log entry."""
        log_id = str(uuid.uuid4())
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO audit_log (log_id, execution_id, node_id, event_type, event_data, user_id, metadata)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (log_id, execution_id, node_id, event_type, json.dumps(event_data), user_id, json.dumps(metadata or {})))
        self.conn.commit()

    def get_audit_logs(self, execution_id: str = None, event_type: str = None,
                      start_time: str = None, end_time: str = None, limit: int = 100) -> List[Dict]:
        """Query audit logs with filters."""
        cursor = self.conn.cursor()
        query = "SELECT * FROM audit_log WHERE 1=1"
        params = []

        if execution_id:
            query += " AND execution_id = ?"
            params.append(execution_id)
        if event_type:
            query += " AND event_type = ?"
            params.append(event_type)
        if start_time:
            query += " AND timestamp >= ?"
            params.append(start_time)
        if end_time:
            query += " AND timestamp <= ?"
            params.append(end_time)

        query += " ORDER BY timestamp DESC LIMIT ?"
        params.append(limit)

        cursor.execute(query, params)
        return [dict(row) for row in cursor.fetchall()]

    def get_execution_audit_trail(self, execution_id: str) -> Dict:
        """Get complete audit trail for an execution with statistics."""
        logs = self.get_audit_logs(execution_id=execution_id, limit=10000)

        # Calculate statistics
        stats = {
            "total_events": len(logs),
            "event_types": {},
            "gate_evaluations": {"pass": 0, "fail": 0, "pending": 0},
            "node_executions": {"completed": 0, "failed": 0, "in_progress": 0},
            "duration_seconds": 0
        }

        for log in logs:
            event_type = log['event_type']
            stats["event_types"][event_type] = stats["event_types"].get(event_type, 0) + 1

            # Track gate evaluation outcomes
            if event_type == "gate_evaluation":
                event_data = json.loads(log['event_data'])
                status = event_data.get('status', 'unknown')
                if status in stats["gate_evaluations"]:
                    stats["gate_evaluations"][status] += 1

        # Calculate duration
        if logs:
            start = logs[-1]['timestamp']  # Oldest log (DESC order)
            end = logs[0]['timestamp']     # Newest log
            # Note: Would need proper datetime parsing for accurate duration

        return {
            "execution_id": execution_id,
            "logs": logs,
            "statistics": stats
        }

    def close(self):
        """Close database connection."""
        self.conn.close()

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()


# Convenience functions
def init_database(db_path: str = "agentic_flows.db") -> FlowDatabase:
    """Initialize and return a database instance."""
    return FlowDatabase(db_path)
