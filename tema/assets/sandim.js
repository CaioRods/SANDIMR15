/* Sandim R15 · tema Shopify · CRdevs
   Loading, gavetas, carrinho AJAX (/cart/*.js), variações, galeria com arraste, barra de compra e filtros. */
(function () {
  'use strict';
  var S = window.Sandim || {};
  var COEF = parseFloat(S.coef12x) || 0.101326;
  var $ = function (s, el) { return (el || document).querySelector(s); };
  var $$ = function (s, el) { return Array.prototype.slice.call((el || document).querySelectorAll(s)); };
  var esc = function (s) { return String(s == null ? '' : s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); };
  var wait = function (ms) { return new Promise(function (r) { setTimeout(r, ms); }); };
  function brl(cents) {
    return (cents / 100).toLocaleString('pt-BR', { style: 'currency', currency: S.moeda || 'BRL' });
  }

  /* ---------- loading: entra, corre no centro até carregar, sai ---------- */
  (function loader() {
    var el = $('#sandim-loader');
    if (!el) return;
    try { if (sessionStorage.getItem('sandimLoader')) { el.remove(); return; } sessionStorage.setItem('sandimLoader', '1'); } catch (e) {}
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) { el.remove(); return; }
    var spd = function (n) { el.dataset.spd = n; };
    var carregou = new Promise(function (r) { if (document.readyState === 'complete') r(); else window.addEventListener('load', r); });
    el.style.setProperty('--sl-idle', '1400ms');
    el.classList.add('is-enter'); spd(3);
    setTimeout(function () { spd(2); }, 380); setTimeout(function () { spd(1); }, 640); setTimeout(function () { spd(0); }, 860);
    wait(1000).then(function () {
      el.classList.replace('is-enter', 'is-idle');
      return Promise.race([Promise.all([carregou, wait(1400)]), wait(6000)]);
    }).then(function () {
      el.classList.replace('is-idle', 'is-exit'); spd(1);
      setTimeout(function () { spd(2); }, 120); setTimeout(function () { spd(3); }, 280);
      return wait(800);
    }).then(function () {
      el.classList.add('is-done');
      setTimeout(function () { el.remove(); }, 500);
    });
  })();

  /* ---------- aviso ---------- */
  var tt;
  function toast(m) { var t = $('#toast'); if (!t) return; t.textContent = m; t.classList.add('on'); clearTimeout(tt); tt = setTimeout(function () { t.classList.remove('on'); }, 2600); }

  /* ---------- gavetas ---------- */
  function abrir(id) {
    fechar();
    var g = document.getElementById(id); if (!g) return;
    g.hidden = false; $('#veu').hidden = false; document.body.style.overflow = 'hidden';
    var f = $('[data-fechar]', g); if (f) f.focus();
  }
  function fechar() {
    $$('.gaveta').forEach(function (g) { g.hidden = true; });
    var v = $('#veu'); if (v) v.hidden = true;
    document.body.style.overflow = '';
  }
  document.addEventListener('click', function (e) {
    var a = e.target.closest('[data-abrir]');
    if (a) { if (a.dataset.abrir === 'carrinho') { abrirCarrinho(); } else { abrir(a.dataset.abrir); } return; }
    if (e.target.closest('[data-fechar]') || e.target.id === 'veu') { fechar(); return; }
    if (e.target.closest('[data-buscar]')) {
      fechar(); window.scrollTo({ top: 0, behavior: 'smooth' });
      setTimeout(function () { var q = $('#busca-q'); if (q) q.focus(); }, 250);
    }
  });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') fechar(); });

  /* ---------- cabeçalho que encolhe ---------- */
  var hdr = $('#topo'), checaBuy = null;
  function altHdr() { if (hdr) document.documentElement.style.setProperty('--hdr-h', hdr.offsetHeight + 'px'); }
  window.addEventListener('scroll', function () {
    if (hdr) hdr.classList.toggle('min', window.scrollY > 80);
    altHdr(); if (checaBuy) checaBuy();
  }, { passive: true });
  window.addEventListener('resize', altHdr); altHdr();

  /* ---------- carrinho (AJAX) ---------- */
  function contador(n) {
    $$('[data-qtd-carrinho]').forEach(function (b) { b.textContent = n; b.hidden = !n; });
  }
  function pintaCarrinho(c) {
    contador(c.item_count);
    var lista = $('#carrinho-itens'), base = $('#carrinho-base');
    if (!lista) return;
    if (!c.item_count) {
      lista.innerHTML = '<p class="vazio">Seu carrinho está vazio.</p>';
      base.hidden = true; return;
    }
    lista.innerHTML = c.items.map(function (i, k) {
      var foto = i.image ? i.image + (i.image.indexOf('?') > -1 ? '&' : '?') + 'width=160' : '';
      return '<div class="item">' + (foto ? '<img src="' + esc(foto) + '" alt="" width="72" height="72" loading="lazy">' : '<span></span>') +
        '<div><a class="nm" href="' + esc(i.url) + '">' + esc(i.product_title) + '</a>' +
        (i.variant_title && !i.product_has_only_default_variant ? '<div class="vr">' + esc(i.variant_title) + '</div>' : '') +
        '<div class="qtd"><button type="button" data-linha="' + (k + 1) + '" data-q="' + (i.quantity - 1) + '" aria-label="Diminuir">−</button>' +
        '<input value="' + i.quantity + '" readonly aria-label="Quantidade"><button type="button" data-linha="' + (k + 1) + '" data-q="' + (i.quantity + 1) + '" aria-label="Aumentar">+</button></div>' +
        '<button type="button" class="rm" data-linha="' + (k + 1) + '" data-q="0">Remover</button></div>' +
        '<div class="pr">' + brl(i.final_line_price) + '</div></div>';
    }).join('');
    base.hidden = false;
    $('#carrinho-total').textContent = brl(c.total_price);
    $('#carrinho-parc').textContent = 'Frete grátis · ou 12x de ' + brl(Math.round(c.total_price * COEF));
  }
  function buscaCarrinho() {
    return fetch((S.rotas && S.rotas.cart || '/cart') + '.js', { headers: { Accept: 'application/json' } }).then(function (r) { return r.json(); });
  }
  function abrirCarrinho() { abrir('carrinho'); buscaCarrinho().then(pintaCarrinho).catch(function () {}); }
  document.addEventListener('click', function (e) {
    var b = e.target.closest('[data-linha]'); if (!b) return;
    b.disabled = true;
    fetch((S.rotas && S.rotas.change || '/cart/change') + '.js', {
      method: 'POST', headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
      body: JSON.stringify({ line: +b.dataset.linha, quantity: +b.dataset.q })
    }).then(function (r) { return r.json(); }).then(pintaCarrinho).catch(function () { toast('Não foi possível atualizar o carrinho. Tente de novo.'); });
  });
  document.addEventListener('submit', function (e) {
    var f = e.target;
    if (!f.matches('[data-carrinho-ajax]')) return;
    e.preventDefault();
    var botoes = $$('[data-comprar]'); botoes.forEach(function (x) { x.disabled = true; });
    fetch((S.rotas && S.rotas.add || '/cart/add') + '.js', { method: 'POST', headers: { Accept: 'application/json' }, body: new FormData(f) })
      .then(function (r) { return r.json().then(function (j) { if (!r.ok) throw j; return j; }); })
      .then(function () { return buscaCarrinho(); })
      .then(function (c) { pintaCarrinho(c); abrir('carrinho'); })
      .catch(function (err) { toast((err && (err.description || err.message)) || 'Não foi possível adicionar. Tente de novo.'); })
      .then(function () { botoes.forEach(function (x) { x.disabled = x.dataset.esgotado === '1'; }); });
  });

  /* ---------- produto ---------- */
  (function produto() {
    var raiz = $('[data-produto]'); if (!raiz) return;
    var dados = {}; try { dados = JSON.parse($('[data-produto-json]').textContent); } catch (e) { return; }
    var trilho = $('[data-trilho]'), form = $('#form-produto');

    function ativo(i) {
      $$('[data-minis] button').forEach(function (b, k) { b.classList.toggle('on', k === i); });
      $$('[data-pontos] i').forEach(function (b, k) { b.classList.toggle('on', k === i); });
    }
    function vaiPara(i) { if (trilho) { trilho.scrollTo({ left: i * trilho.clientWidth, behavior: 'smooth' }); ativo(i); } }
    if (trilho) trilho.addEventListener('scroll', function () { ativo(Math.round(trilho.scrollLeft / trilho.clientWidth)); }, { passive: true });
    raiz.addEventListener('click', function (e) {
      var f = e.target.closest('[data-f]'); if (f) vaiPara(+f.dataset.f);
      var q = e.target.closest('[data-qtd]');
      if (q) { var inp = $('[data-qtd-input]'); inp.value = Math.max(1, (parseInt(inp.value, 10) || 1) + +q.dataset.qtd); }
    });

    function selecionadas() { return $$('[data-opcao]').map(function (fs) { var r = $('input:checked', fs); return r ? r.value : null; }); }
    function atualiza() {
      var ops = selecionadas();
      var v = (dados.variants || []).find(function (x) { return x.options.every(function (o, k) { return o === ops[k]; }); });
      $$('[data-opcao]').forEach(function (fs, k) {
        $$('.var', fs).forEach(function (l) { var inp = $('input', l); l.classList.toggle('on', inp.checked); });
        var nome = $('[data-opcao-nome]', fs); if (nome) nome.textContent = ops[k] || '';
      });
      if (!v) { $$('[data-comprar]').forEach(function (b) { b.disabled = true; b.dataset.esgotado = '1'; b.textContent = 'Indisponível'; }); return; }
      $('[data-variante-id]').value = v.id;
      $$('[data-preco]').forEach(function (x) { x.textContent = brl(v.price); });
      $$('[data-parc]').forEach(function (x) { x.textContent = brl(Math.round(v.price * COEF)); });
      var de = $('[data-de]'), off = $('[data-off]');
      if (v.compare_at_price && v.compare_at_price > v.price) {
        de.hidden = false; de.textContent = brl(v.compare_at_price);
        var p = Math.round((1 - v.price / v.compare_at_price) * 100);
        off.hidden = p < 5; off.textContent = '−' + p + '%';
      } else { de.hidden = true; off.hidden = true; }
      $$('[data-comprar]').forEach(function (b) {
        b.disabled = !v.available; b.dataset.esgotado = v.available ? '' : '1';
        b.textContent = v.available ? (b.closest('[data-buybar]') ? 'Comprar' : 'Adicionar ao carrinho') : 'Esgotado';
      });
      if (v.featured_media) {
        var alvo = $$('[data-media-id]', trilho).findIndex(function (m) { return +m.dataset.mediaId === v.featured_media.id; });
        if (alvo > -1) vaiPara(alvo);
      }
      if (window.history.replaceState) { var u = new URL(window.location.href); u.searchParams.set('variant', v.id); window.history.replaceState({}, '', u.toString()); }
    }
    if (form) form.addEventListener('change', function (e) { if (e.target.name && e.target.name.indexOf('opcao-') === 0) atualiza(); });

    var bb = $('[data-buybar]'), comprar = $('#form-produto [data-comprar]');
    checaBuy = function () { if (bb && comprar) bb.classList.toggle('on', comprar.getBoundingClientRect().bottom < 120); };
  })();

  /* ---------- coleção: filtro por moto e ordenação ---------- */
  (function colecao() {
    var chips = $('[data-filtro-moto]'), lista = $('#lista');
    if (chips && lista) {
      chips.addEventListener('click', function (e) {
        var b = e.target.closest('[data-m]'); if (!b) return;
        $$('[data-m]', chips).forEach(function (x) { x.classList.toggle('on', x === b); });
        var m = b.dataset.m, vis = 0;
        $$('.card', lista).forEach(function (c) { var ok = !m || (' ' + c.dataset.moto + ' ').indexOf(' ' + m + ' ') > -1; c.hidden = !ok; if (ok) vis++; });
        var vazio = $('#lista-vazia'); if (vazio) vazio.hidden = vis > 0;
      });
    }
    var ord = $('[data-ordem]');
    if (ord) ord.addEventListener('change', function () { var u = new URL(window.location.href); u.searchParams.set('sort_by', ord.value); u.searchParams.delete('page'); window.location.href = u.toString(); });
  })();
})();
