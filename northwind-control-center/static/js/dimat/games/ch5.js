/* ch5 — Fibonacci Chain: predict the next term in a recursion. */
(() => {
  const SEQS = [
    {label: 'Fibonacci', start: [1, 1], next: (a) => a[a.length-1] + a[a.length-2]},
    {label: 'Lucas',     start: [2, 1], next: (a) => a[a.length-1] + a[a.length-2]},
    {label: 'Tribonacci',start: [1, 1, 2], next: (a) => a.slice(-3).reduce((s, x) => s + x, 0)},
    {label: 'Pell',      start: [0, 1], next: (a) => 2 * a[a.length-1] + a[a.length-2]},
    {label: 'Padovan',   start: [1, 1, 1], next: (a) => a[a.length-2] + a[a.length-3]},
    {label: 'Hanoi',     start: [0, 1], next: (a) => 2 * a[a.length-1] + 1},
    {label: 'Powers of 2', start: [1, 2], next: (a) => 2 * a[a.length-1]},
    {label: 'Triangular', start: [1, 3, 6], next: (a, i) => a[a.length-1] + (a.length + 1)},
  ];

  function genQuestion() {
    const L = window.DimatGameLib;
    const S = L.choice(SEQS);
    const arr = S.start.slice();
    while (arr.length < 7) arr.push(S.next(arr, arr.length));
    const showCount = 5;
    const shown = arr.slice(0, showCount);
    const correct = arr[showCount];
    const distractors = [correct + 1, correct - 1, correct * 2, Math.floor(correct / 2)]
      .filter(d => d !== correct).slice(0, 3);
    const opts = L.shuffle([correct, ...distractors]);
    return {
      prompt: `<span style="font-family:monospace;color:#a8d8f0">${shown.join(', ')}, …</span><br>Mi a következő tag? <em>(${S.label})</em>`,
      options: opts.map(o => o.toString()),
      answer: opts.indexOf(correct),
      explanation: `Rekurzió: a következő = ${correct}.`,
    };
  }

  function start(host, ctx) {
    const items = Array.from({length: 8}, genQuestion);
    window.DimatGameLib.questGame(host, items, {limit: 80}, ctx.onScore);
  }
  function startText(pane, ctx) {
    const items = Array.from({length: 6}, genQuestion);
    window.DimatGameLib.textModeQuiz(pane, items, (s, m) => ctx.onScore(s * 15, m * 15));
  }
  window.DimatGames.register('ch5', {title: 'Fibonacci Chain', icon: '🐚', hint: 'Felismered a rekurzió szabályát?', start, startText});
})();
