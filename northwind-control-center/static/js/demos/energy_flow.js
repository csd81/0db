/* energy_flow.js — Global Oil & Gas Max-Flow visualization */
'use strict';

// ── Constants ──────────────────────────────────────────────────────────────────
const EF_TILE_DARK  = 'https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png';
const EF_TILE_LIGHT = 'https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png';
const LINE_ALT      = 8000;   // metres above ellipsoid for Cesium lines

const NODE_COLORS = {
  oil_producer:      '#22c55e',
  oil_consumer:      '#3b82f6',
  chokepoint:        '#ef4444',
  lng_export:        '#22d3ee',
  lng_import:        '#0ea5e9',
  gas_producer:      '#10b981',
  pipeline_junction: '#f59e0b',
};

const CRISIS_PRESETS = {
  houthi:     { 'chk-bab': 16 },
  hormuz:     { 'chk-hormuz': 0 },
  suez:       { 'chk-suez': 0 },
  nordstream: { 'chk-druzhba': 27 },  // 27% ≈ southern-branch-only (600/2200 kbd)
};

// ── State ──────────────────────────────────────────────────────────────────────
let currentMode      = 'oil';
let currentMonthIdx  = 0;
let allMonths        = [];
let constrictions    = {};
let leafletLayer     = null;
let leafletMap       = null;
let cesiumViewer     = null;
let cesiumReady      = false;
let playInterval     = null;
let allNodes         = [];
let allEdges         = [];
let chokeData        = [];

// Leaflet layer groups
const lfLayers = { nodes: null, edges: null, flow: null };
// Cesium collections
const csCollections = { points: null, lines: [] };

// ── Utility ────────────────────────────────────────────────────────────────────
function esc(s) {
  return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
}

function lerpColor(hex1, hex2, t) {
  const parse = h => [parseInt(h.slice(1,3),16), parseInt(h.slice(3,5),16), parseInt(h.slice(5,7),16)];
  const [r1,g1,b1] = parse(hex1);
  const [r2,g2,b2] = parse(hex2);
  const r = Math.round(r1 + (r2-r1)*t);
  const g = Math.round(g1 + (g2-g1)*t);
  const b = Math.round(b1 + (b2-b1)*t);
  return `#${r.toString(16).padStart(2,'0')}${g.toString(16).padStart(2,'0')}${b.toString(16).padStart(2,'0')}`;
}

function flowColor(pct, commodity) {
  if (commodity === 'gas') {
    if (pct < 50) return lerpColor('#0a2a4a', '#22d3ee', pct / 50);
    return lerpColor('#22d3ee', '#7c3aed', (pct - 50) / 50);
  }
  if (pct < 50) return lerpColor('#1e3a5f', '#f97316', pct / 50);
  return lerpColor('#f97316', '#ef4444', (pct - 50) / 50);
}

function logWidth(cap) {
  return Math.max(1, Math.log(cap + 1) * 0.5);
}

// Normalise consecutive lngs so no jump exceeds 180° — makes trans-Pacific lines
// draw westward on the Leaflet Mercator map instead of wrapping eastward.
function normalizeAntimeridian(latlngs) {
  if (!latlngs || latlngs.length < 2) return latlngs;
  const out = [[latlngs[0][0], latlngs[0][1]]];
  for (let i = 1; i < latlngs.length; i++) {
    let [lat, lng] = latlngs[i];
    const prev = out[i - 1][1];
    while (lng - prev >  180) lng -= 360;
    while (prev - lng >  180) lng += 360;
    out.push([lat, lng]);
  }
  return out;
}

function currentMonthKey() {
  return allMonths[currentMonthIdx]?.key ?? '2021-01';
}

// ── Leaflet init ───────────────────────────────────────────────────────────────
function initLeaflet() {
  const initTheme = document.documentElement.getAttribute('data-bs-theme') || 'dark';
  leafletMap = L.map('ef-map', {
    center: [25, 20], zoom: 2,
    zoomControl: true,
    worldCopyJump: false,
  });
  leafletLayer = L.tileLayer(initTheme === 'light' ? EF_TILE_LIGHT : EF_TILE_DARK, {
    attribution: '© CartoDB', subdomains: 'abcd', maxZoom: 19,
  }).addTo(leafletMap);

  lfLayers.edges = L.layerGroup().addTo(leafletMap);
  lfLayers.nodes = L.layerGroup().addTo(leafletMap);
  lfLayers.flow  = L.layerGroup().addTo(leafletMap);
}

