'use strict';

// ── CesiumJS globe ────────────────────────────────────────────────────────────
const viewer = new Cesium.Viewer('gi-map', {
    animation:            false,
    baseLayerPicker:      false,
    fullscreenButton:     false,
    geocoder:             false,
    homeButton:           false,
    infoBox:              false,
    sceneModePicker:      false,
    selectionIndicator:   false,
    timeline:             false,
    navigationHelpButton: false,
    imageryProvider:      false,
    terrainProvider:      new Cesium.EllipsoidTerrainProvider(),
});

// CARTO tile base — respects light/dark theme
const GI_TILE_DARK  = 'https://a.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}.png';
const GI_TILE_LIGHT = 'https://a.basemaps.cartocdn.com/light_all/{z}/{x}/{y}.png';

function giSetTiles(theme) {
    viewer.imageryLayers.removeAll();
    viewer.imageryLayers.addImageryProvider(new Cesium.UrlTemplateImageryProvider({
        url:          theme === 'light' ? GI_TILE_LIGHT : GI_TILE_DARK,
        tilingScheme: new Cesium.WebMercatorTilingScheme(),
        credit:       'CARTO · OpenStreetMap',
        maximumLevel: 19,
    }));
    viewer.scene.globe.baseColor       = Cesium.Color.fromCssColorString(theme === 'light' ? '#d0d8e4' : '#06080c');
    viewer.scene.backgroundColor       = theme === 'light'
        ? new Cesium.Color(0.9, 0.93, 0.97, 1.0)
        : new Cesium.Color(0.02, 0.03, 0.05, 1.0);
}

const _giInitTheme = document.documentElement.getAttribute('data-bs-theme') || 'dark';
giSetTiles(_giInitTheme);

document.addEventListener('themeChanged', function(e) { giSetTiles(e.detail); });

// Globe appearance
viewer.scene.globe.enableLighting         = true;
viewer.scene.globe.showGroundAtmosphere   = false;
viewer.scene.fog.enabled                  = false;
viewer.scene.skyAtmosphere.show           = false;

try { viewer.cesiumWidget.creditContainer.style.display = 'none'; } catch (_) {}

// Initial camera — looking at globe from space
viewer.camera.setView({
    destination: Cesium.Cartesian3.fromDegrees(10.0, 25.0, 22_000_000),
});

// ── Entity groups (one array per toggleable layer) ────────────────────────────
const entityGroups = {
    cloud_dc:      [],
    ixp:           [],
    cable_landing: [],
    starlink_gw:   [],
    openai_dc:     [],
    aws_ai:        [],
    meta_ai:       [],
    chokepoint:    [],
    edges:         [],
    path_fiber:    [],
    path_starlink: [],
};

// Satellites use a GPU-batch PointPrimitiveCollection for 10k+ markers
const satCollection = viewer.scene.primitives.add(new Cesium.PointPrimitiveCollection());
satCollection.show = false;

// ── Styling tables ────────────────────────────────────────────────────────────
const TYPE_PIXEL_SIZE = {
    cloud_dc: 7, ixp: 5, cable_landing: 4, starlink_gw: 6,
    openai_dc: 11, aws_ai: 11, meta_ai: 9, chokepoint: 7,
};
const TYPE_COLOR_HEX = {
    cloud_dc: '#f97316', ixp: '#a855f7', cable_landing: '#22d3ee',
    starlink_gw: '#4ade80', openai_dc: '#06b6d4', aws_ai: '#f59e0b',
    meta_ai: '#818cf8', chokepoint: '#ef4444',
};
const PROVIDER_COLOR = {
    AWS: '#f97316', GCP: '#facc15', Azure: '#60a5fa',
    Oracle: '#e05c2a', OpenAI: '#06b6d4',
};
const EDGE_STYLE = {
    fiber:          { hex: '#1e3a4f', alpha: 0.5,  width: 1   },
    submarine:      { hex: '#0e4a6a', alpha: 0.55, width: 1.2 },
    starlink_laser: { hex: '#134d25', alpha: 0.35, width: 0.8 },
    dark_fiber:     { hex: '#1a1a6f', alpha: 0.7,  width: 1.5 },
};

