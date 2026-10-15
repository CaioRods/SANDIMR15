"""Moto do loading: corpo do logo sem as rodas originais + rodas completas menores."""
import numpy as np
from PIL import Image, ImageDraw
S = 0.84                                   # escala das rodas novas
b = np.array(Image.open('build/bike.png')) < 128          # 2x
fx, fy, R = np.load('build/frente_fit.npy')               # 2x
rx, ry = 784.4 * 2, fy            # centro da roda nova
ox, oy = 783.4 * 2, 419.2 * 2      # centro da roda traseira original
H, W = b.shape
yy, xx = np.mgrid[0:H, 0:W]
rf = np.hypot(xx - fx, yy - fy); rr = np.hypot(xx - ox, yy - oy)
corpo = b.copy()
corpo[rf <= R + 8] = False                                  # dianteira: tudo
corpo[(rr <= R + 8) & ((rr >= 0.70 * R) & (xx < 810 * 2) | (xx < 735 * 2) | ((xx < 765 * 2) & (((xx - 765 * 2) / 60.0) ** 2 + ((yy - 372 * 2) / 130.0) ** 2 > 1)))] = False   # traseira: pneu e aro, mantém escapamento
img = Image.fromarray(corpo)
d = ImageDraw.Draw(img)
k = 2
d.polygon([(1384*k,262*k),(1418*k,258*k),(1456*k,442*k),(1428*k,442*k)], fill=True)      # garfo
d.ellipse([(1442.6-14)*k,(441.7-14)*k,(1442.6+14)*k,(441.7+14)*k], fill=True)
corpo = np.array(img)
Image.fromarray(np.where(corpo, 0, 255).astype('uint8')).save('build/corpo-loader.png')
# prévia
roda = Image.open('build/roda-completa.png').convert('L')
n = int(roda.width * S); roda = roda.resize((n, n), Image.LANCZOS)
prev = Image.new('L', (W, H + 400), 255)
for cx, cy in ((rx, ry), (fx, fy)):
    m = roda.point(lambda v: 255 if v < 128 else 0)
    prev.paste(0, (int(cx - n / 2), int(cy - n / 2)), m)
c = Image.fromarray(np.where(corpo, 0, 255).astype('uint8'))
prev.paste(0, (0, 0), c.point(lambda v: 255 if v < 128 else 0))
prev.crop((1100, 0, 3300, H + 300)).resize((1100, (H + 300) // 2)).save('build/previa-loader.png')
print('ok')
