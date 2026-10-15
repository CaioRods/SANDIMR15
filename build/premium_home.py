"""Nova home premium do protótipo + inclusão do premium.css."""
A = 'site/app.js'
s = open(A, encoding='utf8').read()
i = s.index('  function home() {'); j = s.index('  function colecao(h, q) {')
nova = r"""  function home() {
    var maisVend = daColecao('mais-vendidos');
    var conta = function (m) { return D.produtos.filter(function (p) { return p.moto.indexOf(m) > -1; }).length; };
    var moto = $('#moto-completa') ? $('#moto-completa').innerHTML : motoSvg('url(#sg-branco)', 'url(#sg-azulc)');
    var dest = daColecao('escapamentos')[0] || maisVend[0];
    var tamanhos = ['g', '', '', '', '', 'l', '', ''];
    var mosaico = CATS.slice(2).map(function (c, k) {
      var ps = daColecao(c.h); if (!ps.length) return '';
      return '<a class="mos ' + (tamanhos[k] || '') + '" href="#/c/' + c.h + '"><span class="ft"><img loading="lazy" src="' + img(ps[0].img[0], 500) + '" alt=""></span><b>' + c.n + '</b><small>' + ps.length + ' peças</small></a>';
    }).join('');
    var icone = {
      frete: '<svg viewBox="0 0 24 24"><path d="M3 7h11v9H3zM14 10h4l3 3v3h-7z"/><circle cx="7" cy="17.5" r="1.8"/><circle cx="17" cy="17.5" r="1.8"/></svg>',
      cartao: '<svg viewBox="0 0 24 24"><rect x="3" y="6" width="18" height="12" rx="2"/><path d="M3 10h18"/></svg>',
      escudo: '<svg viewBox="0 0 24 24"><path d="M12 3l8 3v6c0 4.5-3.4 8-8 9-4.6-1-8-4.5-8-9V6z"/><path d="m9 12 2 2 4-4"/></svg>'
    };
    return '<section class="hero">' + cena +
      '<div class="hero-in"><div class="hero-txt">' +
        '<span class="kicker eyebrow">Loja oficial do canal SandimR15</span>' +
        '<h1>Feito por quem <em>vive a R15.</em></h1>' +
        '<p class="lead">Acessórios para Yamaha R15 e R3, escolhidos por quem pilota todo dia.</p>' +
        '<div class="ctas"><a class="btn" href="#/c/acessorios">Ver peças da R15</a><a class="btn vidro" href="#/c/acessorios-r3">Linha R3</a></div>' +
      '</div><div class="hero-palco"><span class="hero-gigante" aria-hidden="true">R15</span><div class="hero-moto moto-parada">' + moto + '</div><div class="hero-chao"></div></div></div>' +
      '<button class="hero-scroll" type="button" data-rolar="maquinas"><i></i>Role</button></section>' +

      '<section class="secao" id="maquinas"><div class="wrap"><div class="sec-head"><div><span class="kicker">Comece por aqui</span><h2>Escolha sua máquina</h2></div></div>' +
      '<div class="maquinas">' +
        '<a class="maq r15" href="#/c/acessorios"><span class="num">R15</span><span class="moto-bg moto-parada">' + moto + '</span><div class="rod"><p><b>Linha R15</b>' + conta('R15') + ' acessórios para todos os anos</p><span class="seta" aria-hidden="true">→</span></div></a>' +
        '<a class="maq" href="#/c/acessorios-r3"><span class="num">R3</span><span class="moto-bg moto-parada">' + moto + '</span><div class="rod"><p><b>Linha R3</b>' + conta('R3') + ' acessórios</p><span class="seta" aria-hidden="true">→</span></div></a>' +
        '<p class="maq-outras">Tem uma SBM 250s? <a href="#/c/sbm-250s">Ver acessórios</a></p>' +
      '</div></div></section>' +

      vitrine('Mais vendidos', '', 'mais-vendidos', 8, maisVend, true) +

      (dest ? '<section class="secao"><div class="wrap destaque">' +
        '<a class="palco" href="#/p/' + dest.h + '"><span class="tag-canal">Usado no canal</span><img src="' + img(dest.img[0], 900) + '" alt="' + esc(dest.t) + '" loading="lazy"></a>' +
        '<div><span class="kicker">Destaque da garagem</span><h2>' + esc(dest.t) + '</h2>' +
        '<div class="preco-g">' + brl(dest.preco) + '<small>ou 12x de ' + brl(dest.preco * COEF_12X) + ' no cartão</small></div>' +
        '<ul><li>Compatível com Yamaha ' + dest.moto.join(' e ') + '</li><li>Frete grátis para todo o Brasil</li><li>Escolhido por quem pilota a R15 no canal</li></ul>' +
        '<div class="ctas"><a class="btn" href="#/p/' + dest.h + '">Ver produto</a><a class="btn vidro" href="#/c/escapamentos">Mais desempenho</a></div></div>' +
      '</div></section>' : '') +

      '<section class="secao"><div class="wrap"><div class="sec-head"><div><span class="kicker">Catálogo</span><h2>Monte a sua do seu jeito</h2></div></div><div class="mosaico">' + mosaico + '</div></div></section>' +

      '<section class="canal"><div class="wrap canal-in"><span class="kicker">Do canal para a sua garagem</span>' +
        '<h2>Quem vende, <em>pilota.</em></h2>' +
        '<p>O canal SandimR15 virou referência em dicas, análises e solução de problemas da R15. A loja nasceu dali: cada peça foi escolhida por quem anda com a moto todo dia.</p>' +
        '<div class="selos-canal"><span>Escolhido por quem usa</span><span>Frete grátis para todo o Brasil</span><span>Até 12x no cartão</span></div>' +
        '<a class="btn vidro" href="#/pagina/quem-somos">Conheça a história</a></div></section>' +

      vitrine('Lançamentos', '', 'news', 8, null, true) +

      '<section class="secao" style="padding-top:0"><div class="wrap garantia-faixa">' +
        '<div>' + icone.frete + '<p style="margin:0"><b>Frete grátis</b><span>Para todo o Brasil, com rastreio</span></p></div>' +
        '<div>' + icone.cartao + '<p style="margin:0"><b>Até 12x</b><span>No cartão de crédito</span></p></div>' +
        '<div>' + icone.escudo + '<p style="margin:0"><b>Compra segura</b><span>Checkout da Shopify</span></p></div>' +
      '</div></section>';
  }

"""
s = s[:i] + nova + s[j:]
# rolar suave pelo indicador do banner
gancho = "  document.addEventListener('click', function (e) {\n    var q = e.target.closest('[data-q]');"
assert gancho in s
s = s.replace(gancho, "  document.addEventListener('click', function (e) {\n    var rl = e.target.closest('[data-rolar]');\n    if (rl) { var alvo = document.getElementById(rl.dataset.rolar); if (alvo) alvo.scrollIntoView({ behavior: 'smooth', block: 'start' }); return; }\n    var q = e.target.closest('[data-q]');", 1)
open(A, 'w', encoding='utf8').write(s)

# CSS por último + rodas paradas em todas as motos decorativas
T = 'build/site.src.html'; t = open(T, encoding='utf8').read()
if 'premium.css' not in t:
    t = t.replace('<link rel="stylesheet" href="limpo.css">', '<link rel="stylesheet" href="limpo.css">\n<link rel="stylesheet" href="premium.css">')
open(T, 'w', encoding='utf8').write(t)
P = 'build/site.py'; p = open(P, encoding='utf8').read()
if 'premium.css' not in p:
    p = p.replace("rep['limpo.css\"'] = 'limpo.css?v=' + ver + '\"'", "rep['limpo.css\"'] = 'limpo.css?v=' + ver + '\"'\nrep['premium.css\"'] = 'premium.css?v=' + ver + '\"'")
open(P, 'w', encoding='utf8').write(p)
c = open('site/premium.css', encoding='utf8').read()
if '.moto-parada .sl-spin' not in c:
    c += '\n.moto-parada .sl-spin{animation:none!important}\n.moto-parada .sl-spin use[opacity]{display:none}\n'
open('site/premium.css', 'w', encoding='utf8').write(c)
print('home premium ok')
