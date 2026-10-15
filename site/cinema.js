/* Sandim R15 · camada cinematográfica · CRdevs
   Genérico (protótipo e tema Shopify): revelação ao rolar, abertura do banner, paralaxe,
   contadores, indicadores deslizantes, transição de página, gavetas animadas e produto voando ao carrinho. */
(function () {
  'use strict';
  var calmo = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var $$ = function (s, el) { return Array.prototype.slice.call((el || document).querySelectorAll(s)); };
  var io = null;

  /* ---------- revelação ao rolar ---------- */
  var ALVOS = [
    ['.sec-head', ''], ['.grade .card', ''], ['.categorias .cat', ''], ['.motos .moto-card', 'rv-zoom'],
    ['.canal .txt', 'rv-esq'], ['.canal .visual', 'rv-zoom'], ['.beneficios > div', ''], ['.catalogo-nav .cn', ''],
    ['.garantias', ''], ['.acc', ''], ['.desc-box', ''], ['.rodape-in > div', ''], ['[data-rv]', '']
  ];
  function revela(el) { el.classList.add('rv-in'); if (io) io.unobserve(el); contar(el); }
  // cascata ordenada: posição na tela define a ordem; o atraso recomeça a cada lote
  function lote(itens) {
    itens.sort(function (a, b) { return Math.abs(a.r.top - b.r.top) > 12 ? a.r.top - b.r.top : a.r.left - b.r.left; });
    itens.forEach(function (x, k) { x.el.style.setProperty('--i', Math.min(k, 8)); revela(x.el); });
  }
  function scan(raiz) {
    raiz = raiz || document;
    heroPalavras(raiz);
    progressoCarrossel(raiz);
    if (calmo) { $$('[data-contar]', raiz).forEach(function (n) { n.textContent = n.dataset.contar; }); return; }
    if (!io && 'IntersectionObserver' in window) {
      io = new IntersectionObserver(function (es) {
        lote(es.filter(function (e) { return e.isIntersecting; }).map(function (e) { return { el: e.target, r: e.boundingClientRect }; }));
      }, { rootMargin: '0px 0px -8% 0px', threshold: .08 });
    }
    var altura = window.innerHeight, novos = [], naTela = [];
    ALVOS.forEach(function (par) {
      $$(par[0], raiz).forEach(function (el) {
        if (el.classList.contains('rv')) return;
        el.classList.add('rv'); if (par[1]) el.classList.add(par[1]);
        novos.push(el);
      });
    });
    // mede tudo de uma vez (uma única leitura de layout) e separa o que já está na tela
    novos.map(function (el) { return { el: el, r: el.getBoundingClientRect() }; }).forEach(function (x) {
      if (x.r.top < altura * .92 && x.r.bottom > 0) naTela.push(x);
      else if (io) io.observe(x.el);
      else revela(x.el);
    });
    if (naTela.length) requestAnimationFrame(function () { requestAnimationFrame(function () { lote(naTela); }); });
    // garantia: nada fica invisível se o observador não disparar
    clearTimeout(scan._t);
    scan._t = setTimeout(function () {
      lote($$('.rv:not(.rv-in)').map(function (el) { return { el: el, r: el.getBoundingClientRect() }; }).filter(function (x) { return x.r.top < window.innerHeight && x.r.bottom > 0; }));
    }, 1800);
  }

  /* ---------- banner: título palavra por palavra ---------- */
  function heroPalavras(raiz) {
    $$('.hero h1', raiz).forEach(function (h) {
      if (h.dataset.partido) return; h.dataset.partido = '1';
      var i = 0;
      (function parte(no) {
        Array.prototype.slice.call(no.childNodes).forEach(function (n) {
          if (n.nodeType === 3) {
            var frag = document.createDocumentFragment();
            n.textContent.split(/(\s+)/).forEach(function (w) {
              if (!w) return;
              if (/^\s+$/.test(w)) { frag.appendChild(document.createTextNode(' ')); return; }
              var a = document.createElement('span'); a.className = 'w';
              var b = document.createElement('span'); b.textContent = w; b.style.setProperty('--i', i++);
              a.appendChild(b); frag.appendChild(a);
            });
            no.replaceChild(frag, n);
          } else if (n.nodeType === 1) parte(n);
        });
      })(h);
    });
  }
  function heroPlay() {
    $$('.hero').forEach(function (h) {
      if (!h.querySelector('.hero-beam')) { var b = document.createElement('div'); b.className = 'hero-beam'; b.setAttribute('aria-hidden', 'true'); h.insertBefore(b, h.firstChild); }
      if (!h.querySelector('.hero-vento')) { var v = document.createElement('div'); v.className = 'hero-vento'; v.setAttribute('aria-hidden', 'true'); v.innerHTML = '<i></i><i></i><i></i><i></i><i></i>'; h.insertBefore(v, h.firstChild); }
      requestAnimationFrame(function () { h.classList.add('play'); });
    });
  }

  /* ---------- números que contam ---------- */
  function contar(raiz) {
    var lista = raiz.matches && raiz.matches('[data-contar]') ? [raiz] : $$('[data-contar]', raiz);
    lista.forEach(function (n) {
      if (n.dataset.contou) return; n.dataset.contou = '1';
      var fim = parseFloat(n.dataset.contar) || 0, ini = performance.now(), dur = 1200;
      (function passo(t) {
        var k = Math.min(1, (t - ini) / dur), e = 1 - Math.pow(1 - k, 3);
        n.textContent = Math.round(fim * e).toLocaleString('pt-BR') + (n.dataset.sufixo || '');
        if (k < 1) requestAnimationFrame(passo);
      })(ini);
    });
  }

  /* ---------- barra de progresso dos carrosséis ---------- */
  function progressoCarrossel(raiz) {
    $$('.grade.carrossel', raiz).forEach(function (g) {
      if (g.nextElementSibling && g.nextElementSibling.classList.contains('carrossel-prog')) return;
      var p = document.createElement('div'); p.className = 'carrossel-prog'; p.innerHTML = '<i></i>';
      g.parentNode.insertBefore(p, g.nextSibling);
      var bar = p.firstChild;
      function at() {
        var max = g.scrollWidth - g.clientWidth, vis = g.clientWidth / Math.max(g.scrollWidth, 1);
        bar.style.width = (vis * 100) + '%';
        bar.style.transform = 'translateX(' + (max > 0 ? (g.scrollLeft / max) * ((1 - vis) / vis) * 100 : 0) + '%)';
      }
      g.addEventListener('scroll', at, { passive: true }); at();
    });
  }

  /* ---------- paralaxe e cabeçalho ---------- */
  var ultimoY = window.scrollY, tic = false;
  function rolagem() {
    var y = window.scrollY;
    $$('.hero .hero-moto').forEach(function (m) { var h = m.closest('.hero'); if (y < h.offsetHeight + 200) m.style.translate = '0 ' + (y * .18) + 'px'; });
    $$('.hero .sl-scene').forEach(function (s) { s.style.translate = '0 ' + (y * .08) + 'px'; });
    var hdr = document.getElementById('topo');
    if (hdr && window.innerWidth <= 720) {
      var gaveta = $$('.gaveta').some(function (g) { return !g.hidden; });
      if (!gaveta) hdr.classList.toggle('oculto', y > 160 && y > ultimoY + 2);
      if (y < ultimoY - 2 || y < 160) hdr.classList.remove('oculto');
    }
    ultimoY = y; tic = false;
  }
  if (!calmo) window.addEventListener('scroll', function () { if (!tic) { tic = true; requestAnimationFrame(rolagem); } }, { passive: true });

  /* ---------- brilho que segue o dedo/mouse nos cards ---------- */
  var brilho = null;
  document.addEventListener('pointermove', function (e) {
    if (e.pointerType !== 'mouse') return;
    var c = e.target.closest && e.target.closest('.card'); if (!c) return;
    var pend = !!brilho; brilho = { c: c, x: e.clientX, y: e.clientY }; if (pend) return;
    requestAnimationFrame(function () {
      var b = brilho; brilho = null; var r = b.c.getBoundingClientRect();
      b.c.style.setProperty('--mx', (b.x - r.left) + 'px'); b.c.style.setProperty('--my', (b.y - r.top) + 'px');
    });
  }, { passive: true });

  /* ---------- indicador deslizante (menus e filtros) ---------- */
  function indicador(cont, ativo) {
    if (!cont) return;
    var ind = cont.querySelector(':scope > .ind');
    if (!ind) { ind = document.createElement('span'); ind.className = 'ind'; ind.setAttribute('aria-hidden', 'true'); cont.appendChild(ind); }
    if (!ativo) { ind.style.opacity = 0; return; }
    ind.style.opacity = 1;
    ind.style.width = ativo.offsetWidth + 'px';
    ind.style.transform = 'translateX(' + ativo.offsetLeft + 'px)';
    if (cont.scrollWidth > cont.clientWidth) {
      var alvo = ativo.offsetLeft - (cont.clientWidth - ativo.offsetWidth) / 2;
      cont.scrollTo({ left: alvo, behavior: calmo ? 'auto' : 'smooth' });
    }
  }

  /* ---------- transição entre páginas ---------- */
  function barra() {
    var b = document.querySelector('.vt-barra');
    if (!b) { b = document.createElement('div'); b.className = 'vt-barra'; b.setAttribute('aria-hidden', 'true'); document.body.appendChild(b); }
    b.classList.remove('vai'); void b.offsetWidth; b.classList.add('vai');
  }
  function transicao(fn) {
    barra();
    if (calmo || !document.startViewTransition) { fn(); var a = document.getElementById('app'); if (a && !calmo) { a.classList.remove('entra'); void a.offsetWidth; a.classList.add('entra'); } return; }
    if (document.hidden) { fn(); return; }
    var vt = document.startViewTransition(function () { fn(); });
    var ignora = function () {};
    if (vt.ready) vt.ready.catch(ignora);
    if (vt.finished) vt.finished.catch(ignora);
    if (vt.updateCallbackDone) vt.updateCallbackDone.catch(ignora);
  }
  // tema Shopify: navegação entre páginas com transição nativa do navegador (cross-document)
  window.addEventListener('pageswap', function () { document.documentElement.classList.add('saindo'); });

  /* ---------- gavetas com animação de saída ---------- */
  function fecharGaveta(g, depois) {
    if (!g || g.hidden) { if (depois) depois(); return; }
    if (calmo) { g.hidden = true; if (depois) depois(); return; }
    g.classList.add('fechando');
    var veu = document.getElementById('veu'); if (veu) veu.classList.add('fechando');
    setTimeout(function () {
      g.hidden = true; g.classList.remove('fechando');
      if (veu) veu.classList.remove('fechando');
      if (depois) depois();
    }, 260);
  }

  /* ---------- produto voando até o carrinho ---------- */
  function voar(origem) {
    if (calmo || !origem) return;
    var alvo = window.innerWidth <= 720 ? document.querySelector('.tabbar [data-tab="cart"], .tabbar [data-abrir="carrinho"]') : document.querySelector('.carrinho-btn');
    if (!alvo) return;
    var a = origem.getBoundingClientRect(), b = alvo.getBoundingClientRect();
    if (!a.width) return;
    var c = document.createElement('img');
    c.src = origem.currentSrc || origem.src; c.className = 'voando'; c.alt = '';
    var lado = Math.min(a.width, a.height, 220);
    c.style.cssText = 'left:' + (a.left + a.width / 2 - lado / 2) + 'px;top:' + (a.top + a.height / 2 - lado / 2) + 'px;width:' + lado + 'px;height:' + lado + 'px';
    document.body.appendChild(c);
    requestAnimationFrame(function () {
      var dx = b.left + b.width / 2 - (a.left + a.width / 2), dy = b.top + b.height / 2 - (a.top + a.height / 2);
      c.style.transform = 'translate(' + dx + 'px,' + dy + 'px) scale(' + (24 / lado) + ')';
      c.style.opacity = '.4'; c.style.borderRadius = '50%';
    });
    setTimeout(function () { c.remove(); alvo.classList.remove('pulo'); void alvo.offsetWidth; alvo.classList.add('pulo'); }, 760);
  }

  window.Cinema = { scan: scan, heroPlay: heroPlay, indicador: indicador, transicao: transicao, barra: barra, fecharGaveta: fecharGaveta, voar: voar, calmo: calmo };
})();
