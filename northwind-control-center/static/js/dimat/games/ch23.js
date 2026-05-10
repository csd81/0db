/* ch23 — Matroid Greedy */
(() => {
  const QS = [
    {prompt: 'Matroid I3 axióma (kiegészítési tulajdonság)?', options: ['Ha |X|<|Y| és X,Y ∈ F, akkor ∃ s ∈ Y\\X : X∪{s} ∈ F', 'F nemüres', 'F leszálló', 'F max elem'], answer: 0},
    {prompt: 'Mi a "grafikus" matroid?', options: ['S = E gráf, F = körmentes részhalmazok', 'S = V', 'S = matrix', 'Csak fán'], answer: 0},
    {prompt: 'Uniform matroid \\(U_{m,k}\\) bázisai?', options: ['Minden k-elemű részhalmaz', 'Csak ∅', 'Csak S', 'Csak fák'], answer: 0},
    {prompt: 'Rangfüggvény szubmoduláris?', options: ['Igen — \\(r(X∪Y)+r(X∩Y) ≤ r(X)+r(Y)\\)', 'Nem', 'Csak grafikuson', 'Csak uniform'], answer: 0},
    {prompt: 'Mohó algoritmus matroidon ad-e optimumot?', options: ['Igen — minden bázis azonos méretű', 'Csak ha súlyok egyenlők', 'Sosem', 'Csak fán'], answer: 0,
     explanation: 'Pontosan a matroidok karakterizálják a "mohó-jó" struktúrákat.'},
    {prompt: 'Egy körre r(C) = ?', options: ['|C| − 1', '|C|', '0', '|C|²'], answer: 0,
     explanation: 'Definíció szerint a körök minimális összefüggő halmazok.'},
  ];
  function start(host, ctx) { window.DimatGameLib.questGame(host, window.DimatGameLib.shuffle(QS), {limit: 80}, ctx.onScore); }
  function startText(pane, ctx) { window.DimatGameLib.textModeQuiz(pane, QS, (s, m) => ctx.onScore(s * 15, m * 15)); }
  window.DimatGames.register('ch23', {title: 'Matroid Greedy', icon: '⚙️', hint: 'Függetlenség, körök, bázisok.', start, startText});
})();
