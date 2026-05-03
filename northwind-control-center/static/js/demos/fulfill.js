'use strict';

// ── Column lists (mirrors Python constants) ───────────────────────────────────
const COL_MAP = {
  customer_card:  ['CompanyName','ContactName','Phone'],
  employee_card:  ['FirstName','LastName','Title'],
  shipper_card:   ['CompanyName','Phone'],
  product_card:   ['ProductName','UnitPrice','UnitsInStock','SupplierID'],
  supplier_card:  ['CompanyName','ContactName','Phone'],
};

// ── Phase banner map ──────────────────────────────────────────────────────────
const PHASE_BANNER = {
  idle:                ['secondary', 'Waiting…'],
  loading:             ['info',      'Loading orders…'],
  reading_order:       ['primary',   'Reading order row'],
  reading_field:       ['primary',   'Reading field'],
  sub_table_open:      ['warning',   'Opening table'],
  sub_table_scan:      ['warning',   'Scanning field →'],
  sub_table_done:      ['info',      'Table scan complete'],
  reading_items:       ['primary',   'Reading order details'],
  stock_checked:       ['info',      'Stock check result'],
  checking_stock:      ['warning',   'Checking stock'],
  begin_tran:          ['warning',   'BEGIN TRANSACTION'],
  creating_package:    ['info',      'Creating package'],
  packing:             ['info',      'Packing items'],
  removing_details:    ['warning',   'Removing order details'],
  shipped:             ['success',   '✓ SHIPPED'],
  rollback:            ['danger',    'ROLLBACK'],
  removing_package:    ['danger',    'Rolling back package'],
  dropped:             ['danger',    '✗ Package dropped'],
  contacting_supplier: ['warning',   'Contacting supplier'],
  delivery_check:      ['info',      'Checking for incoming deliveries…'],
  delivery_arrived:    ['success',   '✓ Delivery arrived'],
  partial_order:       ['warning',   '⚠ Partial order saved — processing next order'],
  completing_partial:  ['info',      'Completing partial order'],
  returning_to_partial:['warning',   'Returning to partial order'],
  done:                ['success',   '✓ All orders processed'],
  error:               ['danger',    'Error'],
};

// ── State ─────────────────────────────────────────────────────────────────────
let pollTimer        = null;
let autoPlayTimer    = null;
let autoPlayInterval = 400;   // ms between auto-steps (1× = 400, 2× = 200, 4× = 100)
let lastSqlLen       = 0;
let lastPkgJson      = '';
const expandedCards  = new Set();  // order_ids currently expanded in the queue

// ── Polling ───────────────────────────────────────────────────────────────────
function startPolling() {
  if (pollTimer) return;
  pollTimer = setInterval(fetchState, 300);
}

function stopPolling() {
  if (pollTimer)     { clearInterval(pollTimer);     pollTimer     = null; }
  if (autoPlayTimer) { clearInterval(autoPlayTimer); autoPlayTimer = null;
    const ab = document.getElementById('autoplay-btn');
    ab.classList.remove('btn-primary'); ab.classList.add('btn-outline-primary');
    ab.innerHTML = '<i class="bi bi-fast-forward me-1"></i>Auto';
  }
}

async function fetchState() {
  try {
    const r = await fetch('/demos/fulfill/state');
    render(await r.json());
  } catch (_) {}
}

// ── Main render ───────────────────────────────────────────────────────────────
function render(s) {
  updateBanner(s);
  updateProgress(s);
  updateOrderQueue(s);
  updateRefillOrder(s);
  updateOrdersTable(s);
  updateSubTable(s);
  updateItemsTable(s);
  updateAllCards(s);
  updatePackage(s);
  appendSql(s);
  updatePnl(s);

  if (['done','error'].includes(s.phase)) stopPolling();

  document.getElementById('start-btn').disabled = s.phase !== 'idle';
  document.getElementById('step-btn').disabled  = !s.waiting_for_step;
}

// ── Order queue ───────────────────────────────────────────────────────────────
const MAX_QUEUE = 10;

