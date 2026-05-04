'use strict';

// ── Leaflet map ──────────────────────────────────────────────────────────────
const map = L.map('gl-map', {zoomControl: true}).setView([35, 40], 3);
L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
    attribution: '&copy; <a href="https://openstreetmap.org">OpenStreetMap</a> &copy; <a href="https://carto.com">CARTO</a>',
    subdomains: 'abcd',
    maxZoom: 19,
}).addTo(map);

// Three path layers — reuse the same visual language as graph_routing.js
const landLine  = L.polyline([], {color: '#0d6efd', weight: 2.5, opacity: 0.85}).addTo(map);
const ferryLine = L.polyline([], {color: '#fd7e14', weight: 3,   opacity: 0.9,  dashArray: '9 6'}).addTo(map);
const oceanLine = L.polyline([], {color: '#9c4dcc', weight: 3,   opacity: 0.9,  dashArray: '4 9'}).addTo(map);

const COLORS = {
    frontier: '#0dcaf0',
    current:  '#ffc107',
    settled:  '#2a3040',
    path:     '#198754',
};

// ── State ────────────────────────────────────────────────────────────────────
let registry   = null;   // {problems, algorithms, reduced_n}
let cityNameMap = {};     // "Name (CC)" → raw name
let labMarkers  = {};     // name → L.circleMarker (created lazily during animation)
let playTimer   = null;
let playMs      = 80;

