/* blockchain.js — Proof of Work / rqlite blockchain demo */

document.addEventListener('DOMContentLoaded', () => {
  const startBtn    = document.getElementById('start-btn');
  const stopBtn     = document.getElementById('stop-btn');
  const phaseBadge  = document.getElementById('phase-badge');
  const blockBadge  = document.getElementById('block-badge');
  const forkBadge   = document.getElementById('fork-badge');
  const ticker      = document.getElementById('sql-ticker');
  const chainBlocks = document.getElementById('chain-blocks');
  const nodeStatus  = document.getElementById('node-status');

  let lastSql       = '';
  let knownHashes   = new Set();
  let pollTimer     = null;

  const PEERS = ['Peer A', 'Peer B', 'Peer C'];

  function esc(s) {
    return String(s ?? '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  }

  function peerId(name) {
    return name.toLowerCase().replace(' ', '-');
  }

  // ── Ticker ─────────────────────────────────────────────────────────────────

  function updateTicker(sql) {
    if (!sql || sql === lastSql) return;
    lastSql = sql;
    ticker.textContent += '\n> ' + sql;
    ticker.scrollTop = ticker.scrollHeight;
  }

  // ── Status badges ───────────────────────────────────────────────────────────

  function updateHeader(state) {
    blockBadge.textContent = state.block_count + ' blocks';
    forkBadge.textContent  = state.fork_count  + ' forks';

    const phaseLabels = {
      idle: ['bg-secondary', 'Idle'],
      starting: ['bg-info text-dark', 'Starting…'],
      mining: ['bg-warning text-dark', 'Mining'],
    };
    const [cls, label] = phaseLabels[state.phase] || ['bg-secondary', state.phase];
    phaseBadge.className = 'badge fs-6 ' + cls;
    phaseBadge.textContent = label;

    if (state.running) {
      startBtn.disabled = true;
      stopBtn.disabled  = false;
    } else {
      startBtn.disabled = false;
      stopBtn.disabled  = true;
    }
  }

  // ── Miner cards ─────────────────────────────────────────────────────────────

  const statusMap = {
    idle:      ['bg-secondary', 'idle'],
    mining:    ['bg-warning text-dark', '⛏ mining'],
    found:     ['bg-success', '✓ found!'],
    committed: ['bg-primary', '✔ committed'],
    orphaned:  ['bg-danger', '✗ orphaned'],
  };

  function updateMiners(peers) {
    PEERS.forEach(peer => {
      const pid  = peerId(peer);
      const data = peers[peer] || {};
      const [cls, label] = statusMap[data.status] || ['bg-secondary', data.status || 'idle'];
      document.getElementById('badge-' + pid).className = 'badge ' + cls;
      document.getElementById('badge-' + pid).textContent = label;
      document.getElementById('nonce-' + pid).textContent =
        data.nonce ? data.nonce.toLocaleString() : '—';
      document.getElementById('hash-' + pid).textContent =
        data.last_hash ? data.last_hash + '…' : '—';
    });
  }

  // ── Blockchain visualization ────────────────────────────────────────────────

  const minerColors = {
    'Satoshi': 'bg-dark text-white',
    'Peer A':  'bg-warning text-dark',
    'Peer B':  'bg-info text-dark',
    'Peer C':  'bg-success text-white',
  };

  function renderChain(blocks) {
    if (!blocks.length) return;

    // Group by height so we can show forks inline
    const byHeight = {};
    blocks.forEach(b => {
      if (!byHeight[b.height]) byHeight[b.height] = [];
      byHeight[b.height].push(b);
    });

    const heights = Object.keys(byHeight).map(Number).sort((a, b) => b - a);
    const newHtml = heights.map((h, i) => {
      const canonical = byHeight[h].find(b => !b.orphan) || byHeight[h][0];
      const orphans   = byHeight[h].filter(b => b.orphan);

      const chainArrow = i < heights.length - 1
        ? `<div class="align-self-center text-muted fw-bold fs-5 px-1">←</div>` : '';

      const blockCard = renderBlock(canonical, false, !knownHashes.has(canonical.hash));
      knownHashes.add(canonical.hash);

      const orphanCards = orphans.map(o => {
        const card = renderBlock(o, true, !knownHashes.has(o.hash));
        knownHashes.add(o.hash);
        return card;
      }).join('');

      const orphanSection = orphanCards
        ? `<div class="d-flex flex-column gap-1">${blockCard}${orphanCards}</div>`
        : blockCard;

      return orphanSection + chainArrow;
    }).join('');

    chainBlocks.innerHTML = newHtml;
  }

  function renderBlock(b, isOrphan, isNew) {
    const colorCls = isOrphan ? 'bg-secondary text-white opacity-50'
                              : (minerColors[b.miner] || 'bg-secondary text-white');
    const borderCls = isNew && !isOrphan ? 'border border-3 border-success' : '';
    const orphanTag = isOrphan
      ? '<div class="badge bg-danger mb-1" style="font-size:.6rem">ORPHANED</div>' : '';
    const txs = (b.txs || '').split(' | ').map(t => `<div>${esc(t)}</div>`).join('');

    return `<div class="card ${borderCls}" style="min-width:160px;font-size:.72rem;">
      <div class="card-header py-1 ${colorCls} text-center fw-bold">
        ${orphanTag}
        Block #${esc(b.height)}
      </div>
      <div class="card-body p-1">
        <div class="text-truncate"><span class="text-muted">hash:</span> <code style="font-size:.65rem">${esc((b.hash||'').substring(0,12))}…</code></div>
        <div class="text-truncate"><span class="text-muted">prev:</span> <code style="font-size:.65rem">${esc((b.prev_hash||'').substring(0,8))}…</code></div>
        <div><span class="text-muted">miner:</span> ${esc(b.miner)}</div>
        <div><span class="text-muted">nonce:</span> ${esc(b.nonce)}</div>
        <div class="text-muted mt-1" style="font-size:.65rem;">${txs}</div>
      </div>
    </div>`;
  }

  // ── Network events ──────────────────────────────────────────────────────────

  const eventStyle = {
    GENESIS: ['bg-dark',    '🌐'],
    BLOCK:   ['bg-success', '✓'],
    FORK:    ['bg-danger',  '⚡'],
  };

  function renderEvents(events) {
    const tbody = document.getElementById('tbl-events');
    if (!events.length) {
      tbody.innerHTML = '<tr><td colspan="2" class="text-muted text-center py-2">No events</td></tr>';
      return;
    }
    tbody.innerHTML = events.map(e => {
      const [cls, icon] = eventStyle[e.event] || ['bg-secondary', '?'];
      const detail = (e.detail || '').substring(0, 60) + ((e.detail||'').length > 60 ? '…' : '');
      return `<tr>
        <td><span class="badge ${cls}">${icon} ${esc(e.event)}</span></td>
        <td style="font-size:.7rem">${esc(detail)}</td>
      </tr>`;
    }).join('');
  }

  // ── rqlite node status ──────────────────────────────────────────────────────

  function renderNodes(nodes) {
    if (!nodes || !Object.keys(nodes).length) {
      nodeStatus.innerHTML = '<span class="text-muted">—</span>';
      return;
    }
    nodeStatus.innerHTML = Object.entries(nodes).map(([id, n]) => {
      const leaderBadge = n.leader ? '<span class="badge bg-warning text-dark ms-1">Leader</span>' : '';
      const reachable   = n.reachable
        ? '<span class="text-success">●</span>'
        : '<span class="text-danger">●</span>';
      return `<div>${reachable} <strong>${esc(id)}</strong>${leaderBadge}
        <br><span class="text-muted">${esc(n.api_addr)}</span></div>`;
    }).join('');
  }

  // ── Poll ────────────────────────────────────────────────────────────────────

  function poll() {
    fetch('/demos/blockchain/state')
      .then(r => r.json())
      .then(state => {
        updateTicker(state.current_sql);
        updateHeader(state);
        updateMiners(state.peers || {});
        renderChain(state.blocks || []);
        renderEvents(state.events || []);
        renderNodes(state.nodes || {});
      })
      .catch(() => {});
  }

  // ── Buttons ─────────────────────────────────────────────────────────────────

  startBtn.addEventListener('click', () => {
    startBtn.disabled = true;
    ticker.textContent = '-- Initializing blockchain — resetting rqlite tables…';
    lastSql = '';
    knownHashes.clear();
    chainBlocks.innerHTML = '<span class="text-muted small align-self-center">Seeding…</span>';
    fetch('/demos/blockchain/start', { method: 'POST' })
      .then(() => poll())
      .catch(() => { startBtn.disabled = false; });
  });

  stopBtn.addEventListener('click', () => {
    stopBtn.disabled = true;
    fetch('/demos/blockchain/stop', { method: 'POST' })
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
