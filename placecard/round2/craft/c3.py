import math
from lib import *

PW, PH = 52.0, 80.0          # closed booklet page w x h
HOLES = [12.0, 40.0, 68.0]   # along the spine from the top
ROLL_D = 42.0
THREAD_D = 0.6
def tcalc():
    o = []
    o.append("C3 ONE THREAD geometry / length check (mm)")
    o.append(f"sheet {2*PW:.0f} x {PH:.0f} folded once -> booklet {PW:.0f} x {PH:.0f}, 4 pages; spine along the {PH:.0f} edge")
    o.append(f"holes on the fold at {HOLES}: spacing {HOLES[1]-HOLES[0]:.0f} / {HOLES[2]-HOLES[1]:.0f}; end margins {HOLES[0]:.0f} / {PH-HOLES[2]:.0f}")
    seg_in = (HOLES[1] - HOLES[0]) + (HOLES[2] - HOLES[1])
    seg_out = HOLES[2] - HOLES[0]
    o.append(f"thread path in the book: inside H2-H1 {HOLES[1]-HOLES[0]:.0f}, outside long stitch H1-H3 {seg_out:.0f}, inside H3-H2 {HOLES[2]-HOLES[1]:.0f} = {seg_in+seg_out:.0f} mm + ~3 x 2 mm for passes")
    o.append(f"H2 is passed twice: 2 x {THREAD_D} thread = {2*THREAD_D:.1f} -> pierce H2 at 1.3 mm, H1/H3 at 0.9 mm")
    belt = math.pi * (ROLL_D + 2 * 2.2)   # roll + booklet thickness + thread
    o.append(f"belt round roll {ROLL_D:.0f} dia + booklet 2.2: pi x {ROLL_D+4.4:.1f} = {belt:.0f} mm")
    bow = 2 * 45 + 2 * 22
    total = seg_in + seg_out + 6 + belt + bow
    o.append(f"bow 2 loops x 45 + 2 tails x 22 = {bow}; total = {total:.0f} mm -> cut {int(math.ceil(total*1.2/50)*50)} mm (20 % spare for the knot, two-turn option adds {belt:.0f})")
    o.append(f"name 'Zhuravkova' at 7.6 mm SemiBold = {tw('Zhuravkova',7.6,600):.1f} mm on a {PW:.0f} mm page -> {(PW-tw('Zhuravkova',7.6,600))/2:.1f} mm each side; cap-height {capheight(600)*7.6:.1f}")
    o.append(f"'Dinner' at 11 mm Bold = {tw('Dinner',11,700):.1f} mm")
    o.append(f"SRA3 320x450 : sheets {2*PW:.0f}x{PH:.0f} -> {int(320//(2*PW))} x {int(450//PH)} = {int(320//(2*PW))*int(450//PH)} per sheet (rotated: {int(450//(2*PW))*int(320//PH)})")
    open("c3_verify.txt", "w").write("\n".join(o) + "\n")
    print("\n".join(o))

