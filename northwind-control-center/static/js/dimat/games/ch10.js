/* ch10 — Euler Tracer: trace an Euler circuit by clicking edges in order. */
(() => {
  const PRESETS = [
    // Each preset: nodes (positions on unit circle), edges, has_circuit
    {label: 'C₄', n: 4, edges: [[0,1],[1,2],[2,3],[3,0]]},
    {label: 'K₃', n: 3, edges: [[0,1],[1,2],[2,0]]},
    {label: 'K₅', n: 5, edges: [[0,1],[0,2],[0,3],[0,4],[1,2],[1,3],[1,4],[2,3],[2,4],[3,4]]},
    {label: 'Octa', n: 6, edges: [[0,1],[0,2],[0,3],[0,4],[1,5],[2,5],[3,5],[4,5],[1,2],[2,3],[3,4],[4,1]]},
  ];

  function nodePos(n, w, h) {
    const cx = w / 2, cy = h / 2;
    const r = Math.min(w, h) * 0.36;
    return Array.from({length: n}, (_, i) => ({
      x: cx + r * Math.cos(2 * Math.PI * i / n - Math.PI / 2),
      y: cy + r * Math.sin(2 * Math.PI * i / n - Math.PI / 2),
    }));
  }

  function start(host, ctx) {
    const L = window.DimatGameLib;
    host.innerHTML = '';
    const preset = L.choice(PRESETS);
    let visited = new Set();
    let cur = 0;
    const overlay = L.makeOverlay(host,
      `<strong>Euler-kör keresés:</strong> ${preset.label}. Kattints élekre sorrendben — mindegyiket pontosan egyszer.<br>
       <span style="color:#94a3b8;font-size:.7rem">Kezdés: csúcs 1. Befejezés: vissza ide.</span>`);
    const canvas = L.makeCanvas(host);
    const score = L.scoreBadge(host);
    const timer = L.timer(host, {limit: 60}, () => finish(false));

    const restartBtn = ctx.el('button', {class: 'dq-btn',
      style: {position: 'absolute', right: '.6rem', bottom: '.6rem', zIndex: 5},
      onclick: () => start(host, ctx)}, '↻ Reset');
    host.appendChild(restartBtn);

    let positions = [];
    function paint() {
      const {ctx: cx, w, h} = L.fitCanvas(canvas);
      cx.fillStyle = '#0d1117'; cx.fillRect(0, 0, w, h);
      positions = nodePos(preset.n, w, h);
      preset.edges.forEach((e, i) => {
        const [u, v] = e;
        const visited_ = visited.has(i);
        L.drawEdge(cx, positions[u].x, positions[u].y, positions[v].x, positions[v].y,
          {color: visited_ ? '#34d399' : '#475569', width: visited_ ? 4 : 2});
      });
      positions.forEach((p, i) => {
        L.drawNode(cx, p.x, p.y, 14, i === cur ? '#fbbf24' : '#38bdf8',
          (i + 1).toString(), {stroke: '#0e1014', lw: 2});
      });
    }

    canvas.addEventListener('click', (e) => {
      const rect = canvas.getBoundingClientRect();
      const mx = e.clientX - rect.left, my = e.clientY - rect.top;
      // Find clicked edge nearest to (mx, my) involving cur
      let best = -1, bestD = 32 * 32;
      preset.edges.forEach((edge, i) => {
        if (visited.has(i)) return;
        const [u, v] = edge;
        if (u !== cur && v !== cur) return;
        // Distance from point to line midpoint
        const x = (positions[u].x + positions[v].x) / 2;
        const y = (positions[u].y + positions[v].y) / 2;
        const d = (x - mx) ** 2 + (y - my) ** 2;
        if (d < bestD) { bestD = d; best = i; }
      });
      if (best >= 0) {
        visited.add(best);
        const [u, v] = preset.edges[best];
        cur = (u === cur) ? v : u;
        score.add(15);
        paint();
        if (visited.size === preset.edges.length && cur === 0) {
          finish(true);
        } else if (visited.size === preset.edges.length) {
          finish(false);
        }
      }
    });

    function finish(success) {
      timer.stop();
      const max = preset.edges.length * 15;
      const s = success ? score.get() : Math.max(0, score.get() - 20);
      ctx.onScore(s, max);
      L.endScreen(host, {
        score: s, max,
        msg: success ? 'Sikeresen Euler-kört rajzoltál!' : 'Próbáld újra — minden élt egyszer, vissza a kezdőcsúcsba.',
        onAgain: () => start(host, ctx),
      });
    }

    paint();
    window.addEventListener('resize', paint);
  }

  function startText(pane, ctx) {
    const L = window.DimatGameLib;
    const QS = [
      {prompt: 'Mikor van egy gráfnak Euler-köre?', options: ['Minden csúcs foka páros és összefüggő', 'Csak fa-gráfoknak', 'Csak K_n-eknek', 'Mindig'], answer: 0},
      {prompt: 'Mikor van Euler-útja (de nem köre)?', options: ['Pontosan 2 páratlan fokú csúcs', 'Minden csúcs páratlan', 'Páros sok él', 'Soha'], answer: 0},
      {prompt: 'Königsberg hidak: mennyi páratlan fokú?', options: ['4', '0', '2', '7'], answer: 0},
      {prompt: 'K₅ tartalmaz-e Euler-kört?', options: ['Igen — minden csúcs foka 4', 'Nem', 'Csak ha n páros', 'Nem értelmes'], answer: 0},
      {prompt: 'Fleury algoritmus mire való?', options: ['Euler-kör konstrukció lépésenként', 'Hamilton-ciklus', 'Színezés', 'Min vágás'], answer: 0},
    ];
    L.textModeQuiz(pane, QS, (s, m) => ctx.onScore(s * 15, m * 15));
  }

  window.DimatGames.register('ch10', {title: 'Euler Tracer', icon: '🚶', hint: 'Klikkelj élekre sorrendben — mindegyiket egyszer, vissza a kezdéshez.', start, startText});
})();
