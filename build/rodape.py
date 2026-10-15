"""Aplica o rodapé com os dados exatos da loja atual, páginas migradas e a assinatura CRdevs."""
import re

p = 'build/site.src.html'; s = open(p, encoding='utf8').read()
novo = '''<footer class="rodape">
  <div class="rodape-in">
    <div class="rod-marca">
      <svg viewBox="0 0 2000 667" aria-label="Sandim R15 Store"><use href="#logo" style="--k:url(#sg-branco);--b:url(#sg-azulc)"/></svg>
      <h4>Atendimento ao cliente</h4>
      <p class="sac">SAC (Serviço de Atendimento ao Consumidor)</p>
      <p class="contato">E-mail: <a href="mailto:sandimcomercial@gmail.com">sandimcomercial@gmail.com</a><br>WhatsApp: <a href="https://wa.me/5532991042903" target="_blank" rel="noopener">+55 (32) 9 9104-2903</a></p>
    </div>
    <div class="rod-menu"><h4>Menu de rodapé</h4><a href="#/">Página inicial</a><a href="#/busca/">Pesquisar</a><a href="#/pagina/quem-somos">Quem Somos</a><a href="#/pagina/privacidade">Política de Privacidade</a><a href="#/pagina/trocas">Trocas e Devoluções</a><a href="#/pagina/envio">Envio e Prazo de Entrega</a></div>
    <div class="news"><h4>Nossa newsletter</h4><p>Assine nossa newsletter e receba as melhores ofertas DE GRAÇA!</p>
      <form id="newsletter" class="news-form"><input id="news-email" type="email" required placeholder="Seu e-mail" aria-label="Seu e-mail"><button class="btn" type="submit">Enviar</button></form>
      <h4 class="aceitamos">Nós aceitamos</h4><div class="pags"><span>American Express</span><span>Boleto</span><span>Elo</span><span>Hypercard</span><span>Mastercard</span><span>Visa</span></div>
    </div>
  </div>
  <div class="rodape-aviso"><p>Preços e condições de pagamento exclusivos para compras neste site oficial, podendo variar com o tempo da oferta. Evite comprar produtos mais baratos ou de outras lojas, pois você pode estar sendo enganado(a) por um golpista. Caso você compre os mesmos produtos em outras lojas, não nos responsabilizamos por quaisquer problemas.</p></div>
  <div class="rodape-base">
    <span>© 2026 Sandim R15 · Todos os direitos reservados · <a href="#/pagina/privacidade">Política de Privacidade</a> · <a href="#/pagina/termos">Termos de serviço</a> · Com tecnologia da Shopify</span>
    <a class="crdevs" href="https://www.instagram.com/caio.riguess/" target="_blank" rel="noopener" aria-label="Desenvolvido por CRdevs, abre o Instagram @caio.riguess">
      <span>Desenvolvido por</span>
      <svg viewBox="0 0 132 32" aria-hidden="true"><path d="M8 2h40l-6 28H2z" fill="#F2F5FA"/><text x="25" y="23.5" text-anchor="middle" font-family="Kanit, Arial Black, sans-serif" font-style="italic" font-weight="800" font-size="20" fill="#1C1F25">CR</text><text x="52" y="23.5" font-family="Kanit, Arial Black, sans-serif" font-style="italic" font-weight="700" font-size="21" fill="#F2F5FA">devs</text></svg>
    </a>
  </div>
</footer>'''
s = re.sub(r'(?s)<footer class="rodape">.*?</footer>', lambda m: novo, s)
s = s.replace('<a class="whats" href="#/pagina/atendimento" aria-label="Atendimento no WhatsApp">',
              '<a class="whats" href="https://wa.me/5532991042903" target="_blank" rel="noopener" aria-label="Atendimento no WhatsApp">')
open(p, 'w', encoding='utf8').write(s)

