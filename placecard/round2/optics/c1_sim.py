from c1_geom import *
from scipy.stats import qmc
import cv2, json, time

PPM=8
GX=(-330,330); GY=(-330,300); RES=0.8
PLATE_C=(0.,-135.); PLATE_R=135.
AMB=0.10
CARD_H=84.

class Card:
    """a pierced standing card in the plane y=0 (world), centred at world x=cx"""
    def __init__(self,W,margin=14.):
        b=W.bounds; self.cx=(b[0]+b[2])/2; self.w=(b[2]-b[0])+2*margin
        self.h=CARD_H; self.W=W; self.rot=0.0
        h=int(self.h*PPM); w=int(self.w*PPM)
        m=np.zeros((h,w),np.uint8)
        def tp(c): return np.round(np.c_[(c[:,0]-self.cx+self.w/2)*PPM,(self.h-c[:,1])*PPM]*16).astype(np.int32)
        for p in W.geoms:
            cv2.fillPoly(m,[tp(np.array(p.exterior.coords))],255,lineType=cv2.LINE_8,shift=4)
            for i in p.interiors: cv2.fillPoly(m,[tp(np.array(i.coords))],0,lineType=cv2.LINE_8,shift=4)
        self.mask=m

def sample_bulb(lamp,n=160,seed=0):
    kind=lamp.get('kind','globe'); d=lamp.get('d',30.0); c=np.array(lamp['pos'],float)
    q=qmc.Halton(3,seed=seed).random(n)
    if kind=='globe':
        r=(d/2)*q[:,0]**(1/3); th=np.arccos(1-2*q[:,1]); ph=2*np.pi*q[:,2]
        pts=c+np.c_[r*np.sin(th)*np.cos(ph),r*np.sin(th)*np.sin(ph),r*np.cos(th)]
    elif kind=='filament':
        pts=c+np.c_[(q[:,0]-.5)*3,(q[:,1]-.5)*3,(q[:,2]-.5)*d]
    else:
        pts=c+np.c_[(q[:,0]-.5)*d,(q[:,1]-.5)*d,(q[:,2]-.5)*d]
    return pts

def irradiance(lamps,card):
    xs=np.arange(GX[0],GX[1]+RES,RES); ys=np.arange(GY[0],GY[1]+RES,RES)
    X,Y=np.meshgrid(xs,ys); E=np.zeros_like(X); mask=card.mask
    for lamp in lamps:
        pts=sample_bulb(lamp); acc=np.zeros_like(X)
        for B in pts:
            dx=B[0]-X; dy=B[1]-Y; dz=B[2]
            r2=dx*dx+dy*dy+dz*dz; contrib=dz/(r2*np.sqrt(r2))
            cross=(Y<0)&(B[1]>0)
            s=np.where(cross,(0-Y)/np.where(cross,dy,1),0)
            cx=X+s*dx-card.cx; cz=s*dz
            inside=cross&(np.abs(cx)<card.w/2)&(cz>0)&(cz<card.h)
            px=np.clip(((cx+card.w/2)*PPM).astype(int),0,mask.shape[1]-1)
            py=np.clip(((card.h-cz)*PPM).astype(int),0,mask.shape[0]-1)
            hole=mask[py,px]>127
            acc+=contrib*~(inside&~hole)
        E+=acc/len(pts)*lamp.get('power',1.0)
    return xs,ys,E

def Eref():
    B=np.array([0,D0,H]); P=np.array([PLATE_C[0],PLATE_C[1],0])
    r=np.linalg.norm(B-P); return H/r**3

def to_srgb(L):
    L=np.clip(L,0,1); return np.where(L<=0.0031308,12.92*L,1.055*L**(1/2.4)-0.055)

def surface_albedo(xs,ys):
    X,Y=np.meshgrid(xs,ys); r=np.hypot(X-PLATE_C[0],Y-PLATE_C[1])
    alb=np.full(X.shape,0.07); alb=np.where(r<PLATE_R,0.82,alb)
    alb=np.where((r<PLATE_R)&(r>PLATE_R-4),0.70,alb)
    alb=np.where((r<PLATE_R-48)&(r>PLATE_R-50),0.74,alb)
    return alb

def table_image(xs,ys,E,eref): return surface_albedo(xs,ys)*(E/eref+AMB)*0.95

def camera(w=1100,h=720,fov=36.0,target=(0,-95,0)):
    f=np.array(target,float)-EYE; f/=np.linalg.norm(f)
    r=np.cross(f,[0,0,1.]); r/=np.linalg.norm(r); u=np.cross(r,f)
    focal=(h/2)/np.tan(np.deg2rad(fov/2))
    i,j=np.meshgrid(np.arange(w)-w/2+.5,np.arange(h)-h/2+.5)
    dirs=f[None,None,:]+(i[...,None]*r+(-j[...,None])*u)/focal
    dirs/=np.linalg.norm(dirs,axis=2,keepdims=True); return dirs

