"""Gera sandim-loader.liquid (tela de carregamento para o tema Shopify)."""
import sys; sys.path.insert(0, 'build')
import loader_svg as LS
LS.arquivo_corpo()
CORPO_URL = "{{ 'sandim-moto-loading-corpo.svg' | asset_url }}"
css = open('build/loader.css').read()
liq = f'''{{% comment %}}
  Tela de carregamento Sandim R15 Store.
  1. Envie logo/moto-loading-corpo.svg e logo/texto-negativo.svg para Assets do tema
     com os nomes sandim-moto-loading-corpo.svg e sandim-texto-negativo.svg.
  2. Salve este arquivo como snippets/sandim-loader.liquid.
  3. Em layout/theme.liquid, logo depois de <body>, coloque: {{% render 'sandim-loader' %}}
  A moto entra pela esquerda, roda no centro até a página carregar e sai pela direita.
  Aparece uma vez por sessão.
{{% endcomment %}}
<style>
#sandim-loader{{position:fixed;inset:0;z-index:99999;transition:opacity .45s ease,visibility 0s linear .45s}}
#sandim-loader.is-done{{opacity:0;visibility:hidden}}
#sandim-loader .sl-corpo{{position:absolute;inset:0;width:100%;height:100%}}
{css}</style>
{LS.FILTROS}
<div class="sl-stage" id="sandim-loader" aria-hidden="true">
  <div class="sl-track">
    {LS.cenario()}
    <div class="sl-road"></div>
    {LS.rush()}
    {LS.rider(LS.moto_shopify(CORPO_URL))}
  </div>
  <div class="sl-word">
    <img src="{{{{ 'sandim-texto-negativo.svg' | asset_url }}}}" alt="Sandim R15 Store" width="1735" height="270">
    <div class="sl-bar"><i></i></div>
  </div>
</div>
<script>
(function(){{
  var el=document.getElementById('sandim-loader');
  try{{ if(sessionStorage.getItem('sandimLoader')){{ el.remove(); return; }} sessionStorage.setItem('sandimLoader','1'); }}catch(e){{}}
  var IDLE_MIN=1400, MAX_WAIT=6000;
  var wait=function(ms){{ return new Promise(function(r){{ setTimeout(r,ms); }}); }};
  var loaded=new Promise(function(r){{ if(document.readyState==='complete') r(); else window.addEventListener('load',r); }});
  el.style.setProperty('--sl-idle',IDLE_MIN+'ms');
  var spd=function(n){{ el.dataset.spd=n; }};
  el.classList.add('is-enter'); spd(3);
  setTimeout(function(){{ spd(2); }},380); setTimeout(function(){{ spd(1); }},640); setTimeout(function(){{ spd(0); }},860);
  wait(1000).then(function(){{
    el.classList.replace('is-enter','is-idle');
    return Promise.race([Promise.all([loaded,wait(IDLE_MIN)]),wait(MAX_WAIT)]);
  }}).then(function(){{
    el.classList.replace('is-idle','is-exit'); spd(1);
    setTimeout(function(){{ spd(2); }},120); setTimeout(function(){{ spd(3); }},280);
    return wait(800);
  }}).then(function(){{
    el.classList.add('is-done');
    setTimeout(function(){{ el.remove(); }},500);
  }});
}})();
</script>
'''
open('sandim-loader.liquid', 'w', encoding='utf8').write(liq)
print('liquid ok')
