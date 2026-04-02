"""
Database schema for the prd-quality-gate-flow plugin.

Extracted from PRDFlowBuilder._create_schema() — SQL is byte-identical
to the original implementation. 9 tables, 7 indexes.
"""

import sqlite3


def ensure_schema(conn):
    """Create database schema for flow, nodes, rules, and execution tracking.

    Idempotent — safe to call multiple times on the same connection.
    Uses CREATE TABLE IF NOT EXISTS / CREATE INDEX IF NOT EXISTS throughout.

    Args:
        conn: An open sqlite3.Connection object.
    """

    # Flows table
    conn.execute("""
        CREATE TABLE IF NOT EXISTS flows (
            flow_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            description TEXT,
            version TEXT DEFAULT '1.0.0',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            metadata JSON
        )
    """)

    # Nodes table
    conn.execute("""
        CREATE TABLE IF NOT EXISTS nodes (
            node_id TEXT PRIMARY KEY,
            flow_id TEXT NOT NULL,
            parent_id TEXT,
            node_type TEXT NOT NULL,
            name TEXT NOT NULL,
            description TEXT,
            config JSON,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (flow_id) REFERENCES flows(flow_id),
            FOREIGN KEY (parent_id) REFERENCES nodes(node_id)
        )
    """)

    # Business rules table
    conn.execute("""
        CREATE TABLE IF NOT EXISTS business_rules (
            rule_id TEXT PRIMARY KEY,
            flow_id TEXT NOT NULL,
            gate_node_id TEXT,
            name TEXT NOT NULL,
            rule_type TEXT NOT NULL,
            condition JSON NOT NULL,
            action JSON,
            priority INTEGER DEFAULT 0,
            enabled BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            metadata JSON,
            FOREIGN KEY (flow_id) REFERENCES flows(flow_id),
            FOREIGN KEY (gate_node_id) REFERENCES nodes(node_id)
        )
    """)

    # Executions table
    conn.execute("""
        CREATE TABLE IF NOT EXISTS executions (
            execution_id TEXT PRIMARY KEY,
            flow_id TEXT NOT NULL,
            status TEXT NOT NULL,
            input_context JSON,
            output_result JSON,
            started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            completed_at TIMESTAMP,
            error_message TEXT,
            metadata JSON,
            FOREIGN KEY (flow_id) REFERENCES flows(flow_id)
        )
    """)

    # Node executions table
    conn.execute("""
        CREATE TABLE IF NOT EXISTS node_executions (
            node_exec_id TEXT PRIMARY KEY,
            execution_id TEXT NOT NULL,
            node_id TEXT NOT NULL,
            status TEXT NOT NULL,
            input_data JSON,
            output_data JSON,
            started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            completed_at TIMESTAMP,
            agent_used TEXT,
            cost_tokens INTEGER,
            FOREIGN KEY (execution_id) REFERENCES executions(execution_id),
            FOREIGN KEY (node_id) REFERENCES nodes(node_id)
        )
    """)

    # Gate evaluations table
    conn.execute("""
        CREATE TABLE IF NOT EXISTS gate_evaluations (
            eval_id TEXT PRIMARY KEY,
            execution_id TEXT NOT NULL,
            gate_node_id TEXT NOT NULL,
            rule_id TEXT NOT NULL,
            status TEXT NOT NULL,
            evaluation_result BOOLEAN,
            score DECIMAL(5,2),
            reason TEXT,
            evaluated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            context_snapshot JSON,
            FOREIGN KEY (execution_id) REFERENCES executions(execution_id),
            FOREIGN KEY (gate_node_id) REFERENCES nodes(node_id),
            FOREIGN KEY (rule_id) REFERENCES business_rules(rule_id)
        )
    """)

    # Episodic memory table
    conn.execute("""
        CREATE TABLE IF NOT EXISTS episodic_memory (
            memory_id TEXT PRIMARY KEY,
            flow_id TEXT NOT NULL,
            goal_signature TEXT NOT NULL,
            example_data JSON NOT NULL,
            success BOOLEAN NOT NULL,
            execution_id TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            metadata JSON,
            FOREIGN KEY (flow_id) REFERENCES flows(flow_id),
            FOREIGN KEY (execution_id) REFERENCES executions(execution_id)
        )
    """)

    # Working memory table (execution-specific)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS working_memory (
            memory_key TEXT NOT NULL,
            execution_id TEXT NOT NULL,
            value JSON NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            expires_at TIMESTAMP,
            PRIMARY KEY (memory_key, execution_id),
            FOREIGN KEY (execution_id) REFERENCES executions(execution_id)
        )
    """)

    # Audit log table
    conn.execute("""
        CREATE TABLE IF NOT EXISTS audit_log (
            log_id TEXT PRIMARY KEY,
            execution_id TEXT NOT NULL,
            event_type TEXT NOT NULL,
            event_data JSON,
            actor TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (execution_id) REFERENCES executions(execution_id)
        )
    """)

    # Create indexes
    conn.execute("CREATE INDEX IF NOT EXISTS idx_nodes_flow ON nodes(flow_id)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_nodes_parent ON nodes(parent_id)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_rules_flow ON business_rules(flow_id)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_rules_gate ON business_rules(gate_node_id)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_executions_flow ON executions(flow_id)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_gate_evals_exec ON gate_evaluations(execution_id)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_episodic_goal ON episodic_memory(goal_signature)")

    conn.commit()
