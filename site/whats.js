/* Sandim R15 · botão do WhatsApp · CRdevs
   Ao clicar, o verde do botão se expande até cobrir a tela e então abre a conversa. */
(function () {
  var calmo = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var DUR = 620;

  function abre(url) {
    var w = null;
    try { w = window.open(url, '_blank'); } catch (e) {}
    if (w) { try { w.opener = null; } catch (e) {} }
    else location.href = url; // pop-up bloqueado: abre na mesma aba
  }

  document.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('a.whats');
    if (!a || e.metaKey || e.ctrlKey || e.shiftKey || calmo) return;
    e.preventDefault();
    if (document.querySelector('.whats-onda')) return;
    var r = a.getBoundingClientRect(), x = r.left + r.width / 2, y = r.top + r.height / 2;
    var raio = Math.hypot(Math.max(x, innerWidth - x), Math.max(y, innerHeight - y)) + 20;
    var onda = document.createElement('div'), ini = r.width / 2 / raio;
    onda.className = 'whats-onda';
    onda.innerHTML = '<i class="whats-bola" style="left:' + (x - raio) + 'px;top:' + (y - raio) + 'px;width:' + 2 * raio + 'px;height:' + 2 * raio + 'px"></i>' +
      '<div class="whats-onda-in">' + a.innerHTML + '<span>Abrindo o WhatsApp…</span></div>';
    document.body.appendChild(onda);
    var bola = onda.firstChild;
    // o verde nasce exatamente do botão e cresce até cobrir a tela
    var anim = bola.animate([{ transform: 'scale(' + ini + ')' }, { transform: 'scale(1)' }], { duration: DUR, easing: 'cubic-bezier(.7,0,.2,1)', fill: 'forwards' });
    anim.onfinish = function () {
      onda.classList.add('cheia');
      abre(a.href);
      // quando a pessoa voltar para a loja, o verde recolhe para o botão
      var recolhe = function () {
        if (document.visibilityState !== 'visible') return;
        if (onda.dataset.volta) return; onda.dataset.volta = '1';
        document.removeEventListener('visibilitychange', recolhe);
        onda.classList.remove('cheia');
        var volta = bola.animate([{ transform: 'scale(1)' }, { transform: 'scale(' + ini + ')' }], { duration: DUR, easing: 'cubic-bezier(.7,0,.2,1)', fill: 'forwards' });
        volta.onfinish = function () { onda.remove(); };
      };
      document.addEventListener('visibilitychange', recolhe);
      setTimeout(function () { if (document.visibilityState === 'visible') recolhe(); }, 1600);
    };
  });
})();
