"""Ícone da página (capacete): gera os PNGs do site e do tema a partir de assets/capacete.webp."""
from PIL import Image

src = Image.open('assets/capacete.webp').convert('RGBA')
src = src.crop(src.getbbox())  # corta a margem transparente

def quadrado(lado, margem=0.04, fundo=None):
    """Centraliza o capacete num quadrado; fundo opcional (iOS não aceita transparência)."""
    tela = Image.new('RGBA', (lado, lado), fundo or (0, 0, 0, 0))
    util = round(lado * (1 - 2 * margem))
    w, h = src.size
    k = util / max(w, h)
    im = src.resize((round(w * k), round(h * k)), Image.LANCZOS)
    tela.alpha_composite(im, ((lado - im.width) // 2, (lado - im.height) // 2))
    return tela

quadrado(192).save('site/favicon.png', optimize=True)
quadrado(180, 0.10, (255, 255, 255, 255)).convert('RGB').save('site/apple-touch-icon.png', optimize=True)
quadrado(192).save('tema/assets/favicon.png', optimize=True)
quadrado(180, 0.10, (255, 255, 255, 255)).convert('RGB').save('tema/assets/apple-touch-icon.png', optimize=True)
quadrado(256, 0.02).save('site/favicon.ico', sizes=[(16, 16), (32, 32), (48, 48)])
print('favicon ok')
