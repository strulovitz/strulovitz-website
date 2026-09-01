/*
  lightbox.js -- click a small picture, see it big, fitted to your screen.
  Works the same with a mouse and with a finger: tap anywhere to close.
  Any <img class="thumb"> on the page gets this behaviour automatically.
  The full-size file and an optional caption come from the img's
  data-full and data-caption attributes.
*/
(function () {
  'use strict';

  var style = document.createElement('style');
  style.textContent = [
    '.lb-overlay{position:fixed;inset:0;z-index:9999;background:rgba(4,6,11,.93);',
    'display:flex;flex-direction:column;align-items:center;justify-content:center;',
    'padding:16px;cursor:zoom-out;}',
    '.lb-overlay img{max-width:100%;max-height:88vh;width:auto;height:auto;',
    'object-fit:contain;border-radius:8px;opacity:0;transition:opacity .2s;}',
    '.lb-overlay img.lb-ready{opacity:1;}',
    '.lb-caption{color:#c7d4ee;font:15px/1.5 system-ui,-apple-system,Segoe UI,sans-serif;',
    'margin-top:10px;text-align:center;max-width:90vw;}',
    '.lb-close{position:fixed;top:10px;right:12px;width:48px;height:48px;',
    'border:none;border-radius:50%;background:#16203a;color:#eaf4ff;',
    'font-size:26px;line-height:1;cursor:pointer;}',
    '.lb-close:hover{background:#1d2b4c;}',
    '.lb-spinner{width:38px;height:38px;border:4px solid #22355c;',
    'border-top-color:#9fd0ff;border-radius:50%;animation:lb-spin .8s linear infinite;}',
    '@keyframes lb-spin{to{transform:rotate(360deg);}}',
    'body.lb-open{overflow:hidden;}'
  ].join('');
  document.head.appendChild(style);

  var overlay = null;

  function close() {
    if (!overlay) return;
    document.body.classList.remove('lb-open');
    overlay.remove();
    overlay = null;
    document.removeEventListener('keydown', onKey);
  }

  function onKey(event) {
    if (event.key === 'Escape') close();
  }

  function open(fullSrc, caption) {
    close();
    overlay = document.createElement('div');
    overlay.className = 'lb-overlay';

    var spinner = document.createElement('div');
    spinner.className = 'lb-spinner';
    overlay.appendChild(spinner);

    var closeBtn = document.createElement('button');
    closeBtn.className = 'lb-close';
    closeBtn.setAttribute('aria-label', 'Close');
    closeBtn.textContent = '\u00D7';
    overlay.appendChild(closeBtn);

    var img = document.createElement('img');
    img.alt = caption || 'Full size picture';
    overlay.appendChild(img);

    if (caption) {
      var cap = document.createElement('div');
      cap.className = 'lb-caption';
      cap.textContent = caption;
      overlay.appendChild(cap);
    }

    overlay.addEventListener('click', close);
    document.body.classList.add('lb-open');
    document.body.appendChild(overlay);
    document.addEventListener('keydown', onKey);

    img.addEventListener('load', function () {
      spinner.remove();
      img.classList.add('lb-ready');
    });
    img.addEventListener('error', function () {
      spinner.remove();
      var sorry = document.createElement('div');
      sorry.className = 'lb-caption';
      sorry.textContent = 'Sorry, the big picture could not be loaded.';
      overlay.appendChild(sorry);
    });
    img.src = fullSrc;
  }

  function activate() {
    for (var thumbs = document.querySelectorAll('img.thumb'), i = 0; i < thumbs.length; i++) {
      thumbs[i].addEventListener('click', function (event) {
        event.stopPropagation();
        var full = this.getAttribute('data-full') || this.src;
        open(full, this.getAttribute('data-caption'));
      });
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', activate);
  } else {
    activate();
  }
})();
