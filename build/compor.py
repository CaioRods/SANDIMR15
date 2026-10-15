"""Monta os SVGs finais do logo a partir de build/paths.json (gerado por vetorizar.py).
Preto fosco e azul com degradê vertical leve."""
import json
P = json.load(open('build/paths.json'))

# degradês leves (topo -> base)
GRAD = {
    'preto':  ('#30333B', '#1A1C21'),   # preto fosco / grafite
    'azul':   ('#1AA6F2', '#0086D1'),   # azul Sandim
    'branco': ('#FFFFFF', '#DDE4EF'),   # para fundo escuro
    'azulc':  ('#4CBDFF', '#169BEF'),   # azul em fundo escuro
}
def lg(id_, cores):
    a, b = cores
    return f'<linearGradient id="{id_}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{a}"/><stop offset="1" stop-color="{b}"/></linearGradient>'
DEFS = '<defs>' + ''.join(lg('sg-' + k, v) for k, v in GRAD.items()) + '</defs>'

def g(names, fill):
    return ''.join(f'<path fill="{fill}" d="{d}" transform="translate({x},{y})"/>' for n in names for d, x, y in P[n])
def svg(vb, parts, bg=None):
    rect = f'<rect x="-100" y="-100" width="2400" height="900" fill="{bg}"/>' if bg else ''
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}">{DEFS}{rect}<g transform="scale(.5)">{parts}</g></svg>\n'

FULL = '0 0 2000 667'; MOTO = '570 18 1050 425'; TXT = '238 395 1735 270'
K, B, W, BC = 'url(#sg-preto)', 'url(#sg-azul)', 'url(#sg-branco)', 'url(#sg-azulc)'
out = {
    'logo-cores.svg':     svg(FULL, g(['speed', 'btext', 'stripe'], B) + g(['bike', 'text'], K)),
    'logo-negativo.svg':  svg(FULL, g(['speed', 'btext', 'stripe'], BC) + g(['bike', 'text'], W)),
    'logo-grafite.svg':   svg(FULL, g(['speed', 'btext', 'stripe', 'bike', 'text'], K)),
    'logo-branco.svg':    svg(FULL, g(['speed', 'btext', 'stripe', 'bike', 'text'], '#FFFFFF')),
    'moto-cores.svg':     svg(MOTO, g(['stripe'], B) + g(['bike'], K)),
    'moto-negativo.svg':  svg(MOTO, g(['stripe'], BC) + g(['bike'], W)),
    'texto-cores.svg':    svg(TXT, g(['btext'], B) + g(['text'], K)),
    'texto-negativo.svg': svg(TXT, g(['btext'], BC) + g(['text'], W)),
}
for f, s in out.items():
    open('logo/' + f, 'w').write(s)

# símbolos para as páginas HTML: cores por variável CSS (--k corpo, --b azul)
def gv(names, var):
    return f'<g style="fill:var({var})">' + ''.join(f'<path d="{d}" transform="translate({x},{y})"/>' for n in names for d, x, y in P[n]) + '</g>'
sym = ('<svg width="0" height="0" style="position:absolute" aria-hidden="true">' + DEFS + '<defs>'
       f'<symbol id="lg-moto" viewBox="{MOTO}"><g transform="scale(.5)">' + gv(['stripe'], '--b') + gv(['bike'], '--k') + '</g></symbol>'
       f'<symbol id="lg-texto" viewBox="{TXT}"><g transform="scale(.5)">' + gv(['btext'], '--b') + gv(['text'], '--k') + '</g></symbol>'
       f'<symbol id="lg-speed" viewBox="{FULL}"><g transform="scale(.5)">' + gv(['speed'], '--b') + '</g></symbol>'
       f'<symbol id="logo" viewBox="{FULL}"><use href="#lg-speed" x="0" y="0" width="2000" height="667"/>'
       '<use href="#lg-moto" x="570" y="18" width="1050" height="425"/><use href="#lg-texto" x="238" y="395" width="1735" height="270"/></symbol>'
       '</defs></svg>')
open('build/simbolos.html', 'w').write(sym)

import sys; sys.path.insert(0,'build'); from rodas import rodas
TREAD = rodas()
src = open('build/identidade.src.html', encoding='utf8').read()
page = (src.replace('{{SIMBOLOS}}', sym).replace('{{LOADER_CSS}}', open('build/loader.css', encoding='utf8').read())
           .replace('{{TREAD}}', ''))
import loader_svg as LS
page = page.replace('{{RIDER}}', LS.rider(LS.moto_svg())).replace('{{FILTROS}}', LS.FILTROS).replace('{{CENA}}', LS.cenario()).replace('{{RUSH}}', LS.rush())
# tokens de cor das instâncias -> degradês
page = (page.replace('--k:#F2F5FA;--b:#1EA7FF', '--k:url(#sg-branco);--b:url(#sg-azulc)')
            .replace('--k:#000;--b:#0093E2', '--k:url(#sg-preto);--b:url(#sg-azul)')
            .replace('--k:#000;--b:#000', '--k:url(#sg-preto);--b:url(#sg-preto)'))
open('identidade.html', 'w', encoding='utf8').write(page)
print('ok', len(page) // 1024, 'KB')