// ── State ─────────────────────────────────────────────────────────────────────
let allNodes      = {};
let cloudNodes    = [];
let allEdgesData  = [];
let disabledEdge  = null;
let animTimers    = [];
let animPackets   = [];
let _animGen      = 0;        // generation counter — incremented on clearAnimation
let ftsMinute     = null;     // null = off; 0–1439 = active minute of day
let ftsPlayTimer  = null;
let hasDynamic    = false;
let satToggleOn   = false;

// ── Hover tooltip ─────────────────────────────────────────────────────────────
const tooltip    = document.getElementById('cesium-tooltip');
const pickHandler = new Cesium.ScreenSpaceEventHandler(viewer.scene.canvas);
pickHandler.setInputAction(mv => {
    const picked = viewer.scene.pick(mv.endPosition);
    if (Cesium.defined(picked) && picked.id?._gi_node) {
        const n = picked.id._gi_node;
        tooltip.style.display = 'block';
        tooltip.style.left    = (mv.endPosition.x + 16) + 'px';
        tooltip.style.top     = (mv.endPosition.y + 12) + 'px';
        tooltip.innerHTML     = `<b>${n.label}</b><br><span style="color:#9ca3af">${n.provider} · ${n.type.replace(/_/g, ' ')}</span>`;
    } else {
        tooltip.style.display = 'none';
    }
}, Cesium.ScreenSpaceEventType.MOUSE_MOVE);

// ── Logging ───────────────────────────────────────────────────────────────────
function log(msg) {
    const el = document.getElementById('gi-log');
    const ts = new Date().toTimeString().slice(0, 8);
    el.textContent = `[${ts}] ${msg}\n` + el.textContent;
}

// ── FTS helpers ───────────────────────────────────────────────────────────────
function minuteToHHMM(m) {
    return `${String(Math.floor(m / 60)).padStart(2, '0')}:${String(m % 60).padStart(2, '0')}`;
}

function trafficLoad(utcMinute, lng) {
    const utcH   = Math.floor(utcMinute / 60);
    const localH = ((utcH + Math.round(lng / 15)) % 24 + 24) % 24;
    if (localH >= 9  && localH < 17) return 1.0;
    if (localH >= 17 && localH < 22) return 0.5;
    if (localH >= 7  && localH < 9)  return 0.5;
    return 0.1;
}
function loadColor(l) { return l >= 0.9 ? '#ef4444' : l >= 0.4 ? '#f59e0b' : '#4ade80'; }
function loadLabel(l) { return l >= 0.9 ? 'PEAK'    : l >= 0.4 ? 'SHOULDER' : 'OFF-PEAK'; }

const FTS_REGIONS = [
    { label: 'Americas', lng: -90 },
    { label: 'Europe',   lng:  15 },
    { label: 'Asia-Pac', lng: 115 },
];

function updateFtsDisplay(m) {
    const display = document.getElementById('hour-display');
    const loads   = document.getElementById('fts-loads');
    const badge   = document.getElementById('dynamic-badge');

    if (m === null) {
        display.textContent = '—';
        loads.innerHTML = '<span style="font-size:.6rem;color:#4b5563">Simulation off</span>';
        badge.classList.add('d-none');
        viewer.clock.currentTime = Cesium.JulianDate.fromDate(new Date());
        return;
    }

    document.getElementById('hour-slider').value = m;
    display.textContent = minuteToHHMM(m) + ' UTC';

    // Sync Cesium day/night terminator to simulation time
    const simDate = new Date(Date.UTC(2026, 0, 1, Math.floor(m / 60), m % 60, 0));
    viewer.clock.currentTime = Cesium.JulianDate.fromDate(simDate);

    loads.innerHTML = FTS_REGIONS.map(r => {
        const l = trafficLoad(m, r.lng);
        return `<span style="font-size:.58rem;padding:1px 5px;border-radius:3px;border:1px solid ${loadColor(l)}44;color:${loadColor(l)};background:${loadColor(l)}18;line-height:1.5">${r.label} <b>${loadLabel(l)}</b></span>`;
    }).join('');

    badge.classList.toggle('d-none', !hasDynamic);
}

