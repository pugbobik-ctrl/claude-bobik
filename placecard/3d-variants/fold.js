// Fold engine: builds a card from a fold spec (see FOLDSPEC.md) and poses it for any t.
// t = 0 is the flat sheet; t = k means steps 1..k are done (fractional t = part way).
import * as THREE from 'three';
import { Reflector } from 'three/addons/objects/Reflector.js';

const LEMON = 0xfeed95;
const loader = new THREE.TextureLoader();
const texCache = new Map();

function tex(url) {
  if (!texCache.has(url)) {
    texCache.set(url, new Promise((res) => loader.load(url, (t) => {
      t.colorSpace = THREE.SRGBColorSpace;
      t.anisotropy = 8;
      res(t);
    }, undefined, () => res(null))));
  }
  return texCache.get(url);
}

function shapeFrom(poly, holes) {
  const s = new THREE.Shape(poly.map(([x, y]) => new THREE.Vector2(x, y)));
  for (const h of holes || []) s.holes.push(new THREE.Path(h.map(([x, y]) => new THREE.Vector2(x, y))));
  return s;
}

function geometry(shape, uvOf) {
  const g = new THREE.ShapeGeometry(shape, 1);
  const pos = g.attributes.position, uv = g.attributes.uv;
  for (let i = 0; i < pos.count; i++) {
    const [u, v] = uvOf(pos.getX(i), pos.getY(i));
    uv.setXY(i, u, v);
  }
  return g;
}

const ease = (s) => s * s * (3 - 2 * s);
const clamp01 = (s) => Math.max(0, Math.min(1, s));
// progress of a step k (1-based) at time t
const prog = (t, k) => ease(clamp01(t - (k - 1)));

function poseMatrix(origin, at, u, v) {
  const U = new THREE.Vector3(...u).normalize();
  let V = new THREE.Vector3(...v);
  V.sub(U.clone().multiplyScalar(V.dot(U))).normalize();      // orthonormalise
  const W = new THREE.Vector3().crossVectors(U, V);             // sheet +z (printed face is -z)
  const m = new THREE.Matrix4().makeBasis(U, V, W);
  const o = new THREE.Vector3(origin[0], origin[1], 0).applyMatrix4(m);
  m.setPosition(new THREE.Vector3(...at).sub(o));
  return m;
}

function propMaterial(kind) {
  switch (kind) {
    case 'acrylic': case 'glass': case 'pet':
      return new THREE.MeshPhysicalMaterial({ color: 0xffffff, transmission: 0.95, roughness: 0.04, thickness: kind === 'pet' ? 0.3 : 20,
        ior: kind === 'glass' ? 1.5 : 1.49, transparent: true, opacity: 1, side: THREE.DoubleSide });
    case 'napkin': return new THREE.MeshStandardMaterial({ color: 0xf3f1ea, roughness: 0.95 });
    case 'wood': return new THREE.MeshStandardMaterial({ color: 0xa47b52, roughness: 0.7 });
    case 'mirror': return new THREE.MeshStandardMaterial({ color: 0xffffff, metalness: 1, roughness: 0.03 });
    default: return new THREE.MeshStandardMaterial({ color: 0xe9e6df, roughness: 0.45 });   // plate / ceramic
  }
}

const buildable = (p) => ['plate', 'box', 'cylinder', 'mirror'].includes(p.type);

function buildProp(p) {
  let obj;
  const mat = propMaterial(p.material || (p.type === 'plate' ? 'plate' : 'acrylic'));
  if (p.type === 'plate') {
    const r = p.r || 135;   // plate: lathe profile, rim 16 mm high
    const prof = [[0, 0], [r * 0.62, 0], [r * 0.66, 8], [r, 16], [r - 2, 18], [r * 0.64, 10.5], [0, 10]].map(([x, y]) => new THREE.Vector2(x, y));
    obj = new THREE.Mesh(new THREE.LatheGeometry(prof, 96), mat);
  } else if (p.type === 'box') {
    obj = new THREE.Mesh(new THREE.BoxGeometry(...p.size), mat);
    if (p.rotY) obj.rotation.y = THREE.MathUtils.degToRad(p.rotY);
  } else if (p.type === 'cylinder') {
    obj = new THREE.Mesh(new THREE.CylinderGeometry(p.r, p.r, p.h, 96, 1, !!p.open), mat);
    if (p.axis === 'x') obj.rotation.z = Math.PI / 2;
    if (p.axis === 'z') obj.rotation.x = Math.PI / 2;
  } else if (p.type === 'mirror') {
    const g = new THREE.PlaneGeometry(p.size[0], p.size[1]);
    obj = new Reflector(g, { textureWidth: 1024, textureHeight: 1024, color: 0xd8d8d8, clipBias: 0.003 });
    obj.rotation.x = -Math.PI / 2;
  }
  if (!obj) return null;
  obj.position.set(...p.at);
  obj.castShadow = p.type !== 'mirror';
  obj.receiveShadow = true;
  return obj;
}

