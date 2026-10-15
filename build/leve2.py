"""Página mais leve (mesmo visual):
- a moto do banner é gerada a partir da moto do carregamento (era uma cópia de ~78 KB no HTML)
- sai do HTML o que o carregamento novo não usa (montanhas, pinheiros, rastros, filtros de desfoque)
- fotos dos cards com srcset (celular baixa a menor que serve)
- pré-conexão com os servidores de imagem
Roda sozinho no fim do build/site.py; pode rodar de novo sem problema."""
import re

def patch(arq, pares):
    s = open(arq, encoding='utf8').read()
    for a, b in pares:
        if a not in s and (not b or b in s): continue
        assert a in s, (arq, a[:90])
        s = s.replace(a, b, 1)
    open(arq, 'w', encoding='utf8').write(s)

# ---------- app.js ----------
patch('site/app.js', [
    ("""  /* ---------- loading ---------- */
  var loader = document.getElementById('sandim-loader'), loaderAcabou = false;""",
     """  /* ---------- loading ---------- */
  var loader = document.getElementById('sandim-loader'), loaderAcabou = false;
  // moto do banner = moto do carregamento com as cores do site (lida antes do carregamento sair da página)
  var MOTO = (function () {
    var s = loader && loader.querySelector('.sl-moto'); if (!s) return '';
    return s.outerHTML.replace(/sl-roda/g, 'hero-roda').replace(/url\\(#sg-branco\\)/g, 'url(#sg-preto)').replace(/url\\(#sg-azulc\\)/g, 'url(#sg-azul)');
  })();"""),
    ("""    var moto = $('#moto-completa') ? $('#moto-completa').innerHTML : motoSvg('url(#sg-branco)', 'url(#sg-azulc)');""",
     """    var moto = MOTO || motoSvg('url(#sg-branco)', 'url(#sg-azulc)');"""),
    # fotos dos cards: o celular baixa a de 360 px quando basta
    ("""<div class="ft"><img loading="lazy" decoding="async" src="' + img(p.img[0], 500) + '\"""",
     """<div class="ft"><img loading="lazy" decoding="async" src="' + img(p.img[0], 500) + '" srcset="' + img(p.img[0], 360) + ' 360w, ' + img(p.img[0], 500) + ' 500w" sizes="(max-width:720px) 46vw, 240px\""""),
])

# ---------- HTML (fonte do build e página gerada) ----------
def enxuga(s):
    # cópia da moto (agora gerada pelo app.js)
    s = re.sub(r'<template id="moto-completa">.*?</template>\n?', '', s, flags=re.S)
    s = s.replace('<template id="moto-completa">{{MOTO_COMPLETA}}</template>\n', '').replace('<template id="moto-completa">{{MOTO_COMPLETA}}</template>', '')
    # filtros de desfoque de movimento (não usados mais)
    s = re.sub(r'<svg width="0" height="0" style="position:absolute" aria-hidden="true"><filter id="sl-mb-3".*?</svg>\n?', '', s, flags=re.S)
    s = s.replace('{{FILTROS}}\n', '').replace('{{FILTROS}}', '')
    # cenário do carregamento: montanhas, pinheiros, rastros e linhas de velocidade
    s = re.sub(r'<div class="sl-scene">.*?</div>(?=<div class="sl-road">)', '', s, flags=re.S)
    s = re.sub(r'<div class="sl-rush">(?:<i></i>)+</div>', '', s)
    s = s.replace('<div class="sl-lines sl-solto"><i></i><i></i><i></i></div>', '').replace('<div class="sl-lines sl-preso"><i></i><i></i></div>', '')
    s = re.sub(r'(?m)^\.sl-scene[^\n]*\n?', '', s)
    s = re.sub(r'(?m)^\[data-spd="\d"\] \.sl-(?:bike|rush)\{[^\n]*\n?', '', s)
    s = re.sub(r'(?m)^\.sl-rush[^\n]*\n?', '', s)
    s = s.replace('.sl-rush{display:none}', '')
    s = re.sub(r'(?m)^@keyframes sl-rush[^\n]*\n?', '', s)
    s = re.sub(r'(?m)^@keyframes sl-(?:mt1|mt2|arv)\{[^\n]*\n?', '', s)
    # pré-conexão com as imagens (Shopify CDN e loja)
    if 'cdn.shopify.com" crossorigin' not in s and 'preconnect" href="https://cdn.shopify.com' not in s:
        s = s.replace('<link rel="preconnect" href="https://fonts.googleapis.com">',
                      '<link rel="preconnect" href="https://cdn.shopify.com">\n<link rel="preconnect" href="https://sandimr15.store">\n<link rel="preconnect" href="https://fonts.googleapis.com">', 1)
    return s

s = open('site/index.html', encoding='utf8').read()
open('site/index.html', 'w', encoding='utf8').write(enxuga(s))
# fonte do build: só sai a cópia da moto (os demais marcadores continuam e são enxugados na página gerada)
patch('build/site.src.html', [('<template id="moto-completa">{{MOTO_COMPLETA}}</template>\n', '')])

# build/site.py: não monta mais a cópia da moto e chama este enxugamento no fim
patch('build/site.py', [
    ("""    '{{MOTO_COMPLETA}}': LS.moto_svg('url(#sg-preto)', 'url(#sg-azul)', 'url(#sg-preto)').replace('sl-roda', 'hero-roda'),\n""", ""),
])
s = open('build/site.py', encoding='utf8').read()
if 'leve2' not in s:
    s = s.replace("print('site ok'", "import runpy; runpy.run_path('build/leve2.py')\nprint('site ok'", 1)
    open('build/site.py', 'w', encoding='utf8').write(s)
import runpy as _r; _r.run_path('build/leve3.py')
print('leve2 ok')