// ── Draw infrastructure nodes ─────────────────────────────────────────────────
function drawNodes(nodes) {
    allNodes = {};
    for (const n of nodes) allNodes[n.key] = n;

    for (const n of nodes) {
        if (!entityGroups[n.type]) continue;

        let hex = TYPE_COLOR_HEX[n.type] || '#22d3ee';
        if (n.type === 'cloud_dc' && PROVIDER_COLOR[n.provider]) hex = PROVIDER_COLOR[n.provider];
        const color = Cesium.Color.fromCssColorString(hex);

        const entity = viewer.entities.add({
            position: Cesium.Cartesian3.fromDegrees(n.lng, n.lat, 5_000),  // 5 km above surface avoids z-fighting
            point: {
                pixelSize:                TYPE_PIXEL_SIZE[n.type] || 5,
                color,
                outlineColor:             color.withAlpha(0.35),
                outlineWidth:             1,
                disableDepthTestDistance: 5e6,  // depth test re-engages at globe-view distance (>5 000 km)
            },
        });
        entity._gi_node = n;
        entityGroups[n.type].push(entity);
    }
}

// ── Draw backbone edges ───────────────────────────────────────────────────────
function drawEdges(edges) {
    for (const e of edges) {
        const s = EDGE_STYLE[e.edge_type] || EDGE_STYLE.fiber;
        const entity = viewer.entities.add({
            polyline: {
                positions: Cesium.Cartesian3.fromDegreesArray(
                    [e.src_lng, e.src_lat, e.dst_lng, e.dst_lat]
                ),
                width:    s.width,
                material: Cesium.Color.fromCssColorString(s.hex).withAlpha(s.alpha),
                arcType:  Cesium.ArcType.GEODESIC,
            },
        });
        entityGroups.edges.push(entity);
    }
}

// ── Satellite markers at 550 km altitude ──────────────────────────────────────
function drawSatellites(sats) {
    satCollection.removeAll();
    const color = Cesium.Color.fromCssColorString('#22c55e').withAlpha(0.72);
    for (const s of sats) {
        satCollection.add({
            position:  Cesium.Cartesian3.fromDegrees(s.lng, s.lat, 550_000),
            color,
            pixelSize: 2,
        });
    }
}

// ── Follow the Sun ────────────────────────────────────────────────────────────
let _topoTimer = null;
function scheduleTopologyFetch(minute) {
    clearTimeout(_topoTimer);
    _topoTimer = setTimeout(() => fetchTopology(minute), 250);
}

async function fetchTopology(minute) {
    if (!satToggleOn) return;
    try {
        const r    = await fetch(`/demos/global-infra/topology?t=${minute}`);
        const data = await r.json();
        if (data.has_data) {
            hasDynamic = true;
            drawSatellites(data.sats);
            updateFtsDisplay(ftsMinute);
            log(`Topology loaded: ${data.sats.length} satellites at ${minuteToHHMM(minute)}`);
        } else {
            hasDynamic = false;
            satCollection.removeAll();
            updateFtsDisplay(ftsMinute);
        }
    } catch (_) {
        hasDynamic = false;
    }
}

function stopFtsAnimate() {
    if (ftsPlayTimer) { clearInterval(ftsPlayTimer); ftsPlayTimer = null; }
    const btn = document.getElementById('btn-fts-play');
    btn.textContent = '▶ Animate 24h';
    btn.style.color = '#38bdf8';
}

