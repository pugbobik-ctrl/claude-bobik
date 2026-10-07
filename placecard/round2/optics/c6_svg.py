from sk import *
from c6 import *
INKC='#111'
W_,H_=1000,760
b=title(6,'Slip','A lemon sleeve with a name hidden in fine lines. Slide the screen a hair: the name flashes light on black, then black on lemon.')
b+=legend(30,742)
GEO2=GEO
lp=geom_path(GEO2,flipy=True)
s=1.0
defs=f'<defs><pattern id="bgp" patternUnits="userSpaceOnUse" width="{P}" height="10" x="{-RW/2}"><rect x="0" y="0" width="{P*DUTY}" height="10" fill="{INKC}"/></pattern>'
defs+=f'<pattern id="ltp" patternUnits="userSpaceOnUse" width="{P}" height="10" x="{-RW/2+P*DUTY}"><rect x="0" y="0" width="{P*DUTY}" height="10" fill="{INKC}"/></pattern>'
defs+=f'<pattern id="ovp" patternUnits="userSpaceOnUse" width="{P}" height="10" x="{-RW/2+P*DUTY}"><rect x="0" y="0" width="{P*DUTY}" height="10" fill="{INKC}"/></pattern>'
defs+=f'<clipPath id="lc"><path d="{lp}" clip-rule="evenodd"/></clipPath></defs>'
b+=defs
# layer 1 base print
def layer(cx,cy,sc,kind):
    o=f'<g transform="translate({cx},{cy}) scale({sc})">'
    if kind=='base':
        o+=f'<rect x="{-RW/2-10}" y="{-RH/2-8}" width="{RW+20}" height="{RH+16}" rx="3" fill="{LEMON}" stroke="{CUT}" stroke-width="1.2" vector-effect="non-scaling-stroke"/>'
        o+=f'<rect x="{-RW/2}" y="{-RH/2}" width="{RW}" height="{RH}" fill="url(#bgp)"/>'
        o+=f'<rect x="{-RW/2}" y="{-RH/2}" width="{RW}" height="{RH}" fill="{LEMON}" clip-path="url(#lc)"/>'
        o+=f'<rect x="{-RW/2}" y="{-RH/2}" width="{RW}" height="{RH}" fill="url(#ltp)" clip-path="url(#lc)"/>'
    if kind=='screen':
        o+=f'<rect x="{-RW/2-4}" y="{-RH/2-4}" width="{RW+8}" height="{RH+8}" fill="#f4f1e6" fill-opacity=".55" stroke="{CUT}" stroke-width="1.2" vector-effect="non-scaling-stroke" stroke-dasharray="3 2"/>'
        o+=f'<rect x="{-RW/2-4}" y="{-RH/2-4}" width="{RW+8}" height="{RH+8}" fill="url(#ovp)"/>'
        o+=f'<rect x="{RW/2+4}" y="-6" width="26" height="12" rx="2" fill="{LEMON}" stroke="{CUT}" stroke-width="1.2" vector-effect="non-scaling-stroke"/>'
    o+='</g>'; return o
b+=T(30,98,'three parts (exploded)',10,INKC,700)
b+=layer(165,170,1.0,'base')
b+=T(165,236,'1  base: name drawn as lines shifted half a pitch',9,INKC,700,'middle')
b+=T(165,249,f'lines {P*DUTY:.1f} mm on a {P:.1f} mm pitch, printed black on lemon',9,GREY,500,'middle')
b+=layer(560,170,1.0,'screen')
b+=T(540,236,'2  screen: clear PET film, same lines (opaque bars)',9,INKC,700,'middle')
b+=T(540,249,'matt black 0.6 mm bars, 1.2 mm pitch; pull-tab at the right',9,GREY,500,'middle')
# sleeve
sx,sy=840,170
b+=f'<rect x="{sx-62}" y="{sy-50}" width="124" height="100" rx="3" fill="{LEMON}" stroke="{CUT}" stroke-width="1.2"/>'
b+=f'<rect x="{sx-45}" y="{sy-23}" width="90" height="46" fill="#fbfaf7" stroke="{CUT}" stroke-width="1.2"/>'
b+=T(sx,sy-34,'Sophia Zhuravkova',9,INKC,700,'middle')
b+=T(sx,sy+40,'стол 3 · место 7',8,INKC,500,'middle')
b+=T(sx,236,'3  sleeve (scale 0.6): window + two rails',9,INKC,700,'middle')
b+=T(sx,249,'glued over 1+2; screen slides 0.3 mm clear',9,GREY,500,'middle')
# sim frames
b+=T(30,290,'computed: the real line pattern composited at three slide positions (eye blur 0.12 mm)',10,INKC,700)
labs=[('c6_s0','slide 0:  name = lemon on black'),('c6_sp_4','slide 0.3 mm:  name gone'),('c6_sp_2','slide 0.6 mm:  name = black on lemon')]
for i,(n,l) in enumerate(labs):
    x=30+i*322
    b+=img_tag(f'{OUT}/{n}.png',x,300,310,124,maxw=900)
    b+=T(x,438,l,9,INKC,700)
b+=img_tag(f'{OUT}/c6_physics.png',30,452,640,205,maxw=1400)
mx=690
b+=T(mx,470,'numbers from the simulation',10,INKC,700)
r=json.load(open(f'{OUT}/c6_results.json'))
ls=[f'name contrast at slide 0: {r["0"]["michelson"]:+.2f} (Michelson); at 0.6 mm: {r["p/2"]["michelson"]:+.2f}',
    'printed black on lemon alone: about 0.89, so the reveal keeps ~90 %',
    'between the two the name is nulled (0.00): the shimmer is the toy',
    'dot gain 0.12 mm (cheap press) still keeps 0.76',
    'screen skew: 0.4 deg keeps 0.73; 0.8 deg drops to 0.2-0.3; 1 deg kills it',
    'pitch 1.2 mm: each letter stroke (3.3 mm) is only ~3 lines wide;',
    'letters read at 17 mm cap; much smaller and strokes alias.',
    'Physics: two gratings of equal pitch; transmitted light is a',
    'product, and shifting by half a pitch swaps which phase passes.']
for i,l in enumerate(ls): b+=T(mx,488+i*15,l,9,INKC if i<2 else GREY,500)
build(f'{OUT}/c6_sketch.svg',W_,H_,b)
