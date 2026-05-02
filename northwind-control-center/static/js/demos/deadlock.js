/* deadlock.js — Three-way Deadlock Detection Demo */

document.addEventListener('DOMContentLoaded', () => {
  const runBtn    = document.getElementById('run-deadlock-btn');
  const pgSelect  = document.getElementById('pg-conn-select');
  const txA       = document.getElementById('tx-a-node');
  const txB       = document.getElementById('tx-b-node');
  const txC       = document.getElementById('tx-c-node');
  const resultCard = document.getElementById('deadlock-result');
  const resultBody = document.getElementById('deadlock-result-body');
  const arrows    = ['arrow-ab', 'arrow-bc', 'arrow-ca'].map(id => document.getElementById(id));

  if (!runBtn) return;

  const nodes = { A: txA, B: txB, C: txC };

  function reset() {
    Object.values(nodes).forEach(n => {
      n.classList.remove('waiting', 'victim', 'committed');
    });
    arrows.forEach(a => {
      if (a) a.classList.remove('active', 'resolved');
    });
    resultCard.classList.add('d-none');
    resultBody.innerHTML = '';
  }

  runBtn.addEventListener('click', async () => {
    const connId = pgSelect ? pgSelect.value : '';
    if (!connId) return;

    runBtn.disabled = true;
    reset();

    // All three show waiting + arrows turn yellow
    Object.values(nodes).forEach(n => n.classList.add('waiting'));
    arrows.forEach(a => { if (a) a.classList.add('active'); });

    try {
      const fd = new FormData();
      fd.append('conn_id', connId);
      const resp = await fetch('/demos/deadlock/run', { method: 'POST', body: fd });
      const result = await resp.json();

      // Stop pulsing
      Object.values(nodes).forEach(n => n.classList.remove('waiting'));
      arrows.forEach(a => { if (a) { a.classList.remove('active'); a.classList.add('resolved'); } });

      if (result.error && !result.victim) {
        resultBody.innerHTML = '<span class="text-danger">Error: ' + esc(result.error) + '</span>';
        resultCard.classList.remove('d-none');
        return;
      }

      // Mark victim red, others green
      ['A', 'B', 'C'].forEach(label => {
        const node = nodes[label];
        if (node) {
          if (result.victim === label) {
            node.classList.add('victim');
          } else {
            node.classList.add('committed');
          }
        }
      });

      // Result summary
      let html = '';
      if (result.victim) {
        html += '<div class="mb-2"><span class="badge bg-danger fs-6">&#x1F480; Victim: Thread ' + esc(result.victim) + '</span>'
          + ' <span class="text-muted">— rolled back by PostgreSQL deadlock detector</span></div>';
      }

      const threadData = { A: result.thread_a, B: result.thread_b, C: result.thread_c };
      ['A', 'B', 'C'].forEach(label => {
        const t = threadData[label];
        if (!t) return;
        const icon = label === result.victim ? '&#x274C;' : '&#x2705;';
        const status = t.ok
          ? '<span class="text-success">Committed</span>'
          : '<span class="text-danger">Rolled back</span>';
        const errMsg = (!t.ok && t.error)
          ? ' <span class="text-muted">— ' + esc(t.error.split('\n')[0].substring(0, 80)) + '</span>'
          : '';
        html += '<div class="mb-1">' + icon + ' <strong>Thread ' + label + ':</strong> ' + status + errMsg + '</div>';
      });

      html += '<div class="text-muted mt-2 border-top pt-2">Elapsed: ' + (result.elapsed_ms || 0) + ' ms</div>';
      resultBody.innerHTML = html;
      resultCard.classList.remove('d-none');

    } catch (err) {
      Object.values(nodes).forEach(n => n.classList.remove('waiting'));
      resultBody.innerHTML = '<span class="text-danger">Request failed: ' + esc(err.message) + '</span>';
      resultCard.classList.remove('d-none');
    } finally {
      runBtn.disabled = false;
    }
  });

  function esc(s) {
    return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  }
});
