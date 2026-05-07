'use strict';

// ══════════════════════════════════════════════════════════════════════════════
// ── 2D Leaflet map ────────────────────────────────────────────────────────────
// ══════════════════════════════════════════════════════════════════════════════
const map = L.map('gr-map', {zoomControl: true}).setView([35, 40], 3);

const TILE_DARK  = 'https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png';
const TILE_LIGHT = 'https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png';
const TILE_ATTR  = '&copy; <a href="https://openstreetmap.org">OpenStreetMap</a> &copy; <a href="https://carto.com">CARTO</a>';

let tileLayer = L.tileLayer(
    document.documentElement.getAttribute('data-bs-theme') === 'light' ? TILE_LIGHT : TILE_DARK,
    { attribution: TILE_ATTR, subdomains: 'abcd', maxZoom: 19 }
).addTo(map);

document.addEventListener('themeChanged', function(e) {
    tileLayer.setUrl(e.detail === 'light' ? TILE_LIGHT : TILE_DARK);
    if (cesiumViewer) _cesiumSetTiles(e.detail);
});

const landLine  = L.polyline([], {color: '#0d6efd', weight: 2.5, opacity: 0.85}).addTo(map);
const ferryLine = L.polyline([], {color: '#fd7e14', weight: 3,   opacity: 0.9,  dashArray: '9 6'}).addTo(map);
const oceanLine = L.polyline([], {color: '#9c4dcc', weight: 3,   opacity: 0.9,  dashArray: '4 9'}).addTo(map);

const COLORS = {
    unvisited: '#2a2d36',
    frontier:  '#0dcaf0',
    current:   '#ffc107',
    settled:   '#394050',
    path:      '#198754',
};

const markers      = {};
let   markersReady = false;
let   citiesLoaded = [];
const cityNameMap  = {};

function esc(s) {
    return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
}

// ── Datalist ─────────────────────────────────────────────────────────────────
async function loadCitiesDatalist() {
    try {
        const r  = await fetch('/demos/graph_routing/cities');
        const cs = await r.json();
        const dl = document.getElementById('cities-dl');
        const frags = [];
        for (const c of cs) {
            const label = `${c.name} (${c.country})`;
            cityNameMap[label]  = c.name;
            cityNameMap[c.name] = c.name;
            frags.push(`<option value="${esc(label)}">`);
        }
        dl.innerHTML = frags.join('');
    } catch (_) {}
}

function resolveCity(v) {
    v = v.trim();
    return cityNameMap[v] || v;
}

// ── Leaflet markers ───────────────────────────────────────────────────────────
function initMarkers(cities) {
    for (const m of Object.values(markers)) map.removeLayer(m);
    Object.keys(markers).forEach(k => delete markers[k]);
    citiesLoaded = cities;
    markersReady = false;

    for (const c of cities) {
        const m = L.circleMarker([c.lat, c.lng], {
            radius: 3, color: COLORS.unvisited,
            fillColor: COLORS.unvisited, fillOpacity: 0.7, weight: 1,
        }).addTo(map);
        m.bindTooltip(`<b>${esc(c.name)}</b> (${esc(c.country)})<br>Pop: ${c.population.toLocaleString()}`, {sticky: true});
        markers[c.name] = m;
    }
    markersReady = true;

    const dl = document.getElementById('cities-dl');
    if (!dl.childElementCount) {
        const frags = [];
        for (const n of cities.map(c => c.name).sort()) {
            frags.push(`<option value="${esc(n)}">`);
            cityNameMap[n] = n;
        }
        dl.innerHTML = frags.join('');
    }

    // Cesium: if viewer is already alive, init its markers too
    if (cesiumViewer) initCesiumMarkers(cities);
}

