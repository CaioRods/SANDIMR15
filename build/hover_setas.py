"""Hover dos cards com "Ver produto" + setas para passar as fotos na galeria do produto."""
A = 'site/app.js'
s = open(A, encoding='utf8').read()

def troca(a, b):
    global s
    if b in s and a not in s: return
    assert a in s, a[:80]
    s = s.replace(a, b, 1)

SETA_E = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M15 5l-7 7 7 7"/></svg>'
SETA_D = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M9 5l7 7-7 7"/></svg>'

# card: pílula "Ver produto" que sobe no hover
troca("""      (p.ok ? '' : '<span class="sem-estoque">Sem estoque</span>') + '</div>' +""",
      """      (p.ok ? '<span class="ver-prod">Ver produto<i aria-hidden="true">→</i></span>' : '<span class="sem-estoque">Sem estoque</span>') + '</div>' +""")

# galeria: setas anterior/próxima
troca("""<div class="trilho" id="trilho"></div><div class="pontos" id="pontos"></div></div></div>' +""",
      """<div class="trilho" id="trilho"></div><div class="pontos" id="pontos"></div>' +
      '<button class="foto-seta ant" type="button" data-passo="-1" aria-label="Foto anterior">""" + SETA_E + """</button><button class="foto-seta prox" type="button" data-passo="1" aria-label="Próxima foto">""" + SETA_D + """</button></div></div>' +""")
troca("""      $('#foto-cont').textContent = (i + 1) + ' / ' + fotos.length; $('#foto-cont').hidden = fotos.length < 2;""",
      """      $('#foto-cont').textContent = (i + 1) + ' / ' + fotos.length; $('#foto-cont').hidden = fotos.length < 2;
      document.querySelectorAll('.foto-seta').forEach(function (b) { b.hidden = fotos.length < 2; });""")
troca("""      var f = e.target.closest('[data-f]'); if (f) { pintaFotos(+f.dataset.f); return; }""",
      """      var f = e.target.closest('[data-f]'); if (f) { pintaFotos(+f.dataset.f); return; }
      var ps = e.target.closest('[data-passo]');
      if (ps) { var tr = $('#trilho'), n = fotos.length, i = Math.round(tr.scrollLeft / Math.max(tr.clientWidth, 1)); pintaFotos((i + +ps.dataset.passo + n) % n); return; }""")
open(A, 'w', encoding='utf8').write(s)
print('hover + setas ok')
