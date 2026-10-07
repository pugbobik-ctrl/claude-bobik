from c3 import *
from sk import *
INKC='#111'
import json
R=json.load(open(f'{OUT}/c3_results.json'))
xt,zc=design('1 RUB'); parts=assemble('1 RUB',xt,zc); M,xc,zcm,Ip=props(parts)
tail_len=-zc+COINS['1 RUB'][1]/2-3
W_,H_=1000,780
b=title(3,'Rim Walker','A name panel perched on the rim of your wine glass, held up by a coin hanging inside it. It nods, wobbles and never falls.')
b+=legend(30,762)
k=2.05
def wall(z): return 14*np.sin(np.pi*np.clip(-z,0,100)/100)**0.9
def rot(pts,th):
    c,s=np.cos(th),np.sin(th); return [(x*c-z*s,x*s+z*c) for x,z in pts]
def frame(cx,cy,th_deg,label):
    P=lambda x,z:(cx+k*x,cy-k*z)
    th=np.radians(th_deg); g=''
    zs=np.linspace(0,-100,40)
    rpts=[P(wall(z),z) for z in zs]; lpts=[P(-64-wall(z),z) for z in zs]
    bowl=' L'.join(f'{x:.1f},{y:.1f}' for x,y in rpts)+f' Q{P(0,-122)[0]:.1f},{P(0,-122)[1]:.1f} {P(-32,-124)[0]:.1f},{P(-32,-124)[1]:.1f} Q{P(-64,-122)[0]:.1f},{P(-64,-122)[1]:.1f} '+' L'.join(f'{x:.1f},{y:.1f}' for x,y in lpts[::-1])
    g+=f'<path d="M{bowl}" fill="#e9f1f7" fill-opacity=".55" stroke="#2b3a46" stroke-width="1.4"/>'
    g+=L(*P(-32,-124),*P(-32,-168),'#2b3a46',1.4)+f'<ellipse cx="{P(-32,-170)[0]:.1f}" cy="{P(-32,-170)[1]:.1f}" rx="{k*26:.1f}" ry="4" fill="none" stroke="#2b3a46" stroke-width="1.4"/>'
    # card parts (edge-on)
    def poly(pts,fill,stroke=INKC,sw=0.9):
        q=rot(pts,th); return f'<polygon points="{" ".join(f"{P(x,z)[0]:.1f},{P(x,z)[1]:.1f}" for x,z in q)}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'
    t=0.7
    g+=poly([(xt-1,t),(XP+t,t),(XP+t,-t),(xt-1,-t)],LEMON)                      # strip
    g+=poly([(XP-t,0),(XP+t,0),(XP+t,PANEL_H),(XP-t,PANEL_H)],LEMON)            # panel
    g+=poly([(xt-t,0),(xt+t,0),(xt+t,-tail_len),(xt-t,-tail_len)],LEMON)        # tail
    # coin
    cc=rot([(xt,zc)],th)[0]; cp=P(*cc)
    g+=f'<circle cx="{cp[0]:.1f}" cy="{cp[1]:.1f}" r="{k*10.25:.1f}" fill="#d9b44a" stroke="#7a5d00" stroke-width="1.2"/>'
    # pocket
    g+=poly([(xt-12,zc-12),(xt+12,zc-12),(xt+12,zc+12),(xt-12,zc+12)],'none','#8a8a8a',0.8).replace('<polygon','<polygon stroke-dasharray="3 2"')
    # pivot + CoM
    pv=P(0,0); g+=f'<polygon points="{pv[0]-5:.1f},{pv[1]+9:.1f} {pv[0]+5:.1f},{pv[1]+9:.1f} {pv[0]:.1f},{pv[1]:.1f}" fill="{CUT}"/>'
    com=rot([(xc,zcm)],th)[0]; cm=P(*com)
    g+=L(pv[0],pv[1],pv[0],pv[1]+k*60,'#d4281c',0.9,'4 3')
    g+=f'<circle cx="{cm[0]:.1f}" cy="{cm[1]:.1f}" r="5" fill="#fff" stroke="#1f5fd1" stroke-width="1.6"/><path d="M{cm[0]-5:.1f},{cm[1]:.1f} h10 M{cm[0]:.1f},{cm[1]-5:.1f} v10" stroke="#1f5fd1" stroke-width="1.2"/>'
    return g,P
fy=222
for i,(cx,th,lab) in enumerate(((190,-22,'nudged away: coin swings up, gravity pulls it back'),(500,0,'at rest: CoM straight under the rim'),(810,22,'nudged toward glass: same, mirrored'))):
    g,P=frame(cx,fy,th,lab); b+=f'<clipPath id="cl{i}"><rect x="{cx-150}" y="70" width="300" height="{fy+k*84-70}"/></clipPath><g clip-path="url(#cl{i})">'+g+'</g>'; b+=T(cx,fy+k*84+24,lab,9.5,INKC,700,'middle'); b+=L(cx-130,fy+k*84,cx+130,fy+k*84,GREY,0.7,'2 3')
