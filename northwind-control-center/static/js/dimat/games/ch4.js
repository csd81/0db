/* ch4 — Inclusion-Exclusion / Derangement quiz */
(() => {
  const QS = [
    {prompt: 'Szitaformula \\(|A_1\\cup A_2| = ?\\)',
     options: ['\\(|A_1| + |A_2| - |A_1\\cap A_2|\\)', '\\(|A_1| \\cdot |A_2|\\)', '\\(|A_1| + |A_2|\\)', '\\(\\max(|A_1|, |A_2|)\\)'], answer: 0,
     explanation: 'Két halmaz uniója — egyszer levonjuk a metszetet.'},
    {prompt: 'Mi az n-dik elcserélt levél (derangement)?',
     options: ['\\(D_n = n!\\sum_{k=0}^n \\frac{(-1)^k}{k!}\\)', 'n!', '2ⁿ', 'n²'], answer: 0,
     explanation: 'Egy permutáció ahol semelyik elem sincs a saját helyén.'},
    {prompt: '\\(D_n / n! \\to ?\\) (n→∞)',
     options: ['1/e', '0', '1', 'e'], answer: 0,
     explanation: 'A levelekből kb. 36.8% derangement (1/e arány).'},
    {prompt: 'Euler-féle \\(\\varphi\\)-függvény jelentése?',
     options: ['Hány n-nel relatív prím szám van [1..n]-ben', 'Osztók száma', 'Prímek száma n alatt', 'n!'], answer: 0,
     explanation: 'Klasszikus számelmélet — szitával kiszámolható.'},
    {prompt: '\\(\\varphi(p) = ?\\) ha p prím',
     options: ['p − 1', 'p', 'p²', '1'], answer: 0,
     explanation: 'Csak p maga nem relatív prím — minden más igen.'},
    {prompt: 'Hány szürjektív függvény van [n] → [k] között? (n ≥ k)',
     options: ['Szita: \\(\\sum_{j=0}^{k}(-1)^j \\binom{k}{j}(k-j)^n\\)', 'kⁿ', 'n!/k!', 'n × k'], answer: 0,
     explanation: 'Szita-elv: vonjuk le azon függvényeket amelyek bizonyos elemeket nem érnek.'},
    {prompt: 'Mi a "Bonferroni" egyenlőtlenség?',
     options: ['Csonkolt szita ad alsó/felső korlátot', 'Másik szitaformula', '|A∩B| ≥ |A|·|B|', 'n! < 2ⁿ'], answer: 0,
     explanation: 'Páratlan tagig vágva: alsó korlát; páros: felső korlát.'},
  ];
  function start(host, ctx) { window.DimatGameLib.questGame(host, window.DimatGameLib.shuffle(QS).slice(0, 6), {limit: 75}, ctx.onScore); }
  function startText(pane, ctx) { window.DimatGameLib.textModeQuiz(pane, QS, (s, m) => ctx.onScore(s * 15, m * 15)); }
  window.DimatGames.register('ch4', {title: 'Sieve & Derangements', icon: '🎩', hint: 'Inclusion-exclusion + derangement.', start, startText});
})();
