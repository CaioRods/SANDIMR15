"""Passada mobile-first: barra inferior, cabeçalho que encolhe, galeria com arraste, compra fixa e carrosséis."""
import re

# ---------- template: barra inferior ----------
p = 'build/site.src.html'; s = open(p, encoding='utf8').read()
if 'class="tabbar"' not in s:
    s = s.replace('<div class="veu" id="veu" hidden></div>', '''<nav class="tabbar" aria-label="Navegação rápida">
  <a href="#/" data-tab="home"><svg viewBox="0 0 24 24"><path d="M4 11 12 4l8 7v9h-5v-6H9v6H4z"/></svg><span>Início</span></a>
  <button type="button" id="tab-cats" data-tab="cats"><svg viewBox="0 0 24 24"><rect x="4" y="4" width="7" height="7" rx="1.5"/><rect x="13" y="4" width="7" height="7" rx="1.5"/><rect x="4" y="13" width="7" height="7" rx="1.5"/><rect x="13" y="13" width="7" height="7" rx="1.5"/></svg><span>Categorias</span></button>
  <button type="button" id="tab-busca" data-tab="busca"><svg viewBox="0 0 24 24"><circle cx="11" cy="11" r="7"/><path d="m20 20-4-4"/></svg><span>Buscar</span></button>
  <button type="button" id="tab-cart" data-tab="cart"><svg viewBox="0 0 24 24"><path d="M3 4h2l2.4 11h10.2L20 7H6.2"/><circle cx="9" cy="19.5" r="1.4"/><circle cx="17" cy="19.5" r="1.4"/></svg><span>Carrinho</span><b class="badge-n" id="qtd-tab" hidden>0</b></button>
</nav>
<div class="veu" id="veu" hidden></div>''')
open(p, 'w', encoding='utf8').write(s)

# ---------- JS ----------
a = open('site/app.js', encoding='utf8').read()
def troca(velho, novo):
    global a
    assert velho in a, velho[:70]
    a = a.replace(velho, novo)

# contador nos dois selos
troca("""    var n = cart.reduce(function (s, i) { return s + i.q; }, 0), b = $('#qtd-carrinho');
    b.textContent = n; b.hidden = !n;""",
"""    var n = cart.reduce(function (s, i) { return s + i.q; }, 0);
    ['#qtd-carrinho', '#qtd-tab'].forEach(function (sel) { var b = $(sel); if (b) { b.textContent = n; b.hidden = !n; } });""")

# menu reaproveitado pela barra inferior
troca("""  $('#abrir-menu').addEventListener('click', function () {""", """  function abrirMenu() {""")
troca("""    abrir('#menu');
  });
  var tt;""", """    abrir('#menu');
  }
  $('#abrir-menu').addEventListener('click', abrirMenu);
  $('#tab-cats').addEventListener('click', abrirMenu);
  $('#tab-cart').addEventListener('click', abrirCarrinho);
  $('#tab-busca').addEventListener('click', function () { fechar(); window.scrollTo({ top: 0, behavior: 'smooth' }); setTimeout(function () { $('#busca-q').focus(); }, 250); });
  var hdr = $('#topo');
  window.addEventListener('scroll', function () { hdr.classList.toggle('min', window.scrollY > 80); }, { passive: true });
  var tt;""")

# vitrines em carrossel
troca("""  function vitrine(tit, sub, h, n, lista) {""", """  function vitrine(tit, sub, h, n, lista, car) {""")
troca("""'</div><div class="grade">' + lista.map(card).join('') + '</div></div></section>';""",
      """'</div><div class="grade' + (car ? ' carrossel' : '') + '">' + lista.map(card).join('') + '</div></div></section>';""")
troca("""vitrine('Mais vendidos', 'O que mais sai para a R15 neste mês', 'mais-vendidos', 8, maisVend)""",
      """vitrine('Mais vendidos', 'O que mais sai para a R15 neste mês', 'mais-vendidos', 10, maisVend, true)""")
troca("""vitrine('Kits com desconto', 'Combinações prontas com preço especial', 'kits-com-desconto', 4)""",
      """vitrine('Kits com desconto', 'Combinações prontas com preço especial', 'kits-com-desconto', 6, null, true)""")
troca("""vitrine('Lançamentos', 'Acabou de chegar na loja', 'news', 8)""",
      """vitrine('Lançamentos', 'Acabou de chegar na loja', 'news', 10, null, true)""")
troca("""vitrine('Combina com', 'Mais peças para a sua ' + p.moto[0], null, 4, rel)""",
      """vitrine('Combina com', 'Mais peças para a sua ' + p.moto[0], null, 8, rel, true)""")
troca("""Object.keys(x.col).some(function (c) { return c in p.col && ['mais-vendidos', 'news', 'ofertas-da-semana', 'acessorios'].indexOf(c) < 0; }); }).slice(0, 4);""",
      """Object.keys(x.col).some(function (c) { return c in p.col && ['mais-vendidos', 'news', 'ofertas-da-semana', 'acessorios'].indexOf(c) < 0; }); }).slice(0, 8);""")

