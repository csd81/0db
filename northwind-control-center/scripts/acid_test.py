#!/usr/bin/env python3
"""
acid_test.py — Concurrent bank transfer ACID test.

Usage:
    python3 acid_test.py --db sqlite
    python3 acid_test.py --db postgresql --host localhost --port 5432 --db-name testdb --user postgres --password secret
    python3 acid_test.py --db mysql --host localhost --port 3306 --db-name testdb --user root --password secret
    python3 acid_test.py --db sqlite --isolation READ_UNCOMMITTED

Creates an 'accounts' table with 10 accounts, each with balance=1000 (total=10000).
Spawns 20 concurrent threads. Each thread:
  1. Picks two random account IDs
  2. Begins a transaction
  3. Reads both balances
  4. Sleeps random 0-50ms (simulates work / races)
  5. Transfers a random amount (1-100) from A to B if A has enough
  6. Commits

After all threads complete:
- Verifies total balance still equals 10000 (ACID atomicity)
- Reports: successes, failures, deadlock retries, total balance, verdict PASS/FAIL
"""

import argparse
import random
import threading
import time
import sys

# ---------------------------------------------------------------------------
# Argument parsing
# ---------------------------------------------------------------------------

def parse_args():
    parser = argparse.ArgumentParser(description="ACID concurrent bank transfer test")
    parser.add_argument("--db", choices=["sqlite", "postgresql", "mysql"],
                        default="sqlite", help="Database backend (default: sqlite)")
    parser.add_argument("--host", default="localhost", help="DB host (PG/MySQL)")
    parser.add_argument("--port", type=int, default=None, help="DB port (default: 5432/3306)")
    parser.add_argument("--db-name", default="acid_test", help="Database name (PG/MySQL)")
    parser.add_argument("--user", default="postgres", help="DB user (PG/MySQL)")
    parser.add_argument("--password", default="", help="DB password (PG/MySQL)")
    parser.add_argument("--threads", type=int, default=20,
                        help="Number of concurrent threads (default: 20)")
    parser.add_argument("--accounts", type=int, default=10,
                        help="Number of accounts (default: 10)")
    parser.add_argument("--initial-balance", type=int, default=1000,
                        help="Starting balance per account (default: 1000)")
    parser.add_argument("--isolation", default=None,
                        help="Isolation level override, e.g. READ_UNCOMMITTED, SERIALIZABLE")
    parser.add_argument("--sqlite-path", default="/tmp/acid_test.db",
                        help="Path for SQLite file (default: /tmp/acid_test.db)")
    return parser.parse_args()


# ---------------------------------------------------------------------------
# Connection factories
# ---------------------------------------------------------------------------

def make_sqlite_connection(args):
    import sqlite3
    conn = sqlite3.connect(args.sqlite_path, check_same_thread=False, timeout=30)
    conn.isolation_level = None  # autocommit off; we manage BEGIN manually
    return conn


def make_postgresql_connection(args):
    try:
        import psycopg2
    except ImportError:
        print("ERROR: psycopg2 is not installed. Run: pip install psycopg2-binary")
        sys.exit(1)
    port = args.port or 5432
    conn = psycopg2.connect(
        host=args.host,
        port=port,
        dbname=args.db_name,
        user=args.user,
        password=args.password,
    )
    conn.autocommit = False
    if args.isolation:
        level = args.isolation.replace("_", " ")
        conn.set_isolation_level(
            {
                "READ UNCOMMITTED": psycopg2.extensions.ISOLATION_LEVEL_READ_UNCOMMITTED,
                "READ COMMITTED": psycopg2.extensions.ISOLATION_LEVEL_READ_COMMITTED,
                "REPEATABLE READ": psycopg2.extensions.ISOLATION_LEVEL_REPEATABLE_READ,
                "SERIALIZABLE": psycopg2.extensions.ISOLATION_LEVEL_SERIALIZABLE,
            }.get(level.upper(), psycopg2.extensions.ISOLATION_LEVEL_READ_COMMITTED)
        )
    return conn


def make_mysql_connection(args):
    try:
        import pymysql
    except ImportError:
        print("ERROR: pymysql is not installed. Run: pip install pymysql")
        sys.exit(1)
    port = args.port or 3306
    conn = pymysql.connect(
        host=args.host,
        port=port,
        db=args.db_name,
        user=args.user,
        password=args.password,
        autocommit=False,
    )
    return conn


def get_connection(args):
    if args.db == "sqlite":
        return make_sqlite_connection(args)
    elif args.db == "postgresql":
        return make_postgresql_connection(args)
    elif args.db == "mysql":
        return make_mysql_connection(args)


# ---------------------------------------------------------------------------
# Schema setup
# ---------------------------------------------------------------------------

