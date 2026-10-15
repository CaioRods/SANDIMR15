"""Da home para a Linha R15 ou R3: o azul do carregamento entra em onda com a pista, a moto passa
sem parar e leva a tela junto, revelando o catálogo. Abaixo do logo aparece R15 ou R3."""
A = 'site/app.js'
s = open(A, encoding='utf8').read()

def troca(a, b):
    global s
    if b in s and a not in s: return
    assert a in s, a[:80]
    s = s.replace(a, b, 1)

# guarda o carregamento antes de ele sair da página (vira a tela da passagem)
troca("""  var MOTO = (function () {""", """  var TELA_MOTO = loader ? loader.outerHTML : '';
  var MOTO = (function () {""")

# saída em onda: modo "traseira" faz a borda seguir a traseira da moto (moto que vem de fora da tela)
troca("""  function ondaSaida(el) {""", """  function ondaSaida(el, traseira) {""")
troca("""        var anda = Math.max(0, rider.getBoundingClientRect().left - x0);  // quanto a moto já andou""",
      """        var rr = rider.getBoundingClientRect(), anda = Math.max(0, rr.left - x0);  // quanto a moto já andou""")
troca("""        var borda = anda * 1.12 - amp, pts = [];""",
      """        var borda = traseira ? rr.left + rr.width * .1 - amp : anda * 1.12 - amp, pts = [];""")
troca("""        if (borda - amp * 1.4 > W || t - ini > 3000) { fim(); return; }""",
      """        if (borda - amp * 1.4 > W || t - ini > (traseira ? 4000 : 3000)) { fim(); return; }""")

troca("""  var loaderPronto = (function () {""", """  // entrada em onda: o azul cobre a tela da esquerda para a direita
  function ondaCobre(el) {
    return new Promise(function (fim) {
      var W = el.clientWidth || innerWidth, H = el.clientHeight || innerHeight, N = 36, ini = performance.now(), dur = 700;
      (function quadro(t) {
        var k = Math.min(1, (t - ini) / dur), e = k < .5 ? 4 * k * k * k : 1 - Math.pow(-2 * k + 2, 3) / 2;
        var amp = 34 * Math.sin(Math.PI * k) + 6, fase = t / 1000 * 5, borda = -80 + e * (W + 200), pts = ['-400px 0px'];
        for (var i = 0; i <= N; i++) {
          var q = i / N, x = borda + amp * Math.sin(q * Math.PI * 2.4 + fase) + amp * .35 * Math.sin(q * Math.PI * 5.2 - fase * 1.4);
          pts.push(x.toFixed(1) + 'px ' + (q * H).toFixed(1) + 'px');
        }
        pts.push('-400px ' + H + 'px');
        el.style.clipPath = 'polygon(' + pts.join(',') + ')';
        if (k < 1) requestAnimationFrame(quadro); else { el.style.clipPath = 'none'; fim(); }
      })(ini);
    });
  }
  // passagem da moto: cobre, troca a página por baixo e a moto passa levando a tela
  function passaMoto(modelo, desenhar) {
    if (!TELA_MOTO || Cinema.calmo || document.getElementById('sandim-loader')) return false;
    var caixa = document.createElement('div'); caixa.innerHTML = TELA_MOTO;
    var el = caixa.firstElementChild;
    el.classList.add('is-cobre');
    el.style.clipPath = 'polygon(-400px 0px,-399px 0px,-400px 1px)';
    el.querySelector('.sl-word').insertAdjacentHTML('beforeend', '<span class="sl-modelo m-' + modelo.toLowerCase() + '">' + modelo + '</span>');
    document.body.appendChild(el);
    ondaCobre(el).then(function () {
      desenhar();
      return new Promise(function (r) { setTimeout(r, 140); });
    }).then(function () {
      el.classList.add('is-passa');
      return ondaSaida(el, true);
    }).then(function () { el.remove(); });
    return true;
  }
  var loaderPronto = (function () {""")

troca("""    var de = idxCat(rotaAnterior), para = idxCat(location.hash);
    rotaAnterior = location.hash;
    if (pularTransicao) { pularTransicao = false; desenha(); return; }""",
      """    var de = idxCat(rotaAnterior), para = idxCat(location.hash), anterior = rotaAnterior;
    rotaAnterior = location.hash;
    if (pularTransicao) { pularTransicao = false; desenha(); return; }
    var linha = location.hash === '#/c/acessorios' ? 'R15' : location.hash === '#/c/acessorios-r3' ? 'R3' : '';
    if (linha && anterior !== location.hash && passaMoto(linha, desenha)) return;  // de qualquer página para a Linha R15/R3""")
open(A, 'w', encoding='utf8').write(s)
print('passagem ok')