function updateMarkers(s) {
    if (!markersReady) return;
    const pathSet  = new Set((s.path || []).map(p => p.name));
    const visited  = new Set(s.visited || []);
    const frontier = new Set((s.frontier || []).map(f => f[0]));
    for (const [name, m] of Object.entries(markers)) {
        let color = COLORS.unvisited, r = 3;
        if (pathSet.has(name))            { color = COLORS.path;     r = 5; }
        else if (name === s.current_city) { color = COLORS.current;  r = 6; }
        else if (visited.has(name))       { color = COLORS.settled; }
        else if (frontier.has(name))      { color = COLORS.frontier; r = 4; }
        m.setStyle({color, fillColor: color, radius: r});
    }
    if (cesiumViewer) updateCesiumMarkers(s);
}

// ── Segment builder (shared by Leaflet + Cesium) ──────────────────────────────
function _buildSegments(path) {
    const land = [], ferry = [], ocean = [];
    if (!path || path.length < 2) return {land, ferry, ocean};
    let curType = 0, curPts = [[path[0].lat, path[0].lng]];
    const flush = (nextLL) => {
        if (nextLL) curPts.push(nextLL);
        if (curPts.length >= 2) {
            if (curType === 2) ocean.push(curPts);
            else if (curType === 1) ferry.push(curPts);
            else land.push(curPts);
        }
    };
    for (let i = 1; i < path.length; i++) {
        const p = path[i], type = p.ocean ? 2 : p.ferry ? 1 : 0, ll = [p.lat, p.lng];
        if (type === curType) { curPts.push(ll); }
        else { flush(ll); curType = type; curPts = [curPts[curPts.length - 1], ll]; }
    }
    flush(null);
    return {land, ferry, ocean};
}

// ── Leaflet path lines ────────────────────────────────────────────────────────
function updatePathLines(s) {
    if (!s.path || s.path.length < 2) {
        landLine.setLatLngs([]); ferryLine.setLatLngs([]); oceanLine.setLatLngs([]);
        if (cesiumViewer) clearCesiumLines();
        return;
    }
    const {land, ferry, ocean} = _buildSegments(s.path);
    landLine.setLatLngs(land);
    ferryLine.setLatLngs(ferry);
    oceanLine.setLatLngs(ocean);
    if (['found_path', 'done'].includes(s.phase) && s.path.length > 1 && !is3D) {
        map.fitBounds(L.latLngBounds(s.path.map(p => [p.lat, p.lng])), {padding: [32, 32]});
    }
    if (cesiumViewer) updateCesiumLines(s);
}

// ══════════════════════════════════════════════════════════════════════════════
// ── 3D Cesium globe (lazy-initialized on first 3D click) ─────────────────────
// ══════════════════════════════════════════════════════════════════════════════
let cesiumViewer  = null;
let is3D          = false;
let cPointColl    = null;   // PointPrimitiveCollection
const cPoints     = {};     // name → PointPrimitive
let cPathEntities = [];     // active path entity handles

function _cesiumSetTiles(theme) {
    if (!cesiumViewer) return;
    cesiumViewer.imageryLayers.removeAll();
    const url = theme === 'light'
        ? 'https://a.basemaps.cartocdn.com/light_all/{z}/{x}/{y}.png'
        : 'https://a.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}.png';
    cesiumViewer.imageryLayers.addImageryProvider(
        new Cesium.UrlTemplateImageryProvider({
            url, tilingScheme: new Cesium.WebMercatorTilingScheme(), maximumLevel: 19,
        })
    );
}

function _cColor(hex) { return Cesium.Color.fromCssColorString(hex); }

