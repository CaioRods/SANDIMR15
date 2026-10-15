"""Página mais leve, mesmo visual: revelação em cascata por lote, rolagem e brilho a 1x por quadro,
imagens decodificadas fora da thread principal, catálogo compactado."""
import json

def patch(arq, pares):
    s = open(arq, encoding='utf8').read()
    for a, b in pares:
        if b in s and a not in s: continue
        assert a in s, (arq, a[:80])
        s = s.replace(a, b, 1)
    open(arq, 'w', encoding='utf8').write(s)

# ---------- cinema.js ----------
patch('site/cinema.js', [
    # observador: o que entra junto na tela anima em sequência (de cima p/ baixo, esquerda p/ direita)
    ("""      io = new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) revela(e.target); }); }, { rootMargin: '0px 0px -8% 0px', threshold: .08 });""",
     """      io = new IntersectionObserver(function (es) {
        lote(es.filter(function (e) { return e.isIntersecting; }).map(function (e) { return { el: e.target, r: e.boundingClientRect }; }));
      }, { rootMargin: '0px 0px -8% 0px', threshold: .08 });"""),
    ("""    var altura = window.innerHeight;
    ALVOS.forEach(function (par) {
      $$(par[0], raiz).forEach(function (el) {
        if (el.classList.contains('rv')) return;
        var pai = el.parentElement, irmaos = pai ? Array.prototype.indexOf.call(pai.children, el) : 0;
        el.style.setProperty('--i', Math.min(irmaos, 8));
        el.classList.add('rv'); if (par[1]) el.classList.add(par[1]);
        var r = el.getBoundingClientRect();
        // o que já está na tela entra logo (sem esperar o observador)
        if (r.top < altura * .92 && r.bottom > 0) requestAnimationFrame(function () { requestAnimationFrame(function () { revela(el); }); });
        else if (io) io.observe(el);
        else revela(el);
      });
    });
    // garantia: nada fica invisível se o observador não disparar
    clearTimeout(scan._t);
    scan._t = setTimeout(function () { $$('.rv:not(.rv-in)').forEach(function (el) { if (el.getBoundingClientRect().top < window.innerHeight) revela(el); }); }, 1800);""",
     """    var altura = window.innerHeight, novos = [], naTela = [];
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
    }, 1800);"""),
    ("""  function revela(el) { el.classList.add('rv-in'); if (io) io.unobserve(el); contar(el); }""",
     """  function revela(el) { el.classList.add('rv-in'); if (io) io.unobserve(el); contar(el); }
  // cascata ordenada: posição na tela define a ordem; o atraso recomeça a cada lote
  function lote(itens) {
    itens.sort(function (a, b) { return Math.abs(a.r.top - b.r.top) > 12 ? a.r.top - b.r.top : a.r.left - b.r.left; });
    itens.forEach(function (x, k) { x.el.style.setProperty('--i', Math.min(k, 8)); revela(x.el); });
  }"""),
    # brilho que segue o mouse: no máximo 1 atualização por quadro
    ("""  document.addEventListener('pointermove', function (e) {
    var c = e.target.closest && e.target.closest('.card'); if (!c) return;
    var r = c.getBoundingClientRect();
    c.style.setProperty('--mx', (e.clientX - r.left) + 'px'); c.style.setProperty('--my', (e.clientY - r.top) + 'px');
  }, { passive: true });""",
     """  var brilho = null;
  document.addEventListener('pointermove', function (e) {
    if (e.pointerType !== 'mouse') return;
    var c = e.target.closest && e.target.closest('.card'); if (!c) return;
    var pend = !!brilho; brilho = { c: c, x: e.clientX, y: e.clientY }; if (pend) return;
    requestAnimationFrame(function () {
      var b = brilho; brilho = null; var r = b.c.getBoundingClientRect();
      b.c.style.setProperty('--mx', (b.x - r.left) + 'px'); b.c.style.setProperty('--my', (b.y - r.top) + 'px');
    });
  }, { passive: true });"""),
])

# ---------- app.js ----------
patch('site/app.js', [
    # rolagem: 1x por quadro e só mede o cabeçalho quando ele muda de estado
    ("""  window.addEventListener('scroll', function () { hdr.classList.toggle('min', window.scrollY > 80); altHdr(); if (checaBuy) checaBuy(); }, { passive: true });""",
     """  var rolou = false;
  window.addEventListener('scroll', function () {
    if (rolou) return; rolou = true;
    requestAnimationFrame(function () {
      rolou = false;
      // folga maior que a diferença de altura do cabeçalho (≈50px): evita o pisca-pisca ao rolar perto do limite
      var min = hdr.classList.contains('min') ? window.scrollY > 20 : window.scrollY > 120;
      if (min !== hdr.classList.contains('min')) { hdr.classList.toggle('min', min); altHdr(); }
      if (checaBuy) checaBuy();
    });
  }, { passive: true });
  hdr.addEventListener('transitionend', function (e) { if (e.target === hdr || e.target.parentNode === hdr) altHdr(); });"""),
    # fotos dos cards decodificam fora da thread principal
    ("""<div class="ft"><img loading="lazy" src="' + img(p.img[0], 500) + '\"""",
     """<div class="ft"><img loading="lazy" decoding="async" src="' + img(p.img[0], 500) + '\""""),
    ("""'<img class="alt" loading="lazy" src="' + img(p.img[1], 500) + '" alt="">'""",
     """'<img class="alt" loading="lazy" decoding="async" src="' + img(p.img[1], 500) + '" alt="">'"""),
])

# ---------- catálogo sem espaços ----------
d = json.load(open('site/catalogo.json', encoding='utf8'))
json.dump(d, open('site/catalogo.json', 'w', encoding='utf8'), ensure_ascii=False, separators=(',', ':'))
patch('build/catalogo.py', [("""open('site/catalogo.json', 'w', encoding='utf8'), ensure_ascii=False)""",
                             """open('site/catalogo.json', 'w', encoding='utf8'), ensure_ascii=False, separators=(',', ':'))""")])
print('leve ok')
