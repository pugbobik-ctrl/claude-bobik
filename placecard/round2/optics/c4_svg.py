from sk import *
from c4 import *
import json
INKC='#111'
S0=summarize(parts(0)); S2=summarize(parts(2))
a=S2['a']
W_,H_=1000,812
b=title(4,'Lemon Cradle','A half-cylinder card shaped like a lemon wedge. Flick it: the name rocks toward you like a little see-saw.')
b+=legend(30,794)
EYE=np.array([0.,-450.,430.]); TGT=np.array([0.,0.,45.])
f=TGT-EYE; f/=np.linalg.norm(f); r=np.cross(f,[0,0,1.]); r/=np.linalg.norm(r); u=np.cross(r,f)
F=640.
def proj(P):
    d=np.array(P)-EYE; z=d@f; return (F*(d@r)/z, -F*(d@u)/z), z
TXT=unary_union([affinity.translate(text_poly('Sophia',13,700,0.03,'c'),0,10.5),affinity.translate(text_poly('Zhuravkova',13,700,0.03,'c'),0,-9.5)])
def body_to_world(uu,vv,ww,th,y0=0.):
    yO=y0-R*th
    y=yO+vv*np.cos(th)-ww*np.sin(th); z=R+vv*np.sin(th)+ww*np.cos(th)
    return np.array([uu,y,z])
def frame(cx,cy,th_deg,label):
    th=np.radians(th_deg); g=''
    # shell strips
    N=28; segs=[]
    for i in range(N):
        a0=-np.pi/2+np.pi*i/N; a1=-np.pi/2+np.pi*(i+1)/N
        pts=[(-Ldeck/2,a0),(Ldeck/2,a0),(Ldeck/2,a1),(-Ldeck/2,a1)]
        W=[body_to_world(uu,R*np.sin(aa+0)*0+R*np.cos(aa+np.pi/2*0)*0+ (-R*np.sin(aa)) , R*np.cos(aa)*-1 ,th) for uu,aa in pts]
        # profile: angle aa from -90..90 measured at O: v = R*sin(aa) , w = -R*cos(aa)
        W=[body_to_world(uu,R*np.sin(aa),-R*np.cos(aa),th) for uu,aa in pts]
        cen=np.mean(W,axis=0)
        n=body_to_world(0,np.sin((a0+a1)/2),-np.cos((a0+a1)/2),th)-body_to_world(0,0,0,th)
        segs.append((np.linalg.norm(cen-EYE),W,n,cen))
    segs.sort(key=lambda s:-s[0])
    for dist,W,n,cen in segs:
        if n@(EYE-cen)<0: continue
        sh=0.55+0.45*max(0,n@np.array([0.2,0.5,0.84])/np.linalg.norm([0.2,0.5,0.84]))
        col=tuple(int(c*sh) for c in (254,237,149))
        pp=[proj(p)[0] for p in W]
        g+=f'<polygon points="{" ".join(f"{cx+x:.1f},{cy+y:.1f}" for x,y in pp)}" fill="rgb{col}" stroke="rgb{col}" stroke-width="0.6"/>'
    # deck
    corners=[(-Ldeck/2,-R),(Ldeck/2,-R),(Ldeck/2,R),(-Ldeck/2,R)]
    W=[body_to_world(uu,vv,0,th) for uu,vv in corners]
    pp=[proj(p)[0] for p in W]
    g+=f'<polygon points="{" ".join(f"{cx+x:.1f},{cy+y:.1f}" for x,y in pp)}" fill="{LEMON}" stroke="#c9b45a" stroke-width="0.8"/>'
    # text
    d=''
    for p in TXT.geoms:
        for ring in [p.exterior]+list(p.interiors):
            q=[proj(body_to_world(x,y,0,th))[0] for x,y in ring.coords]
            d+='M'+' L'.join(f'{cx+x:.2f},{cy+y:.2f}' for x,y in q)+' Z '
    g+=f'<path d="{d}" fill="{INKC}" fill-rule="evenodd"/>'
    g+=T(cx,cy+88,label,9.5,INKC,700,'middle')
    return g