function updateOrderQueue(s) {
  const el = document.getElementById('order-queue');
  let queue = (s.order_queue || []).filter(q => q.status !== 'active');

  // Cap at MAX_QUEUE: keep all partials + refills; drop oldest shipped entries
  if (queue.length > MAX_QUEUE) {
    const keep    = queue.filter(q => q.status !== 'shipped' || q.type === 'refill');
    const shipped = queue.filter(q => q.status === 'shipped' && q.type !== 'refill');
    const slots   = Math.max(0, MAX_QUEUE - keep.length);
    queue = [...keep, ...shipped.slice(-slots)];
  }

  if (!queue.length) { el.innerHTML = ''; return; }

  el.innerHTML = queue.map(q => {
    if (q.type === 'refill') {
      const prod = q.product ? esc(q.product) : `Product #${q.order_id}`;
      if (q.status === 'arrived') {
        return `<div class="queue-card queue-card-shipped px-2 py-1 d-flex justify-content-between align-items-center">
          <span><i class="bi bi-truck me-1"></i><strong>Delivery</strong> — ${prod} ×${q.restock_qty || q.qty}</span>
          <span class="badge bg-success">✓ Arrived</span>
        </div>`;
      }
      return `<div class="queue-card queue-card-refill px-2 py-1 d-flex justify-content-between align-items-center">
        <span><i class="bi bi-arrow-repeat me-1"></i><strong>Refill</strong> — ${prod} ×${q.qty}</span>
        <span class="badge" style="background:#0dcaf0;color:#055160;">✓ Sent</span>
      </div>`;
    }

    // Order cards (partial / shipped) — clickable, expandable
    const expanded  = expandedCards.has(q.order_id);
    const chevron   = expanded ? 'bi-chevron-up' : 'bi-chevron-down';
    let headerCls, icon, badge;
    if (q.status === 'partial') {
      headerCls = 'queue-card-partial';
      icon      = 'bi-hourglass-split';
      badge     = `<span class="badge" style="background:#997404;color:#fff;">⚠ Awaiting Restock</span>`;
    } else {
      headerCls = 'queue-card-shipped';
      icon      = 'bi-check-circle';
      badge     = `<span class="badge bg-success">✓ Shipped</span>`;
    }
    const label = `<strong>Order #${q.order_id}</strong>${q.customer ? ' — ' + esc(q.customer) : ''}`;

    let detail = '';
    if (expanded && q.details) {
      const d     = q.details;
      const items = (d.items || []).map(it => {
        const icon2 = it.status === 'packed' ? '✓' : it.status === 'awaiting_restock' ? '⏳' : '○';
        return `<li style="font-size:.75rem;">${icon2} ${esc(it.name)} ×${it.qty}</li>`;
      }).join('');
      detail = `<div class="px-2 pb-1 pt-0" style="background:inherit;border-top:1px solid rgba(0,0,0,.1);">
        ${d.ship_to ? `<div style="font-size:.72rem;opacity:.8;margin-top:.25rem;"><i class="bi bi-geo-alt me-1"></i>${esc(d.ship_to)}</div>` : ''}
        <ul class="mb-0 ps-3 mt-1">${items}</ul>
      </div>`;
    }

    return `<div class="queue-card ${headerCls}" data-order-id="${q.order_id}" style="cursor:pointer;">
      <div class="px-2 py-1 d-flex justify-content-between align-items-center">
        <span><i class="bi ${icon} me-1"></i>${label}</span>
        <span class="d-flex align-items-center gap-1">${badge}<i class="bi ${chevron} ms-1" style="font-size:.7rem;"></i></span>
      </div>
      ${detail}
    </div>`;
  }).join('');

}

// One persistent delegated listener — survives innerHTML replacements
document.getElementById('order-queue').addEventListener('click', e => {
  const card = e.target.closest('.queue-card[data-order-id]');
  if (!card) return;
  const oid = parseInt(card.dataset.orderId);
  if (expandedCards.has(oid)) expandedCards.delete(oid);
  else expandedCards.add(oid);
  fetchState();
});

