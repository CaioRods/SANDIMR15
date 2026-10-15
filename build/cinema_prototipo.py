"""Liga a camada cinematográfica (cinema.css/js) ao protótipo: loading em cartão, banner,
catálogo redesenhado, transições de página e gavetas animadas."""
import re

# ---------- template ----------
p = 'build/site.src.html'; s = open(p, encoding='utf8').read()
def troca_s(a, b):
    global s
    if b in s: return
    assert a in s, a[:60]; s = s.replace(a, b)
troca_s('<link rel="stylesheet" href="estilo.css">', '<link rel="stylesheet" href="estilo.css">\n<link rel="stylesheet" href="cinema.css">')
troca_s('#sandim-loader{position:fixed;inset:0;z-index:999;transition:opacity .45s ease,visibility 0s linear .45s}\n#sandim-loader.is-done{opacity:0;visibility:hidden}', '')
troca_s('<div class="sl-stage" id="sandim-loader" aria-hidden="true">', '<div class="sl-overlay" id="sandim-loader" aria-hidden="true"><div class="sl-stage">')
troca_s('<div class="sl-bar"><i></i></div></div>\n</div>', '<div class="sl-bar"><i></i></div></div>\n</div></div>')
troca_s('<script src="app.js"></script>', '<script src="cinema.js"></script>\n<script src="app.js"></script>')
open(p, 'w', encoding='utf8').write(s)

# ---------- app.js ----------
p = 'site/app.js'; a = open(p, encoding='utf8').read()
def troca(x, y):
    global a
    assert x in a, x[:70]; a = a.replace(x, y)

# loading: avisa quando terminou para o banner começar
troca("""    if (visto || matchMedia('(prefers-reduced-motion: reduce)').matches) { loader.remove(); return function () {}; }""",
      """    if (visto || matchMedia('(prefers-reduced-motion: reduce)').matches) { loader.remove(); loaderAcabou = true; return function () {}; }""")
troca("""      loader.classList.add('is-done');
      setTimeout(function () { loader.remove(); }, 500);""",
      """      loader.classList.add('is-done'); loaderAcabou = true; if (window.Cinema) Cinema.heroPlay();
      setTimeout(function () { loader.remove(); }, 500);""")
troca("""  var loader = document.getElementById('sandim-loader');""", """  var loader = document.getElementById('sandim-loader'), loaderAcabou = false;""")

# gavetas com saída animada e itens em sequência
troca("""  function abrir(sel) { fechar(); $(sel).hidden = false; $('#veu').hidden = false; document.body.style.overflow = 'hidden'; }
  function fechar() { ['#carrinho', '#menu'].forEach(function (s) { $(s).hidden = true; }); $('#veu').hidden = true; document.body.style.overflow = ''; }""",
"""  function abrir(sel) {
    ['#carrinho', '#menu'].forEach(function (s) { if (s !== sel) $(s).hidden = true; });
    var g = $(sel); g.hidden = false; $('#veu').hidden = false; document.body.style.overflow = 'hidden';
    [].forEach.call(g.querySelectorAll('.gav-corpo > *'), function (el, i) { el.style.setProperty('--i', i); });
  }
  function fechar(depois) {
    var abertas = ['#carrinho', '#menu'].map(function (s) { return $(s); }).filter(function (g) { return !g.hidden; });
    if (!abertas.length) { $('#veu').hidden = true; document.body.style.overflow = ''; if (typeof depois === 'function') depois(); return; }
    abertas.forEach(function (g) { Cinema.fecharGaveta(g, function () { $('#veu').hidden = true; document.body.style.overflow = ''; if (typeof depois === 'function') depois(); }); });
  }""")
troca("""    if (e.target.closest('[data-fechar]') || e.target.id === 'veu') fechar();""",
      """    if (e.target.closest('[data-fechar]') || e.target.id === 'veu') fechar();
    var link = e.target.closest('.gaveta a[href^="#/"]');
    if (link) { e.preventDefault(); fechar(function () { location.hash = link.getAttribute('href'); }); }""")
troca("""  function adicionar(p, v, q) {""", """  function adicionar(p, v, q, origem) {
    if (origem) Cinema.voar(origem);""")
troca("""    salvar(); abrirCarrinho();
  }""", """    salvar(); setTimeout(abrirCarrinho, origem && !Cinema.calmo ? 650 : 0);
  }""")

# menu com fotos das categorias
troca("""      CATS.map(function (c) { return '<a href="#/c/' + c.h + '">' + c.n + '<small>' + c.d + '</small></a>'; }).join('') +""",
      """      CATS.map(function (c) { return '<a href="#/c/' + c.h + '">' + c.n + '<small>' + c.d + '</small></a>'; }).join('') +""")