b+=T(30,98,'side view, section through glass and card (guest on the right, outside the glass)',10,INKC,700)
# annotations on middle frame
cx=500; P=lambda x,z:(cx+k*x,fy-k*z)
b+=T(*P(XP+4,PANEL_H+6),'name panel 90 x 45',8.5,INKC,500,'middle')
b+=T(*P(5,12),'rim = pivot',8.5,'#a3190f',700,'start')
b+=T(*P(-62,-17),'CoM',8.5,'#1f5fd1',700)
b+=T(*P(-16,-47),f'1 RUB coin {COINS["1 RUB"][0]} g',8.5,'#7a5d00',700,'middle')
b+=T(*P(-34,10),'strip over the rim',8.5,GREY,500,'middle')
b+=dim(*P(XP+16,0),*P(XP+16,-15),'',horiz=False)
b+=T(*P(XP+22,-6),f'{-zcm:.0f} mm',8.5,'#1f5fd1',700)
# physics image
b+=img_tag(f'{OUT}/c3_physics.png',30,468,560,200,maxw=1100)
b+=T(30,460,'computed from the actual masses (300 gsm card, 1 RUB coin): potential well and ring-down',9.5,INKC,700)
# numbers
yy=692
b+=T(30,yy,f'mass {M:.1f} g  |  CoM {-zcm:.0f} mm below the rim, 0.0 mm off-axis  |  pitch period {R["design"]["period_s"]:.2f} s',9.5,INKC,700)
b+=T(30,yy+15,'different coin in the same pocket: 2 RUB leans 11 deg, 10 RUB 12 deg, 5 RUB 13 deg (still stable). No coin: panel tips off.',9,GREY,500)
b+=T(30,yy+29,'card 250 gsm: +5 deg lean; 350 gsm: -6 deg; sliding the coin 1 mm in its pocket trims ~2.5 deg. The guest can tune it.',9,GREY,500)
b+=T(30,yy+43,'The coin hangs 15-45 mm below the rim: above any normal wine level, clear of the glass wall at rest.',9,GREY,500)
# dieline (right column)
s=1.5; ox=660; oy=490
b+=T(ox,oy-22,'cut + score (one piece, lemon 300 gsm)',10,INKC,700)
b+=f'<g transform="translate({ox},{oy}) scale({s})">'
PW=PANEL_W; PH=PANEL_H; SW=STRIP_W; SL=XP-xt
cxm=PW/2
b+=f'<rect x="0" y="0" width="{PW}" height="{PH}" rx="3" fill="{LEMON}" stroke="{CUT}" stroke-width="1.2" vector-effect="non-scaling-stroke"/>'
b+=f'<text x="{cxm}" y="17" font-size="10.5" font-weight="700" fill="{INKC}" text-anchor="middle">Sophia</text><text x="{cxm}" y="31" font-size="10.5" font-weight="700" fill="{INKC}" text-anchor="middle">Zhuravkova</text><text x="{cxm}" y="41" font-size="4" font-weight="500" fill="{INKC}" text-anchor="middle">стол 3 · место 7</text>'
b+=f'<rect x="{cxm-SW/2}" y="{PH}" width="{SW}" height="{SL}" fill="{LEMON}" stroke="{CUT}" stroke-width="1.2" vector-effect="non-scaling-stroke"/>'
b+=L(0,PH,PW,PH,FOLD,1,'4 2','vector-effect="non-scaling-stroke"')
b+=L(cxm-SW/2-2,PH+SL-(SL-XP+0),cxm+SW/2+2,PH+SL-(SL-XP+0),FOLD,1,'4 2','vector-effect="non-scaling-stroke"') if False else ''
ry=PH+XP  # ridge at pivot, XP mm from panel fold
b+=L(cxm-SW/2-2,ry,cxm+SW/2+2,ry,FOLD,1,'1.5 1.5','vector-effect="non-scaling-stroke"')
ty0=PH+SL
b+=L(cxm-SW/2,ty0,cxm+SW/2,ty0,FOLD,1,'4 2','vector-effect="non-scaling-stroke"')
b+=f'<rect x="{cxm-SW/2}" y="{ty0}" width="{SW}" height="{tail_len}" fill="{LEMON}" stroke="{CUT}" stroke-width="1.2" vector-effect="non-scaling-stroke"/>'
# pocket (two flaps)
py0=ty0+tail_len
b+=f'<rect x="{cxm-13}" y="{py0}" width="26" height="27" rx="2" fill="{LEMON}" stroke="{CUT}" stroke-width="1.2" vector-effect="non-scaling-stroke"/>'
b+=L(cxm-13,py0+27,cxm+13,py0+27,FOLD,1,'4 2','vector-effect="non-scaling-stroke"')
b+=f'<rect x="{cxm-13}" y="{py0+27}" width="26" height="27" rx="2" fill="{LEMON}" stroke="{CUT}" stroke-width="1.2" vector-effect="non-scaling-stroke"/>'
b+=f'<circle cx="{cxm}" cy="{py0+13.5}" r="10.25" fill="none" stroke="#7a5d00" stroke-width="0.6" stroke-dasharray="2 1.5"/>'
b+='</g>'
b+=T(ox+PW*s+8,oy+PH*s/2+3,'panel (printed black)',8.5,GREY,500)
b+=T(ox+PW*s+8,oy+(PH+SL/2)*s,'strip 10 wide',8.5,GREY,500)
b+=T(ox+PW*s+8,oy+ry*s+3,'ridge fold: the knife edge',8.5,'#1f5fd1',700)
b+=T(ox+PW*s+8,oy+(ty0+tail_len/2)*s,'tail',8.5,GREY,500)
b+=T(ox+PW*s+8,oy+(py0+20)*s,'coin pocket (fold, glue sides)',8.5,GREY,500)
build(f'{OUT}/c3_sketch.svg',W_,H_,b)
