/* trigger_chain.js — Trigger Chain Demo */

document.addEventListener('DOMContentLoaded', () => {
  const connSelect = document.getElementById('conn-select');
  const insertBtn = document.getElementById('insert-btn');
  const productInput = document.getElementById('product-input');
  const qtyInput = document.getElementById('qty-input');
  const ordersTbody = document.getElementById('orders-tbody');
  const auditTbody = document.getElementById('audit-tbody');
  const lightning = document.getElementById('lightning-icon');

  function getConnId() {
    return connSelect ? connSelect.value : '';
  }

  function escHtml(s) {
    return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  }

  function refreshData(connId) {
    if (!connId) return;
    fetch('/demos/trigger-chain/data?conn_id=' + connId)
      .then(r => r.json())
      .then(data => {
        // Orders
        if (!data.orders || data.orders.length === 0) {
          ordersTbody.innerHTML = '<tr><td colspan="4" class="text-muted text-center">No orders yet</td></tr>';
        } else {
          ordersTbody.innerHTML = data.orders.map(o =>
            '<tr><td>' + o.id + '</td><td>' + escHtml(o.product) +
            '</td><td>' + o.qty + '</td><td class="text-muted small">' + escHtml(o.ts || '') + '</td></tr>'
          ).join('');
        }

        // Audit
        if (!data.audit_log || data.audit_log.length === 0) {
          auditTbody.innerHTML = '<tr><td colspan="5" class="text-muted text-center">No audit entries yet</td></tr>';
        } else {
          auditTbody.innerHTML = data.audit_log.map(a =>
            '<tr><td>' + a.id + '</td><td><span class="badge bg-warning text-dark">' +
            escHtml(a.action) + '</span></td><td>' + escHtml(a.table_name) +
            '</td><td class="font-monospace small" style="max-width:180px;word-break:break-all;">' +
            escHtml(a.row_data || '') + '</td><td class="text-muted small">' +
            escHtml(a.ts || '') + '</td></tr>'
          ).join('');
        }
      })
      .catch(() => {});
  }

  if (insertBtn) {
    insertBtn.addEventListener('click', async () => {
      const connId = getConnId();
      if (!connId) return;
      const product = productInput ? productInput.value.trim() || 'Widget' : 'Widget';
      const qty = qtyInput ? parseInt(qtyInput.value) || 1 : 1;

      const fd = new FormData();
      fd.append('conn_id', connId);
      fd.append('product', product);
      fd.append('qty', qty);

      try {
        insertBtn.disabled = true;
        await fetch('/demos/trigger-chain/insert', { method: 'POST', body: fd });

        // Flash lightning
        if (lightning) {
          lightning.classList.add('flash');
          setTimeout(() => lightning.classList.remove('flash'), 600);
        }

        setTimeout(() => refreshData(connId), 300);
      } catch (err) {
        // silent
      } finally {
        insertBtn.disabled = false;
      }
    });
  }

  if (connSelect) {
    connSelect.addEventListener('change', () => refreshData(getConnId()));
    refreshData(getConnId());
  }

  // Auto-refresh every 3 seconds
  setInterval(() => refreshData(getConnId()), 3000);
});