// ── Refill Order card ─────────────────────────────────────────────────────────
function updateRefillOrder(s) {
  const card = document.getElementById('refill-order-card');
  const ro   = s.refill_order;
  if (!ro || ro.status !== 'open') { card.classList.add('d-none'); return; }
  card.classList.remove('d-none');

  // Dynamic title
  const title = document.getElementById('refill-order-title');
  title.textContent = ro.ProductName
    ? `Refill Order — ${ro.ProductName}`
    : `Refill Order (Order #${ro.order_id})`;

  // Build dl rows from all known fields in insertion order
  const REFILL_FIELD_ORDER = [
    'order_id', 'OrderNeed', 'RestockQty',
    'ProductName', 'UnitPrice', 'UnitsInStock', 'SupplierID',
    'CompanyName', 'ContactName', 'Phone',
  ];
  const body = document.getElementById('refill-order-body');

  // Collect keys present in ro, preserving REFILL_FIELD_ORDER then any extras
  const ordered = REFILL_FIELD_ORDER.filter(k => k in ro && k !== 'status');
  const extras  = Object.keys(ro).filter(k => !REFILL_FIELD_ORDER.includes(k) && k !== 'status' && k !== 'ticks_remaining');
  const keys    = [...ordered, ...extras];

  body.innerHTML = keys
    .filter(k => ro[k] != null && ro[k] !== '')
    .map(k => {
      const v = ro[k];
      const label = k === 'order_id' ? 'Order ID' : k;
      return `<dt class="col-5 text-truncate" title="${esc(label)}">${esc(label)}</dt>
              <dd class="col-7 mb-0">${esc(String(v))}</dd>`;
    }).join('');
}

// ── Banner ────────────────────────────────────────────────────────────────────
function updateBanner(s) {
  const [cls, fallback] = PHASE_BANNER[s.phase] || ['secondary', s.phase];
  const label = s.phase_label || fallback;
  const banner = document.getElementById('phase-banner');
  banner.className = `alert alert-${cls} py-1 px-3 mb-3`;
  document.getElementById('phase-text').textContent =
    s.error ? `Error: ${s.error}` : label;
}

// ── Progress ──────────────────────────────────────────────────────────────────
function updateProgress(s) {
  const total = s.orders_total || 1;
  const done  = s.phase === 'done' ? total : s.order_idx;
  document.getElementById('progress-bar').style.width = Math.round((done / total) * 100) + '%';
  document.getElementById('order-badge').textContent =
    `Order ${s.orders_total ? s.order_idx + 1 : 0} / ${s.orders_total}`;
}

// (No column label overrides needed — Orders columns use their native names)

// ── Orders table ──────────────────────────────────────────────────────────────
function updateOrdersTable(s) {
  const tbl  = document.getElementById('orders-table');
  const head = tbl.querySelector('thead');
  const body = tbl.querySelector('tbody');

  if (!s.order_cols || !s.order_cols.length) return;

  if (head.querySelectorAll('th').length !== s.order_cols.length) {
    head.innerHTML = '<tr>' + s.order_cols.map(c =>
      `<th title="${esc(c)}">${esc(c)}</th>`
    ).join('') + '</tr>';
  }

  if (!s.orders || !s.orders.length) return;
  if (body.querySelectorAll('tr').length !== s.orders.length) {
    body.innerHTML = s.orders.map((o, ri) =>
      '<tr data-ri="' + ri + '">' +
      s.order_cols.map(c => `<td>${fmt(o[c])}</td>`).join('') +
      '</tr>'
    ).join('');
  }

  // Build a lookup: OrderID → queue status
  const queueStatus = {};
  for (const q of (s.order_queue || [])) {
    if (q.type !== 'refill') queueStatus[q.order_id] = q.status;
  }

  body.querySelectorAll('tr').forEach((tr, ri) => {
    const active  = ri === s.order_idx;
    const orderId = s.orders[ri]?.OrderID;
    const qst     = queueStatus[orderId];

    tr.classList.remove('table-warning', 'table-success', 'table-info');
    if (active) {
      tr.classList.add('table-warning');
    } else if (qst === 'shipped') {
      tr.classList.add('table-success');
    } else if (qst === 'partial') {
      tr.classList.add('table-info');
    }

    tr.querySelectorAll('td').forEach((td, ci) => {
      td.classList.toggle('cell-active', active && ci === s.order_col_idx);
    });
  });
}

