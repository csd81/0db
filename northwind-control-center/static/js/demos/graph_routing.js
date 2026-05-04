'use strict';

// ── Leaflet map ──────────────────────────────────────────────────────────────
const map = L.map('map-container', {zoomControl: true}).setView([51, 15], 4);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© <a href="https://openstreetmap.org/copyright">OpenStreetMap</a> contributors',
    maxZoom: 18,
}).addTo(map);

const pathLine = L.polyline([], {color: '#0d6efd', weight: 4, opacity: 0.9}).addTo(map);

const COLORS = {
    unvisited: '#adb5bd',
    frontier:  '#0dcaf0',
    current:   '#ffc107',
    settled:   '#6c757d',
    path:      '#198754',
};

const markers    = {};  // name → L.circleMarker
let   markersReady = false;
let   citiesLoaded = [];

function esc(s) {
    return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
}
function fmt(v) { return v == null ? '—' : v; }

// ── Markers ──────────────────────────────────────────────────────────────────
function initMarkers(cities) {
    // Clear old markers
    for (const m of Object.values(markers)) map.removeLayer(m);
    Object.keys(markers).forEach(k => delete markers[k]);
    citiesLoaded = cities;
    markersReady = false;

    for (const c of cities) {
        const m = L.circleMarker([c.lat, c.lng], {
            radius:      4,
            color:       COLORS.unvisited,
            fillColor:   COLORS.unvisited,
            fillOpacity: 0.9,
            weight:      1,
        }).addTo(map);
        m.bindTooltip(`<b>${esc(c.name)}</b><br>${esc(c.country)}<br>Pop: ${c.population.toLocaleString()}`, {sticky: true});
        markers[c.name] = m;
    }
    markersReady = true;

    // Populate searchable datalist (shared by both inputs)
    const allNames = cities.map(c => c.name).sort();
    const dl = document.getElementById('cities-datalist');
    dl.innerHTML = allNames.map(n => `<option value="${esc(n)}"></option>`).join('');
}

function updateMarkers(s) {
    if (!markersReady) return;
    const pathSet    = new Set((s.path || []).map(p => p.name));
    const visitedSet = new Set(s.visited || []);
    const frontSet   = new Set((s.frontier || []).map(f => f[0]));
    for (const [name, m] of Object.entries(markers)) {
        let color = COLORS.unvisited;
        if (pathSet.has(name))              color = COLORS.path;
        else if (name === s.current_city)   color = COLORS.current;
        else if (visitedSet.has(name))      color = COLORS.settled;
        else if (frontSet.has(name))        color = COLORS.frontier;
        m.setStyle({color, fillColor: color});
    }
}

function updatePathLine(s) {
    if (!s.path || s.path.length < 2) {
        pathLine.setLatLngs([]);
        return;
    }
    pathLine.setLatLngs(s.path.map(p => [p.lat, p.lng]));
    if (s.phase === 'found_path' || s.phase === 'done') {
        map.fitBounds(pathLine.getBounds(), {padding: [30, 30]});
    }
}

// ── SQL ticker ───────────────────────────────────────────────────────────────
let lastSqlCount = 0;

function appendSql(s) {
    const ticker = document.getElementById('sql-ticker');
    const log    = s.sql_log || [];
    if (log.length === lastSqlCount) return;
    for (let i = lastSqlCount; i < log.length; i++) {
        const line = document.createElement('div');
        line.className = 'mb-1';
        line.textContent = log[i];
        ticker.appendChild(line);
    }
    lastSqlCount = log.length;
    ticker.scrollTop = ticker.scrollHeight;
}

// ── Sidebar ──────────────────────────────────────────────────────────────────
const PHASE_COLORS = {
    idle:             'secondary',
    seeding_nodes:    'info',
    seeding_edges:    'info',
    querying_graph:   'primary',
    building_networkx:'primary',
    running_astar:    'warning',
    found_path:       'success',
    done:             'success',
    error:            'danger',
};

function updateBanner(s) {
    const badge = document.getElementById('phase-badge');
    const color  = PHASE_COLORS[s.phase] || 'secondary';
    badge.className = `badge bg-${color} phase-badge`;
    badge.textContent = s.phase.replace(/_/g, ' ');
    document.getElementById('phase-label').textContent = s.phase_label || '—';
}

