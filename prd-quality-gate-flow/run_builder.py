"""
Wrapper script to run flow builder with proper encoding
"""
import sys
import io

# Set UTF-8 encoding for output
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Now import and run the builder
from prd_flow_builder import PRDFlowBuilder

if __name__ == "__main__":
    # Build the PRD flow
    builder = PRDFlowBuilder("prd_flows.db")

    try:
        flow_id = builder.build_prd_flow()

        print("\n" + "=" * 60)
        print("PRD Quality Gate Flow Built Successfully!")
        print("=" * 60)
        print(f"\nFlow ID: {flow_id}")
        print(f"Database: prd_flows.db")

        # Export diagram
        diagram = builder.export_flow_diagram(flow_id)
        print("\n" + diagram)

        # Save diagram to file
        with open("prd_flow_diagram.txt", "w", encoding="utf-8") as f:
            f.write(diagram)

        print("\nFlow diagram saved to: prd_flow_diagram.txt")
        print("\nNext steps:")
        print("  1. Review the flow structure in prd_flow_diagram.txt")
        print("  2. Customize business rules as needed")
        print("  3. Run: python prd_execute.py")

    finally:
        builder.close()
