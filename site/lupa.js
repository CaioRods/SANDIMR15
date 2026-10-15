/* Sandim R15 · zoom das fotos do produto · CRdevs
   Computador: clique na foto liga uma lupa de vidro que segue o mouse.
   Celular: toque na foto abre a foto em tela cheia, com pinça, duplo toque e arrastar. */
(function () {
  var computador = window.matchMedia('(hover:hover) and (min-width:721px)');
  var grande = function (src, w) { return src.replace(/([?&])width=\d+/, '$1width=' + w); };

  /* ---------- lupa (computador) ---------- */
  var ZOOM = 2.6, lupa = null, alvo = null, caixa = null, ultimo = null;

  function fotoAtual() {
    var t = document.getElementById('trilho'); if (!t) return null;
    return t.children[Math.round(t.scrollLeft / Math.max(t.clientWidth, 1))] || null;
  }
  // área onde a foto realmente aparece (desconta padding e object-fit: contain)
  function areaFoto(im) {
    var r = im.getBoundingClientRect(), cs = getComputedStyle(im);
    var pl = parseFloat(cs.paddingLeft), pt = parseFloat(cs.paddingTop);
    var w = r.width - pl - parseFloat(cs.paddingRight), h = r.height - pt - parseFloat(cs.paddingBottom);
    var k = Math.min(w / (im.naturalWidth || w), h / (im.naturalHeight || h));
    var dw = (im.naturalWidth || w) * k, dh = (im.naturalHeight || h) * k;
    return { x: r.left + pl + (w - dw) / 2, y: r.top + pt + (h - dh) / 2, w: dw, h: dh };
  }
  function liga(e) {
    caixa = document.querySelector('.galeria .principal');
    lupa = document.createElement('div'); lupa.className = 'lupa'; lupa.innerHTML = '<i></i>';
    document.body.appendChild(lupa); caixa.classList.add('lupa-on');
    move(e);
    void lupa.offsetWidth; lupa.classList.add('on');
  }
  function desliga() {
    if (!lupa) return;
    var l = lupa; lupa = null; alvo = null;
    l.classList.remove('on'); setTimeout(function () { l.remove(); }, 250);
    if (caixa) caixa.classList.remove('lupa-on');
  }
  function move(e) {
    if (!lupa) return;
    ultimo = e;
    var im = fotoAtual(); if (!im) return;
    if (alvo !== im) { alvo = im; lupa.firstChild.style.backgroundImage = 'url("' + grande(im.currentSrc || im.src, 1800) + '")'; }
    var a = areaFoto(im), L = lupa.offsetWidth;
    var mx = e.clientX - a.x, my = e.clientY - a.y;
    var sobreBotao = e.target.closest && e.target.closest('button');
    lupa.classList.toggle('fora', !!sobreBotao || mx < -20 || my < -20 || mx > a.w + 20 || my > a.h + 20);
    lupa.style.left = (e.clientX - L / 2) + 'px'; lupa.style.top = (e.clientY - L / 2) + 'px';
    var d = L - 16; // diâmetro da área ampliada (dentro do aro)
    var i = lupa.firstChild.style;
    i.backgroundSize = (a.w * ZOOM) + 'px ' + (a.h * ZOOM) + 'px';
    i.backgroundPosition = (d / 2 - mx * ZOOM) + 'px ' + (d / 2 - my * ZOOM) + 'px';
  }

  document.addEventListener('click', function (e) {
    var im = e.target.closest && e.target.closest('#trilho img'); if (!im) return;
    if (computador.matches) { lupa ? desliga() : liga(e); }
    else abreVisor(im);
  });
  document.addEventListener('mousemove', function (e) {
    if (!lupa) return;
    if (!caixa.isConnected || !caixa.contains(e.target)) { desliga(); return; }
    move(e);
  });
  // ao trocar de foto pelas setas, a lupa acompanha
  document.addEventListener('scroll', function (e) { if (lupa && e.target.id === 'trilho' && ultimo) move(ultimo); }, true);
  window.addEventListener('hashchange', function () { desliga(); fecha(); });

  /* ---------- visor em tela cheia (celular) ---------- */
  var visor = null, fotos = [], atual = 0, s = 1, tx = 0, ty = 0, toques = {}, gesto = null, ultimoToque = 0;

  function abreVisor(im) {
    if (visor) return;
    var t = document.getElementById('trilho');
    fotos = [].map.call(t.children, function (x) { return grande(x.currentSrc || x.src, 1600); });
    atual = Math.max(0, [].indexOf.call(t.children, im));
    visor = document.createElement('div');
    visor.className = 'visor'; visor.setAttribute('role', 'dialog'); visor.setAttribute('aria-modal', 'true'); visor.setAttribute('aria-label', 'Foto do produto');
    visor.innerHTML = '<div class="visor-topo"><span class="visor-cont"></span><button type="button" class="visor-x" aria-label="Fechar"><svg viewBox="0 0 24 24"><path d="M6 6l12 12M18 6 6 18"/></svg></button></div>' +
      '<div class="visor-palco"><img alt="" draggable="false"></div>' +
      (fotos.length > 1 ? '<button type="button" class="visor-seta ant" aria-label="Foto anterior"><svg viewBox="0 0 24 24"><path d="M15 5l-7 7 7 7"/></svg></button><button type="button" class="visor-seta prox" aria-label="Próxima foto"><svg viewBox="0 0 24 24"><path d="M9 5l7 7-7 7"/></svg></button>' : '') +
      '<p class="visor-dica">Pinça ou toque duas vezes para ampliar</p>';
    document.body.appendChild(visor); document.body.style.overflow = 'hidden';
    mostra(atual);
    void visor.offsetWidth; visor.classList.add('on');
    visor.querySelector('.visor-x').onclick = fecha;
    visor.querySelectorAll('.visor-seta').forEach(function (b) { b.onclick = function () { mostra(atual + (b.classList.contains('prox') ? 1 : -1)); }; });
    var p = visor.querySelector('.visor-palco');
    p.addEventListener('pointerdown', baixa); p.addEventListener('pointermove', arrasta);
    p.addEventListener('pointerup', solta); p.addEventListener('pointercancel', solta);
  }
  function fecha() {
    if (!visor) return;
    var v = visor; visor = null; toques = {}; gesto = null;
    v.classList.remove('on'); document.body.style.overflow = '';
    setTimeout(function () { v.remove(); }, 250);
  }
  function mostra(i) {
    var n = fotos.length; atual = (i + n) % n; s = 1; tx = 0; ty = 0;
    var im = visor.querySelector('.visor-palco img');
    im.src = fotos[atual]; aplica(false);
    visor.querySelector('.visor-cont').textContent = n > 1 ? (atual + 1) + ' / ' + n : '';
  }
  function limita() {
    var im = visor.querySelector('.visor-palco img');
    var mx = Math.max(0, (im.offsetWidth * s - im.offsetWidth) / 2), my = Math.max(0, (im.offsetHeight * s - im.offsetHeight) / 2);
    tx = Math.max(-mx, Math.min(mx, tx)); ty = Math.max(-my, Math.min(my, ty));
  }
  function aplica(animar) {
    var im = visor.querySelector('.visor-palco img');
    im.style.transition = animar ? 'transform .3s cubic-bezier(.2,.8,.2,1)' : 'none';
    im.style.transform = 'translate(' + tx + 'px,' + ty + 'px) scale(' + s + ')';
    visor.classList.toggle('ampliado', s > 1.01);
  }
  // zoom mantendo o ponto (px, py), relativo ao centro do palco, parado sob o dedo
  function zoomEm(novo, px, py) {
    novo = Math.max(1, Math.min(5, novo));
    tx = px - novo * (px - tx) / s; ty = py - novo * (py - ty) / s; s = novo;
    limita();
  }
  function centro(e) {
    var r = visor.querySelector('.visor-palco').getBoundingClientRect();
    return { x: e.clientX - r.left - r.width / 2, y: e.clientY - r.top - r.height / 2 };
  }
  function baixa(e) {
    e.preventDefault(); e.currentTarget.setPointerCapture(e.pointerId);
    toques[e.pointerId] = { x: e.clientX, y: e.clientY };
    var ids = Object.keys(toques);
    if (ids.length === 2) {
      var a = toques[ids[0]], b = toques[ids[1]];
      gesto = { tipo: 'pinca', d: Math.hypot(a.x - b.x, a.y - b.y), s: s };
    } else if (ids.length === 1) {
      var agora = Date.now(), c = centro(e);
      if (agora - ultimoToque < 280) { s > 1.01 ? (s = 1, tx = 0, ty = 0) : zoomEm(2.5, c.x, c.y); aplica(true); ultimoToque = 0; gesto = null; return; }
      ultimoToque = agora;
      gesto = { tipo: s > 1.01 ? 'mover' : 'deslizar', x: e.clientX, y: e.clientY, tx: tx, ty: ty };
    }
  }
  function arrasta(e) {
    if (!toques[e.pointerId] || !gesto) return;
    toques[e.pointerId] = { x: e.clientX, y: e.clientY };
    var ids = Object.keys(toques);
    if (gesto.tipo === 'pinca' && ids.length === 2) {
      var a = toques[ids[0]], b = toques[ids[1]];
      var m = centro({ clientX: (a.x + b.x) / 2, clientY: (a.y + b.y) / 2 });
      zoomEm(gesto.s * Math.hypot(a.x - b.x, a.y - b.y) / gesto.d, m.x, m.y); aplica(false);
    } else if (gesto.tipo === 'mover') {
      tx = gesto.tx + e.clientX - gesto.x; ty = gesto.ty + e.clientY - gesto.y; limita(); aplica(false);
    } else if (gesto.tipo === 'deslizar') {
      tx = e.clientX - gesto.x; ty = Math.max(0, e.clientY - gesto.y) * .6; aplica(false);
      visor.style.setProperty('--fundo', String(Math.max(.4, 1 - ty / 300)));
    }
  }
  function solta(e) {
    delete toques[e.pointerId];
    if (!gesto) return;
    if (gesto.tipo === 'deslizar') {
      var dx = e.clientX - gesto.x, dy = e.clientY - gesto.y;
      visor.style.removeProperty('--fundo');
      if (dy > 110 && Math.abs(dy) > Math.abs(dx)) { fecha(); return; }
      if (Math.abs(dx) > 60 && fotos.length > 1) { mostra(atual + (dx < 0 ? 1 : -1)); gesto = null; return; }
      tx = 0; ty = 0; aplica(true);
    }
    if (gesto.tipo === 'pinca' && s < 1.05) { s = 1; tx = 0; ty = 0; aplica(true); }
    gesto = Object.keys(toques).length ? gesto : null;
  }
  document.addEventListener('keydown', function (e) {
    if (!visor) return;
    if (e.key === 'Escape') fecha();
    if (e.key === 'ArrowRight') mostra(atual + 1);
    if (e.key === 'ArrowLeft') mostra(atual - 1);
  });
})();
