from sk import *
from c2b import *
INKC="#111"
W_,H_=1000,762
b=title(2,'Seat-Lock','Three stacked flats, each carries one slice of the name. The slices line up from your seat only; lean, and the name tears.')
b+=legend(30,750)
# --- dieline: three cards
s=1.42; ox=36; oy=122
TAB=8
for k,(c,ink) in enumerate(zip(CARDS,INK)):
    y0=oy+k*(HC*s+TAB*s+30)
    b+=f'<g transform="translate({ox},{y0+HC*s}) scale({s})">'
    # body with tabs (y up in card coords -> flip)
    tabs=''.join(f'<rect x="{tx}" y="0" width="22" height="{TAB}" fill="{LEMON}" stroke="{CUT}" stroke-width="1" vector-effect="non-scaling-stroke"/>' for tx in (18,WID-40))
    b+=tabs
    b+=f'<rect x="0" y="{-HC}" width="{WID}" height="{HC}" fill="{LEMON}" stroke="{CUT}" stroke-width="1.3" vector-effect="non-scaling-stroke"/>'
    b+=L(0,0,WID,0,FOLD,1,'4 2','vector-effect="non-scaling-stroke"')
    if not ink.is_empty: b+=poly_svg(ink,INKC)
    # tiny legible ID on the foot of card 1 only
    if k==0: b+=f'<text x="6" y="-5" font-size="4.6" font-weight="700" fill="{INKC}">Sophia Zhuravkova  ·  стол 3 · место 7</text>'
    b+='</g>'
    b+=T(ox+WID*s+10,y0+HC*s-HC*s/2+4,f'card {k+1}  ({"front" if k==0 else "middle" if k==1 else "rear"})',9.5,INKC,700)
    b+=T(ox+WID*s+10,y0+HC*s-HC*s/2+17,f'stands at y = {CARDS[k]["O"][1]-CARDS[0]["O"][1]:.0f} mm',9,GREY)
b+=dim(ox,oy-8,ox+WID*s,oy-8,f'{WID:.0f} mm',off=-1,size=9)
b+=T(36,oy-30,'print file: ink only on the slices (shown exactly as projected)',10,INKC,700)
# base
bx,by=560,122; bs=1.35; bw=WID+16; bd=(YK[-1]-YK[0])+44
b+=f'<g transform="translate({bx},{by}) scale({bs})">'
b+=f'<rect x="0" y="0" width="{bw}" height="{bd}" rx="4" fill="{LEMON}" stroke="{CUT}" stroke-width="1.3" vector-effect="non-scaling-stroke"/>'
for k in range(3):
    yy=22+(YK[k]-YK[0])
    for tx in (18,WID-40):
        b+=f'<rect x="{8+tx}" y="{yy:.1f}" width="22" height="0.7" fill="#fbfaf7" stroke="{CUT}" stroke-width="1.1" vector-effect="non-scaling-stroke"/>'
b+='</g>'
b+=T(bx,by-12,'base: 6 slits hold the tabs (0.4 mm card, press-fit)',10,INKC,700)
b+=T(bx,by+bd*bs+16,f'slits at 0 / {YK[1]-YK[0]:.0f} / {YK[2]-YK[0]:.0f} mm  -  the spacing IS the spell',9.5,GREY)
# section
sx,sy=640,500; k_=0.55
def P(y,z): return (sx+k_*y,sy-k_*z)
b+=T(bx,330,'side section (guest at left)',10,INKC,700)
b+=L(*P(-470,0),*P(150,0),INKC,1.4)
for c,col in zip(CARDS,('#111','#111','#111')):
    y=c['O'][1]; b+=f'<rect x="{P(y,HC)[0]-1:.1f}" y="{P(y,HC)[1]:.1f}" width="2.4" height="{k_*HC:.1f}" fill="{LEMON}" stroke="{INKC}" stroke-width="0.9"/>'
eyeP=P(-450,430)
# eye is off-canvas high: draw at clamp
ey=(sx+k_*-470, sy-k_*160)
b+=f'<circle cx="{ey[0]:.1f}" cy="{ey[1]:.1f}" r="6" fill="#fff" stroke="{INKC}" stroke-width="1.2"/><circle cx="{ey[0]+1.5:.1f}" cy="{ey[1]:.1f}" r="2.2" fill="{INKC}"/>'
b+=T(ey[0]-4,ey[1]-12,'eye (430 high, 450 away) - rays drawn schematically',8.5,INKC,500)
# rays through the tops of cards: slope from true eye
for c in CARDS:
    y=c['O'][1]; slope=(430-HC)/(y+450)           # true eye ray through top edge
    y_end=y+120; z_end=HC-slope*120
    b+=L(*P(y,HC),*P(y_end,max(z_end,0)),'#e0a800',1)
    b+=L(*P(-450+ (0),0),*P(-450,0),INKC,0)
# true rays extension to the left (up to the clipped eye): draw from top edges backwards
for c in CARDS:
    y=c['O'][1]; slope=(430-HC)/(y+450)
    ylft=-470; zl=HC+slope*(y-ylft)
    zl=min(zl,160/ (1))
    b+=L(*P(y,HC),*P(ylft,min(zl,300)),'#e0a800',0.8,'3 2')
b+=T(*P(-250,28),'plate',9,GREY,500)
b+=dim(*P(CARDS[0]['O'][1],-12),*P(CARDS[1]['O'][1],-12),f'{CARDS[1]["O"][1]-CARDS[0]["O"][1]:.0f}',off=14,size=8.5)
b+=dim(*P(CARDS[1]['O'][1],-12),*P(CARDS[2]['O'][1],-12),f'{CARDS[2]["O"][1]-CARDS[1]["O"][1]:.0f}',off=14,size=8.5)
b+=T(560,548,'Each card ends exactly where the sight line over the card in front reaches it, so',9.5,INKC,500)
b+=T(560,562,'the visible bands tile with no gap. Ink is projected from the eye onto each card:',9.5,INKC,500)
b+=T(560,576,'letter slices on card k = (text ∩ band k) projected eye → card plane.',9.5,INKC,500)
# thumbnails
tw,th=228,157; ty=598
labels=[('seat','your seat'),('head_right_60','lean 60 mm'),('neighbour_right','next seat (650 mm)'),('across_table','across the table')]
for i,(k,lab) in enumerate(labels):
    x=36+i*(tw+12)
    b+=img_tag(f'{OUT}/c2_view_{k}.png',x,ty-0,tw,th*0.76,maxw=480)
    b+=T(x+4,ty+th*0.76+11,lab,9,INKC,700)
b+=T(36,ty-6,'render of the real print file, seen from four places',9.5,INKC,700)
build(f'{OUT}/c2_sketch.svg',W_,H_,b)
