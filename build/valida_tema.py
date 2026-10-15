"""Validação local do tema (sem Shopify CLI): JSON, schemas, blocos Liquid balanceados,
settings usados x declarados, snippets e assets referenciados."""
import json, os, re, glob, sys
R = 'tema'
erros, avisos = [], []

def rel(p): return os.path.relpath(p, R).replace('\\', '/')

# 1. JSON
for p in glob.glob(f'{R}/**/*.json', recursive=True):
    try:
        json.load(open(p, encoding='utf8'))
    except Exception as e:
        erros.append(f'{rel(p)}: JSON inválido: {e}')

# 2. Liquid: blocos balanceados + schema
PARES = {'if': 'endif', 'unless': 'endunless', 'for': 'endfor', 'case': 'endcase', 'form': 'endform',
         'paginate': 'endpaginate', 'capture': 'endcapture', 'comment': 'endcomment', 'schema': 'endschema',
         'style': 'endstyle', 'javascript': 'endjavascript', 'raw': 'endraw'}
FECHA = {v: k for k, v in PARES.items()}
schemas = {}
for p in glob.glob(f'{R}/**/*.liquid', recursive=True):
    s = open(p, encoding='utf8').read()
    # tags dentro de {% liquid %} viram linhas
    toks = []
    for m in re.finditer(r'\{%-?\s*(.*?)\s*-?%\}', s, re.S):
        corpo = m.group(1)
        if corpo.startswith('liquid'):
            for linha in corpo[6:].splitlines():
                linha = linha.strip()
                if linha:
                    toks.append(linha.split()[0])
        else:
            toks.append(corpo.split()[0] if corpo.split() else '')
    pilha = []
    dentro_comment = False
    for t in toks:
        if dentro_comment and t != 'endcomment':
            continue
        if t in PARES:
            pilha.append(t)
            if t == 'comment': dentro_comment = True
        elif t in FECHA:
            if t == 'endcomment': dentro_comment = False
            if not pilha or pilha[-1] != FECHA[t]:
                erros.append(f'{rel(p)}: "{t}" sem abertura correspondente (pilha={pilha[-3:]})'); break
            pilha.pop()
    if pilha:
        erros.append(f'{rel(p)}: blocos não fechados: {pilha}')
    sc = re.search(r'\{%-?\s*schema\s*-?%\}(.*?)\{%-?\s*endschema\s*-?%\}', s, re.S)
    if sc:
        try:
            schemas[rel(p)] = json.loads(sc.group(1))
        except Exception as e:
            erros.append(f'{rel(p)}: schema inválido: {e}')
    # snippets e assets referenciados
    for sn in re.findall(r"render\s+'([^']+)'", s):
        if not os.path.exists(f'{R}/snippets/{sn}.liquid'):
            erros.append(f'{rel(p)}: snippet inexistente "{sn}"')
    for a in re.findall(r"'([^']+\.(?:svg|css|js|png|jpg))'\s*\|\s*asset_url", s):
        if not os.path.exists(f'{R}/assets/{a}'):
            erros.append(f'{rel(p)}: asset inexistente "{a}"')
    # settings globais usados
    globais = {x['id'] for g in json.load(open(f'{R}/config/settings_schema.json', encoding='utf8')) for x in g.get('settings', []) if 'id' in x}
    for g in set(re.findall(r'(?<![\w.])settings\.([a-z_0-9]+)', s)):
        if g not in globais:
            erros.append(f'{rel(p)}: settings.{g} não existe em settings_schema.json')
    # settings da seção
    if p.startswith(f'{R}{os.sep}sections') and sc:
        sch = schemas[rel(p)]
        ids = {x['id'] for x in sch.get('settings', []) if 'id' in x}
        for u in set(re.findall(r'section\.settings\.([a-z_0-9]+)', s)):
            if u not in ids:
                erros.append(f'{rel(p)}: section.settings.{u} não declarado no schema')
        bids = {x['id'] for b in sch.get('blocks', []) for x in b.get('settings', []) if 'id' in x}
        for u in set(re.findall(r'block\.settings\.([a-z_0-9]+)', s)):
            if u not in bids:
                erros.append(f'{rel(p)}: block.settings.{u} não declarado no schema')

# 3. templates JSON apontam para seções existentes, com settings/blocos válidos
for p in glob.glob(f'{R}/templates/*.json') + glob.glob(f'{R}/sections/*-group.json'):
    d = json.load(open(p, encoding='utf8'))
    for k, sec in d.get('sections', {}).items():
        arq = f"sections/{sec['type']}.liquid"
        if arq not in schemas:
            erros.append(f'{rel(p)}: seção "{sec["type"]}" não existe'); continue
        sch = schemas[arq]
        ids = {x['id'] for x in sch.get('settings', []) if 'id' in x}
        for sk in sec.get('settings', {}):
            if sk not in ids: erros.append(f'{rel(p)}: setting "{sk}" não existe em {arq}')
        tipos = {b['type']: {x['id'] for x in b.get('settings', []) if 'id' in x} for b in sch.get('blocks', [])}
        for bk, b in sec.get('blocks', {}).items():
            if b['type'] not in tipos: erros.append(f'{rel(p)}: bloco "{b["type"]}" não existe em {arq}'); continue
            for sk in b.get('settings', {}):
                if sk not in tipos[b['type']]: erros.append(f'{rel(p)}: bloco {bk}: setting "{sk}" não existe')
        if 'block_order' in sec and set(sec['block_order']) != set(sec.get('blocks', {})):
            erros.append(f'{rel(p)}: block_order não bate com blocks em "{k}"')
    if set(d.get('order', [])) != set(d.get('sections', {})):
        erros.append(f'{rel(p)}: "order" não bate com "sections"')

# 4. estrutura mínima
for obrig in ['layout/theme.liquid', 'config/settings_schema.json', 'config/settings_data.json', 'templates/index.json', 'templates/product.json', 'templates/collection.json', 'templates/cart.json', 'templates/page.json', 'templates/search.json', 'templates/404.json']:
    if not os.path.exists(f'{R}/{obrig}'): erros.append(f'falta {obrig}')
if not glob.glob(f'{R}/locales/*.default.json'): erros.append('falta locale default')
lay = open(f'{R}/layout/theme.liquid', encoding='utf8').read()
for k in ['content_for_header', 'content_for_layout']:
    if k not in lay: erros.append(f'layout sem {k}')

print('arquivos:', len(glob.glob(f'{R}/**/*.*', recursive=True)), '| seções com schema:', len([s for s in schemas if s.startswith('sections')]))
for e in erros: print('ERRO ', e)
for a in avisos: print('aviso', a)
print('OK' if not erros else f'{len(erros)} erro(s)')
sys.exit(1 if erros else 0)
