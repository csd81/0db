"""
Global Infrastructure Digital Twin — NetworkX routing service.

Two NetworkX graphs:
  G_terrestrial  — Cloud DCs ↔ IXPs ↔ Cable Landings, weighted by fiber latency
  G_starlink     — Cloud DCs ↔ Starlink Gateways ↔ Laser Mesh, weighted by vacuum latency

Latency model:
  fiber / submarine : km / 200 000 × 1000  ms  (light in glass  ≈ 2c/3)
  starlink_laser    : km / 300 000 × 1000  ms  (vacuum speed of light)
  starlink_uplink   : 12 ms fixed             (550 km slant + hardware framing)

Graphs are built once at module load from the hardcoded node/edge catalogue.
Both graphs are read-only after init — thread-safe for concurrent Flask requests.
"""
import math
import threading
import networkx as nx

# Optional fast k-NN (scipy + numpy). Falls back gracefully if absent.
try:
    import numpy as _np
    from scipy.spatial import cKDTree as _cKDTree
    _SCIPY = True
except ImportError:
    _SCIPY = False

# ---------------------------------------------------------------------------
# Speed constants
# ---------------------------------------------------------------------------
FIBER_KM_S        = 200_000   # km/s — speed of light in silica glass fibre
VACUUM_KM_S       = 300_000   # km/s — speed of light in vacuum
UPLINK_MS         = 12.0      # ms  — baseline ground↔satellite latency (satellite directly overhead)
UPLINK_EXTRA_MS   = 20.0      # ms  — max additional uplink latency from poor elevation geometry
CONGESTION_FACTOR = 0.5       # max latency multiplier at 100% business-hour load

# ---------------------------------------------------------------------------
# Satellite constellation constants
# ---------------------------------------------------------------------------
SAT_COUNT  = 10_000 if _SCIPY else 1_000   # Fibonacci sphere satellite count
SAT_ALT_KM = 550                            # km — Starlink Shell-1 altitude
R_SAT      = 6371.0 + SAT_ALT_KM           # km — orbital radius from Earth centre
SAT_ISL_K  = 4                             # ISL links per satellite (k-NN)
GW_SAT_K   = 3                             # ground-station → satellite uplinks

