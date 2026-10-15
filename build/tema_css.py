"""Monta tema/assets/sandim.css: estilo do protótipo + loading + ajustes do tema."""
css = open('site/estilo.css', encoding='utf8').read()
troca = {
    '.logo svg{height:58px;width:auto;display:block}': '',
    '.logo svg{height:44px}': '',
    '.hdr .logo svg{transition:height .2s}': '',
    '.hdr.min .logo svg{height:34px}': '',
    '.moto-card svg{position:absolute;right:-6%;bottom:-6%;width:62%;opacity:.12}': '',
    '.moto-card.r15 svg{opacity:.22}': '',
    '.hero-moto svg{width:100%;height:auto;display:block;filter:drop-shadow(0 18px 30px rgba(0,0,0,.45))}': '',
    '.canal .visual svg{width:100%;height:auto;opacity:.95}': '',
    '.rod-marca svg{width:230px;height:auto;margin-bottom:12px}': '',
    '.rod-marca svg{width:230px;height:auto;margin-bottom:18px}': '',
}
for a, b in troca.items():
    css = css.replace(a, b)
# no tema o botão de carrinho do topo some no celular (a barra inferior assume)
loader = open('build/loader.css', encoding='utf8').read()
extra = open('build/tema-extra.css', encoding='utf8').read()
saida = '/* Sandim R15 · tema Shopify · CRdevs */\n' + css + '\n/* ===== loading ===== */\n' + loader + extra
open('tema/assets/sandim.css', 'w', encoding='utf8').write(saida)
print('sandim.css', len(saida) // 1024, 'KB')