function esc(s) { return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;'); }

// ── Registry — dual dropdown ─────────────────────────────────────────────────
async function loadRegistry() {
    try {
        registry = await fetch('/demos/graph_lab/algorithms').then(r => r.json());
        buildProblemDropdown();
    } catch (e) {
        console.error('Failed to load algorithm registry', e);
    }
}

function buildProblemDropdown() {
    const sel = document.getElementById('sel-problem');
    sel.innerHTML = Object.entries(registry.problems)
        .map(([k, v]) => `<option value="${esc(k)}">${esc(v.label)}</option>`)
        .join('');
    sel.addEventListener('change', () => buildAlgoDropdown(sel.value));
    buildAlgoDropdown(sel.value);
}

function buildAlgoDropdown(problem) {
    const sel   = document.getElementById('sel-algo');
    const algos = registry.problems[problem]?.algorithms || [];
    sel.innerHTML = algos
        .map(a => `<option value="${esc(a)}">${esc(registry.algorithms[a]?.label || a)}</option>`)
        .join('');
    sel.onchange = updateDescription;
    updateDescription();
}

function updateDescription() {
    const algo = document.getElementById('sel-algo').value;
    document.getElementById('algo-desc').textContent =
        registry?.algorithms[algo]?.description || '—';
}

// ── City datalist ─────────────────────────────────────────────────────────────
async function loadCitiesDatalist() {
    try {
        const cs = await fetch('/demos/graph_routing/cities').then(r => r.json());
        const dl = document.getElementById('cities-dl');
        const frags = [];
        for (const c of cs) {
            const label = `${c.name} (${c.country})`;
            cityNameMap[label]  = c.name;
            cityNameMap[c.name] = c.name;
            frags.push(`<option value="${esc(label)}">`);
        }
        dl.innerHTML = frags.join('');
    } catch (_) { /* optional — raw names still work */ }
}

function resolveCity(val) {
    const v = val.trim();
    return cityNameMap[v] || v;
}

// ── Markers — created lazily during animation ─────────────────────────────────
function ensureMarker(name, coords, color, radius) {
    if (!labMarkers[name]) {
        const m = L.circleMarker([coords.lat, coords.lng], {
            radius: radius || 4,
            color, fillColor: color, fillOpacity: 0.85, weight: 1,
        }).addTo(map);
        m.bindTooltip(`<b>${esc(name)}</b>${coords.country ? ' (' + esc(coords.country) + ')' : ''}`,
                      {sticky: true});
        labMarkers[name] = m;
    } else {
        labMarkers[name].setStyle({color, fillColor: color,
                                   radius: radius || labMarkers[name].options.radius});
    }
}

function clearMarkers() {
    for (const m of Object.values(labMarkers)) map.removeLayer(m);
    labMarkers = {};
}

// ── Path line rendering — same _buildSegments logic as graph_routing.js ───────
function _buildSegments(path) {
    const land = [], ferry = [], ocean = [];
    if (!path || path.length < 2) return {land, ferry, ocean};
    let curType = 0;
    let curPts  = [[path[0].lat, path[0].lng]];
    const flush = (nextLL) => {
        if (nextLL) curPts.push(nextLL);
        if (curPts.length >= 2) {
            if (curType === 2) ocean.push(curPts);
            else if (curType === 1) ferry.push(curPts);
            else land.push(curPts);
        }
    };
    for (let i = 1; i < path.length; i++) {
        const p    = path[i];
        const type = p.ocean ? 2 : p.ferry ? 1 : 0;
        const ll   = [p.lat, p.lng];
        if (type === curType) {
            curPts.push(ll);
        } else {
            flush(ll);
            curType = type;
            curPts  = [curPts[curPts.length - 1], ll];
        }
    }
    flush(null);
    return {land, ferry, ocean};
}

function renderFinalPath(path, cityCoords) {
    const {land, ferry, ocean} = _buildSegments(path);
    landLine.setLatLngs(land);
    ferryLine.setLatLngs(ferry);
    oceanLine.setLatLngs(ocean);

    // Colour path markers green
    for (const hop of path) {
        ensureMarker(hop.name, {lat: hop.lat, lng: hop.lng, country: hop.country},
                     COLORS.path, 5);
    }

    if (path.length > 1) {
        map.fitBounds(L.latLngBounds(path.map(p => [p.lat, p.lng])), {padding: [32, 32]});
    }
}

function clearLines() {
    landLine.setLatLngs([]);
    ferryLine.setLatLngs([]);
    oceanLine.setLatLngs([]);
}

// ── Banner helpers ────────────────────────────────────────────────────────────
function setBadge(text, color) {
    const b = document.getElementById('phase-badge');
    b.className   = `badge bg-${color} phase-badge`;
    b.textContent = text;
}

function setLabel(text) {
    document.getElementById('phase-label').textContent = text;
}

// ── Universal event replayer ──────────────────────────────────────────────────
function applyStep(step, cityCoords) {
    const coords = cityCoords[step.node] || cityCoords[step.source];

    if (step.type === 'visit_node') {
        if (coords) ensureMarker(step.node, coords, COLORS.current, 5);
    }
    else if (step.type === 'enqueue' || step.type === 'push_stack') {
        const c = cityCoords[step.node];
        if (c) ensureMarker(step.node, c, COLORS.frontier, 4);
        // Dim the source to settled
        if (step.source && labMarkers[step.source]) {
            labMarkers[step.source].setStyle({color: COLORS.settled, fillColor: COLORS.settled});
        }
    }
    else if (step.type === 'relax_edge') {
        // Mark source as settled, target as frontier
        if (step.source && labMarkers[step.source]) {
            labMarkers[step.source].setStyle({color: COLORS.settled, fillColor: COLORS.settled});
        }
        const tc = cityCoords[step.target];
        if (tc) ensureMarker(step.target, tc, COLORS.frontier, 4);
    }
    else if (step.type === 'negative_relax') {  // Phase 2 Bellman-Ford
        const tc = cityCoords[step.target];
        if (tc) ensureMarker(step.target, tc, '#ff2255', 5);
    }
    else if (step.type === 'error') {
        setBadge('error', 'danger');
        setLabel(step.flags?.message || 'Algorithm error');
        clearInterval(playTimer);
        playTimer = null;
    }
}

// ── Main run ──────────────────────────────────────────────────────────────────
async function runLab() {
    clearInterval(playTimer);
    playTimer = null;
    clearMarkers();
    clearLines();
    ['m-dist','m-hops','m-visited','m-time'].forEach(id =>
        document.getElementById(id).textContent = '—');

    const src = resolveCity(document.getElementById('sel-src').value);
    const dst = resolveCity(document.getElementById('sel-dst').value);
    const problem   = document.getElementById('sel-problem').value;
    const algorithm = document.getElementById('sel-algo').value;

    setBadge('computing…', 'warning');
    setLabel(`${registry?.algorithms[algorithm]?.label || algorithm}: ${src} → ${dst}`);

    const t0 = performance.now();
    let data;
    try {
        const r = await fetch('/demos/graph_lab/solve', {
            method:  'POST',
            headers: {'Content-Type': 'application/json'},
            body:    JSON.stringify({problem, algorithm, src, dst}),
        });
        data = await r.json();
    } catch (e) {
        setBadge('error', 'danger');
        setLabel(`Network error: ${esc(e.message)}`);
        return;
    }
    const solveMs = (performance.now() - t0).toFixed(0);

    if (data.error) {
        setBadge('error', 'danger');
        setLabel(data.error);
        return;
    }

    document.getElementById('m-time').textContent = solveMs;

    const steps      = data.steps || [];
    const cityCoords = data.city_coords || {};

    if (!steps.length) {
        // Phase 0 fallback — no animation, just draw the path
        renderFinalPath(data.path, cityCoords);
        setBadge('done', 'success');
        const fb_conf = data.confidence != null ? ` · ${(data.confidence * 100).toFixed(1)}% reliable` : '';
        setLabel(data.warnings?.[0] || `${data.hop_count} hops · ${(data.total_km ?? 0).toLocaleString()} km${fb_conf}`);
        updateMetrics(data);
        return;
    }

    setBadge('running', 'warning');
    let i = 0;
    playTimer = setInterval(() => {
        if (i >= steps.length) {
            clearInterval(playTimer);
            playTimer = null;
            renderFinalPath(data.path, cityCoords);
            setBadge('done', 'success');
            const confStr = data.confidence != null
                ? ` · ${(data.confidence * 100).toFixed(1)}% reliable` : '';
            setLabel(`${data.hop_count} hops · ${(data.total_km ?? 0).toLocaleString()} km · ${solveMs} ms${confStr}`);
            updateMetrics(data);
            return;
        }
        applyStep(steps[i++], cityCoords);
    }, playMs);
}

function updateMetrics(data) {
    document.getElementById('m-dist').textContent    = (data.total_km ?? '—').toLocaleString();
    document.getElementById('m-hops').textContent    = data.hop_count ?? '—';
    document.getElementById('m-visited').textContent = data.n_visited  ?? '—';
}

// ── Reset ─────────────────────────────────────────────────────────────────────
function resetLab() {
    clearInterval(playTimer);
    playTimer = null;
    clearMarkers();
    clearLines();
    ['m-dist','m-hops','m-visited','m-time'].forEach(id =>
        document.getElementById(id).textContent = '—');
    setBadge('idle', 'secondary');
    setLabel('—');
}

// ── Button handlers ───────────────────────────────────────────────────────────
document.getElementById('btn-run').addEventListener('click', runLab);
document.getElementById('btn-reset').addEventListener('click', resetLab);

document.querySelectorAll('.speed-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        playMs = parseInt(btn.dataset.ms, 10);
        document.querySelectorAll('.speed-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
    });
});

// ── Init ──────────────────────────────────────────────────────────────────────
loadRegistry();
loadCitiesDatalist();