for i,(cx,th,lab) in enumerate(((175,-18,'rolled away from you'),(500,0,'at rest'),(825,18,'rolled toward you'))):
    b+=f'<rect x="{cx-150}" y="108" width="300" height="190" fill="#efece4" rx="6"/>'
    b+=frame(cx,196,th,lab)
b+=T(30,100,'what the guest sees from the seat (perspective render of the real print: eye 430 up, 450 away)',10,INKC,700)
# end-on diagram
ex,ey=150,438; k=1.75
def P(y,z): return (ex+k*y,ey-k*z)
def endview(cx,th_deg,label,tint=False):
    th=np.radians(th_deg); g=''; P=lambda y,z:(cx+k*y,ey-k*z)
    yO=-R*th
    pts=[]
    for aa in np.linspace(-np.pi/2,np.pi/2,60):
        v,w=R*np.sin(aa),-R*np.cos(aa)
        y=yO+v*np.cos(th)-w*np.sin(th); z=R+v*np.sin(th)+w*np.cos(th); pts.append(P(y,z))
    g+=f'<polygon points="{" ".join(f"{x:.1f},{y:.1f}" for x,y in pts)}" fill="{LEMON}" stroke="{INKC}" stroke-width="1.4"/>'
    # radial lemon segments (printed on the caps)
    for aa in np.linspace(-np.pi/2+np.pi/6,np.pi/2-np.pi/6,5):
        v,w=R*np.sin(aa)*0.86,-R*np.cos(aa)*0.86
        y=yO+v*np.cos(th)-w*np.sin(th); z=R+v*np.sin(th)+w*np.cos(th)
        y0=yO; z0=R
        g+=L(*P(y0,z0),*P(y,z),INKC,0.6)
    g+=L(*P(-R*1.5,0),*P(R*1.5,0),INKC,1.2)
    O=P(yO,R); g+=f'<circle cx="{O[0]:.1f}" cy="{O[1]:.1f}" r="3.2" fill="#fff" stroke="#1f5fd1" stroke-width="1.4"/>'
    cm=P(yO+(-a)*np.sin(th)*(-1)*0 + a*np.sin(th)*(-1)*0 + (-(-a*np.sin(th))) if False else yO+ (a*np.sin(th))*(-1)*(-1)*0 - 0, 0)
    # CoM body (v=0,w=-a)
    y=yO+0*np.cos(th)-(-a)*np.sin(th); z=R+0*np.sin(th)+(-a)*np.cos(th); cm=P(y,z)
    g+=f'<circle cx="{cm[0]:.1f}" cy="{cm[1]:.1f}" r="4.5" fill="#fff" stroke="#d4281c" stroke-width="1.6"/><path d="M{cm[0]-4.5:.1f},{cm[1]:.1f} h9 M{cm[0]:.1f},{cm[1]-4.5:.1f} v9" stroke="#d4281c" stroke-width="1.1"/>'
    cp=P(yO,0); g+=f'<polygon points="{cp[0]-4:.1f},{cp[1]+7:.1f} {cp[0]+4:.1f},{cp[1]+7:.1f} {cp[0]:.1f},{cp[1]:.1f}" fill="{INKC}"/>'
    # gravity line from CoM to table and contact
    g+=L(cm[0],cm[1],cm[0],ey,'#d4281c',0.8,'3 3')
    g+=T(cx,ey+34,label,9,INKC,700,'middle')
    return g