def render_view(xs,ys,Lt,card,dirs,card_col=(0.50,0.44,0.20)):
    h,w,_=dirs.shape; dz=dirs[...,2]; dy=dirs[...,1]; dx=dirs[...,0]
    img=np.zeros((h,w,3)); img[:]=np.array([0.012,0.010,0.009])
    tt=np.where(dz<-1e-6,-EYE[2]/np.where(dz<-1e-6,dz,-1),np.inf)
    Tx=EYE[0]+tt*dx; Ty=EYE[1]+tt*dy
    ok=np.isfinite(tt)&(Tx>xs[0])&(Tx<xs[-1])&(Ty>ys[0])&(Ty<ys[-1])
    mx=np.where(ok,(Tx-xs[0])/RES,0).astype(np.float32); my=np.where(ok,(Ty-ys[0])/RES,0).astype(np.float32)
    samp=cv2.remap(Lt.astype(np.float32),mx,my,cv2.INTER_LINEAR)
    col=np.repeat(samp[...,None],3,2)*np.array([1.0,0.93,0.80])
    img=np.where(ok[...,None],col,img)
    tc=np.where(np.abs(dy)>1e-9,(0-EYE[1])/np.where(np.abs(dy)>1e-9,dy,1),np.inf)
    cx=EYE[0]+tc*dx-card.cx; cz=EYE[2]+tc*dz
    hit=(tc>0)&(tc<tt)&(np.abs(cx)<card.w/2)&(cz>0)&(cz<card.h)
    px=np.clip(((cx+card.w/2)*PPM).astype(int),0,card.mask.shape[1]-1)
    py=np.clip(((card.h-cz)*PPM).astype(int),0,card.mask.shape[0]-1)
    hole=card.mask[py,px]>127
    img=np.where((hit&~hole)[...,None],np.array(card_col)[None,None,:],img)
    return img

RW,RH,SPAN=700,330,(260,120)
def rectified(xs,ys,Lt):
    u=np.linspace(-SPAN[0]/2,SPAN[0]/2,RW); v=np.linspace(SPAN[1]/2,-SPAN[1]/2,RH)
    U,V=np.meshgrid(u,v); P=T0[None,None,:]+U[...,None]*ex+V[...,None]*ev
    t=EYE[2]/(EYE[2]-P[...,2]); T=EYE+t[...,None]*(P-EYE)
    mx=((T[...,0]-xs[0])/RES).astype(np.float32); my=((T[...,1]-ys[0])/RES).astype(np.float32)
    return cv2.remap(Lt.astype(np.float32),mx,my,cv2.INTER_LINEAR)

def ideal_text():
    G=text_poly('Sophia',CAP,700,0.08,'c'); G2=text_poly('Zhuravkova',CAP,700,0.08,'c'); lead=CAP*1.62
    G=unary_union([affinity.translate(G,0,lead/2),affinity.translate(G2,0,-lead/2)]).buffer(EMB)
    m=np.zeros((RH,RW),np.uint8)
    def tp(c): return np.round(np.c_[(c[:,0]+SPAN[0]/2)/SPAN[0]*RW,(SPAN[1]/2-c[:,1])/SPAN[1]*RH]*16).astype(np.int32)
    for p in G.geoms:
        cv2.fillPoly(m,[tp(np.array(p.exterior.coords))],255,shift=4)
        for i in p.interiors: cv2.fillPoly(m,[tp(np.array(i.coords))],0,shift=4)
    return m
IDEAL=ideal_text()
KB=cv2.GaussianBlur(IDEAL.astype(np.float32)/255.,(0,0),3.0)

def ncc(a,b):
    a=(a-a.mean())/(a.std()+1e-9); b=(b-b.mean())/(b.std()+1e-9); return float((a*b).mean())

def legibility(rect):
    """r_fixed: correlation with the ideal text where it should be.  r_best: best correlation after allowing the viewer's
    brain a stretch/shear/shift (what a human tolerates)."""
    r_fixed=ncc(rect,KB)
    best=-1
    rect32=rect.astype(np.float32)
    cx,cy=RW/2,RH/2
    for sy in (0.7,0.85,1.0,1.2,1.45):
        for sx in (0.85,1.0,1.15):
            for sh in (-0.45,-0.3,-0.15,0,0.15,0.3,0.45):
                M=np.array([[sx,sh,0],[0,sy,0]],np.float32); M[:,2]=[cx-(M[0,0]*cx+M[0,1]*cy),cy-(M[1,0]*cx+M[1,1]*cy)]
                t=cv2.warpAffine(KB,M,(RW,RH))
                # template = central crop of warped ideal; search over translation
                tpl=t[40:RH-40,70:RW-70]
                res=cv2.matchTemplate(rect32,tpl,cv2.TM_CCOEFF_NORMED)
                best=max(best,float(res.max()))
    return r_fixed,best

def save(img,path):
    im=to_srgb(np.clip(img,0,1)); cv2.imwrite(path,(im[...,::-1]*255+.5).astype(np.uint8))

def run(lamps,tag,card,eref,dirs=None,do_view=False,metric=True):
    t0=time.time()
    xs,ys,E=irradiance(lamps,card); Lt=table_image(xs,ys,E,eref); rect=rectified(xs,ys,Lt)
    sc=legibility(rect) if metric else (0,0)
    if do_view: save(render_view(xs,ys,Lt,card,dirs),f'{OUT}/c1_view_{tag}.png')
    save(np.repeat(rect[...,None],3,2)*np.array([1.0,0.93,0.80]),f'{OUT}/c1_rect_{tag}.png')
    print(f'{tag}: r_fixed={sc[0]:.3f} r_best={sc[1]:.3f} ({time.time()-t0:.1f}s)',flush=True)
    return xs,ys,Lt,rect,sc

def design(lx=0.,Dl=D0,G=None,open_mm=0.8):
    from shapely.geometry import box
    G=G or name_geometry(); W=warp_geom(G,Dl,lx)
    b=W.bounds; R=box(b[0]-30,-5,b[2]+30,CARD_H+5)
    sheet=R.difference(W).buffer(-open_mm/2).buffer(open_mm/2)   # remove laser-hostile slivers
    Wc=R.difference(sheet)
    Wc=MultiPolygon([p for p in (Wc.geoms if hasattr(Wc,'geoms') else [Wc]) if p.area>0.5 and p.bounds[0]>b[0]-25 and p.bounds[2]<b[2]+25 and p.bounds[1]>-1 and p.bounds[3]<CARD_H])
    return Card(Wc)
