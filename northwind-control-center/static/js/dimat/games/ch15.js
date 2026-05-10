/* ch15 — Kruskal Sort */
(() => {
  const QS = [
    {prompt: 'Kruskal algoritmus stratégiája?', options: ['Mohón a legrövidebb élt addig amíg nem zár kört', 'Tárolja az összes utat', 'BFS-rel', 'Random kiválasztás'], answer: 0},
    {prompt: 'Prim algoritmus?', options: ['Egy csúcs köré legrövidebb élt választunk', 'Az élek súly szerint rendezve', 'BFS', 'DFS'], answer: 0,
     explanation: 'Mindkettő helyes MST-t ad — különböző sorrendben.'},
    {prompt: 'Kruskal futási ideje (union-find optimalizálva)?', options: ['\\(O(|E| \\alpha(|V|))\\) ≈ O(E)', 'O(V³)', 'O(V·E)', 'O(V²)'], answer: 0},
    {prompt: 'TSP közelítés MST-vel: hány-szoros?', options: ['2× az optimum (3-szögegyenlőtlenséggel)', 'optimum', '4×', 'nem közelít'], answer: 0,
     explanation: 'Christofides: 1.5× — még jobb.'},
    {prompt: 'Kirchhoff tétel: feszítőfák száma = ?', options: ['Bármely cofaktor a Laplace-mátrixban', 'det L', 'eigenvalues', 'edge count'], answer: 0},
    {prompt: 'K_n feszítőfáinak száma?', options: ['n^(n-2)', 'n!', '2^n', 'C(n,2)'], answer: 0,
     explanation: 'Cayley-formula.'},
  ];
  function start(host, ctx) { window.DimatGameLib.questGame(host, window.DimatGameLib.shuffle(QS), {limit: 75}, ctx.onScore); }
  function startText(pane, ctx) { window.DimatGameLib.textModeQuiz(pane, QS, (s, m) => ctx.onScore(s * 15, m * 15)); }
  window.DimatGames.register('ch15', {title: 'Kruskal Sort', icon: '🌲', hint: 'Feszítőfák és MST.', start, startText});
})();