// ── Cesium init (lazy) ─────────────────────────────────────────────────────────
function initCesium() {
  if (cesiumReady) return;
  const initTheme = document.documentElement.getAttribute('data-bs-theme') || 'dark';
  const tileUrl = initTheme === 'light' ? EF_TILE_LIGHT : EF_TILE_DARK;

  cesiumViewer = new Cesium.Viewer('ef-globe', {
    imageryProvider: false,
    terrainProvider: new Cesium.EllipsoidTerrainProvider(),
    baseLayerPicker: false, geocoder: false, homeButton: false,
    sceneModePicker: false, navigationHelpButton: false,
    animation: false, timeline: false, fullscreenButton: false,
    selectionIndicator: false, infoBox: false,
  });
  cesiumViewer.scene.screenSpaceCameraController.enableCollisionDetection = false;
  cesiumViewer.scene.globe.enableLighting = false;

  csCollections.points = new Cesium.PointPrimitiveCollection();
  cesiumViewer.scene.primitives.add(csCollections.points);
  cesiumReady = true;
  _efSetTiles(document.documentElement.getAttribute('data-bs-theme') || 'dark');
}

function _efSetTiles(theme) {
  if (!cesiumViewer) return;
  const url = (theme === 'light' ? EF_TILE_LIGHT : EF_TILE_DARK).replace('{r}','').replace('{s}','a');
  cesiumViewer.imageryLayers.removeAll();
  cesiumViewer.imageryLayers.addImageryProvider(
    new Cesium.UrlTemplateImageryProvider({ url, credit: '' })
  );
  cesiumViewer.scene.globe.baseColor = Cesium.Color.fromCssColorString(
    theme === 'light' ? '#d0d8e4' : '#06080c');
  cesiumViewer.scene.backgroundColor = theme === 'light'
    ? new Cesium.Color(0.9, 0.93, 0.97, 1.0)
    : new Cesium.Color(0.02, 0.03, 0.05, 1.0);
}

// ── 2D / 3D toggle ────────────────────────────────────────────────────────────
document.getElementById('btn-2d').addEventListener('click', () => {
  document.getElementById('ef-map').style.display   = '';
  document.getElementById('ef-globe').style.display = 'none';
  document.getElementById('btn-2d').classList.add('active');
  document.getElementById('btn-3d').classList.remove('active');
});
document.getElementById('btn-3d').addEventListener('click', () => {
  document.getElementById('ef-globe').style.display = '';
  document.getElementById('ef-map').style.display   = 'none';
  document.getElementById('btn-3d').classList.add('active');
  document.getElementById('btn-2d').classList.remove('active');
  initCesium();
  renderNodesCesium(allNodes);
  renderEdgesCesium(allEdges);
});

// ── Theme listener ─────────────────────────────────────────────────────────────
document.addEventListener('themeChanged', e => {
  const theme = e.detail;
  if (leafletLayer) leafletLayer.setUrl(theme === 'light' ? EF_TILE_LIGHT : EF_TILE_DARK);
  _efSetTiles(theme);
});

// ── Node rendering: Leaflet ────────────────────────────────────────────────────
function renderNodesLeaflet(nodes) {
  lfLayers.nodes.clearLayers();
  nodes.forEach(n => {
    const show = shouldShowNode(n);
    if (!show) return;
    const color = NODE_COLORS[n.type] || '#888';
    const r = nodeRadius(n);
    const marker = L.circleMarker([n.lat, n.lng], {
      radius: r, color, fillColor: color, fillOpacity: 0.85,
      weight: n.type === 'chokepoint' ? 2 : 1,
      dashArray: n.type === 'chokepoint' ? '4,2' : null,
    });
    marker.bindTooltip(buildTooltip(n), { className: 'leaflet-dark-tip' });
    lfLayers.nodes.addLayer(marker);
  });
}

function shouldShowNode(n) {
  if (currentMode === 'oil')
    return ['oil_producer','oil_consumer','chokepoint','pipeline_junction'].includes(n.type);
  if (currentMode === 'gas')
    return ['gas_producer','lng_export','lng_import','oil_consumer','chokepoint','pipeline_junction'].includes(n.type);
  return true;
}

