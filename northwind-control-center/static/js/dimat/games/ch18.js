/* ch18 — Map 4-Colour */
(() => {
  const QS = [
    {prompt: 'Mi χ(G)?', options: ['G kromatikus száma — minimális szín szám', 'Fokszám', 'Élek száma', 'Csúcsok száma'], answer: 0},
    {prompt: 'χ(C_5) = ?', options: ['3', '2', '4', '5'], answer: 0,
     explanation: 'Páratlan kör nem 2-színezhető.'},
    {prompt: 'χ(K_n) = ?', options: ['n', '2', 'log n', '∞'], answer: 0},
    {prompt: 'Brooks-tétel?', options: ['χ(G) ≤ Δ(G), kivéve K_n és páratlan körök', 'χ(G) = Δ(G)', 'χ(G) = 2Δ(G)', 'Mindig'], answer: 0},
    {prompt: '4-szín-tétel — mire vonatkozik?', options: ['Síkgráfok 4-színezhetők', 'Minden gráf 4-színezhető', 'Csak K_n', 'Csak fák'], answer: 0},
    {prompt: 'Ramsey R(3,3) = ?', options: ['6', '4', '5', '9'], answer: 0,
     explanation: 'K₆ minden 2-színezésében van monokróm K₃.'},
    {prompt: 'Kromatikus polinom P(G,k) — mi a tétel?', options: ['Polinom k-ban; P(G,k) = P(G−e,k) − P(G/e,k)', 'P(G,k) = k', 'P csak fák esetén értelmes', 'P mindig 0'], answer: 0,
     explanation: 'Deletion-contraction.'},
  ];
  function start(host, ctx) { window.DimatGameLib.questGame(host, window.DimatGameLib.shuffle(QS), {limit: 80}, ctx.onScore); }
  function startText(pane, ctx) { window.DimatGameLib.textModeQuiz(pane, QS, (s, m) => ctx.onScore(s * 15, m * 15)); }
  window.DimatGames.register('ch18', {title: 'Map 4-Colour', icon: '🎨', hint: 'Színezések és kromatikus szám.', start, startText});
})();
