"""Check fold specs (FOLDSPEC.md) before viewing them.

    python3 check_spec.py SPEC.json [...]

Checks the schema, the panel tree, hinges lying on the shared edge, overlapping panels, the
pose vectors, back regions, and that the assembled card stays above the table (y >= -1 mm).
Exit code 1 on any ERROR; WARN lines are worth a look.
"""
import json
import math
import pathlib
import re
import sys
import xml.etree.ElementTree as ET

import numpy as np
from shapely.geometry import LineString, Polygon


def rot(axis, ang):
    a = axis / np.linalg.norm(axis)
    x, y, z = a
    c, s = math.cos(ang), math.sin(ang)
    C = 1 - c
    return np.array([[c + x * x * C, x * y * C - z * s, x * z * C + y * s],
                     [y * x * C + z * s, c + y * y * C, y * z * C - x * s],
                     [z * x * C - y * s, z * y * C + x * s, c + z * z * C]])


def pose(origin, at, u, v):
    U = np.array(u, float); U /= np.linalg.norm(U)
    V = np.array(v, float); V -= U * V.dot(U); V /= np.linalg.norm(V)
    W = np.cross(U, V)
    R = np.stack([U, V, W], 1)
    T = np.array(at, float) - R @ np.array([origin[0], origin[1], 0.0])
    return R, T


