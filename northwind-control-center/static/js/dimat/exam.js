/* exam.js — small client module for /demos/dimat/exam/<NN> pages.
   - KaTeX auto-render of body + formulas
   - Prev/Next keyboard nav (← / →)
   - "Add SRS" button → POST /demos/dimat/api/srs_grade */
(() => {
  'use strict';
  const root = document.querySelector('.exam-page');
  if (!root) return;

  const n = parseInt(root.dataset.tetelN || '0', 10);
  const prevN = parseInt(root.dataset.prev || '0', 10);
  const nextN = parseInt(root.dataset.next || '0', 10);

  // KaTeX auto-render
  const DELIMS = [
    {left: '$$', right: '$$', display: true},
    {left: '\\[', right: '\\]', display: true},
    {left: '$', right: '$', display: false},
    {left: '\\(', right: '\\)', display: false},
  ];
  window.__renderExamMath = function () {
    if (!window.renderMathInElement) return;
    try {
      window.renderMathInElement(root, {
        delimiters: DELIMS,
        throwOnError: false,
        ignoredTags: ['script', 'noscript', 'style', 'textarea', 'pre', 'code'],
      });
    } catch (e) { /* swallow */ }
  };
  // Defensive: also run after window load in case onload fired before this script.
  if (window.renderMathInElement) window.__renderExamMath();
  window.addEventListener('load', () => window.__renderExamMath());

  // Keyboard prev/next
  document.addEventListener('keydown', (e) => {
    if (e.target && /^(INPUT|TEXTAREA|SELECT)$/.test(e.target.tagName)) return;
    if (e.key === 'ArrowLeft' && prevN) {
      window.location.href = '/demos/dimat/exam/' + String(prevN).padStart(2, '0');
    } else if (e.key === 'ArrowRight' && nextN) {
      window.location.href = '/demos/dimat/exam/' + String(nextN).padStart(2, '0');
    }
  });

  // Add to SRS
  const btn = document.getElementById('dq-exam-srs-add');
  if (btn) {
    btn.addEventListener('click', async () => {
      btn.disabled = true;
      const orig = btn.textContent;
      try {
        const r = await fetch('/demos/dimat/api/srs_grade', {
          method: 'POST',
          credentials: 'same-origin',
          headers: {'Content-Type': 'application/json'},
          body: JSON.stringify({
            ch: 'tetel',
            question_id: 'tetel-' + String(n).padStart(2, '0'),
            grade: 3,
          }),
        });
        if (r.ok) {
          btn.textContent = '✓ Hozzáadva';
          btn.style.color = '#34d399';
          btn.style.borderColor = '#34d399';
        } else if (r.status === 401) {
          btn.textContent = 'Jelentkezz be';
          btn.style.color = '#f59e0b';
        } else {
          btn.textContent = 'Hiba';
          btn.style.color = '#ef4444';
        }
      } catch (_) {
        btn.textContent = 'Hiba';
        btn.style.color = '#ef4444';
      }
      setTimeout(() => {
        btn.textContent = orig;
        btn.style.color = '';
        btn.style.borderColor = '';
        btn.disabled = false;
      }, 2200);
    });
  }
})();
