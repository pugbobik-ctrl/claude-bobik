from lib import *
s = S()
s.header('09', 'BLACK TO COLOUR', 'A black bar on a paper strip dips into a shot of water. Over the evening it separates into blocks of colour. A slow clock.')
sc = 1.55
def panel(x0, frac, label, sub):
    gy = 470
    P = lambda x, z: (x0 + x * sc, gy - z * sc)
    # card 100 x 130
    s.poly([P(-50, 0), P(50, 0), P(50, 130), P(-50, 130)], LEMON, INK, 2)
    s.text(P(-14, 100), 'Sophia', 10 * sc, 700, INK, 'middle'); s.text(P(-14, 84), 'Zhuravkova', 10 * sc, 700, INK, 'middle')
    s.text(P(-14, 40), 'TABLE 4', 5.4 * sc, 600, INK, 'middle', ls=1); s.text(P(-14, 31), 'SEAT 07', 5.4 * sc, 600, INK, 'middle', ls=1)
    # window with strip
    s.poly([P(26, 14), P(42, 14), P(42, 118), P(26, 118)], '#ffffff', INK, 1.4)
    strip_top = 118
    # strip below bottom into glass: tail drops to z=-10
    s.poly([P(28, -14), P(40, -14), P(40, 14), P(28, 14)], '#ffffff', GREY, 1)
    # shot glass at front
    s.poly([P(14, -26), P(54, -26), P(52, 8), P(16, 8)], '#dbe9ef', GREY, 1.4, op=0.5)
    s.poly([P(16, -26), P(52, -26), P(51.5, -12), P(16.5, -12)], '#9ec6d8', 'none', 0, op=0.7)
    s.line(P(15, -12), P(53, -12), '#4f8fae', 1.2)
    # origin line (black bar) at z=24..30 (above waterline -12 by ~36mm?). bar at 18..24
    bar_lo, bar_hi = 20, 27
    front = 20 + frac * 98      # water front height in the window (mm)
    def seg(z0, z1, col, op=1.0):
        z0 = max(z0, 14); z1 = min(z1, 118)
        if z1 > z0: s.poly([P(26, z0), P(42, z0), P(42, z1), P(26, z1)], col, 'none', 0, op=op)
    if frac < 0.02:
        seg(bar_lo, bar_hi, '#141414')
    else:
        # wet zone tint
        seg(14, front, '#eef3f4')
        # separated bands, leading edge first
        yel = bar_hi + (front - bar_hi) * 0.92; mag = bar_hi + (front - bar_hi) * 0.62; cya = bar_hi + (front - bar_hi) * 0.36
        seg(mag, yel, '#f5c518'); seg(cya, mag, '#d63a73'); seg(bar_hi, cya, '#2f9fd4'); seg(bar_lo, bar_hi, '#2a1e3d')
        # gradients: soften with thin lines
        for zz, cc in ((yel, '#f5c518'), (mag, '#d63a73'), (cya, '#2f9fd4')):
            pass
        s.line(P(26, front), P(42, front), '#7aa6b8', 1)
    s.poly([P(26, 14), P(42, 14), P(42, 118), P(26, 118)], 'none', INK, 1.4)
    s.line((x0 - 70 * sc, gy), (x0 + 70 * sc, gy), INK, 1.4)
    s.text((x0, gy + 55), label, 13, 700, INK, 'middle')
    s.text((x0, gy + 74), sub, 12, 500, GREY, 'middle')
xs = [170, 470, 770, 1070]
for x0, (fr, a, b) in zip(xs, [(0.0, '20:00', 'seated: a black bar'), (0.3, '20:30', 'starter: yellow runs ahead'), (0.65, '21:30', 'main: pink, then blue'), (1.0, '23:00', 'dessert: the whole block')]):
    panel(x0, fr, a, b)
s.text((48, 160), 'THE CARD, FOUR TIMES, THE SAME EVENING', 12, 700, GREY, ls=1)
s.note((48, 690), ['Card 100 x 130 mm with a 16 mm window; strip of chromatography paper, 12 x 130 mm, tail 14 mm into a shot glass with 10 mm of water.', 'The bar is dye-based black (inkjet black or a water-soluble marker): its dyes travel at different speeds, so one black becomes yellow, pink, blue.', 'Climb rate is the risk: filter paper rises about 10 mm in 2 min then slows. Needs a test with the actual ink and the room temperature.', 'The shot glass is the second object on the table: a pour of water, a pour of colour.'], 13)
s.save('../svg/09_black_to_colour.svg')
