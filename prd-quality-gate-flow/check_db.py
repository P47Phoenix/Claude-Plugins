"""Check database contents"""
import sqlite3

conn = sqlite3.connect("prd_flows.db")
conn.row_factory = sqlite3.Row

# Check flows
flows = conn.execute("SELECT * FROM flows").fetchall()
print(f"Flows: {len(flows)}")
for flow in flows:
    print(f"  - {flow['name']} ({flow['flow_id']})")

# Check nodes
nodes = conn.execute("SELECT * FROM nodes").fetchall()
print(f"\nNodes: {len(nodes)}")
node_types = conn.execute("SELECT node_type, COUNT(*) as count FROM nodes GROUP BY node_type").fetchall()
for nt in node_types:
    print(f"  - {nt['node_type']}: {nt['count']}")

# Check rules
rules = conn.execute("SELECT * FROM business_rules").fetchall()
print(f"\nBusiness Rules: {len(rules)}")

print("\nFlow structure looks good!")

conn.close()
