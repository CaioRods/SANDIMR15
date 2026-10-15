"""Card que sobe, gira e expande até a página do produto (protótipo)."""
A = 'site/app.js'
s = open(A, encoding='utf8').read()

def troca(a, b):
    global s
    if b in s: return
    assert a in s, a[:70]
    s = s.replace(a, b, 1)

troca("""  function abrirCarrinho() {""", r"""  /* ---------- card que sobe, gira e vira a página do produto ---------- */
  var pularTransicao = false, vooAtivo = false;
  function abrirCard(c, href) {
    if (vooAtivo) return;
    var foto = c.querySelector('.ft img');
    if (Cinema.calmo || !foto || !c.animate) { location.hash = href; return; }
    vooAtivo = true;
    var r = c.getBoundingClientRect(), W = window.innerWidth, H = window.innerHeight;
    var voo = document.createElement('div');
    voo.className = 'card-voo';
    voo.innerHTML = '<div class="cv-face"><div class="cv-ft"><img src="' + (foto.currentSrc || foto.src) + '" alt=""></div><div class="cv-info">' + c.querySelector('.info').innerHTML + '</div></div>';
    voo.style.cssText = 'left:' + r.left + 'px;top:' + r.top + 'px;width:' + r.width + 'px;height:' + r.height + 'px';
    document.body.appendChild(voo);
    c.style.visibility = 'hidden';
    var mw = Math.min(W * .72, 420), mh = mw * (r.height / r.width);
    var p = 'perspective(1400px) ';
    var dur = W <= 720 ? 1000 : 1150;
    var a = voo.animate([
      { left: r.left + 'px', top: r.top + 'px', width: r.width + 'px', height: r.height + 'px', transform: p + 'rotateY(0deg) scale(1)', borderRadius: '24px' },
      { offset: .2, left: r.left + 'px', top: (r.top - 16) + 'px', width: r.width + 'px', height: r.height + 'px', transform: p + 'rotateY(0deg) scale(1.07)', borderRadius: '24px' },
      { offset: .62, left: (W - mw) / 2 + 'px', top: (H - mh) / 2 + 'px', width: mw + 'px', height: mh + 'px', transform: p + 'rotateY(360deg) scale(1)', borderRadius: '28px' },
      { left: '0px', top: '0px', width: W + 'px', height: H + 'px', transform: p + 'rotateY(360deg) scale(1)', borderRadius: '0px' }
    ], { duration: dur, easing: 'cubic-bezier(.65,0,.35,1)', fill: 'forwards' });
    voo.querySelector('.cv-info').animate([{ opacity: 1 }, { opacity: 1, offset: .5 }, { opacity: 0, offset: .8 }, { opacity: 0 }], { duration: dur, fill: 'forwards' });
    a.onfinish = function () {
      pularTransicao = true;
      if (location.hash === href) desenha(); else location.hash = href;
      requestAnimationFrame(function () {
        var sai = voo.animate([{ opacity: 1 }, { opacity: 0 }], { duration: 450, easing: 'ease', fill: 'forwards' });
        sai.onfinish = function () { voo.remove(); vooAtivo = false; };
      });
    };
  }
  app.addEventListener('click', function (e) {
    var c = e.target.closest('a.card');
    if (!c || e.metaKey || e.ctrlKey || e.shiftKey || e.button > 0) return;
    e.preventDefault();
    abrirCard(c, c.getAttribute('href'));
  });

  function abrirCarrinho() {""")

troca("""  function rota() {
    Cinema.transicao(desenha);
  }""", """  function rota() {
    if (pularTransicao) { pularTransicao = false; desenha(); return; }
    Cinema.transicao(desenha);
  }""")
open(A, 'w', encoding='utf8').write(s)
print('card voo ok')
