from c1_sim import *
from PIL import Image, ImageDraw, ImageFont
G=name_geometry(); eref=Eref(); dirs=camera()
F=ImageFont.truetype(FONTDIR+'WixMadeforText-500.ttf',15); FB=ImageFont.truetype(FONTDIR+'WixMadeforText-700.ttf',17)
nom=design(0,D0,G); c300=design(-300,D0,G); c600=design(-600,D0,G)
fil=lambda x=0,y=D0,z=H,d=25: dict(pos=(x,y,z),kind='filament',d=d)
scen=[
 ('LED capsule 8 mm',nom,[dict(pos=(0,D0,H),kind='point',d=8)]),
 ('clear filament 25 mm',nom,[fil()]),
 ('opal globe 45 mm',nom,[dict(pos=(0,D0,H),kind='globe',d=45)]),
 ('opal globe 80 mm',nom,[dict(pos=(0,D0,H),kind='globe',d=80)]),
 ('card cut for lamp 300 mm to the left',c300,[fil(-300)]),
 ('card cut for lamp 600 mm to the left',c600,[fil(-600)]),
 ('lamp placed 60 mm off its mark (sideways)',nom,[fil(60)]),
 ('lamp placed 120 mm off its mark (sideways)',nom,[fil(120)]),
 ('lamp 100 mm nearer than marked',nom,[fil(0,D0-100)]),
 ('lamp 200 mm farther than marked',nom,[fil(0,D0+200)]),
 ('lamp 30 mm lower than assumed',nom,[fil(0,D0,H-30)]),
 ('+ neighbour lamp 900 mm along table',nom,[fil(),fil(900)]),
]
tiles=[]; res={}
for name,card,lamps in scen:
    xs,ys,Lt,rect,sc=run(lamps,'m%d'%len(tiles),card,eref,dirs)
    res[name]=dict(r_fixed=sc[0],r_best=sc[1])
    im=np.repeat(rect[...,None],3,2)*np.array([1.0,0.93,0.80]); im=to_srgb(np.clip(im,0,1))
    pil=Image.fromarray((im*255).astype(np.uint8)).resize((520,245))
    tile=Image.new('RGB',(520,245+54),(250,250,248)); tile.paste(pil,(0,54))
    d=ImageDraw.Draw(tile); d.text((8,6),name,font=FB,fill=(20,20,20)); d.text((8,30),f'legibility: as-placed r={sc[0]:.2f} | allowing stretch/shear r={sc[1]:.2f}',font=F,fill=(90,90,90))
    tiles.append(tile)
cols=3; rows=(len(tiles)+cols-1)//cols
sheet=Image.new('RGB',(530*cols+10,309*rows+10),(250,250,248))
for i,t in enumerate(tiles): sheet.paste(t,(10+(i%cols)*530,10+(i//cols)*309))
sheet.save(f'{OUT}/c1_matrix.png'); json.dump(res,open(f'{OUT}/c1_scores.json','w'),indent=1)
