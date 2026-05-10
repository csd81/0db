/* ch1 — Venn Painter: paint regions to match a Boolean formula. */
(() => {
  const FORMULAS = [
    {expr: 'A ∪ B',      pred: (a, b, c) => a || b},
    {expr: 'A ∩ B',      pred: (a, b, c) => a && b},
    {expr: 'A \\ B',     pred: (a, b, c) => a && !b},
    {expr: '(A ∪ B) \\ C', pred: (a, b, c) => (a || b) && !c},
    {expr: 'A △ B',      pred: (a, b, c) => a !== b},
    {expr: 'A ∩ B ∩ C',  pred: (a, b, c) => a && b && c},
    {expr: 'A̅',          pred: (a, b, c) => !a},
    {expr: '(A ∩ B) ∪ C', pred: (a, b, c) => (a && b) || c},
  ];

  // 7 Venn regions (3-circle diagram)
  // Encoded as combos of (inA, inB, inC). The 8th is "outside everything",
  // which we consider a region too.
  const REGIONS = [
    [false, false, false], [true, false, false], [false, true, false], [false, false, true],
    [true, true, false], [true, false, true], [false, true, true], [true, true, true],
  ];

  function start(host, ctx) {
    const L = window.DimatGameLib;
    host.innerHTML = '';
    const target = L.choice(FORMULAS);
    const correctMask = REGIONS.map(([a, b, c]) => target.pred(a, b, c));
    const userMask = REGIONS.map(() => false);

    const overlay = L.makeOverlay(host,
      `<strong>Színezd be a régiókat amelyek megfelelnek:</strong><br><span style="color:#34d399;font-size:1.05rem">${target.expr}</span>`);
    const canvas = L.makeCanvas(host);
    const score = L.scoreBadge(host);

    const submitBtn = ctx.el('button', {class: 'dq-btn dq-btn-primary',
      style: {position: 'absolute', right: '.6rem', bottom: '.6rem', zIndex: 5},
      onclick: submit}, '✓ Beadom');
    host.appendChild(submitBtn);

    function paint() {
      const {ctx: cx, w, h} = L.fitCanvas(canvas);
      cx.fillStyle = '#0d1117'; cx.fillRect(0, 0, w, h);

      const cx0 = w / 2, cy0 = h / 2 + 10;
      const r = Math.min(w, h) * 0.27;
      const positions = [
        {x: cx0 - r * 0.55, y: cy0 - r * 0.32, label: 'A'},
        {x: cx0 + r * 0.55, y: cy0 - r * 0.32, label: 'B'},
        {x: cx0,            y: cy0 + r * 0.5,  label: 'C'},
      ];

      // Fill regions per userMask
      REGIONS.forEach(([a, b, c], idx) => {
        if (idx === 0) return; // outside region — drawn implicitly
        if (!userMask[idx]) return;
        cx.save();
        // Approximate region by sampling pixels — use parametric sweep & flood
        // Cheap version: draw each circle filled, intersect via globalCompositeOperation
        // Alternative simpler approach: stamp small dots in each region
        for (let py = 0; py < h; py += 2) {
          for (let px = 0; px < w; px += 2) {
            const ina = inCircle(px, py, positions[0].x, positions[0].y, r);
            const inb = inCircle(px, py, positions[1].x, positions[1].y, r);
            const inc = inCircle(px, py, positions[2].x, positions[2].y, r);
            if (ina === a && inb === b && inc === c) {
              cx.fillStyle = '#34d399aa';
              cx.fillRect(px, py, 2, 2);
            }
          }
        }
        cx.restore();
      });

      // Outlines
      positions.forEach(p => {
        cx.beginPath(); cx.arc(p.x, p.y, r, 0, Math.PI * 2);
        cx.strokeStyle = '#94a3b8'; cx.lineWidth = 1.5; cx.stroke();
        cx.fillStyle = '#e6edf3'; cx.font = 'bold 16px sans-serif';
        cx.textAlign = 'center'; cx.textBaseline = 'middle';
        cx.fillText(p.label, p.x, p.y - r - 8);
      });

      // Region centers (clickable hotspots)
      const centers = regionCenters(positions, r);
      centers.forEach((c, idx) => {
        if (idx === 0) return;
        cx.beginPath(); cx.arc(c.x, c.y, 9, 0, Math.PI * 2);
        cx.fillStyle = userMask[idx] ? '#34d399' : 'rgba(13,17,23,.85)';
        cx.fill();
        cx.strokeStyle = '#475569'; cx.lineWidth = 1.5; cx.stroke();
      });
    }

    function regionCenters(p, r) {
      // Approximate centers of 8 regions.
      const m = (a, b) => ({x: (a.x + b.x) / 2, y: (a.y + b.y) / 2});
      const c012 = {x: (p[0].x + p[1].x + p[2].x) / 3, y: (p[0].y + p[1].y + p[2].y) / 3};
      return [
        {x: 30, y: 30},                                   // 0: outside
        {x: p[0].x - r * 0.6, y: p[0].y},                  // 1: A only
        {x: p[1].x + r * 0.6, y: p[1].y},                  // 2: B only
        {x: p[2].x, y: p[2].y + r * 0.6},                  // 3: C only
        {x: m(p[0], p[1]).x, y: m(p[0], p[1]).y - r * 0.05}, // 4: A∩B (no C)
        {x: m(p[0], p[2]).x - r * 0.1, y: m(p[0], p[2]).y}, // 5: A∩C (no B)
        {x: m(p[1], p[2]).x + r * 0.1, y: m(p[1], p[2]).y}, // 6: B∩C (no A)
        c012,                                               // 7: A∩B∩C
      ];
    }

    function inCircle(px, py, cx, cy, r) {
      const dx = px - cx, dy = py - cy;
      return dx * dx + dy * dy <= r * r;
    }

    canvas.addEventListener('click', (e) => {
      const rect = canvas.getBoundingClientRect();
      const mx = e.clientX - rect.left, my = e.clientY - rect.top;
      const positions = [
        {x: rect.width / 2 - rect.width * 0.135, y: rect.height / 2 - 10},
        {x: rect.width / 2 + rect.width * 0.135, y: rect.height / 2 - 10},
        {x: rect.width / 2, y: rect.height / 2 + rect.width * 0.135 + 10},
      ];
      const r = Math.min(rect.width, rect.height) * 0.27;
      const centers = regionCenters(positions, r);
      let best = -1, bestD = 28 * 28;
      centers.forEach((c, idx) => {
        const d = (c.x - mx) ** 2 + (c.y - my) ** 2;
        if (d < bestD) { bestD = d; best = idx; }
      });
      if (best >= 0) {
        userMask[best] = !userMask[best];
        paint();
      }
    });

    function submit() {
      let s = 0;
      correctMask.forEach((c, i) => {
        if (i === 0) return; // ignore outside region
        if (c === userMask[i]) s += 10;
        else s -= 5;
      });
      s = Math.max(0, s);
      const max = (correctMask.length - 1) * 10;
      ctx.onScore(s, max);
      L.endScreen(host, {
        score: s, max,
        msg: `Cél: ${target.expr}`,
        onAgain: () => start(host, ctx),
      });
    }

    paint();
    window.addEventListener('resize', paint);
  }

  function startText(pane, ctx) {
    const L = window.DimatGameLib;
    const items = L.shuffle(FORMULAS).slice(0, 5).map(f => {
      const distractors = L.shuffle(FORMULAS.filter(g => g !== f)).slice(0, 3);
      const cells = REGIONS.map(([a, b, c], i) => i === 0 ? null : f.pred(a, b, c) ? '●' : '○').slice(1).join(' ');
      const correctOpt = `Régiók (1..7): ${cells}`;
      const opts = L.shuffle([
        correctOpt,
        ...distractors.map(d => `Régiók (1..7): ${REGIONS.map(([a, b, c], i) => i === 0 ? null : d.pred(a, b, c) ? '●' : '○').slice(1).join(' ')}`),
      ]);
      return {
        prompt: `Melyik régió-mintázat felel meg ennek: ${f.expr}?`,
        options: opts,
        answer: opts.indexOf(correctOpt),
      };
    });
    L.textModeQuiz(pane, items, (s, m) => ctx.onScore(s * 10, m * 10));
  }

  window.DimatGames.register('ch1', {
    title: 'Venn Painter',
    icon: '🎨',
    hint: 'Kattints a régiók közepére a be-/kikapcsoláshoz, majd „Beadom".',
    start, startText,
  });
})();
