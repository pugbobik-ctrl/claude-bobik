# Concept 5: Spin Plate - a thaumatrope disc on a skewer. Front: an empty place setting. Back: the name. Spin it: name served on the plate.
from common import *
import cv2, json
from shapely.geometry import Point, box, LineString
DIA=110.; RR=DIA/2
RING_R=33.0
def fork(x0,cy,L=64.):
    # handle + neck + head with 4 tines (centred at x0, vertical extent L)
    hw=2.6; top=cy+L/2; bot=cy-L/2
    handle=box(x0-hw,bot,x0+hw,cy+4)
    head=box(x0-6.2,cy+4,x0+6.2,top-12)
    tines=[box(x0-6.2+i*(12.4-2.4)/3,top-12,x0-6.2+i*(12.4-2.4)/3+2.4,top) for i in range(4)]
    neck=Polygon([(x0-hw,cy+4),(x0+hw,cy+4),(x0+6.2,cy+8),(x0-6.2,cy+8)])
    g=unary_union([handle,head,neck]+tines)
    return g
def knife(x0,cy,L=64.):
    hw=2.6; top=cy+L/2; bot=cy-L/2
    handle=box(x0-hw,bot,x0+hw,cy+2)
    blade=Polygon([(x0-hw,cy+2),(x0+hw+4.2,cy+2),(x0+hw+4.2,top-8),(x0+hw+2,top-1),(x0-hw,top)]).buffer(0.6)
    return unary_union([handle,blade])
def front_geom():
    ring=Point(0,0).buffer(RING_R).difference(Point(0,0).buffer(RING_R-3.6))
    inner=Point(0,0).buffer(RING_R-6.5).difference(Point(0,0).buffer(RING_R-7.5))
    f=fork(-44,0); k=knife(44,0)
    return unary_union([ring,inner,f,k])
def back_geom():
    c=RING_R-7
    l1=text_poly('Sophia',7.2,700,0.0,'c'); l2=text_poly('Zhuravkova',7.2,700,0.0,'c')
    nm=unary_union([affinity.translate(l1,0,5.6),affinity.translate(l2,0,-6.4)]).buffer(0.3)
    seat=text_poly('№ 7',4.0,700,0.05,'c'); seat=affinity.translate(seat,0,-19.5)
    return unary_union([nm,seat])
PPM=8
def raster(g,size=DIA+4):
    n=int(size*PPM); m=np.zeros((n,n),np.uint8)
    def tp(c): return np.round(np.c_[(np.array(c)[:,0]+size/2)*PPM,(size/2-np.array(c)[:,1])*PPM]*16).astype(np.int32)
    for p in ([g] if g.geom_type=='Polygon' else g.geoms):
        cv2.fillPoly(m,[tp(p.exterior.coords)],255,shift=4)
        for i in p.interiors: cv2.fillPoly(m,[tp(i.coords)],0,shift=4)
    return m
FG=front_geom(); BG=back_geom()
FR=raster(FG); BR=raster(BG)
SIZE=DIA+4
def sample(tex,u,v):
    n=tex.shape[0]; px=np.clip(((u+SIZE/2)*PPM).astype(int),0,n-1); py=np.clip(((SIZE/2-v)*PPM).astype(int),0,n-1)
    return tex[py,px]>127
EYE=np.array([0.,-450.,430.]); CEN=np.array([0.,0.,95.])
def cam(w,h,fov,target):
    f=target-EYE; f/=np.linalg.norm(f); r=np.cross(f,[0,0,1.]); r/=np.linalg.norm(r); u=np.cross(r,f)
    focal=(h/2)/np.tan(np.deg2rad(fov/2)); i,j=np.meshgrid(np.arange(w)-w/2+.5,np.arange(h)-h/2+.5)
    d=f[None,None,:]+(i[...,None]*r+(-j[...,None])*u)/focal; d/=np.linalg.norm(d,axis=2,keepdims=True); return d
LEM=np.array([0xfe,0xed,0x95])/255.
def frame(phi,dirs,eye=EYE,cen=CEN,edge_fade=True):
    """returns (coverage, ink) arrays: coverage=1 where disc is hit; ink=1 where black"""
    n=np.array([0,-np.cos(phi),np.sin(phi)]); e1=np.array([1.,0,0]); e2=np.cross(n,e1)
    dn=dirs@n; ok=np.abs(dn)>1e-6
    t=np.where(ok,((cen-eye)@n)/np.where(ok,dn,1),np.inf)
    Q=eye[None,None,:]+t[...,None]*dirs; u=(Q-cen)@e1; v=(Q-cen)@e2
    hit=ok&(t>0)&(u*u+v*v<RR*RR)
    facing_front=(n@(eye-cen))>0
    if facing_front: ink=sample(FR,u,v)
    else: ink=sample(BR,u,-v)          # back image is stored upright; seen from behind with up = -e2
    return hit,ink&hit
def spin_average(dirs,N=120,table=None):
    cov=np.zeros(dirs.shape[:2]); ink=np.zeros(dirs.shape[:2])
    for k in range(N):
        h,i=frame(2*np.pi*(k+.5)/N,dirs); cov+=h; ink+=i
    return cov/N,ink/N
def compose(cov,ink,bg=(0.16,0.15,0.14)):
    # persistence: mix of ground colour / lemon disc / ink
    lem=cov-ink; col=ink[...,None]*np.array([0.05,0.05,0.05])+lem[...,None]*LEM**2.2+(1-cov)[...,None]*np.array(bg)
    return col
def srgb(L): L=np.clip(L,0,1); return np.where(L<=0.0031308,12.92*L,1.055*L**(1/2.4)-0.055)
def save(img,path): cv2.imwrite(path,(srgb(img)[...,::-1]*255+.5).astype(np.uint8))
if __name__=='__main__':
    dirs=cam(900,620,13.0,CEN)
    # static frames
    for name,phi in (('rest_front',0.0),('rest_back_from_behind',np.pi)):
        pass
    h,i=frame(0.0,dirs); save(compose(h.astype(float),i.astype(float)),f'{OUT}/c5_static_front.png')
    cov,ink=spin_average(dirs,N=180); save(compose(cov,ink),f'{OUT}/c5_spin_seat.png')
    # ideal fusion (disc held face-on, weights 50/50) in disc space
    sz=int(DIA*6); u=np.linspace(-RR,RR,sz); U,V=np.meshgrid(u,u[::-1])
    a=sample(FR,U,V); b=sample(BR,U,V)    # back image upright as printed
    disc=(U**2+V**2<RR**2)
    ink=0.5*a+0.5*b; img=np.zeros((sz,sz,3)); img[:]=(0.16,0.15,0.14)
    lem=np.where(disc,1-ink,0)
    col=ink[...,None]*disc[...,None]*0.05+(np.where(disc,1-ink,0))[...,None]*LEM**2.2
    img=np.where(disc[...,None],col,img); save(img,f'{OUT}/c5_fused_ideal.png')
    # front, back flat renderings
    for nm,A in (('front',FR),('back',BR)):
        sz2=A.shape[0]; V2=np.linspace(0,0,1)
        im=np.where((A>127)[...,None],0.05,0)+np.where((A<=127)[...,None],LEM**2.2,0)
        yy,xx=np.mgrid[:sz2,:sz2]; r=np.hypot(xx-sz2/2,yy-sz2/2)/PPM
        im=np.where((r<RR)[...,None],im,np.array([0.16,0.15,0.14])); save(im,f'{OUT}/c5_flat_{nm}.png')
    print('done')
