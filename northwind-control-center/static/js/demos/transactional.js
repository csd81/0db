/* transactional.js — Transactional Replication Demo (orders/balances/inventory) */

document.addEventListener('DOMContentLoaded', () => {
  const startBtn    = document.getElementById('start-btn');
  const stopBtn     = document.getElementById('stop-btn');
  const statusBadge = document.getElementById('status-badge');
  const txBadge     = document.getElementById('tx-badge');
  const okBadge     = document.getElementById('ok-badge');
  const failBadge   = document.getElementById('fail-badge');
  const ticker      = document.getElementById('sql-ticker');

  let lastSql         = '';
  let lastPubOrderIds = new Set();
  let lastSubOrderIds = new Set();
  let prevPubBal      = {};   // customer → balance
  let prevSubBal      = {};
  let prevPubInv      = {};   // item → stock
  let prevSubInv      = {};
  let pollTimer       = null;

  function esc(s) {
    return String(s ?? '').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
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

  // ── Status badges ───────────────────────────────────────────────────────────

  function updateStatus(running, txCount, okCount, failCount) {
    if (running) {
      statusBadge.className = 'badge bg-success fs-6';
      statusBadge.textContent = 'Running';
      startBtn.disabled = true;
      stopBtn.disabled  = false;
    } else {
      statusBadge.className = 'badge bg-secondary fs-6';
      statusBadge.textContent = 'Stopped';
      startBtn.disabled = false;
      stopBtn.disabled  = true;
    }
    txBadge.textContent   = txCount   + ' tx';
    okBadge.textContent   = okCount   + ' OK';
    failBadge.textContent = failCount + ' fail';
  }

  // ── Orders table (Publisher & Subscriber) ───────────────────────────────────

  function renderOrders(tbodyId, badgeId, rows, seenIds) {
    const tbody = document.getElementById(tbodyId);
    const badge = document.getElementById(badgeId);
    badge.textContent = rows.length;
    if (!rows.length) {
      tbody.innerHTML = '<tr><td colspan="6" class="text-muted text-center py-2">—</td></tr>';
      return seenIds;
    }
    const newIds = new Set(rows.map(r => r.id));
    tbody.innerHTML = rows.map(r => {
      const isNew  = !seenIds.has(r.id);
      const isFail = r.status === 'failed';
      const cls    = isFail ? 'table-danger' : (isNew ? 'table-success' : '');
      return `<tr class="${cls}">` +
        `<td>${esc(r.id)}</td>` +
        `<td>${esc(r.customer)}</td>` +
        `<td>${esc(r.item)}</td>` +
        `<td>${esc(r.qty)}</td>` +
        `<td>${esc(r.amount != null ? r.amount.toFixed(2) : '')}</td>` +
        `<td><small>${esc(r.status)}</small></td>` +
        `</tr>`;
    }).join('');
    return newIds;
  }

  // ── Balances table ──────────────────────────────────────────────────────────

  function renderBalances(tbodyId, badgeId, rows, prevBal) {
    const tbody = document.getElementById(tbodyId);
    const badge = document.getElementById(badgeId);
    badge.textContent = rows.length;
    if (!rows.length) {
      tbody.innerHTML = '<tr><td colspan="2" class="text-muted text-center py-2">—</td></tr>';
      return prevBal;
    }
    const newBal = {};
    rows.forEach(r => { newBal[r.customer] = r.balance; });
    tbody.innerHTML = rows.map(r => {
      const prev    = prevBal[r.customer];
      const changed = prev !== undefined && prev !== r.balance;
      const cls     = changed ? 'table-warning' : '';
      const arrow   = changed
        ? (r.balance > prev ? ' <span class="text-success">▲</span>' : ' <span class="text-danger">▼</span>')
        : '';
      return `<tr class="${cls}">` +
        `<td><strong>${esc(r.customer)}</strong></td>` +
        `<td>${r.balance != null ? r.balance.toFixed(2) : ''}${arrow}</td>` +
        `</tr>`;
    }).join('');
    return newBal;
  }

  // ── Inventory table ─────────────────────────────────────────────────────────

  function renderInventory(tbodyId, badgeId, rows, prevInv) {
    const tbody = document.getElementById(tbodyId);
    const badge = document.getElementById(badgeId);
    badge.textContent = rows.length;
    if (!rows.length) {
      tbody.innerHTML = '<tr><td colspan="3" class="text-muted text-center py-2">—</td></tr>';
      return prevInv;
    }
    const newInv = {};
    rows.forEach(r => { newInv[r.item] = r.stock; });
    tbody.innerHTML = rows.map(r => {
      const prev    = prevInv[r.item];
      const changed = prev !== undefined && prev !== r.stock;
      const cls     = changed ? (r.stock < prev ? 'table-warning' : 'table-success') : '';
      const arrow   = changed
        ? (r.stock > prev ? ' <span class="text-success">▲</span>' : ' <span class="text-danger">▼</span>')
        : '';
      return `<tr class="${cls}">` +
        `<td>${esc(r.item)}</td>` +
        `<td>${esc(r.stock)}${arrow}</td>` +
        `<td>${r.price != null ? r.price.toFixed(2) : ''}</td>` +
        `</tr>`;
    }).join('');
    return newInv;
  }

  // ── Distributor log ─────────────────────────────────────────────────────────

  function renderDist(rows) {
    const tbody = document.getElementById('tbl-dist');
    const badge = document.getElementById('badge-dist');
    const pending = rows.filter(r => r.status === 'pending').length;
    badge.textContent = pending > 0 ? pending + ' pending' : rows.length + ' entries';
    if (!rows.length) {
      tbody.innerHTML = '<tr><td colspan="3" class="text-muted text-center py-2">Queue empty</td></tr>';
      return;
    }
    tbody.innerHTML = rows.map(r => {
      const isPending = r.status === 'pending';
      const rowCls    = isPending ? 'table-warning fw-bold' : 'text-muted';
      const sql       = (r.op_sql || '').substring(0, 48) + ((r.op_sql || '').length > 48 ? '…' : '');
      const statusHtml = isPending
        ? '<span class="badge bg-warning text-dark">⏳</span>'
        : '<span class="text-success small">✓</span>';
      return `<tr class="${rowCls}">` +
        `<td>${esc(r.id)}</td>` +
        `<td style="font-size:.72rem;font-family:monospace">${esc(sql)}</td>` +
        `<td>${statusHtml}</td>` +
        `</tr>`;
    }).join('');
  }

  // ── Company account ─────────────────────────────────────────────────────────

  let prevPubCompany = 0;
  let prevSubCompany = 0;

  function renderCompany(elId, rows, prevBal) {
    const el  = document.getElementById(elId);
    const bal = rows.length ? (rows[0].balance ?? 0) : 0;
    el.textContent = '$' + bal.toFixed(2);
    if (bal > prevBal) {
      el.classList.add('text-success');
      el.classList.remove('text-danger');
    } else if (bal < prevBal) {
      el.classList.add('text-danger');
      el.classList.remove('text-success');
    }
    return bal;
  }

  // ── Poll ────────────────────────────────────────────────────────────────────

  function poll() {
    fetch('/demos/transactional/state')
      .then(r => r.json())
      .then(state => {
        updateStatus(state.running, state.tx_count, state.success_count, state.fail_count);
        updateTicker(state.current_sql);

        lastPubOrderIds = renderOrders('tbl-pub-orders', 'badge-pub-orders',
                                       state.pub_orders   || [], lastPubOrderIds);
        prevPubBal      = renderBalances('tbl-pub-balances', 'badge-pub-balances',
                                         state.pub_balances || [], prevPubBal);
        prevPubInv      = renderInventory('tbl-pub-inventory', 'badge-pub-inventory',
                                          state.pub_inventory || [], prevPubInv);
        prevPubCompany  = renderCompany('pub-company-bal', state.pub_company || [], prevPubCompany);

        renderDist(state.dist_log || []);

        lastSubOrderIds = renderOrders('tbl-sub-orders', 'badge-sub-orders',
                                       state.sub_orders   || [], lastSubOrderIds);
        prevSubBal      = renderBalances('tbl-sub-balances', 'badge-sub-balances',
                                         state.sub_balances || [], prevSubBal);
        prevSubInv      = renderInventory('tbl-sub-inventory', 'badge-sub-inventory',
                                          state.sub_inventory || [], prevSubInv);
        prevSubCompany  = renderCompany('sub-company-bal', state.sub_company || [], prevSubCompany);
      })
      .catch(() => {});
  }

  // ── Buttons ─────────────────────────────────────────────────────────────────

  startBtn.addEventListener('click', () => {
    startBtn.disabled = true;
    ticker.textContent = '-- Starting transactional replication stream…';
    lastSql = '';
    lastPubOrderIds = new Set();
    lastSubOrderIds = new Set();
    prevPubBal = {}; prevSubBal = {};
    prevPubInv = {}; prevSubInv = {};
    fetch('/demos/transactional/start', { method: 'POST' })
      .then(() => poll())
      .catch(() => { startBtn.disabled = false; });
  });

  stopBtn.addEventListener('click', () => {
    stopBtn.disabled = true;
    fetch('/demos/transactional/stop', { method: 'POST' })
      .then(() => poll())
      .catch(() => {});
  });

  // ── Init ────────────────────────────────────────────────────────────────────

  poll();
  pollTimer = setInterval(poll, 500);

  window.addEventListener('beforeunload', () => {
    if (pollTimer) clearInterval(pollTimer);
  });
});