function _initCesiumViewer() {
    if (cesiumViewer) return;
    cesiumViewer = new Cesium.Viewer('gr-globe', {
        animation: false, baseLayerPicker: false, fullscreenButton: false,
        geocoder: false, homeButton: false, infoBox: false,
        navigationHelpButton: false, sceneModePicker: false,
        selectionIndicator: false, timeline: false,
        imageryProvider: false,
        terrainProvider: new Cesium.EllipsoidTerrainProvider(),
    });
    const theme = document.documentElement.getAttribute('data-bs-theme') || 'dark';
    _cesiumSetTiles(theme);

    cesiumViewer.scene.globe.baseColor           = _cColor('#06080c');
    cesiumViewer.scene.globe.enableLighting      = false;
    cesiumViewer.scene.globe.showGroundAtmosphere = false;
    cesiumViewer.scene.backgroundColor           = new Cesium.Color(0.02, 0.03, 0.05, 1.0);
    cesiumViewer.scene.fog.enabled               = false;
    cesiumViewer.scene.skyAtmosphere.show        = false;
    try { cesiumViewer.cesiumWidget.creditContainer.style.display = 'none'; } catch (_) {}

    // Initial camera — Europe-centered
    cesiumViewer.camera.setView({
        destination: Cesium.Cartesian3.fromDegrees(15, 48, 9_000_000),
    });

    cPointColl = cesiumViewer.scene.primitives.add(new Cesium.PointPrimitiveCollection());

    // If cities already loaded, build markers now
    if (citiesLoaded.length) initCesiumMarkers(citiesLoaded);
}

function initCesiumMarkers(cities) {
    if (!cesiumViewer || !cPointColl) return;
    cPointColl.removeAll();
    Object.keys(cPoints).forEach(k => delete cPoints[k]);
    for (const c of cities) {
        cPoints[c.name] = cPointColl.add({
            position: Cesium.Cartesian3.fromDegrees(c.lng, c.lat, 5000),
            color:    _cColor(COLORS.unvisited),
            pixelSize: 5,
            outlineWidth: 0,
            disableDepthTestDistance: 5e6,  // depth test re-engages at globe-view distance (>5 000 km)
        });
    }
}

function updateCesiumMarkers(s) {
    if (!cPointColl) return;
    const pathSet  = new Set((s.path || []).map(p => p.name));
    const visited  = new Set(s.visited || []);
    const frontier = new Set((s.frontier || []).map(f => f[0]));
    for (const [name, pt] of Object.entries(cPoints)) {
        let color = COLORS.unvisited, size = 5;
        if (pathSet.has(name))            { color = COLORS.path;     size = 8; }
        else if (name === s.current_city) { color = COLORS.current;  size = 9; }
        else if (visited.has(name))       { color = COLORS.settled; }
        else if (frontier.has(name))      { color = COLORS.frontier; size = 6; }
        pt.color     = _cColor(color);
        pt.pixelSize = size;
    }
}

// Draw segments as geodesic polylines lifted 8 km above the ellipsoid.
// Altitude > 0 is required: polylines at altitude 0 cause depth-precision failures
// that let the back hemisphere bleed through the globe surface.
const LINE_ALT = 8000;  // metres above ellipsoid — same principle as the 5 km point lift in global_infra

function _drawCesiumSegments(segments, hex, width) {
    const entities = [];
    const material = new Cesium.ColorMaterialProperty(_cColor(hex));

    for (const seg of segments) {
        if (seg.length < 2) continue;
        // [lng, lat, alt, lng, lat, alt, ...] for fromDegreesArrayHeights
        const degs = [];
        for (const [lat, lng] of seg) degs.push(lng, lat, LINE_ALT);
        entities.push(cesiumViewer.entities.add({
            polyline: {
                positions: Cesium.Cartesian3.fromDegreesArrayHeights(degs),
                width,
                material,
                arcType: Cesium.ArcType.GEODESIC,
                clampToGround: false,
            },
        }));
    }
    return entities;
}

function clearCesiumLines() {
    for (const e of cPathEntities) cesiumViewer.entities.remove(e);
    cPathEntities = [];
}

