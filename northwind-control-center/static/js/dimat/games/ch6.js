/* ch6 — Generating Function Coefficient Race */
(() => {
  const QS = [
    {prompt: 'Mi a generátorfüggvény definíciója?',
     options: ['\\(A(x)=\\sum_{n\\ge 0} a_n x^n\\)', '\\(A(x) = a_0 \\cdot x^n\\)', 'Hatványsor csak pozitív együtthatókkal', 'Polinom'], answer: 0,
     explanation: 'Formális hatványsor — együtthatók kombinatorikus értelműek.'},
    {prompt: '\\(\\frac{1}{1-x} = ?\\) (geometriai sor)',
     options: ['1 + x + x² + x³ + …', '1 - x + x² - x³ + …', 'eˣ', '\\(x/(1-x)\\)'], answer: 0,
     explanation: 'Klasszikus geometriai sor — minden együttható 1.'},
    {prompt: '\\([x^n](1-x)^{-k} = ?\\)',
     options: ['\\(\\binom{n+k-1}{k-1}\\)', '\\(\\binom{n}{k}\\)', 'n!/k!', '2^n'], answer: 0,
     explanation: 'Negatív binomiális kiterjesztés.'},
    {prompt: 'A Catalan-számok generátorfüggvénye?',
     options: ['\\(C(x) = \\frac{1-\\sqrt{1-4x}}{2x}\\)', '\\(\\frac{1}{1-x}\\)', '\\(e^x\\)', '\\(\\log(1-x)\\)'], answer: 0,
     explanation: 'Önreferenciás definíció: C(x) = 1 + x·C(x)².'},
    {prompt: 'A Fibonacci-számok generátorfüggvénye?',
     options: ['\\(\\frac{x}{1-x-x^2}\\)', '\\(\\frac{1}{1-x}\\)', 'x²/(1-x)', 'e^x'], answer: 0,
     explanation: 'Lineáris rekurzió — racionális GF.'},
    {prompt: 'Mi a "OEIS"?',
     options: ['Online Encyclopedia of Integer Sequences', 'Egy programozási nyelv', 'Egy matematikus neve', 'Generátorfüggvény szoftver'], answer: 0,
     explanation: 'Sloane híres adatbázisa — a kombinatorika "Wikipédiája".'},
    {prompt: 'Mi a Catalan-szám \\(C_4\\) értéke?',
     options: ['14', '5', '8', '24'], answer: 0,
     explanation: '\\(C_n = \\binom{2n}{n}/(n+1)\\), \\(C_4 = 70/5 = 14\\).'},
  ];
  function start(host, ctx) { window.DimatGameLib.questGame(host, window.DimatGameLib.shuffle(QS).slice(0, 6), {limit: 80}, ctx.onScore); }
  function startText(pane, ctx) { window.DimatGameLib.textModeQuiz(pane, QS, (s, m) => ctx.onScore(s * 15, m * 15)); }
  window.DimatGames.register('ch6', {title: 'GenFn Race', icon: '🌀', hint: 'Generátorfüggvény azonosságok.', start, startText});
})();
