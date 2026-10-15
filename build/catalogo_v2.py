"""Protótipo: ano em destaque, sem estoque, bordas por moto, menu com faixa azul e transição entre catálogos."""
A = 'site/app.js'
s = open(A, encoding='utf8').read()

def troca(a, b):
    global s
    if b in s and a not in s: return
    assert a in s, a[:80]
    s = s.replace(a, b, 1)

# ---------- card ----------
i = s.index('  function card(p) {'); j = s.index('  function daColecao(h) {')
s = s[:i] + r"""  function classeMoto(p) {
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
""" + s[j:]

# ---------- produto: ano e estoque ----------
troca("""      '<h1>' + esc(p.t) + '</h1><div class="precos" id="precos"></div>' +""",
      """      '<h1>' + esc(p.t) + '</h1>' + (p.anos ? '<p class="ano-destaque">Serve nos anos <b>' + p.anos + '</b></p>' : '') + '<div class="precos" id="precos"></div>' +""")
troca("""        $('#vars').innerHTML = p.v.map(function (x, k) { return '<button type="button" data-v="' + k + '" class="' + (x === v ? 'on' : '') + '"' + (x.ok ? '' : ' disabled') + '>' + (x.img ? '<img src="' + img(x.img, 100) + '" alt="">' : '') + '<span>' + esc(x.t) + '</span></button>'; }).join('');""",
      """        $('#vars').innerHTML = p.v.map(function (x, k) { return '<button type="button" data-v="' + k + '" class="' + (x === v ? 'on' : '') + (x.ok ? '' : ' sem') + '"' + (x.ok ? '' : ' disabled') + '>' + (x.img ? '<img src="' + img(x.img, 100) + '" alt="">' : '') + '<span>' + esc(x.t) + (x.ok ? '' : '<small>sem estoque</small>') + '</span></button>'; }).join('');""")
troca("""      $('#bb-preco').textContent = brl(v.p);""",
      """      ['#comprar', '#comprar2'].forEach(function (id) { var b = $(id); if (b) { b.disabled = !v.ok; b.textContent = v.ok ? (id === '#comprar' ? 'Adicionar ao carrinho' : 'Comprar') : 'Sem estoque'; } });
      $('#bb-preco').textContent = brl(v.p);""")

# ---------- transição entre telas de catálogo ----------
troca("""  function rota() {
    if (pularTransicao) { pularTransicao = false; desenha(); return; }
    Cinema.transicao(desenha);
  }""", r"""  var rotaAnterior = location.hash;
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
    sai.onfinish = function () {
      var y = window.scrollY;
      desenha();
      var topo = $('.col-topo'); if (topo && y > topo.offsetHeight) window.scrollTo(0, topo.offsetHeight - 10);
      sai.cancel();
      app.animate([{ opacity: 0, transform: 'translateX(' + (dir * 56) + 'px)' }, { opacity: 1, transform: 'translateX(0)' }], { duration: 520, easing: 'cubic-bezier(.22,1,.36,1)' });
      var g = $('#lista');
      if (g) { [].forEach.call(g.children, function (el, k) { el.style.setProperty('--i', Math.min(k, 12)); }); g.classList.add('trocando'); }
    };
  }""")

# ---------- menu: faixa azul forte ao clicar, depois abre ----------
troca("""  app.addEventListener('click', function (e) {
    var c = e.target.closest('a.card');""", r"""  document.addEventListener('click', function (e) {
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
    var c = e.target.closest('a.card');""")
open(A, 'w', encoding='utf8').write(s)