# galeria com arraste (trilho com scroll-snap) + pontos
troca("""'<div class="prod"><div class="galeria"><div class="miniaturas" id="minis"></div><div class="principal"><img id="foto" src="' + img(fotos[0], 900) + '" alt="' + esc(p.t) + '"></div></div>'""",
      """'<div class="prod"><div class="galeria"><div class="miniaturas" id="minis"></div><div class="principal"><div class="trilho" id="trilho"></div><div class="pontos" id="pontos"></div></div></div>'""")
troca("""    function pintaFotos(i) {
      $('#foto').src = img(fotos[i], 900);
      $('#minis').innerHTML = fotos.map(function (f, k) { return '<button type="button" data-f="' + k + '" class="' + (k === i ? 'on' : '') + '" aria-label="Foto ' + (k + 1) + '"><img src="' + img(f, 160) + '" alt=""></button>'; }).join('');
    }""",
"""    var montadas = '';
    function ativo(i) {
      [].forEach.call($('#minis').children, function (b, k) { b.classList.toggle('on', k === i); });
      [].forEach.call($('#pontos').children, function (b, k) { b.classList.toggle('on', k === i); });
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
    }""")

# barra de compra fixa no celular
troca("""      '</div></div></div>' + (rel.length ?""",
      """      '</div></div></div><div class="buybar" id="buybar"><div class="bb-txt"><b id="bb-preco"></b><small id="bb-parc"></small></div><button class="btn" type="button" id="comprar2">Comprar</button></div>' + (rel.length ?""")
troca("""      $('#precos').innerHTML = (de ?""", """      $('#bb-preco').textContent = brl(v.p); $('#bb-parc').textContent = 'ou 12x de ' + brl(v.p * COEF_12X);
      $('#precos').innerHTML = (de ?""")
troca("""      if (e.target.closest('#comprar')) adicionar(p, v, qtd);""",
      """      if (e.target.closest('#comprar') || e.target.closest('#comprar2')) adicionar(p, v, qtd);""")
troca("""    pintaFotos(0); pintaPreco();""", """    pintaFotos(0); pintaPreco();
    if ('IntersectionObserver' in window) {
      new IntersectionObserver(function (es) { var bb = $('#buybar'); if (bb) bb.classList.toggle('on', !es[0].isIntersecting && es[0].boundingClientRect.top < 0); }).observe($('#comprar'));
    }""")

# aba ativa e classe da página
troca("""    fechar();
    window.scrollTo(0, 0);""", """    fechar();
    document.body.dataset.rota = r[0] || 'home';
    document.querySelectorAll('.tabbar [data-tab]').forEach(function (t) { t.classList.toggle('on', t.dataset.tab === 'home' && !r[0]); });
    window.scrollTo(0, 0);""")
open('site/app.js', 'w', encoding='utf8').write(a)