function wireFts() {
    document.getElementById('hour-slider').addEventListener('input', e => {
        ftsMinute = parseInt(e.target.value, 10);
        updateFtsDisplay(ftsMinute);
        scheduleTopologyFetch(ftsMinute);
    });

    document.getElementById('btn-fts-now').addEventListener('click', () => {
        stopFtsAnimate();
        const now = new Date();
        ftsMinute = now.getUTCHours() * 60 + now.getUTCMinutes();
        updateFtsDisplay(ftsMinute);
        fetchTopology(ftsMinute);
        doRoute();
    });

    document.getElementById('btn-fts-off').addEventListener('click', () => {
        stopFtsAnimate();
        ftsMinute  = null;
        hasDynamic = false;
        satCollection.removeAll();
        updateFtsDisplay(null);
        doRoute();
    });

    document.getElementById('btn-fts-play').addEventListener('click', () => {
        if (ftsPlayTimer) { stopFtsAnimate(); return; }
        if (ftsMinute === null) ftsMinute = 0;
        const btn = document.getElementById('btn-fts-play');
        btn.textContent = '⏹ Stop';
        btn.style.color = '#ef4444';
        // Step 1 minute every 400 ms → full 24 h in ~9.6 minutes
        ftsPlayTimer = setInterval(() => {
            ftsMinute = (ftsMinute + 1) % 1440;
            updateFtsDisplay(ftsMinute);
            scheduleTopologyFetch(ftsMinute);
            doRoute();
        }, 400);
    });

    document.getElementById('tog-sats').addEventListener('change', e => {
        satToggleOn = e.target.checked;
        satCollection.show = satToggleOn;
        if (satToggleOn) fetchTopology(ftsMinute ?? 0);
        if (!satToggleOn) satCollection.removeAll();
    });

    updateFtsDisplay(null);
}

// ── Layer toggle wiring ───────────────────────────────────────────────────────
function wireToggles() {
    const tog = (id, type) => {
        document.getElementById(id).addEventListener('change', e => {
            for (const ent of entityGroups[type]) ent.show = e.target.checked;
        });
    };
    tog('tog-cloud',  'cloud_dc');
    tog('tog-ixp',    'ixp');
    tog('tog-cable',  'cable_landing');
    tog('tog-gw',     'starlink_gw');
    tog('tog-openai', 'openai_dc');
    tog('tog-awsai',  'aws_ai');
    tog('tog-metaai', 'meta_ai');
    tog('tog-chk',    'chokepoint');
    tog('tog-edges',  'edges');
}

// ── Path drawing helpers ──────────────────────────────────────────────────────
// Returns altitude in metres for a path coordinate key
function nodeAltM(key) {
    if (!key) return 0;
    return (key.startsWith('sat-') || key.startsWith('dynsat-')) ? 550_000 : 0;
}

function clearPaths() {
    for (const e of entityGroups.path_fiber)    viewer.entities.remove(e);
    for (const e of entityGroups.path_starlink) viewer.entities.remove(e);
    entityGroups.path_fiber    = [];
    entityGroups.path_starlink = [];
    clearAnimation();
}

function _addPointMarker(group, lng, lat, alt, hex) {
    const e = viewer.entities.add({
        position: Cesium.Cartesian3.fromDegrees(lng, lat, Math.max(alt, 5_000)),
        point: {
            pixelSize:                6,
            color:                    Cesium.Color.fromCssColorString(hex),
            disableDepthTestDistance: 5e6,
        },
    });
    entityGroups[group].push(e);
    return e;
}

function drawFiberPath(coords) {
    if (!coords || coords.length < 2) return;

    // Flat array [lng, lat, lng, lat, ...] for fromDegreesArray
    const arr = coords.flatMap(c => [c.lng, c.lat]);
    const line = viewer.entities.add({
        polyline: {
            positions: Cesium.Cartesian3.fromDegreesArray(arr),
            width:     2.5,
            material:  Cesium.Color.fromCssColorString('#22d3ee').withAlpha(0.9),
            arcType:   Cesium.ArcType.GEODESIC,   // Cesium interpolates great-circle natively
            depthFailMaterial: Cesium.Color.fromCssColorString('#22d3ee').withAlpha(0.25),
        },
    });
    entityGroups.path_fiber.push(line);

    // Endpoint markers only
    _addPointMarker('path_fiber', coords[0].lng,                   coords[0].lat,                   0, '#22d3ee');
    _addPointMarker('path_fiber', coords[coords.length - 1].lng,   coords[coords.length - 1].lat,   0, '#22d3ee');
}

