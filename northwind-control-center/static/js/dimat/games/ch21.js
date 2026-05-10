/* ch21 — Spectrum Lottery */
(() => {
  const QS = [
    {prompt: 'A szomszédsági mátrix sajátértékeinek összege?', options: ['0 (nyom)', '|E|', '|V|', '|V|²'], answer: 0,
     explanation: 'Egyszerű gráf — diagonális 0.'},
    {prompt: '\\(\\sum_i \\lambda_i^2 = ?\\)', options: ['2|E|', '|V|', '|E|²', '0'], answer: 0,
     explanation: 'Frobenius-norm² = 2 × élszám.'},
    {prompt: 'k-reguláris gráf esetén λ₁?', options: ['k (multiplicitás 1 ha összefüggő)', '0', '|V| - 1', 'log k'], answer: 0},
    {prompt: 'Lovász-Pelikán tétel?', options: ['Kétpólusú ↔ spektrum szimmetrikus 0-ra', 'Mindig szimmetrikus', 'Csak fák', 'Sosem'], answer: 0},
    {prompt: 'Komplementer spektrum (i ≥ 2)?', options: ['λᵢ(Ḡ) = −1 − λᵢ(G)', 'λᵢ(Ḡ) = λᵢ(G)', '0', 'log λᵢ'], answer: 0},
    {prompt: 'Algebrai összefüggőség = ?', options: ['λ₂(L) (második legkisebb Laplace-sajátérték)', 'λ_max(A)', 'det L', 'tr A'], answer: 0,
     explanation: 'Fiedler-érték.'},
  ];
  function start(host, ctx) { window.DimatGameLib.questGame(host, window.DimatGameLib.shuffle(QS), {limit: 80}, ctx.onScore); }
  function startText(pane, ctx) { window.DimatGameLib.textModeQuiz(pane, QS, (s, m) => ctx.onScore(s * 15, m * 15)); }
  window.DimatGames.register('ch21', {title: 'Spectrum Lottery', icon: '🎶', hint: 'Sajátértékek és Lovász–Pelikán.', start, startText});
})();
