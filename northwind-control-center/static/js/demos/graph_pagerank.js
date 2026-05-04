'use strict';

const map = L.map('pg-map', {zoomControl: true}).setView([30, 20], 3);
L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
    attribution: '&copy; <a href="https://openstreetmap.org">OpenStreetMap</a> &copy; <a href="https://carto.com">CARTO</a>',
    subdomains: 'abcd',
    maxZoom: 19,
}).addTo(map);

function esc(s) { return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;'); }

function prColor(pct) {
    if (pct <= 0.01) return '#ffd700';   // top 1%  — gold
    if (pct <= 0.05) return '#fd7e14';   // top 5%  — orange
    if (pct <= 0.20) return '#0dcaf0';   // top 20% — teal
    return '#2d3245';                     // rest    — dark (barely visible on dark map)
}

function prRadius(norm) {
    return 2 + norm * 18;   // 2 px (min) … 20 px (max)
}

async function load() {
    try {
        const r    = await fetch('/demos/graph_pagerank/data');
        const data = await r.json();

        if (data.error) {
            document.getElementById('loading-row').innerHTML =
                `<span class="text-danger">Error: ${esc(data.error)}</span>`;
            return;
        }

        // ── Markers — render top cities with larger, brighter dots ────────────
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

        // ── Stats badge ───────────────────────────────────────────────────────
        const badge = document.getElementById('stats-badge');
        badge.textContent = `${data.n_cities.toLocaleString()} cities · ${data.n_edges.toLocaleString()} roads`;
        badge.className   = 'badge bg-success ms-auto';

        // ── Loading row → hide ────────────────────────────────────────────────
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
