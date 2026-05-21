'use strict';

const PG_TILE_DARK  = 'https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png';
const PG_TILE_LIGHT = 'https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png';

// ── Leaflet map ──────────────────────────────────────────────────────────────
const _initTheme = document.documentElement.getAttribute('data-bs-theme') || 'dark';
const map = L.map('pg-map', {zoomControl: true}).setView([30, 20], 3);
const leafletLayer = L.tileLayer(
    _initTheme === 'light' ? PG_TILE_LIGHT : PG_TILE_DARK,
    {
        attribution: '&copy; <a href="https://openstreetmap.org">OpenStreetMap</a> &copy; <a href="https://carto.com">CARTO</a>',
        subdomains: 'abcd',
        maxZoom: 19,
    }
).addTo(map);

// ── Cesium 3D globe ──────────────────────────────────────────────────────────
let cesiumViewer = null;
let is3D         = false;
let cPointColl   = null;

function _initCesiumViewer() {
    cesiumViewer = new Cesium.Viewer('pg-globe', {
        animation: false, baseLayerPicker: false, fullscreenButton: false,
        geocoder: false, homeButton: false, infoBox: false,
        navigationHelpButton: false, sceneModePicker: false, timeline: false,
        selectionIndicator: false,
        imageryProvider: false,
        terrainProvider: new Cesium.EllipsoidTerrainProvider(),
    });
    cPointColl = cesiumViewer.scene.primitives.add(new Cesium.PointPrimitiveCollection());
    _pgSetTiles(document.documentElement.getAttribute('data-bs-theme') || 'dark');
}

function _pgSetTiles(theme) {
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

// ── 2D/3D toggle ─────────────────────────────────────────────────────────────
document.getElementById('btn-2d').addEventListener('click', () => {
    if (!is3D) return;
    is3D = false;
    document.getElementById('pg-map').style.display   = '';
    document.getElementById('pg-globe').style.display = 'none';
    document.getElementById('btn-2d').classList.add('active');
    document.getElementById('btn-3d').classList.remove('active');
    setTimeout(() => map.invalidateSize(), 50);
});

document.getElementById('btn-3d').addEventListener('click', () => {
    if (is3D) return;
    is3D = true;
    if (!cesiumViewer) {
        _initCesiumViewer();
        // Populate globe if data already loaded
        if (_cachedCities) _renderCesium(_cachedCities);
    }
    document.getElementById('pg-map').style.display   = 'none';
    document.getElementById('pg-globe').style.display = '';
    document.getElementById('btn-2d').classList.remove('active');
    document.getElementById('btn-3d').classList.add('active');
    setTimeout(() => cesiumViewer.resize(), 50);
});

// ── Theme switching ───────────────────────────────────────────────────────────
document.addEventListener('themeChanged', e => {
    const theme = e.detail;
    leafletLayer.setUrl(theme === 'light' ? PG_TILE_LIGHT : PG_TILE_DARK);
    _pgSetTiles(theme);
});

// ── Colour helpers ────────────────────────────────────────────────────────────
function esc(s) { return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;'); }

function prColor(pct) {
    if (pct <= 0.01) return '#ffd700';
    if (pct <= 0.05) return '#fd7e14';
    if (pct <= 0.20) return '#0dcaf0';
    return '#2d3245';
}

function prRadius(norm) { return 2 + norm * 18; }

// ── Cesium rendering ─────────────────────────────────────────────────────────
let _cachedCities = null;

function _renderCesium(cities) {
    if (!cPointColl) return;
    cPointColl.removeAll();
    for (const c of cities) {
        const hex   = prColor(c.pr_pct);
        const color = Cesium.Color.fromCssColorString(hex);
        const isTop = c.pr_pct <= 0.01;
        // Scale pixel size: 2–14 px (smaller than Leaflet radius to avoid clutter at globe scale)
        const sz = 2 + c.pr_norm * 12;
        cPointColl.add({
            position: Cesium.Cartesian3.fromDegrees(c.lng, c.lat, 5000),
            color: isTop ? color : color.withAlpha(0.72),
            pixelSize: sz,
            disableDepthTestDistance: 5e6,
        });
    }
}

// ── Data load ────────────────────────────────────────────────────────────────
async function load() {
    try {
        const r    = await fetch('/demos/graph_pagerank/data');
        const data = await r.json();

        if (data.error) {
            document.getElementById('loading-row').innerHTML =
                `<span class="text-danger">Error: ${esc(data.error)}</span>`;
            return;
        }

        _cachedCities = data.cities;

        // ── Leaflet markers ───────────────────────────────────────────────────
        for (const c of data.cities) {
            const color  = prColor(c.pr_pct);
            const radius = prRadius(c.pr_norm);
            const isTop  = c.pr_pct <= 0.01;
            L.circleMarker([c.lat, c.lng], {
                radius,
                color,
                fillColor:   color,
                fillOpacity: isTop ? 0.88 : 0.65,
                weight:      isTop ? 2 : 1,
            })
            .bindTooltip(
                `<b>${esc(c.name)}</b> (${esc(c.country)})<br>` +
                `Chokepoint rank: #${c.pr_rank.toLocaleString()} of ${data.n_cities.toLocaleString()}<br>` +
                `Pop: ${c.population.toLocaleString()}<br>` +
                `BC score: ${c.pr_norm.toFixed(4)}`,
                {sticky: true}
            )
            .addTo(map);
        }

        // ── Populate globe if already open ────────────────────────────────────
        if (cesiumViewer) _renderCesium(data.cities);

        // ── Stats badge ───────────────────────────────────────────────────────
        const badge = document.getElementById('stats-badge');
        badge.textContent = `${data.n_cities.toLocaleString()} cities · ${data.n_edges.toLocaleString()} roads`;
        badge.className   = 'badge bg-success ms-auto';

        document.getElementById('loading-row').classList.add('d-none');

        // ── Top-25 table ──────────────────────────────────────────────────────
        const tbody = document.getElementById('rank-body');
        tbody.innerHTML = data.top25.map(c => {
            const barW = Math.round(c.pr_norm * 55);
            return `<tr>
              <td class="text-muted">${c.pr_rank}</td>
              <td><strong>${esc(c.name)}</strong></td>
              <td class="text-muted">${esc(c.country)}</td>
              <td>
                <span class="pr-bar" style="width:${barW}px"></span>
                <span class="text-muted ms-1">${c.pr_norm.toFixed(3)}</span>
              </td>
            </tr>`;
        }).join('');

    } catch (e) {
        document.getElementById('loading-row').innerHTML =
            `<span class="text-danger">Network error — ${esc(e.message)}</span>`;
    }
}

load();