# ---------------------------------------------------------------------------
# Node catalogue
# ---------------------------------------------------------------------------
NODES = [
    # ── AWS Cloud Regions (32 of 39 commercial regions — one node per Region)
    # us-east-1 (163 facilities, 2.7 GW) is the gravitational centre of AWS's network.
    # ── Americas ───────────────────────────────────────────────────────────────
    {"key": "aws-us-east-1",      "label": "AWS us-east-1 (N.Virginia)",  "provider": "AWS", "type": "cloud_dc", "lat": 38.96,  "lng": -77.45},
    {"key": "aws-us-east-2",      "label": "AWS us-east-2 (Ohio)",        "provider": "AWS", "type": "cloud_dc", "lat": 39.96,  "lng": -82.99},
    {"key": "aws-us-west-1",      "label": "AWS us-west-1 (N.California)","provider": "AWS", "type": "cloud_dc", "lat": 37.36,  "lng":-121.97},
    {"key": "aws-us-west-2",      "label": "AWS us-west-2 (Oregon)",      "provider": "AWS", "type": "cloud_dc", "lat": 45.52,  "lng":-122.88},
    {"key": "aws-ca-central-1",   "label": "AWS ca-central-1 (Montreal)", "provider": "AWS", "type": "cloud_dc", "lat": 45.50,  "lng": -73.57},
    {"key": "aws-ca-west-1",      "label": "AWS ca-west-1 (Calgary)",     "provider": "AWS", "type": "cloud_dc", "lat": 51.05,  "lng":-114.07},
    {"key": "aws-sa-east-1",      "label": "AWS sa-east-1 (Sao Paulo)",   "provider": "AWS", "type": "cloud_dc", "lat":-23.55,  "lng": -46.63},
    {"key": "aws-mx-central-1",   "label": "AWS mx-central-1 (Mexico City)","provider":"AWS", "type": "cloud_dc", "lat": 19.43,  "lng": -99.13},
    # ── Europe ─────────────────────────────────────────────────────────────────
    {"key": "aws-eu-west-1",      "label": "AWS eu-west-1 (Ireland)",     "provider": "AWS", "type": "cloud_dc", "lat": 53.33,  "lng":  -6.25},
    {"key": "aws-eu-west-2",      "label": "AWS eu-west-2 (London)",      "provider": "AWS", "type": "cloud_dc", "lat": 51.51,  "lng":  -0.13},
    {"key": "aws-eu-west-3",      "label": "AWS eu-west-3 (Paris)",       "provider": "AWS", "type": "cloud_dc", "lat": 48.86,  "lng":   2.35},
    {"key": "aws-eu-central-1",   "label": "AWS eu-central-1 (Frankfurt)","provider": "AWS", "type": "cloud_dc", "lat": 50.11,  "lng":   8.68},
    {"key": "aws-eu-central-2",   "label": "AWS eu-central-2 (Zurich)",   "provider": "AWS", "type": "cloud_dc", "lat": 47.37,  "lng":   8.54},
    {"key": "aws-eu-north-1",     "label": "AWS eu-north-1 (Stockholm)",  "provider": "AWS", "type": "cloud_dc", "lat": 59.33,  "lng":  18.07},
    {"key": "aws-eu-south-1",     "label": "AWS eu-south-1 (Milan)",      "provider": "AWS", "type": "cloud_dc", "lat": 45.46,  "lng":   9.19},
    {"key": "aws-eu-south-2",     "label": "AWS eu-south-2 (Spain)",      "provider": "AWS", "type": "cloud_dc", "lat": 41.65,  "lng":  -0.88},
    # ── Middle East / Africa ───────────────────────────────────────────────────
    {"key": "aws-me-south-1",     "label": "AWS me-south-1 (Bahrain)",    "provider": "AWS", "type": "cloud_dc", "lat": 26.21,  "lng":  50.59},
    {"key": "aws-me-central-1",   "label": "AWS me-central-1 (UAE)",      "provider": "AWS", "type": "cloud_dc", "lat": 24.47,  "lng":  54.37},
    {"key": "aws-il-central-1",   "label": "AWS il-central-1 (Tel Aviv)", "provider": "AWS", "type": "cloud_dc", "lat": 32.08,  "lng":  34.78},
    {"key": "aws-af-south-1",     "label": "AWS af-south-1 (Cape Town)",  "provider": "AWS", "type": "cloud_dc", "lat":-33.93,  "lng":  18.42},
    # ── Asia Pacific ───────────────────────────────────────────────────────────
    {"key": "aws-ap-southeast-1", "label": "AWS ap-southeast-1 (Singapore)","provider":"AWS", "type": "cloud_dc", "lat":  1.35,  "lng": 103.82},
    {"key": "aws-ap-southeast-2", "label": "AWS ap-southeast-2 (Sydney)", "provider": "AWS", "type": "cloud_dc", "lat":-33.87,  "lng": 151.21},
    {"key": "aws-ap-southeast-3", "label": "AWS ap-southeast-3 (Jakarta)","provider": "AWS", "type": "cloud_dc", "lat": -6.21,  "lng": 106.85},
    {"key": "aws-ap-southeast-4", "label": "AWS ap-southeast-4 (Melbourne)","provider":"AWS", "type": "cloud_dc", "lat":-37.81,  "lng": 144.96},
    {"key": "aws-ap-southeast-5", "label": "AWS ap-southeast-5 (Malaysia)","provider":"AWS", "type": "cloud_dc", "lat":  3.14,  "lng": 101.69},
    {"key": "aws-ap-northeast-1", "label": "AWS ap-northeast-1 (Tokyo)",  "provider": "AWS", "type": "cloud_dc", "lat": 35.69,  "lng": 139.69},
    {"key": "aws-ap-northeast-2", "label": "AWS ap-northeast-2 (Seoul)",  "provider": "AWS", "type": "cloud_dc", "lat": 37.57,  "lng": 126.98},
    {"key": "aws-ap-northeast-3", "label": "AWS ap-northeast-3 (Osaka)",  "provider": "AWS", "type": "cloud_dc", "lat": 34.69,  "lng": 135.50},
    {"key": "aws-ap-south-1",     "label": "AWS ap-south-1 (Mumbai)",     "provider": "AWS", "type": "cloud_dc", "lat": 19.07,  "lng":  72.87},
    {"key": "aws-ap-south-2",     "label": "AWS ap-south-2 (Hyderabad)",  "provider": "AWS", "type": "cloud_dc", "lat": 17.39,  "lng":  78.49},
    {"key": "aws-ap-east-1",      "label": "AWS ap-east-1 (Hong Kong)",   "provider": "AWS", "type": "cloud_dc", "lat": 22.32,  "lng": 114.17},
    # ── AWS AI Campus Nodes (stub nodes — Anthropic training, not public transit)
    {"key": "aws-rainier-in",     "label": "AWS Project Rainier (New Carlisle IN)","provider":"AWS","type":"aws_ai","lat": 41.70,  "lng": -86.50},
    {"key": "aws-mississippi",    "label": "AWS AI Campus (Mississippi)", "provider": "AWS", "type": "aws_ai",   "lat": 32.40,  "lng": -90.12},
    {"key": "aws-ohio-ai",        "label": "AWS AI Campus (New Albany OH)","provider": "AWS", "type": "aws_ai",   "lat": 40.08,  "lng": -82.79},
    # ── GCP Cloud Regions (~35 of ~40 total — one node per Region, not per building)
    # gcp-us-central1 covers the Gemini Cluster (Council Bluffs IA campus).
    # ── Americas ───────────────────────────────────────────────────────────────
    {"key": "gcp-us-central1",    "label": "GCP us-central1 (Iowa)",          "provider": "GCP", "type": "cloud_dc", "lat": 41.26,  "lng": -95.86},
    {"key": "gcp-us-east1",       "label": "GCP us-east1 (S.Carolina)",       "provider": "GCP", "type": "cloud_dc", "lat": 33.18,  "lng": -80.01},
    {"key": "gcp-us-east4",       "label": "GCP us-east4 (N.Virginia)",       "provider": "GCP", "type": "cloud_dc", "lat": 38.95,  "lng": -77.34},
    {"key": "gcp-us-east5",       "label": "GCP us-east5 (Columbus OH)",      "provider": "GCP", "type": "cloud_dc", "lat": 39.96,  "lng": -82.99},
    {"key": "gcp-us-south1",      "label": "GCP us-south1 (Dallas TX)",       "provider": "GCP", "type": "cloud_dc", "lat": 32.78,  "lng": -96.80},
    {"key": "gcp-us-west1",       "label": "GCP us-west1 (Oregon)",           "provider": "GCP", "type": "cloud_dc", "lat": 45.59,  "lng":-122.79},
    {"key": "gcp-us-west2",       "label": "GCP us-west2 (Los Angeles)",      "provider": "GCP", "type": "cloud_dc", "lat": 34.05,  "lng":-118.24},
    {"key": "gcp-us-west4",       "label": "GCP us-west4 (Las Vegas NV)",     "provider": "GCP", "type": "cloud_dc", "lat": 36.17,  "lng":-115.14},
    {"key": "gcp-na-northeast1",  "label": "GCP northamerica-northeast1 (Montreal)","provider":"GCP","type":"cloud_dc","lat": 45.50, "lng": -73.57},
    {"key": "gcp-na-northeast2",  "label": "GCP northamerica-northeast2 (Toronto)","provider":"GCP","type":"cloud_dc","lat": 43.65,  "lng": -79.38},
    {"key": "gcp-sa-east1",       "label": "GCP southamerica-east1 (Sao Paulo)","provider":"GCP","type": "cloud_dc", "lat":-23.55,  "lng": -46.63},
    {"key": "gcp-sa-west1",       "label": "GCP southamerica-west1 (Santiago)","provider":"GCP", "type": "cloud_dc", "lat":-33.45,  "lng": -70.67},
    # ── Europe ─────────────────────────────────────────────────────────────────
    {"key": "gcp-europe-west1",   "label": "GCP europe-west1 (Belgium)",      "provider": "GCP", "type": "cloud_dc", "lat": 50.50,  "lng":  3.87},
    {"key": "gcp-europe-west2",   "label": "GCP europe-west2 (London)",       "provider": "GCP", "type": "cloud_dc", "lat": 51.51,  "lng": -0.13},
    {"key": "gcp-europe-west3",   "label": "GCP europe-west3 (Frankfurt)",    "provider": "GCP", "type": "cloud_dc", "lat": 50.10,  "lng":  8.70},
    {"key": "gcp-europe-west4",   "label": "GCP europe-west4 (Netherlands)",  "provider": "GCP", "type": "cloud_dc", "lat": 52.96,  "lng":  5.57},
    {"key": "gcp-europe-west6",   "label": "GCP europe-west6 (Zurich)",       "provider": "GCP", "type": "cloud_dc", "lat": 47.37,  "lng":  8.54},
    {"key": "gcp-europe-west9",   "label": "GCP europe-west9 (Paris)",        "provider": "GCP", "type": "cloud_dc", "lat": 48.86,  "lng":  2.35},
    {"key": "gcp-europe-sw1",     "label": "GCP europe-southwest1 (Madrid)",  "provider": "GCP", "type": "cloud_dc", "lat": 40.42,  "lng": -3.70},
    {"key": "gcp-europe-north1",  "label": "GCP europe-north1 (Finland)",     "provider": "GCP", "type": "cloud_dc", "lat": 60.57,  "lng": 27.19},
    {"key": "gcp-europe-central2","label": "GCP europe-central2 (Warsaw)",    "provider": "GCP", "type": "cloud_dc", "lat": 52.23,  "lng": 21.01},
    # ── Middle East / Africa ───────────────────────────────────────────────────
    {"key": "gcp-me-central1",    "label": "GCP me-central1 (Doha QA)",       "provider": "GCP", "type": "cloud_dc", "lat": 25.29,  "lng": 51.53},
    {"key": "gcp-me-west1",       "label": "GCP me-west1 (Tel Aviv IL)",      "provider": "GCP", "type": "cloud_dc", "lat": 32.08,  "lng": 34.78},
    {"key": "gcp-africa-south1",  "label": "GCP africa-south1 (Johannesburg)","provider": "GCP", "type": "cloud_dc", "lat":-26.20,  "lng": 28.04},
    # ── Asia Pacific ───────────────────────────────────────────────────────────
    {"key": "gcp-asia-east1",     "label": "GCP asia-east1 (Taiwan)",         "provider": "GCP", "type": "cloud_dc", "lat": 24.05,  "lng":120.55},
    {"key": "gcp-asia-east2",     "label": "GCP asia-east2 (Hong Kong)",      "provider": "GCP", "type": "cloud_dc", "lat": 22.32,  "lng":114.17},
    {"key": "gcp-asia-northeast1","label": "GCP asia-northeast1 (Tokyo)",     "provider": "GCP", "type": "cloud_dc", "lat": 35.70,  "lng":139.70},
    {"key": "gcp-asia-northeast2","label": "GCP asia-northeast2 (Osaka)",     "provider": "GCP", "type": "cloud_dc", "lat": 34.69,  "lng":135.50},
    {"key": "gcp-asia-northeast3","label": "GCP asia-northeast3 (Seoul)",     "provider": "GCP", "type": "cloud_dc", "lat": 37.57,  "lng":126.98},
    {"key": "gcp-asia-south1",    "label": "GCP asia-south1 (Mumbai)",        "provider": "GCP", "type": "cloud_dc", "lat": 19.07,  "lng": 72.87},
    {"key": "gcp-asia-south2",    "label": "GCP asia-south2 (Delhi)",         "provider": "GCP", "type": "cloud_dc", "lat": 28.61,  "lng": 77.21},
    {"key": "gcp-asia-southeast1","label": "GCP asia-southeast1 (Singapore)", "provider": "GCP", "type": "cloud_dc", "lat":  1.34,  "lng":103.80},
    {"key": "gcp-asia-southeast2","label": "GCP asia-southeast2 (Jakarta)",   "provider": "GCP", "type": "cloud_dc", "lat": -6.21,  "lng":106.85},
    {"key": "gcp-australia-se1",  "label": "GCP australia-southeast1 (Sydney)","provider":"GCP", "type": "cloud_dc", "lat":-33.86,  "lng":151.20},
    {"key": "gcp-australia-se2",  "label": "GCP australia-southeast2 (Melbourne)","provider":"GCP","type":"cloud_dc","lat":-37.81,  "lng":144.96},
    # ── Azure Cloud DCs ────────────────────────────────────────────────────
    {"key": "az-eastus",          "label": "Azure East US (Virginia)",    "provider": "Azure",  "type": "cloud_dc",      "lat": 37.37,  "lng": -79.82},
    {"key": "az-westus",          "label": "Azure West US (California)",  "provider": "Azure",  "type": "cloud_dc",      "lat": 37.34,  "lng":-121.89},
    {"key": "az-southcentralus",  "label": "Azure S.Central US (Texas)", "provider": "Azure",  "type": "cloud_dc",      "lat": 29.42,  "lng": -98.49},
    {"key": "az-westeurope",      "label": "Azure West Europe (Amsterdam)","provider":"Azure",  "type": "cloud_dc",      "lat": 52.37,  "lng":  4.90},
    {"key": "az-northeurope",     "label": "Azure North Europe (Dublin)", "provider": "Azure",  "type": "cloud_dc",      "lat": 53.35,  "lng": -6.27},
    {"key": "az-uksouth",         "label": "Azure UK South (London)",     "provider": "Azure",  "type": "cloud_dc",      "lat": 51.51,  "lng": -0.13},
    {"key": "az-southeastasia",   "label": "Azure SE Asia (Singapore)",   "provider": "Azure",  "type": "cloud_dc",      "lat":  1.33,  "lng": 103.81},
    {"key": "az-japaneast",       "label": "Azure Japan East (Tokyo)",    "provider": "Azure",  "type": "cloud_dc",      "lat": 35.68,  "lng": 139.71},
    {"key": "az-australiaeast",   "label": "Azure Australia East (Sydney)","provider":"Azure",  "type": "cloud_dc",      "lat":-33.87,  "lng": 151.22},
    {"key": "az-brazilsouth",     "label": "Azure Brazil South (SP)",     "provider": "Azure",  "type": "cloud_dc",      "lat":-23.54,  "lng": -46.63},
    {"key": "az-centralindia",    "label": "Azure Central India (Pune)",  "provider": "Azure",  "type": "cloud_dc",      "lat": 18.52,  "lng":  73.86},
    {"key": "az-uaenorth",        "label": "Azure UAE North (Dubai)",      "provider": "Azure", "type": "cloud_dc", "lat": 25.20,  "lng":  55.27},
    # ── Azure Cloud Regions — expanded to 43 (70+ total exist; routing-relevant subset)
    # ── Americas ───────────────────────────────────────────────────────────────
    {"key": "az-centralus",       "label": "Azure Central US (Iowa)",      "provider": "Azure", "type": "cloud_dc", "lat": 41.59,  "lng": -93.62},
    {"key": "az-northcentralus",  "label": "Azure N.Central US (Chicago)", "provider": "Azure", "type": "cloud_dc", "lat": 41.87,  "lng": -87.63},
    {"key": "az-eastus2",         "label": "Azure East US 2 (Virginia)",   "provider": "Azure", "type": "cloud_dc", "lat": 36.60,  "lng": -78.86},
    {"key": "az-westus2",         "label": "Azure West US 2 (Washington)", "provider": "Azure", "type": "cloud_dc", "lat": 47.23,  "lng":-119.85},
    {"key": "az-westus3",         "label": "Azure West US 3 (Phoenix AZ)", "provider": "Azure", "type": "cloud_dc", "lat": 33.44,  "lng":-112.07},
    {"key": "az-canadacentral",   "label": "Azure Canada Central (Toronto)","provider":"Azure", "type": "cloud_dc", "lat": 43.65,  "lng": -79.38},
    {"key": "az-canadaeast",      "label": "Azure Canada East (Quebec)",   "provider": "Azure", "type": "cloud_dc", "lat": 46.81,  "lng": -71.22},
    {"key": "az-mexicocentral",   "label": "Azure Mexico Central (Queretaro)","provider":"Azure","type":"cloud_dc", "lat": 20.59,  "lng":-100.39},
    {"key": "az-brazilsoutheast", "label": "Azure Brazil SE (Rio)",        "provider": "Azure", "type": "cloud_dc", "lat":-22.92,  "lng": -43.17},
    # ── Europe ─────────────────────────────────────────────────────────────────
    {"key": "az-francecentral",   "label": "Azure France Central (Paris)", "provider": "Azure", "type": "cloud_dc", "lat": 48.86,  "lng":  2.35},
    {"key": "az-germanywestcentral","label":"Azure Germany WC (Frankfurt)","provider": "Azure", "type": "cloud_dc", "lat": 50.11,  "lng":  8.68},
    {"key": "az-switzerlandnorth","label": "Azure Switzerland N (Zurich)", "provider": "Azure", "type": "cloud_dc", "lat": 47.37,  "lng":  8.54},
    {"key": "az-norwayeast",      "label": "Azure Norway East (Oslo)",     "provider": "Azure", "type": "cloud_dc", "lat": 59.91,  "lng": 10.74},
    {"key": "az-swedencentral",   "label": "Azure Sweden Central (Gavle)", "provider": "Azure", "type": "cloud_dc", "lat": 60.67,  "lng": 17.14},
    {"key": "az-polandcentral",   "label": "Azure Poland Central (Warsaw)","provider": "Azure", "type": "cloud_dc", "lat": 52.23,  "lng": 21.01},
    {"key": "az-italynorth",      "label": "Azure Italy North (Milan)",    "provider": "Azure", "type": "cloud_dc", "lat": 45.46,  "lng":  9.19},
    {"key": "az-spaincentral",    "label": "Azure Spain Central (Madrid)", "provider": "Azure", "type": "cloud_dc", "lat": 40.42,  "lng": -3.70},
    # ── Middle East / Africa ───────────────────────────────────────────────────
    {"key": "az-qatarcentral",    "label": "Azure Qatar Central (Doha)",   "provider": "Azure", "type": "cloud_dc", "lat": 25.29,  "lng": 51.53},
    {"key": "az-israelcentral",   "label": "Azure Israel Central (Tel Aviv)","provider":"Azure","type": "cloud_dc", "lat": 32.08,  "lng": 34.78},
    {"key": "az-southafricanorth","label": "Azure S.Africa North (Joburg)","provider": "Azure", "type": "cloud_dc", "lat":-26.20,  "lng": 28.04},
    # ── Asia Pacific ───────────────────────────────────────────────────────────
    {"key": "az-eastasia",        "label": "Azure East Asia (Hong Kong)",  "provider": "Azure", "type": "cloud_dc", "lat": 22.32,  "lng":114.17},
    {"key": "az-koreacentral",    "label": "Azure Korea Central (Seoul)",  "provider": "Azure", "type": "cloud_dc", "lat": 37.57,  "lng":126.98},
    {"key": "az-japanwest",       "label": "Azure Japan West (Osaka)",     "provider": "Azure", "type": "cloud_dc", "lat": 34.69,  "lng":135.50},
    {"key": "az-australiacentral","label": "Azure Australia Central (Canberra)","provider":"Azure","type":"cloud_dc","lat":-35.31, "lng":149.12},
    {"key": "az-australiasoutheast","label":"Azure Australia SE (Melbourne)","provider":"Azure","type": "cloud_dc", "lat":-37.81,  "lng":144.96},
    {"key": "az-southindia",      "label": "Azure South India (Chennai)",  "provider": "Azure", "type": "cloud_dc", "lat": 13.08,  "lng": 80.27},
    {"key": "az-jioindiawest",    "label": "Azure Jio India West (Jamnagar)","provider":"Azure","type":"cloud_dc",  "lat": 22.47,  "lng": 70.06},
    {"key": "az-indonesiacentral","label": "Azure Indonesia Central (Jakarta)","provider":"Azure","type":"cloud_dc","lat": -6.21,  "lng":106.85},
    {"key": "az-malaysiawest",    "label": "Azure Malaysia West (KL)",     "provider": "Azure", "type": "cloud_dc", "lat":  3.14,  "lng":101.69},
    {"key": "az-taiwannorth",     "label": "Azure Taiwan North (Taipei)",  "provider": "Azure", "type": "cloud_dc", "lat": 25.04,  "lng":121.56},
    {"key": "az-newzealandnorth", "label": "Azure New Zealand N (Auckland)","provider":"Azure", "type": "cloud_dc", "lat":-36.87,  "lng":174.77},
    # ── Oracle Cloud DCs (Stargate JV backbone) ───────────────────────────────
    {"key": "oracle-ashburn",     "label": "Oracle Cloud Ashburn VA",     "provider": "Oracle", "type": "cloud_dc",      "lat": 39.04,  "lng": -77.49},
    {"key": "oracle-phoenix",     "label": "Oracle Cloud Phoenix AZ",     "provider": "Oracle", "type": "cloud_dc",      "lat": 33.43,  "lng":-112.05},
    {"key": "oracle-chicago",     "label": "Oracle Cloud Chicago IL",     "provider": "Oracle", "type": "cloud_dc",      "lat": 41.88,  "lng": -87.63},
    {"key": "oracle-amsterdam",   "label": "Oracle Cloud Amsterdam",      "provider": "Oracle", "type": "cloud_dc",      "lat": 52.37,  "lng":   4.90},
    {"key": "oracle-london",      "label": "Oracle Cloud London",         "provider": "Oracle", "type": "cloud_dc",      "lat": 51.51,  "lng":  -0.13},
    {"key": "oracle-saopaulo",    "label": "Oracle Cloud Sao Paulo",      "provider": "Oracle", "type": "cloud_dc",      "lat":-23.55,  "lng": -46.63},
    {"key": "oracle-dubai",       "label": "Oracle Cloud Dubai UAE",      "provider": "Oracle", "type": "cloud_dc",      "lat": 25.20,  "lng":  55.27},
    # ── OpenAI Stargate (stub nodes — private AI supercomputing clusters) ──────
    # Not public IXP participants. Wired exclusively to Azure + Oracle via dark fiber.
    {"key": "oai-lordstown",      "label": "Stargate OH (Lordstown)",     "provider": "OpenAI", "type": "openai_dc",     "lat": 41.16,  "lng": -80.83},
    {"key": "oai-dona-ana",       "label": "Stargate NM (Dona Ana Co.)", "provider": "OpenAI", "type": "openai_dc",     "lat": 32.32,  "lng":-106.77},
    {"key": "oai-milam-tx",       "label": "Stargate TX (Milam Co.)",    "provider": "OpenAI", "type": "openai_dc",     "lat": 30.77,  "lng": -96.99},
    {"key": "oai-shackelford",    "label": "Stargate TX (Shackelford)",  "provider": "OpenAI", "type": "openai_dc",     "lat": 32.73,  "lng": -99.34},
    {"key": "oai-patagonia",      "label": "Stargate Argentina (Neuquen)","provider":"OpenAI", "type": "openai_dc",     "lat":-38.95,  "lng": -68.07},
    {"key": "oai-uae",            "label": "Stargate UAE (Abu Dhabi)",   "provider": "OpenAI", "type": "openai_dc",     "lat": 24.47,  "lng":  54.37},
    # ── IXPs — PeeringDB, net_count >= 50 (257 exchanges) ─────────────────────

    {"key": "ixp-ix-br-ptt-br-s-o-paulo-br", "label": "IX.br (PTT.br) São Paulo", "provider": "IX.br (PTT.br) São Paulo", "type": "ixp", "lat":  -23.651, "lng":  -46.721},  # 1855 peers
    {"key": "ixp-de-cix-frankfurt-de", "label": "DE-CIX Frankfurt", "provider": "DE-CIX Frankfurt", "type": "ixp", "lat":   50.119, "lng":    8.735},  # 1016 peers
    {"key": "ixp-ams-ix-nl", "label": "AMS-IX", "provider": "AMS-IX", "type": "ixp", "lat":   52.356, "lng":    4.951},  # 856 peers
    {"key": "ixp-linx-lon1-gb", "label": "LINX LON1", "provider": "LINX LON1", "type": "ixp", "lat":   51.500, "lng":   -0.011},  # 843 peers
    {"key": "ixp-jkt-ix-id", "label": "JKT-IX", "provider": "JKT-IX", "type": "ixp", "lat":   -6.238, "lng":  106.823},  # 810 peers
    {"key": "ixp-iix-jakarta-id", "label": "IIX-Jakarta", "provider": "IIX-Jakarta", "type": "ixp", "lat":   -6.238, "lng":  106.824},  # 769 peers
    {"key": "ixp-openixp-nice-id", "label": "OpenIXP / NiCE", "provider": "OpenIXP / NiCE", "type": "ixp", "lat":   -2.483, "lng":  117.890},  # 606 peers
    {"key": "ixp-ix-br-ptt-br-fortaleza-br", "label": "IX.br (PTT.br) Fortaleza", "provider": "IX.br (PTT.br) Fortaleza", "type": "ixp", "lat":   -3.753, "lng":  -38.519},  # 603 peers
    {"key": "ixp-napafrica-ix-johannesburg-za", "label": "NAPAfrica IX Johannesburg", "provider": "NAPAfrica IX Johannesburg", "type": "ixp", "lat":  -26.138, "lng":   28.198},  # 543 peers
    {"key": "ixp-nl-ix-nl", "label": "NL-ix", "provider": "NL-ix", "type": "ixp", "lat":   52.356, "lng":    4.951},  # 526 peers
    {"key": "ixp-ix-br-ptt-br-rio-de-janeiro-br", "label": "IX.br (PTT.br) Rio de Janeiro", "provider": "IX.br (PTT.br) Rio de Janeiro", "type": "ixp", "lat":  -22.530, "lng":  -43.217},  # 512 peers
    {"key": "ixp-equinix-singapore-sg", "label": "Equinix Singapore", "provider": "Equinix Singapore", "type": "ixp", "lat":    1.295, "lng":  103.790},  # 463 peers
    {"key": "ixp-de-cix-mumbai-in", "label": "DE-CIX Mumbai", "provider": "DE-CIX Mumbai", "type": "ixp", "lat":   19.141, "lng":   73.009},  # 453 peers
    {"key": "ixp-france-ix-paris-fr", "label": "France-IX Paris", "provider": "France-IX Paris", "type": "ixp", "lat":   48.857, "lng":    2.385},  # 446 peers
    {"key": "ixp-fogixp-ch", "label": "FogIXP", "provider": "FogIXP", "type": "ixp", "lat":   47.450, "lng":    8.540},  # 419 peers
    {"key": "ixp-gnm-ix-nl", "label": "GNM-IX", "provider": "GNM-IX", "type": "ixp", "lat":   50.099, "lng":    8.632},  # 418 peers
    {"key": "ixp-epix-katowice-pl", "label": "EPIX.Katowice", "provider": "EPIX.Katowice", "type": "ixp", "lat":   50.262, "lng":   19.025},  # 396 peers
    {"key": "ixp-mix-it-it", "label": "MIX-IT", "provider": "MIX-IT", "type": "ixp", "lat":   45.476, "lng":    9.104},  # 392 peers
    {"key": "ixp-epix-warszawa-pl", "label": "EPIX.Warszawa", "provider": "EPIX.Warszawa", "type": "ixp", "lat":   52.227, "lng":   21.003},  # 382 peers
    {"key": "ixp-ar-ix-cabase-argentina-ar", "label": "AR-IX Cabase - Argentina", "provider": "AR-IX Cabase - Argentina", "type": "ixp", "lat":  -34.607, "lng":  -58.379},  # 373 peers
    {"key": "ixp-six-seattle-us", "label": "SIX Seattle", "provider": "SIX Seattle", "type": "ixp", "lat":   47.614, "lng": -122.339},  # 370 peers
    {"key": "ixp-bbix-tokyo-jp", "label": "BBIX Tokyo", "provider": "BBIX Tokyo", "type": "ixp", "lat":   35.687, "lng":  139.779},  # 349 peers
    {"key": "ixp-equinix-ashburn-us", "label": "Equinix Ashburn", "provider": "Equinix Ashburn", "type": "ixp", "lat":   39.016, "lng":  -77.459},  # 344 peers
    {"key": "ixp-aix-id", "label": "AIX", "provider": "AIX", "type": "ixp", "lat":   -6.441, "lng":  106.877},  # 335 peers
    {"key": "ixp-tpix-pl-pl", "label": "TPIX PL", "provider": "TPIX PL", "type": "ixp", "lat":   52.228, "lng":   21.005},  # 325 peers
    {"key": "ixp-linx-lon2-gb", "label": "LINX LON2", "provider": "LINX LON2", "type": "ixp", "lat":   51.500, "lng":   -0.011},  # 317 peers
    {"key": "ixp-msk-ix-moscow-ru", "label": "MSK-IX Moscow", "provider": "MSK-IX Moscow", "type": "ixp", "lat":   55.653, "lng":   37.529},  # 304 peers
    {"key": "ixp-lonap-gb", "label": "LONAP", "provider": "LONAP", "type": "ixp", "lat":   51.500, "lng":   -0.011},  # 302 peers
    {"key": "ixp-4b42-internet-exchange-point-ch", "label": "4b42 Internet Exchange Point", "provider": "4b42 Internet Exchange Point", "type": "ixp", "lat":   47.446, "lng":    8.211},  # 297 peers
    {"key": "ixp-kleyrex-de", "label": "KleyReX", "provider": "KleyReX", "type": "ixp", "lat":   50.119, "lng":    8.735},  # 285 peers
    {"key": "ixp-frys-ix-nl", "label": "Frys-IX", "provider": "Frys-IX", "type": "ixp", "lat":   52.356, "lng":    4.951},  # 284 peers
    {"key": "ixp-speed-ix-nl", "label": "Speed-IX", "provider": "Speed-IX", "type": "ixp", "lat":   52.356, "lng":    4.951},  # 283 peers
    {"key": "ixp-napafrica-ix-cape-town-za", "label": "NAPAfrica IX Cape Town", "provider": "NAPAfrica IX Cape Town", "type": "ixp", "lat":  -33.971, "lng":   18.465},  # 280 peers
    {"key": "ixp-locix-frankfurt-de", "label": "LOCIX FRANKFURT", "provider": "LOCIX FRANKFURT", "type": "ixp", "lat":   50.122, "lng":    8.745},  # 269 peers
    {"key": "ixp-de-cix-new-york-us", "label": "DE-CIX New York", "provider": "DE-CIX New York", "type": "ixp", "lat":   40.718, "lng":  -74.008},  # 267 peers
    {"key": "ixp-jpix-tokyo-jp", "label": "JPIX TOKYO", "provider": "JPIX TOKYO", "type": "ixp", "lat":   35.686, "lng":  139.765},  # 266 peers
    {"key": "ixp-any2west-us", "label": "Any2West", "provider": "Any2West", "type": "ixp", "lat":   34.048, "lng": -118.256},  # 266 peers
    {"key": "ixp-hkix-hk", "label": "HKIX", "provider": "HKIX", "type": "ixp", "lat":   22.420, "lng":  114.206},  # 261 peers
    {"key": "ixp-giganet-ixn-ua", "label": "Giganet IXN", "provider": "Giganet IXN", "type": "ixp", "lat":   50.551, "lng":   30.630},  # 260 peers
    {"key": "ixp-sgix-sg", "label": "SGIX", "provider": "SGIX", "type": "ixp", "lat":    1.337, "lng":  103.894},  # 251 peers
    {"key": "ixp-equinix-chicago-us", "label": "Equinix Chicago", "provider": "Equinix Chicago", "type": "ixp", "lat":   41.854, "lng":  -87.618},  # 250 peers
    {"key": "ixp-jpnap-tokyo-jp", "label": "JPNAP Tokyo", "provider": "JPNAP Tokyo", "type": "ixp", "lat":   35.617, "lng":  139.748},  # 250 peers
    {"key": "ixp-equinix-hong-kong-hk", "label": "Equinix Hong Kong", "provider": "Equinix Hong Kong", "type": "ixp", "lat":   22.366, "lng":  114.119},  # 244 peers
    {"key": "ixp-equinix-paris-fr", "label": "Equinix Paris", "provider": "Equinix Paris", "type": "ixp", "lat":   48.857, "lng":    2.385},  # 243 peers
    {"key": "ixp-piter-ix-st-petersburg-ru", "label": "PITER-IX St. Petersburg", "provider": "PITER-IX St. Petersburg", "type": "ixp", "lat":   59.935, "lng":   30.317},  # 243 peers
    {"key": "ixp-extreme-ix-mumbai-in", "label": "Extreme IX Mumbai", "provider": "Extreme IX Mumbai", "type": "ixp", "lat":   19.114, "lng":   72.893},  # 242 peers
    {"key": "ixp-ix-br-ptt-br-porto-alegre-br", "label": "IX.br (PTT.br) Porto Alegre", "provider": "IX.br (PTT.br) Porto Alegre", "type": "ixp", "lat":  -30.029, "lng":  -51.230},  # 240 peers
    {"key": "ixp-piter-ix-moscow-ru", "label": "PITER-IX Moscow", "provider": "PITER-IX Moscow", "type": "ixp", "lat":   55.653, "lng":   37.529},  # 237 peers
    {"key": "ixp-swissix-ch", "label": "SwissIX", "provider": "SwissIX", "type": "ixp", "lat":   47.433, "lng":    8.557},  # 235 peers
    {"key": "ixp-equinix-warsaw-pl", "label": "Equinix Warsaw", "provider": "Equinix Warsaw", "type": "ixp", "lat":   52.227, "lng":   21.003},  # 235 peers
    {"key": "ixp-torix-ca", "label": "TorIX", "provider": "TorIX", "type": "ixp", "lat":   43.645, "lng":  -79.384},  # 231 peers
    {"key": "ixp-megaix-sydney-au", "label": "MegaIX Sydney", "provider": "MegaIX Sydney", "type": "ixp", "lat":  -33.922, "lng":  151.188},  # 227 peers
    {"key": "ixp-equinix-sydney-au", "label": "Equinix Sydney", "provider": "Equinix Sydney", "type": "ixp", "lat":  -33.922, "lng":  151.188},  # 215 peers
    {"key": "ixp-bgp-exchange-frankfurt-de", "label": "BGP.Exchange - Frankfurt", "provider": "BGP.Exchange - Frankfurt", "type": "ixp", "lat":   50.111, "lng":    8.682},  # 210 peers
    {"key": "ixp-de-cix-dusseldorf-de", "label": "DE-CIX Dusseldorf", "provider": "DE-CIX Dusseldorf", "type": "ixp", "lat":   51.186, "lng":    6.870},  # 207 peers
    {"key": "ixp-cxc-jakarta-id", "label": "CXC Jakarta", "provider": "CXC Jakarta", "type": "ixp", "lat":   -6.238, "lng":  106.823},  # 206 peers
    {"key": "ixp-equinix-dallas-us", "label": "Equinix Dallas", "provider": "Equinix Dallas", "type": "ixp", "lat":   32.801, "lng":  -96.820},  # 204 peers
    {"key": "ixp-dtel-ix-ua", "label": "DTEL-IX", "provider": "DTEL-IX", "type": "ixp", "lat":   50.551, "lng":   30.630},  # 201 peers
    {"key": "ixp-namex-rome-it", "label": "Namex Rome", "provider": "Namex Rome", "type": "ixp", "lat":   41.899, "lng":   12.512},  # 199 peers
    {"key": "ixp-odix-omadata-id", "label": "ODIX Omadata", "provider": "ODIX Omadata", "type": "ixp", "lat":   -7.273, "lng":  112.743},  # 197 peers
    {"key": "ixp-nyiix-new-york-us", "label": "NYIIX New York", "provider": "NYIIX New York", "type": "ixp", "lat":   40.718, "lng":  -74.008},  # 196 peers
    {"key": "ixp-fl-ix-us", "label": "FL-IX", "provider": "FL-IX", "type": "ixp", "lat":   25.783, "lng":  -80.193},  # 195 peers
    {"key": "ixp-jinx-za", "label": "JINX", "provider": "JINX", "type": "ixp", "lat":  -25.928, "lng":   28.141},  # 193 peers
    {"key": "ixp-kcix-us", "label": "KCIX", "provider": "KCIX", "type": "ixp", "lat":   39.101, "lng":  -94.581},  # 193 peers
    {"key": "ixp-de-cix-madrid-es", "label": "DE-CIX Madrid", "provider": "DE-CIX Madrid", "type": "ixp", "lat":   40.439, "lng":   -3.621},  # 192 peers
    {"key": "ixp-netnod-stockholm-green-mtu1500-se", "label": "Netnod Stockholm GREEN -- MTU1500", "provider": "Netnod Stockholm GREEN -- MTU1500", "type": "ixp", "lat":   59.363, "lng":   17.956},  # 188 peers
    {"key": "ixp-peering-cz-cz", "label": "Peering.cz", "provider": "Peering.cz", "type": "ixp", "lat":   50.060, "lng":   14.483},  # 186 peers
    {"key": "ixp-interix-nl", "label": "INTERIX", "provider": "INTERIX", "type": "ixp", "lat":   52.033, "lng":    4.496},  # 184 peers
    {"key": "ixp-equinix-san-jose-us", "label": "Equinix San Jose", "provider": "Equinix San Jose", "type": "ixp", "lat":   37.242, "lng": -121.783},  # 182 peers
    {"key": "ixp-locix-dusseldorf-de", "label": "LOCIX DUSSELDORF", "provider": "LOCIX DUSSELDORF", "type": "ixp", "lat":   51.267, "lng":    6.818},  # 182 peers
    {"key": "ixp-de-cix-munich-de", "label": "DE-CIX Munich", "provider": "DE-CIX Munich", "type": "ixp", "lat":   48.143, "lng":   11.556},  # 181 peers
    {"key": "ixp-1-ix-eu-pl", "label": "1-IX EU", "provider": "1-IX EU", "type": "ixp", "lat":   52.227, "lng":   21.003},  # 181 peers
    {"key": "ixp-ix-australia-sydney-nsw-ix-au", "label": "IX Australia Sydney (NSW-IX)", "provider": "IX Australia Sydney (NSW-IX)", "type": "ixp", "lat":  -33.922, "lng":  151.188},  # 180 peers
    {"key": "ixp-netnod-stockholm-blue-mtu1500-se", "label": "Netnod Stockholm BLUE -- MTU1500", "provider": "Netnod Stockholm BLUE -- MTU1500", "type": "ixp", "lat":   59.363, "lng":   17.956},  # 178 peers
    {"key": "ixp-nixi-mumbai-in", "label": "NIXI Mumbai", "provider": "NIXI Mumbai", "type": "ixp", "lat":   19.114, "lng":   72.893},  # 177 peers
    {"key": "ixp-bix-jakarta-id", "label": "BIX Jakarta", "provider": "BIX Jakarta", "type": "ixp", "lat":   -6.238, "lng":  106.824},  # 177 peers
    {"key": "ixp-extreme-ix-delhi-in", "label": "Extreme IX Delhi", "provider": "Extreme IX Delhi", "type": "ixp", "lat":   28.631, "lng":   77.208},  # 175 peers
    {"key": "ixp-era-ix-amsterdam-nl", "label": "ERA-IX Amsterdam", "provider": "ERA-IX Amsterdam", "type": "ixp", "lat":   52.356, "lng":    4.951},  # 172 peers
    {"key": "ixp-nix-cz-cz", "label": "NIX.CZ", "provider": "NIX.CZ", "type": "ixp", "lat":   50.060, "lng":   14.483},  # 171 peers
    {"key": "ixp-ix-br-ptt-br-curitiba-br", "label": "IX.br (PTT.br) Curitiba", "provider": "IX.br (PTT.br) Curitiba", "type": "ixp", "lat":  -25.470, "lng":  -49.350},  # 171 peers
    {"key": "ixp-ix-br-ptt-br-bras-lia-br", "label": "IX.br (PTT.br) Brasília", "provider": "IX.br (PTT.br) Brasília", "type": "ixp", "lat":  -15.646, "lng":  -47.769},  # 170 peers
    {"key": "ixp-vix-at", "label": "VIX", "provider": "VIX", "type": "ixp", "lat":   48.214, "lng":   16.358},  # 169 peers
    {"key": "ixp-de-cix-hamburg-de", "label": "DE-CIX Hamburg", "provider": "DE-CIX Hamburg", "type": "ixp", "lat":   53.551, "lng":   10.047},  # 169 peers
    {"key": "ixp-bgp-exchange-amsterdam-nl", "label": "BGP.Exchange - Amsterdam", "provider": "BGP.Exchange - Amsterdam", "type": "ixp", "lat":   52.395, "lng":    4.864},  # 169 peers
    {"key": "ixp-equinix-miami-us", "label": "Equinix Miami", "provider": "Equinix Miami", "type": "ixp", "lat":   25.783, "lng":  -80.193},  # 167 peers
    {"key": "ixp-de-cix-jakarta-id", "label": "DE-CIX Jakarta", "provider": "DE-CIX Jakarta", "type": "ixp", "lat":   -6.239, "lng":  106.824},  # 166 peers
    {"key": "ixp-onix-ca", "label": "ONIX", "provider": "ONIX", "type": "ixp", "lat":   43.651, "lng":  -79.362},  # 165 peers
    {"key": "ixp-equinix-s-o-paulo-br", "label": "Equinix São Paulo", "provider": "Equinix São Paulo", "type": "ixp", "lat":  -23.498, "lng":  -46.815},  # 163 peers
    {"key": "ixp-tpix-tw-tw", "label": "TPIX-TW", "provider": "TPIX-TW", "type": "ixp", "lat":   25.073, "lng":  121.578},  # 162 peers
    {"key": "ixp-de-cix-dallas-us", "label": "DE-CIX Dallas", "provider": "DE-CIX Dallas", "type": "ixp", "lat":   32.801, "lng":  -96.819},  # 161 peers
    {"key": "ixp-espanix-madrid-lower-lan-es", "label": "ESpanix Madrid Lower LAN", "provider": "ESpanix Madrid Lower LAN", "type": "ixp", "lat":   40.466, "lng":   -3.661},  # 159 peers
    {"key": "ixp-piter-ix-frankfurt-de", "label": "PITER-IX Frankfurt", "provider": "PITER-IX Frankfurt", "type": "ixp", "lat":   50.099, "lng":    8.632},  # 154 peers
    {"key": "ixp-pit-santiago-pit-chile-cl", "label": "PIT Santiago - PIT Chile", "provider": "PIT Santiago - PIT Chile", "type": "ixp", "lat":  -33.358, "lng":  -70.676},  # 153 peers
    {"key": "ixp-ua-ix-ua", "label": "UA-IX", "provider": "UA-IX", "type": "ixp", "lat":   50.551, "lng":   30.630},  # 152 peers
    {"key": "ixp-digital-realty-atlanta-us", "label": "Digital Realty Atlanta", "provider": "Digital Realty Atlanta", "type": "ixp", "lat":   33.755, "lng":  -84.392},  # 151 peers
    {"key": "ixp-bbix-singapore-sg", "label": "BBIX Singapore", "provider": "BBIX Singapore", "type": "ixp", "lat":    1.295, "lng":  103.790},  # 149 peers
    {"key": "ixp-mice-us", "label": "MICE", "provider": "MICE", "type": "ixp", "lat":   44.971, "lng":  -93.255},  # 147 peers
    {"key": "ixp-bdix-bd", "label": "BDIX", "provider": "BDIX", "type": "ixp", "lat":   23.751, "lng":   90.386},  # 146 peers
    {"key": "ixp-thinx-warsaw-pl", "label": "THINX Warsaw", "provider": "THINX Warsaw", "type": "ixp", "lat":   52.185, "lng":   20.998},  # 145 peers
    {"key": "ixp-fcix-us", "label": "FCIX", "provider": "FCIX", "type": "ixp", "lat":   37.472, "lng": -121.920},  # 145 peers
    {"key": "ixp-de-cix-asean-sg", "label": "DE-CIX ASEAN", "provider": "DE-CIX ASEAN", "type": "ixp", "lat":    1.463, "lng":  103.772},  # 143 peers
    {"key": "ixp-global-ix-nl", "label": "Global-IX", "provider": "Global-IX", "type": "ixp", "lat":   55.653, "lng":   37.529},  # 142 peers
    {"key": "ixp-bgp-exchange-dusseldorf-de", "label": "BGP.Exchange - Dusseldorf", "provider": "BGP.Exchange - Dusseldorf", "type": "ixp", "lat":   51.225, "lng":    6.776},  # 142 peers
    {"key": "ixp-bcix-de", "label": "BCIX", "provider": "BCIX", "type": "ixp", "lat":   52.502, "lng":   13.369},  # 138 peers
    {"key": "ixp-linx-manchester-gb", "label": "LINX Manchester", "provider": "LINX Manchester", "type": "ixp", "lat":   53.463, "lng":   -2.237},  # 138 peers
    {"key": "ixp-netix-bg", "label": "NetIX", "provider": "NetIX", "type": "ixp", "lat":   50.119, "lng":    8.735},  # 135 peers
    {"key": "ixp-napafrica-ix-durban-za", "label": "NAPAfrica IX Durban", "provider": "NAPAfrica IX Durban", "type": "ixp", "lat":  -29.783, "lng":   30.990},  # 135 peers
    {"key": "ixp-eurasia-peering-ix-ru", "label": "Eurasia Peering IX", "provider": "Eurasia Peering IX", "type": "ixp", "lat":   55.862, "lng":   37.577},  # 135 peers
    {"key": "ixp-kixp-nairobi-ke", "label": "KIXP - Nairobi", "provider": "KIXP - Nairobi", "type": "ixp", "lat":   -1.340, "lng":   36.897},  # 132 peers
    {"key": "ixp-megaix-melbourne-au", "label": "MegaIX Melbourne", "provider": "MegaIX Melbourne", "type": "ixp", "lat":  -37.822, "lng":  144.931},  # 130 peers
    {"key": "ixp-edgeix-sydney-au", "label": "EdgeIX - Sydney", "provider": "EdgeIX - Sydney", "type": "ixp", "lat":  -33.785, "lng":  151.131},  # 130 peers
    {"key": "ixp-edgenxt-id", "label": "EdgeNXT", "provider": "EdgeNXT", "type": "ixp", "lat":   -6.291, "lng":  106.786},  # 130 peers
    {"key": "ixp-piter-ix-helsinki-fi", "label": "PITER-IX Helsinki", "provider": "PITER-IX Helsinki", "type": "ixp", "lat":   60.205, "lng":   24.922},  # 128 peers
    {"key": "ixp-bbix-osaka-jp", "label": "BBIX Osaka", "provider": "BBIX Osaka", "type": "ixp", "lat":   34.695, "lng":  135.491},  # 126 peers
    {"key": "ixp-interlan-ix-ro", "label": "InterLAN-IX", "provider": "InterLAN-IX", "type": "ixp", "lat":   50.099, "lng":    8.632},  # 125 peers
    {"key": "ixp-bix-bg-bg", "label": "BIX.BG", "provider": "BIX.BG", "type": "ixp", "lat":   42.703, "lng":   23.306},  # 124 peers
    {"key": "ixp-ix-br-ptt-br-salvador-br", "label": "IX.br (PTT.br) Salvador", "provider": "IX.br (PTT.br) Salvador", "type": "ixp", "lat":  -12.979, "lng":  -38.461},  # 122 peers
    {"key": "ixp-equinix-tokyo-jp", "label": "Equinix Tokyo", "provider": "Equinix Tokyo", "type": "ixp", "lat":   35.617, "lng":  139.748},  # 121 peers
    {"key": "ixp-myix-my", "label": "MyIX", "provider": "MyIX", "type": "ixp", "lat":    3.150, "lng":  101.706},  # 120 peers
    {"key": "ixp-stuix-tw", "label": "STUIX", "provider": "STUIX", "type": "ixp", "lat":   25.073, "lng":  121.578},  # 120 peers
    {"key": "ixp-nixi-delhi-in", "label": "NIXI Delhi", "provider": "NIXI Delhi", "type": "ixp", "lat":   28.625, "lng":   77.376},  # 117 peers
    {"key": "ixp-ix-br-ptt-br-recife-br", "label": "IX.br (PTT.br) Recife", "provider": "IX.br (PTT.br) Recife", "type": "ixp", "lat":   -8.058, "lng":  -34.890},  # 117 peers
    {"key": "ixp-ixpn-lagos-ng", "label": "IXPN Lagos", "provider": "IXPN Lagos", "type": "ixp", "lat":    6.427, "lng":    3.418},  # 116 peers
    {"key": "ixp-cinx-za", "label": "CINX", "provider": "CINX", "type": "ixp", "lat":  -33.919, "lng":   18.421},  # 114 peers
    {"key": "ixp-getafix-manila-ph", "label": "GetaFIX Manila", "provider": "GetaFIX Manila", "type": "ixp", "lat":   14.561, "lng":  121.017},  # 114 peers
    {"key": "ixp-evix-us", "label": "EVIX", "provider": "EVIX", "type": "ixp", "lat":   37.472, "lng": -121.920},  # 113 peers
    {"key": "ixp-jpix-osaka-jp", "label": "JPIX OSAKA", "provider": "JPIX OSAKA", "type": "ixp", "lat":   34.695, "lng":  135.491},  # 111 peers
    {"key": "ixp-megaix-frankfurt-de", "label": "MegaIX Frankfurt", "provider": "MegaIX Frankfurt", "type": "ixp", "lat":   50.099, "lng":    8.632},  # 111 peers
    {"key": "ixp-france-ix-marseille-fr", "label": "France-IX Marseille", "provider": "France-IX Marseille", "type": "ixp", "lat":   43.311, "lng":    5.374},  # 110 peers
    {"key": "ixp-cix-atl-us", "label": "CIX-ATL", "provider": "CIX-ATL", "type": "ixp", "lat":   33.755, "lng":  -84.392},  # 110 peers
    {"key": "ixp-fremix-us", "label": "FREMIX", "provider": "FREMIX", "type": "ixp", "lat":   37.472, "lng": -121.920},  # 110 peers
    {"key": "ixp-bgp-exchange-london-gb", "label": "BGP.Exchange - London", "provider": "BGP.Exchange - London", "type": "ixp", "lat":   51.507, "lng":   -0.128},  # 110 peers
    {"key": "ixp-ispab-nix-bd", "label": "ISPAB-NIX", "provider": "ISPAB-NIX", "type": "ixp", "lat":   23.764, "lng":   90.389},  # 110 peers
    {"key": "ixp-minap-milan-it", "label": "MINAP Milan", "provider": "MINAP Milan", "type": "ixp", "lat":   45.478, "lng":    9.105},  # 108 peers
    {"key": "ixp-de-cix-marseille-fr", "label": "DE-CIX Marseille", "provider": "DE-CIX Marseille", "type": "ixp", "lat":   43.311, "lng":    5.374},  # 108 peers
    {"key": "ixp-1-ix-ua-ua", "label": "1-IX UA", "provider": "1-IX UA", "type": "ixp", "lat":   50.445, "lng":   30.510},  # 107 peers
    {"key": "ixp-inex-lan1-ie", "label": "INEX LAN1", "provider": "INEX LAN1", "type": "ixp", "lat":   53.296, "lng":   -6.419},  # 106 peers
    {"key": "ixp-bix-hu", "label": "BiX", "provider": "BiX", "type": "ixp", "lat":   47.518, "lng":   19.056},  # 103 peers
    {"key": "ixp-uae-ix-ae", "label": "UAE-IX", "provider": "UAE-IX", "type": "ixp", "lat":   25.026, "lng":   55.187},  # 103 peers
    {"key": "ixp-lsix-nl", "label": "LSIX", "provider": "LSIX", "type": "ixp", "lat":   52.065, "lng":    4.387},  # 103 peers
    {"key": "ixp-equinix-new-york-us", "label": "Equinix New York", "provider": "Equinix New York", "type": "ixp", "lat":   40.741, "lng":  -74.003},  # 102 peers
    {"key": "ixp-top-ix-it", "label": "TOP-IX", "provider": "TOP-IX", "type": "ixp", "lat":   45.478, "lng":    9.102},  # 102 peers
    {"key": "ixp-jpnap-osaka-jp", "label": "JPNAP Osaka", "provider": "JPNAP Osaka", "type": "ixp", "lat":   34.676, "lng":  135.496},  # 102 peers
    {"key": "ixp-nine-fr", "label": "nine", "provider": "nine", "type": "ixp", "lat":   48.857, "lng":    2.385},  # 102 peers
    {"key": "ixp-ix-australia-melbourne-vic-ix-au", "label": "IX Australia Melbourne (VIC-IX)", "provider": "IX Australia Melbourne (VIC-IX)", "type": "ixp", "lat":  -37.822, "lng":  144.931},  # 101 peers
    {"key": "ixp-bbix-hong-kong-hk", "label": "BBIX Hong Kong", "provider": "BBIX Hong Kong", "type": "ixp", "lat":   22.266, "lng":  114.247},  # 101 peers
    {"key": "ixp-ix-br-ptt-br-florian-polis-br", "label": "IX.br (PTT.br) Florianópolis", "provider": "IX.br (PTT.br) Florianópolis", "type": "ixp", "lat":  -27.601, "lng":  -48.594},  # 98 peers
    {"key": "ixp-dinx-za", "label": "DINX", "provider": "DINX", "type": "ixp", "lat":  -29.783, "lng":   30.990},  # 98 peers
    {"key": "ixp-akl-ix-auckland-nz-nz", "label": "AKL-IX (Auckland NZ)", "provider": "AKL-IX (Auckland NZ)", "type": "ixp", "lat":  -36.849, "lng":  174.765},  # 98 peers
    {"key": "ixp-megaix-dusseldorf-de", "label": "MegaIX Dusseldorf", "provider": "MegaIX Dusseldorf", "type": "ixp", "lat":   51.186, "lng":    6.870},  # 95 peers
    {"key": "ixp-nwax-us", "label": "NWAX", "provider": "NWAX", "type": "ixp", "lat":   45.521, "lng": -122.681},  # 95 peers
    {"key": "ixp-megaix-brisbane-au", "label": "MegaIX Brisbane", "provider": "MegaIX Brisbane", "type": "ixp", "lat":  -27.466, "lng":  153.030},  # 94 peers
    {"key": "ixp-digital-edge-epix-jakarta-id", "label": "Digital Edge EPIX Jakarta", "provider": "Digital Edge EPIX Jakarta", "type": "ixp", "lat":   -6.239, "lng":  106.825},  # 92 peers
    {"key": "ixp-yycix-ca", "label": "YYCIX", "provider": "YYCIX", "type": "ixp", "lat":   51.047, "lng": -114.080},  # 91 peers
    {"key": "ixp-sfmix-us", "label": "SFMIX", "provider": "SFMIX", "type": "ixp", "lat":   37.789, "lng": -122.391},  # 90 peers
    {"key": "ixp-de-cix-delhi-in", "label": "DE-CIX Delhi", "provider": "DE-CIX Delhi", "type": "ixp", "lat":   28.631, "lng":   77.208},  # 90 peers
    {"key": "ixp-ix-denver-us", "label": "IX-Denver", "provider": "IX-Denver", "type": "ixp", "lat":   39.661, "lng": -104.850},  # 89 peers
    {"key": "ixp-pit-peru-lima-pe", "label": "PIT - Peru - Lima", "provider": "PIT - Peru - Lima", "type": "ixp", "lat":  -12.087, "lng":  -76.973},  # 89 peers
    {"key": "ixp-extreme-ix-chennai-in", "label": "Extreme IX Chennai", "provider": "Extreme IX Chennai", "type": "ixp", "lat":   13.065, "lng":   80.248},  # 88 peers
    {"key": "ixp-cdix-id", "label": "CDIX", "provider": "CDIX", "type": "ixp", "lat":   -6.239, "lng":  106.824},  # 87 peers
    {"key": "ixp-kinx-kr", "label": "KINX", "provider": "KINX", "type": "ixp", "lat":   37.488, "lng":  127.051},  # 85 peers
    {"key": "ixp-bbix-us-west-us", "label": "BBIX US-West", "provider": "BBIX US-West", "type": "ixp", "lat":   34.048, "lng": -118.256},  # 85 peers
    {"key": "ixp-bgp-exchange-zurich-ch", "label": "BGP.Exchange - Zurich", "provider": "BGP.Exchange - Zurich", "type": "ixp", "lat":   47.374, "lng":    8.541},  # 85 peers
    {"key": "ixp-sthix-stockholm-se", "label": "STHIX - Stockholm", "provider": "STHIX - Stockholm", "type": "ixp", "lat":   59.363, "lng":   17.956},  # 84 peers
    {"key": "ixp-equinix-los-angeles-us", "label": "Equinix Los Angeles", "provider": "Equinix Los Angeles", "type": "ixp", "lat":   34.048, "lng": -118.257},  # 83 peers
    {"key": "ixp-megaix-auckland-nz", "label": "MegaIX Auckland", "provider": "MegaIX Auckland", "type": "ixp", "lat":  -36.741, "lng":  174.729},  # 83 peers
    {"key": "ixp-equinix-frankfurt-de", "label": "Equinix Frankfurt", "provider": "Equinix Frankfurt", "type": "ixp", "lat":   50.098, "lng":    8.588},  # 83 peers
    {"key": "ixp-lu-cix-lu", "label": "LU-CIX", "provider": "LU-CIX", "type": "ixp", "lat":   49.788, "lng":    6.087},  # 82 peers
    {"key": "ixp-stlix-us", "label": "STLIX", "provider": "STLIX", "type": "ixp", "lat":   38.626, "lng":  -90.195},  # 81 peers
    {"key": "ixp-bbix-manila-ph", "label": "BBIX Manila", "provider": "BBIX Manila", "type": "ixp", "lat":   14.561, "lng":  121.017},  # 80 peers
    {"key": "ixp-bnix-be", "label": "BNIX", "provider": "BNIX", "type": "ixp", "lat":   50.871, "lng":    4.477},  # 79 peers
    {"key": "ixp-canix-montreal-ca", "label": "CANIX Montreal", "provider": "CANIX Montreal", "type": "ixp", "lat":   45.497, "lng":  -73.570},  # 79 peers
    {"key": "ixp-det-ix-us", "label": "DET-iX", "provider": "DET-iX", "type": "ixp", "lat":   42.472, "lng":  -83.238},  # 78 peers
    {"key": "ixp-zxix-hong-kong-hk", "label": "ZXIX Hong Kong", "provider": "ZXIX Hong Kong", "type": "ixp", "lat":   22.279, "lng":  114.163},  # 78 peers
    {"key": "ixp-sonix-stockholm-se", "label": "SONIX Stockholm", "provider": "SONIX Stockholm", "type": "ixp", "lat":   59.410, "lng":   17.949},  # 77 peers
    {"key": "ixp-vanix-ca", "label": "VANIX", "provider": "VANIX", "type": "ixp", "lat":   49.287, "lng": -123.120},  # 76 peers
    {"key": "ixp-ix-br-ptt-br-belo-horizonte-br", "label": "IX.br (PTT.br) Belo Horizonte", "provider": "IX.br (PTT.br) Belo Horizonte", "type": "ixp", "lat":  -19.920, "lng":  -43.937},  # 75 peers
    {"key": "ixp-vsix-it", "label": "VSIX", "provider": "VSIX", "type": "ixp", "lat":   45.389, "lng":   11.929},  # 75 peers
    {"key": "ixp-de-cix-chicago-us", "label": "DE-CIX Chicago", "provider": "DE-CIX Chicago", "type": "ixp", "lat":   41.876, "lng":  -87.631},  # 75 peers
    {"key": "ixp-ix-australia-perth-wa-ix-au", "label": "IX Australia Perth (WA-IX)", "provider": "IX Australia Perth (WA-IX)", "type": "ixp", "lat":  -31.956, "lng":  115.855},  # 74 peers
    {"key": "ixp-france-ix-aura-fr", "label": "France-IX AURA", "provider": "France-IX AURA", "type": "ixp", "lat":   45.723, "lng":    4.863},  # 74 peers
    {"key": "ixp-ix-australia-brisbane-qld-ix-au", "label": "IX Australia Brisbane (QLD-IX)", "provider": "IX Australia Brisbane (QLD-IX)", "type": "ixp", "lat":  -27.466, "lng":  153.030},  # 74 peers
    {"key": "ixp-de-cix-chennai-in", "label": "DE-CIX Chennai", "provider": "DE-CIX Chennai", "type": "ixp", "lat":   13.026, "lng":   80.272},  # 73 peers
    {"key": "ixp-netnod-stockholm-green-mtu4470-se", "label": "Netnod Stockholm GREEN -- MTU4470", "provider": "Netnod Stockholm GREEN -- MTU4470", "type": "ixp", "lat":   59.363, "lng":   17.956},  # 73 peers
    {"key": "ixp-netnod-stockholm-blue-mtu4470-se", "label": "Netnod Stockholm BLUE -- MTU4470", "provider": "Netnod Stockholm BLUE -- MTU4470", "type": "ixp", "lat":   59.363, "lng":   17.956},  # 73 peers
    {"key": "ixp-mass-ix-us", "label": "MASS-IX", "provider": "MASS-IX", "type": "ixp", "lat":   42.368, "lng":  -71.087},  # 72 peers
    {"key": "ixp-edgeix-melbourne-au", "label": "EdgeIX - Melbourne", "provider": "EdgeIX - Melbourne", "type": "ixp", "lat":  -37.822, "lng":  144.931},  # 72 peers
    {"key": "ixp-any2denver-us", "label": "Any2Denver", "provider": "Any2Denver", "type": "ixp", "lat":   39.746, "lng": -104.996},  # 71 peers
    {"key": "ixp-ix-br-ptt-br-vit-ria-br", "label": "IX.br (PTT.br) Vitória", "provider": "IX.br (PTT.br) Vitória", "type": "ixp", "lat":  -20.313, "lng":  -40.297},  # 71 peers
    {"key": "ixp-piter-ix-riga-lv", "label": "PITER-IX Riga", "provider": "PITER-IX Riga", "type": "ixp", "lat":   56.924, "lng":   24.137},  # 71 peers
    {"key": "ixp-era-ix-frankfurt-de", "label": "ERA-IX Frankfurt", "provider": "ERA-IX Frankfurt", "type": "ixp", "lat":   50.098, "lng":    8.588},  # 71 peers
    {"key": "ixp-equinix-palo-alto-us", "label": "Equinix Palo Alto", "provider": "Equinix Palo Alto", "type": "ixp", "lat":   37.446, "lng": -122.161},  # 70 peers
    {"key": "ixp-de-cix-istanbul-tr", "label": "DE-CIX Istanbul", "provider": "DE-CIX Istanbul", "type": "ixp", "lat":   40.994, "lng":   28.827},  # 70 peers
    {"key": "ixp-piter-ix-tallinn-ee", "label": "PITER-IX Tallinn", "provider": "PITER-IX Tallinn", "type": "ixp", "lat":   59.435, "lng":   24.715},  # 70 peers
    {"key": "ixp-iix-jawatimur-id", "label": "IIX-JawaTimur", "provider": "IIX-JawaTimur", "type": "ixp", "lat":   -7.273, "lng":  112.743},  # 69 peers
    {"key": "ixp-netnod-copenhagen-blue-mtu9k-dk", "label": "Netnod Copenhagen BLUE -- MTU9K", "provider": "Netnod Copenhagen BLUE -- MTU9K", "type": "ixp", "lat":   55.728, "lng":   12.377},  # 69 peers
    {"key": "ixp-bknix-thailand-th", "label": "BKNIX (Thailand)", "provider": "BKNIX (Thailand)", "type": "ixp", "lat":   13.770, "lng":  100.574},  # 68 peers
    {"key": "ixp-ams-ix-mumbai-in", "label": "AMS-IX Mumbai", "provider": "AMS-IX Mumbai", "type": "ixp", "lat":   19.114, "lng":   72.893},  # 68 peers
    {"key": "ixp-gr-ix-athens-gr", "label": "GR-IX::Athens", "provider": "GR-IX::Athens", "type": "ixp", "lat":   37.871, "lng":   23.870},  # 67 peers
    {"key": "ixp-edgeix-perth-au", "label": "EdgeIX - Perth", "provider": "EdgeIX - Perth", "type": "ixp", "lat":  -31.864, "lng":  115.896},  # 67 peers
    {"key": "ixp-inex-lan2-ie", "label": "INEX LAN2", "provider": "INEX LAN2", "type": "ixp", "lat":   53.296, "lng":   -6.419},  # 66 peers
    {"key": "ixp-w-ix-ru", "label": "W-IX", "provider": "W-IX", "type": "ixp", "lat":   55.653, "lng":   37.529},  # 66 peers
    {"key": "ixp-six-seattle-jumbo-us", "label": "SIX Seattle (Jumbo)", "provider": "SIX Seattle (Jumbo)", "type": "ixp", "lat":   47.614, "lng": -122.339},  # 66 peers
    {"key": "ixp-chix-ch-ch", "label": "CHIX-CH", "provider": "CHIX-CH", "type": "ixp", "lat":   47.388, "lng":    8.520},  # 66 peers
    {"key": "ixp-nix1-no", "label": "NIX1", "provider": "NIX1", "type": "ixp", "lat":   59.925, "lng":   10.810},  # 65 peers
    {"key": "ixp-netnod-copenhagen-green-mtu9k-dk", "label": "Netnod Copenhagen GREEN -- MTU9K", "provider": "Netnod Copenhagen GREEN -- MTU9K", "type": "ixp", "lat":   55.571, "lng":   12.936},  # 65 peers
    {"key": "ixp-transhybrid-ix-network-id", "label": "Transhybrid IX Network", "provider": "Transhybrid IX Network", "type": "ixp", "lat":    1.295, "lng":  103.790},  # 65 peers
    {"key": "ixp-ncix-neucentrix-id", "label": "NCIX - neuCentrIX", "provider": "NCIX - neuCentrIX", "type": "ixp", "lat":   -6.917, "lng":  107.611},  # 64 peers
    {"key": "ixp-chix-us", "label": "ChIX", "provider": "ChIX", "type": "ixp", "lat":   41.854, "lng":  -87.618},  # 63 peers
    {"key": "ixp-nix-sk-sk", "label": "NIX.SK", "provider": "NIX.SK", "type": "ixp", "lat":   48.119, "lng":   17.096},  # 63 peers
    {"key": "ixp-balt-ix-lt", "label": "BALT-IX", "provider": "BALT-IX", "type": "ixp", "lat":   54.637, "lng":   25.307},  # 63 peers
    {"key": "ixp-de-cix-lisbon-pt", "label": "DE-CIX Lisbon", "provider": "DE-CIX Lisbon", "type": "ixp", "lat":   38.788, "lng":   -9.123},  # 63 peers
    {"key": "ixp-qcix-us", "label": "QCIX", "provider": "QCIX", "type": "ixp", "lat":   41.548, "lng":  -90.621},  # 63 peers
    {"key": "ixp-houix-us", "label": "HOUIX", "provider": "HOUIX", "type": "ixp", "lat":   29.753, "lng":  -95.366},  # 62 peers
    {"key": "ixp-thailand-ix-th-ix-th", "label": "THAILAND IX (TH-IX)", "provider": "THAILAND IX (TH-IX)", "type": "ixp", "lat":   13.725, "lng":  100.516},  # 61 peers
    {"key": "ixp-unm-exch-canada-west-ca", "label": "UNM-Exch Canada-West", "provider": "UNM-Exch Canada-West", "type": "ixp", "lat":   49.259, "lng": -123.030},  # 61 peers
    {"key": "ixp-six-sk-sk", "label": "SIX.SK", "provider": "SIX.SK", "type": "ixp", "lat":   48.151, "lng":   17.113},  # 60 peers
    {"key": "ixp-ficix-2-helsinki-fi", "label": "FICIX 2 (Helsinki)", "provider": "FICIX 2 (Helsinki)", "type": "ixp", "lat":   60.205, "lng":   24.922},  # 60 peers
    {"key": "ixp-citraix-yogyakarta-id", "label": "CitraIX Yogyakarta", "provider": "CitraIX Yogyakarta", "type": "ixp", "lat":   -7.779, "lng":  110.395},  # 60 peers
    {"key": "ixp-ixplay-global-peers-es", "label": "IXPlay Global Peers", "provider": "IXPlay Global Peers", "type": "ixp", "lat":   40.439, "lng":   -3.621},  # 60 peers
    {"key": "ixp-poema-ix-tw", "label": "Poema IX", "provider": "Poema IX", "type": "ixp", "lat":   25.038, "lng":  121.562},  # 60 peers
    {"key": "ixp-gnm-ix-ua-ua", "label": "GNM-IX UA", "provider": "GNM-IX UA", "type": "ixp", "lat":   50.450, "lng":   30.524},  # 60 peers
    {"key": "ixp-protocol-7-ix-hong-kong-hk", "label": "Protocol 7 IX - Hong Kong", "provider": "Protocol 7 IX - Hong Kong", "type": "ixp", "lat":   22.279, "lng":  114.163},  # 60 peers
    {"key": "ixp-msk-ix-saint-petersburg-ru", "label": "MSK-IX Saint-Petersburg", "provider": "MSK-IX Saint-Petersburg", "type": "ixp", "lat":   59.984, "lng":   30.330},  # 59 peers
    {"key": "ixp-boston-internet-exchange-us", "label": "Boston Internet Exchange", "provider": "Boston Internet Exchange", "type": "ixp", "lat":   42.355, "lng":  -71.060},  # 59 peers
    {"key": "ixp-bgp-exchange-singapore-sg", "label": "BGP.Exchange - Singapore", "provider": "BGP.Exchange - Singapore", "type": "ixp", "lat":    1.357, "lng":  103.819},  # 59 peers
    {"key": "ixp-pit-colombia-bogota-co", "label": "PIT - Colombia - Bogota", "provider": "PIT - Colombia - Bogota", "type": "ixp", "lat":    4.752, "lng":  -74.142},  # 59 peers
    {"key": "ixp-nixi-chennai-in", "label": "NIXI Chennai", "provider": "NIXI Chennai", "type": "ixp", "lat":   12.990, "lng":   80.248},  # 58 peers
    {"key": "ixp-ninja-ix-phoenix-us", "label": "Ninja-IX Phoenix", "provider": "Ninja-IX Phoenix", "type": "ixp", "lat":   33.416, "lng": -112.009},  # 58 peers
    {"key": "ixp-megaix-perth-au", "label": "MegaIX Perth", "provider": "MegaIX Perth", "type": "ixp", "lat":  -31.864, "lng":  115.896},  # 58 peers
    {"key": "ixp-equinix-melbourne-au", "label": "Equinix Melbourne", "provider": "Equinix Melbourne", "type": "ixp", "lat":  -37.822, "lng":  144.915},  # 57 peers
    {"key": "ixp-equinix-amsterdam-nl", "label": "Equinix Amsterdam", "provider": "Equinix Amsterdam", "type": "ixp", "lat":   52.300, "lng":    4.943},  # 57 peers
    {"key": "ixp-cxc-denpasar-id", "label": "CXC Denpasar", "provider": "CXC Denpasar", "type": "ixp", "lat":   -8.655, "lng":  115.218},  # 57 peers
    {"key": "ixp-espanix-madrid-upper-lan-es", "label": "ESpanix Madrid Upper LAN", "provider": "ESpanix Madrid Upper LAN", "type": "ixp", "lat":   40.466, "lng":   -3.661},  # 56 peers
    {"key": "ixp-equinix-london-gb", "label": "Equinix London", "provider": "Equinix London", "type": "ixp", "lat":   51.524, "lng":   -0.636},  # 56 peers
    {"key": "ixp-dci-indonesia-dci-ix-id", "label": "DCI Indonesia DCI-IX", "provider": "DCI Indonesia DCI-IX", "type": "ixp", "lat":   -6.300, "lng":  107.089},  # 56 peers
    {"key": "ixp-f4ix-mci-us", "label": "F4IX MCI", "provider": "F4IX MCI", "type": "ixp", "lat":   39.137, "lng":  -94.578},  # 56 peers
    {"key": "ixp-digital-realty-new-york-us", "label": "Digital Realty New York", "provider": "Digital Realty New York", "type": "ixp", "lat":   40.718, "lng":  -74.008},  # 55 peers
    {"key": "ixp-b-ix-bg", "label": "B-IX", "provider": "B-IX", "type": "ixp", "lat":   42.703, "lng":   23.306},  # 55 peers
    {"key": "ixp-ix-br-ptt-br-goi-nia-br", "label": "IX.br (PTT.br) Goiânia", "provider": "IX.br (PTT.br) Goiânia", "type": "ixp", "lat":  -16.714, "lng":  -49.265},  # 55 peers
    {"key": "ixp-gigapix-lan-1-pt", "label": "GigaPIX - LAN 1", "provider": "GigaPIX - LAN 1", "type": "ixp", "lat":   38.756, "lng":   -9.147},  # 54 peers
    {"key": "ixp-megaix-hamburg-de", "label": "MegaIX Hamburg", "provider": "MegaIX Hamburg", "type": "ixp", "lat":   53.548, "lng":   10.044},  # 54 peers
    {"key": "ixp-linx-nova-us", "label": "LINX NoVA", "provider": "LINX NoVA", "type": "ixp", "lat":   38.951, "lng":  -77.365},  # 54 peers
    {"key": "ixp-cloud-ix-msk-ru", "label": "CLOUD-IX MSK", "provider": "CLOUD-IX MSK", "type": "ixp", "lat":   59.935, "lng":   30.317},  # 53 peers
    {"key": "ixp-bgp-exchange-fremont-us", "label": "BGP.Exchange - Fremont", "provider": "BGP.Exchange - Fremont", "type": "ixp", "lat":   37.548, "lng": -121.989},  # 53 peers
    {"key": "ixp-bgp-exchange-barcelona-es", "label": "BGP.Exchange - Barcelona", "provider": "BGP.Exchange - Barcelona", "type": "ixp", "lat":   41.349, "lng":    2.130},  # 53 peers
    {"key": "ixp-jkt-ix-surabaya-id", "label": "JKT-IX Surabaya", "provider": "JKT-IX Surabaya", "type": "ixp", "lat":   -7.246, "lng":  112.738},  # 53 peers
    {"key": "ixp-omahaix-us", "label": "OmahaIX", "provider": "OmahaIX", "type": "ixp", "lat":   41.257, "lng":  -95.938},  # 52 peers
    {"key": "ixp-edgeix-brisbane-au", "label": "EdgeIX - Brisbane", "provider": "EdgeIX - Brisbane", "type": "ixp", "lat":  -27.466, "lng":  153.030},  # 52 peers
    {"key": "ixp-nvix-us", "label": "NVIX", "provider": "NVIX", "type": "ixp", "lat":   39.016, "lng":  -77.459},  # 52 peers
    {"key": "ixp-solix-mtu1500-se", "label": "SOLIX MTU1500", "provider": "SOLIX MTU1500", "type": "ixp", "lat":   59.363, "lng":   17.956},  # 51 peers
    {"key": "ixp-ohio-ix-us", "label": "Ohio IX", "provider": "Ohio IX", "type": "ixp", "lat":   40.116, "lng":  -83.002},  # 51 peers
    {"key": "ixp-ix-br-ptt-br-s-o-lu-s-br", "label": "IX.br (PTT.br) São Luís", "provider": "IX.br (PTT.br) São Luís", "type": "ixp", "lat":   -2.507, "lng":  -44.242},  # 51 peers
    {"key": "ixp-mhk-ix-ph", "label": "MHK-IX", "provider": "MHK-IX", "type": "ixp", "lat":   14.561, "lng":  121.017},  # 51 peers
    {"key": "ixp-catnix-es", "label": "CATNIX", "provider": "CATNIX", "type": "ixp", "lat":   41.387, "lng":    2.112},  # 50 peers
    {"key": "ixp-bbix-amsterdam-nl", "label": "BBIX Amsterdam", "provider": "BBIX Amsterdam", "type": "ixp", "lat":   52.357, "lng":    4.953},  # 50 peers
    {"key": "ixp-bgp-exchange-hong-kong-hk", "label": "BGP.Exchange - Hong Kong", "provider": "BGP.Exchange - Hong Kong", "type": "ixp", "lat":   22.368, "lng":  114.137},  # 50 peers
    # ── Digital Realty (300+ DCs; listed as neutral IXP hubs for peering) ──────
    {"key": "dr-ashburn",         "label": "Digital Realty Ashburn VA",    "provider": "Digital Realty", "type": "ixp", "lat": 39.04,  "lng": -77.49},
    {"key": "dr-dallas",          "label": "Digital Realty Dallas TX",     "provider": "Digital Realty", "type": "ixp", "lat": 32.78,  "lng": -96.80},
    {"key": "dr-chicago",         "label": "Digital Realty Chicago IL",    "provider": "Digital Realty", "type": "ixp", "lat": 41.88,  "lng": -87.63},
    {"key": "dr-newyork",         "label": "Digital Realty New York",      "provider": "Digital Realty", "type": "ixp", "lat": 40.75,  "lng": -74.01},
    {"key": "dr-atlanta",         "label": "Digital Realty Atlanta GA",    "provider": "Digital Realty", "type": "ixp", "lat": 33.75,  "lng": -84.39},
    {"key": "dr-losangeles",      "label": "Digital Realty Los Angeles",   "provider": "Digital Realty", "type": "ixp", "lat": 34.05,  "lng":-118.24},
    {"key": "dr-london",          "label": "Digital Realty London (Slough)","provider":"Digital Realty", "type": "ixp", "lat": 51.50,  "lng":  -0.80},
    {"key": "dr-amsterdam",       "label": "Digital Realty Amsterdam",     "provider": "Digital Realty", "type": "ixp", "lat": 52.37,  "lng":   4.90},
    {"key": "dr-frankfurt",       "label": "Digital Realty Frankfurt",     "provider": "Digital Realty", "type": "ixp", "lat": 50.11,  "lng":   8.68},
    {"key": "dr-paris",           "label": "Digital Realty Paris",         "provider": "Digital Realty", "type": "ixp", "lat": 48.86,  "lng":   2.35},
    {"key": "dr-singapore",       "label": "Digital Realty Singapore",     "provider": "Digital Realty", "type": "ixp", "lat":  1.28,  "lng": 103.85},
    {"key": "dr-sydney",          "label": "Digital Realty Sydney",        "provider": "Digital Realty", "type": "ixp", "lat":-33.87,  "lng": 151.21},
    {"key": "dr-tokyo",           "label": "Digital Realty Tokyo",         "provider": "Digital Realty", "type": "ixp", "lat": 35.69,  "lng": 139.69},
    # ── Cable Landing Stations ─────────────────────────────────────────────
    {"key": "cls-new-york",       "label": "Cable Landing New York",       "provider": "Cable",  "type": "cable_landing", "lat": 40.57,  "lng": -73.97},
    {"key": "cls-miami",          "label": "Cable Landing Miami",          "provider": "Cable",  "type": "cable_landing", "lat": 25.73,  "lng": -80.28},
    {"key": "cls-los-angeles",    "label": "Cable Landing Los Angeles",    "provider": "Cable",  "type": "cable_landing", "lat": 33.74,  "lng":-118.29},
    {"key": "cls-seattle",        "label": "Cable Landing Seattle",        "provider": "Cable",  "type": "cable_landing", "lat": 47.61,  "lng":-122.34},
    {"key": "cls-hawaii",         "label": "Cable Landing Hawaii",         "provider": "Cable",  "type": "cable_landing", "lat": 21.30,  "lng":-157.85},
    {"key": "cls-guam",           "label": "Cable Landing Guam",           "provider": "Cable",  "type": "cable_landing", "lat": 13.44,  "lng": 144.79},
    {"key": "cls-fortaleza",      "label": "Cable Landing Fortaleza",      "provider": "Cable",  "type": "cable_landing", "lat": -3.72,  "lng": -38.54},
    {"key": "cls-rio",            "label": "Cable Landing Rio de Janeiro", "provider": "Cable",  "type": "cable_landing", "lat":-22.90,  "lng": -43.17},
    {"key": "cls-widemouth-bay",  "label": "Cable Landing Widemouth Bay",  "provider": "Cable",  "type": "cable_landing", "lat": 50.79,  "lng":  -4.56},
    {"key": "cls-lands-end",      "label": "Cable Landing Land's End",     "provider": "Cable",  "type": "cable_landing", "lat": 50.07,  "lng":  -5.71},
    {"key": "cls-lisbon",         "label": "Cable Landing Lisbon",         "provider": "Cable",  "type": "cable_landing", "lat": 38.71,  "lng":  -9.14},
    {"key": "cls-marseille",      "label": "Cable Landing Marseille",      "provider": "Cable",  "type": "cable_landing", "lat": 43.30,  "lng":   5.37},
    {"key": "cls-palermo",        "label": "Cable Landing Palermo",        "provider": "Cable",  "type": "cable_landing", "lat": 38.13,  "lng":  13.34},
    {"key": "cls-alexandria",     "label": "Cable Landing Alexandria",     "provider": "Cable",  "type": "cable_landing", "lat": 31.20,  "lng":  29.92},
    {"key": "cls-djibouti",       "label": "Cable Landing Djibouti",       "provider": "Cable",  "type": "cable_landing", "lat": 11.59,  "lng":  43.14},
    {"key": "cls-mumbai",         "label": "Cable Landing Mumbai",         "provider": "Cable",  "type": "cable_landing", "lat": 18.96,  "lng":  72.84},
    {"key": "cls-chennai",        "label": "Cable Landing Chennai",        "provider": "Cable",  "type": "cable_landing", "lat": 13.08,  "lng":  80.27},
    {"key": "cls-singapore",      "label": "Cable Landing Singapore",      "provider": "Cable",  "type": "cable_landing", "lat":  1.27,  "lng": 103.82},
    {"key": "cls-hong-kong",      "label": "Cable Landing Hong Kong",      "provider": "Cable",  "type": "cable_landing", "lat": 22.35,  "lng": 114.12},
    {"key": "cls-okinawa",        "label": "Cable Landing Okinawa",        "provider": "Cable",  "type": "cable_landing", "lat": 26.33,  "lng": 127.80},
    {"key": "cls-tokyo",          "label": "Cable Landing Tokyo",          "provider": "Cable",  "type": "cable_landing", "lat": 35.63,  "lng": 139.76},
    {"key": "cls-sydney",         "label": "Cable Landing Sydney",         "provider": "Cable",  "type": "cable_landing", "lat":-33.83,  "lng": 151.25},
    {"key": "cls-perth",          "label": "Cable Landing Perth",          "provider": "Cable",  "type": "cable_landing", "lat":-31.95,  "lng": 115.86},
    {"key": "cls-mombasa",        "label": "Cable Landing Mombasa",        "provider": "Cable",  "type": "cable_landing", "lat": -4.05,  "lng":  39.66},
    {"key": "cls-accra",          "label": "Cable Landing Accra",          "provider": "Cable",  "type": "cable_landing", "lat":  5.55,  "lng":  -0.19},
    # ── Chokepoints ────────────────────────────────────────────────────────
    {"key": "chk-suez",           "label": "Suez Canal",                   "provider": "—",      "type": "chokepoint",    "lat": 30.58,  "lng":  32.27},
    {"key": "chk-malacca",        "label": "Strait of Malacca",            "provider": "—",      "type": "chokepoint",    "lat":  2.50,  "lng": 101.40},
    {"key": "chk-hormuz",         "label": "Strait of Hormuz",             "provider": "—",      "type": "chokepoint",    "lat": 26.60,  "lng":  56.27},
    {"key": "chk-bab-el-mandeb",  "label": "Bab-el-Mandeb (Red Sea)",      "provider": "—",      "type": "chokepoint",    "lat": 12.58,  "lng":  43.50},
    {"key": "chk-engchan",        "label": "English Channel",              "provider": "—",      "type": "chokepoint",    "lat": 51.10,  "lng":   1.85},
    {"key": "chk-luzon",          "label": "Luzon Strait",                 "provider": "—",      "type": "chokepoint",    "lat": 20.50,  "lng": 122.00},
    {"key": "chk-gibraltar",      "label": "Strait of Gibraltar",          "provider": "—",      "type": "chokepoint",    "lat": 35.97,  "lng":  -5.45},
    {"key": "chk-good-hope",      "label": "Cape of Good Hope",            "provider": "—",      "type": "chokepoint",    "lat":-34.36,  "lng":  18.48},
    # ── Starlink Ground Stations ───────────────────────────────────────────
    {"key": "slgw-clarksburg",    "label": "Starlink GW Clarksburg MD",    "provider": "SpaceX", "type": "starlink_gw",   "lat": 39.12,  "lng": -77.18},
    {"key": "slgw-bastrop",       "label": "Starlink GW Bastrop TX",       "provider": "SpaceX", "type": "starlink_gw",   "lat": 30.11,  "lng": -97.32},
    {"key": "slgw-california",    "label": "Starlink GW California",       "provider": "SpaceX", "type": "starlink_gw",   "lat": 34.40,  "lng":-117.69},
    {"key": "slgw-hawaii",        "label": "Starlink GW Hawaii",           "provider": "SpaceX", "type": "starlink_gw",   "lat": 19.90,  "lng":-155.58},
    {"key": "slgw-alaska",        "label": "Starlink GW Alaska",           "provider": "SpaceX", "type": "starlink_gw",   "lat": 58.30,  "lng":-134.42},
    {"key": "slgw-toronto",       "label": "Starlink GW Toronto",          "provider": "SpaceX", "type": "starlink_gw",   "lat": 43.67,  "lng": -79.38},
    {"key": "slgw-chile",         "label": "Starlink GW Punta Arenas",     "provider": "SpaceX", "type": "starlink_gw",   "lat":-53.16,  "lng": -70.91},
    {"key": "slgw-brazil",        "label": "Starlink GW São Paulo",        "provider": "SpaceX", "type": "starlink_gw",   "lat":-23.62,  "lng": -46.52},
    {"key": "slgw-uk",            "label": "Starlink GW Buckinghamshire",  "provider": "SpaceX", "type": "starlink_gw",   "lat": 51.77,  "lng":  -0.81},
    {"key": "slgw-germany",       "label": "Starlink GW Landstuhl DE",     "provider": "SpaceX", "type": "starlink_gw",   "lat": 49.41,  "lng":   7.57},
    {"key": "slgw-sweden",        "label": "Starlink GW Kiruna SE",        "provider": "SpaceX", "type": "starlink_gw",   "lat": 67.86,  "lng":  20.23},
    {"key": "slgw-portugal",      "label": "Starlink GW Lisboa PT",        "provider": "SpaceX", "type": "starlink_gw",   "lat": 38.80,  "lng":  -9.15},
    {"key": "slgw-nigeria",       "label": "Starlink GW Lagos",            "provider": "SpaceX", "type": "starlink_gw",   "lat":  6.45,  "lng":   3.48},
    {"key": "slgw-southafrica",   "label": "Starlink GW Johannesburg",     "provider": "SpaceX", "type": "starlink_gw",   "lat":-26.20,  "lng":  28.04},
    {"key": "slgw-india",         "label": "Starlink GW Bengaluru",        "provider": "SpaceX", "type": "starlink_gw",   "lat": 12.97,  "lng":  77.59},
    {"key": "slgw-singapore",     "label": "Starlink GW Singapore",        "provider": "SpaceX", "type": "starlink_gw",   "lat":  1.29,  "lng": 103.79},
    {"key": "slgw-japan",         "label": "Starlink GW Inukai JP",        "provider": "SpaceX", "type": "starlink_gw",   "lat": 32.83,  "lng": 131.57},
    {"key": "slgw-taiwan",        "label": "Starlink GW Tainan TW",        "provider": "SpaceX", "type": "starlink_gw",   "lat": 23.00,  "lng": 120.21},
    {"key": "slgw-australia",     "label": "Starlink GW Blenheim NZ",      "provider": "SpaceX", "type": "starlink_gw",   "lat":-41.51,  "lng": 173.96},
    {"key": "slgw-uae",           "label": "Starlink GW Abu Dhabi UAE",    "provider": "SpaceX", "type": "starlink_gw",   "lat": 24.47,  "lng":  54.37},
    # ── Additional Starlink GWs — expanded to 35 for fuller global coverage ──────
    # Each GW arrays Ka-band antennas tracking LEO sats; laser ISLs run at 200 Gbps.
    {"key": "slgw-mexico",        "label": "Starlink GW Mexico City",      "provider": "SpaceX", "type": "starlink_gw",   "lat": 19.43,  "lng": -99.13},
    {"key": "slgw-colombia",      "label": "Starlink GW Bogota CO",        "provider": "SpaceX", "type": "starlink_gw",   "lat":  4.71,  "lng": -74.07},
    {"key": "slgw-spain",         "label": "Starlink GW Madrid ES",        "provider": "SpaceX", "type": "starlink_gw",   "lat": 40.42,  "lng":  -3.70},
    {"key": "slgw-poland",        "label": "Starlink GW Warsaw PL",        "provider": "SpaceX", "type": "starlink_gw",   "lat": 52.23,  "lng":  21.01},
    {"key": "slgw-turkey",        "label": "Starlink GW Istanbul TR",      "provider": "SpaceX", "type": "starlink_gw",   "lat": 41.01,  "lng":  28.98},
    {"key": "slgw-egypt",         "label": "Starlink GW Cairo EG",         "provider": "SpaceX", "type": "starlink_gw",   "lat": 30.06,  "lng":  31.25},
    {"key": "slgw-saudi",         "label": "Starlink GW Riyadh SA",        "provider": "SpaceX", "type": "starlink_gw",   "lat": 24.69,  "lng":  46.72},
    {"key": "slgw-kenya",         "label": "Starlink GW Nairobi KE",       "provider": "SpaceX", "type": "starlink_gw",   "lat": -1.29,  "lng":  36.82},
    {"key": "slgw-ethiopia",      "label": "Starlink GW Addis Ababa ET",   "provider": "SpaceX", "type": "starlink_gw",   "lat":  9.02,  "lng":  38.74},
    {"key": "slgw-thailand",      "label": "Starlink GW Bangkok TH",       "provider": "SpaceX", "type": "starlink_gw",   "lat": 13.75,  "lng": 100.52},
    {"key": "slgw-indonesia",     "label": "Starlink GW Jakarta ID",       "provider": "SpaceX", "type": "starlink_gw",   "lat": -6.21,  "lng": 106.85},
    {"key": "slgw-philippines",   "label": "Starlink GW Manila PH",        "provider": "SpaceX", "type": "starlink_gw",   "lat": 14.60,  "lng": 121.00},
    {"key": "slgw-newzealand",    "label": "Starlink GW Auckland NZ",      "provider": "SpaceX", "type": "starlink_gw",   "lat":-36.87,  "lng": 174.77},
    {"key": "slgw-kazakhstan",    "label": "Starlink GW Almaty KZ",        "provider": "SpaceX", "type": "starlink_gw",   "lat": 43.25,  "lng":  76.95},
    # ── Meta AI Campuses (~14 of ~35 total; major active facilities) ───────────
    # Meta peers at IXPs via AS32934; campuses connect to 2 nearest IXP hubs.
    # ── Americas ───────────────────────────────────────────────────────────────
    {"key": "meta-menlopark",     "label": "Meta HQ Campus (Menlo Park CA)","provider":"Meta",   "type": "meta_ai",       "lat": 37.48,  "lng":-122.15},
    {"key": "meta-altoona",       "label": "Meta DC Altoona IA",           "provider": "Meta",   "type": "meta_ai",       "lat": 41.64,  "lng": -93.47},
    {"key": "meta-prineville",    "label": "Meta DC Prineville OR",        "provider": "Meta",   "type": "meta_ai",       "lat": 44.30,  "lng":-120.84},
    {"key": "meta-eagle-mountain","label": "Meta DC Eagle Mountain UT",    "provider": "Meta",   "type": "meta_ai",       "lat": 40.31,  "lng":-111.93},
    {"key": "meta-los-lunas",     "label": "Meta DC Los Lunas NM",         "provider": "Meta",   "type": "meta_ai",       "lat": 34.80,  "lng":-106.73},
    {"key": "meta-fort-worth",    "label": "Meta DC Fort Worth TX",        "provider": "Meta",   "type": "meta_ai",       "lat": 32.75,  "lng": -97.33},
    {"key": "meta-forest-city",   "label": "Meta DC Forest City NC",       "provider": "Meta",   "type": "meta_ai",       "lat": 35.33,  "lng": -81.87},
    {"key": "meta-dekalb",        "label": "Meta DC DeKalb County GA",     "provider": "Meta",   "type": "meta_ai",       "lat": 33.83,  "lng": -84.14},
    {"key": "meta-gallatin",      "label": "Meta DC Gallatin TN",          "provider": "Meta",   "type": "meta_ai",       "lat": 36.39,  "lng": -86.45},
    {"key": "meta-new-albany",    "label": "Meta DC New Albany OH",        "provider": "Meta",   "type": "meta_ai",       "lat": 40.08,  "lng": -82.79},
    # ── Europe ─────────────────────────────────────────────────────────────────
    {"key": "meta-odense",        "label": "Meta DC Odense Denmark",       "provider": "Meta",   "type": "meta_ai",       "lat": 55.40,  "lng":  10.38},
    {"key": "meta-lulea",         "label": "Meta DC Lulea Sweden",         "provider": "Meta",   "type": "meta_ai",       "lat": 65.58,  "lng":  22.16},
    {"key": "meta-clonee",        "label": "Meta DC Clonee Ireland",       "provider": "Meta",   "type": "meta_ai",       "lat": 53.41,  "lng":  -6.40},
    # ── Asia Pacific ───────────────────────────────────────────────────────────
    {"key": "meta-singapore",     "label": "Meta DC Singapore",            "provider": "Meta",   "type": "meta_ai",       "lat":  1.35,  "lng": 103.81},
]

