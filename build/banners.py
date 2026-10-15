"""Home: carrossel com os banners da loja + pontos nos produtos do banner (Esgotado quando o produto
não existe no catálogo ou está sem estoque). Link para produto inexistente vira página de Esgotado."""
A = 'site/app.js'
s = open(A, encoding='utf8').read()

def troca(a, b):
    global s
    if b in s and a not in s: return
    assert a in s, a[:80]
    s = s.replace(a, b, 1)

CDN = '//sandimr15.store/cdn/shop/files/'

troca("""  /* ---------- páginas ---------- */""", """  /* ---------- banners da loja ---------- */
  // Para trocar: coloque as imagens em site/banners/ e mude pc (3:1, ex. 1800x600) e cel (ex. 700x1027).
  // link: para onde o banner leva ('' = sem link). pontos: [handle do produto, nome, x%, y% no computador, x%, y% no celular]
  var LOJA = '//sandimr15.store/cdn/shop/files/';
  var BANNERS = [
    { pc: LOJA + 'Banner_01_1800x.png?v=1744927293', cel: LOJA + 'Banner_Mes_pais_-_Mobile_700x.png?v=1744927292', link: '#/c/mais-vendidos', alt: 'Potência no estilo, adrenalina nos detalhes', pontos: [] },
    { pc: LOJA + 'Banner_02_1800x.png?v=1744927293', cel: LOJA + 'Banner_Mes_pais_-_Mobile_1_700x.png?v=1744927293', link: '', alt: 'Frete grátis para todo o Brasil', pontos: [
      ['bico-de-pato', 'Bico de Pato', 15, 57, 13, 64],
      ['amortecedor-de-direcao', 'Amortecedor de Direção', 31, 52, 40, 65],
      ['bolha-esportiva', 'Bolha Esportiva', 24, 86, 30, 78]
    ] }
  ];
  function ponto(pt) {
    var p = porH[pt[0]], ok = p && p.ok;
    var tag = ok ? 'a href="#/p/' + p.h + '"' : 'span';
    return '<' + tag + ' class="bn-ponto' + (ok ? '' : ' esgotado') + '" style="--x:' + pt[2] + '%;--y:' + pt[3] + '%;--xm:' + pt[4] + '%;--ym:' + pt[5] + '%">' +
      '<i aria-hidden="true"></i><span class="bn-tag"><b>' + esc(pt[1]) + '</b>' + (ok ? brl(p.preco) : '<em>Esgotado</em>') + '</span></' + tag.split(' ')[0] + '>';
  }
  function banners() {
    return '<section class="banners" aria-label="Destaques da loja"><div class="bn-trilho" id="bn-trilho">' + BANNERS.map(function (b, k) {
      var foto = '<picture><source media="(max-width:720px)" srcset="' + b.cel + '">' +
        '<img src="' + b.pc + '" alt="' + esc(b.alt) + '"' + (k ? ' loading="lazy"' : '') + ' decoding="async"></picture>';
      return '<div class="bn-slide">' + (b.link ? '<a class="bn-link" href="' + b.link + '">' + foto + '</a>' : foto) + b.pontos.map(ponto).join('') + '</div>';
    }).join('') + '</div>' +
      '<button class="foto-seta ant bn-seta" type="button" data-bn="-1" aria-label="Banner anterior"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M15 5l-7 7 7 7"/></svg></button>' +
      '<button class="foto-seta prox bn-seta" type="button" data-bn="1" aria-label="Próximo banner"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M9 5l7 7-7 7"/></svg></button>' +
      '<div class="bn-pontos" id="bn-pontos">' + BANNERS.map(function (b, k) { return '<button type="button" data-bni="' + k + '" aria-label="Banner ' + (k + 1) + '"' + (k ? '' : ' class="on"') + '></button>'; }).join('') + '</div></section>';
  }
  // carrossel: arrastar, setas, bolinhas e troca automática (pausa ao interagir ou fora da tela)
  var bnTimer = null;
  function bnLiga() {
    var t = $('#bn-trilho'); if (!t) return;
    var n = t.children.length, atual = function () { return Math.round(t.scrollLeft / Math.max(t.clientWidth, 1)); };
    var vai = function (i) { t.scrollTo({ left: ((i + n) % n) * t.clientWidth, behavior: 'smooth' }); };
    t.onscroll = function () { var i = atual(); [].forEach.call($('#bn-pontos').children, function (b, k) { b.classList.toggle('on', k === i); }); };
    var sec = t.parentNode, visivel = true, parado = false;
    sec.onclick = function (e) {
      var a = e.target.closest('[data-bn]'), b = e.target.closest('[data-bni]');
      if (a) vai(atual() + +a.dataset.bn); if (b) vai(+b.dataset.bni);
      var esg = e.target.closest('.bn-ponto.esgotado'); if (esg) { esg.classList.toggle('aberto'); }
    };
    sec.onpointerenter = function () { parado = true; }; sec.onpointerleave = function () { parado = false; };
    t.addEventListener('touchstart', function () { parado = true; clearTimeout(t._v); t._v = setTimeout(function () { parado = false; }, 8000); }, { passive: true });
    if ('IntersectionObserver' in window) new IntersectionObserver(function (es) { visivel = es[0].isIntersecting; }).observe(sec);
    clearInterval(bnTimer);
    bnTimer = setInterval(function () { if (!t.isConnected) { clearInterval(bnTimer); return; } if (visivel && !parado && !document.hidden) vai(atual() + 1); }, 6000);
  }

  /* ---------- páginas ---------- */""")

# banners logo depois do banner principal
troca("""      '<button class="hero-scroll" type="button" data-rolar="maquinas"><i></i>Role</button></section>' +
""", """      '<button class="hero-scroll" type="button" data-rolar="maquinas"><i></i>Role</button></section>' +
      banners() +
""")
troca("""    else app.innerHTML = home();""", """    else { app.innerHTML = home(); bnLiga(); }""")

# link para produto que não existe: página de Esgotado com sugestões
troca("""    if (!p) { app.innerHTML = '<div class="wrap pagina"><h1>Produto não encontrado</h1><p><a href="#/" style="color:var(--azul)">Voltar para a loja</a></p></div>'; return; }""",
      """    if (!p) {
      app.innerHTML = '<div class="wrap pagina esgotado-pag"><span class="sem-estoque">Esgotado</span><h1>Este produto está esgotado</h1><p>Ele saiu do nosso estoque por enquanto. Veja o que temos pronto para envio:</p><p><a class="btn" href="#/c/mais-vendidos">Ver mais vendidos</a></p></div>' + vitrine('Pronto para envio', '', 'mais-vendidos', 8, null, true);
      return;
    }""")
open(A, 'w', encoding='utf8').write(s)
print('banners ok')
