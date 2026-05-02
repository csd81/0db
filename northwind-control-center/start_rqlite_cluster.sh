#!/usr/bin/env bash
# start_rqlite_cluster.sh — spin up a 3-node rqlite cluster for local development
# Usage: bash start_rqlite_cluster.sh
# Stops any running cluster first, then starts 3 nodes and seeds Northwind sample data.

set -e

DATA_DIR=/tmp/rqlite
LOG_DIR=/tmp/rqlite/logs

echo "==> Stopping any existing rqlite processes..."
pkill -f rqlited 2>/dev/null && sleep 1 || true

echo "==> Cleaning data dirs..."
rm -rf "$DATA_DIR"
mkdir -p "$DATA_DIR"/{node1,node2,node3} "$LOG_DIR"

echo "==> Starting Node 1 (leader candidate) on :4001 / raft :4002 ..."
rqlited \
  -node-id node1 \
  -http-addr 127.0.0.1:4001 \
  -raft-addr 127.0.0.1:4002 \
  "$DATA_DIR/node1" >"$LOG_DIR/node1.log" 2>&1 &
NODE1_PID=$!
echo "    PID $NODE1_PID"

echo "==> Waiting for Node 1 to be ready..."
until curl -sf http://127.0.0.1:4001/status >/dev/null 2>&1; do sleep 0.5; done
echo "    Node 1 is up."

echo "==> Starting Node 2 on :4003 / raft :4004 ..."
rqlited \
  -node-id node2 \
  -http-addr 127.0.0.1:4003 \
  -raft-addr 127.0.0.1:4004 \
  -join http://127.0.0.1:4001 \
  "$DATA_DIR/node2" >"$LOG_DIR/node2.log" 2>&1 &
echo "    PID $!"

echo "==> Starting Node 3 on :4005 / raft :4006 ..."
rqlited \
  -node-id node3 \
  -http-addr 127.0.0.1:4005 \
  -raft-addr 127.0.0.1:4006 \
  -join http://127.0.0.1:4001 \
  "$DATA_DIR/node3" >"$LOG_DIR/node3.log" 2>&1 &
echo "    PID $!"

sleep 2

echo "==> Seeding Northwind sample data..."
curl -s -XPOST 'http://127.0.0.1:4001/db/execute' \
  -H 'Content-Type: application/json' \
  -d '[
    "CREATE TABLE IF NOT EXISTS orders (order_id INTEGER PRIMARY KEY, customer_id TEXT, employee_id INTEGER, order_date TEXT, ship_country TEXT, total REAL)",
    "CREATE TABLE IF NOT EXISTS products (product_id INTEGER PRIMARY KEY, product_name TEXT, category TEXT, unit_price REAL, units_in_stock INTEGER)",
    "INSERT OR IGNORE INTO products VALUES (1,'\''Chai'\'','\''Beverages'\'',18.00,39)",
    "INSERT OR IGNORE INTO products VALUES (2,'\''Chang'\'','\''Beverages'\'',19.00,17)",
    "INSERT OR IGNORE INTO products VALUES (3,'\''Aniseed Syrup'\'','\''Condiments'\'',10.00,13)",
    "INSERT OR IGNORE INTO products VALUES (4,'\''Chef Anton Cajun Seasoning'\'','\''Condiments'\'',22.00,53)",
    "INSERT OR IGNORE INTO products VALUES (5,'\''Grandma Boysenberry Spread'\'','\''Condiments'\'',25.00,120)",
    "INSERT OR IGNORE INTO orders VALUES (10248,'\''VINET'\'',5,'\''2025-01-04'\'','\''France'\'',440.00)",
    "INSERT OR IGNORE INTO orders VALUES (10249,'\''TOMSP'\'',6,'\''2025-01-05'\'','\''Germany'\'',1863.40)",
    "INSERT OR IGNORE INTO orders VALUES (10250,'\''HANAR'\'',4,'\''2025-01-08'\'','\''Brazil'\'',1552.60)",
    "INSERT OR IGNORE INTO orders VALUES (10251,'\''VICTE'\'',3,'\''2025-01-08'\'','\''France'\'',654.06)",
    "INSERT OR IGNORE INTO orders VALUES (10252,'\''SUPRD'\'',4,'\''2025-01-09'\'','\''Belgium'\'',3597.90)",
    "INSERT OR IGNORE INTO orders VALUES (10253,'\''HANAR'\'',3,'\''2025-01-10'\'','\''Brazil'\'',1444.80)",
    "INSERT OR IGNORE INTO orders VALUES (10254,'\''CHOPS'\'',5,'\''2025-01-11'\'','\''Switzerland'\'',625.20)"
  ]' | python3 -c "import sys,json; r=json.load(sys.stdin); print('  Seeded:', r)"

echo ""
echo "==> Cluster is running!"
echo "    Node 1 (leader): http://127.0.0.1:4001"
echo "    Node 2:          http://127.0.0.1:4003"
echo "    Node 3:          http://127.0.0.1:4005"
echo "    Logs:            $LOG_DIR/"
echo ""
echo "    Quick test: curl 'http://127.0.0.1:4001/db/query?q=SELECT+*+FROM+orders'"
echo ""
echo "    To stop: pkill -f rqlited"
