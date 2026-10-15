"""Menos espera, mesmo visual:
- catalogo.json começa a baixar junto com o HTML (preload) e sem as descrições
- descrições em descricoes.json, baixadas em segundo plano depois que a página abre
- lista grande de produtos desenhada em duas etapas (primeiro o que aparece na tela)
- fontes do Google não bloqueiam o primeiro desenho
- toque no menu navega em 160 ms (era 320–340 ms)
Pode rodar de novo sem problema; o build/catalogo.py chama a parte do catálogo no fim."""
import json, os, re

def patch(arq, pares):
    s = open(arq, encoding='utf8').read()
    for a, b in pares:
        if a not in s and (not b or b in s): continue
        assert a in s, (arq, a[:90])
        s = s.replace(a, b, 1)
    open(arq, 'w', encoding='utf8').write(s)

# ---------- catálogo sem descrições ----------
def separa_descricoes():
    d = json.load(open('site/catalogo.json', encoding='utf8'))
    desc = {p['h']: p.pop('desc') for p in d['produtos'] if p.get('desc')}
    for p in d['produtos']: p.pop('desc', None)
    if desc or not os.path.exists('site/descricoes.json'):
        json.dump(desc, open('site/descricoes.json', 'w', encoding='utf8'), ensure_ascii=False, separators=(',', ':'))
    json.dump(d, open('site/catalogo.json', 'w', encoding='utf8'), ensure_ascii=False, separators=(',', ':'))

separa_descricoes()
if os.environ.pop('SO_CATALOGO', None) == '1':  # chamado pelo build/catalogo.py: só o catálogo
    raise SystemExit

patch('build/catalogo.py', [("""print(len(out), 'produtos;'""", """import os, runpy; os.environ['SO_CATALOGO'] = '1'
try: runpy.run_path('build/leve3.py')
except SystemExit: pass
print(len(out), 'produtos;'""")])

# ---------- app.js ----------
patch('site/app.js', [
    # catálogo: usa o preload (sem forçar revalidação dupla) e busca as descrições depois
    ("""  fetch('catalogo.json', { cache: 'no-cache' }).then(function (r) { return r.json(); }).then(function (d) {
    D = d; d.produtos.forEach(function (p) { porH[p.h] = p; });""",
     """  fetch('catalogo.json').then(function (r) { return r.json(); }).then(function (d) {
    D = d; d.produtos.forEach(function (p) { porH[p.h] = p; });
    if (window.requestIdleCallback) requestIdleCallback(carregaDescricoes, { timeout: 2500 }); else setTimeout(carregaDescricoes, 1200);"""),
    # descrição do produto: vem do arquivo separado (preenche quando chegar)
    ("""      (p.desc ? '<details class="acc"' + (window.innerWidth > 720 ? ' open' : '') + '><summary>Sobre o produto</summary><div class="desc">' + esc(p.desc) + '</div></details>' : '') +""",
     """      '<details class="acc" id="acc-desc"' + (window.innerWidth > 720 ? ' open' : '') + (DESC && DESC[p.h] ? '' : ' hidden') + '><summary>Sobre o produto</summary><div class="desc" id="desc-txt">' + (DESC && DESC[p.h] ? esc(DESC[p.h]) : '') + '</div></details>' +"""),
    ("""  function produto(h) {""",
     """  // descrições dos produtos: arquivo à parte, baixado em segundo plano
  var DESC = null, descPedido = null;
  function carregaDescricoes() {
    if (!descPedido) descPedido = fetch('descricoes.json').then(function (r) { return r.json(); }).then(function (d) {
      DESC = d;
      var m = /^#\\/p\\/(.+)/.exec(location.hash), box = $('#acc-desc');
      if (m && box && DESC[m[1]]) { $('#desc-txt').textContent = DESC[m[1]]; box.hidden = false; }
    }).catch(function () { descPedido = null; });
    return descPedido;
  }
  function produto(h) {
    if (!DESC) carregaDescricoes();"""),
    # lista grande: primeiro o que aparece na tela, o resto no quadro seguinte
    ("""      var g = $('#lista');
      g.innerHTML = l.length ? l.map(card).join('') :""",
     """      var g = $('#lista'), PRIMEIROS = 12, resto = null;
      clearTimeout(g._resto);
      if (l.length > PRIMEIROS) {
        resto = l.slice(PRIMEIROS);
        var fila = resto.slice();
        (function lote() {  // 24 cards por vez, um lote por quadro: o toque nunca espera
          g._resto = setTimeout(function () {
            if (!g.isConnected || !fila.length) return;
            var antes = g.children.length;
            g.insertAdjacentHTML('beforeend', fila.splice(0, 24).map(card).join(''));
            if (animar) [].forEach.call(g.children, function (el, i) { if (i >= antes) el.style.setProperty('--i', 12); });
            else Cinema.scan(g.parentNode);
            if (fila.length) requestAnimationFrame(lote);
          }, 16);
        })();
        l = l.slice(0, PRIMEIROS);
      }
      g.innerHTML = l.length ? l.map(card).join('') :"""),
    ("""      $('#res-cont').textContent = l.length + (l.length === 1""", """      $('#res-cont').textContent = (l.length + (resto ? resto.length : 0)) + ((l.length + (resto ? resto.length : 0)) === 1"""),
    # toque no menu: navega mais cedo (a animação do toque continua igual)
    ("""    setTimeout(function () { a.classList.remove('clicado'); if (location.hash !== href) location.hash = href; }, Cinema.calmo ? 0 : 320);""",
     """    setTimeout(function () { if (location.hash !== href) location.hash = href; }, Cinema.calmo ? 0 : 160);
    setTimeout(function () { a.classList.remove('clicado'); }, Cinema.calmo ? 0 : 320);"""),
    ("""setTimeout(function () { fechar(function () { location.hash = link.getAttribute('href'); }); }, Cinema.calmo ? 0 : 340); }""",
     """setTimeout(function () { fechar(function () { location.hash = link.getAttribute('href'); }); }, Cinema.calmo ? 0 : 160); }"""),
])
# ---------- HTML: preload do catálogo e fontes sem bloquear ----------
def cabeca(s):
    if 'rel="preload" href="catalogo.json"' not in s:
        s = s.replace('<link rel="preconnect" href="https://cdn.shopify.com">',
                      '<link rel="preload" href="catalogo.json" as="fetch" crossorigin>\n<link rel="preconnect" href="https://cdn.shopify.com">', 1)
    m = re.search(r'<link rel="stylesheet" href="(https://fonts\.googleapis\.com/css2[^"]+)">', s)
    if m and 'rel="preload" as="style"' not in s:
        u = m.group(1)
        s = s.replace(m.group(0), '<link rel="preload" as="style" href="' + u + '" onload="this.onload=null;this.rel=\'stylesheet\'">\n<noscript><link rel="stylesheet" href="' + u + '"></noscript>', 1)
    return s
_h = cabeca(open('site/index.html', encoding='utf8').read())  # lê antes de abrir para escrita
open('site/index.html', 'w', encoding='utf8').write(_h)
s = open('build/leve2.py', encoding='utf8').read()
if 'leve3' not in s:
    s = s.replace("print('leve2 ok')", "import runpy as _r; _r.run_path('build/leve3.py')\nprint('leve2 ok')")
    open('build/leve2.py', 'w', encoding='utf8').write(s)
print('leve3 ok')
