/* snapshot.js — Snapshot Replication Demo */

window.addEventListener('beforeunload', () => {});

document.addEventListener('DOMContentLoaded', () => {
  const startBtn   = document.getElementById('start-btn');
  const phaseBadge = document.getElementById('phase-badge');
  const ticker     = document.getElementById('sql-ticker');

  let lastSql = '';
  let lastDistRows = 0;
  let lastSubRows  = 0;
  let pollTimer    = null;

  // ── Phase badge ──────────────────────────────────────────────────────────────

  function updatePhase(state) {
    let cls, label;
    switch (state.phase) {
      case 'filling':
        cls = 'bg-primary'; label = `Filling publisher — ${state.filled}/${state.total}`; break;
      case 'gap':
        cls = 'bg-secondary'; label = `Scheduled gap — ${state.countdown}s`; break;
      case 'snapshot':
        cls = 'bg-warning text-dark'; label = 'BCP Snapshot → Distributor'; break;
      case 'push_a':
        cls = 'bg-info'; label = 'Push → Sub A'; break;
      case 'push_b':
        cls = 'bg-info'; label = 'Push → Sub B'; break;
      case 'push_c':
        cls = 'bg-info'; label = 'Push → Sub C'; break;
      case 'done':
        cls = 'bg-success'; label = 'Done ✓ — All subscribers in sync'; break;
      case 'error':
        cls = 'bg-danger'; label = 'Error'; break;
      default:
        cls = 'bg-secondary'; label = 'Idle';
    }
    phaseBadge.className = 'badge fs-6 ' + cls;
    phaseBadge.textContent = label;
  }

  // ── SQL Ticker ───────────────────────────────────────────────────────────────

  function updateTicker(sql) {
    if (!sql || sql === lastSql) return;
    lastSql = sql;
    ticker.textContent += '\n' + sql;
    ticker.scrollTop = ticker.scrollHeight;
  }

  // ── Table renderers ──────────────────────────────────────────────────────────

  function esc(s) {
    return String(s ?? '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  }

  function renderCurrencyTable(tbodyId, badgeId, rows, badgeText, emptyMsg, highlightNew) {
    const tbody = document.getElementById(tbodyId);
    const badge = document.getElementById(badgeId);
    if (badge) badge.textContent = badgeText;
    if (!rows || !rows.length) {
      tbody.innerHTML = `<tr><td colspan="4" class="text-muted text-center py-3">${emptyMsg}</td></tr>`;
      return;
    }
    const prevCount = highlightNew ? (tbodyId === 'tbl-dist-body' ? lastDistRows : lastSubRows) : rows.length;
    tbody.innerHTML = rows.map((r, i) => {
      const isNew = highlightNew && i >= prevCount;
      const cls = isNew ? 'table-success' : '';
      return `<tr class="${cls}">` +
        `<td>${esc(r.id)}</td><td><strong>${esc(r.currency_from)}</strong></td>` +
        `<td>${esc(r.currency_to)}</td><td>${esc(r.rate)}</td></tr>`;
    }).join('');
    // scroll to bottom when new rows appear
    if (highlightNew) {
      const wrapper = tbody.closest('.card-body');
      if (wrapper) wrapper.scrollTop = wrapper.scrollHeight;
    }
  }

  function renderTables(state) {
    // Publisher: rows appear one by one (no highlight needed — always growing)
    renderCurrencyTable(
      'tbl-pub-body', 'badge-pub-count',
      state.publisher_rows, state.publisher_rows.length + ' rows',
      'Empty', false
    );

    // Distributor: appears all at once (BCP) — highlight all as new when first filled
    const distNew = state.distributor_rows.length > 0 && lastDistRows === 0;
    renderCurrencyTable(
      'tbl-dist-body', 'badge-dist-count',
      state.distributor_rows, state.distributor_rows.length + ' rows (BCP)',
      'Empty — waiting for BCP snapshot', distNew
    );
    if (state.distributor_rows.length > 0) lastDistRows = state.distributor_rows.length;

    // Subscribers: show whichever is furthest along (a > b > c)
    const subRows = state.sub_c_rows?.length ? state.sub_c_rows
                  : state.sub_b_rows?.length ? state.sub_b_rows
                  : state.sub_a_rows?.length ? state.sub_a_rows
                  : [];
    const syncedCount = (state.sub_a_ready ? 1 : 0) + (state.sub_b_ready ? 1 : 0) + (state.sub_c_ready ? 1 : 0);
    const subNew = subRows.length > 0 && lastSubRows === 0;
    renderCurrencyTable(
      'tbl-sub-body', 'badge-sub-count',
      subRows, `${syncedCount} / 3 synced`,
      'Waiting for push…', subNew
    );
    if (subRows.length > 0) lastSubRows = subRows.length;
  }

  // ── SVG Topology graph ───────────────────────────────────────────────────────

  function setNode(circleId, labelId, fill, stroke, labelText) {
    const c = document.getElementById(circleId);
    if (c) {
      c.setAttribute('fill', fill);
      c.setAttribute('stroke', stroke);
    }
    const l = document.getElementById(labelId);
    if (l) l.textContent = labelText;
  }

  function setEdge(edgeId, state) {
    const el = document.getElementById(edgeId);
    if (!el) return;
    if (state === 'done') {
      el.setAttribute('stroke', '#198754');
      el.setAttribute('stroke-dasharray', 'none');
      el.setAttribute('marker-end', 'url(#arr-done)');
      el.classList.remove('edge-active');
    } else if (state === 'active') {
      el.setAttribute('stroke', '#ffc107');
      el.setAttribute('stroke-dasharray', '10,5');
      el.setAttribute('marker-end', 'url(#arr-act)');
      el.classList.add('edge-active');
    } else {
      el.setAttribute('stroke', '#6c757d');
      el.setAttribute('stroke-dasharray', '10,5');
      el.setAttribute('marker-end', 'url(#arr-idle)');
      el.classList.remove('edge-active');
    }
  }

  function updateGraph(state) {
    const ph = state.phase;
    const pubFilled = state.filled > 0;

    // Publisher node
    setNode('node-pub', 'label-pub',
      pubFilled ? '#0d6efd' : '#1a1a1a',
      pubFilled ? '#0d6efd' : '#6c757d',
      pubFilled ? `${state.filled} rows` : 'empty'
    );

    // Edge P→D
    const pdDone   = state.dist_ready;
    const pdActive = ph === 'snapshot';
    setEdge('edge-pd', pdDone ? 'done' : (pdActive ? 'active' : 'idle'));

    // Distributor node
    setNode('node-dist', 'label-dist',
      state.dist_ready ? '#fd7e14' : '#1a1a1a',
      state.dist_ready ? '#fd7e14' : '#6c757d',
      state.dist_ready ? `${state.distributor_rows?.length ?? 20} rows` : 'empty'
    );

    // Edge D→A
    setEdge('edge-da', state.sub_a_ready ? 'done' : (ph === 'push_a' ? 'active' : 'idle'));
    setNode('node-suba', 'label-suba',
      state.sub_a_ready ? '#198754' : '#1a1a1a',
      state.sub_a_ready ? '#198754' : '#6c757d',
      state.sub_a_ready ? '✓ synced' : '—'
    );

    // Edge D→B
    setEdge('edge-db', state.sub_b_ready ? 'done' : (ph === 'push_b' ? 'active' : 'idle'));
    setNode('node-subb', 'label-subb',
      state.sub_b_ready ? '#198754' : '#1a1a1a',
      state.sub_b_ready ? '#198754' : '#6c757d',
      state.sub_b_ready ? '✓ synced' : '—'
    );

    // Edge D→C
    setEdge('edge-dc', state.sub_c_ready ? 'done' : (ph === 'push_c' ? 'active' : 'idle'));
    setNode('node-subc', 'label-subc',
      state.sub_c_ready ? '#198754' : '#1a1a1a',
      state.sub_c_ready ? '#198754' : '#6c757d',
      state.sub_c_ready ? '✓ synced' : '—'
    );
  }

  // ── Poll ─────────────────────────────────────────────────────────────────────

  function poll() {
    fetch('/demos/snapshot/state')
      .then(r => r.json())
      .then(state => {
        updatePhase(state);
        updateTicker(state.current_sql);
        renderTables(state);
        updateGraph(state);
      })
      .catch(() => {});
  }

  // ── Start button ─────────────────────────────────────────────────────────────

  if (startBtn) {
    startBtn.addEventListener('click', () => {
      startBtn.disabled = true;
      ticker.textContent = '-- Starting snapshot replication demo…';
      lastSql = '';
      lastDistRows = 0;
      lastSubRows  = 0;

      fetch('/demos/snapshot/start', { method: 'POST' })
        .then(r => r.json())
        .then(() => {
          poll();
          startBtn.disabled = false;
        })
        .catch(() => { startBtn.disabled = false; });
    });
  }

  poll();
  pollTimer = setInterval(poll, 800);

  window.addEventListener('beforeunload', () => {
    if (pollTimer) clearInterval(pollTimer);
  });
});
