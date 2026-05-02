#!/usr/bin/env python3
"""
concurrent_insert_race.py — Demonstrates lost updates without proper locking.

Creates a 'counter' table with value=0.
100 threads each read the value and write value+1 WITHOUT a transaction.
Expected: value=100. Without isolation: value < 100 (lost updates).
Then repeats WITH proper transactions: value=100 exactly.
Educational: shows why transactions matter.

Usage:
    python3 concurrent_insert_race.py
    python3 concurrent_insert_race.py --threads 100 --db /tmp/race_test.db
    python3 concurrent_insert_race.py --delay-ms 5 --runs 3
"""

import argparse
import sqlite3
import threading
import time
import sys
import random


# ---------------------------------------------------------------------------
# Argument parsing
# ---------------------------------------------------------------------------

def parse_args():
    parser = argparse.ArgumentParser(
        description="Demonstrate lost updates with and without transactions"
    )
    parser.add_argument(
        "--threads", type=int, default=100,
        help="Number of concurrent threads (default: 100)"
    )
    parser.add_argument(
        "--db", default="/tmp/race_test.db",
        help="SQLite DB path (default: /tmp/race_test.db)."
    )
    parser.add_argument(
        "--delay-ms", type=float, default=0,
        help="Optional artificial delay in ms between READ and WRITE to amplify races (default: 0)"
    )
    parser.add_argument(
        "--runs", type=int, default=1,
        help="Number of times to repeat each test (default: 1)"
    )
    parser.add_argument(
        "--quiet", action="store_true",
        help="Suppress per-thread output (only print summary)"
    )
    return parser.parse_args()


# ---------------------------------------------------------------------------
# Database helpers
# ---------------------------------------------------------------------------

def get_connection(db_path):
    """Return a new SQLite connection with WAL mode for better concurrency."""
    conn = sqlite3.connect(db_path, check_same_thread=False, timeout=30)
    conn.execute("PRAGMA journal_mode=WAL")
    return conn


def reset_counter(db_path):
    """Drop and recreate the counter table with value=0."""
    conn = get_connection(db_path)
    conn.execute("DROP TABLE IF EXISTS counter")
    conn.execute("CREATE TABLE counter (id INTEGER PRIMARY KEY, value INTEGER NOT NULL)")
    conn.execute("INSERT INTO counter (id, value) VALUES (1, 0)")
    conn.commit()
    conn.close()


def read_counter(db_path):
    """Return the current counter value."""
    conn = get_connection(db_path)
    row = conn.execute("SELECT value FROM counter WHERE id = 1").fetchone()
    conn.close()
    return row[0] if row else None


# ---------------------------------------------------------------------------
# UNSAFE worker (no transaction — illustrates lost updates)
# ---------------------------------------------------------------------------

def unsafe_increment(db_path, delay_ms, results, idx):
    """
    Read current value, sleep, then write value+1.
    NO transaction: classic lost-update race condition.
    """
    try:
        conn = get_connection(db_path)
        # Step 1: Read
        row = conn.execute("SELECT value FROM counter WHERE id = 1").fetchone()
        current = row[0]

        # Step 2: Simulate processing time (amplifies the race window)
        if delay_ms > 0:
            time.sleep(delay_ms / 1000.0 + random.uniform(0, delay_ms / 2000.0))

        # Step 3: Write back (NO locking — another thread may have changed value!)
        conn.execute("UPDATE counter SET value = ? WHERE id = 1", (current + 1,))
        conn.commit()
        conn.close()
        results[idx] = "ok"
    except Exception as e:
        results[idx] = f"error: {e}"


# ---------------------------------------------------------------------------
# SAFE worker (with transaction — serializes updates)
# ---------------------------------------------------------------------------

def safe_increment(db_path, delay_ms, results, idx):
    """
    Read and write inside a transaction with IMMEDIATE locking.
    Retries on 'database is locked' errors.
    """
    max_retries = 20
    for attempt in range(max_retries):
        try:
            conn = get_connection(db_path)
            # IMMEDIATE acquires a write lock at BEGIN, preventing lost updates
            conn.execute("BEGIN IMMEDIATE")

            row = conn.execute("SELECT value FROM counter WHERE id = 1").fetchone()
            current = row[0]

            # Simulate processing time (safe inside a locked transaction)
            if delay_ms > 0:
                time.sleep(delay_ms / 1000.0 + random.uniform(0, delay_ms / 2000.0))

            conn.execute("UPDATE counter SET value = ? WHERE id = 1", (current + 1,))
            conn.execute("COMMIT")
            conn.close()
            results[idx] = "ok"
            return
        except sqlite3.OperationalError as e:
            if "locked" in str(e).lower() and attempt < max_retries - 1:
                time.sleep(0.005 * (2 ** min(attempt, 5)) + random.uniform(0, 0.005))
                continue
            results[idx] = f"error after {attempt+1} retries: {e}"
            return
        except Exception as e:
            results[idx] = f"error: {e}"
            return


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------