# ---------------------------------------------------------------------------
# Specific backbone edges — major known submarine cable routes
# (auto-edges handle local connections; these ensure oceanic connectivity)
# ---------------------------------------------------------------------------
BACKBONE_EDGES = [
    # ── Transatlantic ───────────────────────────────────────────────────────
    ("cls-new-york",    "cls-widemouth-bay",  "submarine"),   # AEConnect / Hibernia
    ("cls-new-york",    "cls-lands-end",      "submarine"),   # TAT-14
    ("cls-miami",       "cls-widemouth-bay",  "submarine"),   # Concerto
    ("cls-miami",       "cls-fortaleza",      "submarine"),   # BRUSA / SAC
    ("cls-fortaleza",   "cls-lisbon",         "submarine"),   # EllaLink / SAIL
    ("cls-fortaleza",   "cls-widemouth-bay",  "submarine"),   # Seabras-1
    ("cls-widemouth-bay","cls-lisbon",        "submarine"),   # FLAG / AC-1
    ("cls-accra",       "cls-fortaleza",      "submarine"),   # SAIL West Africa
    # ── North Atlantic chokepoint ────────────────────────────────────────────
    ("cls-widemouth-bay","chk-engchan",       "submarine"),
    ("chk-engchan",     "cls-marseille",      "submarine"),
    # ── Mediterranean / Red Sea ──────────────────────────────────────────────
    ("cls-marseille",   "cls-palermo",        "submarine"),   # SEA-ME-WE cables
    ("cls-palermo",     "cls-alexandria",     "submarine"),
    ("cls-alexandria",  "chk-suez",           "submarine"),
    ("chk-suez",        "chk-bab-el-mandeb",  "submarine"),
    ("chk-bab-el-mandeb","cls-djibouti",      "submarine"),
    ("cls-djibouti",    "cls-mombasa",        "submarine"),   # EASSy / SEACOM
    ("cls-djibouti",    "cls-mumbai",         "submarine"),   # SMW4 / AAE-1
    # ── Around Africa ───────────────────────────────────────────────────────
    ("cls-accra",       "cls-mombasa",        "submarine"),   # WACS / SEACOM around SA
    ("cls-mombasa",     "chk-good-hope",      "submarine"),
    ("chk-good-hope",   "cls-rio",            "submarine"),   # alternate route
    # ── Indian Ocean / Asia ──────────────────────────────────────────────────
    ("cls-mumbai",      "cls-chennai",        "submarine"),
    ("cls-chennai",     "cls-singapore",      "submarine"),   # SMW4 / AAE-1
    # ── India IXP ↔ cable landings (fiber backhaul) ───────────────────────────
    ("ixp-de-cix-mumbai", "cls-mumbai",       "fiber"),
    ("ixp-nixi-delhi",    "ixp-de-cix-mumbai","fiber"),
    ("ixp-nixi-chennai",  "cls-chennai",      "fiber"),
    ("cls-singapore",   "chk-malacca",        "submarine"),
    ("chk-malacca",     "cls-hong-kong",      "submarine"),
    ("cls-singapore",   "cls-hong-kong",      "submarine"),   # SEA-ME-WE 5
    ("cls-hong-kong",   "chk-luzon",          "submarine"),
    ("chk-luzon",       "cls-okinawa",        "submarine"),
    ("cls-okinawa",     "cls-tokyo",          "submarine"),
    # ── Transpacific ────────────────────────────────────────────────────────
    ("cls-los-angeles", "cls-hawaii",         "submarine"),   # TGN-Pacific
    ("cls-hawaii",      "cls-guam",           "submarine"),   # SEA-US
    ("cls-guam",        "cls-okinawa",        "submarine"),
    ("cls-guam",        "cls-tokyo",          "submarine"),
    ("cls-seattle",     "cls-okinawa",        "submarine"),   # NCP / Pacific Crossing
    ("cls-los-angeles", "cls-sydney",         "submarine"),   # Southern Cross
    ("cls-hawaii",      "cls-sydney",         "submarine"),   # Hawaii-Australia
    ("cls-perth",       "cls-singapore",      "submarine"),   # SEA-ME-WE 3
    # ── Southern Pacific ────────────────────────────────────────────────────
    ("cls-sydney",      "cls-singapore",      "submarine"),   # ASC
    # ── North Pacific / Arctic ───────────────────────────────────────────────
    ("cls-seattle",     "cls-alaska",         "fiber"),       # US terrestrial
]

