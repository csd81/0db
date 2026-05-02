/* deadlock.js — Deadlock Detection Demo */

document.addEventListener('DOMContentLoaded', () => {
  const runBtn = document.getElementById('run-deadlock-btn');
  const pgSelect = document.getElementById('pg-conn-select');
  const txA = document.getElementById('tx-a-node');
  const txB = document.getElementById('tx-b-node');
  const resultCard = document.getElementById('deadlock-result');
  const resultBody = document.getElementById('deadlock-result-body');

  if (!runBtn) return;

  runBtn.addEventListener('click', async () => {
    const connId = pgSelect ? pgSelect.value : '';
    if (!connId) return;

    runBtn.disabled = true;
    resultCard.classList.add('d-none');
    resultBody.innerHTML = '';

    // Reset node states
    [txA, txB].forEach(n => {
      n.classList.remove('waiting', 'victim', 'committed');
    });

    // Show waiting state
    txA.classList.add('waiting');
    txB.classList.add('waiting');

    try {
      const fd = new FormData();
      fd.append('conn_id', connId);
      const resp = await fetch('/demos/deadlock/run', { method: 'POST', body: fd });
      const result = await resp.json();

      // Remove waiting
      txA.classList.remove('waiting');
      txB.classList.remove('waiting');

      if (result.error && !result.victim) {
        resultBody.innerHTML = '<span class="text-danger">Error: ' + escHtml(result.error) + '</span>';
        resultCard.classList.remove('d-none');
        return;
      }

      // Apply outcome classes
      if (result.victim === 'A') {
        txA.classList.add('victim');
        txB.classList.add('committed');
      } else if (result.victim === 'B') {
        txB.classList.add('victim');
        txA.classList.add('committed');
      } else {
        txA.classList.add('committed');
        txB.classList.add('committed');
      }

      let html = '';
      if (result.victim) {
        html += '<div class="mb-2"><span class="badge bg-danger">Victim: Thread ' + result.victim + '</span></div>';
      }
      if (result.thread_a) {
        html += '<div><strong>Thread A:</strong> ' +
          (result.thread_a.ok ? '<span class="text-success">Committed</span>' :
           '<span class="text-danger">Rolled back — ' + escHtml(result.thread_a.error || '') + '</span>') +
          '</div>';
      }
      if (result.thread_b) {
        html += '<div><strong>Thread B:</strong> ' +
          (result.thread_b.ok ? '<span class="text-success">Committed</span>' :
           '<span class="text-danger">Rolled back — ' + escHtml(result.thread_b.error || '') + '</span>') +
          '</div>';
      }
      html += '<div class="text-muted mt-2">Elapsed: ' + (result.elapsed_ms || 0) + ' ms</div>';
      resultBody.innerHTML = html;
      resultCard.classList.remove('d-none');

    } catch (err) {
      txA.classList.remove('waiting');
      txB.classList.remove('waiting');
      resultBody.innerHTML = '<span class="text-danger">Request failed: ' + escHtml(err.message) + '</span>';
      resultCard.classList.remove('d-none');
    } finally {
      runBtn.disabled = false;
    }
  });

  function escHtml(s) {
    return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  }
});
