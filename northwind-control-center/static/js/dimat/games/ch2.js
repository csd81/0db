/* ch2 — Dice Counter: predict # outcomes for elementary counting puzzles. */
(() => {
  const QS = [
    {prompt: 'Hányféleképpen rakhatunk sorrendbe 5 különböző könyvet?',
     options: ['5! = 120', '5² = 25', '5×4 = 20', '2⁵ = 32'], answer: 0,
     explanation: 'Permutáció: n! = 5·4·3·2·1 = 120.'},
    {prompt: 'Hány különböző háromjegyű szám írható a {1,2,3,4,5} jegyekből (ismétlés megengedett)?',
     options: ['125', '60', '15', '5³ × 3', ], answer: 0,
     explanation: 'Minden helyre 5 választás → 5³ = 125.'},
    {prompt: 'Hány 4 fős bizottság választható 10 emberből?',
     options: ['C(10,4) = 210', 'P(10,4) = 5040', '10⁴ = 10000', '4! = 24'], answer: 0,
     explanation: 'Sorrend nem számít → C(10,4) = 210.'},
    {prompt: 'Hány különböző "AABBC" típusú betűsorrend létezik?',
     options: ['5!/(2!·2!·1!) = 30', '5! = 120', '120/2 = 60', '20'], answer: 0,
     explanation: 'Multinomiális: 5!/(2!·2!·1!) = 30.'},
    {prompt: '6 megkülönböztethetetlen golyó hányféleképpen osztható szét 3 dobozba?',
     options: ['C(8,2) = 28', 'C(6,3) = 20', '3⁶ = 729', '3! = 6'], answer: 0,
     explanation: 'Csillagok-és-vonalak: C(n+k-1, k-1) = C(8,2) = 28.'},
    {prompt: 'Egy 8 fős csoportból hányféleképpen választható egy elnök ÉS egy alelnök?',
     options: ['8 × 7 = 56', 'C(8,2) = 28', '8² = 64', '2! = 2'], answer: 0,
     explanation: 'Sorrend számít: 8·7 = 56.'},
    {prompt: 'Hány 5-elemű részhalmaza van egy 10-elemű halmaznak?',
     options: ['C(10,5) = 252', '10⁵', '5!·10', '2¹⁰ = 1024'], answer: 0,
     explanation: 'Binomiális együttható: C(10,5) = 252.'},
    {prompt: 'Hány tartomány képződik n egyenes által a síkon (általános helyzetben)?',
     options: ['1 + n + C(n,2)', '2ⁿ', 'n! ', 'n²/2'], answer: 0,
     explanation: 'Híres formula: f(n) = 1 + n + n(n-1)/2.'},
  ];
  function start(host, ctx) { window.DimatGameLib.questGame(host, window.DimatGameLib.shuffle(QS).slice(0, 6), {limit: 75}, ctx.onScore); }
  function startText(pane, ctx) { window.DimatGameLib.textModeQuiz(pane, QS, (s, m) => ctx.onScore(s * 15, m * 15)); }
  window.DimatGames.register('ch2', {title: 'Dice Counter', icon: '🎲', hint: 'Becsüld meg a leszámlálási feladatok eredményét.', start, startText});
})();
