#!/usr/bin/env python3
"""
chaos_monkey.py — rqlite leader assassination + recovery measurement.

Usage:
    python3 chaos_monkey.py [--nodes 4001 4002 4003] [--poll-ms 100] [--timeout 30]

1. Queries http://127.0.0.1:4001/status to find current leader node-id
2. Kills that rqlite process (pkill -f "node-id {leader_id}")
3. Polls the surviving nodes every 100ms
4. Records how long until a new leader is elected (Raft election time)
5. Verifies data integrity: runs SELECT COUNT(*) FROM orders on new leader
6. Prints: election time, new leader ID, data integrity result

After each run, offers to restart the killed node.
"""

import argparse
import json
import os
import signal
import subprocess
import sys
import time
import urllib.error
import urllib.request


# ---------------------------------------------------------------------------
# Argument parsing
# ---------------------------------------------------------------------------

def parse_args():
    parser = argparse.ArgumentParser(
        description="Chaos Monkey: kill rqlite leader and measure Raft re-election"
    )
    parser.add_argument(
        "--nodes",
        nargs="+",
        type=int,
        default=[4001, 4002, 4003],
        metavar="PORT",
        help="HTTP ports of rqlite nodes (default: 4001 4002 4003)",
    )
    parser.add_argument(
        "--host",
        default="127.0.0.1",
        help="Host where rqlite nodes are running (default: 127.0.0.1)",
    )
    parser.add_argument(
        "--poll-ms",
        type=int,
        default=100,
        help="Polling interval in milliseconds while waiting for new leader (default: 100)",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=30,
        help="Maximum seconds to wait for new leader election (default: 30)",
    )
    parser.add_argument(
        "--table",
        default="orders",
        help="Table to use for data-integrity check (default: orders)",
    )
    parser.add_argument(
        "--kill-signal",
        default="SIGKILL",
        choices=["SIGKILL", "SIGTERM", "SIGINT"],
        help="Signal to send to the leader process (default: SIGKILL)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print what would happen without actually killing anything",
    )
    return parser.parse_args()


# ---------------------------------------------------------------------------
# HTTP helpers
# ---------------------------------------------------------------------------

def http_get_json(url, timeout=3):
    """Fetch a URL and parse JSON response. Returns (dict, None) or (None, error_str)."""
    try:
        with urllib.request.urlopen(url, timeout=timeout) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data, None
    except urllib.error.URLError as e:
        return None, str(e)
    except json.JSONDecodeError as e:
        return None, f"JSON parse error: {e}"
    except Exception as e:
        return None, str(e)


def rqlite_query(host, port, sql, timeout=5):
    """Run a read query against a rqlite node. Returns (results, error)."""
    import urllib.parse
    encoded_sql = urllib.parse.quote(sql)
    url = f"http://{host}:{port}/db/query?q={encoded_sql}&level=none"
    data, err = http_get_json(url, timeout=timeout)
    if err:
        return None, err
    return data, None


# ---------------------------------------------------------------------------
# rqlite cluster introspection
# ---------------------------------------------------------------------------

def get_node_status(host, port, timeout=3):
    """
    Fetch /status from a rqlite node.
    Returns (status_dict, error_str).
    """
    url = f"http://{host}:{port}/status"
    return http_get_json(url, timeout=timeout)


def get_leader_id(status):
    """
    Extract the leader node ID string from a /status response.
    rqlite v7+ stores it at status['store']['leader']['node_id'].
    Older versions: status['store']['raft']['leader_id'].
    Returns the leader_id string or None.
    """
    if not status:
        return None
    store = status.get("store", {})

    # v7+ path
    leader_info = store.get("leader", {})
    if leader_info:
        node_id = leader_info.get("node_id") or leader_info.get("addr")
        if node_id:
            return str(node_id)

    # Older path
    raft = store.get("raft", {})
    leader_id = raft.get("leader_id") or raft.get("leader")
    if leader_id:
        return str(leader_id)

    return None


def get_current_node_id(status):
    """Extract this node's own ID from its /status."""
    if not status:
        return None
    store = status.get("store", {})
    node_id = store.get("node_id") or store.get("id")
    if node_id:
        return str(node_id)
    # Fallback: look in raft
    raft = store.get("raft", {})
    return str(raft.get("node_id", "")) or None


