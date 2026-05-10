/* ch11 — Hamilton Quest */
(() => {
  const QS = [
    {prompt: 'Mi a Hamilton-kör?', options: ['Minden csúcsot pontosan egyszer érintő kör', 'Minden élt egyszer', 'Min út', 'MST'], answer: 0,
     explanation: 'Vigyázat: az "élek vs. csúcsok" különbség Euler-vs-Hamilton.'},
    {prompt: 'Dirac tétele (n ≥ 3)?', options: ['Ha minden \\(d(v) \\ge n/2\\), akkor van Hamilton-kör', 'Ha minden \\(d(v) = 2\\)', 'Ha n páros', 'Mindig'], answer: 0,
     explanation: 'Csúcs-fokszám alapú elégséges feltétel.'},
    {prompt: 'Ore tétele?', options: ['Bármely 2 nem-szomszédos csúcsra \\(d(u) + d(v) \\ge n\\)', '\\(d(u) = d(v)\\)', 'Páros gráfra', 'Csak fán'], answer: 0,
     explanation: 'Általánosabb, mint Dirac.'},
    {prompt: 'Mi a TSP (utazó ügynök)?', options: ['Min Hamilton-kör keresése súlyozott gráfban', 'Max kör', 'Euler-séta', 'MST'], answer: 0,
     explanation: 'NP-nehéz probléma.'},
    {prompt: 'A huszárvándorlás Hamilton-?', options: ['Hamilton-séta a 64 mezős táblán', 'Euler-séta', 'BFS', 'Min vágás'], answer: 0,
     explanation: 'Klasszikus 8×8 sakk-tábla feladat.'},
    {prompt: 'Q₃ kockagráf — van Hamilton-köre?', options: ['Igen — Gray-kód', 'Nem', 'Csak párosra', 'Csak gyökeres fán'], answer: 0,
     explanation: 'Gray-kód éppen Hamilton-kör Q_n-en.'},
  ];
  function start(host, ctx) { window.DimatGameLib.questGame(host, window.DimatGameLib.shuffle(QS), {limit: 75}, ctx.onScore); }
  function startText(pane, ctx) { window.DimatGameLib.textModeQuiz(pane, QS, (s, m) => ctx.onScore(s * 15, m * 15)); }
  window.DimatGames.register('ch11', {title: 'Hamilton Quest', icon: '👑', hint: 'Hamilton-utak és tételek.', start, startText});
})();