def dieline():
    W, H = 330, 250
    d = Doc(0, 0, W, H, scale=5.0)
    d.title(10, 13, "03  ONE THREAD — a 4-page book sewn with the thread that becomes the napkin ring",
            "Dieline 1:1 (mm). One 104 x 80 sheet of 300 g lemon board, scored once, three pierced holes on the fold. Black waxed linen thread 0.6 mm, 500 mm.")
    def panel(ox, oy, label, left, right, side):
        d.rect(ox, oy, 2 * PW, PH, "cut", LEMON)
        d.line(ox + PW, oy, ox + PW, oy + PH, "val" if side == "inside" else "mtn")
        for y in HOLES:
            d.circle(ox + PW, oy + y, 0.9 if y != HOLES[1] else 1.3, "cut", "#ffffff")
        d.note(ox, oy - 3, label, 2.8, INK, weight=600)
        left(ox, oy); right(ox + PW, oy)
    def p4(x, y):  # back cover (outside left)
        d.note(x + PW / 2, y + PH - 6, "back cover: blank lemon", 2.4, GREY, "middle")
    def p1(x, y):  # front cover
        d.text(x + PW / 2, y + 26, "Dinner", 11, 700, INK, "middle")
        d.text(x + PW / 2, y + 33, "10.10.2026", 3.4, 500, INK, "middle")
        d.text(x + PW / 2, y + PH - 6, "Colorblock × DNA Kitchen", 2.6, 500, INK, "middle")
    def p2(x, y):
        d.text(x + PW / 2, y + 34, "Colorblock", 3.8, 600, INK, "middle")
        d.text(x + PW / 2, y + 39, "× DNA Kitchen", 3.8, 600, INK, "middle")
        d.text(x + PW / 2, y + 46, "Moscow", 3.0, 500, INK, "middle")
        d.text(x + PW / 2, y + 50, "10 October 2026", 3.0, 500, INK, "middle")
    def p3(x, y):
        d.text(x + PW / 2, y + 36, "Sophia", 7.6, 600, INK, "middle")
        d.text(x + PW / 2, y + 36 + 8.6, "Zhuravkova", 7.6, 600, INK, "middle")
    panel(14, 28, "OUTSIDE (print plate 1)  fold = mountain", p4, p1, "outside")
    panel(14 + 2 * PW + 18, 28, "INSIDE (print plate 2)  fold = valley", p2, p3, "inside")
    # dims
    d.line(14, 28 + PH + 5, 14 + 2 * PW, 28 + PH + 5, "dim"); d.note(14 + PW, 28 + PH + 9, "104", 2.6, INK, "middle")
    d.line(10, 28, 10, 28 + PH, "dim")
    d.add(f'<text transform="translate(7 {28+PH/2}) rotate(-90)" font-size="2.6" text-anchor="middle" fill="{INK}">80</text>')
    for i, y in enumerate(HOLES):
        d.note(14 + PW - 2.5, 28 + y + 0.8, f"H{i+1}  y = {y:.0f}, hole " + ("1.3" if i == 1 else "0.9"), 2.3, GREY, "end")
    # thread path diagram (spine view, spine vertical)
    gx, gy = 30, 135
    d.text(gx - 16, gy - 8, "Thread path along the spine", 3.0, 600, INK)
    sx = gx + 20
    d.line(sx, gy, sx, gy + PH, "mtn")
    for i, y in enumerate(HOLES):
        d.circle(sx, gy + y, 1.2, "thin", "#fff"); d.note(sx + 2.4, gy + y + 0.9, f"H{i+1}", 2.4, INK)
    # outside side to the left (x-8), inside to the right (x+8) ; show as profile: left = outside
    ox_, ix_ = sx - 10, sx + 10
    seq = [(ox_, gy + HOLES[1] - 8, "tail A (outside)"), ]
    # steps
    def seg(x1, y1, x2, y2, cls="ink", dash=""):
        d.add(f'<line x1="{f2(x1)}" y1="{f2(y1)}" x2="{f2(x2)}" y2="{f2(y2)}" stroke="{INK}" stroke-width=".55" {dash} stroke-linecap="round"/>')
    # 1 tail A from outside into H2
    seg(ox_ - 8, gy + HOLES[1] - 6, sx, gy + HOLES[1]); 
    # inside run H2->H1
    seg(sx, gy + HOLES[1], ix_, gy + HOLES[1] - 2, dash='stroke-dasharray="1.4 .9"')
    seg(ix_, gy + HOLES[1] - 2, ix_, gy + HOLES[0] + 2, dash='stroke-dasharray="1.4 .9"')
    seg(ix_, gy + HOLES[0] + 2, sx, gy + HOLES[0], dash='stroke-dasharray="1.4 .9"')
    # outside long stitch H1->H3
    seg(sx, gy + HOLES[0], ox_, gy + HOLES[0] + 2); seg(ox_, gy + HOLES[0] + 2, ox_, gy + HOLES[2] - 2); seg(ox_, gy + HOLES[2] - 2, sx, gy + HOLES[2])
    # inside run H3->H2
    seg(sx, gy + HOLES[2], ix_ + 3, gy + HOLES[2] - 2, dash='stroke-dasharray="1.4 .9"')
    seg(ix_ + 3, gy + HOLES[2] - 2, ix_ + 3, gy + HOLES[1] + 2, dash='stroke-dasharray="1.4 .9"')
    seg(ix_ + 3, gy + HOLES[1] + 2, sx, gy + HOLES[1], dash='stroke-dasharray="1.4 .9"')
    # tail B out of H2
    seg(sx, gy + HOLES[1], ox_ - 8, gy + HOLES[1] + 6)
    d.note(ox_ - 12, gy + HOLES[1] - 7, "tail A", 2.4, INK, "end")
    d.note(ox_ - 12, gy + HOLES[1] + 9, "tail B", 2.4, INK, "end")
    d.note(ox_ - 1.5, gy + 40 - 0.5, "long stitch", 2.4, INK, "end", extra='')
    d.note(sx, gy + PH + 6, "left: OUTSIDE of the spine   |   right: INSIDE (dashed)", 2.4, GREY, "middle")
    d.notes(100, 145, [
        "SEWING (2 min)",
        "1  Tail A: outside -> in at H2.   2  Inside run up to H1, out.",
        "3  Outside, long stitch H1 -> H3 (passing H2), in at H3.",
        "4  Inside run up to H2, out: tail B. Both tails now leave H2 on the outside,",
        "    one each side of the long stitch.   5  Tie a half knot over the long stitch,",
        "    leave tails ~ 200 mm each. No knot inside the book.",
        "TABLE (guest, 20 s)",
        "6  Lay the book on the napkin roll, spine left; tails around the roll (and the book),",
        "    bow on the cover. The belt is the napkin ring; the book is its tag.",
    ], 2.7, 1.5, INK)
    d.legend(200, 220, [("cut", "outline / pierced holes"), ("mtn", "mountain crease (scored 0.4)"), ("val", "valley crease (inside)")])
    d.save("c3_dieline.svg")

