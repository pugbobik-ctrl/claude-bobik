from sk import *
from c5 import *
INKC='#111'
W_,H_=1000,700
b=title(5,'Spin Plate','Roll the skewer between your palms: an empty place setting and your name blur into one picture, your name on the plate.')
b+=legend(30,682)
def disc(cx,cy,g,label,sub,flipv=False):
    s=1.75
    o=f'<g transform="translate({cx},{cy}) scale({s})">'
    o+=f'<circle r="{RR}" fill="{LEMON}" stroke="{CUT}" stroke-width="1.2" vector-effect="non-scaling-stroke"/>'
    gg=affinity.scale(g,1,-1,origin=(0,0)) if flipv else g
    o+=f'<path d="{geom_path(gg,flipy=True)}" fill="{INKC}" fill-rule="evenodd"/>'
    o+=f'<line x1="{-RR}" y1="0" x2="{RR}" y2="0" stroke="{FOLD}" stroke-width="1" stroke-dasharray="4 2" vector-effect="non-scaling-stroke"/></g>'
    o+=T(cx,cy+RR*s+18,label,10.5,INKC,700,'middle')+T(cx,cy+RR*s+32,sub,9,GREY,500,'middle')
    return o
b+=disc(150,200,FG,'side A: the empty place setting','what you see at rest, facing you')
b+=disc(445,200,BG,'side B: printed upside-down','(flip about the skewer line = upright)',flipv=True)
b+=T(30,98,'cut + print (two discs, Ø110, 300 gsm; dashed line = skewer axis)',10,INKC,700)
# fused ideal + spin sim
b+=T(560,98,'what the eye gets when it spins (computed)',10,INKC,700)
b+=img_tag(f'{OUT}/c5_fused_ideal.png',560,108,190,190,maxw=520)
b+=T(655,312,'ideal: 50/50 persistence',9,INKC,700,'middle')
im=Image.open(f'{OUT}/c5_spin_seat.png').crop((150,60,750,560)); im.save(f'{OUT}/c5_spin_seat_crop.png')
b+=img_tag(f'{OUT}/c5_spin_seat_crop.png',770,108,190,190*500/600,maxw=520)
b+=T(865,312,'3D simulation from the seat',9,INKC,700,'middle')
b+=T(865,324,'(180 phases / turn, disc flips edge-on)',8.5,GREY,500,'middle')
# assembly section
b+=T(30,420,'assembly',10,INKC,700)
ax,ay=60,500
b+=f'<line x1="{ax}" y1="{ay}" x2="{ax+300}" y2="{ay}" stroke="#a67c3d" stroke-width="3.5" stroke-linecap="round"/>'
for dy,lab in ((-5,'A'),(5,'B')):
    pass
b+=f'<rect x="{ax+110}" y="{ay-70}" width="3.2" height="140" fill="{LEMON}" stroke="{INKC}" stroke-width="0.8"/><rect x="{ax+113.2}" y="{ay-70}" width="3.2" height="140" fill="{LEMON}" stroke="{INKC}" stroke-width="0.8"/>'
b+=T(ax+130,ay-62,'disc A + disc B back to back,',9,INKC,500)
b+=T(ax+130,ay-49,'skewer sandwiched on the diameter',9,INKC,500)
b+=T(ax+130,ay-36,'(2 x 0.4 mm card, 3 mm skewer, PVA)',9,GREY,500)
b+=T(ax+305,ay+4,'roll me',9,'#8a6a00',700)
# base cradle
b+=f'<polygon points="{ax+40},{ay+100} {ax+80},{ay+100} {ax+80},{ay+78} {ax+68},{ay+78} {ax+60},{ay+90} {ax+52},{ay+78} {ax+40},{ay+78}" fill="{LEMON}" stroke="{CUT}" stroke-width="1.2"/>'
b+=f'<polygon points="{ax+250},{ay+100} {ax+290},{ay+100} {ax+290},{ay+78} {ax+278},{ay+78} {ax+270},{ay+90} {ax+262},{ay+78} {ax+250},{ay+78}" fill="{LEMON}" stroke="{CUT}" stroke-width="1.2"/>'
b+=T(ax,ay+120,'two lemon V-cradles hold the skewer ends on the table (name printed small on them)',9,GREY,500)
# physics text
yy=420
b+=T(470,yy,'the physics',10,INKC,700)
lines=['Skewer 3 mm, palms sliding past each other at 10 cm/s: omega = 0.2 m/s / 3 mm = 67 rad/s = about 10 turns/s.',
'Each turn shows A then B: 20 swaps/s, above the ~16 Hz fusion limit of a lamp-lit dinner room (eye integrates ~1/20 s).',
'Persistence = average of the two images, so ink on one side only reads 50 %; ink on both reads 100 %.',
'Measured in the sim: name strokes at ~17 % luminance contrast (printed black on lemon is ~89 %). It reads, but it is a ghost.',
'Disc rotates about the line of the text, so text rows stay near the axis and stay sharp; ring and cutlery smear vertically.',
'Back side is printed upside-down so it flips upright (thaumatrope rule). Name Ø110: cap 7.2 mm, 0.9 deg at 450 mm.']
for i,l in enumerate(lines): b+=T(470,yy+18+i*15,l,9,INKC if i in (0,3) else GREY,500)
build(f'{OUT}/c5_sketch.svg',W_,H_,b)
