/* ch7 — Sperner Antichain */
(() => {
  const QS = [
    {prompt: 'Sperner-tétel: mekkora egy maximális antilánc 𝒫([n])-ben?',
     options: ['\\(\\binom{n}{\\lfloor n/2 \\rfloor}\\)', '\\(2^n\\)', 'n', 'n!'], answer: 0,
     explanation: 'A "középső szint" méretű, központi binomiális.'},
    {prompt: 'Mi az antilánc?',
     options: ['Olyan halmazcsalád ahol egyik tag sem részhalmaza a másiknak', 'Diszjunkt halmazok', 'Lánc fordítottja', 'Antiszimmetrikus reláció'], answer: 0,
     explanation: 'Bármely két F, G ∈ 𝒜 esetén F ⊄ G és G ⊄ F.'},
    {prompt: 'LYM-egyenlőtlenség alakja?',
     options: ['\\(\\sum_F \\frac{1}{\\binom{n}{|F|}} \\le 1\\)', '|𝒜| ≤ n', '𝒜 véges', 'mindig egyenlőség'], answer: 0,
     explanation: 'Lubell-Yamamoto-Meshalkin súlyozott becslés.'},
    {prompt: 'Erdős-Ko-Rado tétel feltétele?',
     options: ['n ≥ 2k és minden k-as halmaz metsző', 'n = k', 'minden halmaz egymásból kapható', 'n prím'], answer: 0,
     explanation: 'Maximális metsző k-as családja: \\(\\binom{n-1}{k-1}\\).'},
    {prompt: 'Fisher-egyenlőtlenség: ha minden pár egyenlő méretű metszetbe esik…',
     options: ['Akkor #blokkok ≥ #pontok', 'Akkor 𝒜 üres', 'Akkor n osztható kettővel', '#blokkok ≤ #pontok'], answer: 0,
     explanation: 'Fontos lineáris algebrai bizonyítás.'},
    {prompt: 'Dilworth-tétel?',
     options: ['Egy poset minimális lánc-fedése = max antilánc mérete', 'Minden poset rendezett', 'Lánc = antilánc', 'Poset = lánc'], answer: 0,
     explanation: 'Dual Mirsky-tételének.'},
  ];
  function start(host, ctx) { window.DimatGameLib.questGame(host, window.DimatGameLib.shuffle(QS), {limit: 80}, ctx.onScore); }
  function startText(pane, ctx) { window.DimatGameLib.textModeQuiz(pane, QS, (s, m) => ctx.onScore(s * 15, m * 15)); }
  window.DimatGames.register('ch7', {title: 'Sperner Antichain', icon: '🎭', hint: 'Extremális halmazrendszerek.', start, startText});
})();
