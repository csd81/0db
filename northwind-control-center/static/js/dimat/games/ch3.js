/* ch3 — Pascal Sniper: target appears on triangle, click before timeout. */
(() => {
  const QS = [
    {prompt: '\\(\\binom{n}{0}+\\binom{n}{1}+\\cdots+\\binom{n}{n} = ?\\)',
     options: ['2ⁿ', 'n!', 'n²', '0'], answer: 0,
     explanation: 'Binomiális tétel: (1+1)ⁿ = 2ⁿ.'},
    {prompt: 'Pascal-azonosság: \\(\\binom{n}{k} = ?\\)',
     options: ['\\(\\binom{n-1}{k-1}+\\binom{n-1}{k}\\)', '\\(\\binom{n+1}{k+1}\\)', 'n!/k!', 'n×k'], answer: 0,
     explanation: 'Klasszikus Pascal-háromszög konstrukció.'},
    {prompt: 'Vandermonde-azonosság: \\(\\sum_{k}\\binom{m}{k}\\binom{n}{r-k} = ?\\)',
     options: ['\\(\\binom{m+n}{r}\\)', '\\(\\binom{m \\cdot n}{r}\\)', '\\(\\binom{m}{r}+\\binom{n}{r}\\)', 'mn'], answer: 0,
     explanation: 'Konvolúció kombinatorikus értelmezése.'},
    {prompt: 'Newton binomiális tétel: \\((x+y)^n = ?\\)',
     options: ['\\(\\sum_{k=0}^{n}\\binom{n}{k}x^{n-k}y^k\\)', 'xⁿ + yⁿ', 'n(x+y)', 'xy'], answer: 0,
     explanation: 'Az alaptétel: kifejtés binomiális együtthatókkal.'},
    {prompt: 'Mennyi a \\(\\binom{6}{3}\\)?',
     options: ['20', '15', '10', '120'], answer: 0,
     explanation: '6!/(3!·3!) = 720/36 = 20.'},
    {prompt: 'Hat \\(\\binom{n}{k}\\) páratlan, ha n = ?',
     options: ['7 = 111₂ — minden együttható páratlan', 'n = 4', 'n = páros', 'n = ∞'], answer: 0,
     explanation: 'Lucas-tétel: a 2-féle binomiálisok bináris reprezentációval analizálhatók.'},
  ];
  function start(host, ctx) { window.DimatGameLib.questGame(host, window.DimatGameLib.shuffle(QS), {limit: 70}, ctx.onScore); }
  function startText(pane, ctx) { window.DimatGameLib.textModeQuiz(pane, QS, (s, m) => ctx.onScore(s * 15, m * 15)); }
  window.DimatGames.register('ch3', {title: 'Pascal Sniper', icon: '🔢', hint: 'Binomiális együttható-azonosságok.', start, startText});
})();