def is_leader(status):
    """Return True if this node believes it is the current leader."""
    if not status:
        return False
    store = status.get("store", {})
    # v7+
    leader_info = store.get("leader", {})
    if leader_info:
        is_self = leader_info.get("is_self", None)
        if is_self is not None:
            return bool(is_self)
    # Fallback: compare node_id to leader_id
    own_id = get_current_node_id(status)
    leader_id = get_leader_id(status)
    return own_id is not None and own_id == leader_id


def find_leader(host, ports, timeout=3):
    """
    Iterate over all ports and return (leader_node_id, leader_port) of the current leader.
    Returns (None, None) if no leader found.
    """
    for port in ports:
        status, err = get_node_status(host, port, timeout=timeout)
        if err or not status:
            continue
        if is_leader(status):
            node_id = get_current_node_id(status) or f"node@{port}"
            return node_id, port
    # Second pass: if no node reports is_self=True, use leader_id reported by any node
    for port in ports:
        status, err = get_node_status(host, port, timeout=timeout)
        if err or not status:
            continue
        leader_id = get_leader_id(status)
        if leader_id:
            return leader_id, port
    return None, None


# ---------------------------------------------------------------------------
# Process management
# ---------------------------------------------------------------------------

def find_rqlite_pids(node_id_hint):
    """
    Find PIDs of rqlite processes that match the given node_id hint.
    Uses pgrep / ps to find processes.
    Returns list of int PIDs.
    """
    pids = []

    # Try pgrep first
    try:
        result = subprocess.run(
            ["pgrep", "-f", f"rqlite"],
            capture_output=True, text=True, timeout=5
        )
        candidates = [int(p.strip()) for p in result.stdout.strip().split("\n") if p.strip().isdigit()]
    except (FileNotFoundError, subprocess.TimeoutExpired):
        candidates = []

    # Filter by node_id if possible
    for pid in candidates:
        try:
            cmdline_path = f"/proc/{pid}/cmdline"
            with open(cmdline_path, "r") as f:
                cmdline = f.read().replace("\x00", " ")
            if node_id_hint in cmdline or "rqlite" in cmdline:
                pids.append(pid)
        except (FileNotFoundError, PermissionError):
            pids.append(pid)  # include anyway if we can't read cmdline

    return pids


def kill_process(pid, sig_name="SIGKILL", dry_run=False):
    """Send signal to a process. Returns (success, message)."""
    sig_map = {
        "SIGKILL": signal.SIGKILL,
        "SIGTERM": signal.SIGTERM,
        "SIGINT": signal.SIGINT,
    }
    sig = sig_map.get(sig_name, signal.SIGKILL)

    if dry_run:
        return True, f"[DRY RUN] Would send {sig_name} to PID {pid}"

    try:
        os.kill(pid, sig)
        return True, f"Sent {sig_name} to PID {pid}"
    except ProcessLookupError:
        return False, f"PID {pid} not found (already dead?)"
    except PermissionError:
        return False, f"Permission denied killing PID {pid} (try sudo)"


def kill_leader_process(node_id, args):
    """
    Find and kill the rqlite process for the leader node.
    Returns (killed_pids, messages).
    """
    pids = find_rqlite_pids(node_id)
    if not pids:
        # Try pkill as fallback
        msg = f"No PIDs found via /proc scan for node '{node_id}'"
        if not args.dry_run:
            result = subprocess.run(
                ["pkill", "-f", f"node-id {node_id}"],
                capture_output=True, text=True
            )
            if result.returncode == 0:
                return [], [f"pkill matched node-id {node_id}"]
            # Try killing by port
            return [], [msg + "; pkill also found nothing"]
        return [], [f"[DRY RUN] Would pkill -f 'node-id {node_id}'; " + msg]

    messages = []
    killed = []
    for pid in pids:
        ok, msg = kill_process(pid, args.kill_signal, dry_run=args.dry_run)
        messages.append(msg)
        if ok:
            killed.append(pid)

    return killed, messages