// ── Universal sub-table ───────────────────────────────────────────────────────
function updateSubTable(s) {
  const card = document.getElementById('sub-table-card');
  if (!s.sub_table) { card.classList.add('d-none'); return; }
  card.classList.remove('d-none');

  const st = s.sub_table;
  document.getElementById('sub-table-title').textContent = st.table_name;

  const thead = document.getElementById('sub-table-head');
  if (thead.querySelectorAll('th').length !== st.columns.length) {
    thead.innerHTML = '<tr>' + st.columns.map(c => `<th>${esc(c)}</th>`).join('') + '</tr>';
  }

  const tbody = document.getElementById('sub-table-body');
  tbody.innerHTML = (st.rows || []).map((row, ri) => {
    const rowCls = ri === st.active_row_idx ? 'table-warning' : '';
    const cells  = st.columns.map((col, ci) => {
      const cellCls = (ri === st.active_row_idx && ci === st.active_col_idx)
        ? 'cell-active' : '';
      return `<td class="${cellCls}">${fmt(row[col])}</td>`;
    }).join('');
    return `<tr class="${rowCls}">${cells}</tr>`;
  }).join('');

  // Scroll active row into view within the sub-table container only — never the page
  const tblWrap = document.querySelector('#sub-table-card .tbl-wrap');
  const activeRow = tbody.querySelector('tr.table-warning');
  if (tblWrap && activeRow) {
    const rowTop = activeRow.offsetTop;
    const rowBot = rowTop + activeRow.offsetHeight;
    if (rowTop < tblWrap.scrollTop)
      tblWrap.scrollTop = rowTop;
    else if (rowBot > tblWrap.scrollTop + tblWrap.clientHeight)
      tblWrap.scrollTop = rowBot - tblWrap.clientHeight;
  }
}

// ── Items table ───────────────────────────────────────────────────────────────
function updateItemsTable(s) {
  const body = document.getElementById('items-table').querySelector('tbody');
  if (!s.items || !s.items.length) { body.innerHTML = ''; return; }

  body.innerHTML = s.items.map((item, i) => {
    const active   = i === s.item_idx;
    const badge    = item.status === 'pending' ? '' :
      item.status === 'ok'
        ? '<span class="badge bg-success">✓ OK</span>'
        : '<span class="badge bg-danger">✗ SHORT</span>';
    return `<tr class="${active ? 'table-warning' : ''}">
      <td>${item.ProductID}</td>
      <td>${esc(item.ProductName)}</td>
      <td>${item.Quantity}</td>
      <td>${item.UnitPrice != null ? item.UnitPrice.toFixed(2) : ''}</td>
      <td>${item.Discount != null ? (item.Discount * 100).toFixed(0) + '%' : ''}</td>
      <td class="${item.status === 'short' ? 'text-danger fw-bold' : ''}">${item.UnitsInStock}</td>
      <td>${badge}</td>
    </tr>`;
  }).join('');
}

// ── Context cards ─────────────────────────────────────────────────────────────
function updateAllCards(s) {
  for (const [key, cols] of Object.entries(COL_MAP)) {
    const prefix = key.replace('_card', '');
    fillCard(`${prefix}-card`, `${prefix}-body`, s[key], cols);
  }
}

function fillCard(cardId, bodyId, data, cols) {
  const card = document.getElementById(cardId);
  if (!card) return;
  if (!data || !Object.keys(data).length) { card.classList.add('d-none'); return; }
  card.classList.remove('d-none');
  document.getElementById(bodyId).innerHTML = buildDl(cols, data);
}

