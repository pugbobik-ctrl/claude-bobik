from c1_sim import *
from sk import *
G=name_geometry(); card=design(0,D0,G); Wc=card.W
cw,ch=card.w,card.h; cx=card.cx
W_,H_=1000,650
b=title(1,'Under the Lamp','Pierced screen: the table lamp throws your name onto your plate. The card itself reads upside-down; light un-warps it.')
b+=legend(30,630)
# --- dieline group (1 mm = 2.05 units)
s=1.95; ox,oy=36+(card.w/2-card.cx)*1.95,262
b+=f'<g transform="translate({ox},{oy}) scale({s})">'
b+=f'<rect x="{cx-cw/2:.2f}" y="{-ch}" width="{cw:.2f}" height="{ch}" fill="{LEMON}" stroke="{CUT}" stroke-width="1.4" vector-effect="non-scaling-stroke" rx="3"/>'
b+=f'<path d="{geom_path(Wc,flipy=True)}" fill="#fbfaf7" fill-rule="evenodd" stroke="{CUT}" stroke-width="1" vector-effect="non-scaling-stroke"/>'
# print band (black ink) + tiny name, bottom 14 mm
b+=f'<rect x="{cx-cw/2:.2f}" y="-13" width="{cw:.2f}" height="13" fill="{INKC}"/>'
b+=f'<text x="{cx-cw/2+4:.2f}" y="-4.6" font-size="5.2" font-weight="700" fill="{LEMON}">Sophia Zhuravkova</text>'
b+=f'<text x="{cx+cw/2-4:.2f}" y="-4.6" font-size="4.2" font-weight="500" fill="{LEMON}" text-anchor="end">стол 3 · место 7</text>'
# feet slots (open at bottom)
for fx in (cx-33,cx+33):
    b+=f'<rect x="{fx-0.3:.2f}" y="-10" width="0.6" height="10" fill="#fbfaf7" stroke="{CUT}" stroke-width="1" vector-effect="non-scaling-stroke"/>'
# foot piece (2x)
fx0,fy0=cx-45,22
b+=f'<rect x="{fx0}" y="{fy0}" width="90" height="26" fill="{LEMON}" stroke="{CUT}" stroke-width="1.4" vector-effect="non-scaling-stroke" rx="3"/>'
b+=f'<rect x="{cx-0.3}" y="{fy0}" width="0.6" height="10" fill="#fbfaf7" stroke="{CUT}" stroke-width="1" vector-effect="non-scaling-stroke"/>'
b+=f'<text x="{cx}" y="{fy0+20}" font-size="4.6" font-weight="500" fill="{INKC}" text-anchor="middle">foot  x2 — slots into the card</text>'
b+='</g>'
# dims
b+=dim(ox+(cx-cw/2)*s,oy+14,ox+(cx+cw/2)*s,oy+14,f'{cw:.0f} mm',off=-1,size=9)
b+=dim(ox+(cx-cw/2)*s-14,oy-ch*s,ox+(cx-cw/2)*s-14,oy,f'{ch:.0f}',horiz=False,size=9)
b+=T(36,oy-ch*s-12,'cut file  (laser or plotter-cut, front view as the guest sees it)',10,INKC,700)
b+=T(36,oy+142,'No ink on the pierced zone: black band + name only along the bottom 13 mm.',9,GREY)
b+=T(36,oy+156,'Bridges (stencil islands for o, p, a) 1.0-1.6 mm; use 350 gsm to survive handling.',9,GREY)
b+=T(36,oy+170,'Per-seat file: pattern is re-computed from the floor plan (lamp x, y) by script.',9,GREY)
# --- side section (1 mm = 0.40 units)
k=0.42; sx,sy=742,480
def P(y,z): return (sx+k*y, sy-k*z)
b+=T(560,120,'section through the table, seen from the end',10,INKC,700)
# table
b+=L(*P(-560,0),*P(560,0),INKC,1.5)
# plate
pts=[P(-270,0),P(-262,18),P(-8,18),P(0,0)]
b+=f'<polygon points="{" ".join(f"{x:.1f},{y:.1f}" for x,y in pts)}" fill="#fff" stroke="{INKC}" stroke-width="1"/>'
# card
b+=f'<rect x="{P(-1.5,84)[0]:.1f}" y="{P(0,84)[1]:.1f}" width="{k*3:.1f}" height="{k*84:.1f}" fill="{LEMON}" stroke="{INKC}" stroke-width="1"/>'
# lamp
lx,lz=D0,H
b+=L(*P(lx,0),*P(lx,lz-14),INKC,1.2)+f'<ellipse cx="{P(lx,0)[0]:.1f}" cy="{P(lx,0)[1]:.1f}" rx="{k*55:.1f}" ry="2.2" fill="{INKC}"/>'
b+=f'<polygon points="{P(lx-10,420)[0]:.1f},{P(lx-10,420)[1]:.1f} {P(lx+10,420)[0]:.1f},{P(lx+10,420)[1]:.1f} {P(lx+95,330)[0]:.1f},{P(lx+95,330)[1]:.1f} {P(lx-95,330)[0]:.1f},{P(lx-95,330)[1]:.1f}" fill="{INKC}"/>'
b+=f'<circle cx="{P(lx,lz)[0]:.1f}" cy="{P(lx,lz)[1]:.1f}" r="{k*14:.1f}" fill="#fff3b0" stroke="{INKC}" stroke-width="1"/>'
# rays
zb,zt=18.6,66.7
for z,col in ((zb,'#e0a800'),(zt,'#e0a800')):
    Y=D0*z/(H-z)
    b+=L(*P(lx,lz),*P(-Y,0),col,1,'none') .replace('stroke-dasharray="none"','')
    b+=L(*P(lx,lz),*P(0,z),col,1)