def bow_path(d, x, y, sc=1.0, w=1.2):
    d.path(f"M{x},{y} C{x-14*sc},{y-11*sc} {x-17*sc},{y+4*sc} {x},{y} C{x+14*sc},{y-11*sc} {x+17*sc},{y+4*sc} {x},{y}", "ink", extra=f'stroke-width="{w}"')
    d.path(f"M{x},{y} C{x-5*sc},{y+8*sc} {x-9*sc},{y+14*sc} {x-14*sc},{y+22*sc}", "ink", extra=f'stroke-width="{w}"')
    d.path(f"M{x},{y} C{x+5*sc},{y+8*sc} {x+9*sc},{y+13*sc} {x+15*sc},{y+19*sc}", "ink", extra=f'stroke-width="{w}"')

def assembled():
    W, H = 330, 215
    d = Doc(0, 0, W, H, scale=5.0)
    d.title(10, 13, "03  ONE THREAD — assembled", "Left: book tied onto the napkin roll (top view, roll axis points away from the guest). Right: the bow undone, book open to the name.")
    # roll
    rx, ry, rw, rh = 58, 30, ROLL_D, 140
    d.defs.append('<linearGradient id="rollg" x1="0" x2="1"><stop offset="0" stop-color="#cfc8b8"/><stop offset=".3" stop-color="#f7f4ec"/><stop offset=".7" stop-color="#ece7da"/><stop offset="1" stop-color="#bdb6a4"/></linearGradient>')
    d.add(f'<rect x="{rx}" y="{ry}" width="{rw}" height="{rh}" rx="6" fill="url(#rollg)" stroke="#9a9484" stroke-width=".3"/>')
    for i in range(1, 12):
        d.add(f'<line x1="{rx+1}" y1="{ry+i*rh/12}" x2="{rx+rw-1}" y2="{ry+i*rh/12}" stroke="#d6d0c0" stroke-width=".15"/>')
    d.add(f'<ellipse cx="{rx+rw/2}" cy="{ry+4}" rx="{rw/2-1}" ry="3" fill="#e4dfd0" stroke="#9a9484" stroke-width=".25"/>')
    d.note(rx + rw / 2, ry + rh + 7, "linen napkin rolled, 42 mm dia", 2.6, GREY, "middle")
    # booklet closed on top, spine left edge at x = rx + (rw-PW)/2 
    bx = rx + (rw - PW) / 2 - 0; by = ry + 30
    d.add(f'<rect x="{bx+1.2}" y="{by+1.4}" width="{PW}" height="{PH}" fill="#000" opacity=".15"/>')
    d.rect(bx, by, PW, PH, "edge", LEMON)
    for i in range(1, 4):
        d.add(f'<line x1="{bx+PW-0.35*i}" y1="{by+1}" x2="{bx+PW-0.35*i}" y2="{by+PH-1}" stroke="#b79c2a" stroke-width=".15"/>')
    d.add(f'<text x="{bx+PW/2+1}" y="{by+26}" font-size="11" font-weight="700" text-anchor="middle" fill="{INK}">Dinner</text>')
    d.add(f'<text x="{bx+PW/2+1}" y="{by+33}" font-size="3.4" font-weight="500" text-anchor="middle" fill="{INK}">10.10.2026</text>')
    # long stitch on spine (outside)
    d.add(f'<line x1="{bx+1.0}" y1="{by+HOLES[0]}" x2="{bx+1.0}" y2="{by+HOLES[2]}" stroke="{INK}" stroke-width=".7"/>')
    # belt around book + roll at y = by+HOLES[1]
    yb = by + HOLES[1]
    d.add(f'<line x1="{bx+1.0}" y1="{yb}" x2="{rx+rw+0.6}" y2="{yb}" stroke="{INK}" stroke-width="1.0"/>')
    d.add(f'<line x1="{rx-0.6}" y1="{yb}" x2="{bx+1.0}" y2="{yb}" stroke="{INK}" stroke-width="1.0"/>')
    bow_path(d, bx + 9, yb, 1.5, 1.1)
    d.note(bx + PW / 2, by + PH + 8, "closed: 52 x 80 x 2.2 mm", 2.6, INK, "middle")
    d.note(bx - 2, by + 14, "spine, long stitch", 2.3, GREY, "end")
    # open view on the right
    ox, oy = 168, 52
    d.add(f'<rect x="{ox+1.4}" y="{oy+1.6}" width="{2*PW}" height="{PH}" fill="#000" opacity=".15"/>')
    d.rect(ox, oy, 2 * PW, PH, "edge", LEMON)
    d.line(ox + PW, oy, ox + PW, oy + PH, "edgeL")
    d.text(ox + PW / 2, oy + 34, "Colorblock", 3.8, 600, INK, "middle")
    d.text(ox + PW / 2, oy + 39, "× DNA Kitchen", 3.8, 600, INK, "middle")
    d.text(ox + PW / 2, oy + 46, "Moscow", 3.0, 500, INK, "middle")
    d.text(ox + PW / 2, oy + 50, "10 October 2026", 3.0, 500, INK, "middle")
    d.text(ox + PW + PW / 2, oy + 36, "Sophia", 7.6, 600, INK, "middle")
    d.text(ox + PW + PW / 2, oy + 36 + 8.6, "Zhuravkova", 7.6, 600, INK, "middle")
    # inside stitches visible on the gutter (thread inside H2-H1, H3-H2)
    for y1, y2 in ((HOLES[0], HOLES[1]), (HOLES[1], HOLES[2])):
        d.add(f'<line x1="{ox+PW-0.5}" y1="{oy+y1}" x2="{ox+PW-0.5}" y2="{oy+y2}" stroke="{INK}" stroke-width=".6"/>')
    for y in HOLES:
        d.circle(ox + PW - 0.5, oy + y, 0.8, "ink")
    # loose thread: the tails hang over the left edge, curl
    d.add(f'<path d="M{ox+PW-0.5},{oy+HOLES[1]} C{ox+PW-40},{oy+HOLES[1]-34} {ox-30},{oy+8} {ox-26},{oy+40} S{ox-48},{oy+66} {ox-34},{oy+92}" fill="none" stroke="{INK}" stroke-width=".9"/>')
    d.add(f'<path d="M{ox+PW-0.5},{oy+HOLES[1]} C{ox+PW-36},{oy+HOLES[1]+30} {ox-20},{oy+PH+4} {ox+10},{oy+PH+16} S{ox+60},{oy+PH+22} {ox+90},{oy+PH+12}" fill="none" stroke="{INK}" stroke-width=".9"/>')
    d.note(ox + PW, oy - 6, "open: 104 x 80", 2.6, INK, "middle")
    d.note(ox + PW, oy + PH + 32, "the two tails are the napkin ring (cut 500 mm total)", 2.6, GREY, "middle")
    d.save("c3_assembled.svg")

if __name__ == "__main__":
    tcalc(); dieline(); assembled()
