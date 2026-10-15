"""Empacota tema/ em sandim-r15-tema.zip (pastas na raiz do zip, como a Shopify espera)."""
import os, zipfile
destino = 'sandim-r15-tema.zip'
with zipfile.ZipFile(destino, 'w', zipfile.ZIP_DEFLATED) as z:
    for raiz, _, arquivos in os.walk('tema'):
        for a in sorted(arquivos):
            p = os.path.join(raiz, a)
            z.write(p, os.path.relpath(p, 'tema').replace('\\', '/'))
with zipfile.ZipFile(destino) as z:
    nomes = z.namelist()
print(destino, os.path.getsize(destino) // 1024, 'KB,', len(nomes), 'arquivos')
print(sorted({n.split('/')[0] for n in nomes}))
