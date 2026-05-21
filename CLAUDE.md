# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Running the App

```bash
cd northwind-control-center
pip install -r requirements.txt
python app.py          # http://0.0.0.0:5000  — default login: admin / admin
```

No build step. All frontend dependencies are CDN-loaded (see `package.json`).

## Environment Variables

Copy `.env.example` to `.env`. The critical ones:

```
SECRET_KEY=<random>
SQL_SERVER=localhost
SQL_DATABASE=Northwind
SQL_USERNAME=flask_user
SQL_PASSWORD=<pw>
SQL_SA_USERNAME=sa
SQL_SA_PASSWORD=<pw>
SQL_DRIVER=ODBC Driver 18 for SQL Server
SQL_ENCRYPT=yes
SQL_TRUST_SERVER_CERT=yes
FERNET_KEY=<generate with: python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())">
```

Optional (cloud infra, backup, WinRM, SSH, GCS) env vars are in `config.py`.

## Architecture

### Request Flow

```
Browser → Flask Blueprint (blueprints/*.py)
               → Service layer (services/*.py)
                    → SQL Server via pyodbc (db.py / db_adapter.py)
                    → Meta DB via SQLite (meta_db.py)
```

Blueprints are thin controllers — they validate input, call one service function, and return JSON or render a template. All business logic lives in services.

### Key Files

| File | Purpose |
|---|---|
| `app.py` | App factory, blueprint registration (lines 106–144), startup sequence |
| `config.py` | All env var parsing; `Config` class injected into `g` |
| `auth.py` | `@login_required` / `@admin_required` decorators; session user fetch |
| `db.py` | Raw pyodbc connection to SQL Server |
| `db_adapter.py` | Multi-DB router: SQLite / SQL Server / PostgreSQL / MySQL / Redis / Neo4j / MongoDB |
| `meta_db.py` | Local SQLite (`instance/meta.db`): users, registered connections, app config |
| `services/demo_service.py` | All animated demo state machines (log shipping, snapshot, merge replication, ACID, etc.) |

### Meta-Database (`instance/meta.db`)

Created automatically at startup. Stores users, external connection credentials (Fernet-encrypted), and the last-working SQL Server config (survives `.env` changes). Uses `_write_lock` for serialized writes.

### Startup Sequence (`app.py` lines 36–89)

1. Load persisted config from `meta_db` (overrides `.env` if a working config was saved)
2. Start SQL Server if stopped (Docker or systemd)
3. Try connection → fall back to `master` DB → fall back to SA credentials
4. Persist the working config back to `meta_db`
5. Start APScheduler background jobs (replication, backups)

### Demo State Machines (`services/demo_service.py`)

Each animated demo (Log Shipping, Snapshot, Merge Replication, ACID, Deadlock, Blockchain) runs in a background `threading.Thread` with a shared `_XY_STATE` dict and `_XY_LOCK`. The frontend polls `/demos/xy/state` at ~800 ms intervals. To change timing, edit `time.sleep()` or `range(N, 0, -1)` countdown values in `_xy_worker()`.

### Adding a New Demo

1. Add routes to `blueprints/demos_bp.py` (page + `/state` + `/start`)
2. Add state dict + worker + `start`/`get_state` functions to `services/demo_service.py`
3. Create `templates/demos/my_demo.html` (extend `base.html`, follow sidebar/map/globe pattern)
4. Create `static/js/demos/my_demo.js`
5. Add a card to `templates/demos/index_graph.html` or the relevant index page

### 2D/3D Map Pattern

Demos with maps follow a consistent pattern:
- Leaflet.js for 2D (`#xy-map`), CesiumJS 1.116 for 3D (`#xy-globe`), both `position:absolute;inset:0`
- CesiumJS is **lazy-initialized** on first "3D" button click — never load it eagerly
- Use `Cesium.Entity` API with `arcType: Cesium.ArcType.GEODESIC` for polylines (not Primitives)
- Use `PointPrimitiveCollection` for large point sets (handles 18k+ points at GPU level)
- Theme switching: listen for `document` → `themeChanged` custom event, swap CARTO dark/light tile URLs

### Critical Constants (do not change without checking callers)

```python
# services/graph_routing_service.py
FERRY_PENALTY = 1.5
ASTAR_EPSILON = 1.5

# services/demo_service.py — _chord() helper
# Must return 2*sin(km/(2*R)), NOT 2*R*sin(...) — wrong version generates 10M+ edges
```

## No Tests

There is no test suite. The `scripts/` directory has manual integration scripts (`acid_test.py`, `chaos_monkey.py`, `concurrent_insert_race.py`). Verification is done by running the app and exercising the UI.
