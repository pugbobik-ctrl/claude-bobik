# Concept 1 geometry: vertical pierced screen; shadow of its holes falls on the plate and reads from the seat.
from common import *
import cv2
from shapely.geometry import LineString, LinearRing

H=300.0         # bulb height above table
D0=450.0        # lamp horizontal distance beyond the card plane (nominal; lamp on table centreline opposite the guest)
EYE=np.array([0.,-450.,430.])
T0=np.array([0.,-100.,0.])   # centre of the intended name on the table
CAP=27.0        # visual cap height on the picture plane (mm)
EMB=0.45        # embolden (mm, text space) each side
BRIDGE=4.2      # stencil bridge width (mm text space)

# picture plane perpendicular to the sight line to T0
d=(T0-EYE); d/=np.linalg.norm(d)
ex=np.array([1.,0,0]); ev=np.cross(d,ex); ev/=np.linalg.norm(ev)
if ev[2]<0: ev=-ev

def name_geometry(emb=EMB,bridge=BRIDGE,cap=CAP):
    l1=text_poly('Sophia',cap,700,0.08,'c'); l2=text_poly('Zhuravkova',cap,700,0.08,'c')
    lead=cap*1.62
    l1=affinity.translate(l1,0,lead/2); l2=affinity.translate(l2,0,-lead/2)
    G=unary_union([l1,l2])
    G=G.buffer(emb,join_style=1,resolution=8)
    # stencil bridges for every island (counter)
    polys=[G] if isinstance(G,Polygon) else list(G.geoms)
    out=[]
    for p in polys:
        q=p
        for ring in list(p.interiors):
            isl=Polygon(ring); c=isl.centroid
            best=None
            for ang in (0,90,180,270):
                a=np.deg2rad(ang); dv=np.array([np.cos(a),np.sin(a)])
                ln=LineString([(c.x,c.y),(c.x+dv[0]*60,c.y+dv[1]*60)])
                seg=ln.intersection(Polygon(p.exterior).difference(isl))
                # first segment hitting stroke
                geoms=[seg] if seg.geom_type=='LineString' else list(getattr(seg,'geoms',[]))
                geoms=[g for g in geoms if g.geom_type=='LineString' and g.length>0]
                if not geoms: continue
                g0=min(geoms,key=lambda g: g.distance(c))
                L=g0.length
                if best is None or L<best[0]: best=(L,g0,dv)
            L,g0,dv=best
            (x0,y0),(x1,y1)=g0.coords[0],g0.coords[-1]
            ln=LineString([(x0-dv[0]*1.0,y0-dv[1]*1.0),(x1+dv[0]*1.0,y1+dv[1]*1.0)])
            q=q.difference(ln.buffer(bridge/2,cap_style=2))
        out.append(q)
    G=unary_union(out)
    return G

def map_pts(P,Dl=D0,lx=0.0):
    """text-plane (u,v) -> card plane (x,z) via eye ray -> table -> lamp ray."""
    P=np.asarray(P,float); u=P[:,0]; v=P[:,1]
    Pw=T0[None,:]+u[:,None]*ex[None,:]+v[:,None]*ev[None,:]
    t=EYE[2]/(EYE[2]-Pw[:,2])
    T=EYE[None,:]+t[:,None]*(Pw-EYE[None,:])
    Ty=T[:,1]; Tx=T[:,0]
    s=Dl/(Dl-Ty)
    x=lx+s*(Tx-lx); z=H*(1-s)
    return np.c_[x,z], T

def warp_geom(G,Dl=D0,lx=0.0):
    def wpoly(p):
        def ring(r):
            c=np.array(r.coords); w,_=map_pts(c,Dl,lx); return w
        # densify first
        p=p.segmentize(1.0)
        return Polygon(ring(p.exterior),[ring(i) for i in p.interiors])
    if isinstance(G,Polygon): return wpoly(G)
    return MultiPolygon([wpoly(p) for p in G.geoms])

def table_bounds(G):
    P=np.array([c for p in ([G] if isinstance(G,Polygon) else G.geoms) for c in p.exterior.coords])
    _,T=map_pts(P); return T[:,0].min(),T[:,0].max(),T[:,1].min(),T[:,1].max()

if __name__=='__main__':
    G=name_geometry(); print('text bounds',G.bounds, 'n polys',len(G.geoms))
    print('table bounds x0,x1,y0,y1',table_bounds(G))
    W=warp_geom(G); print('card hole bounds',W.bounds)
