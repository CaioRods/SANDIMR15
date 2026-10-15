"""Celular:
- um toque no produto já abre (o 1º toque não ativa mais o efeito de passar o mouse, que trocava a foto)
- ao abrir um produto lá embaixo no catálogo, a página pula para o topo de verdade antes de medir onde a
  foto pousa (o html tem scroll-behavior:smooth e o Safari ignora behavior:'instant', aí a página subia
  devagar e a foto voava para o lugar errado)"""
A = 'site/app.js'
s = open(A, encoding='utf8').read()

def troca(a, b, todas=False):
    global s
    if b in s and a not in s: return
    assert a in s, a[:80]
    s = s.replace(a, b) if todas else s.replace(a, b, 1)

troca("""  /* ---------- card: a foto sobe, gira e pousa na galeria do produto ---------- */""",
      """  // rolagem imediata em qualquer navegador (o html tem scroll-behavior:smooth; o Safari ignora 'instant')
  function rolaJa(y) {
    var h = document.documentElement, antes = h.style.scrollBehavior;
    h.style.scrollBehavior = 'auto'; window.scrollTo(0, y); h.style.scrollBehavior = antes;
  }
  /* ---------- card: a foto sobe, gira e pousa na galeria do produto ---------- */""")
troca("""    window.scrollTo({ top: 0, left: 0, behavior: 'instant' });""", """    rolaJa(0);""")
troca("""window.scrollTo({ top: topo.offsetHeight - 10, behavior: 'instant' });""", """rolaJa(topo.offsetHeight - 10);""")
# a foto só mede onde pousar depois que a página chegou ao topo
troca("""      aposDesenhar = function () {
        var caixa = document.querySelector('.galeria .principal');""", """      aposDesenhar = function mede() {
        if (window.scrollY > 2 && (mede.n = (mede.n || 0) + 1) < 15) { rolaJa(0); requestAnimationFrame(mede); return; }
        var caixa = document.querySelector('.galeria .principal');""")
open(A, 'w', encoding='utf8').write(s)

C = 'site/azul.css'
c = open(C, encoding='utf8').read()
if 'html{scroll-behavior:auto}' not in c:
    c += """
/* rolagem suave só onde o código pede (setas, "Role", carrosséis); pulos de página são imediatos */
html{scroll-behavior:auto}
/* ---------- toque (celular): sem efeitos de "passar o mouse" nos cards — um toque já abre ---------- */
@media (hover:none){
  .card .ft .alt{display:none}
  .card:hover,.card:hover .ft{transform:none}
  .card:hover .ft .alt{opacity:0}
  .card .ver-prod{display:none}
}
"""
    open(C, 'w', encoding='utf8').write(c)
print('toque ok')