// keep the texture's alpha (the die outline) but paint it plain lemon
function blankSide(mat) {
  mat.onBeforeCompile = (sh) => {
    sh.fragmentShader = sh.fragmentShader.replace('#include <map_fragment>',
      '#include <map_fragment>\n  diffuseColor.rgb = vec3(0.991, 0.846, 0.301);');
  };
  mat.customProgramCacheKey = () => 'blank-side';
}

export async function buildCard(spec, texBase) {
  const root = new THREE.Group();
  const stem = spec.svg.replace(/\.svg$/, '');
  const [tBoard, tClear] = await Promise.all([
    tex(`${texBase}/${stem}.webp`),
    spec.sheets.some((s) => s.stock === 'acetate') ? tex(`${texBase}/${stem}_clear.webp`) : null]);
  // the texture covers the SVG viewBox; textures.py writes its size in mm next to it
  const size = spec.size || await fetch(`${texBase}/${stem}.size.json`).then((r) => r.json()).catch(() => null);
  const img = tBoard && tBoard.image;
  const vbW = size ? size[0] : (img ? img.width / 4 : 100), vbH = size ? size[1] : (img ? img.height / 4 : 100);
  const uvFront = (x, y) => [x / vbW, 1 - y / vbH];

  const sheets = [];
  let maxStep = 0, flatX = 0;
  for (const sh of spec.sheets) {
    const acetate = sh.stock === 'acetate';
    const back = sh.back;
    const uvBack = back ? (x, y) => {
      const [fx, fy, fw] = back.front, [rx, ry] = back.region;
      return uvFront(rx + fw - (x - fx), ry + (y - fy));
    } : uvFront;
    // matte board: Lambert keeps the ink black and the lemon true (no specular sheen)
    // film ink is blended, not cut out, so fine grille bars average into a see-through tint
    const frontMat = new THREE.MeshLambertMaterial({ map: acetate ? tClear : tBoard, color: tBoard ? 0xffffff : LEMON,
      alphaTest: acetate ? 0.02 : 0.5, transparent: acetate, depthWrite: !acetate, side: acetate ? THREE.DoubleSide : THREE.BackSide });
    const backMat = new THREE.MeshLambertMaterial({ map: tBoard, color: 0xffffff, alphaTest: 0.5, side: THREE.FrontSide });
    if (!back) blankSide(backMat);            // unprinted side 2: lemon board with the same outline
    const depthMat = new THREE.MeshDepthMaterial({ depthPacking: THREE.RGBADepthPacking, map: acetate ? tClear : tBoard, alphaTest: 0.5 });
    const film = acetate ? new THREE.MeshPhysicalMaterial({ color: 0xffffff, transparent: true, opacity: 0.12, roughness: 0.05,
      metalness: 0, side: THREE.DoubleSide, depthWrite: false }) : null;

    const byId = {};
    for (const p of sh.panels) byId[p.id] = { spec: p, group: new THREE.Group(), kids: [] };
    let rootP = null;
    for (const p of sh.panels) {
      const node = byId[p.id];
      node.group.matrixAutoUpdate = false;
      const shape = shapeFrom(p.poly, p.holes);
      const gF = geometry(shape, uvFront);
      const mF = new THREE.Mesh(gF, frontMat);
      mF.castShadow = true; mF.receiveShadow = true; mF.customDepthMaterial = depthMat;
      node.group.add(mF);
      if (!acetate) {
        const mB = new THREE.Mesh(geometry(shape, uvBack), backMat);
        mB.receiveShadow = true;
        node.group.add(mB);
      } else {
        const mf = new THREE.Mesh(gF, film);
        mf.renderOrder = 2;
        node.group.add(mf);
      }
      if (p.parent) {
        const par = byId[p.parent];
        par.kids.push(node);
        par.group.add(node.group);
        // hinge axis oriented so that +angle is a valley seen from the printed side (-z)
        const a = new THREE.Vector3(p.hinge[1][0] - p.hinge[0][0], p.hinge[1][1] - p.hinge[0][1], 0).normalize();
        const c = new THREE.Vector2();
        p.poly.forEach(([x, y]) => c.add(new THREE.Vector2(x, y)));
        c.multiplyScalar(1 / p.poly.length);
        const d = new THREE.Vector3(c.x - p.hinge[0][0], c.y - p.hinge[0][1], 0);
        d.sub(a.clone().multiplyScalar(d.dot(a)));
        const turn = new THREE.Vector3().crossVectors(a, d);
        if (turn.z > 0) a.negate();                               // (a x d) must point to -z
        node.axis = a;
        node.pivot = new THREE.Vector3(p.hinge[0][0], p.hinge[0][1], 0);
        node.angle = THREE.MathUtils.degToRad(p.angle || 0);
        node.step = p.step || 1;
        maxStep = Math.max(maxStep, node.step);
      } else rootP = node;
    }
    const holder = new THREE.Group();
    holder.matrixAutoUpdate = false;
    holder.add(rootP.group);
    rootP.group.matrix.identity();
    root.add(holder);

    const pose = sh.pose || { origin: [0, 0], at: [0, 0, 0], u: [1, 0, 0], v: [0, 0, 1] };
    const final = poseMatrix(pose.origin, pose.at, pose.u, pose.v);
    // flat: printed side up on the table, laid out in a row
    const xs = sh.panels.flatMap((p) => p.poly.map((q) => q[0])), ys = sh.panels.flatMap((p) => p.poly.map((q) => q[1]));
    const minX = Math.min(...xs), maxX = Math.max(...xs), minY = Math.min(...ys), maxY = Math.max(...ys);
    const flatAt = sh.flat && sh.flat.at ? sh.flat.at : [flatX - minX, 0.2, -(minY + maxY) / 2];
    if (!(sh.flat && sh.flat.at)) flatX += (maxX - minX) + 40;
    const flat = poseMatrix([0, 0], flatAt, [1, 0, 0], [0, 0, 1]);
    const step = sh.step || 1;
    maxStep = Math.max(maxStep, step);
    sheets.push({ holder, final, flat, step, nodes: Object.values(byId), originPt: pose.origin });
  }
  // centre the flat layout on the origin
  const shift = -(flatX - 40) / 2;
  for (const s of sheets) s.flat.premultiply(new THREE.Matrix4().makeTranslation(shift, 0, 0));

  const props = new THREE.Group();
  props.userData.prop = true;
  for (const p of (spec.props || []).filter((q) => buildable(q))) props.add(buildProp(p));
  root.add(props);

  const tmpA = new THREE.Vector3(), tmpB = new THREE.Vector3(), qa = new THREE.Quaternion(), qb = new THREE.Quaternion(),
    sa = new THREE.Vector3(), sb = new THREE.Vector3();
  function update(t) {
    props.visible = t >= 0.999;
    for (const s of sheets) {
      const k = prog(t, s.step);
      s.flat.decompose(tmpA, qa, sa);
      s.final.decompose(tmpB, qb, sb);
      // move the pose origin point along a lifted arc
      const o = new THREE.Vector3(s.originPt[0], s.originPt[1], 0);
      const pa = o.clone().applyMatrix4(s.flat), pb = o.clone().applyMatrix4(s.final);
      const q = qa.clone().slerp(qb, k);
      const p = pa.lerp(pb, k);
      p.y += Math.sin(Math.PI * k) * 60;
      const m = new THREE.Matrix4().makeRotationFromQuaternion(q);
      const oo = o.clone().applyMatrix4(m);
      m.setPosition(p.sub(oo));
      s.holder.matrix.copy(m);
      for (const n of s.nodes) {
        if (!n.axis) continue;
        const ang = n.angle * prog(t, n.step);
        const M = new THREE.Matrix4().makeTranslation(n.pivot.x, n.pivot.y, 0)
          .multiply(new THREE.Matrix4().makeRotationAxis(n.axis, ang))
          .multiply(new THREE.Matrix4().makeTranslation(-n.pivot.x, -n.pivot.y, 0));
        n.group.matrix.copy(M);
      }
    }
    root.updateMatrixWorld(true);
  }
  update(maxStep);
  // a plate always sits in front of the assembled card with a 30 mm gap, so it never hides the name
  const cb = bounds(root, true);
  props.children.forEach((o, i) => {
    const p = (spec.props || []).filter((q) => buildable(q))[i];
    if (p && p.type === 'plate' && isFinite(cb.max.z)) o.position.z = Math.max(o.position.z, cb.max.z + (p.r || 135) + 30);
  });
  return { object: root, update, maxStep, steps: spec.steps || [] };
}

export function bounds(object, cardOnly) {
  const b = new THREE.Box3();
  const walk = (o) => {
    if (cardOnly && o.userData.prop) return;
    if (o.isMesh && !(o instanceof Reflector)) b.expandByObject(o);
    o.children.forEach(walk);
  };
  walk(object);
  return b;
}
