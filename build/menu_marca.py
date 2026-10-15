"""Menu: item selecionado nunca fica apagado + letreiro R15/R3 vazado no fundo do catálogo."""
A = 'site/app.js'
s = open(A, encoding='utf8').read()

def troca(a, b):
    global s
    if b in s and a not in s: return
    assert a in s, a[:80]
    s = s.replace(a, b, 1)

# 1) o indicador do menu era medido com o cabeçalho compacto (menu escondido = largura 0).
#    Mede de novo depois de abrir o cabeçalho e sempre que o menu muda de tamanho.
troca("""    $('#topo').classList.remove('oculto', 'min', 'busca-aberta'); altHdr();""",
      """    $('#topo').classList.remove('oculto', 'min', 'busca-aberta'); altHdr();
    Cinema.indicador($('#cats'), $('#cats a.on'));""")
troca("""  window.addEventListener('resize', altHdr); altHdr();""",
      """  window.addEventListener('resize', altHdr); altHdr();
  if (window.ResizeObserver) new ResizeObserver(function () { var on = $('#cats a.on'); if (on && on.offsetWidth) Cinema.indicador($('#cats'), on); }).observe($('#cats'));""")

# 2) letreiro no fundo: R15 azul claro, R3 grafite fosco, só contorno
troca("""    var moto = 'Todas', ord = 'rel';
    function pinta(animar) {""",
      """    var moto = 'Todas', ord = 'rel';
    var marca = document.createElement('span'); marca.className = 'marca-fundo'; marca.setAttribute('aria-hidden', 'true'); app.appendChild(marca);
    function pintaMarca() {
      var m = moto !== 'Todas' ? moto : h === 'acessorios' ? 'R15' : h === 'acessorios-r3' ? 'R3' : '';
      if (marca.dataset.m === m) return;
      marca.classList.remove('on');
      setTimeout(function () { marca.textContent = m; marca.dataset.m = m; marca.className = 'marca-fundo m-' + m.toLowerCase() + (m ? ' on' : ''); }, marca.dataset.m ? 220 : 0);
    }
    function pinta(animar) {
      pintaMarca();""")
open(A, 'w', encoding='utf8').write(s)
print('menu + marca ok')
