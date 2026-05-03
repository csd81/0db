/* log_shipping.js — 3-Panel Log Shipping Demo */

document.addEventListener('DOMContentLoaded', () => {
  const startBtn   = document.getElementById('start-btn');
  const phaseBadge = document.getElementById('phase-badge');
  const ticker     = document.getElementById('sql-ticker');

  let lastSql = '';
  let lastReplicaIds = new Set();
  let pollTimer = null;

  const phaseMap = {
    idle:   ['bg-secondary', 'Idle'],
    done:   ['bg-primary', 'Done ✓'],
    error:  ['bg-danger', 'Error'],
  };

  function updatePhase(state) {
    let cls, label;
    if (state.phase === 'active') {
      cls = 'bg-success';
      label = `Active — cycle ${state.cycle}/${state.total_cycles}`;
    } else if (state.phase === 'gap') {
      cls = 'bg-warning text-dark';
      label = `Gap — ${state.countdown}s`;
    } else if (state.phase === 'replay') {
      cls = 'bg-info';
      label = `Replaying — ${state.replayed}/${state.log_count}`;
    } else {
      const entry = phaseMap[state.phase] || ['bg-secondary', state.phase];
      [cls, label] = entry;
    }
    phaseBadge.className = 'badge fs-6 ' + cls;
    phaseBadge.textContent = label;
  }

  function updateTicker(sql) {
    if (!sql || sql === lastSql) return;
    lastSql = sql;
    ticker.textContent += '\n> ' + sql;
    ticker.scrollTop = ticker.scrollHeight;
  }

  function esc(s) {
    return String(s ?? '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  }

  function statusBadge(status) {
    const map = {
      pending:    'bg-secondary',
      processing: 'bg-primary',
      shipped:    'bg-success',
      cancelled:  'bg-danger',
    };
    return map[status] || 'bg-secondary';
  }

  function renderMaster(rows) {
    const tbody = document.getElementById('tbl-master-body');
    const badge = document.getElementById('badge-master-count');
    badge.textContent = rows.length + ' rows';
    if (!rows.length) {
      tbody.innerHTML = '<tr><td colspan="6" class="text-muted text-center py-3">Empty</td></tr>';
      return;
    }
    tbody.innerHTML = rows.map(r =>
      `<tr>` +
      `<td>${esc(r.id)}</td>` +
      `<td>${esc(r.customer)}</td>` +
      `<td>${esc(r.product)}</td>` +
      `<td>${esc(r.qty)}</td>` +
      `<td>${esc(r.price)}</td>` +
      `<td><span class="badge ${statusBadge(r.status)}">${esc(r.status)}</span></td>` +
      `</tr>`
    ).join('');
  }

  function renderLog(entries) {
    const tbody = document.getElementById('tbl-log-body');
    const badge = document.getElementById('badge-log-count');
    const scrollDiv = document.getElementById('log-scroll');
    badge.textContent = entries.length + ' entries';
    if (!entries.length) {
      tbody.innerHTML = '<tr><td colspan="5" class="text-muted text-center py-3">Empty</td></tr>';
      return;
    }
    const atBottom = scrollDiv
      ? (scrollDiv.scrollHeight - scrollDiv.scrollTop - scrollDiv.clientHeight) < 40
      : true;
    tbody.innerHTML = entries.map(e => {
      const rowCls = e.operation === 'INSERT' ? 'table-success'
                   : e.operation === 'UPDATE' ? 'table-warning'
                   : 'table-danger';
      const ts = (e.ts || '').split(' ')[1] || (e.ts || '');
      const sqlShort = (e.sql_text || '').length > 42
        ? esc(e.sql_text.substring(0, 42)) + '…'
        : esc(e.sql_text || '');
      return `<tr class="${rowCls}">` +
        `<td>${esc(e.seq)}</td>` +
        `<td><strong>${esc(e.operation)}</strong></td>` +
        `<td>${esc(e.row_id)}</td>` +
        `<td class="font-monospace" style="font-size:.78rem;" title="${esc(e.sql_text)}">${sqlShort}</td>` +
        `<td class="small">${esc(ts)}</td>` +
        `</tr>`;
    }).join('');
    if (atBottom && scrollDiv) scrollDiv.scrollTop = scrollDiv.scrollHeight;
  }

  function renderReplica(rows) {
    const tbody = document.getElementById('tbl-replica-body');
    const badge = document.getElementById('badge-replica-count');
    badge.textContent = rows.length + ' rows';
    if (!rows.length) {
      tbody.innerHTML = '<tr><td colspan="6" class="text-muted text-center py-3">Waiting for replay…</td></tr>';
      lastReplicaIds = new Set();
      return;
    }
    const currentIds = new Set(rows.map(r => r.id));
    tbody.innerHTML = rows.map(r => {
      const isNew = !lastReplicaIds.has(r.id);
      const rowCls = isNew ? 'table-success' : '';
      return `<tr class="${rowCls}">` +
        `<td>${esc(r.id)}</td>` +
        `<td>${esc(r.customer)}</td>` +
        `<td>${esc(r.product)}</td>` +
        `<td>${esc(r.qty)}</td>` +
        `<td>${esc(r.price)}</td>` +
        `<td><span class="badge ${statusBadge(r.status)}">${esc(r.status)}</span></td>` +
        `</tr>`;
    }).join('');
    lastReplicaIds = currentIds;
  }

  function poll() {
    fetch('/demos/log-shipping/state')
      .then(r => r.json())
      .then(state => {
        updatePhase(state);
        updateTicker(state.current_sql);
        renderMaster(state.master_rows || []);
        renderLog(state.log_entries || []);
        renderReplica(state.replica_rows || []);
      })
      .catch(() => {});
  }

  if (startBtn) {
    startBtn.addEventListener('click', () => {
      startBtn.disabled = true;
      ticker.textContent = '-- Starting…';
      lastSql = '';
      lastReplicaIds = new Set();

      fetch('/demos/log-shipping/start', { method: 'POST' })
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