def setup_schema(args):
    conn = get_connection(args)
    cur = conn.cursor()

    if args.db == "sqlite":
        cur.execute("BEGIN")
        cur.execute("DROP TABLE IF EXISTS accounts")
        cur.execute("""
            CREATE TABLE accounts (
                id      INTEGER PRIMARY KEY,
                balance INTEGER NOT NULL CHECK(balance >= 0)
            )
        """)
        for i in range(1, args.accounts + 1):
            cur.execute("INSERT INTO accounts (id, balance) VALUES (?, ?)",
                        (i, args.initial_balance))
        cur.execute("COMMIT")
    elif args.db == "postgresql":
        cur.execute("DROP TABLE IF EXISTS accounts")
        cur.execute("""
            CREATE TABLE accounts (
                id      SERIAL PRIMARY KEY,
                balance INTEGER NOT NULL CHECK(balance >= 0)
            )
        """)
        for i in range(1, args.accounts + 1):
            cur.execute("INSERT INTO accounts (id, balance) VALUES (%s, %s)",
                        (i, args.initial_balance))
        conn.commit()
    elif args.db == "mysql":
        cur.execute("DROP TABLE IF EXISTS accounts")
        cur.execute("""
            CREATE TABLE accounts (
                id      INT PRIMARY KEY AUTO_INCREMENT,
                balance INT NOT NULL,
                CONSTRAINT chk_balance CHECK (balance >= 0)
            ) ENGINE=InnoDB
        """)
        for i in range(1, args.accounts + 1):
            cur.execute("INSERT INTO accounts (id, balance) VALUES (%s, %s)",
                        (i, args.initial_balance))
        conn.commit()

    cur.close()
    conn.close()
    print(f"  Schema ready: {args.accounts} accounts x {args.initial_balance} "
          f"= {args.accounts * args.initial_balance} total")


# ---------------------------------------------------------------------------
# Transfer worker
# ---------------------------------------------------------------------------

DEADLOCK_MAX_RETRIES = 5

def is_deadlock_error(db_type, exc):
    """Return True if the exception represents a deadlock/lock timeout."""
    msg = str(exc).lower()
    if db_type == "sqlite":
        return "database is locked" in msg or "locked" in msg
    elif db_type == "postgresql":
        # psycopg2 raises OperationalError with pgcode 40P01 for deadlocks
        pgcode = getattr(exc, "pgcode", None)
        return pgcode in ("40P01", "40001") or "deadlock" in msg
    elif db_type == "mysql":
        errno = getattr(exc, "args", [None])[0] if exc.args else None
        return errno in (1213, 1205) or "deadlock" in msg or "lock wait timeout" in msg
    return False


def placeholder(db_type):
    return "?" if db_type == "sqlite" else "%s"


def transfer_worker(args, stats, lock):
    """
    Thread target: attempt a random transfer between two random accounts.
    Retries on deadlock up to DEADLOCK_MAX_RETRIES times.
    Updates shared stats dict (protected by lock).
    """
    ph = placeholder(args.db)
    deadlock_retries = 0

    for attempt in range(DEADLOCK_MAX_RETRIES + 1):
        conn = None
        try:
            conn = get_connection(args)
            cur = conn.cursor()

            account_ids = random.sample(range(1, args.accounts + 1), 2)
            src_id, dst_id = account_ids[0], account_ids[1]
            amount = random.randint(1, 100)

            if args.db == "sqlite":
                cur.execute("BEGIN IMMEDIATE")
            elif args.db == "postgresql":
                cur.execute("BEGIN")
                if args.isolation:
                    level = args.isolation.replace("_", " ")
                    cur.execute(f"SET TRANSACTION ISOLATION LEVEL {level}")
            elif args.db == "mysql":
                cur.execute("START TRANSACTION")
                if args.isolation:
                    level = args.isolation.replace("_", " ")
                    cur.execute(f"SET TRANSACTION ISOLATION LEVEL {level}")

            # Read source balance
            cur.execute(f"SELECT balance FROM accounts WHERE id = {ph}", (src_id,))
            row = cur.fetchone()
            if row is None:
                if args.db == "sqlite":
                    cur.execute("ROLLBACK")
                else:
                    conn.rollback()
                cur.close()
                conn.close()
                with lock:
                    stats["failures"] += 1
                return

            src_balance = row[0]

            # Simulate some work / induce races
            time.sleep(random.uniform(0, 0.05))

            if src_balance >= amount:
                cur.execute(
                    f"UPDATE accounts SET balance = balance - {ph} WHERE id = {ph}",
                    (amount, src_id),
                )
                cur.execute(
                    f"UPDATE accounts SET balance = balance + {ph} WHERE id = {ph}",
                    (amount, dst_id),
                )
                if args.db == "sqlite":
                    cur.execute("COMMIT")
                else:
                    conn.commit()
                with lock:
                    stats["successes"] += 1
                    stats["deadlock_retries"] += deadlock_retries
            else:
                # Insufficient funds — rollback cleanly
                if args.db == "sqlite":
                    cur.execute("ROLLBACK")
                else:
                    conn.rollback()
                with lock:
                    stats["insufficient"] += 1
                    stats["deadlock_retries"] += deadlock_retries

            cur.close()
            conn.close()
            return  # done

        except Exception as exc:
            if conn:
                try:
                    if args.db == "sqlite":
                        conn.execute("ROLLBACK")
                    else:
                        conn.rollback()
                except Exception:
                    pass
                try:
                    conn.close()
                except Exception:
                    pass

            if is_deadlock_error(args.db, exc) and attempt < DEADLOCK_MAX_RETRIES:
                deadlock_retries += 1
                backoff = 0.01 * (2 ** attempt) + random.uniform(0, 0.01)
                time.sleep(backoff)
                continue  # retry

            # Non-deadlock error or retries exhausted
            with lock:
                stats["failures"] += 1
                stats["deadlock_retries"] += deadlock_retries
            return