// ── Package panel ─────────────────────────────────────────────────────────────
function updatePackage(s) {
  const list           = document.getElementById('pkg-list');
  const empty          = document.getElementById('pkg-empty');
  const title          = document.getElementById('pkg-title');
  const metaDl         = document.getElementById('pkg-meta');
  const metaHr         = document.getElementById('pkg-meta-divider');
  const contentsHdr    = document.getElementById('pkg-contents-header');
  const stamp          = document.getElementById('pkg-stamp');

  const items   = s.package_items || [];
  const meta    = s.package_meta  || {};
  const newJson = JSON.stringify([s.phase, meta, items.map(i => [i.ProductID, i.Quantity, i.status])]);
  if (newJson === lastPkgJson) return;
  lastPkgJson = newJson;

  // Title
  if (s.package_id) {
    const orderID = s.orders[s.order_idx]?.OrderID || '';
    title.textContent = `Package #${s.package_id} (Order ${orderID})`;
  } else {
    title.textContent = Object.keys(meta).length ? `Package (Order ${meta.OrderID || '…'})` : 'Package';
  }

  // Metadata section — render every key/value pair
  const metaKeys = Object.keys(meta);
  const shipComplete = 'ShipCountry' in meta;

  const visibleMeta = Object.entries(meta).filter(([, v]) => v != null && v !== '');
  if (visibleMeta.length) {
    metaDl.style.display = '';
    metaDl.innerHTML = visibleMeta.map(([k, v]) =>
      `<dt class="col-5 text-truncate" title="${esc(k)}">${esc(k)}</dt>
       <dd class="col-7 mb-0">${esc(String(v))}</dd>`
    ).join('');
    empty.classList.add('d-none');
  } else {
    metaDl.style.display = 'none';
  }

  // Separator + Contents header — appear once ShipCountry is filled
  metaHr.style.display         = shipComplete ? '' : 'none';
  contentsHdr.style.display    = shipComplete ? '' : 'none';

  // Items list
  if (!items.length) {
    list.innerHTML = '';
    stamp.style.display = 'none';
    if (!metaKeys.length) empty.classList.remove('d-none');
    return;
  }
  empty.classList.add('d-none');
  const icons = { queued:'○', awaiting_restock:'⏳', packing:'⏳', packed:'✓', completing:'⏳', removing:'↩', removed:'' };
  list.innerHTML = items.map(item => {
    const rm   = item.status === 'removing' ? 'pkg-removing' : '';
    const icon = icons[item.status] || '';
    return `<li class="list-group-item py-1 px-2 ${rm}" style="font-size:.82rem;">
      ${icon} <strong>${esc(item.ProductName)}</strong> × ${item.Quantity}
    </li>`;
  }).join('');

  // Stamp
  const phase = s.phase;
  if (phase === 'shipped' || phase === 'done') {
    stamp.style.display = '';
    stamp.innerHTML = '<span class="pkg-stamp pkg-stamp-ok">✓ Order Complete — Ready to Ship</span>';
  } else if (['partial_order','contacting_supplier','delivery_check','delivery_arrived','returning_to_partial','completing_partial'].includes(phase)) {
    stamp.style.display = '';
    stamp.innerHTML = '<span class="pkg-stamp pkg-stamp-warn">⚠ Partial Order — Awaiting Restock</span>';
  } else if (['rollback','removing_package','dropped'].includes(phase)) {
    stamp.style.display = '';
    stamp.innerHTML = '<span class="pkg-stamp pkg-stamp-warn">⚠ Incomplete Order — Do Not Ship!<br>Rollback All Transactions</span>';
  } else {
    stamp.style.display = 'none';
  }
}

// ── SQL ticker ────────────────────────────────────────────────────────────────
function appendSql(s) {
  const ticker = document.getElementById('sql-ticker');
  const log    = s.sql_log || [];
  if (log.length <= lastSqlLen) return;
  ticker.textContent += log.slice(lastSqlLen).join('\n') + '\n';
  lastSqlLen = log.length;
  ticker.scrollTop = ticker.scrollHeight;
}

// ── Helpers ───────────────────────────────────────────────────────────────────
function fmt(v) {
  if (v == null) return '<span class="text-muted">—</span>';
  const s = String(v);
  if (s.length > 20) return `<span title="${esc(s)}">${esc(s.slice(0, 18))}…</span>`;
  return esc(s);
}

function esc(s) {
  return String(s)
    .replace(/&/g, '&amp;').replace(/</g, '&lt;')
    .replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}

function buildDl(cols, row) {
  return cols
    .filter(c => row[c] != null && row[c] !== '' && row[c] !== false)
    .map(c => `<dt class="col-5 text-truncate" title="${esc(c)}">${esc(c)}</dt>
               <dd class="col-7 mb-0">${esc(String(row[c]))}</dd>`)
    .join('');
}

// ── Button handlers ───────────────────────────────────────────────────────────
document.getElementById('start-btn').addEventListener('click', async () => {
  document.getElementById('start-btn').disabled = true;
  lastSqlLen  = 0;
  lastPkgJson = '';
  document.getElementById('sql-ticker').textContent = '';
  await fetch('/demos/fulfill/start', { method: 'POST' });
  startPolling();
});

document.getElementById('step-btn').addEventListener('click', async () => {
  document.getElementById('step-btn').disabled = true;
  await fetch('/demos/fulfill/step', { method: 'POST' });
});

document.getElementById('autoplay-btn').addEventListener('click', () => {
  const btn = document.getElementById('autoplay-btn');
  if (autoPlayTimer) {
    clearInterval(autoPlayTimer);
    autoPlayTimer = null;
    btn.classList.remove('btn-primary');
    btn.classList.add('btn-outline-primary');
    btn.innerHTML = '<i class="bi bi-fast-forward me-1"></i>Auto';
  } else {
    startAutoPlay();
  }
});

