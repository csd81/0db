/* crypto_exchange.js — CEX simulation demo */

document.addEventListener('DOMContentLoaded', () => {
  const startBtn   = document.getElementById('start-btn');
  const stopBtn    = document.getElementById('stop-btn');
  const priceBadge = document.getElementById('price-badge');
  const tradeBadge = document.getElementById('trade-badge');
  const spreadBadge= document.getElementById('spread-badge');
  const spreadVal  = document.getElementById('spread-val');
  const ticker     = document.getElementById('sql-ticker');

  let lastSql      = '';
  let prevLedger   = {};     // trader → { usdt, btc }
  let prevTradeId  = 0;
  let lastTradePrice = null;
  let pollTimer    = null;

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

  // ── Header badges ───────────────────────────────────────────────────────────

  function updateHeader(state) {
    priceBadge.textContent  = state.last_price != null
      ? '$ ' + Number(state.last_price).toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2})
      : '$ —';
    tradeBadge.textContent  = (state.trade_count ?? 0) + ' trades';

    const sp = state.spread;
    if (sp != null) {
      spreadBadge.textContent = 'spread ' + Number(sp).toFixed(2);
    }

    if (state.running) {
      startBtn.disabled = true;
      stopBtn.disabled  = false;
    } else {
      startBtn.disabled = false;
      stopBtn.disabled  = true;
    }
  }

  // ── Asks (sell orders) ──────────────────────────────────────────────────────

  function renderAsks(rows) {
    const tbody = document.getElementById('tbl-asks');
    if (!rows || !rows.length) {
      tbody.innerHTML = '<tr><td colspan="3" class="text-muted text-center py-2">—</td></tr>';
      return;
    }
    tbody.innerHTML = rows.map(r =>
      `<tr class="text-danger">
        <td class="fw-bold">${Number(r.price).toFixed(2)}</td>
        <td>${Number(r.qty).toFixed(4)}</td>
        <td>${esc(r.trader)}</td>
      </tr>`
    ).join('');
  }

  // ── Bids (buy orders) ───────────────────────────────────────────────────────

  function renderBids(rows) {
    const tbody = document.getElementById('tbl-bids');
    if (!rows || !rows.length) {
      tbody.innerHTML = '<tr><td colspan="3" class="text-muted text-center py-2">—</td></tr>';
      return;
    }
    tbody.innerHTML = rows.map(r =>
      `<tr class="text-success">
        <td class="fw-bold">${Number(r.price).toFixed(2)}</td>
        <td>${Number(r.qty).toFixed(4)}</td>
        <td>${esc(r.trader)}</td>
      </tr>`
    ).join('');
  }

  // ── Spread ──────────────────────────────────────────────────────────────────

  function renderSpread(state) {
    const sp = state.spread;
    if (sp == null) { spreadVal.textContent = '—'; return; }
    const val = Number(sp).toFixed(2);
    spreadVal.textContent = val;
    spreadVal.className = sp > 50 ? 'text-danger fw-bold' : 'text-success fw-bold';
  }

  // ── Kafka Event Stream ──────────────────────────────────────────────────────

  const topicMap = {
    ORDER_PLACED:    ['bg-secondary',       '📋'],
    TRADE_EXECUTED:  ['bg-success',         '✓'],
    BALANCE_UPDATED: ['bg-primary',         '💳'],
    ORDER_CANCELLED: ['bg-warning text-dark','✗'],
  };

  function renderEvents(rows) {
    const tbody = document.getElementById('tbl-events');
    if (!rows || !rows.length) {
      tbody.innerHTML = '<tr><td colspan="3" class="text-muted text-center py-2">No events</td></tr>';
      return;
    }
    tbody.innerHTML = rows.map(r => {
      const [cls, icon] = topicMap[r.topic] || ['bg-secondary', '?'];
      const time = (r.ts || '').split(' ')[1] || r.ts || '';
      return `<tr>
        <td><span class="badge ${cls}" style="font-size:.65rem;">${icon} ${esc(r.topic)}</span></td>
        <td style="max-width:160px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">${esc(r.detail)}</td>
        <td class="text-muted" style="white-space:nowrap;">${esc(time)}</td>
      </tr>`;
    }).join('');
  }

  // ── Recent Trades ───────────────────────────────────────────────────────────

  function renderTrades(rows) {
    const tbody = document.getElementById('tbl-trades');
    if (!rows || !rows.length) {
      tbody.innerHTML = '<tr><td colspan="3" class="text-muted text-center py-2">No trades yet</td></tr>';
      lastTradePrice = null;
      return;
    }
    tbody.innerHTML = rows.map((r, i) => {
      const price = Number(r.price);
      let arrow = '';
      const prevPrice = i === rows.length - 1 ? null : Number(rows[i + 1].price);
      if (prevPrice !== null) {
        arrow = price > prevPrice ? ' <span class="text-success">▲</span>'
              : price < prevPrice ? ' <span class="text-danger">▼</span>' : '';
      }
      const isNew = r.id > prevTradeId;
      const rowCls = isNew ? 'table-success' : '';
      return `<tr class="${rowCls}">
        <td class="fw-bold">${price.toFixed(2)}${arrow}</td>
        <td>${Number(r.qty).toFixed(4)}</td>
        <td>${esc(r.buyer)} → ${esc(r.seller)}</td>
      </tr>`;
    }).join('');
    if (rows.length) prevTradeId = Math.max(...rows.map(r => r.id));
  }

  // ── Ledger ──────────────────────────────────────────────────────────────────

  function renderLedger(rows) {
    const tbody = document.getElementById('tbl-ledger');
    if (!rows || !rows.length) {
      tbody.innerHTML = '<tr><td colspan="3" class="text-muted text-center py-2">—</td></tr>';
      return;
    }
    tbody.innerHTML = rows.map(r => {
      const prev = prevLedger[r.trader] || {};
      const btcChanged  = prev.btc  != null && Math.abs(r.btc  - prev.btc)  > 0.000001;
      const usdtChanged = prev.usdt != null && Math.abs(r.usdt - prev.usdt) > 0.01;
      const rowCls = (btcChanged || usdtChanged) ? 'table-warning' : '';

      const btcArrow  = btcChanged  ? (r.btc  > prev.btc  ? ' <span class="text-success">▲</span>' : ' <span class="text-danger">▼</span>') : '';
      const usdtArrow = usdtChanged ? (r.usdt > prev.usdt ? ' <span class="text-success">▲</span>' : ' <span class="text-danger">▼</span>') : '';

      return `<tr class="${rowCls}">
        <td class="fw-semibold">${esc(r.trader)}</td>
        <td>${Number(r.btc).toFixed(4)}${btcArrow}</td>
        <td>${Number(r.usdt).toFixed(2)}${usdtArrow}</td>
      </tr>`;
    }).join('');

    rows.forEach(r => { prevLedger[r.trader] = { usdt: r.usdt, btc: r.btc }; });
  }

  // ── Poll ────────────────────────────────────────────────────────────────────

  function poll() {
    fetch('/demos/crypto-exchange/state')
      .then(r => r.json())
      .then(state => {
        updateTicker(state.current_sql);
        updateHeader(state);
        renderSpread(state);
        renderAsks(state.order_book_asks || []);
        renderBids(state.order_book_bids || []);
        renderEvents(state.events || []);
        renderTrades(state.recent_trades || []);
        renderLedger(state.ledger || []);
      })
      .catch(() => {});
  }

  // ── Buttons ─────────────────────────────────────────────────────────────────

  startBtn.addEventListener('click', () => {
    startBtn.disabled = true;
    ticker.textContent = '-- Initializing exchange — resetting tables…';
    lastSql = '';
    prevLedger = {};
    prevTradeId = 0;
    lastTradePrice = null;
    fetch('/demos/crypto-exchange/start', { method: 'POST' })
      .then(() => poll())
      .catch(() => { startBtn.disabled = false; });
  });

  stopBtn.addEventListener('click', () => {
    stopBtn.disabled = true;
    fetch('/demos/crypto-exchange/stop', { method: 'POST' })
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
