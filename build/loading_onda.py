"""Carregamento: só a moto. Ao acelerar de novo, ela arrasta a tela de carregamento junto e revela o
site com uma borda em onda que acompanha a moto (quanto mais rápido, mais a onda balança)."""
A = 'site/app.js'
s = open(A, encoding='utf8').read()

def troca(a, b):
    global s
    if b in s and a not in s: return
    assert a in s, a[:80]
    s = s.replace(a, b, 1)

troca("""  var loaderPronto = (function () {""", """  // saída do carregamento: a borda esquerda da tela segue o deslocamento da moto, em onda
  function ondaSaida(el) {
    return new Promise(function (fim) {
      var rider = el.querySelector('.sl-rider'); if (!rider) { fim(); return; }
      var W = el.clientWidth, H = el.clientHeight, N = 36, x0 = rider.getBoundingClientRect().left;
      var fase = 0, amp = 0, ult = performance.now(), ini = ult, antes = 0;
      (function quadro(t) {
        var dt = Math.min(.05, Math.max(.001, (t - ult) / 1000)); ult = t;
        var anda = Math.max(0, rider.getBoundingClientRect().left - x0);  // quanto a moto já andou
        var vel = (anda - antes) / dt; antes = anda;                         // px/s
        amp += (Math.min(70, 6 + vel * .035) - amp) * Math.min(1, dt * 8);  // onda cresce com a velocidade
        fase += dt * (4 + vel * .004);
        var borda = anda * 1.12 - amp, pts = [];
        for (var i = 0; i <= N; i++) {
          var k = i / N, y = k * H;
          var x = borda + amp * Math.sin(k * Math.PI * 2.4 + fase) + amp * .35 * Math.sin(k * Math.PI * 5.2 - fase * 1.4);
          pts.push(x.toFixed(1) + 'px ' + y.toFixed(1) + 'px');
        }
        el.style.clipPath = 'polygon(' + pts.join(',') + ',' + (W + 400) + 'px ' + H + 'px,' + (W + 400) + 'px 0px)';
        if (borda - amp * 1.4 > W || t - ini > 3000) { fim(); return; }
        requestAnimationFrame(quadro);
      })(ult);
    });
  }
  var loaderPronto = (function () {""")
troca("""      setTimeout(function () { spd(2); }, 120); setTimeout(function () { spd(3); }, 280);
      return wait(800);""", """      setTimeout(function () { spd(2); }, 120); setTimeout(function () { spd(3); }, 280);
      loaderAcabou = true; if (window.Cinema) Cinema.heroPlay(); // o site já entra animando atrás da onda
      return ondaSaida(loader);""")
open(A, 'w', encoding='utf8').write(s)
print('loading onda ok')
