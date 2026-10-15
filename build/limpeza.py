"""Passada de limpeza visual do protótipo: loading em tela cheia, cabeçalho centralizado no celular,
cards só com foto/nome/preço, banner mais limpo e home com menos blocos."""

def troca(caminho, a, b):
    s = open(caminho, encoding='utf8').read()
    if a not in s:
        if b in s: return
        raise SystemExit(f'não achei em {caminho}: {a[:80]}')
    open(caminho, 'w', encoding='utf8').write(s.replace(a, b, 1))

T = 'build/site.src.html'
# loading volta a ser tela cheia
troca(T, '<div class="sl-overlay" id="sandim-loader" aria-hidden="true"><div class="sl-stage">', '<div class="sl-stage" id="sandim-loader" aria-hidden="true">')
troca(T, '<div class="sl-bar"><i></i></div></div>\n</div></div>', '<div class="sl-bar"><i></i></div></div>\n</div>')
# cabeçalho: botão de busca no celular
troca(T, '''      <a class="icon-btn hide-sm" href="#/pagina/rastreio" aria-label="Rastrear pedido">''',
      '''      <button class="icon-btn busca-btn" id="abrir-busca" type="button" aria-label="Buscar" aria-expanded="false"><svg viewBox="0 0 24 24"><circle cx="11" cy="11" r="7"/><path d="m20 20-4-4"/></svg></button>
      <a class="icon-btn hide-sm" href="#/pagina/rastreio" aria-label="Rastrear pedido">''')
# faixa do topo mais curta
troca(T, '<div class="topline"><span>Frete grátis<span class="hide-sm"> para todo o Brasil</span></span><span class="dot">·</span><span><b>12x</b> no cartão</span><span class="dot hide-sm">·</span><span class="hide-sm">Envio com rastreio</span></div>',
      '<div class="topline"><span>Frete grátis para todo o Brasil</span><span class="dot hide-sm">·</span><span class="hide-sm"><b>12x</b> no cartão</span></div>')

A = 'site/app.js'
# card limpo: foto, nome, preço
s = open(A, encoding='utf8').read()
i = s.index('  function card(p) {'); j = s.index('  function daColecao(h) {')
s = s[:i] + r"""  function card(p) {
    var o = pct(p);
    return '<a class="card" href="#/p/' + p.h + '"><div class="ft"><img loading="lazy" src="' + img(p.img[0], 500) + '" alt="' + esc(p.t) + '">' +
      (p.img[1] ? '<img class="alt" loading="lazy" src="' + img(p.img[1], 500) + '" alt="">' : '') +
      (o >= 10 ? '<span class="off">−' + o + '%</span>' : '') + '</div>' +
      '<div class="info"><span class="nome">' + esc(p.t) + '</span>' +
      '<span class="preco">' + (p.varia ? '<small>a partir de </small>' : '') + brl(p.preco) + '</span>' +
      '<span class="parc">12x de ' + brl(p.preco * COEF_12X) + '</span></div></a>';
  }
""" + s[j:]
open(A, 'w', encoding='utf8').write(s)

# banner: título, um botão e um link; sem parágrafo
troca(A, """      '<span class="eyebrow" style="color:var(--azul-claro)">Loja oficial do canal SandimR15</span>' +
      '<h1>Feito por quem <em>vive a R15.</em></h1><p>Acessórios para Yamaha R15 e R3 escolhidos e usados por quem anda com a moto todo dia. Frete grátis para todo o Brasil.</p>' +
      '<div class="ctas"><a class="btn" href="#/c/acessorios">Ver peças da R15</a><a class="btn claro" href="#/c/acessorios-r3">Linha R3</a></div></div>' +""",
      """      '<span class="eyebrow" style="color:var(--azul-claro)">Loja oficial do canal SandimR15</span>' +
      '<h1>Feito por quem <em>vive a R15.</em></h1>' +
      '<div class="ctas"><a class="btn" href="#/c/acessorios">Ver peças da R15</a><a class="link-r3" href="#/c/acessorios-r3">Linha R3 →</a></div></div>' +""")
