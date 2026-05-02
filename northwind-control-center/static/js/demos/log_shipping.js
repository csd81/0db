/* log_shipping.js — Log Shipping Demo */

document.addEventListener('DOMContentLoaded', () => {
  const masterSelect = document.getElementById('master-select');
  const replicaSelect = document.getElementById('replica-select');
  const runStepBtn = document.getElementById('run-step-btn');
  const insertMasterBtn = document.getElementById('insert-master-btn');
  const stepResult = document.getElementById('step-result');

  const badgeMaster = document.getElementById('badge-master');
  const badgeReplica = document.getElementById('badge-replica');
  const badgePending = document.getElementById('badge-pending');
  const badgeSync = document.getElementById('badge-sync');

  function getMasterConnId() { return masterSelect ? masterSelect.value : ''; }
  function getReplicaConnId() { return replicaSelect ? replicaSelect.value : ''; }

  function setStepOpacity(stepNum, opacity) {
    const el = document.getElementById('step-' + stepNum);
    if (el) el.style.opacity = opacity;
  }

  function refreshState() {
    const m = getMasterConnId();
    const r = getReplicaConnId();
    if (!m || !r) return;
    fetch('/demos/log-shipping/state?master_conn_id=' + m + '&replica_conn_id=' + r)
      .then(resp => resp.json())
      .then(state => {
        if (badgeMaster) badgeMaster.textContent = 'Master: ' + state.master_log_count + ' entries';
        if (badgeReplica) badgeReplica.textContent = 'Replica: ' + state.replica_log_count + ' entries';
        if (badgePending) badgePending.textContent = 'Pending: ' + state.pending_count;
        if (badgeSync) {
          if (state.in_sync) {
            badgeSync.classList.remove('d-none');
            // activate all steps
            [1, 2, 3, 4, 5].forEach(i => setStepOpacity(i, '1'));
          } else {
            badgeSync.classList.add('d-none');
          }
        }
      })
      .catch(() => {});
  }

  function animateStepSequence(onDone) {
    [1, 2, 3, 4, 5].forEach(i => setStepOpacity(i, '0.3'));
    let i = 1;
    function next() {
      if (i > 5) { if (onDone) onDone(); return; }
      setStepOpacity(i, '1');
      i++;
      setTimeout(next, 300);
    }
    setTimeout(next, 100);
  }

  if (runStepBtn) {
    runStepBtn.addEventListener('click', async () => {
      const m = getMasterConnId();
      const r = getReplicaConnId();
      if (!m || !r) return;

      runStepBtn.disabled = true;
      if (stepResult) stepResult.textContent = 'Running...';

      const fd = new FormData();
      fd.append('master_conn_id', m);
      fd.append('replica_conn_id', r);

      try {
        const resp = await fetch('/demos/log-shipping/run', { method: 'POST', body: fd });
        const result = await resp.json();

        animateStepSequence(() => {
          refreshState();
          if (stepResult) {
            stepResult.textContent = result.error
              ? 'Error: ' + result.error
              : 'Replicated ' + result.replicated_count + ' entries.';
          }
        });
      } catch (err) {
        if (stepResult) stepResult.textContent = 'Request failed: ' + err.message;
      } finally {
        runStepBtn.disabled = false;
      }
    });
  }

  if (insertMasterBtn) {
    insertMasterBtn.addEventListener('click', async () => {
      const m = getMasterConnId();
      if (!m) return;
      insertMasterBtn.disabled = true;

      const fd = new FormData();
      fd.append('conn_id', m);
      fd.append('product', 'TestItem');
      fd.append('qty', '1');

      try {
        await fetch('/demos/trigger-chain/insert', { method: 'POST', body: fd });
        setTimeout(refreshState, 400);
      } catch (err) {
        // silent
      } finally {
        insertMasterBtn.disabled = false;
      }
    });
  }

  if (masterSelect) masterSelect.addEventListener('change', refreshState);
  if (replicaSelect) replicaSelect.addEventListener('change', refreshState);

  refreshState();
  // Auto-refresh every 5 seconds
  setInterval(refreshState, 5000);
});
