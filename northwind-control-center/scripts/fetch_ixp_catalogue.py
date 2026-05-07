#!/usr/bin/env python3
"""
fetch_ixp_catalogue.py
======================
Pull IXP data from PeeringDB and rebuild the IXP section of
services/global_infra_service.py.

Selection criterion: net_count >= MIN_PEERS (number of networks peering at the IXP).
This is an objective, data-driven threshold — no editorial choices needed.

Coordinate resolution (in priority order):
  1. First facility lat/lng from PeeringDB  (depth=2)
  2. Nominatim geocoding of "city, country" (1 req/s rate limit)
  3. Skip the IXP if neither works

Run:
    cd northwind-control-center
    pip install requests
    python scripts/fetch_ixp_catalogue.py            # write in-place
    python scripts/fetch_ixp_catalogue.py --dry-run  # print only, no file write
    python scripts/fetch_ixp_catalogue.py --min-peers 100
"""

import argparse
import re
import sys
import time
from pathlib import Path

ROOT         = Path(__file__).resolve().parent.parent
SERVICE_FILE = ROOT / "services" / "global_infra_service.py"

PEERINGDB_URL = "https://www.peeringdb.com/api/ix"
NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"

# Both services require a descriptive User-Agent
HEADERS = {
    "User-Agent": "NorthwindCC-GlobalInfraDemo/1.0 (educational; csorfolydaniel@gmail.com)",
    "Accept":     "application/json",
}

DEFAULT_MIN_PEERS = 50   # captures ~100 IXPs globally — all continents represented

# Optional: set PEERINGDB_API_KEY env var or pass --api-key to lift rate limits.
# Free key: https://www.peeringdb.com/account/apikeys (sign up, then generate).
import os as _os
_ENV_API_KEY = _os.environ.get("PEERINGDB_API_KEY", "")

# Markers that delimit the IXP block inside the NODES list
MARKER_START = "# ── IXPs "
MARKER_END   = "# ── Digital Realty "


# ── Step 1: Fetch from PeeringDB ──────────────────────────────────────────────

CACHE_FILE = ROOT / "scripts" / "_peeringdb_ix_cache.json"
CACHE_TTL  = 86_400   # seconds — re-fetch after 24 h


def fetch_ixps(min_peers: int, args_api_key: str = "") -> list[dict]:
    import json, requests

    # Use cached response if fresh enough
    if CACHE_FILE.exists():
        age = time.time() - CACHE_FILE.stat().st_mtime
        if age < CACHE_TTL:
            print(f"[1/3] Loading IXPs from cache ({age/3600:.1f} h old) …")
            all_ix = json.loads(CACHE_FILE.read_text())
        else:
            all_ix = None
    else:
        all_ix = None

    if all_ix is None:
        hdrs = dict(HEADERS)
        api_key = args_api_key or _ENV_API_KEY
        if api_key:
            hdrs["Authorization"] = f"Api-Key {api_key}"
            print(f"[1/3] Fetching IXPs from PeeringDB (authenticated, depth=2) …")
        else:
            print(f"[1/3] Fetching IXPs from PeeringDB (anonymous, depth=2) …")
            print(f"      Tip: get a free API key at peeringdb.com/account/apikeys")
            print(f"           then pass --api-key KEY or set PEERINGDB_API_KEY=KEY")
        for attempt in range(1, 5):
            try:
                r = requests.get(
                    PEERINGDB_URL,
                    headers=hdrs,
                    params={"depth": 2},
                    timeout=90,
                )
                if r.status_code == 429:
                    if attempt == 4:
                        sys.exit(
                            "ERROR: PeeringDB rate-limited on all 4 attempts.\n"
                            "       Wait ~1 hour, or get a free API key:\n"
                            "       https://www.peeringdb.com/account/apikeys\n"
                            "       then: python fetch_ixp_catalogue.py --api-key YOUR_KEY"
                        )
                    wait = 60 * attempt
                    print(f"      429 rate-limit — waiting {wait}s (attempt {attempt}/4) …")
                    time.sleep(wait)
                    continue
                r.raise_for_status()
                all_ix = r.json()["data"]
                CACHE_FILE.write_text(json.dumps(all_ix))
                print(f"      Cached → {CACHE_FILE}")
                break
            except requests.exceptions.HTTPError as exc:
                if attempt == 4:
                    sys.exit(f"ERROR: PeeringDB fetch failed: {exc}")
                time.sleep(30)

        if all_ix is None:
            sys.exit("ERROR: PeeringDB fetch failed after all retries — check network access")

    print(f"      {len(all_ix)} total IXPs in PeeringDB")
    filtered = [ix for ix in all_ix if ix.get("net_count", 0) >= min_peers]
    print(f"      {len(filtered)} with >= {min_peers} member networks")
    return filtered