# Additional chokepoint reachability — connect chokepoints to nearest cable landings
CHOKEPOINT_LINKS = [
    ("chk-hormuz",  "cls-mumbai",    "submarine"),
    ("chk-hormuz",  "cls-djibouti",  "submarine"),
    ("chk-luzon",   "cls-guam",      "submarine"),
    ("chk-gibraltar","cls-lisbon",   "submarine"),
    ("chk-gibraltar","cls-marseille","submarine"),
]

# Stargate stub node wiring — dedicated dark-fiber to Azure + Oracle JV partners.
# openai_dc nodes do NOT participate in public IXP transit; these are their only edges.
STARGATE_DIRECT_LINKS = [
    ("oai-lordstown",  "az-eastus",         "dark_fiber"),  # Virginia corridor
    ("oai-lordstown",  "oracle-ashburn",    "dark_fiber"),
    ("oai-dona-ana",   "az-southcentralus", "dark_fiber"),  # Texas/NM corridor
    ("oai-dona-ana",   "oracle-phoenix",    "dark_fiber"),
    ("oai-milam-tx",   "az-southcentralus", "dark_fiber"),
    ("oai-milam-tx",   "oracle-chicago",    "dark_fiber"),
    ("oai-shackelford","az-southcentralus", "dark_fiber"),
    ("oai-shackelford","oracle-phoenix",    "dark_fiber"),
    ("oai-patagonia",  "az-brazilsouth",    "dark_fiber"),  # southernmost site
    ("oai-patagonia",  "oracle-saopaulo",   "dark_fiber"),
    ("oai-uae",        "az-uaenorth",       "dark_fiber"),  # UAE corridor
    ("oai-uae",        "oracle-dubai",      "dark_fiber"),
]

