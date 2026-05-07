'use strict';

// ── Tile URLs ────────────────────────────────────────────────────────────────
const GL_TILE_DARK  = 'https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png';
const GL_TILE_LIGHT = 'https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png';
const LINE_ALT = 8000;  // metres — lift lines above ellipsoid for depth precision

// ── Leaflet map ──────────────────────────────────────────────────────────────
const _initTheme = document.documentElement.getAttribute('data-bs-theme') || 'dark';
const map = L.map('gl-map', {zoomControl: true}).setView([35, 40], 3);
const leafletLayer = L.tileLayer(
    _initTheme === 'light' ? GL_TILE_LIGHT : GL_TILE_DARK,
    {
        attribution: '&copy; <a href="https://openstreetmap.org">OpenStreetMap</a> &copy; <a href="https://carto.com">CARTO</a>',
        subdomains: 'abcd',
        maxZoom: 19,
    }
).addTo(map);

// Three path layers — same visual language as graph_routing.js
const landLine  = L.polyline([], {color: '#0d6efd', weight: 2.5, opacity: 0.85}).addTo(map);
const ferryLine = L.polyline([], {color: '#fd7e14', weight: 3,   opacity: 0.9,  dashArray: '9 6'}).addTo(map);
const oceanLine = L.polyline([], {color: '#9c4dcc', weight: 3,   opacity: 0.9,  dashArray: '4 9'}).addTo(map);

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

// ── Cesium 3D globe ──────────────────────────────────────────────────────────
let cesiumViewer = null;
let is3D         = false;
let cPointColl   = null;
let cPoints      = {};   // name → PointPrimitive
let cPolylines   = [];   // Cesium Entity refs for cleanup

function _cColor(hex) {
    return Cesium.Color.fromCssColorString(hex);
}

function _initCesiumViewer() {
    cesiumViewer = new Cesium.Viewer('gl-globe', {
        animation: false, baseLayerPicker: false, fullscreenButton: false,
        geocoder: false, homeButton: false, infoBox: false,
        navigationHelpButton: false, sceneModePicker: false, timeline: false,
        selectionIndicator: false,
        imageryProvider: false,
        terrainProvider: new Cesium.EllipsoidTerrainProvider(),
    });
    cPointColl = cesiumViewer.scene.primitives.add(new Cesium.PointPrimitiveCollection());
    _glSetTiles(document.documentElement.getAttribute('data-bs-theme') || 'dark');
}

function _glSetTiles(theme) {
    if (!cesiumViewer) return;
    cesiumViewer.imageryLayers.removeAll();
    cesiumViewer.imageryLayers.addImageryProvider(
        new Cesium.UrlTemplateImageryProvider({
            url: theme === 'light'
                ? 'https://a.basemaps.cartocdn.com/light_all/{z}/{x}/{y}.png'
                : 'https://a.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}.png',
            credit: '',
        })
    );
    cesiumViewer.scene.globe.baseColor = Cesium.Color.fromCssColorString(
        theme === 'light' ? '#d0d8e4' : '#06080c');
    cesiumViewer.scene.backgroundColor = theme === 'light'
        ? new Cesium.Color(0.9, 0.93, 0.97, 1.0)
        : new Cesium.Color(0.02, 0.03, 0.05, 1.0);
}

function _ensureCPoint(name, lat, lng, colorHex, pixelSize) {
    const color = _cColor(colorHex);
    const sz    = pixelSize || 5;
    if (cPoints[name]) {
        cPoints[name].color     = color;
        cPoints[name].pixelSize = sz;
    } else {
        cPoints[name] = cPointColl.add({
            position: Cesium.Cartesian3.fromDegrees(lng, lat, 5000),
            color,
            pixelSize: sz,
            disableDepthTestDistance: 5e6,
        });
    }
}

function _clearCPoints() {
    if (cPointColl) cPointColl.removeAll();
    cPoints = {};
}

function _drawCLine(lat1, lng1, lat2, lng2, colorHex, width) {
    if (!cesiumViewer) return;
    const entity = cesiumViewer.entities.add({
        polyline: {
            positions: Cesium.Cartesian3.fromDegreesArrayHeights([
                lng1, lat1, LINE_ALT,
                lng2, lat2, LINE_ALT,
            ]),
            width: width || 2,
            material: new Cesium.ColorMaterialProperty(_cColor(colorHex)),
            arcType: Cesium.ArcType.GEODESIC,
        },
    });
    cPolylines.push(entity);
}

