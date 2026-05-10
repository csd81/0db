/* ch14 — Prüfer Encoder */
(() => {
  const QS = [
    {prompt: 'Cayley-formula (címkézett fák száma n csúcson)?', options: ['\\(n^{n-2}\\)', '\\(n!\\)', '\\(2^n\\)', 'n²'], answer: 0,
     explanation: 'Híres bizonyítás Prüfer-kóddal.'},
    {prompt: 'Hány bázis van egy fában?', options: ['1 — maga a fa', 'n', '\\(\\binom{n}{2}\\)', 'Nincs'], answer: 0},
    {prompt: 'Egy fa éleinek száma?', options: ['n − 1', 'n', 'n + 1', '2n'], answer: 0,
     explanation: 'Pontosan n − 1 él egy n-csúcsú fában.'},
    {prompt: 'Bináris keresőfa (BST) magassága balanszírozva?', options: ['\\(\\lceil \\log_2 n \\rceil\\)', 'n', 'n/2', 'n²'], answer: 0},
    {prompt: 'Prüfer-kód hossza n csúcsú fán?', options: ['n − 2', 'n', 'n − 1', 'log n'], answer: 0},
    {prompt: 'Fa középpontja: hány csúcs?', options: ['1 vagy 2', 'mindig 1', 'mindig 2', 'tetszőleges'], answer: 0,
     explanation: 'Iteratívan távolítva a leveleket.'},
    {prompt: 'Lánc gráf: hány feszítőfája van?', options: ['1', 'n', 'n!', 'nincs'], answer: 0},
  ];
  function start(host, ctx) { window.DimatGameLib.questGame(host, window.DimatGameLib.shuffle(QS), {limit: 80}, ctx.onScore); }
  function startText(pane, ctx) { window.DimatGameLib.textModeQuiz(pane, QS, (s, m) => ctx.onScore(s * 15, m * 15)); }
  window.DimatGames.register('ch14', {title: 'Prüfer Encoder', icon: '🌳', hint: 'Fák és Cayley-formula.', start, startText});
})();