c = open('site/estilo.css', encoding='utf8').read()
i = c.index('/* rodapé */'); j = c.index('.whats{')
c = c[:i] + '''/* rodapé */
.rodape{background:var(--g-noite);color:#C2CADB}
.rodape-in{max-width:var(--larg);margin-inline:auto;padding:48px var(--gut) 28px;display:grid;grid-template-columns:1.3fr 1fr 1.3fr;gap:36px}
.rodape h4{color:#fff;font-size:16px;margin-bottom:12px}
.rodape a{color:#DDE4EF}
.rodape a:hover{color:#fff;text-decoration:underline}
.rod-menu a{display:block;padding:6px 0;font-size:15px}
.rod-marca svg{width:230px;height:auto;margin-bottom:18px}
.rod-marca p{margin:0 0 8px;font-size:15px}
.rod-marca .sac{color:#9AA6C0;font-size:14px}
.news p{margin:0 0 12px;font-size:15px}
.news-form{display:flex;gap:8px;margin-bottom:22px}
.news-form input{flex:1;min-width:0;border:1px solid #2A3A66;background:rgba(255,255,255,.06);color:#fff;border-radius:3px;padding:12px;font:inherit;font-size:16px}
.news-form input::placeholder{color:#8C9AB8}
.news-form .btn{padding:11px 18px;font-size:14px}
.aceitamos{margin-top:4px}
.pags{display:flex;flex-wrap:wrap;gap:6px}
.pags span{border:1px solid #2A3A66;border-radius:3px;padding:3px 8px;font-size:12.5px;font-weight:600;color:#DDE4EF}
.rodape-aviso{max-width:var(--larg);margin-inline:auto;padding:0 var(--gut) 24px}
.rodape-aviso p{margin:0;font-size:13px;color:#8C9AB8;max-width:110ch}
.rodape-base{max-width:var(--larg);margin-inline:auto;padding:16px var(--gut) calc(84px + env(safe-area-inset-bottom,0px));border-top:1px solid #22345F;display:flex;justify-content:space-between;align-items:center;gap:12px 24px;flex-wrap:wrap;font-size:12.5px;color:#8C9AB8}
.rodape-base a{color:#C2CADB}
.crdevs{display:inline-flex;align-items:center;gap:8px;color:#8C9AB8!important;text-decoration:none!important;opacity:.85;transition:opacity .15s;padding:6px 0}
.crdevs:hover{opacity:1}
.crdevs svg{height:22px;width:auto}
@media (max-width:820px){.rodape-in{grid-template-columns:1fr;gap:28px}.rodape-base{justify-content:center;text-align:center}}
''' + c[j:]
c = c.replace('.pagina p{color:#3A4358;font-size:17px}',
              '.pagina p,.pagina li{color:#3A4358;font-size:17px}\n.pagina h2,.pagina h3{font-size:22px;margin:28px 0 10px}\n.pagina a{color:var(--azul);word-break:break-word}\n.pagina .contato-box{background:#fff;border:1px solid var(--borda);border-radius:4px;padding:20px;margin-top:20px}')
open('site/estilo.css', 'w', encoding='utf8').write(c)

a = open('site/app.js', encoding='utf8').read()
i = a.index("    'envio': ['Envio e prazo de entrega'"); j = a.index("  };\n\n  var D = null")
a = a[:i] + """    'rastreio': ['Rastrear pedido', ['O código de rastreio é enviado por e-mail depois da confirmação do pagamento. No site final, esta página abre o rastreio da Shopify com o número do pedido.']],
    'atendimento': ['Atendimento', ['SAC (Serviço de Atendimento ao Consumidor)']]
""" + a[j:]
velho = a[a.index('  function pagina(id) {'):a.index('  /* ---------- rotas ---------- */')]
a = a.replace(velho, """  var PG = {};
  var CONTATO = '<div class="contato-box"><b>Atendimento ao cliente</b><p>E-mail: <a href="mailto:sandimcomercial@gmail.com">sandimcomercial@gmail.com</a><br>WhatsApp: <a href="https://wa.me/5532991042903" target="_blank" rel="noopener">+55 (32) 9 9104-2903</a></p></div>';
  function pagina(id) {
    if (PG[id]) { app.innerHTML = '<div class="wrap pagina"><h1>' + esc(PG[id].titulo) + '</h1>' + PG[id].html + CONTATO + '</div>'; return; }
    var pg = PAGINAS[id] || ['Página', ['Conteúdo em construção.']];
    app.innerHTML = '<div class="wrap pagina"><h1>' + pg[0] + '</h1>' + pg[1].map(function (t) { return '<p>' + esc(t) + '</p>'; }).join('') + (id === 'quem-somos' ? '' : CONTATO) + '</div>';
  }

""")
a = a.replace("""  fetch('catalogo.json').then(function (r) { return r.json(); }).then(function (d) {
    D = d;""", """  $('#newsletter').addEventListener('submit', function (e) {
    e.preventDefault(); $('#news-email').value = ''; toast('E-mail cadastrado. No site final, entra na lista da Shopify.');
  });
  fetch('paginas.json').then(function (r) { return r.json(); }).then(function (p) { PG = p; if (location.hash.indexOf('#/pagina/') === 0) rota(); }).catch(function () {});
  fetch('catalogo.json').then(function (r) { return r.json(); }).then(function (d) {
    D = d;""")
a = a.replace("""    if (r[0] === 'c') colecao(r[1]);""", """    if (r[0] === 'busca' && !q) { app.innerHTML = '<div class="wrap pagina"><h1>Pesquisar</h1><p>Digite o nome da peça na busca do topo.</p></div>'; fechar(); $('#busca-q').focus(); return; }
    if (r[0] === 'c') colecao(r[1]);""")
open('site/app.js', 'w', encoding='utf8').write(a)
print('rodapé ok')
