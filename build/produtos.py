"""Barra de baixo: "Categorias" vira "Produtos" (#/c/produtos), com todos os produtos da loja."""
A = 'site/app.js'
s = open(A, encoding='utf8').read()

def troca(a, b):
    global s
    if b in s and a not in s: return
    assert a in s, a[:80]
    s = s.replace(a, b, 1)

# botão da barra não abre mais o menu
troca("""  $('#tab-cats').addEventListener('click', abrirMenu);\n""", "")

# coleção "produtos": todos os produtos, disponíveis primeiro
troca("""    var c = CATS.find(function (x) { return x.h === h; }) || { n: D.colecoes[h] || 'Produtos', d: '' };
    var base = h === 'busca' ?""", """    var c = CATS.find(function (x) { return x.h === h; }) || (h === 'produtos' ? { n: 'Produtos', d: 'Todos os produtos da loja, em um só lugar.' } : { n: D.colecoes[h] || 'Produtos', d: '' });
    var base = h === 'produtos' ? D.produtos.filter(function (p) { return p.ok; }).concat(D.produtos.filter(function (p) { return !p.ok; })) : h === 'busca' ?""")

# aba acesa na rota certa + título da página
troca("""t.classList.toggle('on', t.dataset.tab === 'home' && !r[0]); });""",
      """t.classList.toggle('on', (t.dataset.tab === 'home' && !r[0]) || (t.dataset.tab === 'produtos' && r[0] === 'c' && r[1] === 'produtos')); });""")
troca("""r[0] === 'c' ? ((CATS.find(function (c) { return c.h === r[1]; }) || {}).n || '') + ' · ' : '';""",
      """r[0] === 'c' ? (r[1] === 'produtos' ? 'Produtos' : ((CATS.find(function (c) { return c.h === r[1]; }) || {}).n || '')) + ' · ' : '';""")
open(A, 'w', encoding='utf8').write(s)

# botão da barra (HTML)
SACOLA = '<svg viewBox="0 0 24 24"><path d="M5 8h14l-1.2 11.2a2 2 0 0 1-2 1.8H8.2a2 2 0 0 1-2-1.8z"/><path d="M9 10V7a3 3 0 0 1 6 0v3"/></svg>'
import re
for f in ['build/site.src.html', 'site/index.html']:
    h = open(f, encoding='utf8').read()
    h = re.sub(r'<button type="button" id="tab-cats" data-tab="cats">.*?</button>',
               '<a href="#/c/produtos" id="tab-produtos" data-tab="produtos">' + SACOLA + '<span>Produtos</span></a>', h, count=1)
    assert 'tab-produtos' in h, f
    open(f, 'w', encoding='utf8').write(h)
print('produtos ok')
