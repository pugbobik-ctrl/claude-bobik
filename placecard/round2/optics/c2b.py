# Concept 2 (final): "Stage Flats" - three parallel cards; each carries one horizontal slice of the name; slices line up from the seat only.
from common import *
import cv2, json
from shapely.geometry import box
EYE=np.array([0.,-450.,430.])
WID=170.; HC=62.           # card width, visible height
CAP=18.0; LEAD=31.0
C0=np.array([0.,40.,40.])   # aim point
d0=(C0-EYE); d0/=np.linalg.norm(d0)
EXU=np.array([1.,0,0]); EVU=np.cross(d0,EXU); EVU/=np.linalg.norm(EVU)
if EVU[2]<0: EVU=-EVU
def vcoord(P,eye=EYE):
    d=np.array(P)-eye; t=((C0-eye)@d0)/(d@d0); Q=eye+t*d; return float((Q-C0)@EVU)
def y_for_v(v,z=HC):
    lo,hi=-200.,600.
    for _ in range(80):
        m=(lo+hi)/2
        if vcoord((0,m,z))<v: lo=m
        else: hi=m
    return (lo+hi)/2
# text lines centred around v=0 ; line 2 (lower) mid at -LEAD/2, line 1 mid at +LEAD/2  (mid of cap height)
def text_geo():
    l1=text_poly('Sophia',CAP,700,0.04,'c'); l2=text_poly('Zhuravkova',CAP,700,0.04,'c')
    return unary_union([affinity.translate(l1,0,LEAD/2-CAP/2),affinity.translate(l2,0,-LEAD/2-CAP/2)])
TEXT=text_geo()
VB=[-LEAD/2+0.0, LEAD/2, LEAD/2+CAP*0.95]       # top-edge heights (view coords) of front, middle, rear card
YK=[y_for_v(v) for v in VB]
BANDS=[(-60.0,VB[0]),(VB[0],VB[1]),(VB[1],VB[2])]   # v-range owned by each card (front = lowest)
CARDS=[]
for k,(y,(vlo,vhi)) in enumerate(zip(YK,BANDS)):
    CARDS.append(dict(name=f'card{k+1}',O=np.array([-WID/2,y,0.]),a=np.array([1.,0,0]),b=np.array([0,0,1.]),size=(WID,HC),n=np.array([0,-1.,0]),band=(vlo,vhi)))

def project_poly(g,face,eye=EYE):
    O,a,b,n=face['O'],face['a'],face['b'],face['n']
    def mp(coords):
        c=np.array(coords); P=C0[None,:]+c[:,0:1]*EXU[None,:]+c[:,1:2]*EVU[None,:]
        d=P-eye[None,:]; t=((O-eye)@n)/(d@n); Q=eye[None,:]+t[:,None]*d
        return np.c_[(Q-O)@a,(Q-O)@b]
    return Polygon(mp(g.exterior.coords),[mp(i.coords) for i in g.interiors])
def card_ink(face,eye=EYE):
    vlo,vhi=face['band']; band=box(-400,vlo,400,vhi); rect=box(0,0,*face['size']); out=[]
    for p in TEXT.geoms:
        q=p.intersection(band)
        if q.is_empty: continue
        for qq in ([q] if q.geom_type=='Polygon' else [g for g in q.geoms if g.geom_type=='Polygon']):
            r=project_poly(qq,face,eye)
            if not r.is_valid: r=r.buffer(0)
            r=r.intersection(rect)
            if not r.is_empty: out.append(r)
    return unary_union(out) if out else Polygon()
INK=[card_ink(c) for c in CARDS]
PPM=10
def tex_of(ink,size):
    w,h=int(size[0]*PPM),int(size[1]*PPM); m=np.zeros((h,w),np.uint8)
    polys=[] if ink.is_empty else ([ink] if ink.geom_type=='Polygon' else [g for g in ink.geoms if g.geom_type=='Polygon'])
    def tp(c): return np.round(np.c_[np.array(c)[:,0]*PPM,(size[1]-np.array(c)[:,1])*PPM]*16).astype(np.int32)
    for p in polys:
        cv2.fillPoly(m,[tp(p.exterior.coords)],255,shift=4)
        for i in p.interiors: cv2.fillPoly(m,[tp(i.coords)],0,shift=4)
    return m
TEX=[tex_of(i,c['size']) for i,c in zip(INK,CARDS)]

