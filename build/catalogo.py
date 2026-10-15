"""Normaliza o catálogo público da loja (products.json) para o protótipo: site/catalogo.json."""
import json, glob, os, re, html
prods = {}
for f in sorted(glob.glob('dados/products-*.json')):
    for p in json.load(open(f, encoding='utf8'))['products']:
        prods[p['handle']] = p
cols = {c['handle']: c['title'] for c in json.load(open('dados/collections.json', encoding='utf8'))['collections']}
mem = {}
for f in glob.glob('dados/col-*.json'):
    h = os.path.basename(f)[4:-5]
    for i, p in enumerate(json.load(open(f, encoding='utf8'))['products']):
        mem.setdefault(p['handle'], {})[h] = i

EMOJI = re.compile('[\U0001F000-\U0001FFFF☀-➿️]')
def limpa(t):
    t = EMOJI.sub('', t)
    t = re.sub(r'\s*\|\s*(Menor Preço Histórico|Novidade)\s*', ' ', t, flags=re.I)
    t = re.sub(r'Yamaha\s+Yzf', 'Yamaha YZF', t, flags=re.I)
    t = re.sub(r'YZF[\s-]?R15', 'YZF-R15', t)
    t = re.sub(r'YZF[\s-]?R3', 'YZF-R3', t)
    t = re.sub(r'\s{2,}', ' ', t).strip(' |-')
    return t
ANO = re.compile(r'\s*\(?\s*(20\d\d)\s*(?:a|-|–|até)\s*(20\d\d)\s*\)?|\s*\b(20\d\d)\b')
def anos(t):
    m = ANO.search(t)
    if not m: return None, t
    faixa = f'{m.group(1)}–{m.group(2)}' if m.group(1) else m.group(3)
    limpo = (t[:m.start()] + t[m.end():]).strip(' |-')
    return faixa, re.sub(r'\s{2,}', ' ', limpo)
def motos(p, m):
    t = p['title'].upper()
    r = []
    if 'R15' in t or 'acessorios' in m: r.append('R15')
    if 'R3' in t.replace('R30', '') or 'acessorios-r3' in m: r.append('R3')
    if 'SBM' in t or 'sbm-250s' in m: r = ['SBM']
    return r or ['R15']
def texto(h):
    h = re.sub(r'<(br|/p|/li|/h\d)[^>]*>', '\n', h or '', flags=re.I)
    h = re.sub(r'<li[^>]*>', '• ', h, flags=re.I)
    t = html.unescape(re.sub(r'<[^>]+>', '', h))
    t = EMOJI.sub('', t)
    return '\n'.join(l.strip() for l in t.splitlines() if l.strip())[:1800]
out = []
for h, p in prods.items():
    v = p['variants']
    precos = [float(x['price']) for x in v]
    barata = min(v, key=lambda x: float(x['price']))          # o "de" acompanha a variação mais barata, como na loja
    de = [float(barata['compare_at_price'])] if barata.get('compare_at_price') and float(barata['compare_at_price']) > float(barata['price']) else []
    m = mem.get(h, {})
    out.append({
        'h': h, 't': anos(limpa(p['title']))[1], 'anos': anos(limpa(p['title']))[0], 'orig': p['title'],
        'ok': any(x.get('available', True) for x in v),
        'preco': min(precos), 'varia': len(set(precos)) > 1,
        'de': max(de) if de else None,
        'img': [i['src'].split('?')[0] for i in p['images'][:6]],
        'op': [o['name'] for o in p['options'] if o['name'] != 'Title'],
        'v': [{'t': x['title'], 'p': float(x['price']), 'd': float(x['compare_at_price']) if x.get('compare_at_price') else None,
               'ok': x.get('available', True), 'img': (x.get('featured_image') or {}).get('src', '').split('?')[0]} for x in v],
        'col': m, 'moto': motos(p, m), 'tipo': p.get('product_type', ''),
        'desc': texto(p.get('body_html')), 'data': p.get('published_at', ''),
    })
json.dump({'colecoes': cols, 'produtos': out}, open('site/catalogo.json', 'w', encoding='utf8'), ensure_ascii=False)
from collections import Counter
print(len(out), 'produtos;', Counter(x for p in out for x in p['moto']))
print({c: sum(1 for p in out if c in p['col']) for c in cols})
print([p['t'] for p in out[:8]])
