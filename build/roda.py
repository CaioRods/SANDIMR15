"""Gera uma roda completa replicando um setor limpo do aro dianteiro do logo."""
import numpy as np, math
from PIL import Image
b=np.array(Image.open('build/bike.png'))<128          # máscara 2x (True = preto)
cx,cy,R=np.load('build/frente_fit.npy')               # coordenadas 2x
R=R+1.5
N=int(2*R)+4; c=N/2
yy,xx=np.mgrid[0:N,0:N]; dx,dy=xx-c,yy-c
r=np.hypot(dx,dy); th=np.degrees(np.arctan2(dy,dx))
A0,SPAN=-75.5,36.0
ths=A0+np.mod(th-A0,SPAN)
sx=np.clip(np.round(cx+r*np.cos(np.radians(ths))).astype(int),0,b.shape[1]-1)
sy=np.clip(np.round(cy+r*np.sin(np.radians(ths))).astype(int),0,b.shape[0]-1)
out=b[sy,sx]
out[r<0.33*R]=True          # cubo
out[r>R]=False
Image.fromarray(np.where(out,0,255).astype('uint8')).save('build/roda-completa.png')
print('roda',N,'px (2x), raio 1x',R/2)