# AWS AI campus stub nodes — wired directly to parent AWS Regions, not public IXPs.
# Rainier is the $11B Anthropic training campus; Ohio/Mississippi are expansion sites.
AWS_AI_LINKS = [
    ("aws-rainier-in",  "aws-us-east-1", "dark_fiber"),  # Virginia ↔ Indiana corridor
    ("aws-rainier-in",  "aws-us-east-2", "dark_fiber"),  # Ohio ↔ Indiana corridor
    ("aws-ohio-ai",     "aws-us-east-2", "dark_fiber"),  # co-located in Central Ohio
    ("aws-ohio-ai",     "aws-us-east-1", "dark_fiber"),  # redundant Virginia link
    ("aws-mississippi", "aws-us-east-2", "dark_fiber"),  # nearest region backbone
    ("aws-mississippi", "aws-us-east-1", "dark_fiber"),  # secondary Virginia link
]

# ---------------------------------------------------------------------------
# Follow-the-Sun congestion model
# ---------------------------------------------------------------------------
def _traffic_load(utc_hour: int, lng: float) -> float:
    """Business-hour traffic load 0.1–1.0 based on UTC hour + rough timezone from longitude."""
    local_hour = int((utc_hour + round(lng / 15)) % 24)
    if 9 <= local_hour < 17:
        return 1.0   # peak — business hours
    if 7 <= local_hour < 9 or 17 <= local_hour < 22:
        return 0.5   # shoulder
    return 0.1       # off-peak / overnight