b+=T(30,328,'end view: where the weight is, and what holds it up',10,INKC,700)
b+=endview(115,0,'at rest: CoM below the centre')
b+=endview(305,18,'tilted 18 deg: CoM has risen')
O0=P(0,R)
b+=T(30,500,'blue ring: O, centre of curvature (on the deck)  |  red cross: CoM, '+f'{a:.1f} mm below O  |  black tip: contact, 45 mm below O',8.5,INKC,500,'start')
b+=img_tag(f'{OUT}/c4_physics.png',420,336,560,150,maxw=1500)
b+=T(420,328,'computed: restoring well, ring-down, period vs CoM depth',9.5,INKC,700)
b+=T(30,526,f'paper only: {S0["M"]:.1f} g, CoM {S0["a"]:.1f} mm under O, period {S0["T"]:.2f} s.   with 2 two-rouble coins taped under the deck: {S2["M"]:.1f} g, {S2["a"]:.1f} mm, {S2["T"]:.2f} s.',9.5,INKC,700)
b+=T(30,541,'Rolling-without-slipping rocker: restoring torque M g a sin(tilt); stable for any a > 0, so it cannot be built wrong, only too lively (a large) or too sleepy (a small).',9,GREY,500)
# dieline
s=0.95; ox,oy=40,580
b+=T(ox,oy-8,'cut + score',10,INKC,700)
b+=f'<g transform="translate({ox},{oy}) scale({s})">'
DW=2*R; SHL=np.pi*R; TAB=10
b+=f'<rect x="0" y="0" width="{DW+SHL+TAB:.1f}" height="{Ldeck}" fill="{LEMON}" stroke="{CUT}" stroke-width="1.2" vector-effect="non-scaling-stroke"/>'
b+=L(DW,0,DW,Ldeck,FOLD,1,'4 2','vector-effect="non-scaling-stroke"')+L(DW+SHL,0,DW+SHL,Ldeck,FOLD,1,'4 2','vector-effect="non-scaling-stroke"')
for i in range(1,12): b+=L(DW+SHL*i/12,0,DW+SHL*i/12,Ldeck,FOLD,0.5,'1 2','vector-effect="non-scaling-stroke"')
# name on deck: reading along strip's long axis (rotate): deck is DW wide (v) x Ldeck (u): text runs along the 150 mm side => rotate
tp=''
for p in TXT.geoms:
    for ring in [p.exterior]+list(p.interiors):
        tp+='M'+' L'.join(f'{(R-y):.2f},{(Ldeck/2-x):.2f}' for x,y in ring.coords)+' Z '
# text up = +v (toward fold at x=DW?) : map (tx,ty)->(X=R-ty? ) keep text readable when deck rotated 90 deg
b+=f'<path d="{tp}" fill="{INKC}" fill-rule="evenodd" transform="rotate(0)"/>'
b+=f'<text x="{DW+SHL/2}" y="{Ldeck/2}" font-size="7" fill="{GREY}" text-anchor="middle" font-weight="500">curved shell: score every 14 mm, roll over the caps</text>'
b+=f'<text x="{DW+SHL+TAB/2}" y="{Ldeck/2}" font-size="5" fill="{GREY}" transform="rotate(90 {DW+SHL+TAB/2} {Ldeck/2})" text-anchor="middle">glue tab</text>'
b+='</g>'
b+=T(ox+10,oy+Ldeck*s+14,'deck (name; text runs along the 150 mm side)  |  shell  |  tab',9,GREY,500)
# caps
cx0=ox+(DW+SHL+TAB)*s+60
b+=f'<g transform="translate({cx0},{oy+10}) scale(1.3)">'
for j,(dx) in enumerate((0,R*2+16)):
    pts=[(dx+R+R*np.cos(t),R*np.sin(t)) for t in np.linspace(0,np.pi,50)]
    b+=f'<polygon points="{" ".join(f"{x:.1f},{y:.1f}" for x,y in pts)}" fill="{LEMON}" stroke="{CUT}" stroke-width="1.2" vector-effect="non-scaling-stroke"/>'
    b+=L(dx,0,dx+2*R,0,FOLD,1,'4 2','vector-effect="non-scaling-stroke"')
    for aa in np.linspace(np.pi/6,5*np.pi/6,5):
        b+=L(dx+R,0,dx+R+R*0.86*np.cos(aa),R*0.86*np.sin(aa),INKC,0.5,None,'vector-effect="non-scaling-stroke"')
b+='</g>'
b+=T(cx0,oy+10+R*1.3+26,'2 end caps, glue 2 layers (600 gsm); wedge segments printed black',9,GREY,500)
b+=T(cx0,oy+10+R*1.3+40,'coins: 2 x 2-rouble taped to the deck underside, 25 mm in from each end',9,GREY,500)
build(f'{OUT}/c4_sketch.svg',W_,H_,b)
