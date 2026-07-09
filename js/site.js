document.documentElement.classList.replace('no-js', 'js');

(function () {
  'use strict';

  var CATEGORIES = ['animation', 'video', 'ai'];

  function currentCategory() {
    var hash = location.hash.slice(1);
    return CATEGORIES.indexOf(hash) !== -1 ? hash : '';
  }

  function applyFilter() {
    var cat = currentCategory();
    var tiles = document.querySelectorAll('.grid .tile');
    for (var i = 0; i < tiles.length; i++) {
      var cats = (tiles[i].getAttribute('data-category') || '').split(' ');
      tiles[i].hidden = cat !== '' && cats.indexOf(cat) === -1;
    }
    var titles = document.querySelectorAll('.menu-cat-title');
    for (var j = 0; j < titles.length; j++) {
      var isActive = cat !== '' && titles[j].getAttribute('href') === '/#' + cat;
      titles[j].classList.toggle('is-active', isActive);
    }
    var all = document.querySelector('.menu-all');
    if (all) {
      var onHome = location.pathname === '/' || /\/index\.html$/.test(location.pathname);
      all.classList.toggle('is-active', onHome && cat === '');
    }
  }

  function markActivePage(scope) {
    var links = scope.querySelectorAll('a[href^="/cases/"], a[href="/about.html"]');
    for (var i = 0; i < links.length; i++) {
      if (links[i].pathname === location.pathname) links[i].classList.add('is-active');
    }
  }

  function initToggle(scope) {
    var btn = scope.querySelector('.menu-toggle');
    if (!btn) return;
    btn.addEventListener('click', function () {
      var open = document.body.classList.toggle('menu-open');
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    scope.addEventListener('click', function (e) {
      var link = e.target.closest && e.target.closest('a');
      if (link && document.body.classList.contains('menu-open')) {
        document.body.classList.remove('menu-open');
        btn.setAttribute('aria-expanded', 'false');
      }
    });
  }

  fetch('/menu.html')
    .then(function (r) { return r.text(); })
    .then(function (html) {
      var mount = document.getElementById('site-menu');
      if (!mount) return;
      mount.innerHTML = html;
      markActivePage(mount);
      initToggle(mount);
      applyFilter();
    });

  // Casetitel in woorden splitsen voor de reveal-animatie (CSS regelt beweging + verloop)
  var title = document.querySelector('.case-article h1');
  if (title) {
    var words = title.textContent.trim().split(/\s+/);
    title.textContent = '';
    for (var w = 0; w < words.length; w++) {
      var span = document.createElement('span');
      span.className = 'w';
      span.textContent = words[w];
      span.style.animationDelay = (w * 70) + 'ms';
      title.appendChild(span);
      if (w < words.length - 1) title.appendChild(document.createTextNode(' '));
    }
  }

  window.addEventListener('hashchange', applyFilter);
  applyFilter();
})();