def run_test(label, worker_fn, db_path, n_threads, delay_ms, quiet):
    """
    Spawn n_threads threads each calling worker_fn.
    Returns (final_value, successes, errors, elapsed_secs).
    """
    results = [None] * n_threads
    threads = []

    t_start = time.time()
    for i in range(n_threads):
        t = threading.Thread(target=worker_fn, args=(db_path, delay_ms, results, i))
        threads.append(t)

    for t in threads:
        t.start()
    for t in threads:
        t.join()

    elapsed = time.time() - t_start

    successes = sum(1 for r in results if r == "ok")
    errors = [r for r in results if r != "ok"]

    final_value = read_counter(db_path)
    return final_value, successes, errors, elapsed


# ---------------------------------------------------------------------------
# Pretty output
# ---------------------------------------------------------------------------

BOLD   = "\033[1m"
GREEN  = "\033[92m"
YELLOW = "\033[93m"
RED    = "\033[91m"
CYAN   = "\033[96m"
RESET  = "\033[0m"
DIM    = "\033[2m"


def bar(n, total, width=30):
    filled = int(round(n / total * width)) if total > 0 else 0
    return "[" + "#" * filled + "-" * (width - filled) + "]"


def print_result(label, final_value, expected, successes, errors, elapsed, n_threads):
    is_correct = final_value == expected
    status_color = GREEN if is_correct else RED
    status_label = "CORRECT" if is_correct else "LOST UPDATES"

    print(f"\n  {BOLD}{label}{RESET}")
    print(f"  {'─' * 54}")
    print(f"  Threads run   : {n_threads}")
    print(f"  Successful ops: {successes}")
    print(f"  Errors        : {len(errors)}")
    print(f"  Elapsed       : {elapsed:.3f}s")
    print(f"  Expected value: {expected}")
    print(f"  Actual value  : {status_color}{final_value}{RESET}  "
          f"{status_color}[{status_label}]{RESET}")

    if not is_correct:
        lost = expected - final_value
        pct  = lost / expected * 100 if expected > 0 else 0
        print(f"  Lost updates  : {RED}{lost} ({pct:.1f}% of increments were silently discarded){RESET}")
        print(f"\n  {DIM}Explanation: Thread A read value=X, Thread B also read value=X,")
        print(f"  Thread A wrote X+1, Thread B also wrote X+1.  One increment was lost.{RESET}")

    if errors:
        print(f"\n  {YELLOW}Sample errors:{RESET}")
        for e in errors[:5]:
            print(f"    {DIM}{e}{RESET}")


def print_explanation():
    print(f"""
{BOLD}╔══════════════════════════════════════════════════════════╗
║          Why Lost Updates Happen                         ║
╚══════════════════════════════════════════════════════════╝{RESET}

  {YELLOW}WITHOUT transactions (race condition timeline):{RESET}

    Thread A           Thread B
    ─────────          ─────────
    READ  value=5      READ  value=5
    (compute 5+1)      (compute 5+1)
    WRITE value=6      WRITE value=6
                                ← Both wrote 6, but we expected 7!
                                  One increment is LOST.

  {GREEN}WITH BEGIN IMMEDIATE transactions (serialized):{RESET}

    Thread A acquires write lock
    ─────────────────────────────────────────
    READ  value=5
    WRITE value=6
    COMMIT  → releases lock
                          Thread B acquires write lock
                          ─────────────────────────────
                          READ  value=6
                          WRITE value=7
                          COMMIT
                                ← Both increments preserved. ✓
""")


