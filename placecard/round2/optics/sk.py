from common import *
INKC='#111'; CUT='#d4281c'; FOLD='#1f5fd1'; GREY='#6b6b6b'; LGREY='#c9c9c9'
def T(x,y,s,size=5,fill=INKC,w=500,anchor='start',extra=''):
    return f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{w}" fill="{fill}" text-anchor="{anchor}" {extra}>{s}</text>'
def L(x1,y1,x2,y2,stroke=INKC,sw=1,dash=None,extra=''):
    d=f' stroke-dasharray="{dash}"' if dash else ''
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke}" stroke-width="{sw}"{d} {extra}/>'
def title(n,name,sub,W=1000):
    return (T(30,44,f'{n:02d}',34,INKC,700)+T(86,40,name,22,INKC,700)+T(86,60,sub,11.5,GREY,500))
def legend(x,y):
    return (L(x,y,x+26,y,CUT,1.6)+T(x+32,y+4,'cut',9,GREY)+L(x+66,y,x+92,y,FOLD,1.6,'5 3')+T(x+98,y+4,'fold / score',9,GREY)
            +f'<rect x="{x+170}" y="{y-5}" width="12" height="10" fill="{LEMON}" stroke="{LGREY}"/>'+T(x+188,y+4,'lemon card #feed95, black print',9,GREY))
def dim(x1,y1,x2,y2,label,off=0,size=8,horiz=True):
    s=L(x1,y1,x2,y2,GREY,0.7)
    if horiz:
        s+=L(x1,y1-3,x1,y1+3,GREY,0.7)+L(x2,y2-3,x2,y2+3,GREY,0.7)+T((x1+x2)/2,y1-4+off,label,size,GREY,500,'middle')
    else:
        s+=L(x1-3,y1,x1+3,y1,GREY,0.7)+L(x2-3,y2,x2+3,y2,GREY,0.7)+T(x1-5+off,(y1+y2)/2+3,label,size,GREY,500,'end')
    return s
def build(path,W,Hh,body):
    open(path,'w').write(svg_head(W,Hh,bg='#fbfaf7')+body+'\n</svg>\n')

import base64, io
from PIL import Image
def img_tag(path,x,y,w,h,maxw=520,q=82):
    im=Image.open(path).convert('RGB'); r=maxw/im.width
    if r<1: im=im.resize((maxw,int(im.height*r)))
    buf=io.BytesIO(); im.save(buf,'JPEG',quality=q)
    return f'<image x="{x}" y="{y}" width="{w}" height="{h}" preserveAspectRatio="xMidYMid slice" href="data:image/jpeg;base64,{base64.b64encode(buf.getvalue()).decode()}"/>'
def poly_svg(g,fill,stroke='none',sw=0,flipy=True,rule='evenodd'):
    return f'<path d="{geom_path(g,flipy=flipy)}" fill="{fill}" fill-rule="{rule}" stroke="{stroke}" stroke-width="{sw}"/>'
