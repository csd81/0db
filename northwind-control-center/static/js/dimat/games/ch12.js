/* ch12 — Matrix→Graph Match */
(() => {
  const QS = [
    {prompt: 'Mi a szomszédsági mátrix \\(A_{ij}\\) jelentése?', options: ['1 ha (i,j) él, különben 0', 'Élek súlya', 'Foksorozat', 'Path-mátrix'], answer: 0},
    {prompt: '\\(A^k_{ij}\\) számolja meg…', options: ['Az i-ből j-be vezető k-hosszú séták számát', 'k-edik hatvány élsúlya', 'k-clique', 'Min út hossza'], answer: 0,
     explanation: 'Mátrixhatvány gráfelméleti jelentése.'},
    {prompt: 'A Laplace-mátrix definíciója \\(L = ?\\)', options: ['D − A (D fokmátrix, A adj)', 'A + D', 'A²', 'A × A^T'], answer: 0},
    {prompt: 'Kirchhoff (Matrix-Tree) tétel?', options: ['L bármely kofaktora = feszítőfák száma', 'L sajátértéke', 'det L = élek száma', 'L⁻¹ adja MST-t'], answer: 0,
     explanation: 'Egy klasszikus eredmény Cayley által ihletve.'},
    {prompt: 'L mindig pozitív szemidefinit?', options: ['Igen — sajátértékei \\(\\ge 0\\)', 'Nem', 'Csak ha gráf összefüggő', 'Csak fák esetén'], answer: 0},
    {prompt: '\\(\\lambda_2(L) > 0\\) ↔ ?', options: ['Gráf összefüggő', 'Gráf kétpólusú', 'Gráf reguláris', 'Gráf síkbarajzolható'], answer: 0,
     explanation: 'Az ún. algebrai összefüggőség.'},
  ];
  function start(host, ctx) { window.DimatGameLib.questGame(host, window.DimatGameLib.shuffle(QS), {limit: 80}, ctx.onScore); }
  function startText(pane, ctx) { window.DimatGameLib.textModeQuiz(pane, QS, (s, m) => ctx.onScore(s * 15, m * 15)); }
  window.DimatGames.register('ch12', {title: 'Matrix→Graph', icon: '🧩', hint: 'Gráf-mátrixok és sajátértékek.', start, startText});
})();
