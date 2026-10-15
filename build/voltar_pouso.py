"""Botão de voltar + pouso exato da foto do card na foto da galeria do produto."""
A = 'site/app.js'
s = open(A, encoding='utf8').read()

def troca(a, b):
    global s
    if b in s and a not in s: return
    assert a in s, a[:80]
    s = s.replace(a, b, 1)

SETA = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M15 5l-7 7 7 7"/></svg>'

# ---------- voltar ----------
troca("""  var rotaAnterior = location.hash;""", """  var rotaAnterior = location.hash, passos = 0;
  function voltar() {
    if (passos > 0) { history.back(); return; }
    var p = /^#\\/p\\/(.+)/.exec(location.hash), prod = p && porH[p[1]];
    location.hash = prod ? '#/c/' + (prod.moto[0] === 'R3' ? 'acessorios-r3' : 'acessorios') : '#/';
  }
  document.addEventListener('click', function (e) { if (e.target.closest('[data-voltar]')) { e.preventDefault(); voltar(); } });""")
troca("""  function rota() {
    var de = idxCat(rotaAnterior), para = idxCat(location.hash);""", """  function rota() {
    passos++;
    var de = idxCat(rotaAnterior), para = idxCat(location.hash);""")

# produto: botão no topo (computador) e sobre a foto (celular)
troca("""    app.innerHTML = '<div class="wrap"><div class="migalha" style="color:var(--apoio);padding-top:20px"><a href="#/">Início</a> / <a href="#/c/' + (p.moto[0] === 'R3' ? 'acessorios-r3' : 'acessorios') + '">Linha ' + p.moto[0] + '</a> / ' + esc(p.t) + '</div>' +
      '<div class="prod"><div class="galeria"><div class="miniaturas" id="minis"></div><div class="principal"><span class="foto-cont" id="foto-cont"></span>""",
      """    app.innerHTML = '<div class="wrap"><div class="topo-prod"><button class="voltar" type="button" data-voltar>""" + SETA + """Voltar</button><div class="migalha"><a href="#/">Início</a> / <a href="#/c/' + (p.moto[0] === 'R3' ? 'acessorios-r3' : 'acessorios') + '">Linha ' + p.moto[0] + '</a> / ' + esc(p.t) + '</div></div>' +
      '<div class="prod"><div class="galeria"><div class="miniaturas" id="minis"></div><div class="principal"><button class="voltar-foto" type="button" data-voltar aria-label="Voltar">""" + SETA + """</button><span class="foto-cont" id="foto-cont"></span>""")
# coleção: botão antes da migalha
troca("""'<div class="wrap"><div class="migalha"><a href="#/">Início</a> / ' + tit + '</div><div class="col-tit">""",
      """'<div class="wrap"><div class="topo-col"><button class="voltar" type="button" data-voltar>""" + SETA + """Voltar</button><div class="migalha"><a href="#/">Início</a> / ' + tit + '</div></div><div class="col-tit">""")

# ---------- pouso exato ----------
# 1) cabeçalho volta ao tamanho do topo ANTES de medir
troca("""    $('#topo').classList.remove('oculto');""", """    $('#topo').classList.remove('oculto', 'min', 'busca-aberta'); altHdr();""")
# 2) foto grande pré-carregada no clique e alvo = a própria foto da galeria
troca("""    var r = ft.getBoundingClientRect();
    var voo = document.createElement('div');""", """    var r = ft.getBoundingClientRect();
    var hp = /^#\\/p\\/(.+)/.exec(href), prod = hp && porH[hp[1]];
    var grande = new Image(); if (prod) grande.src = img(prod.img[0], 900);
    var voo = document.createElement('div');""")
