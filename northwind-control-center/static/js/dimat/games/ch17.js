/* ch17 — Planar Untangler */
(() => {
  const QS = [
    {prompt: 'Euler-formula síkgráfra?', options: ['v − e + f = 2', 'v + e + f = 2', 'v · e · f = 0', 'v² + e² = f²'], answer: 0,
     explanation: 'Az egyik leghíresebb gráfelméleti eredmény.'},
    {prompt: 'Kuratowski tétele?', options: ['Síkba rajzolható ↔ nem tartalmaz K₅ vagy K₃,₃ minort', 'Síkbarajzolható ↔ fa', 'Csak Hamilton-ciklusra', 'Csak Euler-séta'], answer: 0},
    {prompt: 'Hány él lehet legfeljebb síkgráfban?', options: ['3v − 6 (egyszerű, v ≥ 3)', '\\(\\binom{v}{2}\\)', 'v', 'v + e'], answer: 0},
    {prompt: 'K₅ — síkbarajzolható?', options: ['Nem — nem teljesíti 3v−6', 'Igen', 'Csak ha n ≥ 4', 'Csak ha mátrixmátlak'], answer: 0},
    {prompt: 'K₃,₃ — síkbarajzolható?', options: ['Nem — Kuratowski', 'Igen', 'Csak ha bipartit', 'Csak fa'], answer: 0},
    {prompt: '4-szín-tétel?', options: ['Minden síkgráf 4-színezhető', 'Minden gráf 3-színezhető', 'Csak fák', 'NP-teljes'], answer: 0,
     explanation: 'Appel-Haken 1976; majd Robertson et al. 1996.'},
    {prompt: 'Fullerén — milyen poliéder?', options: ['Síkgráfra leképezhető 3-reguláris fokszámmal', 'Fa', 'Lánc', 'Kocka'], answer: 0},
  ];
  function start(host, ctx) { window.DimatGameLib.questGame(host, window.DimatGameLib.shuffle(QS), {limit: 80}, ctx.onScore); }
  function startText(pane, ctx) { window.DimatGameLib.textModeQuiz(pane, QS, (s, m) => ctx.onScore(s * 15, m * 15)); }
  window.DimatGames.register('ch17', {title: 'Planar Untangler', icon: '🗺️', hint: 'Síkgráfok és Euler-formula.', start, startText});
})();