function updateCesiumLines(s) {
    if (!cesiumViewer) return;
    clearCesiumLines();
    if (!s.path || s.path.length < 2) return;
    const {land, ferry, ocean} = _buildSegments(s.path);
    cPathEntities = [
        ..._drawCesiumSegments(land,  '#0d6efd', 3.5),
        ..._drawCesiumSegments(ferry, '#fd7e14', 3),
        ..._drawCesiumSegments(ocean, '#9c4dcc', 3),
    ];
    // Fly camera to path when it's final
    if (is3D && ['found_path', 'done'].includes(s.phase) && s.path.length > 1) {
        const positions = s.path.map(p => Cesium.Cartesian3.fromDegrees(p.lng, p.lat, LINE_ALT));
        const bs = Cesium.BoundingSphere.fromPoints(positions);
        cesiumViewer.camera.flyToBoundingSphere(bs, {
            duration: 1.5,
            offset: new Cesium.HeadingPitchRange(0, -0.5, Math.max(bs.radius * 2.8, 800_000)),
        });
    }
}

// ── 2D / 3D toggle ────────────────────────────────────────────────────────────
document.getElementById('btn-2d').addEventListener('click', () => {
    if (!is3D) return;
    is3D = false;
    document.getElementById('gr-globe').style.display = 'none';
    document.getElementById('gr-map').style.display   = 'block';
    document.getElementById('btn-2d').classList.add('active');
    document.getElementById('btn-3d').classList.remove('active');
    map.invalidateSize();
});

document.getElementById('btn-3d').addEventListener('click', () => {
    if (is3D) return;
    is3D = true;
    _initCesiumViewer();
    document.getElementById('gr-map').style.display   = 'none';
    document.getElementById('gr-globe').style.display = 'block';
    document.getElementById('btn-3d').classList.add('active');
    document.getElementById('btn-2d').classList.remove('active');
    setTimeout(() => { if (cesiumViewer) cesiumViewer.resize(); }, 50);
});

// ── SQL ticker ────────────────────────────────────────────────────────────────
let lastSqlCount = 0;
function appendSql(s) {
    const ticker = document.getElementById('sql-ticker');
    const log    = s.sql_log || [];
    if (log.length === lastSqlCount) return;
    for (let i = lastSqlCount; i < log.length; i++) {
        const div = document.createElement('div');
        div.className = 'mb-1'; div.textContent = log[i];
        ticker.appendChild(div);
    }
    lastSqlCount = log.length;
    ticker.scrollTop = ticker.scrollHeight;
}

// ── Sidebar ───────────────────────────────────────────────────────────────────
const PHASE_COLORS = {
    idle:'secondary', seeding_nodes:'info', seeding_edges:'info',
    querying_graph:'primary', building_networkx:'primary',
    running_astar:'warning', found_path:'success', done:'success', error:'danger',
};
function updateBanner(s) {
    const badge = document.getElementById('phase-badge');
    badge.className   = `badge bg-${PHASE_COLORS[s.phase]||'secondary'} phase-badge`;
    badge.textContent = s.phase.replace(/_/g, ' ');
    document.getElementById('phase-label').textContent = s.phase_label || '—';
}
function updateSidebar(s) {
    document.getElementById('current-city').textContent =
        s.current_city ? `${s.current_city}  (${(s.distances||{})[s.current_city]??'?'} km)` : '—';
    const fl = document.getElementById('frontier-list');
    const front = s.frontier || [];
    fl.innerHTML = front.map(([name, d]) =>
        `<li class="frontier-li"><span>${esc(name)}</span><span class="text-muted">${d} km</span></li>`
    ).join('') || '<li class="text-muted" style="font-size:.73rem">—</li>';
    const vc = document.getElementById('visited-count');
    vc.textContent = (s.visited && s.visited.length)
        ? `Visited: ${s.visited.length.toLocaleString()} / ${citiesLoaded.length.toLocaleString()} cities` : '';
    if (s.path && s.path.length > 1) {
        const ferryHops = s.path.filter(p => p.ferry).length;
        const oceanHops = s.path.filter(p => p.ocean).length;
        document.getElementById('m-dist').textContent  = (s.total_distance??'—').toLocaleString();
        document.getElementById('m-hops').textContent  = s.hop_count??'—';
        document.getElementById('m-ferry').textContent = ferryHops;
        document.getElementById('m-ocean').textContent = oceanHops;
    }
    const spWrap = document.getElementById('sp-wrap');
    if (s.sqlserver_route && s.sqlserver_route.length) {
        spWrap.classList.remove('d-none');
        document.getElementById('sp-route').textContent =
            s.sqlserver_route.join(' → ') + ` [${s.sqlserver_hops} hops]`;
    }
}