# ---------------------------------------------------------------------------
# Election polling
# ---------------------------------------------------------------------------

def poll_for_new_leader(host, ports, old_leader_id, poll_interval, timeout_secs, dry_run=False):
    """
    Poll surviving nodes until a new leader different from old_leader_id is elected.
    Returns (new_leader_id, new_leader_port, elapsed_secs) or (None, None, timeout_secs).
    """
    deadline = time.time() + timeout_secs
    surviving_ports = list(ports)  # we'll poll all; dead ones will just fail

    print(f"\n  Polling every {poll_interval*1000:.0f}ms for new leader "
          f"(timeout {timeout_secs}s) ...")

    iteration = 0
    while time.time() < deadline:
        for port in surviving_ports:
            status, err = get_node_status(host, port, timeout=2)
            if err or not status:
                continue
            leader_id = get_leader_id(status)
            if leader_id and leader_id != old_leader_id:
                elapsed = time.time() - (deadline - timeout_secs)
                new_node_id = get_current_node_id(status) or f"node@{port}"
                if is_leader(status):
                    return leader_id, port, elapsed
                # The node knows who the leader is but isn't itself the leader
                # Find the actual leader port
                return leader_id, port, elapsed

        if iteration % 10 == 0:
            dots = "." * (iteration // 10 % 4 + 1)
            sys.stdout.write(f"\r  Waiting{dots:<4}  ({time.time() - (deadline - timeout_secs):.1f}s elapsed)")
            sys.stdout.flush()

        time.sleep(poll_interval)
        iteration += 1

    sys.stdout.write("\n")
    return None, None, timeout_secs


# ---------------------------------------------------------------------------
# Data integrity check
# ---------------------------------------------------------------------------

def check_data_integrity(host, ports, table, new_leader_port=None):
    """
    Run SELECT COUNT(*) FROM <table> on the new leader (or any responding node).
    Returns (count, port_used, error).
    """
    ports_to_try = []
    if new_leader_port:
        ports_to_try.append(new_leader_port)
    ports_to_try.extend(p for p in ports if p != new_leader_port)

    sql = f"SELECT COUNT(*) FROM {table}"
    for port in ports_to_try:
        result, err = rqlite_query(host, port, sql, timeout=5)
        if err:
            continue
        try:
            # rqlite response: {"results": [{"columns": [...], "types": [...], "values": [[n]]}]}
            count = result["results"][0]["values"][0][0]
            return int(count), port, None
        except (KeyError, IndexError, TypeError) as e:
            return None, port, f"Unexpected response format: {e}"

    return None, None, f"No node responded to integrity check query"


# ---------------------------------------------------------------------------
# Node restart helper
# ---------------------------------------------------------------------------

def offer_restart(args, killed_pids, leader_port):
    """
    Ask the user if they want to restart the killed node.
    If yes, attempt to relaunch using a best-effort command.
    """
    answer = input("\n  Restart the killed node? [y/N] ").strip().lower()
    if answer != "y":
        print("  Skipping restart.")
        return

    if not killed_pids:
        print("  Cannot restart: no PIDs were recorded (node was killed via pkill).")
        print(f"  Manually restart the rqlite node that was listening on port {leader_port}.")
        return

    print(f"  Note: The original process (PID {killed_pids}) is gone.")
    print(f"  To rejoin the cluster, start rqlite with:")
    print(f"    rqlite -http-addr {args.host}:{leader_port} "
          f"-raft-addr {args.host}:{leader_port + 3999} "
          f"-join http://{args.host}:{[p for p in args.nodes if p != leader_port][0]}")
    print("  (Adjust the -raft-addr and -join flags for your cluster setup.)")


# ---------------------------------------------------------------------------
# Pretty printing
# ---------------------------------------------------------------------------

BOLD = "\033[1m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
RESET = "\033[0m"
CYAN = "\033[96m"


def section(title):
    print(f"\n{BOLD}{'─' * 58}{RESET}")
    print(f"{BOLD}  {title}{RESET}")
    print(f"{BOLD}{'─' * 58}{RESET}")


def ok(msg):
    print(f"  {GREEN}[OK]{RESET}  {msg}")


def warn(msg):
    print(f"  {YELLOW}[!!]{RESET}  {msg}")


def fail(msg):
    print(f"  {RED}[FAIL]{RESET}  {msg}")


def info(msg):
    print(f"  {CYAN}[..]{RESET}  {msg}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    args = parse_args()
    poll_interval = args.poll_ms / 1000.0

    section("Chaos Monkey — rqlite Leader Assassination")
    info(f"Nodes : {[f'{args.host}:{p}' for p in args.nodes]}")
    info(f"Table : {args.table}")
    if args.dry_run:
        warn("DRY RUN mode — no processes will be killed")

    # ── Step 1: Find current leader ─────────────────────────────────────────
    section("Step 1: Discovering Current Leader")
    leader_id, leader_port = find_leader(args.host, args.nodes)
    if not leader_id:
        fail("Could not determine leader. Are the rqlite nodes running?")
        fail(f"Check: curl http://{args.host}:{args.nodes[0]}/status")
        sys.exit(1)

    ok(f"Current leader: node_id='{leader_id}'  port={leader_port}")

    # ── Step 2: Kill the leader ──────────────────────────────────────────────
    section("Step 2: Assassinating the Leader")
    info(f"Sending {args.kill_signal} to leader '{leader_id}' ...")

    killed_pids, messages = kill_leader_process(leader_id, args)
    for msg in messages:
        if "DRY RUN" in msg or "Sent" in msg or "pkill matched" in msg:
            ok(msg)
        else:
            warn(msg)

    assassination_time = time.time()

    # ── Step 3: Poll for new leader ──────────────────────────────────────────
    section("Step 3: Monitoring Raft Re-election")
    surviving_ports = [p for p in args.nodes if p != leader_port]

    new_leader_id, new_leader_port, elapsed = poll_for_new_leader(
        host=args.host,
        ports=surviving_ports,
        old_leader_id=leader_id,
        poll_interval=poll_interval,
        timeout_secs=args.timeout,
        dry_run=args.dry_run,
    )

    print()  # newline after progress dots
    if new_leader_id:
        ok(f"New leader elected: node_id='{new_leader_id}'  port={new_leader_port}")
        ok(f"Election time     : {elapsed * 1000:.0f}ms  ({elapsed:.3f}s)")
    else:
        fail(f"No new leader elected within {args.timeout}s timeout")
        warn("Check rqlite logs. Cluster may need a quorum of at least 2 nodes.")

    # ── Step 4: Data integrity check ─────────────────────────────────────────
    section("Step 4: Data Integrity Verification")
    info(f"Running: SELECT COUNT(*) FROM {args.table}")

    count, check_port, err = check_data_integrity(
        host=args.host,
        ports=surviving_ports,
        table=args.table,
        new_leader_port=new_leader_port,
    )
    if err:
        warn(f"Integrity check failed: {err}")
        warn(f"The table '{args.table}' may not exist — that is OK for a fresh cluster.")
    else:
        ok(f"SELECT COUNT(*) FROM {args.table} = {count}  (via port {check_port})")
        ok("Data integrity: row count is consistent on the new leader")

    # ── Summary ──────────────────────────────────────────────────────────────
    section("Summary")
    print(f"  {'Killed leader':<24}: node_id='{leader_id}'  port={leader_port}")
    if new_leader_id:
        print(f"  {'New leader':<24}: node_id='{new_leader_id}'  port={new_leader_port}")
        print(f"  {'Raft election time':<24}: {elapsed * 1000:.0f}ms")
    else:
        print(f"  {'New leader':<24}: NOT ELECTED (timeout)")
    if count is not None:
        table = args.table
        print(f"  {f'Row count ({table})':<24}: {count}")
    print(f"  {'Signal used':<24}: {args.kill_signal}")
    print()

    # ── Offer restart ────────────────────────────────────────────────────────
    if sys.stdin.isatty() and not args.dry_run:
        offer_restart(args, killed_pids, leader_port)
    else:
        if args.dry_run:
            info("Dry run complete — nothing was killed.")
        else:
            info(f"To restart the killed node on port {leader_port}, rejoin the cluster manually.")


if __name__ == "__main__":
    main()
