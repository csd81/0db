/* acid.js — ACID Bank Transfer Demo */

document.addEventListener('DOMContentLoaded', () => {
  const connSelect = document.getElementById('conn-select');
  const form = document.getElementById('transfer-form');
  const stepLog = document.getElementById('step-log');
  const resultBanner = document.getElementById('result-banner');
  const runBtn = document.getElementById('run-btn');

  function getConnId() {
    return connSelect ? connSelect.value : '';
  }

  function updateBalanceCards(balances) {
    const nameMap = {};
    balances.forEach(b => { nameMap[b.id] = b; });
    [1, 2, 3].forEach(id => {
      const el = document.getElementById('bal-' + id);
      if (el && nameMap[id]) {
        el.textContent = '$' + nameMap[id].balance.toFixed(2);
      }
    });
  }

  function flashCard(id, cls) {
    const card = document.getElementById('card-' + id);
    if (!card) return;
    card.classList.add(cls);
    setTimeout(() => card.classList.remove(cls), 1200);
  }

  function fetchAccounts() {
    const connId = getConnId();
    if (!connId) return;
    fetch('/demos/acid/accounts?conn_id=' + connId)
      .then(r => r.json())
      .then(data => updateBalanceCards(data))
      .catch(() => {});
  }

  function appendStep(step) {
    const row = document.createElement('div');
    row.className = 'mb-1';
    const badge = step.ok
      ? '<span class="badge bg-success ms-2">OK</span>'
      : '<span class="badge bg-danger ms-2">FAIL</span>';
    row.innerHTML =
      '<span class="text-muted me-2">#' + step.step + '</span>' +
      '<code class="text-light">' + escHtml(step.sql || '') + '</code>' +
      badge;
    stepLog.appendChild(row);
    stepLog.scrollTop = stepLog.scrollHeight;
  }

  function escHtml(s) {
    return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  }

  function animateSteps(steps, onDone) {
    stepLog.innerHTML = '';
    let i = 0;
    function next() {
      if (i >= steps.length) { if (onDone) onDone(); return; }
      appendStep(steps[i++]);
      setTimeout(next, 300);
    }
    next();
  }

  if (connSelect) {
    fetchAccounts();
    connSelect.addEventListener('change', fetchAccounts);
  }

  if (form) {
    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      runBtn.disabled = true;
      resultBanner.className = 'alert d-none';
      resultBanner.textContent = '';

      const fd = new FormData(form);
      try {
        const resp = await fetch('/demos/acid/run', { method: 'POST', body: fd });
        const result = await resp.json();

        animateSteps(result.steps || [], () => {
          updateBalanceCards(result.final_balances || []);

          if (result.success) {
            resultBanner.className = 'alert alert-success';
            resultBanner.innerHTML = '<strong>COMMITTED ✓</strong> — Transfer completed successfully.';
            (result.final_balances || []).forEach(b => flashCard(b.id, 'flash-green'));
          } else {
            resultBanner.className = 'alert alert-danger';
            resultBanner.innerHTML =
              '<strong>ROLLED BACK ✗</strong> — Balances unchanged.' +
              (result.error ? '<br><small class="font-monospace">' + escHtml(result.error) + '</small>' : '');
            (result.final_balances || []).forEach(b => flashCard(b.id, 'flash-red'));
          }
        });
      } catch (err) {
        resultBanner.className = 'alert alert-danger';
        resultBanner.textContent = 'Request failed: ' + err.message;
      } finally {
        runBtn.disabled = false;
      }
    });
  }
});