def _apply_congestion(G: nx.Graph, node_map: dict, utc_hour: int) -> nx.Graph:
    """Return a NEW graph with latency_ms scaled by the Follow-the-Sun congestion model.
    Weight_actual = base_latency × (1 + CONGESTION_FACTOR × max(load_src, load_dst))
    Max congestion (both endpoints at peak) → 1.5× base latency.
    """
    H: nx.Graph = G.__class__()
    for n, data in G.nodes(data=True):
        H.add_node(n, **data)
    for u, v, data in G.edges(data=True):
        nu, nv = node_map.get(u), node_map.get(v)
        if nu and nv:
            peak = max(_traffic_load(utc_hour, nu["lng"]),
                       _traffic_load(utc_hour, nv["lng"]))
        else:
            peak = 0.0
        new_data = dict(data)
        new_data["latency_ms"] = round(data["latency_ms"] * (1.0 + CONGESTION_FACTOR * peak), 3)
        H.add_edge(u, v, **new_data)
    return H


# ---------------------------------------------------------------------------
# Starlink orbital geometry model
# ---------------------------------------------------------------------------
def _sat_geometry_factor(utc_hour: int, lat: float, lng: float) -> float:
    """
    Approximates how the Starlink constellation geometry varies across 24 hours.
    Returns 0.0 (best — satellite directly overhead) to 1.0 (worst — lowest usable elevation).

    Physics: Shell-1 has 72 orbital planes at 53° inclination, 550 km altitude.
    The dominant variation at any ground station comes from the 95-min orbital period
    beating against Earth's 24-hour rotation, producing a ~6-hour macro-cycle in the
    "best overhead satellite" elevation angle. High-latitude sites near ±53° see stronger
    variation because they sit closest to the inclination boundary (orbital seam).
    """
    local_h    = (utc_hour + lng / 15.0) % 24.0
    phase_6h   = math.sin(2 * math.pi * local_h / 6.0)        # macro-cycle
    phase_95m  = math.sin(2 * math.pi * local_h / 1.583)      # 95-min orbital period
    lat_factor = min(1.0, abs(lat) / 53.0)                     # seam sensitivity
    raw = 0.5 + 0.4 * phase_6h + 0.1 * phase_95m * lat_factor
    return max(0.0, min(1.0, raw))


def _apply_starlink_geometry(Gs: nx.Graph, node_map: dict, utc_hour: int) -> nx.Graph:
    """
    Return a NEW Starlink graph with starlink_uplink edges adjusted for orbital geometry.

    Uplink latency = UPLINK_MS + UPLINK_EXTRA_MS × geometry_factor
    Range: 12 ms (best coverage) → 32 ms (worst coverage).
    Laser ISL edges are unaffected — vacuum propagation speed is independent of geometry.
    With 2 uplink hops (src→GW + GW→dst) the total path varies by up to 40 ms.
    """
    H: nx.Graph = Gs.__class__()
    for n, data in Gs.nodes(data=True):
        H.add_node(n, **data)
    # Also search satellite nodes for the ground-side lookup
    combined_map = {**node_map, **_SAT_NODE_MAP}
    for u, v, data in Gs.edges(data=True):
        new_data = dict(data)
        if data.get("edge_type") == "starlink_uplink":
            nu, nv = combined_map.get(u), combined_map.get(v)
            # The ground-side node (DC or GW) determines the elevation-angle geometry.
            # In the satellite mesh, uplinks are GW→satellite — use the GW location.
            ground = next(
                (n for n in (nu, nv)
                 if n and n.get("type") in
                 ("cloud_dc", "openai_dc", "aws_ai", "meta_ai", "starlink_gw")),
                None
            )
            if ground:
                geo = _sat_geometry_factor(utc_hour, ground["lat"], ground["lng"])
                new_data["latency_ms"] = round(
                    data["latency_ms"] + UPLINK_EXTRA_MS * geo, 3)
        H.add_edge(u, v, **new_data)
    return H


# ---------------------------------------------------------------------------
# Fibonacci sphere — 10 000-satellite static mesh
# ---------------------------------------------------------------------------
def _fibonacci_sphere(n: int) -> list[tuple[float, float]]:
    """
    Distribute n points uniformly on a unit sphere using the Fibonacci lattice.
    Returns a list of (lat, lng) tuples in degrees. The golden-ratio angular step
    eliminates clustering at poles and produces a near-uniform point distribution,
    which approximates the coverage of the Starlink Shell-1 constellation.
    """
    phi = (1.0 + math.sqrt(5.0)) / 2.0       # golden ratio ≈ 1.618
    pts: list[tuple[float, float]] = []
    for i in range(n):
        y = 1.0 - (i / (n - 1)) * 2.0        # y ∈ [1, -1] pole to pole
        r = math.sqrt(max(0.0, 1.0 - y * y)) # ring radius at height y
        theta = 2.0 * math.pi * i / phi       # golden-angle longitude step
        lat = math.degrees(math.asin(max(-1.0, min(1.0, y))))
        lng = math.degrees(math.atan2(math.sin(theta) * r, math.cos(theta) * r))
        pts.append((lat, lng))
    return pts