function updateSidebar(s) {
    document.getElementById('current-city').textContent =
        s.current_city ? `${s.current_city}  (${(s.distances||{})[s.current_city] ?? '?'} km)` : '—';

    const fl = document.getElementById('frontier-list');
    const front = s.frontier || [];
    fl.innerHTML = front.map(([name, d]) =>
        `<li class="d-flex justify-content-between">
           <span>${esc(name)}</span>
           <span class="text-muted ms-2">${d} km</span>
         </li>`
    ).join('') || '<li class="text-muted">—</li>';

    const vc = document.getElementById('visited-count');
    if (s.visited && s.visited.length > 0) {
        const total = citiesLoaded.length || '?';
        vc.textContent = `Visited: ${s.visited.length} / ${total} cities`;
    } else {
        vc.textContent = '';
    }
}

function updateRouteBar(s) {
    const bar = document.getElementById('route-bar');
    if (!s.sqlserver_route?.length && !s.path?.length) {
        bar.classList.add('d-none');
        return;
    }
    bar.classList.remove('d-none');

    const spEl = document.getElementById('sp-route');
    if (s.sqlserver_route?.length) {
        spEl.textContent = s.sqlserver_route.join(' → ')
            + (s.sqlserver_hops ? ` [${s.sqlserver_hops} hops]` : '');
    } else {
        spEl.textContent = 'not available (SQL Server < 2019)';
    }

    const aEl = document.getElementById('astar-route');
    if (s.path?.length) {
        aEl.textContent = s.path.map(p => p.name).join(' → ')
            + (s.total_distance ? ` — ${s.total_distance} km` : '');
    } else {
        aEl.textContent = '…';
    }
}

// ── Main render ──────────────────────────────────────────────────────────────
function render(s) {
    updateBanner(s);
    if (s.cities?.length && !markersReady) initMarkers(s.cities);
    updateMarkers(s);
    updatePathLine(s);
    updateSidebar(s);
    appendSql(s);
    updateRouteBar(s);

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
let pollTimer = null;

function startPolling() {
    if (pollTimer) return;
    pollTimer = setInterval(fetchState, 300);
}

function stopPolling() {
    clearInterval(pollTimer);
    pollTimer = null;
}

async function fetchState() {
    try {
        const r = await fetch('/demos/graph_routing/state');
        render(await r.json());
    } catch (e) { /* network transient */ }
}

// ── Auto-play ────────────────────────────────────────────────────────────────
let autoTimer  = null;
let autoMs     = 400;

function startAuto() {
    if (autoTimer) return;
    document.getElementById('btn-auto').classList.replace('btn-outline-info', 'btn-info');
    autoTimer = setInterval(async () => {
        try {
            const r  = await fetch('/demos/graph_routing/state');
            const s  = await r.json();
            render(s);
            if (s.waiting_for_step) {
                await fetch('/demos/graph_routing/step', {method: 'POST'});
            }
        } catch (e) { /* transient */ }
    }, autoMs);
}

function stopAuto() {
    clearInterval(autoTimer);
    autoTimer = null;
    document.getElementById('btn-auto').classList.replace('btn-info', 'btn-outline-info');
}

// ── Button handlers ──────────────────────────────────────────────────────────
document.getElementById('btn-start').addEventListener('click', async () => {
    stopPolling();
    stopAuto();
    lastSqlCount = 0;
    document.getElementById('sql-ticker').innerHTML = '';
    pathLine.setLatLngs([]);
    document.getElementById('route-bar').classList.add('d-none');

    const start = document.getElementById('sel-start').value;
    const end   = document.getElementById('sel-end').value;
    await fetch('/demos/graph_routing/start', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({start, end}),
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
    pathLine.setLatLngs([]);
    document.getElementById('route-bar').classList.add('d-none');
    // Clear markers state (keep them visible but reset colors)
    for (const m of Object.values(markers)) {
        m.setStyle({color: COLORS.unvisited, fillColor: COLORS.unvisited});
    }

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

// ── Init ─────────────────────────────────────────────────────────────────────
fetchState();
