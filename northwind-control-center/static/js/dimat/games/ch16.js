/* ch16 — Twin Spotter */
(() => {
  const QS = [
    {prompt: 'Mi az izomorfia szükséges feltétele?', options: ['Azonos fok-sorozat, csúcsszám, élszám', 'Azonos színezés', 'Min út egyezik', 'Determináns egyezik'], answer: 0,
     explanation: 'Nem elégséges — találhatók ugyanilyen fokú nem-izomorf gráfok.'},
    {prompt: 'GI-probléma komplexitása?', options: ['Quasi-polinomiális (Babai 2016)', 'NP-teljes', 'P', 'EXPTIME'], answer: 0},
    {prompt: 'Fák izomorfiája?', options: ['P-ben — kanonikus alak BFS-szel', 'NP-teljes', 'EXPTIME', 'Eldöntetlen'], answer: 0},
    {prompt: 'Fokmátrix-spektrum elégséges?', options: ['Nem — nem-izomorf gráfok lehet azonos spektrumú', 'Igen', 'Csak fán', 'Csak K_n-en'], answer: 0,
     explanation: 'Izospektrális gráfok példák.'},
    {prompt: 'Aut(G): mi az?', options: ['G automorfizmus-csoportja', 'G éleinek halmaza', 'G hatványa', 'G ⊕ Ḡ'], answer: 0},
    {prompt: 'Kanonikus alak egy fa esetén?', options: ['Mindig egyértelmű — BFS layered', 'Sosem', 'Csak rendezett', 'Csak színes'], answer: 0},
  ];
  function start(host, ctx) { window.DimatGameLib.questGame(host, window.DimatGameLib.shuffle(QS), {limit: 80}, ctx.onScore); }
  function startText(pane, ctx) { window.DimatGameLib.textModeQuiz(pane, QS, (s, m) => ctx.onScore(s * 15, m * 15)); }
  window.DimatGames.register('ch16', {title: 'Twin Spotter', icon: '👯', hint: 'Izomorfia és invariánsok.', start, startText});
})();
