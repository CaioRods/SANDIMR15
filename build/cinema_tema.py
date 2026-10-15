"""Leva a camada cinematográfica para o tema Shopify."""
import json, shutil

def troca(caminho, a, b, obrig=True):
    s = open(caminho, encoding='utf8').read()
    if b in s and a not in s:
        return
    if a not in s:
        if obrig: raise SystemExit(f'não achei em {caminho}: {a[:70]}')
        return
    open(caminho, 'w', encoding='utf8').write(s.replace(a, b))

# cinema.js vai como asset próprio, carregado antes do sandim.js
shutil.copy('site/cinema.js', 'tema/assets/cinema.js')
troca('tema/layout/theme.liquid', """    <script src="{{ 'sandim.js' | asset_url }}" defer></script>""",
      """    <script src="{{ 'cinema.js' | asset_url }}" defer></script>
    <script src="{{ 'sandim.js' | asset_url }}" defer></script>""")

# loading em cartão no centro
troca('build/tema_loader.py', """'<div class="sl-stage" id="sandim-loader" aria-hidden="true">'""", """'<div class="sl-overlay" id="sandim-loader" aria-hidden="true"><div class="sl-stage">'""")
troca('build/tema_loader.py', """'<div class="sl-word"><img src="' + texto + '" alt="" width="1735" height="270"><div class="sl-bar"><i></i></div></div>'
        '</div>\\n'""", """'<div class="sl-word"><img src="' + texto + '" alt="" width="1735" height="270"><div class="sl-bar"><i></i></div></div>'
        '</div></div>\\n'""")
troca('build/tema-extra.css', """#sandim-loader{position:fixed;inset:0;z-index:999;transition:opacity .45s ease,visibility 0s linear .45s}
#sandim-loader.is-done{opacity:0;visibility:hidden}
""", '')

# CSS do tema passa a incluir o cinema.css
troca('build/tema_css.py', """extra = open('build/tema-extra.css', encoding='utf8').read()""",
      """extra = open('build/tema-extra.css', encoding='utf8').read() + '\\n' + open('site/cinema.css', encoding='utf8').read()""")

# produto: contador de fotos e descrição recolhível
troca('tema/sections/main-product.liquid', """      <div class="principal">
        <div class="trilho" data-trilho>""", """      <div class="principal">
        {%- if product.media.size > 1 -%}<span class="foto-cont" data-foto-cont>1 / {{ product.media.size }}</span>{%- endif -%}
        <div class="trilho" data-trilho>""")
troca('tema/sections/main-product.liquid', """        <div class="desc-box"><h2>Sobre o produto</h2><div class="desc rte">{{ product.description }}</div></div>""",
      """        <details class="acc" data-acc-desktop><summary>Sobre o produto</summary><div class="desc rte">{{ product.description }}</div></details>""")

# home: letreiro depois dos benefícios
p = 'tema/templates/index.json'; d = json.load(open(p, encoding='utf8'))
if 'letreiro' not in d['sections']:
    d['sections']['letreiro'] = {"type": "letreiro", "settings": {"itens": "R15, R3, Frete grátis, 12x no cartão, Testado no canal", "velocidade": 28}}
    d['order'].insert(d['order'].index('beneficios') + 1, 'letreiro')
json.dump(d, open(p, 'w', encoding='utf8'), ensure_ascii=False, indent=2)
print('tema: cinema ok')
