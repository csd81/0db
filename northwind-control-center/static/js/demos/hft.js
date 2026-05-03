/* hft.js — HFT Latency Arbitrage Race demo (event-driven, no polling loop) */

document.addEventListener('DOMContentLoaded', () => {
  const triggerBtn      = document.getElementById('trigger-btn');
  const resetBtn        = document.getElementById('reset-btn');
  const raceCountBadge  = document.getElementById('race-count-badge');
  const sqlTicker       = document.getElementById('sql-ticker');
  const nyPrice         = document.getElementById('ny-price');
  const chiPrice        = document.getElementById('chi-price');
  const hftBar          = document.getElementById('hft-bar');
  const retailBar       = document.getElementById('retail-bar');
  const hftStatus       = document.getElementById('hft-status');
  const retailStatus    = document.getElementById('retail-status');
  const hftLatencyLabel = document.getElementById('hft-latency-label');
  const retLatencyLabel = document.getElementById('retail-latency-label');
  const hftConfigBadge  = document.getElementById('hft-config-badge');
  const retConfigBadge  = document.getElementById('retail-config-badge');
  const hftPnl          = document.getElementById('hft-pnl');
  const hftWins         = document.getElementById('hft-wins');
  const retailPnl       = document.getElementById('retail-pnl');
  const retailWins      = document.getElementById('retail-wins');
  const tblRaces        = document.getElementById('tbl-races');

  const WINNER_ANIM = 2500; // ms — winner bar always takes exactly 2.5 s

  // Client-side latency lookup for immediate label update on config change
  const LATENCIES = {
    'microwave|cloud':     [4.1,  67.0],
    'fiber|cloud':         [6.1,  67.0],
    'microwave|colocated': [4.1,   8.5],
    'fiber|colocated':     [6.1,   8.5],
  };

  // ── Config labels ─────────────────────────────────────────────────────────────

  function getNetwork() {
    return document.querySelector('input[name="hft-network"]:checked')?.value ?? 'microwave';
  }

  function getSetup() {
    return document.querySelector('input[name="retail-setup"]:checked')?.value ?? 'cloud';
  }

  function updateConfigLabels() {
    const net   = getNetwork();
    const setup = getSetup();
    const key   = net + '|' + setup;
    const [hftMs, retMs] = LATENCIES[key] ?? [4.1, 67.0];

    hftLatencyLabel.textContent = 'Latency: ' + hftMs.toFixed(1) + ' ms';
    retLatencyLabel.textContent = 'Latency: ' + retMs.toFixed(1) + ' ms';

    const netLabel   = net   === 'microwave' ? 'Microwave' : 'Fiber';
    const setupLabel = setup === 'cloud'     ? 'Cloud Ohio' : 'Co-located NY';
    hftConfigBadge.textContent = 'Co-located · ' + netLabel;
    retConfigBadge.textContent = setupLabel;
  }

  document.querySelectorAll('input[name="hft-network"], input[name="retail-setup"]')
    .forEach(el => el.addEventListener('change', updateConfigLabels));

  // ── Helpers ───────────────────────────────────────────────────────────────────

  function fmt$(n) {
    const sign = n < 0 ? '-' : '';
    return sign + '$' + Math.abs(Number(n)).toLocaleString(undefined,
      { minimumFractionDigits: 2, maximumFractionDigits: 2 });
  }

  function esc(s) {
    return String(s ?? '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  }

  function appendTicker(sql) {
    if (!sql) return;
    sqlTicker.textContent += '\n' + sql;
    sqlTicker.scrollTop = sqlTicker.scrollHeight;
  }

  // ── Scoreboard ────────────────────────────────────────────────────────────────

  function updateScoreboard(state) {
    raceCountBadge.textContent = 'Race #' + (state.race_count ?? 0);

    hftPnl.textContent    = fmt$(state.hft_pnl    ?? 0);
    hftWins.textContent   = state.hft_wins    ?? 0;
    retailPnl.textContent = fmt$(state.retail_pnl ?? 0);
    retailWins.textContent = state.retail_wins ?? 0;

    if (state.ny_price != null) nyPrice.textContent  = fmt$(state.ny_price);
    if (state.chi_price != null) chiPrice.textContent = fmt$(state.chi_price);

    renderRaces(state.races ?? []);
  }

  // ── Race History Table ────────────────────────────────────────────────────────

  function renderRaces(races) {
    if (!races.length) {
      tblRaces.innerHTML = '<tr><td colspan="8" class="text-muted text-center py-3">No races yet. Press Trigger.</td></tr>';
      return;
    }
    tblRaces.innerHTML = races.map(r => {
      const isHft   = r.winner === 'hft';
      const winnerLabel = isHft
        ? '<span class="badge bg-warning text-dark">⚡ HFT</span>'
        : '<span class="badge bg-info text-dark">💻 Retail</span>';
      const rowCls = isHft ? 'table-warning' : 'table-info';
      return `<tr class="${rowCls}" style="opacity:.9;">
        <td>${esc(r.id)}</td>
        <td>${esc(r.hft_network)}</td>
        <td>${esc(r.retail_setup)}</td>
        <td>${Number(r.hft_latency_ms).toFixed(2)}</td>
        <td>${Number(r.ret_latency_ms).toFixed(2)}</td>
        <td>${(Number(r.ret_latency_ms) - Number(r.hft_latency_ms)).toFixed(2)} ms</td>
        <td>${winnerLabel}</td>
        <td class="fw-bold text-success">${fmt$(r.profit)}</td>
      </tr>`;
    }).join('');
  }

  // ── Race Animation ────────────────────────────────────────────────────────────

  function resetBars() {
    hftBar.style.width        = '0%';
    hftBar.className          = 'progress-bar bg-warning';
    hftBar.textContent        = '';
    retailBar.style.width     = '0%';
    retailBar.className       = 'progress-bar bg-info';
    retailBar.textContent     = '';
    hftStatus.textContent     = 'Waiting…';
    hftStatus.style.color     = '#e3b341';
    retailStatus.textContent  = 'Waiting…';
    retailStatus.style.color  = '#58a6ff';
  }

  function runRace(data) {
    const hftMs  = data.hft_latency_ms;
    const retMs  = data.ret_latency_ms;
    const winner = data.last_race_result; // 'hft' or 'retail'

    const minMs  = Math.min(hftMs, retMs);
    const maxMs  = Math.max(hftMs, retMs);

    const winnerDuration   = WINNER_ANIM;
    const rawLoserDuration = WINNER_ANIM * (maxMs / minMs);
    // Fix 2: cap loser so it finishes max 1.5 s after winner
    const loserDuration    = Math.min(rawLoserDuration, WINNER_ANIM + 1500);

    const hftDuration    = hftMs  <= retMs ? winnerDuration : loserDuration;
    const retailDuration = retMs  <= hftMs ? winnerDuration : loserDuration;

    let hftDone    = false;
    let retailDone = false;

    appendTicker(data.current_sql ?? '');

    // Update latency labels with the actual jittered values
    hftLatencyLabel.textContent = 'Latency: ' + hftMs.toFixed(2) + ' ms';
    retLatencyLabel.textContent = 'Latency: ' + retMs.toFixed(2) + ' ms';

    nyPrice.textContent  = data.ny_price  != null ? fmt$(data.ny_price)  : '$99.95';
    chiPrice.textContent = data.chi_price != null ? fmt$(data.chi_price) : '$100.00';

    const start = performance.now();

    function frame(now) {
      const elapsed = now - start;

      const hftPct   = Math.min(100, (elapsed / hftDuration)    * 100);
      const retPct   = Math.min(100, (elapsed / retailDuration) * 100);

      hftBar.style.width    = hftPct  + '%';
      retailBar.style.width = retPct  + '%';

      if (hftPct >= 100 && !hftDone) {
        hftDone = true;
        if (winner === 'hft') {
          hftBar.className      = 'progress-bar bg-success';
          hftBar.textContent    = '✓ ORDER FILLED +$5.00';
          hftStatus.textContent = '✓ FILLED +$5.00';
          hftStatus.style.color = '#3fb950';
        } else {
          hftBar.className      = 'progress-bar bg-danger';
          hftBar.textContent    = '✗ REJECTED';
          hftStatus.textContent = '✗ REJECTED';
          hftStatus.style.color = '#f85149';
        }
      }

      if (retPct >= 100 && !retailDone) {
        retailDone = true;
        if (winner === 'retail') {
          retailBar.className      = 'progress-bar bg-success';
          retailBar.textContent    = '✓ ORDER FILLED +$5.00';
          retailStatus.textContent = '✓ FILLED +$5.00';
          retailStatus.style.color = '#3fb950';
        } else {
          retailBar.className      = 'progress-bar bg-danger';
          retailBar.textContent    = '✗ REJECTED';
          retailStatus.textContent = '✗ REJECTED';
          retailStatus.style.color = '#f85149';
        }
      }

      if (hftPct < 100 || retPct < 100) {
        requestAnimationFrame(frame);
      } else {
        updateScoreboard(data);
        triggerBtn.disabled = false;
        resetBtn.disabled   = false;
      }
    }

    requestAnimationFrame(frame);
  }

  // ── Trigger ───────────────────────────────────────────────────────────────────

  triggerBtn.addEventListener('click', () => {
    triggerBtn.disabled = true;
    resetBtn.disabled   = true;
    resetBars();

    hftStatus.textContent    = 'Racing…';
    retailStatus.textContent = 'Racing…';

    const body = new URLSearchParams({
      network: getNetwork(),
      setup:   getSetup(),
    });

    fetch('/demos/hft/trigger', { method: 'POST', body })
      .then(r => {
        if (!r.ok) return r.json().then(e => { throw new Error(e.error ?? 'Error'); });
        return r.json();
      })
      .then(data => runRace(data))
      .catch(err => {
        hftStatus.textContent    = 'Error';
        retailStatus.textContent = 'Error';
        appendTicker('-- ERROR: ' + err.message);
        triggerBtn.disabled = false;
        resetBtn.disabled   = false;
      });
  });

  // ── Reset ─────────────────────────────────────────────────────────────────────

  resetBtn.addEventListener('click', () => {
    resetBtn.disabled   = true;
    triggerBtn.disabled = true;

    fetch('/demos/hft/reset', { method: 'POST' })
      .then(() => fetch('/demos/hft/state'))
      .then(r => r.json())
      .then(state => {
        resetBars();
        sqlTicker.textContent = '-- HFT demo ready. Configure and press Trigger.';
        nyPrice.textContent   = '$100.00';
        chiPrice.textContent  = '$100.00';
        updateScoreboard(state);
        updateConfigLabels();
        triggerBtn.disabled = false;
        resetBtn.disabled   = false;
      })
      .catch(() => {
        triggerBtn.disabled = false;
        resetBtn.disabled   = false;
      });
  });

  // ── Init ──────────────────────────────────────────────────────────────────────

  updateConfigLabels();

  fetch('/demos/hft/state')
    .then(r => r.json())
    .then(state => updateScoreboard(state))
    .catch(() => {});
});
