document.addEventListener('DOMContentLoaded', function () {
  const picker = document.getElementById('queryPicker');
  const descEl = document.getElementById('queryDesc');
  const loadCyBtn = document.getElementById('loadCyBtn');
  const cyEl = document.getElementById('cy');

  if (picker && descEl && typeof queryDescs !== 'undefined') {
    function updateDesc() {
      descEl.textContent = queryDescs[picker.value] || '';
    }
    picker.addEventListener('change', updateDesc);
    updateDesc();
  }

  if (loadCyBtn && cyEl && typeof selectedKey !== 'undefined' && selectedKey) {
    loadCyBtn.addEventListener('click', async function () {
      loadCyBtn.disabled = true;
      loadCyBtn.textContent = 'Loading…';
      try {
        const r = await fetch(`/graph/data/${selectedKey}`);
        const data = await r.json();
        if (data.error) {
          cyEl.textContent = data.error;
          return;
        }
        cytoscape({
          container: cyEl,
          elements: data.elements,
          style: [
            {
              selector: 'node',
              style: {
                label: 'data(label)',
                'background-color': '#4e73df',
                color: '#fff',
                'text-valign': 'center',
                'text-halign': 'center',
                'font-size': '11px',
                width: 60,
                height: 60,
              },
            },
            {
              selector: 'edge',
              style: {
                width: 2,
                'line-color': '#aab',
                'target-arrow-color': '#aab',
                'target-arrow-shape': 'triangle',
                'curve-style': 'bezier',
              },
            },
          ],
          layout: { name: 'breadthfirst', directed: true, padding: 20 },
        });
        loadCyBtn.textContent = 'Reload';
        loadCyBtn.disabled = false;
      } catch (err) {
        cyEl.textContent = 'Failed to load graph data.';
        loadCyBtn.disabled = false;
      }
    });
  }
});
