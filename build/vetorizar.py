import re, sys, numpy as np, vtracer
from PIL import Image, ImageFilter
from scipy import ndimage as nd
S=2
im=Image.open('assets/logo-cliente.webp').convert('RGBA')
im=im.resize((im.width*S,im.height*S),Image.LANCZOS)
a=np.array(im).astype(int); r,g,b,al=a[...,0],a[...,1],a[...,2],a[...,3]
op=al>110
black=op&(r+g+b<260)
blue=op&(b>140)&(r<140)&~black
def comps(mask):
    lab,n=nd.label(mask); out=[]
    for i,sl in enumerate(nd.find_objects(lab),1):
        out.append((i,sl,lab))
    return lab,n
layers={}
lab,n=nd.label(black)
objs=nd.find_objects(lab)
bike=np.zeros_like(black); text=np.zeros_like(black)
for i,sl in enumerate(objs,1):
    if sl is None: continue
    y0=sl[0].start/S
    (bike if y0<400 else text)[lab==i]=True
lab,n=nd.label(blue); objs=nd.find_objects(lab)
stripe=np.zeros_like(blue); speed=np.zeros_like(blue); btext=np.zeros_like(blue)
for i,sl in enumerate(objs,1):
    if sl is None: continue
    y0,x0,x1=sl[0].start/S,sl[1].start/S,sl[1].stop/S
    if (sl[0].stop-sl[0].start)*(sl[1].stop-sl[1].start)<60: continue
    if x0>760 and y0<400: stripe[lab==i]=True
    elif x1<720 and y0<440: speed[lab==i]=True
    else: btext[lab==i]=True
res={}
for name,m in [('bike',bike),('text',text),('stripe',stripe),('speed',speed),('btext',btext)]:
    m=nd.binary_opening(m,iterations=1)
    Image.fromarray(np.where(m,0,255).astype('uint8')).save(f'build/{name}.png')
    vtracer.convert_image_to_svg_py(f'build/{name}.png',f'build/{name}.svg',colormode='binary',mode='spline',filter_speckle=8,corner_threshold=70,length_threshold=4.0,splice_threshold=45,path_precision=1)
    svg=open(f'build/{name}.svg').read()
    paths=re.findall(r'<path d="([^"]+)"[^>]*?transform="translate\(([-\d.]+),([-\d.]+)\)"',svg)
    res[name]=paths
    ys,xs=np.where(m); print(name,len(paths),'bbox',xs.min()/S,ys.min()/S,xs.max()/S,ys.max()/S)
import json; json.dump(res,open('build/paths.json','w'))