def check(path):
    errs, warns = [], []
    E, Wn = errs.append, warns.append
    p = pathlib.Path(path)
    try:
        spec = json.loads(p.read_text())
    except Exception as e:
        return [f"not JSON: {e}"], []
    svg = p.parent.parent / "final" / spec.get("svg", "")
    vb = None
    if not svg.exists():
        Wn(f"svg not found at {svg}")
    else:
        root = ET.parse(svg).getroot()
        vb = [float(x) for x in re.split(r"[ ,]+", root.get("viewBox").strip())]
    sheets = spec.get("sheets") or []
    if not sheets:
        E("no sheets")
    max_step = 0
    lowest = []
    for sh in sheets:
        sid = sh.get("id", "?")
        panels = sh.get("panels") or []
        if sh.get("stock", "board") not in ("board", "acetate"):
            E(f"{sid}: stock must be board or acetate")
        ids = {}
        for pa in panels:
            if pa["id"] in ids:
                E(f"{sid}: duplicate panel id {pa['id']}")
            ids[pa["id"]] = pa
            if len(pa.get("poly", [])) < 3:
                E(f"{sid}/{pa['id']}: poly needs >= 3 points")
        roots = [pa for pa in panels if not pa.get("parent")]
        if len(roots) != 1:
            E(f"{sid}: needs exactly one root panel (no parent), has {len(roots)}")
        polys = {}
        for pa in panels:
            try:
                pg = Polygon(pa["poly"], pa.get("holes") or [])
                if not pg.is_valid:
                    pg = pg.buffer(0)
                    Wn(f"{sid}/{pa['id']}: polygon self-intersects (repaired for the check)")
                polys[pa["id"]] = pg
            except Exception as e:
                E(f"{sid}/{pa['id']}: bad polygon {e}")
            if vb:
                xs = [q[0] for q in pa["poly"]]; ys = [q[1] for q in pa["poly"]]
                if min(xs) < vb[0] - 1 or min(ys) < vb[1] - 1 or max(xs) > vb[0] + vb[2] + 1 or max(ys) > vb[1] + vb[3] + 1:
                    E(f"{sid}/{pa['id']}: poly outside the SVG viewBox {vb}")
        names = list(polys)
        for i in range(len(names)):
            for j in range(i + 1, len(names)):
                a = polys[names[i]].intersection(polys[names[j]]).area
                if a > 1.0:
                    E(f"{sid}: panels {names[i]} and {names[j]} overlap by {a:.1f} mm2")
        for pa in panels:
            if not pa.get("parent"):
                continue
            if pa["parent"] not in ids:
                E(f"{sid}/{pa['id']}: parent {pa['parent']} not found"); continue
            h = pa.get("hinge")
            if not h or len(h) != 2:
                E(f"{sid}/{pa['id']}: hinge must be two points"); continue
            if math.dist(h[0], h[1]) < 1:
                E(f"{sid}/{pa['id']}: hinge shorter than 1 mm")
            line = LineString(h)
            for who in (pa["id"], pa["parent"]):
                if who in polys and polys[who].exterior.distance(line.interpolate(0.5, normalized=True)) > 0.6:
                    E(f"{sid}/{pa['id']}: hinge midpoint is not on the edge of {who}")
            # child must lie on one side of the hinge
            if pa["id"] in polys:
                d = np.array(h[1], float) - np.array(h[0], float)
                n = np.array([-d[1], d[0]])
                side = [np.dot(np.array(q, float) - h[0], n) for q in pa["poly"]]
                if min(side) < -0.5 * np.linalg.norm(n) and max(side) > 0.5 * np.linalg.norm(n):
                    Wn(f"{sid}/{pa['id']}: panel lies on both sides of its hinge")
            if abs(pa.get("angle", 0)) > 180:
                E(f"{sid}/{pa['id']}: angle beyond +-180")
            max_step = max(max_step, pa.get("step", 1))
        # cycles
        for pa in panels:
            seen, cur = set(), pa
            while cur.get("parent"):
                if cur["id"] in seen:
                    E(f"{sid}: parent cycle at {cur['id']}"); break
                seen.add(cur["id"]); cur = ids.get(cur["parent"], {})
        po = sh.get("pose")
        if not po:
            Wn(f"{sid}: no pose (stays flat on the table)")
            po = {"origin": [0, 0], "at": [0, 0, 0], "u": [1, 0, 0], "v": [0, 0, 1]}
        else:
            u, v = np.array(po["u"], float), np.array(po["v"], float)
            if abs(np.linalg.norm(u) - 1) > 0.02 or abs(np.linalg.norm(v) - 1) > 0.02:
                Wn(f"{sid}: pose u/v not unit length (normalised by the viewer)")
            if abs(u.dot(v)) > 0.03:
                Wn(f"{sid}: pose u and v not perpendicular (v is orthogonalised to u)")
        max_step = max(max_step, sh.get("step", 1))
        bk = sh.get("back")
        if bk:
            f, r = bk.get("front"), bk.get("region")
            if not f or not r or len(f) != 4 or len(r) != 4:
                E(f"{sid}: back needs front and region as [x, y, w, h]")
            elif abs(f[2] - r[2]) > 0.5 or abs(f[3] - r[3]) > 0.5:
                E(f"{sid}: back front and region differ in size")
        # assembled positions
        R0, T0 = pose(po["origin"], po["at"], po["u"], po["v"])
        if roots and not errs:
            def walk(pa, M):            # M: 4x4 sheet->sheet transform accumulated for this panel
                pts = np.array([[q[0], q[1], 0, 1] for q in pa["poly"]], float) @ M.T
                world = (R0 @ pts[:, :3].T).T + T0
                lowest.append((world[:, 1].min(), f"{sid}/{pa['id']}"))
                for ch in panels:
                    if ch.get("parent") != pa["id"]:
                        continue
                    h = np.array(ch["hinge"], float)
                    a = np.array([h[1][0] - h[0][0], h[1][1] - h[0][1], 0.0]); a /= np.linalg.norm(a)
                    c = np.mean(np.array(ch["poly"], float), 0)
                    d = np.array([c[0] - h[0][0], c[1] - h[0][1], 0.0]); d -= a * d.dot(a)
                    if np.cross(a, d)[2] > 0:
                        a = -a
                    Rm = rot(a, math.radians(ch.get("angle", 0)))
                    L = np.eye(4); L[:3, :3] = Rm
                    P = np.eye(4); P[:2, 3] = h[0]
                    Pi = np.eye(4); Pi[:2, 3] = -h[0]
                    walk(ch, M @ P @ L @ Pi)
            walk(roots[0], np.eye(4))
    for y, who in lowest:
        if y < -1.0:
            E(f"{who}: assembled panel goes {-y:.1f} mm below the table")
    steps = spec.get("steps") or []
    if len(steps) < max_step:
        Wn(f"{len(steps)} step captions for {max_step} steps")
    for pr in spec.get("props", []):
        if pr.get("type") not in ("plate", "box", "cylinder", "mirror"):
            E(f"prop type {pr.get('type')} unknown")
    return errs, warns


if __name__ == "__main__":
    bad = 0
    for f in sys.argv[1:]:
        e, w = check(f)
        print(f"{'FAIL' if e else 'ok  '} {f}")
        for x in e:
            print("   ERROR", x)
        for x in w:
            print("   WARN ", x)
        bad += bool(e)
    sys.exit(1 if bad else 0)
