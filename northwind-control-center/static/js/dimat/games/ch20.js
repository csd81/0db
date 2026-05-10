/* ch20 — Turán Builder */
(() => {
  const QS = [
    {prompt: 'Turán-tétel: \\(ex(n, K_{r+1}) = ?\\)', options: ['\\(e(T(n,r)) \\approx (1-1/r) n^2/2\\)', 'n', 'n!', '2^n'], answer: 0,
     explanation: 'Turán-gráf T(n,r) az extremum.'},
    {prompt: 'T(n,2) (K₃-mentes max) =?', options: ['Teljes páros gráf K_{⌊n/2⌋,⌈n/2⌉}', 'K_n', 'Fa', 'Üres gráf'], answer: 0},
    {prompt: 'Aszimptotikus sűrűség K_{r+1}-mentes gráfban?', options: ['1 − 1/r', '1', '0', '1/2'], answer: 0,
     explanation: 'Turán-tétel következménye.'},
    {prompt: 'Kővári-Sós-Turán: \\(ex(n, K_{s,t}) \\le ?\\)', options: ['\\(\\frac{1}{2}(t-1)^{1/s} n^{2-1/s} + O(n)\\)', 'n²', 'n^t', '0'], answer: 0},
    {prompt: 'ex(n, K_{2,2}) ≈ ?', options: ['\\(\\Theta(n^{3/2})\\)', '\\(\\Theta(n^2)\\)', 'O(n)', 'O(n log n)'], answer: 0,
     explanation: 'Híres alsó becslés Erdős-Rényi.'},
    {prompt: 'Zykov-szimmetrizáció — mire jó?', options: ['Turán-tétel egyik bizonyítása', 'MST', 'Színezés', 'Síkbarajzolhatóság'], answer: 0},
  ];
  function start(host, ctx) { window.DimatGameLib.questGame(host, window.DimatGameLib.shuffle(QS), {limit: 80}, ctx.onScore); }
  function startText(pane, ctx) { window.DimatGameLib.textModeQuiz(pane, QS, (s, m) => ctx.onScore(s * 15, m * 15)); }
  window.DimatGames.register('ch20', {title: 'Turán Builder', icon: '📊', hint: 'Extremális gráfok és Turán-tétel.', start, startText});
})();