function nodeRadius(n) {
  if (n.type === 'chokepoint')   return 7;
  if (n.type === 'lng_import')   return 5;
  if (n.type === 'oil_producer' || n.type === 'gas_producer' || n.type === 'lng_export') {
    const val = n.kbd || n.bcm || 100;
    return Math.max(4, Math.sqrt(val / 50));
  }
  const val = n.kbd || n.bcm || 100;
  return Math.max(5, Math.sqrt(val / 80));
}

function buildTooltip(n) {
  let cap = '';
  if (n.kbd)         cap = `<br><small>${n.kbd.toLocaleString()} kbd export</small>`;
  else if (n.bcm)    cap = `<br><small>${n.bcm} bcm/yr</small>`;
  else if (n.normal_kbd) cap = `<br><small>${n.normal_kbd.toLocaleString()} kbd capacity</small>`;
  return `<b>${esc(n.label)}</b>${cap}`;
}

// ── Node rendering: Cesium ─────────────────────────────────────────────────────
function renderNodesCesium(nodes) {
  if (!cesiumReady) return;
  csCollections.points.removeAll();
  nodes.forEach(n => {
    if (!shouldShowNode(n)) return;
    const color = Cesium.Color.fromCssColorString(NODE_COLORS[n.type] || '#888');
    const r = nodeRadius(n);
    csCollections.points.add({
      position: Cesium.Cartesian3.fromDegrees(n.lng, n.lat, 5000),
      color, pixelSize: r * 2.2,
      outlineColor: Cesium.Color.BLACK.withAlpha(0.5),
      outlineWidth: 1,
      disableDepthTestDistance: 5e6,
    });
  });
}

// ── Edge rendering: Leaflet ────────────────────────────────────────────────────
function renderEdgesLeaflet(edges, flowMap) {
  lfLayers.edges.clearLayers();
  lfLayers.flow.clearLayers();

  edges.forEach(e => {
    if (!shouldShowEdge(e)) return;
    if (!e.lat1 && !e.lng1 && !e.lat2 && !e.lng2) return;

    const width = logWidth(e.capacity || 1);
    const isPipeline = e.type === 'pipeline' || e.type === 'gas_pipeline';
    const dashArr = isPipeline ? '6,4' : null;
    let color = '#2a3040';

    const fkey = `${e.src}|${e.dst}`;
    const fd   = flowMap ? flowMap[fkey] : null;
    if (fd) {
      color = flowColor(fd.pct, fd.commodity);
    }

    const pts = normalizeAntimeridian(e.latlngs || [[e.lat1, e.lng1], [e.lat2, e.lng2]]);
    const line = L.polyline(pts, {
      color, weight: fd ? Math.max(1.5, width * (0.3 + 0.7 * (fd.pct/100))) : Math.max(1.5, width * 0.75),
      opacity: fd ? (0.2 + 0.8 * (fd.pct / 100)) : 0.65,
      dashArray: dashArr,
    });
    line.bindTooltip(`${esc(e.label)}<br><small>${e.capacity} ${e.unit}</small>`);
    (fd ? lfLayers.flow : lfLayers.edges).addLayer(line);
  });
}

function shouldShowEdge(e) {
  if (currentMode === 'oil') return e.commodity === 'oil';
  if (currentMode === 'gas') return e.commodity === 'gas';
  return true;
}

// ── Edge rendering: Cesium ─────────────────────────────────────────────────────
function _clearCesiumLines() {
  csCollections.lines.forEach(e => cesiumViewer.entities.remove(e));
  csCollections.lines = [];
}

function renderEdgesCesium(edges, flowMap) {
  if (!cesiumReady) return;
  _clearCesiumLines();

  edges.forEach(e => {
    if (!shouldShowEdge(e)) return;
    if (!e.lat1 && !e.lng1) return;

    const fkey = `${e.src}|${e.dst}`;
    const fd   = flowMap ? flowMap[fkey] : null;
    const hexC = fd ? flowColor(fd.pct, fd.commodity) : '#4a5570';
    const alpha = fd ? (0.2 + 0.8 * fd.pct / 100) : 0.65;
    const width = fd ? Math.max(1, logWidth(fd.capacity) * (0.3 + 0.7 * fd.pct/100)) : Math.max(1.5, logWidth(e.capacity || 1) * 0.75);
    const color = Cesium.Color.fromCssColorString(hexC).withAlpha(alpha);

    const pts = (e.latlngs || [[e.lat1, e.lng1], [e.lat2, e.lng2]])
      .flatMap(([lt, lg]) => [lg, lt, LINE_ALT]);
    const entity = cesiumViewer.entities.add({
      polyline: {
        positions: Cesium.Cartesian3.fromDegreesArrayHeights(pts),
        width,
        material: new Cesium.ColorMaterialProperty(color),
        arcType: Cesium.ArcType.GEODESIC,
      },
    });
    csCollections.lines.push(entity);
  });
}

