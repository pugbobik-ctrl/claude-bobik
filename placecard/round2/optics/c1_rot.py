from c1_sim import *
from PIL import Image, ImageDraw, ImageFont
G=name_geometry(); W=warp_geom(G); mask=make_mask(W); eref=Eref(); dirs=camera()
F=ImageFont.truetype(FONTDIR+'WixMadeforText-500.ttf',15); FB=ImageFont.truetype(FONTDIR+'WixMadeforText-700.ttf',17)
tiles=[]
for lx,rotdeg in [(-300,0),(-300,20),(-300,34),(-600,0),(-600,25),(-600,45)]:
    ROT[0]=np.deg2rad(rotdeg)
    xs,ys,Lt,rect,score=run([dict(pos=(lx,D0,H),kind='filament',d=25)],f'r{lx}_{rotdeg}',mask,eref,dirs,do_view=True)
    im=cv2.imread(f'{OUT}/c1_view_r{lx}_{rotdeg}.png')[...,::-1]
    pil=Image.fromarray(im).resize((520,340)); tile=Image.new('RGB',(520,340+30),(250,250,248)); tile.paste(pil,(0,30))
    d=ImageDraw.Draw(tile); d.text((8,5),f'lamp {abs(lx)} mm to the left, card turned {rotdeg} deg',font=FB,fill=(20,20,20))
    tiles.append(tile)
ROT[0]=0
sheet=Image.new('RGB',(530*3+10,380*2+10),(250,250,248))
for i,t in enumerate(tiles): sheet.paste(t,(10+(i%3)*530,5+(i//3)*380))
sheet.save(f'{OUT}/c1_rot.png')
