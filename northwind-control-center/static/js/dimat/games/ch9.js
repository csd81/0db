/* ch9 — Handshake Detective */
(() => {
  const QS = [
    {prompt: 'Kézfogások tétele: \\(\\sum_v d(v) = ?\\)',
     options: ['2|E|', '|E|', '|V|', 'V × E'], answer: 0,
     explanation: 'Minden él két csúcs fokához számít → összeg = 2|E|.'},
    {prompt: 'Hány páratlan fokú csúcs lehet egy gráfban?',
     options: ['Páros sok', 'Mindig páros', 'Mindig páratlan', 'Akármi'], answer: 0,
     explanation: 'A kézfogás-lemma direkt következménye.'},
    {prompt: 'Petersen-gráf: |V|=?',
     options: ['10', '5', '15', '20'], answer: 0,
     explanation: '5 belső + 5 külső = 10 csúcs.'},
    {prompt: 'Mennyi a \\(K_n\\) (teljes gráf) éleinek száma?',
     options: ['\\(\\binom{n}{2} = n(n-1)/2\\)', 'n²', 'n', 'n!'], answer: 0,
     explanation: 'Minden csúcspár egy él.'},
    {prompt: 'Mennyi a \\(K_{m,n}\\) (teljes páros gráf) éleinek száma?',
     options: ['mn', 'm + n', 'm² + n²', '2mn'], answer: 0,
     explanation: 'Minden A-csúcs minden B-csúcsra rákötve.'},
    {prompt: 'Mi a "fok-sorozat"?',
     options: ['A csúcsok fokszámainak rendezett listája', 'Élek hossza', 'Útvonal hossza', 'Színezés'], answer: 0,
     explanation: 'Izomorfia szükséges (de nem elégséges) feltétele.'},
    {prompt: 'Königsberg-i hidak: hány páratlan fokú csúcs?',
     options: ['4', '0', '2', '7'], answer: 0,
     explanation: 'Pontosan 4 — ezért nincs Euler-séta.'},
  ];
  function start(host, ctx) { window.DimatGameLib.questGame(host, window.DimatGameLib.shuffle(QS), {limit: 75}, ctx.onScore); }
  function startText(pane, ctx) { window.DimatGameLib.textModeQuiz(pane, QS, (s, m) => ctx.onScore(s * 15, m * 15)); }
  window.DimatGames.register('ch9', {title: 'Handshake Detective', icon: '🤝', hint: 'Gráf alapfogalmak.', start, startText});
})();