function _clearCLines() {
    if (!cesiumViewer) return;
    for (const e of cPolylines) cesiumViewer.entities.remove(e);
    cPolylines = [];
}

// ── 2D/3D toggle ─────────────────────────────────────────────────────────────
document.getElementById('btn-2d').addEventListener('click', () => {
    if (!is3D) return;
    is3D = false;
    document.getElementById('gl-map').style.display   = '';
    document.getElementById('gl-globe').style.display = 'none';
    document.getElementById('btn-2d').classList.add('active');
    document.getElementById('btn-3d').classList.remove('active');
    setTimeout(() => map.invalidateSize(), 50);
});

document.getElementById('btn-3d').addEventListener('click', () => {
    if (is3D) return;
    is3D = true;
    if (!cesiumViewer) _initCesiumViewer();
    document.getElementById('gl-map').style.display   = 'none';
    document.getElementById('gl-globe').style.display = '';
    document.getElementById('btn-2d').classList.remove('active');
    document.getElementById('btn-3d').classList.add('active');
    setTimeout(() => cesiumViewer.resize(), 50);
});

// ── Theme switching ───────────────────────────────────────────────────────────
document.addEventListener('themeChanged', e => {
    const theme = e.detail;
    leafletLayer.setUrl(theme === 'light' ? GL_TILE_LIGHT : GL_TILE_DARK);
    _glSetTiles(theme);
});

// ── State ────────────────────────────────────────────────────────────────────
let registry    = null;
let cityNameMap = {};
let labMarkers  = {};
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

    // Always show the To field — grey it out when the algorithm doesn't need it
    const needsDst = algoMeta.needs_dst !== false;
    const dstInput = document.getElementById('sel-dst');
    const dstRow   = document.getElementById('dst-row');
    dstInput.disabled    = !needsDst;
    dstRow.style.opacity = needsDst ? '1' : '0.3';

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

    // Best-database badge
    const db = algoMeta.best_db || {};
    document.getElementById('db-badge').innerHTML = db.name ? `
      <span style="display:inline-flex;align-items:center;gap:.35rem;
                   background:#0e1014;border:1px solid ${db.color}33;
                   border-left:3px solid ${db.color};border-radius:.25rem;
                   padding:.2rem .45rem;font-size:.65rem;color:${db.color}">
        <b>${esc(db.type)}:</b>&nbsp;${esc(db.name)}
      </span>
      <div style="font-size:.62rem;color:#6c757d;margin-top:.2rem">${esc(db.why)}</div>
    ` : '';
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

// ── Leaflet markers ───────────────────────────────────────────────────────────
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
    if (is3D) _ensureCPoint(name, coords.lat, coords.lng, color, (radius || 4) + 1);
}

function clearMarkers() {
    for (const m of Object.values(labMarkers)) map.removeLayer(m);
    labMarkers = {};
    _clearCPoints();
}

// ── MST edge rendering ────────────────────────────────────────────────────────
function _addMstEdge(c1, c2, ferry, ocean) {
    const color = ocean ? '#9c4dcc' : ferry ? '#fd7e14' : COLORS.mst;
    const dash  = ocean ? '4 9' : ferry ? '9 6' : null;
    const opts  = {color, weight: 1.5, opacity: 0.75};
    if (dash) opts.dashArray = dash;
    const pl = L.polyline([[c1.lat, c1.lng], [c2.lat, c2.lng]], opts).addTo(map);
    mstPolylines.push(pl);
    if (is3D) _drawCLine(c1.lat, c1.lng, c2.lat, c2.lng, color, 1.5);
}

function renderTreeEdges(treeEdges, cityCoords) {
    for (const e of treeEdges) {
        const c1 = cityCoords[e.u] || {lat: e.lat1, lng: e.lng1};
        const c2 = cityCoords[e.v] || {lat: e.lat2, lng: e.lng2};
        _addMstEdge(c1, c2, e.ferry, e.ocean);
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
    _clearCLines();
}

// ── Path line rendering ───────────────────────────────────────────────────────
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

    if (is3D) {
        for (let i = 1; i < path.length; i++) {
            const a = path[i-1], b = path[i];
            const col = b.ocean ? '#9c4dcc' : b.ferry ? '#fd7e14' : '#0d6efd';
            _drawCLine(a.lat, a.lng, b.lat, b.lng, col, 2.5);
        }
    }

    for (const hop of path) {
        ensureMarker(hop.name, {lat: hop.lat, lng: hop.lng, country: hop.country},
                     COLORS.path, 5);
    }
    if (path.length > 1) {
        map.fitBounds(L.latLngBounds(path.map(p => [p.lat, p.lng])), {padding: [32, 32]});
    }
}

