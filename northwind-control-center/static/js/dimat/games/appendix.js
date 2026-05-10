/* appendix — Polynomial Coefficient Race */
(() => {
  const QS = [
    {prompt: '\\(\\binom{x}{2} = ?\\) (mint polinom)', options: ['\\(\\frac{x^2 - x}{2}\\)', 'x²', '\\(\\frac{x^2 + x}{2}\\)', 'x'], answer: 0},
    {prompt: '\\(\\binom{x}{0} = ?\\)', options: ['1', '0', 'x', 'x − 1'], answer: 0},
    {prompt: '\\(\\sum_{i=1}^n i = ?\\)', options: ['n(n+1)/2', 'n²', 'n!', '2n'], answer: 0},
    {prompt: '\\(\\sum_{i=1}^n i^2 = ?\\)', options: ['n(n+1)(2n+1)/6', 'n²(n+1)/2', '(n+1)³/3', 'n³'], answer: 0},
    {prompt: '\\(\\sum_{i=1}^n i^3 = ?\\)', options: ['\\((\\sum i)^2 = (n(n+1)/2)^2\\)', 'n³(n+1)', 'n^4/4', 'n²'], answer: 0,
     explanation: 'Klasszikus: a köbök összege = az összegek négyzete.'},
    {prompt: 'Parciális törtek: a nevező \\(x²-1\\) = ?', options: ['\\((x-1)(x+1)\\)', 'x², 0', '\\(x^2+1\\)', '\\((x-1)^2\\)'], answer: 0},
    {prompt: 'Ha p(x) =\\(\\frac{1}{x²-1}\\), parciális törtre bontva?', options: ['\\(\\frac{1/2}{x-1} - \\frac{1/2}{x+1}\\)', '\\(\\frac{1}{x-1}\\)', '0', 'x'], answer: 0},
  ];
  function start(host, ctx) { window.DimatGameLib.questGame(host, window.DimatGameLib.shuffle(QS), {limit: 80}, ctx.onScore); }
  function startText(pane, ctx) { window.DimatGameLib.textModeQuiz(pane, QS, (s, m) => ctx.onScore(s * 15, m * 15)); }
  window.DimatGames.register('appendix', {title: 'Polynomial Race', icon: '📐', hint: '\\(\\binom{x}{n}\\) és \\(P_k(n)\\) polinomok.', start, startText});
})();