# home: sem faixa de benefícios, sem letreiro, sem vitrine de kits, canal sem números
s = open(A, encoding='utf8').read()
i = s.index("      '<div class=\"beneficios\">' +"); j = s.index("      letreiro() +") + len("      letreiro() +\n")
s = s[:i] + s[j:]
s = s.replace("""      vitrine('Kits com desconto', 'Combinações prontas com preço especial', 'kits-com-desconto', 6, null, true) +\n""", '')
i = s.index("""      '<div class="num">"""); j = s.index("""      '<div class="ctas" style="display:flex;gap:12px;flex-wrap:wrap">""")
s = s[:i] + s[j:]
s = s.replace("""vitrine('Mais vendidos', 'O que mais sai para a R15 neste mês', 'mais-vendidos', 10, maisVend, true)""",
              """vitrine('Mais vendidos', '', 'mais-vendidos', 8, maisVend, true)""")
s = s.replace("""vitrine('Lançamentos', 'Acabou de chegar na loja', 'news', 10, null, true)""",
              """vitrine('Lançamentos', '', 'news', 8, null, true)""")
s = s.replace("""<span>' + r15 + ' acessórios · todos os anos</span>""", """<span>' + r15 + ' acessórios</span>""")
open(A, 'w', encoding='utf8').write(s)

# busca no celular abre/fecha pelo ícone e pela barra inferior
troca(A, """  $('#tab-busca').addEventListener('click', function () { fechar(); window.scrollTo({ top: 0, behavior: 'smooth' }); setTimeout(function () { $('#busca-q').focus(); }, 250); });""",
      """  function alternaBusca(abrirSempre) {
    var h = $('#topo'), aberta = abrirSempre || !h.classList.contains('busca-aberta');
    h.classList.toggle('busca-aberta', aberta); h.classList.remove('oculto');
    $('#abrir-busca').setAttribute('aria-expanded', aberta);
    if (aberta) setTimeout(function () { $('#busca-q').focus(); }, 60);
  }
  $('#abrir-busca').addEventListener('click', function () { alternaBusca(false); });
  $('#tab-busca').addEventListener('click', function () { fechar(); window.scrollTo({ top: 0, behavior: 'smooth' }); alternaBusca(true); });""")
troca(A, """    var q = $('#busca-q').value.trim(); if (q) location.hash = '#/busca/' + encodeURIComponent(q);""",
      """    var q = $('#busca-q').value.trim(); if (q) { $('#topo').classList.remove('busca-aberta'); $('#busca-q').blur(); location.hash = '#/busca/' + encodeURIComponent(q); }""")

# produto: garantias numa linha discreta
troca(A, """      '<div class="garantias"><div><svg viewBox="0 0 24 24"><path d="M3 7h11v9H3zM14 10h4l3 3v3h-7z"/><circle cx="7" cy="17.5" r="1.8"/><circle cx="17" cy="17.5" r="1.8"/></svg><span><b>Frete grátis</b> para todo o Brasil, com rastreio</span></div>' +
      '<div><svg viewBox="0 0 24 24"><path d="M12 3l8 3v6c0 4.5-3.4 8-8 9-4.6-1-8-4.5-8-9V6z"/><path d="m9 12 2 2 4-4"/></svg><span>Compra segura pelo checkout da Shopify</span></div>' +
      '<div><svg viewBox="0 0 24 24"><rect x="4" y="5" width="16" height="12" rx="2"/><path d="m10 9 5 2.5-5 2.5z"/></svg><span>Escolhido e testado por quem usa a R15 no canal</span></div></div>' +""",
      """      '<p class="garantia-linha"><svg viewBox="0 0 24 24"><path d="M3 7h11v9H3zM14 10h4l3 3v3h-7z"/><circle cx="7" cy="17.5" r="1.8"/><circle cx="17" cy="17.5" r="1.8"/></svg>Frete grátis para todo o Brasil · compra segura</p>' +""")
print('limpeza ok')
