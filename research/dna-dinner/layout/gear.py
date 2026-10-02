"""Glass ring with the DINNER dents around its edge (ref 8 gear/sun), as an SVG path in mm."""
import sys, math; sys.path.insert(0, '.')
from lib import *
F = load('flat'); top = np.array(F['top'], np.float32)
prof = top[347:955]; prof = (prof - prof.min())/(prof.max() - prof.min())
def gear(R=45.0, depth=0.17, copies=2, n=1440, phase=0.0):
    pts = []
    for i in range(n):
        t = i/n; th = 2*math.pi*t - math.pi/2
        p = prof[int(((t*copies + phase) % 1)*(len(prof)-1))]
        r = R*(1 - depth*p)
        pts.append((r*math.cos(th), r*math.sin(th)))
    return 'M' + ' L'.join(f'{x:.2f} {y:.2f}' for x, y in pts) + ' Z'
out = {'g2': gear(copies=2, depth=0.24), 'g3': gear(copies=3, depth=0.2, phase=0.0), 'g1': gear(copies=1, depth=0.28, phase=0.0)}
# the source edge strip for the diagram: top edge of I-N-N-E, in mask px
out['edge'] = 'M' + ' L'.join(f'{x} {int(top[x])-34}' for x in range(347, 956, 3))
save('gear', out); print('ok')