function drawStarlinkPath(coords) {
    if (!coords || coords.length < 2) return;

    // Each coord gets correct altitude — ground nodes at 0m, satellite nodes at 550 km
    const positions = coords.map(c =>
        Cesium.Cartesian3.fromDegrees(c.lng, c.lat, nodeAltM(c.key))
    );

    // arcType NONE = straight 3D lines in Cartesian space
    // Correct for ISL lasers (through vacuum, not along Earth surface)
    const line = viewer.entities.add({
        polyline: {
            positions,
            width:     2,
            material:  Cesium.Color.fromCssColorString('#4ade80').withAlpha(0.85),
            arcType:   Cesium.ArcType.NONE,
            depthFailMaterial: Cesium.Color.fromCssColorString('#4ade80').withAlpha(0.25),
        },
    });
    entityGroups.path_starlink.push(line);

    // Mark the ground nodes at each end of the path (DC and GW only, skip satellite hops)
    const ground = coords.filter(c => nodeAltM(c.key) === 0);
    for (const c of [...ground.slice(0, 2), ...ground.slice(-2)]) {
        _addPointMarker('path_starlink', c.lng, c.lat, 0, '#4ade80');
    }
}

// ── Packet animation ──────────────────────────────────────────────────────────
function clearAnimation() {
    _animGen++;
    animTimers.forEach(clearTimeout);
    animTimers = [];
    for (const e of animPackets) {
        try { viewer.entities.remove(e); } catch (_) {}
    }
    animPackets = [];
}

function animatePacket(coords, colorHex, speedFactor) {
    if (!coords || coords.length < 2) return;

    const myGen = _animGen;

    // Build interpolated arc — 18 steps between each waypoint
    const waypoints = coords.map(c =>
        Cesium.Cartesian3.fromDegrees(c.lng, c.lat, nodeAltM(c.key) + 4_000)
    );
    const arcPts = [];
    const STEPS  = 18;
    for (let i = 0; i < waypoints.length - 1; i++) {
        for (let j = 0; j < STEPS; j++) {
            arcPts.push(Cesium.Cartesian3.lerp(
                waypoints[i], waypoints[i + 1], j / STEPS, new Cesium.Cartesian3()
            ));
        }
    }
    arcPts.push(waypoints[waypoints.length - 1]);

    const packetEnt = viewer.entities.add({
        position: arcPts[0],
        point: {
            pixelSize:                5,
            color:                    Cesium.Color.fromCssColorString(colorHex),
            disableDepthTestDistance: 5e6,
        },
    });
    animPackets.push(packetEnt);

    let idx          = 0;
    const interval   = Math.max(12, 28 / speedFactor);

    function step() {
        if (_animGen !== myGen) return;   // cancelled
        idx++;
        if (idx >= arcPts.length) {
            try { viewer.entities.remove(packetEnt); } catch (_) {}
            const i = animPackets.indexOf(packetEnt);
            if (i >= 0) animPackets.splice(i, 1);
            return;
        }
        packetEnt.position = new Cesium.ConstantPositionProperty(arcPts[idx]);
        animTimers.push(setTimeout(step, interval));
    }
    animTimers.push(setTimeout(step, 30));
}

// ── Populate dropdowns ────────────────────────────────────────────────────────
function populateDropdowns(cloud) {
    cloudNodes = cloud;
    const srcEl = document.getElementById('sel-src');
    const dstEl = document.getElementById('sel-dst');

    const groups = {};
    for (const n of cloud) {
        const grp = n.provider;
        if (!groups[grp]) groups[grp] = [];
        groups[grp].push(n);
    }

    function buildOptions(el, defaultKey) {
        el.innerHTML = '';
        for (const [grp, nodes] of Object.entries(groups)) {
            const og = document.createElement('optgroup');
            og.label = grp;
            for (const n of nodes) {
                const opt = document.createElement('option');
                opt.value       = n.key;
                opt.textContent = n.label;
                og.appendChild(opt);
            }
            el.appendChild(og);
        }
        if (defaultKey) el.value = defaultKey;
    }

    buildOptions(srcEl, 'aws-us-east-1');
    buildOptions(dstEl, 'gcp-asia-northeast1');
}