def _build_sat_graph(all_nodes: list[dict]) -> tuple[nx.Graph, dict]:
    """
    Build the Fibonacci-sphere satellite mesh and return (graph, sat_node_map).

    Graph topology:
      Cloud DC  ──fiber──►  Ground Station  ──uplink──►  Satellite
      Satellite  ──ISL laser──►  Satellite (k=4 nearest)
      Satellite  ──downlink──►  Ground Station  ──fiber──►  Cloud DC

    Latency model:
      DC→GW      fiber  (FIBER_KM_S)
      GW→sat     uplink (slant range at VACUUM_KM_S + UPLINK_MS fixed)
      sat→sat    ISL    (orbital arc at VACUUM_KM_S)

    With SAT_COUNT=10 000 and ISL_K=4, average nearest-neighbor distance is
    ~140 km surface (152 km orbital arc → 0.51 ms/hop). London→Tokyo needs
    ~68 hops → ~35 ms ISL + 2×uplinks → total ~60 ms, vs ~120 ms fiber.
    """
    import math as _m
    node_map = {n["key"]: n for n in all_nodes}
    sat_latlng = _fibonacci_sphere(SAT_COUNT)

    # Pre-compute 3D Cartesian coordinates (unit sphere) — used for k-NN
    def _xyz(lat, lng):
        ph, la = _m.radians(lat), _m.radians(lng)
        c = _m.cos(ph)
        return (c * _m.cos(la), c * _m.sin(la), _m.sin(ph))

    coords3d = [_xyz(lat, lng) for lat, lng in sat_latlng]

    Gs = nx.Graph()
    sat_node_map: dict = {}

    # ── 1. Satellite nodes ────────────────────────────────────────────────────
    sat_keys = [f"sat-{i}" for i in range(SAT_COUNT)]
    for i, (lat, lng) in enumerate(sat_latlng):
        data = {"key": sat_keys[i], "type": "satellite", "provider": "SpaceX",
                "label": f"Starlink SL-{i}", "lat": lat, "lng": lng}
        Gs.add_node(sat_keys[i], **data)
        sat_node_map[sat_keys[i]] = data

    # ── 2. Ground-station and DC nodes ───────────────────────────────────────
    gw_nodes = [n for n in all_nodes if n["type"] == "starlink_gw"]
    dc_nodes = [n for n in all_nodes
                if n["type"] in ("cloud_dc", "openai_dc", "aws_ai", "meta_ai")]
    for n in gw_nodes + dc_nodes:
        Gs.add_node(n["key"], **n)

    # ── 3. Satellite ISL edges (k=SAT_ISL_K nearest neighbours) ──────────────
    if _SCIPY:
        arr = _np.array(coords3d)
        tree = _cKDTree(arr)
        _, idxs = tree.query(arr, k=SAT_ISL_K + 1)     # +1 because result[0] = self
        for i, neighbours in enumerate(idxs):
            for j in neighbours[1:]:
                if i < j:
                    # Arc length at orbital altitude
                    km_surf = _haversine_km(sat_latlng[i][0], sat_latlng[i][1],
                                            sat_latlng[j][0], sat_latlng[j][1])
                    km_orb = km_surf * (R_SAT / 6371.0)
                    ms = (km_orb / VACUUM_KM_S) * 1000.0
                    Gs.add_edge(sat_keys[i], sat_keys[j],
                                edge_type="starlink_laser",
                                distance_km=round(km_orb, 1),
                                latency_ms=round(ms, 4))
    else:
        # Pure-Python fallback: index-window search on the Fibonacci spiral.
        # Nearest neighbours in the spiral live within ±WINDOW indices.
        WINDOW = max(120, int(_m.sqrt(SAT_COUNT) * 2))
        def _csq(a, b):
            return (a[0]-b[0])**2 + (a[1]-b[1])**2 + (a[2]-b[2])**2
        for i in range(SAT_COUNT):
            lo, hi = max(0, i - WINDOW), min(SAT_COUNT, i + WINDOW + 1)
            cands = sorted((j for j in range(lo, hi) if j != i),
                           key=lambda j: _csq(coords3d[i], coords3d[j]))
            for j in cands[:SAT_ISL_K]:
                if i < j:
                    km_surf = _haversine_km(sat_latlng[i][0], sat_latlng[i][1],
                                            sat_latlng[j][0], sat_latlng[j][1])
                    km_orb = km_surf * (R_SAT / 6371.0)
                    ms = (km_orb / VACUUM_KM_S) * 1000.0
                    Gs.add_edge(sat_keys[i], sat_keys[j],
                                edge_type="starlink_laser",
                                distance_km=round(km_orb, 1),
                                latency_ms=round(ms, 4))

    # ── 4. GW → satellite uplinks ─────────────────────────────────────────────
    def _nearest_sats(lat, lng, k):
        """Return indices of k nearest satellite nodes."""
        gw_xyz = _xyz(lat, lng)
        if _SCIPY:
            _, idxs = tree.query(_np.array([gw_xyz]), k=k)
            return idxs[0].tolist()
        def _csq2(b): return sum((a - b[j])**2 for j, a in enumerate(gw_xyz))
        return sorted(range(SAT_COUNT), key=lambda i: _csq2(coords3d[i]))[:k]

    for gw in gw_nodes:
        for si in _nearest_sats(gw["lat"], gw["lng"], GW_SAT_K):
            km_surf  = _haversine_km(gw["lat"], gw["lng"],
                                     sat_latlng[si][0], sat_latlng[si][1])
            km_slant = _m.sqrt(km_surf ** 2 + SAT_ALT_KM ** 2)
            ms = (km_slant / VACUUM_KM_S) * 1000.0 + UPLINK_MS
            Gs.add_edge(gw["key"], sat_keys[si],
                        edge_type="starlink_uplink",
                        distance_km=round(km_slant, 1),
                        latency_ms=round(ms, 3))

    # ── 5. DC → GW fiber (terrestrial segment to reach gateway) ──────────────
    for dc in dc_nodes:
        nearest_gws = sorted(gw_nodes,
                             key=lambda g: _haversine_km(dc["lat"], dc["lng"],
                                                          g["lat"], g["lng"]))[:2]
        for gw in nearest_gws:
            km = _haversine_km(dc["lat"], dc["lng"], gw["lat"], gw["lng"])
            ms = (km / FIBER_KM_S) * 1000.0
            Gs.add_edge(dc["key"], gw["key"],
                        edge_type="fiber",
                        distance_km=round(km, 1),
                        latency_ms=round(ms, 3))

    return Gs, sat_node_map


# ---------------------------------------------------------------------------
# Haversine distance
# ---------------------------------------------------------------------------
def _haversine_km(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
    R = 6371.0
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlam = math.radians(lng2 - lng1)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlam / 2) ** 2
    return R * 2 * math.asin(math.sqrt(a))


def _lat_lng_arr():
    """Return (keys, lats, lngs) as parallel arrays for nearest-neighbour search."""
    keys = [n["key"] for n in NODES]
    lats = [n["lat"] for n in NODES]
    lngs = [n["lng"] for n in NODES]
    return keys, lats, lngs


def _nearest_of_types(src_key: str, types: list[str], k: int) -> list[str]:
    """Return k nearest node keys of given types (excluding src)."""
    src = next(n for n in NODES if n["key"] == src_key)
    candidates = [n for n in NODES if n["type"] in types and n["key"] != src_key]
    scored = sorted(
        candidates,
        key=lambda n: _haversine_km(src["lat"], src["lng"], n["lat"], n["lng"])
    )
    return [n["key"] for n in scored[:k]]


def _edge_latency(edge_type: str, km: float) -> float:
    if edge_type == "starlink_uplink":
        return UPLINK_MS
    if edge_type == "starlink_laser":
        return (km / VACUUM_KM_S) * 1000.0
    return (km / FIBER_KM_S) * 1000.0    # fiber or submarine


# ---------------------------------------------------------------------------
# Graph construction
# ---------------------------------------------------------------------------
def _build_graphs():
    node_map = {n["key"]: n for n in NODES}

    def add_edge(G, src, dst, edge_type):
        if src not in G or dst not in G:
            return
        km = _haversine_km(
            node_map[src]["lat"], node_map[src]["lng"],
            node_map[dst]["lat"], node_map[dst]["lng"],
        )
        ms = _edge_latency(edge_type, km)
        G.add_edge(src, dst,
                   edge_type=edge_type,
                   distance_km=round(km, 1),
                   latency_ms=round(ms, 3))

    # ── Terrestrial graph ────────────────────────────────────────────────────
    Gt = nx.Graph()
    for n in NODES:
        if n["type"] not in ("starlink_gw",):          # exclude sat-only nodes
            Gt.add_node(n["key"], **n)

    # Cloud DCs → nearest IXPs (fiber).
    # openai_dc / aws_ai are pure stubs (dark fiber only); meta_ai peers at 2 IXPs.
    for n in NODES:
        if n["type"] == "cloud_dc":
            for ixp_key in _nearest_of_types(n["key"], ["ixp"], 3):
                add_edge(Gt, n["key"], ixp_key, "fiber")
        elif n["type"] == "meta_ai":
            for ixp_key in _nearest_of_types(n["key"], ["ixp"], 2):
                add_edge(Gt, n["key"], ixp_key, "fiber")

    # AI campus pure stubs → hyperscaler backbone via dedicated dark-fiber wavelengths
    for src, dst, etype in STARGATE_DIRECT_LINKS + AWS_AI_LINKS:
        if src in node_map and dst in node_map:
            add_edge(Gt, src, dst, etype)

    # IXP → IXP cross-connects (fiber, local)
    for n in NODES:
        if n["type"] == "ixp":
            for peer_key in _nearest_of_types(n["key"], ["ixp"], 2):
                km = _haversine_km(n["lat"], n["lng"],
                                   node_map[peer_key]["lat"], node_map[peer_key]["lng"])
                if km < 1500:          # only continental cross-connects
                    add_edge(Gt, n["key"], peer_key, "fiber")

    # IXP → Cable Landings
    for n in NODES:
        if n["type"] == "ixp":
            for cls_key in _nearest_of_types(n["key"], ["cable_landing"], 2):
                add_edge(Gt, n["key"], cls_key, "submarine")

    # Backbone submarine cable routes
    for src, dst, etype in (BACKBONE_EDGES + CHOKEPOINT_LINKS):
        if src in node_map and dst in node_map:
            add_edge(Gt, src, dst, etype)

    # Cable landing → nearby cable landings (regional connectivity)
    for n in NODES:
        if n["type"] == "cable_landing":
            for peer_key in _nearest_of_types(n["key"], ["cable_landing", "chokepoint"], 3):
                km = _haversine_km(n["lat"], n["lng"],
                                   node_map[peer_key]["lat"], node_map[peer_key]["lng"])
                if 50 < km < 3000:     # skip same-site, skip ultra-long local
                    add_edge(Gt, n["key"], peer_key, "submarine")

    # ── Starlink graph ───────────────────────────────────────────────────────
    Gs = nx.Graph()
    for n in NODES:
        if n["type"] in ("cloud_dc", "openai_dc", "aws_ai", "meta_ai", "starlink_gw"):
            Gs.add_node(n["key"], **n)

    # Each DC connects to its 2 nearest GWs — dual entry points give Dijkstra
    # better arc options when one GW is geographically sub-optimal.
    for n in NODES:
        if n["type"] in ("cloud_dc", "openai_dc", "aws_ai", "meta_ai"):
            for gw_key in _nearest_of_types(n["key"], ["starlink_gw"], 2):
                if gw_key not in Gs:
                    continue
                km = _haversine_km(n["lat"], n["lng"],
                                   node_map[gw_key]["lat"], node_map[gw_key]["lng"])
                ms = (km / FIBER_KM_S) * 1000.0 + UPLINK_MS
                Gs.add_edge(n["key"], gw_key,
                            edge_type="starlink_uplink",
                            distance_km=round(km, 1),
                            latency_ms=round(ms, 3))

    # GW → GW ISL mesh — 200 Gbps optical lasers at vacuum speed of light.
    # k=12 ensures robust intercontinental arcs (transatlantic + transpacific).
    for n in NODES:
        if n["type"] == "starlink_gw":
            for peer_key in _nearest_of_types(n["key"], ["starlink_gw"], 12):
                if peer_key not in Gs:
                    continue
                km = _haversine_km(n["lat"], n["lng"],
                                   node_map[peer_key]["lat"], node_map[peer_key]["lng"])
                ms = (km / VACUUM_KM_S) * 1000.0   # vacuum — no extra overhead
                Gs.add_edge(n["key"], peer_key,
                            edge_type="starlink_laser",
                            distance_km=round(km, 1),
                            latency_ms=round(ms, 3))

    return Gt, Gs


# ---------------------------------------------------------------------------
# SQL enrichment — load extra nodes/edges from InfraNodes/InfraEdges if available
# ---------------------------------------------------------------------------
def _load_from_sql(conn_str: str) -> tuple[list[dict], list[dict]]:
    """
    Try to read InfraNodes + InfraEdges from SQL Server.
    Returns (extra_nodes, extra_edges) — nodes not already in NODES catalogue.
    Falls back to ([], []) on any error.
    """
    try:
        from services.sqlite_fallback import sql_or_sqlite  # noqa: PLC0415
        infra_cs = _infra_conn_str(conn_str)
        conn, backend = sql_or_sqlite(infra_cs, 'infra.db', timeout=8)
        cur = conn.cursor()

        # Check InfraNodes table exists (MS SQL uses INFORMATION_SCHEMA; SQLite has sqlite_master)
        if backend == 'mssql':
            cur.execute(
                "SELECT COUNT(*) FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME='InfraNodes'"
            )
        else:
            cur.execute(
                "SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name='InfraNodes'"
            )
        if cur.fetchone()[0] == 0:
            conn.close()
            return [], []

        cat_keys = {n["key"] for n in NODES}

        cur.execute("SELECT NodeKey,Label,Provider,Type,Latitude,Longitude FROM InfraNodes")
        extra_nodes = []
        for row in cur.fetchall():
            key = row[0]
            if key in cat_keys:
                continue
            extra_nodes.append({
                "key": key, "label": row[1] or key,
                "provider": row[2] or "—", "type": row[3] or "cable_landing",
                "lat": float(row[4]), "lng": float(row[5]),
            })

        cur.execute("SELECT SourceKey,TargetKey,EdgeType,DistanceKM FROM InfraEdges")
        extra_edges = [
            {"src": r[0], "dst": r[1], "type": r[2], "km": float(r[3])}
            for r in cur.fetchall()
        ]

        conn.close()
        return extra_nodes, extra_edges

    except Exception:
        return [], []


def _build_graphs_enriched(extra_nodes: list[dict], extra_edges: list[dict]):
    """
    Build graphs using NODES catalogue + extra nodes/edges from SQL.
    Extra nodes are added to G_terrestrial as cable_landing / ixp nodes.
    Extra edges (submarine cables from TeleGeography) are added as submarine edges.
    """
    all_nodes = NODES + extra_nodes
    node_map  = {n["key"]: n for n in all_nodes}

    # --- Terrestrial graph --------------------------------------------------
    Gt = nx.Graph()
    for n in all_nodes:
        if n["type"] not in ("starlink_gw",):
            Gt.add_node(n["key"], **n)

    def add_terrestrial(src, dst, etype):
        if src not in Gt or dst not in Gt:
            return
        km = _haversine_km(node_map[src]["lat"], node_map[src]["lng"],
                           node_map[dst]["lat"], node_map[dst]["lng"])
        ms = _edge_latency(etype, km)
        Gt.add_edge(src, dst, edge_type=etype,
                    distance_km=round(km, 1), latency_ms=round(ms, 3))

    # Hardcoded backbone edges first
    for src, dst, etype in (BACKBONE_EDGES + CHOKEPOINT_LINKS):
        add_terrestrial(src, dst, etype)

    # SQL-sourced submarine cable edges (TeleGeography)
    for e in extra_edges:
        add_terrestrial(e["src"], e["dst"], e["type"])

    # Auto-connect cloud DCs → nearest IXPs (unchanged logic)
    def nearest_of_types(src_key, types, k):
        src = node_map[src_key]
        cands = [n for n in all_nodes if n["type"] in types and n["key"] != src_key]
        return [n["key"] for n in
                sorted(cands, key=lambda n: _haversine_km(src["lat"], src["lng"], n["lat"], n["lng"]))[:k]]

    # openai_dc / aws_ai: pure stubs; meta_ai: peers at 2 IXPs via public interconnect
    for n in all_nodes:
        if n["type"] == "cloud_dc":
            for ixp_key in nearest_of_types(n["key"], ["ixp"], 3):
                add_terrestrial(n["key"], ixp_key, "fiber")
        elif n["type"] == "meta_ai":
            for ixp_key in nearest_of_types(n["key"], ["ixp"], 2):
                add_terrestrial(n["key"], ixp_key, "fiber")

    for src, dst, etype in STARGATE_DIRECT_LINKS + AWS_AI_LINKS:
        add_terrestrial(src, dst, etype)

    for n in all_nodes:
        if n["type"] == "ixp":
            for p in nearest_of_types(n["key"], ["ixp"], 2):
                if _haversine_km(n["lat"], n["lng"], node_map[p]["lat"], node_map[p]["lng"]) < 1500:
                    add_terrestrial(n["key"], p, "fiber")
            for cls_key in nearest_of_types(n["key"], ["cable_landing"], 2):
                add_terrestrial(n["key"], cls_key, "submarine")

    for n in all_nodes:
        if n["type"] == "cable_landing":
            for p in nearest_of_types(n["key"], ["cable_landing", "chokepoint"], 3):
                km = _haversine_km(n["lat"], n["lng"], node_map[p]["lat"], node_map[p]["lng"])
                if 50 < km < 3000:
                    add_terrestrial(n["key"], p, "submarine")

    # --- Starlink graph (same as before, uses only NODES catalogue) ----------
    Gs = nx.Graph()
    for n in NODES:
        if n["type"] in ("cloud_dc", "openai_dc", "aws_ai", "meta_ai", "starlink_gw"):
            Gs.add_node(n["key"], **n)

    def _nearest_gw(src_key, k):
        src = node_map[src_key]
        gws = [n for n in NODES if n["type"] == "starlink_gw" and n["key"] != src_key]
        return [n["key"] for n in
                sorted(gws, key=lambda n: _haversine_km(src["lat"], src["lng"], n["lat"], n["lng"]))[:k]]

    for n in NODES:
        if n["type"] in ("cloud_dc", "openai_dc", "aws_ai", "meta_ai"):
            for gw_key in _nearest_gw(n["key"], 2):
                if gw_key not in Gs:
                    continue
                km = _haversine_km(n["lat"], n["lng"], node_map[gw_key]["lat"], node_map[gw_key]["lng"])
                ms = (km / FIBER_KM_S) * 1000.0 + UPLINK_MS
                Gs.add_edge(n["key"], gw_key, edge_type="starlink_uplink",
                            distance_km=round(km, 1), latency_ms=round(ms, 3))

    for n in NODES:
        if n["type"] == "starlink_gw":
            for peer_key in _nearest_gw(n["key"], 12):
                if peer_key not in Gs:
                    continue
                km = _haversine_km(n["lat"], n["lng"], node_map[peer_key]["lat"], node_map[peer_key]["lng"])
                ms = (km / VACUUM_KM_S) * 1000.0
                Gs.add_edge(n["key"], peer_key, edge_type="starlink_laser",
                            distance_km=round(km, 1), latency_ms=round(ms, 3))

    return Gt, Gs, all_nodes


# ---------------------------------------------------------------------------
# Cache — built once at first call
# ---------------------------------------------------------------------------
_LOCK = threading.Lock()
_G_TERRESTRIAL: nx.Graph | None = None
_G_STARLINK:    nx.Graph | None = None
_NODE_MAP:     dict = {}
_ALL_NODES:    list = []
_SAT_NODE_MAP: dict = {}     # satellite-only nodes — not in _NODE_MAP

# Per-minute SQL-backed satellite graph cache (one slot)
_G_STARLINK_SQL:        nx.Graph | None = None
_G_STARLINK_SQL_MINUTE: int             = -1
_SQL_STAR_LOCK = threading.Lock()

_INFRA_DB_NAME = "InfraDB"

def _infra_conn_str(conn_str: str) -> str:
    """Return conn_str with DATABASE swapped to InfraDB."""
    import re
    return re.sub(r'DATABASE=[^;]+', f'DATABASE={_INFRA_DB_NAME}', conn_str, flags=re.IGNORECASE)


