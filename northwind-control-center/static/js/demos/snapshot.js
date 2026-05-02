/* snapshot.js — Snapshot Replication Demo (Cytoscape.js) */

// window.addEventListener beforeunload placeholder
// (no SSE here, nothing to close)
window.addEventListener('beforeunload', () => { /* no SSE here, nothing to close */ });

document.addEventListener('DOMContentLoaded', () => {
  const pushBtn = document.getElementById('push-btn');
  const resetBtn = document.getElementById('reset-btn');

  const BRANCH_COUNT = 6;
  const RADIUS = 200;
  const CENTER_X = 300;
  const CENTER_Y = 300;

  // Build nodes + edges
  const elements = [];

  // HQ node
  elements.push({ data: { id: 'hq', label: 'HQ' }, classes: 'hq' });

  // Branch nodes arranged around a circle
  for (let i = 1; i <= BRANCH_COUNT; i++) {
    const angle = (2 * Math.PI * (i - 1)) / BRANCH_COUNT - Math.PI / 2;
    const x = CENTER_X + RADIUS * Math.cos(angle);
    const y = CENTER_Y + RADIUS * Math.sin(angle);
    elements.push({
      data: { id: 'b' + i, label: 'Branch ' + i, origLabel: 'Branch ' + i },
      position: { x, y },
      classes: 'branch',
    });
    elements.push({ data: { id: 'e' + i, source: 'hq', target: 'b' + i } });
  }

  const cy = cytoscape({
    container: document.getElementById('cy'),
    elements,
    layout: { name: 'preset' },
    style: [
      {
        selector: 'node.hq',
        style: {
          'background-color': '#0d6efd',
          'label': 'data(label)',
          'color': '#fff',
          'text-valign': 'center',
          'font-weight': 'bold',
          'width': 70,
          'height': 70,
          'font-size': 14,
        },
      },
      {
        selector: 'node.branch',
        style: {
          'background-color': '#343a40',
          'label': 'data(label)',
          'color': '#adb5bd',
          'text-valign': 'bottom',
          'text-margin-y': 6,
          'width': 50,
          'height': 50,
          'font-size': 12,
        },
      },
      {
        selector: 'edge',
        style: {
          'line-color': '#6c757d',
          'target-arrow-color': '#6c757d',
          'target-arrow-shape': 'triangle',
          'curve-style': 'straight',
          'width': 2,
        },
      },
      {
        selector: 'edge.active',
        style: {
          'line-color': '#198754',
          'target-arrow-color': '#198754',
          'width': 3,
        },
      },
      {
        selector: 'node.updated',
        style: {
          'background-color': '#0f5132',
          'color': '#75b798',
        },
      },
    ],
  });

  // Position HQ at center
  cy.$('#hq').position({ x: CENTER_X, y: CENTER_Y });

  let animRunning = false;

  function resetAll() {
    for (let i = 1; i <= BRANCH_COUNT; i++) {
      const branch = cy.$('#b' + i);
      const edge = cy.$('#e' + i);
      branch.removeClass('updated');
      branch.data('label', branch.data('origLabel'));
      edge.removeClass('active');
    }
    if (pushBtn) pushBtn.disabled = false;
    animRunning = false;
  }

  if (pushBtn) {
    pushBtn.addEventListener('click', () => {
      if (animRunning) return;
      animRunning = true;
      pushBtn.disabled = true;

      // Reset first
      for (let i = 1; i <= BRANCH_COUNT; i++) {
        cy.$('#b' + i).removeClass('updated');
        cy.$('#e' + i).removeClass('active');
        cy.$('#b' + i).data('label', cy.$('#b' + i).data('origLabel'));
      }

      // Animate each branch with 1-second delay
      for (let i = 1; i <= BRANCH_COUNT; i++) {
        (function(idx) {
          setTimeout(() => {
            const edge = cy.$('#e' + idx);
            const branch = cy.$('#b' + idx);
            edge.addClass('active');
            setTimeout(() => {
              branch.addClass('updated');
              branch.data('label', branch.data('origLabel') + '\nUpdated ✓');
              if (idx === BRANCH_COUNT) {
                // All done
                pushBtn.disabled = false;
                animRunning = false;
              }
            }, 500);
          }, (idx - 1) * 1000);
        })(i);
      }
    });
  }

  if (resetBtn) {
    resetBtn.addEventListener('click', resetAll);
  }
});
