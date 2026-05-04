'use strict';

const map = L.map('map-container', {zoomControl: true}).setView([30, 55], 3);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© <a href="https://openstreetmap.org/copyright">OpenStreetMap</a> contributors',
    maxZoom: 18,
}).addTo(map);

function esc(s) { return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;'); }

function prColor(pct) {
    if (pct <= 0.01) return '#ffd700';   // top 1%  — gold
    if (pct <= 0.05) return '#fd7e14';   // top 5%  — orange
    if (pct <= 0.20) return '#0dcaf0';   // top 20% — teal
    return '#6c757d';                     // rest    — gray
}

function prRadius(norm) {
    return 2 + norm * 16;   // 2 px (min) … 18 px (max)
}

async function load() {
    try {
        const r    = await fetch('/demos/graph_pagerank/data');
        const data = await r.json();

        if (data.error) {
            document.getElementById('loading-overlay').textContent = 'Error: ' + data.error;
            return;
        }

        // ── Markers ──────────────────────────────────────────────────────────
        for (const c of data.cities) {
            const color  = prColor(c.pr_pct);
            const radius = prRadius(c.pr_norm);
            L.circleMarker([c.lat, c.lng], {
                radius,
                color,
                fillColor:   color,
                fillOpacity: 0.85,
                weight:      c.pr_pct <= 0.01 ? 2 : 1,
            })
            .bindTooltip(
                `<b>${esc(c.name)}</b> (${esc(c.country)})<br>` +
                `Rank: #${c.pr_rank} of ${data.n_cities}<br>` +
                `Pop: ${c.population.toLocaleString()}<br>` +
                `PR score: ${c.pr_norm.toFixed(3)}`,
                {sticky: true}
            )
            .addTo(map);
        }

        // ── Stats badge ───────────────────────────────────────────────────────
        document.getElementById('stats-badge').textContent =
            `${data.n_cities.toLocaleString()} cities · ${data.n_edges.toLocaleString()} roads`;
        document.getElementById('stats-badge').className = 'badge bg-success';

        // ── Top-25 table ──────────────────────────────────────────────────────
        const tbody = document.getElementById('rank-body');
        tbody.innerHTML = data.top25.map(c => {
            const barW = Math.round(c.pr_norm * 60);
            return `<tr>
              <td class="text-muted">${c.pr_rank}</td>
              <td><strong>${esc(c.name)}</strong></td>
              <td>${esc(c.country)}</td>
              <td>
                <span class="pr-bar" style="width:${barW}px"></span>
                <span class="ms-1 text-muted">${c.pr_norm.toFixed(3)}</span>
              </td>
            </tr>`;
        }).join('');

        // ── Hide overlay ──────────────────────────────────────────────────────
        document.getElementById('loading-overlay').style.display = 'none';

    } catch (e) {
        document.getElementById('loading-overlay').textContent = 'Network error — ' + e.message;
    }
}

load();
