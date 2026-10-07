# Concept 2: stepped card, name resolves only from the seat (Varini-style anamorphosis on a folded stair)
from common import *
import cv2, json
EYE=np.array([0.,-450.,430.])
WID=160.
F_D,R1_H,T1_D,R2_H,T2_D=36.,24.,34.,24.,30.
Y1=F_D; Y2=Y1+T1_D; Y3=Y2+T2_D; Z1=R1_H; Z2=Z1+R2_H
FACES=[ # name, origin, a-axis, b-axis, (wa,wb), normal
 ('F0',(-WID/2,0,0),(1,0,0),(0,1,0),(WID,F_D),(0,0,1)),
 ('R1',(-WID/2,Y1,0),(1,0,0),(0,0,1),(WID,R1_H),(0,-1,0)),
 ('T1',(-WID/2,Y1,Z1),(1,0,0),(0,1,0),(WID,T1_D),(0,0,1)),
 ('R2',(-WID/2,Y2,Z1),(1,0,0),(0,0,1),(WID,R2_H),(0,-1,0)),
 ('T2',(-WID/2,Y2,Z2),(1,0,0),(0,1,0),(WID,T2_D),(0,0,1)),
 ('R3',(-WID/2,Y3,0),(1,0,0),(0,0,1),(WID,Z2),(0,1,0)),
]
FACES=[dict(name=n,O=np.array(o,float),a=np.array(a,float),b=np.array(b,float),size=sz,n=np.array(nn,float)) for n,o,a,b,sz,nn in FACES]
C0=np.array([0.,Y2,Z1+4])           # centre of the stair the name is aimed at
CAP=18.0
VOFF=9.0
d0=(C0-EYE); d0/=np.linalg.norm(d0)
EXU=np.array([1.,0,0]); EVU=np.cross(d0,EXU); EVU/=np.linalg.norm(EVU)
if EVU[2]<0: EVU=-EVU
def name_text(cap=CAP):
    l1=text_poly('Sophia',cap,700,0.04,'c'); l2=text_poly('Zhuravkova',cap,700,0.04,'c'); lead=cap*1.7
    return unary_union([affinity.translate(l1,0,lead/2-cap*0.5+VOFF),affinity.translate(l2,0,-lead/2-cap*0.5+VOFF)])
TEXT=name_text()

def project_poly(g,face,eye=EYE):
    """text-plane polygon -> face-local coords (s,t), exact projective map"""
    O,a,b,n=face['O'],face['a'],face['b'],face['n']
    def mp(coords):
        c=np.array(coords); P=C0[None,:]+c[:,0:1]*EXU[None,:]+c[:,1:2]*EVU[None,:]
        d=P-eye[None,:]; t=((O-eye)@n)/(d@n); Q=eye[None,:]+t[:,None]*d
        return np.c_[(Q-O)@a,(Q-O)@b]
    return Polygon(mp(g.exterior.coords),[mp(i.coords) for i in g.interiors])
def face_ink(face,eye=EYE,text=None):
    text=text or TEXT
    from shapely.geometry import box
    rect=box(0,0,*face['size']); out=[]
    for p in text.geoms:
        q=project_poly(p,face,eye)
        if not q.is_valid: q=q.buffer(0)
        q=q.intersection(rect)
        if not q.is_empty: out.append(q)
    return unary_union(out) if out else Polygon()
INK={f['name']:(face_ink(f) if f['name']!='R3' else Polygon()) for f in FACES}

PPM=10
def tex_of(ink,size):
    w,h=int(size[0]*PPM),int(size[1]*PPM); m=np.zeros((h,w),np.uint8)
    polys=[] if ink.is_empty else ([ink] if ink.geom_type=='Polygon' else [g for g in ink.geoms if g.geom_type=='Polygon'])
    def tp(c): return np.round(np.c_[np.array(c)[:,0]*PPM,(size[1]-np.array(c)[:,1])*PPM]*16).astype(np.int32)
    for p in polys:
        cv2.fillPoly(m,[tp(p.exterior.coords)],255,shift=4)
        for i in p.interiors: cv2.fillPoly(m,[tp(i.coords)],0,shift=4)
    return m
TEX={f['name']:tex_of(INK[f['name']],f['size']) for f in FACES}
# side walls (profile in y,z)
PROFILE=Polygon([(Y1,0),(Y3,0),(Y3,Z2),(Y2,Z2),(Y2,Z1),(Y1,Z1)])
def prof_mask():
    m=np.zeros((int(Z2*PPM),int(Y3*PPM)),np.uint8)
    cv2.fillPoly(m,[np.round(np.c_[np.array(PROFILE.exterior.coords)[:,0]*PPM,(Z2-np.array(PROFILE.exterior.coords)[:,1])*PPM]).astype(np.int32)],255)
    return m
PM=prof_mask()

def camera(eye,target=(0,Y2,Z1),w=900,h=620,fov=26.0):
    eye=np.array(eye,float); f=np.array(target,float)-eye; f/=np.linalg.norm(f)
    r=np.cross(f,[0,0,1.]); r/=np.linalg.norm(r); u=np.cross(r,f)
    focal=(h/2)/np.tan(np.deg2rad(fov/2))
    i,j=np.meshgrid(np.arange(w)-w/2+.5,np.arange(h)-h/2+.5)
    dirs=f[None,None,:]+(i[...,None]*r+(-j[...,None])*u)/focal
    dirs/=np.linalg.norm(dirs,axis=2,keepdims=True); return dirs

