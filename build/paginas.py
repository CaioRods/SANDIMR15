"""Migra as páginas institucionais da loja atual para site/paginas.json (HTML limpo, só tags seguras)."""
import json, re, html

PERMITIDAS = {'p', 'br', 'strong', 'b', 'em', 'i', 'ul', 'ol', 'li', 'h2', 'h3', 'h4', 'a'}

def limpa(h):
    h = re.sub(r'(?is)<(script|style)[^>]*>.*?</\1>', '', h)
    h = re.sub(r'(?i)<h1([^>]*)>', r'<h2\1>', h).replace('</h1>', '</h2>')
    def tag(m):
        fecha, nome, attrs = m.group(1), m.group(2).lower(), m.group(3) or ''
        if nome not in PERMITIDAS:
            return ''
        if nome == 'a' and not fecha:
            href = re.search(r'href="([^"]+)"', attrs)
            if href and re.match(r'(https?:|mailto:)', href.group(1)):
                return f'<a href="{href.group(1)}" target="_blank" rel="noopener">'
            return '<a>'
        return f'<{fecha}{nome}>'
    h = re.sub(r'<(/?)([a-zA-Z0-9]+)([^>]*)>', tag, h)
    h = re.sub(r'(<p>\s*(&nbsp;|\s)*</p>)', '', h)
    return re.sub(r'\n\s*\n+', '\n', h).strip()

out = {}
for pid, arq in [('privacidade', 'politica-de-privacidade'), ('trocas', 'trocas-e-devolucoes'), ('envio', 'envio-e-prazo-de-entrega')]:
    d = json.load(open(f'dados/paginas/{arq}.json', encoding='utf8'))['page']
    out[pid] = {'titulo': d['title'], 'html': limpa(d['body_html'])}
for pid, arq, tit in [('termos', 'terms-of-service', 'Termos de serviço')]:
    s = open(f'dados/paginas/pol-{arq}.html', encoding='utf8').read()
    m = re.search(r'(?s)<div class="shopify-policy__body">(.*?)</div>\s*</div>', s) or re.search(r'(?s)<div class="rte">(.*?)</div>', s)
    t = re.search(r'(?s)<h1[^>]*>(.*?)</h1>', s)
    out[pid] = {'titulo': html.unescape(re.sub('<[^>]+>', '', t.group(1))).strip() if t else tit, 'html': limpa(m.group(1)) if m else ''}
json.dump(out, open('site/paginas.json', 'w', encoding='utf8'), ensure_ascii=False)
for k, v in out.items():
    print(k, '|', v['titulo'], '|', len(v['html']), 'chars')
