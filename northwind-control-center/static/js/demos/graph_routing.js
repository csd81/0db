'use strict';

// ── Leaflet map ──────────────────────────────────────────────────────────────
const map = L.map('gr-map', {zoomControl: true}).setView([35, 40], 3);
L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
    attribution: '&copy; <a href="https://openstreetmap.org">OpenStreetMap</a> &copy; <a href="https://carto.com">CARTO</a>',
    subdomains: 'abcd',
    maxZoom: 19,
}).addTo(map);

// Three visual layers — land (solid cyan), ferry (orange dash), ocean (purple dot-dash)
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

const markers      = {};   // name → L.circleMarker
let   markersReady = false;
let   citiesLoaded = [];
const cityNameMap  = {};   // "Name (CC)" → raw name  (for datalist resolution)

function esc(s) {
    return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
}

// ── Datalist — loaded on init from /cities ───────────────────────────────────
async function loadCitiesDatalist() {
    try {
        const r  = await fetch('/demos/graph_routing/cities');
        const cs = await r.json();
        const dl = document.getElementById('cities-dl');
        const frags = [];
        for (const c of cs) {
            const label = `${c.name} (${c.country})`;
            cityNameMap[label]  = c.name;
            cityNameMap[c.name] = c.name;   // raw name also resolves
            frags.push(`<option value="${esc(label)}">`);
        }
        dl.innerHTML = frags.join('');
    } catch (_) { /* optional — raw names still work */ }
}

function resolveCity(inputVal) {
    const v = inputVal.trim();
    return cityNameMap[v] || v;
}

// ── Markers ──────────────────────────────────────────────────────────────────
function initMarkers(cities) {
    for (const m of Object.values(markers)) map.removeLayer(m);
    Object.keys(markers).forEach(k => delete markers[k]);
    citiesLoaded   = cities;
    markersReady   = false;

    for (const c of cities) {
        const m = L.circleMarker([c.lat, c.lng], {
            radius:      3,
            color:       COLORS.unvisited,
            fillColor:   COLORS.unvisited,
            fillOpacity: 0.7,
            weight:      1,
        }).addTo(map);
        m.bindTooltip(
            `<b>${esc(c.name)}</b> (${esc(c.country)})<br>Pop: ${c.population.toLocaleString()}`,
            {sticky: true}
        );
        markers[c.name] = m;
    }
    markersReady = true;

    // Sync datalist — city records from state have lat/lng; upsert into cityNameMap
    const dl = document.getElementById('cities-dl');
    if (!dl.childElementCount) {
        const frags = [];
        const allNames = cities.map(c => c.name).sort();
        for (const n of allNames) {
            frags.push(`<option value="${esc(n)}">`);
            cityNameMap[n] = n;
        }
        dl.innerHTML = frags.join('');
    }
}

function updateMarkers(s) {
    if (!markersReady) return;
    const pathSet  = new Set((s.path || []).map(p => p.name));
    const visited  = new Set(s.visited || []);
    const frontier = new Set((s.frontier || []).map(f => f[0]));
    for (const [name, m] of Object.entries(markers)) {
        let color = COLORS.unvisited;
        let r     = 3;
        if (pathSet.has(name))            { color = COLORS.path;     r = 5; }
        else if (name === s.current_city) { color = COLORS.current;  r = 6; }
        else if (visited.has(name))       { color = COLORS.settled; }
        else if (frontier.has(name))      { color = COLORS.frontier; r = 4; }
        m.setStyle({color, fillColor: color, radius: r});
    }
}

// ── Path line rendering ───────────────────────────────────────────────────────
function _buildSegments(path) {
    // Returns {land: [[latlng,...]], ferry: [[latlng,...]], ocean: [[latlng,...]]}
    // Each inner array is a continuous segment of the same crossing type.
    const land = [], ferry = [], ocean = [];
    if (!path || path.length < 2) return {land, ferry, ocean};

    let curType = 0;  // 0=land 1=ferry 2=ocean
    let curPts  = [[path[0].lat, path[0].lng]];

    const flush = (nextLL) => {
        if (nextLL) curPts.push(nextLL);  // include transition point
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
            flush(ll);          // include bridge point in the closing segment
            curType = type;
            curPts  = [curPts[curPts.length - 1], ll];  // new segment starts at bridge
        }
    }
    flush(null);
    return {land, ferry, ocean};
}

