from lib import *
s = S()
s.header('04', 'CHEERS', 'Slide the black sleeve and two glasses on the card clink, again and again. Your name sits on top.')
labs = ['sleeve at 0.0 mm', 'sleeve at 0.7 mm', 'sleeve at 1.4 mm']
for i in range(3):
    x = 48 + i * 385
    s.raw(f'<image href="{b64img(f"../calc/c04_eye{i}.png")}" x="{x}" y="150" width="365" height="203"/>')
    s.poly([(x, 150), (x+365, 150), (x+365, 353), (x, 353)], 'none', GREY_L, 1)
    s.text((x, 140), ['FRAME 1', 'FRAME 2', 'FRAME 3'][i], 12, 700, GREY, ls=1)
    s.text((x, 374), labs[i] + ['  glasses apart', '  glasses close', '  clink, sparks'][i], 12, 500)
s.text((48, 396), 'Simulated: interlaced print and slit sleeve composed column by column, then blurred as the eye would. Then it repeats every 2.1 mm of travel.', 12, 500, GREY)
# object axon
cam = Cam(az=-18, el=14, s=3.1, ox=250, oy=800)
def P(x, z, y=0): return cam.p(x, y, z)
# lemon card 100 x 80, tent foot
foot = [cam.p(-50, -12, 0), cam.p(50, -12, 0), cam.p(50, 18, 0), cam.p(-50, 18, 0)]
s.poly(foot, LEMON_D, INK, 1.4)
s.poly([P(-50, 0), P(50, 0), P(50, 80), P(-50, 80)], LEMON, INK, 1.6)
s.face_text(cam, (0, 0, 66), (1, 0, 0), (0, 0, 1), 'Sophia Zhuravkova', 8.2, 700, INK, 'middle', extra='')
# sleeve (black), window zone z 8..58 ; sleeve 84 wide shifted
sl = [P(-40, 6), P(44, 6), P(44, 58), P(-40, 58)]
s.poly([cam.p(-40, -0.8, 6), cam.p(44, -0.8, 6), cam.p(44, -0.8, 58), cam.p(-40, -0.8, 58)], '#1c1c1c', INK, 1.6)
for i in range(0, 41):
    x = -38 + i * 2.0
    s.line(cam.p(x, -1, 8), cam.p(x, -1, 56), '#5a5a40', 0.9)
# tab
s.poly([cam.p(44, -0.8, 24), cam.p(66, -0.8, 24), cam.p(66, -0.8, 40), cam.p(44, -0.8, 40)], '#1c1c1c', INK, 1.4)
s.face_text(cam, (55, -1, 28), (1, 0, 0), (0, 0, 1), 'pull', 6, 700, LEMON, 'middle')
s.line(cam.p(68, -1, 32), cam.p(86, -1, 32), INK, 1.6); s.poly([cam.p(86, -1, 32), cam.p(80, -1, 35), cam.p(80, -1, 29)], INK, INK, 1)
s.note((48, 850), ['Black sleeve 84 x 52 mm, laser-cut slits 0.7 mm. Lemon card 100 x 80 mm: interlaced print', 'under the window, name above, slotted foot.'], 13)
# slit detail
dx, dy, sc = 600, 480, 46
s.text((dx, dy - 14), 'SLIT DETAIL (mm), one pitch repeated', 12, 700, GREY, ls=1)
for r in range(4):
    x0 = dx + r * 2.1 * sc
    s.poly([(x0, dy), (x0 + 1.4*sc, dy), (x0 + 1.4*sc, dy + 70), (x0, dy + 70)], '#1c1c1c', INK, 1)
    for j, c in enumerate(['#d9d3a0', '#fdf0b0', '#ffffff']):
        pass
    s.poly([(x0 + 1.4*sc, dy), (x0 + 2.1*sc, dy), (x0 + 2.1*sc, dy + 70), (x0 + 1.4*sc, dy + 70)], LEMON, INK, 1)
s.text((dx, dy + 95), 'bar 1.4  |  slit 0.7  |  pitch 2.1', 12, 600)
for j in range(3):
    xx = dx + j * 0.7 * sc
    s.poly([(xx, dy + 118), (xx + 0.7*sc, dy + 118), (xx + 0.7*sc, dy + 148), (xx, dy + 148)], ['#e8d27a', '#bfae5c', '#7a6f30'][j], INK, 1)
    s.text((xx + 0.35*sc, dy + 138), f'F{j+1}', 12, 700, INK, 'middle')
s.text((dx, dy + 168), 'print under the slits: three 0.7 mm slices per pitch, one per frame', 12, 500)
s.note((600, 700), ['Slide 0.7 mm: next frame. A 15 mm pull plays the loop 7 times.', 'Black bars take 2/3 of the light: the picture is dark but sharp,', 'so the sleeve face is also printed with the name as a lemon label.'], 13)
s.save('../svg/04_cheers.svg')