# ── Step 2: Resolve coordinates ───────────────────────────────────────────────

def coords_from_peeringdb(ix: dict) -> tuple[float, float] | tuple[None, None]:
    """Extract lat/lng from the first embedded facility (depth=2 response)."""
    for fac in ix.get("fac_set", []):
        if isinstance(fac, dict):
            lat = fac.get("latitude") or fac.get("lat")
            lng = fac.get("longitude") or fac.get("lng") or fac.get("lon")
            if lat is not None and lng is not None:
                try:
                    return float(lat), float(lng)
                except (TypeError, ValueError):
                    pass
    return None, None


_nominatim_cache: dict[str, tuple] = {}

def coords_from_nominatim(city: str, country: str) -> tuple[float, float] | tuple[None, None]:
    """Geocode 'city, country' via Nominatim (1 req/s rate-limit)."""
    import requests
    cache_key = f"{city}|{country}"
    if cache_key in _nominatim_cache:
        return _nominatim_cache[cache_key]

    time.sleep(1.1)   # Nominatim ToS: max 1 req/s
    try:
        r = requests.get(
            NOMINATIM_URL,
            headers=HEADERS,
            params={"q": f"{city}, {country}", "format": "json", "limit": 1},
            timeout=10,
        )
        r.raise_for_status()
        results = r.json()
        if results:
            result = float(results[0]["lat"]), float(results[0]["lon"])
            _nominatim_cache[cache_key] = result
            return result
    except Exception:
        pass

    _nominatim_cache[cache_key] = (None, None)
    return None, None


def resolve_coords(ix: dict) -> tuple[float, float] | tuple[None, None]:
    lat, lng = coords_from_peeringdb(ix)
    if lat is not None:
        return lat, lng
    return coords_from_nominatim(ix.get("city", ""), ix.get("country", ""))


# ── Step 3: Build catalogue entries ──────────────────────────────────────────

_KEY_RE = re.compile(r"[^a-z0-9]+")

def make_key(name: str, country: str) -> str:
    """Deterministic node key: ixp-<normalised-name>-<country>."""
    slug = _KEY_RE.sub("-", name.lower()).strip("-")
    return f"ixp-{slug}-{country.lower()}"[:52]


def build_entries(ixps: list[dict]) -> list[dict]:
    print("[2/3] Resolving coordinates …")
    entries  = []
    skipped  = []

    # Sort descending by peer count so the most significant appear first
    for ix in sorted(ixps, key=lambda x: -x.get("net_count", 0)):
        lat, lng = resolve_coords(ix)
        if lat is None:
            skipped.append(ix["name"])
            print(f"      SKIP (no coords):  {ix['name']:<30}  {ix['city']}, {ix['country']}")
            continue

        # Use org name as provider if available, fall back to IXP name
        org  = ix.get("org")
        prov = (org.get("name", ix["name"]) if isinstance(org, dict) else ix["name"])[:50]

        entries.append({
            "key":      make_key(ix["name"], ix["country"]),
            "label":    ix["name"],
            "provider": prov,
            "lat":      round(lat, 3),
            "lng":      round(lng, 3),
            "peers":    ix.get("net_count", 0),
        })
        print(f"      [{ix['net_count']:>4} peers]  {ix['name']:<32}  "
              f"{ix['city']:<20}  {ix['country']}  →  {lat:>8.3f}, {lng:>8.3f}")

    print(f"\n      Built: {len(entries)}  Skipped: {len(skipped)}")
    if skipped:
        print("      Skipped IXPs:", ", ".join(skipped))
    return entries