def print_summary_table(unsafe_result, safe_result, n_threads, runs):
    print(f"\n{BOLD}{'═' * 60}{RESET}")
    print(f"{BOLD}  SUMMARY{RESET}")
    print(f"{BOLD}{'═' * 60}{RESET}")
    print(f"  {'Metric':<28} {'UNSAFE':>10} {'SAFE':>10}")
    print(f"  {'─' * 54}")

    for (label, u_val, s_val) in [
        ("Expected value",         n_threads,                n_threads),
        ("Actual final value",     unsafe_result[0],         safe_result[0]),
        ("Lost updates",
            n_threads - unsafe_result[0],
            n_threads - safe_result[0]),
        ("Thread errors",          len(unsafe_result[2]),    len(safe_result[2])),
    ]:
        u_color = RED if (label == "Lost updates" and u_val > 0) else ""
        s_color = GREEN if (label in ("Actual final value", "Lost updates") and s_val == (n_threads if label == "Actual final value" else 0)) else ""
        print(f"  {label:<28} {u_color}{u_val:>10}{RESET} {s_color}{s_val:>10}{RESET}")

    print(f"  {'─' * 54}")
    u_verdict = f"{GREEN}PASS{RESET}" if unsafe_result[0] == n_threads else f"{RED}FAIL (lost updates){RESET}"
    s_verdict = f"{GREEN}PASS{RESET}" if safe_result[0] == n_threads else f"{RED}FAIL{RESET}"
    print(f"  {'Verdict':<28} {u_verdict:>10}   {s_verdict:>10}")
    print(f"{BOLD}{'═' * 60}{RESET}\n")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    args = parse_args()
    n_threads = args.threads
    db_path   = args.db
    delay_ms  = args.delay_ms

    print(f"\n{BOLD}Concurrent Counter Race Condition Demo{RESET}")
    print(f"  Threads  : {n_threads}")
    print(f"  DB       : {db_path}")
    print(f"  Delay    : {delay_ms}ms between READ and WRITE (amplifies races)")
    print(f"  Runs     : {args.runs}")

    print_explanation()

    all_unsafe = []
    all_safe   = []

    for run in range(1, args.runs + 1):
        if args.runs > 1:
            print(f"\n{BOLD}{'─' * 60}{RESET}")
            print(f"{BOLD}  Run {run}/{args.runs}{RESET}")
            print(f"{BOLD}{'─' * 60}{RESET}")

        # ── Test 1: UNSAFE (no transaction) ─────────────────────────────────
        print(f"\n{CYAN}[Test 1/2]{RESET} UNSAFE — read-then-write WITHOUT transaction")
        print(f"  Resetting counter to 0 ...")
        reset_counter(db_path)
        print(f"  Spawning {n_threads} threads (each reads value, sleeps, writes value+1) ...")

        unsafe = run_test(
            label="UNSAFE (no transaction)",
            worker_fn=unsafe_increment,
            db_path=db_path,
            n_threads=n_threads,
            delay_ms=delay_ms,
            quiet=args.quiet,
        )
        all_unsafe.append(unsafe)
        print_result(
            "UNSAFE result",
            final_value=unsafe[0],
            expected=n_threads,
            successes=unsafe[1],
            errors=unsafe[2],
            elapsed=unsafe[3],
            n_threads=n_threads,
        )

        # ── Test 2: SAFE (with transaction) ─────────────────────────────────
        print(f"\n{CYAN}[Test 2/2]{RESET} SAFE — read-then-write WITH BEGIN IMMEDIATE transaction")
        print(f"  Resetting counter to 0 ...")
        reset_counter(db_path)
        print(f"  Spawning {n_threads} threads (each uses a locked transaction) ...")

        safe = run_test(
            label="SAFE (with transaction)",
            worker_fn=safe_increment,
            db_path=db_path,
            n_threads=n_threads,
            delay_ms=delay_ms,
            quiet=args.quiet,
        )
        all_safe.append(safe)
        print_result(
            "SAFE result",
            final_value=safe[0],
            expected=n_threads,
            successes=safe[1],
            errors=safe[2],
            elapsed=safe[3],
            n_threads=n_threads,
        )

        print_summary_table(unsafe, safe, n_threads, args.runs)

    # ── Multi-run aggregate ──────────────────────────────────────────────────
    if args.runs > 1:
        avg_unsafe = sum(r[0] for r in all_unsafe) / args.runs
        avg_safe   = sum(r[0] for r in all_safe) / args.runs
        print(f"{BOLD}Aggregate over {args.runs} runs:{RESET}")
        print(f"  Average final value (UNSAFE) : {avg_unsafe:.1f} / {n_threads}")
        print(f"  Average final value (SAFE)   : {avg_safe:.1f} / {n_threads}")
        unsafe_passes = sum(1 for r in all_unsafe if r[0] == n_threads)
        safe_passes   = sum(1 for r in all_safe   if r[0] == n_threads)
        print(f"  UNSAFE passed {unsafe_passes}/{args.runs} runs (got exact count)")
        print(f"  SAFE   passed {safe_passes}/{args.runs} runs (got exact count)")
        print()


if __name__ == "__main__":
    main()
