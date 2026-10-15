# Sandim R15 Store

Redesign da loja [sandimr15.store](https://sandimr15.store) (Shopify): identidade visual, protótipo do site novo e tema Shopify.

Desenvolvido por **CRdevs** · [@caio.riguess](https://www.instagram.com/caio.riguess/)

## Pastas

| Pasta | O que tem |
|---|---|
| `identidade.html` | Página de identidade visual (logo, versões, paleta, tipografia, loading animado) |
| `site/` | Protótipo do site novo (tema claro, mobile primeiro) com o catálogo real da loja |
| `logo/` | Logo vetorizado em SVG (cores, negativo, grafite, branco, só a moto, só o texto) |
| `tema/` | Tema Shopify (Online Store 2.0) — **em atualização**, ainda não reflete o protótipo atual |
| `sandim-loader.liquid` | Snippet da tela de carregamento para o Shopify |
| `build/` | Scripts que geram tudo acima (vetorização, loading, catálogo, tema) |
| `dados/` | Catálogo público da loja atual (`products.json`, coleções e páginas) |
| `assets/` | Arte original do logo aprovado |

## Ver o protótipo

```bash
python -m http.server 8765
```

Depois abra `http://localhost:8765/site/` (o catálogo é carregado por `fetch`, então precisa de um servidor local).

## Regenerar

```bash
python build/catalogo.py   # catálogo a partir de dados/
python build/site.py       # site/index.html
python build/compor.py     # logos e identidade.html
```