// ── Main render ───────────────────────────────────────────────────────────────
function render(s) {
    updateBanner(s);
    if (s.cities && s.cities.length && !markersReady) initMarkers(s.cities);
    updateMarkers(s);
    updatePathLines(s);
    updateSidebar(s);
    appendSql(s);
    document.getElementById('btn-step').disabled = !s.waiting_for_step;
    if (['done', 'error'].includes(s.phase)) { stopPolling(); stopAuto(); }
    if (s.error) {
        document.getElementById('phase-label').innerHTML =
            `<span class="text-danger">${esc(s.error)}</span>`;
    }
}

// ── Polling ───────────────────────────────────────────────────────────────────
let pollTimer = null;
function startPolling() {
    if (pollTimer) return;
    pollTimer = setInterval(fetchState, 150);
}
function stopPolling() { clearInterval(pollTimer); pollTimer = null; }
async function fetchState() {
    try {
        const s = await (await fetch('/demos/graph_routing/state')).json();
        render(s);
        if (['done', 'error', 'idle'].includes(s.phase) && pollTimer) {
            clearInterval(pollTimer);
            pollTimer = setInterval(fetchState, 600);
        }
    } catch (_) {}
}

// ── Auto-play ─────────────────────────────────────────────────────────────────
let autoTimer = null, autoMs = 400;
function startAuto() {
    if (autoTimer) return;
    document.getElementById('btn-auto').classList.replace('btn-outline-info', 'btn-info');
    autoTimer = setInterval(async () => {
        try {
            const s = await (await fetch('/demos/graph_routing/state')).json();
            render(s);
            if (s.waiting_for_step) await fetch('/demos/graph_routing/step', {method: 'POST'});
        } catch (_) {}
    }, autoMs);
}
function stopAuto() {
    clearInterval(autoTimer); autoTimer = null;
    document.getElementById('btn-auto').classList.replace('btn-info', 'btn-outline-info');
}

// ── Helpers ───────────────────────────────────────────────────────────────────
function _clearAll() {
    landLine.setLatLngs([]); ferryLine.setLatLngs([]); oceanLine.setLatLngs([]);
    if (cesiumViewer) clearCesiumLines();
    ['m-dist','m-hops','m-ferry','m-ocean'].forEach(id =>
        document.getElementById(id).textContent = '—');
}

// ── Button handlers ───────────────────────────────────────────────────────────
document.getElementById('btn-start').addEventListener('click', async () => {
    stopPolling(); stopAuto(); lastSqlCount = 0;
    document.getElementById('sql-ticker').innerHTML = '';
    document.getElementById('sp-wrap').classList.add('d-none');
    _clearAll();
    await fetch('/demos/graph_routing/start', {
        method: 'POST', headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            start: resolveCity(document.getElementById('sel-start').value),
            end:   resolveCity(document.getElementById('sel-end').value),
        }),
    });
    startPolling(); startAuto();
});

document.getElementById('btn-step').addEventListener('click', async () => {
    await fetch('/demos/graph_routing/step', {method: 'POST'});
});

document.getElementById('btn-auto').addEventListener('click', () => {
    autoTimer ? stopAuto() : startAuto();
});

document.getElementById('btn-reset').addEventListener('click', async () => {
    stopPolling(); stopAuto(); lastSqlCount = 0;
    document.getElementById('sql-ticker').innerHTML = '';
    document.getElementById('sp-wrap').classList.add('d-none');
    _clearAll();
    for (const m of Object.values(markers))
        m.setStyle({color: COLORS.unvisited, fillColor: COLORS.unvisited, radius: 3});
    if (cesiumViewer) updateCesiumMarkers({path:[], visited:[], frontier:[], current_city: null});
    await fetch('/demos/graph_routing/reset', {method: 'POST'});
    render(await (await fetch('/demos/graph_routing/state')).json());
});

