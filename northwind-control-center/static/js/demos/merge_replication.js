/* merge_replication.js — Merge Replication Last-Mile Delivery Demo */

document.addEventListener('DOMContentLoaded', () => {
  const startBtn      = document.getElementById('start-btn');
  const stopBtn       = document.getElementById('stop-btn');
  const phaseBadge    = document.getElementById('phase-badge');
  const syncBadge     = document.getElementById('sync-badge');
  const conflictBadge = document.getElementById('conflict-badge');
  const ticker        = document.getElementById('sql-ticker');
  const offlineBanner = document.getElementById('offline-banner');
  const offlineChip   = document.getElementById('offline-chip');
  const countdownVal  = document.getElementById('countdown-val');

  let lastSql         = '';
  let prevCentralDirty = {};  // id → dirty value
  let prevDriverDirty  = {};
  let pollTimer        = null;

  function esc(s) {
    return String(s ?? '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  }

  function fmtTime(ts) {
    return (ts || '').split(' ')[1] || ts || '';
  }

  // ── Ticker ─────────────────────────────────────────────────────────────────

  function updateTicker(sql) {
    if (!sql || sql === lastSql) return;
    lastSql = sql;
    ticker.textContent += '\n> ' + sql;
    ticker.scrollTop = ticker.scrollHeight;
  }

  // ── Phase badge ─────────────────────────────────────────────────────────────

  const phaseMap = {
    idle:           ['bg-secondary',           'Idle'],
    starting:       ['bg-info text-dark',       'Starting…'],
    central_update: ['bg-primary',              'Central Office updating'],
    driver_update:  ['bg-info text-dark',       'Driver updating (offline)'],
    offline:        ['bg-warning text-dark',    'Driver offline'],
    syncing:        ['bg-danger',               'Merge Agent syncing'],
    synced:         ['bg-success',              'Sync complete'],
  };

  function updateStatus(state) {
    const [cls, label] = phaseMap[state.phase] || ['bg-secondary', state.phase];
    phaseBadge.className = 'badge fs-6 ' + cls;
    phaseBadge.textContent = state.phase === 'offline'
      ? `Offline — ${state.offline_countdown}s`
      : label;

    syncBadge.textContent     = state.sync_count     + ' syncs';
    conflictBadge.textContent = state.conflict_count + ' conflicts';

    const isOffline = state.phase === 'offline' || state.phase === 'driver_update';
    offlineBanner.classList.toggle('d-none', !isOffline);
    offlineChip.classList.toggle('d-none',   !isOffline);
    if (isOffline && state.offline_countdown > 0) {
      countdownVal.textContent = state.offline_countdown;
    }

    if (state.running) {
      startBtn.disabled = true;
      stopBtn.disabled  = false;
    } else {
      startBtn.disabled = false;
      stopBtn.disabled  = true;
    }
  }

  // ── Status badge helper ─────────────────────────────────────────────────────

  function statusBadge(status) {
    const map = {
      pending:   'bg-secondary',
      delivered: 'bg-success',
      cancelled: 'bg-danger',
      failed:    'bg-warning text-dark',
    };
    const cls = map[status] || 'bg-secondary';
    return `<span class="badge ${cls}">${esc(status)}</span>`;
  }

  // ── Delivery table renderer ─────────────────────────────────────────────────

  function renderDeliveryTable(tbodyId, badgeId, rows, prevDirty) {
    const tbody = document.getElementById(tbodyId);
    const badge = document.getElementById(badgeId);
    const dirty = rows.filter(r => r.dirty).length;
    badge.textContent = dirty > 0 ? `${dirty} dirty` : `${rows.length} rows`;

    if (!rows.length) {
      tbody.innerHTML = '<tr><td colspan="4" class="text-muted text-center py-2">—</td></tr>';
      return {};
    }

    const newDirty = {};
    rows.forEach(r => { newDirty[r.id] = r.dirty; });

    tbody.innerHTML = rows.map(r => {
      const wasDirty  = prevDirty[r.id];
      const isDirty   = r.dirty === 1;
      const justDirty = !wasDirty && isDirty;
      const cls = isDirty ? 'table-warning' : (justDirty ? 'table-info' : '');
      const dirtyMark = isDirty ? ' <span title="pending sync">⚡</span>' : '';
      const notes = (r.notes || '').substring(0, 18) + ((r.notes || '').length > 18 ? '…' : '');
      return `<tr class="${cls}">` +
        `<td><strong>${esc(r.package_id)}</strong></td>` +
        `<td>${esc(r.customer)}</td>` +
        `<td>${statusBadge(r.status)}${dirtyMark}</td>` +
        `<td style="font-size:.72rem">${esc(notes)}</td>` +
        `</tr>`;
    }).join('');

    return newDirty;
  }

  // ── Merge log renderer ──────────────────────────────────────────────────────

  const eventMap = {
    sync_start: ['bg-info text-dark',    '▶',  ''],
    push:       ['bg-primary',           '↑',  'table-primary'],
    pull:       ['bg-secondary',         '↓',  ''],
    conflict:   ['bg-danger',            '⚡', 'table-danger'],
    resolved:   ['bg-warning text-dark', '✓',  'table-warning'],
    sync_done:  ['bg-success',           '✔',  'table-success'],
  };

  function renderMergeLog(rows) {
    const tbody = document.getElementById('tbl-merge');
    const badge = document.getElementById('badge-merge');
    badge.textContent = rows.length;

    if (!rows.length) {
      tbody.innerHTML = '<tr><td colspan="3" class="text-muted text-center py-2">Log empty</td></tr>';
      return;
    }

    tbody.innerHTML = rows.map(r => {
      const [badgeCls, icon, rowCls] = eventMap[r.event_type] || ['bg-secondary', '?', ''];
      const desc = (r.description || '').substring(0, 42) + ((r.description || '').length > 42 ? '…' : '');
      return `<tr class="${rowCls}">` +
        `<td><span class="badge ${badgeCls}">${icon} ${esc(r.event_type)}</span></td>` +
        `<td><small>${esc(r.package_id)}</small></td>` +
        `<td style="font-size:.72rem">${esc(desc)}</td>` +
        `</tr>`;
    }).join('');
  }

  // ── Poll ────────────────────────────────────────────────────────────────────

  function poll() {
    fetch('/demos/merge-replication/state')
      .then(r => r.json())
      .then(state => {
        updateTicker(state.current_sql);
        updateStatus(state);
        prevCentralDirty = renderDeliveryTable(
          'tbl-central', 'badge-central', state.central_rows || [], prevCentralDirty
        );
        renderMergeLog(state.merge_log || []);
        prevDriverDirty = renderDeliveryTable(
          'tbl-driver', 'badge-driver', state.driver_rows || [], prevDriverDirty
        );
      })
      .catch(() => {});
  }

  // ── Buttons ─────────────────────────────────────────────────────────────────

  startBtn.addEventListener('click', () => {
    startBtn.disabled = true;
    ticker.textContent = '-- Initializing Last-Mile Delivery simulation…';
    lastSql = '';
    prevCentralDirty = {};
    prevDriverDirty  = {};
    fetch('/demos/merge-replication/start', { method: 'POST' })
      .then(() => poll())
      .catch(() => { startBtn.disabled = false; });
  });

  stopBtn.addEventListener('click', () => {
    stopBtn.disabled = true;
    fetch('/demos/merge-replication/stop', { method: 'POST' })
      .then(() => poll())
      .catch(() => {});
  });

  // ── Init ────────────────────────────────────────────────────────────────────

  poll();
  pollTimer = setInterval(poll, 600);

  window.addEventListener('beforeunload', () => {
    if (pollTimer) clearInterval(pollTimer);
  });
});
