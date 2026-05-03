/* nasdaq.js — NASDAQ simulation demo */

document.addEventListener('DOMContentLoaded', () => {
  const startBtn    = document.getElementById('start-btn');
  const stopBtn     = document.getElementById('stop-btn');
  const marketBadge = document.getElementById('market-badge');
  const priceBadge  = document.getElementById('price-badge');
  const tradeBadge  = document.getElementById('trade-badge');
  const settleBadge = document.getElementById('settle-badge');
  const spreadVal   = document.getElementById('spread-val');
  const cycleBadge  = document.getElementById('cycle-badge');
  const ticker      = document.getElementById('sql-ticker');

  let lastSql       = '';
  let prevHoldings  = {};       // broker → { shares, cash }
  let knownSettled  = new Set();
  let prevTradeId   = 0;
  let pollTimer     = null;

  function esc(s) {
    return String(s ?? '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  }

  // ── Ticker ──────────────────────────────────────────────────────────────────

  function updateTicker(sql) {
    if (!sql || sql === lastSql) return;
    lastSql = sql;
    ticker.textContent += '\n> ' + sql;
    ticker.scrollTop = ticker.scrollHeight;
  }

  // ── Market status + header badges ───────────────────────────────────────────

  const phaseMap = {
    closed:          ['bg-danger',           'CLOSED'],
    opening_auction: ['bg-warning text-dark', 'OPENING AUCTION 🔔'],
    trading:         ['bg-success',           'OPEN'],
    closing_auction: ['bg-warning text-dark', 'CLOSING AUCTION 🔔'],
    settlement:      ['bg-info text-dark',    'AFTER-HOURS · SETTLEMENT'],
    starting:        ['bg-secondary',         'Starting…'],
    idle:            ['bg-secondary',         'Idle'],
  };

  function renderMarket(state) {
    const [cls, label] = phaseMap[state.phase] || ['bg-secondary', state.phase];
    marketBadge.className   = 'badge fs-6 ' + cls;
    marketBadge.textContent = label;

    priceBadge.textContent  = state.last_price != null
      ? '$ ' + Number(state.last_price).toFixed(2)
      : '$—';
    tradeBadge.textContent  = (state.trade_count ?? 0) + ' trades';
    settleBadge.textContent = (state.pending_settlements ?? 0) + ' pending T+1';
    if (cycleBadge) cycleBadge.textContent = state.cycle ?? 0;

    if (state.running) {
      startBtn.disabled = true;
      stopBtn.disabled  = false;
    } else {
      startBtn.disabled = false;
      stopBtn.disabled  = true;
    }
  }

  // ── Order flow: Retail + HFT ─────────────────────────────────────────────────

  function renderOrders(orders) {
    const retail = orders.filter(o => o.broker_type === 'retail');
    const hft    = orders.filter(o => o.broker_type === 'hft');

    const makeTbody = (rows, empty) => {
      if (!rows.length) return `<tr><td colspan="4" class="text-muted text-center py-2">${empty}</td></tr>`;
      return rows.map(o => {
        const sideCls = o.side === 'buy' ? 'text-success' : 'text-danger';
        return `<tr>
          <td>${esc(o.broker)}</td>
          <td class="${sideCls} fw-bold">${esc(o.side)}</td>
          <td>${esc(o.qty)}</td>
          <td>${Number(o.price).toFixed(2)}</td>
        </tr>`;
      }).join('');
    };

    document.getElementById('tbl-retail').innerHTML = makeTbody(retail, '—');

    const hftBody = document.getElementById('tbl-hft');
    if (!hft.length) {
      hftBody.innerHTML = '<tr><td colspan="4" class="text-muted text-center py-2">—</td></tr>';
    } else {
      hftBody.innerHTML = hft.map(o => {
        const sideCls = o.side === 'buy' ? 'text-success' : 'text-danger';
        return `<tr class="table-warning">
          <td><span class="badge bg-warning text-dark" style="font-size:.62rem;">⚡ ${esc(o.broker)}</span></td>
          <td class="${sideCls} fw-bold">${esc(o.side)}</td>
          <td>${esc(o.qty)}</td>
          <td>${Number(o.price).toFixed(2)}</td>
        </tr>`;
      }).join('');
    }
  }

  // ── Order Book ───────────────────────────────────────────────────────────────

  function renderBook(asks, bids, state) {
    const askBody = document.getElementById('tbl-asks');
    if (!asks || !asks.length) {
      askBody.innerHTML = '<tr><td colspan="2" class="text-muted text-center">—</td></tr>';
    } else {
      askBody.innerHTML = asks.map(r =>
        `<tr class="text-danger">
          <td class="fw-bold">${Number(r.price).toFixed(2)}</td>
          <td>${esc(r.qty)}</td>
        </tr>`
      ).join('');
    }

    const bidBody = document.getElementById('tbl-bids');
    if (!bids || !bids.length) {
      bidBody.innerHTML = '<tr><td colspan="2" class="text-muted text-center">—</td></tr>';
    } else {
      bidBody.innerHTML = bids.map(r =>
        `<tr class="text-success">
          <td class="fw-bold">${Number(r.price).toFixed(2)}</td>
          <td>${esc(r.qty)}</td>
        </tr>`
      ).join('');
    }

    const sp = state.spread;
    if (sp != null) {
      spreadVal.textContent = Number(sp).toFixed(2);
      spreadVal.className   = sp > 3 ? 'fw-bold text-danger' : 'fw-bold text-success';
    } else {
      spreadVal.textContent = '—';
    }
  }

  // ── DTCC Settlement Queue ────────────────────────────────────────────────────

  function renderSettlement(rows) {
    const tbody = document.getElementById('tbl-settlement');
    if (!rows || !rows.length) {
      tbody.innerHTML = '<tr><td colspan="5" class="text-muted text-center py-2">No settlements yet</td></tr>';
      return;
    }

    tbody.innerHTML = rows.map(r => {
      const isSettled = r.status === 'settled';
      const statusBadge = isSettled
        ? '<span class="badge bg-success" style="font-size:.62rem;">✓ settled</span>'
        : '<span class="badge bg-warning text-dark" style="font-size:.62rem;">⏳ pending</span>';
      const isNew = isSettled && !knownSettled.has(r.id);
      const rowCls = isNew ? 'table-success' : '';
      if (isSettled) knownSettled.add(r.id);
      return `<tr class="${rowCls}">
        <td class="text-muted">${esc(r.trade_id)}</td>
        <td style="white-space:nowrap;">${esc(r.buyer)} → ${esc(r.seller)}</td>
        <td>${esc(r.qty)}</td>
        <td>${Number(r.price).toFixed(2)}</td>
        <td>${statusBadge}</td>
      </tr>`;
    }).join('');
  }

  // ── DTC Custodian Holdings ───────────────────────────────────────────────────

  function renderHoldings(rows) {
    const tbody = document.getElementById('tbl-custodian');
    if (!rows || !rows.length) {
      tbody.innerHTML = '<tr><td colspan="3" class="text-muted text-center py-2">—</td></tr>';
      return;
    }

    tbody.innerHTML = rows.map(r => {
      const prev    = prevHoldings[r.broker] || {};
      const shrChg  = prev.shares != null && r.shares !== prev.shares;
      const cashChg = prev.cash   != null && Math.abs(r.cash - prev.cash) > 0.01;
      const rowCls  = (shrChg || cashChg) ? 'table-info' : '';

      const shrArrow  = shrChg  ? (r.shares > prev.shares  ? ' <span class="text-success">▲</span>' : ' <span class="text-danger">▼</span>') : '';
      const cashArrow = cashChg ? (r.cash   > prev.cash    ? ' <span class="text-success">▲</span>' : ' <span class="text-danger">▼</span>') : '';

      const btype = r.broker === 'AlgoFast' || r.broker === 'QuantBot'
        ? '<span class="badge bg-warning text-dark ms-1" style="font-size:.6rem;">HFT</span>' : '';

      return `<tr class="${rowCls}">
        <td class="fw-semibold">${esc(r.broker)}${btype}</td>
        <td>${esc(r.shares)}${shrArrow}</td>
        <td>$${Number(r.cash).toLocaleString(undefined, {minimumFractionDigits:2, maximumFractionDigits:2})}${cashArrow}</td>
      </tr>`;
    }).join('');

    rows.forEach(r => { prevHoldings[r.broker] = { shares: r.shares, cash: r.cash }; });
  }

  // ── Poll ─────────────────────────────────────────────────────────────────────

  function poll() {
    fetch('/demos/nasdaq/state')
      .then(r => r.json())
      .then(state => {
        updateTicker(state.current_sql);
        renderMarket(state);
        renderOrders(state.orders || []);
        renderBook(state.asks || [], state.bids || [], state);
        renderSettlement(state.settlement_queue || []);
        renderHoldings(state.custodian_holdings || []);
      })
      .catch(() => {});
  }

  // ── Buttons ──────────────────────────────────────────────────────────────────

  startBtn.addEventListener('click', () => {
    startBtn.disabled = true;
    ticker.textContent = '-- Initializing NASDAQ simulation — resetting tables…';
    lastSql = '';
    prevHoldings = {};
    knownSettled.clear();
    prevTradeId = 0;
    fetch('/demos/nasdaq/start', { method: 'POST' })
      .then(() => poll())
      .catch(() => { startBtn.disabled = false; });
  });

  stopBtn.addEventListener('click', () => {
    stopBtn.disabled = true;
    fetch('/demos/nasdaq/stop', { method: 'POST' })
      .then(() => poll())
      .catch(() => {});
  });

  // ── Init ─────────────────────────────────────────────────────────────────────

  poll();
  pollTimer = setInterval(poll, 600);

  window.addEventListener('beforeunload', () => {
    if (pollTimer) clearInterval(pollTimer);
  });
});