// ── Crisis dropdown ───────────────────────────────────────────────────────────
function populateCrisisDropdown(edges) {
    allEdgesData = edges;
    const sel    = document.getElementById('crisis-select');
    const seen   = new Set();
    for (const e of edges.filter(e => e.edge_type === 'submarine' || e.edge_type === 'fiber')) {
        const k = [e.src, e.dst].sort().join(',');
        if (seen.has(k)) continue;
        seen.add(k);
        const opt       = document.createElement('option');
        opt.value       = `${e.src},${e.dst}`;
        const srcLbl    = allNodes[e.src]?.label || e.src;
        const dstLbl    = allNodes[e.dst]?.label || e.dst;
        opt.textContent = `✂ ${srcLbl} ↔ ${dstLbl}  (${e.distance_km} km)`;
        sel.appendChild(opt);
    }
}

// ── Draw route result ─────────────────────────────────────────────────────────
function drawResult(data) {
    clearPaths();

    const fib = data.terrestrial;
    const sl  = data.starlink;

    if (fib.coords?.length > 1) drawFiberPath(fib.coords);
    if (sl.coords?.length  > 1) drawStarlinkPath(sl.coords);

    // Fly camera to encompass both ground paths
    const groundCoords = [...(fib.coords || []), ...(sl.coords || [])]
        .filter(c => nodeAltM(c.key) === 0);
    if (groundCoords.length > 0) {
        const bs = Cesium.BoundingSphere.fromPoints(
            groundCoords.map(c => Cesium.Cartesian3.fromDegrees(c.lng, c.lat))
        );
        viewer.camera.flyToBoundingSphere(bs, {
            duration: 1.5,
            offset:   new Cesium.HeadingPitchRange(
                viewer.camera.heading,
                -Cesium.Math.toRadians(38),
                Math.max(bs.radius * 3, 3_000_000),  // never closer than 3 000 km
            ),
        });
    }

    // ── Sidebar panels ───────────────────────────────────────────────────────
    document.getElementById('error-wrap').classList.add('d-none');
    document.getElementById('results-wrap').classList.remove('d-none');

    const fmt = v => v != null ? v : '—';
    document.getElementById('fiber-ms').textContent    = fmt(fib.latency_ms);
    document.getElementById('fiber-km').textContent    = fmt(fib.distance_km);
    document.getElementById('fiber-hops').textContent  = fmt(fib.hops);
    document.getElementById('fiber-route').textContent = fib.path.join(' → ');

    document.getElementById('sl-ms').textContent       = fmt(sl.latency_ms);
    document.getElementById('sl-km').textContent       = fmt(sl.distance_km);
    document.getElementById('sl-hops').textContent     = fmt(sl.hops);
    document.getElementById('sl-route').textContent    = sl.path.join(' → ');

    const fibPanel = document.getElementById('panel-fiber');
    const slPanel  = document.getElementById('panel-starlink');
    fibPanel.classList.remove('winner');
    slPanel.classList.remove('winner');
    if (fib.latency_ms != null && sl.latency_ms != null) {
        if (sl.latency_ms < fib.latency_ms)      slPanel.classList.add('winner');
        else if (fib.latency_ms < sl.latency_ms) fibPanel.classList.add('winner');
    }

    // Savings note
    const note = document.getElementById('savings-note');
    if (data.savings_pct != null) {
        const faster = sl.latency_ms < fib.latency_ms;
        const kmDiff = (sl.distance_km || 0) - (fib.distance_km || 0);
        note.textContent = faster
            ? `💡 Starlink is ${data.savings_pct}% faster — vacuum light beats glass, even ${kmDiff > 0 ? 'travelling ' + kmDiff.toLocaleString() + ' km more' : 'at similar distance'}.`
            : `ℹ️ Terrestrial is ${Math.abs(data.savings_pct)}% faster — uplink overhead dominates on this short hop.`;
    } else {
        note.textContent = '';
    }

    // Congestion + topology note
    const conNote = document.getElementById('congestion-note');
    if (data.congestion_active) {
        const m       = data.minute_of_day ?? ((data.hour_utc ?? 0) * 60);
        const regions = FTS_REGIONS.map(r => `${r.label}: ${loadLabel(trafficLoad(m, r.lng))}`).join('  ·  ');
        const dynLine = data.dynamic_topology
            ? `<br><span style="color:#4ade80">🛰 Real orbital topology — ${minuteToHHMM(m)} UTC</span>`
            : data.starlink_geometry_active
                ? `<br><span style="color:#818cf8">🛰 Starlink geometry model active (12–32 ms/hop)</span>`
                : '';
        conNote.innerHTML = `<span>⚠ Fiber congestion ${minuteToHHMM(m)} UTC — ${regions}</span>${dynLine}`;
    } else {
        conNote.textContent = '';
    }

    // Packet animation — Starlink packet ~33 % faster than fiber
    const fibSpd = 1.0;
    const slSpd  = fib.latency_ms && sl.latency_ms ? fib.latency_ms / sl.latency_ms * 1.5 : 1.5;
    if (fib.coords?.length > 1)
        animatePacket(fib.coords, '#22d3ee', fibSpd);
    if (sl.coords?.length > 1)
        setTimeout(() => animatePacket(sl.coords, '#4ade80', slSpd), 200);
}