# ── Step 4: Render Python source block ───────────────────────────────────────

def render_block(entries: list[dict], min_peers: int) -> str:
    header = (
        f"    # ── IXPs — PeeringDB, net_count >= {min_peers} "
        f"({len(entries)} exchanges) ─────────────────────\n"
    )
    lines = [header]
    for e in entries:
        # Align columns for readability
        key_part   = f'"key": "{e["key"]}",'
        label_part = f'"label": "{e["label"]}",'
        prov_part  = f'"provider": "{e["provider"]}",'
        lines.append(
            f'    {{"key": "{e["key"]}", '
            f'"label": "{e["label"]}", '
            f'"provider": "{e["provider"]}", '
            f'"type": "ixp", '
            f'"lat": {e["lat"]:>8.3f}, '
            f'"lng": {e["lng"]:>8.3f}}},  # {e["peers"]} peers'
        )
    return "\n".join(lines) + "\n    "


# ── Step 5: Patch the service file ───────────────────────────────────────────

def patch_service(block: str, dry_run: bool) -> None:
    print("[3/3] Patching global_infra_service.py …")
    text = SERVICE_FILE.read_text()

    start = text.find(MARKER_START)
    end   = text.find(MARKER_END)

    if start == -1:
        sys.exit(f"ERROR: could not find start marker {MARKER_START!r} in {SERVICE_FILE}")
    if end == -1:
        sys.exit(f"ERROR: could not find end marker {MARKER_END!r} in {SERVICE_FILE}")
    if start >= end:
        sys.exit("ERROR: markers are in wrong order")

    # Trim to the start of the marker line
    start = text.rfind("\n", 0, start) + 1   # beginning of that line

    old_section = text[start:end]
    new_text    = text[:start] + block + text[end:]

    old_lines = old_section.count("\n")
    new_lines = block.count("\n")

    if dry_run:
        print(f"  --dry-run: would replace {old_lines} lines with {new_lines} lines")
        print("\n── First 20 lines of new block ──────────────────────────────────────")
        print("\n".join(block.splitlines()[:20]))
        print("  …")
        return

    # Backup
    backup = SERVICE_FILE.with_suffix(".py.ixp-bak")
    backup.write_text(text)
    print(f"  Backup  → {backup}")

    SERVICE_FILE.write_text(new_text)
    print(f"  Written → {SERVICE_FILE}")
    print(f"  IXP section: {old_lines} lines → {new_lines} lines")


# ── Main ─────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--dry-run",    action="store_true",
                        help="Print output without modifying any file")
    parser.add_argument("--min-peers",  type=int, default=DEFAULT_MIN_PEERS,
                        help=f"Minimum member count (default: {DEFAULT_MIN_PEERS})")
    parser.add_argument("--api-key",    default="",
                        help="PeeringDB API key (or set PEERINGDB_API_KEY env var). "
                             "Free at peeringdb.com/account/apikeys")
    args = parser.parse_args()

    try:
        import requests  # noqa: F401
    except ImportError:
        sys.exit("ERROR: 'requests' not installed — run: pip install requests")

    ixps    = fetch_ixps(args.min_peers, args_api_key=args.api_key)
    entries = build_entries(ixps)

    if not entries:
        sys.exit("ERROR: no IXPs resolved — check network access to PeeringDB and Nominatim")

    block = render_block(entries, args.min_peers)
    patch_service(block, dry_run=args.dry_run)

    print(f"\nDone — {len(entries)} IXPs written.")
    print("Restart Flask to rebuild the NetworkX graph with the new nodes.")


if __name__ == "__main__":
    main()