// ── Build flow lookup map ──────────────────────────────────────────────────────
function buildFlowMap(data) {
  const map = {};
  function addEdgeFlows(flows, commodity) {
    flows.forEach(ef => {
      map[`${ef.src}|${ef.dst}`] = { ...ef, commodity };
    });
  }
  if (data.oil && (currentMode === 'oil' || currentMode === 'both'))
    addEdgeFlows(data.oil.edge_flows, 'oil');
  if (data.gas && (currentMode === 'gas' || currentMode === 'both'))
    addEdgeFlows(data.gas.edge_flows, 'gas');
  return map;
}

// ── Min-cut flash ──────────────────────────────────────────────────────────────
let _minCutInterval = null;
let _minCutLines    = [];

function flashMinCut(cutEdges) {
  if (_minCutInterval) { clearInterval(_minCutInterval); _minCutInterval = null; }
  _minCutLines.forEach(l => lfLayers.flow.removeLayer(l));
  _minCutLines = [];

  cutEdges.forEach(ce => {
    const n1 = allNodes.find(n => n.key === ce.src);
    const n2 = allNodes.find(n => n.key === ce.dst);
    if (!n1 || !n2) return;
    const edgeData = allEdges.find(e => e.src === ce.src && e.dst === ce.dst);
    const pts = normalizeAntimeridian(edgeData?.latlngs || [[n1.lat, n1.lng],[n2.lat, n2.lng]]);
    const line = L.polyline(pts, {
      color: '#ef4444', weight: 4, opacity: 1, dashArray: '8,4',
    });
    lfLayers.flow.addLayer(line);
    _minCutLines.push(line);
  });

  let vis = true;
  _minCutInterval = setInterval(() => {
    vis = !vis;
    _minCutLines.forEach(l => l.setStyle({ opacity: vis ? 1 : 0.1 }));
  }, 500);
}

// ── Render flow result ─────────────────────────────────────────────────────────
function renderFlowResult(data) {
  const flowMap = buildFlowMap(data);
  renderEdgesLeaflet(allEdges, flowMap);
  if (cesiumReady) renderEdgesCesium(allEdges, flowMap);

  // Min-cut
  const cutEdges = [];
  if (data.oil && (currentMode !== 'gas'))
    data.oil.min_cut_edges.forEach(e => cutEdges.push(e));
  if (data.gas && (currentMode !== 'oil'))
    data.gas.min_cut_edges.forEach(e => cutEdges.push(e));
  flashMinCut(cutEdges);

  // Metrics
  const oilFlow = data.oil?.total_flow ?? '—';
  const oilDef  = data.oil?.deficit_pct ?? '—';
  const gasFlow = data.gas?.total_flow ?? '—';
  const gasDef  = data.gas?.deficit_pct ?? '—';

  document.getElementById('m-oil-flow').textContent = typeof oilFlow === 'number' ? oilFlow.toLocaleString() : oilFlow;
  document.getElementById('m-oil-def').textContent  = typeof oilDef  === 'number' ? oilDef.toFixed(1) + '%' : oilDef;
  document.getElementById('m-gas-flow').textContent = typeof gasFlow === 'number' ? gasFlow.toLocaleString() : gasFlow;
  document.getElementById('m-gas-def').textContent  = typeof gasDef  === 'number' ? gasDef.toFixed(1) + '%' : gasDef;

  // Result panel
  const panel = document.getElementById('result-panel');
  panel.classList.remove('d-none');
  const oilCutLabels = (data.oil?.min_cut_nodes || []).map(n => n.label).join(', ');
  const gasCutLabels = (data.gas?.min_cut_nodes || []).map(n => n.label).join(', ');
  const cross = data.snapshot_desc || '';

  panel.innerHTML = `
    <div style="color:#f97316;font-weight:700;margin-bottom:.3rem">⛽ Oil Min-Cut</div>
    <div>${esc(oilCutLabels || 'None identified')}</div>
    <div style="color:#22d3ee;font-weight:700;margin:.3rem 0 .2rem">🔵 Gas Min-Cut</div>
    <div>${esc(gasCutLabels || 'None identified')}</div>
    ${cross ? `<div style="color:#6c757d;margin-top:.35rem;font-size:.61rem">${esc(cross)}</div>` : ''}
  `;

  setBadge('done', 'success');
}

