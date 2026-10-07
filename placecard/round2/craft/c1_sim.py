import math, itertools
from lib import *

S = 200.0
R = S / math.sqrt(2)      # half diagonal
DIAMOND = [(0, R), (-R, 0), (0, -R), (R, 0)]   # T, L, B, R  (y up)

def affine_reflect(T, p, d):
    """compose: new point = reflect(T(q)). T as function list; we track T by images of 3 points"""
    return [reflect_pt(q, p, d) for q in T]

class Layer:
    def __init__(s, name, poly, T, z, flips):
        s.name, s.poly, s.T, s.z, s.flips = name, poly, T, z, flips

def fold(layers, p, d, flap_left, which=None, tag=""):
    """fold: parts of selected layers lying on flap side get reflected about line (p,d). Return new list."""
    out = []
    flaps = []
    for L in layers:
        if which is not None and L.name not in which:
            out.append(L); continue
        flap = clip_halfplane(L.poly, p, d, keep_left=flap_left)
        stay = clip_halfplane(L.poly, p, d, keep_left=not flap_left)
        if len(stay) >= 3 and abs(area(stay)) > 1e-6:
            out.append(Layer(L.name, stay, L.T, L.z, L.flips))
        if len(flap) >= 3 and abs(area(flap)) > 1e-6:
            fp = [reflect_pt(q, p, d) for q in flap]
            fT = [reflect_pt(q, p, d) for q in L.T]
            flaps.append(Layer(L.name + tag, fp, fT, L.z, L.flips + 1))
    # flaps go on top, order inverted
    top = max([l.z for l in out] + [0])
    flaps.sort(key=lambda l: -l.z)
    for i, f in enumerate(flaps):
        f.z = top + 1 + i
        out.append(f)
    return out

# transform tracking: T = images of 3 reference points (0,0),(1,0),(0,1) in sheet coords
REF = [(0, 0), (1, 0), (0, 1)]
def apply_T(T, q):
    o, ex, ey = T
    return (o[0] + q[0] * (ex[0] - o[0]) + q[1] * (ey[0] - o[0]),
            o[1] + q[0] * (ex[1] - o[1]) + q[1] * (ey[1] - o[1]))
def svg_matrix(T, ymul=-1):
    """matrix string mapping sheet coords (y up) -> final view coords (y up), then y flip for svg"""
    o, ex, ey = T
    a, b = ex[0] - o[0], ex[1] - o[1]
    c, d = ey[0] - o[0], ey[1] - o[1]
    # svg y = -y
    return f"matrix({f2(a)} {f2(-b)} {f2(-c)} {f2(d)} {f2(o[0])} {f2(-o[1])})"

def build(P):
    base = Layer("base", [(0, R), (-R, 0), (0, -R), (R, 0)], list(REF), 0, 0)
    L = [base]
    # F1 bottom corner up
    L = fold(L, (0, P["c1"]), (1, 0), flap_left=False, tag="/F1")   # flap = below the line
    # F2 right lapel: line from Pr (on TR edge) to M ; flap = right side
    Pr = (P["xs"], R - P["xs"]); Qr = (P["qx"], P["c1"])
    d = (Qr[0] - Pr[0], Qr[1] - Pr[1])
    L = fold(L, Pr, d, flap_left=True, tag="/F2")
    Pl = (-P["xs"], R - P["xs"]); Ql = (-P["qx"], P["c1"])
    d2 = (Ql[0] - Pl[0], Ql[1] - Pl[1])
    L = fold(L, Pl, d2, flap_left=False, tag="/F3")
    return L, (Pr, Pl, Qr, Ql)

def finish_apex(L, c4):
    """fold apex of base layer down along y=c4 (only layer 'base')."""
    return fold(L, (0, c4), (1, 0), flap_left=True, which=["base"], tag="/F4")

if __name__ == "__main__":
    import sys
    P = dict(pack=(132, 82), c1=-41, xs=float(sys.argv[1]), qx=float(sys.argv[2]), c4=45)
    L, _ = build(P)
    for l in L:
        xs = [q[0] for q in l.poly]; ys = [q[1] for q in l.poly]
        print(l.name, l.z, l.flips, "x[%.0f,%.0f] y[%.0f,%.0f]" % (min(xs), max(xs), min(ys), max(ys)))
