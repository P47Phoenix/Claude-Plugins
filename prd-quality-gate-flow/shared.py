"""
Shared constants and utilities for the prd-quality-gate-flow plugin.

Centralizes DB_PATH, timestamp ID generation, and UTF-8 output configuration
so they are defined once and never hardcoded across multiple files.
"""

import sys
import io
import sqlite3
from datetime import datetime


# Database file path — single source of truth
DB_PATH = "prd_flows.db"


def generate_timestamp_id(prefix: str) -> str:
    """Generate a timestamp-based ID with the given prefix.

    Args:
        prefix: String prefix for the ID (e.g., 'flow', 'node', 'rule')

    Returns:
        String in format '{prefix}_{YYYYMMDD_HHMMSS}' or with microseconds
        for node/rule IDs to avoid collisions.
    """
    now = datetime.now()
    if prefix == "flow":
        return f"{prefix}_{now.strftime('%Y%m%d_%H%M%S')}"
    else:
        return f"{prefix}_{now.strftime('%Y%m%d%H%M%S%f')}"


def ensure_utf8_output():
    """Wrap sys.stdout and sys.stderr in UTF-8 TextIOWrapper on Windows.

    Safe to call on any platform — no-op on non-Windows systems.
    """
    if sys.platform == "win32":
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')


def get_connection(db_path=None):
    """Open a SQLite connection with schema initialized.

    Args:
        db_path: Path to SQLite database file. Defaults to DB_PATH.

    Returns:
        sqlite3.Connection with row_factory set and schema ensured.
    """
    if db_path is None:
        db_path = DB_PATH
    from schema import ensure_schema
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    ensure_schema(conn)
    return conn
