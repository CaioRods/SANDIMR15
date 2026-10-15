"""Gera tema/snippets/loader.liquid e junta os estilos do loading em tema/assets/sandim.css."""
import sys; sys.path.insert(0, 'build')
import loader_svg as LS
corpo = "{{ 'moto-loading-corpo.svg' | asset_url }}"
texto = "{{ 'texto-negativo.svg' | asset_url }}"
snip = ('{%- comment -%} Tela de carregamento: aparece uma vez por sessão. Gerado por build/tema_loader.py {%- endcomment -%}\n'
        + LS.FILTROS + '\n'
        '<div class="sl-stage" id="sandim-loader" aria-hidden="true">'
        '<div class="sl-track">' + LS.cenario() + '<div class="sl-road"></div>' + LS.rush() + LS.rider(LS.moto_shopify(corpo)) + '</div>'
        '<div class="sl-word"><img src="' + texto + '" alt="" width="1735" height="270"><div class="sl-bar"><i></i></div></div>'
        '</div>\n'
        '<script>try{if(sessionStorage.getItem("sandimLoader")){document.getElementById("sandim-loader").remove()}}catch(e){}</script>\n')
open('tema/snippets/loader.liquid', 'w', encoding='utf8').write(snip)
print('loader.liquid', len(snip) // 1024, 'KB')