// ── Route request ─────────────────────────────────────────────────────────────
async function doRoute() {
    const src = document.getElementById('sel-src').value;
    const dst = document.getElementById('sel-dst').value;
    if (!src || !dst) return;
    if (src === dst) { log('Source and destination must differ.'); return; }

    const timeStr = ftsMinute !== null ? `  [${minuteToHHMM(ftsMinute)} UTC]` : '';
    log(`Routing ${src} → ${dst}${disabledEdge ? '  [CRISIS]' : ''}${timeStr} …`);
    document.getElementById('btn-route').disabled = true;

    let url = `/demos/global-infra/route?src=${encodeURIComponent(src)}&dst=${encodeURIComponent(dst)}`;
    if (disabledEdge) url += `&disabled_edge=${encodeURIComponent(disabledEdge.join(','))}`;
    if (ftsMinute !== null) url += `&t=${ftsMinute}`;

    try {
        const r    = await fetch(url);
        const data = await r.json();

        if (data.error && !data.terrestrial) {
            document.getElementById('error-msg').textContent = '⚠ ' + data.error;
            document.getElementById('error-wrap').classList.remove('d-none');
            document.getElementById('results-wrap').classList.add('d-none');
            log('ERROR: ' + data.error);
        } else {
            drawResult(data);
            if (!!data.dynamic_topology !== hasDynamic) {
                hasDynamic = !!data.dynamic_topology;
                updateFtsDisplay(ftsMinute);
            }
            const fibMs  = data.terrestrial?.latency_ms;
            const slMs   = data.starlink?.latency_ms;
            const dynTag = data.dynamic_topology ? ' [SQL orbital]' : '';
            log(`Done. Fiber: ${fibMs != null ? fibMs + ' ms' : 'N/A'}  |  Starlink: ${slMs != null ? slMs + ' ms' : 'N/A'}${dynTag}`);
        }
    } catch (err) {
        log('Fetch error: ' + err.message);
    } finally {
        document.getElementById('btn-route').disabled = false;
    }
}

// ── Crisis button ─────────────────────────────────────────────────────────────
document.getElementById('btn-crisis').addEventListener('click', () => {
    const val = document.getElementById('crisis-select').value;
    if (!val) {
        disabledEdge = null;
        log('Crisis cleared. Re-routing on full network…');
    } else {
        disabledEdge = val.split(',');
        log(`⚠ CRISIS: cutting ${disabledEdge.join(' ↔ ')}  Re-routing…`);
    }
    doRoute();
});

document.getElementById('btn-route').addEventListener('click', doRoute);

// ── Init ──────────────────────────────────────────────────────────────────────
async function init() {
    log('Loading global infrastructure graph…');
    try {
        const [nodesResp, edgesResp] = await Promise.all([
            fetch('/demos/global-infra/nodes'),
            fetch('/demos/global-infra/edges'),
        ]);
        const nodesData = await nodesResp.json();
        const edgesData = await edgesResp.json();

        drawNodes(nodesData.all);
        drawEdges(edgesData);
        populateDropdowns(nodesData.cloud);
        populateCrisisDropdown(edgesData);
        wireToggles();
        wireFts();

        log(`Loaded ${nodesData.all.length} nodes, ${edgesData.length} backbone edges. Ready.`);
    } catch (err) {
        log('Init error: ' + err.message);
    }
}

init();
