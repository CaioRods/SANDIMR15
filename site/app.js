/* Sandim R15 Store — protótipo do site novo (SPA com rotas por hash).
   Dados: catalogo.json, gerado de products.json da loja atual (build/catalogo.py). */
(function () {
  'use strict';

  var COEF_12X = 0.101326;            // mesmo coeficiente que a loja usa hoje (459,90 -> 12x 46,60)
  var CATS = [
    { h: 'acessorios', n: 'R15', cls: 'r15', d: 'Tudo para a sua Yamaha R15' },
    { h: 'acessorios-r3', n: 'R3', d: 'Linha para Yamaha R3' },
    { h: 'suporte-sliders', n: 'Proteção', d: 'Sliders, protetores e crashbar' },
    { h: 'estetica', n: 'Estética', d: 'Carenagens, piscas, lanternas e retrovisores' },
    { h: 'escapamentos', n: 'Desempenho', d: 'Escapamentos e filtros' },
    { h: 'desempenho', n: 'Segurança', d: 'Travas, iluminação e acessórios de segurança' },
    { h: 'manutencao', n: 'Manutenção', d: 'Relação, pastilhas, limpeza e ferramentas' },
    { h: 'adesivos', n: 'Adesivos', d: 'Kits completos, frisos e proteção de tanque' },
    { h: 'vestuario', n: 'Vestuário', d: 'Camisetas, moletons e luvas' },
    { h: 'kits-com-desconto', n: 'Kits', d: 'Combinações com preço especial' }
  ];
  var PAGINAS = {
    'quem-somos': ['Quem somos', [
      'Meu nome é Victor, mais conhecido como Sandim. Sou apaixonado por motos e criador do canal SandimR15, o canal mais completo sobre a Yamaha R15 do Brasil.',
      'Desde o primeiro contato com essa máquina, percebi que faltava conteúdo específico e de qualidade sobre ela, então resolvi criar. Com o tempo, o canal virou referência, ajudando milhares de pessoas com dicas, análises, problemas técnicos e novidades.',
      'Faltava uma loja especializada, feita por quem realmente gosta da R15. Cada produto aqui foi escolhido com base na experiência de quem usa, testa e vive essa moto no dia a dia.',
      'Seja bem-vindo. Aqui você encontra mais que acessórios: confiança, qualidade e paixão por duas rodas.']],
    'rastreio': ['Rastrear pedido', ['O código de rastreio é enviado por e-mail depois da confirmação do pagamento. No site final, esta página abre o rastreio da Shopify com o número do pedido.']],
    'atendimento': ['Atendimento', ['SAC (Serviço de Atendimento ao Consumidor)']]
  };

  var D = null, porH = {};
  var app = document.getElementById('app');
  var $ = function (s, el) { return (el || document).querySelector(s); };
  var esc = function (s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); };
  var brl = function (v) { return 'R$ ' + v.toFixed(2).replace('.', ',').replace(/\B(?=(\d{3})+(?!\d),)/g, '.'); };
  var img = function (u, w) { return u ? u + '?width=' + w : ''; };
  var pct = function (p) { return p.de ? Math.round((1 - p.preco / p.de) * 100) : 0; };

  /* ---------- loading ---------- */
  var loader = document.getElementById('sandim-loader'), loaderAcabou = false;
  var loaderPronto = (function () {
    var visto = false;
    try { visto = !!sessionStorage.getItem('sandimLoader'); sessionStorage.setItem('sandimLoader', '1'); } catch (e) {}
    if (visto || matchMedia('(prefers-reduced-motion: reduce)').matches) { loader.remove(); loaderAcabou = true; return function () {}; }
    var wait = function (ms) { return new Promise(function (r) { setTimeout(r, ms); }); };
    var spd = function (n) { loader.dataset.spd = n; };
    var pronto, sinal = new Promise(function (r) { pronto = r; });
    loader.style.setProperty('--sl-idle', '1400ms');
    loader.classList.add('is-enter'); spd(3);
    setTimeout(function () { spd(2); }, 380); setTimeout(function () { spd(1); }, 640); setTimeout(function () { spd(0); }, 860);
    wait(1000).then(function () {
      loader.classList.replace('is-enter', 'is-idle');
      return Promise.race([Promise.all([sinal, wait(1400)]), wait(6000)]);
    }).then(function () {
      loader.classList.replace('is-idle', 'is-exit'); spd(1);
      setTimeout(function () { spd(2); }, 120); setTimeout(function () { spd(3); }, 280);
      return wait(800);
    }).then(function () {
      loader.classList.add('is-done'); loaderAcabou = true; if (window.Cinema) Cinema.heroPlay();
      setTimeout(function () { loader.remove(); }, 500);
    });
    return pronto;
  })();

  /* ---------- carrinho ---------- */
  var cart = [];
  try { cart = JSON.parse(localStorage.getItem('sandimCarrinho') || '[]'); } catch (e) {}
  function salvar() { try { localStorage.setItem('sandimCarrinho', JSON.stringify(cart)); } catch (e) {} contador(); }
  function contador() {
    var n = cart.reduce(function (s, i) { return s + i.q; }, 0);
    ['#qtd-carrinho', '#qtd-tab'].forEach(function (sel) { var b = $(sel); if (b) { b.textContent = n; b.hidden = !n; } });
  }
  function adicionar(p, v, q, origem) {
    if (origem) Cinema.voar(origem);
    var id = p.h + '|' + v.t, it = cart.find(function (i) { return i.id === id; });
    if (it) it.q += q; else cart.push({ id: id, h: p.h, t: p.t, v: v.t, p: v.p, img: v.img || p.img[0], q: q });
    salvar(); setTimeout(abrirCarrinho, origem && !Cinema.calmo ? 650 : 0);
  }
  /* ---------- card: a foto sobe, gira e pousa na galeria do produto ---------- */
  var pularTransicao = false, vooAtivo = false, aposDesenhar = null;
  // termina a animação pelo evento ou pelo tempo (se a aba estiver em segundo plano o evento não chega)
  function aoAcabar(anim, ms, fn) { var feito = false; var vai = function () { if (feito) return; feito = true; fn(); }; anim.onfinish = vai; setTimeout(vai, ms + 120); }
  function abrirCard(c, href) {
    if (vooAtivo) return;
    var ft = c.querySelector('.ft'), foto = c.querySelector('.ft img');
    if (Cinema.calmo || !ft || !foto || !ft.animate) { location.hash = href; return; }
    vooAtivo = true;
    var r = ft.getBoundingClientRect();
    var voo = document.createElement('div');
    voo.className = 'card-voo';
    voo.innerHTML = '<img src="' + (foto.currentSrc || foto.src) + '" alt="">';
    voo.style.cssText = 'left:' + r.left + 'px;top:' + r.top + 'px;width:' + r.width + 'px;height:' + r.height + 'px';
    document.body.appendChild(voo);
    c.classList.add('saindo');
    var P = 'perspective(2200px) ';
    var sobe = voo.animate([
      { transform: P + 'translate3d(0,0,0) rotateY(0deg) scale(1)', boxShadow: '0 10px 24px rgba(15,23,42,.10)' },
      { transform: P + 'translate3d(0,-12px,0) rotateY(0deg) scale(1.05)', boxShadow: '0 30px 60px rgba(15,23,42,.20)' }
    ], { duration: 260, easing: 'cubic-bezier(.2,.8,.2,1)', fill: 'forwards' });
    aoAcabar(sobe, 260, function () {
      document.body.classList.add('chegando');
      aposDesenhar = function () {
        var alvo = document.querySelector('.galeria .principal');
        var t = alvo ? alvo.getBoundingClientRect() : { left: 0, top: 80, width: window.innerWidth, height: window.innerWidth };
        var dx = (t.left + t.width / 2) - (r.left + r.width / 2);
        var dy = (t.top + t.height / 2) - (r.top + r.height / 2);
        var esc = t.width / r.width;
        var raio = alvo ? getComputedStyle(alvo).borderRadius : '0px';
        var dur = window.innerWidth <= 720 ? 760 : 880;
        var voa = voo.animate([
          { transform: P + 'translate3d(0,-12px,0) rotateY(0deg) scale(1.05)', borderRadius: '18px', boxShadow: '0 30px 60px rgba(15,23,42,.20)' },
          { offset: .55, transform: P + 'translate3d(' + dx * .62 + 'px,' + (dy * .62 - 30) + 'px,0) rotateY(250deg) scale(' + (1 + (esc - 1) * .6) + ')', boxShadow: '0 40px 80px rgba(15,23,42,.22)' },
          { transform: P + 'translate3d(' + dx + 'px,' + dy + 'px,0) rotateY(360deg) scale(' + esc + ')', borderRadius: (parseFloat(raio) / esc) + 'px', boxShadow: '0 0 0 rgba(15,23,42,0)' }
        ], { duration: dur, easing: 'cubic-bezier(.45,0,.2,1)', fill: 'forwards' });
        aoAcabar(voa, dur, function () {
          document.body.classList.remove('chegando');
          var some = voo.animate([{ opacity: 1 }, { opacity: 0 }], { duration: 220, easing: 'ease-out', fill: 'forwards' });
          aoAcabar(some, 220, function () { voo.remove(); vooAtivo = false; });
        });
      };
      pularTransicao = true;
      if (location.hash === href) rota(); else location.hash = href;
    });
  }
  document.addEventListener('click', function (e) {
    var a = e.target.closest('#cats a, .catalogo-nav a.cn');
    if (!a || e.metaKey || e.ctrlKey) return;
    e.preventDefault();
    var href = a.getAttribute('href');
    if (a.closest('#cats')) {
      document.querySelectorAll('#cats a').forEach(function (x) { x.classList.toggle('on', x === a); });
      Cinema.indicador($('#cats'), a);
    } else {
      document.querySelectorAll('.catalogo-nav a.cn').forEach(function (x) { x.classList.toggle('on', x === a); });
    }
    a.classList.add('clicado');
    setTimeout(function () { a.classList.remove('clicado'); if (location.hash !== href) location.hash = href; }, Cinema.calmo ? 0 : 320);
  });
  app.addEventListener('click', function (e) {
    var c = e.target.closest('a.card');
    if (!c || e.metaKey || e.ctrlKey || e.shiftKey || e.button > 0) return;
    e.preventDefault();
    abrirCard(c, c.getAttribute('href'));
  });

  function abrirCarrinho() { renderCarrinho(); abrir('#carrinho'); }
  function renderCarrinho() {
    var el = $('#carrinho'), tot = cart.reduce(function (s, i) { return s + i.p * i.q; }, 0);
    el.innerHTML = '<div class="gav-topo"><h2>Seu carrinho</h2><button class="icon-btn" data-fechar aria-label="Fechar carrinho" type="button"><svg viewBox="0 0 24 24"><path d="M6 6l12 12M18 6 6 18"/></svg></button></div>' +
      '<div class="gav-corpo">' + (cart.length ? cart.map(function (i, k) {
        return '<div class="item"><img src="' + img(i.img, 160) + '" alt=""><div><div class="nm">' + esc(i.t) + '</div>' +
          (i.v !== 'Default Title' ? '<div class="vr">' + esc(i.v) + '</div>' : '') +
          '<div class="qtd"><button type="button" data-q="' + k + '" data-d="-1" aria-label="Diminuir">−</button><input value="' + i.q + '" readonly aria-label="Quantidade"><button type="button" data-q="' + k + '" data-d="1" aria-label="Aumentar">+</button></div></div>' +
          '<div class="pr">' + brl(i.p * i.q) + '</div></div>';
      }).join('') : '<p class="vazio">Seu carrinho está vazio.<br>Que tal começar pela <a href="#/c/acessorios" style="color:var(--azul)">linha R15</a>?</p>') + '</div>' +
      (cart.length ? '<div class="gav-base"><div class="tot"><span>Subtotal</span><b>' + brl(tot) + '</b></div><p class="mini">Frete grátis · ou 12x de ' + brl(tot * COEF_12X) + '</p>' +
        '<button class="btn cheio" type="button" id="finalizar">Finalizar compra</button></div>' : '');
  }
  document.addEventListener('click', function (e) {
    var rl = e.target.closest('[data-rolar]');
    if (rl) { var alvo = document.getElementById(rl.dataset.rolar); if (alvo) alvo.scrollIntoView({ behavior: 'smooth', block: 'start' }); return; }
    var q = e.target.closest('[data-q]');
    if (q) {
      var it = cart[+q.dataset.q]; it.q += +q.dataset.d;
      if (it.q < 1) cart.splice(+q.dataset.q, 1);
      salvar(); renderCarrinho(); return;
    }
    if (e.target.closest('#finalizar')) { toast('No site final, aqui vai para o checkout da Shopify.'); return; }
    if (e.target.closest('[data-fechar]') || e.target.id === 'veu') fechar();
    var link = e.target.closest('.gaveta a[href^="#/"]');
    if (link) { e.preventDefault(); link.classList.add('clicado'); setTimeout(function () { fechar(function () { location.hash = link.getAttribute('href'); }); }, Cinema.calmo ? 0 : 340); }
  });

  /* ---------- gavetas ---------- */
  function abrir(sel) {
    ['#carrinho', '#menu'].forEach(function (s) { if (s !== sel) $(s).hidden = true; });
    var g = $(sel); g.hidden = false; $('#veu').hidden = false; document.body.style.overflow = 'hidden';
    [].forEach.call(g.querySelectorAll('.gav-corpo > *'), function (el, i) { el.style.setProperty('--i', i); });
  }
  function fechar(depois) {
    var abertas = ['#carrinho', '#menu'].map(function (s) { return $(s); }).filter(function (g) { return !g.hidden; });
    if (!abertas.length) { $('#veu').hidden = true; document.body.style.overflow = ''; if (typeof depois === 'function') depois(); return; }
    abertas.forEach(function (g) { Cinema.fecharGaveta(g, function () { $('#veu').hidden = true; document.body.style.overflow = ''; if (typeof depois === 'function') depois(); }); });
  }
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') fechar(); });
  $('#abrir-carrinho').addEventListener('click', abrirCarrinho);
  function abrirMenu() {
    $('#menu').innerHTML = '<div class="gav-topo"><h2>Menu</h2><button class="icon-btn" data-fechar aria-label="Fechar menu" type="button"><svg viewBox="0 0 24 24"><path d="M6 6l12 12M18 6 6 18"/></svg></button></div><div class="gav-corpo">' +
      CATS.map(function (c) { return '<a href="#/c/' + c.h + '">' + c.n + '<small>' + c.d + '</small></a>'; }).join('') +
      '<a href="#/pagina/quem-somos">Quem somos<small>A loja do canal SandimR15</small></a></div>';
    abrir('#menu');
  }
  $('#abrir-menu').addEventListener('click', abrirMenu);
  $('#tab-cats').addEventListener('click', abrirMenu);
  $('#tab-cart').addEventListener('click', abrirCarrinho);
  function alternaBusca(abrirSempre) {
    var h = $('#topo'), aberta = abrirSempre || !h.classList.contains('busca-aberta');
    h.classList.toggle('busca-aberta', aberta); h.classList.remove('oculto');
    $('#abrir-busca').setAttribute('aria-expanded', aberta);
    if (aberta) setTimeout(function () { $('#busca-q').focus(); }, 60);
  }
  $('#abrir-busca').addEventListener('click', function () { alternaBusca(false); });
  $('#tab-busca').addEventListener('click', function () { fechar(); window.scrollTo({ top: 0, behavior: 'smooth' }); alternaBusca(true); });
  var hdr = $('#topo');
  function altHdr() { document.documentElement.style.setProperty('--hdr-h', hdr.offsetHeight + 'px'); }
  var checaBuy = null;
  window.addEventListener('scroll', function () { hdr.classList.toggle('min', window.scrollY > 80); altHdr(); if (checaBuy) checaBuy(); }, { passive: true });
  window.addEventListener('resize', altHdr); altHdr();
  var tt;
  function toast(m) { var t = $('#toast'); t.textContent = m; t.classList.add('on'); clearTimeout(tt); tt = setTimeout(function () { t.classList.remove('on'); }, 2600); }

  /* ---------- componentes ---------- */
  function classeMoto(p) {
    var r15 = p.moto.indexOf('R15') > -1, r3 = p.moto.indexOf('R3') > -1;
    return r15 && r3 ? ' m-ambos' : r15 ? ' m-r15' : r3 ? ' m-r3' : ' m-outra';
  }
  function card(p) {
    return '<a class="card' + classeMoto(p) + (p.ok ? '' : ' esgotado') + '" href="#/p/' + p.h + '"><div class="ft"><img loading="lazy" src="' + img(p.img[0], 500) + '" alt="' + esc(p.t) + '">' +
      (p.img[1] && p.ok ? '<img class="alt" loading="lazy" src="' + img(p.img[1], 500) + '" alt="">' : '') +
      '<div class="tags">' + p.moto.map(function (m) { return '<span class="selo ' + m + '">' + (m === 'SBM' ? 'SBM 250s' : m) + '</span>'; }).join('') + '</div>' +
      (p.ok ? '' : '<span class="sem-estoque">Sem estoque</span>') + '</div>' +
      '<div class="info">' + (p.anos ? '<span class="ano">' + p.anos + '</span>' : '') + '<span class="nome">' + esc(p.t) + '</span>' +
      '<span class="preco">' + (p.varia ? '<small>a partir de </small>' : '') + brl(p.preco) + '</span>' +
      '<span class="parc">' + (p.ok ? '12x de ' + brl(p.preco * COEF_12X) : 'Avise-me quando chegar') + '</span></div></a>';
  }
  function daColecao(h) {
    return D.produtos.filter(function (p) { return h in p.col; }).sort(function (a, b) { return a.col[h] - b.col[h]; });
  }
  function vitrine(tit, sub, h, n, lista, car) {
    lista = (lista || daColecao(h)).slice(0, n);
    return '<section class="secao"><div class="wrap"><div class="sec-head"><div><h2>' + tit + '</h2>' + (sub ? '<p>' + sub + '</p>' : '') + '</div>' +
      (h ? '<a class="ver-todos" href="#/c/' + h + '">Ver todos</a>' : '') + '</div><div class="grade' + (car ? ' carrossel' : '') + '">' + lista.map(card).join('') + '</div></div></section>';
  }
  function letreiro() {
    var itens = ['<span class="az">R15</span>', '<span class="pt">/</span>', '<span>R3</span>', '<span class="pt">/</span>', '<span>Frete grátis</span>', '<span class="pt">/</span>', '<span class="az">12x no cartão</span>', '<span class="pt">/</span>', '<span>Testado no canal</span>', '<span class="pt">/</span>'].join('');
    return '<div class="letreiro" aria-hidden="true"><div class="letreiro-in">' + itens + itens + itens + itens + '</div></div>';
  }
  var cena = '<div class="sl-scene"><i class="sl-mt1"></i><i class="sl-mt2"></i><i class="sl-arv"></i></div>';
  var motoSvg = function (k, b) { return '<svg viewBox="570 18 1050 425" aria-hidden="true"><use href="#lg-moto" x="570" y="18" width="1050" height="425" style="--k:' + k + ';--b:' + b + '"/></svg>'; };

  /* ---------- páginas ---------- */
  function home() {
    var maisVend = daColecao('mais-vendidos');
    var conta = function (m) { return D.produtos.filter(function (p) { return p.moto.indexOf(m) > -1; }).length; };
    var moto = $('#moto-completa') ? $('#moto-completa').innerHTML : motoSvg('url(#sg-branco)', 'url(#sg-azulc)');
    var dest = daColecao('escapamentos')[0] || maisVend[0];
    var tamanhos = ['g', '', '', '', '', 'l', '', ''];
    var mosaico = CATS.slice(2).map(function (c, k) {
      var ps = daColecao(c.h); if (!ps.length) return '';
      return '<a class="mos ' + (tamanhos[k] || '') + '" href="#/c/' + c.h + '"><span class="ft"><img loading="lazy" src="' + img(ps[0].img[0], 500) + '" alt=""></span><b>' + c.n + '</b><small>' + ps.length + ' peças</small></a>';
    }).join('');
    var icone = {
      frete: '<svg viewBox="0 0 24 24"><path d="M3 7h11v9H3zM14 10h4l3 3v3h-7z"/><circle cx="7" cy="17.5" r="1.8"/><circle cx="17" cy="17.5" r="1.8"/></svg>',
      cartao: '<svg viewBox="0 0 24 24"><rect x="3" y="6" width="18" height="12" rx="2"/><path d="M3 10h18"/></svg>',
      escudo: '<svg viewBox="0 0 24 24"><path d="M12 3l8 3v6c0 4.5-3.4 8-8 9-4.6-1-8-4.5-8-9V6z"/><path d="m9 12 2 2 4-4"/></svg>'
    };
    return '<section class="hero">' + cena +
      '<div class="hero-in"><div class="hero-txt">' +
        '<span class="kicker eyebrow">Loja oficial do canal SandimR15</span>' +
        '<h1>Feito por quem <em>vive a R15.</em></h1>' +
        '<p class="lead">Acessórios para Yamaha R15 e R3, escolhidos por quem pilota todo dia.</p>' +
        '<div class="ctas"><a class="btn" href="#/c/acessorios">Ver peças da R15</a><a class="btn vidro" href="#/c/acessorios-r3">Linha R3</a></div>' +
      '</div><div class="hero-palco"><span class="hero-gigante" aria-hidden="true">R15</span><div class="hero-moto moto-parada">' + moto + '</div><div class="hero-chao"></div></div></div>' +
      '<button class="hero-scroll" type="button" data-rolar="maquinas"><i></i>Role</button></section>' +

      '<section class="secao" id="maquinas"><div class="wrap"><div class="sec-head"><div><span class="kicker">Comece por aqui</span><h2>Escolha sua máquina</h2></div></div>' +
      '<div class="maquinas">' +
        '<a class="maq r15" href="#/c/acessorios"><span class="num">R15</span><span class="moto-bg moto-parada">' + moto + '</span><div class="rod"><p><b>Linha R15</b>' + conta('R15') + ' acessórios para todos os anos</p><span class="seta" aria-hidden="true">→</span></div></a>' +
        '<a class="maq" href="#/c/acessorios-r3"><span class="num">R3</span><span class="moto-bg moto-parada">' + moto + '</span><div class="rod"><p><b>Linha R3</b>' + conta('R3') + ' acessórios</p><span class="seta" aria-hidden="true">→</span></div></a>' +
        '<p class="maq-outras">Tem uma SBM 250s? <a href="#/c/sbm-250s">Ver acessórios</a></p>' +
      '</div></div></section>' +

      vitrine('Mais vendidos', '', 'mais-vendidos', 8, maisVend, true) +

      (dest ? '<section class="secao"><div class="wrap destaque">' +
        '<a class="palco" href="#/p/' + dest.h + '"><span class="tag-canal">Usado no canal</span><img src="' + img(dest.img[0], 900) + '" alt="' + esc(dest.t) + '" loading="lazy"></a>' +
        '<div><span class="kicker">Destaque da garagem</span><h2>' + esc(dest.t) + '</h2>' +
        '<div class="preco-g">' + brl(dest.preco) + '<small>ou 12x de ' + brl(dest.preco * COEF_12X) + ' no cartão</small></div>' +
        '<ul><li>Compatível com Yamaha ' + dest.moto.join(' e ') + '</li><li>Frete grátis para todo o Brasil</li><li>Escolhido por quem pilota a R15 no canal</li></ul>' +
        '<div class="ctas"><a class="btn" href="#/p/' + dest.h + '">Ver produto</a><a class="btn vidro" href="#/c/escapamentos">Mais desempenho</a></div></div>' +
      '</div></section>' : '') +

      '<section class="secao"><div class="wrap"><div class="sec-head"><div><span class="kicker">Catálogo</span><h2>Monte a sua do seu jeito</h2></div></div><div class="mosaico">' + mosaico + '</div></div></section>' +

      '<section class="canal"><div class="wrap canal-in"><span class="kicker">Do canal para a sua garagem</span>' +
        '<h2>Quem vende, <em>pilota.</em></h2>' +
        '<p>O canal SandimR15 virou referência em dicas, análises e solução de problemas da R15. A loja nasceu dali: cada peça foi escolhida por quem anda com a moto todo dia.</p>' +
        '<div class="selos-canal"><span>Escolhido por quem usa</span><span>Frete grátis para todo o Brasil</span><span>Até 12x no cartão</span></div>' +
        '<a class="btn vidro" href="#/pagina/quem-somos">Conheça a história</a></div></section>' +

      vitrine('Lançamentos', '', 'news', 8, null, true) +

      '<section class="secao" style="padding-top:0"><div class="wrap garantia-faixa">' +
        '<div>' + icone.frete + '<p style="margin:0"><b>Frete grátis</b><span>Para todo o Brasil, com rastreio</span></p></div>' +
        '<div>' + icone.cartao + '<p style="margin:0"><b>Até 12x</b><span>No cartão de crédito</span></p></div>' +
        '<div>' + icone.escudo + '<p style="margin:0"><b>Compra segura</b><span>Checkout da Shopify</span></p></div>' +
      '</div></section>';
  }

  function colecao(h, q) {
    var c = CATS.find(function (x) { return x.h === h; }) || { n: D.colecoes[h] || 'Produtos', d: '' };
    var base = h === 'busca' ? D.produtos.filter(function (p) { var t = (p.t + ' ' + p.orig).toLowerCase(); return q.toLowerCase().split(/\s+/).every(function (w) { return t.indexOf(w) > -1; }); }) : daColecao(h);
    var tit = h === 'busca' ? 'Busca: “' + esc(q) + '”' : (h === 'acessorios' ? 'Linha R15' : h === 'acessorios-r3' ? 'Linha R3' : esc(c.n));
    var fundo = base[0] ? img(base[0].img[0], 600) : '';
    var nav = h === 'busca' ? '' : '<nav class="catalogo-nav" aria-label="Outras categorias">' + CATS.map(function (k) {
      var ps = daColecao(k.h), foto = ps[0] ? img(ps[0].img[0], 160) : '', moto = k.h === 'acessorios' || k.h === 'acessorios-r3';
      return '<a class="cn' + (moto ? ' moto' : '') + (k.h === h ? ' on' : '') + '" href="#/c/' + k.h + '"' + (k.h === h ? ' aria-current="page"' : '') + '><span class="bola">' + (moto ? '<b>' + k.n + '</b>' : '<img src="' + foto + '" alt="" loading="lazy">') + '</span><span>' + (moto ? 'Linha ' + k.n : k.n) + '</span></a>';
    }).join('') + '</nav>';
    app.innerHTML = '<section class="col-topo">' + (fundo ? '<div class="fundo" style="background-image:url(' + fundo + ')"></div>' : '') + '<div class="wrap"><div class="migalha"><a href="#/">Início</a> / ' + tit + '</div><div class="col-tit"><h1>' + tit + '</h1><span class="qtd-badge">' + base.length + ' produtos</span></div><p>' + (c.d || '') + '</p></div></section>' +
      '<div class="wrap">' + nav + '<div class="filtros"><div class="seg" id="chips" role="group" aria-label="Filtrar por moto">' +
      ['Todas', 'R15', 'R3'].map(function (m, i) { return '<button type="button" class="' + (i ? '' : 'on') + '" data-m="' + m + '" aria-pressed="' + (i ? 'false' : 'true') + '">' + (i ? m : 'Todas') + '</button>'; }).join('') +
      '</div><label class="ordem" for="ordem"><span class="sr">Ordenar</span><select id="ordem"><option value="rel">Mais vendidos</option><option value="menor">Menor preço</option><option value="maior">Maior preço</option><option value="novo">Mais recentes</option></select></label></div>' +
      '<div class="res-cont" id="res-cont"></div><div class="grade" id="lista"></div><div style="height:56px"></div></div>';
    var moto = 'Todas', ord = 'rel';
    function pinta(animar) {
      var l = base.filter(function (p) { return moto === 'Todas' || p.moto.indexOf(moto) > -1; }).slice();
      if (ord === 'menor') l.sort(function (a, b) { return a.preco - b.preco; });
      if (ord === 'maior') l.sort(function (a, b) { return b.preco - a.preco; });
      if (ord === 'novo') l.sort(function (a, b) { return a.data < b.data ? 1 : -1; });
      var g = $('#lista');
      g.innerHTML = l.length ? l.map(card).join('') : '<p class="vazio" style="grid-column:1/-1">Nenhum produto encontrado. Tente outra palavra ou veja a <a href="#/c/acessorios" style="color:var(--azul)">linha R15</a>.</p>';
      $('#res-cont').textContent = l.length + (l.length === 1 ? ' produto' : ' produtos') + (moto === 'Todas' ? '' : ' para ' + moto);
      if (animar) {
        [].forEach.call(g.children, function (el, i) { el.style.setProperty('--i', Math.min(i, 12)); });
        g.classList.remove('trocando'); void g.offsetWidth; g.classList.add('trocando');
      } else Cinema.scan(g.parentNode);
    }
    $('#chips').addEventListener('click', function (e) {
      var b = e.target.closest('[data-m]'); if (!b) return;
      moto = b.dataset.m;
      [].forEach.call($('#chips').querySelectorAll('[data-m]'), function (x) { x.classList.toggle('on', x === b); x.setAttribute('aria-pressed', x === b); });
      Cinema.indicador($('#chips'), b); pinta(true);
    });
    $('#ordem').addEventListener('change', function (e) { ord = e.target.value; pinta(true); });
    pinta(false);
    requestAnimationFrame(function () { Cinema.indicador($('#chips'), $('#chips .on')); var cn = $('.catalogo-nav .on'); if (cn) cn.scrollIntoView({ inline: 'center', block: 'nearest' }); });
  }

  function produto(h) {
    var p = porH[h];
    if (!p) { app.innerHTML = '<div class="wrap pagina"><h1>Produto não encontrado</h1><p><a href="#/" style="color:var(--azul)">Voltar para a loja</a></p></div>'; return; }
    var v = p.v.find(function (x) { return x.ok; }) || p.v[0], qtd = 1, fotos = p.img.slice();
    var temOpcao = p.op.length && p.v.length > 1;
    var rel = D.produtos.filter(function (x) { return x !== p && x.moto.some(function (m) { return p.moto.indexOf(m) > -1; }) && Object.keys(x.col).some(function (c) { return c in p.col && ['mais-vendidos', 'news', 'ofertas-da-semana', 'acessorios'].indexOf(c) < 0; }); }).slice(0, 8);
    app.innerHTML = '<div class="wrap"><div class="migalha" style="color:var(--apoio);padding-top:20px"><a href="#/">Início</a> / <a href="#/c/' + (p.moto[0] === 'R3' ? 'acessorios-r3' : 'acessorios') + '">Linha ' + p.moto[0] + '</a> / ' + esc(p.t) + '</div>' +
      '<div class="prod"><div class="galeria"><div class="miniaturas" id="minis"></div><div class="principal"><span class="foto-cont" id="foto-cont"></span><div class="trilho" id="trilho"></div><div class="pontos" id="pontos"></div></div></div>' +
      '<div class="compra"><div class="selos">' + p.moto.map(function (m) { return '<span class="selo ' + m + '">' + (m === 'SBM' ? 'SBM 250s' : 'Yamaha ' + m) + '</span>'; }).join('') + '<small>Compatibilidade</small></div>' +
      '<h1>' + esc(p.t) + '</h1>' + (p.anos ? '<p class="ano-destaque">Serve nos anos <b>' + p.anos + '</b></p>' : '') + '<div class="precos" id="precos"></div>' +
      (temOpcao ? '<div class="opcao"><h3>' + esc(p.op[0]) + ': <b id="vnome"></b></h3><div class="variantes" id="vars"></div></div>' : '') +
      '<div class="linha-compra"><div class="qtd"><button type="button" id="menos" aria-label="Diminuir">−</button><input id="qtd" value="1" readonly aria-label="Quantidade"><button type="button" id="mais" aria-label="Aumentar">+</button></div>' +
      '<button class="btn" style="flex:1" type="button" id="comprar">Adicionar ao carrinho</button></div>' +
      '<p class="garantia-linha"><svg viewBox="0 0 24 24"><path d="M3 7h11v9H3zM14 10h4l3 3v3h-7z"/><circle cx="7" cy="17.5" r="1.8"/><circle cx="17" cy="17.5" r="1.8"/></svg>Frete grátis para todo o Brasil · compra segura</p>' +
      (p.desc ? '<details class="acc"' + (window.innerWidth > 720 ? ' open' : '') + '><summary>Sobre o produto</summary><div class="desc">' + esc(p.desc) + '</div></details>' : '') +
      '</div></div></div><div class="buybar" id="buybar"><div class="bb-txt"><b id="bb-preco"></b><small id="bb-parc"></small></div><button class="btn" type="button" id="comprar2">Comprar</button></div>' + (rel.length ? vitrine('Combina com', 'Mais peças para a sua ' + p.moto[0], null, 8, rel, true) : '');
    var montadas = '';
    function ativo(i) {
      [].forEach.call($('#minis').children, function (b, k) { b.classList.toggle('on', k === i); });
      [].forEach.call($('#pontos').children, function (b, k) { b.classList.toggle('on', k === i); });
      $('#foto-cont').textContent = (i + 1) + ' / ' + fotos.length; $('#foto-cont').hidden = fotos.length < 2;
    }
    function pintaFotos(i) {
      var t = $('#trilho');
      if (montadas !== fotos.join()) {
        montadas = fotos.join();
        t.innerHTML = fotos.map(function (f, k) { return '<img src="' + img(f, 900) + '" alt="' + esc(p.t) + ' — foto ' + (k + 1) + '"' + (k ? ' loading="lazy"' : '') + '>'; }).join('');
        $('#minis').innerHTML = fotos.map(function (f, k) { return '<button type="button" data-f="' + k + '" aria-label="Foto ' + (k + 1) + '"><img src="' + img(f, 160) + '" alt=""></button>'; }).join('');
        $('#pontos').innerHTML = fotos.length > 1 ? fotos.map(function () { return '<i></i>'; }).join('') : '';
        t.onscroll = function () { ativo(Math.round(t.scrollLeft / t.clientWidth)); };
      }
      t.scrollTo({ left: i * t.clientWidth, behavior: 'smooth' });
      ativo(i);
    }
    function pintaPreco() {
      var de = v.d && v.d > v.p ? v.d : null, o = de ? Math.round((1 - v.p / de) * 100) : 0;
      ['#comprar', '#comprar2'].forEach(function (id) { var b = $(id); if (b) { b.disabled = !v.ok; b.textContent = v.ok ? (id === '#comprar' ? 'Adicionar ao carrinho' : 'Comprar') : 'Sem estoque'; } });
      $('#bb-preco').textContent = brl(v.p); $('#bb-parc').textContent = 'ou 12x de ' + brl(v.p * COEF_12X);
      $('#precos').innerHTML = (de ? '<span class="de">' + brl(de) + '</span>' : '') + '<span class="preco">' + brl(v.p) + (o >= 5 ? '<span class="off">−' + o + '%</span>' : '') + '</span><span class="parc">ou 12x de ' + brl(v.p * COEF_12X) + ' no cartão</span>';
      if (temOpcao) {
        $('#vnome').textContent = v.t;
        $('#vars').innerHTML = p.v.map(function (x, k) { return '<button type="button" data-v="' + k + '" class="' + (x === v ? 'on' : '') + (x.ok ? '' : ' sem') + '"' + (x.ok ? '' : ' disabled') + '>' + (x.img ? '<img src="' + img(x.img, 100) + '" alt="">' : '') + '<span>' + esc(x.t) + (x.ok ? '' : '<small>sem estoque</small>') + '</span></button>'; }).join('');
      }
    }
    app.onclick = function (e) {
      var f = e.target.closest('[data-f]'); if (f) { pintaFotos(+f.dataset.f); return; }
      var b = e.target.closest('[data-v]');
      if (b) { v = p.v[+b.dataset.v]; if (v.img) { var k = fotos.indexOf(v.img); if (k < 0) { fotos.unshift(v.img); k = 0; } pintaFotos(k); } pintaPreco(); return; }
      if (e.target.closest('#menos')) { qtd = Math.max(1, qtd - 1); $('#qtd').value = qtd; }
      if (e.target.closest('#mais')) { qtd++; $('#qtd').value = qtd; }
      if (e.target.closest('#comprar') || e.target.closest('#comprar2')) {
        var t = $('#trilho'), atual = t ? t.children[Math.round(t.scrollLeft / Math.max(t.clientWidth, 1))] : null;
        adicionar(p, v, qtd, atual);
      }
    };
    pintaFotos(0); pintaPreco();
    checaBuy = function () {
      var b = $('#comprar'), bb = $('#buybar'); if (!b || !bb) return;
      var r = b.getBoundingClientRect(), topo = window.innerWidth <= 720 ? 70 : 120;
      bb.classList.toggle('on', r.bottom < topo || r.top > window.innerHeight - 140);
    };
    checaBuy();
  }

  var PG = {};
  var CONTATO = '<div class="contato-box"><b>Atendimento ao cliente</b><p>E-mail: <a href="mailto:sandimcomercial@gmail.com">sandimcomercial@gmail.com</a><br>WhatsApp: <a href="https://wa.me/5532991042903" target="_blank" rel="noopener">+55 (32) 9 9104-2903</a></p></div>';
  function pagina(id) {
    if (PG[id]) { app.innerHTML = '<div class="wrap pagina"><h1>' + esc(PG[id].titulo) + '</h1>' + PG[id].html + CONTATO + '</div>'; return; }
    var pg = PAGINAS[id] || ['Página', ['Conteúdo em construção.']];
    app.innerHTML = '<div class="wrap pagina"><h1>' + pg[0] + '</h1>' + pg[1].map(function (t) { return '<p>' + esc(t) + '</p>'; }).join('') + (id === 'quem-somos' ? '' : CONTATO) + '</div>';
  }

  /* ---------- rotas ---------- */
  var rotaAnterior = location.hash;
  function idxCat(hash) { var m = /^#\/c\/([^/]+)/.exec(hash || ''); if (!m) return -1; var k = CATS.findIndex(function (c) { return c.h === m[1]; }); return k < 0 ? 99 : k; }
  function rota() {
    var de = idxCat(rotaAnterior), para = idxCat(location.hash);
    rotaAnterior = location.hash;
    if (pularTransicao) { pularTransicao = false; desenha(); return; }
    if (de > -1 && para > -1 && !Cinema.calmo && app.animate) { trocaCatalogo(para >= de ? 1 : -1); return; }
    Cinema.transicao(desenha);
  }
  function trocaCatalogo(dir) {
    Cinema.barra();
    var sai = app.animate([{ opacity: 1, transform: 'translateX(0)' }, { opacity: 0, transform: 'translateX(' + (-dir * 48) + 'px)' }], { duration: 200, easing: 'cubic-bezier(.4,0,1,1)', fill: 'forwards' });
    aoAcabar(sai, 200, function () {
      var y = window.scrollY;
      desenha();
      var topo = $('.col-topo'); if (topo && y > topo.offsetHeight) window.scrollTo(0, topo.offsetHeight - 10);
      sai.cancel();
      app.animate([{ opacity: 0, transform: 'translateX(' + (dir * 56) + 'px)' }, { opacity: 1, transform: 'translateX(0)' }], { duration: 520, easing: 'cubic-bezier(.22,1,.36,1)' });
      var g = $('#lista');
      if (g) { [].forEach.call(g.children, function (el, k) { el.style.setProperty('--i', Math.min(k, 12)); }); g.classList.add('trocando'); }
    });
  }
  function desenha() {
    var r = location.hash.replace(/^#\/?/, '').split('/'), q = '';
    app.onclick = null; checaBuy = null;
    if (r[0] === 'busca') q = decodeURIComponent(r[1] || '');
    var ativo = null;
    document.querySelectorAll('#cats a').forEach(function (a) { var on = a.getAttribute('href') === '#/c/' + r[1] && r[0] === 'c'; a.classList.toggle('on', on); if (on) ativo = a; });
    Cinema.indicador($('#cats'), ativo);
    ['#carrinho', '#menu'].forEach(function (s) { $(s).hidden = true; }); $('#veu').hidden = true; document.body.style.overflow = '';
    $('#topo').classList.remove('oculto');
    if (r[0] === 'busca' && !q) { app.innerHTML = '<div class="wrap pagina"><h1>Pesquisar</h1><p>Digite o nome da peça na busca do topo.</p></div>'; $('#busca-q').focus(); return; }
    if (r[0] === 'c') colecao(r[1]);
    else if (r[0] === 'p') produto(r[1]);
    else if (r[0] === 'busca') colecao('busca', q);
    else if (r[0] === 'pagina') pagina(r[1]);
    else app.innerHTML = home();
    document.body.dataset.rota = r[0] || 'home';
    document.querySelectorAll('.tabbar [data-tab]').forEach(function (t) { t.classList.toggle('on', t.dataset.tab === 'home' && !r[0]); });
    window.scrollTo(0, 0);
    Cinema.scan(app);
    if (!r[0] && loaderAcabou) Cinema.heroPlay();
    var t = r[0] === 'p' && porH[r[1]] ? porH[r[1]].t + ' · ' : r[0] === 'c' ? ((CATS.find(function (c) { return c.h === r[1]; }) || {}).n || '') + ' · ' : '';
    document.title = t + 'Sandim R15 Store';
    if (aposDesenhar) { var f = aposDesenhar; aposDesenhar = null; setTimeout(f, 16); }
  }

  $('#busca').addEventListener('submit', function (e) {
    e.preventDefault();
    var q = $('#busca-q').value.trim(); if (q) { $('#topo').classList.remove('busca-aberta'); $('#busca-q').blur(); location.hash = '#/busca/' + encodeURIComponent(q); }
  });
  $('#cats').innerHTML = CATS.map(function (c) { return '<a href="#/c/' + c.h + '"' + (c.cls ? ' class="' + c.cls + '"' : '') + '>' + c.n + '</a>'; }).join('');
  contador();

  $('#newsletter').addEventListener('submit', function (e) {
    e.preventDefault(); $('#news-email').value = ''; toast('E-mail cadastrado. No site final, entra na lista da Shopify.');
  });
  fetch('paginas.json', { cache: 'no-cache' }).then(function (r) { return r.json(); }).then(function (p) { PG = p; if (location.hash.indexOf('#/pagina/') === 0) rota(); }).catch(function () {});
  fetch('catalogo.json', { cache: 'no-cache' }).then(function (r) { return r.json(); }).then(function (d) {
    D = d; d.produtos.forEach(function (p) { porH[p.h] = p; });
    window.addEventListener('hashchange', rota);
    desenha(); loaderPronto();
    window.addEventListener('resize', function () { Cinema.indicador($('#cats'), $('#cats a.on')); var ch = $('#chips'); if (ch) Cinema.indicador(ch, ch.querySelector('.on')); });
  }).catch(function () {
    app.innerHTML = '<div class="wrap pagina"><h1>Não foi possível carregar o catálogo</h1><p>Abra o site por um servidor local (python -m http.server) em vez de abrir o arquivo direto.</p></div>';
    loaderPronto();
  });
})();
