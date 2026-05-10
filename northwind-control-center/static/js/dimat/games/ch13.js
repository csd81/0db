/* ch13 — Dijkstra Race */
(() => {
  const QS = [
    {prompt: 'Dijkstra futási ideje (heap-pel)?', options: ['\\(O((|V|+|E|)\\log|V|)\\)', '\\(O(|V|^3)\\)', '\\(O(|V|!)\\)', 'O(|E|)'], answer: 0},
    {prompt: 'Dijkstra feltétele?', options: ['Minden élsúly \\(\\ge 0\\)', 'Élsúlyok egészek', 'Gráf összefüggő', 'Gráf irányított'], answer: 0,
     explanation: 'Negatív súlyokkal Bellman-Ford kell.'},
    {prompt: 'Bellman-Ford negatív kört detektál?', options: ['Igen — n-edik iteráció után még csökken', 'Nem', 'Csak DAG-okon', 'Csak Dijkstra'], answer: 0},
    {prompt: 'Floyd-Warshall futási ideje?', options: ['\\(O(|V|^3)\\)', 'O(V²)', 'O(VE)', 'O(V log V)'], answer: 0},
    {prompt: 'A* algoritmus?', options: ['Heurisztika-vezérelt rövid út', 'Csak DFS', 'MST', 'Min vágás'], answer: 0,
     explanation: 'A* Dijkstra + h(v) heurisztika.'},
    {prompt: 'Mikor optimális A*?', options: ['Ha h(v) konzisztens (admissible & monoton)', 'Mindig', 'Soha', 'Csak fa-gráfon'], answer: 0},
    {prompt: 'BFS-shortest path mire jó?', options: ['Súlyozatlan gráfok rövid útjaira', 'Nem rövidít', 'Negatív súlyok', 'MST'], answer: 0},
  ];
  function start(host, ctx) { window.DimatGameLib.questGame(host, window.DimatGameLib.shuffle(QS), {limit: 80}, ctx.onScore); }
  function startText(pane, ctx) { window.DimatGameLib.textModeQuiz(pane, QS, (s, m) => ctx.onScore(s * 15, m * 15)); }
  window.DimatGames.register('ch13', {title: 'Dijkstra Race', icon: '🛣️', hint: 'Útkereső algoritmusok.', start, startText});
})();