def camera(eye,target,w,h,fov):
    eye=np.array(eye,float); f=np.array(target,float)-eye; f/=np.linalg.norm(f)
    r=np.cross(f,[0,0,1.]); r/=np.linalg.norm(r); u=np.cross(r,f)
    focal=(h/2)/np.tan(np.deg2rad(fov/2))
    i,j=np.meshgrid(np.arange(w)-w/2+.5,np.arange(h)-h/2+.5)
    dirs=f[None,None,:]+(i[...,None]*r+(-j[...,None])*u)/focal
    dirs/=np.linalg.norm(dirs,axis=2,keepdims=True); return dirs
LEM=(np.array([0xfe,0xed,0x95])/255.)**2.2; INKC=np.array([0.05,0.05,0.05])
LAMP=np.array([0.,450.,300.])
def render(eye,w=900,h=620,fov=24.0,target=(0,40,25)):
    eye=np.array(eye,float); dirs=camera(eye,target,w,h,fov)
    img=np.zeros((h,w,3)); img[:]=np.array([0.10,0.085,0.075])
    dz=dirs[...,2]; tt=np.where(dz<-1e-6,-eye[2]/np.where(dz<-1e-6,dz,-1),np.inf)
    Tx=eye[0]+tt*dirs[...,0]; Ty=eye[1]+tt*dirs[...,1]
    r=np.hypot(Tx,Ty+135)
    tab=np.full((h,w),0.16); tab=np.where(r<135,0.85,tab); tab=np.where((r<135)&(r>131),0.7,tab)
    Rl=np.sqrt(Tx**2+(Ty-450)**2+300**2); tab=tab*np.clip((300/Rl)**2*2.2,0.25,1.2)
    img=np.where(np.isfinite(tt)[...,None],tab[...,None]*np.array([1.0,0.95,0.85]),img)
    best=np.where(np.isfinite(tt),tt,np.inf)
    # base slab
    y0,y1=YK[0]-14,YK[-1]+14
    t=np.where(dz<-1e-6,-(eye[2]-0.8)/np.where(dz<-1e-6,dz,-1),np.inf)
    Q=eye[None,None,:]+t[...,None]*dirs
    hit=np.isfinite(t)&(t<best)&(np.abs(Q[...,0])<WID/2+8)&(Q[...,1]>y0)&(Q[...,1]<y1)
    img=np.where(hit[...,None],LEM[None,None,:]*0.95,img); best=np.where(hit,t,best)
    for f,tex in zip(CARDS,TEX):
        n=f['n']; dn=dirs@n; ok=np.abs(dn)>1e-6
        t=np.where(ok,((f['O']-eye)@n)/np.where(ok,dn,1),np.inf)
        Q=eye[None,None,:]+t[...,None]*dirs
        s=(Q-f['O'])@f['a']; u=(Q-f['O'])@f['b']
        hit=ok&(t>0)&(t<best)&(s>=0)&(s<=f['size'][0])&(u>=0)&(u<=f['size'][1])
        px=np.clip((s*PPM).astype(int),0,tex.shape[1]-1); py=np.clip(((f['size'][1]-u)*PPM).astype(int),0,tex.shape[0]-1)
        front=dn<0
        ink=(tex[py,px]>127)&front
        nn=np.where(front[...,None],n[None,None,:],-n[None,None,:])
        L=LAMP[None,None,:]-Q; L/=np.linalg.norm(L,axis=-1,keepdims=True)
        sh=0.55+0.45*np.clip(np.sum(L*nn,axis=-1),0,1)
        col=np.where(ink[...,None],INKC[None,None,:]*sh[...,None],LEM[None,None,:]*sh[...,None]*1.05)
        img=np.where(hit[...,None],col,img); best=np.where(hit,t,best)
    return img
def srgb(L): L=np.clip(L,0,1); return np.where(L<=0.0031308,12.92*L,1.055*L**(1/2.4)-0.055)
def save(img,path): cv2.imwrite(path,(srgb(img)[...,::-1]*255+.5).astype(np.uint8))
VIEWS={'seat':EYE,'head_right_30':EYE+[30,0,0],'head_right_60':EYE+[60,0,0],'head_up_40':EYE+[0,0,40],'head_back_60':EYE+[0,-60,0],
       'neighbour_right':np.array([650,-450,430.]),'across_table':np.array([0,1000,430.]),'standing_over_shoulder':np.array([-250,-600,950.]),'end_of_table':np.array([-1300,-450,430.])}
if __name__=='__main__':
    print('card y positions',[round(y,1) for y in YK],'band v',BANDS)
    for k,e in VIEWS.items():
        save(render(e),f'{OUT}/c2_view_{k}.png'); print(k,flush=True)
    for c,i in zip(CARDS,INK): print(c['name'],'ink mm2',round(i.area,1))
