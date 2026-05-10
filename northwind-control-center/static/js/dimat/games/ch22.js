/* ch22 — Flow Optimiser */
(() => {
  const QS = [
    {prompt: 'Max-flow min-cut tétel?', options: ['Max F(f) = min C(V₁,V₂)', 'Max F(f) ≤ |E|', 'min C ≥ 0', 'mindig egyenlő |V|'], answer: 0,
     explanation: 'Ford-Fulkerson alaperedménye.'},
    {prompt: 'Ford-Fulkerson algoritmus?', options: ['Augmentáló utat keres BFS/DFS-szel iteratívan', 'Csak DFS', 'Csak DAG-okon', 'Min vágás csak'], answer: 0},
    {prompt: 'Edmonds-Karp futási ideje?', options: ['\\(O(VE^2)\\)', '\\(O(V^3)\\)', 'O(V!)', 'O(E)'], answer: 0,
     explanation: 'BFS-vel keresett rövid augmentáló utak.'},
    {prompt: 'Mit takar Kirchhoff I. törvénye folyamhálózatban?', options: ['Befolyó = kifolyó belső csúcsoknál', '|V| = |E|', 'Síkbarajzolhatóság', 'Csak Euler'], answer: 0},
    {prompt: 'Páros gráf max párosítás vissza vezethető?', options: ['Igen — max-flow problémára', 'Csak fa esetén', 'Sosem', 'Csak K_n'], answer: 0},
    {prompt: 'Reziduális gráf tartalmaz?', options: ['Hátramutató éleket is', 'Csak előre', 'Csak források', 'Csak nyelők'], answer: 0,
     explanation: 'Hátramutató = "visszavehető" folyam.'},
  ];
  function start(host, ctx) { window.DimatGameLib.questGame(host, window.DimatGameLib.shuffle(QS), {limit: 80}, ctx.onScore); }
  function startText(pane, ctx) { window.DimatGameLib.textModeQuiz(pane, QS, (s, m) => ctx.onScore(s * 15, m * 15)); }
  window.DimatGames.register('ch22', {title: 'Flow Optimiser', icon: '🌊', hint: 'Max-flow min-cut és augmentáló utak.', start, startText});
})();