// ── Compute API call ───────────────────────────────────────────────────────────
async function computeFlow() {
  setBadge('computing…', 'warning');
  const body = { month: currentMonthKey(), constrictions };
  try {
    const r = await fetch('/demos/energy-flow/compute', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    });
    const data = await r.json();
    if (data.error) { setBadge('error', 'danger'); return; }
    renderFlowResult(data);
  } catch (err) {
    setBadge('error', 'danger');
    console.error(err);
  }
}

// ── Badge helper ───────────────────────────────────────────────────────────────
function setBadge(text, variant) {
  const b = document.getElementById('ef-badge');
  b.className = `badge ms-auto bg-${variant}`;
  b.textContent = text;
  b.style.fontSize = '.62rem';
}

// ── Constriction sliders ───────────────────────────────────────────────────────
let _computeTimer = null;
function scheduleCompute() {
  clearTimeout(_computeTimer);
  _computeTimer = setTimeout(computeFlow, 400);
}

function buildChokeSliders(chokes) {
  chokeData = chokes;
  const container = document.getElementById('choke-sliders');
  container.innerHTML = '';
  chokes.forEach(c => {
    const div = document.createElement('div');
    div.className = 'choke-row';
    div.innerHTML = `
      <div class="choke-lbl-row">
        <span class="choke-name">${esc(c.label)}</span>
        <span class="choke-val" id="cv-${c.key}">100% · ${c.normal_kbd.toLocaleString()} kbd</span>
      </div>
      <input type="range" class="choke-slider" id="cs-${c.key}"
             data-key="${c.key}" data-oil="${c.normal_kbd}" data-gas="${c.gas_bcm}"
             min="0" max="100" value="100" step="5">
    `;
    container.appendChild(div);

    const sl = div.querySelector('input');
    sl.addEventListener('input', () => {
      const pct = parseInt(sl.value);
      constrictions[c.key] = pct;
      const oilEff = Math.round(c.normal_kbd * pct / 100);
      document.getElementById(`cv-${c.key}`).textContent =
        `${pct}% · ${oilEff.toLocaleString()} kbd`;
      sl.className = pct === 100 ? 'choke-slider normal' : 'choke-slider';
      scheduleCompute();
    });
  });
}

function setSlider(key, pct) {
  const sl = document.getElementById(`cs-${key}`);
  if (!sl) return;
  sl.value = pct;
  sl.dispatchEvent(new Event('input'));
}

function resetSliders() {
  chokeData.forEach(c => setSlider(c.key, 100));
}

// ── Crisis presets ─────────────────────────────────────────────────────────────
document.querySelectorAll('.preset-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    const preset = btn.dataset.preset;
    resetSliders();
    const overrides = CRISIS_PRESETS[preset] || {};
    Object.entries(overrides).forEach(([k, v]) => setSlider(k, v));
    // For nordstream, jump to 2022-09 snapshot
    if (preset === 'nordstream') {
      const idx = allMonths.findIndex(m => m.key === '2022-09');
      if (idx >= 0) { currentMonthIdx = idx; updateTimeline(); }
    }
    document.querySelectorAll('.preset-btn').forEach(b => b.classList.remove('armed'));
    btn.classList.add('armed');
    computeFlow();
  });
});

// ── Commodity toggle ──────────────────────────────────────────────────────────
document.querySelectorAll('.commodity-pill').forEach(btn => {
  btn.addEventListener('click', () => {
    currentMode = btn.dataset.c;
    document.querySelectorAll('.commodity-pill').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    renderNodesLeaflet(allNodes);
    renderEdgesLeaflet(allEdges, null);
    if (cesiumReady) { renderNodesCesium(allNodes); renderEdgesCesium(allEdges, null); }
  });
});

// ── Timeline ──────────────────────────────────────────────────────────────────
function buildShockMarks(months) {
  const container = document.getElementById('shock-marks');
  container.innerHTML = '';
  const total = months.length - 1;
  months.forEach((m, i) => {
    if (!m.shock) return;
    const pct = (i / total) * 100;
    const mark = document.createElement('div');
    mark.className = 'shock-mark';
    mark.style.left = pct + '%';
    mark.dataset.label = m.shock;
    mark.title = m.shock;
    mark.addEventListener('click', () => {
      currentMonthIdx = i;
      document.getElementById('timeline-slider').value = i;
      updateTimeline();
      computeFlow();
    });
    container.appendChild(mark);
  });
}

