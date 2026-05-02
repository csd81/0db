"""
transaction_service.py — Python-level change tracking for SQLite databases.

All mutations go through tracked_insert / tracked_update / tracked_delete which
capture OldData and NewData as JSON into a TransactionLog table on the target DB.
This approach works across SQLite versions without requiring complex trigger syntax.
"""

import json
import sqlite3


def ensure_transaction_log(conn: sqlite3.Connection) -> None:
    conn.execute("""
        CREATE TABLE IF NOT EXISTS TransactionLog (
            LogID     INTEGER PRIMARY KEY AUTOINCREMENT,
            TableName TEXT    NOT NULL,
            Operation TEXT    NOT NULL,
            RecordID  TEXT,
            OldData   TEXT,
            NewData   TEXT,
            Timestamp DATETIME DEFAULT (datetime('now'))
        )
    """)
    conn.commit()


def tracked_insert(conn: sqlite3.Connection, table: str, data: dict) -> int:
    cols = ', '.join(f'[{c}]' for c in data)
    placeholders = ', '.join('?' for _ in data)
    cur = conn.execute(
        f"INSERT INTO [{table}] ({cols}) VALUES ({placeholders})",
        list(data.values()),
    )
    rowid = cur.lastrowid
    conn.execute(
        "INSERT INTO TransactionLog (TableName, Operation, RecordID, NewData) VALUES (?, 'INSERT', ?, ?)",
        (table, str(rowid), json.dumps(data)),
    )
    conn.commit()
    return rowid


def tracked_update(conn: sqlite3.Connection, table: str,
                   pk_col: str, pk_val, updates: dict) -> int:
    old_cur = conn.execute(f"SELECT * FROM [{table}] WHERE [{pk_col}] = ?", (pk_val,))
    old_row = old_cur.fetchone()
    old_data = dict(zip([d[0] for d in old_cur.description], old_row)) if old_row else {}

    set_clause = ', '.join(f'[{c}] = ?' for c in updates)
    cur = conn.execute(
        f"UPDATE [{table}] SET {set_clause} WHERE [{pk_col}] = ?",
        list(updates.values()) + [pk_val],
    )
    conn.execute(
        "INSERT INTO TransactionLog (TableName, Operation, RecordID, OldData, NewData) VALUES (?, 'UPDATE', ?, ?, ?)",
        (table, str(pk_val), json.dumps(old_data), json.dumps(updates)),
    )
    conn.commit()
    return cur.rowcount


def tracked_delete(conn: sqlite3.Connection, table: str,
                   pk_col: str, pk_val) -> int:
    old_cur = conn.execute(f"SELECT * FROM [{table}] WHERE [{pk_col}] = ?", (pk_val,))
    old_row = old_cur.fetchone()
    old_data = dict(zip([d[0] for d in old_cur.description], old_row)) if old_row else {}

    cur = conn.execute(f"DELETE FROM [{table}] WHERE [{pk_col}] = ?", (pk_val,))
    conn.execute(
        "INSERT INTO TransactionLog (TableName, Operation, RecordID, OldData) VALUES (?, 'DELETE', ?, ?)",
        (table, str(pk_val), json.dumps(old_data)),
    )
    conn.commit()
    return cur.rowcount


def get_transaction_log(conn: sqlite3.Connection,
                        table: str | None = None, limit: int = 200) -> list[dict]:
    if table:
        cur = conn.execute(
            "SELECT * FROM TransactionLog WHERE TableName = ? ORDER BY LogID DESC LIMIT ?",
            (table, limit),
        )
    else:
        cur = conn.execute(
            "SELECT * FROM TransactionLog ORDER BY LogID DESC LIMIT ?", (limit,)
        )
    cols = [d[0] for d in cur.description]
    return [dict(zip(cols, row)) for row in cur.fetchall()]


def replay_log_entry(target_conn: sqlite3.Connection, entry: dict) -> tuple[bool, str | None]:
    """Replay a single TransactionLog entry on a different SQLite DB (for log shipping)."""
    try:
        op = entry['Operation']
        table = entry['TableName']

        if op == 'INSERT':
            data = json.loads(entry['NewData'] or '{}')
            if data:
                cols = ', '.join(f'[{c}]' for c in data)
                placeholders = ', '.join('?' for _ in data)
                target_conn.execute(
                    f"INSERT OR REPLACE INTO [{table}] ({cols}) VALUES ({placeholders})",
                    list(data.values()),
                )
        elif op == 'UPDATE':
            new_data = json.loads(entry['NewData'] or '{}')
            pk_val = entry['RecordID']
            old_data = json.loads(entry['OldData'] or '{}')
            pk_col = next(iter(old_data), 'rowid') if old_data else 'rowid'
            if new_data:
                set_clause = ', '.join(f'[{c}] = ?' for c in new_data)
                target_conn.execute(
                    f"UPDATE [{table}] SET {set_clause} WHERE [{pk_col}] = ?",
                    list(new_data.values()) + [pk_val],
                )
        elif op == 'DELETE':
            old_data = json.loads(entry['OldData'] or '{}')
            pk_val = entry['RecordID']
            pk_col = next(iter(old_data), 'rowid') if old_data else 'rowid'
            target_conn.execute(
                f"DELETE FROM [{table}] WHERE [{pk_col}] = ?", (pk_val,)
            )

        target_conn.commit()
        return True, None
    except Exception as e:
        return False, str(e)