def _load_sat_graph_for_minute(minute: int, conn_str: str) -> "nx.Graph | None":
    """
    Load one minute's Starlink snapshot from SQL and build a routing graph.
    Single-slot cache: repeated calls for the same minute return immediately.
    Returns None if SQL tables are absent or the query fails.
    """
    global _G_STARLINK_SQL, _G_STARLINK_SQL_MINUTE

    # Fast path — no lock needed for read check
    if _G_STARLINK_SQL is not None and _G_STARLINK_SQL_MINUTE == minute:
        return _G_STARLINK_SQL

    with _SQL_STAR_LOCK:
        # Re-check under lock
        if _G_STARLINK_SQL is not None and _G_STARLINK_SQL_MINUTE == minute:
            return _G_STARLINK_SQL

        infra_cs = _infra_conn_str(conn_str)
        if not _dynamic_tables_exist(infra_cs):
            return None

        try:
            from services.sqlite_fallback import sql_or_sqlite
            conn, _ = sql_or_sqlite(infra_cs, 'infra.db', timeout=10)
            cur = conn.cursor()

            cur.execute(
                "SELECT SatID, Lat, Lng FROM SpaceNodes_Dynamic WHERE MinuteOfDay=?",
                (minute,),
            )
            sat_data = {
                f"dynsat-{r[0]}": {
                    "key": f"dynsat-{r[0]}", "lat": float(r[1]), "lng": float(r[2]),
                    "type": "satellite", "provider": "SpaceX", "label": f"SL-{r[0]}",
                }
                for r in cur.fetchall()
            }

            cur.execute(
                "SELECT SatA, SatB, DistKM, LatencyMS FROM SpaceEdges_Dynamic WHERE MinuteOfDay=?",
                (minute,),
            )
            isl_edges = [
                (f"dynsat-{r[0]}", f"dynsat-{r[1]}", float(r[2]), float(r[3]))
                for r in cur.fetchall()
            ]
            conn.close()
        except Exception:
            return None

        Gs = nx.Graph()
        gw_nodes = [n for n in _ALL_NODES if n["type"] == "starlink_gw"]
        dc_nodes = [n for n in _ALL_NODES
                    if n["type"] in ("cloud_dc", "openai_dc", "aws_ai", "meta_ai")]

        for n in gw_nodes + dc_nodes:
            Gs.add_node(n["key"], **n)
        for key, data in sat_data.items():
            Gs.add_node(key, **data)

        for satA, satB, dist_km, lat_ms in isl_edges:
            if satA in Gs and satB in Gs:
                Gs.add_edge(satA, satB, edge_type="starlink_laser",
                            distance_km=dist_km, latency_ms=lat_ms)

        sat_list = list(sat_data.values())
        for gw in gw_nodes:
            nearest = sorted(sat_list,
                             key=lambda s: _haversine_km(gw["lat"], gw["lng"],
                                                          s["lat"], s["lng"]))[:GW_SAT_K]
            for sat in nearest:
                km_surf = _haversine_km(gw["lat"], gw["lng"], sat["lat"], sat["lng"])
                if km_surf > 800:
                    continue
                km_slant = math.sqrt(km_surf ** 2 + SAT_ALT_KM ** 2)
                ms = (km_slant / VACUUM_KM_S) * 1000.0 + UPLINK_MS
                Gs.add_edge(gw["key"], sat["key"],
                            edge_type="starlink_uplink",
                            distance_km=round(km_slant, 1),
                            latency_ms=round(ms, 3))

        for dc in dc_nodes:
            for gw in sorted(gw_nodes,
                             key=lambda g: _haversine_km(dc["lat"], dc["lng"],
                                                          g["lat"], g["lng"]))[:2]:
                km = _haversine_km(dc["lat"], dc["lng"], gw["lat"], gw["lng"])
                ms = (km / FIBER_KM_S) * 1000.0
                Gs.add_edge(dc["key"], gw["key"],
                            edge_type="fiber",
                            distance_km=round(km, 1),
                            latency_ms=round(ms, 3))

        _G_STARLINK_SQL        = Gs
        _G_STARLINK_SQL_MINUTE = minute
        return Gs


def _ensure_graphs(conn_str: str | None = None):
    global _G_TERRESTRIAL, _G_STARLINK, _NODE_MAP, _ALL_NODES, _SAT_NODE_MAP
    if _G_TERRESTRIAL is not None:
        return
    with _LOCK:
        if _G_TERRESTRIAL is None:
            import logging
            log = logging.getLogger(__name__)

            extra_nodes, extra_edges = [], []
            if conn_str:
                extra_nodes, extra_edges = _load_from_sql(conn_str)
                if extra_nodes:
                    log.info("global_infra: loaded %d extra nodes + %d edges from SQL",
                             len(extra_nodes), len(extra_edges))

            Gt, _, all_nodes = _build_graphs_enriched(extra_nodes, extra_edges)

            log.info("global_infra: building %d-satellite Fibonacci mesh%s …",
                     SAT_COUNT, " (scipy)" if _SCIPY else " (pure-python fallback)")
            Gs_sat, sat_map = _build_sat_graph(all_nodes)
            log.info("global_infra: satellite graph ready — %d nodes, %d edges",
                     Gs_sat.number_of_nodes(), Gs_sat.number_of_edges())

            _ALL_NODES     = all_nodes
            _NODE_MAP      = {n["key"]: n for n in all_nodes}
            _SAT_NODE_MAP  = sat_map
            _G_TERRESTRIAL = Gt
            _G_STARLINK    = Gs_sat


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------
def get_all_nodes(conn_str: str | None = None) -> list[dict]:
    _ensure_graphs(conn_str)
    return _ALL_NODES


def get_cloud_nodes(conn_str: str | None = None) -> list[dict]:
    """Return all routable endpoint nodes for the routing dropdowns."""
    _ensure_graphs(conn_str)
    return [n for n in _ALL_NODES if n["type"] in ("cloud_dc", "openai_dc", "aws_ai", "meta_ai")]


def get_edges_for_display(conn_str: str | None = None) -> list[dict]:
    """Return terrestrial backbone edges for background map rendering."""
    _ensure_graphs(conn_str)
    edges = []
    seen = set()
    for u, v, data in _G_TERRESTRIAL.edges(data=True):
        key = tuple(sorted([u, v]))
        if key in seen:
            continue
        seen.add(key)
        nu, nv = _NODE_MAP.get(u), _NODE_MAP.get(v)
        if nu and nv:
            edges.append({
                "src": u, "dst": v,
                "src_lat": nu["lat"], "src_lng": nu["lng"],
                "dst_lat": nv["lat"], "dst_lng": nv["lng"],
                "edge_type": data.get("edge_type", "fiber"),
                "distance_km": data.get("distance_km", 0),
                "latency_ms": data.get("latency_ms", 0),
            })
    return edges


def route(src: str, dst: str, disabled_edge: tuple | None = None,
          conn_str: str | None = None, hour_utc: int | None = None,
          minute: int | None = None) -> dict:
    """
    Find shortest-latency path on both graphs.

    minute (0-1439): use pre-computed SQL orbital snapshot as the Starlink graph.
                     Also enables congestion weighting (minute // 60 → UTC hour).
    disabled_edge  : (node_a, node_b) to remove from terrestrial graph (crisis mode).
    hour_utc       : legacy; used only when minute is None.
    """
    _ensure_graphs(conn_str)

    if src not in _NODE_MAP:
        return {"error": f"Unknown source node: {src!r}"}
    if dst not in _NODE_MAP:
        return {"error": f"Unknown destination node: {dst!r}"}

    # Effective UTC hour for congestion (minute takes precedence)
    effective_hour: int | None = minute // 60 if minute is not None else hour_utc

    # ── Terrestrial — crisis cut + congestion ────────────────────────────────
    Gt = _G_TERRESTRIAL
    if disabled_edge:
        Gt = Gt.copy()
        a, b = disabled_edge
        if Gt.has_edge(a, b):
            Gt.remove_edge(a, b)
    if effective_hour is not None:
        Gt = _apply_congestion(Gt, _NODE_MAP, effective_hour)

    try:
        t_path   = nx.dijkstra_path(Gt, src, dst, weight="latency_ms")
        t_ms     = sum(Gt[u][v]["latency_ms"]  for u, v in zip(t_path, t_path[1:]))
        t_km     = sum(Gt[u][v]["distance_km"] for u, v in zip(t_path, t_path[1:]))
        t_etypes = [Gt[u][v].get("edge_type", "fiber") for u, v in zip(t_path, t_path[1:])]
    except nx.NetworkXNoPath:
        t_path, t_ms, t_km, t_etypes = [], None, None, []
    except nx.NodeNotFound as e:
        return {"error": f"Node not in terrestrial graph: {e}"}

    # ── Starlink — SQL snapshot if minute set, else Fibonacci + geometry ─────
    sql_sat_map: dict = {}
    dynamic_topology  = False

    Gs = _G_STARLINK
    if minute is not None and conn_str:
        sql_gs = _load_sat_graph_for_minute(minute, conn_str)
        if sql_gs is not None:
            Gs               = sql_gs
            dynamic_topology = True
            sql_sat_map      = {k: v for k, v in Gs.nodes(data=True)
                                if k.startswith("dynsat-")}

    if not dynamic_topology and effective_hour is not None:
        Gs = _apply_starlink_geometry(Gs, _NODE_MAP, effective_hour)

    try:
        s_path   = nx.dijkstra_path(Gs, src, dst, weight="latency_ms")
        s_ms     = sum(Gs[u][v]["latency_ms"]  for u, v in zip(s_path, s_path[1:]))
        s_km     = sum(Gs[u][v]["distance_km"] for u, v in zip(s_path, s_path[1:]))
        s_etypes = [Gs[u][v].get("edge_type", "starlink_laser") for u, v in zip(s_path, s_path[1:])]
    except (nx.NetworkXNoPath, nx.NodeNotFound):
        s_path, s_ms, s_km, s_etypes = [], None, None, []

    if t_ms is None and s_ms is None:
        return {"error": "System Offline — no path found on any network. Try removing the crisis event."}

    # ── Path → coordinate arrays ─────────────────────────────────────────────
    def path_coords(path):
        results = []
        for k in path:
            n = _NODE_MAP.get(k) or _SAT_NODE_MAP.get(k) or sql_sat_map.get(k)
            if n:
                results.append({"key": k, "lat": n["lat"], "lng": n["lng"],
                                 "label": n.get("label", k)})
        return results

    return {
        "terrestrial": {
            "path":        t_path,
            "coords":      path_coords(t_path),
            "edge_types":  t_etypes,
            "latency_ms":  round(t_ms, 1) if t_ms is not None else None,
            "distance_km": round(t_km)    if t_km is not None else None,
            "hops":        len(t_path) - 1,
        },
        "starlink": {
            "path":        s_path,
            "coords":      path_coords(s_path),
            "edge_types":  s_etypes,
            "latency_ms":  round(s_ms, 1) if s_ms is not None else None,
            "distance_km": round(s_km)    if s_km is not None else None,
            "hops":        len(s_path) - 1,
        },
        "savings_pct": (
            round((1 - s_ms / t_ms) * 100, 1)
            if t_ms and s_ms and t_ms > 0 else None
        ),
        "all_nodes":                  _NODE_MAP,
        "hour_utc":                   effective_hour,
        "minute_of_day":              minute,
        "congestion_active":          effective_hour is not None,
        "starlink_geometry_active":   not dynamic_topology and effective_hour is not None,
        "dynamic_topology":           dynamic_topology,
    }


# ---------------------------------------------------------------------------
# Dynamic topology — pre-computed orbital snapshots in SQL
# ---------------------------------------------------------------------------
def _dynamic_tables_exist(conn_str: str) -> bool:
    """Return True if SpaceNodes_Dynamic and SpaceEdges_Dynamic are accessible (SQL or SQLite)."""
    try:
        from services.sqlite_fallback import sql_or_sqlite
        conn, backend = sql_or_sqlite(conn_str, 'infra.db', timeout=5)
        cur = conn.cursor()
        if backend == 'mssql':
            cur.execute("""
                SELECT COUNT(*) FROM INFORMATION_SCHEMA.TABLES
                WHERE TABLE_NAME IN ('SpaceNodes_Dynamic','SpaceEdges_Dynamic')
            """)
        else:
            cur.execute("""
                SELECT COUNT(*) FROM sqlite_master
                WHERE type='table' AND name IN ('SpaceNodes_Dynamic','SpaceEdges_Dynamic')
            """)
        count = cur.fetchone()[0]
        conn.close()
        return count == 2
    except Exception:
        return False


def get_dynamic_topology(minute_of_day: int, conn_str: str) -> dict:
    """
    Return {sats: [{key, lat, lng}], has_data: bool} for a given minute.
    Used by the Leaflet frontend to draw 2 000 moving satellite markers.
    Falls back to has_data=False if SQL tables are absent.
    """
    infra_cs = _infra_conn_str(conn_str) if conn_str else None
    if not infra_cs or not _dynamic_tables_exist(infra_cs):
        return {"has_data": False, "sats": []}
    try:
        from services.sqlite_fallback import sql_or_sqlite
        conn, _ = sql_or_sqlite(infra_cs, 'infra.db', timeout=8)
        cur = conn.cursor()
        cur.execute(
            "SELECT SatID, Lat, Lng FROM SpaceNodes_Dynamic WHERE MinuteOfDay=?",
            (minute_of_day,)
        )
        sats = [{"key": f"dynsat-{r[0]}", "lat": float(r[1]), "lng": float(r[2])}
                for r in cur.fetchall()]
        conn.close()
        return {"has_data": True, "sats": sats, "minute": minute_of_day}
    except Exception as exc:
        return {"has_data": False, "sats": [], "error": str(exc)}


def route_dynamic(src: str, dst: str, minute_of_day: int,
                  conn_str: str | None = None,
                  disabled_edge: tuple | None = None) -> dict:
    """
    Route through the pre-computed dynamic satellite topology for a given minute.
    Graph is built on-the-fly from SQL: DC→GW fiber, GW→nearest-sat uplinks,
    sat→sat ISL edges. Falls back to static route() if tables are absent.
    """
    _ensure_graphs(conn_str)

    if src not in _NODE_MAP:
        return {"error": f"Unknown source: {src!r}"}
    if dst not in _NODE_MAP:
        return {"error": f"Unknown destination: {dst!r}"}

    infra_cs = _infra_conn_str(conn_str) if conn_str else None
    if not infra_cs or not _dynamic_tables_exist(infra_cs):
        return route(src, dst, disabled_edge=disabled_edge,
                     conn_str=conn_str, hour_utc=minute_of_day // 60)

    try:
        import pyodbc
        conn = pyodbc.connect(infra_cs, timeout=8)
        cur  = conn.cursor()

        # Load satellite positions
        cur.execute(
            "SELECT SatID, Lat, Lng FROM SpaceNodes_Dynamic WHERE MinuteOfDay=?",
            minute_of_day
        )
        sat_data = {f"dynsat-{r[0]}": {"key": f"dynsat-{r[0]}", "lat": float(r[1]),
                                        "lng": float(r[2]), "type": "satellite",
                                        "provider": "SpaceX", "label": f"SL-{r[0]}"}
                    for r in cur.fetchall()}

        # Load ISL edges
        cur.execute(
            "SELECT SatA, SatB, DistKM, LatencyMS FROM SpaceEdges_Dynamic WHERE MinuteOfDay=?",
            minute_of_day
        )
        isl_edges = [(f"dynsat-{r[0]}", f"dynsat-{r[1]}", float(r[2]), float(r[3]))
                     for r in cur.fetchall()]
        conn.close()

    except Exception as exc:
        return route(src, dst, disabled_edge=disabled_edge,
                     conn_str=conn_str, hour_utc=minute_of_day // 60)

    # ── Build the per-minute Starlink graph ───────────────────────────────────
    Gs = nx.Graph()
    gw_nodes = [n for n in _ALL_NODES if n["type"] == "starlink_gw"]
    dc_nodes = [n for n in _ALL_NODES
                if n["type"] in ("cloud_dc", "openai_dc", "aws_ai", "meta_ai")]

    for n in gw_nodes + dc_nodes:
        Gs.add_node(n["key"], **n)
    for key, data in sat_data.items():
        Gs.add_node(key, **data)

    # ISL laser edges
    for satA, satB, dist_km, lat_ms in isl_edges:
        if satA in Gs and satB in Gs:
            Gs.add_edge(satA, satB, edge_type="starlink_laser",
                        distance_km=dist_km, latency_ms=lat_ms)

    # GW → nearest satellite uplinks (max 800 km slant range)
    sat_list = list(sat_data.values())
    for gw in gw_nodes:
        nearest = sorted(sat_list,
                         key=lambda s: _haversine_km(gw["lat"], gw["lng"],
                                                      s["lat"], s["lng"]))[:GW_SAT_K]
        for sat in nearest:
            km_surf  = _haversine_km(gw["lat"], gw["lng"], sat["lat"], sat["lng"])
            if km_surf > 800:
                continue
            km_slant = math.sqrt(km_surf ** 2 + SAT_ALT_KM ** 2)
            ms       = (km_slant / VACUUM_KM_S) * 1000.0 + UPLINK_MS
            Gs.add_edge(gw["key"], sat["key"],
                        edge_type="starlink_uplink",
                        distance_km=round(km_slant, 1),
                        latency_ms=round(ms, 3))

    # DC → nearest 2 GWs via fiber
    for dc in dc_nodes:
        for gw in sorted(gw_nodes,
                         key=lambda g: _haversine_km(dc["lat"], dc["lng"],
                                                      g["lat"], g["lng"]))[:2]:
            km = _haversine_km(dc["lat"], dc["lng"], gw["lat"], gw["lng"])
            ms = (km / FIBER_KM_S) * 1000.0
            Gs.add_edge(dc["key"], gw["key"],
                        edge_type="fiber",
                        distance_km=round(km, 1),
                        latency_ms=round(ms, 3))

    # ── Terrestrial path (with congestion) ───────────────────────────────────
    Gt = _apply_congestion(_G_TERRESTRIAL, _NODE_MAP, minute_of_day // 60)
    if disabled_edge:
        Gt = Gt.copy()
        if Gt.has_edge(*disabled_edge):
            Gt.remove_edge(*disabled_edge)

    combined_map = {**_NODE_MAP, **sat_data}

    def _coords(path):
        return [{"key": k, "lat": combined_map[k]["lat"], "lng": combined_map[k]["lng"],
                 "label": combined_map[k]["label"]}
                for k in path if k in combined_map]

    try:
        t_path = nx.dijkstra_path(Gt, src, dst, weight="latency_ms")
        t_ms   = sum(Gt[u][v]["latency_ms"]  for u, v in zip(t_path, t_path[1:]))
        t_km   = sum(Gt[u][v]["distance_km"] for u, v in zip(t_path, t_path[1:]))
    except (nx.NetworkXNoPath, nx.NodeNotFound):
        t_path, t_ms, t_km = [], None, None

    try:
        s_path = nx.dijkstra_path(Gs, src, dst, weight="latency_ms")
        s_ms   = sum(Gs[u][v]["latency_ms"]  for u, v in zip(s_path, s_path[1:]))
        s_km   = sum(Gs[u][v]["distance_km"] for u, v in zip(s_path, s_path[1:]))
    except (nx.NetworkXNoPath, nx.NodeNotFound):
        s_path, s_ms, s_km = [], None, None

    if t_ms is None and s_ms is None:
        return {"error": "No path found on any network for this minute."}

    return {
        "terrestrial": {
            "path":        t_path,
            "coords":      _coords(t_path),
            "latency_ms":  round(t_ms, 1) if t_ms is not None else None,
            "distance_km": round(t_km)    if t_km is not None else None,
            "hops":        len(t_path) - 1,
        },
        "starlink": {
            "path":        s_path,
            "coords":      _coords(s_path),
            "latency_ms":  round(s_ms, 1) if s_ms is not None else None,
            "distance_km": round(s_km)    if s_km is not None else None,
            "hops":        len(s_path) - 1,
        },
        "savings_pct": (
            round((1 - s_ms / t_ms) * 100, 1) if t_ms and s_ms and t_ms > 0 else None
        ),
        "minute_of_day":  minute_of_day,
        "hour_utc":       minute_of_day // 60,
        "congestion_active":         True,
        "starlink_geometry_active":  True,
        "dynamic_topology":          True,
    }