function updateTimeline() {
  const m = allMonths[currentMonthIdx];
  if (!m) return;
  document.getElementById('timeline-slider').value = currentMonthIdx;
  document.getElementById('timeline-label').textContent = m.shock || m.key;
  // Fetch snapshot desc
  const snap = Object.values({
    '2021-01': 'Pre-crisis baseline. All routes at full capacity.',
    '2022-02': 'Sanctions begin. Russian exports start declining.',
    '2022-09': 'Nord Stream sabotaged Sep 26, 2022. Major EU gas supply shock.',
    '2023-01': 'EU fully bans Russian crude. Druzhba pipeline halted.',
    '2024-01': 'Houthi attacks force ~84% reduction in Bab-el-Mandeb tanker traffic.',
    '2024-06': 'Tanker fleets adapt to Cape route. Bab-el-Mandeb partially recovers.',
    '2025-01': 'Russian oil flows to Asia via shadow fleet. Status quo.',
    '2026-05': 'Iran War (2026). Hormuz closed. ~20% global oil cut. Qatar LNG stranded. Iraq reroutes via Kirkuk–Ceyhan.',
  });
  const snapshots = {
    '2021-01': 'Pre-crisis baseline. All routes at full capacity.',
    '2022-02': 'Sanctions begin. Russian exports start declining.',
    '2022-09': 'Nord Stream sabotaged Sep 26, 2022. Major EU gas supply shock.',
    '2023-01': 'EU fully bans Russian crude. Druzhba pipeline halted.',
    '2024-01': 'Houthi attacks force ~84% reduction in Bab-el-Mandeb tanker traffic.',
    '2024-06': 'Tanker fleets adapt to Cape route. Bab-el-Mandeb partially recovers.',
    '2025-01': 'Russian oil flows to Asia via shadow fleet. Status quo.',
    '2026-05': 'Iran War (2026). Hormuz closed. ~20% global oil cut. Qatar LNG stranded. Iraq reroutes via Kirkuk–Ceyhan.',
  };
  // Show nearest snapshot desc
  const nearestKey = Object.keys(snapshots).reverse().find(k => k <= m.key) || '2021-01';
  document.getElementById('snapshot-desc').textContent = snapshots[nearestKey] || '';
}

const slider = document.getElementById('timeline-slider');
slider.addEventListener('input', () => {
  currentMonthIdx = parseInt(slider.value);
  updateTimeline();
  scheduleCompute();
});

// ── Play / pause ───────────────────────────────────────────────────────────────
const btnPlay = document.getElementById('btn-play');
btnPlay.addEventListener('click', () => {
  if (playInterval) {
    clearInterval(playInterval);
    playInterval = null;
    btnPlay.textContent = '▶';
  } else {
    btnPlay.textContent = '⏸';
    if (currentMonthIdx >= allMonths.length - 1) currentMonthIdx = 0;
    playInterval = setInterval(() => {
      currentMonthIdx++;
      updateTimeline();
      computeFlow();
      if (currentMonthIdx >= allMonths.length - 1) {
        clearInterval(playInterval);
        playInterval = null;
        btnPlay.textContent = '▶';
      }
    }, 1800);
  }
});

// ── Compute button ─────────────────────────────────────────────────────────────
document.getElementById('btn-compute').addEventListener('click', computeFlow);

// ── Bootstrap ─────────────────────────────────────────────────────────────────
async function init() {
  initLeaflet();

  const [nodesRes, edgesRes, timelineRes, chokesRes] = await Promise.all([
    fetch('/demos/energy-flow/nodes').then(r => r.json()),
    fetch('/demos/energy-flow/edges?month=2021-01').then(r => r.json()),
    fetch('/demos/energy-flow/timeline').then(r => r.json()),
    fetch('/demos/energy-flow/chokepoints').then(r => r.json()),
  ]);

  allNodes  = nodesRes;
  allEdges  = edgesRes;
  allMonths = timelineRes;

  // Set slider max
  document.getElementById('timeline-slider').max = allMonths.length - 1;

  buildShockMarks(allMonths);
  buildChokeSliders(chokesRes);
  renderNodesLeaflet(allNodes);
  renderEdgesLeaflet(allEdges, null);
  updateTimeline();
  setBadge('ready', 'secondary');

  // Auto-compute on load
  await computeFlow();
}

init();