function updatePathLines(s) {
    if (!s.path || s.path.length < 2) {
        landLine.setLatLngs([]);
        ferryLine.setLatLngs([]);
        oceanLine.setLatLngs([]);
        return;
    }

    const {land, ferry, ocean} = _buildSegments(s.path);
    landLine.setLatLngs(land);
    ferryLine.setLatLngs(ferry);
    oceanLine.setLatLngs(ocean);

    if (['found_path', 'done'].includes(s.phase) && s.path.length > 1) {
        const allCoords = s.path.map(p => [p.lat, p.lng]);
        map.fitBounds(L.latLngBounds(allCoords), {padding: [32, 32]});
    }
}

// ── SQL ticker ───────────────────────────────────────────────────────────────
let lastSqlCount = 0;

function appendSql(s) {
    const ticker = document.getElementById('sql-ticker');
    const log    = s.sql_log || [];
    if (log.length === lastSqlCount) return;
    for (let i = lastSqlCount; i < log.length; i++) {
        const div = document.createElement('div');
        div.className   = 'mb-1';
        div.textContent = log[i];
        ticker.appendChild(div);
    }
    lastSqlCount = log.length;
    ticker.scrollTop = ticker.scrollHeight;
}

// ── Sidebar updates ───────────────────────────────────────────────────────────
const PHASE_COLORS = {
    idle:              'secondary',
    seeding_nodes:     'info',
    seeding_edges:     'info',
    querying_graph:    'primary',
    building_networkx: 'primary',
    running_astar:     'warning',
    found_path:        'success',
    done:              'success',
    error:             'danger',
};

function updateBanner(s) {
    const badge = document.getElementById('phase-badge');
    const col   = PHASE_COLORS[s.phase] || 'secondary';
    badge.className   = `badge bg-${col} phase-badge`;
    badge.textContent = s.phase.replace(/_/g, ' ');
    document.getElementById('phase-label').textContent = s.phase_label || '—';
}

function updateSidebar(s) {
    // Expanding city
    document.getElementById('current-city').textContent =
        s.current_city
            ? `${s.current_city}  (${(s.distances || {})[s.current_city] ?? '?'} km)`
            : '—';

    // Frontier list
    const fl    = document.getElementById('frontier-list');
    const front = s.frontier || [];
    fl.innerHTML = front.map(([name, d]) =>
        `<li class="frontier-li">
           <span>${esc(name)}</span>
           <span class="text-muted">${d} km</span>
         </li>`
    ).join('') || '<li class="text-muted" style="font-size:.73rem">—</li>';

    // Visited count
    const vc = document.getElementById('visited-count');
    vc.textContent = (s.visited && s.visited.length)
        ? `Visited: ${s.visited.length.toLocaleString()} / ${citiesLoaded.length.toLocaleString()} cities`
        : '';

    // Metrics (only when path is available)
    if (s.path && s.path.length > 1) {
        const ferryHops = s.path.filter(p => p.ferry).length;
        const oceanHops = s.path.filter(p => p.ocean).length;
        document.getElementById('m-dist').textContent  = (s.total_distance ?? '—').toLocaleString();
        document.getElementById('m-hops').textContent  = s.hop_count ?? '—';
        document.getElementById('m-ferry').textContent = ferryHops;
        document.getElementById('m-ocean').textContent = oceanHops;
    }

    // SQL Server shortest-path result
    const spWrap = document.getElementById('sp-wrap');
    if (s.sqlserver_route && s.sqlserver_route.length) {
        spWrap.classList.remove('d-none');
        document.getElementById('sp-route').textContent =
            s.sqlserver_route.join(' → ') + ` [${s.sqlserver_hops} hops]`;
    }
}

