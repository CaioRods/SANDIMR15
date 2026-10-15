"""Monta site/index.html a partir de build/site.src.html (loading + símbolos do logo)."""
import sys, shutil; sys.path.insert(0, 'build')
import loader_svg as LS
src = open('build/site.src.html', encoding='utf8').read()
rep = {
    '{{LOADER_CSS}}': open('build/loader.css', encoding='utf8').read(),
    '{{SIMBOLOS}}': open('build/simbolos.html', encoding='utf8').read(),
    '{{FILTROS}}': LS.FILTROS, '{{CENA}}': LS.cenario(), '{{RUSH}}': LS.rush(),
    '{{RIDER}}': LS.rider(LS.moto_svg()),
}
import time
ver = str(int(time.time()))
rep['estilo.css"'] = 'estilo.css?v=' + ver + '"'
rep['app.js"'] = 'app.js?v=' + ver + '"'
rep['lupa.js"'] = 'lupa.js?v=' + ver + '"'
rep['whats.js"'] = 'whats.js?v=' + ver + '"'
rep['cinema.css"'] = 'cinema.css?v=' + ver + '"'
rep['cinema.js"'] = 'cinema.js?v=' + ver + '"'
rep['limpo.css"'] = 'limpo.css?v=' + ver + '"'
rep['claro.css"'] = 'claro.css?v=' + ver + '"'
rep['azul.css"'] = 'azul.css?v=' + ver + '"'
for k, v in rep.items():
    assert k in src, k
    src = src.replace(k, v)
open('site/index.html', 'w', encoding='utf8').write(src)
import runpy; runpy.run_path('build/leve2.py')
print('site ok', len(src) // 1024, 'KB')