# ---------- CSS ----------
css = r"""

/* ===== catálogo v2 ===== */
/* bordas finas por moto: R15 azul, R3 grafite fosco, ambos metade/metade */
.card{border:1.5px solid transparent}
.card.m-r15{border-color:rgba(0,147,226,.75)}
.card.m-r3{border-color:#4A4F59}
.card.m-ambos{background:linear-gradient(#fff,#fff) padding-box,linear-gradient(90deg,rgba(0,147,226,.75) 0 50%,#4A4F59 50% 100%) border-box}
.card.m-outra{border-color:var(--linha)}

/* ano em destaque */
.card .ano{align-self:flex-start;font-family:var(--label);font-weight:700;font-size:11.5px;letter-spacing:.06em;color:#0077B8;background:rgba(0,147,226,.1);border-radius:999px;padding:2px 9px;margin-bottom:4px}
.ano-destaque{margin:-4px 0 0;font-size:15px;color:var(--cinza)}
.ano-destaque b{font-family:var(--label);font-weight:700;letter-spacing:.04em;color:#0077B8;background:rgba(0,147,226,.1);border-radius:999px;padding:3px 12px;margin-left:4px}

/* sem estoque */
.card.esgotado .ft img{filter:grayscale(1);opacity:.45}
.card .sem-estoque{position:absolute;left:50%;bottom:12px;transform:translateX(-50%);white-space:nowrap;background:rgba(18,21,28,.86);color:#fff;font-family:var(--label);font-weight:700;font-size:12px;letter-spacing:.12em;text-transform:uppercase;padding:6px 14px;border-radius:999px}
.card.esgotado .preco{color:#9AA3B5}
.card.esgotado .parc{color:#0077B8;font-weight:600}
.variantes button.sem{opacity:.55}
.variantes button.sem span{text-decoration:line-through}
.variantes button.sem small{display:block;text-decoration:none;font-size:11px;color:#C2410C;font-weight:600}
.btn[disabled]{background:#C9D0DB!important;box-shadow:none!important;color:#fff!important;cursor:not-allowed;transform:none!important}

/* menu: hover azul claro, ativo com faixa azul forte */
.cats{position:relative;isolation:isolate}
.cats a{position:relative;z-index:1;border-radius:999px;transition:color .25s,background-color .25s}
.cats a:hover{background:rgba(0,147,226,.09);color:var(--azul)}
.cats a.on,.cats a.on:hover{color:#fff;background:transparent}
.cats .ind{top:6px;bottom:6px;height:auto;border-radius:999px;background:var(--g-azul);box-shadow:0 6px 16px rgba(0,134,209,.3);z-index:0}
.cats a.clicado{animation:clique .32s cubic-bezier(.2,.8,.2,1)}
@keyframes clique{40%{transform:scale(.94)}}

/* faixa de categorias da coleção: mesmo comportamento */
.cn .bola{transition:border-color .25s,transform .3s cubic-bezier(.2,.8,.2,1),box-shadow .3s,background .3s}
.cn:hover .bola{box-shadow:0 0 0 4px rgba(0,147,226,.12)}
.cn:hover span{color:var(--azul)}
.cn.on .bola{border-color:var(--azul);box-shadow:0 0 0 3px var(--azul)}
.cn.clicado .bola{animation:bola-clique .32s cubic-bezier(.2,.8,.2,1)}
.cn.clicado span{color:var(--azul)}
@keyframes bola-clique{40%{transform:scale(.9)}}

/* menu lateral (celular): hover azul claro e faixa azul ao tocar */
.menu-lat .gav-corpo a{position:relative;border-radius:14px;padding-inline:12px;margin-inline:-12px;overflow:hidden;isolation:isolate;transition:color .25s,background-color .25s}
.menu-lat .gav-corpo a:hover{background:rgba(0,147,226,.08);color:var(--azul)}
.menu-lat .gav-corpo a::before{content:"";position:absolute;inset:0;z-index:-1;background:var(--g-azul);transform:scaleX(0);transform-origin:left;transition:transform .32s cubic-bezier(.65,0,.35,1)}
.menu-lat .gav-corpo a.clicado{color:#fff}
.menu-lat .gav-corpo a.clicado small{color:rgba(255,255,255,.8)}
.menu-lat .gav-corpo a.clicado::before{transform:scaleX(1)}

/* escolha sua máquina: lado a lado no celular */
@media (max-width:720px){
  .maquinas{grid-template-columns:1fr 1fr;gap:10px}
  .maq{min-height:210px;padding:16px;border-radius:20px}
  .maq .num{font-size:64px}
  .maq .moto-bg{top:30%;right:-30%;width:120%}
  .maq .rod{flex-direction:column;align-items:flex-start;gap:10px}
  .maq .rod p{font-size:12.5px;line-height:1.3}
  .maq .rod b{font-size:16px;margin-bottom:2px}
  .maq .seta{width:36px;height:36px;font-size:16px;align-self:flex-end;position:absolute;top:0;right:0;transform:translateY(-130px)}
  .maq:hover .seta{transform:translateY(-130px) rotate(-45deg)}
}
"""
c = open('site/claro.css', encoding='utf8').read()
if '/* ===== catálogo v2 ===== */' not in c:
    open('site/claro.css', 'a', encoding='utf8').write(css)
print('catálogo v2 ok')