document.querySelectorAll('.speed-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        autoMs = parseInt(btn.dataset.ms, 10);
        document.querySelectorAll('.speed-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        if (autoTimer) { stopAuto(); startAuto(); }
    });
});

// ── Fast route ────────────────────────────────────────────────────────────────
async function fastRoute() {
    stopPolling(); stopAuto(); lastSqlCount = 0;
    document.getElementById('sql-ticker').innerHTML = '';
    document.getElementById('sp-wrap').classList.add('d-none');
    _clearAll();

    const start = resolveCity(document.getElementById('sel-start').value);
    const end   = resolveCity(document.getElementById('sel-end').value);
    const badge = document.getElementById('phase-badge');
    badge.className = 'badge bg-warning phase-badge'; badge.textContent = 'computing…';
    document.getElementById('phase-label').textContent = `A* route: ${start} → ${end}`;

    const t0 = performance.now();
    try {
        const data = await (await fetch('/demos/graph_routing/fast', {
            method: 'POST', headers: {'Content-Type': 'application/json'},
            body:   JSON.stringify({start, end}),
        })).json();
        const ms = (performance.now() - t0).toFixed(0);

        if (data.error) {
            badge.className = 'badge bg-danger phase-badge'; badge.textContent = 'error';
            document.getElementById('phase-label').innerHTML =
                `<span class="text-danger">${esc(data.error)}</span>`;
            return;
        }

        const {land, ferry, ocean} = _buildSegments(data.path);
        landLine.setLatLngs(land); ferryLine.setLatLngs(ferry); oceanLine.setLatLngs(ocean);

        if (data.path.length > 1 && !is3D)
            map.fitBounds(L.latLngBounds(data.path.map(p => [p.lat, p.lng])), {padding: [32, 32]});

        // Cesium path
        if (cesiumViewer) {
            updateCesiumLines({path: data.path, phase: 'done'});
            if (markersReady) {
                const pathSet = new Set(data.path.map(p => p.name));
                for (const [name, m] of Object.entries(markers)) {
                    const onPath = pathSet.has(name);
                    m.setStyle({
                        color:     onPath ? COLORS.path : COLORS.unvisited,
                        fillColor: onPath ? COLORS.path : COLORS.unvisited,
                        radius:    onPath ? 5 : 3,
                    });
                }
                updateCesiumMarkers({path: data.path, visited:[], frontier:[], current_city: null});
            }
        }

        document.getElementById('m-dist').textContent  = (data.total_distance??'—').toLocaleString();
        document.getElementById('m-hops').textContent  = data.hop_count??'—';
        document.getElementById('m-ferry').textContent = data.path.filter(p => p.ferry).length;
        document.getElementById('m-ocean').textContent = data.path.filter(p => p.ocean).length;
        badge.className = 'badge bg-success phase-badge'; badge.textContent = 'done';
        document.getElementById('phase-label').textContent =
            `⚡ ${data.hop_count} hops · ${(data.total_distance??0).toLocaleString()} km · ${ms} ms`;

        if (!cesiumViewer && markersReady) {
            const pathSet = new Set(data.path.map(p => p.name));
            for (const [name, m] of Object.entries(markers))
                m.setStyle(pathSet.has(name)
                    ? {color: COLORS.path,     fillColor: COLORS.path,     radius: 5}
                    : {color: COLORS.unvisited, fillColor: COLORS.unvisited, radius: 3});
        }
    } catch (e) {
        badge.className = 'badge bg-danger phase-badge'; badge.textContent = 'error';
        document.getElementById('phase-label').innerHTML =
            `<span class="text-danger">Network error: ${esc(e.message)}</span>`;
    }
}

document.getElementById('btn-fast').addEventListener('click', fastRoute);

// ── Init ──────────────────────────────────────────────────────────────────────
loadCitiesDatalist();
fetchState();
