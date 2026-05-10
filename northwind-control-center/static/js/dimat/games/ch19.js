/* ch19 — Hall Marriage */
(() => {
  const QS = [
    {prompt: 'Hall-tétel feltétele tökéletes párosításhoz \\(K_{A,B}\\)-ben?', options: ['\\(\\forall S \\subseteq A: |N(S)| \\ge |S|\\)', '|A| = |B|', 'Bipartit', 'Reguláris'], answer: 0},
    {prompt: 'König-tétel: páros gráfra?', options: ['ν(G) = τ(G) — max párosítás = min csúcsfedés', 'χ(G) = Δ(G)', 'Mindig', 'ν(G) = |E|'], answer: 0},
    {prompt: 'Magyar módszer mit old meg?', options: ['Súlyozott hozzárendelési feladat optimális', 'TSP', 'Min vágás', 'MST'], answer: 0,
     explanation: 'Egerváry & Kuhn munkája.'},
    {prompt: 'Augmentáló út párosításban?', options: ['Páratlan hosszú út, párosított és nem-párosított élek váltják egymást', 'Mindig páros hosszú', 'Bármi', 'Csak Hamilton'], answer: 0},
    {prompt: 'Ha létezik augmentáló út, a párosítás...?', options: ['Növelhető 1-gyel', 'Maximális', 'Üres', 'NP-nehéz'], answer: 0},
    {prompt: 'Páros gráf jellemzése?', options: ['Nincs páratlan kör', 'Síkbarajzolható', 'Minden csúcs fokú 2', '3-színezhető'], answer: 0},
  ];
  function start(host, ctx) { window.DimatGameLib.questGame(host, window.DimatGameLib.shuffle(QS), {limit: 80}, ctx.onScore); }
  function startText(pane, ctx) { window.DimatGameLib.textModeQuiz(pane, QS, (s, m) => ctx.onScore(s * 15, m * 15)); }
  window.DimatGames.register('ch19', {title: 'Hall Marriage', icon: '💍', hint: 'Páros gráfok, Hall-feltétel, König.', start, startText});
})();