function renderBridgeEdges(treeEdges, cityCoords) {
    for (const e of treeEdges) {
        const c1 = cityCoords[e.u] || {lat: e.lat1, lng: e.lng1};
        const c2 = cityCoords[e.v] || {lat: e.lat2, lng: e.lng2};
        const pl = L.polyline([[c1.lat, c1.lng], [c2.lat, c2.lng]],
                              {color: '#ff2255', weight: 2.5, opacity: 0.9}).addTo(map);
        mstPolylines.push(pl);
        if (is3D) _drawCLine(c1.lat, c1.lng, c2.lat, c2.lng, '#ff2255', 2.5);
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
    if (step.type === 'visit_node') {
        const c = cityCoords[step.node];
        if (c) ensureMarker(step.node, c, COLORS.current, 5);
    }
    else if (step.type === 'enqueue' || step.type === 'push_stack') {
        const c = cityCoords[step.node];
        if (c) ensureMarker(step.node, c, COLORS.frontier, 4);
        if (step.source && labMarkers[step.source]) {
            labMarkers[step.source].setStyle({color: COLORS.settled, fillColor: COLORS.settled});
            if (is3D && cPoints[step.source]) cPoints[step.source].color = _cColor(COLORS.settled);
        }
    }
    else if (step.type === 'pivot_node') {
        const c = cityCoords[step.node];
        if (c) ensureMarker(step.node, c, '#ffc107', 7);
    }
    else if (step.type === 'mst_edge') {
        const c1 = cityCoords[step.source];
        const c2 = cityCoords[step.target];
        if (c1 && c2) _addMstEdge(c1, c2, false, false);
        if (c1) ensureMarker(step.source, c1, COLORS.settled, 4);
        if (c2) ensureMarker(step.target, c2, COLORS.frontier, 5);
    }
    else if (step.type === 'relax_edge') {
        if (step.source && labMarkers[step.source]) {
            labMarkers[step.source].setStyle({color: COLORS.settled, fillColor: COLORS.settled});
            if (is3D && cPoints[step.source]) cPoints[step.source].color = _cColor(COLORS.settled);
        }
        const tc = cityCoords[step.target];
        if (tc) ensureMarker(step.target, tc, COLORS.frontier, 4);
    }
    else if (step.type === 'check_node') {
        const c    = cityCoords[step.node];
        const role = step.flags?.role;
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
    else if (step.type === 'bridge_edge') {
        const c1 = cityCoords[step.source];
        const c2 = cityCoords[step.target];
        if (c1 && c2) {
            const pl = L.polyline([[c1.lat, c1.lng], [c2.lat, c2.lng]],
                                  {color: '#ff2255', weight: 2.5, opacity: 0.9}).addTo(map);
            mstPolylines.push(pl);
            if (is3D) _drawCLine(c1.lat, c1.lng, c2.lat, c2.lng, '#ff2255', 2.5);
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

// ── Result panel ──────────────────────────────────────────────────────────────
function setResultPanel(text) {
    const p = document.getElementById('result-panel');
    if (!p) return;
    p.textContent = text || '';
    p.classList.toggle('d-none', !text);
}

// ── Completion renderer ───────────────────────────────────────────────────────
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
        if ((data.tree_edges || []).length) renderBridgeEdges(data.tree_edges, cityCoords);
        for (const name of (a.cut_vertices || [])) {
            const c = cityCoords[name];
            if (c) ensureMarker(name, c, '#ff2255', 8);
        }
        setLabel(a.verdict || 'Analysis complete');
        setResultPanel(a.detail || '');
        document.getElementById('m-dist').textContent    = a.n_cut  != null ? a.n_cut  : (a.n_odd != null ? `${a.n_odd} odd` : '—');
        document.getElementById('m-hops').textContent    = a.n_bridges != null ? a.n_bridges : '—';
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