// ── Main render ──────────────────────────────────────────────────────────────
function render(s) {
    updateBanner(s);
    if (s.cities && s.cities.length && !markersReady) initMarkers(s.cities);
    updateMarkers(s);
    updatePathLines(s);
    updateSidebar(s);
    appendSql(s);

    document.getElementById('btn-step').disabled = !s.waiting_for_step;

    if (['done', 'error'].includes(s.phase)) {
        stopPolling();
        stopAuto();
    }
    if (s.error) {
        document.getElementById('phase-label').innerHTML =
            `<span class="text-danger">${esc(s.error)}</span>`;
    }
}

// ── Polling ──────────────────────────────────────────────────────────────────
let pollTimer  = null;
const POLL_MS_ACTIVE = 150;   // during A*
const POLL_MS_IDLE   = 600;

function startPolling() {
    if (pollTimer) return;
    pollTimer = setInterval(fetchState, POLL_MS_ACTIVE);
}

function stopPolling() {
    clearInterval(pollTimer);
    pollTimer = null;
}

async function fetchState() {
    try {
        const r = await fetch('/demos/graph_routing/state');
        const s = await r.json();
        render(s);
        // Slow down poll once done
        if (['done', 'error', 'idle'].includes(s.phase) && pollTimer) {
            clearInterval(pollTimer);
            pollTimer = setInterval(fetchState, POLL_MS_IDLE);
        }
    } catch (_) { /* transient */ }
}

// ── Auto-play ─────────────────────────────────────────────────────────────────
let autoTimer = null;
let autoMs    = 400;

function startAuto() {
    if (autoTimer) return;
    document.getElementById('btn-auto').classList.replace('btn-outline-info', 'btn-info');
    autoTimer = setInterval(async () => {
        try {
            const r = await fetch('/demos/graph_routing/state');
            const s = await r.json();
            render(s);
            if (s.waiting_for_step) {
                await fetch('/demos/graph_routing/step', {method: 'POST'});
            }
        } catch (_) { /* transient */ }
    }, autoMs);
}

function stopAuto() {
    clearInterval(autoTimer);
    autoTimer = null;
    const btn = document.getElementById('btn-auto');
    btn.classList.replace('btn-info', 'btn-outline-info');
}

// ── Button handlers ───────────────────────────────────────────────────────────
document.getElementById('btn-start').addEventListener('click', async () => {
    stopPolling();
    stopAuto();
    lastSqlCount = 0;
    document.getElementById('sql-ticker').innerHTML = '';
    document.getElementById('sp-wrap').classList.add('d-none');
    landLine.setLatLngs([]);
    ferryLine.setLatLngs([]);
    oceanLine.setLatLngs([]);
    ['m-dist','m-hops','m-ferry','m-ocean'].forEach(id =>
        document.getElementById(id).textContent = '—'
    );

    const start = resolveCity(document.getElementById('sel-start').value);
    const end   = resolveCity(document.getElementById('sel-end').value);
    await fetch('/demos/graph_routing/start', {
        method:  'POST',
        headers: {'Content-Type': 'application/json'},
        body:    JSON.stringify({start, end}),
    });
    startPolling();
    startAuto();
});

document.getElementById('btn-step').addEventListener('click', async () => {
    await fetch('/demos/graph_routing/step', {method: 'POST'});
});

document.getElementById('btn-auto').addEventListener('click', () => {
    autoTimer ? stopAuto() : startAuto();
});

document.getElementById('btn-reset').addEventListener('click', async () => {
    stopPolling();
    stopAuto();
    lastSqlCount = 0;
    document.getElementById('sql-ticker').innerHTML = '';
    document.getElementById('sp-wrap').classList.add('d-none');
    landLine.setLatLngs([]);
    ferryLine.setLatLngs([]);
    oceanLine.setLatLngs([]);
    ['m-dist','m-hops','m-ferry','m-ocean'].forEach(id =>
        document.getElementById(id).textContent = '—'
    );
    for (const m of Object.values(markers))
        m.setStyle({color: COLORS.unvisited, fillColor: COLORS.unvisited, radius: 3});

    await fetch('/demos/graph_routing/reset', {method: 'POST'});
    const r = await fetch('/demos/graph_routing/state');
    render(await r.json());
});