# home: letreiro, contadores
troca("""      '<div><svg viewBox="0 0 24 24"><rect x="4" y="5" width="16" height="12" rx="2"/><path d="m10 9 5 2.5-5 2.5z"/></svg><p style="margin:0"><b>Testado no canal</b><span>Quem vende, usa</span></p></div></div>' +""",
      """      '<div><svg viewBox="0 0 24 24"><rect x="4" y="5" width="16" height="12" rx="2"/><path d="m10 9 5 2.5-5 2.5z"/></svg><p style="margin:0"><b>Testado no canal</b><span>Quem vende, usa</span></p></div></div>' +
      letreiro() +""")
troca("""  var cena = '<div class="sl-scene">""", """  function letreiro() {
    var itens = ['<span class="az">R15</span>', '<span class="pt">/</span>', '<span>R3</span>', '<span class="pt">/</span>', '<span>Frete grátis</span>', '<span class="pt">/</span>', '<span class="az">12x no cartão</span>', '<span class="pt">/</span>', '<span>Testado no canal</span>', '<span class="pt">/</span>'].join('');
    return '<div class="letreiro" aria-hidden="true"><div class="letreiro-in">' + itens + itens + itens + itens + '</div></div>';
  }
  var cena = '<div class="sl-scene">""")
troca("""'<div class="num"><div><b>' + D.produtos.length + '</b><span>Produtos no catálogo</span></div>""",
      """'<div class="num"><div><b data-contar="' + D.produtos.length + '">0</b><span>Produtos no catálogo</span></div>""")

# coleção redesenhada
velho = a[a.index('  function colecao(h, q) {'):a.index('  function produto(h) {')]
novo = r"""  function colecao(h, q) {
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

"""
a = a.replace(velho, novo)

# produto: contador de fotos, descrição recolhível, voar ao carrinho, barra de compra
troca("""<div class="principal"><div class="trilho" id="trilho"></div><div class="pontos" id="pontos"></div></div>""",
      """<div class="principal"><span class="foto-cont" id="foto-cont"></span><div class="trilho" id="trilho"></div><div class="pontos" id="pontos"></div></div>""")
troca("""(p.desc ? '<div class="desc-box"><h2>Sobre o produto</h2><div class="desc">' + esc(p.desc) + '</div></div>' : '') +""",
      """(p.desc ? '<details class="acc"' + (window.innerWidth > 720 ? ' open' : '') + '><summary>Sobre o produto</summary><div class="desc">' + esc(p.desc) + '</div></details>' : '') +""")
troca("""      [].forEach.call($('#pontos').children, function (b, k) { b.classList.toggle('on', k === i); });
    }""", """      [].forEach.call($('#pontos').children, function (b, k) { b.classList.toggle('on', k === i); });
      $('#foto-cont').textContent = (i + 1) + ' / ' + fotos.length; $('#foto-cont').hidden = fotos.length < 2;
    }""")
troca("""      if (e.target.closest('#comprar') || e.target.closest('#comprar2')) adicionar(p, v, qtd);""",
      """      if (e.target.closest('#comprar') || e.target.closest('#comprar2')) {
        var t = $('#trilho'), atual = t ? t.children[Math.round(t.scrollLeft / Math.max(t.clientWidth, 1))] : null;
        adicionar(p, v, qtd, atual);
      }""")
troca("""    checaBuy = function () { var b = $('#comprar'), bb = $('#buybar'); if (b && bb) bb.classList.toggle('on', b.getBoundingClientRect().bottom < 120); };""",
      """    checaBuy = function () {
      var b = $('#comprar'), bb = $('#buybar'); if (!b || !bb) return;
      var r = b.getBoundingClientRect(), topo = window.innerWidth <= 720 ? 70 : 120;
      bb.classList.toggle('on', r.bottom < topo || r.top > window.innerHeight - 140);
    };
    checaBuy();""")

# rotas com transição, revelação e indicador do menu
velho = a[a.index('  function rota() {'):a.index("  $('#busca').addEventListener('submit'")]
novo = r"""  function rota() {
    Cinema.transicao(desenha);
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
  }

"""
a = a.replace(velho, novo)
troca("""    window.addEventListener('hashchange', rota);
    rota(); loaderPronto();""", """    window.addEventListener('hashchange', rota);
    desenha(); loaderPronto();
    window.addEventListener('resize', function () { Cinema.indicador($('#cats'), $('#cats a.on')); var ch = $('#chips'); if (ch) Cinema.indicador(ch, ch.querySelector('.on')); });""")
open(p, 'w', encoding='utf8').write(a)
print('protótipo ok')