Yb=D0*zb/(H-zb); Yt=D0*zt/(H-zt)
b+=f'<rect x="{P(-Yt,0)[0]:.1f}" y="{sy-3:.1f}" width="{k*(Yt-Yb):.1f}" height="3" fill="#e0a800"/>'
b+=T(*P(-Yt-20,44),'name lands here',8.5,'#8a6a00',700,'end')
b+=T(*P(-330,10),'plate 270',8.5,GREY,500,'end')
# eye
ex_,ey_=P(-450,430)
b+=f'<circle cx="{ex_:.1f}" cy="{ey_:.1f}" r="6" fill="#fff" stroke="{INKC}" stroke-width="1.2"/><circle cx="{ex_+1.5:.1f}" cy="{ey_:.1f}" r="2.2" fill="{INKC}"/>'
b+=L(ex_,ey_,*P(-(Yb+Yt)/2,0),INKC,0.8,'3 2')
b+=T(ex_-6,ey_-12,'guest eye  430 above / 450 from card',8.5,INKC,500,'start')
b+=T(*P(lx+60,455),'cone lamp, bare bulb 300 mm up',8.5,INKC,500,'end')
b+=dim(*P(0,-30),*P(lx,-30),f'lamp marked {D0:.0f} mm beyond card',off=16,size=8.5)
b+=T(*P(-10,90),f'card {ch:.0f} mm',8.5,INKC,500,'end')
# notes
b+=T(560,560,'Shadow = projection of the holes through the bulb onto the plate (z=0):',9.5,INKC,700)
b+=T(560,574,'   Y = D*z/(H-z),  x_shadow = x*H/(H-z)   (D 450, H 300)',9.5,INKC,500)
b+=T(560,590,'Hole at height z on the card → shadow at depth Y; pre-warped so the eye at',9.5,GREY,500)
b+=T(560,604,'(0,-450,430) sees an upright, undistorted two-line name.',9.5,GREY,500)
b+=T(560,626,'Needs: clear filament / LED bulb ≤ 25 mm, lamp on its taped mark ±60 mm.',9.5,'#a3190f',700)
build(f'{OUT}/c1_sketch.svg',W_,H_,b)
