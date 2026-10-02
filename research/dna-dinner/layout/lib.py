"""Shared helpers: lettering masks from the poster, tracing to absolute SVG paths."""
import cv2, numpy as np, re, subprocess, json, os
V2 = os.path.dirname(os.path.abspath(__file__))
GEN = os.path.join(V2, 'gen'); os.makedirs(GEN, exist_ok=True)
PAD = 110

def flat_mask():
    """Flat (unrotated) DINNER alpha, 0..1 float, cropped with PAD on each side."""
    a = cv2.imread(os.path.join(V2, 'dinner_alpha_flat.png'), -1).astype(np.float32) / 255
    ys, xs = np.where(a > 0.5)
    y0, y1, x0, x1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
    return a[y0 - PAD:y1 + PAD, x0 - PAD:x1 + PAD].copy()

def poster_mask():
    return cv2.imread(os.path.join(V2, 'dinner_alpha_poster.png'), -1).astype(np.float32) / 255

def _abs_path(d, scale, Hs):
    """potrace path (0.1 units, y up, relative c/l) -> absolute path in source px."""
    toks = re.findall(r'[MmCcLlZz]|-?\d+(?:\.\d+)?', d)
    out = []; i = 0; cx = cy = 0.0; sx = sy = 0.0; cmd = None
    def P(x, y):
        return f'{x*0.1/scale:.1f} {(Hs - y*0.1)/scale:.1f}'
    while i < len(toks):
        t = toks[i]
        if re.match(r'[A-Za-z]', t):
            cmd = t; i += 1
            if cmd in 'Zz':
                out.append('Z'); cx, cy = sx, sy
            continue
        if cmd in 'Mm':
            x, y = float(toks[i]), float(toks[i+1]); i += 2
            if cmd == 'm': x += cx; y += cy
            cx, cy = x, y; sx, sy = x, y
            out.append('M' + P(x, y)); cmd = 'l' if cmd == 'm' else 'L'
        elif cmd in 'Cc':
            v = [float(toks[i+k]) for k in range(6)]; i += 6
            if cmd == 'c': v = [v[0]+cx, v[1]+cy, v[2]+cx, v[3]+cy, v[4]+cx, v[5]+cy]
            out.append('C' + P(v[0], v[1]) + ' ' + P(v[2], v[3]) + ' ' + P(v[4], v[5]))
            cx, cy = v[4], v[5]
        elif cmd in 'Ll':
            x, y = float(toks[i]), float(toks[i+1]); i += 2
            if cmd == 'l': x += cx; y += cy
            out.append('L' + P(x, y)); cx, cy = x, y
        else:
            raise ValueError(cmd)
    return ''.join(out)

def trace(alpha, name, scale=3, smooth=0.6, thr=0.5, turd=40):
    """Trace a 0..1 mask; returns an absolute path string in mask pixel coordinates."""
    big = cv2.resize(alpha.astype(np.float32), (alpha.shape[1]*scale, alpha.shape[0]*scale), interpolation=cv2.INTER_CUBIC)
    if smooth: big = cv2.GaussianBlur(big, (0, 0), scale*smooth)
    b = (big > thr).astype(np.uint8)
    pbm = os.path.join(GEN, name + '.pbm'); svg = os.path.join(GEN, name + '.svg')
    cv2.imwrite(pbm, (1 - b) * 255)
    subprocess.run(['potrace', pbm, '-s', '-o', svg, '-t', str(turd), '-a', '1.1', '-O', '0.9', '-u', '10'], check=True)
    s = open(svg).read()
    Hs = alpha.shape[0] * scale
    ds = re.findall(r'<path d="([^"]+)"', s)
    os.remove(pbm)
    return ' '.join(_abs_path(d, scale, Hs) for d in ds)

def save(name, obj):
    json.dump(obj, open(os.path.join(GEN, name + '.json'), 'w'))

def load(name):
    return json.load(open(os.path.join(GEN, name + '.json')))
