/* lang_switch.js — site-wide HU/EN preference.
   Loaded synchronously in <head> so the body class is applied BEFORE the
   first paint and there is no flash of wrong-language content.
   Default language: Hungarian (no class). English: body.lang-en. */
(function () {
  'use strict';

  var KEY = 'lang_pref';
  var DEFAULT_LANG = 'hu';

  function readPref() {
    try {
      return localStorage.getItem(KEY) || DEFAULT_LANG;
    } catch (e) {
      return DEFAULT_LANG;
    }
  }

  function applyPref(lang) {
    var html = document.documentElement;
    if (lang === 'en') {
      html.classList.add('lang-en');
      html.classList.remove('lang-hu');
    } else {
      html.classList.remove('lang-en');
      html.classList.add('lang-hu');
    }
    // Mirror to <body> if present (matches CSS selectors that target either)
    var b = document.body;
    if (b) {
      if (lang === 'en') {
        b.classList.add('lang-en');
        b.classList.remove('lang-hu');
      } else {
        b.classList.remove('lang-en');
        b.classList.add('lang-hu');
      }
    }
    // Screen-reader / accessibility hint
    html.lang = lang === 'en' ? 'en' : 'hu';
  }

  function setPref(lang) {
    try { localStorage.setItem(KEY, lang); } catch (e) { /* private mode */ }
    applyPref(lang);
    updateButtons(lang);
    // Notify listeners (e.g. dimat_quiz.js) so they can re-render dynamic content
    try {
      window.dispatchEvent(new CustomEvent('langchange', { detail: { lang: lang } }));
    } catch (e) { /* IE-style fallback */ }
  }

  function updateButtons(lang) {
    var btns = document.querySelectorAll('.lang-toggle .lang-btn');
    btns.forEach(function (b) {
      b.classList.toggle('active', b.getAttribute('data-lang') === lang);
      b.setAttribute('aria-pressed', String(b.getAttribute('data-lang') === lang));
    });
  }

  function wire() {
    document.querySelectorAll('.lang-toggle .lang-btn').forEach(function (b) {
      b.addEventListener('click', function () {
        setPref(b.getAttribute('data-lang'));
      });
    });
    updateButtons(readPref());
  }

  // Public API
  window.LangSwitch = {
    get: readPref,
    set: setPref,
    apply: applyPref,
  };

  // Apply preference immediately (body may or may not exist yet)
  applyPref(readPref());

  // Re-apply + wire button handlers once DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function () {
      applyPref(readPref());
      wire();
    });
  } else {
    applyPref(readPref());
    wire();
  }
})();
