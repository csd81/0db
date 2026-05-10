/* dimat games shared helpers — tiny canvas/DOM utilities used by every game.
   Loaded once via dimat_quiz.js context; exposes window.DimatGameLib. */
(() => {
  'use strict';
  if (window.DimatGameLib) return;

  const Lib = {};

  Lib.fitCanvas = (canvas) => {
    const dpr = window.devicePixelRatio || 1;
    const rect = canvas.getBoundingClientRect();
    canvas.width = rect.width * dpr;
    canvas.height = rect.height * dpr;
    const ctx = canvas.getContext('2d');
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    return {ctx, w: rect.width, h: rect.height};
  };

  Lib.makeCanvas = (host) => {
    const c = document.createElement('canvas');
    c.className = 'dq-game-canvas';
    c.tabIndex = 0;
    host.appendChild(c);
    return c;
  };

  Lib.makeOverlay = (host, html) => {
    const o = document.createElement('div');
    o.style.position = 'absolute';
    o.style.left = '0'; o.style.right = '0';
    o.style.top = '0'; o.style.padding = '.5rem .85rem';
    o.style.fontSize = '.78rem';
    o.style.color = '#c4cdd8';
    o.style.background = 'linear-gradient(180deg, rgba(13,17,23,.92), rgba(13,17,23,0))';
    o.style.pointerEvents = 'none';
    o.innerHTML = html;
    host.appendChild(o);
    return o;
  };

  Lib.drawNode = (ctx, x, y, r, fill, label, opt) => {
    opt = opt || {};
    ctx.beginPath(); ctx.arc(x, y, r, 0, Math.PI * 2);
    ctx.fillStyle = fill; ctx.fill();
    if (opt.stroke) { ctx.strokeStyle = opt.stroke; ctx.lineWidth = opt.lw || 2; ctx.stroke(); }
    if (label != null) {
      ctx.fillStyle = opt.textColor || '#000';
      ctx.font = `${opt.fontWeight || 700} ${opt.fontSize || 11}px sans-serif`;
      ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
      ctx.fillText(label, x, y);
    }
  };

  Lib.drawEdge = (ctx, x1, y1, x2, y2, opt) => {
    opt = opt || {};
    ctx.beginPath(); ctx.moveTo(x1, y1); ctx.lineTo(x2, y2);
    ctx.strokeStyle = opt.color || '#475569';
    ctx.lineWidth = opt.width || 1.5;
    if (opt.dash) { ctx.setLineDash(opt.dash); }
    ctx.stroke();
    if (opt.dash) ctx.setLineDash([]);
  };

  Lib.timer = (host, opts, onExpire) => {
    const start = Date.now();
    const limit = opts.limit || 60;
    const div = document.createElement('div');
    Object.assign(div.style, {
      position: 'absolute', right: '.6rem', top: '.5rem',
      fontFamily: 'monospace', fontSize: '1rem', fontWeight: 700,
      color: '#fbbf24', background: 'rgba(13,17,23,.85)',
      padding: '.25rem .65rem', borderRadius: '.3rem',
      pointerEvents: 'none', zIndex: 5,
    });
    host.appendChild(div);
    let raf;
    const tick = () => {
      const elapsed = (Date.now() - start) / 1000;
      const left = Math.max(0, limit - elapsed);
      const mm = Math.floor(left / 60);
      const ss = Math.floor(left % 60);
      div.textContent = `${mm}:${ss.toString().padStart(2, '0')}`;
      if (left <= 5) div.style.color = '#ef4444';
      if (left <= 0) { cancelAnimationFrame(raf); if (onExpire) onExpire(elapsed); return; }
      raf = requestAnimationFrame(tick);
    };
    tick();
    return {
      element: div,
      stop() { cancelAnimationFrame(raf); },
      elapsed: () => (Date.now() - start) / 1000,
    };
  };

  Lib.scoreBadge = (host) => {
    const div = document.createElement('div');
    Object.assign(div.style, {
      position: 'absolute', left: '.6rem', top: '.5rem',
      fontFamily: 'monospace', fontSize: '.95rem', fontWeight: 700,
      color: '#34d399', background: 'rgba(13,17,23,.85)',
      padding: '.25rem .65rem', borderRadius: '.3rem',
      pointerEvents: 'none', zIndex: 5,
    });
    host.appendChild(div);
    let s = 0;
    const update = () => { div.textContent = `Score: ${s}`; };
    update();
    return {
      get() { return s; },
      add(n) { s += n; update(); },
      set(n) { s = n; update(); },
    };
  };

  Lib.endScreen = (host, {score, max, msg, onAgain}) => {
    const o = document.createElement('div');
    Object.assign(o.style, {
      position: 'absolute', inset: 0,
      display: 'flex', flexDirection: 'column',
      alignItems: 'center', justifyContent: 'center',
      background: 'rgba(13,17,23,.96)',
      textAlign: 'center', color: '#c4cdd8',
      padding: '1.5rem', zIndex: 10,
    });
    const big = document.createElement('div');
    Object.assign(big.style, {
      fontSize: '2.5rem', fontWeight: 800, lineHeight: 1,
      background: 'linear-gradient(135deg,#34d399,#38bdf8)',
      WebkitBackgroundClip: 'text', backgroundClip: 'text',
      WebkitTextFillColor: 'transparent',
    });
    big.textContent = `${score} / ${max}`;
    o.appendChild(big);
    if (msg) {
      const p = document.createElement('div');
      p.style.marginTop = '.5rem'; p.style.fontSize = '.85rem';
      p.style.color = '#94a3b8';
      p.textContent = msg;
      o.appendChild(p);
    }
    if (onAgain) {
      const btn = document.createElement('button');
      btn.className = 'dq-btn';
      btn.textContent = '↻ Újra';
      btn.style.marginTop = '1rem';
      btn.onclick = () => { o.remove(); onAgain(); };
      o.appendChild(btn);
    }
    host.appendChild(o);
    return o;
  };

  Lib.shuffle = (a) => {
    const arr = a.slice();
    for (let i = arr.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [arr[i], arr[j]] = [arr[j], arr[i]];
    }
    return arr;
  };

  Lib.rand = (a, b) => a + Math.random() * (b - a);
  Lib.randint = (a, b) => Math.floor(a + Math.random() * (b - a + 1));
  Lib.choice = (arr) => arr[Math.floor(Math.random() * arr.length)];

  /* questGame: a fancy single-canvas-style quiz that walks through items
     visually with a timer and progress bar. items: [{prompt, options[], answer, explanation?}] */
  Lib.questGame = (host, items, opts, onScore) => {
    opts = opts || {};
    const limit = opts.limit || (items.length * 12);
    host.style.background = '#0d1117';
    host.innerHTML = '';
    let idx = 0, correct = 0;

    const score = Lib.scoreBadge(host);
    const timer = Lib.timer(host, {limit}, () => finish(true));
    const stage = document.createElement('div');
    Object.assign(stage.style, {
      position: 'absolute', inset: 0, padding: '3rem 1.5rem 1rem',
      display: 'flex', flexDirection: 'column', overflow: 'auto',
    });
    host.appendChild(stage);

    const progress = document.createElement('div');
    Object.assign(progress.style, {
      height: '5px', background: '#1e2533', borderRadius: '3px',
      overflow: 'hidden', marginBottom: '1rem',
    });
    const pbar = document.createElement('div');
    Object.assign(pbar.style, {
      height: '100%', width: '0%', transition: 'width .3s',
      background: 'linear-gradient(90deg, #34d399, #38bdf8)',
    });
    progress.appendChild(pbar); stage.appendChild(progress);

    const card = document.createElement('div');
    Object.assign(card.style, {
      background: '#161b22', border: '1px solid #1e2533', borderRadius: '.5rem',
      padding: '1.2rem', flex: 1,
    });
    stage.appendChild(card);

    function render() {
      if (idx >= items.length) return finish(false);
      const it = items[idx];
      pbar.style.width = ((idx) / items.length * 100) + '%';
      card.innerHTML = `
        <div style="font-size:.78rem;color:#94a3b8;margin-bottom:.6rem">
          Kérdés ${idx + 1} / ${items.length}
        </div>
        <div style="font-size:.95rem;color:#e6edf3;margin-bottom:1rem;line-height:1.6">${it.prompt}</div>
      `;
      const opts = document.createElement('div');
      opts.style.display = 'flex'; opts.style.flexDirection = 'column'; opts.style.gap = '.35rem';
      it.options.forEach((opt, i) => {
        const b = document.createElement('button');
        b.className = 'dq-btn';
        b.style.textAlign = 'left'; b.style.fontSize = '.84rem';
        b.style.whiteSpace = 'normal'; b.style.padding = '.55rem .8rem';
        b.innerHTML = `<span style="display:inline-block;width:1.4rem;color:#64748b;font-weight:700">${String.fromCharCode(65+i)})</span> ${opt}`;
        b.onclick = () => {
          [...opts.children].forEach(x => x.disabled = true);
          if (i === it.answer) {
            correct++; score.add(15);
            b.style.background = '#0d2b1e'; b.style.borderColor = '#34d399'; b.style.color = '#34d399';
          } else {
            score.add(-5);
            b.style.background = '#2b0d11'; b.style.borderColor = '#ef4444'; b.style.color = '#ef4444';
            const ans = opts.children[it.answer];
            if (ans) {
              ans.style.background = '#0d2b1e';
              ans.style.borderColor = '#34d399'; ans.style.color = '#34d399';
            }
          }
          if (it.explanation) {
            const ex = document.createElement('div');
            ex.style.cssText = 'margin-top:.6rem;padding:.55rem .75rem;background:#040a10;border-left:2px solid #38bdf8;border-radius:.25rem;font-size:.78rem;color:#94a3b8;line-height:1.7';
            ex.innerHTML = '<strong style="color:#38bdf8">💡</strong> ' + it.explanation;
            card.appendChild(ex);
          }
          setTimeout(() => { idx++; render(); }, 1100);
        };
        opts.appendChild(b);
      });
      card.appendChild(opts);
    }
    function finish(timedOut) {
      timer.stop();
      const max = items.length * 15;
      const s = Math.max(0, score.get());
      onScore && onScore(s, max);
      Lib.endScreen(host, {
        score: s, max,
        msg: timedOut ? 'Lejárt az idő' : `Helyes: ${correct} / ${items.length}`,
        onAgain: () => Lib.questGame(host, items, opts, onScore),
      });
    }
    render();
  };

  // Simple text-mode list renderer. Each item is {prompt, options, answer, explanation}.
  Lib.textModeQuiz = (host, items, onScore) => {
    let idx = 0, score = 0;
    const render = () => {
      host.innerHTML = '';
      if (idx >= items.length) {
        host.innerHTML = `<h3 style="color:#34d399;text-align:center">${score}/${items.length}</h3>`;
        if (onScore) onScore(score, items.length);
        return;
      }
      const it = items[idx];
      const wrap = document.createElement('div');
      wrap.innerHTML = `<div style="font-weight:600;margin-bottom:.6rem">Q${idx+1}/${items.length}: ${it.prompt}</div>`;
      it.options.forEach((opt, i) => {
        const btn = document.createElement('button');
        btn.className = 'dq-btn';
        btn.style.display = 'block';
        btn.style.width = '100%';
        btn.style.textAlign = 'left';
        btn.style.marginBottom = '.35rem';
        btn.textContent = String.fromCharCode(65 + i) + ') ' + opt;
        btn.onclick = () => {
          if (i === it.answer) score++;
          idx++; render();
        };
        wrap.appendChild(btn);
      });
      host.appendChild(wrap);
    };
    render();
  };

  window.DimatGameLib = Lib;
})();
