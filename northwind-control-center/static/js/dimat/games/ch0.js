/* ch0 — Notation Drag-Match: drag KaTeX-rendered symbols onto definitions. */
(() => {
  const PAIRS = [
    {sym: '𝒫(A)',    def: 'Az A halmaz hatványhalmaza'},
    {sym: '[A]^k',    def: 'k-elemű részhalmazok halmaza'},
    {sym: 'A*',       def: 'véges szavak halmaza A-ból'},
    {sym: '𝒪(f)',    def: 'aszimptotikus felső korlát'},
    {sym: '⌊x⌋',      def: 'alsó egészrész (floor)'},
    {sym: '⌈x⌉',      def: 'felső egészrész (ceiling)'},
    {sym: 'A^ℕ',      def: 'végtelen sorozatok halmaza'},
    {sym: '|A|',      def: 'A halmaz számossága'},
  ];

  function start(host, ctx) {
    const L = window.DimatGameLib;
    host.innerHTML = '';
    const round = L.shuffle(PAIRS).slice(0, 6);
    const score = L.scoreBadge(host);
    const timer = L.timer(host, {limit: 60}, (elapsed) => finish(elapsed));

    const wrap = ctx.el('div', {style: {position: 'absolute', inset: 0, padding: '2.5rem 1rem 1rem',
      display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '.7rem', overflow: 'auto'}});
    host.appendChild(wrap);

    const left = ctx.el('div', {style: {display: 'flex', flexDirection: 'column', gap: '.4rem'}});
    const right = ctx.el('div', {style: {display: 'flex', flexDirection: 'column', gap: '.4rem'}});
    wrap.appendChild(left); wrap.appendChild(right);

    const symButtons = round.map((p, i) => {
      const btn = ctx.el('button', {class: 'dq-btn', 'data-i': i, style: {
        textAlign: 'left', padding: '.6rem .85rem', fontSize: '.95rem',
        fontFamily: 'KaTeX_Main, monospace', color: '#a8d8f0',
      }}, p.sym);
      btn.onclick = () => selectSym(i);
      left.appendChild(btn);
      return btn;
    });

    const defOrder = L.shuffle(round.map((_, i) => i));
    const defButtons = defOrder.map((origIdx) => {
      const btn = ctx.el('button', {class: 'dq-btn', 'data-i': origIdx, style: {
        textAlign: 'left', padding: '.6rem .85rem', fontSize: '.78rem', whiteSpace: 'normal',
      }}, round[origIdx].def);
      btn.onclick = () => selectDef(origIdx);
      right.appendChild(btn);
      return btn;
    });

    let activeSym = null;
    function selectSym(i) {
      if (symButtons[i].disabled) return;
      symButtons.forEach(b => b.classList.remove('selected'));
      symButtons[i].classList.add('selected');
      symButtons[i].style.borderColor = '#38bdf8';
      activeSym = i;
    }
    function selectDef(origIdx) {
      if (activeSym == null) return;
      if (origIdx === activeSym) {
        score.add(10);
        symButtons[activeSym].disabled = true;
        symButtons[activeSym].style.background = '#0d2b1e';
        symButtons[activeSym].style.borderColor = '#34d399';
        const btn = defButtons.find(b => +b.dataset.i === origIdx);
        btn.disabled = true;
        btn.style.background = '#0d2b1e';
        btn.style.borderColor = '#34d399';
        if (score.get() >= round.length * 10) finish(timer.elapsed());
      } else {
        score.add(-3);
        const btn = defButtons.find(b => +b.dataset.i === origIdx);
        btn.style.background = '#2b0d11';
        setTimeout(() => { if (!btn.disabled) btn.style.background = ''; }, 400);
      }
      activeSym = null;
      symButtons.forEach(b => b.classList.remove('selected'));
    }

    function finish(elapsed) {
      timer.stop();
      const max = round.length * 10;
      const s = Math.max(0, score.get());
      ctx.onScore(s, max);
      L.endScreen(host, {
        score: s, max,
        msg: `Idő: ${elapsed.toFixed(1)} s`,
        onAgain: () => start(host, ctx),
      });
    }
  }

  function startText(pane, ctx) {
    const L = window.DimatGameLib;
    const round = L.shuffle(PAIRS).slice(0, 6);
    const items = round.map(p => {
      const distractors = L.shuffle(PAIRS.filter(q => q !== p)).slice(0, 3);
      const opts = L.shuffle([p.def, ...distractors.map(d => d.def)]);
      return {
        prompt: `Mit jelöl ${p.sym}?`,
        options: opts,
        answer: opts.indexOf(p.def),
      };
    });
    L.textModeQuiz(pane, items, (s, m) => ctx.onScore(s * 10, m * 10));
  }

  window.DimatGames.register('ch0', {
    title: 'Notation Match',
    icon: '🔤',
    hint: 'Húzd a jelölést a megfelelő definícióra. Helyes pár: +10. Hibás: −3.',
    start, startText,
  });
})();
