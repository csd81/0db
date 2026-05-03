/* nyse.js — NYSE Auction Market + DMM simulation demo */

document.addEventListener('DOMContentLoaded', () => {
  const startBtn      = document.getElementById('start-btn');
  const stopBtn       = document.getElementById('stop-btn');
  const flashBtn      = document.getElementById('flash-crash-btn');
  const flashBtn2     = document.getElementById('flash-crash-btn2');
  const marketBadge   = document.getElementById('market-badge');
  const priceBadge    = document.getElementById('price-badge');
  const tradeBadge    = document.getElementById('trade-badge');
  const dmmBadge      = document.getElementById('dmm-badge');
  const spreadVal     = document.getElementById('spread-val');
  const spreadWarning = document.getElementById('spread-warning');
  const dmmCashEl     = document.getElementById('dmm-cash');
  const dmmSharesEl   = document.getElementById('dmm-shares');
  const dmmIntEl      = document.getElementById('dmm-interventions');
  const ticker        = document.getElementById('sql-ticker');

  let lastSql        = '';
  let prevDmmCash    = null;
  let prevDmmShares  = null;
  let pollTimer      = null;

  function esc(s) {
    return String(s ?? '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  }

  function fmt$(n) {
    return '$' + Number(n).toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2});
  }

  // ── Ticker ──────────────────────────────────────────────────────────────────

  function updateTicker(sql) {
    if (!sql || sql === lastSql) return;
    lastSql = sql;
    ticker.textContent += '\n> ' + sql;
    ticker.scrollTop = ticker.scrollHeight;
  }

  // ── Header ──────────────────────────────────────────────────────────────────

  function renderHeader(state) {
    const running = state.running;
    if (running) {
      marketBadge.className   = 'badge fs-6 bg-success';
      marketBadge.textContent = 'OPEN';
    } else {
      marketBadge.className   = 'badge fs-6 bg-secondary';
      marketBadge.textContent = state.phase === 'idle' ? 'Idle' : state.phase;
    }
    priceBadge.textContent  = state.last_price != null ? fmt$(state.last_price) : '$—';
    tradeBadge.textContent  = (state.trade_count ?? 0) + ' trades';
    dmmBadge.textContent    = (state.dmm_interventions ?? 0) + ' interventions';

    startBtn.disabled     = running;
    stopBtn.disabled      = !running;
    flashBtn.disabled     = !running;
    flashBtn2.disabled    = !running;
  }

  // ── Order Book ───────────────────────────────────────────────────────────────

  function makeBookRow(r, sideClass) {
    const isDmm = r.is_dmm;
    const rowCls  = isDmm ? 'table-warning' : '';
    const traderLabel = isDmm
      ? '<span class="badge bg-warning text-dark" style="font-size:.62rem;">★ DMM</span>'
      : esc(r.trader_id);
    return `<tr class="${rowCls}">
      <td class="fw-bold ${sideClass}">${Number(r.price).toFixed(2)}</td>
      <td>${esc(r.qty)}</td>
      <td>${traderLabel}</td>
    </tr>`;
  }

  function renderBook(bids, asks, state) {
    const bidBody = document.getElementById('tbl-bids');
    bidBody.innerHTML = bids && bids.length
      ? bids.map(r => makeBookRow(r, 'text-success')).join('')
      : '<tr><td colspan="3" class="text-muted text-center py-2">—</td></tr>';

    const askBody = document.getElementById('tbl-asks');
    askBody.innerHTML = asks && asks.length
      ? asks.map(r => makeBookRow(r, 'text-danger')).join('')
      : '<tr><td colspan="3" class="text-muted text-center py-2">—</td></tr>';

    const sp = state.spread;
    if (sp != null) {
      spreadVal.textContent = Number(sp).toFixed(2);
      const wide = sp > 2.0;
      spreadVal.className = wide ? 'fw-bold text-danger' : 'fw-bold text-success';
      spreadWarning.classList.toggle('d-none', !wide);
    } else {
      spreadVal.textContent = '—';
      spreadVal.className   = 'fw-bold text-muted';
      spreadWarning.classList.add('d-none');
    }
  }

  // ── Trade Tape ───────────────────────────────────────────────────────────────

  function renderTape(trades) {
    const tbody = document.getElementById('tbl-tape');
    if (!trades || !trades.length) {
      tbody.innerHTML = '<tr><td colspan="5" class="text-muted text-center py-2">No trades yet</td></tr>';
      return;
    }
    tbody.innerHTML = trades.map(t => {
      const rowCls = t.is_dmm_involved ? 'table-warning' : '';
      const dmmMark = t.is_dmm_involved
        ? '<span class="badge bg-warning text-dark ms-1" style="font-size:.6rem;">★ DMM</span>' : '';
      return `<tr class="${rowCls}">
        <td class="fw-bold">${Number(t.price).toFixed(2)}</td>
        <td>${esc(t.qty)}</td>
        <td>#${esc(t.buyer_order_id)}</td>
        <td>#${esc(t.seller_order_id)}</td>
        <td>${dmmMark}</td>
      </tr>`;
    }).join('');
  }

  // ── Event Log ────────────────────────────────────────────────────────────────

  const typeMap = {
    TRADE:         ['bg-success',          '✓'],
    DMM_INTERVENE: ['bg-warning text-dark', '🛡'],
    FLASH_CRASH:   ['bg-danger',            '💥'],
    ORDER_PLACED:  ['bg-secondary',         '📋'],
  };

  function renderEvents(events) {
    const tbody = document.getElementById('tbl-events');
    if (!events || !events.length) {
      tbody.innerHTML = '<tr><td colspan="2" class="text-muted text-center py-2">No events</td></tr>';
      return;
    }
    tbody.innerHTML = events.map(e => {
      const [cls, icon] = typeMap[e.event_type] || ['bg-secondary', '?'];
      return `<tr${e.event_type === 'FLASH_CRASH' ? ' class="table-danger"' : e.event_type === 'DMM_INTERVENE' ? ' class="table-warning"' : ''}>
        <td><span class="badge ${cls}" style="font-size:.64rem;">${icon} ${esc(e.event_type)}</span></td>
        <td style="font-size:.68rem;max-width:180px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">${esc(e.detail)}</td>
      </tr>`;
    }).join('');
  }

  // ── DMM Inventory ────────────────────────────────────────────────────────────

  function renderDMM(state) {
    const cash   = state.dmm_cash   ?? 500000;
    const shares = state.dmm_shares ?? 5000;
    const ints   = state.dmm_interventions ?? 0;

    let cashArrow = '', sharesArrow = '';
    if (prevDmmCash !== null) {
      if (cash < prevDmmCash) cashArrow = ' <span class="text-danger">▼</span>';
      else if (cash > prevDmmCash) cashArrow = ' <span class="text-success">▲</span>';
    }
    if (prevDmmShares !== null) {
      if (shares < prevDmmShares) sharesArrow = ' <span class="text-danger">▼</span>';
      else if (shares > prevDmmShares) sharesArrow = ' <span class="text-success">▲</span>';
    }

    const cashLow   = cash < 50000;
    const sharesLow = shares < 200;
    dmmCashEl.innerHTML   = fmt$(cash) + cashArrow;
    dmmCashEl.className   = 'fs-4 fw-bold ' + (cashLow ? 'text-danger' : 'text-success');
    dmmSharesEl.innerHTML = Number(shares).toLocaleString() + sharesArrow;
    dmmSharesEl.className = 'fs-4 fw-bold ' + (sharesLow ? 'text-danger' : '');
    dmmIntEl.textContent  = ints + ' interventions';

    prevDmmCash   = cash;
    prevDmmShares = shares;
  }

  // ── Poll ─────────────────────────────────────────────────────────────────────

  function poll() {
    fetch('/demos/nyse/state')
      .then(r => r.json())
      .then(state => {
        updateTicker(state.current_sql);
        renderHeader(state);
        renderBook(state.bids || [], state.asks || [], state);
        renderTape(state.trades || []);
        renderEvents(state.events || []);
        renderDMM(state);
      })
      .catch(() => {});
  }

  // ── Flash Crash ──────────────────────────────────────────────────────────────

  function doFlashCrash() {
    flashBtn.disabled  = true;
    flashBtn2.disabled = true;
    fetch('/demos/nyse/flash-crash', { method: 'POST' })
      .then(() => {
        setTimeout(() => {
          flashBtn.disabled  = !document.getElementById('stop-btn').disabled === false;
          flashBtn2.disabled = flashBtn.disabled;
        }, 2000);
      })
      .catch(() => {});
  }
  flashBtn.addEventListener('click', doFlashCrash);
  flashBtn2.addEventListener('click', doFlashCrash);

  // ── Buttons ──────────────────────────────────────────────────────────────────

  startBtn.addEventListener('click', () => {
    startBtn.disabled = true;
    ticker.textContent = '-- Initializing NYSE simulation — seeding order book…';
    lastSql = '';
    prevDmmCash = null;
    prevDmmShares = null;
    fetch('/demos/nyse/start', { method: 'POST' })
      .then(() => poll())
      .catch(() => { startBtn.disabled = false; });
  });

  stopBtn.addEventListener('click', () => {
    stopBtn.disabled  = true;
    flashBtn.disabled = true;
    flashBtn2.disabled = true;
    fetch('/demos/nyse/stop', { method: 'POST' })
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
