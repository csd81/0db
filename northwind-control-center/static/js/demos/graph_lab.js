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

// MST edge layer — individual polylines accumulated during animation
let mstPolylines = [];

const COLORS = {
    frontier: '#0dcaf0',
    current:  '#ffc107',
    settled:  '#2a3040',
    path:     '#198754',
    mst:      '#adb5bd',
};

const PALETTE = [
    '#e63946', '#2a9d8f', '#e9c46a', '#457b9d',
    '#f4a261', '#8338ec', '#06d6a0', '#fb5607',
];

// ── State ────────────────────────────────────────────────────────────────────
let registry    = null;   // {problems, algorithms, reduced_n}
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
    sel.onchange = updateAlgoUI;
    updateAlgoUI();
}

function updateAlgoUI() {
    const algo     = document.getElementById('sel-algo').value;
    const algoMeta = registry?.algorithms[algo] || {};

    // Show/hide the "To" row
    const needsDst = algoMeta.needs_dst !== false;
    document.getElementById('dst-row').style.display = needsDst ? '' : 'none';

    // Build extra-param inputs (e.g. walk-length k)
    const extraParams = algoMeta.extra_params || [];
    const epRow    = document.getElementById('extra-params-row');
    const epInputs = document.getElementById('extra-params-inputs');
    if (extraParams.length) {
        epInputs.innerHTML = extraParams.map(p => `
            <div>
              <div class="section-lbl">${esc(p.label)}</div>
              <input id="ep-${esc(p.id)}" type="number"
                     class="form-control form-control-sm bg-dark text-light border-secondary"
                     value="${p.default}" min="${p.min}" max="${p.max}">
            </div>`).join('');
        epRow.classList.remove('d-none');
    } else {
        epInputs.innerHTML = '';
        epRow.classList.add('d-none');
    }

    document.getElementById('algo-desc').textContent = algoMeta.description || '—';
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

// ── MST edge rendering ────────────────────────────────────────────────────────
function _addMstEdge(c1, c2, ferry, ocean) {
    const color = ocean ? '#9c4dcc' : ferry ? '#fd7e14' : COLORS.mst;
    const dash  = ocean ? '4 9' : ferry ? '9 6' : null;
    const opts  = {color, weight: 1.5, opacity: 0.75};
    if (dash) opts.dashArray = dash;
    const pl = L.polyline([[c1.lat, c1.lng], [c2.lat, c2.lng]], opts).addTo(map);
    mstPolylines.push(pl);
}

function renderTreeEdges(treeEdges, cityCoords) {
    for (const e of treeEdges) {
        const c1 = cityCoords[e.u] || {lat: e.lat1, lng: e.lng1};
        const c2 = cityCoords[e.v] || {lat: e.lat2, lng: e.lng2};
        _addMstEdge(c1, c2, e.ferry, e.ocean);
        // Colour both endpoints as "path" green
        if (cityCoords[e.u]) ensureMarker(e.u, cityCoords[e.u], COLORS.path, 4);
        if (cityCoords[e.v]) ensureMarker(e.v, cityCoords[e.v], COLORS.path, 4);
    }
    if (treeEdges.length) {
        const allPts = treeEdges.flatMap(e => [[e.lat1, e.lng1], [e.lat2, e.lng2]]);
        map.fitBounds(L.latLngBounds(allPts), {padding: [32, 32]});
    }
}

function clearMstEdges() {
    for (const pl of mstPolylines) map.removeLayer(pl);
    mstPolylines = [];
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
    if (!path || !path.length) return;
    const {land, ferry, ocean} = _buildSegments(path);
    landLine.setLatLngs(land);
    ferryLine.setLatLngs(ferry);
    oceanLine.setLatLngs(ocean);

    for (const hop of path) {
        ensureMarker(hop.name, {lat: hop.lat, lng: hop.lng, country: hop.country},
                     COLORS.path, 5);
    }
    if (path.length > 1) {
        map.fitBounds(L.latLngBounds(path.map(p => [p.lat, p.lng])), {padding: [32, 32]});
    }
}

function renderColoring(coloring, cityCoords) {
    for (const [name, colorIdx] of Object.entries(coloring)) {
        const c = cityCoords[name];
        if (c) ensureMarker(name, c, PALETTE[colorIdx % PALETTE.length], 5);
    }
    const pts = Object.values(cityCoords).map(c => [c.lat, c.lng]);
    if (pts.length) map.fitBounds(L.latLngBounds(pts), {padding: [32, 32]});
}

function clearLines() {
    landLine.setLatLngs([]);
    ferryLine.setLatLngs([]);
    oceanLine.setLatLngs([]);
    clearMstEdges();
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
        if (step.source && labMarkers[step.source]) {
            labMarkers[step.source].setStyle({color: COLORS.settled, fillColor: COLORS.settled});
        }
    }
    else if (step.type === 'pivot_node') {
        const c = cityCoords[step.node];
        if (c) ensureMarker(step.node, c, '#ffc107', 7);
    }
    else if (step.type === 'mst_edge') {
        // Draw the edge being admitted to the spanning tree
        const c1 = cityCoords[step.source];
        const c2 = cityCoords[step.target];
        if (c1 && c2) _addMstEdge(c1, c2, false, false);
        if (c1) ensureMarker(step.source, c1, COLORS.settled, 4);
        if (c2) ensureMarker(step.target, c2, COLORS.frontier, 5);
    }
    else if (step.type === 'relax_edge') {
        if (step.source && labMarkers[step.source]) {
            labMarkers[step.source].setStyle({color: COLORS.settled, fillColor: COLORS.settled});
        }
        const tc = cityCoords[step.target];
        if (tc) ensureMarker(step.target, tc, COLORS.frontier, 4);
    }
    else if (step.type === 'check_node') {
        const c    = cityCoords[step.node];
        const role = step.flags?.role;
        // walk_count: source = blue, dest = orange; euler/matrix: red
        const color = role === 'source' ? '#0dcaf0'
                    : role === 'dest'   ? '#fd7e14'
                    : '#ff2255';
        if (c) ensureMarker(step.node, c, color, 7);
    }
    else if (step.type === 'color_node') {
        const c = cityCoords[step.node];
        const color = PALETTE[(step.flags?.color ?? 0) % PALETTE.length];
        if (c) {
            ensureMarker(step.node, c, COLORS.current, 6);
            setTimeout(() => ensureMarker(step.node, c, color, 4), 150);
        }
    }
    else if (step.type === 'negative_relax') {
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

// ── Result panel (analysis algorithms) ───────────────────────────────────────
function setResultPanel(text) {
    const p = document.getElementById('result-panel');
    if (!p) return;
    p.textContent = text || '';
    p.classList.toggle('d-none', !text);
}

// ── Completion renderer — branches on result_type ─────────────────────────────
function _onComplete(data, cityCoords, solveMs) {
    setBadge('done', 'success');

    if (data.result_type === 'coloring') {
        renderColoring(data.coloring || {}, cityCoords);
        const chi = data.chromatic_number ?? '?';
        setLabel(data.verdict || `χ(G) = ${chi} colours`);
        setResultPanel(data.detail || '');
        document.getElementById('m-dist').textContent    = chi;
        document.getElementById('m-hops').textContent    = '—';
        document.getElementById('m-visited').textContent = data.n_visited ?? '—';

    } else if (data.result_type === 'tree') {
        renderTreeEdges(data.tree_edges || [], cityCoords);
        const edgeCount = (data.tree_edges || []).length;
        setLabel(`${edgeCount} edges · ${(data.total_km ?? 0).toLocaleString()} km MST · ${solveMs} ms`);
        document.getElementById('m-dist').textContent    = (data.total_km ?? '—').toLocaleString();
        document.getElementById('m-hops').textContent    = edgeCount;
        document.getElementById('m-visited').textContent = data.n_visited ?? '—';
        setResultPanel('');

    } else if (data.result_type === 'analysis') {
        const a = data.analysis || {};
        setLabel(a.verdict || 'Analysis complete');
        setResultPanel(a.detail || '');
        document.getElementById('m-dist').textContent    = '—';
        document.getElementById('m-hops').textContent    = a.n_odd != null ? `${a.n_odd} odd` : '—';
        document.getElementById('m-visited').textContent = data.n_visited ?? '—';

    } else {
        renderFinalPath(data.path || [], cityCoords);
        const confStr = data.confidence != null
            ? ` · ${(data.confidence * 100).toFixed(1)}% reliable` : '';
        const isTsp = data.algorithm === 'tsp_approx';
        const suffix = isTsp ? ' (≤2×OPT)' : confStr;
        setLabel(`${data.hop_count} hops · ${(data.total_km ?? 0).toLocaleString()} km · ${solveMs} ms${suffix}`);
        updateMetrics(data);
        setResultPanel('');
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

    const src       = resolveCity(document.getElementById('sel-src').value);
    const dst       = resolveCity(document.getElementById('sel-dst').value);
    const problem   = document.getElementById('sel-problem').value;
    const algorithm = document.getElementById('sel-algo').value;
    const needsDst  = registry?.algorithms[algorithm]?.needs_dst !== false;

    // Collect any extra params (e.g. k for walk_count)
    const extraParams = {};
    for (const p of (registry?.algorithms[algorithm]?.extra_params || [])) {
        const el = document.getElementById(`ep-${p.id}`);
        if (el) extraParams[p.id] = p.type === 'int'
            ? Math.max(p.min, Math.min(p.max, parseInt(el.value, 10) || p.default))
            : parseFloat(el.value) || p.default;
    }

    setBadge('computing…', 'warning');
    setLabel(needsDst
        ? `${registry?.algorithms[algorithm]?.label || algorithm}: ${src} → ${dst}`
        : `${registry?.algorithms[algorithm]?.label || algorithm}: from ${src}`);

    const t0 = performance.now();
    let data;
    try {
        const r = await fetch('/demos/graph_lab/solve', {
            method:  'POST',
            headers: {'Content-Type': 'application/json'},
            body:    JSON.stringify({problem, algorithm, src, dst, params: extraParams}),
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
        setBadge('done', 'success');
        const fb_conf = data.confidence != null ? ` · ${(data.confidence * 100).toFixed(1)}% reliable` : '';
        setLabel(data.warnings?.[0] || `${data.hop_count} hops · ${(data.total_km ?? 0).toLocaleString()} km${fb_conf}`);
        _onComplete(data, cityCoords, solveMs);
        return;
    }

    setBadge('running', 'warning');
    let i = 0;
    playTimer = setInterval(() => {
        if (i >= steps.length) {
            clearInterval(playTimer);
            playTimer = null;
            _onComplete(data, cityCoords, solveMs);
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
    setResultPanel('');
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
