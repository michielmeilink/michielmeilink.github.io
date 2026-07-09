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

  // Eigen minimale videospeler voor self-hosted mp4's
  function initPlayers() {
    var players = document.querySelectorAll('.player');
    for (var i = 0; i < players.length; i++) (function (p) {
      var video = p.querySelector('video');
      var play = p.querySelector('.player-play');
      var mute = p.querySelector('.player-mute');
      var bar = p.querySelector('.player-progress');
      var fill = p.querySelector('.player-progress-fill');
      video.removeAttribute('controls');
      function toggle() { if (video.paused) { video.play(); } else { video.pause(); } }
      function syncPlay() {
        p.classList.toggle('is-playing', !video.paused);
        play.setAttribute('aria-label', video.paused ? 'Play' : 'Pause');
      }
      function syncMute() {
        p.classList.toggle('is-muted', video.muted);
        mute.setAttribute('aria-label', video.muted ? 'Unmute' : 'Mute');
      }
      play.addEventListener('click', toggle);
      video.addEventListener('click', toggle);
      mute.addEventListener('click', function () { video.muted = !video.muted; });
      video.addEventListener('play', syncPlay);
      video.addEventListener('pause', syncPlay);
      video.addEventListener('volumechange', syncMute);
      video.addEventListener('timeupdate', function () {
        if (video.duration) fill.style.width = (video.currentTime / video.duration * 100) + '%';
      });
      bar.addEventListener('click', function (e) {
        var r = bar.getBoundingClientRect();
        if (video.duration) video.currentTime = Math.max(0, Math.min(1, (e.clientX - r.left) / r.width)) * video.duration;
      });
      var fs = p.querySelector('.player-fs');
      if (fs) fs.addEventListener('click', function () {
        if (document.fullscreenElement === p) {
          document.exitFullscreen();
        } else if (p.requestFullscreen) {
          p.requestFullscreen();
        } else if (video.webkitEnterFullscreen) {
          video.webkitEnterFullscreen(); // iPhone Safari: alleen native fullscreen op de video zelf
        }
      });
      syncPlay();
      syncMute();
    })(players[i]);
  }
  initPlayers();

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