LEM=np.array([0xfe,0xed,0x95])/255.; INKC=np.array([0.07,0.07,0.07])
LAMP=np.array([0.,450.,300.])
def shade(n,P):
    l=LAMP-P; l/=np.linalg.norm(l,axis=-1,keepdims=True)
    return 0.62+0.38*np.clip(l@n,0,1) if l.ndim==1 else 0.62+0.38*np.clip(np.sum(l*n,axis=-1),0,1)

def render(eye,w=900,h=620,fov=26.0,target=(0,Y2,Z1),heightmark=False):
    eye=np.array(eye,float); dirs=camera(eye,target,w,h,fov)
    img=np.zeros((h,w,3)); img[:]=np.array([0.10,0.085,0.075])
    # table + plate
    dz=dirs[...,2]; tt=np.where(dz<-1e-6,-eye[2]/np.where(dz<-1e-6,dz,-1),np.inf)
    Tx=eye[0]+tt*dirs[...,0]; Ty=eye[1]+tt*dirs[...,1]
    r=np.hypot(Tx-0,Ty+135)
    tab=np.full((h,w),0.16); tab=np.where(r<135,0.85,tab); tab=np.where((r<135)&(r>131),0.7,tab)
    # lamp light fall-off
    Rl=np.sqrt((Tx-0)**2+(Ty-450)**2+300**2); tab=tab*np.clip((300/Rl)**2*2.2,0.25,1.2)
    img=np.where(np.isfinite(tt)[...,None],(tab[...,None]*np.array([1.0,0.95,0.85])),img)
    best=np.where(np.isfinite(tt),tt,np.inf)
    # faces
    for f in FACES:
        n=f['n']; dn=dirs@n; ok=dn<-1e-6
        t=np.where(ok,((f['O']-eye)@n)/np.where(ok,dn,1),np.inf)
        Q=eye[None,None,:]+t[...,None]*dirs
        s=(Q-f['O'])@f['a']; u=(Q-f['O'])@f['b']
        hit=ok&(t>0)&(t<best)&(s>=0)&(s<=f['size'][0])&(u>=0)&(u<=f['size'][1])
        if not hit.any(): continue
        px=np.clip((s*PPM).astype(int),0,TEX[f['name']].shape[1]-1); py=np.clip(((f['size'][1]-u)*PPM).astype(int),0,TEX[f['name']].shape[0]-1)
        ink=TEX[f['name']][py,px]>127
        sh=0.62+0.38*np.clip(np.sum(((LAMP[None,None,:]-Q)/np.linalg.norm(LAMP[None,None,:]-Q,axis=-1,keepdims=True))*n,axis=-1),0,1)
        col=np.where(ink[...,None],INKC[None,None,:]*sh[...,None],LEM[None,None,:]**2.2*sh[...,None]*1.05)
        img=np.where(hit[...,None],col,img); best=np.where(hit,t,best)
    # side walls (blank lemon)
    for sx,nx in ((-WID/2,-1),(WID/2,1)):
        n=np.array([nx,0,0.]); dn=dirs@n; ok=dn<-1e-6
        t=np.where(ok,((np.array([sx,0,0])-eye)@n)/np.where(ok,dn,1),np.inf)
        Q=eye[None,None,:]+t[...,None]*dirs
        y=Q[...,1]; z=Q[...,2]
        inb=(y>=0)&(y<Y3)&(z>=0)&(z<Z2)
        py=np.clip(((Z2-z)*PPM).astype(int),0,PM.shape[0]-1); px=np.clip((y*PPM).astype(int),0,PM.shape[1]-1)
        hit=ok&(t>0)&(t<best)&inb&(PM[py,px]>127)
        img=np.where(hit[...,None],LEM[None,None,:]**2.2*0.55,img); best=np.where(hit,t,best)
    return img

def srgb(L): L=np.clip(L,0,1); return np.where(L<=0.0031308,12.92*L,1.055*L**(1/2.4)-0.055)
def save(img,path,ss=1):
    cv2.imwrite(path,(srgb(img)[...,::-1]*255+.5).astype(np.uint8))

if __name__=='__main__':
    views={'seat':EYE,'dx60':EYE+[60,0,0],'back60':EYE+[0,-60,0],'up60':EYE+[0,0,60],
           'neighbour':np.array([650,-450,430.]),'across':np.array([0,1000,430.]),'standing':np.array([-250,-600,950.]),'seat_left_side':np.array([-1300,-450,430.])}
    for k,e in views.items():
        img=render(e); save(img,f'{OUT}/c2_view_{k}.png'); print(k,flush=True)
    # fragment stats
    for f in FACES: print(f['name'],'ink area mm2',round(INK[f['name']].area,1))
    def vc(P):
        d=np.array(P)-EYE; t=((C0-EYE)@d0)/(d@d0); Q=EYE+t*d; return round(float((Q-C0)@EVU),1)
    print('edge v:',{'F0/R1':vc((0,Y1,0)),'R1/T1':vc((0,Y1,Z1)),'T1/R2':vc((0,Y2,Z1)),'R2/T2':vc((0,Y2,Z2)),'T2end':vc((0,Y3,Z2)),'front':vc((0,0,0))}, 'text v range',TEXT.bounds[1],TEXT.bounds[3])
