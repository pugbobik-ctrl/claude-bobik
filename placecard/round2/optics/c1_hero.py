from c1_sim import *
G=name_geometry(); eref=Eref(); dirs=camera()
nom=design(0,D0,G)
run([dict(pos=(0,D0,H),kind='filament',d=25)],'hero',nom,eref,dirs,do_view=True)
run([dict(pos=(0,D0,H),kind='point',d=8)],'hero_led',nom,eref,dirs,do_view=True)
# min bridge width after warp
from shapely.geometry import box
W=nom.W; sheet=box(nom.cx-nom.w/2,0,nom.cx+nom.w/2,CARD_H).difference(W)
n0=len(sheet.geoms) if sheet.geom_type=='MultiPolygon' else 1
for w in np.arange(0.4,4,0.1):
    e=sheet.buffer(-w/2)
    n=len(e.geoms) if e.geom_type=='MultiPolygon' else (0 if e.is_empty else 1)
    if n!=n0: print('thin card features break at width',round(w,2),'mm; components',n0,'->',n); break
print('card',nom.w,nom.h,'cx',nom.cx,'holes',W.bounds)
# narrowest hole
hw=W.buffer(-0.5)
for w in np.arange(0.4,6,0.1):
    e=W.buffer(-w/2)
    if e.is_empty or (e.geom_type=='MultiPolygon' and len(e.geoms)<len(W.geoms)): print('first hole vanishes at width',round(w,2)); break