troca("""        var alvo = document.querySelector('.galeria .principal');
        var t = alvo ? alvo.getBoundingClientRect() : { left: 0, top: 80, width: window.innerWidth, height: window.innerWidth };""",
      """        var caixa = document.querySelector('.galeria .principal');
        var alvo = document.querySelector('#trilho img') || caixa;
        var t = alvo ? alvo.getBoundingClientRect() : { left: 0, top: 80, width: window.innerWidth, height: window.innerWidth };
        var trocaFoto = function () { var im = voo.querySelector('img'); if (grande.complete && grande.naturalWidth) im.src = grande.src; };
        if (grande.complete) trocaFoto(); else grande.onload = trocaFoto;""")
troca("""        var raio = alvo ? getComputedStyle(alvo).borderRadius : '0px';""",
      """        var raio = caixa ? getComputedStyle(caixa).borderRadius : '0px';""")
# 3) só some depois que a foto da galeria carregou (no máximo 700 ms)
troca("""        aoAcabar(voa, dur, function () {
          document.body.classList.remove('chegando');
          var some = voo.animate([{ opacity: 1 }, { opacity: 0 }], { duration: 220, easing: 'ease-out', fill: 'forwards' });
          aoAcabar(some, 220, function () { voo.remove(); vooAtivo = false; });
        });""", """        aoAcabar(voa, dur, function () {
          var foto = document.querySelector('#trilho img');
          var fim = function () {
            if (fim.feito) return; fim.feito = true;
            document.body.classList.remove('chegando');
            var some = voo.animate([{ opacity: 1 }, { opacity: 0 }], { duration: 180, easing: 'ease-out', fill: 'forwards' });
            aoAcabar(some, 180, function () { voo.remove(); vooAtivo = false; });
          };
          if (!foto || (foto.complete && foto.naturalWidth)) fim();
          else { foto.addEventListener('load', fim, { once: true }); setTimeout(fim, 700); }
        });""")
open(A, 'w', encoding='utf8').write(s)

css = """

/* ===== voltar + pouso ===== */
.topo-prod,.topo-col{display:flex;align-items:center;gap:14px;flex-wrap:wrap;padding-top:18px}
.topo-col{padding-top:0;margin-bottom:10px}
.topo-prod .migalha,.topo-col .migalha{margin:0;padding:0}
.voltar{display:inline-flex;align-items:center;gap:6px;border:1px solid var(--linha);background:#fff;border-radius:999px;padding:8px 16px 8px 10px;font-family:var(--label);font-weight:700;font-size:13px;letter-spacing:.08em;text-transform:uppercase;color:var(--tinta);box-shadow:var(--sombra-1);cursor:pointer;transition:transform .25s,box-shadow .25s,color .25s}
.voltar svg,.voltar-foto svg{width:18px;height:18px;fill:none;stroke:currentColor;stroke-width:2.2;stroke-linecap:round;stroke-linejoin:round;transition:transform .25s}
.voltar:hover{color:var(--azul);box-shadow:var(--sombra-2)}
.voltar:hover svg{transform:translateX(-3px)}
.voltar:active{transform:scale(.96)}
.voltar-foto{display:none}
.trilho img{box-sizing:border-box}
@media (max-width:720px){
  .topo-prod{display:none}
  .prod{padding-top:0}
  .voltar-foto{display:grid;place-items:center;position:absolute;top:12px;left:12px;z-index:3;width:42px;height:42px;border-radius:50%;border:1px solid var(--linha);background:rgba(255,255,255,.9);-webkit-backdrop-filter:blur(10px);backdrop-filter:blur(10px);color:var(--tinta);box-shadow:var(--sombra-1);cursor:pointer}
  .voltar-foto:active{transform:scale(.92)}
  .topo-col .migalha{display:none}
  .voltar{padding:7px 14px 7px 8px;font-size:12px}
}
"""
c = open('site/claro.css', encoding='utf8').read()
if '/* ===== voltar + pouso ===== */' not in c:
    open('site/claro.css', 'a', encoding='utf8').write(css)
print('voltar + pouso ok')
