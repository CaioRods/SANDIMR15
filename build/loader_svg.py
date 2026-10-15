"""Vetoriza corpo e roda do loading e monta o SVG da moto com rodas girando."""
import re, json, vtracer
S = 0.84
def trace(png):
    out = png.replace('.png', '.svg')
    vtracer.convert_image_to_svg_py(png, out, colormode='binary', mode='spline', filter_speckle=8,
                                    corner_threshold=70, length_threshold=4.0, splice_threshold=45, path_precision=1)
    return re.findall(r'<path d="([^"]+)"[^>]*?transform="translate\(([-\d.]+),([-\d.]+)\)"', open(out).read())
P = json.load(open('build/paths.json'))
corpo = trace('build/corpo-loader.png')
roda = trace('build/roda-completa.png')
N = 674                                   # lado da imagem da roda (2x)
FRONT = (1442.6, 441.7); REAR = (784.4, 441.7)
VB = '570 18 1050 566'
def paths(lst): return ''.join(f'<path d="{d}" transform="translate({x},{y})"/>' for d, x, y in lst)

def roda_symbol():
    return f'<symbol id="sl-roda" viewBox="0 0 {N} {N}">{paths(roda)}</symbol>'
def rodas(fill):
    h = N / 2; k = 0.5 * S
    g = ''
    for cx, cy in (REAR, FRONT):
        g += (f'<g transform="translate({cx - h * k:.1f},{cy - h * k:.1f}) scale({k})"><g class="sl-spin" style="fill:{fill}">'
              f'<circle cx="{h}" cy="{h}" r="{h}" fill="none"/>'
              f'<use href="#sl-roda" width="{N}" height="{N}" opacity=".28" transform="rotate(-14 {h} {h})"/>'
              f'<use href="#sl-roda" width="{N}" height="{N}" opacity=".45" transform="rotate(-7 {h} {h})"/>'
              f'<use href="#sl-roda" width="{N}" height="{N}"/></g></g>')
    return g
def corpo_g(k, b):
    return (f'<g transform="scale(.5)"><g style="fill:{b}">{paths(P["stripe"])}</g>'
            f'<g style="fill:{k}">{paths(corpo)}</g></g>')
def moto_svg(k='url(#sg-branco)', b='url(#sg-azulc)', roda_fill='url(#sg-branco)', defs=''):
    return (f'<svg class="sl-moto" viewBox="{VB}" aria-hidden="true"><defs>{defs}{roda_symbol()}</defs>'
            f'{rodas(roda_fill)}{corpo_g(k, b)}</svg>')
if __name__ == '__main__':
    s = moto_svg('#FFFFFF', '#1EA7FF', '#FFFFFF')
    print(len(s) // 1024, 'KB')

def _filtro(id_, rastros, nitidez):
    """rastros: (blur_x, deslocamento, opacidade). Rastro azul translúcido feito da silhueta, não do branco."""
    f = f'<filter id="{id_}" x="-90%" y="-8%" width="195%" height="116%" color-interpolation-filters="sRGB">'
    nodes = ''
    for n, (bx, dx, a) in enumerate(rastros):
        f += (f'<feGaussianBlur in="SourceAlpha" stdDeviation="{bx} 1" result="b{n}"/>'
              f'<feOffset in="b{n}" dx="{-dx}" result="o{n}"/>'
              f'<feFlood flood-color="#3BB0FF" flood-opacity="{a}" result="c{n}"/>'
              f'<feComposite in="c{n}" in2="o{n}" operator="in" result="f{n}"/>')
        nodes += f'<feMergeNode in="f{n}"/>'
    f += f'<feGaussianBlur in="SourceGraphic" stdDeviation="{nitidez} 0" result="s"/>'
    return f + f'<feMerge>{nodes}<feMergeNode in="s"/></feMerge></filter>'

FILTROS = ('<svg width="0" height="0" style="position:absolute" aria-hidden="true">'
  + _filtro('sl-mb-3', [(34, 120, .16), (18, 64, .24), (8, 26, .32)], 2.2)
  + _filtro('sl-mb-2', [(18, 62, .14), (8, 24, .24)], 1.2)
  + _filtro('sl-mb-1', [(7, 18, .16)], .5)
  + '</svg>')

def rush():
    return '<div class="sl-rush">' + '<i></i>' * 9 + '</div>'

def cenario():
    return '<div class="sl-scene"><i class="sl-mt1"></i><i class="sl-mt2"></i><i class="sl-arv"></i></div>'

def rider(moto):
    return ('<div class="sl-rider"><div class="sl-lines sl-solto"><i></i><i></i><i></i></div>'
            '<div class="sl-tilt"><div class="sl-lines sl-preso"><i></i><i></i></div>'
            f'<div class="sl-bike">{moto}</div></div></div>')

def arquivo_corpo():
    """SVG do corpo (sem rodas) para subir nos Assets do Shopify."""
    defs = ('<defs><linearGradient id="k" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFFFFF"/><stop offset="1" stop-color="#DDE4EF"/></linearGradient>'
            '<linearGradient id="b" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#4CBDFF"/><stop offset="1" stop-color="#169BEF"/></linearGradient></defs>')
    open('logo/moto-loading-corpo.svg', 'w').write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{VB}">{defs}{corpo_g("url(#k)", "url(#b)")}</svg>\n')

def moto_shopify(src):
    return (f'<svg class="sl-moto" viewBox="{VB}" aria-hidden="true"><defs>{roda_symbol()}</defs>{rodas("#EEF2F8")}</svg>'
            f'<img class="sl-corpo" src="{src}" alt="" width="1050" height="566">')
