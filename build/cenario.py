"""Silhuetas do cenário do loading (montanhas e árvores), em tiles que repetem sem emenda.
Gera build/cenario.css com as camadas de paralaxe."""
import math, random
from urllib.parse import quote

def tile_svg(w, h, body, defs=''):
    s = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" preserveAspectRatio="none"><defs>{defs}</defs>{body}</svg>'
    return 'url("data:image/svg+xml,' + quote(s, safe=' =:/,;()-.') + '")'

def grad(id_, a, b):
    return f'<linearGradient id="{id_}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{a}"/><stop offset="1" stop-color="{b}"/></linearGradient>'

def montanhas(w, h, seed, picos, base, amp, cor_a, cor_b):
    rnd = random.Random(seed)
    # soma de senos periódicos no tile: emenda perfeita
    harm = [(k, rnd.uniform(0, 2 * math.pi), rnd.uniform(.3, 1) / k ** .8) for k in picos]
    tot = sum(a for _, _, a in harm)
    pts = []
    for x in range(0, w + 1, 6):
        t = 2 * math.pi * x / w
        tri = lambda u: 1 - 2 * abs((u / (2 * math.pi)) % 1 - .5)              # onda triangular: picos retos
        v = sum(a * tri(k * t + p) ** 1.6 for k, p, a in harm) / tot
        pts.append(f'{x},{h - base - amp * v:.1f}')
    d = f'M0,{h} L' + ' L'.join(pts) + f' L{w},{h} Z'
    return tile_svg(w, h, f'<path d="{d}" fill="url(#g)"/>', grad('g', cor_a, cor_b))

def arvores(w, h, seed, cor_a, cor_b):
    rnd = random.Random(seed)
    body = ''
    x = 14
    while x < w - 30:
        alt = rnd.uniform(.45, 1) * (h - 6)
        larg = alt * rnd.uniform(.34, .44)
        tiers = 3 if alt > h * .6 else 2
        for i in range(tiers):
            top = h - alt + i * alt * .26
            bot = h - alt * (.30 if i < tiers - 1 else .06) + i * alt * .05
            lw = larg * (.55 + .45 * (i + 1) / tiers)
            body += f'<path d="M{x:.1f},{top:.1f} L{x + lw / 2:.1f},{bot:.1f} L{x - lw / 2:.1f},{bot:.1f} Z"/>'
        body += f'<rect x="{x - 2.5:.1f}" y="{h - alt * .08:.1f}" width="5" height="{alt * .08 + 1:.1f}"/>'
        x += larg * rnd.uniform(.55, 1.6) + (rnd.uniform(20, 90) if rnd.random() < .3 else 0)
    body = f'<g fill="url(#g)">{body}</g><rect x="0" y="{h - 3}" width="{w}" height="3" fill="{cor_b}"/>'
    return tile_svg(w, h, body, grad('g', cor_a, cor_b))

camadas = [
    # nome, imagem, altura da camada, largura do tile (cqw), segundos por tile, opacidade
    ('sl-mt1', montanhas(1200, 300, 7, [1, 2, 3, 7, 13], 30, 250, '#24376E', '#172550'), '92%', 95, 48, .9),
    ('sl-mt2', montanhas(1000, 240, 3, [2, 3, 5, 11], 8, 190, '#16244C', '#0E1938'), '62%', 70, 15, 1),
    ('sl-arv', arvores(700, 160, 11, '#0A1330', '#050A1A'), '34%', 46, 1.15, 1),
]
css = '.sl-scene{position:absolute;inset:0 0 2px 0;overflow:hidden;pointer-events:none}\n'
css += '.sl-scene i{position:absolute;left:0;right:0;bottom:0;background-repeat:repeat-x;background-position:0 100%}\n'
for nome, img, alt, tw, seg, op in camadas:
    css += (f'.sl-scene .{nome}{{height:{alt};background-image:{img};background-size:{tw}cqw 100%;opacity:{op};'
            f'animation:{nome} {seg}s linear infinite}}\n'
            f'@keyframes {nome}{{to{{background-position:-{tw}cqw 100%}}}}\n')
open('build/cenario.css', 'w').write(css)
print(len(css) // 1024, 'KB')