# ---------- CSS mobile ----------
c = open('site/estilo.css', encoding='utf8').read()
c = c[:c.index('/* ===== celular ===== */')] if '/* ===== celular ===== */' in c else c
c = c.replace('.busca input{flex:1;min-width:0;border:0;padding:11px 14px;font:inherit;font-size:15px;', '.busca input{flex:1;min-width:0;border:0;padding:11px 14px;font:inherit;font-size:16px;')
c = c.replace('.galeria .principal img{width:100%;height:100%;object-fit:contain}', '.galeria .principal{position:relative}\n.trilho{display:flex;width:100%;height:100%;overflow-x:auto;scroll-snap-type:x mandatory;scrollbar-width:none;overscroll-behavior-x:contain}\n.trilho::-webkit-scrollbar{display:none}\n.trilho img{flex:0 0 100%;width:100%;height:100%;object-fit:contain;scroll-snap-align:start;background:#fff}\n.pontos{position:absolute;left:0;right:0;bottom:10px;display:flex;justify-content:center;gap:6px;pointer-events:none}\n.pontos i{width:7px;height:7px;border-radius:4px;background:rgba(28,31,37,.25);transition:width .2s,background .2s}\n.pontos i.on{width:20px;background:var(--azul)}')
c += '''
/* ===== celular ===== */
.tabbar,.buybar{display:none}
.hdr .logo svg{transition:height .2s}
@media (max-width:720px){
  body{padding-bottom:calc(64px + env(safe-area-inset-bottom,0px))}
  .topline{font-size:11.5px;padding-block:6px}
  .hdr-in{padding-block:6px}
  .hdr.min .logo svg{height:34px}
  .hdr.min .busca{display:none}
  .hdr.min .cats{display:none}
  .cats a{padding:8px 10px 10px;font-size:13px}
  .acoes .carrinho-btn{display:none}
  .icon-btn{width:44px;height:44px}

  .tabbar{display:grid;grid-template-columns:repeat(4,1fr);position:fixed;left:0;right:0;bottom:0;z-index:70;background:rgba(255,255,255,.97);backdrop-filter:blur(10px);border-top:1px solid var(--borda);padding:6px max(8px,env(safe-area-inset-right,0px)) calc(6px + env(safe-area-inset-bottom,0px)) max(8px,env(safe-area-inset-left,0px))}
  .tabbar a,.tabbar button{position:relative;border:0;background:none;display:flex;flex-direction:column;align-items:center;gap:2px;padding:6px 0;min-height:48px;color:var(--apoio);font-family:var(--label);font-weight:700;font-size:11.5px;letter-spacing:.04em}
  .tabbar svg{width:23px;height:23px;fill:none;stroke:currentColor;stroke-width:1.8;stroke-linecap:round;stroke-linejoin:round}
  .tabbar .on{color:var(--azul)}
  .tabbar .badge-n{top:2px;right:calc(50% - 22px)}
  .whats{bottom:calc(78px + env(safe-area-inset-bottom,0px));width:50px;height:50px;right:14px}
  .whats svg{width:26px;height:26px}
  body[data-rota="p"] .whats{display:none}
  .toast{bottom:calc(84px + env(safe-area-inset-bottom,0px))}

  .hero-in{padding-top:28px;gap:8px}
  .hero h1{font-size:clamp(34px,10vw,44px)}
  .hero p{font-size:16px}
  .hero .ctas .btn{flex:1;padding-inline:12px}
  .beneficios{display:flex;overflow-x:auto;scroll-snap-type:x mandatory;scrollbar-width:none}
  .beneficios::-webkit-scrollbar{display:none}
  .beneficios div{flex:0 0 72%;scroll-snap-align:start;border-bottom:0!important;padding:16px}
  .secao{padding-block:36px}
  .sec-head{margin-bottom:16px}
  .sec-head h2{font-size:26px}
  .sec-head p{font-size:14px}

  .grade.carrossel{display:grid;grid-auto-flow:column;grid-auto-columns:46%;grid-template-columns:none;overflow-x:auto;scroll-snap-type:x mandatory;scroll-padding-inline:var(--gut);margin-inline:calc(-1 * var(--gut));padding:4px var(--gut) 10px;scrollbar-width:none}
  .grade.carrossel::-webkit-scrollbar{display:none}
  .grade.carrossel .card{scroll-snap-align:start}
  .card:hover{transform:none}
  .card .frete{font-size:11px}
  .categorias{display:grid;grid-auto-flow:column;grid-auto-columns:38%;grid-template-columns:none;overflow-x:auto;scroll-snap-type:x mandatory;margin-inline:calc(-1 * var(--gut));padding:0 var(--gut) 6px;scroll-padding-inline:var(--gut);scrollbar-width:none}
  .categorias::-webkit-scrollbar{display:none}
  .cat{scroll-snap-align:start}

  .canal-in{padding-block:40px}
  .canal .visual{display:none}

  .col-topo{padding-block:24px 20px}
  .filtros{position:sticky;top:var(--hdr-h,52px);z-index:20;background:var(--fundo);padding-block:10px;margin-inline:calc(-1 * var(--gut));padding-inline:var(--gut);border-bottom:1px solid var(--borda)}
  .chips{flex-wrap:nowrap;overflow-x:auto;scrollbar-width:none}
  .chip{white-space:nowrap;padding:9px 14px}
  .ordem select{font-size:16px;padding:8px}

  .prod{padding-top:4px;gap:16px}
  .galeria{margin-inline:calc(-1 * var(--gut))}
  .galeria .principal{border:0;border-radius:0}
  .galeria .miniaturas{display:none}
  .compra h1{font-size:24px}
  .precos .preco{font-size:34px}
  .variantes button{flex:1 1 calc(50% - 4px)}
  .linha-compra .btn{padding-inline:12px}
  .buybar{display:flex;position:fixed;left:0;right:0;bottom:calc(64px + env(safe-area-inset-bottom,0px));z-index:65;align-items:center;gap:12px;padding:10px max(16px,env(safe-area-inset-right,0px)) 10px max(16px,env(safe-area-inset-left,0px));background:#fff;border-top:1px solid var(--borda);box-shadow:0 -8px 24px rgba(10,20,48,.08);transform:translateY(140%);transition:transform .25s ease}
  .buybar.on{transform:none}
  .bb-txt{display:flex;flex-direction:column;line-height:1.15;min-width:0}
  .bb-txt b{font-family:var(--display);font-style:italic;font-weight:800;font-size:22px}
  .bb-txt small{color:var(--apoio);font-size:12px}
  .buybar .btn{margin-left:auto;padding:13px 22px}

  .gaveta{width:100vw}
  .item{grid-template-columns:64px 1fr auto}
  .item img{width:64px;height:64px}
  .rodape-in{padding-top:36px}
}
'''
open('site/estilo.css', 'w', encoding='utf8').write(c)
print('mobile ok')