document.querySelectorAll('.speed-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        autoMs = parseInt(btn.dataset.ms, 10);
        document.querySelectorAll('.speed-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        if (autoTimer) { stopAuto(); startAuto(); }
    });
});

// ── Fast route — single A* call, no step-by-step state machine ───────────────
async function fastRoute() {
    stopPolling();
    stopAuto();
    lastSqlCount = 0;
    document.getElementById('sql-ticker').innerHTML = '';
    document.getElementById('sp-wrap').classList.add('d-none');
    landLine.setLatLngs([]);
    ferryLine.setLatLngs([]);
    oceanLine.setLatLngs([]);
    ['m-dist','m-hops','m-ferry','m-ocean'].forEach(id =>
        document.getElementById(id).textContent = '—'
    );

    const start = resolveCity(document.getElementById('sel-start').value);
    const end   = resolveCity(document.getElementById('sel-end').value);

    const badge = document.getElementById('phase-badge');
    badge.className   = 'badge bg-warning phase-badge';
    badge.textContent = 'computing…';
    document.getElementById('phase-label').textContent = `A* route: ${start} → ${end}`;

    const t0 = performance.now();
    try {
        const r    = await fetch('/demos/graph_routing/fast', {
            method:  'POST',
            headers: {'Content-Type': 'application/json'},
            body:    JSON.stringify({start, end}),
        });
        const data = await r.json();
        const ms   = (performance.now() - t0).toFixed(0);

        if (data.error) {
            badge.className   = 'badge bg-danger phase-badge';
            badge.textContent = 'error';
            document.getElementById('phase-label').innerHTML =
                `<span class="text-danger">${esc(data.error)}</span>`;
            return;
        }

        const {land, ferry, ocean} = _buildSegments(data.path);
        landLine.setLatLngs(land);
        ferryLine.setLatLngs(ferry);
        oceanLine.setLatLngs(ocean);

        if (data.path.length > 1) {
            map.fitBounds(L.latLngBounds(data.path.map(p => [p.lat, p.lng])), {padding: [32, 32]});
        }

        const ferryHops = data.path.filter(p => p.ferry).length;
        const oceanHops = data.path.filter(p => p.ocean).length;
        document.getElementById('m-dist').textContent  = (data.total_distance ?? '—').toLocaleString();
        document.getElementById('m-hops').textContent  = data.hop_count ?? '—';
        document.getElementById('m-ferry').textContent = ferryHops;
        document.getElementById('m-ocean').textContent = oceanHops;

        badge.className   = 'badge bg-success phase-badge';
        badge.textContent = 'done';
        document.getElementById('phase-label').textContent =
            `⚡ ${data.hop_count} hops · ${(data.total_distance ?? 0).toLocaleString()} km · ${ms} ms`;

        if (markersReady) {
            const pathSet = new Set(data.path.map(p => p.name));
            for (const [name, m] of Object.entries(markers)) {
                if (pathSet.has(name)) {
                    m.setStyle({color: COLORS.path, fillColor: COLORS.path, radius: 5});
                } else {
                    m.setStyle({color: COLORS.unvisited, fillColor: COLORS.unvisited, radius: 3});
                }
            }
        }
    } catch (e) {
        badge.className   = 'badge bg-danger phase-badge';
        badge.textContent = 'error';
        document.getElementById('phase-label').innerHTML =
            `<span class="text-danger">Network error: ${esc(e.message)}</span>`;
    }
}

document.getElementById('btn-fast').addEventListener('click', fastRoute);

// ── Init ─────────────────────────────────────────────────────────────────────
loadCitiesDatalist();
fetchState();
