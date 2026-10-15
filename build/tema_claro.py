"""Tema claro no protótipo + nova animação do card (foto voa e pousa na galeria do produto)."""

def troca(caminho, a, b):
    s = open(caminho, encoding='utf8').read()
    if b in s and a not in s: return
    assert a in s, f'{caminho}: {a[:80]}'
    open(caminho, 'w', encoding='utf8').write(s.replace(a, b, 1))

T = 'build/site.src.html'
troca(T, '<link rel="stylesheet" href="premium.css">', '<link rel="stylesheet" href="claro.css">')
troca(T, '<a class="logo" href="#/" aria-label="Sandim R15 Store, página inicial"><svg viewBox="0 0 2000 667"><use href="#logo" style="--k:url(#sg-branco);--b:url(#sg-azulc)"/></svg></a>',
         '<a class="logo" href="#/" aria-label="Sandim R15 Store, página inicial"><svg viewBox="0 0 2000 667"><use href="#logo" style="--k:url(#sg-preto);--b:url(#sg-azul)"/></svg></a>')
P = 'build/site.py'
troca(P, "rep['premium.css\"'] = 'premium.css?v=' + ver + '\"'", "rep['claro.css\"'] = 'claro.css?v=' + ver + '\"'")
troca(P, "    '{{MOTO_COMPLETA}}': LS.moto_svg().replace('sl-roda', 'hero-roda'),",
         "    '{{MOTO_COMPLETA}}': LS.moto_svg('url(#sg-preto)', 'url(#sg-azul)', 'url(#sg-preto)').replace('sl-roda', 'hero-roda'),")

A = 'site/app.js'
s = open(A, encoding='utf8').read()
i = s.index('  /* ---------- card que sobe, gira e vira a página do produto ---------- */')
j = s.index("  app.addEventListener('click', function (e) {\n    var c = e.target.closest('a.card');")
nova = r"""  /* ---------- card: a foto sobe, gira e pousa na galeria do produto ---------- */
  var pularTransicao = false, vooAtivo = false, aposDesenhar = null;
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
    sobe.onfinish = function () {
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
        voa.onfinish = function () {
          document.body.classList.remove('chegando');
          var some = voo.animate([{ opacity: 1 }, { opacity: 0 }], { duration: 220, easing: 'ease-out', fill: 'forwards' });
          some.onfinish = function () { voo.remove(); vooAtivo = false; };
        };
      };
      pularTransicao = true;
      if (location.hash === href) rota(); else location.hash = href;
    };
  }
"""
s = s[:i] + nova + s[j:]
# chama a continuação do voo logo depois de desenhar a página
gancho = "    document.title = t + 'Sandim R15 Store';\n  }"
assert gancho in s
s = s.replace(gancho, "    document.title = t + 'Sandim R15 Store';\n    if (aposDesenhar) { var f = aposDesenhar; aposDesenhar = null; requestAnimationFrame(f); }\n  }", 1)
open(A, 'w', encoding='utf8').write(s)
print('tema claro + voo ok')
