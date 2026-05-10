/* ch8 — Bell Partition Builder */
(() => {
  const QS = [
    {prompt: 'Mi a Bell-szám \\(B_n\\)?',
     options: ['Egy n-elemű halmaz partícióinak száma', 'n!', '2ⁿ', '\\(\\binom{n}{2}\\)'], answer: 0,
     explanation: '\\(B_0=1, B_1=1, B_2=2, B_3=5, B_4=15, B_5=52\\).'},
    {prompt: 'Mi a Stirling-szám \\(S(n,k)\\) (második fajú)?',
     options: ['n elem k nemüres blokkba osztásainak száma', 'Permutációk száma', 'n choose k', 'Bell-szám'], answer: 0,
     explanation: '\\(B_n = \\sum_k S(n,k)\\).'},
    {prompt: 'Bell-szám rekurzió: \\(B_{n+1} = ?\\)',
     options: ['\\(\\sum_k \\binom{n}{k} B_k\\)', '\\(B_n + 1\\)', '\\(2 B_n\\)', '\\(B_n \\cdot B_{n-1}\\)'], answer: 0,
     explanation: 'Az utolsó elem blokkja k társaval — k-ra szumálva.'},
    {prompt: 'A Bell-szám exponenciális generátorfüggvénye?',
     options: ['\\(e^{e^x - 1}\\)', '\\(e^x\\)', '\\(\\frac{1}{1-x}\\)', 'sin(x)'], answer: 0,
     explanation: 'Klasszikus EGF azonosság.'},
    {prompt: 'Stirling-számok rekurziója: \\(S(n,k) = ?\\)',
     options: ['\\(k \\cdot S(n-1,k) + S(n-1,k-1)\\)', '\\(\\binom{n}{k}\\)', '\\(n!/k!\\)', 'S(n-1,k) - S(n,k+1)'], answer: 0,
     explanation: 'Az n-edik elem új blokkban vagy egy meglévőben.'},
    {prompt: 'A 11 esetből hány van, ahol "n golyó k dobozba" képletünk van?',
     options: ['12 (Stanley táblázata)', '5', '20', '11'], answer: 0,
     explanation: 'Tényleg 12 — a Stanley féle "twelvefold way" rendszerez.'},
  ];
  function start(host, ctx) { window.DimatGameLib.questGame(host, window.DimatGameLib.shuffle(QS), {limit: 80}, ctx.onScore); }
  function startText(pane, ctx) { window.DimatGameLib.textModeQuiz(pane, QS, (s, m) => ctx.onScore(s * 15, m * 15)); }
  window.DimatGames.register('ch8', {title: 'Bell Partition', icon: '🔔', hint: 'Bell- és Stirling-számok.', start, startText});
})();