# ---------------------------------------------------------------------------
# Verify total balance
# ---------------------------------------------------------------------------

def verify_total(args):
    conn = get_connection(args)
    cur = conn.cursor()
    cur.execute("SELECT SUM(balance) FROM accounts")
    row = cur.fetchone()
    total = row[0] if row and row[0] is not None else 0
    cur.close()
    conn.close()
    return int(total)


# ---------------------------------------------------------------------------
# Reporting
# ---------------------------------------------------------------------------

def print_banner(text):
    width = 60
    print("=" * width)
    print(f"  {text}")
    print("=" * width)


def print_summary(args, stats, total, elapsed):
    expected = args.accounts * args.initial_balance
    verdict = "PASS" if total == expected else "FAIL"
    verdict_color = "\033[92m" if verdict == "PASS" else "\033[91m"
    reset = "\033[0m"

    print()
    print_banner("ACID Test Results")
    print(f"  Database        : {args.db.upper()}")
    if args.isolation:
        print(f"  Isolation level : {args.isolation}")
    print(f"  Threads         : {args.threads}")
    print(f"  Accounts        : {args.accounts}")
    print(f"  Initial total   : {expected}")
    print(f"  Elapsed         : {elapsed:.2f}s")
    print()
    print(f"  Successful xfers: {stats['successes']}")
    print(f"  Insuf. funds    : {stats['insufficient']}")
    print(f"  Failures        : {stats['failures']}")
    print(f"  Deadlock retries: {stats['deadlock_retries']}")
    print()
    print(f"  Final total bal : {total}")
    print(f"  Expected total  : {expected}")
    print()
    print(f"  Verdict         : {verdict_color}{verdict}{reset}")
    print("=" * 60)
    if verdict == "FAIL":
        lost = expected - total
        print(f"\n  WARNING: {abs(lost)} units {'lost' if lost > 0 else 'created'}!")
        print("  This indicates a violation of ACID atomicity/isolation.")
    print()


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    args = parse_args()

    print()
    print_banner("ACID Concurrent Bank Transfer Test")
    print(f"  Backend  : {args.db.upper()}")
    if args.db == "sqlite":
        print(f"  DB file  : {args.sqlite_path}")
    else:
        print(f"  Host     : {args.host}")
        print(f"  DB name  : {args.db_name}")
    print(f"  Threads  : {args.threads}")
    print(f"  Accounts : {args.accounts}  x  balance {args.initial_balance}")
    if args.isolation:
        print(f"  Isolation: {args.isolation}")
    print()

    # 1. Setup schema
    print("[1/3] Setting up schema ...")
    setup_schema(args)

    # 2. Run concurrent transfers
    print(f"[2/3] Spawning {args.threads} concurrent transfer threads ...")
    stats = {"successes": 0, "insufficient": 0, "failures": 0, "deadlock_retries": 0}
    lock = threading.Lock()

    threads = []
    start = time.time()
    for _ in range(args.threads):
        t = threading.Thread(target=transfer_worker, args=(args, stats, lock))
        threads.append(t)

    for t in threads:
        t.start()
    for t in threads:
        t.join()

    elapsed = time.time() - start
    print(f"  All threads finished in {elapsed:.2f}s")

    # 3. Verify ACID invariant
    print("[3/3] Verifying total balance ...")
    total = verify_total(args)

    print_summary(args, stats, total, elapsed)


if __name__ == "__main__":
    main()