function startAutoPlay() {
  if (autoPlayTimer) clearInterval(autoPlayTimer);
  autoPlayTimer = setInterval(async () => {
    const stepBtn = document.getElementById('step-btn');
    if (!stepBtn.disabled) {
      stepBtn.disabled = true;
      await fetch('/demos/fulfill/step', { method: 'POST' });
    }
  }, autoPlayInterval);
  const btn = document.getElementById('autoplay-btn');
  btn.classList.remove('btn-outline-primary');
  btn.classList.add('btn-primary');
  btn.innerHTML = '<i class="bi bi-stop-circle me-1"></i>Stop Auto';
}

const SPEEDS = [
  { id: 'speed-0x',  ms: 800  },
  { id: 'speed-1x',  ms: 400  },
  { id: 'speed-2x',  ms: 200  },
  { id: 'speed-4x',  ms: 100  },
  { id: 'speed-8x',  ms: 50   },
  { id: 'speed-16x', ms: 25   },
  { id: 'speed-32x', ms: 12   },
];

function setSpeed(ms) {
  autoPlayInterval = ms;
  SPEEDS.forEach(s => document.getElementById(s.id).classList.toggle('active', s.ms === ms));
  if (autoPlayTimer) startAutoPlay();
}

SPEEDS.forEach(s => document.getElementById(s.id).addEventListener('click', () => setSpeed(s.ms)));

// ── P&L panel ─────────────────────────────────────────────────────────────────
function updatePnl(s) {
  const p = s.pnl;
  if (!p) return;

  const ic          = p.initial_capital || 0;
  const revenue     = p.revenue    || 0;
  const cogs        = p.cogs       || 0;
  const freight     = p.freight    || 0;
  const inventory   = p.inventory  || 0;   // asset purchase — not deducted from net income
  const salaries    = p.salaries   || 0;
  const overhead    = p.overhead   || 0;
  const grossProfit = revenue - cogs;
  const netIncome   = revenue - cogs - freight - salaries - overhead;
  const netCapital  = ic + netIncome;

  const fmt = v => '$' + Math.abs(v).toLocaleString('en-US', {minimumFractionDigits:2, maximumFractionDigits:2});
  const sign = v => v < 0 ? '−' : v > 0 ? '+' : '';
  const cls  = v => v >= 0 ? 'text-success' : 'text-danger';

  const rows = [
    ['+ Revenue',      revenue,     'text-success'],
    ['− COGS',         -cogs,       'text-danger'],
    ['= Gross Profit', grossProfit, cls(grossProfit)],
    ['─────────────────────────', null, ''],
    ['− Freight',      -freight,    'text-danger'],
    ['− Salaries',     -salaries,   salaries > 0 ? 'text-danger' : 'text-muted'],
    ['− Overhead',     -overhead,   overhead > 0 ? 'text-danger' : 'text-muted'],
    ['═ Net Income',   netIncome,   cls(netIncome)],
    ['─────────────────────────', null, ''],
    ['Initial Capital',    ic,        'text-muted'],
    ['Net Capital',        netCapital, cls(netCapital)],
    ['─────────────────────────', null, ''],
    ['∗ Inventory Purchased', inventory, 'text-info'],
  ];

  document.getElementById('pnl-body').innerHTML = rows.map(([label, val, klass]) => {
    if (val === null) return `<tr><td colspan="2" class="text-muted py-0" style="font-size:.65rem;">${label}</td></tr>`;
    const bold = label.startsWith('═') || label === 'Net Capital' ? 'fw-bold' : '';
    const noSign = label.startsWith('∗');
    return `<tr class="${bold}">
      <td class="py-0 text-muted">${label}</td>
      <td class="py-0 text-end ${klass}">${noSign ? '' : sign(val)}${fmt(val)}</td>
    </tr>`;
  }).join('');

  // Badge on card header
  const badge = document.getElementById('pnl-net-badge');
  badge.textContent = fmt(netCapital);
  badge.className = 'badge ' + (netCapital >= ic ? 'bg-success' : netCapital >= ic * 0.8 ? 'bg-warning text-dark' : 'bg-danger');
}

document.getElementById('reset-btn').addEventListener('click', async () => {
  stopPolling();
  await fetch('/demos/fulfill/reset', { method: 'POST' });
  lastSqlLen  = 0;
  lastPkgJson = '';
  document.getElementById('sql-ticker').textContent = '';
  const r = await fetch('/demos/fulfill/state');
  render(await r.json());
});
