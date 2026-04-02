"""
Check database contents for the prd-quality-gate-flow plugin.

Restructured with descriptive functions, main() guard, and
graceful error handling when the database file does not exist.
"""
import os
import sys

from shared import DB_PATH


def list_flows(conn):
    """List all flows in the database.

    Args:
        conn: An open sqlite3.Connection with row_factory set.
    """
    flows = conn.execute("SELECT * FROM flows").fetchall()
    print(f"Flows: {len(flows)}")
    for flow in flows:
        print(f"  - {flow['name']} ({flow['flow_id']})")


def list_nodes(conn):
    """List node type breakdown from the database.

    Args:
        conn: An open sqlite3.Connection with row_factory set.
    """
    nodes = conn.execute("SELECT * FROM nodes").fetchall()
    print(f"\nNodes: {len(nodes)}")
    node_types = conn.execute(
        "SELECT node_type, COUNT(*) as count FROM nodes GROUP BY node_type"
    ).fetchall()
    for nt in node_types:
        print(f"  - {nt['node_type']}: {nt['count']}")


def list_rules(conn):
    """List business rules summary from the database.

    Args:
        conn: An open sqlite3.Connection with row_factory set.
    """
    rules = conn.execute("SELECT * FROM business_rules").fetchall()
    print(f"\nBusiness Rules: {len(rules)}")


def main():
    """Inspect the prd_flows database and print a summary."""
    if not os.path.exists(DB_PATH):
        print(f"Error: Database file '{DB_PATH}' does not exist.", file=sys.stderr)
        print("Run 'python prd_flow_builder.py' first to create the flow.", file=sys.stderr)
        sys.exit(1)

    from shared import get_connection
    conn = get_connection(DB_PATH)
    try:
        list_flows(conn)
        list_nodes(conn)
        list_rules(conn)
        print("\nFlow structure looks good!")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
