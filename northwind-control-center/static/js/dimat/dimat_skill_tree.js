/* dimat_skill_tree.js — canvas renderer for the chapter prereq graph.
   Pure visualisation; clicking a node navigates to /demos/dimat/<ch>.
   No hard locks — every node is reachable regardless of progress. */
(async () => {
  'use strict';
  const canvas = document.getElementById('dq-skill-tree-canvas');
  if (!canvas) return;

  const J = (url) => fetch(url, {credentials:'same-origin'}).then(r => r.ok ? r.json() : {});
  const tree = await J('/demos/dimat/api/skill_tree');
  const me = await J('/demos/dimat/api/me');
  const perCh = me.per_chapter || {};

  // Lay out nodes by chapter index in a grid (5 cols × 5 rows)
  const COLS = 5;
  const layout = {};
  tree.nodes.forEach((n, i) => {
    const row = Math.floor(i / COLS);
    const col = i % COLS;
    layout[n.ch] = {row, col, n};
  });

  function fit() {
    const dpr = window.devicePixelRatio || 1;
    const rect = canvas.getBoundingClientRect();
    canvas.width = rect.width * dpr;
    canvas.height = rect.height * dpr;
    const ctx = canvas.getContext('2d');
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    return {ctx, w: rect.width, h: rect.height};
  }

  function pos(ch, w, h) {
    const lo = layout[ch];
    if (!lo) return null;
    const x = (lo.col + 0.5) / COLS * w;
    const rows = Math.ceil(tree.nodes.length / COLS);
    const y = (lo.row + 0.5) / rows * h;
    return {x, y};
  }

  function draw() {
    const {ctx, w, h} = fit();
    ctx.fillStyle = '#0d1117'; ctx.fillRect(0, 0, w, h);

    // Edges (with arrowheads)
    ctx.strokeStyle = '#334155'; ctx.lineWidth = 1.2;
    tree.edges.forEach(e => {
      const a = pos(e.from, w, h), b = pos(e.to, w, h);
      if (!a || !b) return;
      const dx = b.x - a.x, dy = b.y - a.y, len = Math.hypot(dx, dy);
      const r = 32;
      const sx = a.x + dx / len * r, sy = a.y + dy / len * r;
      const ex = b.x - dx / len * r, ey = b.y - dy / len * r;
      ctx.beginPath(); ctx.moveTo(sx, sy); ctx.lineTo(ex, ey); ctx.stroke();
      // Arrowhead
      const ang = Math.atan2(ey - sy, ex - sx);
      const ah = 7;
      ctx.beginPath(); ctx.moveTo(ex, ey);
      ctx.lineTo(ex - ah * Math.cos(ang - .45), ey - ah * Math.sin(ang - .45));
      ctx.lineTo(ex - ah * Math.cos(ang + .45), ey - ah * Math.sin(ang + .45));
      ctx.closePath(); ctx.fillStyle = '#334155'; ctx.fill();
    });

    // Nodes
    tree.nodes.forEach(n => {
      const p = pos(n.ch, w, h);
      if (!p) return;
      const stats = perCh[n.ch] || {};
      const solved = stats.solved || 0;
      const total = n.count || 0;
      const ratio = total > 0 ? solved / total : 0;
      const partColour = n.ch === 'appendix' ? '#a78bfa'
        : (parseInt(n.ch.slice(2)) || 0) < 9 ? '#10b981'
        : '#38bdf8';
      // Outer circle (filled by progress)
      ctx.beginPath(); ctx.arc(p.x, p.y, 28, 0, Math.PI * 2);
      ctx.fillStyle = '#161b22'; ctx.fill();
      ctx.strokeStyle = partColour; ctx.lineWidth = 2; ctx.stroke();
      // Progress arc
      if (ratio > 0) {
        ctx.beginPath();
        ctx.arc(p.x, p.y, 28, -Math.PI / 2, -Math.PI / 2 + ratio * Math.PI * 2);
        ctx.lineWidth = 4; ctx.strokeStyle = '#34d399'; ctx.stroke();
      }
      // Label
      ctx.fillStyle = '#e6edf3'; ctx.font = 'bold 12px sans-serif';
      ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
      ctx.fillText(n.ch, p.x, p.y - 4);
      ctx.font = '9px sans-serif'; ctx.fillStyle = '#8b949e';
      ctx.fillText(`${solved}/${total}`, p.x, p.y + 10);
    });
  }

  function hit(mx, my, w, h) {
    for (const n of tree.nodes) {
      const p = pos(n.ch, w, h);
      if (!p) continue;
      if ((p.x - mx) ** 2 + (p.y - my) ** 2 < 28 * 28) return n.ch;
    }
    return null;
  }

  canvas.addEventListener('click', (e) => {
    const rect = canvas.getBoundingClientRect();
    const mx = e.clientX - rect.left, my = e.clientY - rect.top;
    const ch = hit(mx, my, rect.width, rect.height);
    if (ch) window.location.href = '/demos/dimat/' + ch;
  });
  canvas.addEventListener('mousemove', (e) => {
    const rect = canvas.getBoundingClientRect();
    const mx = e.clientX - rect.left, my = e.clientY - rect.top;
    canvas.style.cursor = hit(mx, my, rect.width, rect.height) ? 'pointer' : 'default';
  });

  draw();
  window.addEventListener('resize', draw);
})();
