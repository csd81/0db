/* dimat_quiz.js
   ─────────────────────────────────────────────────────────────────────────
   Universal client module for /demos/dimat/* pages.
   Auto-detects current chapter from the URL, then injects 3 universal tabs
   (Feladatok / Kvíz / Mini-játék) into the existing nav row of every dimat
   chapter — no per-chapter template changes needed.

   Public globals (used by per-chapter game files):
     window.DimatQuiz        — { renderExercises, renderQuiz, renderMiniGame,
                                 awardXP, toast, fetchJSON, postJSON }
     window.DimatGames       — { register(ch, gameSpec) } populated by
                                 static/js/dimat/games/{ch}.js as it loads
   ───────────────────────────────────────────────────────────────────────── */
(() => {
  'use strict';

  const M = (window.location.pathname.match(/^\/demos\/dimat\/(ch\d+|appendix)/) || [])[1];
  if (!M && !window.location.pathname.startsWith('/demos/dimat/challenges')
        && !window.location.pathname.startsWith('/learn/dimat')) {
    return; // Not a dimat page; bail.
  }
  const CH = M;  // may be undefined on /challenges or /learn/dimat

  // ── tiny helpers ─────────────────────────────────────────────────────────

  const el = (tag, attrs = {}, kids = []) => {
    const e = document.createElement(tag);
    for (const [k, v] of Object.entries(attrs)) {
      if (k === 'style' && typeof v === 'object') Object.assign(e.style, v);
      else if (k === 'class') e.className = v;
      else if (k === 'html') e.innerHTML = v;
      else if (k.startsWith('on') && typeof v === 'function') e.addEventListener(k.slice(2), v);
      else if (v !== false && v != null) e.setAttribute(k, v);
    }
    for (const k of [].concat(kids)) {
      if (k == null) continue;
      e.appendChild(typeof k === 'string' ? document.createTextNode(k) : k);
    }
    return e;
  };

  const fetchJSON = (url) => fetch(url, { credentials: 'same-origin' })
    .then(r => r.ok ? r.json() : Promise.reject(r.status));
  const postJSON = (url, body) => fetch(url, {
    method: 'POST', credentials: 'same-origin',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(body || {}),
  }).then(r => r.ok ? r.json() : Promise.reject(r.status));

  // ── KaTeX render helper (uses global if present) ─────────────────────────

  function renderMath(node) {
    if (!node) return;
    if (window.renderMathInElement) {
      try {
        window.renderMathInElement(node, {
          delimiters: [
            {left: '$$', right: '$$', display: true},
            {left: '\\[', right: '\\]', display: true},
            {left: '\\(', right: '\\)', display: false},
            {left: '$',  right: '$',  display: false},
          ],
          throwOnError: false,
        });
      } catch (_) { /* no-op */ }
    }
  }

  // ── Toast / XP popup ─────────────────────────────────────────────────────

  function ensureToastStack() {
    let s = document.getElementById('dq-toast-stack');
    if (!s) {
      s = el('div', {id: 'dq-toast-stack'});
      document.body.appendChild(s);
    }
    return s;
  }
  function toast(opts) {
    const stack = ensureToastStack();
    const t = el('div', {class: 'dq-toast ' + (opts.kind ? 'toast-' + opts.kind : '')}, [
      opts.title ? el('strong', {}, opts.title) : null,
      el('span', {html: opts.body || ''}),
    ]);
    stack.appendChild(t);
    setTimeout(() => t.remove(), 5200);
  }
  function awardToast(xp, reason) {
    if (xp > 0) toast({kind: 'xp', title: '+' + xp + ' XP', body: reason || ''});
  }
  function badgeToasts(newly) {
    (newly || []).forEach(b => toast({
      kind: 'badge', title: b.icon + ' ' + b.title,
      body: b.description,
    }));
  }

  // ── Inject universal tabs (Feladatok / Kvíz / Mini-játék) ────────────────
  // Strategy: find the chapter's existing tab nav (a row of .ila-nav-link
  // spans) and append our 3 new ones in a sibling block. Then create 3
  // tab-panel divs as siblings of the existing .ila-tab divs.

  const TAB_IDS = ['t-fel-univ', 't-kvi-univ', 't-min-univ'];
  const TAB_LABELS = [
    {id: 't-fel-univ', icon: '📝', label: 'Feladatok'},
    {id: 't-kvi-univ', icon: '🎯', label: 'Kvíz'},
    {id: 't-min-univ', icon: '🎮', label: 'Mini-játék'},
  ];

  function findNavRow() {
    const span = document.querySelector('.ila-nav-link');
    return span ? span.parentElement : null;
  }

  function findTabContainer() {
    const tab = document.querySelector('.ila-tab');
    return tab ? tab.parentElement : null;
  }

  // Walk the chapter's existing showTab() (defined inline in each chapter) — it
  // hides ALL .ila-tab elements via class toggles. Our new panels follow the
  // same convention so we don't need to monkey-patch the chapter's function.
  function injectTabs() {
    if (!CH) return;
    const nav = findNavRow();
    const tabContainer = findTabContainer();
    if (!nav || !tabContainer) return;

    if (document.querySelector('.dq-injected-nav')) return; // already injected

    // 1. Build extension nav block
    const navExt = el('span', {class: 'dq-injected-nav'});
    TAB_LABELS.forEach(t => {
      const span = el('span', {
        class: 'ila-nav-link',
        'data-dq-tab': t.id,
        onclick: function(ev) {
          // Use the chapter's own showTab if available, else fallback.
          const fn = window.showTab;
          if (typeof fn === 'function') {
            fn(t.id, this);
          } else {
            document.querySelectorAll('.ila-tab').forEach(p => p.classList.remove('active'));
            document.querySelectorAll('.ila-nav-link').forEach(b => b.classList.remove('active'));
            document.getElementById(t.id).classList.add('active');
            this.classList.add('active');
          }
          // Lazy-render content the first time the tab is opened
          renderTab(t.id);
        },
      }, t.icon + ' ' + t.label);
      navExt.appendChild(span);
    });
    nav.appendChild(navExt);

    // 2. Build 3 hidden tab panels
    TAB_LABELS.forEach(t => {
      const panel = el('div', {id: t.id, class: 'ila-tab', 'data-dq-rendered': '0'});
      tabContainer.appendChild(panel);
    });
  }

  // ── Tab content renderers ────────────────────────────────────────────────

  const renderedTabs = new Set();

  function renderTab(id) {
    if (renderedTabs.has(id)) return;
    renderedTabs.add(id);
    if (id === 't-fel-univ') renderExercises();
    else if (id === 't-kvi-univ') renderQuiz();
    else if (id === 't-min-univ') renderMiniGame();
  }

  // ── Feladatok tab ────────────────────────────────────────────────────────

  let _exerciseData = null;
  let _myProgress = {};

  async function loadProgress() {
    try {
      const me = await fetchJSON('/demos/dimat/api/me');
      _myProgress = (me.per_chapter || {})[CH] || {};
      // also fetch per-exercise statuses by hitting a minimal endpoint? we
      // don't have one yet — use _myProgress aggregate counts only for now.
      return me;
    } catch (e) {
      return {authenticated: false};
    }
  }

  async function renderExercises() {
    const panel = document.getElementById('t-fel-univ');
    if (!panel) return;
    panel.innerHTML = '';
    panel.appendChild(spinner());
    if (!_exerciseData) {
      try { _exerciseData = await fetchJSON('/demos/dimat/api/exercises/' + CH); }
      catch (e) { panel.innerHTML = ''; panel.appendChild(emptyMsg('🚧', 'Nem sikerült betölteni a feladatokat.', '')); return; }
    }
    const me = await fetchJSON('/demos/dimat/api/me').catch(() => ({}));
    const exStatus = await fetchJSON('/demos/dimat/api/exercise_status/' + CH).catch(() => ({}));
    const exes = _exerciseData.exercises || [];
    panel.innerHTML = '';

    if (!exes.length) {
      panel.appendChild(emptyMsg('🌱', 'Még nincsenek feladatok ehhez a fejezethez.',
        'A feladatok kiválogatása folyamatban van.'));
      return;
    }

    // Filter chips
    let activeFilter = 'all';
    const filterRow = el('div', {class: 'dq-filter-row'});
    [
      ['all',       'Mind'],
      ['untried',   'Nem próbáltam'],
      ['attempted', 'Próbáltam'],
      ['solved',    'Megoldva'],
      ['revealed',  'Megnézett'],
    ].forEach(([k, label]) => {
      const c = el('button', {
        class: 'dq-filter-chip' + (k === activeFilter ? ' active' : ''),
        onclick: () => {
          activeFilter = k;
          filterRow.querySelectorAll('.dq-filter-chip').forEach(b => b.classList.remove('active'));
          c.classList.add('active');
          applyFilter();
        },
      }, label);
      filterRow.appendChild(c);
    });
    panel.appendChild(filterRow);

    // Cards
    const list = el('div', {class: 'dq-ex-list'});
    panel.appendChild(list);

    const exStatusMap = exStatus.statuses || {};
    exes.forEach(ex => {
      list.appendChild(buildExerciseCard(ex, exStatusMap[ex.id] || ''));
    });
    renderMath(panel);

    function applyFilter() {
      list.querySelectorAll('.dq-ex-card').forEach(card => {
        const s = card.getAttribute('data-status') || '';
        let show = true;
        if (activeFilter === 'untried')   show = !s;
        else if (activeFilter === 'attempted') show = s === 'attempted';
        else if (activeFilter === 'solved')    show = s === 'solved';
        else if (activeFilter === 'revealed')  show = s === 'revealed';
        card.style.display = show ? '' : 'none';
      });
    }
  }

  function statusPill(status) {
    if (status === 'solved')   return el('span', {class: 'dq-ex-pill dq-pill-solved'}, '🟢 Megoldva');
    if (status === 'revealed') return el('span', {class: 'dq-ex-pill dq-pill-revealed'}, '🔵 Megoldás megnézve');
    if (status === 'attempted')return el('span', {class: 'dq-ex-pill dq-pill-attempted'}, '🟡 Próbáltam');
    return el('span', {class: 'dq-ex-pill dq-pill-untried'}, '⚪ Nem próbáltam');
  }

  function buildExerciseCard(ex, status) {
    const card = el('div', {class: 'dq-ex-card', 'data-status': status, 'data-ex-id': ex.id});
    const head = el('div', {class: 'dq-ex-head'}, [
      el('span', {class: 'dq-ex-id'}, ex.id),
      el('span', {class: 'dq-ex-title'}, ex.title || '(cím nélkül)'),
      statusPill(status),
    ]);
    const body = el('div', {class: 'dq-ex-body', html: mdToHtml(ex.problem_md || '')});
    const actions = el('div', {class: 'dq-ex-actions'});

    const solvedBtn = el('button', {class: 'dq-btn dq-btn-primary', onclick: () => mark(card, 'solved', ex)},
      '✓ Megoldottam (+10 XP)');
    actions.appendChild(solvedBtn);

    if (ex.hint_md) {
      let hintShown = false;
      const hintBtn = el('button', {class: 'dq-btn dq-btn-hint', onclick: () => {
        hintShown = !hintShown;
        if (hintShown) {
          if (!card.querySelector('.dq-hint-block')) {
            const h = el('div', {class: 'dq-solution-block dq-hint-block', html: '<strong>💡 Útmutatás:</strong><br>' + mdToHtml(ex.hint_md)});
            body.parentNode.insertBefore(h, actions);
            renderMath(h);
          }
          card.querySelector('.dq-hint-block').style.display = '';
        } else if (card.querySelector('.dq-hint-block')) {
          card.querySelector('.dq-hint-block').style.display = 'none';
        }
      }}, '💡 Hint');
      actions.appendChild(hintBtn);
    }

    if (ex.solution_md) {
      const revBtn = el('button', {class: 'dq-btn dq-btn-reveal', onclick: () => {
        const existing = card.querySelector('.dq-solution-show');
        if (existing) { existing.remove(); return; }
        const sol = el('div', {class: 'dq-solution-block dq-solution-show',
                               html: '<strong>👁 Megoldás:</strong><br>' + mdToHtml(ex.solution_md)});
        body.parentNode.insertBefore(sol, actions);
        renderMath(sol);
        if (status !== 'solved' && status !== 'revealed') {
          mark(card, 'revealed', ex);
        }
      }}, '👁 Megoldás (+5 XP)');
      actions.appendChild(revBtn);
    }

    card.appendChild(head);
    card.appendChild(body);
    card.appendChild(actions);
    return card;
  }

  async function mark(card, status, ex) {
    try {
      const r = await postJSON('/demos/dimat/api/progress',
        {ch: CH, exercise_id: ex.id, status: status});
      if (r.anonymous) {
        toast({kind: 'error', title: 'Bejelentkezés szükséges',
               body: 'Az XP-megőrzéshez jelentkezz be.'});
        return;
      }
      card.setAttribute('data-status', status);
      card.querySelector('.dq-ex-pill').replaceWith(statusPill(status));
      if (r.xp_delta > 0) awardToast(r.xp_delta,
        status === 'solved' ? 'Megoldottad a feladatot' : 'Megnézted a megoldást');
      badgeToasts(r.newly_earned);
    } catch (e) {
      toast({kind: 'error', body: 'Hiba: ' + e});
    }
  }

  // ── Quiz tab ─────────────────────────────────────────────────────────────

  let _quizState = null;

  async function renderQuiz() {
    const panel = document.getElementById('t-kvi-univ');
    if (!panel) return;
    panel.innerHTML = '';
    panel.appendChild(quizControls());
    const stage = el('div', {id: 'dq-quiz-stage'});
    panel.appendChild(stage);
    panel.appendChild(emptyMsg('🎯', 'Kvíz indítása',
      'Válassz nehézséget, és kattints az „Indítás" gombra.'));
  }

  function quizControls() {
    let diff = 'normal';
    const wrap = el('div', {class: 'dq-quiz-controls'});
    const diffRow = el('div', {class: 'dq-diff-row'});
    [
      ['easy', 'Easy ×0.7'],
      ['normal', 'Normal ×1.0'],
      ['hard', 'Hard ×1.5'],
    ].forEach(([k, lbl]) => {
      const b = el('button', {
        class: 'dq-diff-btn' + (k === 'normal' ? ' active' : ''),
        onclick: () => {
          diff = k;
          diffRow.querySelectorAll('.dq-diff-btn').forEach(x => x.classList.remove('active'));
          b.classList.add('active');
        },
      }, lbl);
      diffRow.appendChild(b);
    });
    const startBtn = el('button', {class: 'dq-btn dq-btn-primary', onclick: () => startQuiz(diff)},
      '▶ Indítás');
    wrap.appendChild(diffRow);
    wrap.appendChild(startBtn);
    return wrap;
  }

  async function startQuiz(difficulty) {
    const stage = document.getElementById('dq-quiz-stage');
    const panel = document.getElementById('t-kvi-univ');
    panel.querySelector('.dq-empty')?.remove();
    stage.innerHTML = '';
    stage.appendChild(spinner());
    let qs;
    try {
      qs = (await fetchJSON('/demos/dimat/api/quiz/' + CH + '?d=' + difficulty)).questions || [];
    } catch (e) {
      stage.innerHTML = '';
      stage.appendChild(emptyMsg('🚧', 'Nem sikerült betölteni a kvízt.', ''));
      return;
    }
    if (!qs.length) {
      stage.innerHTML = '';
      stage.appendChild(emptyMsg('🌱', 'Nincs elég anyag a kvízhez.',
        'Erre a fejezetre még nem készült elég feladat.'));
      return;
    }
    const total = qs.length;
    const timeLimit = difficulty === 'easy' ? 150 : difficulty === 'hard' ? 60 : 90;
    _quizState = {
      qs, idx: 0, answers: {}, t0: Date.now(),
      timeLeft: timeLimit, difficulty, total,
    };
    stage.innerHTML = '';
    stage.appendChild(quizUI());
    showCurrent();
    startTimer();
  }

  function quizUI() {
    const wrap = el('div', {class: 'dq-quiz-wrap'});
    wrap.appendChild(el('div', {class: 'dq-quiz-progress'},
      el('div', {class: 'dq-quiz-progress-bar', id: 'dq-qprog'})));
    wrap.appendChild(el('div', {class: 'dq-quiz-controls'}, [
      el('div', {id: 'dq-quiz-counter', style: {fontSize: '.78rem', color: '#94a3b8'}}, ''),
      el('div', {class: 'dq-quiz-timer', id: 'dq-quiz-timer'}, ''),
    ]));
    wrap.appendChild(el('div', {id: 'dq-quiz-q-area'}));
    wrap.appendChild(el('div', {id: 'dq-quiz-actions', style: {marginTop: '.6rem', display: 'flex', gap: '.5rem'}}));
    return wrap;
  }

  function showCurrent() {
    const s = _quizState;
    if (!s) return;
    const q = s.qs[s.idx];
    const area = document.getElementById('dq-quiz-q-area');
    area.innerHTML = '';
    document.getElementById('dq-qprog').style.width = ((s.idx) / s.total * 100) + '%';
    document.getElementById('dq-quiz-counter').textContent = `Kérdés ${s.idx + 1} / ${s.total}`;
    const card = el('div', {class: 'dq-quiz-q'});
    card.appendChild(el('div', {class: 'dq-quiz-q-text', html: mdToHtml(q.q || '')}));
    const opts = el('div', {class: 'dq-quiz-options'});
    (q.options || []).forEach(o => {
      const btn = el('button', {
        class: 'dq-quiz-opt' + (s.answers[q.id] === o.k ? ' selected' : ''),
        onclick: () => {
          s.answers[q.id] = o.k;
          opts.querySelectorAll('.dq-quiz-opt').forEach(x => x.classList.remove('selected'));
          btn.classList.add('selected');
        },
      }, [
        el('span', {class: 'dq-quiz-opt-letter'}, o.k + ')'),
        el('span', {html: mdToHtml(o.text || '')}),
      ]);
      opts.appendChild(btn);
    });
    card.appendChild(opts);
    area.appendChild(card);
    renderMath(card);

    const actions = document.getElementById('dq-quiz-actions');
    actions.innerHTML = '';
    if (s.idx > 0) actions.appendChild(el('button', {class: 'dq-btn',
      onclick: () => { s.idx--; showCurrent(); }}, '← Előző'));
    actions.appendChild(el('div', {style: {flex: '1'}}));
    if (s.idx < s.total - 1) {
      actions.appendChild(el('button', {class: 'dq-btn dq-btn-primary',
        onclick: () => { s.idx++; showCurrent(); }}, 'Következő →'));
    } else {
      actions.appendChild(el('button', {class: 'dq-btn dq-btn-primary', onclick: submitQuiz},
        '✓ Beadom'));
    }
  }

  function startTimer() {
    const s = _quizState;
    if (!s) return;
    if (s._timerHandle) clearInterval(s._timerHandle);
    const tick = () => {
      if (!_quizState || _quizState !== s) { clearInterval(s._timerHandle); return; }
      s.timeLeft--;
      const t = document.getElementById('dq-quiz-timer');
      if (t) {
        const mm = Math.floor(Math.max(0, s.timeLeft) / 60);
        const ss = Math.max(0, s.timeLeft) % 60;
        t.textContent = `${mm}:${ss.toString().padStart(2, '0')}`;
        if (s.timeLeft <= 10) t.classList.add('warn');
      }
      if (s.timeLeft <= 0) {
        clearInterval(s._timerHandle);
        submitQuiz();
      }
    };
    tick();
    s._timerHandle = setInterval(tick, 1000);
  }

  async function submitQuiz() {
    const s = _quizState;
    if (!s) return;
    if (s._timerHandle) clearInterval(s._timerHandle);
    let score = 0;
    const wrong = [];
    s.qs.forEach(q => {
      if (s.answers[q.id] === q.answer) score++;
      else wrong.push(q.id);
    });
    const duration = Math.round((Date.now() - s.t0) / 1000);

    let res = {};
    try {
      res = await postJSON('/demos/dimat/api/quiz_result', {
        ch: CH, score, total: s.total,
        duration_sec: duration,
        difficulty: s.difficulty,
        wrong_qids: wrong,
      });
    } catch (_) { /* anonymous or network */ }

    const stage = document.getElementById('dq-quiz-stage');
    stage.innerHTML = '';
    const result = el('div', {class: 'dq-quiz-result'});
    result.appendChild(el('div', {class: 'dq-quiz-score'}, `${score} / ${s.total}`));
    result.appendChild(el('div', {class: 'dq-quiz-pct'},
      `${(score / s.total * 100).toFixed(0)}%   |   ${duration}s   |   ${s.difficulty.toUpperCase()}`));
    if (res.xp_delta > 0) {
      result.appendChild(el('div', {class: 'dq-quiz-xp'}, `+${res.xp_delta} XP`));
    }
    const review = el('div', {style: {marginTop: '1.5rem', textAlign: 'left'}});
    s.qs.forEach((q, i) => {
      const correct = s.answers[q.id] === q.answer;
      review.appendChild(el('div', {style: {marginBottom: '.5rem', fontSize: '.78rem',
        color: correct ? '#34d399' : '#ef4444', fontFamily: 'monospace'}},
        (correct ? '✓ ' : '✗ ') + `Q${i + 1}: ${q.q.slice(0, 60)}${q.q.length > 60 ? '…' : ''} → válaszodtál: ${s.answers[q.id] || '—'} | helyes: ${q.answer}`));
    });
    result.appendChild(review);
    result.appendChild(el('div', {style: {marginTop: '1.2rem', display: 'flex', gap: '.5rem', justifyContent: 'center'}}, [
      el('button', {class: 'dq-btn', onclick: () => { renderedTabs.delete('t-kvi-univ'); renderQuiz(); }},
        '↻ Újra'),
    ]));
    stage.appendChild(result);
    if (res.xp_delta > 0) awardToast(res.xp_delta, 'Kvíz teljesítve');
    badgeToasts(res.newly_earned);
    _quizState = null;
  }

  // ── Mini-game tab ────────────────────────────────────────────────────────

  window.DimatGames = window.DimatGames || {
    _registry: {},
    register(ch, spec) { this._registry[ch] = spec; },
    get(ch) { return this._registry[ch]; },
  };

  async function renderMiniGame() {
    const panel = document.getElementById('t-min-univ');
    if (!panel) return;
    panel.innerHTML = '';
    const wrap = el('div', {class: 'dq-game-wrap'});
    panel.appendChild(wrap);

    // Try to load the chapter-specific game module on demand
    if (CH && !window.DimatGames.get(CH)) {
      await loadScript('/static/js/dimat/games/' + CH + '.js').catch(() => null);
    }
    const spec = CH ? window.DimatGames.get(CH) : null;
    if (!spec) {
      panel.innerHTML = '';
      panel.appendChild(emptyMsg('🎮', 'Mini-játék hamarosan',
        'Erre a fejezetre még nem készült el a mini-játék.'));
      return;
    }

    // Header
    const header = el('div', {class: 'dq-game-header'});
    header.appendChild(el('div', {class: 'dq-game-title'}, spec.icon + ' ' + spec.title));
    header.appendChild(el('div', {class: 'dq-game-score', id: 'dq-game-score'}, 'Score: 0'));

    let textMode = false;
    const textBtn = el('button', {class: 'dq-btn',
      onclick: () => { textMode = !textMode; mount(); }},
      '📄 Szöveges mód');
    header.appendChild(textBtn);
    const restartBtn = el('button', {class: 'dq-btn',
      onclick: () => mount()}, '↻ Újra');
    header.appendChild(restartBtn);
    wrap.appendChild(header);

    const stage = el('div', {class: 'dq-game-canvas-wrap', id: 'dq-game-stage'});
    wrap.appendChild(stage);
    if (spec.hint) wrap.appendChild(el('div', {class: 'dq-game-hint', html: spec.hint}));

    const ctx = {
      el, fetchJSON, postJSON, awardXP: awardToast, toast,
      onScore: async (score, max) => {
        document.getElementById('dq-game-score').textContent = `Score: ${score}/${max}`;
        try {
          const r = await postJSON('/demos/dimat/api/game_result',
            {ch: CH, score, max_score: max});
          if (r.xp_delta > 0) awardToast(r.xp_delta, spec.title);
          badgeToasts(r.newly_earned);
        } catch (_) {}
      },
    };

    function mount() {
      stage.innerHTML = '';
      if (textMode && spec.startText) {
        const pane = el('div', {class: 'dq-text-mode-pane'});
        stage.appendChild(pane);
        spec.startText(pane, ctx);
      } else if (spec.start) {
        spec.start(stage, ctx);
      }
    }
    mount();
  }

  function loadScript(src) {
    return new Promise((resolve, reject) => {
      const s = document.createElement('script');
      s.src = src; s.async = true;
      s.onload = resolve;
      s.onerror = reject;
      document.head.appendChild(s);
    });
  }

  // ── Markdown renderer (bare-minimum: code, bold, italic, line breaks, KaTeX
  //                       passthrough). Solutions.md is heavy LaTeX, so we
  //                       intentionally leave most of it unchanged for KaTeX. )

  function mdToHtml(md) {
    if (!md) return '';
    // Escape HTML first
    let h = md.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
    // Don't touch math blocks: temporarily replace $$..$$, \[..\], \(..\), $..$
    const placeholders = [];
    const stash = (re) => {
      h = h.replace(re, (m) => {
        placeholders.push(m);
        return ` DQ${placeholders.length - 1} `;
      });
    };
    stash(/\$\$[\s\S]*?\$\$/g);
    stash(/\\\[[\s\S]*?\\\]/g);
    stash(/\\\([\s\S]*?\\\)/g);
    stash(/\$[^$\n]+\$/g);
    // Code fences
    h = h.replace(/```([\s\S]*?)```/g, (_, c) => '<pre>' + c + '</pre>');
    h = h.replace(/`([^`\n]+)`/g, '<code>$1</code>');
    // Bold / italic
    h = h.replace(/\*\*([^*\n]+)\*\*/g, '<strong>$1</strong>');
    h = h.replace(/(?<!\*)\*([^*\n]+)\*(?!\*)/g, '<em>$1</em>');
    // Headings
    h = h.replace(/^####\s+(.*)$/gm, '<h5>$1</h5>');
    h = h.replace(/^###\s+(.*)$/gm, '<h4>$1</h4>');
    h = h.replace(/^##\s+(.*)$/gm, '<h3>$1</h3>');
    // Lists (super basic)
    h = h.replace(/(^|\n)([-*]) (.*)/g, '$1<li>$3</li>');
    // Paragraphs / line breaks
    h = h.replace(/\n{2,}/g, '</p><p>');
    h = h.replace(/\n/g, '<br>');
    h = '<p>' + h + '</p>';
    // Restore math
    h = h.replace(/ DQ(\d+) /g, (_, i) => placeholders[+i]);
    return h;
  }

  function spinner() {
    return el('div', {class: 'dq-empty'}, [
      el('span', {class: 'dq-spinner'}),
      el('span', {style: {marginLeft: '.5rem'}}, 'Betöltés…'),
    ]);
  }
  function emptyMsg(icon, title, body) {
    return el('div', {class: 'dq-empty'}, [
      el('span', {class: 'dq-empty-icon'}, icon),
      el('strong', {style: {color: '#94a3b8', display: 'block', marginBottom: '.3rem'}}, title),
      body || null,
    ]);
  }

  // ── Public surface ───────────────────────────────────────────────────────

  window.DimatQuiz = {
    fetchJSON, postJSON,
    toast, awardXP: awardToast,
    renderExercises, renderQuiz, renderMiniGame,
    renderMath,
    el,
    get currentChapter() { return CH; },
  };

  // ── Boot ─────────────────────────────────────────────────────────────────

  function boot() {
    if (CH) injectTabs();
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }
})();
